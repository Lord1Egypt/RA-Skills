# Output files

All files are written to the `--workdir` folder.

| File | Purpose |
|---|---|
| `input.csv` | The URL list (header: `url`, `website`, `link`, `domain` or `site`). |
| `output.csv` | Results, rewritten atomically after every URL. One row per email; one row for a site with none. |
| `suspicious.csv` | Emails flagged as likely typos (TLD like `.con`, provider typos like `gmial.com`). Never auto-corrected. |
| `cache.json` | Checkpoint: `{ "<url as written in input>": [rows…] }`. Used for resume. Errors are cached too. |
| `run.log` | Optional: stdout/stderr if you redirected it. |
| `*_archived_<timestamp>.*` | Created by `--fresh`; previous run's files. |

## output.csv columns (unchanged from the original script)

| Column | Meaning |
|---|---|
| `url` | Normalized site URL that was scraped |
| `business_name` | Guessed from the domain (e.g. `acme-plumbing.com` → `acme plumbing`) — a guess, not verified |
| `email` | Lower-cased email; empty if none found |
| `phone` | Phones found on the site (`tel:` links, JSON-LD, visible text), ` | `-separated |
| `email_count` | Number of emails found for this URL |
| `email_source` | `mailto`, `json-ld`, `data-email`, `data-mail`, `attr-*`, `cloudflare`, `text`, `deobfuscated`, `html` |
| `confidence` | `high` / `medium` / `low` (see below) |
| `suspicious` | Always `false` in output.csv (suspicious ones go to suspicious.csv) |
| `notes` | Repairs applied, e.g. `decoded-escape`, `stripped-phone-prefix` |
| `source_page` | Page the email was found on |
| `fb_page_url` | Facebook link published on the site (hint only; skill version never visits Facebook) |
| `channel` | `website` for found rows |
| `status` | `found`, `not_found`, `blocked` (HTTP 429/403/503; added in the skill version), `error` |
| `error` | Reason for `error` / `blocked` rows |
| `scraped_at` | ISO timestamp |

## Confidence
- **high** – `mailto:` link, JSON-LD `email`, `data-email`/`data-mail`, Cloudflare-protected email decoded.
- **medium** – visible page text, `aria-label`/`content`/`title`/`alt`/`value` attributes, `name [at] domain [dot] com` de-obfuscation.
- **low** – match only in raw HTML (scripts, comments). Verify before use.

The scraper's crawl stops early once it has at least one high/medium email for a site.
