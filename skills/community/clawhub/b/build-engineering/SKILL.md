---
name: build-engineering
description: Optimizes build toolchain and engineering setup: Vite/Webpack config, Monorepo with pnpm/Turborepo, Module Federation, CI/CD pipeline, code generation, and DX improvements. Use when 构建优化, Monorepo, 模块联邦, CI/CD, 工程化, Vite, Webpack, Turborepo, or build config.
model: opus
---

# 构建与工程化（Build Engineering）

解决构建慢、包体积大、多包协作混乱、CI 不稳定等工程问题，让团队把时间花在业务上而不是工具上。

## 触发场景

- 「构建太慢了」「热更新卡」「CI 跑 20 分钟」
- 「多个项目共享组件，怎么管理」「Monorepo 怎么搭」
- 「微前端怎么做」「模块联邦怎么配」
- 「bundle 分析完了，不知道怎么优化」
- 「代码生成」「自动化脚本」「工程规范落地」

---

## 执行流程

### 1. 先定位问题类型

| 用户描述 | 实际问题 | 第一步 |
|---------|---------|-------|
| 「构建慢」「dev 启动慢」 | 构建性能 | 问：用 Vite 还是 Webpack？冷启动多久？热更新多久？ |
| 「多个项目共享代码」 | 代码共享架构 | 问：几个项目？是否需要独立发版？团队规模？ |
| 「微前端」「模块联邦」 | 运行时集成 | 问：是独立部署还是同仓库？需要共享状态吗？ |
| 「CI 太慢」「流水线不稳定」 | CI/CD 优化 | 问：用什么 CI？哪个步骤最慢？有没有缓存？ |
| 「bundle 大」 | 产物优化 | 直接让用户跑分析工具，看报告再说 |

### 2. 构建性能优化

**Vite 项目慢的常见原因和解法：**

| 问题 | 诊断方式 | 解法 |
|------|---------|------|
| 冷启动慢 | 看 `vite --debug` 输出 | 检查是否有大量 CommonJS 依赖需要预构建；用 `optimizeDeps.include` 预声明 |
| 热更新慢 | 改一个文件，看 HMR 耗时 | 检查是否有循环依赖；大型组件库按需引入 |
| 生产构建慢 | `vite build --profile` | 开启 `build.rollupOptions.output.manualChunks` 手动分包；关闭不需要的插件 |

**Webpack 项目提速的优先级顺序：**

1. 升级到 Webpack 5（持久化缓存 `cache: { type: 'filesystem' }`）
2. 缩小 loader 处理范围（`include: path.resolve('src')`，排除 node_modules）
3. 开启多线程（`thread-loader` 用于 babel/ts 编译）
4. 用 `esbuild-loader` 替换 `babel-loader`（速度提升 10-20x）
5. 考虑迁移到 Vite（新项目首选，存量项目评估迁移成本）

**不要做的事：**
- 不要为了"优化"随意升级 Webpack 大版本，破坏性变更多
- 不要在没有 profile 数据的情况下盲目加插件

### 3. Monorepo 架构决策

**什么时候需要 Monorepo：**
- 3 个以上项目共享组件/工具/类型
- 需要原子提交（一个 PR 同时改多个包）
- 团队需要统一的 lint/test/build 规范

**什么时候不需要：**
- 项目完全独立，没有共享代码
- 团队 < 3 人，管理成本大于收益

**推荐方案（2025 年）：**

```
pnpm workspace + Turborepo
├── apps/
│   ├── web/          # 主应用
│   └── admin/        # 管理后台
├── packages/
│   ├── ui/           # 共享组件库
│   ├── utils/        # 工具函数
│   ├── types/        # 共享类型
│   └── config/       # 共享配置（eslint���tsconfig、tailwind）
├── pnpm-workspace.yaml
└── turbo.json
```

**Turborepo 关键配置：**

```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],  // 先构建依赖包
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "dev": {
      "cache": false,           // dev 不缓存
      "persistent": true
    }
  }
}
```

**包之间的依赖声明：**

```json
// apps/web/package.json
{
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "@myorg/utils": "workspace:*"
  }
}
```

### 4. 模块联邦（Module Federation）

**适用场景：** 多个独立部署的应用需要在运行时共享组件或逻辑（微前端）。

**不适用场景：** 同一仓库的多个包——用 Monorepo 就够了，不需要模块联邦。

**Vite 模块联邦配置（`@originjs/vite-plugin-federation`）：**

```ts
// 提供方（组件库应用）vite.config.ts
import federation from '@originjs/vite-plugin-federation'

export default {
  plugins: [
    federation({
      name: 'remote-app',
      filename: 'remoteEntry.js',
      exposes: {
        './Button': './src/components/Button.vue',
        './utils': './src/utils/index.ts',
      },
      shared: ['vue', 'pinia'],  // 共享依赖，避免重复加载
    })
  ],
  build: { target: 'esnext' }  // 模块联邦需要 esnext
}

// 消费方 vite.config.ts
export default {
  plugins: [
    federation({
      name: 'host-app',
      remotes: {
        'remote-app': 'http://localhost:5001/assets/remoteEntry.js',
      },
      shared: ['vue', 'pinia'],
    })
  ]
}
```

**模块联邦的坑：**
- 共享依赖版本必须兼容，否则会加载两份
- 类型不会自动共享，需要单独处理（发布 `.d.ts` 或用 `@module-federation/typescript`）
- 本地开发需要先构建提供方，或用 `vite preview` 模拟

### 5. CI/CD 优化

**CI 慢的排查顺序：**

1. **缓存命中率**：`node_modules`、构建产物、测试结果是否有缓存？
2. **并行化**：lint、test、build 能否并行跑？
3. **增量执行**：只跑受影响的包（Turborepo `--filter` 或 `affected`）
4. **测试分片**：大型测试套件拆分到多个 runner 并行

**GitHub Actions 最佳实践：**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v3
        with: { version: 9 }

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'          # 缓存 pnpm store

      - run: pnpm install --frozen-lockfile

      - name: Cache Turborepo
        uses: actions/cache@v4
        with:
          path: .turbo
          key: turbo-${{ github.sha }}
          restore-keys: turbo-   # 前缀匹配，复用历史缓存

      - run: pnpm turbo build test --filter='[HEAD^1]'  # 只跑有变更的包
```

### 6. 代码生成与自动化

**值得自动化的场景：**
- 从 OpenAPI/Swagger 生成 API 类型和请求函数（`openapi-typescript` + `orval`）
- 从设计 token 生成 CSS 变量和 Tailwind 配置（`style-dictionary`）
- 新功能脚手架（`plop` 或自定义 CLI）

**OpenAPI 代码生成示例：**

```bash
# 安装
pnpm add -D openapi-typescript orval

# 生成类型
npx openapi-typescript ./api/openapi.yaml -o ./src/types/api.d.ts

# orval 生成 React Query hooks
# orval.config.ts
export default {
  api: {
    input: './api/openapi.yaml',
    output: {
      mode: 'tags-split',
      target: './src/api',
      schemas: './src/types',
      client: 'react-query',
      override: {
        mutator: { path: './src/lib/axios.ts', name: 'customInstance' }
      }
    }
  }
}
```

**新功能脚手架（plop）：**

```js
// plopfile.js
export default function (plop) {
  plop.setGenerator('component', {
    description: '创建新组件',
    prompts: [
      { type: 'input', name: 'name', message: '组件名称（PascalCase）' },
      { type: 'list', name: 'type', choices: ['ui', 'feature', 'page'] }
    ],
    actions: [
      { type: 'add', path: 'src/components/{{name}}/index.tsx', templateFile: 'plop-templates/component.hbs' },
      { type: 'add', path: 'src/components/{{name}}/{{name}}.test.tsx', templateFile: 'plop-templates/component.test.hbs' },
    ]
  })
}
```

---

## 输出模板

```markdown
## 工程化方案

### 问题诊断
- 当前瓶颈：…（构建耗时 / CI 耗时 / 包管理问题）

### 方案
- 构建工具：Vite / Webpack 5 + 具体配置
- 包管理：pnpm workspace + Turborepo
- CI 优化：缓存策略 + 并行化 + 增量构建

### 关键配置
- turbo.json pipeline 设计
- CI 缓存 key 策略
- 代码生成工具链

### 预期收益
- 构建时间：X min → Y min
- CI 时间：X min → Y min
```
