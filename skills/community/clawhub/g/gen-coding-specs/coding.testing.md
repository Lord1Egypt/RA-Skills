# 测试规范

## 概述
本文档定义测试策略和标准，确保代码质量和系统可靠性。

## 测试金字塔

```
        /\
       /  \
      /E2E \       少量端到端测试
     /------\
    /        \
   / Integration\  适量集成测试
  /--------------\
 /                \
/   Unit Tests     \  大量单元测试
/------------------\
```

### 测试比例
- **单元测试**: 70%
- **集成测试**: 20%
- **端到端测试**: 10%

## 单元测试

### 测试结构
```typescript
describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      save: jest.fn(),
    };
    userService = new UserService(mockRepository);
  });

  describe('createUser', () => {
    it('应该成功创建用户', async () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };
      mockRepository.save.mockResolvedValue({ id: 1, ...userData });

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result.id).toBe(1);
      expect(mockRepository.save).toHaveBeenCalledWith(userData);
    });

    it('应该抛出错误当邮箱已存在', async () => {
      // Arrange
      const userData = { name: 'John', email: 'existing@example.com' };
      mockRepository.save.mockRejectedValue(new DuplicateEmailError());

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow(DuplicateEmailError);
    });
  });
});
```

### 测试命名
- 使用描述性名称
- 格式：`应该[预期行为]当[条件]`
- 示例：`应该返回用户当提供有效ID时`

### 测试原则
- **AAA模式**：Arrange（准备）、Act（执行）、Assert（断言）
- **独立性**：每个测试应该独立
- **快速**：单元测试应该快速执行

## 集成测试

### 测试范围
- 测试多个组件交互
- 测试数据库操作
- 测试外部服务集成

### 示例
```typescript
describe('User API Integration', () => {
  let app: Application;
  let db: Database;

  beforeAll(async () => {
    app = await createTestApp();
    db = await setupTestDatabase();
  });

  afterAll(async () => {
    await cleanupTestDatabase(db);
    await app.close();
  });

  it('应该创建并获取用户', async () => {
    // 创建用户
    const createResponse = await request(app)
      .post('/api/v1/users/create')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(200);

    const userId = createResponse.body.data.id;

    // 获取用户
    const getResponse = await request(app)
      .post('/api/v1/users/detail')
      .send({ id: userId })
      .expect(200);

    expect(getResponse.body.data.name).toBe('John');
  });
});
```

## 端到端测试

### 测试范围
- 测试完整用户流程
- 测试关键业务场景
- 测试跨系统交互

### 示例
```typescript
describe('订单流程 E2E', () => {
  it('应该完成完整的订单流程', async () => {
    // 1. 用户登录
    const loginResponse = await request(app)
      .post('/api/v1/auth/login')
      .send({ email: 'user@example.com', password: 'password' });
    
    const token = loginResponse.body.token;

    // 2. 创建订单
    const orderResponse = await request(app)
      .post('/api/v1/orders/create')
      .set('Authorization', `Bearer ${token}`)
      .send({ items: [{ productId: 1, quantity: 2 }] })
      .expect(200);

    // 3. 验证订单状态
    expect(orderResponse.body.data.status).toBe('PENDING');
  });
});
```

## 测试覆盖率

### 覆盖率要求
- **单元测试**: ≥ 80%
- **关键业务逻辑**: ≥ 90%
- **集成测试**: 覆盖主要流程

### 覆盖率工具
```bash
# Jest
npm test -- --coverage

# Python
pytest --cov=app --cov-report=html
```

## 测试数据

### 测试数据管理
```typescript
// 使用工厂模式创建测试数据
class UserFactory {
  static create(overrides?: Partial<User>): User {
    return {
      id: 1,
      name: 'Test User',
      email: 'test@example.com',
      ...overrides,
    };
  }
}

// 使用fixtures
const testUsers = [
  UserFactory.create({ id: 1, name: 'User 1' }),
  UserFactory.create({ id: 2, name: 'User 2' }),
];
```

### 测试数据库
- 使用独立的测试数据库
- 每次测试前清理数据
- 使用事务回滚

## Mock和Stub

### Mock外部服务
```typescript
// Mock HTTP客户端
jest.mock('./httpClient', () => ({
  httpClient: {
    get: jest.fn(),
    post: jest.fn(),
  },
}));

// Mock数据库
const mockRepository = {
  findById: jest.fn(),
  save: jest.fn(),
};
```

## 测试最佳实践

### 1. 测试应该快速
- 避免慢速操作
- 使用Mock替代真实服务
- 并行执行测试

### 2. 测试应该独立
- 不依赖其他测试
- 不依赖执行顺序
- 可以单独运行

### 3. 测试应该可读
- 使用描述性名称
- 遵循AAA模式
- 添加必要的注释

### 4. 测试应该可靠
- 避免flaky测试
- 使用确定性的数据
- 避免时间依赖

---

> **上下文提示**：在编写测试时，建议同时加载：
> - `coding.coding-style.md` - 编码风格规范
> - `coding.api.md` - 接口规范
> - `coding.code-review.md` - 代码审查规范

