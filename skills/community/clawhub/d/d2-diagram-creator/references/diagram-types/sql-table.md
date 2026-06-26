# SQL Table Diagram

## Use Cases

- Database table structure design
- ER Diagrams (Entity-Relationship)
- Data model documentation
- Table relationship visualization

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Table Shape | `shape: sql_table` | Define SQL table |
| Field Definition | `field_name: type` | Table columns |
| Primary Key | `constraint: primary_key` | Primary key field |
| Foreign Key | `constraint: foreign_key` | Foreign key field |
| Unique Constraint | `constraint: unique` | Unique field |
| Table Connection | `TableA.field -> TableB.field` | Foreign key relationship |

## Basic Example

```d2
direction: right

users: {
  shape: sql_table
  id: int {constraint: primary_key}
  username: varchar(50)
  email: varchar(100) {constraint: unique}
  created_at: timestamp
}
```

## Table with Constraints

### Single Constraint

```d2
products: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar(100)
  price: decimal(10,2)
  sku: varchar(20) {constraint: unique}
  created_at: timestamp
}
```

### Multiple Constraints

Use an array to specify multiple constraint conditions:

```d2
items: {
  shape: sql_table
  id: int {constraint: [primary_key; unique]}
  code: varchar(20) {constraint: [unique; not_null]}
  name: varchar(100)
}
```

## Table Relationships (Foreign Keys)

### One-to-Many Relationship

```d2
direction: right

users: {
  shape: sql_table
  id: int {constraint: primary_key}
  username: varchar(50)
  email: varchar(100)
}

orders: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: foreign_key}
  total: decimal(10,2)
  status: varchar(20)
}

orders.user_id -> users.id
```

### Multi-table Relationships

```d2
direction: right

users: {
  shape: sql_table
  id: int {constraint: primary_key}
  username: varchar(50)
  email: varchar(100)
}

posts: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: foreign_key}
  title: varchar(200)
  content: text
  created_at: timestamp
}

comments: {
  shape: sql_table
  id: int {constraint: primary_key}
  post_id: int {constraint: foreign_key}
  user_id: int {constraint: foreign_key}
  content: text
  created_at: timestamp
}

posts.user_id -> users.id
comments.post_id -> posts.id
comments.user_id -> users.id
```

## Nested in Containers

Organize tables into logical groups:

```d2
direction: right

cloud: {
  disks: {
    shape: sql_table
    id: int {constraint: primary_key}
    name: varchar(100)
    size_gb: int
  }

  blocks: {
    shape: sql_table
    id: int {constraint: primary_key}
    disk_id: int {constraint: foreign_key}
    data: blob
  }

  blocks.disk_id -> disks.id
}

AWS S3 -> cloud.disks
```

## Complete E-commerce Data Model

```d2
direction: right

User Module: {
  users: {
    shape: sql_table
    id: int {constraint: primary_key}
    username: varchar(50)
    email: varchar(100) {constraint: unique}
    password_hash: varchar(255)
    created_at: timestamp
  }

  addresses: {
    shape: sql_table
    id: int {constraint: primary_key}
    user_id: int {constraint: foreign_key}
    province: varchar(50)
    city: varchar(50)
    address: varchar(200)
  }

  addresses.user_id -> users.id
}

Product Module: {
  categories: {
    shape: sql_table
    id: int {constraint: primary_key}
    name: varchar(100)
    parent_id: int {constraint: foreign_key}
  }

  products: {
    shape: sql_table
    id: int {constraint: primary_key}
    category_id: int {constraint: foreign_key}
    name: varchar(200)
    price: decimal(10,2)
    stock: int
  }

  categories.parent_id -> categories.id
  products.category_id -> categories.id
}

Order Module: {
  orders: {
    shape: sql_table
    id: int {constraint: primary_key}
    user_id: int {constraint: foreign_key}
    address_id: int {constraint: foreign_key}
    total: decimal(10,2)
    status: varchar(20)
    created_at: timestamp
  }

  order_items: {
    shape: sql_table
    id: int {constraint: primary_key}
    order_id: int {constraint: foreign_key}
    product_id: int {constraint: foreign_key}
    quantity: int
    price: decimal(10,2)
  }

  orders.user_id -> User Module.users.id
  orders.address_id -> User Module.addresses.id
  order_items.order_id -> orders.id
  order_items.product_id -> Product Module.products.id
}
```

## Reserved Keyword Handling

If a field name is a reserved keyword, wrap it in quotes:

```d2
my_table: {
  shape: sql_table
  id: int {constraint: primary_key}
  "label": string
  "order": int
  "group": varchar(50)
}
```

## Supported Data Types

Common SQL data types:

| Type | Description |
|------|-------------|
| `int` / `integer` | Integer |
| `varchar(n)` | Variable-length string |
| `text` | Long text |
| `decimal(m,n)` | Exact decimal |
| `float` | Floating point |
| `boolean` / `bool` | Boolean |
| `date` | Date |
| `timestamp` | Timestamp |
| `json` / `jsonb` | JSON data |
| `blob` | Binary data |
| `uuid` | UUID identifier |

## Constraint Types

| Constraint | Description |
|------------|-------------|
| `primary_key` | Primary key |
| `foreign_key` | Foreign key |
| `unique` | Unique value |
| `not_null` | Not null |

## Design Principles

1. **Direction Layout** - Use `direction: right` for clearer relationship lines
2. **Logical Grouping** - Organize related tables into containers
3. **Label Relationships** - Add relationship descriptions on connection lines
4. **Naming Conventions** - Use consistent naming (snake_case recommended)

## Common Patterns

### Self-referencing Relationship

```d2
categories: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar(100)
  parent_id: int {constraint: foreign_key}
}

categories.parent_id -> categories.id: "Parent category"
```

### Many-to-Many Junction Table

```d2
direction: right

students: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar(100)
}

courses: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar(100)
}

enrollments: {
  shape: sql_table
  student_id: int {constraint: foreign_key}
  course_id: int {constraint: foreign_key}
  enrolled_at: timestamp
}

enrollments.student_id -> students.id
enrollments.course_id -> courses.id
```
