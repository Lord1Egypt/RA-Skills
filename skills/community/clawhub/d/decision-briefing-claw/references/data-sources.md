# 数据源配置指南

## config/data-sources.json 结构

```json
{
  "sources": [
    {
      "name": "mysql_prod",
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "database": "production",
      "user": "readonly_user",
      "password": "${MYSQL_PASSWORD}",
      "queries": {
        "orders": "SELECT COUNT(*) as count, SUM(amount) as gmv FROM orders WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY",
        "new_users": "SELECT COUNT(*) as count FROM users WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY"
      }
    },
    {
      "name": "finance_api",
      "type": "api",
      "url": "https://finance.example.com/api/daily-summary",
      "method": "GET",
      "headers": { "Authorization": "Bearer ${FINANCE_API_TOKEN}" },
      "params": { "date": "{yesterday}" },
      "mapping": { "revenue": "data.revenue", "cost": "data.cost" }
    },
    {
      "name": "ops_bitable",
      "type": "feishu_bitable",
      "app_token": "YOUR_APP_TOKEN",
      "table_id": "YOUR_TABLE_ID",
      "date_field": "日期",
      "fields": ["DAU", "MAU", "转化率"]
    },
    {
      "name": "sales_csv",
      "type": "csv",
      "path": "/data/sales/daily.csv",
      "date_column": "date",
      "value_columns": ["sales", "refunds"]
    }
  ]
}
```

## 支持的数据源类型

| 类型 | type 值 | 依赖 |
|------|---------|------|
| MySQL | `mysql` | `sqlalchemy`, `pymysql` |
| PostgreSQL | `postgresql` | `sqlalchemy`, `psycopg2` |
| MongoDB | `mongodb` | `pymongo` |
| RESTful API | `api` | `requests` |
| Excel | `excel` | `openpyxl` |
| CSV | `csv` | `pandas` |
| 飞书多维表格 | `feishu_bitable` | OpenClaw Feishu 插件 |

## 常见错误处理

- **连接超时**：增加 `"connect_timeout": 10`
- **SSL 错误**：添加 `"ssl": {"ca": "/path/to/ca.pem"}`
- **API 限流**：配置 `"retry": {"max": 3, "backoff": 2}`
- **编码问题**：CSV/Excel 添加 `"encoding": "utf-8-sig"`
