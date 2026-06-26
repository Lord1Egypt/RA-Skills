---
name: ecwid
description: |
  Ecwid REST API v3 integration for managing e-commerce store data including
  products, orders, customers, categories, discount coupons, promotions,
  abandoned carts, and store profile. Use when the user wants to interact with
  their Ecwid online store.
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env:
        - ECWID_STORE_ID
        - ECWID_SECRET_TOKEN
    primaryEnv: ECWID_SECRET_TOKEN
    emoji: "🛒"
    homepage: https://github.com/droneitgroup
compatibility: |
  Requires an Ecwid store with API access enabled. Token should be a secret
  API token (format: secret_xxxxx). For read-only use, create a token with
  scopes: read_store_profile, read_catalog, read_orders, read_customers,
  read_discount_coupons. No CLI binaries required — uses HTTP API via
  Direct API connection or curl.
license: MIT-0
---

# Ecwid

Ecwid REST API v3 integration for managing e-commerce store data including products, orders, customers, categories, discount coupons, promotions, abandoned carts, and store profile.

**Official docs**: https://docs.ecwid.com/api-reference
**Publisher**: https://github.com/droneitgroup

---

## Connection Setup

Set up a **Direct API (HTTP)** connection with the following settings:

| Setting | Value |
|---|---|
| **Service name** | Ecwid |
| **Base URL** | `https://app.ecwid.com/api/v3/{storeId}` (replace `{storeId}` with your actual store ID) |
| **Auth type** | Bearer token |
| **Token** | Your store's secret API token (format: `secret_xxxxx`) |
| **HTTP methods** | `GET` for read-only access. Add `POST`, `PUT`, `DELETE` for write operations. |

### Finding your Store ID and API token

1. Log in to your Ecwid admin panel
2. Go to **Settings → API**
3. Your **Store ID** is displayed at the top
4. Your **Secret API token** starts with `secret_` — use this as the Bearer token

### ⚠️ Security best practices

- **Use the minimum scopes needed.** If you only need to read data, create a token with read-only scopes (e.g. `read_store_profile`, `read_catalog`, `read_orders`, `read_customers`, `read_discount_coupons`) and set HTTP methods to `GET` only.
- **Never use a full admin token** unless you specifically need write access.
- **Test with a sandbox/test store first** before connecting a production store.
- **Rotate tokens** if you suspect they've been exposed.
- For more on Ecwid API permissions, see: https://docs.ecwid.com/api-reference/rest-api/authentication

---

## Common Patterns

### Pagination

All list endpoints return the same pagination envelope:

```json
{
  "total": 150,
  "count": 100,
  "offset": 0,
  "limit": 100,
  "items": [...]
}
```

Use `offset` and `limit` query parameters to paginate. Maximum and default `limit` is **100**.

Example: `?offset=0` → `?offset=100` → `?offset=200` ...

### Response field filtering

All endpoints support the `responseFields` query parameter to limit which fields are returned:

```
?responseFields=total,items(id,name,price)
```

This reduces response size and speeds up requests.

### Date formats

Date parameters accept both:
- **UNIX timestamps**: `1447804800`
- **Datetime strings**: `2023-01-15 19:27:50`

### Authentication

All requests require the `Authorization` header:
```
Authorization: Bearer secret_xxxxx
```

---

## Products

**Scope required**: `read_catalog`

### Search/list products

```
GET /products
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `keyword` | string | Search term. Searches name, description, SKU, options, category name, gallery image descriptions, attribute values. Add `*` at end to disable exact match. |
| `productId` | number | Internal product IDs (comma-separated). If set, other search params are ignored. |
| `sku` | string | Exact product or variation SKU match. If set, other params ignored except `productId`. |
| `category` | string | Category ID to filter products by. |
| `categories` | string | Comma-separated category IDs, e.g. `0,123456,138470508`. |
| `includeProductsFromSubcategories` | boolean | Set `true` to include products from subcategories. |
| `priceFrom` | number | Minimum product price. |
| `priceTo` | number | Maximum product price. |
| `createdFrom` | number/string | Product creation date lower bound. |
| `createdTo` | number/string | Product creation date upper bound. |
| `updatedFrom` | number/string | Product update date lower bound. |
| `updatedTo` | number/string | Product update date upper bound. |
| `enabled` | boolean | `true` for enabled only, `false` for disabled only. |
| `inStock` | boolean | `true` for in-stock only, `false` for out-of-stock only. |
| `sortBy` | string | One of: `RELEVANCE` (default), `DEFINED_BY_STORE_OWNER`, `ADDED_TIME_DESC`, `ADDED_TIME_ASC`, `NAME_ASC`, `NAME_DESC`, `PRICE_ASC`, `PRICE_DESC`, `UPDATED_TIME_ASC`, `UPDATED_TIME_DESC`. |
| `offset` | number | Pagination offset. |
| `limit` | number | Max items to return (max/default: 100). |
| `responseFields` | string | Limit response fields. Example: `items(id,name,price,sku)` |

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal product ID. |
| `sku` | string | Product SKU. |
| `name` | string | Product name. |
| `price` | number | Base product price. |
| `defaultDisplayedPrice` | number | Price shown on storefront (includes taxes). |
| `compareToPrice` | number | Pre-sale / "compare to" price. |
| `quantity` | number | Stock quantity (absent if `unlimited` is true). |
| `unlimited` | boolean | Whether product has unlimited stock. |
| `inStock` | boolean | Whether in stock. |
| `enabled` | boolean | Whether visible on storefront. |
| `weight` | number | Product weight. |
| `url` | string | Storefront product page URL. |
| `created` | string | Creation datetime. |
| `updated` | string | Last update datetime. |
| `createTimestamp` | number | Creation UNIX timestamp. |
| `updateTimestamp` | number | Last update UNIX timestamp. |
| `description` | string | Product description (HTML). |
| `categoryIds` | array | IDs of assigned categories. |
| `defaultCategoryId` | number | Default category ID. |
| `imageUrl` | string | Main image URL (1200px). |
| `thumbnailUrl` | string | Thumbnail URL (400px). |
| `originalImageUrl` | string | Full-size image URL. |
| `options` | array | Product options (size, color, etc.). |
| `combinations` | array | Product variations. |
| `attributes` | array | Product attributes and values. |
| `isGiftCard` | boolean | Whether this is a gift card. |

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/products?keyword=drone&limit=10' \
  -H 'Authorization: Bearer secret_token'
```

### Get single product

```
GET /products/{productId}
```

Returns the full product object directly (not wrapped in pagination envelope). The `productId` is a **number**.

---

## Orders

**Scope required**: `read_orders`

### Search/list orders

```
GET /orders
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `ids` | string | Comma-separated order IDs, internal IDs, prefixes, and suffixes. Example: `EG4H2,J77J8` |
| `keywords` | string | Search order ID, transaction ID, addresses, email, tracking code, item SKUs/names, admin notes. |
| `email` | string | Customer email. |
| `customerId` | number | Customer's internal ID. |
| `productId` | number/string | Product IDs in order (comma-separated). |
| `totalFrom` | number | Minimum order total. |
| `totalTo` | number | Maximum order total. |
| `createdFrom` | number/string | Order placement datetime lower bound. |
| `createdTo` | number/string | Order placement datetime upper bound. |
| `updatedFrom` | number/string | Order update datetime lower bound. |
| `updatedTo` | number/string | Order update datetime upper bound. |
| `paymentStatus` | string | Payment status filter. Supports multiple comma-separated values: `AWAITING_PAYMENT`, `PAID`, `CANCELLED`, `REFUNDED`, `PARTIALLY_REFUNDED`, `INCOMPLETE`. |
| `fulfillmentStatus` | string | Fulfillment status filter. Supports multiple comma-separated values: `AWAITING_PROCESSING`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `WILL_NOT_DELIVER`, `RETURNED`, `READY_FOR_PICKUP`, `OUT_FOR_DELIVERY`. |
| `paymentMethod` | string | Payment method name. |
| `shippingMethod` | string | Shipping method name. |
| `couponCode` | string | Discount coupon code applied to the order. |
| `offset` | number | Pagination offset. |
| `limit` | number | Max items to return (max/default: 100). |
| `responseFields` | string | Limit response fields. Example: `items(id,email,total,paymentStatus)` |

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `id` | string | **Order ID (string, not number!)** e.g. `"ORD001"`, `"XYZ99"`. |
| `internalId` | number | Internal numeric order ID. |
| `email` | string | Customer email. |
| `total` | number | Order total with all modifiers. |
| `subtotal` | number | Cost of products before modifiers. |
| `tax` | number | Sum of all taxes. |
| `couponDiscount` | number | Discount from coupon. |
| `discount` | number | Sum of all advanced discounts. |
| `paymentStatus` | string | Payment status. |
| `fulfillmentStatus` | string | Fulfillment status. |
| `paymentMethod` | string | Payment method name. |
| `createDate` | string | Order placement datetime. |
| `updateDate` | string | Last update datetime. |
| `createTimestamp` | number | Order placement UNIX timestamp. |
| `updateTimestamp` | number | Last update UNIX timestamp. |
| `customerId` | number | Internal customer ID. |
| `items` | array | Products in the order (with `productId`, `name`, `price`, `quantity`, `sku`). |
| `shippingPerson` | object | Shipping address (`name`, `street`, `city`, `countryCode`, `postalCode`, `phone`). |
| `billingPerson` | object | Billing address (same fields as shippingPerson). |
| `shippingOption` | object | Shipping details (`shippingMethodName`, `shippingRate`). |
| `trackingNumber` | string | Shipping tracking code. |
| `privateAdminNotes` | string | Private notes by store owner. |
| `orderComments` | string | Customer's order comments. |

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/orders?paymentStatus=PAID&fulfillmentStatus=DELIVERED&limit=10' \
  -H 'Authorization: Bearer secret_token'
```

### Get single order

```
GET /orders/{orderId}
```

Returns the full order object directly. **Note**: `orderId` is a **string** (e.g. `"ORD001"`), not a number.

---

## Customers

**Scope required**: `read_customers`

### Search/list customers

```
GET /customers
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `keyword` | string | Search customer name and email. |
| `name` | string | Search customer name (`billingPerson.name`). |
| `email` | string | Search customer email. |
| `useExactEmailMatch` | boolean | `true` for exact email match (requires `email` param). |
| `phone` | string | Search customer phone number. |
| `city` | string | Search customer city in shipping address. |
| `postalCode` | string | Search customer ZIP code. |
| `stateOrProvinceCode` | string | Two-digit state code. |
| `countryCodes` | string | Country codes in shipping address. |
| `companyName` | string | Company name in shipping address. |
| `acceptMarketing` | boolean | Filter by marketing email acceptance. |
| `customerGroupIds` | string | Customer group IDs (comma-separated). |
| `minOrderCount` | number | Minimum number of customer orders. |
| `maxOrderCount` | number | Maximum number of customer orders. |
| `minSalesValue` | number | Minimum total order value. |
| `maxSalesValue` | number | Maximum total order value. |
| `createdFrom` | number/string | Registration datetime lower bound. |
| `createdTo` | number/string | Registration datetime upper bound. |
| `updatedFrom` | number/string | Last update datetime lower bound. |
| `updatedTo` | number/string | Last update datetime upper bound. |
| `sortBy` | string | One of: `NAME_ASC`, `NAME_DESC`, `EMAIL_ASC`, `EMAIL_DESC`, `ORDER_COUNT_ASC`, `ORDER_COUNT_DESC`, `REGISTERED_DATE_DESC`, `REGISTERED_DATE_ASC`, `UPDATED_DATE_DESC`, `UPDATED_DATE_ASC`, `SALES_VALUE_ASC`, `SALES_VALUE_DESC`. |
| `offset` | number | Pagination offset. |
| `limit` | number | Max items (max/default: 100). |
| `responseFields` | string | Limit response fields. |

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal customer ID. |
| `email` | string | Customer email. |
| `name` | string | Customer name. |
| `totalOrderCount` | number | Total orders placed. |
| `registered` | string | Registration datetime. |
| `updated` | string | Last update datetime. |
| `billingPerson` | object | Billing name/address. |
| `shippingAddresses` | array | Saved shipping addresses. |
| `contacts` | array | Contact info (email, phone, social media). |
| `customerGroupId` | number | Customer group ID. |
| `customerGroupName` | string | Customer group name. |
| `taxExempt` | boolean | Whether customer is tax exempt. |
| `acceptMarketing` | boolean | Whether customer accepted marketing emails. |
| `stats` | object | Sales stats: `numberOfOrders`, `salesValue`, `averageOrderValue`, `firstOrderDate`, `lastOrderDate`. |
| `privateAdminNotes` | string | Private admin notes. |

The response also includes `allCustomerCount` (total unique customers in store) at the top level.

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/customers?email=john@example.com' \
  -H 'Authorization: Bearer secret_token'
```

### Get single customer

```
GET /customers/{customerId}
```

Returns the full customer object directly. `customerId` is a **number**.

---

## Categories

**Scope required**: `read_catalog`

### Search/list categories

```
GET /categories
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `keyword` | string | Search category name and description. |
| `parent` | number | Parent category ID — returns only direct children. |
| `parentIds` | string | Comma-separated parent category IDs for descendants search. |
| `withSubcategories` | boolean | `true` to get full category tree (subcategories of subcategories). |
| `hidden_categories` | boolean | `true` to include disabled categories. |
| `offset` | number | Pagination offset. |
| `limit` | number | Max items (max/default: 100). |
| `responseFields` | string | Limit response fields. |

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal category ID. |
| `parentId` | number | Parent category ID. |
| `name` | string | Category name. |
| `url` | string | Full storefront URL. |
| `productCount` | number | Products in category and subcategories. |
| `enabledProductCount` | number | Enabled products (requires `productIds=true`). |
| `description` | string | Category description (HTML). |
| `enabled` | boolean | Whether category is enabled. |
| `imageUrl` | string | Category image (1200px). |
| `thumbnailUrl` | string | Category thumbnail (400px). |
| `orderBy` | number | Sort order (starts from 10, increments by 10). |
| `productIds` | array | Product IDs in category (requires `productIds=true` query param). |

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/categories?parent=0' \
  -H 'Authorization: Bearer secret_token'
```

### Get single category

```
GET /categories/{categoryId}
```

Returns the full category object directly. `categoryId` is a **number**.

---

## Discount Coupons

**Scope required**: `read_discount_coupons`

### Search/list coupons

```
GET /discount_coupons
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `code` | string | Search by coupon code. |
| `discount_type` | string | Filter by type: `ABS`, `PERCENT`, `SHIPPING`, `ABS_AND_SHIPPING`, `PERCENT_AND_SHIPPING`. |
| `availability` | string | Filter by status: `ACTIVE`, `PAUSED`, `EXPIRED`, `USEDUP`. |
| `createdFrom` | number/string | Creation date lower bound. |
| `createdTo` | number/string | Creation date upper bound. |
| `updatedFrom` | number/string | Update date lower bound. |
| `updatedTo` | number/string | Update date upper bound. |
| `offset` | number | Pagination offset. |
| `limit` | number | Max items (max/default: 100). |
| `responseFields` | string | Limit response fields. |

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal coupon ID. |
| `name` | string | Coupon name. |
| `code` | string | Coupon code used at checkout. |
| `discountType` | string | Type: `ABS`, `PERCENT`, `SHIPPING`, `ABS_AND_SHIPPING`, `PERCENT_AND_SHIPPING`. |
| `status` | string | Status: `ACTIVE`, `PAUSED`, `EXPIRED`, `USEDUP`. |
| `discount` | number | Discount value. |
| `launchDate` | string | Coupon launch date. |
| `expirationDate` | string | Coupon expiration date. |
| `totalLimit` | number | Minimum order subtotal for coupon to apply. |
| `usesLimit` | string | Uses limit: `UNLIMITED`, `ONCEPERCUSTOMER`, `SINGLE`. |
| `applicationLimit` | string | Application limit: `UNLIMITED`, `NEW_CUSTOMER_ONLY`, `REPEAT_CUSTOMER_ONLY`. |
| `creationDate` | string | Coupon creation date. |
| `updateDate` | string | Last update date. |
| `orderCount` | number | Number of orders using this coupon. |
| `catalogLimit` | object | Product/category limitations (`products`, `categories` arrays). |

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/discount_coupons?availability=ACTIVE' \
  -H 'Authorization: Bearer secret_token'
```

### Get single coupon

```
GET /discount_coupons/{couponId}
```

Returns the full coupon object directly. `couponId` is a **number**.

---

## Promotions

**Scope required**: `read_promotion`

### List promotions

```
GET /promotions
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `responseFields` | string | Limit response fields. Example: `items(name,enabled)` |

**Note**: Promotions endpoint has minimal filtering — only `responseFields` is supported.

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal promotion ID. |
| `name` | string | Promotion name visible at checkout. |
| `enabled` | boolean | Whether promotion is active. |
| `discountBase` | string | Discount base: `ITEM`, `SUBTOTAL`, `SHIPPING`. |
| `discountType` | string | Discount type: `PERCENT`, `ABSOLUTE`, `FIXED_PRICE`. |
| `amount` | number | Discount amount. |
| `triggers` | object | Trigger conditions (`subtotal`, `startDate`, `endDate`, `customerGroups`, `minProductQuantityInCart`, etc.). |
| `targets` | object | Target limitations (`categories`, `products`, `shippingMethods`, etc.). |

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/promotions' \
  -H 'Authorization: Bearer secret_token'
```

---

## Abandoned Carts

**Scope required**: `read_orders`

> **IMPORTANT**: The endpoint path is `/carts`, **NOT** `/abandoned_carts`. Using `/abandoned_carts` returns a 404 error.

### Search abandoned carts

```
GET /carts
```

#### Query parameters

| Name | Type | Description |
|---|---|---|
| `showHidden` | boolean | Set `false` to exclude deleted carts. |
| `totalFrom` | number | Minimum cart total. |
| `totalTo` | number | Maximum cart total. |
| `createdFrom` | number/string | Cart creation datetime lower bound. |
| `createdTo` | number/string | Cart creation datetime upper bound. |
| `updatedFrom` | number/string | Cart update datetime lower bound. |
| `updatedTo` | number/string | Cart update datetime upper bound. |
| `email` | string | Customer email. |
| `customerId` | number | Customer's internal ID. |
| `offset` | number | Pagination offset. |
| `limit` | number | Max items (max: 100, default: 10). |
| `responseFields` | string | Limit response fields. Example: `items(cartId,total,email)` |

#### Key response fields (items)

| Field | Type | Description |
|---|---|---|
| `cartId` | string | Unique cart ID (UUID format), e.g. `"6626E60A-A6F9-4CD5-8230-43D5F162E0CD"`. |
| `email` | string | Customer email. |
| `total` | number | Cart total. |
| `subtotal` | number | Cart subtotal. |
| `tax` | number | Total tax. |
| `createDate` | string | Cart creation datetime. |
| `updateDate` | string | Last update datetime. |
| `createTimestamp` | number | Creation UNIX timestamp. |
| `updateTimestamp` | number | Last update UNIX timestamp. |
| `customerId` | number | Internal customer ID. |
| `paymentMethod` | string | Selected payment method. |
| `items` | array | Products in cart (`productId`, `name`, `price`, `quantity`, `sku`). |
| `billingPerson` | object | Billing address. |
| `shippingPerson` | object | Shipping address. |
| `shippingOption` | object | Selected shipping option. |
| `couponDiscount` | number | Discount from coupon. |
| `discount` | number | Sum of all advanced discounts. |
| `recoveredOrderId` | number | Order ID if cart was recovered. |
| `hidden` | boolean | Whether cart is hidden from admin. |

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/carts?email=customer@example.com' \
  -H 'Authorization: Bearer secret_token'
```

### Get single abandoned cart

```
GET /carts/{cartId}
```

Returns the full cart object directly. `cartId` is a **string** (UUID format).

---

## Store Profile

**Scope required**: `read_store_profile`

### Get store profile

```
GET /profile
```

Returns store settings including general info, company details, languages, currencies, tax settings, and more.

No query parameters required (supports `responseFields` for filtering).

#### Example

```
curl 'https://app.ecwid.com/api/v3/1003/profile' \
  -H 'Authorization: Bearer secret_token'
```

---

## Quick Reference

| Resource | List Endpoint | Single Endpoint | Scope |
|---|---|---|---|
| Products | `GET /products` | `GET /products/{productId}` | `read_catalog` |
| Orders | `GET /orders` | `GET /orders/{orderId}` | `read_orders` |
| Customers | `GET /customers` | `GET /customers/{customerId}` | `read_customers` |
| Categories | `GET /categories` | `GET /categories/{categoryId}` | `read_catalog` |
| Coupons | `GET /discount_coupons` | `GET /discount_coupons/{couponId}` | `read_discount_coupons` |
| Promotions | `GET /promotions` | — | `read_promotion` |
| Abandoned Carts | `GET /carts` | `GET /carts/{cartId}` | `read_orders` |
| Store Profile | `GET /profile` | — | `read_store_profile` |

### ID Types

| Resource | ID Type | Example |
|---|---|---|
| Products | number | `12345678` |
| Orders | **string** | `"ORD001"` |
| Customers | number | `177737165` |
| Categories | number | `9691094` |
| Coupons | number | `162428889` |
| Abandoned Carts | **string (UUID)** | `"6626E60A-A6F9-4CD5-8230-43D5F162E0CD"` |
