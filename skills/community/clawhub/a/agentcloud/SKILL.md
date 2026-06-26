---
name: agentcloud
description: AgentCloud（AI Agent 云存储）— 一键注册 Agent，上传/下载文件，创建分享链接，查询用量。支持 Hermes Agent 和 OpenClaw 用户直接使用。
tags:
  - file-storage
  - agent-storage
  - cloud-storage
  - api
---

# AgentCloud Skill

> 为 AI Agent 打造的云存储服务。让你的 Agent 拥有专属文件存储空间，支持跨 Agent 文件传输和分享。

## 快速开始

### 一键注册 Agent（无需手机/邮箱，无需先注册人类账号）

只需一个命令，Agent 就能获得专属存储空间：

```bash
curl -X POST https://api.traceclaw.cn/api/v1/agents/register/open \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent"}'

# 返回示例
# {
#   "agent_id": "agt_xxxxx",
#   "api_key": "avk_yyyyy",   # ← 保存好！只返回一次
#   "name": "my-agent",
#   "plan": "free",
#   "total_storage_mb": 30
# }
```

> ⚠️ `api_key` 只返回一次，请妥善保存。如果丢失，可在 Dashboard 重置。

### 设置 API Key

```bash
# 保存到环境变量（推荐）
export AGENTCLOUD_KEY="avk_yyyyy"

# 或直接写在请求头中
# X-Agent-Key: avk_yyyyy
```

## API 概览

所有请求都通过 `https://api.traceclaw.cn/api/v1` 访问。

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/agents/register/open` | 无（开放注册，限频3次/小时/IP） | 注册新 Agent |
| GET | `/agents/me` | `X-Agent-Key` | 查询本 Agent 信息 |
| POST | `/agents/{id}/reset-key` | `X-Agent-Key` | 重置 API Key |
| DELETE | `/agents/{id}` | `X-Agent-Key` | 删除 Agent |
| POST | `/files/upload` | `X-Agent-Key` | 上传文件 |
| GET | `/files/download/{id}` | `X-Agent-Key` | 下载文件 |
| GET | `/files` | `X-Agent-Key` | 文件列表 |
| DELETE | `/files/{id}` | `X-Agent-Key` | 删除文件 |
| POST | `/files/{id}/share` | `X-Agent-Key` | 创建分享链接 |
| GET | `/files/shared/{token}` | 无需认证 | 通过分享链接下载 |

> **认证方式**：Agent 使用 `X-Agent-Key` 请求头，值为注册时获得的 `avk_xxx` API Key。

## Python 使用示例

### 安装依赖

```bash
pip install requests
```

### 注册 Agent

```python
import requests

BASE = "https://api.traceclaw.cn/api/v1"

# 注册（无需任何认证）
r = requests.post(f"{BASE}/agents/register/open", json={"name": "my-agent"})
data = r.json()

api_key = data["api_key"]  # 保存好！
agent_id = data["agent_id"]
print(f"注册成功！Agent ID: {agent_id}")
```

### 上传文件

```python
API_KEY = "avk_xxxxx"  # 注册时获得的 Key

with open("report.pdf", "rb") as f:
    r = requests.post(
        f"{BASE}/files/upload",
        files={"file": ("report.pdf", f, "application/pdf")},
        headers={"X-Agent-Key": API_KEY}
    )
file_id = r.json()["file_id"]
print(f"上传成功！File ID: {file_id}")
```

### 下载文件

```python
r = requests.get(
    f"{BASE}/files/download/{file_id}",
    headers={"X-Agent-Key": API_KEY}
)
with open("downloaded.pdf", "wb") as f:
    f.write(r.content)
```

### 创建分享链接（给其他 Agent）

```python
# 生成 1 小时有效分享链接
r = requests.post(
    f"{BASE}/files/{file_id}/share",
    json={"expires_in": 3600},
    headers={"X-Agent-Key": API_KEY}
)
share_token = r.json()["share_token"]
share_url = f"https://api.traceclaw.cn/api/v1/files/shared/{share_token}"
print(f"分享链接: {share_url}")

# 对方无需认证即可下载
r = requests.get(share_url)
with open("shared_file.pdf", "wb") as f:
    f.write(r.content)
```

### 查看文件列表

```python
r = requests.get(
    f"{BASE}/files",
    headers={"X-Agent-Key": API_KEY}
)
files = r.json()
for f in files:
    print(f"{f['filename']} — {f['file_size']} bytes")
```

### 查询 Agent 信息

```python
r = requests.get(
    f"{BASE}/agents/me",
    headers={"X-Agent-Key": API_KEY}
)
print(r.json())
# {
#   "agent_id": "agt_xxx",
#   "name": "my-agent",
#   "total_storage_mb": 30,
#   "used_storage_mb": 1.2,
#   "subscription_end": null
# }
```

## curl 一行命令版

```bash
# 注册
curl -s -X POST https://api.traceclaw.cn/api/v1/agents/register/open \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent"}'

# 上传文件
curl -s -X POST https://api.traceclaw.cn/api/v1/files/upload \
  -H "X-Agent-Key: avk_xxxxx" \
  -F "file=@myfile.pdf"

# 下载文件
curl -s -o output.pdf \
  https://api.traceclaw.cn/api/v1/files/download/{file_id} \
  -H "X-Agent-Key: avk_xxxxx"

# 创建分享链接
curl -s -X POST https://api.traceclaw.cn/api/v1/files/{file_id}/share \
  -H "X-Agent-Key: avk_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"expires_in": 3600}'

# 查看文件列表
curl -s https://api.traceclaw.cn/api/v1/files \
  -H "X-Agent-Key: avk_xxxxx" | jq .
```

## Web 管理后台

注册后可通过浏览器管理文件：
- **首页**: https://agentcloud.traceclaw.cn
- **登录**: https://agentcloud.traceclaw.cn/login
- **控制台**: https://agentcloud.traceclaw.cn/dashboard

登录后可查看存储使用量、管理上传的文件、查看 API Key。

## 套餐说明

AgentCloud 采用会员制：

| 套餐 | 价格 | 存储空间 |
|------|------|----------|
| 🆓 免费 | ¥0 | 30 MB |
| ⭐ VIP | ¥6/月 | 600 MB |
| 💎 SVIP | ¥30/月 | 3.2 GB |
| 👑 SVIP+ | ¥128/月 | 15 GB |

注册即送免费额度，可通过 Web 后台充值升级。

## OpenClaw / OpenCode 用户使用

### 安装方式

OpenClaw/OpenCode **不支持** `hermes skills install`，但支持本地 skill 目录发现。有两种方式让 skill 生效：

**方式一：直接克隆仓库用 CLI 脚本**

```bash
git clone https://github.com/jiangzh0202/agentcloud-skill.git ~/agentcloud-skill
cd ~/agentcloud-skill
pip install requests
python3 scripts/agentcloud.py register
python3 scripts/agentcloud.py me
```

**方式二：让 OpenClaw 自动发现 SKILL.md**

```bash
# 全局安装（所有项目生效）
mkdir -p ~/.config/opencode/skills/agentcloud
cp ~/agentcloud-skill/SKILL.md ~/.config/opencode/skills/agentcloud/

# 或项目级安装（仅当前项目生效）
mkdir -p .opencode/skills/agentcloud
cp ~/agentcloud-skill/SKILL.md .opencode/skills/agentcloud/
```

OpenClaw/OpenCode 会自动从 `~/.config/opencode/skills/`、`.opencode/skills/`、`.claude/skills/`、`.agents/skills/` 目录加载 skill。安装后 Agent 在对话中可自动发现并使用。

### 在代码中调用 API

```python
# OpenClaw 脚本示例
import requests

# 注册（开放注册，无需任何前置条件）
r = requests.post("https://api.traceclaw.cn/api/v1/agents", json={
    "name": context.agent.name  # 使用 Agent 自身名称
})
config = r.json()
context.memory.set("agentcloud_key", config["api_key"])

# 上传文件
r = requests.post(
    "https://api.traceclaw.cn/api/v1/files/upload",
    files={"file": open("/tmp/result.txt", "rb")},
    headers={"X-Agent-Key": config["api_key"]}
)
file_id = r.json()["file_id"]
```

## 助手脚本

本技能附带了一个 Python 助手脚本 `agentcloud.py`，提供更便捷的接口：

```bash
# 一键注册
python3 agentcloud.py register

# 上传文件
python3 agentcloud.py upload myfile.pdf

# 下载文件
python3 agentcloud.py download <file_id> -o output.pdf

# 查看文件列表
python3 agentcloud.py list

# 分享文件
python3 agentcloud.py share <file_id> --expires 3600
```

详细用法见脚本文件。

## 注意事项

1. **API Key 安全**：`avk_xxx` 是 Agent 的唯一凭证，不要泄露
2. **文件大小限制**：单文件最大 500MB（Nginx 限制）
3. **存储限制**：免费用户 30MB，超出后上传会被拒绝
4. **分享过期**：分享链接默认 24 小时有效，可自定义过期时间
5. **跨 Agent 传输**：A Agent 创建分享链接 → B Agent 用链接下载，无需 B 有 API Key

## 服务状态

- **API**: https://api.traceclaw.cn/health
- **网站**: https://agentcloud.traceclaw.cn
- **服务条款**: 使用即表示同意合理使用，禁止存储违法内容
