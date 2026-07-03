# 项目执行纪律备忘

## 任务执行 Checklist（每个任务必须）

1. 完整读取 `.spec-flow/active/{slug}/tasks.md` §0 — 开发约束、Agent 规则、执行约定
2. 必须通过 `Task` 工具派发给指定 subagent 执行
3. 模块开发前先创建该模块的 `CLAUDE.md`
4. 执行前准备 — 读 CLAUDE.md → 了解模块结构 → 检查依赖完成
5. 安全合规 — 禁止硬编码密码、日志脱敏、输入验证
6. 代码质量 — 类型提示、async/await、错误处理、结构化日志
7. 测试策略 — 按任务指定的测试模式执行
8. **`CLAUDE.md` 同步** — 改完代码后必须更新模块 CLAUDE.md（Stop hook 会检查）

## 教训

<!-- 犯错后在此记录，避免重复。例： -->
<!-- - 2026-06-26 改完接口忘更新 CLAUDE.md，被 Stop hook 阻断 -->
