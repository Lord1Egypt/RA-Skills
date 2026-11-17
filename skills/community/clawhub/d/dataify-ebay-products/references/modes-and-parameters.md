# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Product URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm` | `spider_parameters` | eBay product URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple eBay product URL groups? If yes, provide multiple `url` values."

Product URL mode handling:

- `url` must start with `https://www.ebay.com/`.
- Submit `spider_id=ebay_ebay_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"}]
```

## Category URL Mode Parameters

Use this section only when the user chooses `category-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829` | `spider_parameters` | eBay category URL. |
| `Count` | No | `60` | `spider_parameters` | Count field required by this collector. Must be an integer greater than or equal to `0`. |
| `count` | No | `60` | `spider_parameters` | Quantity field. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple eBay category URL groups? If yes, provide multiple groups with `url`, `Count`, and `count`."

Category URL mode handling:

- `url` must start with `https://www.ebay.com/`.
- `Count` must be an integer greater than or equal to `0`.
- `count` must be an integer greater than or equal to `0`.
- Submit both `Count` and `count` exactly as separate fields.
- Submit `spider_id=ebay_ebay_by-category-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829","Count":"60","count":"60"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keywords`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keywords` | Yes | `baby toys` | `spider_parameters` | eBay search keyword. |
| `count` | No | `60` | `spider_parameters` | Quantity field. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple eBay keyword groups? If yes, provide multiple groups with `keywords` and `count`."

Keyword mode handling:

- `keywords` cannot be empty.
- `count` must be an integer greater than or equal to `0`.
- Submit `spider_id=ebay_ebay_by-keywords`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keywords":"baby toys","count":"60"}]
```

## Store URL Mode Parameters

Use this section only when the user chooses `listurl`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086` | `spider_parameters` | eBay store URL. |
| `count` | No | `60` | `spider_parameters` | Quantity field. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple eBay store URL groups? If yes, provide multiple groups with `url` and `count`."

Store URL mode handling:

- `url` must start with `https://www.ebay.com/`.
- `count` must be an integer greater than or equal to `0`.
- Submit `spider_id=ebay_ebay_by-listurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086","count":"60"}]
```
