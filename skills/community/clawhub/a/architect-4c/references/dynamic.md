# Dynamic interaction diagram

Select one scenario and show how static-model elements collaborate at runtime.

## Drawing approach

- Use L2 containers and external systems. Draw a separate L3 sequence for internal detail, keeping containers and their components at separate levels.
- Use `sequenceDiagram` for order and conditions. Ground interactions in structural relationships.
- Distinguish accepted requests, final payment state, and acknowledged merchant delivery. A timeout leaves the result uncertain.

This fictional target design covers payment initiation and result notification. Solid arrows are requests, dashed arrows responses, and notes constraints.

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
sequenceDiagram
    autonumber
    participant Merchant as Merchant order system<br/>External system
    participant PayApp as Payment application<br/>Application container
    participant PayDB as Payment database<br/>Data container
    participant Provider as Payment provider<br/>External system
    Merchant->>PayApp: Initiate payment with merchant order key
    PayApp->>PayDB: Claim unique order key or read original payment
    PayDB-->>PayApp: Original payment or new pending record
    alt Duplicate request
        PayApp-->>Merchant: Return original payment ID and status
    else First acceptance
        PayApp->>Provider: Request charge with stable idempotency ID
        alt Verifiable final result available
            Provider-->>PayApp: Payment result and proof
            Note over PayApp: Verify provider result and apply state rules
            PayApp->>PayDB: Atomically commit final state and delivery task
            PayApp-->>Merchant: Return payment ID and final status
        else Timeout or uncertain result
            Note over PayApp,Provider: Jobs or verified callbacks reconcile results<br/>Keep pending until final, apply bounded handling
            PayApp-->>Merchant: Return payment ID and pending status
        end
    end
    opt Final-state delivery task exists, including later reconciliation
        Note over PayApp,PayDB: Later final results also commit state and task atomically
        PayApp->>PayDB: Claim delivery task with processing lease
        PayDB-->>PayApp: Notification event and stable event ID
        PayApp->>Merchant: Signed result notification, deduplicate by event ID
        alt Merchant acknowledges
            Merchant-->>PayApp: Acknowledgment
            PayApp->>PayDB: Mark task complete
        else No acknowledgment or timeout
            PayApp->>PayDB: Record failure and next delivery time
            Note over PayApp: Retry with backoff, alert or escalate at limit
        end
    end
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
sequenceDiagram
    autonumber
    participant Merchant as Merchant order system<br/>External system
    participant PayApp as Payment application<br/>Application container
    participant PayDB as Payment database<br/>Data container
    participant Provider as Payment provider<br/>External system
    Merchant->>PayApp: Initiate payment with merchant order key
    PayApp->>PayDB: Claim unique order key or read original payment
    PayDB-->>PayApp: Original payment or new pending record
    alt Duplicate request
        PayApp-->>Merchant: Return original payment ID and status
    else First acceptance
        PayApp->>Provider: Request charge with stable idempotency ID
        alt Verifiable final result available
            Provider-->>PayApp: Payment result and proof
            Note over PayApp: Verify provider result and apply state rules
            PayApp->>PayDB: Atomically commit final state and delivery task
            PayApp-->>Merchant: Return payment ID and final status
        else Timeout or uncertain result
            Note over PayApp,Provider: Jobs or verified callbacks reconcile results<br/>Keep pending until final, apply bounded handling
            PayApp-->>Merchant: Return payment ID and pending status
        end
    end
    opt Final-state delivery task exists, including later reconciliation
        Note over PayApp,PayDB: Later final results also commit state and task atomically
        PayApp->>PayDB: Claim delivery task with processing lease
        PayDB-->>PayApp: Notification event and stable event ID
        PayApp->>Merchant: Signed result notification, deduplicate by event ID
        alt Merchant acknowledges
            Merchant-->>PayApp: Acknowledgment
            PayApp->>PayDB: Mark task complete
        else No acknowledgment or timeout
            PayApp->>PayDB: Record failure and next delivery time
            Note over PayApp: Retry with backoff, alert or escalate at limit
        end
    end
```

A merchant order key reuses the original payment record. Provider requests use a stable idempotency identifier. Jobs or verified callbacks reconcile results. Final state and delivery task commit atomically. Notifications use at-least-once delivery and merchant deduplication by event identifier. Retries use backoff and count or time limits, followed by alerts or manual handling.

## Checks

- Map interactions to the structure and assign owners for state changes and failure responses.
- Check idempotency for repeated requests, callbacks, and delivery. Define stop conditions for uncertain results and retries.

See the [C4 dynamic diagram definition](https://c4model.com/diagrams/dynamic).
