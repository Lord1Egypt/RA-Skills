---
name: archunit-architecture-guard
description: 扫描既有 Java/Kotlin 工程，识别其架构模式（分层/MVC、DDD、六边形/端口适配器、整洁架构、按功能分包/模块化单体、或 Android MVVM），报告架构坏味道并给出具体修复指导，再生成 ArchUnit 守护测试把"应有的架构"固化下来，使后续（通常是 AI 生成的）代码无法让它腐烂。当用户想要"守护/约束/保护/测试"某个 Java/Kotlin 工程的架构、提到 ArchUnit、架构适应度函数（architecture fitness function）、依赖规则、越层、包循环、架构腐烂（architecture erosion/rot），或想阻止 AI 生成的代码破坏既有设计时，使用本 Skill。当用户问"这个工程用的什么架构""我的架构干净吗"，或想给一个被 AI 反复修改的代码库加护栏时，也应触发。
---

# ArchUnit 架构守护（Architecture Guard）

## 何时使用本 Skill

> 说明：真正生效的触发条件写在文件顶部 frontmatter 的 `description` 字段里（那是 Claude 判断是否加载本 Skill 的唯一依据）。本小节是给维护者看的人类可读版，二者应保持一致；改了触发条件请同步更新 `description`。

**适用：**
- 用户想给某个 Java/Kotlin 工程的架构加"护栏"——守护、约束、保护、测试架构。
- 用户提到 ArchUnit、架构适应度函数（architecture fitness function）、依赖规则、越层、包循环、架构腐烂（architecture erosion/rot）。
- 用户想阻止 AI 生成的代码破坏既有架构设计，或想给一个被 AI 反复修改的代码库加约束。
- 用户问"这个工程用的什么架构""我的架构干净吗""帮我看看依赖有没有乱"。
- 用户想生成 / 编写架构测试、固化分层或模块边界。

**不适用：**
- 纯粹的功能性单元测试 / 集成测试（本 Skill 只管架构约束，不管业务逻辑正确性）。
- 运行时性能、安全漏洞扫描这类与"结构依赖"无关的问题。
- 非 JVM 工程（ArchUnit 只分析 Java 字节码；它能覆盖 Kotlin、Scala 等编译到 JVM 的语言，但不适用于 Go、Python、前端 JS/TS 等）。

## 目的与核心思想

AI 生成的代码会漂移。每一次单独的改动看起来都合理，但累积许多次之后，controller 开始直接调 repository，领域模型导入了 Spring，包之间冒出了循环。代码库就这样一次一个"看似合理的 diff"地腐烂下去。

本 Skill 把工程**应有的架构**翻译成**可执行测试**，使用 [ArchUnit](https://github.com/TNG/ArchUnit)，让新代码一旦破坏规则，构建立即失败。工作流分四个阶段：

1. **扫描** 真实的包结构与依赖结构。
2. **识别** 架构模式（基于证据）。
3. **诊断** 坏味道并给出修复指导。
4. **生成** ArchUnit 守护测试（默认：*冻结存量违规，只拦新增*）。

**锚定原则——守护的是"回归"，不是"历史"。** 用户几乎从不希望构建在第一天就因为历史债务而失败。ArchUnit 的 `freeze(...)` 会把当前违规记成基线，只对**新增**违规报错。这正是"阻止 AI 把架构改得更差"这个场景的命门。默认采用冻结；把严格模式作为可选项提供。

**两种规则推导方式**——必须明确说明你在用哪种：
- **描述性（descriptive）** 规则：固化*现状*的架构（适合冻结 + 锁定团队已经在遵循的约定）。
- **规定性（prescriptive）** 规则：固化*应有*的架构（所识别模式的标准形态）。对依赖方向、隔离这类规则用规定性，然后 `freeze` 它们，使存量例外不阻塞构建、但不允许任何新增。

务必告诉用户哪些规则是描述性、哪些是规定性，让他们清楚自己在约束什么。

## 输出语言

所有面向用户的分析内容（架构报告、坏味道发现、修复指导）使用**用户在对话中所用的语言**。Java 标识符、包名、代码注释保持英文。生成的测试代码本身与语言无关。

---

## 阶段一 —— 扫描结构

目标：在做任何判断之前先建立一份客观的工程地图。不要凭单个类去猜，要收集证据。

1. **定位源码根目录与构建文件。** 找到 `pom.xml` / `build.gradle(.kts)` / `settings.gradle`，以及 `src/main/java`（和 `src/main/kotlin`）。注意是否为多模块结构。
2. **探测构建工具与测试框架**（这决定生成的测试形态）：
   - 从构建文件判断 Maven 还是 Gradle。
   - 从既有测试依赖判断 JUnit 5（`org.junit.jupiter`）还是 JUnit 4（`junit:junit`）。
   - 是否存在 Spring Boot / Spring、JPA/Hibernate、Android（`com.android.*`、`AndroidManifest.xml`）。
3. **盘点包结构。** 列出每个源码根下的包树。识别根包/基础包（公共前缀）。记录其下的顶层子包。
4. **构建包依赖图。** 对每个包，统计它导入了哪些*内部*包。这是最重要的产物——它揭示依赖方向、循环和分层。用扫描脚本可靠地生成，而不是肉眼看：运行 `python references/scan_packages.py <源码根> --base <基础包>`（输出格式见该脚本头部说明）。若脚本无法运行，再退而用 grep 抓 `import` 语句推导同样的依赖图，但优先用脚本。
5. **探测角色信号**：按包名和注解识别角色。统计包名中出现的角色关键字频率：`controller`、`web`、`api`、`resource`、`endpoint`、`service`、`usecase`、`application`、`domain`、`model`、`entity`、`aggregate`、`vo`、`valueobject`、`repository`、`dao`、`persistence`、`mapper`、`infrastructure`、`infra`、`adapter`、`port`、`config`、`dto`、`client`、`gateway`、`viewmodel`、`view`。同时统计注解：`@RestController`/`@Controller`、`@Service`、`@Repository`、`@Component`、`@Entity`、`@Configuration`。

把这些都记成客观事实，由阶段二来解读。

---

## 阶段二 —— 识别架构模式

把证据匹配到模式上。输出一个**带排名**的识别结果，附置信度和具体证据——绝不只给一个光秃秃的标签。报出*混合*或*不一致*的结论很常见也完全合理（例如"分层为主，其中两个模块正向按功能分包漂移"）。

完整的信号表和判定指南见 `references/pattern-detection.md`。主要模式概要：

- **分层 / MVC** —— 按技术角色分包（`controller` → `service` → `repository`），有 Spring 构造型注解，自上而下。Java 后端最常见的形态。
- **DDD（战术）+ 分层** —— `domain` 包含 `aggregate`/`entity`/`valueobject`/`domainservice`，外加 `application` 与 `infrastructure`。领域层意在保持无框架依赖。
- **六边形 / 端口与适配器** —— domain/application 核心，外加 `port`（接口）和 `adapter`（实现：web、persistence、messaging）。适配器向内依赖。
- **整洁架构** —— 同心圆：entities ⊂ usecases ⊂ interface-adapters ⊂ frameworks；依赖只能向内。
- **按功能分包 / 模块化单体** —— 顶层包是业务能力（`orders`、`billing`、`catalog`），每个功能内部有自己的分层；功能之间不应依赖彼此的内部实现。
- **MVVM（Android/客户端）** —— `view`、`viewmodel`、`model`/`repository`，配合 `LiveData`/`StateFlow`/DataBinding。View ↔ ViewModel ↔ Model；View 不得直接碰 Model，ViewModel 不得引用 Android 的 `View`/`Activity` 等 UI 类型。提醒用户 MVVM 主要是客户端（Android）模式——若在服务端看到它，要再三确认。

证据混杂时直说，并选取*主导*模式作为守护规则的基础，把偏离项列为阶段三的候选坏味道。

---

## 阶段三 —— 诊断坏味道并给出修复指导

每条发现都报告：**是什么**（坏味道）、**在哪**（包/类）、**为何要紧**（具体风险）、**怎么修**（具体重构）。按严重度排序。完整目录和修复模式见 `references/smell-catalog.md`。高价值检查项：

- **包循环** —— 几乎总值得标记；它阻断独立推理与测试。
- **越层 / 依赖方向违规** —— controller → repository 跳过 service；domain → infrastructure；内层依赖外层。
- **框架泄漏进领域层** —— `domain` 内部出现 Spring/JPA 注解或导入（破坏 DDD/六边形的隔离，把业务规则耦合到框架）。
- **持久化实体泄漏到 Web 层** —— JPA `@Entity` 类型被直接当成 API 的请求/响应体，而非用 DTO。
- **放置/命名不一致** —— 一部分 controller 在 `web`、另一部分在 `controller`；这正是 AI 改动造成的漂移，也是引入守护测试最有力的理由。
- **上帝包** —— 一个所有东西都依赖的包（超出合理的共享 `common` 范畴）。

要诚实对待置信度：某个"违规"可能是有意的例外。对边界情况，表述为"先确认意图，再决定修复还是冻结"。

---

## 阶段四 —— 生成 ArchUnit 守护测试

这是最终交付物。可直接复制的规则配方、依赖坐标、JUnit 4/5 模板、冻结/存储配置见 `references/archunit-cookbook.md`。

流程：

1. **配置依赖**：按探测到的构建工具与 JUnit 版本（手册里 Maven/Gradle 都有）。提醒用户加上，不要假设已存在。
2. **为主导模式选规则集**：
   - 分层/MVC → 用探测到的层调用 `layeredArchitecture()`。
   - DDD/六边形/整洁 → `onionArchitecture()`（ArchUnit 内置），或用显式的 `noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat()...` 规则约束"只能向内"的依赖方向。
   - 按功能分包 → 用 `slices().matching(...)` 禁止跨功能访问内部实现。
   - MVVM → view/viewmodel/model 之间的方向规则，外加"viewmodel 不准出现 Android UI 类型"。
3. **无论什么模式都加上这些**：
   - 无包循环：`slices().matching("<base>.(*)..").should().beFreeOfCycles()`。
   - 与现状匹配的命名约定（例如 `..controller..` 里的类以 `Controller` 结尾）——这能极低成本地阻止放错位置。
   - 若团队明显有此约定，再禁用特定通用 API（如 `java.util.logging`、字段注入）。
4. **默认冻结。** 把依赖方向、循环、隔离这类规则包进 `freeze(...)`，使存量违规变成基线、只有新增才失败。生成 `archunit.properties` 并解释存储文件（要提交进版本库）。同时提供清晰标注的"严格模式"变体（去掉 `freeze(...)`），供想对所有违规都报错的团队使用。冻结细节见手册的冻结小节。
5. **放置测试**：`src/test/java/<base>/architecture/ArchitectureTest.java`（或按模块各放一个）。用 `@AnalyzeClasses(packages = "<base>", importOptions = ImportOption.DoNotIncludeTests.class)`。
6. **让每条规则可追溯。** 在每个 `@ArchTest` 规则上方加注释，写明它守护的是哪条坏味道/模式约束，以及它是描述性还是规定性。这样将来某次构建失败时（人或 AI）能看懂*为什么*失败。
7. **告诉用户怎么跑**（`mvn test` / `gradle test`）以及首次运行的预期（冻结会记录基线；要提交存储文件）。

当用户的工程在磁盘上时，把测试作为真实文件写出来；否则以内联代码/工件形式给出，让用户直接放进工程。

---

## 汇总 —— 报告结构

按以下顺序交付，让用户先看到推理、再看到代码：

1. **识别到的架构** —— 带排名的模式、置信度、证据（一小段 + 一张角色关键字计数小表即可）。
2. **架构地图** —— 分层/功能依赖图以及任何循环，紧凑描述。
3. **坏味道与修复** —— 按严重度排序，每条含 是什么/在哪/为何/怎么修。
4. **守护测试** —— 依赖配置、`ArchitectureTest` 类、`archunit.properties`、冻结 vs 严格的说明、运行方式。
5. **它拦住了什么** —— 一两句话把规则映射回"AI 腐烂"这个关切，让用户明白护栏确实在起作用。

行文要紧凑。代码和发现才是价值所在，不要围着它们堆评论。

## 常见陷阱（要避免）

- 不要为了"整齐"而硬编一个模式。"不一致 / 无明确模式"是一个有效且有用的结论，反而更能论证守护测试的必要性。
- 除非用户明确要严格模式，否则不要生成会让构建在历史代码上立刻失败的规则——那样测试第二天就会被删掉。要冻结。
- 不要硬编 `com.example`。处处使用真实探测到的基础包。
- 若有网络，到 Maven Central 核对 ArchUnit 版本；手册里的版本号可能已过时。提醒用户确认最新版。
- 多模块工程要按模块限定 `@AnalyzeClasses` 范围，或用该模块的基础包；在聚合 pom 上跑单个测试往往会导入错误的类路径。
