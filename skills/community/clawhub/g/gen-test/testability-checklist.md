# 可测试性评审清单

本文档是 Phase 3（可测试性评审）的详细参考。对每个函数逐项检查，给出判定。

---

## 评审维度详解

### 1. 纯度 (Purity)

**定义**：相同输入是否总是产生相同输出，且无可观测的副作用。

| 级别 | 特征 | 测试难度 |
|------|------|----------|
| 纯函数 | 无副作用，输出完全由输入决定 | 最易测试 |
| 可控副作用 | 有副作用但通过参数注入依赖 | 可测试 |
| 隐式副作用 | 内部直接操作全局状态、文件、网络 | 难以测试 |

**好的设计**

```typescript
function calculateDiscount(price: number, tier: CustomerTier): number {
  // 纯计算，无副作用
}
```

**坏的设计**

```typescript
function calculateDiscount(userId: string): number {
  const user = db.query(`SELECT * FROM users WHERE id = ?`, userId); // 隐式 DB 依赖
  const config = globalConfig.discountRates; // 全局状态依赖
  logService.info(`Calculating discount for ${userId}`); // 副作用
  // ...
}
```

**判定标准**：
- 函数签名中没有任何表示外部依赖注入的参数，但函数名暗示需要外部数据 → 可能有隐式依赖 → 标记 NEEDS_REFACTOR
- 签名为 `(primitives) → primitives` 且无 async → 大概率为纯函数 → TESTABLE

---

### 2. 依赖注入 (Dependency Injection)

**定义**：外部依赖（DB、HTTP client、文件系统、时钟等）是否通过参数/构造函数传入。

**好的设计**

```go
type UserService struct {
    repo UserRepository  // 接口，可替换为 mock
    clock Clock          // 接口，可控制时间
}

func (s *UserService) CreateUser(ctx context.Context, req CreateUserReq) (*User, error) {
    // repo 和 clock 都可以在测试中替换
}
```

**坏的设计**

```go
func CreateUser(ctx context.Context, req CreateUserReq) (*User, error) {
    db := database.GetConnection()  // 硬编码获取数据库连接
    now := time.Now()               // 不可控的时间
    // ...
}
```

**判定标准**：
- 构造函数/工厂接受接口参数 → TESTABLE
- 函数内部使用全局单例或硬编码 `new` → NEEDS_REFACTOR
- 建议重构方向：将依赖抽为接口，通过参数注入

---

### 3. 接口隔离 (Interface Segregation)

**定义**：参数是否职责清晰，而非传入过度耦合的大对象。

**好的设计**

```python
def send_notification(recipient_email: str, subject: str, body: str) -> bool:
    # 只接收需要的数据
```

**坏的设计**

```python
def send_notification(context: AppContext) -> bool:
    # AppContext 包含数百个字段，函数只用其中 3 个
    # 测试时必须构造整个 AppContext
```

**判定标准**：
- 参数为具体的业务值或小接口 → TESTABLE
- 参数为 God Object（字段数 > 10 且函数只用少数） → NEEDS_REFACTOR
- 建议重构方向：提取函数实际需要的最小参数集

---

### 4. 确定性 (Determinism)

**定义**：函数是否依赖不可控的外部状态（时间、随机数、环境变量等）。

**常见的不确定性来源**

| 来源 | 问题 | 解决方案 |
|------|------|----------|
| `time.Now()` / `Date.now()` | 每次运行结果不同 | 注入 Clock 接口 |
| `Math.random()` / `rand` | 不可重现 | 注入 seed 或 RNG 接口 |
| 环境变量 | 环境依赖 | 通过参数传入配置 |
| 文件系统路径 | 路径依赖 | 使用临时目录或内存 FS |
| 网络调用 | 外部服务不可控 | 注入 HTTP client 接口 |

**判定标准**：
- 签名中有 Clock/RNG/Config 接口参数 → TESTABLE
- 函数名含 `now` / `random` / `uuid` 且无注入参数 → 可能不确定 → 需进一步检查
- 确认不确定后 → NEEDS_REFACTOR

---

### 5. 可观测性 (Observability)

**定义**：函数的关键行为是否可通过返回值或明确的输出通道验证。

**好的设计**

```typescript
function processOrder(order: Order): ProcessResult {
  return { status: 'completed', total: 42.0, notifications: ['email_sent'] };
  // 所有结果通过返回值可观测
}
```

**坏的设计**

```typescript
function processOrder(order: Order): void {
  // 内部发送邮件、更新数据库、写日志
  // 调用者无法得知发生了什么
}
```

**判定标准**：
- 返回有意义的值或 error → TESTABLE
- 返回 void/None 且函数名暗示有副作用 → 可能不可观测 → NEEDS_REFACTOR
- 建议重构方向：返回结果对象，或通过事件/回调暴露行为

---

### 6. 函数粒度 (Granularity)

**定义**：函数是否只做一件事。

**判定标准**：
- 函数名含 `and` 或 `Or` → 可能职责过多
- 参数列表过长（> 5 个参数） → 可能在做多件事
- 返回类型过于复杂（返回多种不相关的数据） → 可能在做多件事
- 建议重构方向：拆分为多个单职责函数

---

## 判定决策树

```
对每个函数：

1. 是否为 trivial getter/setter 或纯委托？
   → YES: SKIP（说明原因）
   → NO: 继续

2. 函数签名是否可以推断出隐式外部依赖？
   （无依赖注入参数，但函数名暗示需要 DB/网络/文件等）
   → YES: NEEDS_REFACTOR（缺少依赖注入）
   → NO: 继续

3. 返回值是否可观测？
   （void/None 返回且名称暗示副作用）
   → 不可观测: NEEDS_REFACTOR（缺少可观测性）
   → 可观测: 继续

4. 参数是否为 God Object？
   → YES: NEEDS_REFACTOR（接口未隔离）
   → NO: 继续

5. 签名中是否有不确定性因素且无注入？
   → YES: NEEDS_REFACTOR（缺少确定性控制）
   → NO: TESTABLE
```

---

## 报告格式模板

```markdown
## 可测试性报告

### 统计
- 总计扫描: N 个函数
- 可测 (TESTABLE): X 个
- 需重构 (NEEDS_REFACTOR): Y 个
- 跳过 (SKIP): Z 个

---

### TESTABLE 函数

| 模块 | 函数 | 测试维度 |
|------|------|----------|

---

### NEEDS_REFACTOR 函数

#### [module].[functionName]

| 项目 | 详情 |
|------|------|
| 问题 | [具体的设计缺陷，引用评审维度] |
| 影响 | [为什么导致测试困难，会造成哪种低质量测试] |
| 建议 | [具体的重构方向，用代码片段说明 before/after] |
| 严重程度 | 高/中/低 |

---

### SKIP 函数

| 模块 | 函数 | 跳过原因 |
|------|------|----------|
```

---

## 常见反模式速查

| 反模式 | 症状（从签名可见） | 判定 |
|--------|---------------------|------|
| 隐藏依赖 | 无依赖参数但函数名含 save/send/fetch/query | NEEDS_REFACTOR |
| God Function | 参数 > 5 个，或名称含 and/process/handle | NEEDS_REFACTOR |
| Void 黑洞 | 返回 void 且名称暗示有重要行为 | NEEDS_REFACTOR |
| 不可控时间 | 涉及 schedule/expire/timeout 但无 Clock 参数 | NEEDS_REFACTOR |
| Stringly Typed | 大量 string 参数代替枚举/类型 | 中等风险，标注注意 |
| Boolean Trap | 多个 bool 参数，调用者无法知道含义 | 中等风险，标注注意 |
