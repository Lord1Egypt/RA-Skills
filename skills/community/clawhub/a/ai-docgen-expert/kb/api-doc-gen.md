---
subdomain: api-doc-gen
version: 2
updated: 2026-11-17
---

# api-doc-gen — API 参考文档生成（TSDoc / 工具链 / 错误与废弃 / OpenAPI spec / AI 生成纪律）

## 定位与心智模型

本子域覆盖 TS 项目 API reference 文档的生成与治理：TSDoc 标注规范、TypeDoc/ApiExtractor 工具链、reference 条目结构（五要素）、错误与废弃文档化、OpenAPI spec 生成路线、AI 生成 API 文档的纪律。

核心思想：**类型系统是第一文档层**。TS 类型签名 > 命名 > TSDoc 注释 > 手写文档——每往上一层，信息少一份维护负担；文档只写类型系统表达不了的内容（约束/单位/语义/边界/副作用）。[模型经验]（elicited/04）

TSDoc 的存在理由是解决「每个工具一个方言」的碎片化（ESLint/TypeDoc/ApiExtractor 曾各认一套注释语法）。官方三设计要求 [官方文档](https://tsdoc.org)：

| 设计要求 | 含义 |
|---|---|
| Extensibility | 可扩展——自定义标签必须能被其他工具安全忽略 |
| Interoperability | 互操作——跨工具（TypeDoc / DocFX / API Extractor / ESLint / VS Code）统一解析 |
| Familiar syntax | 熟悉语法——从 JSDoc 迁移无陡坡 |

适用边界：TS 项目（JSDoc 面向 JS；TSDoc 的前提是类型信息由 TS 承担）。REST/HTTP API 的 spec 层由 OpenAPI 路线覆盖（见场景 6）。

## 法则

编号与 elicited/09-laws.md 一致，AD-1 ~ AD-13。

**AD-1** **MUST**（[GLOBAL] 候选）: 自文档化层级：类型 > 命名 > 注释 > 手写文档。能进类型系统的不写注释，能命名自明的不解释；文档只写类型系统表达不了的（约束/单位/语义/边界/副作用）。
- 违反后果: 信息双份存储——签名重构后注释/文档漂移，读者照过期文档写代码。
- 溯源: [模型经验]（elicited/04-signature-design-impact）

**AD-2** **MUST**（[GLOBAL] 候选）: 无源不生成，事实数据零编造。签名、参数名、默认值、错误码、移除版本是事实数据——必须来自源码/类型/官方文档；无源时只能产出「结构模板 + 待填标注」，不得用「同类 API 典型形态」补全。
- 违反后果: 签名幻觉/参数编造/错误码虚构直接进文档，读者照抄即崩溃；编造内容与事实内容输出形态相同，使用者无法分流。
- 溯源: [模型经验]（elicited/07-ai-api-doc-mistakes）

**AD-3** **MUST**: reference 条目五要素完备：签名/参数/返回/错误/示例。缺项即不完整：有默认值必写默认行为、返回 Promise 必列 reject 路径、会抛必列条件、重载必分支化、有副作用必显式。
- 违反后果: 读者只看到 happy path——catch 后对着 code 猜语义、边界值猜形态、重载分支差异未知。
- 溯源: [模型经验]（elicited/02-api-reference-anatomy）

**AD-4** **MUST**: TSDoc 摘要行只放一句话，细节进 @remarks。首句短（tooltip 可完整显示）；类型信息不重复进注释（TS 项目禁手写 `@param {type}`）；跨工具统一用 TSDoc 而非 JSDoc 方言。
- 违反后果: tooltip 截断；类型双份维护漂移；工具方言渲染差异。
- 溯源: [模型经验]（elicited/01-tsdoc-annotation）+ [官方文档](https://tsdoc.org)（标签规范）

**AD-5** **MUST**: 边界条件是文档主体。空结果形态、null/undefined/省略三态、末页游标、无匹配行为——「是什么」之后必答「何时不是」。
- 违反后果: 读者在空结果/三态/分页边界场景写错代码，产出运行时 bug。
- 溯源: [模型经验]（elicited/02）

**AD-6** **MUST**: 错误文档三件套：清单/分类/可重试性。每个错误：触发条件（读者视角）+ 建议 + 重试语义；传输层（HTTP）与业务层错误码双体系显式映射；错误信息文案本身要可操作（含字段/规则/实际值）。
- 违反后果: 读者盲目 retry 或放弃；排障者对着 `invalid input` 无从定位。
- 溯源: [模型经验]（elicited/05-error-codes-documentation）

**AD-7** **MUST**: 示例最小可运行。每个 reference 条目至少一个含 import 的最小调用示例；示例不得调用不存在/已废弃的方法；长示例退到 how-to。
- 违反后果: 新用户照示例第一步即失败（调用已改名/已废弃方法），示例成为错误传播源。
- 溯源: [模型经验]（elicited/02、07）

**AD-8** **MUST**: 工具链生成 raw，治理出文档。TypeDoc 等生成的是素材不是成品：注释覆盖率检查、@internal 过滤、生成进 CI、与手写站导航统一——四项治理缺一不可；文档站产物不提交仓库，ApiExtractor 报告（.api.md）提交（diff 即 API 审查面）。
- 违反后果: 出站一半导出裸签名、内部 API 泄露进公开文档、本地生成一次后再没更新。
- 溯源: [模型经验]（elicited/03-toolchain-config）+ [官方文档](https://typedoc.org)（入口点发现）+ [官方文档](https://api-extractor.com/pages/overview/demo_api_report/)（.api.md 报告 Git 追踪、随 PR 提交、diff 即 API 审查面——第 7 轮补锚溯源升级）

**AD-9** **MUST**: 废弃三承诺：替代/宽限/预告。废弃必给替代与迁移指引、移除版本在宣布日预告、废弃期行为冻结；`@deprecated` 裸标注（无原因无替代无版本）是缺陷。
- 违反后果: 用户知道不能用但不知道去哪；升级即断裂；库信任流失。
- 溯源: [模型经验]（elicited/06-deprecation-lifecycle）

**AD-10** **MUST**: 废弃即全站扫描。标注 @deprecated 当天 grep 全部文档资产（tutorial/README/示例；changelog 历史条目例外——保持历史准确不回改）；官方示例不得继续使用废弃 API。
- 违反后果: 新用户照 tutorial 写出废弃调用，废弃在全站扩散。
- 溯源: [模型经验]（elicited/06）

**AD-11** **MUST**: 迁移指南起点是旧代码。读者带着存量代码来：旧→新对照表 + 行为差异列（默认值/错误处理/时序）+ 可否机械替换；不是新 API 教程。
- 违反后果: 机械替换后出微妙 bug（默认值/错误类型差异静默）。
- 溯源: [模型经验]（elicited/06）

**AD-12** **MUST**: 文档难写是设计坏味信号。布尔魔法参数、长位置列表、tuple 返回、隐式副作用、上帝参数——文档被迫硬解释时应上报设计问题（ADR/issue），而非用文字打补丁。
- 违反后果: 文档持续给坏设计打补丁，每个版本的文档成本只增不减。
- 溯源: [模型经验]（elicited/04）

**AD-13** **MUST**: OpenAPI spec 与代码只能有一个手写真源。spec-first（spec 生成桩/客户端）或 code-first（装饰器/注释生成 spec）二选一；CI 双向校验（spec↔代码 diff）；错误响应（非 200）必入 spec（spec 是错误文档的机器可读载体——AD-6 联动）；schema 复用（components 引用）防 spec 膨胀漂移；装饰器与注释两路线按框架现实取舍。
- 违反后果: spec 与代码漂移，客户端 SDK 按旧契约生成；错误类型全靠猜。
- 溯源: [模型经验]（elicited/08-openapi-spec-generation；结构层高置信，装饰器语法细节待验证）

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| TSDoc | TS 项目的注释规范，解决工具方言碎片化；类型交给 TS，注释只写类型外语义 [官方文档](https://tsdoc.org) |
| JSDoc | JS 时代事实标准；60+ block 标签 + 2 inline 标签，多数标签为 JS 类型标注服务 [官方文档](https://jsdoc.app) |
| TypeDoc | TS 生态主流文档工具：读 .ts 源 + TSDoc 注释生成文档站，输出 HTML/JSON [官方文档](https://typedoc.org) |
| API Extractor（@microsoft/api-extractor） | TypeScript 分析工具，三输出：API Report（默认 `etc/<pkg>.api.md`，Git 追踪、变更随 PR 提交、diff 即 API 审查面）/ .d.ts Rollup（按 release type 修剪）/ doc model JSON（api-documenter 伴生工具）；alpha/beta/public 毕业模型；不是文档站工具 [官方文档](https://api-extractor.com/)（第 7 轮补锚溯源升级） |
| entryPoints | 文档生成入口点；库场景可由 package.json exports/main 自动发现 [官方文档](https://typedoc.org) |
| entryPointStrategy Expand | TypeDoc 策略：应用（非库）场景逐文件展开生成文档 [官方文档](https://typedoc.org) |
| 摘要行 vs @remarks | 摘要行 = 第一句（tooltip 显示）；@remarks = 长说明与边界条件主体 |
| 五要素 | reference 条目完备判据：签名/参数/返回/错误/示例 |
| 错误三件套 | 错误清单 / 错误分类（调用方/系统/业务）/ 可重试性 |
| 废弃三承诺 | 废弃即给替代方案、宽限期足够长且移除版本预先宣告、废弃期行为冻结 |
| 废弃生命周期 | deprecated → 宽限期（警告不破坏）→ 移除（breaking） |
| spec-first / code-first | spec 生成桩（spec 是 SSOT）vs 代码生成 spec（代码是 SSOT）——只能有一个手写真源 |
| 装饰器路线 vs 注释路线 | OpenAPI 信息由路由装饰器携带（NestJS/tsoa）vs 注释块内嵌 YAML（swagger-jsdoc） |
| 自文档化层级 | 类型签名 > 命名 > TSDoc 注释 > 手写文档 |
| @microsoft/tsdoc | TSDoc 参考解析器 + Playground；lint 集成路径 eslint-plugin-tsdoc 在位 [官方文档](https://tsdoc.org) |

## 最佳实践

### 场景 1：从 JSDoc 习惯迁移到 TSDoc（TS 项目注释标注）

推荐路径：
1. 类型信息全部交给 TS 类型系统；注释只写类型外语义（约束/单位/默认行为/副作用）。
2. 摘要行一句话；细节与边界条件进 `@remarks`。
3. 标签拼写用 TSDoc 全集（见 API 速查表）——默认值用 `@defaultValue`，不是 JSDoc 的 `@default`。
4. 跨工具一致性用 `@microsoft/tsdoc` 参考解析器 / eslint-plugin-tsdoc 校验。[官方文档](https://tsdoc.org)

```ts
// ✗ JSDoc 时代写法：手写类型 + 复读参数名
/**
 * @param {string} url - the url string
 * @returns {Promise<object>} the result object
 */
function listResources(url: string, timeout?: number): Promise<QueryResult> {}

// ✓ TSDoc：类型交给 TS，注释写类型外语义
/**
 * 获取资源列表。
 * @param url - 资源地址，须为绝对 URL（类型系统只知是 string，约束写文档）
 * @param timeout - 超时毫秒数；省略与传 undefined 等价（用全局默认 5000）
 * @remarks `rows` 无匹配时为空数组（非 null）；`cursor` 末页为 null。
 * @throws NetworkError 网络不可达时抛出
 */
```

边界条件：纯 JS 项目（无 TS）仍用 JSDoc——TSDoc 的前提是类型信息由 TS 承担。自明命名的参数允许极简描述但保持覆盖（工具渲染一致性）。[模型经验]（elicited/01）

本实践源于 [AD-1]、[AD-4]。

### 场景 2：写一个完整的 reference 条目（五要素）

推荐路径：
1. 签名：完整类型签名，重载每个分支单独文档化。
2. 参数：逐参数写类型外信息——有默认值必写「不传会发生什么」；可空参数写省略/undefined/`{}` 三态差异。
3. 返回：返回值语义 + 关键字段边界（空/末页/null）。
4. 错误：`@throws` 条件或错误码表（触发条件 + 建议处理 + 可重试性）。
5. 示例：含 import 的最小可运行调用。
6. 副作用（缓存失效/事件触发/状态变更）、幂等性/取消能力（AbortSignal）有则必显式。

```ts
// ✗ 类型复读 + happy path only
/**
 * @param options - the options
 * @returns the result
 */

// ✓ 边界条件为主体
/**
 * 查询数据。
 * @param options - 省略与传 undefined 等价（用全局默认）；传 `{}` 时各字段退化为默认值
 * @returns 命中行；无命中时 `rows` 为空数组（非 null）
 * @remarks 调用两次会命中缓存（副作用：缓存失效时间戳更新）。
 */
```

边界条件：从签名推导不出类型外语义（约束/默认值/单位）——无实现源码时应标注「需人工补充」而非编造。[模型经验]（elicited/02 自我质询 2，[AD-2] 联动）

本实践源于 [AD-3]、[AD-5]、[AD-7]。

### 场景 3：错误文档化（三件套）

推荐路径：
1. 错误清单盘点：遍历实现中的 throw/reject 点，每条含——标识（code/异常类名）、触发条件（读者视角：什么输入会触发，不是「validator 返回 false」这类实现注释）、错误信息示例、建议处理、关联错误族。
2. 错误分类：调用方错误（4xx 型）/ 系统错误（5xx 型）/ 业务规则错误——处理策略不同，分表或分段。
3. 可重试性：每条标注 `retry: yes(backoff) / no / needs-action`。
4. HTTP 状态码与 body 业务错误码双体系做显式映射表：状态码 × body code × 触发条件 × 处理。
5. 错误信息文案本身要可操作（它是排障者第一接触面）。

```ts
// ✗ throw new Error('invalid input') —— 哪个字段？什么规则？
// ✓ throw new Error('field "email" failed pattern /^[^@]+@[^@]+$/: got "a@b"')
```

边界条件：错误码清单是事实数据——AI 无源只能生成「结构模板」让实现侧填，不得凑一列看起来合理的 code（[AD-2]）。[模型经验]（elicited/05）

本实践源于 [AD-6]。

### 场景 4：废弃一个 API（全流程）

推荐路径：
1. `@deprecated` 标注一次写全：原因 + 替代 + 迁移指引 + 移除版本。移除版本是项目决策——无源留占位符，不得编造（[AD-2]）。
2. 迁移指南：旧→新对照表 + 行为差异列（默认值/错误处理/时序）+ 可否机械替换。
3. 全站扫描：当天 grep 全部文档资产（tutorial/README/示例），官方示例不得继续使用废弃 API；changelog 历史条目保持历史准确不回改。
4. changelog 联动 + ADR 记录废弃动机。
5. 废弃期行为冻结：只修安全 bug，不加功能。

```ts
// ✗ @deprecated
// ✓ @deprecated 自 v3.2：此函数在 SSR 场景泄漏监听器，改用 useSafeListener()
//    （迁移指南：/docs/migrate/v3#listener）。v5.0 移除。
```

边界条件：宽限期**时长**无官方数字，但最低结构约束是官方规定——SemVer 规则 7：public API 功能标记 deprecated 时 MUST bump MINOR；官方 FAQ：完全移除只能发生在其后的新 major，且此前至少有一个含该 deprecation 的 minor release（「先 minor 后 major」）[官方文档](https://semver.org/spec/v2.0.0.html)。移除版本在宣布日预告即锚定此结构。内部 API 可走快删通道（与公共 API 纪律分离）。[官方文档](https://semver.org/spec/v2.0.0.html) + [模型经验]（elicited/06）

本实践源于 [AD-9]、[AD-10]、[AD-11]。

### 场景 5：搭建并治理 TypeDoc 文档管线

推荐路径：
1. `npm i -D typedoc`。[官方文档](https://typedoc.org)
2. 入口点：库场景依赖自动发现（package.json exports/main），或显式传参；应用（非库）场景用 `--entryPointStrategy Expand` 逐文件展开。[官方文档](https://typedoc.org)
3. 注释覆盖率检查进 CI（脚本遍历导出符号查 TSDoc 摘要），阈值门槛。
4. `@internal` 标注 + 过滤，防内部 API 混进公开文档。
5. 生成进 CI；产物策略二分：文档站产物不提交仓库（CI 部署），ApiExtractor `.api.md` 报告提交（PR diff 即 API 变更审查面）。
6. 文档站已用 Docusaurus/VitePress 时，用 markdown 输出管线（typedoc-plugin-markdown / api-documenter）进同一 SSG 导航树，避免生成站与手写站割裂。

边界条件：配置键名必须来自官方文档，不得凭记忆虚构（TypeDoc 配置项以 typedoc.org 为准）。monorepo 的 entryPoints 多包治理是真实痛点——新增包忘加入口点即文档缺失。[模型经验]（elicited/03）

本实践源于 [AD-8]。

### 场景 6：OpenAPI spec 生成路线选型

推荐路径：
1. 定真源：spec-first（外部契约稳定性要求高、多客户端并行时）或 code-first（内部快速迭代）——二选一，两边手写必漂移。
2. code-first 内选路线：装饰器体系成熟的项目（NestJS/tsoa）走装饰器路线（类型推导强、与代码同步强）；轻量/无装饰器框架（Express + swagger-jsdoc）走注释路线（框架无关，但 YAML schema 与 TS 类型双写是漂移源——尽量加类型推导转换层）。
3. 错误响应（非 200）必入 spec——spec 是错误文档的机器可读载体。
4. schema 复用（components 引用），防每端点内联重复定义导致 spec 膨胀 + 漂移。
5. 生成的 spec 进 CI：跑 validator + spec↔代码双向 diff 校验。
6. `examples` 字段必填——spec 有 schema 无示例，文档站渲染空洞。

边界条件：具体装饰器/注释语法（NestJS `@ApiOperation`、tsoa 注解、swagger-jsdoc `@openapi` 块格式）未经文档验证——使用时必须锚定对应框架文档，不得凭记忆（[AD-2] 同根纪律）。OpenAPI 3.0 vs 3.1 取舍素材不足，生成版本建议时保守。[模型经验]（elicited/08）

本实践源于 [AD-13]、[AD-6]。

### 场景 7：AI 生成 API 文档的纪律（无源场景）

推荐路径：
1. 源在手（类型定义/实现源码/官方文档）才生成逐项文档；无源只产出「结构模板 + 待填标注」。
2. 事实数据清单化处理：签名、参数名、默认值、错误码、移除版本——一律视为「需源验证」，凡具体值必溯实现。
3. 区分「源驱动段落」与「推断段落」，推断段显式标注置信度——编造内容与事实内容不得同形输出。
4. 长文档分批生成 + 自检，防「疲劳漂移」（前 20 条严谨、后面复读化）。
5. 示例写「该 API 真实最小用法」，不写教科书化完美示例；易错用法正是读者踩坑处，需警示。

边界条件：本场景为模型自我内省 + 行业观察，无上游文档对应——是本知识库特有贡献层。[模型经验]（elicited/07）

本实践源于 [AD-2]。

## 高频坑点（速查）

### 速查表

| 症状 | 根因 | 修复 | 法则 |
|---|---|---|---|
| `@param {string} url` 但签名是 `url: number` | JSDoc 习惯迁移，类型双份存储，重构忘改注释 | 删 `{type}`，只写类型外语义 | AD-4 / AD-1 |
| TSDoc 注释里写了 `@default` | JSDoc/TSDoc 拼写混用 | TSDoc 用 `@defaultValue`（JSDoc 才是 `@default`） | AD-4 |
| 示例调用 `getClient()`，API 三版本前已改名 | `@example` 内容不被编译器校验 | 示例最小化；工具链提取示例做编译校验 | AD-7 |
| `@returns 返回结果对象`，20 个字段靠猜 | 注释只写「是什么」不写字段边界 | `@remarks` 展开关键字段边界 | AD-5 / AD-3 |
| `@defaultValue 3000`，实际是 5000 | 默认值藏在实现里，未读实现猜值 | 读实现填值；读不到写「待确认（见源码）」 | AD-2 |
| `Promise<T>` 文档写成 `T`，示例不 await | 同步异步混淆 | 五要素自检第一步：核对真实签名 | AD-3 |
| 把必填参数写成可选（或反之） | 可选性幻觉，「?」一字符之差 | 签名比对（源驱动） | AD-2 / AD-3 |
| `{@link Foo}` 指向不存在的导出 | link 幻觉 | 生成后比对导出清单 | AD-2 |
| reference 站一半导出裸签名无说明 | TypeDoc 不强制注释，无覆盖率治理 | 覆盖率检查进 CI，阈值门槛 | AD-8 |
| 内部 API 混进公开文档 | `@internal` 未标/未过滤 | 标注 + 过滤；`@internal` 跨工具解析歧义（tsdoc.org 官方案例）用 `@microsoft/tsdoc` 参考解析器统一 | AD-8 |
| 新增包文档站缺失 | entryPoints 配置漂移（忘加） | 库用自动发现（exports/main）；应用用 `--entryPointStrategy Expand`；CI 校验 | AD-8 |
| 每 PR 出现巨型文档 diff | 文档站产物提交进仓库 | 站点产物不提交（CI 部署）；仅 `.api.md` API 报告提交 | AD-8 |
| 升级后用户编译错误/运行时断裂 | 直接删除，不走废弃流程 | 走废弃生命周期三阶段 | AD-9 |
| `@deprecated` 三个字孤零零 | 废弃标注当义务动作而非服务动作 | 原因 + 替代 + 迁移指引 + 移除版本 | AD-9 |
| 新用户照 tutorial 写出废弃调用 | 废弃只改了 reference 层 | 废弃当天全站 grep 扫描 | AD-10 |
| 机械替换旧 API 后出微妙 bug | 迁移指南只有映射无行为差异列 | 对照表 + 差异列（默认值/错误处理/时序） | AD-11 |
| `Error: invalid input` 无法定位 | 错误信息写给作者自己而非排障者 | 字段 + 规则 + 实际值 | AD-6 |
| 限流错误与参数错误混排，读者盲目 retry | 未按处理策略分类 | 可重试性标注（yes/no/needs-action） | AD-6 |
| 404 对应多个 body code，语义不明 | HTTP 状态码与业务错误码双体系未分层 | 显式映射表：状态码 × code × 条件 × 处理 | AD-6 |
| spec 与代码漂移，客户端按旧契约生成 | spec 与代码双真源手写 | 单一真源 + CI 双向 diff 校验 | AD-13 |
| spec 每端点只有 200/201 响应 | 错误响应缺失 | 非 200 响应必入 spec | AD-13 / AD-6 |
| 注释 YAML 的 User schema 与 TS interface 双写漂移 | 注释路线类型双份维护 | 类型推导转换层，或转装饰器路线 | AD-13 / AD-1 |
| 文档花大量篇幅解释布尔魔法参数 | 设计坏味，文档在打补丁 | 上报设计问题（ADR/issue） | AD-12 |
| 生成 API 文档参数名 `options.retry`，实际叫 `options.retries` | 参数编造（先验当事实） | 凡具体参数名一律视为需源验证 | AD-2 |

### Top 坑 1：签名幻觉（最高危）

- 症状：文档描述的 API 与真实 API 不符——参数多/少/名字不同/顺序不同；输出以同样确定的口吻。
- 根因：生成时未读源码，用「同类库的典型形态」补全；API 名字空间高度重复（每个 HTTP 库都有 get/post），记忆重叠即串包。
- 代码对照：

```ts
// ✗ 无源生成完整 reference（参数名是编的）
/** @param options.retry - 重试次数 */
// ✓ 有源逐项生成；无源只给结构模板
/** @param options.（待填：参数名以 src/api/client.ts 为准） */
```

- 修复：AI 文档工作流硬前提 = 源在手；无源产出结构模板 + 待填标注。[AD-2]

### Top 坑 2：@example 漂移

- 症状：示例调用 `getClient()`，但该 API 三个版本前已改名——TypeDoc 照渲染，无任何告警。
- 根因：TSDoc 注释块内代码不被编译器检查；示例与实现独立演化。
- 代码对照：

```ts
// ✗ 示例虚构 import 与上下文，调用已不存在的方法
// import { getClient } from 'my-lib';  // v3 已改名 createClient
// ✓ 单 API 最小调用，import 真实存在
// import { createClient } from 'my-lib';
```

- 修复：示例尽量薄（只调该 API 一层）；工具链（如 ApiExtractor 类提取管线）对示例做编译验证；生成后与导出清单比对。[AD-7]、[AD-2]

## API 速查表

### TSDoc 官方标签全表

清单逐项转录自 ingest 记录（tsdoc.org 首页 + 标签导航全表，记录计数 24 标签）[官方文档](https://tsdoc.org)：

| 标签 | 用途 | 易错点 |
|---|---|---|
| @param | 参数的类型外语义（约束/单位/默认行为） | 手写 `{type}` 与 TS 重复且漂移；描述复读参数名 |
| @typeParam | 泛型参数说明 | 与 @param 混用（泛型参数须用 @typeParam） |
| @returns | 返回值语义（不是重复类型） | 复杂返回只写「结果对象」——字段语义应展开进 @remarks |
| @remarks | 长说明/边界条件主体 | 与摘要行重复；首句之后的内容误写进摘要行 |
| @defaultValue | 参数/属性默认值 | 拼写成 JSDoc 的 `@default` 是混用错误；无源猜默认值 |
| @deprecated | 废弃标注 | 裸标注（无原因/替代/移除版本）违反 [AD-9] |
| @example | 示例代码块 | 内容不被编译器校验——漂移无告警 |
| @see | 参见引用（块标签） | 误以为非标准「需统一到 {@link}」——两者皆标准，分工不同 |
| {@link} | 行内链接（inline 标签） | link 幻觉——指向不存在的导出 |
| @inheritDoc | 继承上游注释 | 上游无注释时渲染为空 |
| @privateRemarks | 内部备注（不进公开文档） | 内部语义误写进公开摘要 |
| @packageDocumentation | 包级入口文档 | 放在非入口文件不生效 |
| @throws | 抛错条件 | 只写 happy path 漏 @throws；Promise 漏 reject 路径 |
| @eventProperty | 事件属性标注 | 与普通属性说明混写 |
| @decorator | 装饰器相关标注 | —— |
| @label | 声明可被 {@link} 引用的标签名 | —— |
| @alpha | 发布阶段：alpha | 与 @beta/@experimental 阶段语义混用 |
| @beta | 发布阶段：beta（预览，可能变更） | 同上 |
| @experimental | 发布阶段：experimental | 同上 |
| @internal | 内部 API（过滤出公开文档） | 未标 → 内部 API 泄露；跨工具解析歧义（tsdoc.org 官方案例） |
| @override | 覆写基类成员 | —— |
| @public | 显式公开 | —— |
| @readonly | 只读标注 | 与 TS `readonly` 关键字语义分工混淆 |
| @sealed | 密封（不允许子类扩展） | —— |
| @virtual | 允许子类覆写 | 与 @override 方向混淆（virtual=可覆写，override=已覆写） |

### TSDoc ↔ JSDoc 关键标签对照

| 语义 | TSDoc | JSDoc | 注意 |
|---|---|---|---|
| 默认值 | `@defaultValue` | `@default`（同义 `@defaultvalue`） | 两体系拼写不同，混用即错误 [官方文档](https://tsdoc.org) / [官方文档](https://jsdoc.app) |
| 参数 | `@param name`（不写类型） | `@param {type} name` | TS 项目手写 `{type}` 双份漂移 |
| 类型标注 | 不需要（TS 类型系统承担） | `@type` / `@typedef` | 「JSDoc 标签多为 JS 类型标注服务」——TSDoc 官方定性 [官方文档](https://tsdoc.org) |
| 类/构造 | 不需要 | `@class` / `@constructor` | 运行时语义标签在 TS 中无意义 |
| 参见 | `@see`（块标签） | `@see` | 两者皆标准 |
| 行内链接 | `{@link}` | `{@link}` | 两者皆标准；与 @see 分工不同（inline vs 块） |
| 规模对比 | 24 标签（ingest 记录） | 60+ block 标签 + 2 inline 标签 | JSDoc 语法「inferred from behavior, not rigorously specified」[官方文档](https://jsdoc.app) / [官方文档](https://tsdoc.org) |

### TypeDoc 关键配置/CLI

| 项 | 值/说明 | 易错点 |
|---|---|---|
| 安装 | `npm i -D typedoc` | —— |
| entryPoints 发现 | 库：自动发现（package.json exports/main）或显式传参 | 新增包忘加入口点 → 文档缺失 |
| `--entryPointStrategy Expand` | 应用（非库）场景：逐文件展开生成文档 | 库场景不需要 Expand；应用场景不用则入口发现失效 |
| 输出格式 | HTML / JSON | 站点产物不提交仓库（[AD-8]） |
| TSDoc 校验 | `@microsoft/tsdoc` 参考解析器 + Playground；eslint-plugin-tsdoc（lint 集成在位）[官方文档](https://tsdoc.org) | 只跑生成器不做 lint——方言标签静默进站 |

以上仅列 ingest 有文档佐证的项；其余配置键名以 typedoc.org 为准，不得凭记忆虚构（elicited/03 自我质询 3）。

## 版本注意

仅记录萃取/ingest 素材中有文档佐证或明确标注的版本相关事实；无佐证的具体版本号一律不写。

- TSDoc 规范基线：tsdoc.org 首页 + 标签导航全表（ingest 2026-11-17）——24 标签清单与三设计要求以该页为准 [官方文档](https://tsdoc.org)。
- TSDoc 语法版本敏感度低（规范稳定）[模型经验]（elicited/01 边界轮）。
- JSDoc 现状：jsdoc.app 全索引 60+ block 标签 + 2 inline 标签 [官方文档](https://jsdoc.app)；TSDoc 官方对 JSDoc 语法的定性：「inferred from behavior, not rigorously specified」[官方文档](https://tsdoc.org)。
- OpenAPI：3.0.x 与 3.1 混用是坑点 [模型经验]（elicited/08）；两版本生态取舍无文档佐证——生成版本建议时保守。
- ESDoc 维护状态：ingest 未解决（jsdoc.app 不涉及）——保持待考，不作为事实输出。
- NestJS/tsoa/swagger-jsdoc 装饰器与注释语法：未 ingest 框架文档——版本敏感区，使用时必须锚定框架官方文档。
- SemVer 2.0.0（第 2 轮补锚）：deprecate→MUST bump MINOR（规则 7）；完全移除只能在其后的新 major，且此前至少一个含 deprecation 的 minor release（FAQ）；版本一经发布内容 MUST NOT 修改（规则 3）；`v1.2.3` 的 `v` 前缀不是语义化版本组成部分（规则 9）。[官方文档](https://semver.org/spec/v2.0.0.html)

## 与其他子领域的集成要点

- **code-comment**（`kb/code-comment.md`）：函数级 docstring 纪律与 TSDoc 摘要行规则同源——[AD-1] 自文档化层级（类型>命名>注释>文档）适用于一切注释场景；注释密度/何时该写注释的判据在 code-comment 展开。
- **doc-quality**（`kb/doc-quality.md`）：[AD-7] 示例最小可运行与 doc-quality 的示例规范互为约束——示例漂移治理、示例错误处理展示（至少一种典型错误处理或显式声明省略）由 doc-quality 细化。
- **ai-doc-verification**（`kb/ai-doc-verification.md`）：[AD-2] 无源不生成的执行层——生成后签名比对、{@link} 目标存在性校验、示例编译验证等流水线在该子域展开。
- **laws.md**：[AD-1]、[AD-2] 已标 [GLOBAL] 候选，阶段 3 与其他子领域同源法则（如 DT-12 编造零容忍）查重合并后入全局宪法。
- **ai-mistakes.md**：elicited/07 的 AI 系统性错误 Top 15（签名幻觉/参数编造/错误码虚构/示例漂移/注释复读等）汇入 ai-mistakes 总集的 api-doc-gen 分节。

## 来源索引

官方文档（ingest 抓取成功，2026-11-17）：

- https://tsdoc.org —— TSDoc 24 标签全表、三设计要求（Extensibility/Interoperability/Familiar syntax）、工具生态名单（TypeDoc / DocFX / API Extractor / ESLint / VS Code）、`@microsoft/tsdoc` 参考解析器 + Playground、eslint-plugin-tsdoc、@internal 解析歧义官方案例
- https://typedoc.org —— Quick Start：HTML/JSON 输出、入口点发现（package.json exports/main / 显式传参）、`--entryPointStrategy Expand` 适用场景
- https://jsdoc.app —— 全索引：60+ block 标签 + 2 inline 标签、`@default`（synonym `@defaultvalue`）

模型经验（elicited 萃取文件，未经逐条文档验证）：

- elicited/01-tsdoc-annotation.md —— TSDoc 标注规范、JSDoc 时代语法问题 Top 8
- elicited/02-api-reference-anatomy.md —— 五要素结构与完整性判据（归纳共识：Stripe/Node/MDN 风格归纳，无单一规范来源）
- elicited/03-toolchain-config.md —— 工具链选型与治理缺陷
- elicited/04-signature-design-impact.md —— 签名设计 ↔ 文档质量（工程共识归纳）
- elicited/05-error-codes-documentation.md —— 错误文档三件套
- elicited/06-deprecation-lifecycle.md —— 废弃生命周期与三承诺
- elicited/07-ai-api-doc-mistakes.md —— AI 系统性错误 Top 15（无上游文档对应，本知识库特有贡献层）
- elicited/08-openapi-spec-generation.md —— OpenAPI 两条路线（结构层可靠；装饰器/注释语法层未经文档验证）
- elicited/09-laws.md —— AD-1 ~ AD-13 法则化原文

### 第 2 轮新增（SemVer 2.0.0 官方规格）

- https://semver.org/spec/v2.0.0.html — SemVer 2.0.0 规格全文：MAJOR/MINOR/PATCH 语义全表、规则 3（版本一经发布内容不可修改）、规则 7（deprecate→MUST bump MINOR）、规则 8（breaking→MAJOR）、FAQ 废弃处理（移除前至少一个含 deprecation 的 minor release）、`v` 前缀非版本组成部分（CC BY 3.0）。[官方文档]
- 未经文档验证声明（更新）：五要素结构为归纳共识；NestJS/tsoa/swagger-jsdoc 语法细节（框架文档未 ingest，lastReviewed: 2026-11-18，维持降级）；ESDoc 维护状态待考（lastReviewed: 2026-11-18，维持待考）。ApiExtractor 配置细节项于第 7 轮补锚解决（api-extractor.com 三页，见冲突消解 #8），从本清单移除。

### 第 7 轮新增（refresh 补锚：API Extractor 官方站）

- https://api-extractor.com/ — API Extractor 官方站（Rush Stack，微软）：TypeScript 库包工具定位、build time 由工具链调用 + TS 编译器引擎、六问题场景（意外破坏/漏导出/意外导出/alpha-beta 毕业/*.d.ts rollup/在线文档）、五功能（检测导出 API surface/捕获契约为简明报告/常见错误告警/生成按 release type 修剪的 rollup/输出可移植 API 文档格式）。[官方文档]
- https://api-extractor.com/pages/overview/intro/ — 三输出官方定义：API Report（API review workflow 基础）/ .d.ts Rollups（类比 Webpack 打包）/ API Documentation（doc model JSON；api-documenter 伴生工具可生成 API reference 站或作自定义管线输入）。[官方文档]
- https://api-extractor.com/pages/overview/demo_api_report/ — API 报告实践：默认文件名 `etc/<package>.api.md`（API Extractor 7 前用 .api.ts 后缀，因被工具误判为真 TS 代码而改）；报告文件由 Git 追踪、变更须随 PR 提交（漏提交则 PR validation 失败）；可定义「.api.md 变更需 stakeholder 审批」的 PR 分支策略；diff 仅在显著契约变更时发生（函数签名/导出声明/文档有无（`// (undocumented)`）/release tag——忽略函数体与句子级文档改动）；@internal 定义默认监控（@preapproved 可抑制）。[官方文档]

## 冲突消解记录

| # | 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|---|
| 1 | 「TSDoc 推荐 {@link}，@see 需统一到 {@link}」（elicited/01 自我质询 4） | `@see` 是 TSDoc 标准块标签，`{@link}` 是标准 inline 标签——两者分工不同，皆标准 [官方文档](https://tsdoc.org)（ingest 修正） | 不写「需统一到 {@link}」；@see 用于参见引用（块级），{@link} 用于行内链接，按位置选用 |
| 2 | @defaultValue vs @default 拼写待验证（elicited/01 边界轮） | TSDoc 用 `@defaultValue`；JSDoc 用 `@default`（synonym `@defaultvalue`）[官方文档](https://tsdoc.org) / [官方文档](https://jsdoc.app) | 两体系拼写不同；TSDoc 注释内写 `@default` 定性为混用错误（速查表登记） |
| 3 | TSDoc 标签全集记忆约 10 个，不得凭记忆列举（elicited/01 自我质询 5、边界轮） | tsdoc.org 官方全表（ingest 记录 24 标签）[官方文档](https://tsdoc.org) | 以官方全表为准（见 API 速查表），逐一校准 @internal/@sealed/@virtual 等语义 |
| 4 | TSDoc↔JSDoc 兼容矩阵不确定（elicited/01 边界轮） | TSDoc 官方定性：JSDoc 语法「inferred from behavior, not rigorously specified」，且多数标签为 JS 类型标注服务（TS 不需要）[官方文档](https://tsdoc.org) | 部分解决——官方定性背书「TS 项目弃 JSDoc 类型标注类标签」论点；逐标签兼容矩阵仍无官方表，不编造 |
| 5 | entryPoints 配置漂移是推测的治理痛点（elicited/03 缺陷 7） | typedoc.org Quick Start 确认：入口点自动发现（exports/main）+ `--entryPointStrategy Expand` 用于应用逐文件文档 [官方文档](https://typedoc.org) | 工具现实确认；速查表与场景 5 按官方口径表述 |
| 6 | ESDoc「已不维护」（置信度中，elicited/03 广度轮） | ingest 未解决（jsdoc.app 不涉及） | 不作为事实输出，保持待考；ESDoc 仅作历史提法 |
| 7 | 宽限期长度无官方规定，「至少一个 major 周期」是社区惯例（elicited/06，semver.org 未 ingest 待验证） | 第 2 轮补抓 [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html)：规则 7 deprecate→MUST bump MINOR；官方 FAQ——完全移除只能发生在其后的新 major，且此前至少有一个含 deprecation 的 minor release | 最低结构约束官方化（先含 deprecation 的 minor、后移除的 major）；时长数字仍无官方规定，维持经验判断；场景 4 边界条件按官方口径重写 |
| 8 | ApiExtractor「.api.md 报告提交（diff 即 API 审查面）」未经官方验证（elicited/03；第 2 轮登记「api-extractor.com 未 ingest」挂账） | 第 7 轮补抓 [api-extractor.com](https://api-extractor.com/pages/overview/demo_api_report/)：报告默认名 `etc/<package>.api.md`（API Extractor 7 前用 .api.ts）；报告文件由 Git 追踪、变更须随 PR 提交（漏提交则 PR validation 失败）；官方建议「.api.md 变更需 stakeholder 审批」的 PR 分支策略；diff 仅在显著契约变更时发生 | [AD-8] 溯源升级「官方锚 + 模型经验」；概念表 ApiExtractor 行按官方三输出重写；「配置细节未验证」项从未经文档验证声明移除 |
