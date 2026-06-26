---
name: frontend-architecture
description: Designs scalable frontend architecture for large applications: project structure, module boundaries, dependency management, code splitting strategy, and technical debt prevention. Use when 前端架构, 项目结构, 模块划分, 技术选型, 架构设计, or scaling frontend apps.
model: opus
---

# 前端架构设计（Frontend Architecture）

为大型前端应用设计可扩展的架构——不是"用什么框架"，而是如何组织代码、划分模块、管理依赖，让项目在 2 年后还能维护。

## 触发场景

- 「新项目技术选型」「从零搭建前端架构」
- 「项目越来越乱」「不知道代码该放哪」「模块耦合严重」
- 「多团队协作」「微前端」「代码复用」
- 「技术债务」「重构策略」「如何避免架构腐化」

---

## 执行流程

### 1. 先搞清楚项目规模和约束

不要一上来就给"最佳实践"，先问清楚：

| 问题 | 为什么重要 | 影响的决策 |
|------|-----------|----------|
| 团队规模？ | 3 人和 30 人的架构完全不同 | 是否需要严格的模块边界、代码审查流程 |
| 预期生命周期？ | 3 个月 MVP 和 3 年产品的架构不同 | 是否需要考虑扩展性、技术债管理 |
| 性能要求？ | ToB 后台和 ToC 电商的性能要求不同 | SSR/SSG、代码分割策略、CDN 策略 |
| 是否多团队？ | 影响模块划分和发布策略 | Monorepo、微前端、API 契约 |
| 现有技术栈？ | 存量项目迁移成本高 | 渐进式重构 vs 推倒重来 |

### 2. 项目结构设计

**小型项目（< 3 人，< 6 个月）：**

```
src/
├── components/       # 所有组件
├── pages/           # 路由页面
├── hooks/           # 自定义 hooks
├── utils/           # 工具函数
├── api/             # API 请求
└── types/           # 类型定义
```

**中型项目（3-10 人，6 个月 - 2 年）：**

```
src/
├── features/              # 按功能域划分
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   ├── types.ts
│   │   └── index.ts      # 导出公共接口
│   ├── dashboard/
│   └── settings/
├── shared/                # 跨 feature 共享
│   ├── components/       # 通用组件（Button、Modal）
│   ├── hooks/
│   ├── utils/
│   └── types/
├── app/                   # 应用层（路由、布局、全局状态）
│   ├── routes/
│   ├── layouts/
│   └── providers/
└── lib/                   # 第三方库封装
    ├── axios.ts
    ├── react-query.ts
    └── analytics.ts
```

**大型项目（10+ 人，2 年+）：**

```
packages/                  # Monorepo
├── apps/
│   ├── web/              # 主应用
│   ├── admin/            # 管理后台
│   └── mobile/           # 移动端（可选）
├── features/             # 业务功能包
│   ├── auth/
│   ├── payment/
│   └── analytics/
├── ui/                   # 设计系统
│   ├── components/
│   ├── tokens/
│   └── themes/
├── shared/               # 共享工具
│   ├── utils/
│   ├── types/
│   ├── hooks/
│   └── api-client/
└── config/               # 共享配置
    ├── eslint/
    ├── tsconfig/
    └── tailwind/
```

### 3. 模块边界与依赖规则

**分层架构（推荐）：**

```
app/          # 应用层：路由、布局、全局状态
  ↓ 可以依赖
features/     # 功能层：业务逻辑
  ↓ 可以依赖
shared/       # 共享层：通用组件、工具
  ↓ 可以依赖
lib/          # 基础设施层：第三方库封装
```

**依赖规则（用 ESLint 强制）：**

```js
// .eslintrc.js
{
  rules: {
    'no-restricted-imports': ['error', {
      patterns: [
        {
          group: ['@/features/*'],
          message: 'shared/ 不能依赖 features/'
        },
        {
          group: ['@/features/auth/*'],
          importNames: ['*'],
          message: 'features 之间不能直接依赖，通过 shared/ 或事件通信'
        }
      ]
    }]
  }
}
```

**feature 之间的通信：**

```ts
// ❌ 错：feature A 直接导入 feature B
import { useUserStore } from '@/features/auth/store'

// ✅ 对：通过 shared 层暴露接口
// shared/stores/user.ts
export { useUserStore } from '@/features/auth/store'

// 或用事件总线解耦
// shared/events.ts
export const eventBus = mitt()
// feature A
eventBus.emit('user:logout')
// feature B
eventBus.on('user:logout', handleLogout)
```

### 4. 代码分割策略

**分割粒度的决策：**

| 场景 | 策略 | 原因 |
|------|------|------|
| 路由页面 | 每个页面一个 chunk | 用户不会一次访问所有页面 |
| 大型依赖（echarts、pdf.js） | 单独 chunk | 不是所有页面都需要 |
| 低频功能（导出、打印） | 懒加载 | 大多数用户不会用 |
| 通用组件（Button、Modal） | 打进主 chunk | 几乎每个页面都用，拆了反而多请求 |

**Next.js App Router 的分割：**

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import dynamic from 'next/dynamic'

// 路由级自动分割，不需要手动 dynamic
export default function DashboardPage() {
  return <DashboardContent />
}

// 大型图表库按需加载
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,  // 不在服务端渲染
})

// 低频功能懒加载
const ExportModal = dynamic(() => import('./ExportModal'))
```

**Vite 的手动分包：**

```ts
// vite.config.ts
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-ui': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          'vendor-charts': ['echarts', 'recharts'],
        }
      }
    }
  }
}
```

### 5. 技术选型决策框架

**不要凭感觉选，用决策矩阵：**

| 维度 | 权重 | 方案 A | 方案 B | 方案 C |
|------|------|--------|--------|--------|
| 学习曲线 | 20% | 8 | 6 | 4 |
| 生态成熟度 | 25% | 9 | 7 | 5 |
| 性能 | 20% | 7 | 9 | 8 |
| 团队熟悉度 | 15% | 9 | 5 | 3 |
| 社区活跃度 | 10% | 8 | 7 | 6 |
| 迁移成本 | 10% | 6 | 8 | 9 |
| **加权总分** | | **7.85** | **7.15** | **5.85** |

**关键技术选型的决策点：**

**框架选择（React vs Vue vs Svelte）：**
- 团队已有技能 > 框架本身优劣
- ToB 后台、数据密集 → React（生态最完善）
- 快速原型、小团队 → Vue（上手快）
- 性能极致要求 → Svelte（编译时优化）

**状态管理（Zustand vs Redux vs Jotai）：**
- 简单全局状态 → Zustand
- 复杂业务逻辑、需要中间件 → Redux Toolkit
- 原子化状态、细粒度更新 → Jotai

**样式方案（Tailwind vs CSS Modules vs CSS-in-JS）：**
- 快速开发、设计系统 → Tailwind
- 组件库、样式隔离 → CSS Modules
- 动态主题、运行时样式 → CSS-in-JS（Stitches/Panda）

### 6. 技术债管理

**技术债的分类：**

| 类型 | 特征 | 处理策略 |
|------|------|---------|
| 架构债 | 模块耦合、分层混乱 | 渐进式重构，设边界 |
| 代码债 | 重复代码、命名混乱 | 日常重构，code review |
| 测试债 | 覆盖率低、测试脆弱 | 新功能必须有测试，存量逐步补 |
| 依赖债 | 过时依赖、安全漏洞 | 定期升级，用 Dependabot |
| 文档债 | 文档过时、缺失 | 重要决策必须记录 ADR |

**ADR（Architecture Decision Record）模板：**

```markdown
# ADR-001: 选择 Zustand 作为状态管理方案

## 状态
已决定

## 背景
项目需要全局状态管理，主要用于主题、用户信息、通知等 UI 状态。

## 决策
选择 Zustand，不用 Redux。

## 理由
- 代码量少（Redux 需要 action/reducer/selector，Zustand 直接 set）
- 性能好（细粒度订阅，不需要 reselect）
- 学习曲线低（团队新人多）
- 不需要 Redux 的中间件生态（没有复杂异步逻辑）

## 后果
- 正面：开发效率高，代码简洁
- 负面：如果未来需要时间旅行调试，需要额外配置
- 缓解：用 Redux DevTools 扩展监控 Zustand
```

### 7. 渐进式重构策略

**什么时候重构，什么时候重写：**

| 场景 | 策略 | 原因 |
|------|------|------|
| 代码质量差但架构清晰 | 渐进式重构 | 风险低，可持续交付 |
| 架构腐化严重 | 绞杀者模式（Strangler Fig） | 新功能用新架构，旧功能逐步迁移 |
| 技术栈过时且无法升级 | 重写 | 继续维护成本 > 重写成本 |

**绞杀者模式示例（微前端）：**

```
旧应用（legacy.example.com）
  ├── /dashboard  → 保留
  ├── /settings   → 迁移到新应用
  └── /reports    → 迁移到新应用

新应用（app.example.com）
  ├── /settings   → 新架构实现
  └── /reports    → 新架构实现

Nginx 路由：
  /settings → app.example.com
  /reports  → app.example.com
  /*        → legacy.example.com
```

---

## 架构反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 过度设计 | 3 人团队用微前端 | 按当前规模设计，预留扩展点 |
| 没有边界 | 所有代码在 src/ 平铺 | 按功能域或分层组织 |
| 循环依赖 | A 导入 B，B 导入 A | 用 ESLint 检测，提取公共依赖到 shared |
| 全局状态滥用 | 所有状态都放 store | 状态尽量下沉，能放组件就不放 store |
| 技术债不可见 | 没有记录，靠口口相传 | 用 ADR 记录重要决策，用 TODO 标记技术债 |

## 输出模板

```markdown
## 前端架构方案

### 项目背景
- 团队规模：X 人
- 预期生命周期：X 年
- 性能要求：[ToB 后台 / ToC 高性能]
- 现有技术栈：[新项目 / 存量迁移]

### 技术选型
| 维度 | 方案 | 理由 |
|------|------|------|
| 框架 | React / Vue / Svelte | … |
| 状态管理 | Zustand / Redux / Jotai | … |
| 样式 | Tailwind / CSS Modules | … |
| 构建 | Vite / Next.js | … |

### 项目结构
[目录树 + 分层说明]

### 模块边界
- 依赖规则：[分层图]
- ESLint 规则：[no-restricted-imports 配置]

### 代码分割策略
- 路由级：每个页面一个 chunk
- 大型依赖：[列出需要单独分割的库]
- 懒加载：[列出低频功能]

### 技术债管理
- ADR 存放位置：docs/adr/
- 重构策略：[渐进式 / 绞杀者模式]
```
