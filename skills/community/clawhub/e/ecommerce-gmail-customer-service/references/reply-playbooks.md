# General reply solution library

The three-level classification table assigns 2–3 scenario IDs to each leaf intent. Choose one of them as the main plan; multiple appeal emails can combine multiple plans, but only generate one coherent email. All `[]` fields must be populated from a verified context, omitted or asked if missing, no guesswork allowed.

## General solution

### NEED-INFO｜Request the minimum necessary information

Confirm what is understood; list 1–3 minimal pieces of information that are still missing; explain why it is needed; commit to continuing after receiving it. Do not repeatedly request information already in the system.

### NEED-ORDER｜Safe positioning order

It means that the corresponding order cannot be found in the current email address; please provide the minimum combination of order number, order email address or product name and approximate date; remind not to send passwords, verification codes or complete card numbers.

### RESOLVE-NOW｜Verified and resolved immediately

Confirm the verification results; clarify the actions that have been performed; provide traceability identification and follow-up timeliness; invite customers to reply when the results are abnormal.

### EXPLAIN-POLICY｜Explain applicable terms

Quote the policy name and summary of relevant terms; explain why it applies to this order; list the customer's available paths; and attach an official policy link. Avoid pasting the entire policy.

### HUMAN-REVIEW｜Manual review

Confirm the appeal and collected evidence; explain that it has been transferred to the corresponding team; give the case number and a reasonable update time; do not predict the outcome, and do not require the customer to submit repeated submissions.

### SAFETY-ESCALATE｜Safety incident

First ask customers to stop using and stay away from potential dangers; if anyone is injured, it is recommended to contact local emergency/medical services; collect minimum batch and incident information; upgrade the safety manager immediately and do not automatically close the case.

### CLOSE-THANKS｜Thank you and close

Briefly confirm that thanks have been received or the problem has been solved; do not repeat marketing; explain that if you still have problems, you can reply to the original thread.

## Pre-sale and merchandise

### PROD-SPEC｜Verify product information

Directly answer the verified specifications, materials, sizes, ingredients, origin or packaging; point out variation differences; attach product pages/instructions. Unknown parts clearly require confirmation from the product team.

### PROD-FIT｜Adaptation and compatibility

Restate the customer's equipment/scenario/dimensions; list compatibility conditions and incompatibility points; recommend specific variants and explain the basis; if it cannot be guaranteed, it is recommended to measure or confirm with professionals.

### PROD-RECOMMEND｜Demand-based recommendation

Confirm budget, purpose, and constraints first; give 2–3 sellable options; compare key differences; don’t fake effects or pressure to buy.

### PROD-COMPARE｜Product comparison

Compare customer-specified products using the same dimensions: price, specifications, applicable scenarios, restrictions, inventory and after-sales; finally, make conditional recommendations based on known needs.

### STOCK-AVAILABLE｜Spot reply

Indicate current region/variant stock and data times; provide purchase links or optional substitutions; remind that stock may change but do not create a false sense of urgency.

### STOCK-RESTOCK｜Replenishment/Out of stock

Explain that it is currently out of stock; provide a verified replenishment date or simply state that there is no date yet; recommend arrival notifications or alternative products; do not promise unconfirmed time.

### PREORDER-INFO｜Pre-sale instructions

Explain the pre-sale products, estimated delivery window, whether to ship separately, deduction time, cancellation rules and possible changes; please confirm whether you accept it.

### PRICE-EXPLAIN｜Explanation of prices and fees

List product prices, discounts, taxes, freight, tariffs and currencies item by item; explain the source of differences; if errors are shown, transfer to billing for review.

### PRICE-MATCH｜Price Protection/Matching

Check the merchant's policies, products, channels, dates and evidence; if they match, explain the adjustment actions; if they don't match, explain the reasons in detail and provide available alternative offers (if authorized).

### PRODUCT-POLICY｜Pre-sales policy

Briefly describe applicable terms for shipping, returns, warranties, digital goods, or subscriptions; highlight deadlines, fees, and exceptions; guide customers to confirm before purchasing.

## Checkout, Payments, Taxes and Vouchers

### CHECKOUT-FIX｜Checkout Troubleshooting

Confirm the error message and the steps in which it occurred; provide risk-free troubleshooting (refresh, go incognito, change browsers, clear cache, check region); if it still fails, collect time and screenshots and upgrade without asking for a password.

### PAYMENT-DECLINED｜Payment declined

Explain that merchants usually cannot see the bank's specific reasons for rejection; it is recommended to check the billing address, limit, 3DS or replacement method; do not let customers try repeatedly and frequently; contact the card issuer if necessary.

### PAYMENT-PENDING｜Pending authorization

Distinguish between authorized occupation and settled deductions; provide payment status, whether the order is established, and expected release/update range; upgrade the payment team after timeout.

### PAYMENT-DUPLICATE｜Suspected duplicate deductions

List the verified order and transaction status; if an authorization is pending, explain it; if it is confirmed to be repeated, explain the refund/cancellation action; if exceptions or refusals occur, transfer to manual.

### PAYMENT-UNAUTHORIZED｜Unauthorized transaction

Do not admit responsibility or accuse fraud; lock high-risk actions; advise customers to contact the card issuer and protect the account; immediately refer to the risk control/payment team.

### PAYMENT-VERIFY｜Payment/Order Verification

Provide a discloseable portion of the reason for order hold; use approved secure verification channels; do not ask for full card number, CVV, verification code, or ID email attachments.

### INVOICE-ISSUE｜Receipts and Invoices

Check the order, header, tax number, address and local rules; if it can be generated, explain the delivery method; if correction is needed or the window has passed, please refer to Finance and give an estimate.

### TAX-DUTY｜Taxes and duties

Distinguish between checkout taxes, import duties, carrier fees and estimates; quote orders and policies; do not provide personal tax/tariff legal advice, and refer disputes to finance or local agencies.

### GIFTCARD-HELP｜Gift Cards and Balance

Verify purchase records and status; do not display full codes in emails; provide safe activation/balance/replacement paths; immediately refer suspected theft to the security team.

## Order management

### ORDER-CONFIRM｜Confirmation and receipt

Confirm whether the order is created, pay and send a confirmation letter; resend it to a verified email address; use `NEED-ORDER` when it cannot be found to avoid exposing similar orders.

### ORDER-DUPLICATE｜Duplicate order

List the time, product and status of the suspected duplicate order; apply for cancellation if it has not been shipped and is allowed; indicate the return path if it has been shipped; permission is required for refund actions.

### ORDER-CANCEL｜Orders can be canceled

Check the non-fulfillment status and cancellation policy; execute or submit cancellation if it meets the requirements; explain the refund method and time limit; there is no guarantee that orders that have been processed by the warehouse will be intercepted.

### ORDER-CANCEL-LATE｜Has been shipped/cannot be canceled

Clarify the current fulfillment status and reasons for failure to intercept; provide options and fees for rejection or return after receipt; transfer emergency address/security issues to logistics and labor.

### ORDER-EDIT｜Modify product/quantity/variation

Check whether the order can still be edited, inventory, price difference and tax; if it can be edited, confirm the change list; if it cannot be edited, provide a path to cancel the re-order or exchange the goods.

### ADDRESS-CHANGE｜Change address

Verify identity first; check warehouse and carrier status; can be changed to confirm the masked summary of the new address, cannot be changed to provide the carrier/return to sender path.

### SHIPPING-METHOD-CHANGE｜Shipping method modification

Check whether the contract has been fulfilled, available services and price differences; if it can be changed, the fee and new time limit will be stated; if it cannot be changed, there is no guarantee of carrier upgrade.

### ORDER-HOLD｜Order on hold

Explain the disclosable reasons for the suspension, what the customer needs to do and the deadline; risk details will not be disclosed; the order status will be confirmed after resolution.

### ORDER-SPLIT｜Split/combine orders

Explain the relationship between orders and packages, the products of each package and tracking; explain restrictions and fees when merging/splitting; avoid mistaking partial shipments as missing parts.

### ORDER-GIFT｜Gift remarks/packaging

Check whether it can still be added or modified, whether it is charged, and whether the price is displayed with the package; if it cannot be modified, provide a feasible alternative.

## Shipping and Distribution

### SHIP-STATUS｜In transit status

Give the verified carrier, latest scan, tracking link, estimated window and next checkpoint; "label created" must clearly not be received.

### SHIP-NOT-SENT｜Not shipped yet

Explain the current fulfillment stage, expected window and blockage of the order/commodity; provide cancellation or upgrade options when the commitment is exceeded; pre-sale/out-of-stock items must be explained separately.

### SHIP-DELAY｜Transportation delay

Acknowledge the delay; list the latest scan and known reasons; provide a new reasonable window, carrier investigation, or refund/reissue eligibility path.

### SHIP-LOST｜Suspected lost item

Check the final scan and lost item thresholds; initiate a carrier investigation; explain the investigation period and reissue/refund conditions; transfer high-value or abnormal cases to manual work.

### SHIP-DNR｜Shows delivered but not received

Check the delivery time, address masking summary, photos/signature; ask customers to check the safe location, front desk or family; also initiate an investigation according to policy to avoid putting customers at risk of searching.

### SHIP-FAILED｜Delivery failed

Explain the reason for the failure and the next delivery/pickup option; provide official channels; explain the return and resend fees if the address is wrong or fails multiple times.

### SHIP-RTS｜Return to sender

Indicate reason for return and current location; provide reship or refund options, fees, and address verification requirements; do not promise payment until return is confirmed.

### SHIP-PARTIAL｜Partial shipment

List shipped and unshipped goods by package; track or estimate shipments for each; check out-of-stock, free gifts, and multi-warehouse status.

### SHIP-DAMAGE｜Shipping packaging damaged

It is recommended to take photos of the outer box, label and product under the premise of safety; distinguish packaging damage from product damage; provide reissue, return or carrier investigation according to the policy.

### SHIP-CUSTOMS｜Customs/Duty Detention

Explain the shipping status, required documents or fees and who is responsible; only provide official channels; explain return and refund rules if customs clearance cannot be achieved.

### SHIP-PICKUP｜Store pickup/local delivery

Indicate the preparation status, location, time period, pickup verification and retention period; the person picking up or modifying the goods needs to be verified according to the security process.

## Abnormal delivery and product quality

### ITEM-WRONG｜Received wrong item

Verify order line items and photos; apologize and explain the approval process for no/required returns; and provide options for reissue, exchange, or refund of the correct merchandise.

### ITEM-MISSING｜Missing parts/missing accessories

First eliminate splitting orders, sending extra gifts and packaging interlayers; collect necessary photos/weight information; provide reissue, refund or accessory delivery.

### ITEM-DAMAGED｜Damaged upon arrival

Prioritize safety; collect necessary photos and batches; provide exchange, reissue or refund; use `SAFETY-ESCALATE` for suspected safety risks.

### ITEM-DEFECT｜Functional failure

Confirm symptoms, model, serial/batch and steps attempted; only give safe approval for troubleshooting; enter repair, replacement or refund path if invalid.

### ITEM-NAD｜Not as described

Compare product pages, variations and actual products when ordering; acknowledge verified differences; offer exchanges, returns or refunds; synchronize product page errors to the content team.

### ITEM-FIT｜Size/color/fit issues

Use neutral language; check variations with size charts; differentiate between shipping errors, describe problems and personal fit; offer exchanges/returns or usage suggestions.

### ITEM-QUALITY｜Unsatisfied with quality/performance

Clarify observable problems and usage conditions; compare promised specifications and maintenance requirements; provide troubleshooting, warranty, return or manual quality inspection paths.

### ITEM-EXPIRY｜Expiration, expiration or hygiene issues

Verify batches, dates, sealing and storage; recommend discontinuation of suspect merchandise; offer replacements/refunds and upgrade the quality team.

## Returns, Exchanges and Refunds

### RETURN-ELIGIBLE｜Eligible for returns

Describe applicable periods and eligibility; provide return portal/address, labels, packaging, fees, and deadlines; indicate when refunds are triggered.

### RETURN-EXCEPTION｜Suspected non-compliance/exception

Be specific about the relationship of item, time or condition to terms; check mandatory rights and defect exceptions first; offer exchanges, repairs or manual review, and prohibit ending with a "final sale".

### RETURN-LABEL｜Label/address issue

Check return records; reissue valid labels or secure addresses; indicate carrier, expiration date and label fees; clearly indicate when old labels are expired.

### RETURN-STATUS｜Return is being processed

Provide the shipping scan, warehouse receipt/quality inspection status, and estimated refund node; if it times out, it will be upgraded, and "sent" will not be written as "refunded".

### RETURN-REFUSED｜Return rejected

Explain the quality inspection results and evidence that can be disclosed; quote terms; provide appeals/manual review and product return arrangements, and do not destroy disputed products.

### EXCHANGE-REQUEST｜Exchange application

Check eligibility, target variant inventory, spreads, fees, and retention rules; create exchanges or provide return re-routing.

### EXCHANGE-STATUS｜Exchange status

List returned items, quality inspections, replacement items, and tracking status; provide refunds or alternative options when inventory changes.

### RETURN-GIFT｜Gift return and exchange

Securely verify gift orders; do not disclose unnecessary buyer information to recipients; indicate refunds, gift points, or exchange options.

### RETURN-INTERNATIONAL｜Cross-border returns

Describe the approved shipping method, customs declaration description, taxes/duties, return address and time limit; transfer high-value or restricted categories to labor.

### REFUND-ISSUED｜Refund initiated

Clarify the amount, currency, date of initiation, original payment method and expected credit range; explain that the merchant cannot control the speed of bank credit; provide a contact path after timeout.

### REFUND-PENDING｜Refund status tracking

Check refund processor status; give reference number (when disclosable), number of days elapsed and next checkpoint; transfer to finance if out of range.

### REFUND-FAILED｜Refund failed/returned

Explain that failure status can be disclosed; do not change to other accounts without authorization; alternative paths will be handled by the payment team after the customer is verified.

### REFUND-PARTIAL｜Partial refund

Explain item by item, tax, freight, discount, and return fee; check and recalculate activities; upgrade and correct calculation errors if found.

### REFUND-CREDIT｜Store Credit/Gift Card Refund

Explain the amount, validity period, restrictions and irreversibility; it can only be used when the customer agrees and the policy allows, and cannot be used to pretend to be the original refund.

### REFUND-COSTS｜Freights, taxes and duties refunds

Distinguish between standard shipping charges, expedited shipping charges, return shipping charges, taxes and import charges; explain the refundable range by region and policy.

### REFUND-COMP｜Compensation and goodwill plan

Acknowledge the experience; provide optional compensation within the authorized limit; explain whether this affects return/legal rights; transfer approval if the limit is exceeded.

## Warranty, Maintenance and Safety

### WARRANTY-COVER｜Warranty Qualification

Distinguish between legal guarantee, manufacturer warranty, merchant extended warranty and insurance; check the purchase date, serial number, faults and exceptions; provide next step materials.

### REPAIR-FLOW｜Repair Process

Explain safe deactivation, data backup, delivery/door-to-door method, cost, cycle and status inquiry; no guidance on unapproved disassembly and repair will be provided.

### PARTS-FLOW｜Accessories/Parts

Check model, part number, inventory and compatibility; provide reshipment, purchase or repair solutions; transfer safety critical parts to technical team.

### REPLACEMENT-FLOW｜Warranty replacement

Explain the first return and then exchange/first exchange and then return, deposit, inventory, replacement status and new warranty starting point; high value exceptions will be transferred to labor.

### RECALL-FLOW｜Recall

Verify official recalls, batches and remediations; request discontinuation of use; provide official refund/repair/replacement/disposal procedures; log safety cases immediately.

### INJURY-FLOW｜Injury or accident

Focus on safety first and recommend necessary local emergency/medical help; do not diagnose, do not admit legal responsibility; collect minimal incident information and escalate immediately.

## Subscriptions, Digital Goods, Accounts and Privacy

### SUB-CANCEL｜Cancel subscription

Check subscriptions, next charges and generated orders; confirm cancellation of future renewals; separately indicate whether the current order is refundable/cancellable.

### SUB-PAUSE｜Pause/Skip/Reschedule

Check the deadline and next performance; confirm the specific cycle and recovery date; provide cancellation or return paths if changes cannot be made.

### SUB-CHANGE｜Modify subscription

Check product, quantity, frequency, address and price changes; list before and after changes; perform high-impact changes only after customer confirmation.

### SUB-BILLING｜Renewal and trial deduction

Check the consent record, trial end, deduction date and cancellation status; transfer payment/labor without authorization or dispute; do not hide important terms.

### DIGITAL-DELIVERY｜Digital content not received

Check delivery logs, email addresses and eligibility; resend secure links or resume downloads; do not expose full license keys in emails.

### DIGITAL-ACTIVATE｜Activation/Licensing Failure

Check the platform, device, version and errors; provide approval troubleshooting; report abnormal license status to the technical team.

### DIGITAL-REFUND｜Refund for digital goods

Check the download, activation, usage, consent records, merchant policies and regional rights; if they are consistent, a refund will be issued; if they are not clear, manual review will be performed.

### ACCOUNT-ACCESS｜Login and account access

Provide official reset and security check; do not ask for passwords or verification codes; lock sensitive actions and refer to the security team when a takeover is suspected.

### ACCOUNT-PROFILE｜Merge data and account

Verify identity; explain modifiable fields, impact on orders and irreversible matters; account merging/deletion transfer to controlled process.

### PRIVACY-REQUEST｜Access/deletion/correction and other rights requests

Confirm receipt and request scope; give case number and security verification method; refer to privacy manager and track deadline; do not attach large amounts of data to regular emails.

### SECURITY-PHISHING｜Phishing or account security

It is recommended not to click on suspicious links, use official sites instead, change passwords and enable MFA; log suspicious emails; and contact the security team immediately.

### UNSUBSCRIBE｜Marketing Unsubscribe

Confirm that marketing preferences have been submitted or completed; indicate that transactional and secure emails may still be sent; and set no login, payment, or additional identity barriers.

## Promotion, membership, platform, B2B and feedback

### PROMO-VALIDATE｜Promotion qualifications

Check the code, product, region, channel, threshold, time and overlay; if they are consistent but fail, repair/compensate, and if they are not consistent, give specific reasons.

### PROMO-EXPIRED｜Event ends/no stacking

Indicate the verified end time or conflicting rules; do not forge extensions; provide currently valid alternatives within the scope of authorization.

### LOYALTY-ADJUST｜Points/Levels/Rewards

List earning, revocation, expiration, refund and adjustment records; confirm modifications and effective time; transfer to member team if abnormal.

### REFERRAL-FLOW｜Recommendations and Rebates

Check recommenders, invitees, attribution time, qualifications and anti-cheating status; only disclose necessary information; disputes will be transferred manually.

### MARKETPLACE-ROUTE｜Platform/Third Party Seller

Confirm the sales entity and order ownership; explain the actions that the merchant can perform; provide platform cases or contact paths for actual sellers, without kicking the ball.

### B2B-QUALIFY｜Wholesale/Corporate Procurement

Confirm the company, region, product, quantity, delivery date, tax and customization requirements; transfer to the sales/wholesale team and do not commit to price or billing period without approval.

### B2B-QUOTE｜Quotation/PO/account period

Explain the quotation validity period, currency, tax, MOQ, delivery date and payment terms; changes require a new quotation; credit approval and contract sub-authorization team.

### FEEDBACK-POSITIVE｜Positive feedback

Sincerely thank and specifically respond to customer points; record feedback as configured; do not take the opportunity to ask for public praise unless there is an approval process in place.

### COMPLAINT-RECOVER｜General complaint recovery

Restate the problem, acknowledge the impact, and summarize the verified facts; give specific remedies and responsible persons; promise the next update time instead of a vague "will provide feedback."

### MANAGER-ESCALATE｜Manager/manual upgrade

Confirm the customer's requirements; summarize the case and completed actions; immediately transfer to the manual queue and provide the case number; do not force the customer to accept the automatic plan first.

### LEGAL-ESCALATE｜Legal/Regulatory/Media

Only confirm receipt, no debate, no responsibility, no commitment to results; preserve threads and evidence; transfer to the person in charge of legal affairs, compliance or public relations.

### CHARGEBACK-ESCALATE｜Chargeback/Dispute

Confirm that it has been recorded; avoid repeated refunds or disputes; transfer the payment dispute team to check the time limit and evidence; do not give customers internal risk control details.

### ACCESSIBILITY-FLOW｜Accessibility/Language Support

Identify barriers; provide assistance in accessible formats, alternative channels, or languages; prioritize upgrades when affecting purchases/entitlements without blaming customer equipment or capabilities.

