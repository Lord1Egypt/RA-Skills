---
name: api-indonesia
description: Look up Indonesian public data through API Indonesia (apiindonesia.id). Use when a task needs Indonesian administrative regions (provinces down to villages) and postal codes, region boundaries (GeoJSON), public holidays and cuti bersama, prayer times, Hijri dates, schools (NPSN), universities, hospitals, BMKG earthquakes, weather and warnings, air quality, Bank Indonesia exchange rates, minimum wage (UMP), NIK/NPWP format checks, QRIS parsing, rupiah formatting and terbilang, halal (BPJPH) and BPOM lookups, DJKI trademarks, OJK legal and illegal investment lists, food prices, Transjakarta routes, KBBI, Al-Quran or Alkitab.
license: MIT
homepage: https://apiindonesia.id
metadata:
  author: Khaisa Studio
  version: "1.0.0"
---

# API Indonesia

API Indonesia is one REST API (plus a remote MCP server) for Indonesian public data from official sources such as Kemendagri, Kemendikdasmen, Kemenkes, BMKG, Bank Indonesia, BPJPH, BPOM, DJKI and OJK. Every response uses the same JSON envelope.

## 1. Get an API key (the human does this)

You cannot create a key yourself. Ask the human to:

1. Sign up at https://dashboard.apiindonesia.id/register (3,000 free credits, no card).
2. Open **API Keys**, create a key and give it to you. Keys start with `aip_live_`.

Treat the key as a secret. Do not echo it back, commit it, or write it to a shared file. Prefer an environment variable such as `API_INDONESIA_KEY`.

Pricing: a successful request costs 2 credits (Rp2). Failed requests (bad input, upstream error) are not billed.

## 2. Pick a way to call it

**MCP (preferred for agents).** Streamable HTTP server:

- URL: `https://mcp.apiindonesia.id/mcp`
- Header: `Authorization: Bearer <API key>`

```json
{"mcpServers": {"api-indonesia": {"url": "https://mcp.apiindonesia.id/mcp", "headers": {"Authorization": "Bearer ${API_INDONESIA_KEY}"}}}}
```

To add the server to other local agents (Claude Code, Codex, Cursor, VS Code, opencode, Gemini CLI, Windsurf, Zed, Claude Desktop), the human can run the installer described at https://docs.apiindonesia.id . It needs macOS or Linux with Node.js 18+.

**REST.** Base URL `https://use.apiindonesia.id`, header `x-api-key: <API key>`.

```sh
curl -s "https://use.apiindonesia.id/api/v1/libur/upcoming" -H "x-api-key: <API key>"
```

Full reference: https://apiindonesia.id/openapi.json (OpenAPI 3.1) and https://apiindonesia.id/llms-full.txt.

## 3. Common endpoints (all GET unless noted, prefix `/api/v1`)

| Need | Endpoint |
|---|---|
| Regions | `/wilayah/provinsi`, `/wilayah/provinsi/{id}/kabupaten`, `/wilayah/kabupaten/{id}/kecamatan`, `/wilayah/kecamatan/{id}/kelurahan`, `/wilayah/search?q=` |
| Region boundaries (GeoJSON) | `/wilayah-boundary/{code}` |
| Postal codes | `/kodepos/search?q=`, `/kodepos/lookup` |
| Holidays and cuti bersama | `/libur?tahun=`, `/libur/upcoming` |
| Prayer times | `/sholat/list-kota`, `/sholat?kabupaten_id=&tanggal=`, `/sholat/monthly` |
| Hijri calendar | `/hijriah/konversi`, `/hijriah/kalender` |
| Schools, universities, hospitals | `/sekolah/search?q=`, `/sekolah/{npsn}`, `/kampus/search`, `/rumah-sakit/search` |
| BMKG | `/gempa/terkini`, `/gempa/dirasakan`, `/cuaca?adm4=<village code>`, `/peringatan-dini`, `/kualitas-udara/{city}` |
| Exchange rates | `/kurs-bi/latest`, `/kurs-bi/history`, `/kurs/latest` |
| Minimum wage | `/ump`, `/ump/{province_code}/{year}` |
| Validation (POST) | `/validasi/nik`, `/validasi/npwp`; bank list `/validasi/bank` |
| Rupiah and QRIS (POST) | `/util/rupiah/format`, `/util/rupiah/terbilang`, `/util/qris/parse` |
| Halal, BPOM | `/halal?q=`, `/bpom?q=`, `/bpom/{nie}` |
| Trademarks (DJKI) | `/merek/search?q=`, `/merek/{appNumber}`, `/merek/journal` |
| OJK investments | `/ojk/products`, `/ojk/apps`, `/ojk/illegals` |
| Others | `/harga-pangan`, `/transjakarta/rute`, `/kbbi/word/{word}`, `/quran/surah/{id}`, `/alkitab/verse/{book}/{chapter}/{verse}`, `/astronomi/sun`, `/plates/{code}` |

Check exact parameters in the OpenAPI spec before calling an endpoint you have not used yet.

## 4. Rules

- Format checks on NIK and NPWP only confirm the number is well-formed. They do not confirm a real person or taxpayer exists. Say so when you report a result.
- Cite the data source shown in the response metadata when you present data to the human.
- If `use.apiindonesia.id` or `mcp.apiindonesia.id` is unreachable (proxy 403, DNS failure, timeout), tell the human their network policy blocks it and stop. Do not try other hosts.
- A 401 means the key is missing or wrong. A 402 means the account is out of credits; point the human to https://dashboard.apiindonesia.id to top up.
