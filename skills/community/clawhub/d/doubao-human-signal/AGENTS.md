# AGENTS.md — AI 技能说明书

技能：`doubao-human-signal`（豆包人类信号）
一句话定位：一眼看出是 AI 写的，扣印象分。发送前给文字做 0-100 的 AI 痕迹体检（启发式，不构成判定）。

## 调用入口

AI 代理先读 `SKILL.md`，按 frontmatter 的 `name`/`description`/`read_when` 判断是否适用，再执行正文流程。

## 文件约定

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + read_when + 执行步骤 |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览 |
| `llms.txt` | 面向 AI 的轻量索引 |
| `scripts/ai_reply_heuristics.py` | 零依赖 CLI 引擎（与源包逐字节一致） |

## 边界

- 许可与署名声明不得删除或弱化。
- 引擎脚本为只读分析工具：无网络、无文件写入、无子进程。
- 如实报告：分数是启发式提示，不得表述为"判定某段文字由 AI 生成"。
