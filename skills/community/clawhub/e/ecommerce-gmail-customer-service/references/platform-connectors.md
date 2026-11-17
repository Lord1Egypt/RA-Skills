# Commerce platform API capability and credential guide

## Purpose and non-negotiable boundary

Use this guide only after the merchant has selected or confirmed its real order system in onboarding. It has two purposes:

1. Show the merchant the relevant **official** documentation and the vendor's supported data capabilities.
2. Guide the merchant or its authorized technical operator to create or retrieve the minimum credential needed by an approved connector.

Public storefront discovery remains separate. It may read public product pages, campaign copy, and policy pages, but it cannot retrieve a private order, customer record, fulfillment, tracking event, payment, private inventory, or a customer-specific promotion. Do not log in to a merchant admin page or scrape an authenticated page as a substitute for an API.

This is an API capability map, **not** a claim that this Skill already implements every platform. The bundled Skill currently has no native Shopify, WooCommerce, Amazon SP-API, eBay, Etsy, Walmart, BigCommerce, or Wix connector; it has no OAuth callback service and stores no platform secret. A selected platform still needs an approved external connector that conforms to [merchant-data-contract.md](merchant-data-contract.md). Until that connector passes the test below, private data remains unavailable and the Agent must create a draft or transfer the case to manual work.

In the table below, `R` means the vendor exposes a relevant read operation and `W` means the vendor exposes at least one related write operation. `R/W` is a statement about the vendor API only. This Skill starts every connector read-only and does not activate a vendor write operation merely because it exists.

| Platform | Orders | Customers | Logistics / tracking | Products / listings | First connection model |
| --- | --- | --- | --- | --- | --- |
| Shopify | R/W | R/W | R/W fulfillment and tracking | R/W | Scoped Admin API app token |
| WooCommerce | R/W | R/W | R/W shipping zones and methods; carrier tracking is extension/carrier-specific | R/W | Store REST API key for a WordPress user |
| Amazon | R; no generic order write baseline | Order-associated buyer/recipient data only, subject to restricted roles | R package/fulfillment data; write is program/API-specific | Catalog R; seller listings R/W | SP-API app authorization, LWA credentials and seller authorization |
| eBay | R | Order-associated buyer data only | R/W fulfillment and tracking submission | R/W inventory and listings | Developer app plus OAuth user token |
| Etsy | R receipts/orders | Order-associated buyer data only | R/W receipt shipment/tracking | R/W listings | Developer app plus OAuth 2.0 with PKCE |
| Walmart Marketplace | R/W order lifecycle | Order-associated buyer data only | R/W shipping/fulfillment; inventory R/W | R/W items, catalog and inventory | Seller or approved-provider OAuth 2.0 connection |
| BigCommerce | R/W | R/W | R/W order shipments | R/W catalog | Store API account or OAuth app with scoped token |
| Wix | R/W | R/W Wix Contacts | R/W order fulfillment | R/W products and variants | Wix app OAuth with app-instance authorization |

### Marketplace customer-data limitation

Amazon, eBay, Etsy, and Walmart Marketplace are not generic customer CRMs. Their buyer data is normally returned only with an authorized order and can be incomplete or restricted by marketplace privacy rules. For these platforms, an adapter may support `find_customer` and customer-scoped `list_recent_orders` only when it can safely resolve the customer from a verified order number, platform buyer identifier, or permitted order-associated data. It must not claim that an arbitrary email address is searchable or that arbitrary customer-history lookup is available. If a verified match is unavailable, return a structured no-match/insufficient-permission result and keep the case in draft/manual mode.

## Onboarding sequence after a platform is selected

Perform this sequence one platform at a time. A merchant that sells through several platforms needs a separate source, account identifier, scope review, and test result for each one.

1. Confirm the actual platform, merchant/store or seller account, production versus sandbox environment, and whether a compatible external connector already exists. A platform marker found on a public page is only a hint, never authorization.
2. Open the selected platform's official links below and show the merchant the relevant capability row. Explain both the available vendor operations and the limitations, especially any marketplace buyer-data limitation.
3. Ask the current owner to choose one of two paths:
   - **Existing approved connector:** the owner authorizes that connector in the platform's official consent or API-key flow. Confirm exactly which read operations and data fields it supports.
   - **Custom connector:** an authorized technical operator registers/installs the vendor app or creates the vendor credential using the linked official guide. The operator must request only the read scopes needed for `find_customer`, `list_recent_orders`, `get_order`, `get_product`, `list_campaigns`, and `list_policies` that the platform can actually supply.
4. The Agent may explain the portal steps and link to them, but it must not create an app, click consent, receive a secret in chat, or copy a token from a page. The merchant/operator performs those actions while signed in to the platform.
5. Put raw secrets only in the connector's approved OS keychain, secret manager, or deployment-secret store. Do **not** put a client secret, API key, access token, refresh token, authorization code, private key, or password in Gmail, chat, `user_memory.md`, a report, this repository, an Agent workspace, `config.json`, a command line, or a browser-discovery file. The onboarding record may retain only a non-secret secret-manager reference.
6. Record non-secret connection metadata in the connector's controlled configuration: platform, store/seller/account identifier, production or sandbox, connector name/version, official-doc URL, granted read capabilities/scopes, secret-manager reference, and verification time. Do not record the secret value.
7. Test the connector with a controlled or masked case. It must return structured JSON, source name, retrieval time, stable IDs, and the fields required by [merchant-data-contract.md](merchant-data-contract.md). Do not use a live write request as a connection test.
8. If a platform cannot provide a required field, or the connector has an authorization/schema/timeout error, record the limitation and fail closed. Use the public source only for public facts; do not guess private order, buyer, tracking, entitlement, or historical-policy facts.

### Initial permission rule

The initial connection is read-only. Request only the smallest vendor scopes that support the approved read operations, normally orders, products/listings, customers where a first-party customer resource exists, and fulfillment/tracking read where required. Do not request a write scope merely for future convenience. A later write capability needs a separately designed connector, explicit owner approval, the existing optional-write controls in [merchant-data-contract.md](merchant-data-contract.md), and retesting; it is not enabled by this onboarding flow.

## Platform cards

### Shopify

- **Official docs:** [Admin GraphQL order query and order access](https://shopify.dev/docs/api/admin-graphql/latest/queries/order), [GraphQL Admin API setup and read scopes](https://shopify.dev/docs/apps/build/graphql/basics/queries), and [access-token guidance](https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/generate-app-access-tokens-admin).
- **Vendor capability:** The Admin GraphQL API exposes orders with customer, line-item, financial, and fulfillment information; it also has Customer, Product, and fulfillment resources. Shopify's order object supports updates, returns, exchanges, refunds, and fulfillment workflows, subject to the corresponding scopes. By default, only the most recent 60 days of orders are available; older history requires approved all-orders access.
- **Credential path:** Select the app model supported by the connector. For an existing compatible admin-created app, follow Shopify's current Admin API configuration and installation guidance. For a new integration, use Shopify's current developer/app flow rather than relying on an obsolete admin-screen path. Start with the current equivalent of `read_orders`, `read_customers`, and `read_products`; add fulfillment-read and older-order permission only when the approved support use case requires them. Store the generated token only in the connector's secret manager.
- **Connector note:** A public `myshopify.com` or storefront marker proves neither store ownership nor API access. Do not ask for `write_*` scopes during this onboarding path.

### WooCommerce

- **Official docs:** [WooCommerce REST API](https://developer.woocommerce.com/docs/apis/rest-api/), [REST API authentication and key permissions](https://developer.woocommerce.com/docs/apis/rest-api/authentication), and [API overview](https://developer.woocommerce.com/docs/apis/).
- **Vendor capability:** The authenticated WC REST API can create, read, update, and delete orders, products, customers, coupons, and shipping zones/methods. It exposes order shipping fields, but package-level carrier tracking is not a universal core endpoint; the connector must use the merchant's approved tracking extension, fulfillment system, or carrier source when needed.
- **Credential path:** An authorized WordPress/WooCommerce administrator opens **WooCommerce > Settings > Advanced > REST API**, adds a key for a user who has the necessary order/product access, and selects **Read** permission for the initial connector. The consumer key and consumer secret are shown when generated; place them directly in the connector's secret store because the secret is not safely recoverable from this Skill.
- **Connector note:** Do not give the connector a WordPress administrator login. Do not choose `Read/Write` just because WooCommerce supports writes.

### Amazon Selling Partner API (SP-API)

- **Official docs:** [SP-API registration overview](https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/sp-api-registration-overview), [developer onboarding and authorization](https://developer-docs.amazon.com/sp-api/docs/onboarding-overview), [Orders API filtering and PII roles](https://developer-docs.amazon.com/sp-api/lang-en_US/docs/get-orders-with-filtering-criteria), and [product listing role example](https://developer-docs.amazon.com/sp-api/docs/search-available-product-type-definitions).
- **Vendor capability:** The Orders API reads marketplace orders and, with the applicable role, fulfillment/package data. Buyer and shipping-address data are restricted PII: the current Orders documentation requires approved restricted roles for that data. There is no generic customer CRUD resource. Catalog/product-definition APIs are read-oriented; seller listings are managed through the listing-related APIs and roles. Shipment creation or other writes are program-specific and are outside the baseline support connector.
- **Credential path:** The merchant chooses an existing approved SP-API connector or an authorized developer registers a private/public SP-API application, selects only the roles required, and obtains selling-partner authorization. A usable connector normally manages LWA client credentials and a refresh token in its secret store. Do not request restricted PII roles unless the documented customer-service use case actually needs buyer/recipient data, and do not paste LWA/AWS credentials or refresh tokens into chat.
- **Connector note:** Read order basics first. Treat missing PII permission, marketplace/region mismatch, or unavailable package data as a manual-review condition, not an invitation to scrape Seller Central.

### eBay

- **Official docs:** [OAuth authorization and user-token guide](https://developer.ebay.com/develop/guides-v2/authorization), [Sell Fulfillment API](https://developer.ebay.com/develop/api/sell/fulfillment_api), and [Sell Inventory API](https://developer.ebay.com/develop/api/sell/inventory_api).
- **Vendor capability:** The Sell Fulfillment API reads seller orders and supports fulfillment/tracking submission. The Sell Inventory API manages seller inventory and listings. Buyer information is order-associated and constrained by the platform response and policy; it is not a general customer directory.
- **Credential path:** An authorized developer creates an eBay Developer Program application keyset for the correct Sandbox or Production environment, configures the redirect URL name (RuName) when user authorization is needed, and completes the OAuth authorization-code flow with only the endpoint scopes required by the connector. Seller-specific orders require a user token, not merely an application token. The connector stores client secret and refresh token securely.
- **Connector note:** Keep Sandbox and Production credentials separate. Use the endpoint documentation to choose scopes; do not copy a broad sample scope list merely because the portal displays one.

### Etsy

- **Official docs:** [Etsy Open API v3 reference](https://developers.etsy.com/documentation/reference), [authentication](https://developers.etsy.com/documentation/essentials/authentication/), and [developer documentation overview](https://developers.etsy.com/documentation/).
- **Vendor capability:** Shop receipts provide order data with `transactions_r`; buyer address fields can be subject to regional preferred-partnership restrictions. `createReceiptShipment` submits shipping/tracking information with `transactions_w`. Listings have separate read/write scopes. Etsy does not expose a general customer CRM for arbitrary buyer lookup.
- **Credential path:** An authorized developer registers the app in Etsy's Developer Portal and implements Etsy OAuth 2.0 with PKCE, which Etsy requires for every authorization flow. Start with `transactions_r` and `listings_r` only when those reads are needed. Do not request `transactions_w` or listing-write scopes during the initial support connection.
- **Connector note:** The app key, OAuth tokens, and refresh material are secrets. A receipt's buyer data must not be repurposed as a standalone customer database.

### Walmart Marketplace

- **Official docs:** [seller getting-started and API keys](https://developer.walmart.com/us-marketplace/docs/get-started-as-a-seller), [OAuth 2.0 authorization](https://developer.walmart.com/us-marketplace/docs/oauth-20-authorization), [Orders API selection](https://developer.walmart.com/us-marketplace/docs/choose-an-orders-api), [API scopes](https://developer.walmart.com/us-marketplace/docs/api-scope-walmart-marketplace), and [item/inventory integration](https://developer.walmart.com/us-marketplace/docs/integrate-with-marketplace-apis).
- **Vendor capability:** Marketplace APIs support an order lifecycle including retrieval, acknowledgement, shipping, cancellations, and refunds; buyer details are associated with orders rather than a general customer API. Item and inventory APIs retrieve and manage catalog items, content, and stock. WFS has additional fulfillment/tracking operations where applicable.
- **Credential path:** For an approved external connector, the merchant uses Seller Center's app/OAuth connection flow and authorizes only the required categories (for example Orders, Items, Inventory). For a direct seller-managed integration, an authorized account retrieves the `Client ID` and `Client Secret` in the Developer Portal/API Key Management flow. New solution-provider integrations should use the current OAuth path rather than assuming legacy delegated credentials are available.
- **Connector note:** Never send the Client Secret by email or chat. Keep sandbox and production credentials separate, and test with a non-writing order/product read.

### BigCommerce

- **Official docs:** [API accounts and OAuth scopes](https://developer.bigcommerce.com/docs/start/authentication/api-accounts), [Orders and shipments API](https://developer.bigcommerce.com/docs/rest-management/orders), [Customers API](https://developer.bigcommerce.com/docs/rest-management/customers), and [Catalog API](https://developer.bigcommerce.com/docs/rest-management/catalog).
- **Vendor capability:** REST Management APIs provide order, customer, catalog, and order-shipment operations, including related write endpoints. BigCommerce documents read-only OAuth scopes for limiting an API account to safe HTTP reads.
- **Credential path:** For one store, an authorized owner may create a store-level API account at **Settings > Store-level API accounts** and select only the required read-only Orders, Customers, Products/Catalog, and shipment-related scopes. For a reusable connector, use the documented app-level OAuth flow so each store authorizes its own token. Store the access token and client secret in the connector's secret manager.
- **Connector note:** Store-level credentials are powerful and long-lived. Give the connector the minimum scopes and create a separate account for this connector rather than reusing an unrelated integration's token.

### Wix

- **Official docs:** [Orders API](https://dev.wix.com/docs/api-reference/business-solutions/e-commerce/orders/orders/sample-flows), [order fulfillment overview](https://dev.wix.com/docs/api-reference/business-solutions/e-commerce/orders/introduction), [Contacts API](https://dev.wix.com/docs/api-reference/crm/members-contacts/contacts/introduction), [Products API](https://dev.wix.com/docs/api-reference/business-solutions/stores/catalog-v3/products-v3/introduction), [Wix OAuth authentication](https://dev.wix.com/docs/build-apps/develop-your-app/access/authentication/authenticate-using-oauth), and [app permissions](https://dev.wix.com/docs/build-apps/develop-your-app/access/authorization/configure-permissions-for-your-app).
- **Vendor capability:** Wix Orders supports viewing, searching, updating, canceling, and creating orders; order-fulfillment APIs manage shipping, delivery, and tracking. Wix Contacts is the first-party customer/contact resource, and the Products API creates, updates, deletes, and queries products and variants.
- **Credential path:** A compatible connector is a Wix app. Its authorized developer records the app ID and secret in the connector's secret store and obtains the site-specific app instance ID after installation. The site owner installs the app and approves only the endpoint permissions required; Wix then issues access tokens for the authorized app instance. The Agent may link to the official steps, but it must not receive the app secret or approval token.
- **Connector note:** The order endpoint itself declares its required permission (for example, Read Orders or Manage Orders). Select read permissions only for the initial connection and keep app-instance access separate for each site.

## Connection verification checklist

Before Phase 5 can pass, show the merchant a masked test result for every configured platform and verify all of the following:

- The connector identifies the exact platform, account/store or seller ID, environment, and official source.
- It can retrieve a controlled order and its line items without making a change.
- It returns fulfillment/tracking only when the platform/source actually exposes it; otherwise it returns a clear unavailable result.
- It supports customer lookup only to the extent stated above, with a verified match method and no fabricated customer identity.
- It can retrieve the product/listing fields required for the case, while public product/policy/campaign pages remain separately source-traceable.
- It never puts customer input into shell, SQL, or a URL without parameterization, and it never logs secrets or raw sensitive fields.
- Any write operation remains disabled. If the connector configuration, scopes, or platform changes later, return to draft mode and rerun this checklist.
