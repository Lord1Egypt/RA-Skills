# 开发最佳实践

## 目录
- [代码组织](#代码组织)
- [错误处理](#错误处理)
- [安全性实践](#安全性实践)
- [性能优化](#性能优化)
- [测试策略](#测试策略)
- [API设计](#api设计)
- [数据库最佳实践](#数据库最佳实践)
- [日志和监控](#日志和监控)

## 代码组织

### 项目目录结构

#### 前端项目（React）
```
src/
├── assets/           # 静态资源
├── components/       # 可复用组件
│   ├── common/      # 通用组件
│   └── business/    # 业务组件
├── pages/           # 页面组件
├── hooks/           # 自定义Hooks
├── services/        # API服务
├── stores/          # 状态管理
├── utils/           # 工具函数
├── types/           # TypeScript类型定义
├── constants/       # 常量定义
├── config/          # 配置文件
└── styles/          # 全局样式
```

#### 后端项目（Node.js/NestJS）
```
src/
├── modules/         # 业务模块
│   ├── user/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── dto/
│   │   └── entities/
├── common/          # 通用模块
│   ├── filters/    # 异常过滤器
│   ├── guards/     # 守卫
│   ├── interceptors/# 拦截器
│   ├── decorators/ # 装饰器
│   └── utils/      # 工具函数
├── config/          # 配置文件
├── database/        # 数据库配置
└── main.ts
```

#### 后端项目（Java/Spring Boot）
```
src/
├── main/
│   ├── java/
│   │   └── com/example/
│   │       ├── controller/
│   │       ├── service/
│   │       ├── repository/
│   │       ├── entity/
│   │       ├── dto/
│   │       ├── config/
│   │       └── exception/
│   └── resources/
│       ├── application.yml
│       └── mapper/
└── test/
```

### 命名规范

#### 通用原则
- **文件名**：小写字母+连字符（kebab-case），如 `user-service.ts`
- **类名**：帕斯卡命名（PascalCase），如 `UserService`
- **函数/变量**：驼峰命名（camelCase），如 `getUserInfo`
- **常量**：大写字母+下划线，如 `MAX_RETRY_COUNT`
- **私有成员**：下划线前缀，如 `_privateMethod`

#### 目录命名
- 统一使用小写字母和连字符
- 避免使用缩写，保持语义清晰
- 例如：`user-management` 而非 `usr-mgmt`

### 代码注释规范

#### 函数注释（JSDoc/TSDoc）
```javascript
/**
 * 根据用户ID获取用户信息
 * @param {string} userId - 用户ID
 * @param {boolean} includeProfile - 是否包含详细资料
 * @returns {Promise<User>} 用户信息对象
 * @throws {NotFoundError} 用户不存在时抛出
 */
async getUserById(userId: string, includeProfile = false): Promise<User> {
  // 实现代码
}
```

#### 复杂逻辑注释
```javascript
// 使用双因子认证进行安全验证
// 流程：
// 1. 验证密码正确性
// 2. 检查是否开启2FA
// 3. 如果开启，验证OTP码
if (is2FAEnabled) {
  const isValidOTP = await verifyOTP(user.otpSecret, otpCode);
  if (!isValidOTP) {
    throw new UnauthorizedError('Invalid OTP code');
  }
}
```

## 错误处理

### 统一错误处理

#### 后端错误分类
```typescript
// 错误类型定义
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(404, message, 'NOT_FOUND');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(401, message, 'UNAUTHORIZED');
  }
}

export class ValidationError extends AppError {
  constructor(message: string = 'Validation failed') {
    super(400, message, 'VALIDATION_ERROR');
  }
}
```

#### 全局异常处理器
```typescript
@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    let status = 500;
    let message = 'Internal server error';
    let code = 'INTERNAL_ERROR';

    if (exception instanceof AppError) {
      status = exception.statusCode;
      message = exception.message;
      code = exception.code;
    }

    response.status(status).json({
      success: false,
      error: {
        code,
        message,
        timestamp: new Date().toISOString(),
      },
    });
  }
}
```

### 错误日志记录
```typescript
// 记录错误上下文
logger.error('Failed to process payment', {
  userId,
  orderId,
  error: exception.message,
  stack: exception.stack,
  timestamp: new Date(),
});
```

## 安全性实践

### 认证授权

#### JWT认证
```typescript
// 生成JWT Token
function generateToken(user: User): string {
  const payload = {
    userId: user.id,
    email: user.email,
    role: user.role,
  };

  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: '7d',
  });
}

// 验证JWT Token
function verifyToken(token: string): JwtPayload {
  try {
    return jwt.verify(token, JWT_SECRET) as JwtPayload;
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}
```

#### RBAC权限控制
```typescript
// 权限装饰器
export const RequirePermissions = (...permissions: string[]) => {
  return applyDecorators(
    UseGuards(JwtAuthGuard, PermissionsGuard),
    SetMetadata('permissions', permissions)
  );
};

// 使用示例
@Post('admin/users')
@RequirePermissions('user:create')
async createUser(@Body() dto: CreateUserDto) {
  // 只有拥有 user:create 权限的用户可以访问
}
```

### 数据验证

#### 输入验证
```typescript
import { z } from 'zod';

// 定义验证schema
const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
});

// 使用验证
function validateUserData(data: unknown) {
  return CreateUserSchema.parse(data);
}
```

#### SQL注入防护
```typescript
// 使用参数化查询
async getUserByEmail(email: string) {
  const query = 'SELECT * FROM users WHERE email = $1';
  const result = await this.db.query(query, [email]);
  return result.rows[0];
}

// 使用ORM
async getUserByEmail(email: string) {
  return this.userRepository.findOne({ where: { email } });
}
```

### 敏感数据处理

#### 密码加密
```typescript
import bcrypt from 'bcrypt';

// 加密密码
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 10;
  return bcrypt.hash(password, saltRounds);
}

// 验证密码
async function verifyPassword(
  password: string,
  hashedPassword: string
): Promise<boolean> {
  return bcrypt.compare(password, hashedPassword);
}
```

#### 敏感数据脱敏
```typescript
// 日志脱敏
function sanitizeForLogging(data: any): any {
  const sensitiveFields = ['password', 'token', 'secret', 'apiKey'];
  const sanitized = { ...data };

  sensitiveFields.forEach(field => {
    if (sanitized[field]) {
      sanitized[field] = '***REDACTED***';
    }
  });

  return sanitized;
}
```

## 性能优化

### 数据库优化

#### 索引优化
```sql
-- 为常用查询字段添加索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- 复合索引（注意顺序）
CREATE INDEX idx_orders_status_created ON orders(status, created_at);
```

#### 查询优化
```typescript
// 避免N+1查询
async getUsersWithOrders() {
  // 错误方式：N+1查询
  const users = await this.userRepository.find();
  for (const user of users) {
    user.orders = await this.orderRepository.find({ user: user.id });
  }

  // 正确方式：使用JOIN
  return this.userRepository
    .createQueryBuilder('user')
    .leftJoinAndSelect('user.orders', 'orders')
    .getMany();
}
```

#### 分页查询
```typescript
async getUsers(page: number, pageSize: number) {
  const skip = (page - 1) * pageSize;

  return this.userRepository.find({
    skip,
    take: pageSize,
    order: { createdAt: 'DESC' },
  });
}
```

### 缓存策略

#### Redis缓存
```typescript
async getUserById(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;

  // 尝试从缓存获取
  const cached = await this.redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // 从数据库获取
  const user = await this.userRepository.findOne({ where: { id: userId } });

  // 写入缓存（5分钟过期）
  if (user) {
    await this.redis.setex(cacheKey, 300, JSON.stringify(user));
  }

  return user;
}
```

#### 缓存失效策略
```typescript
async updateUser(userId: string, data: UpdateUserDto): Promise<User> {
  // 更新数据库
  const user = await this.userRepository.save({ id: userId, ...data });

  // 删除缓存
  const cacheKey = `user:${userId}`;
  await this.redis.del(cacheKey);

  return user;
}
```

### 前端性能优化

#### 代码分割
```typescript
// 路由懒加载
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

#### 图片优化
```typescript
// 使用懒加载
import { LazyLoadImage } from 'react-lazy-load-image-component';

<LazyLoadImage
  src={imageSrc}
  alt="Description"
  effect="blur"
  width={300}
  height={200}
/>
```

## 测试策略

### 单元测试

#### Jest测试示例
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = createMockRepository();
    service = new UserService(mockRepository);
  });

  it('should return user when exists', async () => {
    const mockUser = { id: '1', name: 'John' };
    mockRepository.findOne.mockResolvedValue(mockUser);

    const result = await service.getUserById('1');

    expect(result).toEqual(mockUser);
    expect(mockRepository.findOne).toHaveBeenCalledWith({ where: { id: '1' } });
  });

  it('should throw NotFoundError when user not exists', async () => {
    mockRepository.findOne.mockResolvedValue(null);

    await expect(service.getUserById('999')).rejects.toThrow(NotFoundError);
  });
});
```

### 集成测试

#### API集成测试
```typescript
describe('UserController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/users (POST)', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(201)
      .expect((res) => {
        expect(res.body).toHaveProperty('id');
        expect(res.body.name).toBe('John');
      });
  });
});
```

### 测试覆盖率

- 目标覆盖率：80%以上
- 核心业务逻辑：90%以上
- 工具函数：95%以上

## API设计

### RESTful API规范

#### 资源命名
```
GET    /users          # 获取用户列表
GET    /users/:id      # 获取单个用户
POST   /users          # 创建用户
PUT    /users/:id      # 完整更新用户
PATCH  /users/:id      # 部分更新用户
DELETE /users/:id      # 删除用户
```

#### 响应格式
```json
// 成功响应
{
  "success": true,
  "data": {
    "id": "123",
    "name": "John",
    "email": "john@example.com"
  }
}

// 错误响应
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  }
}
```

### API版本控制
```typescript
// URL版本控制
@Controller('api/v1/users')
export class UserControllerV1 {
  // V1实现
}

@Controller('api/v2/users')
export class UserControllerV2 {
  // V2实现
}
```

## 数据库最佳实践

### 数据库设计原则

#### 表设计
```sql
-- 使用蛇形命名
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 添加索引
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_created_at ON user_profiles(created_at DESC);
```

#### 软删除
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- 查询时排除已删除
SELECT * FROM users WHERE deleted_at IS NULL;
```

### 数据库迁移

#### 版本控制
```typescript
// 迁移文件示例
export async function up(queryRunner: QueryRunner): Promise<void> {
  await queryRunner.query(`
    CREATE TABLE users (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      email VARCHAR(255) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT NOW()
    )
  `);
}

export async function down(queryRunner: QueryRunner): Promise<void> {
  await queryRunner.query(`DROP TABLE users`);
}
```

## 日志和监控

### 日志规范

#### 日志级别
```typescript
logger.debug('Debug information'); // 调试信息
logger.info('User logged in', { userId }); // 一般信息
logger.warn('API rate limit approaching'); // 警告
logger.error('Database connection failed', { error }); // 错误
```

#### 结构化日志
```typescript
logger.info('Order processed', {
  orderId,
  userId,
  amount,
  paymentMethod,
  processingTime: Date.now() - startTime,
});
```

### 监控指标

#### 关键指标
- **性能指标**：响应时间、吞吐量、错误率
- **业务指标**：DAU、转化率、订单量
- **系统指标**：CPU使用率、内存使用率、磁盘IO

#### 健康检查
```typescript
@Get('health')
healthCheck() {
  return {
    status: 'ok',
    timestamp: new Date(),
    services: {
      database: this.checkDatabase(),
      redis: this.checkRedis(),
      externalApi: this.checkExternalApi(),
    },
  };
}
```

### 告警规则
```yaml
# Prometheus告警规则示例
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"

      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds[5m])) > 1
        for: 10m
        annotations:
          summary: "95th percentile response time exceeds 1s"
```
