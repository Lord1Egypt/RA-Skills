# codex-export-more

Export Codex（CLI / Desktop）会话为干净的 Markdown 对话稿。

[![CI](https://github.com/sb679/codex-export-more/actions/workflows/ci.yml/badge.svg)](https://github.com/sb679/codex-export-more/actions/workflows/ci.yml)

基于 [codex-export](https://github.com/jinghan23/codex-export) 二次开发，在保留原功能的基础上补齐了增量导出、选择性导出、跨平台编码等能力。

## 特性

- 整场会话导出为 Markdown（用户消息 + 助手回复，可选工具调用）
- `--brief`：只保留用户消息与助手回复，过滤工具调用/系统注入内容
- `--since / --until`：按时间范围选择性导出
- `--grep`：按关键词筛选，命中用户提问时自动带上整轮问答
- `--append`：增量导出，只追加新消息，不覆盖你对 Markdown 的手工修改
- `--redact`：可选脱敏，打码邮箱、token、绝对路径，方便对外分享
- `--format html / obsidian / md`：导出 HTML 单文件或带 Obsidian frontmatter 的 Markdown
- `--interactive`：轻量交互选择器，按序号/范围/关键词精确挑选要导出的消息
- `--sessions id1,id2,...`：把多个会话合并成一份文档
- `--watch [秒]`：自动增量轮询，聊完自动追加新消息
- 支持 `$CODEX_HOME` 环境变量，不再硬编码 `~/.codex`
- 同一会话多个 rollout 文件自动合并，并按消息 ID 去重
- 自动剥离注入的系统噪音块（`<app-context>`、`<in-app-browser-context>`、`<environment_context>` 等）
- 显式 UTF-8 读写，Windows 中文环境无需 `PYTHONUTF8=1`
- 输出目录自动创建；归档会话（archived_sessions）自动回退查找
- 导出头部自动附带统计：消息数、工具调用数、会话时长
- `--append` 基于字节偏移只读取新增尾部，大会话增量导出秒级完成
- CI 在 Windows / Linux / macOS 三平台自动跑测试（见上方徽章）

## 安装

```bash
# Python（PyPI）
pip install codex-export-more
codex-export-more --list

# Node（npm，自动调用本机 Python）
npx codex-export-more --list

# Codex skill（clawhub）
npx clawhub@latest install codex-export-more

# 或直接源码运行
python3 scripts/export.py --list
```

发布步骤与回滚见 [docs/PUBLISH.md](docs/PUBLISH.md)。

## 使用方法

```bash
# 列出最近会话
python3 scripts/export.py --list

# 整场会话导出（默认含工具调用）
python3 scripts/export.py <session-id> output.md

# 只保留用户+助手问答
python3 scripts/export.py <session-id> output.md --brief

# 按时间范围
python3 scripts/export.py <session-id> output.md --since 2026-08-10 --until 2026-08-11 --brief

# 按内容筛选（命中问题会自动带上整轮回答）
python3 scripts/export.py <session-id> output.md --grep "Typora" --brief

# 脱敏导出（邮箱/token/路径打码）
python3 scripts/export.py <session-id> output.md --brief --redact

# 导出 HTML 单文件 / Obsidian 笔记
python3 scripts/export.py <session-id> session.html --format html
python3 scripts/export.py <session-id> session.md --format obsidian

# 交互选择要导出的消息（序号/范围/关键词，d 完成）
python3 scripts/export.py <session-id> picked.md --interactive

# 合并多个会话
python3 scripts/export.py --sessions id1,id2,id3 merged.md --brief

# 自动增量轮询（默认 30 秒一次，Ctrl+C 停止）
python3 scripts/export.py <session-id> notes.md --brief --watch 60
```

### 增量导出（推荐工作流）

```bash
# 1. 首次导出（文件不存在时 --append 等价于全量导出，并建立检查点）
python3 scripts/export.py <session-id> notes.md --brief --append

# 2. 继续聊天，之后再次执行：
python3 scripts/export.py <session-id> notes.md --brief --append
#    → 只追加新增消息，手工编辑的内容原样保留
```

检查点记录在输出文件旁的 `<输出名>.state.json`。

**从旧版本导出的文件接续**：旧文件没有检查点，首次使用 `--append` 时请用 `--since` 指定上次导出时间：

```bash
python3 scripts/export.py <session-id> old_notes.md --brief --append --since 2026-08-10T16:00:00+08:00
```

这样只追加该时间点之后的新内容，不会重复。

## 会话存储位置与 `$CODEX_HOME`

Codex 默认把会话保存在 `~/.codex/sessions/**/*.jsonl`（Windows 即 `C:\Users\<你>\.codex\sessions`）。若设置了环境变量 `CODEX_HOME`，数据会改存到 `$CODEX_HOME/sessions`。本工具优先读取 `$CODEX_HOME`，未设置时回退到默认目录。

示例（PowerShell）：

```powershell
$env:CODEX_HOME = "D:\codex-data"
python scripts\export.py --list
```

## 跨平台说明

- Windows / Linux / macOS 均可运行，仅依赖 Python 3 标准库
- 所有文件读写显式使用 UTF-8，Windows 中文环境不再出现 GBK 编码报错
- 路径使用 `pathlib` 构建，兼容各平台分隔符

## 组合限制

- `--append` 不支持 HTML 格式（HTML 请整篇重新导出）
- `--interactive` 与 `--append` 不可组合（交互选择是一次性精确导出）

## 回归测试

```bash
python -m unittest discover -s tests -v
```

## 开发与回滚预案

见 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)：需求映射、提交记录、静态检查、回滚步骤。

## 上游

原始项目：[jinghan23/codex-export](https://github.com/jinghan23/codex-export)
