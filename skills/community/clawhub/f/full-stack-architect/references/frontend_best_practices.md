# React & Next.js 最佳实践总结

> 来源：Vercel React Best Practices
> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、Eliminating Waterfalls（消除瀑布流）

### 1.1 Async API Routes
- 使用异步API路由优化数据获取
- 避免客户端到服务器的数据获取瀑布流
- 推荐使用异步组件和流式渲染

### 1.2 Async Dependencies
- 并行加载异步依赖
- 使用 `Promise.all()` 优化加载顺序
- 避免串行依赖加载

### 1.3 Async Parallel Fetching
- 在服务器端并行获取多个数据源
- 使用 `Promise.all()` 同时发起多个请求
- 大幅减少总加载时间

### 1.4 Async Defer & Await
- 合理使用 `defer` 优化渲染策略
- 区分关键路径和非关键路径数据
- 渐进式加载提升用户体验

### 1.5 Async Suspense Boundaries
- 使用 Suspense 边界控制加载状态
- 避免整个页面因单个组件加载失败而崩溃
- 提供更好的错误处理和用户反馈

---

## 二、Bundle Size Optimization（包大小优化）

### 2.1 Bundle Barrel Imports
- 优化 barrel imports 避免大量导入
- 直接导入所需组件而非整个包
- 使用 tree-shaking 友好的导入方式

### 2.2 Bundle Conditional Imports
- 条件导入减少不必要的依赖
- 根据环境动态加载代码
- 使用 `dynamic import` 实现懒加载

### 2.3 Bundle Dynamic Imports
- 动态导入实现代码分割
- 按需加载组件和功能
- 减少初始加载体积

### 2.4 Bundle Preload
- 预加载关键资源
- 使用 `preload` 和 `prefetch` 提示
- 平衡加载优先级和性能

---

## 三、Server-Side Performance（服务端性能）

### 3.1 Server After Nonblocking
- 非阻塞式API调用
- 将非关键操作放到响应之后
- 优先返回核心内容

### 3.2 Server Auth Actions
- 安全的认证操作设计
- 使用 Server Actions 处理表单提交
- 避免客户端暴露敏感逻辑

### 3.3 Server Cache LRU
- LRU缓存策略优化
- 合理设置缓存大小和过期时间
- 避免频繁重建相同数据

### 3.4 Server Cache React
- React缓存机制利用
- 使用 React Query 或 SWR 管理缓存
- 缓存策略与业务需求匹配

### 3.5 Server Dedup Props
- 去重相同的属性传递
- 避免重复计算和渲染
- 使用 memoization 优化

### 3.6 Server Hoist Static IO
- 提升静态IO操作到组件外
- 避免每次渲染都执行静态操作
- 利用构建时计算

### 3.7 Server Parallel Nested Fetching
- 并行嵌套数据获取
- 优化深层数据依赖
- 减少总体加载时间

### 3.8 Server Serialization
- 优化数据序列化
- 避免传递大型对象
- 使用合适的数据格式

---

## 四、Client-Side Performance（客户端性能）

### 4.1 Client Event Listeners
- 合理管理事件监听器
- 及时清理不再需要的监听器
- 使用事件委托减少监听器数量

### 4.2 Client LocalStorage Schema
- LocalStorage使用规范
- 避免存储大量数据
- 定期清理过期数据

### 4.3 Client Passive Event Listeners
- 使用被动事件监听器
- 优化滚动和触摸事件
- 提升响应性

### 4.4 Client SWR Dedup
- SWR去重机制
- 避免重复请求相同数据
- 合理设置 deduping 策略

---

## 五、Re-render Optimization（重渲染优化）

### 5.1 Rerender Defer Reads
- 延迟读取优化渲染
- 避免在渲染过程中读取不必要的数据
- 使用 `useDeferredValue`

### 5.2 Rerender Dependencies
- 优化依赖数组
- 避免不必要的依赖项
- 使用稳定的引用

### 5.3 Rerender Derived State No Effect
- 派生状态避免使用Effect
- 使用 useMemo 计算派生状态
- 减少不必要的Effect触发

### 5.4 Rerender Derived State
- 派生状态计算优化
- 合理使用 useMemo
- 避免在渲染中执行昂贵计算

### 5.5 Rerender Functional SetState
- 函数式 setState 使用
- 避免状态依赖问题
- 更安全的状态更新

### 5.6 Rerender Lazy State Init
- 懒加载状态初始化
- 避免每次渲染都初始化
- 使用函数初始化状态

### 5.7 Rerender Memo With Default Value
- Memo组件带默认值
- 避免不必要的重新渲染
- 合理设置比较函数

### 5.8 Rerender Memo
- 合理使用 React.memo
- 优化组件渲染性能
- 避免过度使用

### 5.9 Rerender Move Effect To Event
- 将Effect逻辑移到事件处理函数
- 减少不必要的Effect执行
- 更好的性能控制

### 5.10 Rerender No Inline Components
- 避免内联组件定义
- 将组件定义移到函数外
- 减少不必要的组件重建

### 5.11 Rerender Simple Expression In Memo
- Memo中使用简单表达式
- 避免复杂计算影响性能
- 合理拆分逻辑

### 5.12 Rerender Split Combined Hooks
- 拆分组合Hook
- 更好的代码组织
- 更精确的依赖管理

### 5.13 Rerender Transitions
- 使用 Transition API
- 优化用户界面响应
- 区分紧急和非紧急更新

### 5.14 Rerender Use Deferred Value
- 使用 useDeferredValue
- 延迟非关键更新
- 提升关键路径性能

### 5.15 Rerender Use Ref Transient Values
- 使用ref存储临时值
- 避免不必要的状态更新
- 优化组件性能

---

## 六、Rendering Performance（渲染性能）

### 6.1 Rendering Activity
- 渲染活动监控
- 识别不必要的渲染
- 使用React DevTools分析

### 6.2 Rendering Animate SVG Wrapper
- SVG动画优化
- 使用适当的动画策略
- 避免重绘和重排

### 6.3 Rendering Conditional Render
- 条件渲染优化
- 避免不必要的DOM操作
- 使用合适的条件渲染方式

### 6.4 Rendering Content Visibility
- 内容可见性控制
- 使用 content-visibility
- 优化离屏内容渲染

### 6.5 Rendering Hoist JSX
- 提升JSX定义位置
- 避免在渲染中创建新组件
- 优化组件结构

### 6.6 Rendering Hydration No Flicker
- 避免水合闪烁
- 优化服务端渲染
- 使用合适的水合策略

### 6.7 Rendering Hydration Suppress Warning
- 合理抑制水合警告
- 处理客户端和服务端差异
- 避免误报

### 6.8 Rendering Resource Hints
- 资源提示优化
- 使用 preload/prefetch
- 提升资源加载性能

### 6.9 Rendering Script Defer Async
- 脚本加载策略
- 使用 defer/async
- 优化关键渲染路径

### 6.10 Rendering SVG Precision
- SVG精度优化
- 避免不必要的精度
- 平衡质量和性能

### 6.11 Rendering Usetransition Loading
- 使用Transition加载状态
- 更好的用户体验
- 优化状态转换

---

## 七、JavaScript Performance（JavaScript性能）

### 7.1 JS Batch DOM CSS
- 批量DOM和CSS操作
- 减少重排和重绘
- 使用requestAnimationFrame

### 7.2 JS Cache Function Results
- 函数结果缓存
- 使用 memoization
- 避免重复计算

### 7.3 JS Cache Property Access
- 属性访问缓存
- 优化对象属性读取
- 减少重复查找

### 7.4 JS Cache Storage
- 存储操作优化
- 合理使用缓存
- 避免频繁IO操作

### 7.5 JS Combine Iterations
- 合并迭代操作
- 减少循环次数
- 优化数据处理

### 7.6 JS Early Exit
- 提前退出策略
- 避免不必要的计算
- 优化条件判断

### 7.7 JS Flatmap Filter
- Flatmap和Filter优化
- 合理组合数组操作
- 减少中间数组

### 7.8 JS Hoist Regexp
- 正则表达式提升
- 避免在循环中创建正则
- 预编译正则表达式

### 7.9 JS Index Maps
- 索引映射优化
- 使用Map/Set加速查找
- 避免嵌套循环

### 7.10 JS Length Check First
- 先检查长度
- 避免不必要的处理
- 优化边界判断

### 7.11 JS Min Max Loop
- 最小最大循环优化
- 减少循环次数
- 优化算法复杂度

### 7.12 JS Request Idle Callback
- 使用requestIdleCallback
- 后台任务优化
- 不阻塞主线程

### 7.13 JS Set Map Lookups
- Set/Map查找优化
- 利用数据结构特性
- 提升查找性能

### 7.14 JS Tosorted Immutable
- 不可变排序
- 避免原数组修改
- 使用toSorted

---

## 八、Advanced Patterns（高级模式）

### 8.1 Advanced Event Handler Refs
- 事件处理器Ref模式
- 优化事件回调
- 避免不必要的重渲染

### 8.2 Advanced Init Once
- 一次性初始化模式
- 避免重复初始化
- 使用Ref存储初始化结果

### 8.3 Advanced Use Latest
- UseLatest模式
- 获取最新值而不触发渲染
- 优化闭包问题

---

## 性能影响等级说明

- **CRITICAL** - 最高优先级，重大性能提升
- **HIGH** - 显著性能改进
- **MEDIUM-HIGH** - 中高收益
- **MEDIUM** - 中等性能改进
- **LOW-MEDIUM** - 低中收益
- **LOW** - 渐进式改进

---

## 最佳实践原则

1. **性能与开发体验平衡**：不盲目追求性能而牺牲可维护性
2. **测量优先**：优化前先测量，找到真正的瓶颈
3. **渐进式优化**：从高影响项开始，逐步改进
4. **实际场景出发**：根据具体业务需求选择合适的优化策略
5. **代码可读性**：优化代码但保持可读性和可维护性

