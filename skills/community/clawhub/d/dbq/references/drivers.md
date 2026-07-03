# 数据库驱动安装指南

## MySQL / MariaDB

```bash
pip install pymysql
```

## PostgreSQL

```bash
pip install psycopg2-binary
```

## YAML 配置支持 (可选)

如果使用 YAML 格式配置文件:

```bash
pip install pyyaml
```

如果未安装 PyYAML，可用 JSON 格式配置文件 (`assets/connections.json`) 代替。

## 连接示例

### MySQL 8.x+

```yaml
connections:
  mydb:
    type: mysql
    host: 10.18.122.60
    port: 3306
    user: readonly
    password: ${DB_PASS}
    database: mydb
    charset: utf8mb4
    connect_timeout: 10
```

### PostgreSQL 14+

```yaml
connections:
  analytics:
    type: postgresql
    host: 192.168.88.5
    port: 5432
    user: postgres
    password: ${PG_PASS}
    database: analytics
```
