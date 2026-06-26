# Publish to ClawHub (Public)

Use this checklist when releasing `app-legal-pages` to clawhub.com.

## 1) Login

```bash
clawhub login
clawhub whoami
```

## 2) Dry sanity checks

- Ensure `SKILL.md` frontmatter has only `name` + `description`
- Ensure folder structure includes only required files/resources
- Run generator script once with a sample feature doc

Example:

```bash
python3 scripts/generate_legal_site.py \
  --input ./sample-feature.md \
  --out ./out/legal-site \
  --app-name "Demo App" \
  --company "Demo Co" \
  --email "support@example.com" \
  --effective-date "2026-03-04" \
  --jurisdiction "Singapore"
```

## 3) Publish

```bash
clawhub publish ~/.openclaw/workspace/skills/app-legal-pages \
  --slug app-legal-pages \
  --name "App Legal Pages" \
  --version 0.1.0 \
  --tags latest,legal,privacy,terms,cloudflare,github
```

## 4) Verify listing

```bash
clawhub inspect app-legal-pages
clawhub search "app legal privacy terms"
```

## 5) Update release

```bash
clawhub publish ~/.openclaw/workspace/skills/app-legal-pages \
  --slug app-legal-pages \
  --version 0.1.1 \
  --changelog "Improve input checklist and SDK/permission detection" \
  --tags latest,legal,privacy,terms,cloudflare,github
```
