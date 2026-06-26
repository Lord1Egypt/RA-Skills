# Connection management · 连接管理

English | [中文](#连接管理)

The connector uses **direct driver connections** (no connection pool).
`ConnectionManager` handles connect / disconnect lifecycle.

<a id="连接管理"></a>

连接器使用**直连模式**（无连接池），由 `ConnectionManager` 统一管理连接生命周期。

---

## Driver mapping · 驱动映射

| Database | Python driver | Install |
|---|---|---|
| MySQL | `pymysql` | `pip install pymysql` |
| PostgreSQL | `psycopg2` | `pip install psycopg2-binary` |
| Oracle | `oracledb` | `pip install oracledb` |
| SQL Server | `pymssql` | `pip install pymssql` |
| SQLite / H2 | `sqlite3` | Built-in |

## Connection modes · 连接模式

| Scenario | Method | autocommit |
|---|---|---|
| Normal queries | `get_connection()` | `True` |
| Transactions | `get_connection_for_transaction()` | `False` |

## Transaction isolation · 事务隔离

`execute_transaction` uses `_TxConnectionManager` to route all connections
to the same underlying connection:

```python
class _TxConnectionManager(ConnectionManager):
    def get_connection(self): return tx_conn
    def get_connection_for_transaction(self): return tx_conn
    def close_connection(self, conn): pass
```

## Safe close · 安全关闭

```python
@staticmethod
def close_connection(conn):
    if conn is None:
        return
    try:
        conn.close()
    except Exception:
        logger.debug("Ignored error while closing connection", exc_info=True)
```
