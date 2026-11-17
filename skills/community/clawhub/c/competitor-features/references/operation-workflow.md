# Amazon 竞品特性矩阵 专属运营工作流

固定契约：`page_compare/features` → `ops_page_compare`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 销量或市场份额预测
- 实时库存、订单或广告数据
- 没有证据的性能或合规认证
