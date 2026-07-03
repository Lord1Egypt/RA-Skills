# clawsqlite-knowledge Skill

## 这个 Skill 是什么

`clawsqlite-knowledge` 是一个很薄的 OpenClaw/ClawHub skill wrapper。
它围绕 PyPI 已发布的 `clawsqlite` 包工作，指导 Agent 稳定调用官方
`clawsqlite knowledge ...` CLI。

从 ClawHub 安装这个 skill 只会安装 wrapper 文件。必须先运行
`bootstrap_deps.sh`，CLI 才可用。在受管理的 Python 环境里，全局
`clawsqlite` 命令可能不会进入 `PATH`；请使用稳定的本地入口
`bin/clawsqlite`。

## 它和 clawsqlite 的关系

知识库核心逻辑属于上游 `clawsqlite` 包，不属于这个 skill 目录。

这个 skill 不做这些事：

- 不 vendor `clawsqlite` 源码
- 不从 GitHub clone 仓库
- 不增加 `run_clawknowledge.py` 运行时 wrapper
- 不定义第二套 JSON API
- 不维护第二套配置系统

它只做这些事：

- 通过 `bootstrap_deps.sh` 安装或升级 PyPI 包
- 提醒 Agent 使用官方 `clawsqlite knowledge ...` CLI
- 记录常用知识库操作流程

## 安装方式

安装 skill shell 后，在 skill 目录执行：

```bash
sh bootstrap_deps.sh
```

这个脚本只安装/升级 PyPI 包并做最小 CLI 校验，不处理业务逻辑。它也会
验证稳定本地入口：

```bash
./bin/clawsqlite
```

## 配置

在 knowledge instance home 中创建或编辑私有配置，不要放在 skill 目录里：

```bash
./bin/clawsqlite knowledge maintenance init-config --instance default
cd ~/.local/share/clawsqlite-knowledge/default
```

`clawsqlite.toml` 是唯一运行配置来源。这里没有提供 env 示例文件，
是为了避免让 Agent 误以为还存在第二套环境变量配置中心。

## doctor 自检

```bash
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge maintenance doctor --json
```

## 常见命令

```bash
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record ingest --url "https://example.com/post" --category web_article --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record ingest --text "some note" --title "Saved note" --category note --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record search "vector database design" --mode hybrid --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record show --id 123 --full --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge maintenance cleanup --days 3 --dry-run --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge maintenance backup --dry-run --json
```

文本入库里的 `--title` 是 `source_title` 提示，用于归档文件名和元数据。
strict 入库时，真正的知识库标题会由 LLM 写入 `generated_title`。

## 什么时候直接用 clawsqlite

如果你在开发、调试、修改上游包本身，应该直接使用 `clawsqlite` 项目。
如果 Agent 只是要操作一个已配置的知识库 instance，就使用这个 skill
提供的薄说明层。
