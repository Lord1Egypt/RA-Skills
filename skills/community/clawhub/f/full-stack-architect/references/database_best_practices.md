# 数据库最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、数据库选型

### 1.1 关系型数据库 vs 非关系型数据库

**关系型数据库 (RDBMS)：**
- **优势**：ACID事务、强一致性、结构化查询、成熟的生态
- **适用场景**：金融系统、电商交易、需要复杂查询的应用
- **代表**：MySQL, PostgreSQL, Oracle, SQL Server

**非关系型数据库 (NoSQL)：**
- **优势**：高扩展性、灵活的数据模型、高性能
- **适用场景**：大数据、实时应用、IoT、社交网络
- **代表**：MongoDB, Redis, Cassandra, DynamoDB

**选型建议：**
- 数据结构复杂且关系明确 → 关系型
- 数据结构灵活且需要水平扩展 → 非关系型
- 混合使用：关键数据用关系型，非结构化数据用NoSQL

---

### 1.2 数据库选择考量因素

**1. 数据模型**
- 结构化 vs 半结构化 vs 非结构化
- 关系复杂度
- 查询模式

**2. 性能需求**
- 读写比例
- 并发处理能力
- 响应时间要求

**3. 可扩展性**
- 数据增长预测
- 水平扩展能力
- 地理分布需求

**4. 可靠性**
- 数据一致性要求
- 容错能力
- 备份恢复策略

**5. 成本**
- 硬件成本
- 软件许可
- 维护成本
- 云服务费用

---

## 二、关系型数据库最佳实践

### 2.1 表设计

**规范化原则：**
- **第一范式**：原子性，每个列不可再分
- **第二范式**：完全依赖于主键
- **第三范式**：消除传递依赖

**反规范化：**
- 适当的反规范化可以提高查询性能
- 常用于数据仓库和报表系统
- 平衡规范化和性能需求

**表设计示例：**

```sql
-- 用户表
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL,
  status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

### 2.2 索引优化

**索引类型：**
- **主键索引**：唯一且非空
- **唯一索引**：确保列值唯一
- **普通索引**：加速查询
- **复合索引**：多列组合索引
- **全文索引**：文本搜索

**创建索引：**

```sql
-- 普通索引
CREATE INDEX idx_users_email ON users(email);

-- 复合索引
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**索引最佳实践：**
- 为经常查询的列创建索引
- 为外键列创建索引
- 避免过多索引（影响写入性能）
- 考虑索引选择性
- 定期重建索引

---

### 2.3 查询优化

**避免全表扫描：**
- 使用WHERE子句过滤数据
- 为查询列创建索引
- 避免使用SELECT *

**优化JOIN操作：**
- 使用适当的JOIN类型（INNER, LEFT, RIGHT）
- 小表驱动大表
- 为JOIN列创建索引

**分页查询：**

```sql
-- 优化前
SELECT * FROM users LIMIT 10000, 10;

-- 优化后
SELECT * FROM users 
WHERE id > (SELECT id FROM users ORDER BY id LIMIT 10000, 1) 
ORDER BY id LIMIT 10;
```

**使用EXPLAIN分析查询：**

```sql
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```

---

### 2.4 事务管理

**ACID特性：**
- **原子性**：事务要么全部完成，要么全部失败
- **一致性**：事务前后数据状态一致
- **隔离性**：事务之间互不干扰
- **持久性**：事务结果永久保存

**事务隔离级别：**
- **READ UNCOMMITTED**：最低隔离级别，可能读取未提交数据
- **READ COMMITTED**：读取已提交数据，避免脏读
- **REPEATABLE READ**：同一事务中多次读取结果一致
- **SERIALIZABLE**：最高隔离级别，完全串行化

**事务示例：**

```sql
START TRANSACTION;

-- 扣减库存
UPDATE products SET stock = stock - 1 WHERE id = 1;

-- 创建订单
INSERT INTO orders (user_id, product_id, quantity) VALUES (1, 1, 1);

-- 提交事务
COMMIT;
-- 或回滚
-- ROLLBACK;
```

---

## 三、MongoDB 最佳实践

### 3.1 数据模型设计

**文档结构：**
- 嵌入式文档 vs 引用
- 适合文档大小（最大16MB）
- 读写模式考虑

**嵌入式示例：**

```javascript
// 嵌入式结构
{
  _id: ObjectId("60d5f4e3e3e3e3e3e3e3e3e3"),
  name: "John Doe",
  email: "john@example.com",
  addresses: [
    {
      street: "123 Main St",
      city: "New York",
      zip: "10001"
    },
    {
      street: "456 Oak Ave",
      city: "Boston",
      zip: "02110"
    }
  ]
}
```

**引用示例：**

```javascript
// 用户文档
{
  _id: ObjectId("60d5f4e3e3e3e3e3e3e3e3e3"),
  name: "John Doe",
  email: "john@example.com"
}

// 订单文档
{
  _id: ObjectId("60d5f4e3e3e3e3e3e3e3e3e4"),
  user_id: ObjectId("60d5f4e3e3e3e3e3e3e3e3e3"),
  items: [
    { product_id: ObjectId("60d5f4e3e3e3e3e3e3e3e3e5"), quantity: 1 }
  ]
}
```

---

### 3.2 索引优化

**索引类型：**
- **单字段索引**：加速单字段查询
- **复合索引**：加速多字段查询
- **文本索引**：全文搜索
- **地理空间索引**：位置查询

**创建索引：**

```javascript
// MongoDB Shell
db.users.createIndex({ email: 1 });
db.orders.createIndex({ user_id: 1, created_at: -1 });
db.places.createIndex({ location: "2dsphere" });
```

**索引最佳实践：**
- 为常用查询字段创建索引
- 考虑索引顺序
- 监控索引使用情况
- 定期重建索引

---

### 3.3 查询优化

**使用投影：**

```javascript
// 只返回需要的字段
db.users.find({ age: { $gt: 18 } }, { name: 1, email: 1 });
```

**使用聚合管道：**

```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$user_id", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
]);
```

**避免常见错误：**
- 避免在大型集合上使用不带索引的查询
- 避免使用 $where 操作符
- 避免返回过多数据

---

## 四、Redis 最佳实践

### 4.1 数据结构选择

**常用数据结构：**
- **String**：简单键值对
- **List**：链表，适合队列
- **Set**：无序集合，去重
- **Sorted Set**：有序集合，带分数
- **Hash**：字段值映射
- **Stream**：消息流

**使用场景：**
- **String**：缓存、计数器
- **List**：消息队列、最新消息
- **Set**：标签、好友关系
- **Sorted Set**：排行榜、计分系统
- **Hash**：用户信息、配置
- **Stream**：事件流、日志

---

### 4.2 缓存策略

**缓存模式：**
- **Cache-Aside**：应用先查缓存，缓存未命中再查数据库
- **Read-Through**：缓存负责加载数据
- **Write-Through**：写入同时更新缓存
- **Write-Behind**：异步更新缓存

**缓存示例：**

```javascript
// Cache-Aside 模式
const getUser = async (id) => {
  // 先查缓存
  const cachedUser = await redis.get(`user:${id}`);
  if (cachedUser) {
    return JSON.parse(cachedUser);
  }
  
  // 缓存未命中，查数据库
  const user = await db.users.findById(id);
  
  // 存入缓存
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);
  
  return user;
};
```

**缓存失效策略：**
- **TTL**：设置过期时间
- **LRU**：内存不足时淘汰最久未使用的
- **主动更新**：数据变更时主动更新缓存

---

### 4.3 性能优化

**批量操作：**

```javascript
// 批量设置
await redis.mset(
  'user:1', JSON.stringify(user1),
  'user:2', JSON.stringify(user2)
);

// 批量获取
const users = await redis.mget('user:1', 'user:2');
```

**Pipeline：**

```javascript
const pipeline = redis.pipeline();
pipeline.set('key1', 'value1');
pipeline.get('key2');
pipeline.incr('counter');
const results = await pipeline.exec();
```

**避免大键：**
- 拆分大型数据结构
- 使用哈希分片
- 监控内存使用

---

## 五、数据库安全

### 5.1 访问控制

**最佳实践：**
- 使用最小权限原则
- 为不同应用角色创建不同用户
- 定期轮换密码
- 限制数据库访问IP

**MySQL示例：**

```sql
-- 创建用户
CREATE USER 'app_user'@'192.168.1.%' IDENTIFIED BY 'password';

-- 授权
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'app_user'@'192.168.1.%';

-- 撤销权限
REVOKE DELETE ON myapp.* FROM 'app_user'@'192.168.1.%';
```

---

### 5.2 数据加密

**加密类型：**
- **传输加密**：使用SSL/TLS
- **存储加密**：敏感数据加密存储
- **应用层加密**：业务逻辑中的加密

**MySQL SSL配置：**

```sql
-- 启用SSL
ALTER USER 'app_user'@'%' REQUIRE SSL;
```

**密码存储：**

```javascript
// 使用bcrypt加密密码
const bcrypt = require('bcrypt');
const hashedPassword = await bcrypt.hash(password, 10);
```

---

### 5.3 备份与恢复

**备份策略：**
- **完全备份**：定期全量备份
- **增量备份**：记录变更
- **差异备份**：基于上次完全备份

**MySQL备份：**

```bash
# 完全备份
mysqldump -u root -p mydatabase > backup.sql

# 恢复
mysql -u root -p mydatabase < backup.sql
```

**MongoDB备份：**

```bash
# 完全备份
mongodump --db mydatabase --out /backup

# 恢复
mongorestore --db mydatabase /backup/mydatabase
```

---

## 六、监控与维护

### 6.1 性能监控

**关键指标：**
- **查询性能**：响应时间、QPS
- **资源使用**：CPU、内存、磁盘
- **连接数**：活跃连接、连接池状态
- **缓存命中率**：Redis缓存效率

**监控工具：**
- **MySQL**：Percona Monitoring and Management (PMM)
- **PostgreSQL**：pg_stat_statements
- **MongoDB**：MongoDB Atlas Monitoring
- **Redis**：Redis Sentinel

---

### 6.2 日常维护

**定期任务：**
- **优化表**：重建索引、碎片整理
- **分析表**：更新统计信息
- **备份验证**：测试恢复流程
- **日志清理**：归档旧日志

**MySQL维护：**

```sql
-- 优化表
OPTIMIZE TABLE users;

-- 分析表
ANALYZE TABLE users;

-- 检查表
CHECK TABLE users;
```

**MongoDB维护：**

```javascript
// 压缩集合
db.users.runCommand({ compact: "users" });

// 重建索引
db.users.reIndex();
```

---

## 七、云数据库服务

### 7.1 主流云数据库

**AWS：**
- **RDS**：关系型数据库服务
- **DynamoDB**：NoSQL数据库
- **ElastiCache**：Redis/Memcached
- **DocumentDB**：MongoDB兼容

**Azure：**
- **Azure SQL Database**：关系型数据库
- **Cosmos DB**：多模型NoSQL
- **Redis Cache**：缓存服务

**GCP：**
- **Cloud SQL**：关系型数据库
- **Firestore**：文档数据库
- **Memorystore**：Redis服务
- **Bigtable**：NoSQL数据库

---

### 7.2 云数据库优势

- **托管服务**：无需管理基础设施
- **自动扩展**：根据需求自动调整
- **高可用性**：多可用区部署
- **备份恢复**：自动备份和点恢复
- **监控告警**：内置监控系统

---

## 八、常见问题与解决方案

### 8.1 性能问题

**问题：** 查询缓慢
**解决方案：**
- 创建适当的索引
- 优化查询语句
- 考虑分区表
- 使用缓存

**问题：** 连接数过多
**解决方案：**
- 使用连接池
- 优化连接超时设置
- 检查应用是否正确关闭连接

### 8.2 扩展性问题

**问题：** 数据量增长过快
**解决方案：**
- 水平分区（Sharding）
- 读写分离
- 考虑NoSQL数据库
- 云服务自动扩展

**问题：** 高并发写入
**解决方案：**
- 使用队列缓冲
- 批量写入
- 优化事务
- 考虑时序数据库

### 8.3 可靠性问题

**问题：** 数据丢失
**解决方案：**
- 定期备份
- 使用RAID存储
- 多副本部署
- 灾难恢复计划

**问题：** 服务中断
**解决方案：**
- 高可用架构
- 自动故障转移
- 监控告警
- 冗余部署

---

## 九、最佳实践总结

1. **数据库选型**：根据业务需求选择合适的数据库
2. **设计优化**：合理的表结构和索引设计
3. **查询优化**：编写高效的查询语句
4. **性能调优**：监控和优化数据库性能
5. **安全防护**：访问控制和数据加密
6. **备份策略**：定期备份和测试恢复
7. **监控维护**：实时监控和日常维护
8. **扩展性**：考虑未来数据增长和并发需求
9. **云服务**：利用托管服务简化运维
10. **持续优化**：定期评估和改进数据库架构

---

## 相关资源

- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [MongoDB 官方文档](https://docs.mongodb.com/)
- [Redis 官方文档](https://redis.io/documentation)
- [AWS 数据库服务](https://aws.amazon.com/database/)
- [Azure 数据库服务](https://azure.microsoft.com/en-us/products/category/databases)
- [GCP 数据库服务](https://cloud.google.com/products/databases)

