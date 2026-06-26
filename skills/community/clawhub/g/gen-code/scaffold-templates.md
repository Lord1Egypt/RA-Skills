# 项目脚手架模板

本文件由 `/gen-code` 技能按需加载，提供各技术栈的脚手架初始化模板。

**触发条件**：`{backendRoot}` 无任何项目配置文件，或 `{frontendRoot}` 无 `package.json`
**跳过条件**：`{root}/.scaffold-initialized` 文件存在
**防重复**：生成完成后写入 `.scaffold-initialized`

---

## 后端脚手架

### Spring Boot 3 + Maven

**pom.xml**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>{spring-boot.version}</version>
        <relativePath/>
    </parent>
    <groupId>{group-id}</groupId>
    <artifactId>{artifact-id}</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <name>{project-name}</name>
    <properties>
        <java.version>{java.version}</java.version>
        <mybatis-plus.version>{mybatis-plus.version}</mybatis-plus.version>
    </properties>
    <dependencies>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-redis</artifactId></dependency>
        <dependency><groupId>com.baomidou</groupId><artifactId>mybatis-plus-spring-boot3-starter</artifactId><version>${mybatis-plus.version}</version></dependency>
        <dependency><groupId>com.mysql</groupId><artifactId>mysql-connector-j</artifactId><scope>runtime</scope></dependency>
        <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
    </dependencies>
    <build>
        <plugins><plugin><groupId>org.springframework.boot</groupId><artifactId>spring-boot-maven-plugin</artifactId></plugin></plugins>
    </build>
</project>
```

**application.yml**：
```yaml
server:
  port: {server.port}
spring:
  profiles:
    active: dev
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${DB_HOST:localhost}:${DB_PORT:3306}/${DB_NAME}?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:}
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
mybatis-plus:
  mapper-locations: classpath:mapper/*.xml
  configuration:
    map-underscore-to-camel-case: true
  global-config:
    db-config:
      logic-delete-field: isDeleted
      logic-delete-value: 1
      logic-not-delete-value: 0
```

**application-dev.yml**：
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/{db_name}?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
    username: root
    password: {dev-db-password}
  data:
    redis:
      host: localhost
      port: 6379
logging:
  level:
    com.{group-id}: debug
```

**通用代码文件**（版本号和包名从设计文档/规范读取）：
- `Application.java`：`@SpringBootApplication` 启动类
- `config/CorsConfig.java`：`@Configuration` + `CorsFilter`
- `common/Result.java`：`code` + `message` + `data` + `timestamp` 统一响应
- `common/PageResult.java`：`list` + `total` + `page` + `size` 分页响应
- `exception/GlobalExceptionHandler.java`：`@RestControllerAdvice` 全局异常处理
- `.gitignore`：标准 Java/Maven gitignore

### Spring Boot 3 + Gradle

与 Maven 版本产物相同，将 `pom.xml` 替换为 `build.gradle` + `settings.gradle`。

### Python + FastAPI

| 文件 | 内容 |
|------|------|
| `requirements.txt` | fastapi、uvicorn、sqlalchemy、pydantic、python-dotenv |
| `main.py` | FastAPI 实例、router 注册、CORS 中间件、lifespan |
| `config.py` | 从 `.env` 读取数据库 URL、Redis URL、服务端口 |
| `models/` | SQLAlchemy 模型（按业务模块划分） |
| `api/` | API 路由（按业务模块划分） |
| `middleware/` | 认证、日志中间件 |
| `.gitignore` | `__pycache__/`、`.env`、`*.pyc` |
| `.env.example` | 环境变量模板 |

### Python + Django

| 文件 | 内容 |
|------|------|
| `requirements.txt` | django、djangorestframework、psycopg2-binary、python-dotenv |
| `manage.py` | Django 管理脚本 |
| `{project}/settings.py` | 数据库、中间件、REST Framework 配置 |
| `{project}/urls.py` | 根 URL 配置 |
| `apps/` | Django 应用（按业务模块拆分） |
| `.gitignore` | 标准 Python + Django gitignore |

### Python + Flask

| 文件 | 内容 |
|------|------|
| `requirements.txt` | flask、flask-cors、sqlalchemy、python-dotenv |
| `app.py` | Flask 实例、blueprint 注册、CORS 配置 |
| `config.py` | 从 `.env` 读取配置 |
| `blueprints/` | 按业务模块划分的蓝图 |
| `models/` | SQLAlchemy 模型 |
| `.gitignore` | 标准 Python gitignore |

### Node.js + Express

| 文件 | 内容 |
|------|------|
| `package.json` | express、cors、dotenv、helmet、morgan 及 TypeScript 类型 |
| `tsconfig.json` | `target: ES2022`、`module: commonjs` |
| `src/app.ts` | Express 实例、中间件注册、路由挂载 |
| `src/routes/` | 按业务模块划分的路由 |
| `src/middleware/` | 认证、错误处理、日志中间件 |
| `src/config/` | 配置管理 |
| `.gitignore` | `node_modules/`、`.env`、`dist/` |

### Go + Gin

| 文件 | 内容 |
|------|------|
| `go.mod` | `module {module-path}`、gin、gorm、go-redis 依赖 |
| `main.go` | Gin 引擎创建、路由注册、中间件、服务启动 |
| `config/` | 配置加载（YAML/ENV） |
| `handler/` | HTTP handler（按业务模块划分） |
| `model/` | GORM 模型定义 |
| `middleware/` | 认证、CORS、日志中间件 |
| `.gitignore` | `/vendor`、`*.exe` |

---

## 前端脚手架

### Vue 3 + Vite + TypeScript

**package.json**：
```json
{
  "name": "{project-name}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^{vue.version}",
    "vue-router": "^{vue-router.version}",
    "pinia": "^{pinia.version}",
    "axios": "^{axios.version}",
    "ant-design-vue": "^{antd.version}",
    "@ant-design/icons-vue": "^{antd-icons.version}"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^{vite-plugin-vue.version}",
    "typescript": "~{typescript.version}",
    "vite": "^{vite.version}",
    "vue-tsc": "^{vue-tsc.version}",
    "less": "^4.0.0"
  }
}
```

**vite.config.ts**：
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': resolve(__dirname, 'src') },
  },
  server: {
    port: {frontend.port},
    proxy: {
      '/api': {
        target: 'http://localhost:{backend.port}',
        changeOrigin: true,
      },
    },
  },
})
```

**其他文件**：
- `tsconfig.json`：`paths: { "@/*": ["./src/*"] }`
- `index.html`：`<script type="module" src="/src/main.ts"></script>`
- `src/main.ts`：`createApp(App).use(router).use(pinia).mount('#app')`
- `src/App.vue`：`<router-view />` 根组件
- `src/router/index.ts`：路由配置占位
- `src/stores/index.ts`：Pinia 创建
- `src/api/request.ts`：Axios 封装（baseURL、拦截器、统一错误处理、Token 注入）
- `src/types/index.ts`：通用类型定义
- `.env.development` / `.env.production`：环境变量
- `.gitignore`：标准 Node/Vue gitignore

### React + Vite + TypeScript

与 Vue 3 版本类似，差异：
- `react`、`react-dom`、`react-router-dom` 替换 Vue 相关依赖
- `src/main.tsx`：`createRoot().render(<App />)` 替换 `createApp`
- `src/App.tsx`：`<BrowserRouter><Routes /></BrowserRouter>` 替换 `<router-view />`

### Vue 3 + Vite + JavaScript

与 TypeScript 版本相同，移除 `tsconfig.json`、`vue-tsc`、`typescript` 依赖。
