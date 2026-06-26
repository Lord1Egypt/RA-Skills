# Mermaid 图表模板（中文化）

> ⚠️ **此模板仅供生成 HTML 总结报告时参考**，聊天框内可视化已改用 ASCII 线框图。
> 仅在需要渲染 HTML 报告中的流程图时才加载本文件。

---

## 目录

1. [Mermaid 代码生成规范](#mermaid-代码生成规范)
2. [AS-IS 当前流程](#as-is-当前流程)
3. [TO-BE 优化流程](to-be-优化流程)

---

## Mermaid 代码生成规范

```
1. 只使用 flowchart TD 或 flowchart TB
2. 节点文字用 [] 包裹：node["文字"]
3. 子图用 subgraph name["标题"] ... end
4. 连接线用 --> 或 -.-> 或 --->
5. 中文引号内文字：|"中文"|  注意逗号是英文
6. style 放在 end 后面
7. 每个代码块必须完整闭合
```

---

## AS-IS 当前流程

```mermaid
flowchart TD
    subgraph morning["☀️ 上午"]
        A1["📊 任务1"]
        A2["📋 任务2"]
        A3["📦 任务3"]
        A1 --> A2 --> A3
    end

    subgraph afternoon["🌤️ 下午"]
        B1["🏷️ 任务4"]
        B2["💰 任务5"]
        B3["📝 任务6"]
        B1 --> B2 --> B3
    end

    subgraph pain["😤 痛点"]
        P1["❌ 痛点1"]
        P2["❌ 痛点2"]
    end

    morning --> afternoon
    afternoon -->|"每日循环"| A1
    A3 -.->|"触发"| P1

    style morning fill:#e3f2fd,stroke:#1565c0
    style afternoon fill:#e8f5e9,stroke:#2e7d32
    style pain fill:#ffebee,stroke:#c62828
```

---

## TO-BE 优化流程

```mermaid
flowchart TB
    subgraph trigger["⏰ 定时触发"]
        T1["08:00 任务1"]
        T2["09:00 任务2"]
    end

    subgraph auto["🤖 自动化处理"]
        A1["📊 数据汇总"]
        A2["📋 报告生成"]
    end

    subgraph human["👤 人工审批"]
        H1["✅ 确认"]
        H2["📤 发送"]
    end

    T1 --> A1 --> H1 --> H2
    T2 --> A2 --> H1

    style trigger fill:#fff3e0,stroke:#ff9800
    style auto fill:#e8f5e9,stroke:#4caf50
    style human fill:#e3f2fd,stroke:#2196f3
```
