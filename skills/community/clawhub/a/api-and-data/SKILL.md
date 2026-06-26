---
name: api-and-data
description: Designs API layer: request encapsulation, error handling, loading/empty states, caching, and data flow. Use when 接口封装, 请求, 错误处理, loading, 缓存, 数据流, or frontend data layer.
---

# 接口与数据层（API and Data）

帮助设计请求封装、错误与 Loading/空态、缓存与数据流。

## 触发场景

- 用户说「接口封装」「请求」「错误处理」「loading」「空态」「缓存」「数据流」
- 需求：统一请求、重试、取消、鉴权、错误提示、列表分页与刷新

## 分析维度

### 1. 请求封装

| 要点 | 做法 |
|------|------|
| 基地址与超时 | axios/fetch 实例：baseURL、timeout、拦截器 |
| 鉴权 | 请求头注入 token；401 统一跳登录或刷新 token |
| 取消 | 页面卸载或路由离开时取消未完成请求（AbortController） |
| 重试 | 对幂等接口或 GET 可有限重试；指数退避可选 |

### 2. 错误处理

| 层级 | 做法 |
|------|------|
| 请求层 | 网络错误、超时、4xx/5xx 转成统一错误格式 |
| 业务层 | 按 code 或 status 分支：未登录、无权限、业务错误文案 |
| UI 层 | 全局 toast/message 或页面级 error 区；关键操作可弹窗确认 |

### 3. Loading 与空态

| 状态 | 做法 |
|------|------|
| Loading | 首屏骨架或 spinner；列表「加载更多」用局部 loading |
| 空数据 | 空列表/空搜索用插画+文案+操作引导 |
| 失败 | 错误文案+重试按钮；可区分网络错误与业务错误 |

### 4. 缓存与更新

| 场景 | 做法 |
|------|------|
| 列表 | 分页参数、拉取后追加或替换；下拉刷新/上拉加载 |
| 详情 | 进入页拉取；离开可保留一段时间再失效（如 React Query staleTime） |
| 实时性 | 短 staleTime + 窗口 focus 时 refetch；或 WebSocket 推送 |

### 5. 数据流

| 规模 | 建议 |
|------|------|
| 简单 | 组件内 useState + useEffect 请求；状态提升到父组件即可 |
| 多页共享 | Context + 请求函数 或 React Query/SWR 等 |
| 复杂 | 全局 store（Zustand/Redux）+ 异步 thunk/saga 或 React Query 做服务端状态 |

## 执行流程

### 1. 确认用户的实际问题

用户说「接口封装」「请求」这类词时，先判断他们真正卡在哪：

| 用户描述 | 实际问题 | 第一步 |
|---------|---------|-------|
| 「接口怎么封装」「请求层怎么写」 | 从零设计请求层 | 问：用 axios 还是 fetch？有没有现成的拦截器？鉴权方式是什么？ |
| 「loading 怎么做」「空态怎么处理」 | UI 状态管理 | 直接给出该场景的状态机模型和代码示例 |
| 「接口报错了」「401 没处理」 | 具体 bug | 问：错误在哪一层出现的？是请求层还是业务层？ |
| 「用 React Query 还是 SWR」 | 选型决策 | 问：项目规模、是否有 SSR、团队熟悉度，然后给出明确推荐 |
| 「缓存怎么做」 | 缓存策略 | 问：哪类数据需要缓存？实时性要求是什么？ |

不要一上来就把所有维度都输出，先定位用户卡在哪一层。

### 2. 根据问题类型切入

**从零设计请求层时**，按这个顺序问清楚再给方案：
1. HTTP 客户端（axios/fetch/ky）
2. 鉴权方式（token 放哪、刷新逻辑）
3. 错误码约定（后端返回格式是什么）
4. 是否需要请求取消（路由切换时）

信息齐了，给出完整的实例配置 + 拦截器代码，不要只给原则。

**处理具体状态问题时**，直接给代码，不要先讲理论：
- loading/空态/错误态 → 给出状态机或 React Query 的 `isLoading/isError/data` 用法
- 分页 → 给出 `useInfiniteQuery` 或手写分页 hook 的完整示例

**选型问题时**，给明确结论：
- 有 SSR（Next.js）→ React Query，因为它支持 hydration
- 纯 CSR 简单项目 → SWR，更轻量
- 需要复杂缓存控制/乐观更新 → React Query
- 不要给「两个都可以，看情况」这种答案

### 3. 给出方案后主动检查遗漏

方案给完后，自查这几个点是否覆盖：
- [ ] 接口失败时用户看到什么？
- [ ] 请求进行中用户能不能重复触发？
- [ ] token 过期时怎么处理？
- [ ] 组件卸载时未完成的请求会不会报错？

有遗漏的主动补上，不要等用户问。

## 输出模板

```markdown
## 接口与数据层方案

### 请求封装
- 实例：baseURL、timeout、拦截器
- 鉴权/取消/重试：…

### 错误处理
- 分层：请求层 / 业务层 / UI 层
- 文案与重试：…

### Loading 与空态
- 首屏/列表/详情：…
- 空数据/失败：…

### 缓存与数据流
- 列表/详情：…
- 工具：React Query / SWR / 自管理
```

## 项目相关

- React：React Query / SWR 做请求与缓存；axios 或 fetch 做实例与拦截
- Vue：Pinia + 请求封装；或 useRequest / VueUse 等
- Next：服务端 fetch 与 Client 请求分离；注意 hydration 与缓存键
