# Worker Setup

## 1) Deploy backend

```bash
cd <PROJECTS_ROOT>/agent-fleet-backend
wrangler kv namespace create FLEET_KV
```

Put returned namespace id into `wrangler.jsonc` binding `FLEET_KV.id`.

## 2) Set secrets

```bash
wrangler secret put INGEST_TOKEN
wrangler secret put READ_TOKEN
```

## 3) Deploy

```bash
npm install
npm run deploy
```

## 4) Verify

```bash
curl https://<worker>.workers.dev/health
```

`GET /fleet` requires Authorization bearer token.
