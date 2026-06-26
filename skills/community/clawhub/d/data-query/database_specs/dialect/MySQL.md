# MySQL 数据库 SQL 规范

## 一、基本规范

### 1. 日期转字符串
- 使用: `DATE_FORMAT(col, '%Y-%m')` 或 `DATE_FORMAT(col, '%Y-%m-%d')`

### 2. 字符串截取
- 使用: `SUBSTR(col, 1, 10)`（MySQL SUBSTR 从 1 开始计数）

### 3. 分页
```sql
-- 第 11-20 条
SELECT * FROM table LIMIT 10, 10
-- 或
SELECT * FROM table LIMIT 10 OFFSET 10
```

### 4. 空值处理
- `IFNULL(col, default)` 或 `COALESCE(col1, col2, default)`

### 5. 当前时间
- `NOW()` 返回当前时间戳
- `CURDATE()` 返回当前日期

## 二、ShardingSphere 注意事项

### 分片键
- 确保 WHERE 条件包含分片键，否则会全路由
- 避免在分片键上使用函数

### 分页
- 分页查询在大数据量时性能较差，可结合游标分页

## 三、与达梦的差异速查

| 场景 | MySQL | 达梦 DM |
|------|-------|---------|
| 日期转字符串 | `DATE_FORMAT(col, '%Y-%m')` | `SUBSTR(CAST(col AS VARCHAR), 1, 7)` |
| 分页 | `LIMIT offset, count` | `FETCH FIRST n ROWS ONLY` |
| 自增ID | `AUTO_INCREMENT` | `IDENTITY` |
| 字符串截取 | `SUBSTR(col, 1, 10)` | `SUBSTR(col, 1, 10)` |
