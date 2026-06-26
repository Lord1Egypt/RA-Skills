# 安全最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、Web 应用安全

### 1.1 OWASP 十大安全风险

**2021 版 OWASP Top 10：**

1. **Broken Access Control**（失效的访问控制）
   - 未授权访问敏感数据
   - 水平越权和垂直越权
   - 缺少 CSRF 保护

2. **Cryptographic Failures**（加密失效）
   - 敏感数据未加密
   - 弱加密算法
   - 密钥管理不当

3. **Injection**（注入攻击）
   - SQL 注入
   - NoSQL 注入
   - 命令注入

4. **Insecure Design**（不安全的设计）
   - 缺少安全设计原则
   - 不安全的默认配置
   - 缺少威胁建模

5. **Security Misconfiguration**（安全配置错误）
   - 默认配置未修改
   - 不必要的服务和端口
   - 过度的权限

6. **Vulnerable and Outdated Components**（易受攻击的组件）
   - 使用有漏洞的库
   - 未及时更新依赖

7. **Identification and Authentication Failures**（身份认证失效）
   - 弱密码策略
   - 会话管理不当
   - 缺少多因素认证

8. **Software and Data Integrity Failures**（软件和数据完整性失效）
   - 未验证软件更新
   - 缺少数字签名

9. **Security Logging and Monitoring Failures**（安全日志和监控失效）
   - 缺少日志记录
   - 监控不足
   - 响应时间慢

10. **Server-Side Request Forgery**（服务器端请求伪造）
    - 服务器被欺骗向内部系统发送请求

---

### 1.2 输入验证

**最佳实践：**
- 所有用户输入必须验证
- 使用白名单而非黑名单
- 验证数据类型、长度、格式
- 服务端和客户端都需验证

**示例：**

```javascript
// 客户端验证
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// 服务端验证 (Express.js)
const { body, validationResult } = require('express-validator');

app.post('/register', 
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // 处理注册
  }
);
```

---

### 1.3 认证与授权

**认证最佳实践：**
- 使用 bcrypt 等算法哈希存储密码
- 实施密码强度要求
- 支持多因素认证
- 限制登录尝试次数
- 实现账户锁定机制

**授权最佳实践：**
- 基于角色的访问控制（RBAC）
- 最小权限原则
- 权限检查在服务端执行
- 定期权限审计

**示例：**

```javascript
// 密码哈希
const bcrypt = require('bcrypt');

async function hashPassword(password) {
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// RBAC 中间件
function requireRole(role) {
  return (req, res, next) => {
    if (!req.user || !req.user.roles.includes(role)) {
      return res.status(403).json({ error: 'Access denied' });
    }
    next();
  };
}

// 使用
app.get('/admin', requireRole('admin'), (req, res) => {
  // 管理员操作
});
```

---

### 1.4 会话管理

**最佳实践：**
- 使用安全的会话存储
- 设置合理的会话超时
- 生成安全的会话标识符
- 实施 CSRF 保护
- 会话固定攻击防护

**示例：**

```javascript
// Express.js 会话配置
const session = require('express-session');
const RedisStore = require('connect-redis')(session);

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000 // 24小时
  }
}));

// CSRF 保护
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/form', csrfProtection, (req, res) => {
  // 处理表单提交
});
```

---

### 1.5 数据保护

**最佳实践：**
- 敏感数据加密存储
- 传输层使用 HTTPS
- 实施内容安全策略（CSP）
- 使用安全的加密算法
- 定期密钥轮换

**示例：**

```javascript
// 数据加密
const crypto = require('crypto');

function encryptData(data, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return { iv: iv.toString('hex'), encryptedData: encrypted };
}

function decryptData(encryptedData, iv, key) {
  const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), Buffer.from(iv, 'hex'));
  let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

// CSP 头部
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline';"
  );
  next();
});
```

---

## 二、API 安全

### 2.1 REST API 安全

**最佳实践：**
- 使用 HTTPS
- 实施认证（JWT、OAuth 2.0）
- 速率限制
- 输入验证
- 错误处理（不暴露敏感信息）

**JWT 认证示例：**

```javascript
const jwt = require('jsonwebtoken');

// 生成 token
function generateToken(user) {
  return jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
}

// 验证 token
function verifyToken(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// 使用
app.get('/api/protected', verifyToken, (req, res) => {
  res.json({ message: 'Protected resource' });
});
```

---

### 2.2 GraphQL 安全

**最佳实践：**
- 限制查询深度
- 实施查询复杂度分析
- 认证和授权
- 输入验证
- 速率限制

**示例：**

```javascript
// Apollo Server 安全配置
const { ApolloServer } = require('apollo-server-express');
const depthLimit = require('graphql-depth-limit');
const { createComplexityLimitRule } = require('graphql-validation-complexity');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(5), // 限制查询深度
    createComplexityLimitRule(1000) // 限制查询复杂度
  ],
  context: ({ req }) => {
    // 认证逻辑
    const token = req.headers.authorization?.split(' ')[1];
    const user = verifyToken(token);
    return { user };
  }
});
```

---

### 2.3 API 速率限制

**最佳实践：**
- 基于 IP 的速率限制
- 基于用户的速率限制
- 不同端点不同限制
- 合理的错误信息
- 缓存限制状态

**示例：**

```javascript
// Express.js 速率限制
const rateLimit = require('express-rate-limit');

// 通用限制
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 每IP限制100次请求
  message: { error: 'Too many requests, please try again later' }
});

// 登录端点限制
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 每IP限制5次登录尝试
  message: { error: 'Too many login attempts, please try again later' }
});

// 使用
app.use('/api', generalLimiter);
app.post('/api/login', loginLimiter, loginHandler);
```

---

## 三、数据库安全

### 3.1 SQL 注入防护

**最佳实践：**
- 使用参数化查询
- 使用 ORM 框架
- 最小权限原则
- 输入验证
- 定期安全审计

**示例：**

```javascript
// 不安全的查询
// const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

// 安全的参数化查询
const query = 'SELECT * FROM users WHERE username = ? AND password = ?';
db.query(query, [username, password], (err, results) => {
  // 处理结果
});

// 使用 ORM (Sequelize)
const User = sequelize.define('User', {
  username: DataTypes.STRING,
  password: DataTypes.STRING
});

// 安全查询
const user = await User.findOne({
  where: {
    username: username,
    password: password
  }
});
```

---

### 3.2 NoSQL 注入防护

**最佳实践：**
- 输入验证
- 使用参数化查询
- 限制查询条件
- 最小权限原则
- 避免使用 $where 操作符

**示例：**

```javascript
// 不安全的查询
// const query = { username: req.body.username, password: req.body.password };

// 安全的查询
const query = {
  username: req.body.username,
  password: req.body.password
};

// 验证输入类型
if (typeof query.username !== 'string' || typeof query.password !== 'string') {
  return res.status(400).json({ error: 'Invalid input' });
}

const user = await db.collection('users').findOne(query);
```

---

### 3.3 数据库加密

**最佳实践：**
- 敏感数据加密存储
- 传输加密
- 密钥管理
- 定期密钥轮换
- 备份加密

**示例：**

```javascript
// MongoDB 字段级加密
const { ClientEncryption } = require('mongodb-client-encryption');

const clientEncryption = new ClientEncryption({
  keyVaultNamespace: 'encryption.__keyVault',
  kmsProviders: {
    local: {
      key: Buffer.from(process.env.ENCRYPTION_KEY, 'base64')
    }
  }
});

// 加密字段
const encryptedField = await clientEncryption.encrypt(
  'sensitive data',
  {
    algorithm: 'AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic'
  }
);

// 存储加密数据
db.collection('users').insertOne({
  name: 'John',
  ssn: encryptedField
});
```

---

## 四、服务器安全

### 4.1 服务器配置

**最佳实践：**
- 最小化安装
- 及时更新系统
- 关闭不必要的服务
- 配置防火墙
- 禁用 root 登录
- 使用 SSH 密钥认证

**示例：**

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装防火墙
sudo apt install ufw -y
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 禁用 root 登录
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

---

### 4.2 环境变量管理

**最佳实践：**
- 使用 .env 文件管理敏感配置
- 不将 .env 文件提交到版本控制
- 使用环境变量存储密钥
- 不同环境使用不同配置
- 定期轮换密钥

**示例：**

```javascript
// .env 文件
NODE_ENV=production
DATABASE_URL=mongodb://user:password@localhost:27017/db
JWT_SECRET=your-secret-key
API_KEY=your-api-key

// 使用环境变量
require('dotenv').config();

const dbUrl = process.env.DATABASE_URL;
const jwtSecret = process.env.JWT_SECRET;

// 数据库连接
mongoose.connect(dbUrl, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});
```

---

### 4.3 安全日志

**最佳实践：**
- 记录所有安全相关事件
- 日志集中管理
- 定期日志审计
- 日志保留策略
- 防日志篡改

**示例：**

```javascript
// Winston 日志配置
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console()
  ]
});

// 记录安全事件
app.post('/login', (req, res) => {
  try {
    // 登录逻辑
    logger.info('User logged in', { username: req.body.username, ip: req.ip });
    res.json({ message: 'Login successful' });
  } catch (error) {
    logger.error('Login failed', { username: req.body.username, ip: req.ip, error: error.message });
    res.status(401).json({ error: 'Invalid credentials' });
  }
});
```

---

## 五、前端安全

### 5.1 XSS 防护

**最佳实践：**
- 输入验证
- 输出编码
- 使用 Content-Security-Policy
- 避免使用 innerHTML
- 使用安全的框架

**示例：**

```javascript
// 不安全的代码
// document.getElementById('output').innerHTML = userInput;

// 安全的代码
document.getElementById('output').textContent = userInput;

// React 自动转义
function UserProfile({ user }) {
  return <div>{user.name}</div>; // 自动转义
}

// 如需插入 HTML
function SafeHTML({ html }) {
  return <div dangerouslySetInnerHTML={{ __html: sanitize(html) }} />;
}

// 内容安全策略
// 在服务器端设置
res.setHeader(
  'Content-Security-Policy',
  "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
);
```

---

### 5.2 CSRF 防护

**最佳实践：**
- 使用 CSRF 令牌
- 验证 Origin/Referer 头
- 使用 SameSite Cookie
- 实施双重提交防护

**示例：**

```javascript
// Express.js CSRF 保护
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/form', csrfProtection, (req, res) => {
  // 处理表单提交
});

// 前端表单
<form action="/form" method="POST">
  <input type="hidden" name="_csrf" value="<%= csrfToken %>">
  <!-- 其他表单字段 -->
  <button type="submit">Submit</button>
</form>

// SameSite Cookie
app.use(session({
  cookie: {
    sameSite: 'strict', // 或 'lax'
    secure: true,
    httpOnly: true
  }
}));
```

---

### 5.3 前端数据保护

**最佳实践：**
- 不在前端存储敏感数据
- 使用 HTTPS
- 敏感操作二次验证
- 前端输入验证
- 避免硬编码密钥

**示例：**

```javascript
// 不安全的做法
// const apiKey = 'your-api-key';

// 安全的做法
// 从服务器获取或使用环境变量
const apiKey = process.env.REACT_APP_API_KEY;

// 敏感操作验证
function deleteAccount() {
  if (confirm('Are you sure you want to delete your account?')) {
    // 二次验证
    const password = prompt('Please enter your password to confirm');
    if (password) {
      // 调用 API 删除账户
    }
  }
}

// 前端输入验证
function validateForm(formData) {
  const errors = {};
  if (!formData.email) {
    errors.email = 'Email is required';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    errors.email = 'Invalid email format';
  }
  return errors;
}
```

---

## 六、云服务安全

### 6.1 AWS 安全

**最佳实践：**
- 使用 IAM 角色和策略
- 启用 MFA
- 配置安全组
- 启用 CloudTrail
- 使用 KMS 加密
- 定期安全评估

**示例：**

```yaml
# IAM 策略示例
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::my-bucket"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}

# 安全组配置
{
  "Type": "AWS::EC2::SecurityGroup",
  "Properties": {
    "GroupDescription": "Web server security group",
    "SecurityGroupIngress": [
      {
        "IpProtocol": "tcp",
        "FromPort": 80,
        "ToPort": 80,
        "CidrIp": "0.0.0.0/0"
      },
      {
        "IpProtocol": "tcp",
        "FromPort": 443,
        "ToPort": 443,
        "CidrIp": "0.0.0.0/0"
      }
    ]
  }
}
```

---

### 6.2 Azure 安全

**最佳实践：**
- 使用 Azure AD 进行身份管理
- 启用 Azure Security Center
- 配置网络安全组
- 使用 Key Vault 管理密钥
- 启用 Azure Monitor
- 定期安全扫描

**示例：**

```powershell
# 创建 Azure Key Vault
New-AzKeyVault -Name "my-keyvault" -ResourceGroupName "my-resource-group" -Location "eastus"

# 存储密钥
Set-AzKeyVaultSecret -VaultName "my-keyvault" -Name "api-key" -SecretValue (ConvertTo-SecureString "my-secret-value" -AsPlainText -Force)

# 网络安全组规则
$rule1 = New-AzNetworkSecurityRuleConfig -Name "Allow-HTTP" -Description "Allow HTTP" -Access Allow -Protocol Tcp -Direction Inbound -Priority 100 -SourceAddressPrefix * -SourcePortRange * -DestinationAddressPrefix * -DestinationPortRange 80

$nsg = New-AzNetworkSecurityGroup -Name "my-nsg" -ResourceGroupName "my-resource-group" -Location "eastus" -SecurityRules $rule1
```

---

### 6.3 GCP 安全

**最佳实践：**
- 使用 IAM 权限
- 启用 Cloud Identity-Aware Proxy
- 配置 VPC 防火墙
- 使用 Secret Manager
- 启用 Cloud Audit Logs
- 定期安全评估

**示例：**

```bash
# 创建 Secret
gcloud secrets create api-key --replication-policy="automatic"
gcloud secrets versions add api-key --data-file=/path/to/api-key.txt

# 防火墙规则
gcloud compute firewall-rules create allow-http --allow=tcp:80 --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create allow-https --allow=tcp:443 --source-ranges=0.0.0.0/0

# IAM 权限
gcloud projects add-iam-policy-binding my-project \
  --member=user:user@example.com \
  --role=roles/storage.objectViewer
```

---

## 七、容器安全

### 7.1 Docker 安全

**最佳实践：**
- 使用官方基础镜像
- 最小化镜像大小
- 避免使用 root 用户
- 扫描镜像漏洞
- 限制容器权限
- 安全的 Dockerfile

**示例：**

```dockerfile
# 安全的 Dockerfile
FROM node:18-alpine

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S appuser -u 1001

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production && \
    npm cache clean --force

# 复制应用代码
COPY --chown=appuser:nodejs . .

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["node", "src/index.js"]
```

**镜像扫描：**

```bash
# 使用 Trivy 扫描镜像
docker pull aquasec/trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image myapp:latest
```

---

### 7.2 Kubernetes 安全

**最佳实践：**
- 使用 RBAC 权限控制
- 配置网络策略
- 使用 Secret 管理敏感信息
- 启用 Pod 安全策略
- 定期安全审计
- 限制资源使用

**示例：**

```yaml
# RBAC 配置
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
- kind: User
  name: user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io

# 网络策略
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

---

## 八、安全测试

### 8.1 渗透测试

**最佳实践：**
- 定期进行渗透测试
- 使用专业工具
- 测试所有攻击面
- 模拟真实攻击场景
- 生成详细报告

**常用工具：**
- **OWASP ZAP**：自动化安全扫描
- **Burp Suite**：Web 应用渗透测试
- **Nmap**：网络扫描
- **Metasploit**：漏洞利用
- **Nikto**：Web 服务器扫描

**示例：**

```bash
# 使用 OWASP ZAP 扫描
zap-cli quick-scan --self-contained --start-options "-config api.disablekey=true" https://example.com

# 使用 Nmap 扫描
nmap -sV -p 1-65535 example.com

# 使用 Nikto 扫描
nikto -h https://example.com
```

---

### 8.2 代码审计

**最佳实践：**
- 定期代码审计
- 使用静态代码分析工具
- 检查安全漏洞
- 验证安全配置
- 确保代码符合安全标准

**常用工具：**
- **SonarQube**：代码质量和安全分析
- **ESLint**：JavaScript 代码分析
- **Pylint**：Python 代码分析
- **Checkmarx**：静态代码分析
- **Fortify**：应用安全测试

**示例：**

```bash
# 使用 ESLint 检查安全问题
npx eslint --plugin security --ext .js,.ts src/

# 使用 SonarQube 分析
sonar-scanner -Dsonar.projectKey=my-project -Dsonar.sources=src

# 使用 Bandit 检查 Python 代码
bandit -r src/
```

---

### 8.3 漏洞扫描

**最佳实践：**
- 定期漏洞扫描
- 扫描依赖项
- 扫描容器镜像
- 扫描网络设备
- 及时修复漏洞

**常用工具：**
- **Trivy**：容器和依赖扫描
- **Snyk**：依赖项漏洞扫描
- **OpenVAS**：网络漏洞扫描
- **Nessus**：漏洞评估
- **Qualys**：安全和合规性管理

**示例：**

```bash
# 使用 Snyk 扫描依赖
npx snyk test

# 使用 Trivy 扫描镜像
trivy image myapp:latest

# 使用 OpenVAS 扫描
openvas-cli --scan-target 192.168.1.1/24
```

---

## 九、安全事件响应

### 9.1 响应流程

**最佳实践：**
- 建立安全事件响应团队
- 制定响应计划
- 快速识别和响应
- 控制影响范围
- 恢复系统
- 事后分析

**响应步骤：**
1. **准备**：建立响应团队和计划
2. **检测**：识别安全事件
3. **分析**：确定事件性质和影响
4. **控制**：遏制事件影响
5. **根除**：移除威胁
6. **恢复**：恢复系统正常运行
7. **总结**：分析事件原因和改进措施

---

### 9.2 事件分类

**常见安全事件：**
- **数据泄露**：敏感数据被未授权访问
- **恶意代码**：病毒、木马、勒索软件
- **拒绝服务**：DoS/DDoS 攻击
- **权限提升**：未授权获取更高权限
- **网络入侵**：未授权访问网络
- **社会工程**：钓鱼、诈骗

---

### 9.3 应急响应

**示例响应计划：**

```
# 安全事件响应计划

## 1. 响应团队
- 安全负责人：负责协调响应
- 系统管理员：负责系统恢复
- 网络管理员：负责网络隔离
- 开发人员：负责代码修复
- 法律团队：负责法律合规

## 2. 响应流程
### 2.1 检测与分析
- 监控系统告警
- 分析日志和流量
- 确认事件性质

### 2.2 遏制与根除
- 隔离受影响系统
- 终止恶意进程
- 修补漏洞

### 2.3 恢复与总结
- 恢复系统功能
- 验证安全性
- 记录事件详情
- 制定改进措施

## 3. 联系方式
- 紧急联系人：XXX (电话)
- 安全团队：security@example.com
- 外部专家：XXX (电话)
```

---

## 十、最佳实践总结

1. **输入验证**：所有用户输入必须验证
2. **认证授权**：实施强认证和细粒度授权
3. **数据保护**：敏感数据加密存储和传输
4. **安全配置**：最小权限原则和安全默认配置
5. **漏洞管理**：定期扫描和修复漏洞
6. **日志监控**：全面的日志记录和监控
7. **安全测试**：定期渗透测试和代码审计
8. **事件响应**：建立完善的安全事件响应机制
9. **持续学习**：关注最新安全威胁和防护技术
10. **安全文化**：培养团队安全意识

---

## 相关资源

- [OWASP 官方网站](https://owasp.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST 网络安全框架](https://www.nist.gov/cyberframework)
- [SANS 安全资源](https://www.sans.org/)
- [CWE/SANS 最危险的软件错误](https://www.sans.org/top25-software-errors)
- [Mozilla 安全最佳实践](https://infosec.mozilla.org/guidelines/web_security)
- [Google 安全工程](https://security.google.com/)

