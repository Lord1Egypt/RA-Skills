# MySQL DDL 参考

## 数据类型

### 数值类型
| 类型 | 说明 | 范围 |
|------|------|------|
| TINYINT | 微整数 | -128 ~ 127 |
| SMALLINT | 小整数 | -32768 ~ 32767 |
| INT | 整数 | -2^31 ~ 2^31-1 |
| BIGINT | 大整数 | -2^63 ~ 2^63-1 |
| DECIMAL(p,s) | 精确小数 | 精度可控 |
| FLOAT | 单精度浮点 | 近似值 |
| DOUBLE | 双精度浮点 | 近似值 |

### 字符串类型
| 类型 | 说明 | 最大长度 |
|------|------|----------|
| CHAR(n) | 定长字符串 | 255 |
| VARCHAR(n) | 变长字符串 | 65535 |
| TEXT | 长文本 | 65535 |
| MEDIUMTEXT | 中等文本 | 16MB |
| LONGTEXT | 长文本 | 4GB |

### 日期时间类型
| 类型 | 说明 | 格式 |
|------|------|------|
| DATE | 日期 | YYYY-MM-DD |
| TIME | 时间 | HH:MM:SS |
| DATETIME | 日期时间 | YYYY-MM-DD HH:MM:SS |
| TIMESTAMP | 时间戳 | YYYY-MM-DD HH:MM:SS |
| YEAR | 年份 | YYYY |

## 创建表

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    status TINYINT DEFAULT 1 COMMENT '1:active, 0:inactive',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

## 修改表

```sql
-- 添加列
ALTER TABLE users ADD COLUMN phone VARCHAR(20) AFTER email;

-- 修改列
ALTER TABLE users MODIFY COLUMN username VARCHAR(100) NOT NULL;

-- 删除列
ALTER TABLE users DROP COLUMN phone;

-- 添加索引
ALTER TABLE users ADD INDEX idx_status (status);

-- 删除索引
ALTER TABLE users DROP INDEX idx_status;

-- 添加外键
ALTER TABLE orders 
ADD CONSTRAINT fk_user_id 
FOREIGN KEY (user_id) REFERENCES users(id);
```

## 删除表

```sql
-- 删除表（如果存在）
DROP TABLE IF EXISTS users;

-- 清空表（保留结构）
TRUNCATE TABLE users;
```

## 查看表结构

```sql
-- 查看表结构
DESCRIBE users;
DESC users;

-- 查看建表语句
SHOW CREATE TABLE users;

-- 查看所有表
SHOW TABLES;
```
