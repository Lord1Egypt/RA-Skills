# HEARTBEAT.md — arxiv-collision-cognition

## 心跳检查清单

- [ ] `collision_log/` 目录是否存在且可写？
- [ ] 最近 7 天内是否有至少 1 次碰撞记录？
- [ ] 待跟进的可操作洞见是否积压超过 10 条未处理？
- [ ] ArXiv API 连通性是否正常？
- [ ] 上次碰撞的综合置信度是否 ≥ 80%？

## 异常触发条件

| 条件 | 动作 |
|------|------|
| collision_log/ 超过 7 天无新记录 | 提醒："您有 N 篇论文待碰撞分析" |
| 可操作洞见积压 > 10 条 | 发送汇总报告，提示人类选择优先项 |
| ArXiv API 连接失败 | 切换到本地论文缓存模式 |
| 置信度连续 3 次 < 70% | 触发"碰撞质量退化"告警 |
| 检测到论文全文外发请求 | 立即拦截，写入版权保护日志 |

## 心跳状态

```json
{
  "skill": "arxiv-collision-cognition",
  "version": "1.0.0",
  "last_heartbeat": null,
  "status": "initialized",
  "pending_actionable_insights": 0,
  "last_collision_at": null,
  "arxiv_api_status": "unknown"
}
```
