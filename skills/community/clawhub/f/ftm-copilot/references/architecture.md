# FTM Architecture Reference

## Platform Components
- **IBM FTM** — orchestrates, manages, monitors financial transactions through full lifecycle
- **IBM ACE** (App Connect Enterprise, formerly WMB/IIB) — runtime for all FTM message flows
- **IBM MQ** — primary transport/messaging infrastructure
- **IBM WAS** — hosts OAC web console
- **IBM DB2 / Oracle** — supported relational databases
- **IBM RSA** (Rational Software Architect) — design-time FSM and configuration modeling
- **IBM ODM** (Operational Decision Manager) — external rules engine integration
- **IBM WTX/ITX** (WebSphere/IBM Transformation Extender) — alternative mapping technology

## Transaction Processing Engine (TPE)

### Physical Transmission (PT) Flow
Entry point for all inbound messages:
1. Receive via WMB input node (MQInput, HTTPInput, FTPInput)
2. Identify source channel from message metadata or queue name
3. Log physical transmission to DB (`TRANSMISSION_BASE` + `OBJ_BASE`)
4. Invoke inbound mapper (external format → ISF)
5. Store ISF to transaction record (`TRANSACTION_BASE`)
6. Raise event: `E_MpInMappingComplete` or `E_MpInMappingAborted`

**PT Framework Nodes:** `PhysicalTransmissionWrapper`, `BeginMapper`/`EndMapper`,
`BeginOutboundMapper`/`EndOutboundMapper`, `BeginAction`/`EndAction`

### Event Processing (EP) Flow
Orchestration engine:
1. Receive event from MQ event queue
2. Determine target object from event correlation ID
3. Load FSM for object `OBJ_CLASS` + `SUBTYPE`
4. Evaluate transitions for current state + event type
5. Evaluate Object Filter predicate
6. Execute action subflow
7. Update object state in DB; raise any subsequent events

## Data Partitioning
- **Application** (`APPLICATION` table) — logical grouping; data fully isolated
- **Version** (`APP_VERSION` table) — one version "effective" at runtime; supports phased rollouts

## Interface Configuration Hierarchy
```
SERVICE
  └── SERVICE_PARTICIPANT_BASE (logical interface abstraction; has own FSM)
        ├── INPUT_CHANNEL     → FORMAT + MAPPER (inbound)
        └── OUTPUT_CHANNEL    → FORMAT + MAPPER (outbound)
```

## Operational Data Hierarchy
```
TRANSMISSION_BASE  (raw physical message)
  └── BATCH_BASE  (optional logical grouping)
        └── TRANSACTION_BASE  (individual business unit + ISF blob)
              └── TXN_PAYMENT_BASE  (payment-specific extracted fields)
```

All inherit from `OBJ_BASE`: `STATE`, `SUBTYPE`, `OBJ_CLASS`, `TIMEOUT`

## Correlation Strategies (on Channel)
| Strategy | Description |
|---|---|
| `IN_TXN_ACK_MQ1` | MQ CorrelId matches original MsgId |
| `IN_TXN_ACK_MQ2` | MQ CorrelId matches original CorrelId |
| `IN_TXN_ACK_CID` | Custom ID extracted from message content |

## Supported Message Standards
ISO 20022, SWIFT MT (FIN) and MX (MTXML), NACHA (ACH), EDIFACT, ANSI X12
