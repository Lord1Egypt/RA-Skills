# 达梦数据库存储过程审查工具使用指南

## 工具概述

达梦数据库存储过程审查工具是专门为昌叔定制的达梦数据库开发和优化工具，主要功能包括：

1. **SQL语句分析**：识别达梦数据库中常见的语法和性能问题
2. **代码优化建议**：提供针对性的优化建议
3. **模板生成**：快速生成存储过程、函数和触发器模板
4. **格式化**：自动格式化SQL语句

## 常见问题及解决方案

### 1. 字符串连接问题
- **问题**：使用+号进行字符串连接
- **解决方案**：达梦数据库中字符串连接应使用 || 而不是 +
- **示例**：
  ```sql
  -- 错误写法
  SELECT 'Hello' + 'World' FROM dual;
  
  -- 正确写法
  SELECT 'Hello' || 'World' FROM dual;
  ```

### 2. 日期格式不匹配
- **问题**：TO_CHAR的日期格式与目标字段格式不一致
- **解决方案**：确保TO_CHAR的日期格式与目标字段格式一致
- **示例**：
  ```sql
  -- 如果字段是VARCHAR(YYYYMMDD)
  SELECT TO_CHAR(date_col, 'YYYYMMDD') FROM table_name;
  ```

### 3. Calendar表JOIN条件问题
- **问题**：Calendar表Date字段为VARCHAR时使用CAST进行JOIN
- **解决方案**：JOIN条件也应用TO_CHAR匹配
- **示例**：
  ```sql
  -- 正确写法
  JOIN Calendar c ON TO_CHAR(t.date_col, 'YYYYMMDD') = c.Date
  ```

### 4. GTT反复DROP/CREATE问题
- **问题**：在存储过程中反复DROP/CREATE GTT
- **解决方案**：使用TRUNCATE或直接INSERT，避免DROP/CREATE