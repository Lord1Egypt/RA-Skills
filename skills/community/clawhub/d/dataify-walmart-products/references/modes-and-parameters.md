# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Shared Dropdown Options

Dropdown options for `all_variations`:

| Label | Value |
| --- | --- |
| true | `true` |
| false | `false` |

## Product URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true` | `spider_parameters` | Walmart product URL. |
| `all_variations` | No | `false` | `spider_parameters` | Whether to collect all product variations. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.


Also ask: "Do you want to collect multiple Walmart product URL groups? If yes, provide multiple groups with `url` and `all_variations`."

Product URL mode handling:

- `url` must start with `https://www.walmart.com/`.
- `all_variations` must be `true` or `false`.
- Submit `spider_id=walmart_product_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"}]
```

## Category URL Mode Parameters

Use this section only when the user chooses `category-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `category_url` | Yes | `https://www.walmart.com/shop/deals/food/` | `spider_parameters` | Walmart category URL. |
| `all_variations` | Yes | `false` | `spider_parameters` | Whether to collect all product variations. |
| `page_turning` | Yes | `1` | `spider_parameters` | Page limit. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.


Also ask: "Do you want to collect multiple Walmart category URL groups? If yes, provide multiple groups with `category_url`, `all_variations`, and `page_turning`."

Category URL mode handling:

- `category_url` must start with `https://www.walmart.com/`.
- `all_variations` must be `true` or `false`.
- `page_turning` must be an integer greater than or equal to `0`.
- Submit `spider_id=walmart_product_by-category-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"category_url":"https://www.walmart.com/shop/deals/food/","all_variations":"false","page_turning":"1"}]
```

## SKU Mode Parameters

Use this section only when the user chooses `sku`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `sku` | Yes | `439179861` | `spider_parameters` | Walmart SKU product code. |
| `all_variations` | No | `false` | `spider_parameters` | Whether to collect all product variations. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.


Also ask: "Do you want to collect multiple Walmart SKU groups? If yes, provide multiple groups with `sku` and `all_variations`."

SKU mode handling:

- Trim leading and trailing whitespace from `sku`.
- `sku` cannot be empty.
- `all_variations` must be `true` or `false`.
- Submit `spider_id=walmart_product_by-sku`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"sku":"439179861","all_variations":"false"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keywords`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keyword` | Yes | `leggins` | `spider_parameters` | Walmart search keyword. |
| `domain` | Yes | `https://www.walmart.com/` | `spider_parameters` | Walmart main domain. |
| `all_variations` | No | `false` | `spider_parameters` | Whether to collect all product variations. |
| `page_turning` | No | `2` | `spider_parameters` | Page limit. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.


Also ask: "Do you want to collect multiple Walmart keyword groups? If yes, provide multiple groups with `keyword`, `domain`, `all_variations`, and `page_turning`."

Keyword mode handling:

- `keyword` cannot be empty.
- `domain` must start with `https://www.walmart.com/`.
- `all_variations` must be `true` or `false`.
- `page_turning` must be an integer greater than or equal to `0`.
- Submit `spider_id=walmart_product_by-keywords`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keyword":"leggins","domain":"https://www.walmart.com/","all_variations":"false","page_turning":"2"}]
```
