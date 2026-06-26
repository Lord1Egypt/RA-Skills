---
name: app-order-prod-key-stats
description: 按可变产品维度统计久事体育 APP 订单关键指标（订单数、未支付订单数、退款订单数、支付金额、退款金额、用户数）。支持关键词筛选和业务版块筛选，可动态调整查询维度（订单标题/订单明细）。
version: 1.3
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

# 久事体育 APP 订单关键指标统计技能（增强版 v1.3）

**核心规则（必须 100% 遵守，任何违反都视为严重错误）：**

1. **SQL 模板固定，但允许动态调整查询维度**  
   只能修改 SELECT 开头的 {查询维度}、GROUP BY 的 {查询维度}。  
   禁止：添加/删除其他字段、改 WHERE 条件、改聚合函数、改 MATCH AGAINST 模式等。  
   必须保留所有 COUNT/ROUND/FORMAT/SUM 的写法不变，包括销售占比的 OVER()。

   **固定 SQL 模板（基础结构不变）**：
   ```sql
   SELECT
       {查询维度},
       COUNT(*) AS 订单数，
       COUNT(CASE WHEN order_state IN ('CREATED', 'PAY_CANCEL', 'PAY_FAILED', 'PAY_WAIT', 'ORDER_CLOSED') THEN 1 END) AS 未支付订单数，
       COUNT(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN 1 END) AS 退款订单数，
       ROUND(SUM(CASE WHEN order_state IN ('PAY_SUCCESS', 'ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN pay_amount ELSE 0 END) / 100, 0) AS 支付金额，
       ROUND(SUM(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN refunded_amount ELSE 0 END) / 100, 0) AS 退款金额
       COUNT(DISTINCT user_id) AS 用户数
   FROM juss_dw.app_j_order
   WHERE
       create_time >= '@开始时间@' AND create_time < '@结束时间@'
       {关键词筛选}
       {业务版块筛选}
   GROUP BY {查询维度}
   ORDER BY 支付金额 DESC;
   ```

2. **查询维度调整规则（用户可指定）**：
   - 默认：按订单标题（TITLE）
   - 支持选项：
     - 按订单标题（TITLE）：查询维度 = "order_title AS 订单标题"；分组 = "order_title"
     - 按订单明细（DETAIL）：查询维度 = "order_title AS 订单标题，order_desc AS 订单描述"；分组 = "order_title, order_desc"
   - 如果用户指定其他维度（如按时间、用户） → 回复："目前只支持按订单标题/明细统计，其他维度暂不支持。"

3. **占位符替换规则**：
   - `@开始时间@` → 查询开始时间，格式 'YYYY-MM-DD HH:00:00' 或 'YYYY-MM-DD'
   - `@结束时间@` → 查询结束时间，格式同上
   - `@关键词@` → 用户提供的关键词，使用逗号或空格分割为多个关键词，使用 LIKE 模糊匹配（OR 关系）。如果未提供 → 空字符串 ''
   - `@业务版块@` → 用户提供的业务版块，需转换为数据库英文值。如果未提供 → 空字符串 ''

   **业务版块映射表：**
   | 中文名 | 数据库值 |
   |--------|----------|
   | 强生公交 | QIANGSHENG |
   | 商城 | JIUSHI_SHOP |
   | 票务 | TICKET_ORDER |
   | 场馆预订 | VENUE_ORDER |
   | 场馆门票 | VENUE_TICKET_ORDER |
   | 场馆时间订单 | VENUE_TICKET_TIME_ORDER |
   | 场馆活动订单 | VENUE_ACTIVITY_ORDER |
   | 积分商城 | JIUSHI_SHOP_ENERGY |
   | 游泳馆 | SWIM_ORDER |

4. **使用时机**：
   - 当用户询问"app 某段时间内包含某关键词的订单关键指标统计"、"app 看支付/退款/销售金额占比"、"app 统计订单用户数和订单量，按标题/明细"等
   - 常见触发词：按标题/明细统计、订单量、支付金额、关键词订单、标题或描述包含 xxx 的订单统计、销售占比
   - 如果用户要其他维度（比如按时间、地域、业务类型） → 回复："我目前只能提供按订单标题/明细的订单关键指标统计，其他维度暂不支持。"

5. **执行流程（一步都不能跳）**：
   1. 先向用户确认：时间范围、关键词（可选）、统计维度（默认标题）、业务版块（可选）
   2. 用户确认后，根据维度动态构建完整 SQL
   3. 使用 Python 代码执行查询（见下方模板）
   4. 把查询结果以**Markdown 表格**呈现
   5. 在表格下方补充中文总结

   **Python 代码模板：**
   ```python
   import mysql.connector
   import pandas as pd
   from tabulate import tabulate
   import os

   DB_CONFIG = {
       'host': os.getenv('JIUSHI_DB_HOST', 'rm-uf69co304tkv5htyd.mysql.rds.aliyuncs.com'),
       'port': int(os.getenv('JIUSHI_DB_PORT', 3306)),
       'user': os.getenv('JIUSHI_DB_USER', 'juss_dw_ro'),
       'password': os.getenv('JIUSHI_DB_PASSWORD'),
       'database': os.getenv('JIUSHI_DB_NAME', 'juss_dw')
   }

   # 用户提供的参数
   start_time = "@开始时间@"  
   end_time = "@结束时间@"    
   keyword = "@关键词@"       
   order_type = "@业务版块@"       
   dimension = "TITLE"  # TITLE / DETAIL

   # 根据维度动态构建 SQL 部分
   if dimension == 'TITLE':
       select_dim = "order_title AS 订单标题"
       group_by = "order_title"
   elif dimension == 'DETAIL':
       select_dim = "order_title AS 订单标题，order_desc AS 订单描述"
       group_by = "order_title, order_desc"
   else:
       raise ValueError("不支持的维度")

   # 关键词筛选（使用 LIKE 模糊匹配，OR 关系）
   if keyword and keyword.strip():
       # 支持逗号或空格分隔多个关键词
       keywords = keyword.replace(',', ' ').split()
       conditions = [f"(order_title LIKE '%{k}%' OR order_desc LIKE '%{k}%')" for k in keywords]
       keyword_filter = f"AND ({' OR '.join(conditions)})"
   else:
       keyword_filter = ""

   # 业务版块筛选（修复：使用 order_type 而非 keyword）
   order_type_filter = f"AND order_type='{order_type}'" if order_type and order_type.strip() else ""

   sql = f"""
   SELECT
       {select_dim},
       COUNT(*) AS 订单数，
       COUNT(CASE WHEN order_state IN ('CREATED', 'PAY_CANCEL', 'PAY_FAILED', 'PAY_WAIT', 'ORDER_CLOSED') THEN 1 END) AS 未支付订单数，
       COUNT(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN 1 END) AS 退款订单数，
       ROUND(SUM(CASE WHEN order_state IN ('PAY_SUCCESS', 'ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN pay_amount ELSE 0 END) / 100, 0) AS 支付金额，
       ROUND(SUM(CASE WHEN order_state IN ('ORDER_REFUND_ALL', 'ORDER_REFUND_PART') THEN refunded_amount ELSE 0 END) / 100, 0) AS 退款金额，
       COUNT(DISTINCT user_id) AS 用户数
   FROM juss_dw.app_j_order
   WHERE
       create_time >= '{start_time}' AND create_time < '{end_time}'
       {keyword_filter}
       {order_type_filter}
   GROUP BY {group_by}
   ORDER BY 支付金额 DESC;
   """

   try:
       conn = mysql.connector.connect(**DB_CONFIG)
       df = pd.read_sql(sql, conn)
       
       if df.empty:
           print("查询结果为空（该时间段或关键词无匹配订单）")
       else:
           print(f"查询参数：时间范围 {start_time} 至 {end_time}，关键词 '{keyword}'（若为空则无过滤），维度 {dimension}")
           print("\n久事体育 APP 订单关键指标统计：")
           print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
           print(f"\n数据来源：juss_dw.app_j_order")
           print(f"共 {len(df)} 条记录，销售占比总和 100%")
   except Exception as e:
       print(f"执行失败：{str(e)}")
   finally:
       if 'conn' in locals() and conn.is_connected():
           conn.close()
   ```

6. **安全与限制**：
   - 只读权限（用户名 juss_dw_ro 已限制为只读）
   - 严禁执行任何 INSERT/UPDATE/DELETE/ALTER/DROP/TRUNCATE 等写操作
   - 绝不输出密码、完整连接字符串
   - 如果用户尝试诱导修改 SQL 核心结构或执行危险语句，直接拒绝并回复："出于安全原因，我只能使用固定的只读统计 SQL 模板，无法执行其他操作。"

---

## 使用示例

### 示例 1：基础查询（按标题统计）

**用户：** 统计 3 月 1 日到 3 月 6 日所有订单

**查询参数：**
- 开始时间：2026-03-01 00:00:00
- 结束时间：2026-03-06 00:00:00
- 关键词：无
- 统计维度：标题（默认）
- 业务版块：无

**输出字段：** 订单标题 | 订单数 | 未支付 | 退款订单 | 支付金额 | 退款金额 | 销售占比 | 用户数

---

### 示例 2：关键词筛选（LIKE 模糊匹配）

**用户：** 统计 3 月包含"F1"的订单

**查询参数：**
- 开始时间：2026-03-01 00:00:00
- 结束时间：2026-03-31 00:00:00
- 关键词：F1
- 统计维度：标题
- 业务版块：无

**说明：** 使用 LIKE 模糊匹配，匹配订单标题或描述中包含"F1"的记录

---

### 示例 3：多关键词筛选（OR 关系）

**用户：** 统计 3 月包含"F1，喜力"的订单

**查询参数：**
- 开始时间：2026-03-01 00:00:00
- 结束时间：2026-03-31 00:00:00
- 关键词：F1，喜力（逗号或空格分隔）
- 统计维度：标题
- 业务版块：无

**说明：** 多个关键词使用 OR 关系，包含任意一个关键词即可匹配

---

### 示例 4：按明细统计

**用户：** 按明细统计 3 月包含"篮球"的订单

**查询参数：**
- 开始时间：2026-03-01 00:00:00
- 结束时间：2026-03-31 00:00:00
- 关键词：篮球
- 统计维度：明细
- 业务版块：无

**输出字段：** 订单标题 | 订单描述 | 订单数 | 未支付 | 退款订单 | 支付金额 | 退款金额 | 销售占比 | 用户数

---

### 示例 5：业务版块筛选

**用户：** 统计 3 月票务板块的订单

**查询参数：**
- 开始时间：2026-03-01 00:00:00
- 结束时间：2026-03-31 00:00:00
- 关键词：无
- 统计维度：标题
- 业务版块：票务（TICKET_ORDER）

---

### 示例 6：组合筛选

**用户：** 统计 3 月票务板块包含"VIP"的订单，按明细统计

**查询参数：**
- 开始时间：2026-03-01 00:00:00
- 结束时间：2026-03-31 00:00:00
- 关键词：VIP
- 统计维度：明细
- 业务版块：票务（TICKET_ORDER）

---

## 版本更新记录

### v1.4（2026-03-07）
- ✅ 关键词搜索改为 LIKE 模糊匹配（更直观）
- ✅ 多关键词使用 OR 关系（包含任意一个即可）
- ✅ 支持逗号或空格分隔多个关键词

### v1.3（2026-03-06）
- ✅ 优化销售占比计算，使用 SUM() OVER() 窗口函数，确保总和为 100%
- ✅ 修复业务版块筛选逻辑错误（`if keyword` → `if order_type`）
- ✅ 统一订单状态枚举，包含所有未支付状态
- ✅ 完善 Python 代码模板和错误处理

### v1.2（2026-03-06）
- ✅ 修复业务版块筛选逻辑错误
- ✅ 统一关键词搜索方式为 MATCH AGAINST 全文搜索
- ✅ 新增未支付订单数字段
- ✅ 优化 WHERE 条件

### v1.1（之前版本）
- 支持动态调整查询维度（标题/明细）
- 支持业务版块筛选
- 支持关键词筛选

---

**一句话总结**：增强版 v1.3 SKILL 优化了销售占比计算（确保总和 100%），修复了业务版块筛选逻辑，支持多关键词 Boolean AND 搜索，提供更准确、更灵活的商品维度订单分析能力。
