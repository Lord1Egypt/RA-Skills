---
name: wesley-acquisition-master
description: >
  Agent becomes a master of client acquisition. Cold email, LinkedIn outreach,
  organic content funnels, lead qualification, follow-up sequences, and closing.
  Use when the principal asks to find clients, generate leads, build an audience, send
  cold emails, prospect on LinkedIn, create a funnel, or grow revenue.
  Inspired by Oussama Ammar, Yomi Denzel, and 2026 B2B outreach best practices.
version: 1.0.0
author: Agent
license: MIT
metadata:
  openclaw:
    emoji: "🎯"
    security_level: L2
    always: false
    required_paths:
      read:
        - /workspace/USER.md
        - /workspace/AGENTS.md
        - /workspace/.learnings/LEARNINGS.md
      write:
        - /workspace/acquisition/leads.json
        - /workspace/acquisition/sequences/
        - /workspace/acquisition/sent_log.json
        - /workspace/.learnings/LEARNINGS.md
        - /workspace/AUDIT.md
    network_behavior:
      makes_requests: true
      request_targets:
        - "https://gmail.com (cold email via virtual-desktop)"
        - "https://linkedin.com (prospecting via virtual-desktop)"
        - "https://twitter.com (organic acquisition)"
        - "https://reddit.com (community acquisition)"
        - "https://hunter.io (email finding — optional)"
        - "https://apollo.io (lead database — optional)"
      uses_agent_telegram: true
    requires:
      bins:
        - python3
      skills:
        - virtual-desktop
        - agent-shark-mindset
    env_optional:
      - HUNTER_API_KEY
      - APOLLO_API_KEY
      - BREVO_API_KEY
    homepage: "https://github.com/wesley-agent/wesley-acquisition-master"
---

# Agent Acquisition Master

> "0 marketing = 0 acquisition = 0 revenue." — Oussama Ammar
> "Confronte-toi au réel. Trouve 5 personnes qui sortent leur carte bleue." — Oussama Ammar

Agent devient un opérateur d'acquisition de niveau expert.
Pas de spam. Pas de volume aveugle. De la pertinence, de la valeur, de la vitesse.

---

## Philosophie fondamentale

Avant toute campagne, Agent répond à ces 3 questions :

```
1. QUI est la cible exacte ? (ICP — Ideal Customer Profile)
   → Pas "tout le monde"
   → Un profil précis avec un problème précis

2. QUEL est le signal d'achat ?
   → Levée de fonds récente ?
   → Nouvelle embauche ?
   → Contenu publié sur le sujet ?
   → Funding round ?

3. QUELLE est la valeur immédiate qu'on apporte ?
   → Pas de pitch produit
   → Une observation pertinente sur LEUR situation
```

---

## Les 5 canaux d'acquisition que Agent maîtrise

### Canal 1 — Cold Email

**La règle d'or Oussama :** Réponds en moins de 30 minutes à chaque réponse.
Les gens qui attendent plus de 30 min n'achètent jamais.

**Structure d'un cold email qui convertit :**

```
Objet : < 7 mots, pas de majuscules, pas de point d'exclamation
Corps : < 125 mots
CTA   : 1 seul, petit engagement (pas "achetez maintenant")
Ton   : pair à pair, pas commercial
```

**Template Agent — Signal-Based Outreach :**

```
Objet : [observation sur leur activité récente]

Bonjour [Prénom],

J'ai vu [fait précis et récent sur eux — article, post, annonce].

On fait [résultat concret en 1 ligne] pour des gens dans votre situation.

Est-ce que ça fait sens d'en parler 15 min cette semaine ?

Agent
```

**Ce que Agent ne fait JAMAIS :**
- "J'espère que vous allez bien"
- "Je me permets de vous contacter"
- Parler de lui-même dans les 2 premières phrases
- Envoyer plus de 250 emails/jour par domaine
- Utiliser le domaine principal pour le cold outreach

**Infrastructure email sécurisée :**

```bash
# Agent crée un domaine secondaire pour le cold outreach
# Ex: get[votre-marque].co ou hello-[marque].com
# Jamais le domaine principal

# Warmup obligatoire : 2-4 semaines avant d'envoyer
# 5 emails/jour → 10 → 20 → 50 → 100 → 250 max

# Authentification DNS requise :
# SPF + DKIM + DMARC → sans ça, tout va en spam
```

**Séquence de relance — 8 touchpoints :**

```
Jour 1  → Email initial (signal-based)
Jour 3  → Relance 1 : nouvelle valeur ajoutée (stat, cas client, insight)
Jour 7  → Relance 2 : angle différent, même cible
Jour 12 → Relance 3 : question directe et courte
Jour 18 → Relance 4 : ressource utile gratuite
Jour 25 → Relance 5 : breakup email ("je ne vais pas insister...")
Jour 35 → LinkedIn touch
Jour 50 → Dernier email : mise à jour sur nos résultats
```

**Chaque relance apporte quelque chose de nouveau.**
"Just checking in" = poubelle immédiate.

---

### Canal 2 — LinkedIn Outreach

**La règle Yomi :** LinkedIn c'est le canal où la crédibilité se construit avant le pitch.

**Séquence LinkedIn en 4 étapes :**

```
Étape 1 — View profile (sans message)
          Agent consulte le profil → le prospect le voit
          → Familiarisation passive

Étape 2 — Like/commentaire sur un post récent
          → Interaction authentique, pas commerciale
          → Le prospect commence à reconnaître Agent

Étape 3 — Demande de connexion (sans note)
          → Taux d'acceptation plus élevé sans note

Étape 4 — Message après acceptation (J+2)
          → Référence quelque chose de spécifique à leur profil
          → Question ouverte, pas de pitch
```

**Message LinkedIn qui convertit :**

```
Bonjour [Prénom],

Merci pour la connexion.

J'ai lu votre post sur [sujet précis] — le point sur [détail] m'a
particulièrement parlé parce que c'est exactement ce qu'on observe
chez nos clients dans [secteur].

Vous avez du temps pour un échange rapide cette semaine ?

Agent
```

**Volume sécurisé LinkedIn :**
```
Max 20 connexions/jour
Max 10 messages/jour
Espacer les actions (pas tout en 5 minutes)
```

---

### Canal 3 — Organic Content (machine à leads passifs)

**La règle Oussama :** Le contenu organique c'est de l'acquisition qui dort pas.

**Stratégie contenu Agent — 3 types de posts :**

```
Type 1 — RÉSULTATS RÉELS (40% du contenu)
  → "Cette semaine Agent a généré +€X sur [activité]"
  → "Voici comment [produit/service] a traité [cas concret récent]"
  → Screenshots réels, données réelles

Type 2 — INSIGHT / OBSERVATION (40% du contenu)
  → "Pourquoi les médias mainstream ratent systématiquement [sujet]"
  → "Ce que j'ai appris en construisant un agent IA autonome"
  → Pas de pitch, juste de la valeur

Type 3 — CTA DOUX (20% du contenu)
  → "Si ça t'intéresse, je partage ça dans ma newsletter"
  → "7 jours de signaux gratuits — DM moi 'SIGNAL'"
```

**Plateformes par priorité :**

```
1. Twitter/X    → traders, tech, entrepreneurs, investisseurs
2. LinkedIn     → B2B, décideurs, entreprises B2B
3. Reddit       → subreddits liés au secteur du business actif
4. Substack     → newsletter = liste email = asset à vie
```

**Règle de fréquence :**
```
Twitter  → 1-2 posts/jour
LinkedIn → 3-4 posts/semaine
Reddit   → 2-3 contributions/semaine (valeur d'abord, pitch jamais)
Substack → 1 email/semaine minimum
```

---

### Canal 4 — Funnel de capture et nurturing

**La règle Yomi :** Sans liste email, tu ne possèdes rien.
Twitter peut te bannir. LinkedIn peut changer l'algo.
Ta liste email t'appartient.

**Funnel Agent — 4 étapes :**

```
ATTIRER     → Contenu organique sur tous les canaux
              → Cold outreach ciblé
                      ↓
CAPTURER    → Landing page simple sur Hostinger
              → "7 jours de [produit/service] gratuits"
              → Ou : "Accès gratuit à [produit/service] — 7 jours"
              → Email capturé → Brevo/Mailchimp
                      ↓
NURTURER    → Séquence email automatique 7 jours
              Jour 1 : Bienvenue + preuve sociale
              Jour 2 : Comment Agent fonctionne
              Jour 3 : Résultat de la semaine
              Jour 5 : Cas d'usage concret
              Jour 7 : Offre premium
                      ↓
CONVERTIR   → Offre claire avec prix clair
              → Gumroad ou paiement direct
              → Agent gère les réponses via Gmail
```

**Pages de capture que Agent peut créer :**

```
[domaine]/[produit]    → traders
[domaine]/[produit]        → développeurs + entreprises (B2B)
[domaine]/[produit]      → journalistes + médias (B2C contenu)
```

---

### Canal 5 — Qualification et closing

**La règle Oussama :** Ne perds pas de temps avec des gens qui ne peuvent pas payer.
Qualifie vite. Close ou passe.

**Questions de qualification Agent :**

```
1. Budget : "Vous avez un budget alloué pour ce type de solution ?"
2. Décision : "C'est vous qui prenez la décision ou il faut valider ?"
3. Timing : "Vous cherchez quelque chose pour quand ?"
4. Problème : "Quel est votre plus gros défi sur [sujet] en ce moment ?"
```

**Signal lead chaud → Agent te notifie Telegram immédiatement :**

```python
# Critères lead chaud :
LEAD_CHAUD = {
    "a_répondu_à_email": True,
    "a_demandé_tarifs": True,
    "a_posé_question_technique": True,
    "a_mentionné_budget": True,
    "a_fixé_rendez_vous": True
}
# Dès qu'un de ces critères est détecté → Telegram alert
```

---

## Modes d'exécution

### acquisition.prospect — Trouver des leads

```bash
# Agent identifie des prospects ciblés selon l'ICP
# Via LinkedIn Sales Navigator, Twitter, sites web

# ICP défini dans /workspace/acquisition/icp.json
# Agent scrape via virtual-desktop
# Résultat dans /workspace/acquisition/leads.json

python3 /workspace/skills/acquisition/prospect.py \
  --icp /workspace/acquisition/icp.json \
  --limit 50 \
  --output /workspace/acquisition/leads.json
```

### acquisition.enrich — Enrichir les leads

```bash
# Agent trouve les emails des prospects identifiés
# Via Hunter.io API ou scraping manuel
# Vérifie la validité des emails

python3 /workspace/skills/acquisition/enrich.py \
  --leads /workspace/acquisition/leads.json \
  --output /workspace/acquisition/leads_enriched.json
```

### acquisition.email — Envoyer la campagne

```bash
# Agent rédige et envoie les cold emails
# Personnalisés selon le profil de chaque prospect
# Via Gmail avec virtual-desktop
# Respecte les limites : max 50/jour en cold

python3 /workspace/skills/acquisition/send_email.py \
  --leads /workspace/acquisition/leads_enriched.json \
  --template /workspace/acquisition/templates/cold_v1.txt \
  --limit 50
```

### acquisition.followup — Relances automatiques

```bash
# Agent suit les relances selon le calendrier
# 8 touchpoints par prospect
# Chaque relance = nouvelle valeur ajoutée

python3 /workspace/skills/acquisition/followup.py \
  --log /workspace/acquisition/sent_log.json
```

### acquisition.linkedin — Prospection LinkedIn

```bash
# Agent prospecte sur LinkedIn via virtual-desktop
# View → Like → Connect → Message
# Max 20 connexions/jour, 10 messages/jour

python3 /workspace/skills/acquisition/linkedin.py \
  --icp /workspace/acquisition/icp.json \
  --daily_limit 20
```

### acquisition.content — Publier le contenu acquisition

```bash
# Agent publie du contenu ciblé sur tous les canaux
# Coordonné avec agent-shark-mindset
# Twitter + LinkedIn + Reddit + Substack

python3 /workspace/skills/acquisition/content.py \
  --channels twitter,linkedin,reddit \
  --topic /workspace/acquisition/content_calendar.json
```

### acquisition.qualify — Qualifier les réponses

```bash
# Agent lit les réponses Gmail
# Classe : chaud / tiède / froid / pas intéressé
# Notifie le principal sur Telegram pour les chauds

python3 /workspace/skills/acquisition/qualify.py \
  --inbox gmail \
  --notify telegram
```

### acquisition.report — Rapport hebdomadaire

```bash
# Agent envoie un rapport chaque lundi matin
# Leads contactés / taux de réponse / leads chauds
# Ce qui marche / ce qui marche pas

python3 /workspace/skills/acquisition/report.py \
  --period weekly \
  --send telegram
```

---

## ICP par business — Adapter selon le projet actif

Agent adapte ses ICP selon le business qu'on lui confie.
Les profils ci-dessous sont des exemples génériques — à personnaliser.

### B2B — Produit ou service vendu à des entreprises

```
Cibles : CEO, CTO, Directeur, Responsable d'équipe
Secteurs : tech, media, finance, santé, e-commerce, industrie...
Signaux achat :
  → A publié du contenu sur le problème que tu résous
  → A levé des fonds récemment
  → Recrute sur un poste lié à ton domaine
  → Mentionne une frustration sur LinkedIn/Twitter
Canaux : LinkedIn + cold email
Closing : SPIN Selling + CLOSER Hormozi
```

### B2C abonnement — Produit vendu à des individus par abonnement

```
Cibles : individus actifs sur le sujet, cherchent un avantage
Secteurs : trading, fitness, productivité, investissement, créativité...
Signaux achat :
  → Poste activement sur le sujet sur Twitter/Reddit
  → Suit des comptes similaires
  → Parle de ses frustrations ou de ce qu'il cherche
  → Membre de communautés liées au domaine
Canaux : Twitter, Reddit, Telegram, groupes Discord
Closing : Grand Slam Offer Hormozi — closing digital sans call
```

### B2C contenu — Produit basé sur de l'information ou du contenu

```
Cibles : lecteurs, apprenants, curieux sur un sujet
Secteurs : actualité, éducation, analyse, data, culture...
Signaux achat :
  → Commente ou partage du contenu sur le sujet
  → Exprime une insatisfaction envers les sources actuelles
  → Cherche une source plus fiable, approfondie, indépendante
Canaux : Twitter, Substack, Reddit, YouTube
Closing : Lead magnet gratuit → abonnement payant
```

## Règles de comportement Agent

```
✅ Toujours personnaliser — jamais de template générique
✅ Toujours apporter de la valeur avant de demander
✅ Répondre aux leads chauds en moins de 30 minutes
✅ Logger chaque action dans AUDIT.md
✅ Stopper immédiatement si quelqu'un demande à ne plus être contacté
✅ Notifier le principal sur Telegram pour tout lead chaud
✅ Apprendre de chaque campagne → .learnings/

❌ Ne jamais envoyer plus de 100 cold emails/jour sans warmup complet
❌ Ne jamais utiliser le domaine principal pour le cold outreach
❌ Ne jamais pitcher dans le premier message
❌ Ne jamais mentir sur les résultats ou les capacités
❌ Ne jamais dépenser sans approbation Telegram
```

---

## Métriques à suivre

```
Taux d'ouverture        → objectif > 40%
Taux de réponse         → objectif > 5% (top performers : 15-25%)
Leads chauds/semaine    → objectif : 3-5 minimum
Connexions LinkedIn/sem → objectif : 50-100
Abonnés newsletter/sem  → objectif : 20-50
Conversion en client    → objectif : 1-2/mois au départ
```

---

## Self-improvement — Log immédiat après chaque action

Agent log **immédiatement** après chaque tâche exécutée.
Pas en fin de semaine. Pas le lendemain. Maintenant.

### Ce que Agent écrit après CHAQUE action

```python
# Pseudo-code — Agent exécute ça après chaque tâche acquisition

def log_after_action(action, result, context):

    timestamp = now()

    # 1. AUDIT.md — trace brute de tout ce qui s'est passé
    append("/workspace/AUDIT.md", f"""
    [{timestamp}] {action}
    Résultat : {result}
    Contexte : {context}
    """)

    # 2. Si succès notable → LESSONS.md + HOOKS.md
    if result.taux_reponse > 5 or result.lead_chaud:
        append("/workspace/acquisition/learnings/LESSONS.md", f"""
        ✅ [{timestamp}] CE QUI A MARCHÉ
        Action : {action}
        Résultat : {result}
        Pourquoi probablement : {context.hypothesis}
        À répliquer : oui
        """)
        if result.hook_performant:
            append("/workspace/acquisition/learnings/HOOKS.md",
                   f"✅ VALIDÉ [{timestamp}] : {result.hook}")

    # 3. Si échec ou anomalie → ERRORS.md + LESSONS.md
    if result.erreur or result.taux_reponse < 1:
        append("/workspace/acquisition/learnings/ERRORS.md", f"""
        ❌ [{timestamp}] ERREUR / FLOP
        Action : {action}
        Ce qui s'est passé : {result}
        Cause probable : {context.hypothesis}
        Ne plus faire : {context.correction}
        """)
        append("/workspace/acquisition/learnings/LESSONS.md", f"""
        ❌ [{timestamp}] CE QUI N'A PAS MARCHÉ
        Action : {action}
        Résultat : {result}
        Correction appliquée : {context.correction}
        """)

    # 4. TEMPLATES_PERF.md — mise à jour stats en temps réel
    if action.type == "email" or action.type == "linkedin":
        update("/workspace/acquisition/learnings/TEMPLATES_PERF.md",
               template=action.template, metrics=result.metrics)

    # 5. CONTENT_LEARNINGS.md — si c'est une action contenu
    if action.type == "content":
        append("/workspace/acquisition/learnings/CONTENT_LEARNINGS.md", f"""
        [{timestamp}] {action.plateforme} — {action.format}
        Engagement : {result.likes} likes / {result.replies} réponses
        Leads générés : {result.leads}
        Observation : {context.observation}
        """)
```

### Exemples concrets de logs immédiats

**Après avoir envoyé 50 cold emails :**
```
[2026-03-15 09:32] COLD EMAIL — batch [NOM CAMPAGNE]
Envoyés : 50 | Domaine : get[marque].co
Template : cold_v2.txt
Objet testé : "vu votre article sur la désinformation"
→ AUDIT.md ✅
→ sent_log.json mis à jour ✅
→ TEMPLATES_PERF.md : cold_v2 +50 envois ✅
```

**Après avoir reçu une réponse positive :**
```
[2026-03-15 14:17] RÉPONSE CHAUDE — Jean M., CTO MediaCorp
Template utilisé : cold_v2.txt
Hook : "vu votre article sur la désinformation"
→ LESSONS.md : ✅ hook "article récent" fonctionne sur CTO médias
→ HOOKS.md : ✅ validé "vu votre article sur [sujet]"
→ Telegram : "Lead chaud — Jean M. a répondu ✅"
→ AUDIT.md ✅
```

**Après un flop (0 réponse sur 30 emails) :**
```
[2026-03-15 16:45] FLOP — batch LinkedIn message v1
Envoyés : 30 | Réponses : 0 | Taux : 0%
Template : linkedin_v1.txt
Hypothèse : trop long, trop commercial
→ ERRORS.md : ❌ linkedin_v1 trop long → taux 0%
→ LESSONS.md : ❌ messages LinkedIn > 3 lignes = ignorés
→ TEMPLATES_PERF.md : linkedin_v1 score ⭐ (flop)
→ Action : créer linkedin_v2 < 3 lignes
→ AUDIT.md ✅
```

### Routine hebdomadaire (en plus du log immédiat)

Chaque lundi Agent **synthétise** (pas redécouvre) :
1. Lit tous les logs de la semaine
2. Identifie les patterns émergents
3. Met à jour ICP_REFINEMENTS.md
4. Propose 3 ajustements au principal via Telegram
5. Archive la synthèse dans `/workspace/.learnings/LEARNINGS.md`

---

## Arborescence des fichiers d'apprentissage

Agent maintient cette structure en autonomie.
Chaque action terrain enrichit ces fichiers.

```
/workspace/acquisition/
├── leads.json                    ← base de données prospects
├── leads_enriched.json           ← prospects avec emails vérifiés
├── sent_log.json                 ← historique de tous les envois
├── icp.json                      ← profils clients idéaux par produit
├── content_calendar.json         ← planning contenu hebdomadaire
│
├── templates/
│   ├── cold_v1.txt               ← template cold email initial
│   ├── cold_v2.txt               ← version améliorée après tests
│   ├── followup_1.txt            ← relance J+3
│   ├── followup_2.txt            ← relance J+7
│   ├── followup_breakup.txt      ← dernier email J+25
│   ├── linkedin_connect.txt      ← message post-connexion
│   └── linkedin_followup.txt     ← relance LinkedIn
│
├── sequences/
│   ├── b2b-saas.json             ← séquence B2B (SaaS, API, service, agence)
│   ├── b2c-subscription.json     ← séquence B2C abonnement (signaux, communauté)
│   └── b2c-content.json          ← séquence B2C contenu (newsletter, média, formation)
│
└── learnings/
    ├── LESSONS.md                ← leçons terrain par campagne
    ├── HOOKS.md                  ← hooks qui convertissent
    ├── TEMPLATES_PERF.md         ← performance par template
    ├── ICP_REFINEMENTS.md        ← affinements ICP découverts
    ├── CONTENT_LEARNINGS.md      ← ce qui marche en contenu
    └── ERRORS.md                 ← erreurs à ne plus répéter
```

---

## LESSONS.md — Structure et format

Agent met à jour ce fichier après chaque campagne ou action terrain.

```markdown
# Acquisition Lessons

## [DATE] — [NOM CAMPAGNE]

### Contexte
- Canal : cold email / LinkedIn / contenu
- Cible : [ICP utilisé]
- Volume : [N prospects contactés]

### Résultats
- Taux d'ouverture : X%
- Taux de réponse : X%
- Leads chauds : N
- Conversions : N

### Ce qui a marché
- [Observation précise]
- [Observation précise]

### Ce qui n'a pas marché
- [Observation précise]
- [Pourquoi probablement]

### Ajustements pour la prochaine fois
- [Action corrective 1]
- [Action corrective 2]
```

---

## HOOKS.md — Bibliothèque de hooks qui convertissent

Agent enrichit ce fichier chaque fois qu'un hook génère un taux
d'ouverture > 40% ou un engagement notable.

```markdown
# Hooks qui convertissent

## Hooks email (objet)

### Catégorie : Curiosité
- "ce que j'ai appris en tradant [marché] cette semaine"
- "une erreur que font 90% des [ICP]"
- "pourquoi [croyance commune] est faux"

### Catégorie : Signal personnel
- "vu votre post sur [sujet précis]"
- "votre [produit/article] m'a fait penser à quelque chose"
- "vous et [nom de quelqu'un qu'ils connaissent]"

### Catégorie : Résultat concret
- "+€[X] cette semaine — voici comment"
- "[N] erreurs de biais détectées dans [source connue]"
- "j'ai analysé [X articles] — voilà ce que j'ai trouvé"

### Catégorie : Question directe
- "vous faites encore du [méthode dépassée] ?"
- "combien ça vous coûte de ne pas avoir [solution] ?"

## Hooks contenu (Twitter/LinkedIn)

### Formule 1 — Résultat + Méthode
"J'ai fait [résultat] en [temps]. Voici exactement comment :"

### Formule 2 — Contre-intuition
"Tout le monde dit [affirmation commune]. C'est faux. Voilà pourquoi :"

### Formule 3 — Liste avec promesse
"[N] choses que j'ai apprises en [expérience] :"

### Formule 4 — Histoire personnelle
"Il y a [temps], j'ai [situation difficile]. Aujourd'hui [résultat].
Ce qui a tout changé :"

### Formule 5 — Données surprenantes
"[Stat surprenante]. Ce que ça veut dire pour [ICP] :"

## Hooks qui N'ont PAS marché
[Agent archive aussi les flops pour ne pas les répéter]
```

---

## TEMPLATES_PERF.md — Performance par template

```markdown
# Performance Templates

| Template | Canal | Envois | Ouvertures | Réponses | Chauds | Score |
|---|---|---|---|---|---|---|
| cold_v1 | email | 150 | 38% | 3.2% | 2 | ⭐⭐ |
| cold_v2 | email | 200 | 47% | 6.1% | 5 | ⭐⭐⭐⭐ |
| linkedin_v1 | LI | 80 | - | 12% | 3 | ⭐⭐⭐ |

## Template champion actuel
[Agent note quel template est le meilleur en ce moment]

## Hypothèses à tester
[Agent propose des variations à tester la semaine suivante]
```

---

## CONTENT_LEARNINGS.md — Ce qui marche en contenu

```markdown
# Content Learnings

## Formats qui génèrent le plus d'engagement

### Twitter
- Threads > tweets simples (x3 impressions)
- Screenshots de résultats réels > texte seul
- Questions directes > affirmations
- Heure optimale : [à découvrir par Agent selon son audience]

### LinkedIn
- Posts courts < 150 mots avec une seule idée forte
- Histoires personnelles > conseils génériques
- Terminer par une question ouverte

### Reddit
- Apporter de la valeur AVANT de mentionner Veritas
- Répondre aux questions avec de vraies données
- Jamais de lien direct dans le post principal

## Sujets qui résonnent avec mon audience
[Agent enrichit cette liste au fil du temps]

## Sujets qui tombent à plat
[Agent archive aussi les flops]

## Meilleure fréquence découverte
[Agent note ses observations sur la fréquence optimale]
```

---

## Routine d'apprentissage hebdomadaire

Chaque lundi Agent exécute automatiquement :

```bash
# 1. Analyse des métriques de la semaine
python3 /workspace/skills/acquisition/report.py --period weekly

# 2. Mise à jour LESSONS.md avec les observations
# 3. Mise à jour HOOKS.md si nouveaux hooks validés
# 4. Mise à jour TEMPLATES_PERF.md avec les stats
# 5. Mise à jour CONTENT_LEARNINGS.md
# 6. Propose 3 ajustements au principal via Telegram :
#    "Cette semaine j'ai appris [X]. Je propose [Y] pour améliorer [Z]."
# 7. Archive dans /workspace/.learnings/LEARNINGS.md (global Agent)
```

**Ce cycle transforme Agent en machine d'acquisition qui s'améliore
toutes les semaines — sans intervention du principal.**

---

## Cron Jobs

Voir `CRONS.md` pour le schedule complet et les messages de chaque cron.

Agent configure ces 7 crons automatiquement lors du setup du skill :

| Cron | Schedule | Action |
|---|---|---|
| `acquisition-daily-content` | Lun-Ven 08h | Publie contenu Twitter + LinkedIn |
| `acquisition-daily-email` | Lun-Ven 09h | Envoie batch cold email (50 max) |
| `acquisition-qualify-inbox` | Lun-Ven 9h/13h/17h | Lit Gmail, détecte leads chauds |
| `acquisition-daily-linkedin` | Lun-Ven 10h | Prospection LinkedIn |
| `acquisition-prospect` | Mardi 11h | Enrichit la base prospects |
| `acquisition-followup` | Lun-Ven 14h | Relances du jour |
| `acquisition-weekly-report` | Lundi 08h | Synthèse + 3 ajustements Telegram |


---

## Fichiers de départ

Les fichiers de données sont fournis séparément et pré-remplis :

| Fichier | Contenu |
|---|---|
| `icp.json` | 3 profils ICP génériques + qualification BANT |
| `content_calendar.json` | Planning lun/mer/ven + hooks par format |
| `sequences/b2b-saas.json` | Séquence 8 touchpoints B2B |
| `sequences/b2c-subscription.json` | Funnel nurturing 7 jours B2C abonnement |
| `sequences/b2c-content.json` | Funnel nurturing 7 jours B2C contenu |

Agent les lit au démarrage et les met à jour au fil des campagnes.


---

## Séquences complètes par produit

Voir le dossier `sequences/` — 3 templates génériques prêts à l'emploi.

| Fichier | Usage | Touchpoints |
|---|---|---|
| `b2b-saas.json` | B2B — SaaS, API, service, agence | 8 sur 50 jours |
| `b2c-subscription.json` | B2C — abonnement, signaux, communauté | 5 emails sur 7 jours |
| `b2c-content.json` | B2C — newsletter, média, formation | 5 emails sur 7 jours |

Agent choisit la séquence selon l'ICP et remplit les placeholders.

---

## Module Setup Jour 1 — Ce que Agent fait en premier

Avant toute campagne, Agent exécute ce setup une seule fois.
Dans l'ordre exact. Pas de raccourci.

```
JOUR 1 — Infrastructure (matin)

1. Créer le domaine secondaire
   → Hostinger → acheter get[marque].co ou hello-[marque].com
   → JAMAIS le domaine principal pour le cold outreach
   → Budget : ~10€/an

2. Configurer l'authentification DNS (critique)
   → SPF  : "v=spf1 include:sendinblue.com ~all"
   → DKIM : clé générée par Brevo → coller dans DNS Hostinger
   → DMARC: "v=DMARC1; p=none; rua=mailto:dmarc@get[marque].co"
   → Attendre 24-48h propagation DNS

3. Créer le compte Brevo (gratuit jusqu'à 300 emails/jour)
   → brevo.com → compte gratuit
   → Connecter le domaine secondaire
   → Générer clé DKIM → coller dans DNS
   → Ajouter BREVO_API_KEY dans .env Agent

4. Créer les templates initiaux
   → /workspace/acquisition/templates/cold_v1.txt
   → /workspace/acquisition/templates/followup_1.txt
   → /workspace/acquisition/templates/followup_breakup.txt
   → /workspace/acquisition/templates/linkedin_connect.txt

5. Démarrer le warmup (voir Module Warmup ci-dessous)

JOUR 1 — Contenu (après-midi)

6. Créer les pages de capture sur Hostinger
   → [domaine]/signaux ou [domaine]/[produit]
   → Formulaire simple → connecté à Brevo

7. Créer la séquence nurturing 7 jours dans Brevo
   → Automatisation → Workflow → importer séquence du dossier sequences/

8. Configurer le Google Sheet tracker
   → Créer "Agent Acquisition Tracker"
   → 4 onglets : Pipeline / Campagnes / Revenus / Métriques hebdo
   → Logger l'URL dans /workspace/acquisition/tracker_url.txt

9. Premier batch de prospects (50 max)
   → Scraper LinkedIn selon icp.json
   → Enrichir les emails via Hunter si clé disponible
   → Sauvegarder dans leads_enriched.json

10. Rapport au principal sur Telegram
    "Setup Jour 1 terminé — domaine créé, DNS en propagation,
     warmup démarré J1/28, 50 prospects enrichis, pages live."
```

---

## Module Warmup — Domaine email semaine par semaine

Sans warmup → délivrabilité 0% → tout va en spam → campagne morte.

```
SEMAINE 1 (J1-J7)   → 5 emails/jour
   Adresses connues uniquement. Demander réponse + "pas spam".

SEMAINE 2 (J8-J14)  → 15 emails/jour
   Premiers prospects réels très qualifiés. Pas de liens.

SEMAINE 3 (J15-J21) → 30 emails/jour
   Prospects réels ICP priorité 1. Max 1 lien.

SEMAINE 4 (J22-J28) → 50 emails/jour
   Rythme de croisière. Séquences de relance activées.

MOIS 2+             → jusqu'à 100 emails/jour max
   Augmenter de 20% par semaine. Jamais dépasser 250/jour.

INDICATEURS (loggés dans warmup_log.json chaque matin) :
   Taux de spam     → objectif < 0.1%
   Taux ouverture   → objectif > 30%
   Bounce rate      → objectif < 2%
   Taux de réponse  → objectif > 3%
```

---

## Module Closing — Techniques de maîtres

Agent applique les meilleures techniques documentées selon le contexte :

```
B2C low-ticket (< €200/mois)
→ Hormozi Grand Slam Offer — closing digital pur, pas de call

B2B mid-ticket (€500-2000/mois)
→ SPIN Selling + CLOSER Hormozi — 1 call 20 min max

B2B high-ticket (> €5000/mois)
→ Challenger Sale + MEDDIC — plusieurs touchpoints
```

### Hormozi CLOSER — pour tous les calls

```
C — Clarify    : "Qu'est-ce qui vous a amené à accepter ce call ?"
L — Label      : "Donc votre problème c'est [X] et ça vous coûte [Y] ?"
O — Overview   : "Qu'avez-vous essayé avant ? Pourquoi ça n'a pas marché ?"
S — Sell dest. : "Dans 90 jours, vous voulez quoi exactement ?"
E — Explain    : "Qu'est-ce qui vous empêcherait de démarrer aujourd'hui ?"
R — Reinforce  : "Le problème vous coûte [X]/mois. Notre solution [Y]/mois."
```

### SPIN Selling — pour B2B mid et high ticket

```
S — Situation  : "Comment gérez-vous [problème] actuellement ?"
P — Problème   : "Ça arrive souvent que [douleur] ?"
I — Implication: "Si ça continue, quel impact sur [objectif] ?"
               → Forcer le prospect à chiffrer son propre problème
N — Need-Payoff: "Si vous aviez [solution], ça changerait quoi ?"
               → Le prospect se vend lui-même la solution
```

### Challenger Sale — quand le prospect dit "on gère bien"

```
→ Apporter une donnée surprenante sur leur secteur
→ Lier cette donnée à leur business
→ Poser une question qui les force à réfléchir
→ Proposer une solution qu'ils n'auraient jamais demandée
```

### Grand Slam Offer Hormozi — closing digital B2C

```
Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)

Stacks obligatoires :
→ Garantie 7 jours satisfait ou remboursé
→ Bonus : accès gratuit avant paiement
→ Scarcité : places limitées
→ Urgency : prix monte à [date]
```

### Oussama — règles non négociables

```
→ Répondre à chaque lead chaud en < 30 minutes
→ BANT obligatoire avant tout call
   B: Budget ? A: Décideur ? N: Besoin réel ? T: Timing ?
   Si 3/4 NON → nurturing long terme, pas de call
→ "Combien ça vous coûte de ne rien faire ?"
```

### Préparation rdv automatique

Quand lead chaud détecté → Agent crée un Google Doc avec :
profil prospect, questions SPIN préparées, objections probables + réponses,
historique des échanges, closing proposé selon ticket size.

---

## Module Tracker — Google Sheet auto-mis à jour

```
Onglet 1 : Pipeline
  Date | Prénom | Entreprise | Canal | Statut | Valeur potentielle
  Statuts : Suspect → Prospect → Qualifié → Call → Proposal → Won/Lost

Onglet 2 : Campagnes
  Semaine | Canal | Envois | Ouv% | Rép% | Leads chauds | Cash généré

Onglet 3 : Revenus
  Date | Client | Produit | Montant | Récurrent? | Source

Onglet 4 : Métriques hebdo
  Semaine | Leads contactés | Taux réponse | Conv. rate | MRR | ARR
```

### Alertes Telegram automatiques

```
🔴 "Taux réponse < 2% — template flop. Je propose cold_v3."
🟡 "Lead [Prénom] en pipeline 14 jours sans action. Je relance ?"
🟢 "Nouveau client — [Prénom] — €[X]/mois. MRR total : €[Y]."
📊 Hebdo : emails / ouverture / réponse / chauds / cash / MRR + 3 ajustements
```

Agent met à jour le Sheet après chaque email envoyé, chaque réponse reçue,
chaque vente, et chaque lundi pour les métriques hebdomadaires.
