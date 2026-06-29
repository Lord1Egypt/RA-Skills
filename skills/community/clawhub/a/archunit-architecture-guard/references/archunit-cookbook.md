# ArchUnit 配方手册

可直接复制的配方。把 `BASE`（例如 `com.acme.shop`）替换为真实探测到的基础包。若有网络，到 Maven Central 核对 ArchUnit 版本——它会随时间更新。

## 目录
- 依赖配置（Maven / Gradle，JUnit 5 / 4）
- 测试类骨架（JUnit 5 / 4）
- 分层 / MVC 规则
- DDD / 六边形 / 整洁架构规则（onion + 显式）
- 按功能分包（slices）规则
- MVVM（Android）规则
- 通用规则（循环、命名、隔离）
- 冻结：把存量违规记为基线、只拦新增
- 导入选项与多模块说明

---

## 依赖配置

ArchUnit 提供与 JUnit 集成的工件（`archunit-junit5` / `archunit-junit4`）以及一个适配任意测试运行器的纯 `archunit` 工件。优先用与 JUnit 集成的那个。

**Maven（JUnit 5）：**
```xml
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.3.0</version>
    <scope>test</scope>
</dependency>
```

**Maven（JUnit 4）：** artifactId 改用 `archunit-junit4`。

**Gradle（Kotlin DSL，JUnit 5）：**
```kotlin
testImplementation("com.tngtech.archunit:archunit-junit5:1.3.0")
```

**Gradle（Groovy DSL）：**
```groovy
testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
```

> 注意：`1.3.0` 是一个较新版本的占位，请到 Maven Central 核对当前版本并提醒用户确认。

---

## 测试类骨架

**JUnit 5**（推荐）。静态 `@ArchTest` 字段由 `archunit-junit5` 扩展自动运行。

```java
package BASE.architecture;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;
import static com.tngtech.archunit.library.Architectures.*;
import static com.tngtech.archunit.library.dependencies.SlicesRuleDefinition.slices;
import static com.tngtech.archunit.library.freeze.FreezingArchRule.freeze;

@AnalyzeClasses(packages = "BASE", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

    // 规则写在这里，形如：@ArchTest static final ArchRule someRule = ... ;
}
```

**JUnit 4：**
```java
@RunWith(ArchUnitRunner.class)   // com.tngtech.archunit.junit.ArchUnitRunner
@AnalyzeClasses(packages = "BASE", importOptions = ImportOption.DoNotIncludeTests.class)
public class ArchitectureTest {
    @ArchTest
    public static final ArchRule someRule = /* ... */;
}
```

**不依赖 JUnit 集成的写法**（任意框架）：手动导入类，在普通 `@Test` 里调用 `rule.check(...)`：
```java
JavaClasses classes = new ClassFileImporter()
        .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
        .importPackages("BASE");
someRule.check(classes);
```

---

## 分层 / MVC 规则

```java
@ArchTest
static final ArchRule layered = layeredArchitecture().consideringAllDependencies()
        .layer("Controller").definedBy("..controller..", "..web..")
        .layer("Service").definedBy("..service..")
        .layer("Repository").definedBy("..repository..", "..dao..")
        .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
        .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
        .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service");
```

若只想约束所列各层之间的依赖（忽略第三方/JDK），把 `.consideringAllDependencies()` 换成 `.consideringOnlyDependenciesInLayers()`。

单条显式规则的替代写法（单个约束的失败信息更清晰）：
```java
@ArchTest
static final ArchRule controllersDontTouchRepos = noClasses()
        .that().resideInAPackage("..controller..")
        .should().dependOnClassesThat().resideInAPackage("..repository..")
        .because("controllers must go through services");
```

## DDD / 六边形 / 整洁架构规则

ArchUnit 内置的洋葱架构规则很适合 DDD/六边形/整洁：

```java
@ArchTest
static final ArchRule onion = onionArchitecture()
        .domainModels("BASE.domain.model..")
        .domainServices("BASE.domain.service..")
        .applicationServices("BASE.application..")
        .adapter("web", "BASE.adapter.web..")
        .adapter("persistence", "BASE.adapter.persistence..")
        .adapter("messaging", "BASE.adapter.messaging..");
```
`onionArchitecture()` 强制：领域模型不依赖任何东西；领域服务只依赖模型；application 依赖 domain；适配器只向内依赖、且彼此不依赖。

显式的"只能向内"规则（当包布局不太契合 `onionArchitecture()` 时用）：
```java
@ArchTest
static final ArchRule domainIsFrameworkFree = noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAnyPackage(
                "org.springframework..", "jakarta.persistence..", "javax.persistence..")
        .because("the domain core must stay framework-agnostic");

@ArchTest
static final ArchRule domainDoesNotDependOnInfra = noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAnyPackage("..infrastructure..", "..adapter..");
```

## 按功能分包（slices）规则

```java
@ArchTest
static final ArchRule featuresAreIndependent = slices()
        .matching("BASE.(*)..")          // BASE 下第一段包 = 功能名
        .namingSlices("Feature $1")
        .should().notDependOnEachOther()
        .ignoreDependency(resideInAnyPackage("BASE.shared.."), alwaysTrue()); // 放行 shared
```
若功能之间只能通过发布的 API 包通信，禁止访问 `internal`：
```java
@ArchTest
static final ArchRule onlyApiIsPublic = noClasses()
        .that().resideOutsideOfPackage("BASE.(*)..")  // 按功能逐一细化
        .should().dependOnClassesThat().resideInAPackage("..internal..");
```

## MVVM（Android）规则

```java
@ArchTest
static final ArchRule viewModelHasNoAndroidUi = noClasses()
        .that().resideInAPackage("..viewmodel..")
        .should().dependOnClassesThat().resideInAnyPackage(
                "android.view..", "android.widget..", "androidx.appcompat..")
        .because("ViewModels must stay unit-testable, free of Android UI types");

@ArchTest
static final ArchRule viewDoesNotTouchModelDirectly = noClasses()
        .that().resideInAPackage("..view..")
        .should().dependOnClassesThat().resideInAPackage("..repository..");

@ArchTest
static final ArchRule modelDoesNotDependOnUpper = noClasses()
        .that().resideInAnyPackage("..model..", "..repository..")
        .should().dependOnClassesThat().resideInAnyPackage("..viewmodel..", "..view..");
```

## 通用规则（每个工程都加）

```java
// 无包循环 —— 价值最高的单条防腐规则。
@ArchTest
static final ArchRule noCycles = slices().matching("BASE.(*)..")
        .should().beFreeOfCycles();

// 命名：让类待在该待的地方。
@ArchTest
static final ArchRule controllerNaming = classes()
        .that().resideInAPackage("..controller..")
        .should().haveSimpleNameEndingWith("Controller");

@ArchTest
static final ArchRule serviceNaming = classes()
        .that().areAnnotatedWith(org.springframework.stereotype.Service.class)
        .should().resideInAPackage("..service..");

// shared/common 不得依赖功能代码。
@ArchTest
static final ArchRule commonStaysLeaf = noClasses()
        .that().resideInAPackage("..common..")
        .should().dependOnClassesThat().resideInAPackage("BASE..")
        .because("shared code must be a dependency-free leaf");
```

---

## 冻结：把存量违规记为基线、只拦新增

这是守护遗留/被 AI 改动代码库的关键特性。`freeze(rule)` 返回一个 `FreezingArchRule`。首次运行时把当前所有违规记入存储；之后再运行，已记录的违规被忽略，只有**新增**违规才使测试失败。

把任何本会因历史债务而失败的规则包起来：
```java
@ArchTest
static final ArchRule noCycles = freeze(slices().matching("BASE.(*)..").should().beFreeOfCycles());

@ArchTest
static final ArchRule layered = freeze(layeredArchitecture().consideringAllDependencies()
        .layer("Controller").definedBy("..controller..")
        .layer("Service").definedBy("..service..")
        .layer("Repository").definedBy("..repository..")
        .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
        .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
        .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service"));
```

**存储配置** —— 创建 `src/test/resources/archunit.properties`：
```properties
# 默认存储是 archunit_store/ 下的文本文件 —— 可读、利于 diff，请提交进版本库。
freeze.store.default.path=archunit_store
# 允许首次运行创建存储，并在违规被移除时更新存储：
freeze.store.default.allowStoreCreation=true
freeze.store.default.allowStoreUpdate=true
# 设为 true 时，即便修复了违规也不会缩减存储；保持 false，让移除的债务永久消失。
freeze.refreeze=false
```

**给用户讲清楚的工作流：**
1. 首次运行记录基线；把 `archunit_store/` 目录提交进版本库。
2. 新代码若违反某条已冻结规则，构建失败——这就是护栏在拦 AI 腐烂。
3. 当有人*修复*了某条历史违规，存储会缩减（在 `allowStoreUpdate=true` 下），把架构棘轮式地推向干净。提交更新后的存储。
4. 想主动重设基线时，把 `freeze.refreeze=true` 跑一次。

**严格模式（不冻结）：** 直接去掉 `freeze(...)` 包装。构建随即对*所有*违规（含历史）失败。对绿地项目、或准备一次性还清全部债务的团队，提供这个选项。

---

## 导入选项与多模块说明

- `ImportOption.DoNotIncludeTests.class` 把测试类排除在分析之外（几乎总是需要）。
- `ImportOption.DoNotIncludeJars.class` 排除库类。
- 多模块构建：在每个模块各放一个限定到该模块基础包的 `ArchitectureTest`，或分析该模块的编译输出。在聚合器上跑单个测试可能导入错误/空的类路径。
- `@AnalyzeClasses(packages = {...})` 接受多个包；`packagesOf = SomeClass.class` 是比字符串字面量更利于重构的写法。
