# Bitly API notes

Base API URL:
- `https://api-ssl.bitly.com/v4`

Auth:
- Bearer token in `Authorization: Bearer ...`

Core endpoints used by this skill:
- `GET /user` — current account info
- `GET /groups` — accessible groups
- `GET /groups/{group_guid}/bitlinks` — recent/searchable links for a group
- `POST /shorten` — create a bitlink from a long URL
- `GET /bitlinks/{bitlink}` — inspect a single bitlink
- `GET /bitlinks/{bitlink}/clicks` — click metrics
- `POST /custom_bitlinks?custom_bitlink=...` — custom alias creation

Notes:
- This skill prefers a local `.env` file outside the skill folder for secrets.
- The script uses `certifi` when available to avoid local Windows/Python CA-chain issues.
- If `BITLY_DEFAULT_GROUP_GUID` is set in the env file, the CLI uses it before auto-picking the first available group.
