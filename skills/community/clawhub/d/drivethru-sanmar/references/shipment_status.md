# SanMar tracking & shipment status

Two grounded sources:

| Tool | Source | Carries |
| --- | --- | --- |
| `get-tracking` | PromoStandards **Order Shipment Notification** SOAP | Live per-package tracking, carrier, method, ship date, items. |
| `get-shipment-status` | FTP **Daily Shipment Status** (ASN) file | Same tracking numbers **plus per-line costs** + box/LPN detail. |

`check-order-status` is a lightweight roll-up over the same OSN call (SanMar
sales-order number + shipped/submitted status).

---

## `get-tracking` — Order Shipment Notification (OSN) V1.0.0

- PRODUCTION / TEST: `https://ws.sanmar.com:8080/promostandards/OrderShipmentNotificationServiceBinding?wsdl`
  (test host `test-ws.sanmar.com`). One operation: `getOrderShipmentNotification`.
- Namespaces: `…/OrderShipmentNotificationService/1.0.0/` (prefix `ns`) and its
  `/SharedObjects/` (prefix `shar`).
- Auth: PromoStandards style — `<shar:wsVersion>1.0.0</shar:wsVersion>`,
  `<shar:id>` = SanMar.com username, `<shar:password>`. No customer number.

### Query types (the tool maps your input)

| stdin field | `queryType` | `referenceNumber` / selector |
| --- | --- | --- |
| `po_number` (default) | `1` | customer PO number |
| `sales_order_number` | `2` | SanMar sales-order number |
| `shipment_date` | `3` | `shipmentDateTimeStamp` (UTC, **7-day** max window) |

For queryType 3 use UTC, e.g. `2024-01-12T00:00:00Z`.

### Response → `TrackingResult`

```
OrderShipmentNotificationArray / OrderShipmentNotification
  purchaseOrderNumber, complete
  SalesOrderArray / SalesOrder
    salesOrderNumber, complete
    ShipmentLocationArray / ShipmentLocation
      ShipFromAddress {address1, city, region, postalCode, country}
      ShipToAddress   {…}
      PackageArray / Package
        trackingNumber, shipmentDate, carrier, shipmentMethod
        ItemArray / Item {supplierProductId, supplierPartId, quantity}
```

The tool flattens this to one `TrackingShipment` per **package**:
`{tracking_number, carrier` (normalized `ups`/`fedex`/`usps`)`, shipment_method,
ship_date, sales_order_number, ship_from_city, ship_from_state, ship_to_city,
ship_to_state, items: [{style, part_id, quantity}]}`, plus the PO-level
`complete` flag. (SanMar's earlier integrations extracted only tracking number +
carrier; this pulls the full package/item detail.)

> **Test env:** OSN test data requires SanMar to manually invoice your test
> orders (24–48h). Email the integration team your test PO numbers.

---

## `get-shipment-status` — FTP Daily Shipment Status (ASN)

`MM-DD-YYStatus.txt`, **tab-delimited**, one row per shipped line item, created
nightly for orders shipped that day (by request). Unlike OSN it also carries the
line/shipment **costs**. Columns A–AB (FTP Integration Guide v23.1):

| # | Field | # | Field |
| --- | --- | --- | --- |
| A | Customer PO | O | Handling Fee |
| B | SalesOrder# | P | Invoice Total |
| C | Ship From | Q | Track Num |
| D | Ship Date | R | Total Cases |
| E | Ship To Name | S | Ship Via |
| F | Attention | T | Box Number |
| G | Ship To Address1 | U | Style |
| H | Ship To Address2 | V | Description |
| I | Ship To City | W | Color |
| J | Ship To State | X | Size |
| K | Ship To Zip | Y | Qty |
| L | Ship To Country | Z | Inventory Key |
| M | Sub Total | AA | Size ID |
| N | Freight | AB | LPN (License Plate Number) |

Supply the file as inline `text`, a local `path`, or `remote_path` (SFTP; a
directory or omission fetches the newest `*Status.txt` from the outbound
folder). Filter to one order with `po_number`. Each row →
`ShipmentStatusRow` with the costs coerced to floats and Qty/Total Cases to
ints. To roll rows up to a shipment, group by `(customer_po, tracking_number)`.
