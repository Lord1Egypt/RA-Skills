# 后端框架最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、Express.js 最佳实践

### 1.1 项目结构

**推荐结构：**

```
project/
├── src/
│   ├── controllers/     # 控制器
│   ├── routes/         # 路由
│   ├── services/       # 业务逻辑
│   ├── models/         # 数据模型
│   ├── middleware/     # 中间件
│   ├── utils/          # 工具函数
│   ├── config/         # 配置
│   ├── app.js          # 应用配置
│   └── server.js        # 服务器启动
├── tests/              # 测试
├── package.json
└── .env
```

**命名规范：**
- 文件：kebab-case（user-controller.js）
- 变量：camelCase
- 常量：UPPERCASE
- 类：PascalCase
- 函数：camelCase

---

### 1.2 中间件

**最佳实践：**
- 错误处理中间件
- 日志中间件
- 认证中间件
-  cors 中间件
- 速率限制中间件

**示例：**

```javascript
// 错误处理中间件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: {
      message: err.message || 'Internal Server Error'
    }
  });
});

// 日志中间件
app.use((req, res, next) => {
  const start = Date.now();
  const method = req.method;
  const url = req.url;
  
  res.on('finish', () => {
    const end = Date.now();
    const duration = end - start;
    const status = res.statusCode;
    console.log(`${method} ${url} ${status} ${duration}ms`);
  });
  
  next();
});

// 认证中间件
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  // 验证 token
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// 使用
app.get('/protected', authenticate, (req, res) => {
  res.json({ message: 'Protected resource' });
});
```

---

### 1.3 路由

**最佳实践：**
- 模块化路由
- RESTful API 设计
- 路由参数验证
- 合理的路由命名

**示例：**

```javascript
// routes/user.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/user-controller');
const authenticate = require('../middleware/authenticate');

router.get('/', userController.getAllUsers);
router.get('/:id', userController.getUserById);
router.post('/', userController.createUser);
router.put('/:id', authenticate, userController.updateUser);
router.delete('/:id', authenticate, userController.deleteUser);

module.exports = router;

// app.js
const express = require('express');
const app = express();
const userRoutes = require('./routes/user');

app.use('/api/users', userRoutes);
```

---

### 1.4 数据库集成

**最佳实践：**
- 使用 ORM（Sequelize、Mongoose）
- 连接池配置
- 事务管理
- 数据验证

**示例：**

```javascript
// 使用 Mongoose
const mongoose = require('mongoose');

// 连接数据库
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  useCreateIndex: true,
  useFindAndModify: false
});

// 定义模型
const UserSchema = new mongoose.Schema({
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
  }
});

const User = mongoose.model('User', UserSchema);

// 使用模型
app.post('/api/users', async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});
```

---

### 1.5 性能优化

**最佳实践：**
- 缓存
- 压缩
- 合理的数据库查询
- 避免阻塞操作
- 负载均衡

**示例：**

```javascript
// 缓存中间件
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 60 });

function cacheMiddleware(duration) {
  return (req, res, next) => {
    const key = req.originalUrl;
    const cachedResponse = cache.get(key);
    
    if (cachedResponse) {
      return res.json(cachedResponse);
    }
    
    res.originalJson = res.json;
    res.json = function(body) {
      cache.set(key, body, duration);
      return res.originalJson(body);
    };
    
    next();
  };
}

// 使用
app.get('/api/users', cacheMiddleware(300), userController.getAllUsers);

// 压缩
const compression = require('compression');
app.use(compression());

// 数据库查询优化
app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find().select('-password').limit(100);
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## 二、Nest.js 最佳实践

### 2.1 项目结构

**推荐结构：**

```
src/
├── modules/
│   ├── user/
│   │   ├── user.controller.ts
│   │   ├── user.service.ts
│   │   ├── user.module.ts
│   │   ├── user.model.ts
│   │   └── user.dto.ts
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.module.ts
│   │   └── auth.guard.ts
│   └── app.module.ts
├── shared/
│   ├── filters/
│   ├── guards/
│   ├── interceptors/
│   └── utils/
├── config/
└── main.ts
```

**命名规范：**
- 文件：kebab-case（user.controller.ts）
- 类：PascalCase（UserController）
- 变量：camelCase
- 常量：UPPERCASE
- 方法：camelCase

---

### 2.2 控制器

**最佳实践：**
- 使用装饰器
- 合理的路由设计
- 输入验证
- 错误处理

**示例：**

```typescript
import { Controller, Get, Post, Put, Delete, Param, Body, UseGuards } from '@nestjs/common';
import { UserService } from './user.service';
import { CreateUserDto, UpdateUserDto } from './user.dto';
import { AuthGuard } from '../auth/auth.guard';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  async getAllUsers() {
    return this.userService.getAll();
  }

  @Get(':id')
  async getUserById(@Param('id') id: string) {
    return this.userService.getById(id);
  }

  @Post()
  async createUser(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  @Put(':id')
  @UseGuards(AuthGuard)
  async updateUser(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.userService.update(id, updateUserDto);
  }

  @Delete(':id')
  @UseGuards(AuthGuard)
  async deleteUser(@Param('id') id: string) {
    return this.userService.delete(id);
  }
}
```

---

### 2.3 服务

**最佳实践：**
- 业务逻辑分离
- 依赖注入
- 异步操作
- 错误处理

**示例：**

```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { User } from './user.model';
import { CreateUserDto, UpdateUserDto } from './user.dto';

@Injectable()
export class UserService {
  constructor(@InjectModel(User.name) private userModel: Model<User>) {}

  async getAll(): Promise<User[]> {
    return this.userModel.find().select('-password').exec();
  }

  async getById(id: string): Promise<User> {
    const user = await this.userModel.findById(id).select('-password').exec();
    if (!user) {
      throw new NotFoundException(`User with id ${id} not found`);
    }
    return user;
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = new this.userModel(createUserDto);
    return user.save();
  }

  async update(id: string, updateUserDto: UpdateUserDto): Promise<User> {
    const user = await this.userModel.findByIdAndUpdate(id, updateUserDto, { new: true }).exec();
    if (!user) {
      throw new NotFoundException(`User with id ${id} not found`);
    }
    return user;
  }

  async delete(id: string): Promise<void> {
    const result = await this.userModel.findByIdAndDelete(id).exec();
    if (!result) {
      throw new NotFoundException(`User with id ${id} not found`);
    }
  }
}
```

---

### 2.4 模块

**最佳实践：**
- 模块化设计
- 合理的依赖管理
- 共享模块
- 动态模块

**示例：**

```typescript
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { UserController } from './user.controller';
import { UserService } from './user.service';
import { User, UserSchema } from './user.model';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: User.name, schema: UserSchema }])
  ],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService]
})
export class UserModule {}

// 应用模块
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { UserModule } from './user/user.module';
import { AuthModule } from './auth/auth.module';

@Module({
  imports: [
    MongooseModule.forRoot(process.env.MONGODB_URI),
    UserModule,
    AuthModule
  ]
})
export class AppModule {}
```

---

### 2.5 守卫和拦截器

**最佳实践：**
- 认证守卫
- 授权守卫
- 日志拦截器
- 异常拦截器

**示例：**

```typescript
// 认证守卫
import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    
    if (!token) {
      throw new UnauthorizedException('No token provided');
    }
    
    try {
      const payload = await this.jwtService.verifyAsync(token, {
        secret: process.env.JWT_SECRET
      });
      request.user = payload;
    } catch {
      throw new UnauthorizedException('Invalid token');
    }
    
    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = (request.headers as any).authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}

// 日志拦截器
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, Logger } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(LoggingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    const request = context.switchToHttp().getRequest();
    const method = request.method;
    const url = request.url;

    return next.handle().pipe(
      tap(() => {
        const duration = Date.now() - now;
        const response = context.switchToHttp().getResponse();
        const status = response.statusCode;
        this.logger.log(`${method} ${url} ${status} ${duration}ms`);
      })
    );
  }
}
```

---

## 三、Django 最佳实践

### 3.1 项目结构

**推荐结构：**

```
project/
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── user/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   └── admin.py
│   └── blog/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── serializers.py
│       └── admin.py
├── static/
├── media/
├── templates/
└── manage.py
```

**命名规范：**
- 应用：snake_case
- 模型：PascalCase
- 视图：camelCase 或 snake_case
- 函数：snake_case
- 变量：snake_case

---

### 3.2 模型

**最佳实践：**
- 合理的字段设计
- 索引优化
- 关系设计
- 验证

**示例：**

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator()]
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'created_at']),
        ]
```

---

### 3.3 视图

**最佳实践：**
- 使用类视图
- 合理的权限控制
- 分页
- 错误处理

**示例：**

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

---

### 3.4 API（Django REST Framework）

**最佳实践：**
- 使用序列化器
- 视图集
- 权限
- 过滤和排序

**示例：**

```python
from rest_framework import viewsets, permissions, filters
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

# 序列化器
from rest_framework import serializers
from .models import Post, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
```

---

### 3.5 中间件和信号

**最佳实践：**
- 自定义中间件
- 信号处理
- 缓存
- 安全中间件

**示例：**

```python
# 自定义中间件
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"{request.method} {request.path} {response.status_code} {duration:.2f}s")
        return response

# 信号处理
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        # 发送欢迎邮件
        send_welcome_email(instance)

# 缓存
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')
class PostListView(ListView):
    model = Post
    # ...
```

---

## 四、Flask 最佳实践

### 4.1 项目结构

**推荐结构：**

```
project/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── middleware/
│   ├── templates/
│   ├── static/
│   └── config.py
├── migrations/
├── tests/
├── requirements.txt
├── .env
└── run.py
```

**命名规范：**
- 文件：snake_case
- 变量：snake_case
- 函数：snake_case
- 类：PascalCase

---

### 4.2 应用配置

**最佳实践：**
- 环境变量配置
- 不同环境配置
- 安全配置

**示例：**

```python
# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import register_routes
    register_routes(app)
    
    return app
```

---

### 4.3 路由

**最佳实践：**
- 蓝图
- RESTful API
- 路由参数验证
- 错误处理

**示例：**

```python
# app/routes/__init__.py
def register_routes(app):
    from .user import user_bp
    from .post import post_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(post_bp, url_prefix='/api/posts')

# app/routes/user.py
from flask import Blueprint, request, jsonify
from ..controllers.user_controller import UserController
from ..middleware.auth import auth_required

user_bp = Blueprint('user', __name__)
user_controller = UserController()

@user_bp.route('/', methods=['GET'])
def get_users():
    users = user_controller.get_all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = user_controller.get_by_id(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_controller.create(data)
    return jsonify(user.to_dict()), 201

@user_bp.route('/<int:id>', methods=['PUT'])
@auth_required
def update_user(id):
    data = request.get_json()
    user = user_controller.update(id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/<int:id>', methods=['DELETE'])
@auth_required
def delete_user(id):
    success = user_controller.delete(id)
    if not success:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200
```

---

### 4.4 数据库

**最佳实践：**
- SQLAlchemy ORM
- 迁移
- 事务
- 索引

**示例：**

```python
# app/models/user.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# 迁移
# 初始化迁移
def init_migrations():
    from flask_migrate import MigrateCommand
    from flask_script import Manager
    from app import create_app, db
    
    app = create_app()
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager

# 命令
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
```

---

### 4.5 中间件和装饰器

**最佳实践：**
- 认证装饰器
- 日志中间件
- 错误处理
- CORS

**示例：**

```python
# app/middleware/auth.py
from functools import wraps
from flask import request, jsonify
import jwt
from app import app

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            token = token.split(' ')[1]  # Bearer token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data['user_id']
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# app/middleware/logging.py
from flask import request
import time

def logging_middleware(app):
    @app.before_request
    def before_request():
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        duration = time.time() - request.start_time
        print(f"{request.method} {request.path} {response.status_code} {duration:.2f}s")
        return response

# 使用
app = create_app()
logging_middleware(app)
```

---

## 五、后端框架通用最佳实践

### 5.1 代码组织

**最佳实践：**
- 模块化设计
- 关注点分离
- 合理的目录结构
- 代码复用

**示例：**

```
# 良好的代码组织
app/
├── api/            # API层
├── services/       # 业务逻辑
├── models/         # 数据模型
├── schemas/        # 数据验证
├── middleware/     # 中间件
├── utils/          # 工具函数
└── config/         # 配置

# 关注点分离
# 控制器/视图：处理HTTP请求和响应
# 服务：处理业务逻辑
# 模型：处理数据存储
# 中间件：处理横切关注点
```

---

### 5.2 性能优化

**通用最佳实践：**
- 缓存
- 数据库优化
- 异步处理
- 负载均衡
- 代码优化

**示例：**

```javascript
// 缓存示例 (Node.js)
const Redis = require('ioredis');
const redis = new Redis();

async function getCachedData(key, fetchFunction) {
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }
  
  const data = await fetchFunction();
  await redis.set(key, JSON.stringify(data), 'EX', 3600);
  return data;
}

// 使用
app.get('/api/users', async (req, res) => {
  const users = await getCachedData('users', async () => {
    return await User.find().select('-password');
  });
  res.json(users);
});

# 数据库优化 (Python)
# 批量查询
users = User.objects.filter(active=True).only('id', 'username', 'email')

# 预加载
posts = Post.objects.select_related('author').prefetch_related('comments')

# 索引
class User(models.Model):
    # ...
    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
```

---

### 5.3 安全

**通用最佳实践：**
- 输入验证
- 认证和授权
- 密码哈希
- HTTPS
- 防止 SQL 注入
- CORS 配置

**示例：**

```javascript
// 输入验证 (Express)
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // 处理请求
  }
);

# 密码哈希 (Python)
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # ...
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

// CORS 配置 (Express)
const cors = require('cors');
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

---

### 5.4 测试

**通用最佳实践：**
- 单元测试
- 集成测试
- E2E 测试
- 测试覆盖率
- 自动化测试

**示例：**

```javascript
// 单元测试 (Jest)
test('User controller should create user', async () => {
  const userData = { name: 'John', email: 'john@example.com', password: 'password123' };
  const user = await userController.create(userData);
  expect(user).toHaveProperty('id');
  expect(user.name).toBe('John');
  expect(user.email).toBe('john@example.com');
});

# 单元测试 (Python - pytest)
def test_user_creation():
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.check_password('password123')

// 集成测试 (Supertest)
test('POST /api/users should create user', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ name: 'John', email: 'john@example.com', password: 'password123' });
  
  expect(response.statusCode).toBe(201);
  expect(response.body).toHaveProperty('id');
  expect(response.body.name).toBe('John');
});
```

---

### 5.5 部署

**通用最佳实践：**
- 容器化
- CI/CD
- 环境变量管理
- 日志管理
- 监控

**示例：**

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "src/server.js"]

# docker-compose.yml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URI=mongodb://mongo:27017/app
    depends_on:
      - mongo
  mongo:
    image: mongo:4.4
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:

# CI/CD (GitHub Actions)
name: CI/CD

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # 部署命令
```

---

## 六、最佳实践总结

1. **项目结构**：清晰的目录结构和命名规范
2. **代码组织**：模块化设计和关注点分离
3. **数据库**：合理的模型设计和查询优化
4. **API 设计**：RESTful 设计和输入验证
5. **中间件**：认证、日志、错误处理
6. **性能优化**：缓存、异步处理、数据库优化
7. **安全**：输入验证、认证授权、密码哈希
8. **测试**：单元测试、集成测试、E2E 测试
9. **部署**：容器化、CI/CD、环境管理
10. **监控**：日志管理、性能监控、错误跟踪

---

## 相关资源

- [Express.js 官方文档](https://expressjs.com/)
- [Nest.js 官方文档](https://docs.nestjs.com/)
- [Django 官方文档](https://docs.djangoproject.com/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy 官方文档](https://www.sqlalchemy.org/)
- [Django REST Framework 文档](https://www.django-rest-framework.org/)
- [Node.js 官方文档](https://nodejs.org/en/docs/)
- [Python 官方文档](https://docs.python.org/3/)

