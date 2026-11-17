---
name: account-pool-manager
description: "自媒体多账户池管理，支持按部门（自营/社交部/电商部/外包客户）分组管理账号、Cookie健康检查、智能轮换发布。 触发词：账号池/多账号管理/部门账号/账号轮换/Cookie检查/账号健康 不触发：封号换号（用account-manager）/内容发布（用content-publisher）"
version: 1.1.0
user-invocable: true
tools: [read, write, exec, memory_search]
dependencies: []
metadata:
  layer: plugin
  priority: P0
  category: ecom-ops
  openclaw:
    emoji: "👥"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      config: ["mcp.servers.fishclaw-mcp"]
      env: ["ACCOUNT_POOL_DIR"]
---

# Account Pool Manager - 自媒体多账户池管理

**版本**: v1.1  
**创建日期**: 2026-04-26  
**状态**: 🟢 已完成  
**优先级**: P0（自媒体业务核心基础设施）  
**文档字数**: ≥2000 字

---

## 一、业务背景

### 1.1 为什么需要统一的多账户池？

JueJin 自媒体内容营销有 **4 种业务对象**，每种需要不同的账号：

| 业务对象 | 账号归属 | 示例 | 发布内容策略 |
|:---------|:---------|:-----|:-------------|
| **1. 自媒体自营** | 自媒体部门 | `self_media_001` | 自主找热点创作，盈利归自媒体部门 |
| **2. 社交部代运营** | 社交部员工 | `social_employee_001` | 情感/美女热点，引流到社交部 |
| **3. 电商部代运营** | 电商部员工 | `ecommerce_employee_001` | 商品相关热点，带货推广 |
| **4. 外包客户** | 客户（如培训机构） | `client_xxx` | 客户需求定制，服务费归自媒体部门 |

**核心问题**：发布内容时，如何自动选择正确的账号？如何管理所有账号的 Cookie？如何健康检查？

### 1.2 与 account-manager 的区别

| 能力 | account-manager（已有） | account-pool-manager（新建） |
|:-----|:-----------------------|:----------------------------|
| **核心功能** | 封号后换号 | 多账户池管理+Cookie健康检查 |
| **使用场景** | 微信/抖音封号后切换到备用号 | 自媒体发布时选择对应部门账号 |
| **账号类型** | 同一员工的不同账号（wx_001 → wx_002） | 不同部门/客户的多个账号 |
| **管理粒度** | 员工级（一个员工一套备用号） | 部门级（多部门共享账号池） |
| **触发条件** | 账号被封/被限制 | 发布内容时需要选择发布账号 |
| **Cookie管理** | ❌ 不支持 | ✅ Cookie健康检查+过期提醒 |
| **智能轮换** | ❌ 不支持 | ✅ 多账号发布时自动轮换 |
| **业务对象** | 社交套利（员工个人号） | 自媒体内容营销（4种业务对象） |

**边界原则**：
- 当账号被封/被限制时 → 使用 **account-manager** 切换备用号
- 当发布内容需要选择发布账号时 → 使用 **account-pool-manager** 获取账号
- 两者功能互补，互不替代，可以同时存在

**结论**：两者功能互补，互不替代。

---

## 二、架构设计

### 2.1 目录结构

```
data/content/accounts/
├── pool_config.json                    # 账户池全局配置
├── self_media/                         # 自媒体自营账号
│   ├── account_001.json
│   └── account_002.json
├── social_dept/                        # 社交部账号
├── ecommerce_dept/                     # 电商部账号
└── clients/                            # 外包客户账号

data/content/cookies/                # Cookie 存储（统一管理）
├── douyin_self_media_001.json          # 格式：{platform}_{account_id}.json
└── ...

data/content/health/                 # 健康检查记录
└── health_report.json                  # 最新健康报告
```

### 2.2 账号配置文件格式

```json
{
  "account_id": "self_media_001",
  "department": "self_media",
  "platforms": {
    "douyin": {
      "cookie_path": "data/content/cookies/douyin_self_media_001.json",
      "status": "active",
      "last_publish": "2026-04-26T10:00:00Z",
      "publish_count_today": 3,
      "daily_limit": 10
    }
  },
  "created_at": "2026-04-01T00:00:00Z",
  "notes": "自媒体主力账号"
}
```

---

## 三、工作流程

### 3.1 主流程：获取发布账号

```
1. 接收发布请求
   └── 输入：{business_type: "self_media", platforms: ["douyin", "xiaohongshu"]}

2. 查询账户池 → 按部门筛选 → 过滤可用账号 → 轮换选择

3. 检查 Cookie 健康 → 返回账号信息和 cookie 路径

4. 输出 → 供 content-publisher 调用 sau 进行发布
```

### 3.2 Cookie 健康检查流程

```
1. Cron 每日 08:00 触发 → exec 调用 cookie_health.py check_all
2. 扫描所有 Cookie 文件 → 检查文件/大小/时间
3. 生成健康报告 → healthy(≤7天) / warning(7-25天) / expired(>25天)
4. 推送通知 → expired立即通知 / warning每日提醒
```

---

## 四、输入输出格式

### 4.1 获取发布账号

**输入**: `{"action": "get_publish_account", "business_type": "self_media", "platforms": ["douyin", "xiaohongshu"]}`

**输出**: `{"success": true, "data": {"account_id": "self_media_001", "department": "self_media", "platforms": {...}}, "error": null, "code": "AP-SUCCESS-01"}`

### 4.2 Cookie 健康检查

**输入**: `{"action": "check_cookie_health"}`

**输出**: `{"success": true, "data": {"total": 10, "healthy": 7, "warning": 2, "expired": 1, "details": [...]}, "error": null, "code": "AP-SUCCESS-02"}`

---

## 五、异常处理

| 异常场景 | 错误码 | 处理方案 |
|:---------|:------|:---------|
| 账户池目录不存在 | AP-ERR-02 | 自动创建默认目录结构 |
| 无可用账号 | AP-ERR-03 | 返回错误，提示添加账号 |
| Cookie 已过期 | AP-ERR-07 | 标记并推送通知 |
| 业务类型无效 | AP-ERR-01 | 返回支持的业务类型列表 |
| 账号文件损坏 | AP-ERR-UNKNOWN | 备份损坏文件，尝试恢复 |

---

## 六、与 content-publisher 集成

### 6.1 集成流程

```
content-publisher 收到发布请求
    ↓
调用 account-pool-manager 获取账号和 cookie 路径
    ↓
调用 sau 进行真实发布
    ↓
记录发布结果到账号历史
```

### 6.2 content-publisher 修改点

在 `execute_real_publish()` 中：
1. 调用 `account_manager.py get_publish_account` 获取账号
2. 使用返回的 cookie_path 构建 sau CLI 命令
3. 发布成功后更新账号的 publish_count_today

---

## 七、使用示例

### 输入格式

```json
{
  "action": "get_publish_account",
  "business_type": "self_media",
  "platforms": ["douyin", "xiaohongshu"]
}
```

支持action: get_publish_account(获取发布账号)/check_cookie_health(Cookie健康检查)/rotate_account(轮换账号)/list_pool(列出账号池)/add_account(添加账号)


## 示例1：获取发布账号

```bash
python "skills/account-pool-manager/scripts/account_manager.py" get_publish_account self_media "douyin,xiaohongshu"
```

预期输出：
```json
{"success": true, "data": {"account_id": "self_media_001", "department": "self_media",
  "platforms": {"douyin": {"cookie_path": "data/content/cookies/douyin_self_media_001.json",
    "status": "active", "publish_count_today": 3, "daily_limit": 10}}},
  "error": null, "code": "AP-SUCCESS-01"}
```

### 示例2：注册新账号

```bash
python "skills/account-pool-manager/scripts/account_manager.py" register_account '{"account_id": "self_media_003", "department": "self_media", "platforms": {"douyin": {}, "xiaohongshu": {}}, "daily_limit": 10, "notes": "新注册"}'
```

### 示例3：Cookie健康检查

```bash
python "skills/account-pool-manager/scripts/cookie_health.py" check_all
```

预期输出：
```json
{"success": true, "data": {"total": 5, "healthy": 4, "warning": 1, "expired": 0,
  "details": [{"cookie_file": "douyin_self_media_001.json", "status": "healthy", ...}]},
  "error": null, "code": "AP-SUCCESS-02"}
```

### 示例4：查询健康报告

```bash
python "skills/account-pool-manager/scripts/report_manager.py" get_report
```

### 示例5：与 content-publisher 集成

```bash
# content-publisher 内部自动调用 account-pool-manager 获取账号
python "skills/content-publisher/scripts/content_publisher.py" --action publish_auto --content_id video_001 --platforms douyin,xiaohongshu --business_type self_media
```

---

## 八、风控安全规则（来源: 01手册§十10.1）

| 操作 | 安全频率 | 超限后果 |
|:-----|:---------|:---------|
| 多账号发布间隔 | ≥17分钟 | 关联封号 |
| 单账号发布间隔 | 5-10秒 | 限流 |
| 回复间隔 | 1.0-2.0秒 | 标记机器人 |
| 调价频率 | ≤3次/日/商品 | 降权 |
| 擦亮商品 | 每日1次/商品 | 触发验证 |

---

## 九、相关文件

- **SKILL.md**: `skills/account-pool-manager/SKILL.md`
- **exec 脚本**:
  - `skills/account-pool-manager/scripts/account_manager.py` (账号注册/查询/轮换)
  - `skills/account-pool-manager/scripts/cookie_health.py` (Cookie健康检查)
  - `skills/account-pool-manager/scripts/report_manager.py` (健康报告管理)
- **数据目录**: `data/content/accounts/`、`data/content/cookies/`、`data/content/health/`
- **升级方案**: `docs/design/电商营销能力升级方案.md`

---

## 变更历史

| 版本 | 日期 | 作者 | 变更说明 |
|:-----|:-----|:-----|:---------|
| v1.0 | 2026-04-26 | AI Agent | 初始版本，定义统一多账户池架构 |
| v1.1 | 2026-04-26 | AI Agent | 拆分cookie_manager→cookie_health+report_manager，补充使用示例 |
