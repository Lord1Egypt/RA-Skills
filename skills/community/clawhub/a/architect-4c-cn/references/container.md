# L2 容器图

展开一个系统，说明应用与数据存储的职责、技术和通信。

## 画法

- 展开支付平台，内部只有支付应用和支付库。外部系统保留原名称与类型。
- 后台任务在支付应用内执行，属于组件。实际独立启动和部署时，再建模为单独容器。
- 按执行边界划分 SPA、API 和任务进程。依赖库和源码目录不能直接证明容器边界。
- 数据的逻辑归属与托管位置分开表达，机器、副本和负载均衡器放到部署图。

示例是支付平台的虚构目标方案。图例中虚线框是系统边界，绿色为应用容器，紫色为数据容器，灰色为外部系统，实线表示通信。

绘图与配色见共用的 [绘图与视觉规范](diagram-guidelines.md)。

## 完整模板

### 暗色

```mermaid
---
config:
  theme: "base"
  look: "classic"
  fontFamily: "\"PingFang SC\", \"Helvetica Neue\", Arial, sans-serif"
  flowchart: {nodeSpacing: 28, rankSpacing: 40, padding: 14, curve: basis}
  sequence: {mirrorActors: false, actorMargin: 42, messageMargin: 28, boxMargin: 10}
  themeVariables: {darkMode: true, background: '#07111F', fontFamily: '"PingFang SC", "Helvetica Neue", Arial, sans-serif', fontSize: 15px,
      primaryColor: '#0B2B25', primaryTextColor: '#E6EDF3', primaryBorderColor: '#34D399', lineColor: '#B8C4D4',
      textColor: '#E6EDF3', secondaryColor: '#211532', tertiaryColor: '#101B2B', clusterBkg: '#101B2B', clusterBorder: '#66758A',
      edgeLabelBackground: '#07111F', actorBkg: '#101B2B', actorBorder: '#34D399', actorTextColor: '#E6EDF3', actorLineColor: '#66758A',
      signalColor: '#B8C4D4', signalTextColor: '#E6EDF3', labelBoxBkgColor: '#101B2B', labelBoxBorderColor: '#66758A',
      labelTextColor: '#E6EDF3', loopTextColor: '#E6EDF3', noteBkgColor: '#28220E', noteBorderColor: '#FACC15',
      noteTextColor: '#E6EDF3', activationBkgColor: '#0B2B25', activationBorderColor: '#34D399', sequenceNumberColor: '#07111F'}
  themeCSS: |
    .nodeLabel small { color: #9AA9BC; font-size: 12px; }
    .nodeLabel b { font-weight: 600; }
    .cluster-label { font-weight: 600; }
    .edgeLabel { background-color: #07111F; color: #9AA9BC; }
    .cluster rect { rx: 10; ry: 10; }
    .actor { rx: 8; ry: 8; }
---
flowchart LR
    Merchant("<b>商家订单系统</b><br/><small>外部软件系统<br/>管理订单与接收支付结果</small>")
    Provider("<b>支付渠道</b><br/><small>外部软件系统<br/>执行扣款与确认结果</small>")
    subgraph Platform["◈ 支付平台 | L2"]
        direction TB
    PayApp("<b>支付应用</b><br/><small>应用容器 | Java 21 / Spring Boot<br/>受理、核实、通知</small>")
    PayDB[("<b>支付库</b><br/><small>数据容器 | PostgreSQL<br/>支付状态与投递任务</small>")]
    PayApp -->|"读写支付与任务 | SQL/TLS"| PayDB
    end
    Merchant -->|"发起支付 | JSON/HTTPS"| PayApp
    PayApp -->|"通知支付结果 | JSON/HTTPS"| Merchant
    PayApp -->|"请求扣款与查询结果 | JSON/HTTPS"| Provider
    Provider -->|"回传渠道结果 | JSON/HTTPS"| PayApp
    classDef external fill:#101B2B,stroke:#66758A,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef service fill:#0B2B25,stroke:#34D399,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class PayApp service
    classDef data fill:#211532,stroke:#C084FC,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class PayDB data
    style Platform fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

### 亮色

```mermaid
---
config:
  theme: "base"
  look: "classic"
  fontFamily: "\"PingFang SC\", \"Helvetica Neue\", Arial, sans-serif"
  flowchart: {nodeSpacing: 28, rankSpacing: 40, padding: 14, curve: basis}
  sequence: {mirrorActors: false, actorMargin: 42, messageMargin: 28, boxMargin: 10}
  themeVariables: {darkMode: false, background: '#F8FAFC', fontFamily: '"PingFang SC", "Helvetica Neue", Arial, sans-serif',
      fontSize: 15px, primaryColor: '#ECFDF5', primaryTextColor: '#142238', primaryBorderColor: '#047857', lineColor: '#52657D',
      textColor: '#142238', secondaryColor: '#FAF5FF', tertiaryColor: '#F1F5F9', clusterBkg: '#F1F5F9', clusterBorder: '#8090A4',
      edgeLabelBackground: '#F8FAFC', actorBkg: '#F1F5F9', actorBorder: '#047857', actorTextColor: '#142238', actorLineColor: '#8090A4',
      signalColor: '#52657D', signalTextColor: '#142238', labelBoxBkgColor: '#F1F5F9', labelBoxBorderColor: '#8090A4',
      labelTextColor: '#142238', loopTextColor: '#142238', noteBkgColor: '#FFFBEB', noteBorderColor: '#92400E',
      noteTextColor: '#142238', activationBkgColor: '#ECFDF5', activationBorderColor: '#047857', sequenceNumberColor: '#F8FAFC'}
  themeCSS: |
    .nodeLabel small { color: #53647A; font-size: 12px; }
    .nodeLabel b { font-weight: 600; }
    .cluster-label { font-weight: 600; }
    .edgeLabel { background-color: #F8FAFC; color: #53647A; }
    .cluster rect { rx: 10; ry: 10; }
    .actor { rx: 8; ry: 8; }
---
flowchart LR
    Merchant("<b>商家订单系统</b><br/><small>外部软件系统<br/>管理订单与接收支付结果</small>")
    Provider("<b>支付渠道</b><br/><small>外部软件系统<br/>执行扣款与确认结果</small>")
    subgraph Platform["◈ 支付平台 | L2"]
        direction TB
    PayApp("<b>支付应用</b><br/><small>应用容器 | Java 21 / Spring Boot<br/>受理、核实、通知</small>")
    PayDB[("<b>支付库</b><br/><small>数据容器 | PostgreSQL<br/>支付状态与投递任务</small>")]
    PayApp -->|"读写支付与任务 | SQL/TLS"| PayDB
    end
    Merchant -->|"发起支付 | JSON/HTTPS"| PayApp
    PayApp -->|"通知支付结果 | JSON/HTTPS"| Merchant
    PayApp -->|"请求扣款与查询结果 | JSON/HTTPS"| Provider
    Provider -->|"回传渠道结果 | JSON/HTTPS"| PayApp
    classDef external fill:#F1F5F9,stroke:#8090A4,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef service fill:#ECFDF5,stroke:#047857,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class PayApp service
    classDef data fill:#FAF5FF,stroke:#7E22CE,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class PayDB data
    style Platform fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

支付应用独占支付库，保存支付状态和通知任务。终态与通知任务原子持久化是示例设计，组件与动态视图需说明由谁执行。

## 检查

- 确认每个内部节点都是应用或数据存储，职责、技术、协议与数据所有者明确。
- 确认 L1 的外部关系能落到容器，L3 展开的是同一个支付应用。

定义见 [C4 容器图](https://c4model.com/diagrams/container)和 [容器抽象](https://c4model.com/abstractions/container)。
