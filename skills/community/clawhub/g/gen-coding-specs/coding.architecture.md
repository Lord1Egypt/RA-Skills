# 架构规范

## 概述

本文档定义系统架构设计原则和模式，确保系统具有良好的可扩展性、可维护性和可测试性。

## 架构原则

### 1. 后端架构（分层架构）
```
┌─────────────────┐
│  表现层 (UI)     │
├─────────────────┤
│  应用层 (Service)│
├─────────────────┤
│  领域层 (Domain) │
├─────────────────┤
│  基础设施层      │
└─────────────────┘
```

### 2. 前端架构

> Vue.js 前端架构规范（组件化、Composables、Pinia、目录结构、路由）见 `coding.vue.md`。

### 3. 关注点分离
- **表现层**：处理用户交互和请求
- **应用层**：处理业务逻辑和用例
- **领域层**：核心业务实体和规则
- **基础设施层**：数据持久化、外部服务

### 4. 依赖倒置
- 高层模块不依赖低层模块
- 都依赖抽象（接口）
- 抽象不依赖细节，细节依赖抽象

## 设计模式

### 常用模式

#### 1. Repository模式
```typescript
interface UserRepository {
  findById(id: number): Promise<User>;
  save(user: User): Promise<User>;
}

class UserRepositoryImpl implements UserRepository {
  // 实现细节
}
```

#### 2. Service模式
```typescript
class UserService {
  constructor(private userRepo: UserRepository) {}
  
  async createUser(data: CreateUserDto): Promise<User> {
    // 业务逻辑
  }
}
```

#### 3. Factory模式
```typescript
class PaymentProcessorFactory {
  static create(type: string): PaymentProcessor {
    switch (type) {
      case 'stripe': return new StripeProcessor();
      case 'paypal': return new PayPalProcessor();
    }
  }
}
```

## 微服务架构

### 服务划分
- 按业务领域划分服务
- 服务间通过API通信
- 每个服务独立部署

### 服务通信
```typescript
// 同步通信（HTTP）
class ProductServiceClient {
  async getProduct(id: number): Promise<Product> {
    return await httpClient.get(`/api/products/${id}`);
  }
}

// 异步通信（消息队列）
class OrderService {
  async createOrder(order: Order) {
    await this.messageQueue.publish('order.created', order);
  }
}
```

## 组件交互

### 依赖注入
```typescript
class UserController {
  constructor(
    private userService: UserService,
    private logger: Logger
  ) {}
}
```

### 事件驱动
```typescript
class OrderService {
  async createOrder(order: Order) {
    await this.orderRepository.save(order);
    await this.eventBus.publish(new OrderCreatedEvent(order));
  }
}
```

## 数据访问

> MyBatis-Plus Mapper/Service/实体类/QueryWrapper 速查见 `coding.data-models.md` 数据访问章节。

### Repository模式（非 Java 项目）
```typescript
interface UserRepository {
  findById(id: number): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: number): Promise<void>;
}
```

### 事务管理

#### Java (Spring)
```java
@Transactional(rollbackFor = Exception.class)
public Order createOrder(OrderData orderData) {
    Order order = new Order();
    BeanUtils.copyProperties(orderData, order);
    orderMapper.insert(order);
    inventoryService.reserve(order.getItems());
    return order;
}
```

## 错误处理

### 异常层次
```typescript
class DomainException extends Error {}
class ValidationException extends DomainException {}
class NotFoundException extends DomainException {}
class BusinessException extends DomainException {}
```

### 错误处理策略
```typescript
try {
  await this.userService.createUser(data);
} catch (error) {
  if (error instanceof ValidationException) {
    return { code: 400, message: error.message };
  }
  throw error;
}
```

## 架构决策记录（ADR）

### ADR格式
```markdown
# ADR-001: 使用微服务架构

## 状态
已采用

## 上下文
系统需要支持高并发和快速迭代

## 决策
采用微服务架构，按业务领域划分服务

## 后果
- 优点：独立部署、技术栈灵活
- 缺点：运维复杂度增加
```

---

> **上下文提示**：在架构设计时，建议同时加载：
> - `coding.vue.md` - Vue.js 前端架构规范
> - `coding.data-models.md` - 数据模型与数据访问规范
> - `coding.performance.md` - 性能优化规范（缓存、异步、监控）
> - `coding.api.md` - 接口规范
