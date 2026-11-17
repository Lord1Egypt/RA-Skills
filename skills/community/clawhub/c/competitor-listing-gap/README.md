# Amazon 竞品 Listing 差距

对照竞品商品页字段识别 Listing 表达差距

固定工作流：`page_compare/listing_gap`，输出 `ops_page_compare`。

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

- 实时价格或销量结论
- 库存、订单或真实退货率判断
- 广告投放或自动修改页面
