# L4 代码图

展开一个组件，用类、接口、函数或数据结构说明实现。

## 画法

- 本例只展开支付处理，使用 `classDiagram` 表达 Java 类、接口与依赖。
- `PaymentService` 调用 `Payment` 的状态规则，通过 `PaymentStore` 和 `ProviderGateway` 端口访问外部能力。接口属于支付处理，实现在 L3 的存储与渠道适配器中。
- 只保留相关方法。现状图核对实际符号和路径，目标图注明拟议设计。

示例是支付处理的虚构目标方案。图例中 namespace 表示组件代码范围，`<<interface>>` 表示接口，实线箭头表示关联，虚线箭头表示代码依赖。

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
classDiagram
    direction TB
    namespace PaymentProcessing {
        class PaymentService {
            +accept(orderKey) Payment
            +applyVerifiedResult(result) Payment
        }
        class Payment {
            +id
            +orderKey
            +status
            +applyResult(result)
        }
        class PaymentStore {
            <<interface>>
            +claimOrRead(orderKey) Payment
            +commitFinalAndTask(payment)
        }
        class ProviderGateway {
            <<interface>>
            +request(payment) Result
            +verify(proof) Result
        }
    }
    PaymentService --> Payment : 应用状态规则
    PaymentService ..> PaymentStore : 通过端口持久化
    PaymentService ..> ProviderGateway : 请求与验证
    style PaymentService fill:#0B2B25,stroke:#34D399,color:#E6EDF3
    style Payment fill:#0B2B25,stroke:#34D399,color:#E6EDF3
    style PaymentStore fill:#211532,stroke:#C084FC,color:#E6EDF3
    style ProviderGateway fill:#101B2B,stroke:#66758A,color:#E6EDF3
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
classDiagram
    direction TB
    namespace PaymentProcessing {
        class PaymentService {
            +accept(orderKey) Payment
            +applyVerifiedResult(result) Payment
        }
        class Payment {
            +id
            +orderKey
            +status
            +applyResult(result)
        }
        class PaymentStore {
            <<interface>>
            +claimOrRead(orderKey) Payment
            +commitFinalAndTask(payment)
        }
        class ProviderGateway {
            <<interface>>
            +request(payment) Result
            +verify(proof) Result
        }
    }
    PaymentService --> Payment : 应用状态规则
    PaymentService ..> PaymentStore : 通过端口持久化
    PaymentService ..> ProviderGateway : 请求与验证
    style PaymentService fill:#ECFDF5,stroke:#047857,color:#142238
    style Payment fill:#ECFDF5,stroke:#047857,color:#142238
    style PaymentStore fill:#FAF5FF,stroke:#7E22CE,color:#142238
    style ProviderGateway fill:#F1F5F9,stroke:#8090A4,color:#142238
```

`commitFinalAndTask` 约定原子提交终态与通知任务。事务、唯一幂等键和并发更新仍需源码与测试验证。

## 检查

- 确认代码元素属于目标组件，并能对应实际符号或拟议设计。
- 核对接口归属、依赖和关联记法，行为要求有类图之外的证据。

定义见 [C4 代码图](https://c4model.com/diagrams/code)。
