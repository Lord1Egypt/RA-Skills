---
name: code-comment
version: 1.0.0
description: 所有编码任务的注释规范约束。只要任务涉及编写、修改、审查、重构代码，无论是新增功能、修 bug、code review、写工具函数、还是解释代码片段，都必须触发此 skill，确保输出的代码注释符合资深开发者风格：简练、纯中文、聚焦 Why、无 AI 味。支持 Java、C++、Kotlin、JavaScript、TypeScript、Python、Rust、Go、React (JSX/TSX) 等主流语言。
---

#Code Comment Skill

清洗代码中的 AI 味注释，输出可直接运行的完整文件。

## 角色定位

资深 Tech Lead 视角：极度反感冗长、机器翻译腔、解释字面意思的注释。

## 核心规则

### 1. 删繁就简 — No Obvious Comments
坚决删除所有解释"代码字面意思"的废话。

**删除示例：**
```
i++  // 将 i 的值增加 1
list.clear()  // 清空列表
return result  // 返回结果
```
以上全部删掉，不需要任何替代。

### 2. 聚焦 Why，而非 What
只保留以下四类注释：
- **业务背景**：为什么要有这段逻辑
- **复杂算法概括**：非显而易见的算法意图
- **边界/兜底逻辑**：特殊情况的处理原因
- **危险操作警告**：副作用、性能陷阱、并发风险等

### 3. 拒绝翻译腔
消除以下表达模式：
- "这个函数被用来..."
- "它将返回..."
- "为了防止发生不可预见的错误..."
- "该方法用于处理..."

人类开发者写注释**极少**在单行注释末尾加句号，去掉句末标点。

### 4. 纯中文输出
所有英文注释、中英夹杂注释，全部转换为地道纯中文。

---

## 注释处理策略

### 行内注释 / 单行注释
执行最严格的精简：**能不写就不写**。必须写时，限制在 5 个词以内。

好的行内注释示例：
```
// 边界拦截
// 防抖兜底
// 透传数据
// 降级处理
// 幂等校验
```

### 函数/类文档注释（Docstring / JSDoc / KDoc）
保留 `@param`、`@return`、`@throws` 等结构化标签，但重写描述文本，使用大厂惯用表达。

---

## 术语映射表

| AI 味写法 | 重构为 |
|-----------|--------|
| 作为默认的后备值 | 兜底 / 默认兜底 |
| 传递给下一个函数 | 透传 |
| 检查是否为空/未定义 | 判空 / 非空校验 / 拦截 |
| 发送网络请求获取数据 | 拉取数据 |
| 传入的参数 | 入参 |
| 返回的结果 | 出参 |
| 遍历这个数组 | （删掉，废话） |
| 初始化变量 | （删掉，废话） |
| 将结果存储到变量中 | （删掉，废话） |
| 调用xxx方法来处理 | （删掉，废话） |
| 如果条件为真则... | （删掉，废话） |
| 捕获并处理异常 | 异常兜底 |
| 确保线程安全 | 加锁 / 并发保护 |
| 这是一个工具类 | 工具类 |
| 用于格式化输出 | 格式化 |

---

## 各语言注释语法参考

| 语言 | 单行 | 块注释 | 文档注释 |
|------|------|--------|----------|
| Java | `//` | `/* */` | `/** */` |
| Kotlin | `//` | `/* */` | `/** */` (KDoc) |
| C++ | `//` | `/* */` | `///` 或 `/** */` |
| JavaScript / TypeScript | `//` | `/* */` | `/** */` (JSDoc) |
| React (JSX/TSX) | `{/* */}` JSX内 / `//` JS内 | `/* */` | `/** */` |
| Python | `#` | — | `"""docstring"""` |
| Rust | `//` | `/* */` | `///` (外部) / `//!` (模块) |
| Go | `//` | `/* */` | `//` (godoc 格式) |

**注意**：JSX 模板内的注释必须用 `{/* */}`，不能用 `//`，处理 React 文件时严格区分。

---

## 输出要求

1. **绝对不修改**任何执行逻辑、变量名、方法名、导入语句
2. 只处理注释
3. 输出必须是**可直接复制运行**的完整文件
4. 用对应语言的 Markdown 代码块包裹输出
5. **不输出任何解释性文字**，代码块前后不加任何说明

---

## 示例

### 输入（Java，AI 味注释）
```java
/**
 * 这个方法用于计算两个整数的和并返回结果。
 * @param a 第一个需要相加的整数参数
 * @param b 第二个需要相加的整数参数
 * @return 返回两个整数相加之后得到的和
 */
public int add(int a, int b) {
    // 将两个数字进行相加操作
    int result = a + b;  // 计算结果存储在result变量中
    return result;  // 返回最终的计算结果
}
```

### 输出
```java
public int add(int a, int b) {
    int result = a + b;
    return result;
}
```

---

### 输入（TypeScript，AI 味注释）
```typescript
/**
 * 这个函数被用来从服务器获取用户数据。
 * 它将发送一个网络请求到指定的API端点，
 * 并在请求完成后返回用户对象。
 * @param userId 传入的用户ID参数，用于标识要获取的用户
 * @returns 返回一个包含用户信息的Promise对象
 */
async function fetchUser(userId: string): Promise<User> {
    // 检查userId是否为空字符串或者未定义
    if (!userId) {
        // 如果userId为空，则抛出一个错误
        throw new Error('userId is required');
    }
    // 发送网络请求获取数据
    const response = await api.get(`/users/${userId}`);
    // 将响应数据作为默认的后备值返回
    return response.data ?? DEFAULT_USER;
}
```

### 输出
```typescript
/**
 * 拉取单个用户数据
 * @param userId 用户 ID
 * @returns 用户对象
 */
async function fetchUser(userId: string): Promise<User> {
    if (!userId) {  // 判空拦截
        throw new Error('userId is required');
    }
    const response = await api.get(`/users/${userId}`);
    return response.data ?? DEFAULT_USER;  // 兜底
}
```

