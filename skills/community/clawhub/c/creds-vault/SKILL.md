---
name: token-manager
description: "令牌与账号密钥管理中心 v2.1 — 集中管理所有第三方 API 令牌、账号密码、SSH 密钥。支持分类管理、过期提醒、密码生成、加密备份、使用统计、安全审计日志、防暴力破解、安全删除。"
metadata:
  openclaw:
    emoji: "🔐"
---

# token-manager v2.1

令牌与账号密钥管理中心 v2.1。集中存储和管理所有敏感凭证，强化安全防护。

## 核心功能

| 功能 | 说明 |
|------|------|
| 自动截获 | 对话中出现凭证时 AI 自动**检测**并提示确认，确认后才保存，不会静默持久化 |
| 分类管理 | 按平台分类（社交媒体/云服务/开发工具/营销平台/其他） |
| 过期提醒 | 记录 token 有效期，快过期自动提示 |
| 密码生成 | 生成安全随机密码（使用 `secrets` 加密随机数） |
| 加密备份 | AES-256-GCM + PBKDF2，防暴力破解（3次错锁1小时） |
| 使用统计 | 记录每个 token 被读取的次数和时间 |
| 安全审计 | 所有操作（增/查/删/备份）全部记录到 `secrets.audit.log` |
| 安全删除 | 删除 entry 前覆写所有字段值为不可读字符，再从 JSON 中移除 |
| 凭证值上限 | 单个 value 最大 2048 字符，防止内存耗尽 |

## 依赖声明

- **Python 3**：运行所有脚本
- **pycryptodome**（可选）：仅在使用 `backup.py` 加密备份时需要。安装方式：`pip install pycryptodome`。若未安装，备份功能会提示安装

## 数据结构

```json
{
  "categories": ["social", "cloud", "dev", "marketing", "other"],
  "entries": {
    "wechat": {
      "name": "微信公众号",
      "category": "social",
      "fields": {
        "appid": "wxd9f577d56948e564",
        "appsecret": "44b92c25b849a51226c224c4188ffd77"
      },
      "expire_at": null,
      "note": "luisclaw",
      "created_at": "2026-04-15",
      "read_count": 12,
      "last_read": "2026-04-15T20:00:00"
    }
  }
}
```

## 脚本说明

### add.py — 添加令牌

```bash
python add.py <key> <name> <field=value>... [--category social|cloud|dev|marketing|other] [--expire YYYY-MM-DD]

# 示例
python add.py wechat "微信公众号" appid=YOUR_APPID appsecret=YOUR_APPSECRET --category social
python add.py openai "OpenAI API" api_key=sk-xxx --category dev
python add.py aws "AWS" access_key=xxx secret_key=xxx --category cloud
```

### list.py — 列出所有令牌（脱敏）

```bash
python list.py                # 列出所有（脱敏）
python list.py --raw          # 列出所有（完整值，仅本地查看）
python list.py --expire       # 列出 7 天内即将过期
python list.py --expire --days 30   # 列出 30 天内过期
python list.py --category social    # 按分类筛选
```

### get.py — 获取令牌

```bash
python get.py <key> [field]
python get.py wechat appid        # 返回完整值（会记录读取次数）
python get.py wechat              # 显示完整 entry 信息
```

### remove.py — 删除令牌

```bash
python remove.py <key>
```

### genpass.py — 密码生成器

```bash
python genpass.py              # 默认 24 位，字母+数字+符号
python genpass.py 16           # 指定长度
python genpass.py 32 --no-symbols   # 无符号，纯字母数字
python genpass.py 20 --numeric     # 仅数字
python genpass.py 16 --save github  # 生成并保存到 github 条目
```

### backup.py — 加密备份

```bash
python backup.py                 # 加密导出到 secrets.json.enc
python backup.py --import backup.json.enc  # 解密导入（需输入密码）
python backup.py --check         # 检查备份文件完整性
```

> ⚠️ 需要 `pip install pycryptodome`。加密算法：AES-256-GCM + PBKDF2。

### stats.py — 使用统计

```bash
python stats.py              # 显示所有 token 使用统计
python stats.py --top 5       # 显示读取次数最多的 5 个
python stats.py <key>        # 显示单个 token 详情
```

### migrate.py — 格式迁移

```bash
# 一次性迁移旧格式到 v2 格式
python migrate.py
```

### autocapture.py — 自动截获（AI 对话中自动调用）

当 AI 在对话中检测到凭证信息时，自动解析并保存到 `secrets.json`。

**自动识别的凭证类型：**
| 类型 | 匹配模式 | 自动分类 |
|------|---------|---------|
| `appid` / `appsecret` | `AppID: xxx`, `appsecret=xxx` | social（微信） |
| `api_key` | `API_KEY=xxx`, `OPENAI_API_KEY=xxx` | dev |
| `token` | `token: xxx`, `ghp_xxx`（20位+） | dev |
| `access_key` / `secret_key` | AWS 风格密钥 | cloud |
| `password` | `password=xxx` | other |

```bash
# 检测凭证（仅预览，不保存）
python autocapture.py --text "AppID: wxd9f577d56948e564" --context "微信公众号"

# 检测并确认保存
python autocapture.py --text "AppID: wxd9f577d56948e564" --save

# 查看已保存的凭证
python autocapture.py --list
```

> **隐私说明**：自动截获**仅检测不保存**，发现凭证后显示预览并提示「确认」后才写入 `secrets.json`。你随时可以拒绝。

## 安全说明

- 文件权限 600（仅当前用户可读写）
- 读取时自动脱敏：`44b92c25b849a51226c224c4188ffd77` → `44b92...fd77`
- 加密备份：AES-256-GCM + PBKDF2，密码长度至少8位
- **防暴力破解**：备份密码连续3次错误，锁定1小时
- **安全删除**：文件删除前覆写3次随机数据
- **审计日志**：所有操作记录到 `secrets.audit.log`，仅追加不可修改
- **输入消毒**：所有 key 只允许 `[a-zA-Z0-9_\-]`，长度≤64，防止 injection
- 不要将 `secrets.json` 提交到 Git

## 文件结构

```
token-manager/
├── _meta.json
├── SKILL.md
└── scripts/
    ├── add.py        # 添加令牌（审计日志）
    ├── list.py       # 列举令牌（脱敏）
    ├── get.py        # 获取令牌（审计日志）
    ├── remove.py     # 安全删除（覆写3次）
    ├── genpass.py    # 密码生成器（加密随机）
    ├── backup.py     # 加密备份（防暴力破解）
    ├── stats.py      # 使用统计
    ├── migrate.py    # 格式迁移
    ├── autocapture.py # 对话式自动截获（审计日志）
    └── audit.py      # 审计日志查看器
```
