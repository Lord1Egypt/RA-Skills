# Node.js 规范分析指引 | Node.js Analyzer

> 覆盖 Node.js 后端项目的语言特有规范。以项目实际配置为准。

## 分析流程

1. 读 `references/analyze-code-style.md` 中的通用部分
2. 用 `read` 读项目根目录的 `package.json`（type 字段判断 ESM/CJS）
3. 追加写入 `.code-spec/node-style.md`（Node.js 特有条目，不要写入 code-style.md）

## Node.js 特有分析维度

### 模块系统
- **ESM vs CJS**：`package.json` 的 `type: "module"` 还是 CommonJS
- `import/export` vs `require/module.exports` 使用比例
- 动态 import `await import()` 使用场景

### 命名
- **文件**：kebab-case（中间件/配置）vs camelCase（工具函数）vs PascalCase（类）
- **目录**：复数还是单数（routes/ vs route/）
- **中间件**：`xxx.middleware.ts` 命名约定

### 异步模式
- async/await 普及率
- Promise 链 vs callback 使用
- 错误处理：try-catch vs `.catch()` vs 中间件兜底

### 项目结构
- MVC 分层：routes/ → controllers/ → services/ → models/
- 是否有 middleware/ plugins/ guards/ 拦截器目录
- 配置管理：dotenv / config 目录 / 环境变量

### 框架特定
- **Express**：路由组织、中间件链、错误处理中间件
- **Fastify**：plugin 注册、schema 验证、装饰器模式
- **NestJS**：模块/控制器/提供者分层、DI 注入方式、装饰器使用
- **Koa**：ctx 使用模式、洋葱模型中间件

### 工具链
- 包管理器：npm / pnpm / yarn（看 lock 文件）
- Linter：ESLint 配置
- Formatter：Prettier 配置
- 测试：Jest / Vitest / Mocha，测试文件位置和命名
- TypeScript：tsconfig 的 module/moduleResolution/target 设置

### 日志
- console.log vs winston / pino / bunyan
- 日志级别使用约定
- 请求日志中间件

### 安全
- helmet / cors / rate-limit 使用
- 输入验证：joi / zod / class-validator
- 密码处理：bcrypt / argon2
