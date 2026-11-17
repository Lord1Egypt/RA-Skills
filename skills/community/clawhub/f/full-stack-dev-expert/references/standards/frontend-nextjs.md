# Next.js 编码规范（前端工程师实现必读）

适用：Next.js 14+/15 App Router / React 18+ / TypeScript strict。
定位：SSR/SSG/ISR 场景（SEO、首屏性能、内容站、全栈一体 React）；
纯 SPA 用 frontend-react.md 的 Vite 方案，不为了用 Next 而用 Next。

## 1. 工程结构

```
src/
├── app/                      # 路由即目录（App Router）
│   ├── (marketing)/          # 路由组：公开页（SSG/ISR）
│   ├── (app)/                # 登录态区（SSR + 鉴权中间件）
│   ├── api/                  # Route Handlers（仅薄代理/BFF，不写重业务）
│   ├── layout.tsx / page.tsx / loading.tsx / error.tsx / not-found.tsx
│   └── globals.css
├── components/               # 同 frontend-react.md 组织（ui/ + business/）
├── features/<域>/
├── lib/                      # 客户端、工具、配置
└── types/
```

## 2. Server / Client 组件纪律

- **默认 Server Component**；`'use client'` 最小化——只在需要 交互态/浏览器 API/
  第三方客户端库 的叶子组件标注。
- client 边界下沉：`'use client'` 标在交互叶子，不标在页面/layout（整页 client 化是缺陷）。
- 数据获取在 Server Component（async 组件直连服务/DB），props 串行化传给 client 组件；
  禁止把 DB 连接、密钥、大对象传进 client 组件。
- Server Action 用于表单/变更：`'use server'` 函数内校验 + 鉴权 + 重验证（revalidate）；
  入参视为不可信输入（宪法第 7 条）。

## 3. 数据与缓存

- fetch 缓存语义显式：`{ next: { revalidate: 60 } }` / `{ cache: 'no-store' }`，
  默认行为按当前大版本确认后写明，不靠记忆。
- 变更后定向重验证：`revalidatePath`/`revalidateTag`，命名 tag 统一登记。
- ISR/SSG/SSR 策略逐路由写进 ADR 或页面注释：公开内容 SSG+ISR，
  登录态数据 SSR no-store。
- Route Handler 只做 BFF 薄代理（聚合、鉴权转发、会话 cookie），业务规则不写在 Next 里。

## 4. 鉴权与安全

- 中间件（`middleware.ts`）做路由级拦截；会话 cookie `httpOnly` + `secure` + `sameSite`。
- **环境变量红线**：仅 `NEXT_PUBLIC_` 前缀进客户端 bundle；密钥一律无前缀（仅服务端）；
  构建前自查 bundle 无密钥（grep 构建产物）。
- SSRF 警觉：服务端 fetch 用户可控 URL 时白名单校验目标。
- CSP 与安全头（next.config headers 或部署层）启用。

## 5. 性能与流式

- 流式渲染：`loading.tsx`/`<Suspense>` 包慢数据块，先出骨架再填内容。
- 首屏数据并行获取（`Promise.all`），不串行瀑布。
- 图片一律 `next/image`；字体 `next/font`；第三方脚本 `next/script`。
- 客户端 bundle 监控：`@next/bundle-analyzer`，超 200KB gz 单页必须解释。

## 6. 质量命令

```bash
npm run lint && npm run build && npm test -- --run
```

提交前三项全过（`next build` 含类型检查与路由校验）。
React 共性纪律（组件/状态/类型）见 `standards/frontend-react.md`。
