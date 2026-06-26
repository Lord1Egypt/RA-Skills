---
name: awublack-personal-memory-system
description: >
  一个智能化、高可靠性的个人知识操作系统。它不仅自动同步你的 MEMORY.md 到 SQLite 数据库并提供自然语言查询，更通过 Git 版本控制、守护进程和日志监控，确保你的记忆**永不丢失、可追溯、可恢复**。

  **使用场景**：
  (1) 用户需要查询“我过去对 AI 模型的看法？”
  (2) 用户希望系统自动记录重要决策，避免“心理笔记”
  (3) 需要一个可版本控制、可检索、可恢复的个人知识库

  **核心功能**：
  - 自动将 MEMORY.md 中的 ### 标题块同步到 memory.db 数据库
  - **智能查询**：接收自然语言问题，自动转换为 SQL 查询，从 memory.db 中精准检索并生成自然语言回答
  - 与 Obsidian 和 Git 同步，实现个人知识库的完整闭环

  **系统依赖**：
  - 必须存在 /home/awu/.openclaw/workspace-work/MEMORY.md
  - 必须存在 /home/awu/.openclaw/workspace-work/auto_sync_memory.py
  - 必须存在 /home/awu/.openclaw/workspace-work/memory.db
  - 必须存在 /home/awu/.openclaw/workspace-work/skills/awublack-personal-memory-system/query_memory.py
  - **必须存在** /home/awu/.openclaw/workspace-work/obsidian-vault/ （Obsidian 知识库）
  - **必须存在** /home/awu/.openclaw/workspace-work/git_sync_on_save.sh （Git 自动同步守护进程）
  - **必须存在** /home/awu/.openclaw/workspace-work/git_sync.log （同步日志）
  - **必须运行** git_sync_on_save.sh （每10秒检查并推送 Obsidian 变更）

  **重要**：此技能不提供任何外部 API 调用，所有数据均存储在本地，安全可靠。你的记忆存在于三个独立位置：
  1. 本地工作区：MEMORY.md, memory.db, git_sync_on_save.sh
  2. Obsidian 知识库：/home/awu/.openclaw/workspace-work/obsidian-vault/
  3. 远程 Git 仓库：https://github.com/awublack/obsidian-vault
  任何一处损坏，其他两处均可恢复。
---
# Personal Memory System
## 概述
这是一个为 OpenClaw 设计的个人知识管理技能。它解决了“人类记忆不可靠”的核心问题，通过自动化流程，将你最重要的想法和决策从易遗忘的 Markdown 文本，转化为机器可查询的结构化数据库。
## 工作原理
1. **输入**：你将重要的洞察、决策、经验写入 `/home/awu/.openclaw/workspace-work/MEMORY.md` 文件，使用 `###` 标题分隔不同主题。
2. **同步**：每当 OpenClaw 的心跳（heartbeat）被触发，`auto_sync_memory.py` 脚本会自动运行。
3. **处理**：脚本读取 `MEMORY.md`，将每个 `###` 标题及其下的内容解析为一条数据库记录。
4. **输出**：这些记录被写入 `/home/awu/.openclaw/workspace-work/memory.db` SQLite 数据库。
5. **查询**：当你提出自然语言问题（如“我过去对 AI 模型的看法？”），AI 助手会调用 `query_memory.py` 脚本，该脚本会将问题转换为 SQL 查询，从 `memory.db` 中精准检索出所有相关记忆，并为你生成一个自然语言的总结性回答。
## 系统组件
- `MEMORY.md`：你的个人长期记忆库，人类可读，可版本控制。
- `memory.db`：自动同步的 SQLite 数据库，机器可查询。
- `auto_sync_memory.py`：核心同步脚本，由 OpenClaw 心跳机制调用。
- `query_memory.py`：智能查询脚本，负责将自然语言问题转换为 SQL 查询并生成回答。
- `obsidian-vault/`：你的 Obsidian 知识库，所有笔记的原始来源。
- `git_sync_on_save.sh`：后台守护进程，每10秒检查 Obsidian 知识库变更，自动执行 git add/commit/push。
- `git_sync.log`：记录所有 Git 同步事件的日志文件，用于审计和故障排查。
## 安装与使用
1. **安装**：将此技能包放入 OpenClaw 的 `skills` 目录，或通过 `clawhub install awublack-personal-memory-system` 安装。
2. **初始化**：确保你的工作区根目录下存在以下文件和目录：
   - `MEMORY.md`
   - `obsidian-vault/`
   - `git_sync_on_save.sh`
   - `git_sync.log`
   - `auto_sync_memory.py`
   - `query_memory.py`
3. **运行**：确保 `git_sync_on_save.sh` 已通过 `nohup ./git_sync_on_save.sh > git_sync.log 2>&1 &` 启动并常驻后台。
   - 检查：`ps aux | grep git_sync_on_save.sh`
   - 重启：`pkill -f git_sync_on_save.sh && nohup ./git_sync_on_save.sh > git_sync.log 2>&1 &`
4. **查询**：直接向 AI 助手提问，例如：“我过去对 Obsidian 的看法是什么？” 系统会自动调用 `query_memory.py` 脚本检索并回答。
## 安全与隐私
- **完全本地化**：所有数据（`MEMORY.md`, `memory.db`, `query_memory.py`, `obsidian-vault/`, `git_sync_on_save.sh`, `git_sync.log`）均存储在你的本地工作区，不上传、不共享。
- **无外部依赖**：不调用任何网络 API，不访问云服务。
- **可审计**：所有操作均在你的控制之下，你可以随时查看所有相关文件的内容。
- **三重冗余**：你的记忆存在于三个独立位置：
  1. 本地工作区：MEMORY.md, memory.db, git_sync_on_save.sh
  2. Obsidian 知识库：/home/awu/.openclaw/workspace-work/obsidian-vault/
  3. 远程 Git 仓库：https://github.com/awublack/obsidian-vault
  任何一处损坏，其他两处均可恢复，**记忆永不丢失**。
## 未来扩展
- 与 Obsidian 的双向链接功能集成，自动生成知识图谱。
- 每日自动生成 `memory/YYYY-MM-DD.md` 的摘要。
- 支持导出 `memory.db` 为 CSV 或 JSON 以供备份。
- 使用更先进的 NLP 模型（如本地小模型）来增强 `query_memory.py` 的语义理解能力。
> **“记忆不是用来记住的，是用来被访问的。”**
> —— 你的数字大脑