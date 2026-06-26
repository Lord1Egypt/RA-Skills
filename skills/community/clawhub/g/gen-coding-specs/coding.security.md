# 安全规范

## 概述
本文档定义安全编码和防护标准，确保系统的安全性和数据保护。

## 安全原则

### 1. 最小权限原则
- 用户只获得必要的权限
- 服务只访问必要的数据
- 使用角色基础访问控制（RBAC）

### 2. 纵深防御
- 多层安全防护
- 不依赖单一安全措施
- 定期安全审计

### 3. 安全默认
- 默认拒绝访问
- 需要显式授权
- 最小化攻击面

## 输入验证

### 验证所有输入
```typescript
// 使用验证库
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
});

// 验证输入
const result = userSchema.safeParse(input);
if (!result.success) {
  throw new ValidationError(result.error);
}
```

### 防止注入攻击
```typescript
// SQL注入防护 - 使用参数化查询
const query = 'SELECT * FROM users WHERE id = ?';
await db.query(query, [userId]);

// NoSQL注入防护
const user = await User.findOne({
  _id: { $ne: maliciousInput }  // 避免直接拼接
});
```

### XSS防护
```typescript
// 转义用户输入
import { escape } from 'html-escaper';

const safeHtml = escape(userInput);

// 使用CSP（内容安全策略）
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'"
  );
  next();
});
```

## 认证授权

### 密码安全
```typescript
import bcrypt from 'bcrypt';

// 密码哈希
const saltRounds = 10;
const hashedPassword = await bcrypt.hash(password, saltRounds);

// 密码验证
const isValid = await bcrypt.compare(password, hashedPassword);

// 密码要求
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
```

### JWT认证
```typescript
import jwt from 'jsonwebtoken';

// 生成Token
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// 验证Token
const decoded = jwt.verify(token, process.env.JWT_SECRET);
```

### 权限控制
```typescript
// 基于角色的访问控制（RBAC）
enum Role {
  ADMIN = 'ADMIN',
  USER = 'USER',
  GUEST = 'GUEST',
}

// 权限检查中间件
function requirePermission(permission: string) {
  return (req, res, next) => {
    if (!req.user.hasPermission(permission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}
```

## 数据加密

### 敏感数据加密
```typescript
import crypto from 'crypto';

// AES加密
function encrypt(text: string, key: string): string {
  const cipher = crypto.createCipher('aes-256-cbc', key);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
}

// 解密
function decrypt(encrypted: string, key: string): string {
  const decipher = crypto.createDecipher('aes-256-cbc', key);
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}
```

### 传输加密
- 使用HTTPS传输数据
- 不在URL中传递敏感信息
- 使用安全的Cookie设置

```typescript
// 安全Cookie设置
res.cookie('token', token, {
  httpOnly: true,      // 防止XSS
  secure: true,        // 仅HTTPS
  sameSite: 'strict',  // CSRF防护
  maxAge: 3600000,
});
```

## 安全漏洞防护

### CSRF防护
```typescript
import csrf from 'csurf';

// CSRF保护中间件
const csrfProtection = csrf({ cookie: true });

app.post('/api/users', csrfProtection, (req, res) => {
  // 处理请求
});
```

### 速率限制
```typescript
import rateLimit from 'express-rate-limit';

// API速率限制
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 最多100次请求
});

app.use('/api/', limiter);
```

### 安全头设置
```typescript
import helmet from 'helmet';

// 设置安全HTTP头
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
    },
  },
}));
```

## 日志和监控

### 安全日志
```typescript
// 记录安全事件
logger.warn('登录失败', {
  email: userEmail,
  ip: req.ip,
  userAgent: req.get('user-agent'),
  timestamp: new Date(),
});

// 记录敏感操作
logger.info('用户权限变更', {
  userId: user.id,
  oldRole: oldRole,
  newRole: newRole,
  operator: currentUser.id,
});
```

### 不在日志中记录敏感信息
```typescript
// 错误
logger.info('用户登录', { password: user.password });

// 正确
logger.info('用户登录', { userId: user.id, email: user.email });
```

## 依赖安全

### 依赖扫描
```bash
# 扫描依赖漏洞
npm audit
npm audit fix

# 使用Snyk
snyk test
snyk monitor
```

### 依赖更新
- 定期更新依赖
- 关注安全公告
- 使用自动化工具扫描

## 安全审计

### 代码审查检查清单
- [ ] 所有输入都已验证
- [ ] 使用参数化查询
- [ ] 密码已哈希
- [ ] 敏感数据已加密
- [ ] 权限检查已实现
- [ ] 错误信息不泄露敏感信息
- [ ] 安全头已设置
- [ ] 依赖已更新

### 定期安全审计
- 代码安全扫描
- 依赖漏洞扫描
- 渗透测试
- 安全配置审查

---

> **上下文提示**：在实现安全功能时，建议同时加载：
> - `coding.coding-style.md` - 编码风格规范
> - `coding.api.md` - 接口规范
> - `coding.testing.md` - 测试规范

