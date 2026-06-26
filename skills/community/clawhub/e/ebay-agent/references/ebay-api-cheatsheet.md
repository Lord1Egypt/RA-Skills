# eBay REST API Cheatsheet

**A concise, copy-paste-ready reference for the eBay REST APIs: authentication, key endpoints, request/response examples, and condition codes.**

This cheatsheet is for developers integrating with eBay's REST APIs. It covers the Browse API (searching listings), Inventory API (creating listings), Catalog API (product lookup), Fulfillment API (post-sale order management), and Notification API (webhooks). Each section includes the base URL, key endpoints, and working request examples. Assumes basic familiarity with REST APIs and OAuth 2.0.

---

## Authentication (OAuth 2.0)

eBay uses OAuth 2.0 with two grant types depending on what you need to access.

### Two Auth Flows

| Flow | Grant Type | Use Case | User Consent Required? |
|---|---|---|---|
| Client Credentials | `client_credentials` | App-level access: searching, browsing, catalog lookups | No |
| Authorization Code | `authorization_code` | User-level access: listing items, managing orders, fulfillment | Yes |

### Getting Credentials

1. Create an account at [developer.ebay.com](https://developer.ebay.com).
2. Create an application to get your **App ID** (Client ID) and **Cert ID** (Client Secret).
3. For user-level access: redirect the user to eBay's consent URL, receive an authorization code, exchange it for tokens.

### Token Lifetimes

| Token | Validity |
|---|---|
| Access token | 2 hours |
| Refresh token | 18 months |

### Token Refresh Example

```python
import httpx

def refresh_access_token(refresh_token, app_id, cert_id):
    response = httpx.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        auth=(app_id, cert_id),
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory"
        }
    )
    return response.json()["access_token"]
```

### Common OAuth Scopes

| Scope | Purpose |
|---|---|
| `https://api.ebay.com/oauth/api_scope` | Browse API (public data) |
| `https://api.ebay.com/oauth/api_scope/sell.inventory` | Create and manage listings |
| `https://api.ebay.com/oauth/api_scope/sell.fulfillment` | Manage orders and shipping |
| `https://api.ebay.com/oauth/api_scope/commerce.catalog.readonly` | Catalog product lookups |

---

## Browse API (Search Listings)

**Base URL:** `https://api.ebay.com/buy/browse/v1/`

**Auth:** Client Credentials (app-level token) is sufficient.

### Search Items

```
GET /item_summary/search
  ?q={query}
  &filter=price:[{min}..{max}],conditionIds:{conditionId},buyingOptions:{FIXED_PRICE}
  &sort=price
  &limit=20
```

### Filter Examples

| Filter | Example |
|---|---|
| Price range | `price:[50..200]` |
| Condition | `conditionIds:{1000}` (New) |
| Buying format | `buyingOptions:{FIXED_PRICE}` |
| Multiple conditions | `conditionIds:{3000\|4000\|5000}` |

### Sort Options

| Value | Description |
|---|---|
| `price` | Lowest price first |
| `-price` | Highest price first |
| `newlyListed` | Most recent first |
| `endingSoonest` | Ending soonest (auctions) |

### Response Fields to Extract

```json
{
  "itemId": "v1|...",
  "title": "...",
  "price": {"value": "289.99", "currency": "USD"},
  "shippingOptions": [{"shippingCost": {"value": "0.00"}}],
  "condition": "Very Good",
  "seller": {
    "feedbackPercentage": "99.8",
    "feedbackScore": 2341
  },
  "itemLocation": {"country": "US"},
  "estimatedAvailabilities": [{"deliveryOptions": ["..."]}]
}
```

### Sold Listings (Pricing Comps)

For sold/completed listing data, use the **Marketplace Insights API** rather than the Browse API. The Browse API only returns active listings.

---

## Inventory API (Create Listings)

**Base URL:** `https://api.ebay.com/sell/inventory/v1/`

**Auth:** Authorization Code flow (user-level token) required.

The listing workflow has three steps: create inventory item, create offer, publish offer.

### Step 1: Create Inventory Item

```
PUT /inventory_item/{sku}
Authorization: Bearer {user_token}
Content-Type: application/json
```

```json
{
  "product": {
    "title": "Apple iPad Air 2 64GB Space Gray",
    "description": "Great condition, minor scratches on back...",
    "aspects": {
      "Storage Capacity": ["64 GB"],
      "Color": ["Space Gray"]
    },
    "imageUrls": ["https://..."]
  },
  "condition": "GOOD",
  "availability": {
    "shipToLocationAvailability": {
      "quantity": 1
    }
  }
}
```

The `{sku}` is your own identifier (any string). Use something meaningful like `ipad-air2-64-gray-001`.

### Step 2: Create Offer

```
POST /offer
Authorization: Bearer {user_token}
Content-Type: application/json
```

```json
{
  "sku": "ipad-air2-64-gray-001",
  "marketplaceId": "EBAY_US",
  "format": "FIXED_PRICE",
  "listingPolicies": {
    "fulfillmentPolicyId": "...",
    "paymentPolicyId": "...",
    "returnPolicyId": "..."
  },
  "pricingSummary": {
    "price": {"value": "89.00", "currency": "USD"}
  },
  "categoryId": "171485"
}
```

**Note:** You must create fulfillment, payment, and return policies in your eBay seller account before creating offers. Policy IDs come from the Account API or eBay's seller hub.

### Step 3: Publish Offer

```
POST /offer/{offerId}/publish
Authorization: Bearer {user_token}
```

Returns the `listingId` — this is the live eBay listing. The listing URL will be `https://www.ebay.com/itm/{listingId}`.

---

## Catalog API (Product Lookup)

**Base URL:** `https://api.ebay.com/commerce/catalog/v1/`

**Auth:** Client Credentials or Authorization Code.

Use this to look up standardized product data by UPC, EAN, ISBN, or keyword. Useful for auto-populating listing details.

### Search Products

```
GET /product_summary/search
  ?q={upc_or_keyword}
  &aspect_filter=categoryId:{categoryId}
```

Returns eBay catalog entries with standardized title, description, images, and category mapping. Use the returned data to pre-fill inventory item fields.

---

## Fulfillment API (Post-Sale)

**Base URL:** `https://api.ebay.com/sell/fulfillment/v1/`

**Auth:** Authorization Code flow (user-level token) required.

### Get Open Orders

```
GET /order?filter=orderfulfillmentstatus:{NOT_STARTED}
Authorization: Bearer {user_token}
```

Returns all orders awaiting shipment.

### Mark Order as Shipped

```
POST /order/{orderId}/shipping_fulfillment
Authorization: Bearer {user_token}
Content-Type: application/json
```

```json
{
  "lineItems": [
    {
      "lineItemId": "...",
      "quantity": 1
    }
  ],
  "shippedDate": "2026-03-21T00:00:00.000Z",
  "trackingNumber": "1Z999AA10123456784",
  "shippingCarrierCode": "UPS"
}
```

### Common Carrier Codes

| Code | Carrier |
|---|---|
| `USPS` | United States Postal Service |
| `UPS` | UPS |
| `FedEx` | FedEx |
| `DHL` | DHL Express |

---

## Notification API (Webhooks)

**Base URL:** `https://api.ebay.com/commerce/notification/v1/`

### Create Subscription

```
POST /subscription
Authorization: Bearer {user_token}
Content-Type: application/json
```

```json
{
  "topicId": "ITEM_SOLD",
  "deliveryConfig": {
    "endpoint": "https://your-server.com/ebay-webhook",
    "verificationToken": "your-secret"
  }
}
```

### Useful Topics

| Topic | Trigger |
|---|---|
| `ITEM_SOLD` | An item you listed has sold |
| `BEST_OFFER_RECEIVED` | A buyer submitted a Best Offer on your listing |
| `ITEM_OUT_OF_STOCK` | Inventory quantity reached zero |

---

## Sandbox vs. Production

| Environment | Base URL |
|---|---|
| Sandbox | `https://api.sandbox.ebay.com/...` |
| Production | `https://api.ebay.com/...` |

- **Sandbox** provides test accounts with fake listings. Use it for all development and testing.
- **Production** uses real money and real listings. Only switch when your integration is fully tested.
- Toggle via an environment variable in your application config.

### Environment Variables

```
EBAY_APP_ID=<your app id>
EBAY_CERT_ID=<your cert id>
EBAY_USER_TOKEN=<oauth token>
EBAY_ENVIRONMENT=sandbox  # or production
```

---

## Condition ID Reference Table

Use these IDs in Browse API filters and Inventory API condition fields.

| Condition ID | Label | Description |
|---|---|---|
| 1000 | New | Brand new, unused, unopened, in original packaging |
| 1500 | New other | New but missing original packaging or tags |
| 2000 | Certified refurbished | Professionally restored by manufacturer or authorized refurbisher |
| 2500 | Seller refurbished | Restored to working order by the seller |
| 3000 | Used | Previously used, fully functional |
| 4000 | Very Good | Minor cosmetic imperfections, fully functional |
| 5000 | Good | Shows wear, fully functional |
| 6000 | Acceptable | Significant wear but still functional |
| 7000 | For parts or not working | Does not function as intended; suitable for parts or repair |

---

## Useful Resources

| Resource | URL |
|---|---|
| API Explorer (interactive) | https://developer.ebay.com/my-ebay/api-explorer |
| OAuth Scopes reference | https://developer.ebay.com/api-docs/static/oauth-scopes.html |
| Category ID lookup | https://developer.ebay.com/Devzone/merchandising/docs/Concepts/SiteIDToGlobalID.html |
| Seller policies setup | https://www.ebay.com/help/selling/listing-items/setting-up-shipping-policies |
