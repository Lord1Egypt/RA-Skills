# AgentDrive CLI Skill 安装指南

本 README 供智能体（AI Agent）或自动化脚本快速读取，用于自动下载并安装 `agentdrive-cli-skill`。

## 什么是 agentdrive-cli-skill？

`agentdrive-cli-skill` 是一个云盘操作技能包。Agent 安装并加载它后，可以通过执行本地命令行工具（`agentdrive`）直接管理 360 AI 云盘中的文件。详细的命令说明和鉴权配置均已定义在同目录的 [`SKILL.md`](SKILL.md) 中。

## 快速下载

```bash
curl -O http://cn-zhengzhou-3.xstore.qihu.com/yunpan-zz2-pkg/agentdrive-cli-skill.zip
```

## 如何自动化安装

从 GitHub 仓库克隆安装：

```bash
# 1. 创建你的 skills 存放目录（以 .skills 为例）
mkdir -p .skills

# 2. 将包含该 skill 的仓库拉取到本地
git clone https://github.com/yifangyun/ecs-yunpan-skills.git .skills/ecs-yunpan-skills

# 3. 将 agentdrive-cli-skill 移动到你的主 skills 目录，并清理无用文件
mv .skills/ecs-yunpan-skills/agentdrive-cli-skill .skills/
rm -rf .skills/ecs-yunpan-skills
```

执行完毕后，你的本地结构应当如下：

```text
.skills/
└── agentdrive-cli-skill/
    ├── SKILL.md
    ├── README.md
    └── references/
        └── commands.md
```

## 智能体加载与配置

安装到本地后，将 `agentdrive-cli-skill/` 目录放入 Agent 平台的 skills 目录，即可开始使用。

- Claude Code：`~/.claude/skills/agentdrive-cli-skill/`
- OpenCode：`~/Library/Application Support/OpenCode/skills/agentdrive-cli-skill/`（macOS）

**鉴权**：执行以下命令绑定 API Key：

```bash
npx -y -p @aicloud360/agentdrive@latest agentdrive auth login --api-key <YOUR_API_KEY>
```

> **安装校验**：向 Agent 发送「请帮我列出云盘根目录下的文件」，若 Agent 能成功执行 `agentdrive dir ls /` 并返回结果，即表示安装和配置成功。
