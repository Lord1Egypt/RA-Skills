# Next.js App Router 深度 Playbook

> 本文件是 `nextjs-app-router` 子技能的**深层参考**，按需读取。聚焦 App Router 独有的范式决策与高频踩坑，不重复通用 Web 组件 / 样式 / 性能内容。

## 0. 前置：确认版本

App Router 的行为随版本变化很大，落地前先核对：

```bash
npx next --version
```

- **Next 13.4+**：App Router 稳定可用
- **Next 15**：`params` / `searchParams` 变为 **Promise**（需 `await`）；`fetch` 默认**不再缓存**（Pages 时代默认缓存已反转）；`cookies()` / `headers()` 等变为异步
- 以下决策树默认按 **Next 15 语义**描述，旧版本请对照官方迁移指南

---

## 1. 决策树：渲染单元归属

```
这个 UI 单元需要：
├─ 只读数据 / 无交互 / 直接 async 拿数据？
│   └─ Server Component（默认，零客户端 JS，可直连 DB / 内部服务）
├─ 事件处理（onClick）/ 状态（useState）/ 浏览器 API（window）？
│   └─ 必须 Client Component（顶部 'use client'）
├─ 共享布局 / 持久 UI（侧边栏、导航）？
│   └─ layout.tsx（嵌套布局自动复用，不重新挂载）
└─ 单页内容？
    └─ page.tsx（默认 Server Component）
```

**关键纪律**：尽量把 `'use client'` 下推到**叶子**，让父级保持 Server Component。不要把整个 page 标成 client——那样会失去 RSC 的服务端渲染与数据直取优势。

---

## 2. 决策树：数据接口形态

```
需要对外暴露一个 HTTP 端点（给前端 fetch / 第三方调用）？
└─ Route Handler：app/api/.../route.ts 里 export async function GET/POST

需要在「表单提交 / 按钮点击」后改服务端数据，且调用方就是本应用？
└─ Server Action（'use server' 函数），比自己写 fetch 到 route handler 更省样板

需要跨请求复用、手动控制缓存的数据获取？
└─ 用 React cache() 包裹查询；或用 unstable_cache 包裹重计算
```

> Server Action 与主应用同源、自带序列化与渐进增强，适合「应用内写操作」；Route Handler 适合「对外契约端点」（移动端、第三方、webhook）。两者不是替代关系。

---

## 3. 决策树：缓存语义（Next 15 默认）

```
数据多久变一次？
├─ 构建时就确定（文档、营销页）→ 静态渲染（默认，除非用了动态 API）
├─ 每次请求都要新（用户个性化、实时）→ 用 dynamic 函数：cookies()/headers()/searchParams
└─ 中间态（几分钟级）→ 显式 revalidate：
    ├─ fetch(url, { next: { revalidate: 60 } })   # 基于时间
    ├─ revalidateTag('posts')                     # 基于标签，手动失效
    └─ export const revalidate = 60               # 整路由级
```

**陷阱**：Next 15 起 `fetch` 默认**不缓存**（与 14 相反）。想缓存必须显式写 `next: { revalidate }`，否则每次请求都打到源。`unstable_cache` 同理需显式调用。

---

## 4. 决策树：导航与路由结构

```
需要复用布局但 URL 不想多一层？
└─ 路由组 (group)：(marketing)/ 与 (app)/ 共享根 layout 但路径无 group 名

弹窗式路由（画廊点开大图，URL 变但保留背景列表）？
└─ 拦截路由 (intercepting)：@modal/(photos)/photo/[id]

同一 slot 并行渲染多块独立内容（dashboard 多面板）？
└─ 并行路由 (parallel)：@analytics @sidebar 多个 slot 同 layout

全局横切（鉴权跳转、地域、AB）？
└─ middleware.ts（跑在边缘，注意只能读请求头/cookie，不能访问 DB 直连）
```

---

## 5. 上线前检查清单

- [ ] `'use client'` 只在必要时出现，且尽量下推到叶子组件
- [ ] 所有 `params` / `searchParams` 均已 `await`（Next 15+）
- [ ] `cookies()` / `headers()` / `draftMode()` 已 `await`（Next 15+），且只出现在动态上下文
- [ ] 数据获取缓存语义明确：该缓存的标了 `revalidate` / `revalidateTag`，该动态的用了动态 API
- [ ] 客户端组件误引入了 `server-only` 模块？用 `import 'server-only'` 在编译期拦截
- [ ] Metadata：`export const metadata` / `generateMetadata` 已设置（SEO / 社交分享），且不放在 client 组件里
- [ ] `loading.tsx` / `error.tsx` / `not-found.tsx` 在关键路由已配置（流式与降级体验）
- [ ] Route Handler 区分了 `GET`（可缓存）/ `POST`（写操作），写操作优先考虑 Server Action
- [ ] Middleware 匹配范围用 `config.matcher` 收敛，避免对所有静态资源跑边缘逻辑

---

## 6. 高频踩坑速查

| 现象 | 根因 | 修法 |
|------|------|------|
| 客户端组件里 `useState` 报错 / 拿不到 props | 忘了 `'use client'`，或被当成 Server Component | 在文件顶部加 `'use client'` |
| 页面每次都请求最新数据，疑似没缓存 | Next 15 起 fetch 默认不缓存 | 显式 `next: { revalidate }` |
| `params.id` 是 Promise 而非字符串 | Next 15 异步化 | `const { id } = await params` |
| `'use client'` 组件 import 了 DB 驱动 / fs | 违反服务端边界 | 把数据获取上移到 Server Component 或 Route Handler |
| Metadata 不生效 | 写在 `'use client'` 组件里 | 移到 Server Component / `generateMetadata` |
| 布局里共享状态不持久（每次跳转重置） | 把状态放在 page 而非 layout；或误用 `<a>` 整页刷新 | 用 `next/link`；状态提升到 layout |
| Middleware 拖慢所有请求 | matcher 没收敛，静态资源也过一遍 | 用 `config.matcher` 精确匹配路由 |

---

## 7. 脚手架与常用命令

```bash
# 新建 App Router 项目（默认即是 App Router）
npx create-next-app@latest my-app --ts --app --eslint --src-dir

# 开发 / 构建 / 启动 / 类型检查
npm run dev          # 本地开发
npm run build        # 生产构建（含静态/动态分析）
npm run start        # 跑构建产物
npx tsc --noEmit     # 类型检查

# 目录约定（app/ 下）
app/layout.tsx          # 根布局（必需，包裹 <html>/<body>）
app/page.tsx            # 首页
app/(group)/page.tsx    # 路由组：URL 不含 (group)
app/loading.tsx         # 流式加载态（Suspense 边界）
app/error.tsx           # 路由级错误降级（必须是 Client Component）
app/not-found.tsx       # 404
app/api/hello/route.ts  # Route Handler
middleware.ts           # 边缘中间件（项目根或 src/ 根）
```

> 与 `ai-fullstack-engineer` 的契约优先工作流衔接：用 `scripts/scaffold_fullstack.py --fe react` 产出前端骨架后，若选定 Next.js，可按本 playbook 把 `app/` 结构补齐；API 契约仍由 `api-design` 子技能与 OpenAPI 类型生成保障前后端类型安全。

---

## 相关参考

- 前端通用范式与组件/样式/性能落地：[references/frontend-playbook.md](frontend-playbook.md)
- 契约优先工作流（前后端类型安全）：[references/fullstack-workflow.md](fullstack-workflow.md)
- 接口契约设计：[skills/api-design](../skills/api-design/SKILL.md)
- 本 playbook 归属子技能：[skills/nextjs-app-router](../skills/nextjs-app-router/SKILL.md)
