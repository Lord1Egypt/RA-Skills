# AfterShip tools via Agiexa (9)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects AfterShip and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/aftership

| Tool | What it does |
| --- | --- |
| `AFTERSHIP_FIND_SHIPMENTS` | Find tracked shipments by order ID, tracking numbers, keyword (searches tracking number, title, order ID, customer name/email), status or creation dat |
| `AFTERSHIP_LIST_PROBLEM_SHIPMENTS` | List shipments that need attention: Exception (delays, damage, customs, returned to sender), AttemptFail (failed delivery) and Expired (no updates) |
| `AFTERSHIP_GET_TRACKING` | Get one tracked shipment with its latest checkpoints and estimated delivery date |
| `AFTERSHIP_RETRACK_SHIPMENT` | Restart tracking for a shipment whose tracking expired (status Expired) |
| `AFTERSHIP_LIST_RETURNS` | List returns by status (submitted = awaiting approval), creation date, customer email, order name, outcome or return method |
| `AFTERSHIP_GET_RETURN` | Get one return by AfterShip return ID or RMA number, with items, reasons, refunds and return shipments |
| `AFTERSHIP_APPROVE_RETURN` | Approve a submitted return (cannot be undone in AfterShip) |
| `AFTERSHIP_REJECT_RETURN` | Reject a submitted return with a reason shown to the customer (cannot be undone in AfterShip) |
| `AFTERSHIP_RETURN_REASONS_SUMMARY` | Count return reasons and the most-returned products over recent returns (computed by OpenClaw from up to `max_returns` returns) |
