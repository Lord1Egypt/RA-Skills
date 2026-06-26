# Node.js 代码片段

## 1. 基础服务器

### 1.1 Express 基础服务器

```javascript
// server.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由
app.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

// 启动服务器
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
```

### 1.2 Koa 基础服务器

```javascript
// server.js
const Koa = require('koa');
const bodyParser = require('koa-bodyparser');
const app = new Koa();
const port = process.env.PORT || 3000;

// 中间件
app.use(bodyParser());

// 路由
app.use(async (ctx) => {
  if (ctx.path === '/' && ctx.method === 'GET') {
    ctx.body = { message: 'Hello, World!' };
  }
});

// 启动服务器
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
```

## 2. 路由和控制器

### 2.1 Express 路由模块化

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// 用户路由
router.get('/', userController.getUsers);
router.get('/:id', userController.getUserById);
router.post('/', userController.createUser);
router.put('/:id', userController.updateUser);
router.delete('/:id', userController.deleteUser);

module.exports = router;
```

```javascript
// controllers/userController.js
const User = require('../models/User');

// 获取所有用户
exports.getUsers = async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// 根据ID获取用户
exports.getUserById = async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// 创建用户
exports.createUser = async (req, res) => {
  const user = new User({
    name: req.body.name,
    email: req.body.email,
    age: req.body.age
  });

  try {
    const savedUser = await user.save();
    res.status(201).json(savedUser);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

// 更新用户
exports.updateUser = async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // 更新字段
    if (req.body.name) user.name = req.body.name;
    if (req.body.email) user.email = req.body.email;
    if (req.body.age) user.age = req.body.age;

    const updatedUser = await user.save();
    res.json(updatedUser);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

// 删除用户
exports.deleteUser = async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    await user.remove();
    res.json({ message: 'User deleted' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
```

```javascript
// server.js
const express = require('express');
const app = express();
const userRoutes = require('./routes/users');

app.use(express.json());
app.use('/api/users', userRoutes);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 3. 数据库连接

### 3.1 MongoDB 连接

```javascript
// config/database.js
const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    console.log(`MongoDB connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

module.exports = connectDB;
```

```javascript
// server.js
const express = require('express');
const app = express();
const connectDB = require('./config/database');

// 连接数据库
connectDB();

app.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### 3.2 PostgreSQL 连接

```javascript
// config/database.js
const { Pool } = require('pg');

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT
});

// 测试连接
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Error connecting to PostgreSQL:', err);
  } else {
    console.log('PostgreSQL connected:', res.rows[0].now);
  }
});

module.exports = pool;
```

## 4. 认证和授权

### 4.1 JWT 认证

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const auth = (req, res, next) => {
  // 从请求头获取 token
  const token = req.header('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ message: 'No token, authorization denied' });
  }

  try {
    // 验证 token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Token is not valid' });
  }
};

module.exports = auth;
```

```javascript
// controllers/authController.js
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// 注册
exports.register = async (req, res) => {
  const { name, email, password } = req.body;

  try {
    // 检查用户是否已存在
    let user = await User.findOne({ email });
    if (user) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // 创建新用户
    user = new User({ name, email, password });

    // 加密密码
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(password, salt);

    // 保存用户
    await user.save();

    // 生成 token
    const token = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );

    res.json({ token });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// 登录
exports.login = async (req, res) => {
  const { email, password } = req.body;

  try {
    // 检查用户是否存在
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    // 验证密码
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    // 生成 token
    const token = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );

    res.json({ token });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
```

## 5. 错误处理

### 5.1 全局错误处理中间件

```javascript
// middleware/errorHandler.js
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  // 自定义错误
  if (err.name === 'ValidationError') {
    return res.status(400).json({ message: err.message });
  }

  // 404 错误
  if (err.name === 'NotFoundError') {
    return res.status(404).json({ message: err.message });
  }

  // 默认 500 错误
  res.status(500).json({ message: 'Server error' });
};

module.exports = errorHandler;
```

```javascript
// server.js
const express = require('express');
const app = express();
const errorHandler = require('./middleware/errorHandler');

// 路由
app.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

// 404 处理
app.use((req, res, next) => {
  const error = new Error('Not Found');
  error.name = 'NotFoundError';
  next(error);
});

// 全局错误处理
app.use(errorHandler);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 6. 文件上传

### 6.1 单文件上传

```javascript
// server.js
const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

// 配置存储
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

// 配置上传
const upload = multer({ storage });

// 确保上传目录存在
const fs = require('fs');
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

// 路由
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded' });
  }
  res.json({ message: 'File uploaded successfully', file: req.file });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### 6.2 多文件上传

```javascript
// server.js
const express = require('express');
const multer = require('multer');
const app = express();

// 配置存储
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

// 配置上传
const upload = multer({ storage });

// 路由
app.post('/upload-multiple', upload.array('files', 5), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: 'No files uploaded' });
  }
  res.json({ message: 'Files uploaded successfully', files: req.files });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 7. 中间件

### 7.1 日志中间件

```javascript
// middleware/logger.js
const logger = (req, res, next) => {
  console.log(`${req.method} ${req.url} - ${new Date().toISOString()}`);
  next();
};

module.exports = logger;
```

```javascript
// server.js
const express = require('express');
const app = express();
const logger = require('./middleware/logger');

// 使用日志中间件
app.use(logger);

app.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### 7.2 CORS 中间件

```javascript
// server.js
const express = require('express');
const cors = require('cors');
const app = express();

// 配置 CORS
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 8. 环境变量

### 8.1 使用 dotenv

```javascript
// server.js
const express = require('express');
const dotenv = require('dotenv');
const app = express();

// 加载环境变量
dotenv.config();

const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ 
    message: 'Hello, World!',
    environment: process.env.NODE_ENV || 'development'
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
```

```env
# .env
PORT=3000
NODE_ENV=development
MONGO_URI=mongodb://localhost:27017/myapp
JWT_SECRET=your-secret-key
```

## 9. 测试

### 9.1 使用 Jest 测试

```javascript
// tests/server.test.js
const request = require('supertest');
const app = require('../server');

describe('Server tests', () => {
  test('GET / should return 200 OK', async () => {
    const response = await request(app).get('/');
    expect(response.statusCode).toBe(200);
    expect(response.body.message).toBe('Hello, World!');
  });

  test('POST /api/users should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'Test User',
        email: 'test@example.com',
        age: 30
      });
    expect(response.statusCode).toBe(201);
    expect(response.body.name).toBe('Test User');
  });
});
```

## 10. 部署

### 10.1 PM2 部署

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'myapp',
      script: 'server.js',
      instances: 'max',
      env: {
        NODE_ENV: 'development'
      },
      env_production: {
        NODE_ENV: 'production'
      }
    }
  ]
};
```

### 10.2 Docker 部署

```dockerfile
# Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - MONGO_URI=mongodb://mongo:27017/myapp
    depends_on:
      - mongo

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

## 11. 性能优化

### 11.1 缓存中间件

```javascript
// middleware/cache.js
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 60 }); // 60秒过期

const cacheMiddleware = (duration) => {
  return (req, res, next) => {
    const key = req.originalUrl;
    const cachedResponse = cache.get(key);

    if (cachedResponse) {
      return res.json(cachedResponse);
    } else {
      // 重写 res.json 方法
      const originalJson = res.json;
      res.json = function(body) {
        cache.set(key, body, duration);
        return originalJson.call(this, body);
      };
      next();
    }
  };
};

module.exports = cacheMiddleware;
```

```javascript
// server.js
const express = require('express');
const cacheMiddleware = require('./middleware/cache');
const app = express();

// 使用缓存中间件，缓存时间为60秒
app.get('/api/data', cacheMiddleware(60), (req, res) => {
  // 模拟耗时操作
  setTimeout(() => {
    res.json({ 
      data: 'This is cached data',
      timestamp: new Date().toISOString()
    });
  }, 1000);
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### 11.2 压缩中间件

```javascript
// server.js
const express = require('express');
const compression = require('compression');
const app = express();

// 使用压缩中间件
app.use(compression());

app.get('/', (req, res) => {
  res.json({ 
    message: 'Hello, World!',
    data: 'This is a long response that will be compressed'
  });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 12. WebSocket

### 12.1 基本 WebSocket 服务器

```javascript
// server.js
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// 处理 WebSocket 连接
wss.on('connection', (ws) => {
  console.log('New client connected');

  // 发送欢迎消息
  ws.send('Welcome to the WebSocket server!');

  // 处理消息
  ws.on('message', (message) => {
    console.log(`Received: ${message}`);
    // 广播消息给所有客户端
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(`Server: ${message}`);
      }
    });
  });

  // 处理断开连接
  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// 普通 HTTP 路由
app.get('/', (req, res) => {
  res.send('WebSocket server running');
});

server.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 13. GraphQL

### 13.1 基本 GraphQL 服务器

```javascript
// server.js
const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const app = express();

// 定义 schema
const schema = buildSchema(`
  type Query {
    hello: String
    user(id: ID!): User
    users: [User]
  }
  
  type User {
    id: ID
    name: String
    email: String
    age: Int
  }
  
  type Mutation {
    createUser(name: String!, email: String!, age: Int!): User
  }
`);

// 模拟数据
const users = [
  { id: '1', name: 'John Doe', email: 'john@example.com', age: 30 },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', age: 25 }
];

// 根解析器
const root = {
  hello: () => 'Hello, World!',
  user: ({ id }) => users.find(user => user.id === id),
  users: () => users,
  createUser: ({ name, email, age }) => {
    const newUser = {
      id: String(users.length + 1),
      name,
      email,
      age
    };
    users.push(newUser);
    return newUser;
  }
};

// GraphQL 路由
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true // 启用 GraphiQL 界面
}));

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 14. 微服务

### 14.1 基本微服务架构

```javascript
// user-service/server.js
const express = require('express');
const app = express();

app.use(express.json());

// 用户服务路由
app.get('/api/users', (req, res) => {
  res.json([
    { id: 1, name: 'John Doe' },
    { id: 2, name: 'Jane Smith' }
  ]);
});

app.listen(3001, () => {
  console.log('User service running on port 3001');
});
```

```javascript
// order-service/server.js
const express = require('express');
const app = express();
const axios = require('axios');

app.use(express.json());

// 订单服务路由
app.get('/api/orders', (req, res) => {
  res.json([
    { id: 1, userId: 1, product: 'Product 1' },
    { id: 2, userId: 2, product: 'Product 2' }
  ]);
});

// 获取订单详情（包含用户信息）
app.get('/api/orders/:id', async (req, res) => {
  try {
    // 获取订单
    const order = { id: req.params.id, userId: 1, product: 'Product 1' };
    
    // 从用户服务获取用户信息
    const userResponse = await axios.get('http://localhost:3001/api/users/1');
    const user = userResponse.data;
    
    res.json({ ...order, user });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.listen(3002, () => {
  console.log('Order service running on port 3002');
});
```

```javascript
// gateway/server.js
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// 代理到用户服务
app.use('/api/users', createProxyMiddleware({
  target: 'http://localhost:3001',
  changeOrigin: true
}));

// 代理到订单服务
app.use('/api/orders', createProxyMiddleware({
  target: 'http://localhost:3002',
  changeOrigin: true
}));

app.listen(3000, () => {
  console.log('API Gateway running on port 3000');
});
```

*本代码片段库将持续更新，以反映 Node.js 的最新最佳实践和特性。*