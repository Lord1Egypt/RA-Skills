# L3 组件图

展开一个容器，说明具有明确接口的功能单元及其协作。

## 画法

- 只展开支付应用，支付库、商家与渠道留在应用边界之外。
- HTTP 入口、支付处理、后台任务和三个适配器都是组件，在同一应用内执行。
- 本图表达运行调用。源码依赖和接口实现关系需要另画并注明含义。

示例是支付应用的虚构目标方案。图例中虚线框是应用容器，框内为组件，框外为数据容器或外部系统，实线表示运行调用。

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
flowchart TB
    Merchant("<b>商家订单系统</b><br/><small>外部软件系统<br/>管理订单与接收支付结果</small>")
    Provider("<b>支付渠道</b><br/><small>外部软件系统<br/>执行扣款与确认结果</small>")
    subgraph PayApp["◈ 支付应用 | L3"]
        direction TB
    Api("<b>HTTP 入口</b><br/><small>组件 | Spring MVC<br/>鉴权与参数校验</small>")
    Core("<b>支付处理</b><br/><small>组件 | Java<br/>幂等与状态规则</small>")
    Jobs("<b>后台任务</b><br/><small>组件 | Spring Scheduling<br/>核实结果、投递通知</small>")
    Store("<b>存储适配器</b><br/><small>组件 | JDBC<br/>事务与任务存取</small>")
    ChannelClient("<b>渠道适配器</b><br/><small>组件 | Java HTTP<br/>请求渠道、验证结果</small>")
    MerchantClient("<b>商家适配器</b><br/><small>组件 | Java HTTP<br/>签名与结果投递</small>")
    Api -->|"提交命令与查询"| Core
    Core -->|"提交终态与通知任务"| Store
    Core -->|"发起请求与验证结果"| ChannelClient
    Jobs -->|"应用核实结果"| Core
    Jobs -->|"领取与记录任务"| Store
    Jobs -->|"查询支付结果"| ChannelClient
    Jobs -->|"投递支付结果"| MerchantClient
    end
    PayDB[("<b>支付库</b><br/><small>数据容器 | PostgreSQL<br/>支付状态与投递任务</small>")]
    Merchant -->|"发起支付 | HTTPS"| Api
    Provider -->|"回传渠道结果 | HTTPS"| Api
    Store -->|"读写支付与任务 | SQL/TLS"| PayDB
    ChannelClient -->|"请求扣款与查询结果 | HTTPS"| Provider
    MerchantClient -->|"通知支付结果 | HTTPS"| Merchant
    classDef external fill:#101B2B,stroke:#66758A,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef entry fill:#082A36,stroke:#22D3EE,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Api entry
    classDef service fill:#0B2B25,stroke:#34D399,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Core,ChannelClient,MerchantClient service
    classDef worker fill:#0B292B,stroke:#2DD4BF,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Jobs worker
    classDef data fill:#211532,stroke:#C084FC,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Store,PayDB data
    style PayApp fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
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
flowchart TB
    Merchant("<b>商家订单系统</b><br/><small>外部软件系统<br/>管理订单与接收支付结果</small>")
    Provider("<b>支付渠道</b><br/><small>外部软件系统<br/>执行扣款与确认结果</small>")
    subgraph PayApp["◈ 支付应用 | L3"]
        direction TB
    Api("<b>HTTP 入口</b><br/><small>组件 | Spring MVC<br/>鉴权与参数校验</small>")
    Core("<b>支付处理</b><br/><small>组件 | Java<br/>幂等与状态规则</small>")
    Jobs("<b>后台任务</b><br/><small>组件 | Spring Scheduling<br/>核实结果、投递通知</small>")
    Store("<b>存储适配器</b><br/><small>组件 | JDBC<br/>事务与任务存取</small>")
    ChannelClient("<b>渠道适配器</b><br/><small>组件 | Java HTTP<br/>请求渠道、验证结果</small>")
    MerchantClient("<b>商家适配器</b><br/><small>组件 | Java HTTP<br/>签名与结果投递</small>")
    Api -->|"提交命令与查询"| Core
    Core -->|"提交终态与通知任务"| Store
    Core -->|"发起请求与验证结果"| ChannelClient
    Jobs -->|"应用核实结果"| Core
    Jobs -->|"领取与记录任务"| Store
    Jobs -->|"查询支付结果"| ChannelClient
    Jobs -->|"投递支付结果"| MerchantClient
    end
    PayDB[("<b>支付库</b><br/><small>数据容器 | PostgreSQL<br/>支付状态与投递任务</small>")]
    Merchant -->|"发起支付 | HTTPS"| Api
    Provider -->|"回传渠道结果 | HTTPS"| Api
    Store -->|"读写支付与任务 | SQL/TLS"| PayDB
    ChannelClient -->|"请求扣款与查询结果 | HTTPS"| Provider
    MerchantClient -->|"通知支付结果 | HTTPS"| Merchant
    classDef external fill:#F1F5F9,stroke:#8090A4,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef entry fill:#ECFEFF,stroke:#0E7490,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Api entry
    classDef service fill:#ECFDF5,stroke:#047857,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Core,ChannelClient,MerchantClient service
    classDef worker fill:#F0FDFA,stroke:#0F766E,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Jobs worker
    classDef data fill:#FAF5FF,stroke:#7E22CE,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Store,PayDB data
    style PayApp fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

支付处理负责幂等与状态规则，存储适配器负责事务写入。后台任务核实结果，并通过商家适配器投递通知。L4 只展开支付处理，其端口由存储与渠道适配器实现。

## 检查

- 确认组件的职责、接口和所属容器，核对状态、事务与任务处理的负责者。
- 确认组件关系细化了 L2 的接口与数据访问，组件没有被误画为独立部署单元。

定义见 [C4 组件图](https://c4model.com/diagrams/component)和 [组件抽象](https://c4model.com/abstractions/component)。
