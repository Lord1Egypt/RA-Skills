# Agent Migration Checklist

## 迁移前确认
- [ ] 旧 agent id 已确认
- [ ] 新 agent id 已确认
- [ ] 新 workspace 路径已确认
- [ ] 是否一起改 model 已确认
- [ ] 是否替换文档中的旧名字已确认

## 配置修改检查
- [ ] `openclaw.json` 中 agent id 已更新
- [ ] `openclaw.json` 中 workspace 已更新
- [ ] model（如需）已更新
- [ ] 相关文档中的旧名字已替换

## 会话内容迁移检查（默认必须执行）
- [ ] 旧会话内容已复制到新 agent 侧
- [ ] 如有需要，迁移摘要已写入 memory / notes
- [ ] 未强改 `.lock` / session key
- [ ] 未因为“会话是否活跃”而跳过迁移

## 重启后检查
- [ ] Gateway / OpenClaw 已重启
- [ ] UI 中出现新 agent
- [ ] 当前 agent id 正确
- [ ] workspace 正确
- [ ] model 正确
- [ ] 关键 skill / 工具正常
- [ ] 新 agent 可见迁移内容
- [ ] `sessions.json` 等会话显示层元数据里的旧名字已同步改掉

## 清理前确认
- [ ] 用户已再次明确确认是否删除旧 agent
- [ ] 用户已确认是否需要备份
- [ ] 已确认系统已稳定，不再依赖旧 agent
