# 数据模型规范

## 概述
本文档定义数据库设计和数据模型标准，确保数据模型的一致性、可维护性和性能。

## 设计原则

### 1. 规范化
- 遵循第三范式（3NF）
- 避免数据冗余
- 保持数据完整性

### 2. 命名规范
- **表名**：使用复数形式，小写+下划线（snake_case）
- **字段名**：小写+下划线（snake_case）
- **索引名**：`idx_表名_字段名`
- **外键名**：`fk_表名_关联表名`

### 示例
```sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  user_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

## 表结构设计

### 基础字段
每个表应包含以下基础字段：
```sql
id BIGINT PRIMARY KEY AUTO_INCREMENT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
deleted_at TIMESTAMP NULL  -- 软删除
```

### 字段类型
- **ID**：使用BIGINT
- **字符串**：根据长度选择VARCHAR(n)
- **数字**：根据范围选择INT、BIGINT、DECIMAL
- **时间**：使用TIMESTAMP或DATETIME
- **布尔值**：使用TINYINT(1)或BOOLEAN

## 关系设计

### 一对一关系
```sql
CREATE TABLE user_profiles (
  id BIGINT PRIMARY KEY,
  user_id BIGINT UNIQUE NOT NULL,
  avatar_url VARCHAR(500),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 一对多关系
```sql
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  total_amount DECIMAL(10,2),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 多对多关系
```sql
CREATE TABLE user_roles (
  user_id BIGINT NOT NULL,
  role_id BIGINT NOT NULL,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (role_id) REFERENCES roles(id)
);
```

## 索引设计

### 主键索引
- 每个表必须有主键
- 使用自增ID或UUID

### 唯一索引
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### 普通索引
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

### 复合索引
```sql
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

## 约束设计

### 非空约束
```sql
email VARCHAR(255) NOT NULL
```

### 唯一约束
```sql
email VARCHAR(255) UNIQUE NOT NULL
```

### 外键约束
```sql
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

### 检查约束
```sql
CHECK (age >= 0 AND age <= 150)
```

## 数据迁移

### 迁移文件命名
```
001_create_users_table.sql
002_create_orders_table.sql
003_add_user_profile_table.sql
```

### 迁移脚本
```sql
-- 迁移脚本应包含up和down操作
-- Up migration
CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL
);

-- Down migration
DROP TABLE IF EXISTS users;
```

## 数据模型示例

### 用户模型
```typescript
interface User {
  id: number;
  name: string;
  email: string;
  passwordHash: string;
  createdAt: Date;
  updatedAt: Date;
  profile?: UserProfile;
  orders: Order[];
}
```

### 订单模型
```typescript
interface Order {
  id: number;
  userId: number;
  orderNumber: string;
  totalAmount: number;
  status: OrderStatus;
  items: OrderItem[];
  createdAt: Date;
}

enum OrderStatus {
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED'
}
```

## 数据访问

### MyBatis-Plus使用规范（Java项目）

#### Mapper接口规范
```java
@Mapper
public interface UserMapper extends BaseMapper<User> {
    // 基础CRUD已由BaseMapper提供，无需重复定义
    // 只定义复杂查询方法
    
    /**
     * 根据条件查询用户列表
     */
    @Select("SELECT * FROM users WHERE status = #{status} AND created_at >= #{startDate}")
    List<User> selectByCondition(@Param("status") String status, @Param("startDate") LocalDateTime startDate);
}
```

#### Service层规范
```java
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    
    /**
     * 使用LambdaQueryWrapper进行条件查询
     */
    public List<User> findActiveUsers() {
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(User::getStatus, "active")
               .ge(User::getCreatedAt, LocalDateTime.now().minusDays(30))
               .orderByDesc(User::getCreatedAt);
        return list(wrapper);
    }
    
    /**
     * 使用分页查询
     */
    public Page<User> findUsersByPage(int page, int size) {
        Page<User> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        return page(pageParam, wrapper);
    }
    
    /**
     * 批量操作
     */
    public boolean batchSave(List<User> users) {
        return saveBatch(users, 100); // 每批100条
    }
}
```

#### 条件构造器使用
```java
// 使用LambdaQueryWrapper（推荐，类型安全）
LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
wrapper.eq(User::getName, "张三")
       .like(User::getEmail, "@example.com")
       .between(User::getCreatedAt, startDate, endDate)
       .orderByDesc(User::getCreatedAt);

// 使用QueryWrapper（字符串方式，不推荐）
QueryWrapper<User> wrapper = new QueryWrapper<>();
wrapper.eq("name", "张三")
       .like("email", "@example.com");
```

### Repository接口（其他语言）
```typescript
interface UserRepository {
  findById(id: number): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: number): Promise<void>;
}
```

### 查询优化

#### SQL查询优化
```sql
-- 使用索引
SELECT * FROM users WHERE email = 'user@example.com';

-- 避免全表扫描
SELECT * FROM users WHERE name LIKE '%test%';  -- 避免

-- 使用分页
SELECT * FROM users LIMIT 20 OFFSET 0;
```

#### MyBatis-Plus查询优化
```java
// 只查询需要的字段
LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
wrapper.select(User::getId, User::getName, User::getEmail)
       .eq(User::getStatus, "active");

// 使用分页避免一次性加载大量数据
Page<User> page = new Page<>(1, 20);
page(page, wrapper);

// 使用批量操作提高性能
saveBatch(users, 100);
updateBatchById(users, 100);
```

## 数据验证

### 字段验证
```typescript
const userSchema = {
  name: {
    required: true,
    minLength: 2,
    maxLength: 100
  },
  email: {
    required: true,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  }
};
```

## 数据安全

### 敏感数据加密
- 密码：使用bcrypt哈希
- 敏感信息：使用AES加密
- 不在日志中记录敏感数据

### 数据备份
- 定期备份数据库
- 保留至少30天的备份
- 测试恢复流程

---

> **上下文提示**：在设计数据模型时，建议同时加载：
> - `coding.architecture.md` - 架构规范
> - `coding.api.md` - 接口规范
> - `coding.security.md` - 安全规范

