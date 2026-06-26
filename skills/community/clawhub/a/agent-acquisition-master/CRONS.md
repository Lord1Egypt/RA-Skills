# Acquisition Crons — Agent

7 crons autonomes. Lun-Ven sauf mention contraire.
Agent configure ces crons lors du setup du skill.

---

## Format OpenClaw

```json
{
  "cron": {
    "enabled": true,
    "jobs": [

      {
        "name": "acquisition-daily-content",
        "cron": "0 8 * * 1-5",
        "message": "Exécute acquisition.content — publie le contenu du jour selon content_calendar.json. Twitter + LinkedIn. Adapte le sujet à l'actualité du moment si pertinent. Log engagement dans CONTENT_LEARNINGS.md immédiatement après chaque publication. Si un post génère un engagement notable, log dans HOOKS.md.",
        "model": "claude-sonnet-4-6",
        "session": "isolated"
      },

      {
        "name": "acquisition-daily-email",
        "cron": "0 9 * * 1-5",
        "message": "Exécute acquisition.email — envoie le batch cold email du jour (max 50). Lis leads_enriched.json, prends les prospects non encore contactés, utilise le meilleur template selon TEMPLATES_PERF.md. Log immédiatement dans AUDIT.md et sent_log.json après chaque envoi.",
        "model": "claude-sonnet-4-6",
        "session": "isolated"
      },

      {
        "name": "acquisition-qualify-inbox",
        "cron": "0 9,13,17 * * 1-5",
        "message": "Exécute acquisition.qualify — lit les nouvelles réponses Gmail depuis la dernière vérification. Classe chaque réponse : chaud / tiède / froid / désabonnement. Si lead chaud : notifie le principal sur Telegram immédiatement avec nom, message, et contexte. Log dans LESSONS.md si hook validé par une réponse positive. Log dans ERRORS.md si désabonnement ou réponse négative avec raison probable.",
        "model": "claude-haiku-4-5",
        "session": "isolated"
      },

      {
        "name": "acquisition-daily-linkedin",
        "cron": "0 10 * * 1-5",
        "message": "Exécute acquisition.linkedin — prospection LinkedIn du jour selon icp.json. View 20 profils ICP, like 5 posts récents, envoie max 10 messages post-connexion personnalisés. Respecte les limites : max 20 connexions/jour, espacer les actions. Log immédiatement dans AUDIT.md. Log dans LESSONS.md si réponse reçue.",
        "model": "claude-sonnet-4-6",
        "session": "isolated"
      },

      {
        "name": "acquisition-prospect",
        "cron": "0 11 * * 2",
        "message": "Exécute acquisition.prospect — enrichit la base de prospects chaque mardi. Scrape LinkedIn selon icp.json, identifie 50 nouveaux prospects qualifiés avec signaux d'achat détectés. Vérifie les emails via Hunter si HUNTER_API_KEY disponible. Déduplique avec leads.json existant. Log dans AUDIT.md.",
        "model": "claude-sonnet-4-6",
        "session": "isolated"
      },

      {
        "name": "acquisition-followup",
        "cron": "0 14 * * 1-5",
        "message": "Exécute acquisition.followup — envoie les relances du jour selon sent_log.json. Vérifie les prospects en J+3, J+7, J+12, J+18, J+25, J+35, J+50. Chaque relance apporte une nouvelle valeur — jamais 'just checking in'. Log immédiatement dans AUDIT.md et sent_log.json.",
        "model": "claude-sonnet-4-6",
        "session": "isolated"
      },

      {
        "name": "acquisition-weekly-report",
        "cron": "0 8 * * 1",
        "message": "Exécute acquisition.report — synthèse hebdomadaire chaque lundi matin AVANT le cron daily-content. Lis tous les logs de la semaine (AUDIT.md, sent_log.json, LESSONS.md, ERRORS.md). Calcule : emails envoyés, taux ouverture, taux réponse, leads chauds, conversions. Met à jour ICP_REFINEMENTS.md si patterns nouveaux détectés. Archive la synthèse dans /workspace/.learnings/LEARNINGS.md. Envoie au principal sur Telegram : rapport complet + 3 ajustements concrets proposés pour la semaine.",
        "model": "claude-sonnet-4-6",
        "session": "isolated"
      }

    ]
  }
}
```

---

## Ordre d'exécution chaque jour

```
08h00 → content        publie Twitter + LinkedIn
09h00 → email          envoie cold emails
09h00 → qualify        vérifie Gmail (1ère passe)
10h00 → linkedin       prospection LinkedIn
11h00 → prospect       [mardi seulement] enrichit la base
13h00 → qualify        vérifie Gmail (2ème passe)
14h00 → followup       envoie les relances
17h00 → qualify        vérifie Gmail (3ème passe)
```

---

## Notes importantes

```
acquisition-weekly-report tourne le lundi à 08h00
→ AVANT acquisition-daily-content (aussi 08h00)
→ OpenClaw exécute dans l'ordre de déclaration
→ Le rapport de synthèse est prêt avant que Agent publie

acquisition-qualify-inbox tourne 3x/jour
→ Pour respecter la règle Oussama : répondre en < 30 min
→ Haiku utilisé (pas Sonnet) — tâche de classification simple
→ Moins coûteux, suffisant pour lire et classer des emails

acquisition-prospect tourne seulement le mardi
→ Pas besoin de chercher des prospects tous les jours
→ 50 prospects/semaine = 200/mois = largement suffisant au démarrage
```
