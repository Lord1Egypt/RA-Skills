# 性能优化规范

## 概述
本文档定义性能优化原则和策略，确保系统具有良好的性能和响应速度。

## 性能目标

### 响应时间目标
- **API响应时间**: < 200ms（简单查询）
- **页面加载时间**: < 2s
- **数据库查询**: < 100ms
- **第三方API调用**: < 500ms

### 吞吐量目标
- **API吞吐量**: > 1000 req/s
- **并发用户数**: > 1000
- **数据库连接池**: 20-50

## 代码优化

### 算法优化
```typescript
// 避免O(n²)复杂度
// 错误
for (const user of users) {
  for (const order of orders) {
    if (order.userId === user.id) {
      // ...
    }
  }
}

// 正确 - 使用Map
const orderMap = new Map(orders.map(o => [o.userId, o]));
for (const user of users) {
  const order = orderMap.get(user.id);
  // ...
}
```

### 避免不必要的计算
```typescript
// 缓存计算结果
const memoized = (fn: Function) => {
  const cache = new Map();
  return (key: string) => {
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(key);
    cache.set(key, result);
    return result;
  };
};
```

### 延迟加载
```typescript
// 按需加载模块
const heavyModule = await import('./heavy-module');

// 懒加载路由
const LazyComponent = React.lazy(() => import('./LazyComponent'));
```

## 缓存策略

### 多级缓存
```typescript
class CacheService {
  async get(key: string): Promise<any> {
    // 1. 检查本地缓存
    let value = this.localCache.get(key);
    if (value) return value;

    // 2. 检查分布式缓存
    value = await this.redisCache.get(key);
    if (value) {
      this.localCache.set(key, value, 60);
      return value;
    }

    // 3. 从数据库加载
    value = await this.loadFromDatabase(key);
    await this.redisCache.set(key, value, 3600);
    this.localCache.set(key, value, 60);
    return value;
  }
}
```

### 缓存键设计
```typescript
// 使用有意义的缓存键
const cacheKey = `user:${userId}:profile`;
const cacheKey = `products:category:${categoryId}:page:${page}`;
```

### 缓存失效
```typescript
// 更新数据时清除缓存
async updateUser(userId: number, data: UpdateUserDto) {
  await this.userRepository.update(userId, data);
  await this.cache.delete(`user:${userId}`);
  await this.cache.delete(`user:${userId}:profile`);
}
```

## 数据库优化

### 索引优化
```sql
-- 为常用查询创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 使用复合索引
CREATE INDEX idx_products_category_price ON products(category_id, price);
```

### 查询优化
```sql
-- 使用EXPLAIN分析查询
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- 避免SELECT *
SELECT id, name, email FROM users;

-- 使用LIMIT
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20;
```

### 连接池配置
```typescript
const pool = new Pool({
  max: 20,              // 最大连接数
  min: 5,               // 最小连接数
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### 批量操作
```typescript
// 批量插入
await db.query(
  'INSERT INTO users (name, email) VALUES ?',
  [users.map(u => [u.name, u.email])]
);

// 批量更新
await db.query(
  'UPDATE users SET status = ? WHERE id IN (?)',
  ['active', userIds]
);
```

## 异步处理

### 异步操作
```typescript
// 使用Promise.all并行执行
const [user, orders, profile] = await Promise.all([
  userService.getUser(userId),
  orderService.getOrders(userId),
  profileService.getProfile(userId),
]);
```

### 消息队列
```typescript
// 异步处理耗时操作
async createOrder(orderData: OrderData) {
  const order = await this.orderRepository.create(orderData);
  
  // 发送到消息队列，异步处理
  await this.messageQueue.publish('order.created', {
    orderId: order.id,
    userId: order.userId,
  });
  
  return order;
}
```

## 前端优化

### 资源优化
- 压缩JavaScript和CSS
- 使用CDN加载静态资源
- 图片懒加载和压缩
- 使用WebP格式图片

### 代码分割
```typescript
// 路由级别的代码分割
const routes = [
  {
    path: '/users',
    component: React.lazy(() => import('./Users')),
  },
];
```

## 监控和测量

### 性能指标
```typescript
// 记录API响应时间
const startTime = Date.now();
const result = await handler();
const duration = Date.now() - startTime;

metrics.timing('api.duration', duration, {
  endpoint: req.path,
  method: req.method,
});
```

### 性能分析
```typescript
// 使用性能分析工具
import { performance } from 'perf_hooks';

const start = performance.now();
await expensiveOperation();
const duration = performance.now() - start;
console.log(`操作耗时: ${duration}ms`);
```

## 性能测试

### 负载测试
```bash
# 使用Apache Bench
ab -n 1000 -c 10 http://localhost:3000/api/users

# 使用k6
k6 run load-test.js
```

### 性能基准
- 建立性能基准
- 定期运行性能测试
- 监控性能回归

---

> **上下文提示**：在优化性能时，建议同时加载：
> - `coding.architecture.md` - 架构规范
> - `coding.data-models.md` - 数据模型规范
> - `coding.testing.md` - 测试规范

