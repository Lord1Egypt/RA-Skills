---
name: getpost-mail
description: "Buy shipping labels, get rates, and track parcels via API."
version: "1.0.0"
---

# GetPost Mail & Shipping API

Buy shipping labels, get rates, and track parcels via API. Powered by EasyPost — access USPS, UPS, FedEx, and more.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key from the response
```

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Get Shipping Rates
```bash
curl -X POST https://getpost.dev/api/mail/rates \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"name": "Sender", "street1": "123 Main St", "city": "SF", "state": "CA", "zip": "94105", "country": "US"},
    "to": {"name": "Recipient", "street1": "456 Oak Ave", "city": "LA", "state": "CA", "zip": "90001", "country": "US"},
    "parcel": {"length": 10, "width": 8, "height": 4, "weight": 16}
  }'
```

## Buy a Label
```bash
curl -X POST https://getpost.dev/api/mail/labels \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"rate_id": "rate_xxx", "shipment_id": "shp_xxx"}'
```

## Track Shipment
```bash
curl https://getpost.dev/api/mail/track/{tracking_id} \
  -H "Authorization: Bearer gp_live_YOUR_KEY"
```

## Full Docs
https://getpost.dev/docs/api-reference#mail
