# dreamlover-skill

> “搞出来大模型的简直是码神，使用 AI 创造了雷电将军，还要创造玛奇玛，创造喜多川海梦，创造薇尔莉特，创造蕾姆，创造霞之丘诗羽，创造中野二乃，创造樱岛麻衣，最后创造一个只有老婆们的完美世界。”

把虚拟角色资料蒸馏成可复用的角色 skill。  
顶层 `dreamlover-skill` 负责生成；生成出来的子角色 skill 可以直接给 Codex 使用，也可以按需导出到 OpenClaw workspace等软件。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)

仓库地址：[tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)  
[English](README_EN.md)

## 这是什么

`dreamlover-skill` 是一个生成器 skill。

它会先生成一套共享静态角色内容：

- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`

然后基于这套内容生成平台包装层：

- Codex 主安装：`./.agents/skills/{slug}/`
- OpenClaw 可选导出：`<openclaw_workspace>/.agents/skills/{slug}/`

`characters/{slug}/` 视为唯一角色源。  
Codex 安装目录和 OpenClaw 导出目录都属于生成产物，不建议手改。

## 安装

### Claude Code

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill
```

### Codex

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### 环境要求

- Python 3.9+
- 当前版本主要处理文本资料
- 如果要启用条件记忆，运行环境需要 `python3`

## 使用

### 1. 用顶层 skill 创建角色

```text
$dreamlover-skill
帮我创建雷姆这个角色 skill
```

生成器会先进行中文 intake。  
确认草稿后，会先安装 Codex 版本，再询问你是否要额外导出 OpenClaw 版本。

### 2. CLI 创建

```bash
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug rem --name "Rem"
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /path/to/openclaw-workspace
```

### 3. Codex 中使用子角色

生成后，Codex 角色目录在：

```text
./.agents/skills/{slug}/
```

检查与调用：

```text
/skills
$rem
```

### 4. OpenClaw 中使用导出版本

如果选择导出，目录为：

```text
<openclaw_workspace>/.agents/skills/{slug}/
```

然后：

- 刷新 skills 或新建会话
- 让 OpenClaw 从 workspace 自动发现该角色
- 直接用普通对话触发角色扮演

## 条件记忆

子角色 skill 带条件触发式记忆：

- 普通闲聊默认不读写记忆
- 只有命中条件时才读取或写入
- 运行时数据库在 `<workspace>/.dreamlover-data/memory.sqlite3`
- 不会把 `.dreamlover-data/` 打进 skill 目录

如果 `python3` 不可用，角色会退化为无记忆模式，而不是整个 skill 失效。

预期结果：

- `characters/{slug}/` 有共享静态内容
- `./.agents/skills/{slug}/` 有 Codex 可发现的子 skill

## License

MIT
