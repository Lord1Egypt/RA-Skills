---
name: handoff-installer
description: Save or resume task context, record work history, and compress long records for a new session or agent. Use only for explicit handoff requests - resume, save, tidy, or compress - or for maintaining Handoff installation; an existing task record alone does not trigger this skill, and ordinary work does not create a record.
license: MIT-0
---

# Handoff

记录当前任务，让新会话直接继续；保存阶段工作历史，过长时压缩。任务数据在工作目录的
`.agents/tasks/`，规程和模板由本全局 Skill 提供。

- **继续、保存或整理任务**：读取 [PROTOCOL.md](PROTOCOL.md)。用户明确要求时应用，仅存在
  `current.md` 不自动应用；普通工作没有记录时不自动创建。只读请求不改变任务数据。
- **创建记录**：用户要求保存延续性工作时，按规程使用 [assets/TEMPLATE.md](assets/TEMPLATE.md)。
- **清理旧部署与旧入口块、升级**：仅在对应维护请求时读取 [references/protocol.md](references/protocol.md)。
  日常任务不运行 setup、迁移或账本检查，旧部署痕迹本身不触发清理。

名称 `handoff-installer` 保持稳定。`<skill-dir>` 指本 Skill 的安装目录，任务记录无需保存该路径。
