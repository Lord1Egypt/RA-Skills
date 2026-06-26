---
name: cj-dropshipping-api
description: >
  Use when user wants to integrate CJ Dropshipping, search products, create orders, track shipments, manage Shopify listings via CJ, or automate CJ logistics and webhook setups. Triggered for CJ API related tasks like product queries, order creation, shipping calculations, delivery profile management, and webhook configuration.
version: "1.0.0"
---


# CJ Dropshipping API Skill

## Overview

This skill provides concise guidance for interacting with the CJ Dropshipping API (v2.0). It covers authentication, product management, order processing, logistics, delivery profiles, shop management, and webhook configuration. Use the skill when a user asks to:

- Obtain an OAuth token via `accio-mcp-cli`
- Search or list CJ products
- Retrieve product details, variants, or stock
- Add products to "My Products"
- List or batch‑list products to a Shopify store
- Create or query delivery profiles
- Create orders, pay for them, or track shipments
- Configure or manage CJ webhooks
- Query shop information (shops, locations, countries)

All REST calls require the `CJ-Access-Token` header obtained from `accio-mcp-cli call get_cj_access_token`.

## Core Workflow Summary

1. **Authenticate** – Run the two `accio-mcp-cli` commands to obtain the access token.
2. **Make REST Calls** – Use `curl` (or any HTTP client) with the token in the header.
3. **Handle Pagination** – Most list endpoints accept `page` and `size` query parameters.
4. **Error Handling** – Check the `code` field; retry on `500` or respect `rate‑limit` headers.
5. **Webhooks** – Set up callbacks once; store URLs securely.

## Usage Examples

```bash
# 1️⃣ Obtain OAuth token (once)
accio-mcp-cli call start_cj_auth          # opens browser for user consent
accio-mcp-cli call get_cj_access_token    # prints JSON with accessToken

# Store the token in an env var for convenience
export CJ_TOKEN=$(accio-mcp-cli call get_cj_access_token --raw | jq -r .accessToken)

# 2️⃣ Get product list (search)
curl -s "https://developers.cjdropshipping.com/api2.0/v1/product/listV2?keyWord=phone&page=1&size=20" \
  -H "CJ-Access-Token: $CJ_TOKEN" | jq .

# 3️⃣ Get product detail by SKU
curl -s "https://developers.cjdropshipping.com/api2.0/v1/product/query?productSku=ABC123" \
  -H "CJ-Access-Token: $CJ_TOKEN" | jq .

# 4️⃣ Add a product to My Products
curl -X POST "https://developers.cjdropshipping.com/api2.0/v1/product/addToMyProduct" \
  -H "Content-Type: application/json" \
  -H "CJ-Access-Token: $CJ_TOKEN" \
  -d '{"productId":"1234567890"}' | jq .

# 5️⃣ Create a Shopify delivery profile (required for listing)
curl -X POST "https://developers.cjdropshipping.com/api2.0/v1/product/listed/createDeliveryProfile" \
  -H "Content-Type: application/json" \
  -H "CJ-Access-Token: $CJ_TOKEN" \
  -d '{
        "shopId":"YOUR_SHOP_ID",
        "name":"CJ Dropshipping",
        "locationIds":["CJ_LOCATION_ID"],
        "zones":{"countries":[{"countryCode":"US","provinces":[{"provinceCode":"CA"}]}]}
      }' | jq .

# 6️⃣ Batch list products to Shopify (use deliveryProfileId from previous step)
curl -X POST "https://developers.cjdropshipping.com/api2.0/v1/product/listed/listedByPids" \
  -H "Content-Type: application/json" \
  -H "CJ-Access-Token: $CJ_TOKEN" \
  -d '{
        "shopIds":["YOUR_SHOP_ID"],
        "productIds":["123456","789012"],
        "formula":{ "formulaType":3, "shippingFrom":"CN", "shippingTo":"US", "isLogistics":1 },
        "templateShopCategoryVOList":[{"shopId":"YOUR_SHOP_ID","deliveryProfileId":"YOUR_PROFILE_ID"}]
      }' | jq .

# 7️⃣ Create an order (V2)
curl -X POST "https://developers.cjdropshipping.com/api2.0/v1/shopping/order/createOrderV2" \
  -H "Content-Type: application/json" \
  -H "CJ-Access-Token: $CJ_TOKEN" \
  -d '{
        "orderNumber":"ORDER123",
        "shippingCountryCode":"US",
        "shippingAddress":"123 Main St",
        "shippingCustomerName":"John Doe",
        "shippingPhone":"1234567890",
        "logisticName":"CJPacket Sensitive",
        "payType":"1",
        "products":[{"vid":"VID123","quantity":1}]
      }' | jq .

# 8️⃣ Track a shipment
curl -s "https://developers.cjdropshipping.com/api2.0/v1/logistic/trackInfo?trackNumber=TRACK123" \
  -H "CJ-Access-Token: $CJ_TOKEN" | jq .

# 9️⃣ Set up a webhook for order updates
curl -X POST "https://developers.cjdropshipping.com/api2.0/v1/webhook/set" \
  -H "Content-Type: application/json" \
  -H "CJ-Access-Token: $CJ_TOKEN" \
  -d '{
        "order":{"type":"ENABLE","callbackUrls":["https://yourdomain.com/cj/webhook/order"]}
      }' | jq .
```


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
