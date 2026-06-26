# Shopify API Reference

Base URL: `https://{store}.myshopify.com/admin/api/2024-01/graphql.json`
Auth header: `X-Shopify-Access-Token: {token}`

Shopify uses **GraphQL** for its Admin API. All requests are POST to the GraphQL endpoint.

---

## Inventory — Get stock levels

```graphql
query {
  products(first: 50) {
    edges {
      node {
        id
        title
        variants(first: 10) {
          edges {
            node {
              id
              title
              inventoryQuantity
              sku
            }
          }
        }
      }
    }
  }
}
```

## Inventory — Update stock level

First get the inventory item ID and location ID, then:

```graphql
mutation {
  inventoryAdjustQuantity(input: {
    inventoryLevelId: "gid://shopify/InventoryLevel/LEVEL_ID"
    availableDelta: 10
  }) {
    inventoryLevel {
      available
    }
  }
}
```

---

## Orders — List recent orders

```graphql
query {
  orders(first: 20, sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        displayFulfillmentStatus
        totalPriceSet { shopMoney { amount currencyCode } }
        customer { firstName lastName email }
        lineItems(first: 5) {
          edges { node { title quantity } }
        }
      }
    }
  }
}
```

## Orders — Fulfill an order

```graphql
mutation fulfillmentCreateV2($fulfillment: FulfillmentV2Input!) {
  fulfillmentCreateV2(fulfillment: $fulfillment) {
    fulfillment { id status }
    userErrors { field message }
  }
}
```

Variables:
```json
{
  "fulfillment": {
    "lineItemsByFulfillmentOrder": [{ "fulfillmentOrderId": "gid://shopify/FulfillmentOrder/ID" }],
    "notifyCustomer": true
  }
}
```

---

## Products — List products

```graphql
query {
  products(first: 50) {
    edges {
      node {
        id title descriptionHtml status
        priceRangeV2 { minVariantPrice { amount currencyCode } }
        images(first: 1) { edges { node { url } } }
      }
    }
  }
}
```

## Products — Create product

```graphql
mutation {
  productCreate(input: {
    title: "My Product"
    descriptionHtml: "<p>Description here</p>"
    vendor: "My Brand"
    productType: "T-Shirts"
    variants: [{ price: "29.99", sku: "SKU-001", inventoryQuantities: { availableQuantity: 100, locationId: "gid://shopify/Location/LOCATION_ID" } }]
  }) {
    product { id title }
    userErrors { field message }
  }
}
```

## Products — Update product

```graphql
mutation {
  productUpdate(input: {
    id: "gid://shopify/Product/PRODUCT_ID"
    title: "Updated Title"
    variants: [{ id: "gid://shopify/ProductVariant/VARIANT_ID" price: "39.99" }]
  }) {
    product { id title }
    userErrors { field message }
  }
}
```

## Products — Delete product

```graphql
mutation {
  productDelete(input: { id: "gid://shopify/Product/PRODUCT_ID" }) {
    deletedProductId
    userErrors { field message }
  }
}
```

---

## Customers — Search customers

```graphql
query {
  customers(first: 20, query: "email:test@example.com") {
    edges {
      node {
        id firstName lastName email phone
        ordersCount totalSpentV2 { amount currencyCode }
        defaultAddress { address1 city country }
      }
    }
  }
}
```

## Customers — Update customer

```graphql
mutation {
  customerUpdate(input: {
    id: "gid://shopify/Customer/CUSTOMER_ID"
    firstName: "Jane"
    lastName: "Doe"
    email: "jane@example.com"
  }) {
    customer { id firstName lastName }
    userErrors { field message }
  }
}
```

---

## Error handling

Check `userErrors` in every mutation response. Common errors:
- `TAKEN` — SKU or handle already exists
- `INVALID` — Bad field value
- `NOT_FOUND` — ID doesn't exist

Display errors in plain English: "It looks like that SKU is already being used by another product. Try a different one."
