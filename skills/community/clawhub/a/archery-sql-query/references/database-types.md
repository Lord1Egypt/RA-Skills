# 支持的数据库类型

本 skill 支持以下数据库类型：

## TiDB

- **类型**: 分布式 SQL 数据库
- **特点**: 兼容 MySQL 协议，支持水平扩展
- **适用场景**: 大规模数据查询

## MySQL

- **类型**: 关系型数据库
- **特点**: 成熟稳定，生态完善
- **适用场景**: 通用业务查询

## StarRocks

- **类型**: 实时分析型数据库
- **特点**: 高性能 OLAP 查询
- **适用场景**: 数据分析、报表查询

## 其他支持的数据库

- PostgreSQL
- MariaDB
- 其他 MySQL 协议兼容的数据库

## 使用示例

```bash
# TiDB 查询
python3 archery_query.py --instance "your-tidb-instance" --db "your-database" "SELECT * FROM your_table LIMIT 10"

# MySQL 查询
python3 archery_query.py --instance "your-mysql-instance" --db "your-database" "SELECT * FROM your_table LIMIT 10"

# StarRocks 查询
python3 archery_query.py --instance "your-starrocks-instance" --db "your-database" "SELECT * FROM your_table LIMIT 10"
```

## 注意事项

1. 不同数据库类型的 SQL 语法可能略有差异
2. StarRocks 主要用于分析查询，支持聚合函数
3. TiDB 支持大部分 MySQL 语法
