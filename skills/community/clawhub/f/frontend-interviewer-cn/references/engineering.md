# 工程化面试题库

## 初级

### 题目1：Webpack 和 Vite 的主要区别是什么？
**考察点：** 构建原理、开发体验、打包机制

**参考答案：**
| 对比项 | Webpack | Vite |
|--------|---------|------|
| 开发模式 | 打包所有模块后启动 | 基于原生 ESM，按需编译 |
| 冷启动 | 慢（需打包） | 极快（无需打包） |
| HMR | 较慢（重新打包模块） | 极快（精确更新单模块） |
| 生产打包 | 自身打包 | 使用 Rollup |
| 生态 | 成熟，插件丰富 | 快速发展中 |

**Vite 快的原因：**
1. 开发时利用浏览器原生 ESM，无需打包，直接让浏览器请求模块
2. 使用 esbuild（Go编写）预编译依赖，比 JS 快 10-100 倍
3. HMR 精准到模块级别，更新极快

```javascript
// Vite 开发模式：浏览器直接请求 ESM
// <script type="module" src="/src/main.js">
// 浏览器遇到 import 自动请求对应文件

// Webpack 开发模式：将所有模块打包成 bundle
// <script src="/dist/bundle.js">
```

---

### 题目2：什么是 Tree Shaking？如何确保它生效？
**考察点：** 静态分析、ESM、副作用标记

**参考答案：**
Tree Shaking 是通过静态分析，移除未使用代码（dead code）的优化手段。

**生效条件：**
1. 必须使用 **ESM（ES Modules）**，不能用 CommonJS（`require`）
2. 代码必须无副作用，或在 `package.json` 中声明 `sideEffects`

```javascript
// ✅ 支持 Tree Shaking（ESM）
export function add(a, b) { return a + b; }
export function unused() { return 'never used'; }

// 只导入 add，unused 会被 shake 掉
import { add } from './math';

// ❌ 不支持 Tree Shaking（CommonJS）
module.exports = { add, unused };
const { add } = require('./math'); // 整个模块被引入
```

```json
// package.json：声明哪些文件有副作用
{
  "sideEffects": ["*.css", "./src/polyfills.js"],
  // 或声明无副作用
  "sideEffects": false
}
```

---

### 题目3：什么是热模块替换（HMR）？如何实现的？
**考察点：** HMR 原理、WebSocket、模块热更新

**参考答案：**
HMR（Hot Module Replacement）在不刷新页面的情况下，实时替换、添加或删除模块。

**原理：**
1. Dev Server 监听文件变化
2. 文件变化后，通过 **WebSocket** 通知浏览器
3. 浏览器下载变更的模块
4. 运行时替换旧模块，保留应用状态

```javascript
// Vite/Webpack 中手动处理 HMR（Vue/React 插件已自动处理）
if (import.meta.hot) {
  import.meta.hot.accept('./module.js', (newModule) => {
    // 接收新模块，执行更新逻辑
    newModule.render();
  });

  import.meta.hot.dispose(() => {
    // 模块被替换前的清理工作
    clearInterval(timer);
  });
}
```

React Fast Refresh 和 Vue HMR 都是基于此机制，框架层面保证组件状态不丢失。

---

## 中级

### 题目4：Monorepo 是什么？主流方案（pnpm workspace / Turborepo）如何选择？
**考察点：** Monorepo 优缺点、工具选型、依赖管理

**参考答案：**
**Monorepo**：将多个项目/包放在同一个 Git 仓库中管理。

优点：代码复用、统一工具链、原子提交、易于重构
缺点：仓库体积大、需要专门工具、CI 需按需构建

```
# pnpm workspace 结构
my-monorepo/
├── packages/
│   ├── ui/            # 组件库
│   ├── utils/         # 工具函数
│   └── app/           # 主应用
├── pnpm-workspace.yaml
└── package.json
```

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

```json
// packages/app/package.json：引用内部包
{
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "@myorg/utils": "workspace:*"
  }
}
```

**工具选型：**
- **pnpm workspace**：基础 Monorepo，依赖管理
- **Turborepo**：在 workspace 基础上加任务编排、增量构建缓存
- **Nx**：功能最全，适合大型企业项目

---

### 题目5：Webpack 的核心概念：Loader 和 Plugin 的区别？
**考察点：** 转换 vs 扩展、工作时机、使用场景

**参考答案：**
| 对比 | Loader | Plugin |
|------|--------|--------|
| 作用 | 转换文件（转换器） | 扩展构建能力（扩展器） |
| 时机 | 模块加载阶段 | 整个构建生命周期 |
| 形式 | 函数，返回转换结果 | 类，监听 webpack 事件 |

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      // Loader：处理 .scss 文件
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'] // 从右到左执行
      },
      {
        test: /\.tsx?$/,
        use: 'ts-loader'
      }
    ]
  },
  plugins: [
    // Plugin：生成 HTML 文件
    new HtmlWebpackPlugin({ template: './index.html' }),
    // Plugin：抽取 CSS 到单独文件
    new MiniCssExtractPlugin({ filename: '[name].[hash].css' }),
    // Plugin：打包前清理 dist
    new CleanWebpackPlugin()
  ]
};
```

---

### 题目6：如何优化 Webpack 的构建速度和产物体积？
**考察点：** 缓存、并行、代码分割、分析工具

**参考答案：**
**构建速度优化：**
```javascript
module.exports = {
  // 1. 开启持久化缓存（Webpack 5）
  cache: { type: 'filesystem' },

  // 2. 缩小解析范围
  resolve: {
    modules: [path.resolve(__dirname, 'src'), 'node_modules'],
    extensions: ['.js', '.ts'] // 减少后缀尝试
  },

  module: {
    rules: [{
      test: /\.js$/,
      exclude: /node_modules/, // 排除 node_modules
      use: ['thread-loader', 'babel-loader'] // thread-loader 开启多线程
    }]
  }
};
```

**产物体积优化：**
```javascript
// 代码分割（Code Splitting）
optimization: {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      vendors: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all'
      }
    }
  }
}

// 动态导入（懒加载）
const HomePage = lazy(() => import('./pages/Home'));
```

---

## 高级

### 题目7：设计一套前端 CI/CD 流程，需要考虑哪些环节？
**考察点：** 流水线设计、质量门禁、部署策略

**参考答案：**
```yaml
# .github/workflows/ci.yml 示例
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    steps:
      - uses: actions/checkout@v3
      - name: Install deps
        run: pnpm install --frozen-lockfile
      - name: Lint
        run: pnpm lint
      - name: Type check
        run: pnpm tsc --noEmit
      - name: Unit tests
        run: pnpm test --coverage
      - name: Build
        run: pnpm build

  deploy-staging:
    needs: quality
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Deploy to Staging
        run: pnpm deploy:staging

  deploy-prod:
    needs: quality
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Production
        run: pnpm deploy:prod
```

**部署策略选择：**
- **蓝绿部署**：两套环境切换，零停机，回滚快
- **金丝雀发布**：逐步放量（1% → 10% → 100%），降低风险
- **滚动更新**：逐步替换实例，Kubernetes 默认策略

---

### 题目8：Vite 插件开发：如何实现一个自定义 Vite 插件？
**考察点：** Vite 插件 API、钩子函数、Rollup 兼容

**参考答案：**
Vite 插件基于 Rollup 插件接口扩展，额外提供 Vite 专有钩子。

```javascript
// vite-plugin-auto-import-css.js
export default function autoImportCssPlugin() {
  return {
    name: 'auto-import-css',       // 插件名称（必须）

    // 构建开始时
    buildStart() {
      console.log('Build started');
    },

    // 转换模块内容
    transform(code, id) {
      if (!id.endsWith('.vue')) return null;
      // 自动注入 CSS import
      const cssPath = id.replace('.vue', '.css');
      return {
        code: `import '${cssPath}';\n${code}`,
        map: null
      };
    },

    // 解析模块 ID
    resolveId(source) {
      if (source === 'virtual:my-module') {
        return '\0virtual:my-module'; // \0 前缀标记虚拟模块
      }
    },

    // 加载虚拟模块
    load(id) {
      if (id === '\0virtual:my-module') {
        return 'export const msg = "from virtual module"';
      }
    },

    // Vite 专有：开发服务器配置
    configureServer(server) {
      server.middlewares.use('/api/ping', (req, res) => {
        res.end('pong');
      });
    }
  };
}
```

---

### 题目9：Module Federation（模块联邦）原理及应用场景
**考察点：** 微前端、运行时共享、远程模块加载

**参考答案：**
Module Federation（Webpack 5）允许多个独立构建的应用在**运行时**共享代码，是微前端的重要实现方式。

```javascript
// 被消费方（remote）：暴露模块
// webpack.config.js (app-remote)
new ModuleFederationPlugin({
  name: 'remoteApp',
  filename: 'remoteEntry.js',
  exposes: {
    './Button': './src/components/Button',
    './utils': './src/utils/index'
  },
  shared: ['react', 'react-dom'] // 共享依赖，避免重复加载
});

// 消费方（host）：使用远程模块
// webpack.config.js (app-host)
new ModuleFederationPlugin({
  name: 'hostApp',
  remotes: {
    remoteApp: 'remoteApp@http://remote.example.com/remoteEntry.js'
  },
  shared: ['react', 'react-dom']
});

// 在代码中使用远程组件
const Button = React.lazy(() => import('remoteApp/Button'));
```

**适用场景：**
- 大型应用拆分为多个独立部署的子应用
- 多团队协作，各自维护独立仓库
- 跨项目复用组件，无需发布 npm 包
