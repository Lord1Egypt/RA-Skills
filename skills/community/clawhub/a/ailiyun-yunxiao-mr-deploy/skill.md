---
name: 阿里云云效创建MR+发布+通知
description: 支持自定义分支/代码库创建MR、查询MR合并状态、按代码库+环境关键字触发发布流水线，并自动推送通知。支持自然语言输入，由大模型自动识别意图。
---

## 功能说明
- **创建 MR**：大模型自动识别代码库名/源分支/目标分支，代码库名支持精确匹配和模糊匹配
- **查询 MR 状态**：支持按代码库名 + MR 编号查询合并状态、审核情况、分支信息
- **触发发布**：支持按代码库名 + 环境关键字（如 beta、dev）搜索流水线，多条匹配时列出供用户选择；也可直接指定流水线ID
- **通知**：所有操作结果自动推送到指定url,包括办公软件（企微，钉钉等）的各种机器人

## 自然语言示例

### 创建 MR
- `帮我把 feature/login 合到 dev`
- `从 release 创建到 main 的合并请求`
- `在 erp-ops 仓库创建 fix_xxx 到 beta 的 MR`
- `把 260309_espu_inventory 分支提到 beta`
- `新建一个 PR 从 hotfix/xxx 到 master`

### 查询 MR 状态
- `查询 erp-ops #425 的合并状态`
- `erp-ops-api 第152号MR合并了吗`
- `帮我看一下 unitepos-sale MR #307 有没有通过`
- `#306 MR 状态怎么样了`

### 触发发布
- `发布 erp-ops 的 beta 环境`
- `触发 erp-ops-api 的 dev 流水线`
- `部署 unitepos-sale beta`
- `线上发布`（使用默认流水线）
- `触发流水线 4297451`（直接指定ID）

## 配置说明

### 敏感配置（推荐通过环境变量设置）

以下三项优先从系统环境变量读取，未设置时回退到脚本内默认值：

| 环境变量 | 说明 |
|---|---|
| `YUNXIAO_PERSONAL_TOKEN` | 云效个人访问令牌 |
| `YUNXIAO_ORGANIZATION_ID` | 企业/组织 ID |
| `WECOM_WEBHOOK_URL` | 企业微信机器人 Webhook 完整地址 |

**Windows 设置环境变量示例（PowerShell）：**
```powershell
[System.Environment]::SetEnvironmentVariable("YUNXIAO_PERSONAL_TOKEN", "你的令牌", "User")
[System.Environment]::SetEnvironmentVariable("YUNXIAO_ORGANIZATION_ID", "你的企业ID", "User")
[System.Environment]::SetEnvironmentVariable("WECOM_WEBHOOK_URL", "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "User")
```

**macOS / Linux 设置示例（写入 ~/.zshrc 或 ~/.bashrc）：**
```bash
export YUNXIAO_PERSONAL_TOKEN="你的令牌"
export YUNXIAO_ORGANIZATION_ID="你的企业ID"
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
```

### 其他配置（在脚本 `mr_deploy_old_full.py` 的 CONFIG 中填写）

- `DEFAULT_REPO_ID`：未指定代码库时的默认代码库ID
- `DEFAULT_SOURCE`：未指定时的默认源分支
- `DEFAULT_TARGET`：未指定时的默认目标分支
- `DEFAULT_FLOW_ID`：未指定时的默认流水线ID（发布场景无关键字时使用）

## 工作原理
用户输入 → 大模型解析意图（action / repo_name / source_branch / target_branch / mr_id / flow_id / env_keyword）
- `create_mr`：按仓库名查询ID → 调用创建接口 → 企微通知
- `query_mr`：按仓库名查询ID → 查询MR详情 → 返回状态+审核信息
- `deploy`：有 flow_id 则直接触发；否则按 repo_name + env_keyword 搜索流水线（名称匹配规则：`{repo_name}_{env_keyword}`）→ 唯一匹配则触发，多条则列出供确认

## 踩坑经验

（以下由 AI 在实际使用中自动积累，请勿手动删除）
