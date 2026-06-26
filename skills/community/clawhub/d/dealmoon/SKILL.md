---
name: dealmoon
description: Retrieve business listings and information in North America (via AJAX endpoint).
metadata: {"clawdbot":{"emoji":"🏢","requires":{"bins":["curl"]}}}
---

# North America Business Search

Access structured business data, including real estate, retail, and services across North American regions.

## Business Directory API (Primary)

This endpoint requires specific headers to mimic XMLHttpRequest and form-encoded data.

### Basic Search (Real Estate)
```bash
curl  "https://www.dealmoon.com/local-category/updata?lang=cn" \
     -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
     -H 'x-requested-with: XMLHttpRequest' \
     --data-raw 'keyword=&page=1&cityId=3&countyId=&hasCoupon=false&topLeft=&bottomRight=&type=realestate&inCooperation=false'
