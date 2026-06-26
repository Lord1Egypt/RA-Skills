# Dataify Yandex Search API Fields

Endpoint: `POST https://scraperapi.dataify.com/request`

Header:

- `Authorization`: Dataify API token. Use `Bearer <token>`; the bundled script adds `Bearer ` when the provided token does not already include it. Do not show this field in the pre-call parameter table.

Body:

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `engine` | yes | `yandex` | Search engine. Keep `yandex`. |
| `text` | yes | none | Search query from the user request. |
| `json` | yes | `1` | Output format. `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON. The description default is JSON, so use `1`. |
| `yandex_domain` | no | `yandex.com` | Yandex domain. Supported examples include `yandex.com`, `yandex.ru`, `ya.ru`, `yandex.by`, `yandex.kz`, `yandex.uz`, `yandex.com.tr`, `yandex.az`, `yandex.com.ge`, `yandex.com.am`, `yandex.co.il`, `yandex.md`, `yandex.tm`, `yandex.tj`, `yandex.eu`. |
| `lang` | no | `en` when `yandex_domain` is `yandex.com` | Search language. |
| `lr` | no | none | Country or region ID to restrict results. |
| `p` | no | none | Page number. Numbering starts from `0` when specified. |
| `family_mode` | no | `1` | Safe search: `0` off, `1` moderate, `2` strict. The description default is moderate, so use `1`; do not use the example value `0` as the default. |
| `fix_typo` | no | `true` | Enable or disable automatic typo correction. |
| `groups_on_page` | no | `20` | Maximum result groups per page. |
| `no_cache` | no | `false` | `true` bypasses cache; `false` uses cache. The description says `false` is the default; do not use the example value `true` as the default. |

Before every API call, show the complete field table with `参数名`, `当前值`, `默认值`, and `说明`; omit `Authorization`. Return the response body directly to the user without transformation.
