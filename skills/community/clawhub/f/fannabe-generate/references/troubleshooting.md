# Troubleshooting

## "Not logged in" / 401
Ask the user to run `fannabe auth login` (opens a browser) and confirm when done. The token caches in `~/.fannabe`.

## Insufficient credits
`fannabe account` shows the balance. Every generation prints its estimated cost first; preview with `fannabe generate cost <aiId> ...` before spending.

## A job "failed" with no output
Only completed jobs have downloadable media. Inspect with `fannabe jobs get <taskId>`; failed jobs carry an error message and refund credits automatically.

## Wrong id used on `--source`
`--source` needs the Media id (the `Media ID (--source)` column), not the Content id. See source-media.md.

## Non-production environments
Point at staging/dev with `FANNABE_API_URL=<url>` and keep its login separate with `FANNABE_CONFIG_DIR=~/.fannabe-staging` (both env vars). A token minted against one environment will 401 on another.

## AI field rejected
Read `fannabe ai schema <aiId>` for the exact fields and whether they are simple-mode or expert-mode; do not guess.
