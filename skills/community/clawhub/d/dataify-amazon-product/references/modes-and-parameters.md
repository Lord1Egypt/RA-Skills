# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Parameter Checklists

### ASIN

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `asin` | Yes | No default | One or more ASINs. Amazon product URLs can be accepted and converted to ASINs. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Submit multiple ASINs as an array of objects, for example `[{"asin":"B0BZYCJK89"}]`.

### Product URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | No default | One or more complete Amazon product URLs. |
| `zip_code` | Yes | No default | Zip code used for each Amazon URL, for example `94107`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Submit multiple URLs as an array of objects, for example `[{"url":"https://www.amazon.com/.../dp/B0BRXPR726","zip_code":"94107"}]`.

### Keyword

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | No default | Amazon search keyword. |
| `page_turning` | No | `2` | Integer greater than or equal to `1`. |
| `lowest_price` | No | `10` | Lowest price filter. |
| `highest_price` | No | `50` | Highest price filter. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Require `lowest_price <= highest_price`.

### Category URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | No default | Amazon category URL. |
| `page_turning` | Yes | No default | Integer greater than or equal to `1`. |
| `sort_by` | No | `Best Sellers` | Dropdown-style option. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |


| Label | Value |
| --- | --- |
| `Best Sellers` | `Best Sellers` |
| `Newest Arrivals` | `Newest Arrivals` |
| `Avg. Customer Review` | `Avg. Customer Review` |
| `Price: High to Low` | `Price: High to Low` |
| `Price: Low to High` | `Price: Low to High` |
| `Featured` | `Featured` |

Accepted `sort_by` display values and submitted values:

- best sellers or `Best Sellers` -> `Best Sellers`
- newest arrivals or `Newest Arrivals` -> `Newest Arrivals`
- average customer review or `Avg. Customer Review` -> `Avg. Customer Review`
- price high to low or `Price: High to Low` -> `Price: High to Low`
- price low to high or `Price: Low to High` -> `Price: Low to High`
- featured recommendations or `Featured` -> `Featured`

### Best Sellers URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | No default | Amazon Best Sellers category URL. |
| `page_turning` | Yes | No default | Integer greater than or equal to `1`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |
