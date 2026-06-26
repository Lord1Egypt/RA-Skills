---
name: java-code-review
description: "Java项目代码review工具。分析Git变更+完整调用链路上下文，推断业务需求，进行多维度评分和分类汇总，生成完整PRD文档。包含细粒度Java代码审查清单（Null安全、异常处理、Streams、并发、equals/hashCode、资源管理、API设计、性能、MyBatis/ORM、事务边界、SQL/DDL质量）。"
category: development
risk: safe
source: custom
date_added: "2026-04-28"
author: user
tags: [java, code-review, git-diff, business-analysis, risk-detection, performance, optimization, spring, mybatis, transaction, sql-ddl, concurrency, scoring, prd, null-safety, streams, exception-handling, resource-management, api-design]
tools: [git, glob, grep, read, write, bash, lsp_diagnostics, ast_grep_search, lsp_find_references, lsp_goto_definition]
compatibility: opencode
trigger_phrase:
  - 代码评审
  - review代码
  - 分析变更
  - 代码检查
  - 检查bug
  - 风险分析
  - 性能检查
  - 需求分析
  - 业务分析
  - 生成PRD
---

# Java Code Review - Java项目代码评审工具

## 概述

**智能化Java项目代码评审工具**，完整流程（7步）：

1. **Git Diff 变更获取** - 拉取代码变更内容（支持 --cached / 分支对比）
2. **完整上下文分析** - 分析调用链路，推断业务逻辑
3. **PRD文档生成** - 覆盖所有变更点（新增+修改）
4. **代码检测（P0/P1快速扫描）** - 严重缺陷和代码缺陷快速定位
5. **细粒度代码审查清单** - 12类深度检查（A-L）：Null安全、异常处理、Streams、并发、Java惯用法、资源管理、API设计、性能、测试、MyBatis/ORM、事务边界、SQL/DDL质量
6. **多维度评分** - 代码质量评分
7. **Review报告生成** - 输出结构化报告

## 何时使用此技能

- 用户需要进行代码评审
- 用户需要理解变更的业务含义
- 用户需要生成完整PRD文档
- 用户需要评分和质量评估
- 用户说 "review代码" / "检查PR" / "代码review" / "检查下代码"

---

## 第1步：Git Diff 变更获取

### 1.1 确定基准分支

**优先询问用户**，如用户未指定则使用以下策略：
- 当前分支有上游跟踪 → 使用 `@{u}`（上游分支）
- 存在 `develop` 分支 → 使用 `develop`
- 存在 `main`/`master` 分支 → 使用 `main`/`master`
- 否则 → 使用 `HEAD~10`（最近10次提交）

### 1.2 获取变更

```bash
# 场景1：工作区+暂存区 vs 基准分支（最常用）
git diff <基准分支>..HEAD --name-only
git diff <基准分支>..HEAD -U500
git diff <基准分支>..HEAD --stat

# 场景2：仅检查已暂存（staged）的变更
git diff --cached -U500
git diff --cached --stat

# 场景3：工作区未暂存变更
git diff -U500
```

### 1.3 收集信息

- 新增的文件（新增功能）
- 修改的文件（功能修改）
- 删除的文件（功能删除）
- 变更行数统计

---

## 第2步：完整上下文分析

### 2.1 确定入口点

对于每个变更的方法/类，向上追溯找到业务入口：
- Controller层的HTTP入口（@PostMapping/@GetMapping）
- Service层的业务入口方法
- MQ消息入口（@RabbitListener/@KafkaListener）
- 定时任务入口（@Scheduled）
- 外部API入口（Feign Client）

### 2.2 追踪方法链

使用 lsp_find_references 分析每个关键方法：
```
入口点
  ↓ 调用
变更方法
  ↓ 调用
子方法1 → 子方法2 → ... → 数据库/外部服务
```

### 2.3 业务逻辑推断

基于完整链路推断业务逻辑：
```
变更方法：InventoryService.deduct()

完整链路：
Controller.createOrder() [下单入口]
  ↓
OrderService.create() [订单创建]
    ↓
InventoryService.deduct() [变更点] ← 库存扣减
    ↓
PaymentService.pay() [支付]
    ↓
NotificationService.notify() [通知]

推断业务需求：
用户下单 → 自动扣减库存 → 支付 → 通知
核心流程：订单+库存+支付+消息 四模块联动
```

---

## 第3步：PRD文档生成（核心能力）

**重要**：PRD必须覆盖**所有变更点**，包括新增功能和修改功能。

### 3.1 PRD文档结构

```markdown
# 产品需求文档 PRD

## 1. 概述

### 1.1 产品名称
[模块名称-版本号]

### 1.2 需求背景
[为什么需要这个功能，解决什么问题]

### 1.3 需求范围
- 涉及模块：xxx
- 用户类型：xxx
- 使用场景：xxx

---

## 2. 功能需求

### 2.1 功能清单

| # | 功能点名称 | 功能类型 | 优先级 | 涉及文件 | 行号 |
|---|-----------|--------|--------|---------|-----|
| 1 | 功能点A | 新增 | P0 | XxxService.java | 1-100 |
| 2 | 功能点B | 新增 | P1 | XxxServiceImpl.java | 200-300 |
| 3 | 功能点C | 修改 | P2 | XxxConverter.java | 10-30 |
| 4 | 字段调整 | 修改 | P2 | DDL脚本 | - |

### 2.2 功能详情（每个变更点都需要详细描述）

#### 2.2.1 [功能点A-新增功能]

**功能类型**：新增

**功能描述**：
[详细描述这个功能做什么]

**业务规则**：
- 规则1
- 规则2

**核心链路**：
```
[入口] Controller.method() [POST /api/xxx]
  ↓ Service.method()
[核心] 核心业务逻辑 ← 变更内容
  ↓ DAO.method()
[终点] 数据库/外部服务
```

**入参说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| param1 | String | 是 | xxx |
| param2 | Integer | 否 | xxx |

**出参说明**：
| 参数 | 类型 | 说明 |
|------|------|------|
| result1 | String | xxx |

**异常处理**：
| 异常场景 | 错误码 | 提示信息 |
|----------|--------|----------|
| 场景1 | E_xxx | xxx |

---

#### 2.2.2 [功能点B-修改功能]

**功能类型**：修改

**涉及文件**：`xxx.java`
**涉及行号**：xxx-xxx

**修改前**：
```java
// 原代码
```

**修改后**：
```java
// 新代码
```

**变更原因**：
[为什么要这样修改]

**核心链路**：
```
[入口] Controller.method() [POST /api/xxx]
  ↓ Service.method()
[核心] 修改的方法 ← 变更内容
  ↓ DAO.method()
[终点] 数据库/外部服务
```

**影响分析**：
- 影响的上游：xxx
- 影响的下游：xxx
- 兼容性：是否向前兼容
- 数据库：是否需要迁移

---

#### 2.2.3 [功能点C-优化功能]

**功能类型**：优化

**优化前**：
[优化前的描述]

**优化后**：
[优化后的描述]

**优化效果**：
- 性能提升：xxx%
- 代码改进：xxx

---

## 3. 数据库变更

### 3.1 新增表

```sql
CREATE TABLE xxx (
  id VARCHAR(36) PRIMARY KEY,
  tenant_id VARCHAR(32) NOT NULL,
  org_id VARCHAR(32),
  doc_id VARCHAR(36) NOT NULL,
  retry_type VARCHAR(32),
  retry_count INT DEFAULT 0,
  last_retry_time DATETIME,
  create_time DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY idx_doc_id (doc_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xxx表';
```

### 3.2 修改表

```sql
-- 修改字段长度
ALTER TABLE xxx MODIFY COLUMN goods_name VARCHAR(300) COMMENT '商品名称';

-- 新增字段
ALTER TABLE xxx ADD COLUMN operator VARCHAR(300) COMMENT '操作人';
```

### 3.3 数据迁移
[如有数据迁移需求，描述迁移脚本]

---

## 4. 接口设计

### 4.1 新增接口

| 接口名称 | 请求方式 | 路径 | 说明 |
|---------|---------|------|------|
| 接口A | POST | /api/xxx | xxx |

**请求参数**：
```json
{
  "ids": ["xxx"],
  "operator": "xxx"
}
```

**响应参数**：
```json
{
  "code": "0",
  "message": "成功",
  "data": null
}
```

### 4.2 修改接口

| 接口名称 | 请求方式 | 路径 | 说明 |
|---------|---------|------|------|
| 接口A | POST | /api/xxx | 参数调整 |

**变更说明**：
[描述接口参数变更]

---

## 5. 涉及的代码变更

### 5.1 新增文件

| 文件路径 | 说明 |
|---------|------|
| xxx.java | 新增功能 |

### 5.2 修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| xxx.java | 方法A新增、方法B修改 |

### 5.3 删除文件

| 文件路径 | 删除原因 |
|---------|---------|
| xxx.java | 功能废弃 |

---

## 6. 非功能需求

### 6.1 性能要求
- 响应时间：< xxx ms
- 并发能力：xxx TPS

### 6.2 安全要求
- 权限校验：是/否
- 数据加密：是/否

### 6.3 兼容性要求
- 向前兼容：是/否
- 多数据库支持：MySQL/Oracle/PostgreSQL

---

## 7. 测试要点

### 7.1 功能测试
- [ ] 测试点1
- [ ] 测试点2

### 7.2 异常测试
- [ ] 测试点1
- [ ] 测试点2

### 7.3 边界测试
- [ ] 测试点1
- [ ] 测试点2

### 7.4 回归测试
- [ ] 测试点1（确认原有功能不受影响）
- [ ] 测试点2

---

## 8. 上线注意点

- [ ] 注意点1
- [ ] 注意点2

---

## 9. 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v2.4.0.0 | 2026-04-30 | 初始版本 | xxx |
```

---

## 第4步：代码检测（P0/P1快速扫描）

在进入细粒度审查前，先快速扫描严重缺陷和代码缺陷。

### P0严重缺陷

| 检查项 | 检测模式 | 扣分 |
|--------|----------|------|
| 空指针 | `$OBJ.$METHOD()` obj未检查 | -10 |
| SQL注入 | `"SELECT " + $TABLE` 直接拼接 | -10 |
| 密钥泄露 | `password/token = "xxx"` | -10 |
| 事务缺失 | @Transactional 关键方法无事务 | -10 |

### P1代码缺陷

| 检查项 | 检测模式 | 扣分 |
|--------|----------|------|
| 资源泄漏 | new FileInputStream 未关闭 | -5 |
| 线程安全 | private static 共享变量 | -5 |
| 空catch | catch块为空或仅打印日志 | -5 |
| 循环查询 | for循环内数据库操作 | -5 |

### P2代码规范（快速扫描）

以下为不与第5步细粒度审查清单重叠的独立检查项：

| 检查项 | 检测模式 | 扣分 |
|--------|----------|------|
| 参数过多 | 方法参数超过3个 | -2 |
| 魔法数字 | 字面量未定义为常量 | -2 |
| 原始泛型 | List/Map 未指定类型参数 | -2 |

> **注意**：Streams滥用、Boolean参数、Optional.get()、equals缺hashCode、catch Exception 等 P2 检查项已整合到第5步对应分类中，此处不再重复。

---

## 第5步：细粒度代码审查清单 (Detailed Review Checklist)

### 审查策略

1. **Quick scan** - 理解变更意图，确定审查范围
2. **Checklist pass** - 按以下分类逐项检查
3. **Summary** - 按严重度汇总（Critical → Improvement → Minor）

### A. Null 安全

```java
// ❌ NPE 风险：链式调用不检查中间null
String name = user.getName().toUpperCase();

// ✅ 安全：Optional + map
String name = Optional.ofNullable(user.getName())
    .map(String::toUpperCase)
    .orElse("");

// ✅ 也可以：提前返回
if (user.getName() == null) {
    return "";
}
return user.getName().toUpperCase();
```

**检查项：**
- [ ] 链式方法调用是否缺少null检查
- [ ] 公共API缺少 `@Nullable` / `@NonNull` 注解
- [ ] `Optional.get()` 没有 `isPresent()` 检查——**改用 `orElseThrow()`**
- [ ] 方法返回 `null` 而非 `Optional` 或空集合
- [ ] 对集合入参做null检查 → 使用 `Objects.requireNonNull()`

🔧 **检测方法：**
- `grep`: `Optional\.get\(\)` → 检查是否有 `isPresent()` 先导
- `ast_grep_search`: `$OBJ.$METHOD()` pattern 查找链式调用中缺少 null 守卫
- `lsp_find_references`: 追踪方法返回 null 的调用方

**建议：**
- 返回值可能为空时，使用 `Optional<T>` 替代 `null`
- 构造/方法入参使用 `Objects.requireNonNull()`
- 返回空集合用 `Collections.emptyList()` 替代 `null`

### B. 异常处理

```java
// ❌ 吞掉异常（最坏实践）
try {
    process();
} catch (Exception e) {
    // 没有日志，没有处理
}

// ❌ 捕获范围过宽
catch (Exception e) { }
catch (Throwable t) { }

// ❌ 丢失原始异常栈（不传cause）
catch (IOException e) {
    throw new RuntimeException(e.getMessage());  // 丢失堆栈！
}

// ✅ 正确处理
catch (IOException e) {
    log.error("处理文件失败: {}", filename, e);
    throw new ProcessingException("文件处理失败", e);  // 传递cause
}
```

**检查项：**
- [ ] 空 catch 块
- [ ] 捕获范围过宽（`Exception`, `Throwable`）
- [ ] 丢失原始异常（未链式传递 cause）
- [ ] 用异常做流程控制
- [ ] 受检异常泄露到API边界

🔧 **检测方法：**
- `ast_grep_search`: `catch (Exception` 和 `catch (Throwable` → 宽泛捕获
- `grep`: `catch\s*\(` 带上下文行查找空 catch 块
- `grep`: `throw new.*getMessage\(\)` → 丢失原始异常栈

**建议：**
- 日志同时记录**上下文 + 完整栈信息**
- 使用具体的异常子类
- 领域错误使用自定义异常

### C. Streams & 集合操作

```java
// ❌ 遍历中修改集合 → ConcurrentModificationException
for (Item item : items) {
    if (item.isExpired()) {
        items.remove(item);
    }
}

// ✅ 使用 removeIf
items.removeIf(Item::isExpired);

// ❌ 简单逻辑滥用Stream
list.stream().forEach(System.out::println);

// ✅ 简单场景直接用for循环
for (Item item : list) {
    System.out.println(item);
}

// ❌ 假设 Collectors.toList() 返回可变List
List<String> names = users.stream()
    .map(User::getName)
    .collect(Collectors.toList());
names.add("extra");  // 可能不可变！

// ✅ 显式要求可变集合
List<String> names = users.stream()
    .map(User::getName)
    .collect(Collectors.toCollection(ArrayList::new));
```

**检查项：**
- [ ] 遍历时修改集合（用 `removeIf()` 替代）
- [ ] 简单操作用Stream替代for循环（可读性反而差）
- [ ] `Collectors.toList()` 假定返回可变列表
- [ ] 未使用 `List.of()`, `Set.of()`, `Map.of()` 创建不可变集合
- [ ] 不理解就乱用并行流（parallelStream）

🔧 **检测方法：**
- `ast_grep_search`: `.stream().forEach` → 可能的滥用模式
- `grep`: `\.remove\(` 在 `for\s*\(` 块内 → 遍历时修改
- `grep`: `\.collect\(Collectors\.toList\(\)\)` → 检查后续是否有 add/remove 操作

**建议：**
- 防御性拷贝用 `List.copyOf()`
- Stream 用于**数据转换**，循环用于**副作用操作**
- 简单逻辑（1-2行映射）用Stream，复杂逻辑用for循环

### D. 并发安全

```java
// ❌ 非线程安全的集合
private Map<String, User> cache = new HashMap<>();

// ✅ 线程安全集合
private Map<String, User> cache = new ConcurrentHashMap<>();

// ❌ check-then-act 竞态条件
if (!map.containsKey(key)) {
    map.put(key, computeValue());  // 多线程下可能重复计算
}

// ✅ 原子操作
map.computeIfAbsent(key, k -> computeValue());

// ❌ 双重检查锁（没有volatile则broken）
if (instance == null) {
    synchronized(this) {
        if (instance == null) {
            instance = new Instance();  // 可能看到半初始化对象
        }
    }
}

// ✅ 使用静态内部类 / volatile
private volatile Instance instance;
```

**检查项：**
- [ ] 共享可变状态缺少同步
- [ ] check-then-act 操作缺少原子性
- [ ] 共享变量缺少 `volatile`
- [ ] 在非final对象上同步
- [ ] 线程不安全的懒初始化

🔧 **检测方法：**
- `grep`: `private static.*Map|List|Set` → 静态共享集合
- `ast_grep_search`: `synchronized\(` → 检查同步对象是否为 final
- `grep`: `if \(.*== null\)` 在 synchronized 块内 → 双重检查锁

**建议：**
- 优先使用不可变对象
- 优先用 `java.util.concurrent` 并发集合类
- 简单场景用 `AtomicReference`, `AtomicInteger`
- 考虑添加 `@ThreadSafe` / `@NotThreadSafe` 注解

### E. Java 惯用法 (equals/hashCode/toString/Builder)

**equals & hashCode:**
```java
// ❌ 只重写equals不重写hashCode → 破坏HashMap契约！
@Override
public boolean equals(Object o) { ... }
// hashCode 缺失！

// ❌ hashCode用了可变字段 → 放入HashMap后字段变了就找不到了
@Override
public int hashCode() {
    return Objects.hash(id, mutableField);  // 危险！
}

// ✅ 同时重写，只用不可变字段
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User user)) return false;
    return Objects.equals(id, user.id);
}

@Override
public int hashCode() {
    return Objects.hash(id);
}
```

**toString:**
```java
// ❌ 包含敏感数据
return "User{password='" + password + "'}";

// ✅ 调试友好但安全
return "User{id=" + id + ", name='" + name + "'}";
```

**Builder模式:**
```java
// ✅ 当构造参数 > 3 时推荐
User user = User.builder()
    .name("张三")
    .email("zhangsan@example.com")
    .build();
```

**检查项：**
- [ ] `equals` 有但 `hashCode` 缺失 → **确定要破坏HashMap/HashSet吗？**
- [ ] `hashCode` 使用了可变字段
- [ ] 领域对象缺少 `toString`（调试困难）
- [ ] 构造参数 > 3-4 → 建议Builder
- [ ] 未使用 Java 16+ `instanceof` pattern matching

🔧 **检测方法：**
- `ast_grep_search`: `public boolean equals` → 检查同文件是否有 `public int hashCode`
- `grep`: `Objects\.hash\(.*this\.` → hashCode 使用了实例字段（可能可变）
- `grep`: `password|secret|token` 在 `toString\(\)` 方法内 → 敏感数据泄露

### F. 资源管理 (Try-with-resources)

```java
// ❌ 资源泄漏
FileInputStream fis = new FileInputStream(file);
// ... 抛异常前没close

// ✅ try-with-resources
try (FileInputStream fis = new FileInputStream(file)) {
    // 自动关闭
}

// ❌ 多个资源嵌套，可能内层未关闭
try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
    // 如果 BufferedWriter 构造失败，FileWriter 可能泄漏
}

// ✅ 独立声明
try (FileWriter fw = new FileWriter(file);
     BufferedWriter writer = new BufferedWriter(fw)) {
    // 两者都被保证关闭
}
```

**检查项：**
- [ ] `Closeable`/`AutoCloseable` 未使用 try-with-resources
- [ ] 数据库连接/Statement/ResultSet 未正确关闭
- [ ] 嵌套资源声明顺序错误

🔧 **检测方法：**
- `grep`: `new (File|Input|Output|Reader|Writer|Connection|Statement)` → 检查是否在 try-with-resources 内
- `ast_grep_search`: `new $CLOSEABLE($$$)` 不在 `try (` 块内 → 资源泄漏风险

**强制规则：任何实现了 `Closeable`/`AutoCloseable` 的资源，必须使用 try-with-resources。**

### G. API 设计

```java
// ❌ Boolean参数 → 调用端看不懂语义
process(data, true, false);

// ✅ 使用枚举
process(data, ProcessMode.ASYNC, ErrorHandling.STRICT);

// ❌ 找不到返回null (调用方不知道)
public User findById(Long id) {
    return users.get(id);  // 可能null
}

// ✅ 语义明确的 Optional
public Optional<User> findById(Long id) {
    return Optional.ofNullable(users.get(id));
}

// ❌ 入参允许null → 调用方不知道能不能传null
public void process(List<Item> items) {
    if (items == null) items = Collections.emptyList();
}

// ✅ 明确要求非null
public void process(List<Item> items) {
    Objects.requireNonNull(items, "items must not be null");
}
```

**检查项：**
- [ ] Boolean参数 → 建议用枚举替代
- [ ] 方法参数 > 3 → 考虑参数对象
- [ ] 同一模块内null处理不一致
- [ ] 公共API入参缺少校验（`Objects.requireNonNull`）

🔧 **检测方法：**
- `ast_grep_search`: `$VISIBILITY $RET $NAME(boolean $PARAM` → Boolean 参数
- `grep`: `public.*\(.*,.*,.*,.*,` → 参数超过3个的方法签名
- `grep`: `Objects\.requireNonNull` → 检查公共方法是否都有入参校验

### H. 性能注意事项

```java
// ❌ 循环内String拼接 → 每次创建新String对象
String result = "";
for (String s : strings) {
    result += s;
}

// ✅ StringBuilder
StringBuilder sb = new StringBuilder();
for (String s : strings) {
    sb.append(s);
}

// ❌ 循环内编译正则 → 每次都重新编译
for (String line : lines) {
    if (line.matches("pattern.*")) { }
}

// ✅ 预编译为静态常量
private static final Pattern PATTERN = Pattern.compile("pattern.*");
for (String line : lines) {
    if (PATTERN.matcher(line).matches()) { }
}

// ❌ N+1 查询
for (User user : users) {
    List<Order> orders = orderRepo.findByUserId(user.getId());
}

// ✅ 批量查询
Map<Long, List<Order>> ordersByUser = orderRepo.findByUserIds(userIds);
```

**检查项：**
- [ ] 循环内 String 拼接 → 用 StringBuilder
- [ ] 循环内正则编译 → 预编译为 Pattern 常量
- [ ] N+1 查询模式
- [ ] 循环内创建可复用对象
- [ ] 未使用原始类型Stream（`IntStream`, `LongStream`）

🔧 **检测方法：**
- `grep`: `\+=` 在 `for\s*\(` 块内 → 循环内 String 拼接
- `grep`: `\.matches\(` 在 `for\s*\(` 块内 → 循环内正则编译
- `ast_grep_search`: `for.*\{.*\.(select|find|query)` → N+1 查询模式

### I. 测试提示

建议为以下场景补充测试：
- [ ] Null入参
- [ ] 空集合入参
- [ ] 边界值
- [ ] 异常路径
- [ ] 并发访问（如适用）

🔧 **检测方法：**
- `glob`: `**/src/test/**/*Test*.java` → 检查是否有对应测试文件
- `grep`: `@Test` → 统计测试方法数量 vs 变更方法数量

### J. MyBatis/ORM 检查

```java
// ❌ N+1 查询：循环内逐条查询
for (Order order : orders) {
    List<OrderItem> items = orderItemMapper.selectByOrderId(order.getId());
    order.setItems(items);
}

// ✅ 批量查询 + 内存组装
List<Long> orderIds = orders.stream().map(Order::getId).collect(Collectors.toList());
List<OrderItem> allItems = orderItemMapper.selectByOrderIds(orderIds);
Map<Long, List<OrderItem>> itemsMap = allItems.stream()
    .collect(Collectors.groupingBy(OrderItem::getOrderId));
orders.forEach(o -> o.setItems(itemsMap.getOrDefault(o.getId(), Collections.emptyList())));

// ❌ 分页插件滥用：先查全部再内存分页
List<User> allUsers = userMapper.selectAll();
List<User> page = allUsers.subList(offset, offset + limit);

// ✅ 使用分页插件
PageHelper.startPage(pageNum, pageSize);
List<User> users = userMapper.selectByCondition(condition);
```

**检查项：**
- [ ] XML映射ID与方法名不一致
- [ ] N+1 查询模式（循环内调用 Mapper）
- [ ] 分页插件滥用（全量查询后内存分页）
- [ ] 一级缓存/二级缓存不当使用（脏读风险）
- [ ] `<if test>` 条件缺少对空字符串的判断
- [ ] `#{}` 与 `${}` 混用（`${}` 有 SQL 注入风险）

🔧 **检测方法：**
- `grep`: `<select|<update|<insert|<delete` 在 `*.xml` → 检查 id 命名是否与方法名一致
- `ast_grep_search`: `for.*\{.*Mapper\.|for.*\{.*mapper\.` → N+1 查询模式
- `grep`: `PageHelper\.startPage` → 检查是否紧跟 Mapper 调用（分页生效）
- `grep`: `\$\{` 在 `*.xml` → SQL 注入风险（应使用 `#{}`）

### K. 事务边界检查

```java
// ❌ 事务传播级别错误：REQUIRES_NEW 导致外层事务回滚失效
@Transactional(propagation = Propagation.REQUIRED)
public void processOrder(Order order) {
    orderMapper.update(order);
    paymentService.pay(order);  // 内部 REQUIRES_NEW，pay 成功但外层回滚
}

// ❌ 同类方法调用事务失效（Spring AOP 代理限制）
public void batchProcess(List<Order> orders) {
    for (Order order : orders) {
        this.processSingle(order);  // @Transactional 不生效！
    }
}

// ✅ 注入自身代理或拆分到不同类
@Transactional
public void processSingle(Order order) { ... }

// ❌ 长事务导致锁竞争
@Transactional
public void exportReport() {
    // 大量查询 + 文件生成 + 邮件发送 都在一个事务内
    List<Data> data = dataMapper.selectAll();  // 持有数据库连接
    File file = generateExcel(data);           // 耗时操作
    emailService.send(file);                   // 外部IO
}
```

**检查项：**
- [ ] 事务传播级别错误（`REQUIRES_NEW` 嵌套回滚边界）
- [ ] 同类方法调用导致事务失效
- [ ] 长事务（事务内包含外部IO、大量计算）
- [ ] `@Transactional` 仅用于 public 方法（非 public 不生效）
- [ ] 事务内捕获异常未重新抛出（吞掉回滚）
- [ ] `readOnly=true` 未设置（查询方法应标记只读）

🔧 **检测方法：**
- `grep`: `@Transactional` → 检查 `propagation` 属性
- `grep`: `REQUIRES_NEW` → 嵌套事务回滚边界
- `grep`: `@Transactional` 在非 public 方法上 → 事务不生效
- `ast_grep_search`: `@Transactional.*\{.*(?:send|http|file|sleep)` → 长事务嫌疑

### L. SQL/DDL 质量检查

```sql
-- ❌ 缺索引：大表无索引导致全表扫描
CREATE TABLE t_order (
  id BIGINT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  order_no VARCHAR(64) NOT NULL,
  status TINYINT,
  create_time DATETIME
) ENGINE=InnoDB;  -- 缺少 user_id 和 order_no 索引！

-- ✅ 合理索引
CREATE TABLE t_order (
  id BIGINT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  order_no VARCHAR(64) NOT NULL,
  status TINYINT DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_user_id (user_id),
  UNIQUE KEY uk_order_no (order_no),
  KEY idx_status_create (status, create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ❌ 字段类型不当
ALTER TABLE t_order ADD COLUMN amount VARCHAR(32);  -- 金额应用 DECIMAL

-- ✅ 正确类型
ALTER TABLE t_order ADD COLUMN amount DECIMAL(18,2) NOT NULL DEFAULT 0.00 COMMENT '订单金额';
```

**检查项：**
- [ ] 缺索引（WHERE/JOIN/ORDER BY 字段无索引）
- [ ] 字段类型不当（金额用 VARCHAR、状态用 VARCHAR 而非 TINYINT）
- [ ] 缺 COMMENT（表、字段无注释）
- [ ] 字符集不一致（表间 JOIN 字段字符集不同）
- [ ] DDL 缺少回滚脚本
- [ ] VARCHAR 长度不合理（过长或过短）
- [ ] 缺默认值（NOT NULL 字段无 DEFAULT）

🔧 **检测方法：**
- `grep`: `CREATE TABLE` 无 `COMMENT` → 缺表注释
- `grep`: `ALTER TABLE` → 检查是否有对应回滚脚本
- `grep`: `VARCHAR\(` → 检查长度是否合理（如 VARCHAR(1) 或 VARCHAR(5000)）
- `grep`: `amount|price|money.*VARCHAR` → 金额字段类型不当

### 严重度分级参考

| 严重度 | 标准 | 对应评分 |
|--------|------|----------|
| **Critical** | 安全漏洞、可能丢失数据、生产环境必崩 | P0 (-10) |
| **High** | 大概率Bug、严重性能问题、破坏API契约 | P1 (-5) |
| **Medium** | 代码坏味、可维护性问题、缺少最佳实践 | P2 (-2) |
| **Low** | 风格问题、微优化、建议性 | P2 (-2) |

---

## 第6步：多维度评分系统

### 评分维度

| 维度 | 权重 | 计算方式 |
|------|------|----------|
| 代码质量 | 20% | (100 - 扣分) * 权重 |
| 安全性 | 25% | (100 - P0问题*10) * 权重 |
| 性能 | 20% | (100 - 性能问题*8) * 权重 |
| 可维护性 | 15% | (100 - 规范问题*5) * 权重 |
| 业务风险 | 20% | (100 - 风险问题*10) * 权重 |

### 扣分规则

| 问题类型 | 扣分 |
|--------|------|
| P0问题 | -10分/个 |
| P1问题 | -5分/个 |
| P2建议 | -2分/个 |

### 最终评级

| 等级 | 分数 | 颜色 | 行动 |
|------|------|------|------|
| S | 90-100 | 🟢 绿 | 可合并 |
| A | 80-89 | 🟢 绿 | 可合并 |
| B | 70-79 | 🟡 黄 | 需要确认 |
| C | 60-69 | 🟠 橙 | 需要修改 |
| D | <60 | 🔴 红 | 拒绝合并 |

---

## 第7步：Review报告生成

```markdown
# 代码评审报告

## 基本信息
- 项目名称：xxx
- 评审范围：xxx → xxx
- 变更文件数：N
- 变更行数：+X / -Y

## 📊 质量评分

| 维度 | 得分 | 评级 |
|------|------|------|
| 代码质量 | 85 | A |
| 安全性 | 90 | S |
| 性能 | 80 | A |
| 可维护性 | 75 | B |
| 业务风险 | 70 | B |
| **总分** | **82** | **A** |

## 📋 需求汇总

### 需求1：[功能点A]
- 涉及文件：XxxService.java (新增100行)
- 变更类型：新增功能
- 入口：XxxController.create() (POST /api/xxx)
- 核心链路：
  ```
  [入口] XxxController.create()
    ↓ XxxService.process()
  [核心] XxxHandler.handle() ← 变更点
    ↓ XxxRepository.save()
  [终点] 数据库持久化
  ```
- 风险等级：🟡 中

### 需求2：[功能点B]
- 涉及文件：XxxServiceImpl.java, XxxController.java
- 变更类型：新增功能
- 入口：POST /api/xxx/action
- 核心链路：
  ```
  [入口] XxxController.action()
  [核心] XxxServiceImpl.action() ← 变更点
    ↓ 逻辑处理
  [终点] 数据库更新
  ```
- 风险等级：🟡 中

## 🔴 严重问题 (P0)
- [ ] 问题1
  - 文件：xxx.java
  - 行号：xxx
  - 修复方案

## 🟡 中等问题 (P1)
- [ ] 问题1
  - 文件：xxx.java
  - 优化方案

## 🟢 建议优化 (P2)
- [ ] 优化1

## 评审结论
- 总体评级：S/A/B/C/D
- 是否可以合并：是/需修改/拒绝
```

---

## 输出

1. **Review报告** → `code-review-report.md`（含评分 + 业务分析 + 细粒度代码检查）
2. **PRD文档** → `prd-{版本号}.md`
3. **控制台摘要** → 评分+问题统计

---

## Review 执行流程总结

```
Trigger: "review代码" / "检查PR" / "代码评审"

Step 1: git diff 获取变更
  ├─ 确定基准分支（询问用户 / 自动检测）
  ├─ 支持 --cached（仅暂存区）/ 分支对比
  ├─ 统计变更文件和行数
  └─ 识别变更类型（新增/修改/删除）

Step 2: 上下文分析
  ├─ lsp_find_references 追踪调用链
  ├─ 确定业务入口（Controller/MQ/定时任务/Feign）
  └─ 推断业务逻辑

Step 3: PRD文档生成（覆盖所有变更点）
  ├─ 功能清单（含文件+行号）
  ├─ 核心链路图
  ├─ 数据库变更
  └─ 接口设计

Step 4: 代码检测（P0/P1快速扫描）
  ├─ P0严重缺陷（NPE/SQL注入/密钥/事务）
  ├─ P1代码缺陷（资源泄漏/线程安全/空catch/循环查询）
  └─ P2代码规范（参数过多/魔法数字/原始泛型）

Step 5: 细粒度审查清单（12类深度检查）
  ├─ A. Null安全
  ├─ B. 异常处理
  ├─ C. Streams & 集合
  ├─ D. 并发安全
  ├─ E. Java惯用法 (equals/hashCode)
  ├─ F. 资源管理 (try-with-resources)
  ├─ G. API设计
  ├─ H. 性能
  ├─ I. 测试提示
  ├─ J. MyBatis/ORM 检查
  ├─ K. 事务边界检查
  └─ L. SQL/DDL 质量检查

Step 6: 多维度评分
  ├─ 代码质量 20%
  ├─ 安全性 25%
  ├─ 性能 20%
  ├─ 可维护性 15%
  └─ 业务风险 20%

Step 7: 生成Review报告
  ├─ 基本信息
  ├─ 质量评分（含维度拆分）
  ├─ 需求汇总（含调用链路）
  ├─ 问题清单（Critical/High/Medium/Low）
  └─ 评审结论
```

---

## PRD生成 Checklist

生成PRD时，**每个变更点都必须包含**：

- [ ] 功能名称
- [ ] 功能类型（新增/修改/删除/优化）
- [ ] 涉及文件和行号
- [ ] 核心业务链路
- [ ] 入参/出参说明
- [ ] 异常处理
- [ ] 数据库变更（如有）
- [ ] 测试要点
