# 固定注入测量与发布闸门

本模块只面向 Codex 桌面端的固定注入做只读测量。它回答三个问题：现在注入了多少、有没有漂移、MCP 能不能定论。它不改写记忆、AGENTS、rules、插件缓存、MCP 配置、provider 或认证。

## 七块口径

| 块 | 来源 | 口径 |
| --- | --- | --- |
| 记忆摘要 | `$CODEX_HOME/memories/memory_summary.md` | measured |
| 基础系统提示 | Codex CLI/App 静态模板 | static；随版本变化 |
| 技能目录 | `codex debug prompt-input` 的 skills 块 | measured |
| 权限块 | 权限模板 | measured |
| 全局 AGENTS | `$CODEX_HOME/AGENTS.md` | measured；含前后包装字节 |
| MCP schema | `tools/list` | 占位或实测；不是每请求注入 |
| 环境上下文 | 当前工作目录渲染 | measured；cwd 不同会略有差异 |

文本块闸门默认 57,344 B（56 KiB），是本项目的预算线，不是 Codex 的硬上限。需要其他预算时用 `--gate` 显式指定。

## 命令

```sh
# 当前七块测量；超闸门退出 1
python3 scripts/measure_prompt.py --gate 57344

# 机器可读
python3 scripts/measure_prompt.py --json --gate 57344

# 状态机：记录 / 复核 / 插件缓存 volatile 清单
python3 scripts/injection_state.py --record
python3 scripts/injection_state.py --check
python3 scripts/injection_state.py --volatile

# 四层去重与冲突，只报告
python3 scripts/scan_layers.py --summary

# 预算看板
python3 scripts/budget_dashboard.py --no-measure --out /tmp/budget.md

# MCP tools/list schema 字节
python3 scripts/mcp_probe.py --stdio --name svc -- <启动命令>
python3 scripts/mcp_probe.py --http https://example/mcp --name svc --bearer-env TOKEN_ENV

# 首请求 input 观测，不是账单
python3 scripts/token_experiment.py --help

# 自测
python3 scripts/self_test.py
```

## 状态机

`injection_state.py` 记录五类源文件指纹，并抓取当前注入块字节：

- 记忆摘要
- 全局 AGENTS
- `rules/default.rules`
- `lessons/LESSONS.md`
- 技能目录中每个 `SKILL.md` 的 `description` 行哈希与总字节

状态文件默认 `$CODEX_HOME/memory/injection-state.json`，写前备份到 `$CODEX_HOME/backups/injection-state/`。`--check` 只比对，不改文件。

状态含义：

- `OK`：源文件指纹与注入块一致。
- `DRIFT`：`description`、技能数量、记忆/AGENTS/rules/lessons 变化，导致注入可能变化。
- `BODY_CHANGED`：只改技能正文、脚本或 references，不影响技能目录注入。
- `MISSING`：源文件或状态文件缺失。
- `UNMEASURED` / `UNKNOWN`：缺少 App 整体实测或 MCP 实测，不能写成 PASS。

## 发布闸门

任何 Skill 新增或修改，发布前必须全过：

1. `description` 单条 ≤45 字，保留触发词和“不做什么”。
2. `SKILL.md` 目标 ≤8 KB；超出就外移到 `references/`，只搬不删。
3. `injection_state.py --record` 后 `--check` 返回 `overall: OK`。
4. `measure_prompt.py --gate 57344` 文本块 PASS。
5. `self_test.py` 全部 PASS。
6. `check_integration`、`check_release` 和包内测试通过；发布包不含 `.bak.*`、个人路径和公司数据。

`UNMEASURED` 不是 PASS，`UNKNOWN` 不是已支持。没有 App 首请求实测时，只能报告已知上界，不能声称整体注入已验证。

## 隐私边界

- 不读取聊天正文、会话内容、数据库正文、备份正文或日志正文。
- MCP 探针只统计 `tools/list` 的 `tools` 数组字节，不打印 token、请求头、请求体或提示词。
- 测量结果只写调用方指定的输出路径；状态机只写 `$CODEX_HOME/memory/injection-state.json` 及其备份。
- 不联网；HTTP 探针只连用户显式指定的端点。
- 公司数据、图纸、施工资料、客户信息不得进入测量输出或发布包。

## 已知限制

- `measure_prompt.py` 依赖 Codex CLI 的 `debug prompt-input` 输出结构；CLI 改版可能导致解析失败，失败时退出码非 0。
- 基础系统提示是版本相关的静态基线，升级 App 后需要重新核对。
- MCP 原始 `tools/list` 总量不是每请求注入；App 首请求实际注入仍可能 `UNMEASURED`。
- 插件缓存是易挥发内容，描述被平台复原属预期，不计永久收益。
