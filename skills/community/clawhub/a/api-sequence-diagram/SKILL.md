---
name: api-sequence-diagram
description: "根据指定的Java接口（Controller方法/API路径）分析完整调用链路，生成Mermaid时序图，标注关键判断节点、异常处理分支和业务逻辑。当用户要求分析接口调用链路、生成时序图、分析接口流程、查看接口调用关系时使用。"
---

# API 接口时序图生成

## 使用场景

当用户指定一个接口（Controller 方法名、API 路径、或 Service 方法名），自动追踪完整调用链路并生成 Mermaid 时序图。

## 工作流程

### Step 1: 定位目标接口

用户可能提供以下任一信息：
- **API 路径**：如 `/api/v1/dossier/selectDossierVolume`
- **Controller 方法名**：如 `selectDossierVolume`
- **Controller 类名 + 方法名**：如 `EleDossierController#selectDossierVolume`
- **Service 方法名**：需反向查找调用它的 Controller

**操作**：
1. 使用 `search_symbol` 定位目标 Controller 方法，必要时结合 `grep_code` 搜索路径注解
2. 读取 Controller 完整代码，确认 HTTP 方法和请求路径（从 `@RequestMapping`、`@PostMapping` 等注解或对应 API 接口定义获取）
3. 同时读取对应的 API 接口定义文件（`ele-archives-api` 模块），获取注解和路径信息

### Step 2: 追踪调用链路

从 Controller 方法开始，**逐层深入**追踪：

```
Controller → Service(接口) → ServiceImpl(实现) → DAO/Mapper → SQL
                                                → 外部调用(Feign/MQ/Redis)
```

**对每一层执行**：
1. 用 `search_symbol`（带 `relation: calls`）查找被调用方法
2. 用 `read_file` 读取方法完整实现代码
3. 记录：
   - 方法签名、所在类、行号范围
   - 入参和返回值的**业务语义**（不仅是类型名）
   - 调用的下游方法列表
   - **关键判断节点**（if/else、switch、三元表达式）及其**业务含义**
   - **异常处理**（try-catch、throw）
   - **注解信息**（@Transactional、@Async、@TLogAspect 等）
   - **循环处理**（for/while 中的批量操作）
4. 对每个下游方法递归追踪（最多 **4 层**）

**必须关注的调用类型**：
- `@Autowired` 注入的 Service、DAO、工具类
- MyBatis Mapper 接口 → 对应 XML 中的 SQL
- Feign 远程调用接口
- MQ 消息发送（如 `AppMessageSender`、`publisher` 包下的类）
- Redis/缓存操作
- 事件发布（`ApplicationEventPublisher`）

**追踪终止条件**：
- 到达 Mapper 接口方法（尝试查找对应 XML 中 SQL）
- 到达 Feign 接口方法
- 到达 JDK/Spring 框架方法
- 通用工具方法（如 `MessageUtils`、`BeanUtils`、`PageHelper`）仅标注不展开

### Step 3: 生成 Mermaid 时序图

**参与者命名**：

| 层级 | 命名规则 | 示例 |
|------|----------|------|
| 客户端 | `Client` | Client |
| Controller | 类名简称 | Controller |
| Service | 业务名+Service | DossierService |
| Mapper/DAO | 业务名+Mapper | DossierMapper |
| 数据库 | `DB` | DB |
| 缓存 | `Redis` | Redis |
| 消息队列 | `MQ` | MQ |
| 外部服务 | 服务名 | MoiraiService |

**箭头语义**：
- 同步调用：`->>` (实线)
- 同步返回：`-->>` (虚线)
- 异步调用：使用 `Note right of` 标注"异步"

**分支与循环**：
- 条件分支：`alt 条件A业务含义 / else 条件B业务含义 / end`
- 循环：`loop 循环业务含义`
- 可选：`opt 可选条件业务含义`
- 并行：`par 并行任务描述`
- 关键判断用 `Note over 参与者: 判断说明` 标注

**模板**：

```
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant Mapper
    participant DB

    Client->>Controller: POST /api/path (RequestDto)
    Controller->>Controller: 参数预处理（业务含义说明）
    Controller->>Service: methodName(params)

    Note over Service: 关键变量 xxx 的业务含义说明

    alt 条件成立（用业务语言描述）
        Service->>Mapper: queryMethod(params)
        Mapper->>DB: SQL操作描述
        DB-->>Mapper: 结果集
        Mapper-->>Service: List<Entity>
        Note over Service: 对结果进行 xxx 业务处理
    else 条件不成立（用业务语言描述）
        Service-->>Controller: 返回错误/空结果
    end

    opt 存在某可选条件时
        Service->>Mapper: updateMethod(params)
        Mapper->>DB: UPDATE ...
    end

    Service-->>Controller: 处理结果
    Controller-->>Client: BWJsonResult<Vo>
```

### Step 4: 输出关键判断节点表

在时序图之后，以表格形式列出所有关键判断节点：

| 序号 | 位置（类#方法 行号） | 判断条件（代码） | 业务含义（自然语言） | True 分支处理 | False 分支处理 |
|------|----------------------|------------------|----------------------|---------------|----------------|
| 1 | ServiceImpl#method L45 | `if (status == null)` | 校验归档状态是否存在 | 抛出异常：状态不能为空 | 继续后续处理 |
| 2 | ServiceImpl#method L78 | `if ("6".equals(dataState))` | 判断是否为已归档状态 | 过滤未接收的记录 | 保持原始状态不变 |

**要求**：
- "业务含义"列必须用**业务语言**解释，不能仅复述代码
- 对于关键 boolean 变量或表达式，优先说明其**语义**和**判断意图**

### Step 5: 输出调用链路详情

按层级列出每个方法：

```
### 调用链路

1. **Controller 层**
   - `EleDossierController#selectDossierVolume`
   - 职责：接收请求，参数预处理，调用 Service
   - 关键逻辑：将逗号分隔的分类ID拆分为列表

2. **Service 层**
   - `EleDossierServiceImpl#selectDossierVolume`
   - 职责：核心业务逻辑处理
   - 关键逻辑：分页查询、权限过滤
   - 事务：无 / @Transactional(propagation=REQUIRED)

3. **DAO 层**
   - `EleDossierMapper#selectDossierVolume`
   - 对应 SQL：SELECT ... FROM ... WHERE ...
```

### Step 6: 补充分析

根据实际代码情况，选择性输出以下内容：

#### 事务边界
- 标注 `@Transactional` 覆盖范围及传播行为
- 如果存在嵌套事务，说明事务传播链

#### 异常处理链路
- 各层的 try-catch 范围
- 自定义异常类型及其触发条件
- 全局异常处理器是否兜底

#### 性能关注点（如发现则标注）
- N+1 查询
- 循环内数据库调用
- 未分页的全量查询
- 大对象序列化

#### 外部依赖
- 列出所有外部系统调用及其用途

## 完整输出格式

```
## 接口概述

| 属性 | 值 |
|------|-----|
| 接口路径 | POST /api/xxx |
| 所属模块 | xxx模块 |
| Controller | XxxController#methodName |
| 功能描述 | 一句话描述接口功能 |

## 时序图

（Mermaid sequenceDiagram 代码块）

## 关键判断节点

（表格）

## 调用链路详情

（分层列出）

## 补充分析

### 事务边界
（如有）

### 异常处理链路
（如有）

### 性能关注点
（如有）

### 外部依赖
（如有）
```

## 特殊情况处理

1. **接口调用链过长**：先生成主链路概览图，再按模块拆分子链路图
2. **存在异步调用**：在时序图中用 `Note` 标注异步边界，单独说明异步处理流程
3. **存在回调/监听**：追踪事件发布后的 `@EventListener` 或 `subscriber` 处理逻辑
4. **代码中有 TODO/FIXME**：在补充分析中提示
5. **找不到实现类**：明确告知用户，标注为"未找到实现，可能为远程调用或动态代理"
