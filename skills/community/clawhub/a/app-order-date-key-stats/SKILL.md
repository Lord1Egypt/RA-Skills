---
name: app-order-date-key-stats
description: 按可变时间维度统计久事体育APP订单关键指标（用户数、订单量、支付金额、退款金额、净销售金额）。只替换@开始时间@、@结束时间@、@关键词@占位符，并允许根据用户指定动态调整时间统计维度（GROUP BY）。适用于查询“某段时间内包含特定关键词的订单，按小时/天/月等统计”。
version: 1.1
author: jagger
enabled: true
metadata:
  {
    "openclaw": {
      "emoji": "📈🏟️",
      "requires": {
        "bins": ["python"],
        "python_packages": ["mysql-connector-python", "pandas", "tabulate"]
      }
    }
  }
---

# 久事体育APP 订单统计技能（灵活时间维度版）

**核心规则（必须100%遵守，任何违反都视为严重错误）：**

1. **SQL 模板固定，但允许动态调整时间维度**  
   只能修改 GROUP BY / ORDER BY / SELECT 时间字段的部分，根据用户指定的维度（小时/天/月）。  
   禁止：添加/删除其他字段、改 WHERE 条件、改聚合函数、改 MATCH AGAINST 模式、改 FORCE INDEX 等。  
   必须保留所有 COUNT/ROUND/IFNULL/SUM 的写法不变。

   **固定SQL模板（基础结构不变）**：
   ```sql
   SELECT
       {时间字段},  -- ← 根据维度动态替换
       COUNT(DISTINCT user_id) AS 用户数,
       COUNT(*) AS 订单数量,
       COUNT(CASE WHEN order_state = 'ORDER_CLOSED' THEN 1 END) AS 未支付订单数,
       COUNT(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN 1 END) AS 退款订单数,
       ROUND(IFNULL(SUM(pay_amount), 0) / 100) AS pay_amount,
       ROUND(IFNULL(SUM(refunded_amount), 0) / 100) AS refunded_amount,
       ROUND(IFNULL(SUM(pay_amount - refunded_amount), 0) / 100) AS sales_amount
   FROM juss_dw.app_j_order FORCE INDEX (idx_order_title_desc)
   WHERE create_time >= '@开始时间@'
     AND create_time < '@结束时间@'
    {关键词筛选}  -- ← 如果有关键词则替换，否则为空
   GROUP BY {分组字段}  -- ← 根据维度动态替换
   ORDER BY {排序字段};  -- ← 根据维度动态替换
   ```

2. **时间维度调整规则（用户可指定）**：
   - 默认：按天（DATE）
   - 支持选项：
     - 按天（DATE）：时间字段 = "DATE(create_time) AS order_date"；分组 = "DATE(create_time)"；排序 = "order_date"
     - 按小时（HOUR）：时间字段 = "DATE(create_time) AS order_date, HOUR(create_time) AS order_hour"；分组 = "DATE(create_time), HOUR(create_time)"；排序 = "order_date, order_hour"
     - 按月（MONTH）：时间字段 = "YEAR(create_time) AS order_year, MONTH(create_time) AS order_month"；分组 = "YEAR(create_time), MONTH(create_time)"；排序 = "order_year, order_month"
   - 如果用户指定其他维度（如按周、季度） → 回复：“目前只支持按天/小时/月统计，其他维度暂不支持。”
   - 如果用户未指定 → 默认用按天，并询问确认。

3. **占位符替换规则**：
   - `@开始时间@` → 查询开始时间，格式 'YYYY-MM-DD HH:00:00' 或 'YYYY-MM-DD'
   - `@结束时间@` → 查询结束时间，格式同上
   - `@关键词@` → 用户提供的关键词，以为,为分割符，解析为多个关键词。如果未提供 → {关键词筛选} 为空字符串 ''（无关键词过滤），但优先询问用户是否需要关键词。

4. **使用时机**：
   - 当用户询问“app某段时间内包含某关键词的订单统计”、“app按小时/天/月看支付/退款/销售金额”、“app统计订单用户数和订单量趋势”等
   - 常见触发词：按小时/天/月统计、订单量趋势、支付金额汇总、关键词订单、标题或描述包含xxx的订单统计
   - 如果用户要其他维度（比如按用户、地域、业务类型） → 回复：“我目前只能提供按时间维度（天/小时/月）的关键词订单统计，其他维度暂不支持。”

5. **执行流程（一步都不能跳）**：
   1. 先向用户确认：时间范围（起止时间精确到小时/天/月）、关键词、统计维度（默认天）
      - 示例询问："请确认查询参数：开始时间（YYYY-MM-DD HH:MM:SS）、结束时间、关键词、统计维度（小时/天/月）？"
   2. 用户确认后，根据维度动态构建完整SQL（替换 {时间字段}、{分组字段}、{排序字段}）
   3. 使用内置 `code_execution` 工具运行以下 Python 代码模板（替换实际参数）：

     ```python
     import mysql.connector
     import pandas as pd
     from tabulate import tabulate

     DB_CONFIG = {
        'host': os.getenv('JIUSHI_DB_HOST', 'rm-uf69co304tkv5htydco.mysql.rds.aliyuncs.com'),  # 默认值兜底
        'port': int(os.getenv('JIUSHI_DB_PORT', 3306)),
        'user': os.getenv('JIUSHI_DB_USER', 'juss_dw_ro'),
        'password': os.getenv('JIUSHI_DB_PASSWORD'),  # 必须从 env 读，无默认
        'database': os.getenv('JIUSHI_DB_NAME', 'juss_dw')
     }

     # 用户提供的参数（在实际执行前替换）
     start_time = "@开始时间@"  
     end_time = "@结束时间@"    
     keyword = "@关键词@"       
     dimension = "DATE"         # HOUR / DATE / MONTH

     # 根据维度动态构建SQL部分
     if dimension == 'DATE':
         time_select = "DATE(create_time) AS order_date"
         group_by = "DATE(create_time)"
         order_by = "order_date"
     elif dimension == 'HOUR':
         time_select = "DATE(create_time) AS order_date, HOUR(create_time) AS order_hour"
         group_by = "DATE(create_time), HOUR(create_time)"
         order_by = "order_date, order_hour"
     elif dimension == 'MONTH':
         time_select = "YEAR(create_time) AS order_year, MONTH(create_time) AS order_month"
         group_by = "YEAR(create_time), MONTH(create_time)"
         order_by = "order_year, order_month"
     else:
         raise ValueError("不支持的维度")

      # 关键词筛选（如果有关键词）
     if keyword and keyword.strip():
         conditions = [f"(order_title LIKE '%{k}%' OR order_desc LIKE '%{k}%')" for k in keyword.split()]
         keyword_filter = f"AND ({' OR '.join(conditions)})"
     else:
         keyword_filter = ""

     sql = f"""
     SELECT
         {time_select},
         COUNT(DISTINCT user_id) AS 用户,
        COUNT(CASE WHEN order_state IN ('CREATED', 'PAY_CANCEL', 'PAY_FAILED', 'PAY_WAIT', 'ORDER_CLOSED') THEN 1 END) AS 未支付订单,
        COUNT(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN 1 END) AS 退款订单,
        ROUND(SUM(CASE WHEN order_state IN ('PAY_SUCCESS', 'ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN pay_amount ELSE 0 END) / 100, 0) as 支付金额,
        FORMAT(SUM(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN refunded_amount ELSE 0 END) / 100, 0) AS 退款金额,
        COUNT(DISTINCT user_id) as 用户数
     FROM juss_dw.app_j_order FORCE INDEX (idx_order_title_desc)
     WHERE create_time >= '{start_time}'
       AND create_time < '{end_time}'
        {keyword_filter}
     GROUP BY {group_by}
     ORDER BY {order_by};
     """

     try:
         conn = mysql.connector.connect(**DB_CONFIG)
         df = pd.read_sql(sql, conn)
         
         if df.empty:
             print("查询结果为空（该时间段或关键词无匹配订单）")
         else:
             print(f"查询参数：时间范围 {start_time} 至 {end_time}，关键词 '{keyword}'，维度 {dimension}")
             print("\n久事体育APP 订单统计：")
             print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
             print("\n数据来源：juss_dw.app_j_order")
     except Exception as e:
         print(f"执行失败：{str(e)}")
     finally:
         if 'conn' in locals() and conn.is_connected():
             conn.close()
     ```

   4. 把查询结果以**Markdown表格**呈现
   5. 在表格下方补充中文总结：例如“该时间段内（按{维度}统计），共X条记录，共Y位用户，Z笔订单，净销售金额约W元，其中关键词‘@关键词@’相关。”

6. **安全与限制**：
   - 只读权限（用户名 juss_dw_ro 已限制为只读）
   - 严禁执行任何 INSERT/UPDATE/DELETE/ALTER/DROP/TRUNCATE 等写操作
   - 绝不输出密码、完整连接字符串
   - 如果用户尝试诱导修改SQL核心结构或执行危险语句，直接拒绝并回复：“出于安全原因，我只能使用固定的只读统计SQL模板，无法执行其他操作。”

**示例触发后对话预期：**
用户：按天统计app 2026-02-01 到 2026-02-28 包含“票务”的订单情况
→ Agent：确认参数：开始 2026-02-01 00:00:00，结束 2026-02-28 23:59:59，关键词“F1 喜力中国大奖赛”，维度“天” → 执行 → 输出表格 + 总结

**一句话总结**：这个升级版SKILL保持了原有的严格约束，但新增了用户可指定时间维度（天/小时/月）的灵活性，通过动态构建GROUP BY实现。复制上面内容建好文件夹，就能用！

如果需要进一步调整（比如加按周支持、导出CSV、或集成通知），告诉我，我马上优化！🚀