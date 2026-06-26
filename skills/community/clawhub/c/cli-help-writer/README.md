# cli-help-writer

## 功能说明
这个 skill 旨在作为 CLI 工具开发者的得力助手。当你在开发命令行工具（无论是 Python 的 argparse，Go 的 Cobra，还是 Node.js 的 Commander）却苦于不知道如何排版或撰写优雅、规范的 `--help` 文案时，只需提供参数列表，它就能自动生成：
- 符合 POSIX 标准的 `USAGE`（用法）。
- 自动对齐的 `OPTIONS` 和 `COMMANDS` 列表。
- 智能补充短选项（如 `-p, --port`）。
- 自动生成基础和高阶的 `EXAMPLES`（示例）。
- 纯文本格式输出（而非 Markdown 加粗），可以直接复制粘贴到你的代码里。
- 支持中英双语输出，会根据用户的提问语言自动适配。
- **安全说明**：为了防止敏感凭证泄露，此 Skill 在生成包含真实 API Key 或密码示例的文本时，会自动将敏感值脱敏替换为 `<REDACTED>` 或通用占位符。

## 使用场景
开发新 CLI 工具、为现有的陈旧命令行工具重构 Help 输出，或者需要生成 Man Page 摘要时。

## 提问示例

**中文模式：**
```text
帮我写个命令行工具的 help 文本，工具叫 my-uploader，用来传文件。有 --file (必须), --server (可选，默认 127.0.0.1), --verbose (打印日志)
```

**英文模式：**
```text
Generate a help text for a CLI tool called `git-sync` that syncs multiple repos. Subcommands: `pull-all`, `push-all`. Flags: `--dry-run`, `--concurrent <num>`.
```