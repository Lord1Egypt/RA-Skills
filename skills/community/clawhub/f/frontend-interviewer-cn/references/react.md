# React 深度面试题库

## 目录
- [初级](#初级)
- [中级](#中级)
- [高级](#高级)
- [专家](#专家)

---

## 初级

### R-J-01 React 组件生命周期（Class + Hooks 对比）
**难度：** 初级

| 生命周期 | Class | Hooks |
|---------|-------|-------|
| 挂载 | `componentDidMount` | `useEffect(() => {...}, [])` |
| 更新 | `componentDidUpdate` | `useEffect(() => {...}, [deps])` |
| 卸载 | `componentWillUnmount` | `useEffect(() => { return () => {...} }, [])` |
| 错误捕获 | `componentDidCatch` | 无（需 ErrorBoundary class 组件） |
| 渲染优化 | `shouldComponentUpdate` / `PureComponent` | `React.memo` / `useMemo` |

---

### R-J-02 受控组件 vs 非受控组件
**难度：** 初级

- **受控组件**：表单数据由 React state 控制，每次输入触发 setState
- **非受控组件**：数据由 DOM 直接管理，通过 `ref` 获取
- **选择原则**：需要即时校验/联动用受控；简单表单/文件上传用非受控

---

## 中级

### R-M-01 React Fiber 架构
**难度：** 中级/高级  
**考察点：** 渲染机制、并发

**为什么需要 Fiber（React 16 重写）：**
- 旧版 Stack Reconciler：同步递归，无法中断，大量节点更新时阻塞主线程
- Fiber：将渲染工作分解为小单元（Fiber Node），可中断、恢复、优先级调度

**Fiber 节点关键属性：**
```
FiberNode {
  type,          // 组件类型（函数/类/DOM标签）
  key,           // Diff 用的 key
  child,         // 第一个子节点
  sibling,       // 下一个兄弟节点
  return,        // 父节点
  alternate,     // 双缓冲：当前树 ↔ WorkInProgress 树
  effectTag,     // 副作用标记（Placement/Update/Deletion）
  memoizedState, // Hooks 链表（函数组件）
  pendingProps,
  memoizedProps,
}
```

**两个阶段：**
1. **Render/Reconcile 阶段**（可中断）：构建 WorkInProgress Fiber 树，计算副作用
2. **Commit 阶段**（不可中断）：
   - `beforeMutation`：执行 `getSnapshotBeforeUpdate`，异步调度 `useEffect`
   - `mutation`：操作真实 DOM
   - `layout`：执行 `componentDidMount/Update`，同步调度 `useLayoutEffect`

**优先级（Lanes 模型，React 18）：**
```
SyncLane (1)          → 同步（点击等离散事件）
InputContinuousLane   → 连续输入（拖动、滚动）
DefaultLane           → 默认更新
TransitionLane        → startTransition 标记的过渡更新
IdleLane              → 空闲更新
```

---

### R-M-02 React Diff 算法
**难度：** 中级  
**考察点：** 虚拟 DOM、性能

**三个假设（启发式策略）：**
1. 不同类型的节点产生不同子树（直接替换）
2. 通过 `key` 标识跨层级移动的节点
3. 同层比较，不跨层级比较

**单节点 Diff 流程：**
```
新节点 vs 旧节点
├── type && key 都相同 → 复用，标记 Update
├── key 相同但 type 不同 → 删除旧节点，创建新节点
└── key 不同 → 删除旧节点，继续遍历
```

**多节点 Diff（两轮遍历）：**
- 第一轮：处理节点更新（type 相同、key 相同）
- 第二轮：处理新增、删除、移动（使用 Map 优化查找）

**为什么 key 不能用 index：**
- 列表逆序/插入时，index 变化导致大量不必要的重渲染
- 带状态的组件（如 input）会复用错误的 Fiber，状态错位

---

### R-M-03 Hooks 深度解析
**难度：** 中级/高级

**useState 实现原理（简化）：**
```javascript
// Hooks 以链表形式存储在 Fiber.memoizedState 上
let workInProgressFiber;
let workInProgressHook;

function useState(initialState) {
  let hook;
  if (isMount) {
    hook = { memoizedState: initialState, queue: { dispatch: null, pending: null }, next: null };
    // 追加到链表末尾
  } else {
    hook = workInProgressHook; // 按顺序取
    workInProgressHook = workInProgressHook.next;
  }
  
  const dispatch = (action) => {
    hook.queue.pending = { action, next: null };
    scheduleUpdateOnFiber(workInProgressFiber);
  };
  
  return [hook.memoizedState, dispatch];
}
```

**为什么 Hooks 不能在条件语句中调用：**
- Hooks 通过链表顺序维护对应关系
- 条件调用导致顺序错乱，Hook 取到错误状态

**useEffect vs useLayoutEffect：**
| | useEffect | useLayoutEffect |
|--|-----------|-----------------|
| 执行时机 | 浏览器绘制后（异步） | DOM 更新后、绘制前（同步） |
| 适用场景 | 数据请求、订阅 | 需要读取/修改 DOM 布局 |
| SSR | 可用 | 会产生警告 |

**useMemo vs useCallback：**
```javascript
// useMemo 缓存计算结果
const expensiveValue = useMemo(() => compute(a, b), [a, b]);

// useCallback 缓存函数引用
const memoizedFn = useCallback(() => doSomething(a), [a]);
// 等价于 useMemo(() => () => doSomething(a), [a])
```

---

## 高级

### R-S-01 React 18 并发特性
**难度：** 高级

**startTransition：**
```javascript
// 将低优先级更新标记为 Transition
import { startTransition } from 'react';

function handleInput(e) {
  // 高优先级：立即更新输入框
  setInputValue(e.target.value);
  
  // 低优先级：可中断的过渡更新
  startTransition(() => {
    setSearchResults(filter(e.target.value));
  });
}
```

**useDeferredValue：**
```javascript
// 延迟渲染低优先级内容
const deferredQuery = useDeferredValue(query);
return <SearchResults query={deferredQuery} />;
```

**Suspense 与数据获取：**
```javascript
// React 18 Suspense + 异步组件
function UserProfile({ userId }) {
  const user = use(fetchUser(userId)); // React 19 的 use hook
  return <div>{user.name}</div>;
}

<Suspense fallback={<Skeleton />}>
  <UserProfile userId={1} />
</Suspense>
```

**React 18 自动批处理（Automatic Batching）：**
- React 17：仅在 React 事件处理器中批处理
- React 18：所有异步更新（setTimeout、fetch 回调）都自动批处理
- 退出批处理：`flushSync(() => setState(...))`

---

### R-S-02 状态管理方案对比
**难度：** 高级

| 方案 | 原理 | 优势 | 局限 |
|------|------|------|------|
| Context + useReducer | 内置，基于发布订阅 | 无需依赖 | 任意 context 变化触发所有消费者重渲 |
| Zustand | 基于 `useSyncExternalStore` | 简洁，selector 精准更新 | 生态相对小 |
| Redux Toolkit | 单一数据源，纯函数 reducer | 可预测，DevTools 强大 | 样板代码多 |
| Jotai | 原子化状态（atom） | 精细控制，无 Provider | 原子数量多时难管理 |
| Recoil | 原子 + 选择器 | 异步支持好 | Meta 已停更 |
| Valtio | 基于 Proxy | 直接修改，简洁 | 不支持 IE |

---

## 专家

### R-E-01 React Server Components (RSC)
**难度：** 专家

**核心概念：**
- **RSC（Server Components）**：在服务端执行，无 state/effects，可直接访问数据库/文件系统
- **RCC（Client Components）**：添加 `'use client'` 指令，包含交互逻辑
- **RSC Payload**：服务端序列化组件树（JSON-like 格式），传输给客户端

**边界规则：**
```
Server Component
└── Client Component  ('use client')
    └── ❌ 不能直接导入 Server Component
    └── ✅ 可以通过 children prop 接收 Server Component
```

**优势：**
- 零 JS 体积（服务端组件不发送 JS 到客户端）
- 直接数据库查询，无需 API
- 自动代码分割

**追问：** RSC 与 SSR 的区别？
- SSR：在服务端渲染为 HTML，客户端 hydration
- RSC：组件在服务端运行，通过 RSC 协议传输，不一定生成 HTML

---

### R-E-02 性能优化实践
**难度：** 高级/专家

**渲染优化层级：**
```
1. React.memo        → 组件级记忆化（props 浅比较）
2. useMemo           → 计算结果记忆化
3. useCallback       → 函数引用稳定化
4. Context 拆分      → 避免不相关状态更新触发重渲
5. 虚拟列表          → react-virtual / @tanstack/virtual
6. Code Splitting    → React.lazy + Suspense
7. 并发特性          → startTransition / useDeferredValue
```

**Profile 工具：**
- React DevTools Profiler：火焰图分析渲染耗时
- `<React.StrictMode>`：开发模式双调用检测副作用
- `why-did-you-render`：追踪不必要的重渲染
