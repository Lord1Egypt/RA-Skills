# 开发与维护说明

## 需求映射

| 需求 | 实现 | 提交 |
|---|---|---|
| R1 修复 Windows 中文编码 | 读写显式 `encoding="utf-8"` | `fix: utf-8 I/O, $CODEX_HOME support, auto-create output dir` |
| R2 支持 `$CODEX_HOME` | `get_codex_home()` 优先读环境变量，回退 `~/.codex` | 同上 |
| R3 自动创建输出目录 | 写入前 `parent.mkdir(parents=True, exist_ok=True)` | 同上 |
| R4 多 rollout 文件合并 | `find_rollouts()` 收集全部匹配文件并按 mtime 排序 | `feat: merge multi-rollout sessions and dedup by message id` |
| R5 按消息 ID 去重 | `entry_key()` 以 `payload.id` 为稳定身份 | 同上 |
| R6 选择性导出 | `--since/--until` 时间窗 + `--grep` 内容筛选（命中问题带整轮） | `feat: selective export via --since/--until/--grep` |
| R7 增量导出 | `--append` + `<输出>.state.json` 检查点，只追加新消息 | `feat: incremental export via --append with sidecar checkpoint` |
| R8 回归测试 | `tests/test_export.py`（unittest，零依赖，9 个用例） | `test: regression suite for export, selective, incremental, dedup` |
| R9 文档同步 | README / SKILL / 本文档 | docs 提交 |
| R10 剥离系统噪音块 | `strip_injected_blocks()` 剔除 `<app-context>` 等注入块 | `feat: strip injected system blocks from message text` |
| R11 敏感信息脱敏 | `--redact` 打码邮箱/token/绝对路径 | `feat: optional --redact to mask emails, tokens, and paths` |
| R12/R13 HTML 与 Obsidian 导出 | `--format html|obsidian|md`，HTML 单文件带内嵌样式 | `feat: html and obsidian export formats via --format` |
| R14 交互选择 | `--interactive` 序号/范围/关键词挑选消息 | `feat: interactive message picker via --interactive` |
| R15 批量与合并 | `--sessions id1,id2,...` 多会话合成一份文档 | `feat: merge multiple sessions via --sessions` |
| R16 自动增量 | `--watch [秒]` 定时轮询追加（Ctrl+C 停止） | `feat: --watch auto incremental polling mode` |
| R17 文档同步 | README / SKILL / 本文档更新 | docs 提交 |
| R18 导出统计 | 头部附加消息数/工具调用数/会话时长 | `feat: add message/tool/duration statistics to export header` |
| R19 增量性能 | `--append` 按字节偏移只读新增尾部，文件变动自动回退全量 | `perf: tail-read rollout files on --append via byte offsets` |
| R20 打包分发 | PyPI（pyproject+console script）、npm（Node 包装器）、clawhub 元数据 | `feat: packaging for PyPI, npm wrapper, clawhub-ready metadata, utf-8 console` |
| R21 CI | 三平台 unittest + ruff lint，README 徽章 | `ci: three-platform tests, ruff lint, PyPI/npm publish workflow, lint fixes` |
| R22 发布流水线 | 打 `v*` 标签自动发 PyPI/npm；clawhub 本地发布（见 PUBLISH.md） | 同上 |

## 需求变更确认记录

- **选择性导出的方法**：按时间（`--since/--until`）与内容关键词（`--grep`）实现，二者可叠加，也可与 `--brief` 叠加。
- **`--grep` 语义**：命中用户提问时，导出该提问及其后的完整一轮回答（含工具调用，除非 `--brief`）；命中助手回答时只导出该条。
- **增量边界**：以检查点（最后一条消息时间戳 + ID 集合）为准。文件已有内容但无检查点时，首次 `--append` 默认视为“已是最新”并记录检查点；如需接续旧文件，用 `--append --since <上次导出时间>` 指定初始检查点。
- **重复保护**：不做“内容级合并”，只追加不覆盖；手工增删的内容保留，不受追加影响。
- **脱敏范围**：`--redact` 覆盖消息正文与工具调用/输出；路径保留首段与文件名，中间打码。
- **格式**：`--format` 支持 md/html/obsidian；HTML 为独立单文件（内嵌样式），Obsidian 带 YAML frontmatter；`--append` 仅支持 md 与 obsidian。
- **交互选择**：`--interactive` 以“所选即所得”为准，不再叠加时间窗/关键词过滤；不能与 `--append` 组合。
- **合并**：`--sessions` 至少两个会话，按会话分块（`## 📁 Session`），消息标题自动降级到三级标题。
- **自动增量**：`--watch` 本质是循环执行 `--append`，间隔默认 30 秒（可传秒数），Ctrl+C 停止。
- **统计信息**：仅统计导出可见的消息/工具调用与首尾时间差；合并导出时每个会话块各带一份统计。
- **增量性能**：检查点 `file_offsets` 记录每个 rollout 文件的字节偏移；文件被截断/替换（大小小于偏移）时自动回退全量读并重建偏移。
- **发布**：npm/PyPI/clawhub 三个渠道的详细步骤见 `docs/PUBLISH.md`；实际发布需要账号凭据，CI 需要配置 `PYPI_API_TOKEN` 与 `NPM_TOKEN` 两个 Secret。

## 开发流程

1. 从 `main` 创建功能分支（如 `feat/export-enhancements`）
2. 按需求拆分为小步提交，每条提交可独立回滚
3. 每步修改后运行静态检查：`python -m compileall -q scripts tests`
4. 回归测试：`python -m unittest discover -s tests -v`（当前 23 个用例）
5. 文档同步：README、SKILL、本文档随代码更新
6. 本地全部完成后再推送分支，合并回 `main`

## 静态检查

```bash
python -m compileall -q scripts tests
```

当前环境未安装 ruff；如需 lint，可自行 `pip install ruff` 后执行 `ruff check scripts tests`。

## 回滚预案

改动以“小步提交”落在功能分支上，每一条提交都是独立回滚单元：

1. **功能分支回滚**（未合并）：直接 `git reset --hard <合并前基线>`，或删除分支重建。
2. **合并后回滚**：`git revert <提交号>` 逐个还原；提交按需求映射可精确定位（见上文表格）。
3. **对照原版**：已配置 upstream（`jinghan23/codex-export`），可用 `git diff upstream/main` 查看与官方版本的差异。
4. **数据安全**：导出文件与检查点（`*.state.json`）均为生成物，不进入代码库；回滚不影响已导出的对话文件。

## 分支与合并记录

- 分支：`feat/export-enhancements`（v1）、`feat/export-v2`（v2）
- 基线：`4e74bd8`（fork 原版）
- 合并方式：合并完成后保留功能分支，便于审计与回溯
