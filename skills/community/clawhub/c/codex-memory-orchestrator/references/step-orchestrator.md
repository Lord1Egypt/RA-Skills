# 项目步骤自动编排（step_orchestrator.py）

原 SKILL.md 章节，按需查阅。

## 项目步骤自动编排（新增能力，2026-10-20）

把一个大项目拆成有序步骤，由对话记忆管家为每步生成开工提示词；每完成一步自动开新对话框进入下一步，直到完成。

- 脚本：`scripts/step_orchestrator.py`（纯 stdlib，不上网）。plan 文件默认目录 `$CODEX_HOME/memory/plans/`（Windows 用 `%USERPROFILE%\.codex\memory\plans\`），可用 `CODEX_MEMORY_STATE_FALLBACK` 覆盖。
- plan JSON 规范：
  ```json
  {"project": "项目名", "steps": [
    {"id":"s1","title":"步骤标题","prompt":"该步开工提示词","verify":"完成验证方式"}
  ]}
  ```
- 命令：
  - `step_orchestrator.py plan <plan.json> --project 项目` 初始化计划（幂等，重复 init 提示已存在不覆盖已完成步骤）；
  - `render` 输出当前步开工提示词（`--json` 可输出结构化提示词，便于交给 `create_thread`）；`complete --note ... [--thread-id <对话框ID>]` 标记完成并推进；`status` 查看进度；`complete` 自动写 `$CODEX_HOME/audit.log`（附 thread-id 则一并记录接力证据）。
- 断点恢复：中途中断后重跑 `status`/`render` 即从 `current` 处继续；重复 `complete` 已完成步骤不会重复推进（幂等）。
- 开新对话框接力：`complete` 后读取下一次 `render` 的输出，在本 app 用 `create_thread` 把它作为首条 user 消息开新对话框，直到 `current` 到尾。
- 默认免逐步确认（用户预授权全部步骤的本地操作）：调用“对话记忆管家做步骤编排”即进入 auto，新对话框按开工提示词**直接执行、不逐次弹授权**；`complete` 后自动渲染下一步提示词直接接力。
- 权限两档：
  - 默认（不设环境变量）：免逐步确认，新对话框直接执行、不逐次确认；
  - `AUTO=0` / `APPROVAL_MODE=manual`：关闭免确认，回到每完成一步前向用户确认。
- 红线永不豁免（即使 auto）：助手主动把公司内容交给云端/Git 远端、删除原始资料、未授权系统配置改动，一律先询；用户自行网络备份/传输不受限制。监测与步骤编排脚本只记录轮次/进度/审计，不读对话正文、不上网、不上云；只有用户明确调用 checkpoint/压缩时，`export_ctx.py` 才读取指定项目的对话并仅在本机生成临时压缩件。
