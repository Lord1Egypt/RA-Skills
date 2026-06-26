# Database Design Standards and Naming Conventions

## Naming Conventions

### Table Naming

1. **Use lowercase letters, numbers, and underscores only**
   ```
   ✅ Good: users, order_items, product_categories
   ❌ Bad: Users, OrderItems, ProductCategories
   ```

2. **Use plural names for tables**
   ```
   ✅ Good: users, orders, products
   ❌ Bad: user, order, product
   ```

3. **Use snake_case (not camelCase)**
   ```
   ✅ Good: user_profiles, order_history
   ❌ Bad: userProfiles, orderHistory
   ```

4. **Avoid reserved keywords**
   ```
   ❌ Bad: order, group, select, index, key, value
   ✅ Good: orders, user_groups, selection, indexes, key_value
   ```

5. **Prefix tables by module/domain (optional but recommended)**
   ```
   ✅ Good: 
      - auth_users, auth_roles (authentication module)
      - pay_orders, pay_transactions (payment module)
      - inv_products, inv_inventory (inventory module)
   ```

### Column Naming

1. **Use lowercase letters, numbers, and underscores**
   ```
   ✅ Good: user_id, created_at, order_total
   ❌ Bad: userId, createdAt, orderTotal
   ```

2. **Use singular names for columns**
   ```
   ✅ Good: user_name, email_address
   ❌ Bad: users_name, email_addresses
   ```

3. **Primary key should be `id` or `{table}_id`**
   ```
   ✅ Good: 
      - id (auto-increment)
      - user_id (if more descriptive needed)
   ```

4. **Foreign key should be `{referenced_table}_id`**
   ```
   ✅ Good: user_id, order_id, product_id
   ❌ Bad: uid, oid, pid
   ```

5. **Boolean columns should use `is_`, `has_`, or `can_` prefix**
   ```
   ✅ Good: is_active, has_verified, can_edit
   ❌ Bad: active, verified, editable
   ```

6. **Date/time columns should have appropriate suffixes**
   ```
   ✅ Good: 
      - created_at, updated_at, deleted_at (timestamps)
      - birth_date, start_date, end_date (dates)
   ```

### Index Naming

1. **Primary key index: `pk_{table}`**
   ```
   ✅ Good: pk_users, pk_orders
   ```

2. **Unique index: `uk_{table}_{columns}`**
   ```
   ✅ Good: uk_users_email, uk_orders_order_number
   ```

3. **Regular index: `idx_{table}_{columns}`**
   ```
   ✅ Good: idx_users_name, idx_orders_user_id
   ```

4. **Composite index: `idx_{table}_{col1}_{col2}`**
   ```
   ✅ Good: idx_orders_user_created, idx_products_category_status
   ```

5. **Foreign key index: `fk_{table}_{referenced_table}`**
   ```
   ✅ Good: fk_orders_users, fk_order_items_orders
   ```

## Data Type Standards

### Numeric Types

| Type | Usage | Example |
|------|-------|---------|
| TINYINT | Small integers, flags, status | status TINYINT DEFAULT 0 |
| SMALLINT | Small range values | age SMALLINT |
| INT | Primary keys, counts, IDs | id INT AUTO_INCREMENT PRIMARY KEY |
| BIGINT | Large IDs, counts, timestamps | id BIGINT AUTO_INCREMENT PRIMARY KEY |
| DECIMAL(p,s) | Money, precise decimals | price DECIMAL(10,2) |
| FLOAT | Approximate decimals | distance FLOAT |

**Rules:**
- Always use INT or BIGINT for primary keys
- Use DECIMAL for money, never FLOAT
- Choose smallest type that fits the range

### String Types

| Type | Usage | Max Length |
|------|-------|------------|
| CHAR(n) | Fixed-length strings | 255 |
| VARCHAR(n) | Variable-length strings | 65535 |
| TEXT | Long text content | 65535 |
| MEDIUMTEXT | Medium-length text | 16MB |
| LONGTEXT | Very long text | 4GB |

**Rules:**
- Use VARCHAR for variable-length strings up to 255 chars
- Use TEXT for longer content
- Specify reasonable length limits
  - email: VARCHAR(100)
  - phone: VARCHAR(20)
  - name: VARCHAR(50)
  - title: VARCHAR(200)
  - description: TEXT

### Date and Time Types

| Type | Format | Usage |
|------|--------|-------|
| DATE | YYYY-MM-DD | Birth dates, events |
| TIME | HH:MM:SS | Time only |
| DATETIME | YYYY-MM-DD HH:MM:SS | Timestamps with time zone |
| TIMESTAMP | Unix timestamp | Auto-updating timestamps |

**Rules:**
- Use TIMESTAMP for created_at, updated_at (auto-update)
- Use DATETIME for business dates that should not auto-update
- Use DATE for date-only values (birth_date, event_date)

## Primary Key Standards

### Rules

1. **Every table MUST have a primary key**
   ```sql
   ✅ Good:
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50)
   );
   
   ❌ Bad:
   CREATE TABLE users (
       name VARCHAR(50)
   );
   ```

2. **Use auto-increment integers or UUIDs**
   ```sql
   -- Auto-increment (recommended)
   id INT AUTO_INCREMENT PRIMARY KEY
   
   -- Or UUID (for distributed systems)
   id CHAR(36) PRIMARY KEY DEFAULT (UUID())
   ```

3. **Keep primary key immutable**
   - Never update primary key values
   - Don't use business data as primary key

## Foreign Key Standards

### Rules

1. **Always define foreign key constraints**
   ```sql
   ✅ Good:
   CREATE TABLE orders (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users(id) 
           ON DELETE RESTRICT
           ON UPDATE CASCADE
   );
   ```

2. **Choose appropriate ON DELETE action**
   - `RESTRICT`: Prevent deletion (default, safest)
   - `CASCADE`: Delete related records
   - `SET NULL`: Set to NULL (if column allows NULL)
   - `NO ACTION`: Same as RESTRICT

3. **Index foreign key columns**
   ```sql
   CREATE INDEX idx_orders_user_id ON orders(user_id);
   ```

## NOT NULL Standards

### Rules

1. **Primary keys: always NOT NULL**
   ```sql
   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
   ```

2. **Foreign keys: prefer NOT NULL**
   ```sql
   user_id INT NOT NULL  -- Required relationship
   deleted_by INT NULL   -- Optional relationship
   ```

3. **Business-critical fields: NOT NULL with DEFAULT**
   ```sql
   status TINYINT NOT NULL DEFAULT 0,
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
   ```

4. **Optional fields: allow NULL**
   ```sql
   nickname VARCHAR(50) NULL,
   bio TEXT NULL,
   deleted_at TIMESTAMP NULL
   ```

## Default Value Standards

### Rules

1. **Always provide defaults for NOT NULL columns**
   ```sql
   status TINYINT NOT NULL DEFAULT 0,
   is_active BOOLEAN NOT NULL DEFAULT TRUE,
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
   ```

2. **Use meaningful defaults**
   ```sql
   ✅ Good:
   role VARCHAR(20) NOT NULL DEFAULT 'user',
   currency VARCHAR(3) NOT NULL DEFAULT 'CNY'
   
   ❌ Bad:
   role VARCHAR(20) NOT NULL DEFAULT ''
   ```

3. **TIMESTAMP auto-update**
   ```sql
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   ```

## Index Standards

### When to Create Indexes

1. **Primary key** (automatically indexed)
2. **Foreign key columns**
3. **Columns in WHERE clauses**
4. **Columns in ORDER BY / GROUP BY**
5. **Columns used in JOINs**
6. **Unique constraint columns**

### Index Design Rules

1. **Use composite indexes for multiple conditions**
   ```sql
   -- Query: WHERE status = ? AND created_at > ?
   CREATE INDEX idx_orders_status_created ON orders(status, created_at);
   ```

2. **Order matters in composite indexes**
   ```sql
   -- Good for: WHERE status = ? AND user_id = ?
   -- Good for: WHERE status = ?
   -- Bad for: WHERE user_id = ?
   CREATE INDEX idx_orders_status_user ON orders(status, user_id);
   ```

3. **Avoid redundant indexes**
   ```sql
   ❌ Bad:
   INDEX idx_user (user_id),
   INDEX idx_user_status (user_id, status)  -- idx_user is redundant
   
   ✅ Good:
   INDEX idx_user_status (user_id, status)  -- Covers both queries
   ```

## Table Structure Example

```sql
CREATE TABLE orders (
    -- Primary key
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    -- Foreign keys
    user_id BIGINT NOT NULL COMMENT 'User ID',
    product_id BIGINT NOT NULL COMMENT 'Product ID',
    
    -- Business fields
    order_number VARCHAR(32) NOT NULL COMMENT 'Order number',
    total_amount DECIMAL(10,2) NOT NULL COMMENT 'Total amount',
    status TINYINT NOT NULL DEFAULT 0 COMMENT 'Order status: 0-pending, 1-paid, 2-shipped, 3-completed, 4-cancelled',
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time',
    deleted_at TIMESTAMP NULL COMMENT 'Soft delete time',
    
    -- Unique constraints
    UNIQUE KEY uk_order_number (order_number),
    
    -- Indexes
    KEY idx_user_id (user_id),
    KEY idx_product_id (product_id),
    KEY idx_status_created (status, created_at),
    
    -- Foreign keys
    CONSTRAINT fk_orders_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_orders_products FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Orders table';
```

## Common Violations

### 1. Missing Primary Key
```sql
❌ Bad:
CREATE TABLE user_settings (
    user_id INT,
    setting_key VARCHAR(50),
    setting_value TEXT
);

✅ Good:
CREATE TABLE user_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    setting_key VARCHAR(50) NOT NULL,
    setting_value TEXT,
    UNIQUE KEY uk_user_setting (user_id, setting_key)
);
```

### 2. Inconsistent Naming
```sql
❌ Bad:
CREATE TABLE UserProfiles (
    UserID INT,
    FirstName VARCHAR(50),
    created_Time TIMESTAMP
);

✅ Good:
CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Wrong Data Type
```sql
❌ Bad:
price VARCHAR(20),  -- Money stored as string
age TINYINT,        -- OK, but could be inconsistent
phone INT           -- Leading zeros lost

✅ Good:
price DECIMAL(10,2),
age TINYINT UNSIGNED,
phone VARCHAR(20)
```

### 4. Missing Foreign Key Constraints
```sql
❌ Bad:
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT  -- No constraint
);

✅ Good:
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 5. Missing Indexes on Foreign Keys
```sql
❌ Bad:
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
    -- Missing index on user_id
);

✅ Good:
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    KEY idx_user_id (user_id)
);
```
