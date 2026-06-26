# SELF_CHECK

## 规范检查
- [x] 包含 `SKILL.md`
- [x] 包含 `README.md`
- [x] 包含 `SELF_CHECK.md`
- [x] 包含 `scripts/` 且有完整脚本
- [x] 包含 `resources/` 且资源真实被引用
- [x] 包含 `examples/`
- [x] 包含 `tests/smoke-test.md`

## Frontmatter 检查
- [x] 使用 YAML frontmatter
- [x] `name` 存在
- [x] `description` 存在
- [x] `metadata` 使用单行 JSON，符合最新 skills.md 文档约束
- [x] 使用 `requires.bins` 做宿主环境 gating

## 工程检查
- [x] 脚本支持 dry-run
- [x] 脚本支持 execute
- [x] 失败有退出码
- [x] 记录状态文件
- [x] 滚动窗口限速：3600 秒内最多 5 次
- [x] 使用绝对路径更稳
- [x] 无 TODO / 伪代码 / 混淆执行

## 安全检查
- [x] 未使用 `curl|bash`
- [x] 未使用 base64 混淆执行
- [x] 不调用私有未声明 API
- [x] 不绕过 ClawHub 官方 CLI
- [x] 明示依赖：`python3`、`clawhub`
- [x] 明示文件读写范围：队列 JSON、状态 JSON、日志目录

## 可维护性
- [x] 配置集中在脚本参数
- [x] 状态文件为 JSON，便于审计
- [x] 日志输出清晰
- [x] 可由 cron 或 systemd 托管

## 评分
- 规范对齐：9/10
- 实用性：9/10
- 安全性：9/10
- 可维护性：9/10
- 当前外部阻塞：ClawHub CLI 最近存在 publish license terms 兼容问题，不属于本 Skill 内部缺陷
