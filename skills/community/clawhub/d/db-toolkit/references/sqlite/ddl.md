# SQLite DDL 参考

## 数据类型

SQLite 使用动态类型系统，实际存储类型与声明类型可以不同。

### 存储类
| 类型 | 说明 |
|------|------|
| NULL | 空值 |
| INTEGER | 有符号整数（1/2/3/4/6/8 字节） |
| REAL | 浮点数（8 字节） |
| TEXT | UTF-8/UTF-16 字符串 |
| BLOB | 二进制数据 |

### 类型亲和性（推荐声明）
| 声明类型 | 亲和性 |
|----------|--------|
| INT, INTEGER, BIGINT, SMALLINT | INTEGER |
| CHAR, VARCHAR, TEXT, CLOB | TEXT |
| BLOB | BLOB |
| REAL, DOUBLE, FLOAT | REAL |
| NUMERIC, DECIMAL, BOOLEAN, DATE, DATETIME | NUMERIC |

## 创建表

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    status INTEGER DEFAULT 1,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 带约束的表
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'cancelled')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 修改表

SQLite 对 ALTER TABLE 支持有限，复杂修改需要重建表。

```sql
-- 添加列
ALTER TABLE users ADD COLUMN phone TEXT;

-- 重命名表
ALTER TABLE users RENAME TO members;

-- 重命名列（SQLite 3.25.0+）
ALTER TABLE users RENAME COLUMN username TO name;

-- 删除列（SQLite 3.35.0+）
ALTER TABLE users DROP COLUMN phone;

-- 复杂修改：重建表
-- 1. 创建新表
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
    -- 新结构
);

-- 2. 复制数据
INSERT INTO users_new (id, username, email)
SELECT id, username, email FROM users;

-- 3. 删除旧表
DROP TABLE users;

-- 4. 重命名新表
ALTER TABLE users_new RENAME TO users;

-- 5. 重建索引
CREATE INDEX idx_users_username ON users(username);
```

## 删除表

```sql
-- 删除表（如果存在）
DROP TABLE IF EXISTS users;

-- 清空表（保留结构）
-- SQLite 没有直接的 TRUNCATE，使用 DELETE
DELETE FROM users;
-- 重置自增 ID
DELETE FROM sqlite_sequence WHERE name = 'users';
```

## 查看表结构

```sql
-- 查看表结构
.schema users

-- 或使用 PRAGMA
PRAGMA table_info(users);

-- 查看所有表
.tables

-- 查看索引
PRAGMA index_list(users);
PRAGMA index_info(idx_users_username);

-- 查看外键
PRAGMA foreign_key_list(users);
```

## 启用外键约束

```sql
-- SQLite 默认不启用外键约束
PRAGMA foreign_keys = ON;

-- 永久启用（每次连接都要执行）
-- 或在应用启动时执行
```

## 特殊功能

```sql
-- 全文搜索
CREATE VIRTUAL TABLE posts_fts USING fts5(title, content);

-- JSON 扩展（SQLite 3.38.0+）
SELECT json_extract(metadata, '$.name') FROM users;
```
