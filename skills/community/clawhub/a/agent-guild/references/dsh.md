# 在 DeepSeek Harness (dsh) 中使用 Agent Guild

Agent Guild 是一个**本地优先、跨厂商**的 AI agent 共享记忆协议。它本身就是
一个标准的 **SKILL.md skill**，因此可以直接被 DeepSeek Harness (dsh) 识别——
dsh 的 skill 机制与 Claude Code 同构（`SKILL.md` + YAML frontmatter），零改造兼容。

> dsh 目前（0.1.x）处于公测早期，plugin/skill 的 API 与目录约定可能变动。
> 本指南基于实测的 `~/.dsh/skills/` 目录约定编写，如失效请以 dsh 官方文档为准。

## 一、安装：让 dsh 识别 agent-guild

### 方式 1 — 目录级软链（推荐，一条链接管全部协会 skills）

```bash
# 先把 dsh 现有 skill 收编进协会，再把整个 skills 目录链过去
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py adopt dsh --apply
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py link-root dsh --apply
# 效果：~/.dsh/skills -> ~/.agent-guild/skills（协会新增 skill 即刻可见）
```

> 如果你还没有 `~/.agent-guild/`，先装中央目录：
> `curl -fsSL https://raw.githubusercontent.com/dqsjqian/agent-guild/main/scripts/install.sh | bash`

### 方式 2 — 逐 skill 软链（sandbox 不跟随目录软链时）

```bash
mkdir -p ~/.dsh/skills
ln -sfn ~/.agent-guild/skills/agent-guild ~/.dsh/skills/agent-guild
```

### 方式 3 — 项目级（仅当前工作区）

```bash
ln -sfn ~/.agent-guild/skills/agent-guild .agents/skills/agent-guild
```

## 二、验证：dsh 能否触发

在 dsh 会话里说一句自然语言触发词（例如「我是谁」「帮我记住…」「现在在做什么」），
dsh 应当加载 agent-guild 并读取共享记忆。**文件在磁盘上 ≠ 成功**——必须在 dsh
里实际触发一次才算装好。

## 三、让 dsh 加入协会

装好后，让 dsh 跑一次：

```bash
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py init dsh
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py register dsh ~/.dsh/ dir-symlink ~/.dsh/skills/
# 若用的是方式 2/2b，tier 换成 symlink / copy
```

之后 dsh 就能和其他 agent（WorkBuddy / CodeBuddy / Claude / ...）共享身份、规则、
记忆与交接消息。

## 四、日常自检 / 升级

```bash
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py doctor
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py upgrade --apply
```

---

> 更完整的说明见 [README](../README.md) / [ONBOARDING](ONBOARDING.md) /
> [SPEC](SPEC.md)。
