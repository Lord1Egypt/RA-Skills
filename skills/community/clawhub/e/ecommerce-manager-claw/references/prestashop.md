# PrestaShop API Reference

Base URL: `https://{store}/api/`
Auth: HTTP Basic Auth — API key as username, password blank. Use `?output_format=JSON` on all requests.

---

## Products — List products

GET `/api/products?output_format=JSON&display=full&limit=50`

## Products — Get single product

GET `/api/products/{id}?output_format=JSON`

## Products — Update product (stock / price)

PUT `/api/products/{id}`
Body: XML format required. Example:
```xml
<prestashop>
  <product>
    <id>42</id>
    <price>29.990000</price>
  </product>
</prestashop>
```

Note: PrestaShop REST requires XML bodies for write operations. Build XML carefully.

## Inventory — Update stock

Stock is managed via `stock_availables` resource:

GET `/api/stock_availables?output_format=JSON&filter[id_product]={product_id}`

PUT `/api/stock_availables/{stock_id}`
```xml
<prestashop>
  <stock_available>
    <id>{stock_id}</id>
    <quantity>50</quantity>
  </stock_available>
</prestashop>
```

---

## Orders — List orders

GET `/api/orders?output_format=JSON&display=full&limit=20&sort=date_add_DESC`

## Orders — Update order status

POST `/api/order_histories`
```xml
<prestashop>
  <order_history>
    <id_order>{order_id}</id_order>
    <id_order_state>5</id_order_state>
  </order_history>
</prestashop>
```

Order states: `1`=Awaiting check payment, `2`=Payment accepted, `4`=Shipped, `5`=Delivered, `6`=Cancelled

---

## Customers — List customers

GET `/api/customers?output_format=JSON&display=full&limit=20`

GET `/api/customers?output_format=JSON&filter[email]=test@example.com`
