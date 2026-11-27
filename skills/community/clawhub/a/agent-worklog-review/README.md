# agent-worklog-review

盘点本机所有 AI Agent 的会话记录，提取并分类"完成了什么工作"，统计 token 消耗，产出可直接用于周会 / 述职 / AI 落地成效总结的结构化材料。

**纯本地、只读、不联网**：全程只读取本机会话文件，不上传对话正文、代码或密钥。

## 能做什么

- 扫描 26+ 种 AI Agent 的会话存储位置（Windows / Linux / macOS / WSL）
- 21 个专用适配器 + L2 声明式规则 + L3 启发式兜底，三层覆盖
- 提取任务并按项目 / 工作类型 / AI 技能标签 / 月份多维分类
- 统计各 Agent 的 token 消耗（含缓存率、非缓存口径）
- 生成 Markdown 报告 + 11 sheet Excel 工作簿
- **报告只列本机实际在用的 Agent**，未安装的不产生噪音

## 安装

这是一个标准的 Agent Skill（一个包含 `SKILL.md` 的目录），**不绑定任何特定 Agent**。两种方式任选其一：

**方式一：作为 Skill 安装（推荐）**

把整个目录克隆/复制到你所用 Agent 的 skills 目录：

```bash
git clone https://github.com/iorireal/agent-worklog-review.git <你的 skills 目录>/agent-worklog-review
```

常见 Agent 的 skills 目录（**只放你实际使用的那个即可，不必全装**）：

| Agent | Skills 目录 |
|---|---|
| Claude Code | `~/.claude/skills/agent-worklog-review` |
| OpenAI Codex | `~/.codex/skills/agent-worklog-review` |
| WorkBuddy | `~/.workbuddy/skills/agent-worklog-review` |
| Cursor | `<项目>/.cursor/skills/agent-worklog-review` |
| opencode | `~/.config/opencode/skills/agent-worklog-review` |

Windows 下把 `~` 换成 `%USERPROFILE%`（如 `C:\Users\<你的用户名>\.claude\skills\agent-worklog-review`）。其他支持 Skill 的工具参照其文档放到对应目录即可。

**方式二：不装 Skill，直接跑脚本**

脚本不依赖任何 Agent 平台，克隆到任意目录后直接执行即可（见下）。

## 使用

**通过 Agent 触发**：在你使用的 Agent 里说"整理我在各 agent 完成的工作" / "统计 AI 工具使用情况" / "生成 AI 落地汇报材料"（不同 Agent 触发词略有差异，意思到了即可）。

**直接跑脚本**：

```bash
cd /path/to/agent-worklog-review
python scripts/run_all.py            # 一键跑完整链路
python scripts/run_all.py --interactive  # 非常规 WSL 用户名/路径时交互指定
```

输出在 `output/`：

| 文件 | 内容 |
|---|---|
| `agent_scan_report.json` | 检测到的 Agent 及会话存储位置 |
| `all_tasks.jsonl` / `tasks_classified.jsonl` | 原始与分类后的任务 |
| `task_analysis_report.md` | 任务分类报告 + 核心发现 + 在用 Agent 表 |
| `token_usage.jsonl` / `token_report.md` | token 明细与汇总 |
| `agent_worklog.xlsx` | 11 sheet Excel（总览 / 按 Agent / 项目 / 月份 / 模型 / Top 会话 / 任务分类 / 明细） |

## 依赖

- Python 3.8+，**核心链路仅标准库**
- `zstandard`（可选）：dsh 压缩会话统计；脚本自动探测带该模块的解释器（含 conda），找不到则跳过并在报告标注
- `openpyxl`（可选）：Excel 导出；缺失只提示跳过，不影响其他产物

## 配置（可选，本机私有）

复制模板到 `config/local/` 后按需修改，这些文件已被 `.gitignore` 排除，不会外发：

| 模板 | 用途 |
|---|---|
| `config/project_rules.json.example` | 项目分类规则（如把路径映射到项目名） |
| `config/noise_filters.example.json` | 过滤被误判为任务的注入文本 |
| `config/adapter_rules.example.json` | 为新 Agent 声明解析规则（零代码接入） |

环境变量：`WORKLOG_WSL_USER` / `WORKLOG_WSL_DISTRO`（非常规 WSL 环境）、`WORKLOG_EXTRA_ROOTS`（会话库在非标准路径）、`WORKLOG_OUT_DIR`（自定义输出目录）、`WORKLOG_CONFIG`（自定义规则文件）。

## 扩展

给新 Agent 写适配器：复制 `scripts/adapters/_TEMPLATE.py`，实现 `extract_tasks()` / `collect_tokens()`，放到 `scripts/adapters/` 下即可，无需改核心脚本。拿不到 token 就返回空并设 `token_note`，绝不伪造。

更简单的方式：在 `config/local/adapter_rules.local.json` 按 `config/adapter_rules.example.json` 加一条声明式规则，零代码接入。

## 口径提示

- 会话量 ≠ 工作量：含 Agent 自评估 / 自动化测试会话，汇报时说"AI 辅助会话记录"
- 缓存命中 token 是上下文复用、不等于真实消耗，汇报用量建议用**非缓存 token**
- 费用需按厂商定价另行换算，本工具不内置价格表、不臆造数字

详细设计与踩坑记录见 [SKILL.md](SKILL.md)。

## License

MIT-0（MIT No Attribution），与 ClawHub 发布政策一致：任何人可自由使用、修改、再分发（含商用），无需署名。完整条款见 [LICENSE](LICENSE)。
