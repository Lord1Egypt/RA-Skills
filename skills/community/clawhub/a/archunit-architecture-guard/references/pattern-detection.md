# 架构模式识别参考

如何从结构证据识别一个 Java/Kotlin 代码库的架构。使用下面的信号表，给每个模式打分，给出带排名和置信度的结论。识别出混合或不一致的结果很常见，也是有效的。

## 目录
- 如何打分
- 分层 / MVC
- DDD（战术）+ 分层
- 六边形 / 端口与适配器
- 整洁架构
- 按功能分包 / 模块化单体
- MVVM（Android / 客户端）
- 消歧速查表

## 如何打分

对每个模式，统计它有多少信号出现、强度多大。只有当某模式的**结构性**信号（包布局、依赖方向）出现时，它才算强匹配，而不是只看命名。**命名是弱证据，依赖方向才是强证据。**

报告示例："主导：**分层/MVC**（高置信度）—— 按技术角色分包，controller→service→repository，有 Spring 构造型注解。次要：`billing` 模块向**按功能分包**漂移。领域层*未*做框架隔离，因此这不是 DDD/六边形。"

## 分层 / MVC

Java 后端默认形态。包按技术角色命名；自上而下。

信号：
- 顶层（或每个功能下）包：`controller`/`web`/`api`、`service`、`repository`/`dao`、`model`/`entity`/`dto`。
- Spring 构造型注解：`@RestController`/`@Controller`、`@Service`、`@Repository`。
- 依赖方向：controller → service → repository；下层不导入上层。
- 没有刻意做框架隔离的"领域"核心。

要生成的守护规则：用探测到的层调用 `layeredArchitecture()`；controller 不被任何人访问；repository 只被 service 访问；每层的命名约定。

## DDD（战术）+ 分层

领域驱动设计的战术模式，通常叠在分层或六边形之上。

信号：
- 一个 `domain` 包，含 `aggregate`/`entity`/`valueobject`(`vo`)/`domainservice`/`event`/`repository`（这里是*接口*，不是 JPA 实现）。
- `application`（用例/应用服务）和 `infrastructure`（技术实现）。
- 仓储*接口*在 `domain`；*实现*在 `infrastructure`。
- 意图让 `domain` 不含 Spring/JPA（常被违反——这是阶段三的发现）。

守护规则：`onionArchitecture()`（领域模型/服务、应用、适配器），外加"`..domain..` 内无框架导入"，外加"领域不向外依赖"。

## 六边形 / 端口与适配器

一个核心被端口（接口）和适配器（实现）包围。驱动适配器通过输入端口调入核心；核心通过输出端口（由被驱动适配器实现）调出。

信号：
- 包名 `port`/`ports`（常见 `port.in`、`port.out`）与 `adapter`/`adapters`（`adapter.web`、`adapter.persistence`、`adapter.messaging`）。
- 一个 `domain`/`application` 核心，不导入任何 `adapter`。
- 接口在 `port`，实现在 `adapter`。

守护规则：用 `onionArchitecture()` 映射核心 + 适配器；"适配器依赖 application/domain，绝不反向"；"端口是接口"。

## 整洁架构

同心圆；依赖只能向内。常带 `entities`、`usecases`、`interfaceadapters`/`adapters`、`frameworks`/`infrastructure` 等命名。

信号：
- 包：`entity`/`entities`/`domain`、`usecase`/`usecases`/`interactor`、`adapter`/`interfaceadapter`/`presenter`/`gateway`、`framework`/`infrastructure`/`config`。
- 严格的向内依赖规则；用例交互器编排实体；展示器/网关在外层。

守护规则：`onionArchitecture()`，或显式分层规则按 entities → usecases → adapters → frameworks 排列，每个内层只能被相邻外层访问，绝不反向。

## 按功能分包 / 模块化单体

顶层包是业务能力而非技术角色。每个功能拥有自己的分层。

信号：
- 顶层包读起来像业务领域：`orders`、`billing`、`catalog`、`shipping`、`customer`——而不是 `controller`/`service`。
- 每个功能内部可能仍有 `controller`/`service`/`repository`，或扁平切片。
- 可选的 `shared`/`common` 包放横切代码。
- 有时显式区分模块 API 包（`orders.api`）与内部实现（`orders.internal`）。

守护规则：用 `slices().matching("<base>.(*)..")` 禁止一个功能伸进另一个功能的内部；只允许访问对方发布的 API 包；跨功能通信走事件/接口。

## MVVM（Android / 客户端）

主要用于 Android。若在服务端探测到它，请再三确认——那里很少见。

信号：
- `com.android.*` 插件 / `AndroidManifest.xml`；`view`/`ui`、`viewmodel`、`model`/`repository`。
- `LiveData`、`StateFlow`/`MutableStateFlow`、`ViewModel`/`AndroidViewModel`、DataBinding。

守护规则：View 层可依赖 ViewModel，但不可直接依赖 Model/Repository；ViewModel 不得导入 Android UI 类型（`android.view.*`、`android.widget.*`、`Activity`、`Fragment`），以保持可测试；Model/Repository 不得依赖 ViewModel 或 View。

## 消歧速查表

- 顶层有 `controller`/`service`/`repository`、无隔离领域 → **分层/MVC**。
- `domain` + `application` + `infrastructure`，仓储接口在 domain → **DDD + 分层**。
- 有 `port` + `adapter` 包 → **六边形**。
- 有 `entities` + `usecases`、同心圆命名 → **整洁架构**。
- 顶层包是业务名词 → **按功能分包**。
- 有 `viewmodel` + Android + 响应式状态 → **MVVM**。
- 信号混杂 → 报**混合/不一致**，选主导模式作守护规则、把偏离项列为阶段三坏味道。这是最诚实、也最常见的真实结果。
