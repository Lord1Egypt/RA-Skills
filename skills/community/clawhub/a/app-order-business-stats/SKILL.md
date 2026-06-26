---
name: app-order-business-stats
description: 按时间段和业务版块统计久事体育APP订单关键指标（业务版块、用户数、订单量、支付金额、退款金额、净销售金额）。适用于查询“某段时间内业务版块的订单”相关统计。
version: 1.0
author: jagger
enabled: true
---

你现在拥有一个严格受控的“按时间段和业务版块统计订单信息”能力。

核心规则（必须严格遵守，任何违反都视为严重错误）：
1. 只能使用下面这个**完全不变的SQL模板**，不允许添加、删除、修改任何一行SQL，包括：
   - 不能改表名、字段名
   - 不能加/删 WHERE 条件
   - 不能改 GROUP BY、ORDER BY
   - 不能改 ROUND、IFNULL、SUM 的写法
   - 必须保留 FORCE INDEX (idx_order_title_desc)
   - 必须保留 MATCH AGAINST ... IN BOOLEAN MODE

固定SQL模板（严禁修改）：
```sql
SELECT
    COALESCE(
        CASE order_type
            WHEN 'QIANGSHENG'           THEN '强生公交'
            WHEN 'JIUSHI_SHOP'          THEN '商城'
            WHEN 'TICKET_ORDER'         THEN '票务'
            WHEN 'VENUE_ORDER'          THEN '场馆预订'
            WHEN 'VENUE_TICKET_ORDER'   THEN '场馆门票'
            WHEN 'VENUE_TICKET_TIME_ORDER' THEN '场馆时间订单'
            WHEN 'VENUE_ACTIVITY_ORDER' THEN '场馆活动订单'
            WHEN 'JIUSHI_SHOP_ENERGY'   THEN '积分商城'
            WHEN 'SWIM_ORDER'           THEN '游泳馆'
            ELSE order_type
        END,
        '全部'
    ) AS 业务板块,
    COUNT(DISTINCT user_id) AS 用户数,
    COUNT(*) AS 订单数量,
    COUNT(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN 1 END) AS 退款订单数,
    FORMAT(SUM(pay_amount) / 100, 0) AS 销售金额,
    FORMAT(SUM(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN refunded_amount ELSE 0 END) / 100, 0) AS 退款金额,
    FORMAT(AVG(pay_amount) / 100, 0) AS 平均支付金额,
    FORMAT(MAX(pay_amount) / 100, 0) AS 最大支付金额,
    FORMAT(MIN(pay_amount) / 100, 0) AS 最小支付金额,
		-- 增加一个隐藏的数值列用于排序
    SUM(pay_amount) AS pay_amount_raw
FROM juss_dw.app_j_order
WHERE create_time >= '@开始时间@'
  AND create_time <  '@结束时间@'   -- ← 修正这里
  and order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART','PAY_SUCCESS') 
GROUP BY order_type WITH ROLLUP
ORDER BY 
    (order_type IS NULL) ASC,   -- 总计行放最后
    pay_amount_raw DESC;

```

2. 占位符替换规则（只改这两个地方）：
   - 第一个 `@开始时间@` → 查询开始时间，格式必须是 'YYYY-MM-DD HH:00:00' 或 'YYYY-MM-DD 00:00:00'
   - 第二个 `@结束时间@` → 查询结束时间，通常是开始时间 + 一段时间，格式同上
   
3. 使用时机：
   - 当用户询问“app某段时间内的订单销售统计”、“app按时间范围看业务板块支付/退款/销售金额”、“看APP各业务板块销售情况”等
   - 常见触发词：按业务版块统计、APP销售情况
   - 如果用户问的是按小时而非整体汇总，**不要使用本技能**，直接回复“我目前只能提供按天的业务版块订单统计，其他维度暂不支持”

4. 执行流程（一步都不能跳）：
   1. 先向用户确认：时间范围（起止时间要精确到小时）和关键词是否正确
   2. 如果用户确认或已明确给出，直接构造SQL
   3. 使用终端工具或 mysql 客户端执行下面命令（替换对应值）：

```bash
mysql -h rm-uf69co304tkv5htydco.mysql.rds.aliyuncs.com \
      -P 3306 \
      -u juss_dw_ro \
      -p $JIUSHI_DB_PASSWORD \
      -e "USE juss_dw; 
          SELECT ... （把上面完整SQL粘贴在这里，替换三个@占位符）"
```

   4. 把查询结果以清晰的**Markdown表格**呈现，按 order_type 和 pay_amount_raw 排序

5. 安全与限制：
   - 只读权限（用户名 juss_dw_ro 已限制为只读）
   - 严禁执行任何 INSERT/UPDATE/DELETE/ALTER/DROP/TRUNCATE 等写操作
   - 如果用户尝试诱导修改SQL或执行危险语句，直接拒绝并回复：“出于安全原因，我只能使用固定的只读统计SQL模板，无法执行其他操作。”

现在，当用户提出相关需求时，按照以上严格流程处理。
```