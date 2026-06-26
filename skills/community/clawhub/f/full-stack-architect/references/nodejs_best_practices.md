# Node.js 最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、Node.js 核心概念

### 1.1 事件循环

**理解：**
- 单线程异步非阻塞I/O
- 事件驱动架构
- 回调函数机制
- 定时器和微任务

**事件循环阶段：**
1. **Timers** - 执行setTimeout和setInterval回调
2. **Pending Callbacks** - 执行I/O回调
3. **Idle, Prepare** - 系统内部使用
4. **Poll** - 执行I/O操作
5. **Check** - 执行setImmediate回调
6. **Close Callbacks** - 执行关闭事件回调

---

### 1.2 模块系统

**CommonJS vs ES Modules：**

**CommonJS：**
```javascript
// 导出
module.exports = {
  foo: 'bar'
};

// 导入
const { foo } = require('./module');
```

**ES Modules：**
```javascript
// 导出
export const foo = 'bar';

// 导入
import { foo } from './module.js';
```

**建议：** 使用ES Modules，更现代的语法，支持树摇。

---

## 二、项目结构

### 2.1 推荐结构

```
project/
├── src/
│   ├── app/
│   │   ├── controllers/     # 控制器
│   │   ├── services/        # 业务逻辑
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # 路由
│   │   ├── middleware/      # 中间件
│   │   ├── utils/           # 工具函数
│   │   └── config/          # 配置
│   ├── index.js            # 入口文件
│   └── server.js           # 服务器配置
├── tests/                  # 测试文件
├── package.json            # 依赖管理
├── .env.example           # 环境变量示例
└── .gitignore             # Git忽略文件
```

---

### 2.2 配置管理

**最佳实践：**
- 使用环境变量管理配置
- 不同环境使用不同配置文件
- 敏感信息不要硬编码

**示例：**

```javascript
// config.js
require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  database: {
    url: process.env.DATABASE_URL,
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true
    }
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '24h'
  }
};
```

---

## 三、Express 最佳实践

### 3.1 基本结构

**示例：**

```javascript
// src/index.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由
app.use('/api/users', require('./app/routes/userRoutes'));
app.use('/api/posts', require('./app/routes/postRoutes'));

// 错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

---

### 3.2 路由设计

**最佳实践：**
- RESTful API设计
- 路由模块化
- 合理的路径命名
- 适当的HTTP方法使用

**示例：**

```javascript
// app/routes/userRoutes.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// GET /api/users
router.get('/', userController.getAllUsers);

// GET /api/users/:id
router.get('/:id', userController.getUserById);

// POST /api/users
router.post('/', userController.createUser);

// PUT /api/users/:id
router.put('/:id', userController.updateUser);

// DELETE /api/users/:id
router.delete('/:id', userController.deleteUser);

module.exports = router;
```

---

### 3.3 中间件

**常用中间件：**
- **express.json()** - 解析JSON请求体
- **express.urlencoded()** - 解析URL编码请求体
- **morgan** - 日志记录
- **cors** - 跨域资源共享
- **helmet** - 安全头部设置
- **express-rate-limit** - 速率限制

**自定义中间件示例：**

```javascript
// app/middleware/auth.js
const jwt = require('jsonwebtoken');

const auth = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

module.exports = auth;
```

---

## 四、数据库操作

### 4.1 MongoDB

**使用Mongoose：**

```javascript
// app/models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  role: {
    type: String,
    default: 'user'
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('User', userSchema);
```

**连接数据库：**

```javascript
// src/server.js
const mongoose = require('mongoose');
const config = require('./app/config');

mongoose.connect(config.database.url, config.database.options)
  .then(() => console.log('Database connected'))
  .catch(err => console.error('Database connection error:', err));
```

---

### 4.2 PostgreSQL

**使用Sequelize：**

```javascript
// app/models/User.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false
  }
}, {
  timestamps: true
});

module.exports = User;
```

---

## 五、认证与授权

### 5.1 JWT认证

**实现：**

```javascript
// app/controllers/authController.js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const User = require('../models/User');

const login = async (req, res) => {
  try {
    const { email, password } = req.body;
    
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const token = jwt.sign(
      { id: user._id, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    res.json({ token, user: { id: user._id, name: user.name, email: user.email } });
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
};

module.exports = { login };
```

---

### 5.2 密码处理

**最佳实践：**
- 使用bcrypt加密密码
- 设置适当的盐轮数
- 永不存储明文密码

**示例：**

```javascript
// 密码加密
const bcrypt = require('bcrypt');

const hashPassword = async (password) => {
  const saltRounds = 10;
  return await bcrypt.hash(password, saltRounds);
};

// 创建用户时使用
const createUser = async (req, res) => {
  try {
    const { name, email, password } = req.body;
    const hashedPassword = await hashPassword(password);
    
    const user = new User({
      name,
      email,
      password: hashedPassword
    });
    
    await user.save();
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
};
```

---

## 六、错误处理

### 6.1 错误处理中间件

**全局错误处理：**

```javascript
// app/middleware/errorHandler.js
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  res.status(statusCode).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = errorHandler;
```

**使用：**

```javascript
// src/index.js
const errorHandler = require('./app/middleware/errorHandler');

// 其他中间件和路由...

// 错误处理中间件应该在所有路由之后
app.use(errorHandler);
```

---

### 6.2 自定义错误类

**示例：**

```javascript
// app/utils/errors.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;
    
    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = AppError;
```

**使用：**

```javascript
// app/controllers/userController.js
const AppError = require('../utils/errors');

const getUserById = async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return next(new AppError('User not found', 404));
    }
    res.json(user);
  } catch (error) {
    next(error);
  }
};
```

---

## 七、性能优化

### 7.1 代码优化

**建议：**
- 使用异步/await
- 避免阻塞操作
- 合理使用缓存
- 优化数据库查询

**示例：**

```javascript
// 优化前
app.get('/api/users', (req, res) => {
  const users = User.find(); // 阻塞操作
  res.json(users);
});

// 优化后
app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find(); // 非阻塞
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});
```

---

### 7.2 数据库优化

**建议：**
- 创建索引
- 使用聚合管道
- 限制返回字段
- 分页查询

**示例：**

```javascript
// 优化查询
const optimizedQuery = async () => {
  // 创建索引
  await User.createIndex({ email: 1 });
  
  // 限制返回字段
  const users = await User.find({ role: 'admin' }, 'name email');
  
  // 分页
  const page = parseInt(req.query.page) || 1;
  const limit = 10;
  const skip = (page - 1) * limit;
  
  const usersWithPagination = await User.find()
    .skip(skip)
    .limit(limit)
    .exec();
};
```

---

### 7.3 缓存策略

**使用Redis：**

```javascript
const redis = require('redis');
const client = redis.createClient();

const getUsers = async (req, res) => {
  try {
    // 尝试从缓存获取
    const cachedUsers = await client.get('users');
    if (cachedUsers) {
      return res.json(JSON.parse(cachedUsers));
    }
    
    // 缓存未命中，从数据库获取
    const users = await User.find();
    
    // 存入缓存，设置过期时间
    await client.set('users', JSON.stringify(users), 'EX', 3600);
    
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
};
```

---

## 八、测试

### 8.1 单元测试

**使用Jest：**

```javascript
// tests/controllers/userController.test.js
const request = require('supertest');
const app = require('../../src/index');
const User = require('../../src/app/models/User');

jest.mock('../../src/app/models/User');

describe('User Controller', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  test('should get all users', async () => {
    const mockUsers = [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }];
    User.find.mockResolvedValue(mockUsers);
    
    const response = await request(app).get('/api/users');
    
    expect(response.statusCode).toBe(200);
    expect(response.body).toEqual(mockUsers);
    expect(User.find).toHaveBeenCalledTimes(1);
  });
});
```

---

### 8.2 集成测试

**示例：**

```javascript
// tests/integration/user.test.js
const request = require('supertest');
const app = require('../../src/index');
const mongoose = require('mongoose');

beforeAll(async () => {
  // 连接测试数据库
  await mongoose.connect('mongodb://localhost:27017/testdb');
});

afterAll(async () => {
  // 清理测试数据库
  await mongoose.connection.dropDatabase();
  await mongoose.connection.close();
});

describe('User API', () => {
  test('should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123'
      });
    
    expect(response.statusCode).toBe(201);
    expect(response.body.name).toBe('Test User');
    expect(response.body.email).toBe('test@example.com');
  });
});
```

---

## 九、部署

### 9.1 生产环境配置

**建议：**
- 使用PM2管理进程
- 配置环境变量
- 启用HTTPS
- 设置日志管理

**PM2配置：**

```json
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'app',
      script: 'src/index.js',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'development'
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 8080
      }
    }
  ]
};
```

---

### 9.2 Docker部署

**Dockerfile：**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "src/index.js"]
```

**docker-compose.yml：**

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=mongodb://mongo:27017/app
    depends_on:
      - mongo
  mongo:
    image: mongo:4.4
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

---

## 十、安全最佳实践

### 10.1 安全头部

**使用Helmet：**

```javascript
const helmet = require('helmet');
app.use(helmet());
```

### 10.2 CORS配置

**使用cors中间件：**

```javascript
const cors = require('cors');

// 允许所有跨域请求
app.use(cors());

// 配置特定来源
app.use(cors({
  origin: ['https://example.com', 'https://www.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### 10.3 输入验证

**使用express-validator：**

```javascript
const { body, validationResult } = require('express-validator');

const validateUser = [
  body('name').notEmpty().withMessage('Name is required'),
  body('email').isEmail().withMessage('Invalid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters')
];

app.post('/api/users', validateUser, (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  
  // 处理请求
});
```

### 10.4 防止SQL注入

**使用参数化查询：**

```javascript
// 不安全
const user = await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// 安全 - 使用参数化查询
const user = await db.query('SELECT * FROM users WHERE email = ?', [email]);
```

---

## 十一、监控与日志

### 11.1 日志管理

**使用Winston：**

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// 在开发环境中添加控制台输出
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

module.exports = logger;
```

### 11.2 监控

**使用PM2监控：**

```bash
# 启动监控
pm2 monit

# 查看状态
pm2 status

# 查看日志
pm2 logs
```

---

## 十二、常见问题与解决方案

### 12.1 内存泄漏

**问题：** 应用内存使用持续增长
**解决方案：**
- 使用Node.js内置的内存分析工具
- 检查事件监听器是否正确清理
- 避免全局变量累积
- 使用`heapdump`分析内存使用

### 12.2 性能瓶颈

**问题：** 响应时间过长
**解决方案：**
- 使用`clinic`分析性能
- 优化数据库查询
- 使用缓存
- 考虑水平扩展

### 12.3 错误处理不当

**问题：** 未捕获的错误导致应用崩溃
**解决方案：**
- 使用全局错误处理器
- 正确处理Promise错误
- 使用`uncaughtException`和`unhandledRejection`

---

## 十三、最佳实践总结

1. **项目结构**：模块化，清晰的目录结构
2. **代码质量**：使用ESLint和Prettier
3. **安全性**：使用HTTPS，输入验证，防止注入
4. **性能**：异步操作，缓存，数据库优化
5. **可靠性**：错误处理，日志，监控
6. **可维护性**：文档，测试，代码风格
7. **部署**：容器化，CI/CD，环境配置

---

## 相关资源

- [Node.js 官方文档](https://nodejs.org/docs/latest-v18.x/api/)
- [Express 官方文档](https://expressjs.com/)
- [Mongoose 官方文档](https://mongoosejs.com/)
- [Sequelize 官方文档](https://sequelize.org/)
- [Jest 官方文档](https://jestjs.io/)
- [PM2 官方文档](https://pm2.keymetrics.io/)

