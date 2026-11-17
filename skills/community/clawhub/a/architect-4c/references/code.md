# L4 Code diagram

Expand one component into classes, interfaces, functions, or data structures that explain its implementation.

## Drawing approach

- Expand only payment processing. Use `classDiagram` for Java classes, interfaces, and dependencies.
- `PaymentService` invokes `Payment` state rules and uses `PaymentStore` and `ProviderGateway` ports. Interfaces belong to payment processing. L3's storage and provider adapters implement them.
- Keep only relevant methods. Verify actual symbols and paths for current-state views, and label proposed symbols in target views.

This is a fictional target design for payment processing. The namespace is the component's code scope. `<<interface>>` marks an interface, a solid arrow an association, and a dashed arrow a code dependency.

Use the shared [diagram and visual guidelines](diagram-guidelines.md).

## Complete templates

### Dark

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
    PaymentService --> Payment : applies state rules
    PaymentService ..> PaymentStore : persists through port
    PaymentService ..> ProviderGateway : requests and verifies
    style PaymentService fill:#0B2B25,stroke:#34D399,color:#E6EDF3
    style Payment fill:#0B2B25,stroke:#34D399,color:#E6EDF3
    style PaymentStore fill:#211532,stroke:#C084FC,color:#E6EDF3
    style ProviderGateway fill:#101B2B,stroke:#66758A,color:#E6EDF3
```

### Light

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
    PaymentService --> Payment : applies state rules
    PaymentService ..> PaymentStore : persists through port
    PaymentService ..> ProviderGateway : requests and verifies
    style PaymentService fill:#ECFDF5,stroke:#047857,color:#142238
    style Payment fill:#ECFDF5,stroke:#047857,color:#142238
    style PaymentStore fill:#FAF5FF,stroke:#7E22CE,color:#142238
    style ProviderGateway fill:#F1F5F9,stroke:#8090A4,color:#142238
```

`commitFinalAndTask` requires final state and delivery task to commit atomically. Source and tests must verify transactions, unique idempotency keys, and concurrent updates.

## Checks

- Confirm code elements belong to the target component and map to actual symbols or a proposed design.
- Check interface ownership and relationship notation. Support behavioral requirements with evidence beyond the class diagram.

See the [C4 code diagram definition](https://c4model.com/diagrams/code).
