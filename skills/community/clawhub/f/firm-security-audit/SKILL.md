---
name: firm-security-audit
version: 1.0.0
description: >
  Audit de sécurité proactif des déploiements OpenClaw.
  Détecte et remédie aux 4 gaps critiques/hauts identifiés dans openclaw/openclaw :
  SQL injection (C1), sandbox off par défaut (C2), session secret éphémère (C3),
  absence de rate limiting (H8), et documentation sécurité incomplète (M10).
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 2.0.0
tags:
  - security
  - audit
  - compliance
  - hardening
  - devops
---

# firm-security-audit

> ⚠️ Contenu généré par IA — validation par un expert sécurité requise avant toute modification en production.

## Purpose

Ce skill est la **porte de sécurité obligatoire** avant tout déploiement ou exposition
réseau d'un Gateway OpenClaw. Il comble directement les gaps critiques identifiés dans
`openclaw/openclaw` depuis l'extérieur du repo, sans modifier le code upstream.

**Gaps couverts :**
| Gap | Sévérité | Outil |
|-----|----------|-------|
| C1 — SQL injection `/api/metrics/database` | CRITICAL | `openclaw_security_scan` |
| C2 — `sandbox.mode: off` par défaut | CRITICAL | `openclaw_sandbox_audit` |
| C3 — Session secret régénéré au restart | HIGH | `openclaw_session_config_check` |
| H8 — Absence de rate limiting sur WS Gateway | HIGH | `openclaw_rate_limit_check` |
| M10 — Matrix E2EE status non documenté | MEDIUM | checklist documentaire |

## Tools activés

```
openclaw_security_scan         — détection SQL injection (C1)
openclaw_sandbox_audit         — vérification sandbox config (C2)
openclaw_session_config_check  — contrôle session secret persistance (C3)
openclaw_rate_limit_check      — vérification rate limiter (H8)
firm_export_slack_digest       — notification équipe si CRITICAL trouvé
```

## Séquence d'audit obligatoire

**À exécuter avant chaque déploiement ou avant activation de Tailscale Funnel.**

### Étape 1 — Sandbox audit (C2, priorité CRITIQUE)

```json
{
  "tool": "openclaw_sandbox_audit",
  "args": {
    "config_path": "/path/to/.openclaw/config.yaml"
  }
}
```
**Attendu :** `severity: OK` avec `sandbox_mode: non-main` ou `all`
**Si CRITICAL :** appliquer le fix_snippet fourni **avant de continuer**

### Étape 2 — SQL injection scan (C1)

```json
{
  "tool": "openclaw_security_scan",
  "args": {
    "target_path": "/path/to/openclaw/src/api",
    "endpoint": "/api/metrics/database",
    "scan_depth": 4
  }
}
```
**Attendu :** `critical_count: 0`, `high_count: 0`
**Si CRITICAL ou HIGH :** appliquer `remediation_by_severity` avant déploiement

### Étape 3 — Session secret check (C3)

```json
{
  "tool": "openclaw_session_config_check",
  "args": {
    "compose_file_path": "/path/to/docker-compose.yml",
    "env_file_path": "/path/to/.env"
  }
}
```
**Attendu :** `session_secret_found: true`
**Si HIGH :** appliquer `fix_docker` ou `fix_env` fourni

### Étape 4 — Rate limiting check (H8)

```json
{
  "tool": "openclaw_rate_limit_check",
  "args": {
    "gateway_config_path": "/path/to/.openclaw/config.yaml",
    "check_funnel": true
  }
}
```
**Attendu :** `rate_limiter_detected: true` OU `funnel_active: false`
**Si CRITICAL (funnel actif sans rate limiter) :** appliquer `fix_nginx` ou `fix_caddy` **immédiatement**

### Étape 5 — Alerte si CRITICAL (automatique)

Si un des audits retourne `severity: CRITICAL`, dispatcher automatiquement via :
```json
{
  "tool": "firm_export_slack_digest",
  "args": {
    "objective": "Security audit — CRITICAL finding",
    "content": "<résultats de l'audit>",
    "channel": "#security-alerts"
  }
}
```

## Checklist Matrix E2EE (M10)

Vérification documentaire manuelle (pas d'outil disponible — trop repo-spécifique) :
- [ ] Le `CONTRIBUTING.md` OpenClaw mentionne-t-il le statut E2EE Matrix ?
- [ ] Les utilisateurs Matrix privacy-sensitive sont-ils informés de l'absence d'E2EE ?
- [ ] Un ADR (`firm_adr_generate`) documente-t-il la décision E2EE Matrix ?

## Templates de remédiation rapide

### C2 — Sandbox fix (ajout dans config.yaml)

```yaml
agents:
  defaults:
    sandbox:
      mode: non-main   # ← activer isolation Docker pour sessions non-main
  sessions:
    main:
      sandbox:
        mode: off      # main conserve accès hôte (intentionnel)
```

### C3 — Session secret (docker-compose.yml)

```yaml
services:
  openclaw:
    environment:
      SESSION_SECRET: "${SESSION_SECRET:?SESSION_SECRET env var required}"
# Générer : openssl rand -base64 48 > /etc/openclaw/session.secret
```

### H8 — Rate limiting Nginx

```nginx
limit_req_zone $binary_remote_addr zone=openclaw:10m rate=30r/m;
server {
    location /ws {
        limit_req zone=openclaw burst=10 nodelay;
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Escalade

| Résultat | Action |
|----------|--------|
| Tout OK | Déploiement autorisé — log de l'audit dans `docs/security-audits/` |
| CRITICAL sandbox ou SQL | Bloquer le déploiement — fix obligatoire avant push |
| CRITICAL rate limit + funnel | Désactiver Funnel et appliquer Nginx/Caddy immédiatement |
| HIGH session secret | Appliquer fix + redémarrer le container avec le secret persistant |

## Intégration CI/CD

Ajouter dans le workflow GitHub Actions :

```yaml
- name: Security audit (firm-security-audit)
  run: |
    # Depuis le CTO ou Engineering agent avant chaque deploy
    openclaw skill run firm-security-audit \
      --config $OPENCLAW_CONFIG_PATH \
      --fail-on CRITICAL,HIGH
```

---
*OpenClaw gaps : C1 (#29951 SQL injection), C2 (sandbox off), C3 (#29955 session secret), H8 (no rate limit)*

---

## 💎 Support

Si ce skill vous est utile, vous pouvez soutenir le développement :

**Dogecoin** : `DQBggqFNWsRNTPb6kkiwppnMo1Hm8edfWq`
