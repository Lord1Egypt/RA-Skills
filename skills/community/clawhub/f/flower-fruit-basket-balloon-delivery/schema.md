# Flower, Fruit Basket, Balloon Delivery Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `flower-fruit-basket-balloon-delivery`

x402 availability: not enabled for this product.

## `get_order`

Action slug: `get-order`

Price: `0` credits

Look up a completed order by its Florist One confirmation number.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `orderno` | `string` | yes | Florist One confirmation number |

Sample parameters:

```json
{
  "orderno": "example orderno"
}
```

Generated JSON parameter schema:

```json
{
  "orderno": {
    "description": "Florist One confirmation number",
    "required": true,
    "type": "string"
  }
}
```

## `get_order_total`

Action slug: `get-order-total`

Price: `0` credits

Get the full price breakdown (product price, delivery fee, tax, order total) and resolved delivery date for a product and recipient ZIP code. Must be called before place_order.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `delivery_date` | `string` | no | Desired delivery date (MM-DD-YYYY). If omitted, the soonest available date is returned. |
| `product_code` | `string` | yes | Florist One product code from search results |
| `recipient_zipcode` | `string` | yes | Recipient's ZIP/postal code |

Sample parameters:

```json
{
  "delivery_date": "example delivery date",
  "product_code": "example product code",
  "recipient_zipcode": "example recipient zipcode"
}
```

Generated JSON parameter schema:

```json
{
  "delivery_date": {
    "description": "Desired delivery date (MM-DD-YYYY). If omitted, the soonest available date is returned.",
    "required": false,
    "type": "string"
  },
  "product_code": {
    "description": "Florist One product code from search results",
    "required": true,
    "type": "string"
  },
  "recipient_zipcode": {
    "description": "Recipient's ZIP/postal code",
    "required": true,
    "type": "string"
  }
}
```

## `list_categories`

Action slug: `list-categories`

Price: `0` credits

Returns all available product categories grouped by type (Occasions, Product Types, Funeral, Price Ranges, Seasonal, Other).

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_orders`

Action slug: `list-orders`

Price: `0` credits

List past flower delivery orders with pagination.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Max results to return (default 12, max 50) |
| `offset` | `integer` | no | Skip first N results (default 0) |

Sample parameters:

```json
{
  "limit": 12,
  "offset": 0
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 12,
    "description": "Max results to return (default 12, max 50)",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "default": 0,
    "description": "Skip first N results (default 0)",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `place_order`

Action slug: `place-order`

Price: `0` credits

Place a flower delivery order. Requires calling get_order_total first and confirming the total with the user. A credit card request is sent to the user's mobile app after calling this action.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `card_message` | `string` | yes | Message on the card (max 200 characters) |
| `confirmed_total` | `number` | yes | The order_total value returned by get_order_total, confirmed by the user |
| `delivery_date` | `string` | yes | Delivery date from get_order_total (MM-DD-YYYY) |
| `idempotency_key` | `string` | no | Optional key to prevent duplicate orders when retrying |
| `product_code` | `string` | yes | Florist One product code to order |
| `recipient` | `object` | yes | Delivery recipient information |
| `special_instructions` | `string` | no | Delivery instructions (max 100 characters) |

Sample parameters:

```json
{
  "card_message": "example card message",
  "confirmed_total": 1,
  "delivery_date": "example delivery date",
  "idempotency_key": "example idempotency key",
  "product_code": "example product code",
  "recipient": {
    "address1": "example address1",
    "address2": "example address2",
    "city": "example city",
    "institution": "example institution",
    "name": "example name",
    "phone": "example phone",
    "state": "example state",
    "zipcode": "example zipcode"
  },
  "special_instructions": "example special instructions"
}
```

Generated JSON parameter schema:

```json
{
  "card_message": {
    "description": "Message on the card (max 200 characters)",
    "required": true,
    "type": "string"
  },
  "confirmed_total": {
    "description": "The order_total value returned by get_order_total, confirmed by the user",
    "required": true,
    "type": "number"
  },
  "delivery_date": {
    "description": "Delivery date from get_order_total (MM-DD-YYYY)",
    "required": true,
    "type": "string"
  },
  "idempotency_key": {
    "description": "Optional key to prevent duplicate orders when retrying",
    "required": false,
    "type": "string"
  },
  "product_code": {
    "description": "Florist One product code to order",
    "required": true,
    "type": "string"
  },
  "recipient": {
    "description": "Delivery recipient information",
    "properties": {
      "address1": {
        "description": "Street address",
        "required": true,
        "type": "string"
      },
      "address2": {
        "description": "Apt/suite/unit (optional)",
        "required": false,
        "type": "string"
      },
      "city": {
        "description": "City",
        "required": true,
        "type": "string"
      },
      "institution": {
        "description": "Hospital, funeral home, or other facility name (optional)",
        "required": false,
        "type": "string"
      },
      "name": {
        "description": "Recipient's full name",
        "required": true,
        "type": "string"
      },
      "phone": {
        "description": "10-digit phone number",
        "required": true,
        "type": "string"
      },
      "state": {
        "description": "2-letter state code",
        "required": true,
        "type": "string"
      },
      "zipcode": {
        "description": "ZIP/postal code",
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  },
  "special_instructions": {
    "description": "Delivery instructions (max 100 characters)",
    "required": false,
    "type": "string"
  }
}
```

## `search_products`

Action slug: `search-products`

Price: `0` credits

Search for flower products by category name/alias or by a specific product code. Provide exactly one of category or product_code.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category` | `string` | no | Category name, alias, or code from list_categories (e.g., "Birthday", "roses", "bd") |
| `limit` | `integer` | no | Max results to return (default 12, max 50) |
| `page` | `integer` | no | Page number for pagination (1-based, default 1) |
| `product_code` | `string` | no | Florist One product code (e.g., "F1-509", "E2-4305") |
| `sort` | `string` | no | Sort order (default: popularity) |

Sample parameters:

```json
{
  "category": "example category",
  "limit": 12,
  "page": 1,
  "product_code": "example product code",
  "sort": "popularity"
}
```

Generated JSON parameter schema:

```json
{
  "category": {
    "description": "Category name, alias, or code from list_categories (e.g., \"Birthday\", \"roses\", \"bd\")",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 12,
    "description": "Max results to return (default 12, max 50)",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "page": {
    "default": 1,
    "description": "Page number for pagination (1-based, default 1)",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "product_code": {
    "description": "Florist One product code (e.g., \"F1-509\", \"E2-4305\")",
    "required": false,
    "type": "string"
  },
  "sort": {
    "description": "Sort order (default: popularity)",
    "enum": [
      "popularity",
      "price_asc",
      "price_desc",
      "az",
      "za"
    ],
    "required": false,
    "type": "string"
  }
}
```
