---
name: dataify-yandex-search
description: Use this skill when the user wants to search Yandex
---

# Dataify Yandex Search

## Workflow

1. Read the user's request and map it to the API fields below.
2. Apply defaults from the parameter descriptions only. Do not use the example YAML body as the source of defaults.
3. Before every API call, run the bundled script with `--preview` and show the complete table to the user:

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

4. Ask the user whether they want to modify any parameters. Do not call the API until the user confirms.
5. If the user requests changes, adjust the arguments, show the complete preview table again, and ask for confirmation again.
6. After confirmation, check the token. If the user did not provide a token and `DATAIFY_API_TOKEN` is not available, stop and ask the user to provide a Dataify API token or register at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill).
7. Call the API with the confirmed parameters:

```bash
python3 scripts/yandex_search.py --text "<search query>" --token "<token>"
```

8. Return the script stdout directly to the user. Do not parse, summarize, translate, filter, reformat, or otherwise process the API response.


## Preview Table

Always show a complete field list before calling the API. Do not include `Authorization` in the table. The table must contain only these columns:

- `参数名`
- `当前值`
- `默认值`
- `说明`

The bundled script generates this table with:

```bash
python3 scripts/yandex_search.py --text "<search query>" --preview
```

## Defaults

Use these documented defaults when the user does not specify a field:

- `engine`: `yandex`
- `json`: `1`
- `yandex_domain`: `yandex.com`
- `lang`: `en` when `yandex_domain` is `yandex.com`
- `family_mode`: `1`
- `fix_typo`: `true`
- `groups_on_page`: `20`
- `no_cache`: `false`

No documented default:

- `text`: required from the user request.
- `lr`: leave unset unless the user specifies it.
- `p`: leave unset unless the user specifies it; page numbering starts from `0` when specified.

Important corrections from the API example body:

- Do not treat example `family_mode: "0"` as the default. The description default is medium, so use `1`.
- Do not treat example `no_cache: "true"` as the default. The description says `false` is the default.

## Field Mapping

- `--json`: output format. Use `1` JSON, `2` JSON+HTML, `3` HTML, or `4` Light JSON.
- `--yandex-domain`: Yandex domain such as `yandex.com`, `yandex.ru`, `ya.ru`, `yandex.kz`, `yandex.com.tr`, or another supported domain.
- `--lang`: search language, for example `en`, `ru`, `tr`.
- `--lr`: country or region ID.
- `--p`: page number, starting from `0`.
- `--family-mode`: safe search mode. Use `0` off, `1` moderate, `2` strict.
- `--fix-typo`: `true` or `false`.
- `--groups-on-page`: maximum result groups per page.
- `--no-cache`: `true` to bypass cache, `false` to use cache.
- `--params-json`: JSON object of raw field overrides for unusual requests. Use `null` to omit a defaulted field.

For the full field list, read `references/api_fields.md` only when needed.

## Examples

Preview parameters for a normal search:

```bash
python3 scripts/yandex_search.py --text "OpenAI latest news" --preview
```

After user confirmation, call the API:

```bash
python3 scripts/yandex_search.py --text "OpenAI latest news" --token "$DATAIFY_API_TOKEN"
```

Preview Russian Yandex, page 2, HTML output:

```bash
python3 scripts/yandex_search.py --text "artificial intelligence news" --yandex-domain yandex.ru --lang ru --p 1 --json 3 --preview
```
