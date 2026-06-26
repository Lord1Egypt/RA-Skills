# Test Data Generation Patterns

## Overview

This document defines patterns and rules for generating realistic, business-compliant test data. The goal is to create data that:
- Maintains referential integrity
- Follows business rules
- Looks realistic for testing
- Covers edge cases

## Data Type Patterns

### String Patterns

#### Email Addresses
```python
# Pattern: user{number}@test.com
user123@test.com
user456@test.com

# With domain variety
user123@gmail.test.com
user456@company.test.com

# Special cases
test+special@test.com  # Plus addressing
```

#### Phone Numbers
```python
# Chinese mobile: 1 + 3/5/7/8/9 + 8 digits
13800138000
15912345678
18600001111

# International format
+8613800138000
+1-555-123-4567
```

#### Names
```python
# Chinese names (2-4 characters)
张三、李四、王五、赵六、钱七

# Western names
John Smith, Jane Doe, Bob Johnson

# Mix of both for international testing
张伟 (Zhang Wei), 李娜 (Li Na)
```

#### Addresses
```python
# Chinese format
北京市朝阳区建国路88号
上海市浦东新区张江高科技园区

# Western format
123 Main St, Apt 4B, New York, NY 10001
```

#### URLs
```python
# Test URLs
https://test.example.com
http://localhost:8080/api/v1
https://staging.company.com/products/123
```

### Numeric Patterns

#### IDs
```python
# Primary keys (auto-increment simulation)
1, 2, 3, 4, 5, ...

# Foreign keys (reference existing IDs)
# If users table has IDs 1-100
user_id: random.randint(1, 100)
```

#### Money/Prices
```python
# Reasonable price ranges
product_price: random.uniform(10, 10000)  # $10 - $10,000
order_total: random.uniform(100, 50000)   # $100 - $50,000

# Round to 2 decimal places
price: round(random.uniform(10, 1000), 2)
```

#### Quantities
```python
# Small quantities
quantity: random.randint(1, 100)

# Stock levels
stock: random.randint(0, 1000)

# Percentages
discount_rate: random.uniform(0, 1)  # 0.0 - 1.0
```

#### Age/Ratings
```python
# Age (reasonable range)
age: random.randint(18, 70)

# Ratings (1-5 stars)
rating: random.randint(1, 5)

# Scores (0-100)
score: random.randint(0, 100)
```

### Date/Time Patterns

#### Timestamps
```python
# Created at (past)
created_at: now - timedelta(days=random.randint(0, 365))

# Updated at (after created_at)
updated_at: created_at + timedelta(days=random.randint(0, 30))

# Future dates
expires_at: now + timedelta(days=random.randint(30, 365))
```

#### Date Ranges
```python
# Birth dates (18-70 years ago)
birth_date: now - timedelta(days=random.randint(18*365, 70*365))

# Event dates (future)
event_date: now + timedelta(days=random.randint(1, 90))

# Historical dates
transaction_date: now - timedelta(days=random.randint(0, 365))
```

#### Time Patterns
```python
# Business hours (9 AM - 6 PM)
business_time: time(random.randint(9, 18), random.randint(0, 59))

# Time slots (on the hour)
time_slot: f"{random.randint(9, 17)}:00:00"
```

### Boolean Patterns

```python
# Common status flags
is_active: random.choice([True, False])  # or weight toward True
is_verified: random.choice([True, False])
is_deleted: False  # Usually False, test soft-delete separately

# With probability weights
is_premium: random.choices([True, False], weights=[20, 80])[0]  # 20% premium users
```

## Business Domain Patterns

### E-commerce

#### Products
```python
{
    'id': auto_increment,
    'name': f"测试商品_{random.randint(1, 999)}",
    'sku': f"SKU{random.randint(100000, 999999)}",
    'price': round(random.uniform(10, 1000), 2),
    'stock': random.randint(0, 1000),
    'category_id': random.randint(1, 10),
    'status': random.choice(['active', 'inactive', 'out_of_stock']),
    'created_at': now - timedelta(days=random.randint(0, 365))
}
```

#### Orders
```python
{
    'id': auto_increment,
    'order_number': f"ORD{timestamp}{random.randint(1000, 9999)}",
    'user_id': random.randint(1, 1000),  # FK to users
    'total_amount': round(random.uniform(100, 5000), 2),
    'status': random.choice(['pending', 'paid', 'shipped', 'completed', 'cancelled']),
    'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer']),
    'shipping_address': f"测试地址{random.randint(1, 999)}号",
    'created_at': now - timedelta(days=random.randint(0, 90))
}
```

#### Order Items
```python
{
    'id': auto_increment,
    'order_id': random.randint(1, 10000),  # FK to orders
    'product_id': random.randint(1, 500),  # FK to products
    'quantity': random.randint(1, 5),
    'unit_price': round(random.uniform(10, 500), 2),
    'subtotal': quantity * unit_price
}
```

### User Management

#### Users
```python
{
    'id': auto_increment,
    'username': f"user{random.randint(1000, 9999)}",
    'email': f"user{random.randint(1, 10000)}@test.com",
    'phone': f"1{random.choice([3,5,7,8,9])}{random.randint(100000000, 999999999)}",
    'password_hash': hashlib.md5(f"password{random.randint(1, 100)}".encode()).hexdigest(),
    'nickname': random.choice(['张三', '李四', '王五', '赵六']),
    'age': random.randint(18, 60),
    'gender': random.choice(['M', 'F', 'Other']),
    'status': random.choice(['active', 'inactive', 'banned']),
    'is_verified': random.choice([True, False]),
    'created_at': now - timedelta(days=random.randint(0, 365))
}
```

#### User Profiles
```python
{
    'id': auto_increment,
    'user_id': random.randint(1, 1000),  # FK to users (unique)
    'avatar': f"https://test.example.com/avatars/{random.randint(1, 100)}.jpg",
    'bio': f"这是用户简介_{random.randint(1, 100)}",
    'address': f"测试地址{random.randint(1, 999)}号",
    'company': random.choice(['测试公司A', '测试公司B', '测试公司C']),
    'website': f"https://user{random.randint(1, 100)}.test.com"
}
```

### Content Management

#### Articles/Posts
```python
{
    'id': auto_increment,
    'title': f"测试文章_{random.randint(1, 999)}: 这是一篇测试文章",
    'content': f"这是文章内容...{lorem_ipsum_text}",
    'author_id': random.randint(1, 100),  # FK to users
    'category': random.choice(['tech', 'life', 'news', 'entertainment']),
    'tags': random.sample(['python', 'java', 'database', 'web', 'mobile'], k=random.randint(1, 3)),
    'status': random.choice(['draft', 'published', 'archived']),
    'view_count': random.randint(0, 10000),
    'like_count': random.randint(0, 1000),
    'published_at': now - timedelta(days=random.randint(0, 365)),
    'created_at': now - timedelta(days=random.randint(0, 365))
}
```

#### Comments
```python
{
    'id': auto_increment,
    'article_id': random.randint(1, 500),  # FK to articles
    'user_id': random.randint(1, 100),  # FK to users
    'parent_id': random.choice([None, random.randint(1, 100)]),  # For nested comments
    'content': f"这是评论内容_{random.randint(1, 999)}",
    'status': random.choice(['active', 'hidden', 'deleted']),
    'created_at': now - timedelta(days=random.randint(0, 90))
}
```

### Financial

#### Transactions
```python
{
    'id': auto_increment,
    'transaction_id': f"TXN{timestamp}{random.randint(10000, 99999)}",
    'user_id': random.randint(1, 1000),
    'type': random.choice(['deposit', 'withdrawal', 'transfer', 'payment']),
    'amount': round(random.uniform(100, 10000), 2),
    'balance_before': round(random.uniform(1000, 50000), 2),
    'balance_after': balance_before + amount,  # Or minus for withdrawal
    'status': random.choice(['pending', 'completed', 'failed', 'cancelled']),
    'description': f"交易描述_{random.randint(1, 999)}",
    'created_at': now - timedelta(days=random.randint(0, 365))
}
```

#### Accounts
```python
{
    'id': auto_increment,
    'user_id': random.randint(1, 1000),  # FK to users (unique)
    'account_number': f"ACC{random.randint(100000000, 999999999)}",
    'balance': round(random.uniform(0, 100000), 2),
    'currency': 'CNY',
    'status': random.choice(['active', 'frozen', 'closed']),
    'created_at': now - timedelta(days=random.randint(0, 365))
}
```

## Referential Integrity Patterns

### Parent-Child Relationships

#### Generate in Dependency Order
```python
# 1. Generate parent records first
for i in range(100):
    users.append(generate_user())

# 2. Then generate child records with valid FK references
for i in range(500):
    orders.append(generate_order(user_id=random.choice(users).id))

# 3. Then generate grandchildren
for i in range(1000):
    order_items.append(generate_order_item(
        order_id=random.choice(orders).id,
        product_id=random.choice(products).id
    ))
```

### Circular References

#### Handle self-referencing tables
```python
# Categories with parent_category_id
# Generate root categories first (parent_id = NULL)
root_categories = [generate_category(parent_id=None) for _ in range(5)]

# Then generate child categories
child_categories = []
for parent in root_categories:
    children = [generate_category(parent_id=parent.id) for _ in range(3)]
    child_categories.extend(children)
```

## Edge Cases and Special Values

### Boundary Values

```python
# Minimum values
quantity: 0  # Zero quantity
price: 0.01  # Minimum price
age: 18  # Minimum age

# Maximum values
quantity: 999999  # Large quantity
price: 999999.99  # Maximum price
age: 120  # Maximum realistic age

# Just above/below limits
stock: -1  # Invalid (for testing validation)
price: 0.00  # Free item
```

### NULL Values

```python
# Optional fields (10-20% NULL)
nickname: random.choice([None, f"昵称{random.randint(1, 100)}"])
bio: random.choice([None, f"简介{random.randint(1, 100)}"])

# Required fields (never NULL)
user_id: random.randint(1, 100)  # Always has value
created_at: now - timedelta(days=random.randint(0, 365))  # Always has value
```

### Unicode and Special Characters

```python
# Chinese characters
name: random.choice(['张三', '李四', '王五'])

# Emoji (for modern apps)
content: f"测试内容 {random.choice(['😀', '🎉', '👍', '❤️'])}"

# Special characters
description: f"特殊字符测试: <>&\"'{random.randint(1, 100)}"

# Mixed languages
title: f"测试Title{random.randint(1, 100)}_测试"
```

## Data Volume Guidelines

### Development Environment
```
Users: 100-1000
Products: 500-2000
Orders: 1000-5000
Order Items: 3000-10000
Comments: 500-2000
```

### Staging Environment
```
Users: 1000-10000
Products: 2000-10000
Orders: 10000-50000
Order Items: 30000-100000
Comments: 5000-20000
```

### Performance Testing
```
Users: 100000+
Products: 50000+
Orders: 1000000+
Order Items: 5000000+
```

## Example: Complete Table Generation

```python
# Define schema
user_schema = {
    'table_name': 'users',
    'columns': [
        {'name': 'id', 'type': 'BIGINT', 'is_primary_key': True},
        {'name': 'username', 'type': 'VARCHAR(50)'},
        {'name': 'email', 'type': 'VARCHAR(100)'},
        {'name': 'phone', 'type': 'VARCHAR(20)'},
        {'name': 'age', 'type': 'INT'},
        {'name': 'status', 'type': 'TINYINT'},
        {'name': 'created_at', 'type': 'TIMESTAMP'}
    ]
}

# Generate data
generator = TestDataGenerator()
users = generator.generate_for_table(user_schema, count=100)

# Generate SQL
statements = generator.generate_batch_insert('users', users, batch_size=100)

# Output
for stmt in statements:
    print(stmt)
```

## Best Practices

1. ✅ **Generate parent tables first** - Maintain referential integrity
2. ✅ **Use realistic value ranges** - Match production data distribution
3. ✅ **Include edge cases** - Test boundary conditions
4. ✅ **Respect constraints** - Don't violate FK or unique constraints
5. ✅ **Use batch inserts** - Better performance for large datasets
6. ✅ **Make data deterministic** - Use seeds for reproducible tests
7. ✅ **Include NULL values** - Test optional fields
8. ✅ **Use consistent formats** - Same phone format throughout
9. ✅ **Document patterns** - Comment special generation rules
10. ✅ **Validate after generation** - Check FK references exist
