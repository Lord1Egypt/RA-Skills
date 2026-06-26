# HEARTBEAT.md — diepre-vision-cognition

## 心跳检查清单

- [ ] `vision_log/` 目录是否存在且最近 24h 内有写入？
- [ ] 上次 `analyze()` 的综合置信度是否 ≥ 90%？
- [ ] 人工复核队列 `REQUIRES_HUMAN_REVIEW` 是否积压超过 20 条？
- [ ] 模型权重文件是否完整（MD5 校验）？

## 异常触发条件

| 条件 | 动作 |
|------|------|
| 视觉日志超过 48h 未更新 | 发送告警，检查图像输入管道 |
| 人工复核队列 > 50 条 | 暂停自动判决，等待人工清空 |
| 置信度连续 5 次 < 80% | 触发模型健康检查 |
| 检测到外部 HTTP 请求含图像数据 | 立即拦截，写入安全日志 |

## 心跳状态

```json
{
  "skill": "diepre-vision-cognition",
  "version": "1.0.0",
  "last_heartbeat": null,
  "status": "initialized",
  "pending_human_review": 0,
  "avg_confidence_last_10": null
}
```
