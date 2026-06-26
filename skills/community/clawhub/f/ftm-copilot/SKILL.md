---
name: ftm-copilot
description: >
  Expert-level IBM Financial Transaction Manager (FTM) knowledge base and development assistant.
  Invoke this skill whenever the user mentions FTM, IBM Financial Transaction Manager, payments hub,
  payment orchestration, ACE (IBM App Connect Enterprise / WebSphere Message Broker / IIB), RSA
  (IBM Rational Software Architect), ITX/WTX (IBM Transformation Extender / WebSphere Transformation
  Extender), DB2 in a payments context, ISF (Internal Standard Format), ISO 20022 in an IBM context,
  SWIFT integration with IBM tooling, FSM (Finite State Machine) in payments, BAR files, message
  flows, OAC (Operations and Administrative Console), or any combination of these. Also trigger when
  the user asks to act as an "FTM expert", references FTM configuration, or discusses financial
  transaction lifecycle management. When in doubt, trigger — FTM developers always benefit from this
  context.
license: MIT
metadata:
  version: 1.0.0
  tags:
    - ibm
    - ftm
    - payments
    - ace
    - iso20022
    - swift
    - finance
    - integration
  author:
    name: Shoaib Khan
    github: https://github.com/ShoaibKhan
    email: shoaibthedev@gmail.com
    bio: >
      I close the gap between enterprise complexity and developer sanity.
      AI tools, integrations, and automation — built for scale, designed for humans.
---

# IBM FTM Copilot

> Built by [Shoaib Khan](https://github.com/ShoaibKhan) — I close the gap between enterprise complexity
> and developer sanity. AI tools, integrations, and automation — built for scale, designed for humans.

You are an expert IBM FTM developer and architect with deep knowledge of FTM's architecture,
development methodology, tooling ecosystem, and all canonical patterns. Use this to help with
design, development, debugging, configuration, and code review tasks.

## Core Stack

| Component | Role |
|---|---|
| **IBM FTM** | Financial transaction orchestration framework |
| **IBM ACE** (formerly WMB/IIB) | Runtime for all FTM message flows |
| **IBM RSA** | Design-time FSM modeling and config export |
| **IBM ITX/WTX** | Alternative mapping technology (large/complex transforms) |
| **IBM DB2** | Primary data store (Oracle also supported) |
| **IBM MQ** | Transport/messaging infrastructure |
| **IBM WAS** | Hosts Operations and Administrative Console (OAC) |
| **IBM ODM** | External rules engine (routing, validation) |

## Architecture Overview

FTM is a **financial transaction-aware integration platform** built on three pillars:

1. **ISF (Internal Standard Format)** — ISO 20022-based canonical XML; **namespace: `http://www.ibm.com/xmlns/prod/ftm/isf/v3`**
2. **Transaction Processing Engine (TPE)** — runs on ACE/WMB; drives lifecycle via Finite State Machines
3. **Data Model** — DB2 schema storing configuration + operational data

**Two core runtime flows:**
- **Physical Transmission (PT) Flow** — entry point; receives inbound messages, identifies channel, maps to ISF, creates transmission/transaction objects, raises initial event
- **Event Processing (EP) Flow** — event-driven orchestration; reads from MQ event queue, runs FSM engine, fires actions, triggers state transitions

Read `references/architecture.md` for deeper component details.

## Key DB2 Tables

| Table | Purpose |
|---|---|
| `OBJ_BASE` | Base for all lifecycle objects; holds `STATE`, `SUBTYPE`, `TIMEOUT` |
| `TRANSACTION_BASE` | Transaction data + ISF blob |
| `TRANSMISSION_BASE` | Raw transmission data |
| `BATCH_BASE` | Batch grouping |
| `SCHEDULER_TASK_BASE` | Scheduled task with `timeout` field |
| `SERVICE_PARTICIPANT_BASE` | Interface configuration |
| `CHANNEL_BASE` | Channel config (format, mapper, transport) |
| `OBJ_OBJ_REL` | Object relationships (request→response, batch→txn) |
| `EVENT_BASE` | Event instance data |
| `FSM_TRANSITION` | FSM transition rules |
| `VALUE` | Config name-value pairs (e.g., `ROLE_FOR_TXN_TYPE`) |

Read `references/development.md` for DB2 queries and ACE/MQ commands.

## Development Methodology

```
1. DESIGN (RSA)      → Model SPs, Channels, FSMs → export SQL config scripts
2. BUILD (ACE)       → Mapper flows + Action subflows → package as BAR files
3. DEPLOY            → Import config to DB2 + deploy BARs to ACE broker
4. OPERATE (OAC)     → Monitor states, resolve alerts, manage SP lifecycle
```

## The 15 FTM Patterns

| # | Pattern | When to Use |
|---|---|---|
| 9.1 | **Outbound Message/File** | Send a message to an external system |
| 9.2 | **Routing + ODM** | Dynamic routing; multi-target delivery |
| 9.3 | **Inbound Acknowledgement** | Correlate response/ACK to prior request |
| 9.4 | **Store and Release** | Hold transactions until gateway opens |
| 9.5 | **Transformation/Mapping** | Format conversion (any direction) |
| 9.6 | **Debulking** | Split inbound batch → individual transactions |
| 9.7 | **Bulking** | Aggregate transactions → outbound batch |
| 9.8 | **Scheduler-driven Store/Release** | Cut-off time-triggered release |
| 9.9 | **External Services** | Invoke external service (sync or async) |
| 9.10 | **Hosting Services** | FTM hosts a service (MQ or HTTP/SOAP) |
| 9.11 | **Collating Information** | Gather data from multiple messages into one |
| 9.12 | **Scheduled Activity** | Trigger activity at a scheduled time |
| 9.13 | **Scheduled Expectation** | Monitor that an event arrives before deadline |
| 9.14 | **Heartbeat Monitoring** | Send/receive heartbeat pings |
| 9.15 | **Error Handling + Alerts** | Operator notification and resolution |

Read `references/patterns.md` for full implementation details.

## ESQL Quick Reference

```esql
-- Always use these exact namespaces
DECLARE ISF_NS NAMESPACE 'http://www.ibm.com/xmlns/prod/ftm/isf/v3';
DECLARE XSI_NS NAMESPACE 'http://www.w3.org/2001/XMLSchema-instance';

-- ISF output location (inbound mapper)
-- OutputLocalEnvironment.PMP.ISF.XMLNSC

-- Set xsi:type on polymorphic element (e.g. PartyRole)
SET rPartyRole.(XMLNSC.Attribute){XSI_NS}:type = 'isf:DebtorRole';

-- Set XML attribute (e.g. Currency on InstructedAmount)
SET rAmount.(XMLNSC.Attribute)Currency = 'USD';

-- Iterate objects in action flow
DECLARE refObj REFERENCE TO
  Environment.PMP.Variables.Transition[Environment.PMP.Variables.IterationCount]
  .TransObjects.Object[1];
WHILE LASTMOVE(refObj) DO
  MOVE refObj NEXTSIBLING REPEAT NAME;
END WHILE;

-- Delete empty optional ISF element (prevents validation errors)
IF NOT EXISTS(rCT.{ISF_NS}RemittanceInformation.*[]) THEN
  DELETE FIELD rCT.{ISF_NS}RemittanceInformation;
END IF;
```

## Debugging Checklist

1. Check `OBJ_BASE` — `STATE`, `SUBTYPE`, `LAST_UPDATED_TS`
2. Check MQ event queue depth (unprocessed events)
3. Check `EVENT_BASE` for unprocessed events for this transaction
4. Check `FSM_TRANSITION` for expected events in current state
5. Check `OBJ_OBJ_REL` for correlation issues
6. Run `mqsireadlog | mqsiformatlog` for ACE flow errors
7. Check `SERVICE_PARTICIPANT_BASE` — is target SP ACTIVE?
8. Check OAC for `PMP_Alert` states needing operator action

## Error Handling Rules
- Every processing path needs a `PMP_Alert` state for failures
- Every alert state must have Constraints: Cancel / Resubmit / Release
- Mapping failures → `E_MpInMappingAborted` → alert state
- Batch failures cascade to all child transactions
- Always provide a manual operator reset path in the FSM

## Reference Files
- `references/architecture.md` — TPE, data model, interface config hierarchy
- `references/fsm.md` — FSM components, stereotypes, standard events, design checklist
- `references/mapping.md` — ISF structure, ESQL/Java/WTX mapper templates, pitfalls
- `references/patterns.md` — All 15 patterns with implementation steps
- `references/development.md` — ACE CLI, RSA workflow, DB2 queries, Docker debug
