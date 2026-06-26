# ClawHub Publish Command

## 1. Login first

```bash
clawhub login
clawhub whoami
```

## 2. Publish command

```bash
clawhub publish /root/.openclaw/workspace/skills/ccdb-factor-search \
  --slug ccdb-factor-search \
  --name "CCDB Factor Search" \
  --version 0.1.3 \
  --tags carbon,emission-factor,ccdb,sustainability,lca,search \
  --changelog "0.1.3 improves best-fit factor selection with richer README/docs, confirmed API field meanings, better geo-sensitive matching, latest-factor recency handling, stronger authority weighting, clearer carbon-footprint vs emission-factor distinction, and safer direct-use guidance."
```

## 3. Suggested follow-up checks

After publishing, check:

```bash
clawhub whoami
clawhub inspect ccdb-factor-search
```

If later you update the skill, bump the version and publish again.
