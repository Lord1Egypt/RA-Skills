---
name: escalation
description: "Escalader un problème vers l'agent superviseur (David) via webhook gateway. Utiliser quand l'agent client est bloqué sur un problème qu'il ne peut pas résoudre seul après 2-3 tentatives."
---

# Escalation vers l'agent superviseur

## Quand escalader

- Blocage après 2-3 tentatives infructueuses
- Erreur technique hors du périmètre de l'agent (config, infra, API)
- Demande client qui dépasse les compétences de l'agent
- Situation ambiguë nécessitant une décision humaine ou superviseur

## Comment escalader

Exécuter le script `scripts/escalate.sh` via `exec` :

```bash
bash <SKILL_DIR>/scripts/escalate.sh "<description du problème>" "<ce qui a été tenté>" "<résultat obtenu>"
```

### Paramètres

1. **Problème** (obligatoire) — description concise du blocage
2. **Tentatives** (obligatoire) — ce qui a été essayé et pourquoi ça n'a pas marché
3. **Résultat** (optionnel) — dernier message d'erreur ou état actuel

### Exemple

```bash
bash <SKILL_DIR>/scripts/escalate.sh \
  "Impossible de lire les mails Google du client — token expiré" \
  "Tenté refresh via Nango, erreur 401 persistante. Vérifié scopes, OK." \
  "Error: invalid_grant - Token has been expired or revoked"
```

## Ce qui se passe

1. Le script appelle `POST /hooks/agent` sur le gateway local
2. Le superviseur (David) reçoit une session dédiée avec le contexte complet
3. David traite le problème ou escalade à Erwan si nécessaire
4. La réponse est délivrée sur Telegram à Erwan pour visibilité

## Règles

- **Ne pas escalader pour des questions simples** — chercher d'abord dans les skills, la doc, le web
- **Toujours inclure ce qui a été tenté** — le superviseur ne doit pas refaire le travail
- **Un seul escalade par problème** — ne pas spammer le webhook
- **Informer le client** qu'on a escaladé et qu'un retour arrive sous peu
