# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Parameter Checklists

### Product URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.amazon.com/dp/B0CHHSFMRL/` | Amazon product URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Submit `spider_parameters` as an array with one object, for example `[{"url":"https://www.amazon.com/dp/B0CHHSFMRL/"}]`.

### Category URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.amazon.com/s?i=luggage-intl-ship` | Amazon category URL. |
| `maximum` | Yes | `5` | Integer greater than or equal to `0`. |
| `sort_by` | No | `Best Sellers` | Dropdown-style option. |
| `get_sponsored` | No | `true` | Dropdown-style option: `true` or `false`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |


| Label | Value |
| --- | --- |
| `Best Sellers` | `Best Sellers` |
| `Newest Arrivals` | `Newest Arrivals` |
| `Avg. Customer Review` | `Avg. Customer Review` |
| `Price: High to Low` | `Price: High to Low` |
| `Price: Low to High` | `Price: Low to High` |
| `Featured` | `Featured` |


| Label | Value |
| --- | --- |
| `Include Sponsored Products` | `true` |
| `Exclude Sponsored Products` | `false` |

Accepted `sort_by` display values and submitted values:

- best sellers or `Best Sellers` -> `Best Sellers`
- newest arrivals or `Newest Arrivals` -> `Newest Arrivals`
- average customer review or `Avg. Customer Review` -> `Avg. Customer Review`
- price high to low or `Price: High to Low` -> `Price: High to Low`
- price low to high or `Price: Low to High` -> `Price: Low to High`
- featured recommendations or `Featured` -> `Featured`

### Keyword

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `coffee` | Amazon search keyword. |
| `domain` | Yes | `https://www.amazon.com` | Amazon domain. |
| `lowest_price` | No | `20` | Integer greater than or equal to `0`. |
| `highest_price` | No | `50` | Integer greater than or equal to `0`, and must not be less than `lowest_price`. |
| `page_turning` | No | `2` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Require `highest_price >= lowest_price`.

### Keyword Brand

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `shirts` | Amazon search keyword. |
| `brands` | Yes | `Adidas` | Brand filter. |
| `page_turning` | Yes | `2` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |
