# 克隆龙虾 - 配置指南

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CLONE_LOBSTER_REPO_URL` | Git 备份仓库 SSH 地址 | （必填） |
| `OPENCLAW_WORKSPACE` | OpenClaw 工作区路径 | `~/.openclaw/workspace` |
| `OPENCLAW_DIR` | OpenClaw 根目录路径 | `~/.openclaw` |

## Git 仓库设置

### 美团 Code

1. 创建仓库：`https://dev.sankuai.com/code/create-repo`
2. 配置 SSH 密钥：`https://dev.sankuai.com/code/home` → SSH Key
3. 添加仓库权限：在仓库设置页添加 SSH 用户的读写权限和分支 push 权限

### GitHub

1. 创建私有仓库
2. 添加 deploy key（带写入权限）

## 备份仓库目录结构

```
catclaw_configuration/
├── README.md              # 自动生成的说明文件
├── workspace/             # 工作区文件
│   ├── AGENTS.md          # Agent 行为配置
│   ├── SOUL.md            # Agent 个性与身份
│   ├── USER.md            # 用户信息
│   ├── IDENTITY.md        # Agent 身份标识
│   ├── MEMORY.md          # 长期记忆
│   ├── HEARTBEAT.md       # 心跳任务
│   ├── TOOLS.md           # 工具配置
│   ├── memory/            # 每日记忆文件
│   └── .openclaw/         # 工作区状态
├── config/                # OpenClaw 配置
│   ├── openclaw.json      # 主配置
│   └── exec-approvals.json
├── skills/                # 已安装 Skills
├── system/                # 系统级配置
│   ├── supervisord.conf
│   ├── start-desktop.sh
│   ├── ssh_config
│   ├── installed_packages.txt
│   └── supervisor_status.txt
└── context/               # 对话上下文数据
    └── data/
```
