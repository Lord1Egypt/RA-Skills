# React 编码规范（前端工程师实现必读）

适用：React 18+ / TypeScript strict / Vite / React Router 6+ 或 Next.js App Router。

## 1. 工程结构

```
src/
├── api/            # 请求层：client（axios/fetch 封装）+ 按域分模块 + 类型
├── components/
│   ├── ui/         # 基础组件（Button、Input…五态齐全）
│   └── business/   # 业务组件（绑定领域数据）
├── features/<域>/  # 页面 + 域内组件 + 域 hook 聚合（feature 优先组织）
├── hooks/          # 通用 hook
├── stores/         # 全局状态（Zustand/Redux Toolkit，按需）
├── utils/          # 纯函数工具
└── routes/         # 路由定义（路由级懒加载）
```

跨 feature import 只允许走 feature 的公开出口（index.ts）；禁止 feature 互相深引用。

## 2. 类型纪律

- `strict: true`；禁止 `any`、`as` 断言链、`!` 非空断言；API 响应类型从契约/生成代码定义，
  禁止 `any` 接响应后到处断言。
- 组件 props 显式 interface；children/事件处理器类型准确（`React.ReactNode`、
  `React.MouseEvent<HTMLButtonElement>`）。
- API 层是类型唯一入口：组件不手写响应接口，统一从 `api/` 导入。

## 3. 组件规则

- 函数组件 + hooks；禁止类组件（错误边界用 react-error-boundary）。
- 单组件 ≤ 200 行；状态与逻辑抽自定义 hook（`useXxx`），UI 与逻辑分离。
- 渲染控制：条件渲染清晰化（提前 return/子组件），不在 JSX 内写复杂表达式与副作用。
- 列表渲染 key 用稳定业务 id，禁止数组下标。
- 受控组件统一；表单用 react-hook-form（或等价），校验规则与后端契约一致，双端校验不删减。

## 4. 状态与数据

- 状态分层：组件内 UI 态（useState）/ 跨组件域态（Context 或 Zustand）/
  服务端数据（TanStack Query 优先，禁手写 loading/error 样板）。
- 服务端数据与 UI 状态分仓；服务端数据不在本地深拷贝改写。
- 异步组件五态：数据态必须显式处理 loading/error/empty/success，
  用 query 的 isLoading/isError 语义，不搞布尔拼接。

## 5. 性能与可达性

- 默认无需 memo；先测后优化（React DevTools Profiler 定位后再 memo/useMemo）。
- 路由级 `React.lazy` 代码分割；大列表虚拟滚动（@tanstack/react-virtual）。
- 语义化标签 + 键盘可操作 + focus-visible 样式；alt/aria-label 齐全。

## 6. 质量命令

```bash
npm run lint && npm run build && npm test -- --run
```

提交前三项全过；ESLint（typescript-eslint strict + react-hooks 规则）无 ERROR。
