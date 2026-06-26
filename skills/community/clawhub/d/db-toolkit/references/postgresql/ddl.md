# PostgreSQL DDL 参考

## 数据类型

### 数值类型
| 类型 | 说明 | 范围 |
|------|------|------|
| SMALLINT | 小整数 | -32768 ~ 32767 |
| INTEGER | 整数 | -2^31 ~ 2^31-1 |
| BIGINT | 大整数 | -2^63 ~ 2^63-1 |
| DECIMAL(p,s) | 精确小数 | 精度可控 |
| NUMERIC(p,s) | 精确小数 | 精度可控 |
| REAL | 单精度浮点 | 6位精度 |
| DOUBLE PRECISION | 双精度浮点 | 15位精度 |
| SERIAL | 自增整数 | 1 ~ 2^31-1 |
| BIGSERIAL | 自增大整数 | 1 ~ 2^63-1 |

### 字符串类型
| 类型 | 说明 | 最大长度 |
|------|------|----------|
| CHAR(n) | 定长字符串 | - |
| VARCHAR(n) | 变长字符串 | - |
| TEXT | 无限长文本 | 无限制 |

### 日期时间类型
| 类型 | 说明 | 格式 |
|------|------|------|
| DATE | 日期 | YYYY-MM-DD |
| TIME | 时间 | HH:MM:SS |
| TIMESTAMP | 日期时间 | YYYY-MM-DD HH:MM:SS |
| TIMESTAMPTZ | 带时区时间戳 | YYYY-MM-DD HH:MM:SS+TZ |
| INTERVAL | 时间间隔 | - |

### 特殊类型
| 类型 | 说明 |
|------|------|
| JSON | JSON 数据 |
| JSONB | 二进制 JSON（更快） |
| UUID | 通用唯一标识符 |
| ARRAY | 数组类型 |

## 创建表

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    status SMALLINT DEFAULT 1,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_status CHECK (status IN (0, 1))
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- 添加注释
COMMENT ON TABLE users IS '用户表';
COMMENT ON COLUMN users.status IS '1:active, 0:inactive';
```

## 修改表

```sql
-- 添加列
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- 修改列类型
ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(100);

-- 设置非空
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- 删除非空约束
ALTER TABLE users ALTER COLUMN phone DROP NOT NULL;

-- 删除列
ALTER TABLE users DROP COLUMN phone;

-- 添加索引
CREATE INDEX idx_users_status ON users(status);

-- 删除索引
DROP INDEX idx_users_status;

-- 添加外键
ALTER TABLE orders 
ADD CONSTRAINT fk_user_id 
FOREIGN KEY (user_id) REFERENCES users(id);
```

## 删除表

```sql
-- 删除表（如果存在）
DROP TABLE IF EXISTS users CASCADE;

-- 清空表（保留结构）
TRUNCATE TABLE users;
-- 重置序列
TRUNCATE TABLE users RESTART IDENTITY;
```

## 查看表结构

```sql
-- 查看表结构
\d users

-- 查看所有表
\dt

-- 查看建表语句
SELECT 
    'CREATE TABLE ' || tablename || ' (' ||
    string_agg(column_name || ' ' || data_type, ', ') ||
    ');'
FROM information_schema.columns 
WHERE table_name = 'users'
GROUP BY tablename;
```

## 序列操作

```sql
-- 创建序列
CREATE SEQUENCE user_id_seq;

-- 获取下一个值
SELECT nextval('user_id_seq');

-- 获取当前值
SELECT currval('user_id_seq');

-- 重置序列
ALTER SEQUENCE user_id_seq RESTART WITH 1;
```
