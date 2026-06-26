# 代码规范指南

## 目录
- [JavaScript/TypeScript规范](#javascripttypescript规范)
- [Python代码规范](#python代码规范)
- [Java代码规范](#java代码规范)
- [Go代码规范](#go代码规范)
- [SQL代码规范](#sql代码规范)
- [Git提交规范](#git提交规范)

## JavaScript/TypeScript规范

### 命名规范

#### 变量和函数
```typescript
// 变量：驼峰命名
let userName = 'John';
let isLoggedIn = true;

// 函数：驼峰命名，动词开头
function getUserInfo() {}
function validateEmail() {}
function fetchData() {}

// 常量：大写字母+下划线
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';

// 类：帕斯卡命名
class UserService {}
class HttpClient {}

// 私有成员：下划线前缀
class UserService {
  private _cache: Map<string, any>;

  private _formatUser(user: User) {
    // ...
  }
}
```

#### 文件命名
```typescript
// 组件文件：PascalCase
// UserProfile.ts
// ButtonGroup.ts

// 工具文件：camelCase
// apiClient.ts
// dateUtils.ts

// 类型定义文件：.types.ts
// user.types.ts
// api.types.ts
```

### 代码格式

#### 使用Prettier
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "arrowParens": "avoid"
}
```

#### 使用ESLint
```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier'
  ],
  rules: {
    'no-console': 'warn',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off'
  }
};
```

### TypeScript类型规范

#### 类型定义
```typescript
// 接口：用于对象结构
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// 类型别名：用于联合类型、交叉类型
type UserRole = 'admin' | 'user' | 'guest';
type UserID = string;

// 泛型：可复用类型
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

// 使用示例
type UserResponse = ApiResponse<User>;
```

#### 类型导出
```typescript
// 统一导出类型
export type { User, UserRole, UserResponse };
export interface { UserService };
```

### 函数规范

#### 函数定义
```typescript
// 使用类型注解
function calculateSum(a: number, b: number): number {
  return a + b;
}

// 异步函数
async function fetchUserData(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

// 默认参数
function greet(name: string, greeting: string = 'Hello'): string {
  return `${greeting}, ${name}!`;
}

// 可选参数
function createUser(data: UserDto, options?: CreateUserOptions): User {
  // ...
}
```

#### 单一职责原则
```typescript
// ❌ 错误：函数做太多事情
function processUserData(data: any) {
  // 验证数据
  if (!data.email) throw new Error('Email required');
  // 转换数据
  const formatted = { ...data, email: data.email.toLowerCase() };
  // 保存到数据库
  await db.save(formatted);
  // 发送邮件
  await emailService.send(formatted.email);
  // 返回结果
  return formatted;
}

// ✅ 正确：拆分为多个函数
async function createUser(data: UserDataDto): Promise<User> {
  const validated = validateUserData(data);
  const formatted = formatUserData(validated);
  const user = await saveUser(formatted);
  await sendWelcomeEmail(user.email);
  return user;
}

function validateUserData(data: any): UserDataDto {
  if (!data.email) throw new Error('Email required');
  return data;
}

function formatUserData(data: UserDataDto): FormattedUserDto {
  return { ...data, email: data.email.toLowerCase() };
}

async function saveUser(data: FormattedUserDto): Promise<User> {
  return db.save(data);
}

async function sendWelcomeEmail(email: string): Promise<void> {
  await emailService.send(email);
}
```

### React组件规范

#### 组件定义
```typescript
import { useState, useEffect } from 'react';

interface Props {
  userId: string;
  onUpdate?: (user: User) => void;
}

export const UserProfile: React.FC<Props> = ({ userId, onUpdate }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadUser() {
      try {
        setLoading(true);
        const data = await fetchUser(userId);
        setUser(data);
      } catch (err) {
        setError('Failed to load user');
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return null;

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
};
```

#### Hooks规范
```typescript
// 自定义Hook：以use开头
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);

  return { user, loading };
}

// 使用Hook
function UserProfile({ userId }: { userId: string }) {
  const { user, loading } = useUserData(userId);

  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
}
```

## Python代码规范

### 命名规范（PEP 8）

```python
# 变量和函数：蛇形命名
user_name = "John"
is_logged_in = True

def get_user_info():
    pass

def validate_email():
    pass

# 常量：大写字母+下划线
MAX_RETRY_COUNT = 3
API_BASE_URL = "https://api.example.com"

# 类：帕斯卡命名
class UserService:
    pass

class HttpClient:
    pass

# 私有成员：下划线前缀
class UserService:
    def __init__(self):
        self._cache = {}

    def _format_user(self, user):
        pass
```

### 类型注解

```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

# 使用类型注解
def get_user_by_id(user_id: str) -> Optional[User]:
    pass

async def fetch_user_data(user_id: str) -> User:
    pass

def calculate_sum(a: int, b: int) -> int:
    return a + b

# 类型别名
UserID = str
UserRole = "admin" | "user" | "guest"

# 使用dataclass
@dataclass
class User:
    id: UserID
    name: str
    email: str
    role: UserRole
    created_at: datetime
```

### 函数定义

```python
def process_data(
    data: Dict[str, Any],
    *,
    validate: bool = True,
    format_output: bool = False
) -> Dict[str, Any]:
    """
    处理用户数据

    Args:
        data: 输入数据
        validate: 是否验证数据
        format_output: 是否格式化输出

    Returns:
        处理后的数据

    Raises:
        ValueError: 数据验证失败
    """
    if validate:
        if not data.get("email"):
            raise ValueError("Email is required")

    result = {**data}

    if format_output:
        result["email"] = result["email"].lower()

    return result
```

### 异步编程

```python
import asyncio
from typing import List

async def fetch_user(user_id: str) -> User:
    """获取单个用户"""
    pass

async def fetch_multiple_users(user_ids: List[str]) -> List[User]:
    """并发获取多个用户"""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

## Java代码规范

### 命名规范

```java
// 类：帕斯卡命名
public class UserService {
    // 常量：大写字母+下划线
    private static final int MAX_RETRY_COUNT = 3;
    private static final String API_BASE_URL = "https://api.example.com";

    // 变量：驼峰命名
    private String userName;
    private boolean isLoggedIn;

    // 方法：驼峰命名，动词开头
    public User getUserInfo() {
        return null;
    }

    public boolean validateEmail() {
        return false;
    }

    // 私有方法
    private void formatUserData(User user) {
    }
}
```

### 类定义

```java
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private String email;
    private String role;
    private LocalDateTime createdAt;
}
```

### Service层

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final EmailService emailService;

    @Transactional
    public User createUser(CreateUserDto dto) {
        // 验证
        validateUserDto(dto);

        // 创建用户
        User user = User.builder()
            .name(dto.getName())
            .email(dto.getEmail())
            .role("USER")
            .createdAt(LocalDateTime.now())
            .build();

        // 保存
        User savedUser = userRepository.save(user);

        // 发送欢迎邮件
        emailService.sendWelcomeEmail(savedUser.getEmail());

        return savedUser;
    }

    private void validateUserDto(CreateUserDto dto) {
        if (StringUtils.isEmpty(dto.getEmail())) {
            throw new ValidationException("Email is required");
        }
    }
}
```

### Controller层

```java
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ApiResponse<User> getUser(@PathVariable Long id) {
        User user = userService.getUserById(id);
        return ApiResponse.success(user);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ApiResponse<User> createUser(@Valid @RequestBody CreateUserDto dto) {
        User user = userService.createUser(dto);
        return ApiResponse.success(user);
    }
}
```

## Go代码规范

### 命名规范

```go
// 包名：小写，简短
package user

// 导出标识符：帕斯卡命名
type UserService struct {
    cache map[string]any
}

// 未导出标识符：驼峰命名
type internalConfig struct {
    maxRetries int
}

// 接口：以-er结尾
type Reader interface {
    Read(p []byte) (n int, err error)
}

// 常量：驼峰命名
const (
    MaxRetryCount = 3
    APIBaseURL    = "https://api.example.com"
)

// 函数：驼峰命名
func GetUserInfo(id string) (*User, error) {
    return nil, nil
}
```

### 错误处理

```go
import (
    "errors"
    "fmt"
)

// 定义错误
var (
    ErrUserNotFound = errors.New("user not found")
    ErrInvalidInput = errors.New("invalid input")
)

// 函数返回错误
func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, ErrInvalidInput
    }

    user, err := repository.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("failed to find user: %w", err)
    }

    return user, nil
}

// 使用错误
user, err := GetUser("123")
if err != nil {
    if errors.Is(err, ErrUserNotFound) {
        // 处理用户不存在
    }
    return err
}
```

### 结构体和方法

```go
type User struct {
    ID        string    `json:"id"`
    Name      string    `json:"name"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}

type UserService struct {
    repo *UserRepository
}

func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}

// 方法接收者：如果是小结构体，用值；大结构体，用指针
func (s *UserService) GetUser(id string) (*User, error) {
    return s.repo.FindByID(id)
}

func (u User) String() string {
    return fmt.Sprintf("User{id=%s, name=%s}", u.ID, u.Name)
}
```

## SQL代码规范

### 命名规范

```sql
-- 表名：蛇形命名，复数形式
CREATE TABLE users (
    id UUID PRIMARY KEY,
    user_name VARCHAR(100),
    created_at TIMESTAMP
);

CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

-- 字段名：蛇形命名
-- user_name, created_at, updated_at

-- 索引名：idx_表名_字段名
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- 外键名：fk_表名_字段名
ALTER TABLE user_profiles
ADD CONSTRAINT fk_user_profiles_user_id
FOREIGN KEY (user_id) REFERENCES users(id);
```

### 查询规范

```sql
-- 使用格式化
SELECT
    u.id,
    u.user_name,
    u.email,
    COUNT(o.id) AS order_count
FROM
    users u
LEFT JOIN
    orders o ON u.id = o.user_id
WHERE
    u.created_at >= '2024-01-01'
    AND u.is_active = true
GROUP BY
    u.id, u.user_name, u.email
ORDER BY
    order_count DESC
LIMIT 10;
```

## Git提交规范

### Commit Message格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

### 示例

```bash
# 新功能
feat(user): add user registration feature

Implement user registration with email validation
and welcome email sending.

Closes #123

# 修复bug
fix(auth): resolve token expiration issue

The JWT token was not properly refreshed when expired.
Now it's handled correctly with proper error messages.

# 文档更新
docs(readme): update installation instructions

Added Docker deployment guide and updated requirements.

# 重构
refactor(user): extract validation logic to separate service

Move user validation logic from controller to dedicated
validation service for better separation of concerns.
```

### 分支规范

```bash
# 主分支
main/master
develop

# 功能分支
feature/user-authentication
feature/payment-gateway

# 修复分支
bugfix/login-error
hotfix/security-patch

# 发布分支
release/v1.0.0
```
