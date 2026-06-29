# 架构坏味道目录

每条坏味道包含：检测方式、为何要紧、修复方案、以及守护它的 ArchUnit 规则。报告中按严重度排序。始终允许"违规"可能是有意为之——对边界情况表述为"先确认意图，再决定修复还是冻结"。

## 1. 包循环（高严重度）

**检测：** 包 A 导入 B，B（传递地）又导入 A。用 `slices().matching("<base>.(*)..").should().beFreeOfCycles()` 找，或看扫描脚本的循环输出。

**为何要紧：** 有循环就意味着这些包无法被独立理解、测试、构建或抽取。它是腐烂最明显的信号，也是 AI 改动最容易引入的问题。

**修复：** 打破循环：(a) 抽取一个双方都依赖的共享抽象，(b) 用接口反转其中一个依赖（依赖倒置），或 (c) 把共享类型移到 `common` 包。当一方明显是"更底层"时，优先用反转。

**守护：** `freeze(slices().matching("<base>.(*)..").should().beFreeOfCycles())`。

## 2. 越层 / 依赖方向违规（高严重度）

**检测：** controller 直接导入 repository/DAO（跳过 service）；下层导入上层；在六边形/整洁架构中，内层导入外层。

**为何要紧：** 破坏分层契约，责任扩散，上层无法被替换，分层存在的意义被瓦解。

**修复：** 让访问经过应有的层；引入一个 service 方法；对"内层→外层"，用内层拥有的接口做反转。

**守护：** `layeredArchitecture()...whereLayer("Repository").mayOnlyBeAccessedByLayers("Service")`，或 `noClasses().that().resideInAPackage("..controller..").should().dependOnClassesThat().resideInAPackage("..repository..")`。

## 3. 框架泄漏进领域层（对 DDD/六边形/整洁架构为高严重度）

**检测：** `..domain..` 的类导入 `org.springframework..`、`jakarta.persistence..` / `javax.persistence..`，或被标注 `@Entity`、`@Service`、`@Component`。

**为何要紧：** 把业务规则耦合到框架，阻断快速单元测试，并抹掉领域核心存在的意义。AI 特别喜欢"贴心地"给领域类加上 `@Service`/`@Entity`。

**修复：** 让领域保持纯粹；框架注解放到 infrastructure/adapter 类上；在持久化适配器里做领域对象与 JPA 实体的相互映射。

**守护：**
```
noClasses().that().resideInAPackage("..domain..")
    .should().dependOnClassesThat().resideInAnyPackage("org.springframework..", "jakarta.persistence..", "javax.persistence..")
```
冻结它，使存量泄漏被纳入基线、但不允许任何新增。

> 注意：这条只在工程**意图保持领域无框架**（DDD/六边形/整洁）时才算坏味道。在普通分层/MVC 工程里，`domain` 包里的 JPA `@Entity` 是常规写法，**不算坏味道**——但 `@Component`（把实体当 Bean）和实体外泄仍然算。

## 4. 持久化实体泄漏到 Web 层（中严重度）

**检测：** JPA `@Entity` 类型被 `..controller..`/`..web..` 当作请求/响应体引用。

**为何要紧：** 把 API 契约绑死到数据库 schema；schema 一改就变成破坏性 API 变更；还有懒加载与序列化风险。

**修复：** 在 Web 边界引入 DTO；在 service 或专门的 mapper 里做实体↔DTO 映射。

**守护：**
```
noClasses().that().resideInAPackage("..controller..")
    .should().dependOnClassesThat().areAnnotatedWith(jakarta.persistence.Entity.class)
```
（若注解不可靠，可改用 `..entity..` 包匹配。）

## 5. 放置 / 命名不一致（中严重度——但它是引入守护测试最有力的理由）

**检测：** 一部分 controller 在 `web`、另一部分在 `controller`；service 类不带 `Service` 后缀；跨模块约定混乱。

**为何要紧：** 这*就是* AI 造成的漂移。每个 diff 都挑一个"看似合理但各不相同"的约定，直到结构无法阅读。尽早锁定约定，成本极低、价值很高。

**修复：** 选定一个约定，写下来，强制执行。

**守护：**
```
classes().that().resideInAPackage("..controller..").should().haveSimpleNameEndingWith("Controller");
classes().that().areAnnotatedWith(RestController.class).should().resideInAPackage("..controller..");
```

## 6. 上帝包 / 枢纽依赖（中严重度）

**检测：** 一个包几乎被所有东西导入，又几乎导入所有东西（超出合理的、只被依赖的 `common`/`util`）。

**为何要紧：** 它会变成变更磁铁和循环工厂。

**修复：** 按职责拆分；让共享代码保持无依赖（它可以被依赖，但不应依赖功能包）。

**守护：** `noClasses().that().resideInAPackage("..common..").should().dependOnClassesThat().resideInAPackage("<base>..")`（common 不依赖任何内部），外加无循环。

## 7. 跨功能访问内部实现（中严重度——仅按功能分包）

**检测：** 功能 `orders` 直接导入 `billing.internal` 的类型。

**为何要紧：** 摧毁模块边界；功能无法再独立演进或抽取。

**修复：** 只依赖对方发布的 API 包，或通过事件/接口通信。

**守护：**
```
slices().matching("<base>.(*)..").namingSlices("$1").should().notDependOnEachOther()
```
或用显式 `noClasses()` 规则只放行 `api` 子包。

## 8. 生产代码里的测试/工具捷径（低-中严重度）

**检测：** 生产代码依赖仅供测试的辅助类；在以构造注入为约定的工程里用字段注入；以 logger 为标准时却用 `System.out`。

**为何要紧：** 单看每条都很小，但它们标志着纪律在松动。

**守护（仅当团队明显遵循该约定时）：**
```
noFields().should().beAnnotatedWith(Autowired.class);   // 强制构造注入
noClasses().should().accessStandardStreams();            // 禁用 System.out/err
```

## 报告中的严重度指南

- **高：** 包循环、依赖方向违规、领域层框架泄漏。它们破坏架构的保证。
- **中：** 实体泄漏到 Web、命名/放置不一致、上帝包、跨功能访问。
- **低：** 风格约定（注入方式、日志）——仅在明显已采纳时才强制。

把每条生成的守护规则映射回它防范的坏味道，让将来的构建失败可自解释。
