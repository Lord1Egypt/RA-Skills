# cashbook 数据模型

## accounts（账户）

```sql
CREATE TABLE accounts (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname    TEXT NOT NULL,           -- 用户自定义名称，如"招行储蓄卡"
  type        TEXT NOT NULL,           -- debit | credit | wallet
  last4       TEXT,                    -- 卡号尾号（可选）
  currency    TEXT DEFAULT 'CNY',
  balance     REAL DEFAULT 0,
  created_at  TEXT DEFAULT (datetime('now','localtime'))
);
```

## categories（分类）

```sql
CREATE TABLE categories (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  name      TEXT NOT NULL UNIQUE,
  type      TEXT NOT NULL,             -- expense | income
  icon      TEXT,                      -- emoji，可选
  builtin   INTEGER DEFAULT 0          -- 1=预置分类，0=用户自定义
);
```

## transactions（流水）

```sql
CREATE TABLE transactions (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  amount       REAL NOT NULL,
  type         TEXT NOT NULL,          -- expense | income | transfer
  category_id  INTEGER REFERENCES categories(id),
  account_id   INTEGER REFERENCES accounts(id),
  note         TEXT,
  merchant     TEXT,
  date         TEXT NOT NULL,          -- YYYY-MM-DD
  created_at   TEXT DEFAULT (datetime('now','localtime')),
  source       TEXT DEFAULT 'manual'   -- manual | nlp | screenshot | import
);
```

## budgets（预算）

```sql
CREATE TABLE budgets (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  category_id INTEGER REFERENCES categories(id),  -- NULL = 总预算
  amount      REAL NOT NULL,
  period      TEXT NOT NULL,           -- monthly | weekly
  active      INTEGER DEFAULT 1,
  created_at  TEXT DEFAULT (datetime('now','localtime'))
);
```

## config（配置键值）

```sql
CREATE TABLE config (
  key   TEXT PRIMARY KEY,
  value TEXT
);
```

常用 key：`default_account_id`、`currency`、`timezone`、`db_version`
