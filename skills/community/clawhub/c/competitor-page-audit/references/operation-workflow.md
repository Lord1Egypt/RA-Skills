# Amazon 竞品商品页审查 专属运营工作流

固定契约：`page_compare/page` → `ops_page_compare`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 实时经营数据分析
- 广告投放与页面自动修改
- 库存、订单或真实退货率结论
