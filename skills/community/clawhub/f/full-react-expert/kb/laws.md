---
type: cross-cutting
name: laws
version: 2
updated: 2026-11-17
---
# 全局宪法（LAW）

跨领域**不可违背原则**，统一编号可引用。生成代码前逐条自检；引用格式 `LAW-N`。各领域内细则见对应 kb 的「法则」小节（`kb/<subdomain>.md`）。

## 版本纪律

**LAW-1** MUST: 版本敏感问题先确认版本再回答，生成代码前先确认目标版本。
- 违反后果: 方案整体错误（Next 缓存 14/15/16 三次反转是历史教训）；`npm ls` / package.json 是唯一事实来源。
- 溯源: nextjs [NX-1]；全部八领域版本锚定。

## 状态纪律

**LAW-2** NEVER: 服务端数据不得手动复制进全局客户端 store 再手写 loading/error/同步链。
- 违反后果: stale bug 无穷无尽——缓存、失效、去重、重试是 TanStack Query / RSC 的职责，不是你的。
- 溯源: react-core [RC-10]。

**LAW-3** MUST: 服务端环境（SSR/每次请求）的状态容器必须每请求新建（工厂模式），模块级单例仅限浏览器。
- 违反后果: 跨请求/跨用户数据泄漏（SSR 最高危安全事故之一）。
- 溯源: tanstack-query [TQ-5]。

**LAW-4** MUST: 派生值在渲染时计算，不得存 state 再用 effect 同步。
- 违反后果: 双份真相永远修不完的同步 bug。
- 溯源: react-core [RC-2]；You Might Not Need an Effect。

## 安全纪律

**LAW-5** MUST: 一切服务端可执行入口（Server Action、路由、WS 消息、微服务 handler）默认公开——必须服务端鉴权 + 入参校验。
- 违反后果: 任何人拿到入口 id 可直接调用；注入与越权。
- 溯源: nextjs [NX-6]。

**LAW-6** NEVER: 密钥不进任何客户端可达代码（VITE_ 变量、NEXT_PUBLIC_、bundle 内联）。
- 违反后果: 客户端 bundle 可见即公开——静态分析即可提取。
- 溯源: vite-tooling [VT-2]；nextjs [NX]。

## 数据纪律

**LAW-7** MUST: 运行时校验依赖的元数据必须在运行时存在（class / Zod schema / Standard Schema），interface/纯类型一律无效。
- 违反后果: 校验静默失效，非法字段照过——最隐蔽的失败模式。
- 溯源: nestjs [NE-1]。

**LAW-8** MUST: 契约层（DataProvider/API client/adapter）的错误必须显式抛出并携带状态码。
- 违反后果: 上层靠 rejection 驱动通知/登出/重试——吞错等于让整个错误处理链失明。
- 溯源: react-admin [RA-5]。

**LAW-9** MUST: 前后端契约（DTO/类型）必须有单一来源（共享类型包或生成），不得两端各写一份。
- 违反后果: 契约漂移到运行时才暴露。
- 溯源: patterns「共享类型包」。

**LAW-10** MUST: 发布产物必须可追溯到新鲜构建——发版流程固定 build → version → publish。
- 违反后果: 发布旧 dist；漏 private 的应用包误发公共仓库。
- 溯源: monorepo [MO-7]。

## 工程纪律

**LAW-11** MUST: 性能优化先测量（Profiler/Trace/DevTools）再动手。
- 违反后果: 无差别 memo 化制造噪音；优化了不是瓶颈的代码。
- 溯源: react-core [RC-11]。

**LAW-12** MUST: 资源获取与释放必须成对出现在生命周期两侧（连接/订阅/定时器：onModuleInit↔onModuleDestroy、useEffect↔cleanup、订阅↔退订）。
- 违反后果: 连接泄漏、内存泄漏、僵尸订阅更新已卸载组件。
- 溯源: nestjs [NE-6]；react-core [RC-6]。

**LAW-13** NEVER: 测试与异步代码不硬等待（waitForTimeout/sleep）——等待交给自动重试机制（web-first assertions / waitFor / findBy）。
- 违反后果: flaky 测试；慢机器上永远不够快。
- 溯源: testing [TE-4]。

**LAW-14** MUST: 生成的代码交付前自查「静默失效类」错误——无报错但功能失效的模式（校验未挂、回调未订阅、缓存未失效、override 未生效）。
- 违反后果: 这类错误测试和编译都不报，直接带病上线。
- 溯源: ai-mistakes「共性模式」。

## 测试纪律

**LAW-15** MUST: 测行为不测实现——断言 DOM 输出与用户可感知结果，不断言内部 state / mock 调用次数。
- 违反后果: 重构即碎，测试从安全网变成枷锁。
- 溯源: testing [TE-6]。

**LAW-16** MUST: 测试间不得共享可变状态，每测试自造数据。
- 违反后果: 顺序依赖、并行污染。
- 溯源: testing [TE-7]。

## 来源索引

- 本文件全部条款由各 subdomain 法则化萃取的 `[GLOBAL]` 候选合并升维（corpus/react/*/elicited/*-laws.md，2026-11-15）。
- 条款内引用的领域法则详见对应 `kb/<subdomain>.md`「法则」小节与「来源索引」。
- [官方文档] 佐证的条款（LAW-4/7 等）其 URL 见对应 subdomain kb；本文件不重复列出。

## 冲突消解记录

无文档冲突（约束性原则为跨领域共识升维；有官方规则支撑的条款已在溯源中指向对应 kb 的文档锚点）。

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| R43（第四十三轮） | 豁免：无新增 [GLOBAL] 候选（RC-12/RC-13/NX-14/NE-12/RA-13 均为领域内法则，不满足跨领域升维条件） | 2026-11-17 |
| R44（第四十四轮） | 豁免：无新增 [GLOBAL] 候选（RC-14/NX-15/NE-13/RA-14 均为领域内法则；NE-13 的 SSR 单例面向已被 LAW-3 覆盖） | 2026-11-17 |
