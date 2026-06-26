# Dataify Indeed Companies Info API Reference

Endpoint: `https://scraperapi.dataify.com/builder?platform=1`

Submit requests as form data with an `Authorization: Bearer <token>` header.

| Field | Required | Default | Description |
|---|---:|---|---|
| `spider_name` | Yes | `indeed.com` | Fixed spider platform name. |
| `spider_id` | Yes | None | One of the supported Indeed company information spider IDs. |
| `spider_parameters` | Yes | Depends on spider ID | JSON array of one or more parameter objects. |
| `spider_errors` | Yes | `true` | Include spider error details. |
| `file_name` | No | `{{TasksID}}` | Output file name. |

| Spider ID | Parameter object fields | Default parameter object |
|---|---|---|
| `indeed_companies-info_by-company-list-url` | `company_list_url` | `{"company_list_url":"https://www.indeed.com/companies/browse-companies"}` |
| `indeed_companies-info_by-keyword` | `keyword` | `{"keyword":"openai"}` |
| `indeed_companies-info_by-industry-and-state` | `industry`, `state` | `{"industry":"All","state":"United States"}` |
| `indeed_companies-info_by-company-url` | `company_url` | `{"company_url":"https://www.indeed.com/cmp/Allstate-Insurance"}` |

Use `scripts/preview_params.py --dropdown industry` and `scripts/preview_params.py --dropdown state` to print complete dropdown tables with `Label` and `Value` columns.
