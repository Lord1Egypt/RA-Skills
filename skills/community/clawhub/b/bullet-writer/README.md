# Amazon 五点描述优化

把评论证据转成五点表达优化建议

固定工作流：`listing/bullets`，输出 `ops_listing`。

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

- 标题改写
- 广告关键词与竞价
- 自动修改或发布 Amazon 页面
