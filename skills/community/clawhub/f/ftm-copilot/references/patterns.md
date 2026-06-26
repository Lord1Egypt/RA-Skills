# FTM Patterns Reference (Chapter 9)

## 9.1 Outbound Message/File
Send a message from FTM to an external system.
1. Action creates outbound ISF transaction; raises `E_TxnOutCreated` with target SP ID
2. Generic Outbound Transaction FSM runs outbound mapper (ISF → external)
3. Sends via WMB output node; creates `TRANSMISSION_BASE`; raises `E_TransOutSent`

## 9.2 Routing + ODM
1. Action calls ODM via HTTPRequest node; ODM returns target SP IDs
2. Create one outbound transaction per target (pattern 9.1 each)
- ODM error → alert state; operator resubmits after rules fix

## 9.3 Inbound Acknowledgement / Correlation
1. Response arrives → PT flow → Generic Inbound Acknowledgement FSM
2. Correlates via: `IN_TXN_ACK_MQ1` / `IN_TXN_ACK_MQ2` / `IN_TXN_ACK_CID`
3. Success → `E_CorrelationSuccessful`; Failure → `E_CorrelationFailure` → alert

## 9.4 Store and Release
- SP has open/closed FSM driven by Calendar Group
- Transaction arrives when SP closed → `S_AwaitingRelease`
- Scheduler Task fires at cut-off → releases all warehoused transactions

## 9.5 Transformation / Mapping
- Inbound: `BeginMapper`/`EndMapper`; Outbound: `BeginOutboundMapper`/`EndOutboundMapper`
- Technologies: ESQL, Java, WTX, XSLT, SPN (SWIFT only)
- See `mapping.md` for full code examples

## 9.6 Debulking
1. PT flow creates `BATCH_BASE` + `FRAGMENT` objects per message block
2. Each fragment debulked → individual `TRANSACTION_BASE`
3. Each transaction processed independently; Counter table tracks counts

## 9.7 Bulking
1. Transactions accumulate; `COUNTER` table tracks count vs threshold
2. Threshold met → create `BATCH_BASE` + outbound fragments
3. Outbound mapper assembles batch; sends via pattern 9.1

## 9.8 Scheduler-Driven Store/Release
- `E_Heartbeat` carries `NOW`; Object Filter: `NOW >= TIMEOUT`
- `E_ActivityEvent` fires → releases warehoused transactions for target SP

## 9.9 External Services
- **Async**: send request (9.1) → receive response → correlate (9.3)
- **Sync short**: call directly from action via HTTPRequest node
- **Sync long**: intermediate MQ queue + separate "Process Service Request" flow
- Timeout/no-response → alert state

## 9.10 Hosting Services
- **Async (MQ)**: MQInput → PT flow → business FSM → response via 9.1
- **Sync (HTTP)**: HTTPInput → store HTTP Request ID in `TRANSMISSION.UID` → HTTPReply
  - Outbound channel transport = "HTTP"

## 9.11 Collating Information
- Master waits for all children; child raises `E_ChildTxnArrived` on master
- Requirements: common linking data, known expected child count, timeout for missing children

## 9.12 Scheduled Activity
1. `E_HeartbeatStart` → Scheduler Task initializes; reads Calendar Group → computes timeout
2. Stores in `OBJ_BASE.TIMEOUT`; `E_Heartbeat` Object Filter: `NOW >= TIMEOUT`
3. `E_ActivityEvent` → action executes → reset timeout

## 9.13 Scheduled Expectation
- Expected event arrives → reset timeout; timeout breached → `PMP_Alert` state → notify operator

## 9.14 Heartbeat Monitoring
- FTM → External: Scheduler Task sends periodic heartbeat (9.1)
- External → FTM: inbound heartbeat resets Scheduler Task timeout via SP `RESOURCE_REF`

## 9.15 Error Handling and Alerts
- Mapping failure → `E_MpInMappingAborted` → `S_InPTMapFailed` (`PMP_Alert`)
- Every alert state MUST have Constraints: Cancel / Resubmit / Release
- Batch failure cascades to ALL child transactions
- ODM errors: resubmit (re-call ODM), cancel, or release without ODM data
