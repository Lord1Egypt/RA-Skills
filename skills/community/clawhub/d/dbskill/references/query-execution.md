# Query execution · 查询执行

English | [中文](#查询执行)

`QueryExecutor` provides four execution modes, all supporting **parameterized
bindings** to prevent SQL injection.

<a id="查询执行"></a>

`QueryExecutor` 提供四种执行模式，全部支持**参数化绑定**以防止 SQL 注入。

---

## Placeholder conversion · 占位符转换

Accepts JDBC-style `?` placeholders, auto-converted to Python `%s`:

支持 JDBC 风格的 `?` 占位符，自动转为 Python 的 `%s`：

```python
_PLACEHOLDER_RE = re.compile(r"(?<!\?)\?(?!\?)")
def convert_placeholders(sql: str) -> str:
    return _PLACEHOLDER_RE.sub("%s", sql)
```

## Result wrapping · 结果包装

All query results are wrapped in `CaseInsensitiveDict`:

```python
d = CaseInsensitiveDict({"Name": "Alice"})
d["name"]   # "Alice"
d["NAME"]   # "Alice"
d["Name"]   # "Alice"
```

## Four execution modes · 四种执行模式

```python
# SELECT
results = executor.execute_query("SELECT * FROM users WHERE status = ?", "ACTIVE")

# UPDATE / INSERT / DELETE
affected = executor.execute_update("UPDATE users SET status = ? WHERE id = ?", "INACTIVE", 1)

# Batch · 批量
results = executor.execute_batch(["INSERT INTO log VALUES (1)", "INSERT INTO log VALUES (2)"])

# Transaction · 事务
executor.execute_transaction(lambda tx: (
    tx.execute_update("UPDATE accounts SET balance = balance - 100 WHERE id = ?", 1),
    tx.execute_update("UPDATE accounts SET balance = balance + 100 WHERE id = ?", 2),
))
```
