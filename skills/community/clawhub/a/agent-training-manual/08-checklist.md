# 08 — 入职检查清单

> 完成这个清单，你就正式上岗了。

## ✅ 第一天：了解自己

- [ ] 读完 `BOOTSTRAP.md`，和用户确定你的身份
- [ ] 填写 `IDENTITY.md`（名字、形象、定位）
- [ ] 填写 `SOUL.md`（性格、价值观、做事风格）
- [ ] 填写 `USER.md`（用户基本信息、偏好、需求）
- [ ] 删除 `BOOTSTRAP.md`（你不再需要它了）

## ✅ 第一天：搭建工作区

- [ ] 创建 `memory/` 目录
- [ ] 创建 `.learnings/` 目录和三个文件：
  - `LEARNINGS.md`
  - `ERRORS.md`
  - `FEATURE_REQUESTS.md`
- [ ] 创建 `HEARTBEAT.md`（心跳检查清单）
- [ ] 创建 `TOOLS.md`（工具使用记录）
- [ ] 创建 `memory/heartbeat-state.json`（心跳状态追踪）

## ✅ 第一天：安装必备技能

- [ ] 确认 `self-improving-agent` 技能已安装
- [ ] 确认 `mermaid-diagram` 技能已安装（如需画图）
- [ ] 确认了解 `clawhub search` 和 `clawhub install` 的用法
- [ ] 根据工作内容安装按需技能（见 [07-skills-list.md](07-skills-list.md)）

## ✅ 第一周：建立工作习惯

- [ ] 每次会话启动时读 SOUL.md → USER.md → 今天/昨天日志
- [ ] 犯错时立即记录到 `.learnings/ERRORS.md`
- [ ] 收到纠正时立即记录到 `.learnings/LEARNINGS.md`
- [ ] 用户提新需求时记录到 `.learnings/FEATURE_REQUESTS.md`
- [ ] 每天写一条 `memory/YYYY-MM-DD.md` 日志
- [ ] 和用户确认心跳频率和汇报方式

## ✅ 第一周：配置自动化

- [ ] 设置心跳 cron（建议 30 分钟）
- [ ] 设置工作区备份 cron（每天一次）
- [ ] 设置学习回顾 cron（每天一次，delivery: none）
- [ ] 确认所有 cron 任务的 `consecutiveErrors = 0`

## ✅ 持续改进

- [ ] 每周整理一次 MEMORY.md（短期 → 长期）
- [ ] 定期检查 .learnings/ 中的 pending 条目
- [ ] 高价值教训推广到 SOUL.md / TOOLS.md / AGENTS.md
- [ ] 发现新的最佳实践时更新本手册

## 🎓 毕业标准

完成以下所有条件，你就是一个合格的团队成员了：

1. ✅ 连续 7 天心跳正常运行
2. ✅ 至少记录了 5 条 learnings
3. ✅ 至少推广了 2 条教训到核心文件
4. ✅ 没有因为同一个错误被批评两次
5. ✅ 用户对你的工作表示满意

---

*"入职只是开始，成长永不停止。欢迎加入团队！" — 悠悠 · 大师姐*
