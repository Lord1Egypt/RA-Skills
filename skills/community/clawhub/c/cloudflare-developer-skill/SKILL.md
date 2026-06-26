# Cloudflare Developer Platform Skill

## Description
Complete Cloudflare Developer Platform knowledge: Workers, Pages, D1, R2, KV, AI, security best practices, and deployment patterns.

## Quick Actions

### Deploy Workers
```bash
# Init new Worker
wrangler init my-worker

# Dev local
wrangler dev

# Deploy production
wrangler deploy
```

### Setup D1 Database
```bash
# Create database
wrangler d1 create my-db

# Add to wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"

# Run migrations
wrangler d1 migrations apply my-db
```

### Setup R2 Bucket
```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Add to wrangler.toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

## Decision Trees

### Storage Choice
- **Config, feature flags, session tokens** → KV
- **Structured data (SQL tables)** → D1
- **Files, uploads, backups** → R2

### SSL/TLS Mode
- Origin has valid cert → Full (strict) ✅
- Origin self-signed cert → Full
- Origin HTTP only → Flexible (last resort)

### Cache Strategy
- Static assets (/assets/*, *.css, *.js) → Cache, long TTL
- Public HTML (no session) → Cache, medium TTL
- Dynamic HTML (session) → Bypass
- API with auth → Bypass
- Admin/checkout → Bypass

## Best Practices

### Workers
- Always use bindings (env.KV, env.DB, env.MY_BUCKET) instead of REST API
- Await all Promises or use ctx.waitUntil() for background tasks
- Custom domain: Worker as origin, DNS record must be proxied (orange cloud)
- Debug: wrangler tail

### D1
- Create indexes for columns in WHERE clause (email, user_id)
- ONLY index frequently queried columns
- Run migrations: wrangler d1 migrations apply

### Security
- WAF rollout: Log → Simulate (24-48h) → Block
- SSL: Full (strict) when you have valid cert
- DO NOT proxy MX records
- Origin firewall: only allow Cloudflare IPs

### Performance
- Enable Tiered Cache (free)
- DO NOT cache HTML with sessions → data leak
- Bypass cache for /admin, /checkout, /api with cookies
- Check CF-Cache-Status header

## Common Mistakes & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Worker 404 | Route missing DNS proxied | Add DNS record + orange cloud |
| Email down | MX record proxied | Remove proxy from MX |
| Redirect loop | SSL Flexible + HTTPS origin | Change to Full (strict) |
| Data leak | Cache HTML with session | Bypass dynamic pages |
| KV inconsistent | Eventually consistent model | Use D1 for transactional data |
| D1 slow | Missing index | Index columns in WHERE |

## Architecture Patterns

### Fullstack App
```
User → Pages (frontend) → Pages Functions (/api/*) → D1 + KV + R2
```

### API with Workers
```
Client → Custom domain (Worker) → D1/KV/external API
```

### RAG with Workers AI
```
User → Worker → AI Gateway → Workers AI (embedding) → Vectorize → LLM
```

## Troubleshooting

### Worker not running
1. Check wrangler.toml routes
2. Verify DNS record proxied (orange cloud)
3. Check wrangler tail logs
4. Test with wrangler dev local

### D1 migration error
1. Check SQL syntax
2. Verify binding in wrangler.toml
3. Dry run: wrangler d1 migrations list

### Cache not hitting
1. Check CF-Cache-Status header
2. Verify Cache Rules
3. Enable Tiered Cache
4. Review bypass rules

## Resources
- Official docs: https://developers.cloudflare.com/
- Learning Hub: https://onboarding.orangecloud.vn/
- Changelog: https://developers.cloudflare.com/changelog/
- Community: https://community.cloudflare.com/

---
**Last updated:** 2026-06-03  
**Source:** Cloudflare Starter Hub complete learning path
