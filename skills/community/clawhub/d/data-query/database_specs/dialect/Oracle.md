# Oracle 数据库 SQL 规范

## 一、基本规范

### 1. 日期转字符串
- 使用: `TO_CHAR(col, 'YYYY-MM')` 或 `TO_CHAR(col, 'YYYY-MM-DD')`

### 2. 字符串截取
- 使用: `SUBSTR(col, 1, 10)`（Oracle SUBSTR 从 1 开始计数）

### 3. 分页（三层子查询）
```sql
SELECT * FROM (
    SELECT t.*, ROWNUM rn FROM (
        SELECT * FROM table ORDER BY id
    ) t WHERE ROWNUM <= 20
) WHERE rn > 10
```

### 4. 空值处理
- `NVL(col, default)` 或 `COALESCE(col1, col2, default)`

### 5. 当前时间
- `SYSDATE` 返回当前日期时间
- `SYSTIMESTAMP` 返回带时区的时间戳

### 6. 字符串拼接
- `||` 运算符: `col1 || col2`
- 或 `CONCAT(col1, col2)`

## 二、与达梦的差异速查

| 场景 | Oracle | 达梦 DM |
|------|--------|---------|
| 日期转字符串 | `TO_CHAR(col, 'YYYY-MM')` | `SUBSTR(CAST(col AS VARCHAR), 1, 7)` |
| 分页 | 三层 ROWNUM 子查询 | `FETCH FIRST n ROWS ONLY` |
| 自增ID | `序列.NEXTVAL` 或 `IDENTITY` | `IDENTITY` |
| 字符串截取 | `SUBSTR(col, 1, 10)` | `SUBSTR(col, 1, 10)` |
