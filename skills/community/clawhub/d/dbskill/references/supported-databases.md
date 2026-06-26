# Supported databases · 支持的数据库

English | [中文](#支持的数据库)

<a id="支持的数据库"></a>

---

## MySQL 8+

| Property | Value |
|---|---|
| Driver | `pymysql` |
| JDBC URL | `jdbc:mysql://<host>:3306/<db>?useSSL=false&charset=utf8mb4` |
| Placeholder | `?` (auto-converted to `%s`) |
| Python lib | `pymysql>=1.1.0` |
| Schema | `SHOW FULL TABLES`, `SHOW FULL COLUMNS`, `SHOW INDEX` |

## PostgreSQL

| Property | Value |
|---|---|
| Driver | `psycopg2` |
| JDBC URL | `jdbc:postgresql://<host>:5432/<db>` |
| Placeholder | `?` (auto-converted to `%s`) |
| Python lib | `psycopg2-binary>=2.9.9` |
| Schema | `information_schema.tables`, `pg_class` |

## Oracle

| Property | Value |
|---|---|
| Driver | `oracledb` |
| JDBC URL | `jdbc:oracle:thin:@<host>:1521/<service>` |
| Placeholder | `?` (auto-converted to `%s`) |
| Python lib | `oracledb>=2.0.0` |
| Schema | `user_tables`, `user_tab_columns` |

## SQL Server

| Property | Value |
|---|---|
| Driver | `pymssql` |
| JDBC URL | `jdbc:sqlserver://<host>:1433;databaseName=<db>` |
| Placeholder | `?` (auto-converted to `%s`) |
| Python lib | `pymssql>=2.2.0` |
| Schema | `information_schema.tables`, `sys.indexes` |

## SQLite

| Property | Value |
|---|---|
| Driver | `sqlite3` (built-in) |
| JDBC URL | `jdbc:sqlite:<path>/file.db` or `jdbc:h2:mem:test` |
| Placeholder | `?` (auto-converted to `%s`) |
| Python lib | None (stdlib) |
| Schema | `sqlite_master`, `PRAGMA table_info` |

## Column name case sensitivity · 列名大小写

| Driver | Native casing | Wrapper |
|---|---|---|
| pymysql | lowercase | CaseInsensitiveDict |
| psycopg2 | lowercase | CaseInsensitiveDict |
| oracledb | uppercase | CaseInsensitiveDict |
| pymssql | lowercase | CaseInsensitiveDict |
| sqlite3 | as-defined | CaseInsensitiveDict |

## Adding a new database · 扩展新数据库

1. Add JDBC URL prefix to `_DRIVER_REGISTRY` in `connection_manager.py`.
2. Add lazy import function.
3. Add `_connect()` branch in `ConnectionManager`.
4. Add schema queries in `SchemaInspector`.
5. Add dependency to `pyproject.toml`.

1. 在 `connection_manager.py` 的 `_DRIVER_REGISTRY` 中注册 URL 前缀。
2. 添加惰性导入函数。
3. 在 `ConnectionManager._connect()` 中添加分支。
4. 在 `SchemaInspector` 中适配 Schema 查询。
5. 在 `pyproject.toml` 中添加依赖。
