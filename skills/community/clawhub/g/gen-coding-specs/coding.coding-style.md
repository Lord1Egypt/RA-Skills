# 编码风格规范

## 概述
本文档定义代码格式和风格标准，确保代码的一致性、可读性和可维护性。

## 通用原则

### 1. 可读性优先
- 代码应该自解释
- 使用有意义的变量名和函数名
- 保持函数简短（< 50行）

### 2. 一致性
- 遵循团队统一的编码风格
- 使用代码格式化工具
- 保持项目内风格一致

### 3. 简洁性
- 避免不必要的复杂性
- 使用语言特性简化代码
- 删除冗余代码

## 命名规范

### 变量和函数
```typescript
// TypeScript/JavaScript - camelCase
const userName = 'John';
function calculateTotal() {}

// Python - snake_case
user_name = 'John'
def calculate_total():
    pass

// Java - camelCase
String userName = "John";
public void calculateTotal() {}
```

### 类和接口
```typescript
// TypeScript - PascalCase
class UserService {}
interface UserRepository {}

// Python - PascalCase
class UserService:
    pass

// Java - PascalCase
public class UserService {}
```

### 常量
```typescript
// UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';
```

## 代码格式

### 缩进
- **TypeScript/JavaScript**: 2空格
- **Python**: 4空格
- **Java**: 4空格

### 行长度
- 最大行长度：80-100字符
- 超长行应换行

### 示例
```typescript
// 好的格式
function calculateTotal(
  items: Item[],
  taxRate: number
): number {
  const subtotal = items.reduce(
    (sum, item) => sum + item.price,
    0
  );
  return subtotal * (1 + taxRate);
}
```

## 注释规范

### 何时注释
- 解释"为什么"而非"是什么"
- 复杂算法和业务逻辑
- 公共API和接口
- 临时解决方案和工作区

### 注释格式
```typescript
/**
 * 计算包含税费的总价
 * 
 * @param items - 商品列表
 * @param taxRate - 税率（如0.08表示8%）
 * @returns 总价（含税）
 */
function calculateTotalWithTax(
  items: Item[],
  taxRate: number
): number {
  // 计算小计
  const subtotal = items.reduce(
    (sum, item) => sum + item.price,
    0
  );
  
  // 应用税费
  return subtotal * (1 + taxRate);
}
```

## 代码组织

### 文件结构
```typescript
// 1. 导入语句
import { User } from './models';
import { UserService } from './services';

// 2. 类型定义
interface CreateUserDto {
  name: string;
  email: string;
}

// 3. 常量
const DEFAULT_PAGE_SIZE = 20;

// 4. 函数和类
class UserController {
  // ...
}

// 5. 导出
export { UserController };
```

### 函数设计
```typescript
// 单一职责
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// 避免副作用
function calculateTotal(items: Item[]): number {
  // 纯函数，无副作用
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

## 错误处理

### 异常处理
```typescript
try {
  const user = await userService.createUser(data);
  return user;
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('验证失败', { error, data });
    throw new BadRequestError(error.message);
  }
  logger.error('创建用户失败', { error, data });
  throw new InternalServerError('创建用户失败');
}
```

### 错误类型

> 错误类型层次定义见 `coding.architecture.md` 异常层次章节。

## 语言特定规范

### TypeScript
```typescript
// 使用类型注解
function add(a: number, b: number): number {
  return a + b;
}

// 避免使用any
// 错误
function process(data: any) {}

// 正确
function process(data: UserData) {}

// 使用接口而非类型别名（用于对象）
interface User {
  id: number;
  name: string;
}
```

### Python
```python
# 使用类型提示
def add(a: int, b: int) -> int:
    return a + b

# 遵循PEP 8
# 使用4空格缩进
# 行长度不超过79字符
# 导入顺序：标准库、第三方、本地
```

### Java 基础规范
```java
// 使用注解
@Override
public String toString() {
    return "User";
}

// 使用final修饰不可变变量
final String userName = "John";

// 使用Optional处理null
Optional<User> user = userRepository.findById(id);
```

> MyBatis-Plus 实体类/Mapper/Service/Controller 规范见 `coding.architecture.md` 数据访问章节和 `coding.data-models.md` 数据访问规范。

## 代码质量工具

### ESLint (TypeScript/JavaScript)
```json
{
  "extends": ["eslint:recommended", "@typescript-eslint/recommended"],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/explicit-function-return-type": "error"
  }
}
```

### Prettier
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

## 最佳实践

### 1. 避免魔法数字
```typescript
// 错误
if (status === 1) {}

// 正确
const STATUS_ACTIVE = 1;
if (status === STATUS_ACTIVE) {}
```

### 2. 使用枚举
```typescript
enum OrderStatus {
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
  COMPLETED = 'COMPLETED'
}
```

### 3. 避免深层嵌套
```typescript
// 错误
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      // ...
    }
  }
}

// 正确
if (!user || !user.isActive || !user.hasPermission) {
  return;
}
// ...
```

---

> **上下文提示**：在编写代码时，建议同时加载：
> - `coding.architecture.md` - 架构规范（含 Java/MyBatis-Plus 速查）
> - `coding.data-models.md` - 数据模型规范
> - `coding.testing.md` - 测试规范
> - `coding.code-review.md` - 代码审查规范

