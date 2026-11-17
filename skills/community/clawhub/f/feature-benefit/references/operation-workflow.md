# Amazon 特性利益点表达 专属运营工作流

固定契约：`listing/benefits` → `ops_listing`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 广告关键词与竞价
- 无证据夸大商品承诺
- 自动修改或发布 Amazon 页面
