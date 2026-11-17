# 飞书多维表格存储模板（v3.4.0）

> 场景 1 交付物模板（v3.4.0 新增，源自 TRAE 社区爬虫教程）
> 配套方法论：M26 飞书多维表格双存储 + M14 增量同步 + M24 增量唯一 ID
> 用途：用户需要把抓取的数据双存储（本地 CSV + 飞书多维表格）时，AI 引导完成字段映射+代码生成

## 使用说明

**AI 行为**：
- 用户提到"飞书多维表格""双存储""BaseOpenSDK" → 主动展示本模板
- 用户完成字段映射后 → 生成双存储代码

**用户行为**：
- 在飞书创建多维表格，获取 app_token 和 PERSONAL_BASE_TOKEN
- 在多维表格中创建字段，记录字段名+类型
- 把字段清单告诉 AI

---

## Step 1：准备飞书多维表格

### 用户操作
1. 在飞书中创建一个新的多维表格（Bitable）
2. 从 URL 获取 `app_token`（URL 中间那段）
3. 在 [飞书开放平台](https://open.feishu.cn/) 申请 `PERSONAL_BASE_TOKEN`
4. 在多维表格中创建数据表，获取 `table_id`
5. 在数据表中创建字段（按业务需求）

### 记录

```
多维表格链接：[如 https://xxx.feishu.cn/base/BascXXXXXXXX]
app_token：[如 BascXXXXXXXX]
table_id：[如 tblXXXXXXXX]
PERSONAL_BASE_TOKEN：[用户本地保存，不上传 GitHub]
```

⚠️ **安全提示**：`PERSONAL_BASE_TOKEN` 是敏感凭证，必须存到 `.env` 文件，并在 `.gitignore` 中排除。

---

## Step 2：设计字段映射表

### 飞书字段类型映射规则

| 业务字段 | 飞书字段名 | 飞书字段类型 | Python 数据格式 | 转换逻辑 |
|---------|----------|------------|---------------|---------|
| 标题 | 帖子标题 | 文本 | str | 直接用 |
| 作者 | 发送人 | 文本 | str | 直接用 |
| 时间 | 帖子发送时间 | 日期 | int (Unix 毫秒) | `int(dt.timestamp() * 1000)` |
| 点赞 | 点赞量 | 数字 | int | 直接用 |
| 链接 | 帖子链接 | 超链接 | dict | `{"link": url, "text": "查看"}` |
| 分类 | 帖子分类 | 单选 | str | 必须是已创建的选项 |
| 标签 | 标签 | 多选 | list[str] | 必须是已创建的选项 |
| 唯一 ID | 唯一ID | 文本 | str | 用于增量同步去重 |

### 字段长度限制

| 飞书类型 | 最大长度 | 处理建议 |
|---------|---------|---------|
| 单行文本 | 1000 字符 | 超长截断或拆分 |
| 多行文本 | 10000 字符 | 适合长内容 |
| 数字 | 15 位有效数字 | 超大数用字符串 |
| 日期 | 1970-2038 | Unix 毫秒时间戳 |

---

## Step 3：生成双存储代码

### 代码框架

```python
import csv
import os
import time
import requests
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读取 PERSONAL_BASE_TOKEN

# ========== 配置 ==========
FEISHU_APP_TOKEN = "BascXXXXXXXX"  # 替换为实际值
FEISHU_TABLE_ID = "tblXXXXXXXX"     # 替换为实际值
FEISHU_TOKEN = os.getenv("PERSONAL_BASE_TOKEN")
CSV_PATH = "data.csv"

# ========== 字段类型转换 ==========
def format_for_feishu(record: Dict) -> Dict:
    """把业务数据转为飞书多维表格格式"""
    formatted = {}
    for k, v in record.items():
        # 日期转 Unix 毫秒
        if isinstance(v, datetime):
            formatted[k] = int(v.timestamp() * 1000)
        # 超链接转 dict
        elif k.endswith("_link") or k in ("帖子链接", "主题帖链接"):
            formatted[k] = {"link": v, "text": "查看原文"}
        # 其他字段直接用
        else:
            formatted[k] = v
    return formatted

# ========== CSV 存储 ==========
def save_to_csv(records: List[Dict], filepath: str = CSV_PATH):
    """本地 CSV 存储"""
    if not records:
        print("无数据可写入 CSV")
        return
    keys = list(records[0].keys())
    # 追加模式：文件已存在则不写表头
    write_header = not os.path.exists(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if write_header:
            writer.writeheader()
        writer.writerows(records)
    print(f"✅ CSV 写入完成：{len(records)} 条 → {filepath}")

# ========== 飞书多维表格存储 ==========
def save_to_feishu_base(records: List[Dict], app_token: str, table_id: str, token: str):
    """飞书多维表格批量写入"""
    if not records:
        print("无数据可写入飞书")
        return
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 转换为飞书格式
    formatted_records = [{"fields": format_for_feishu(r)} for r in records]
    
    # 批量写入（每批最多 500 条）
    batch_size = 500
    for i in range(0, len(formatted_records), batch_size):
        batch = formatted_records[i:i + batch_size]
        payload = {"records": batch}
        resp = requests.post(url, headers=headers, json=payload)
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get("code") == 0:
                print(f"✅ 飞书写入完成：批次 {i//batch_size + 1}，{len(batch)} 条")
            else:
                print(f"❌ 飞书 API 错误：{result.get('msg')}")
        else:
            print(f"❌ HTTP 错误：{resp.status_code}")
        
        time.sleep(0.5)  # 避免 QPS 限制

# ========== 双存储主流程 ==========
def dual_storage(records: List[Dict]):
    """本地 CSV + 飞书多维表格双存储"""
    print(f"开始双存储 {len(records)} 条数据...")
    save_to_csv(records)
    save_to_feishu_base(records, FEISHU_APP_TOKEN, FEISHU_TABLE_ID, FEISHU_TOKEN)
    print("✅ 双存储完成")

# ========== 增量同步（可选）==========
def load_existing_ids(cache_path: str = "ids_cache.json") -> set:
    """加载已抓取的 ID 缓存"""
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_ids_cache(ids: set, cache_path: str = "ids_cache.json"):
    """保存 ID 缓存"""
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(list(ids), f, ensure_ascii=False)

def incremental_storage(new_records: List[Dict], id_field: str = "唯一ID"):
    """增量存储：只存新数据"""
    existing_ids = load_existing_ids()
    new_data = [r for r in new_records if r.get(id_field) not in existing_ids]
    
    if not new_data:
        print("无新数据")
        return
    
    dual_storage(new_data)
    
    # 更新缓存
    new_ids = {r[id_field] for r in new_data}
    save_ids_cache(existing_ids | new_ids)
    print(f"✅ 增量完成：新增 {len(new_data)} 条，总缓存 {len(existing_ids) + len(new_ids)} 条")

# ========== 主入口 ==========
if __name__ == "__main__":
    # 示例：抓取 5 条测试数据
    test_data = [
        {
            "帖子标题": "测试标题 1",
            "发送人": "张三",
            "帖子发送时间": datetime.now(),
            "点赞量": 10,
            "帖子链接": "https://example.com/1",
            "帖子分类": "技术",
            "唯一ID": "test_001"
        },
        # ... 更多数据
    ]
    
    # 首次全量
    dual_storage(test_data)
    
    # 后续增量
    # incremental_storage(test_data, id_field="唯一ID")
```

---

## Step 4：测试与调试

### 测试流程

1. **先抓 5 条测试**：教程原话"测试的状态获取 5 条数据"
2. **验证 CSV**：打开 CSV 确认字段完整、编码正确（utf-8-sig）
3. **验证飞书**：打开多维表格确认数据已写入
4. **字段类型验证**：
   - 日期字段显示为日期格式（非数字）
   - 超链接字段可点击（非纯文本）
   - 单选字段显示为标签（非纯文本）
5. **全量抓取**：测试通过后放开数量限制

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 401 Unauthorized | Token 失效或错误 | 检查 PERSONAL_BASE_TOKEN 是否正确 |
| 400 Bad Request | 字段类型不匹配 | 检查字段映射，特别是日期和超链接 |
| 字段写入为空 | 字段名拼写错误 | 对比飞书实际字段名 |
| CSV 中文乱码 | 编码问题 | 用 utf-8-sig 而非 utf-8 |
| 数据重复 | 增量逻辑未生效 | 检查 ID 缓存是否正确加载 |

---

## 安全规范

1. **Token 保护**：
   - `PERSONAL_BASE_TOKEN` 必须存到 `.env` 文件
   - `.env` 必须加入 `.gitignore`
   - 代码中用 `os.getenv()` 读取，不硬编码

2. **数据脱敏**：
   - 如抓取的数据含敏感信息（如邮箱、手机），写入前做脱敏
   - 敏感字段单独加密存储

3. **访问控制**：
   - 多维表格权限设置（仅授权人可见）
   - 定期轮换 Token

---

## 与其他模板的关系

- 前置：[website-analysis-script-template.md](website-analysis-script-template.md)（先分析网站，再设计存储）
- 配套：[scenario-1-prompt-template.md](scenario-1-prompt-template.md)（生成最终 Prompt）
- 调试：[crawler-debug-experience.md](crawler-debug-experience.md)（如遇问题参考）

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
