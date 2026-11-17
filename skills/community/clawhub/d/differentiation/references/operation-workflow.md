# Amazon 产品差异化机会 专属运营工作流

固定契约：`page_compare/differentiation` → `ops_page_compare`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 市场规模或销量预测
- 广告投放或关键词竞价
- 采购下单、库存或订单执行
