# Amazon 竞品周报

经确认后生成主品与竞品的证据周报

固定工作流：`weekly/competitor`，输出 `ops_weekly`。

## 使用

```bash
python scripts/ari.py operations capabilities
python scripts/ari.py operations profile --asin <ASIN> --site amz_us
python scripts/ari.py operations quote --asin <ASIN> --site amz_us
# 用户明确确认后，复用报价返回的 requestId：
python scripts/ari.py operations run --asin <ASIN> --site amz_us --request-id <requestId> --confirm
```

评论不足时先单独使用 `collect`；本 Skill 不会隐式采集。流中断时使用
`operations status --request-id <原requestId>`，不要直接重跑。

需要 ARI API Key（`ari_live_*`）。首次使用运行 `python scripts/ari.py setup`。

## 不适用

- 未经确认自动调用付费 LLM
- 免费确定性 watch digest 或小时级监控
- 实时价格、销量、库存、广告、订单或真实退货率
