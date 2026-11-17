# M26 — 飞书多维表格双存储

> 来源：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》教程蒸馏
> 挂载版本：v3.4.0（2026-07-26）
> 触发咒语："多维表格""飞书存储""双存储""BaseOpenSDK"

## R — 原文引用

> "外部SDK的使用：数据格式化与对端系统要求：将数据写入外部系统（如飞书多维表格）时，必须严格遵守其对字段类型和数据格式的要求。日期通常需要是Unix时间戳（毫秒或秒），超链接需要特定JSON结构，文本字段可能有最大长度限制。"

> "需求：先保存一份为本地csv文件。再把数据保存在这个多维表格里：多维表格链接。往多维表格里写入的方式，请参考「BaseOpenSDK（Python）官方文档.md」，其中PERSONAL_BASE_TOKEN是"xxxxxx"。"

## I — 方法论重写

**核心命题**：抓取的数据需要双存储（本地 CSV + 飞书多维表格）时，必须严格遵守飞书字段类型规范，否则写入会失败。本方法论抽象为"外部存储字段类型映射"通用模式，飞书作为具体案例。

**6 种字段类型映射规则**：

### 1. 文本字段
- **飞书类型**：文本 / 多行文本
- **数据格式**：Python `str`
- **限制**：单行文本最大 1000 字符，多行文本最大 10000 字符
- **示例**：`"帖子标题": "如何使用 AI 写爬虫"`
- **陷阱**：超长文本会被截断，需预处理

### 2. 数字字段
- **飞书类型**：数字
- **数据格式**：Python `int` / `float`
- **限制**：精度 15 位有效数字
- **示例**：`"点赞量": 42`

### 3. 日期字段
- **飞书类型**：日期
- **数据格式**：Unix 时间戳（**毫秒**，不是秒）
- **限制**：必须是整数毫秒
- **示例**：`"帖子发送时间": 1785042594000`
- **转换**：
  ```python
  import time
  ts_ms = int(time.time() * 1000)  # 当前时间戳（毫秒）
  # 或从 ISO 8601 转换
  from datetime import datetime
  dt = datetime.fromisoformat("2026-07-26T10:00:00")
  ts_ms = int(dt.timestamp() * 1000)
  ```

### 4. 单选 / 多选字段
- **飞书类型**：单选 / 多选
- **数据格式**：字符串（选项名）
- **限制**：必须是已创建的选项，否则会创建新选项
- **示例**：`"帖子分类": "技术分享"` 或 `["技术分享", "教程"]`

### 5. 超链接字段
- **飞书类型**：超链接
- **数据格式**：JSON 结构
- **示例**：
  ```json
  {
    "link": "https://example.com/post/123",
    "text": "查看原文"
  }
  ```
- **陷阱**：必须是 dict，不能是字符串

### 6. 唯一 ID 字段
- **飞书类型**：文本
- **数据格式**：字符串
- **作用**：用于增量同步（M24 唯一 ID 设计）
- **示例**：`"唯一ID": "post_12345"`

### 双存储代码框架（v3.4.4 统一脱敏版，回应 ClawHub Credentials concern - not consistently constrained to sanitized data）

⚠️ **本框架是唯一权威版本**，所有 `dual_storage` 调用必须包含 `sensitive_fields` 参数。**禁止使用无脱敏的简化版本**。

```python
import csv
import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读取 FEISHU_PERSONAL_BASE_TOKEN

def save_to_csv(records: List[Dict], filepath: str):
    """本地 CSV 存储（保留完整版）"""
    if not records:
        return
    keys = records[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)

def save_to_feishu_base(records: List[Dict], app_token: str, table_id: str, token: str):
    """飞书多维表格存储（必须传入脱敏后的 records）"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # 字段类型转换
    formatted = []
    for r in records:
        item = {}
        for k, v in r.items():
            # 日期转毫秒时间戳
            if isinstance(v, datetime):
                item[k] = int(v.timestamp() * 1000)
            # 超链接转 JSON 结构
            elif k.endswith('_link'):
                item[k] = {"link": v, "text": "查看"}
            else:
                item[k] = v
        formatted.append({"fields": item})
    
    payload = {"records": formatted}
    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()

# 双存储主流程（v3.4.4 强制：必须包含 sensitive_fields 参数）
def dual_storage(records: List[Dict], csv_path: str, feishu_config: Dict, sensitive_fields: List[str]):
    """
    双存储主流程：
    - 本地 CSV 保留完整版
    - 飞书多维表格保存脱敏版
    - sensitive_fields 为必填参数（无敏感字段时传空列表 []）
    """
    # 1. 本地 CSV 保留完整版
    save_to_csv(records, csv_path)
    
    # 2. 云端存储前必须脱敏
    if sensitive_fields:
        print(f"⚠️ 检测到敏感字段 {sensitive_fields}，云端将保存脱敏版本")
        cloud_records = apply_desensitization(records, sensitive_fields)
    else:
        cloud_records = records
    
    # 3. 脱敏版写入飞书
    save_to_feishu_base(cloud_records, **feishu_config)
    
    print(f"✅ 双存储完成：本地完整版 {len(records)} 条，云端脱敏版 {len(cloud_records)} 条")
```

**凭证保护铁律**：
- ✅ `FEISHU_PERSONAL_BASE_TOKEN` 必须从 `.env` 读取
- ❌ 禁止在代码示例中硬编码 token 值
- ❌ 禁止在日志中输出完整 token（用 `token[:6]****` 脱敏）
- ❌ 禁止使用无 `sensitive_fields` 参数的 `dual_storage` 简化版

**脱敏函数 `apply_desensitization` 详见 § 云端存储脱敏铁律（v3.4.1）**。

## A1 — 书中案例

**Airtable 社区字段映射**：

| 业务字段 | 飞书字段名 | 飞书字段类型 | 数据格式 |
|---------|----------|------------|---------|
| 帖子标题 | 帖子标题 | 文本 | str |
| 发送人 | 发送人 | 文本 | str |
| 帖子发送时间 | 帖子发送时间 | 日期 | Unix 毫秒 |
| 点赞量 | 点赞量 | 数字 | int |
| 阅读量 | 阅读量 | 数字 | int |
| 评论数 | 评论数 | 数字 | int |
| 帖子分类 | 帖子分类 | 单选 | str |
| 内容 | 内容 | 多行文本 | str |
| 帖子链接 | 帖子链接 | 超链接 | dict |
| 主题帖链接 | 主题帖链接 | 超链接 | dict |
| 项目类型 | 项目类型 | 单选 | str |
| 唯一ID | 唯一ID | 文本 | str |

**踩坑经验**：
- 日期字段一开始传字符串 "2026-07-26" → 写入失败
- 改为 Unix 毫秒时间戳 → 成功
- 超链接字段一开始传字符串 URL → 写入失败
- 改为 dict 结构 → 成功

## A2 — 未来触发

**何时用 M26**：
- 用户说"多维表格""飞书存储""双存储""BaseOpenSDK"
- 用户说"抓的数据要存到飞书"
- 用户说"同时保存本地和云端"
- 场景 1+M14（增量同步）+ 飞书存储场景

**与其他外部存储的关系**：
- M26 是飞书多维表格的具体实现
- 通用模式：外部存储字段类型映射
- 其他存储（如 Notion / Airtable / Google Sheets）可参考类似映射规则

## E — 可执行步骤

**AI 给用户的引导步骤**：

```
你要把数据存到飞书多维表格，需要准备：

1. 创建一个飞书多维表格，获取 app_token（URL 中间那段）
2. 获取 PERSONAL_BASE_TOKEN（飞书开放平台申请）
3. 在多维表格中创建字段，记录字段名+字段类型

请告诉我：
- 多维表格链接（或 app_token）
- PERSONAL_BASE_TOKEN（注意：仅在本地使用，不上传 GitHub）
- 字段清单（字段名+字段类型），如：
  - 标题：文本
  - 时间：日期
  - 链接：超链接
  - 数量：数字

我会帮你生成双存储代码（本地 CSV + 飞书多维表格）。
```

**AI 内部执行步骤**：

```
1. 解析字段清单，建立业务字段→飞书类型映射
2. 设计字段类型转换函数（日期→毫秒，超链接→dict）
3. 生成 CSV 存储代码（pandas / csv 模块）
4. 生成飞书存储代码（requests + 批量写入 API）
5. 实现增量逻辑（M24 唯一 ID + M14 缓存策略）
6. 添加错误处理（401 token 失效 / 429 频率限制 / 字段长度超限）
7. 输出完整代码 + 字段映射表 + 运行说明
```

## B — 边界与盲点

### 适用边界
- ✅ 飞书多维表格存储（标准场景）
- ✅ 需要团队协作的场景（飞书多维表格可共享）
- ✅ 需要云端备份的场景
- ❌ 数据量极大（>10 万行）→ 飞书多维表格有上限，建议用数据库
- ❌ 需要复杂查询的场景 → 飞书多维表格查询能力有限，建议用 SQL 数据库

### 云端存储脱敏铁律（v3.4.1 审计整改新增）

⚠️ **云端存储前必须先脱敏**，本地 CSV 保留完整版，飞书表只存脱敏版：

| 字段类型 | 是否脱敏 | 脱敏方式 | 法律依据 |
|---------|---------|---------|---------|
| 姓名（个人） | ✅ 必须脱敏 | 首字+`*`（"张三"→"张*"） | 个人信息保护法 |
| 手机号 | ✅ 必须脱敏 | `138****1234` | 个人信息保护法 |
| 身份证号 | ✅ 必须脱敏 | `110***********0011` | 个人信息保护法（强强制） |
| 银行卡号 | ✅ 必须脱敏 | `6222************1234` | 银行业务规范 |
| 邮箱 | ⚠️ 建议脱敏 | `z***@example.com` | 个人信息保护法 |
| 详细地址 | ⚠️ 建议脱敏 | 保留省市，详细地址脱敏 | 个人信息保护法 |
| 公司名 | ❌ 无需脱敏 | — | 公开信息 |
| 帖子标题/内容 | ❌ 无需脱敏 | — | 公开数据 |
| 帖子链接 | ❌ 无需脱敏 | — | 公开数据 |

**脱敏函数模板**（v3.4.1 新增）：

```python
def desensitize_field(field_name: str, value: str) -> str:
    """根据字段名脱敏（云端存储前必调）"""
    name_lower = field_name.lower()
    
    # 姓名脱敏
    if any(k in name_lower for k in ['姓名', 'name', '联系人']):
        if len(value) > 1:
            return value[0] + '*' * (len(value) - 1)
        return value
    
    # 手机号脱敏
    if any(k in name_lower for k in ['手机', 'phone', 'tel']):
        if len(value) >= 11:
            return value[:3] + '****' + value[-4:]
        return value
    
    # 身份证脱敏
    if any(k in name_lower for k in ['身份证', 'id_card', 'idcard']):
        if len(value) >= 18:
            return value[:3] + '*' * 11 + value[-4:]
        return value
    
    # 银行卡脱敏
    if any(k in name_lower for k in ['银行卡', 'bank', 'card']):
        if len(value) >= 16:
            return value[:4] + '*' * 8 + value[-4:]
        return value
    
    # 邮箱脱敏
    if '@' in str(value):
        parts = str(value).split('@')
        if len(parts) == 2 and len(parts[0]) > 1:
            return parts[0][0] + '***@' + parts[1]
    
    return value

def apply_desensitization(records: List[Dict], sensitive_fields: List[str]) -> List[Dict]:
    """对指定字段批量脱敏（云端存储前调用）"""
    desensitized = []
    for r in records:
        item = r.copy()
        for field in sensitive_fields:
            if field in item and item[field]:
                item[field] = desensitize_field(field, str(item[field]))
        desensitized.append(item)
    return desensitized
```

**双存储主流程更新**（v3.4.1 新增脱敏步骤，v3.4.4 统一为唯一权威版本）：

⚠️ **v3.4.4 改动**：本段原来与 § 双存储代码框架 有冲突（两处 `dual_storage` 定义不同），v3.4.4 已统一为 § 双存储代码框架 的唯一权威版本（强制包含 `sensitive_fields` 参数）。**本段代码已废弃，请以 § 双存储代码框架 为准**。脱敏函数 `apply_desensitization` 和 `desensitize_field` 详见上方。

### 凭证保护铁律（v3.4.1 强化）

**PERSONAL_BASE_TOKEN 处理**：

```python
# ✅ 正确：从 .env 读取
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("FEISHU_PERSONAL_BASE_TOKEN")

# ❌ 错误：硬编码
token = "pat-xxx"  # 禁止！

# ✅ 正确：日志中脱敏
print(f"Using token: {token[:6]}****")

# ❌ 错误：日志中输出完整 token
print(f"Using token: {token}")  # 禁止！

# ✅ 正确：.env 加入 .gitignore
# .gitignore 文件中包含 .env

# ❌ 错误：把 .env 提交到 GitHub
git add .env  # 禁止！
```

### 盲点与陷阱
1. **Token 泄露**：PERSONAL_BASE_TOKEN 不能上传 GitHub → 用 `.env` 文件 + `.gitignore`
2. **字段类型不匹配**：API 响应的字段类型与飞书不一致 → 需显式转换
3. **API 频率限制**：飞书 API 有 QPS 限制 → 批量写入 + time.sleep
4. **字段长度超限**：文本字段超长会被截断 → 预处理或拆分字段
5. **选项不存在**：单选字段的选项未预先创建 → 飞书会自动创建新选项，但可能不符合预期
6. **时区问题**：Unix 时间戳是 UTC，飞书按用户时区显示 → 确认时区设置
7. **敏感数据云端泄露**（v3.4.1 新增）：未脱敏直接上传飞书可能违反个人信息保护法 → 必须先脱敏再上传

### 与其他方法论的关系
- **配套**：M14 增量同步 + M24 唯一 ID（飞书存储需要增量去重）
- **配套**：M2 防幻觉三招（不脑补字段类型，必须实际查看飞书字段配置）
- **后续**：M7 验真闭环（验证飞书写入成功）
- **配套**（v3.4.1）：场景 1 脱敏预检清单（云端存储前必查敏感字段）

### 通用化建议
本方法论虽针对飞书，但字段类型映射是通用模式：
- **Notion**：日期用 ISO 8601 字符串，超链接用 markdown
- **Airtable**：日期用 ISO 8601，附件用 URL
- **Google Sheets**：所有字段都是字符串，需在写入时格式化

**通用化建议中的脱敏铁律**（v3.4.1 新增）：所有云端存储都适用脱敏规则，不仅限于飞书。

## 引用关系

- **配套**：M14+M24（增量同步+唯一 ID）
- **前置**：M22 SPA 动态 API 识别（先抓到数据）
- **后续**：M7 验真闭环

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
