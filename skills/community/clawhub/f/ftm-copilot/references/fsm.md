# FSM (Finite State Machine) Reference

## What is an FTM FSM?
Defines object lifecycle. Modeled in RSA → exported as SQL → loaded from DB at runtime by EP flow.
Selected based on object's `OBJ_CLASS` + `SUBTYPE`.

## FSM Components
| Component | DB Table | Description |
|---|---|---|
| FSM | `FSM` | Root; has `OBJECT_SELECTION_TEMPLATE` (SQL) |
| State | `FSM_STATE_REL` | Named state |
| Transition | `FSM_TRANSITION` | (FromState, Event) → (Action, ToState) |
| Event Type | `EVENT_TYPE` | Named event; controls logging + processing mode |

## Transition Properties
- **Event Filter** — ESQL boolean on event context: e.g., `$ContextNULL{BATCH}`
- **Object Filter** — SQL WHERE predicates on object data
- **Override Selection** — SQL override for object selection (optional)
- **FSM Action** — ACE subflow name to execute

## RSA Stereotypes
| Stereotype | Effect |
|---|---|
| `PMP_Alert` | Operator alert in OAC; `Constraints` define allowed actions |
| `PMP_OpsControl` | Requires user intervention; not an alert |
| `PMP_Terminal` | Final state |

**PMP_Alert Constraints:** Cancel / Resubmit / Release / Continue

## Generic (Pre-built) FSMs
- Generic Inbound Transmission FSM
- Generic Outbound Transmission FSM
- Generic Outbound Transaction FSM
- Generic Inbound Acknowledgement Transaction FSM

## Standard Events
| Event | When Raised |
|---|---|
| `E_MpInMappingComplete` | Inbound mapper succeeded |
| `E_MpInMappingAborted` | Inbound mapper failed |
| `E_TransOutSent` | Outbound transmission sent |
| `E_TxnOutCreated` | Outbound transaction created |
| `E_CorrelationSuccessful` | Response correlated to request |
| `E_CorrelationFailure` | Correlation failed |
| `E_Heartbeat` | Periodic tick (~60s) |
| `E_HeartbeatStart` | Broker startup |
| `E_ActivityEvent` | Scheduled activity triggered |
| `E_ChildTxnArrived` | Child transaction arrived (collating pattern) |

## Event Configuration (`EVENT_TYPE`)
- `EVENT_LOGGING` — log event instances
- `RENDER_AS_MESSAGE` — true: async (MQ queue); false: inline
- `AGGREGATE_THRESHOLD` — max events to aggregate

## FSM Design Checklist
- [ ] Every path has a terminal state (completed/cancelled)
- [ ] Every path has a `PMP_Alert` state for failure
- [ ] Every alert state has Constraints (Cancel/Resubmit/Release)
- [ ] Heartbeat transitions use Object Filter on `timeout` field
- [ ] Generic FSMs reused where applicable
- [ ] New `SUBTYPE` values registered in `VALUE` table
