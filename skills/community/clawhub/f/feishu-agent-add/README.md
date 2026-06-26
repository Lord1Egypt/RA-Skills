# feishu-agent-add

`feishu-agent-add` 是一个给 OpenClaw 用户使用的小项目，用来快速新增“飞书机器人 + OpenClaw agent + workspace + binding”这一整套配置。

它同时支持两种使用方式：

- 普通用户：在 OpenClaw 里通过 skill 补问式配置
- 进阶用户：在终端里一条命令直接新增

两种入口共用同一个 Python 执行核心，所以配置规则、校验逻辑、备份策略都是一致的。

## 它能做什么

- 读取本机 `~/.openclaw/openclaw.json`
- 检查 `agentId` 是否冲突
- 新增 `agents.list`
- 新增 `channels.feishu.accounts`
- 新增 `bindings`
- 可选加入 `tools.agentToAgent.allow`
- 创建 workspace
- 可选初始化 `SOUL.md` 和 `BOOTSTRAP.md`
- 自动备份原配置文件
- 支持 `--dry-run`
- 支持 `--json-output`
- 支持交互式补问

## 适合谁

适合两类用户：

- 想直接对 OpenClaw 说“帮我增加一个飞书 agent”的普通用户
- 已经熟悉命令行，希望 `git clone` 后一条命令跑完的进阶用户

## 使用前提

- 你已经安装并初始化 OpenClaw
- 本机存在 `~/.openclaw/openclaw.json`
- 你已经在飞书开放平台创建好机器人，并拿到：
  - `App ID`
  - `App Secret`

默认配置路径：

- macOS / Linux：`~/.openclaw/openclaw.json`
- Windows：`%APPDATA%/openclaw/openclaw.json`

## 安装方式

### 方式一：从 ClawHub 安装，适合普通用户

如果你准备发布到 ClawHub，推荐普通用户走这条路径。

安装后，确认这个 skill 目录里包含以下文件：

```text
feishu-agent-add/
├── README.md
├── SKILL.md
├── scripts/
│   └── add_feishu_agent.py
└── templates/
    ├── BOOTSTRAP.template.md
    └── SOUL.template.md
```

通常安装完成后，把整个目录放到 OpenClaw 的 skills 目录即可，例如：

```bash
~/.openclaw/skills/feishu-agent-add
```

如果你是通过 ClawHub 一键安装的，一般不需要手动复制文件，只需要：

1. 确认 skill 已安装成功
2. 重启 OpenClaw，或重新加载 skills
3. 直接和已有的 OpenClaw agent 对话

### 方式二：从 GitHub 使用，适合进阶用户

如果你准备发布到 GitHub，推荐给进阶用户两种路径。

#### 路径 A：只想用脚本，不关心 skill 触发

```bash
git clone <your-github-repo-url>
cd feishu-agent-add
python3 scripts/add_feishu_agent.py
```

这条路径不要求你先把 skill 安装到 OpenClaw 的 skills 目录。

#### 路径 B：既想用脚本，也想在 OpenClaw 对话里触发 skill

```bash
git clone <your-github-repo-url>
cd <repo-parent-dir>
cp -R feishu-agent-add ~/.openclaw/skills/
```

然后重启 OpenClaw，再直接对已有 agent 说：

```text
帮我增加一个名字叫投研助手，用来做港股分析的飞书 agent
```

## 普通用户怎么用

把 skill 安装好之后，直接像平时聊天一样，对你现有的 OpenClaw agent 说一句：

```text
帮我增加一个名字叫投研助手，用来做港股分析和日报生成的飞书 agent
```

或者：

```text
请使用 feishu-agent-add 这个 skill，帮我新增一个飞书 agent
```

正常情况下，OpenClaw 会进入补问流程，继续问你：

- Agent 名称
- Agent 用途
- 建议的 Agent ID
- 飞书 App ID
- 飞书 App Secret

填完以后，它会先展示预览，再真正执行配置。

## 进阶用户怎么用

### 方式一：补问式命令行

什么参数都不带，直接运行：

```bash
python3 scripts/add_feishu_agent.py
```

脚本会逐步追问，并先打印一个填写示例。

示例：

```text
Agent name（Agent 名称）: 投研助手
Agent purpose（Agent 用途）: 港股分析和日报生成
Agent ID（唯一标识）: research
Workspace path（工作区路径）: 直接回车使用默认值
Feishu App ID（飞书应用 ID）: cli_xxx
Feishu App Secret（飞书应用密钥）: secret_xxx
Model override（模型覆盖，留空则使用默认值）: 直接回车
Feishu groupPolicy override（群策略覆盖，留空则继承现有配置）: 直接回车
Enable agent-to-agent collaboration for this agent（是否加入多 Agent 协作）: y
Create workspace now（现在创建工作区）: y
Write starter SOUL.md and BOOTSTRAP.md files（写入初始化模板文件）: y
Apply these changes [Y/n]: y
```

其中最关键的 4 项是：

- `Agent name`
- `Agent purpose`
- `Feishu App ID`
- `Feishu App Secret`

### 方式二：一条命令直接新增

```bash
python3 scripts/add_feishu_agent.py \
  --agent-id research \
  --agent-name "投研助手" \
  --purpose "港股分析和日报生成" \
  --app-id cli_xxx \
  --app-secret secret_xxx \
  --yes
```

推荐先用 `--dry-run` 预演：

```bash
python3 scripts/add_feishu_agent.py \
  --agent-id research \
  --agent-name "投研助手" \
  --purpose "港股分析和日报生成" \
  --app-id cli_xxx \
  --app-secret secret_xxx \
  --dry-run
```

## 常用参数

- `--agent-id`：唯一 ID，只能用小写字母、数字和 `-`
- `--agent-name`：展示名称
- `--purpose`：用途说明
- `--app-id`：飞书 App ID
- `--app-secret`：飞书 App Secret
- `--model`：可选，覆盖默认模型
- `--workspace-path`：可选，自定义 workspace 路径
- `--workspace-mode`：`auto`、`cli`、`mkdir`
- `--enable-agent-to-agent`：加入协作白名单
- `--disable-agent-to-agent`：不修改协作白名单
- `--no-create-workspace`：只改配置，不建目录
- `--no-init-templates`：不写模板文件
- `--dry-run`：只预览，不落盘
- `--json-output`：输出 JSON，适合给 skill 调用
- `--yes`：跳过最终确认

## skill 如何调用脚本

如果你要把它作为 OpenClaw skill 使用，推荐 skill 最终调用这一类命令：

```bash
python3 scripts/add_feishu_agent.py \
  --agent-id <agent-id> \
  --agent-name "<agent-name>" \
  --purpose "<purpose>" \
  --app-id <app-id> \
  --app-secret <app-secret> \
  --json-output \
  --yes
```

也就是说：

- skill 负责理解用户自然语言
- skill 负责补问缺失字段
- Python 脚本负责真正改配置

这样不会让模型直接手改 JSON，稳定性更高。

## 会修改哪些配置

脚本会修改这些字段：

- `agents.list[]`
- `channels.feishu.accounts.<agentId>`
- `bindings[]`
- `tools.agentToAgent.allow[]`

同时会在原配置文件旁边生成带时间戳的备份文件。

## 多飞书账号说明

当你已经配置了多个飞书机器人账号时，OpenClaw 可能会提示：

- 存在多个账号
- 但没有显式设置默认账号

这时建议你在 `openclaw.json` 的 `channels.feishu` 下增加：

```json
{
  "defaultAccount": "main"
}
```

把 `main` 改成你希望作为默认路由的账号 ID。

如果不设置，通常不一定立刻报错，但在某些兜底路由或插件场景下，行为会不够明确。

## 常见失败场景

脚本会在这些情况下直接停止：

- `openclaw.json` 不存在
- 配置文件不是合法 JSON
- `agentId` 已存在
- 绑定关系已存在
- 飞书凭证缺失

如果只是 workspace 已存在，默认会复用并给出提示，不会直接失败。

## 配置完成后做什么

建议按这个顺序检查：

1. 重启 OpenClaw
2. 打开新 workspace 下的 `SOUL.md`
3. 根据用途补充 agent 的身份和工作方式
4. 给新飞书机器人发一条消息，确认绑定是否生效

## 项目结构

```text
feishu-agent-add/
├── README.md
├── SKILL.md
├── scripts/
│   └── add_feishu_agent.py
└── templates/
    ├── BOOTSTRAP.template.md
    └── SOUL.template.md
```
