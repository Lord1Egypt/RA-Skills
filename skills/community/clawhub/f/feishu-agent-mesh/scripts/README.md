# Scripts

## feishu-callback-server.js

Minimal Feishu webhook handler that:
1. Responds to `url_verification` challenges.
2. Decrypts message events using `ENCRYPT_KEY`.
3. Appends events to the configured log store (defaults to Feishu Bitable).

### Quick start
```bash
cd skills/feishu-agent-mesh/scripts
npm install express body-parser node-fetch crypto
cp ../templates/.env.example .env   # optional helper
node feishu-callback-server.js
```

Environment variables (see `.env.example` if you create one):
- `APP_ID`, `APP_SECRET`, `ENCRYPT_KEY`, `VERIFICATION_TOKEN`
- `BITABLE_APP_TOKEN`, `BITABLE_TABLE_ID`
- `LOG_FIELDS_*` (optional) to map custom column names
- `PORT` (defaults to 8787)

Mount this service behind HTTPS (e.g., `https://relay.example.com/feishu/callback`) and point all Feishu bot event subscriptions to the same URL.
