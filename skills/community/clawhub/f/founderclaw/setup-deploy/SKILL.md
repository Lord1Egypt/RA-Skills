---
name: setup-deploy
description: >
  Configure deployment settings for land-and-deploy. Detects your deploy
  platform (Fly.io, Render, Vercel, Netlify, Heroku, GitHub Actions, custom),
  production URL, health check endpoints, and deploy commands.
  Use when: "setup deploy", "configure deployment", "set up land-and-deploy",
  "how do I deploy".
---

# Setup Deploy

Configure deployment so `land-and-deploy` works automatically. One-time setup per project.

## Step 1: Detect Platform

Check for platform indicators in the project:

```bash
# Vercel
[ -f vercel.json ] && echo "PLATFORM: vercel"
# Netlify
[ -f netlify.toml ] && echo "PLATFORM: netlify"
# Fly.io
[ -f fly.toml ] && echo "PLATFORM: fly"
# Render
[ -f render.yaml ] && echo "PLATFORM: render"
# Heroku
[ -f Procfile ] && echo "PLATFORM: heroku"
# Docker
[ -f Dockerfile ] && echo "PLATFORM: docker"
# GitHub Actions
[ -d .github/workflows ] && ls .github/workflows/*.yml 2>/dev/null | head -3
# Cloudflare Workers
[ -f wrangler.toml ] && echo "PLATFORM: cloudflare-workers"
# Railway
[ -f railway.json ] || [ -f railway.toml ] && echo "PLATFORM: railway"
```

Also check `package.json` for deploy scripts:

```bash
cat package.json 2>/dev/null | grep -A5 '"scripts"' | grep -i "deploy\|ship\|release"
```

## Step 2: Detect Production URL

Try to find the production URL:

```bash
# From vercel.json
cat vercel.json 2>/dev/null | grep -o '"url":[^,}]*'
# From fly.toml
grep "primary_region\|app\s*=" fly.toml 2>/dev/null
# From package.json homepage
cat package.json 2>/dev/null | grep '"homepage"' | grep -o 'https://[^"]*'
# From README badges
grep -o 'https://[^ ]*\.vercel\.app\|https://[^ ]*\.netlify\.app\|https://[^ ]*\.onrender\.com\|https://[^ ]*\.fly.dev\|https://[^ ]*\.herokuapp\.com' README.md 2>/dev/null | head -1
```

## Step 3: Detect Health Check

```bash
# Common health check paths
for path in /health /healthz /api/health /api/healthz /api/status /_health /ping; do
    echo "  $path"
done
```

Ask the user: "What's your health check endpoint? (e.g., /health, /api/healthz)"

## Step 4: Configure

Create or update `founderclaw/data/deploy-config.json` in the project root:

```bash
CONFIG_FILE=".founderclaw-deploy.json"

# Detect values
PLATFORM=$(detect_platform)  # from Step 1
PRODUCTION_URL=$(detect_url)  # from Step 2

cat > "$CONFIG_FILE" << EOF
{
  "platform": "$PLATFORM",
  "productionUrl": "$PRODUCTION_URL",
  "healthCheck": "/health",
  "deployCommand": "fly deploy",
  "statusCommand": "fly status",
  "setupDate": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "Deploy config written to $CONFIG_FILE"
```

## Platform-Specific Setup

### Vercel
```bash
# Deploy command
vercel --prod
# Status
vercel ls
```

### Fly.io
```bash
# Deploy command
fly deploy
# Status
fly status
# Logs
fly logs
```

### Render
```bash
# Deploy via git push
git push origin main
# Or manual trigger
curl -X POST "$RENDER_DEPLOY_HOOK"
```

### Netlify
```bash
# Deploy command
netlify deploy --prod
# Status
netlify status
```

### Heroku
```bash
# Deploy command
git push heroku main
# Status
heroku ps
# Logs
heroku logs --tail
```

### Docker / Custom
```bash
# Build
docker build -t myapp .
# Deploy
docker push registry/myapp:latest
# SSH deploy
ssh server "cd /app && git pull && docker compose up -d"
```

### GitHub Actions
```bash
# Trigger deploy workflow
gh workflow run deploy.yml
# Check status
gh run list --workflow=deploy.yml --limit=1
```

## Step 5: Verify

Test the health check:

```bash
PRODUCTION_URL=$(cat "$CONFIG_FILE" | grep -o '"productionUrl":"[^"]*"' | cut -d'"' -f4)
HEALTH_PATH=$(cat "$CONFIG_FILE" | grep -o '"healthCheck":"[^"]*"' | cut -d'"' -f4)

curl -s "$PRODUCTION_URL$HEALTH_PATH" | head -5
```

If the health check passes, deploy config is ready.

## What This Enables

After setup, `land-and-deploy` can automatically:
1. Run tests
2. Build the project
3. Deploy to your platform
4. Wait for health check to pass
5. Report success/failure

No more looking up deploy commands every time.

## Update Config

To change settings later, edit `.founderclaw-deploy.json` directly or re-run this skill.
