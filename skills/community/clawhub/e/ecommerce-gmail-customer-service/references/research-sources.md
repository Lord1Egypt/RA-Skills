# Research sources and applicable boundaries

Last verification: 2026-07-26. The following information is used to design categories, workflows, and default rules. Regulations change with regions and time; the actual response must reconfirm the applicable region, current version and merchant policy. This document does not constitute legal advice.

## E-commerce work order classification and practical operation

- [Gorgias Customer Intents](https://docs.gorgias.com/customer-intents-5742285): Provides real e-commerce intent baselines such as order cancellation/modification/damaged/wrong parts, refund request/status, return request/status, logistics status/abnormality, product issues/recommendations, inventory and subscriptions, etc.
- [Gorgias Order Management](https://www.gorgias.com/product/order-management): Supports viewing order history first, and then performing refund, cancellation, inventory and new order operations; used for process design of "get context first and then reply".
- [Gorgias Order Management 101](https://docs.gorgias.com/en-US/order-management-101-81861): Return and cancellation buttons submit requests instead of automatically completing actions; used for default draft and manual approval access control.
- [Shopify Returns and exchanges](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns): Distinguish refund, return, exchange and fulfilled/unfulfilled qualifications.
- [Shopify Refunding orders](https://help.shopify.com/en/manual/orders/refund-cancel-order): Notes on full/partial refunds, original payment methods, gift cards and irreversible refunds.
- [Shopify Canceling orders](https://help.shopify.com/en/manual/fulfillment/managing-orders/canceling-orders): The relationship between cancellation, refund, and fulfillment status.
- [Shopify Subscription fulfillment](https://help.shopify.com/en/manual/fulfillment/fulfilling-orders/subscriptions-fulfillment): Prepaid subscription, recurring fulfillment, cancellation and refund are different operations.
- [Etsy Help with an order](https://help.etsy.com/hc/en-us/articles/4402660818583-How-to-Get-Help-with-An-Order): Customer issues such as order status, address modification, order changes, refunds, returns, and cancellations.
- [Etsy Purchase Protection](https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program): non-receipt, damage, delay and not as described differences, and marketplace liability boundaries.

## Gmail, Google OAuth and OpenClaw

- [gogcli official README](https://github.com/steipete/gogcli/blob/main/README.md): Desktop OAuth client, `gog auth credentials`, `gog auth add`, Gmail scope, key chain and automatic refresh. The actual command is subject to the local `gog --help`.
- [Gmail API Python quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python): Enable Gmail API, configure OAuth consent screen and Desktop app client.
- [Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes): `gmail.modify` can read, write/send letters, and belongs to restricted scope; public applications may require verification and security assessment.
- [Google OAuth app audience](https://support.google.com/cloud/answer/15549945): Test users for External + Testing with 7-day authorization/refresh token period.
- [Google OAuth policies](https://developers.google.com/identity/protocols/oauth2/policies): requirements for least privileges, separation of test and production projects, accurate identity, and secure browsers.
- [OpenClaw Cron](https://docs.openclaw.ai/cli/cron): Agent cron, explicit `--agent`, timezone, disable/enable and run history.
- [OpenClaw Skills](https://docs.openclaw.ai/skills): Local Skill discovery, environment filtering and installation behavior.

## Consumer Rights and Distance Selling

- [China's Interim Measures for Seven-Day Return of Goods Purchased Online without Reason](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/art/2023/art_26ca8fe29e184edd899fa0a7a060d935.html): seven-day starting date, integrity standards, exceptions, return information, price refund and freight rules.
- [China Consumer Rights Protection Law](https://www.samr.gov.cn/zfjcj/tzgg/art/2023/art_615af9ed6bcd4974bf853dd2e02bc663.html): Quality non-compliance, remote sales disclosure and platform transaction responsibilities.
- [EU Returns and right of withdrawal](https://europa.eu/youreurope/citizens/consumers/shopping/returns/index_en.htm): Remote contract 14-day withdrawal period, return fees and exceptions.
- [EU B2C distance selling](https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm): Refunds, standard shipping fees, 30-day delivery and risk assumption.
- [EU Consumer guarantees](https://europa.eu/youreurope/business/selling-in-eu/consumer-contracts-guarantees/consumer-guarantees/index_en.htm): Statutory guarantees and remedies for goods that are defective or not as described.
- [UK Accepting returns and giving refunds](https://www.gov.uk/accepting-returns-and-giving-refunds): Online order notifications, return and refund time limits and standard delivery charges.
- [US FTC Mail Internet or Telephone Order Rule guide](https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule): Promised shipping times, delay notifications, cancellations, refund amounts and records.
- [Australia ACCC repair replace refund cancel](https://www.accc.gov.au/consumers/problem-with-a-product-or-service-you-bought/repair-replace-refund-cancel): Consumer guarantees and remedies for non-conforming goods.

## Privacy, Payments, Email & Security

- [ICO Data minimisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/): Personal data should be sufficient, relevant and limited to what is necessary.
- [ICO Storage limitation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/): retention period, periodic review, deletion or anonymization.
- [ICO Subject access response](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/right-of-access/what-should-we-consider-when-responding-to-a-request/): Identification, authentication and typical one-month response period.
- [PCI SSC Small Merchant Guide to Safe Payments](https://www.pcisecuritystandards.org/documents/Small_Merchant_Guide_to_Safe_Payments.pdf): Do not accept payment card information via email and should be directed to an approved secure payment channel.
- [FTC CAN-SPAM compliance guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business): Distinguish transactional/relationship emails from commercial marketing emails, marketing unsubscribes vs. accurate header requirements.
- [CFPB credit card billing mistakes](https://www.consumerfinance.gov/consumer-tools/credit-cards/how-to-fix-mistakes-in-your-credit-card-bill/): Unauthorized, billing errors and cardholder dispute paths; customer service shall not prevent customers from contacting the card issuer in accordance with the law.
- [CPSC duty to report](https://www.cpsc.gov/Business--Manufacturing/Recall-Guidance/Duty-to-Report-to-CPSC-Rights-and-Responsibilities-of-Businesses): Serious injury risks, defects and product safety information need to be updated immediately and cannot be closed as a normal return.

## Version risk record

- The 2024 U.S. FTC “Click-to-Cancel” revised rules were later revoked by the court; the FTC re-solicited opinions on the negative option rules in 2026. The default prompt word therefore only requires compliance with current applicable laws and merchant policies, and does not write the 2024 rules into current national unified obligations. See [FTC current Negative Option Rule page](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule).
- Google, OpenClaw and `gog` CLI will be updated. The installation boot requires the use of native `--help` to verify syntax, and considers version changes as a retest trigger.

