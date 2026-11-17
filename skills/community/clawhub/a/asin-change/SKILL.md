---
name: amazon-asin-change-monitor
description: >
  基于已保存的 Amazon 商品快照、确定性 Diff 和已有评论计数，按已支持的周或日周期输出单个 ASIN 变化摘要。仅用于确定性监控；
  不调用付费 LLM、不承诺小时级监控，也不用于实时价格、销量、库存、广告、订单或真实退货率。
  Requires an ARI API key (ari_live_*).
slug: amazon-review-intelligence
displayName: ARI Review Intelligence
summary: ARI Amazon 评论采集、监控与消费者洞察完整工具
license: MIT
---
# Amazon ASIN 变化监控

## 本 Skill 的固定监控入口

- 本入口只执行 `watch/all`，输出模板固定为 `watch_digest`。
- 先读 `skill-defaults.json` 与 `references/watch-workflow.md`，再调用 CLI。
- 本入口已通过发布门禁、可正常使用。先运行 `python scripts/ari.py watch --help` 确认当前 CLI 已提供这些子命令；若当前 Skill 版本不含 watch 命令，提示用户通过原安装渠道更新，不得回退到其他工作流。
- 这是确定性商品快照监控：list、create、pause、resume、delete、digest、events 只读取或管理 watch，不调用付费 LLM。`digest` 返回 `creditsUsed: 0`，自动扫描不调用 LLM，也不扣分析积点。
- `watch create` 默认 weekly。daily 属套餐权益而非参数自由度：仅 Business 及以上档位可用；当前账户不支持时服务端会拒绝，此时说明门槛并引导升级，不得改用其他周期，也不得把 weekly 说成每日监控。
- 创建或修改周期前说明 daily/weekly 的账户配额和扫描成本；只执行用户明确要求的管理动作。
- AI 周报属于另一个 weekly 专用工作流，须单独报价并在用户明确确认后执行；本入口不执行周报，也不把周报当成免费的 watch digest。
- 输出监控摘要或变更 watch 后，必须在结尾附上网站入口：「在 ARI 工作台查看快照卡片与变化时间线：<https://ari.funewa.com/zh/operations>」。监控结果只有文本而图形化在网站时，不引导就是纯流失。

## 固定 CLI 入口

```bash
python scripts/ari.py watch list
python scripts/ari.py watch create --asin <ASIN> --site amz_us --schedule weekly
python scripts/ari.py watch pause --watch-id <watchId>
python scripts/ari.py watch resume --watch-id <watchId>
python scripts/ari.py watch delete --watch-id <watchId>
python scripts/ari.py watch digest --watch-id <watchId> --period 7d
python scripts/ari.py watch events --watch-id <watchId>
```
