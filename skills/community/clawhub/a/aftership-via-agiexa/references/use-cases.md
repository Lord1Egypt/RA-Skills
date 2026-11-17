# AfterShip use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/aftership

## Detect Delivery Problems Before Customers Complain

Identify shipments with exceptions, failed delivery attempts, or expired tracking, then prioritize the orders that need immediate attention.

- Apps: AfterShip, Shopify
- Tools: `AFTERSHIP_LIST_PROBLEM_SHIPMENTS`, `AFTERSHIP_GET_TRACKING`, `AFTERSHIP_FIND_SHIPMENTS`

> Act as my Shopify delivery operations assistant. Review shipments that need attention, including exceptions, failed delivery attempts, and expired tracking. Match each shipment to its Shopify order where possible. Summarize the order number, customer, latest tracking status, last checkpoint, estimated delivery date when available, and the issue requiring attention. Prioritize cases by urgency and recommend the next action. Clearly distinguish confirmed tracking information from assumptions. Do not change shipment or order records without my approval.

## Track Orders and Answer Delivery Questions

Retrieve the latest shipment updates and estimated delivery dates so you can quickly investigate customer delivery questions.

- Apps: AfterShip, Shopify
- Tools: `AFTERSHIP_FIND_SHIPMENTS`, `AFTERSHIP_GET_TRACKING`

> Act as my Shopify order tracking assistant. When I provide a Shopify order number, tracking number, or customer identifier, find the corresponding shipment and retrieve its latest tracking details. Summarize the carrier status, recent checkpoints, estimated delivery date, and any delivery exceptions. If multiple shipments match, show me the candidates and ask which one I mean. If no tracking information is available, explain what is missing instead of guessing. Provide a concise, customer-friendly summary that I can use to respond to delivery inquiries.

## Restart Tracking for Stalled Shipments

Find expired shipment tracking and restart tracking for selected shipments to help recover visibility into delayed deliveries.

- Apps: AfterShip
- Tools: `AFTERSHIP_FIND_SHIPMENTS`, `AFTERSHIP_RETRACK_SHIPMENT`

> Act as my Shopify shipment monitoring assistant. Find shipments whose tracking status is expired and summarize their associated order numbers, tracking identifiers, and last available updates. Identify which shipments may benefit from restarting tracking. Show me the affected shipments and request confirmation before restarting tracking. After approval, restart tracking for the selected shipments and report the actual outcome for each one. Do not claim that a package is moving or will arrive by a particular date unless the latest tracking information supports that conclusion.

## Connect Delivery Problems With Shopify Orders

Combine Shopify order information with AfterShip tracking to understand which orders are affected by delivery issues and what needs attention.

- Apps: AfterShip, Shopify
- Tools: `AFTERSHIP_LIST_PROBLEM_SHIPMENTS`, `AFTERSHIP_GET_TRACKING`, `AFTERSHIP_FIND_SHIPMENTS`

> Act as my Shopify order and delivery analyst. Review recent Shopify orders and their associated AfterShip tracking records. Identify orders with delivery exceptions, unsuccessful delivery attempts, expired tracking, or other available warning statuses. For each affected order, summarize its order status, fulfillment information, tracking status, latest checkpoint, estimated delivery date, and recommended next action. Group the results by urgency. If an order cannot be matched confidently to a shipment, flag it for manual review. Do not modify orders or tracking records without my approval.

## Review Returns Before Approving Them

Inspect submitted return requests, review returned items and reasons, and examine associated refund and shipment details before making a decision.

- Apps: AfterShip
- Tools: `AFTERSHIP_LIST_RETURNS`, `AFTERSHIP_GET_RETURN`, `AFTERSHIP_APPROVE_RETURN`

> Act as my Shopify returns assistant. Find returns that are awaiting approval and summarize their return IDs, associated order numbers, customers, items, return reasons, return methods, and available refund and shipment information. Retrieve the complete details for individual returns when needed. Flag cases involving damaged products, incorrect items, missing information, or other issues that deserve closer review. Recommend whether each return needs further investigation, approval, or rejection based on the available evidence. Never approve or reject a return automatically. Ask for my explicit confirmation before making a decision, and clearly explain that the decision may not be reversible in AfterShip.

## Discover Why Products Get Returned

Analyze recent return reasons and frequently returned products to identify recurring product issues and opportunities to improve customer satisfaction.

- Apps: AfterShip, Shopify
- Tools: `AFTERSHIP_RETURN_REASONS_SUMMARY`, `AFTERSHIP_LIST_RETURNS`

> Act as my Shopify product returns analyst. Analyze the available AfterShip return records and summarize the most common return reasons and most frequently returned products. Include counts where supported by the available records, explain the period and dataset covered, and identify recurring patterns. When possible, connect returned products to their Shopify product details. Suggest practical actions such as improving size guides, correcting product descriptions, reviewing product quality, or investigating fulfillment errors. Clearly distinguish observed patterns from hypotheses. Do not claim that a product has a high return rate unless the necessary sales and return data are available to calculate it.

## Match Delivery Issues With Pending Returns

Cross-reference shipment exceptions and failed deliveries with submitted returns to identify customer cases that need coordinated investigation.

- Apps: AfterShip, Shopify
- Tools: `AFTERSHIP_LIST_PROBLEM_SHIPMENTS`, `AFTERSHIP_LIST_RETURNS`, `AFTERSHIP_GET_RETURN`

> Act as my Shopify delivery and returns coordinator. Identify shipments with exceptions, failed delivery attempts, or expired tracking, then check whether the associated Shopify orders have submitted return requests. Match records using order identifiers and other reliable fields. Create a combined report containing the order number, customer, shipment status, latest checkpoint, estimated delivery date, return status, return reason, and recommended next action. Prioritize cases where delivery problems and return requests overlap, since those customers are most likely to need a fast, coordinated response. Ask for my approval before approving or rejecting any return, and do not change order or tracking records without my confirmation.
