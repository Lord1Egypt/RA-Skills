# Worked task and changed evidence

Synthetic observations only; descriptive steps refer to discovered provider schemas, not literal API names.

## Worked successful task

**Request:** Prepare the already authorized stream: 86.4 USDC over 24 hours to the supplied recipient.

**Available evidence:** Synthetic exact chain, 6-decimal USDC address and recipient are supplied to the mock builder. Duration 86,400 seconds. Builder enforces total cap and end time, simulation matches terms. Existing authorization covers this exact stream. No submission receipt supplied.

**Read sequence:** Resolve asset decimals, recipient and clock; calculate integer rate and remainder, inspect enforceable cap/end time and simulated funding before signing.

**Completed answer:** Rate = 86,400,000 atomic units / 86,400 seconds = 1,000 atomic units per second, or 0.001 USDC/s. That is the economic rate in token base units, not the value a protocol call takes: Sablier Flow encodes 0.001 tokens per second as UD21x18 (`1e15`), and a Superfluid Super Token is always 18 decimals (`1e15` per second), so encode with the selected protocol's rate scale. Total cap 86.4 USDC; duration 24 hours. Return the calculated stream terms and the supplied simulation result. No encoded unsigned payload or absolute start time was supplied, so an actual signable artifact still needs retrieval and review. Terms are calculated; no stream is confirmed. Do not describe terms alone as a constructed transaction or request the same valid authorization again.

## Recovery and continuation

**Changed evidence:** A submission later returns a timeout with known transaction hash and no receipt.

**Useful response:** Preserve submitted/unknown status and reconcile that hash plus stream creation/funding events before another submission. Do not re-request permission for unchanged valid terms merely because a transport timed out.
