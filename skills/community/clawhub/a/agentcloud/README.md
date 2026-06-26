# AgentCloud Skill

> 为 AI Agent 打造的云存储服务。让 AI Agent 拥有专属云存储空间，支持文件上传、下载和跨 Agent 分享。

## 适用平台

- **Hermes Agent** — 通过 `hermes skills install` 安装
- **OpenClaw / Clawdbot** — 直接复制代码到项目中
- **任何 AI Agent 框架** — 调用 REST API 即可使用

## 快速使用

### 注册你的 Agent

```bash
export AGENTCLOUD_KEY=$(curl -s -X POST https://api.traceclaw.cn/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['api_key'])")

echo "你的 Key: $AGENTCLOUD_KEY"
```

### 上传文件

```bash
curl -X POST https://api.traceclaw.cn/api/v1/files/upload \
  -H "X-Agent-Key: $AGENTCLOUD_KEY" \
  -F "file=@your-file.pdf"
```

### 更多操作

详见 [`SKILL.md`](SKILL.md) 或直接运行助手脚本：

```bash
python3 scripts/agentcloud.py register
python3 scripts/agentcloud.py upload your-file.pdf
python3 scripts/agentcloud.py list
```

## 文件结构

```
agentcloud-skill/
├── SKILL.md                  # 技能说明文档（包含所有API示例）
├── scripts/
│   └── agentcloud.py         # CLI 助手脚本（register/upload/download/list/share）
└── README.md                 # 本文件
```

## Hermes 安装

```bash
# 方法一：从 GitHub 安装
hermes skills install github:jiangzh0202/agentcloud-skill

# 方法二：直接复制到 skills 目录
cp -r agentcloud-skill ~/.hermes/skills/agentcloud
```

## API 端点

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/v1/agents` | 无 | 注册 Agent |
| GET | `/api/v1/agents/me` | `X-Agent-Key` | 查询信息 |
| POST | `/api/v1/files/upload` | `X-Agent-Key` | 上传文件 |
| GET | `/api/v1/files/download/{id}` | `X-Agent-Key` | 下载文件 |
| GET | `/api/v1/files` | `X-Agent-Key` | 文件列表 |
| POST | `/api/v1/files/{id}/share` | `X-Agent-Key` | 创建分享 |
| GET | `/api/v1/files/shared/{token}` | 无 | 分享下载 |

Base URL: `https://api.traceclaw.cn`

## 套餐

| 等级 | 价格 | 存储 |
|------|------|------|
| 免费 | ¥0 | 30 MB |
| VIP | ¥6/月 | 600 MB |
| SVIP | ¥30/月 | 3.2 GB |
| SVIP+ | ¥128/月 | 15 GB |

## 联系我们

- **网站**: https://agentcloud.traceclaw.cn
- **微信**: robbiejiang2022
