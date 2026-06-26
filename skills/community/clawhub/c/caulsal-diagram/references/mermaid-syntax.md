# 因果图 Mermaid 语法参考

## 基本语法

### 1. 定义图表类型

```mermaid
flowchart TB
    %% TB = Top to Bottom（上下布局）
    %% LR = Left to Right（左右布局）
    %% BT = Bottom to Top
    %% RL = Right to Left
```

### 2. 定义节点

```mermaid
flowchart TB
    A[节点A]
    B[节点B]
    C[节点C]
```

### 3. 定义边（箭头）

```mermaid
flowchart TB
    A --> B      %% 实线箭头
    A -->|标签| B   %% 带标签的箭头
    A -.-> B     %% 虚线箭头
    A ==> B      %% 粗箭头
```

## 常见因果图模板

### 链式结构

```mermaid
flowchart LR
    A[原因] --> B[中介] --> C[结果]
```

### 分叉结构

```mermaid
flowchart TB
    B[共同原因] --> A[变量1]
    B --> C[变量2]
```

### 对撞结构

```mermaid
flowchart TB
    A[原因1] --> B[对撞节点]
    C[原因2] --> B
```

### 混杂结构

```mermaid
flowchart TB
    C[混杂因素] --> E[暴露]
    C --> O[结果]
    E --> O
```

### M 结构

```mermaid
flowchart TB
    A --> B --> C
    A --> C
```

## 样式定制

### 节点形状

```mermaid
flowchart TB
    A[矩形节点]
    B(圆角节点)
    C([体育场形])
    D[[子程序]]
    E[(数据库)]
    F((圆形))
    G>旗帜]
    H{菱形}
    I{{六边形}}
```

### 颜色和样式

```mermaid
flowchart TB
    A[默认样式]
    B[蓝色样式]:::blueClass
    
    classDef blueClass fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#1565c0
```

## 实际案例

### 案例1：止痛药与心脏病

```mermaid
flowchart TB
    A[年龄] --> B[疼痛程度]
    B --> C[生活方式]
    B --> D[止痛药使用]
    C --> E[基础疾病]
    D --> F[心脏病风险]
    E --> F
```

### 案例2：班级规模与学生成绩

```mermaid
flowchart TB
    A[学校资金] --> B[班级规模]
    C[学生需求] --> B
    A --> D[教师质量]
    B --> E[学生成绩]
    D --> E
```

### 案例3：药物疗效研究

```mermaid
flowchart TB
    Z[年龄] --> X[药物使用]
    Z --> Y[康复]
    X --> Y
    W[健康状况] --> X
    W --> Y
```

## 注意事项

1. **节点 ID 不能重复**：每个节点需要唯一的 ID（如 A, B, C）
2. **中文支持**：Mermaid 支持中文，但建议在方括号内使用
3. **布局选择**：
   - 因果层级明确 → `TB`（上下）
   - 时间序列 → `LR`（左右）
4. **复杂图拆分**：超过 10 个节点建议拆分为多个子图