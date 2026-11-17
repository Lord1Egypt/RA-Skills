# Ownership (Enterprise)

Registered owners and residents. Requires an Enterprise `ownership` entitlement. Billed per returned record (`owners` / `matches` / `records`), not per request.

Do **not** call `/v1/ownership/phone`.

`include` is optional: comma-separated `demographics,emails,phones,vehicle_history`. Omit it to get everything. `include` only shapes which sections are shown; it does not change billing.

Street `address` is street only — no city or state (max 100). ZIP is 5-digit US (person/address may be ZIP+4; zip lookup is exactly 5 digits).

HTTP 404 / `error: "no_data"` means no match and is **not** billed. HTTP 401 / entitlement error means the key is not entitled.

## VIN

```
GET https://api.carsxe.com/v1/ownership/vin?key=$CARSXE_KEY&vin={VIN}&source=openclaw[&include={INCLUDE}]
```

Required: 17-character VIN.

## Person

```
GET https://api.carsxe.com/v1/ownership/person?key=$CARSXE_KEY&first_name={FIRST}&last_name={LAST}&address={ADDRESS}&zip={ZIP}&source=openclaw[&include={INCLUDE}]
```

Required: `first_name`, `last_name`, street `address`, `zip`.

## Address

```
GET https://api.carsxe.com/v1/ownership/address?key=$CARSXE_KEY&address={ADDRESS}&zip={ZIP}&source=openclaw[&include={INCLUDE}]
```

Required: street `address`, `zip`.

## ZIP

```
GET https://api.carsxe.com/v1/ownership/zip?key=$CARSXE_KEY&zip={ZIP}&source=openclaw[&gender={GENDER}][&min_age={MIN}][&max_age={MAX}][&income={INCOME}][&page={PAGE}][&limit={LIMIT}][&include={INCLUDE}]
```

Required: 5-digit `zip`. Optional: `gender` (`M` or `F`), `min_age`, `max_age`, `income` (code or label), `page` (default 1), `limit` (default 15, max 100).

Warn before a ZIP search with a high `limit` — one page can bill many units.
