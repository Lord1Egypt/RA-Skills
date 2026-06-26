# Flight Scout Skill

This directory contains the managed files for the `flight-scout` skill.

Version: c744614da5b1

This directory contains managed skill files only.

Recommended workflow:

1. Use the official Flight Scout installer for both install and update.
2. Keep your real local configuration in `skills/flight-scout/.env`.
3. Re-run the same installer when you want to update the skill; it should preserve `.env` by default.
4. Repository releases for this skill are published automatically when `skills/flight-scout/` changes on `master`.

Manual install:

1. Copy this `flight-scout` directory into your local `skills/` directory.
2. If `skills/flight-scout/.env` does not exist, copy `.env.example` to `.env` and fill in your real API key.
3. `scripts/call_api.py` will auto-load `skills/flight-scout/.env` when it exists, so manual `source .env` is optional.

Example shell setup:

```bash
cd skills/flight-scout
cp .env.example .env
# edit .env and fill a real FLIGHT_SCOUT_API_KEY
python3 scripts/call_api.py search --from SHA --to HND --date 2026-06-12
python3 scripts/call_api.py usage --period month
```

Security note:

- This directory intentionally does not contain a live API key.
- `usage` 返回的 `data.quota` 包含当前周期已用、剩余和重置时间；如果业务请求命中额度限制，脚本会保留服务端返回的 `quota_exceeded` 错误与额度字段。
