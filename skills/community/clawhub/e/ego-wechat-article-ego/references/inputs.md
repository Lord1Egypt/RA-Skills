# Inputs

The caller passes absolute paths. This skill does not bake in a home directory or a product checkout.

```bash
node skills/wechat-article-ego/scripts/save-draft.mjs \
  --markdown /absolute/path/to/article.md \
  --asset-root /absolute/path/to/assets \
  --source-url https://example.com/post \
  --expect-account "账号名称" \
  --receipt-dir /absolute/path/to/receipts \
  --screenshot-dir /absolute/path/to/shots \
  --yes --json
```

| Flag | Required | Meaning |
|------|----------|---------|
| `--markdown` | yes, for save-draft | Markdown or MDX-like text. YAML front matter may set `title` and `description`. |
| `--yes` | no | Save one new draft. Without it, exit `3` and do not upload. |
| `--title` | no | Overrides front matter. WeChat allows 64 characters. Longer titles fail before the browser opens. |
| `--digest` | no | Overrides `description`. Longer than 120 characters is clipped and reported. |
| `--source-url` | no | Fills 原文链接 only when that field is visible. |
| `--asset-root` | no | Extra directory for relative images. `../` may not escape the markdown directory or this root. |
| `--expect-account` | no | The visible nickname must match exactly. |
| `--receipt-dir` | no | Duplicate-safe receipts. Default is `$HOME/.local/state/wechat-article-ego/receipts`, or `WECHAT_ARTICLE_EGO_RECEIPT_DIR`. |
| `--screenshot-dir` | no | After a confirmed save, writes top / middle / end shots. |
| `--json` | no | Print the summary JSON on success too. |

Images may be local files or `http(s)` URLs already written in the markdown. Remote bytes are saved next to the receipt directory and then uploaded through the editor. The skill does not send the article to any other host.

Author, 原创, categories, and tags are left unset. Do not invent them.

Receipt statuses:

- `pending` — a save was about to start or was in progress
- `saved` — the draft list showed exactly one row with this title
- `uncertain` — 保存 was clicked but the draft list was not a single match
- `aborted` — the editor was opened but 保存 was not clicked

A later `--yes` for the same content hash loads that receipt. `saved` and a reconciled `pending` / `uncertain` row do not create another draft.
