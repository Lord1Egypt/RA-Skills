# PIPELINE.md — Méthode Herbert × Jury

*Méthode générique — applicable à tout projet de rédaction.*
*À relire au démarrage de chaque session.*
*Mis à jour le 13 avril 2026 d'après le schéma complet.*

---

## Vue d'ensemble

```
INPUT UTILISATEUR
    ↓
ORCHESTRATEUR — Structuration narrative
    ↓
[ENRICHISSEMENT SEEDS — optionnel]
    ↓
┌── BOUCLE × 40-50 seeds ──────────────────────────────┐
│                                                        │
│   HERBERT — Rédaction (iter 1)                        │
│       ↓                                               │
│   JURY — Évaluation (3 itérations fixes)              │
│       ↓                                               │
│   [CONTRÔLE DE COHÉRENCE — tous les 5 seeds]         │
│       ↓ (si incohérence : 4e itération corrective)   │
│                                                        │
└────────────────────────────────────────────────────────┘
    ↓
AGENT PUBLICATION — Export DOCX (local)
```

---

## Règle 0 — Session fraîche par projet (OBLIGATOIRE)

**Herbert doit être spawné dans une nouvelle session à chaque nouveau projet.**

Raison : une session longue accumule le contexte de tous les projets précédents. Après 3-4 projets, le contexte dépasse 400k tokens et est rechargé intégralement à chaque tour — coût ×10 inutile.

**Règle :**
- Chaque projet → nouvelle instance Herbert (sessions_spawn)
- Ne jamais réutiliser une session Herbert existante pour un nouveau projet
- La session Herbert peut survivre pendant toute la durée d'un projet (bibles → seeds → corrections → export)
- Dès qu'un nouveau projet démarre : nouvelle session

L'orchestrateur (Boto) est responsable de cette règle.

---

## Étape 1 — Input utilisateur

L'auteur soumet le point de départ de l'œuvre.

**Format attendu :** Thème + Pitch (quelques lignes d'intention)

---

## Étape 2 — Orchestrateur : Structuration narrative

L'agent central prépare l'architecture complète de l'œuvre **avant toute rédaction**.

**Livrables :**
- Arcs narratifs (tension centrale, structure globale)
- Bibles personnages / univers
- Sommaire des 40–50 seeds (toutes les unités numérotées et titrées)

---

## Étape 3 — Enrichissement des seeds (optionnel / facultatif)

L'orchestrateur peut interroger l'auteur pour préciser chaque seed avant d'écrire.

**Format :** Questions contextuelles par seed (intention, détail imposé, contrainte de style)

> Cette étape est facultative. Si les seeds sont suffisamment précises, on passe directement à l'étape 4.

---

## Étape 4 — Herbert : Rédaction de la seed

Herbert rédige l'unité courante en **itération 1**, avec le contexte narratif injecté.

**Contexte injecté automatiquement :**
- La seed de l'auteur
- Les arcs narratifs du personnage concerné
- Les bibles pertinentes (personnage, univers, époque)

**Règle :** Herbert ne rédige qu'**une seed à la fois**. Il ne passe pas à la suivante avant validation du Jury.

---

## Étape 5 — Agent Jury : Évaluation multi-critiques

Le Jury orchestre **10 critiques spécialisés**, **3 évaluateurs-lecteurs**, et un **scoring non-linéaire** sur **3 itérations fixes**.

### 10 Critiques spécialisés

**Groupe Techniques (4)** — exécution formelle :

| ID | Description |
|----|-------------|
| `critique-lisibilite` | La prose est-elle fluide, sans accroc de lecture ? |
| `critique-fluidite` | Le texte coule-t-il sans ruptures de rythme ? |
| `critique-lexique` | Le vocabulaire est-il précis, ancré dans la bible ? |
| `critique-coherence` | L'unité est-elle cohérente avec les précédentes ? |

**Groupe Impact (6)** — effet sur le lecteur :

| ID | Description |
|----|-------------|
| `critique-voix` | Le point de vue est-il tenu avec cohérence ? |
| `critique-emotion` | La scène provoque-t-elle un état émotionnel réel ? |
| `critique-sensoriel` | Les détails concrets ancrent-ils le lecteur ? |
| `critique-structure` | La construction de la scène est-elle efficace ? |
| `critique-tension` | La scène crée-t-elle une attente, une question non résolue ? |
| `critique-originalite` | Y a-t-il quelque chose d'inattendu, de non-attendu ? |

### 3 Évaluateurs-lecteurs

| Évaluateur | Focus |
|------------|-------|
| **Lecteur ordinaire** | Fluidité, émotion, accroche brute |
| **Lecteur exigeant** | Voix, tension, précision de la langue |
| **Expert du monde** | Fidélité historique / géographique / médicale |

### Scoring non-linéaire

Chaque évaluateur note chaque critère de **0 à 100**.

**Formule de transformation :**
```
f(x) = (x / 100)^1.5 × 100
```

Les excellences sont surpondérées — les faiblesses amplifiées. Pas de moyenne simple.

Exemples :
- 90 → **85.4** / 70 → **58.6** / 50 → **35.4**

**Score final** = moyenne des 3 scores transformés, ramené à /10.

### Pipeline d'itérations

```
Iter 1 → Iter 2 → Iter 3 → ✅ Meilleure version livrée
```

**Règle :** toujours 3 itérations, même si le score est excellent dès iter 1. On livre toujours la meilleure des 3.

### ⚠️ Alertes automatiques à l'auteur

- Régression > 1.0 pt entre deux itérations
- Score < 6.0 à n'importe quelle itération
- Fin des 3 itérations → bilan comparatif iter1 / iter2 / iter3

---

## Étape 6 — Contrôle de cohérence (tous les 5 seeds)

Après chaque bloc de **5 seeds validées**, 3 agents analysent l'ensemble du bloc pour détecter les ruptures globales.

**3 critiques d'arc :**

| ID | Description |
|----|-------------|
| `critique-arc-tension` | La tension narrative globale progresse-t-elle correctement ? |
| `critique-arc-structure` | La structure des 5 unités est-elle cohérente ? |
| `critique-arc-emotion` | L'arc émotionnel du personnage est-il continu et crédible ? |

**Si incohérence détectée :**
→ Production d'une **4e itération corrective** sur les seeds concernées, soumise au Jury.
→ L'auteur est alerté si la correction ne résout pas l'incohérence.

**Si aucune incohérence :** on continue la boucle.

---

## Étape 7 — Boucle × 40-50 seeds

Les étapes 4 → 5 → 6 se répètent pour **chaque unité de rédaction** jusqu'à complétion de l'œuvre.

---

## Étape 8 — Agent Publication : Export DOCX

Agrège toutes les seeds validées et génère un **document Word complet**, mis en forme, prêt à l'édition.

**Livrables :**
- Compilation complète de toutes les unités
- Fichier `.docx` mis en page
- Prêt pour lecture éditoriale

---


---

## Format du rapport Jury (par itération)

```markdown
## Rapport Jury — [Unité] — Iter [N/3]

### Scores
| Critère | Lecteur ord. | Lecteur ex. | Expert | Transformé |
|---------|-------------|-------------|--------|------------|
| lisibilite | X | X | X | X |
| fluidite | X | X | X | X |
| lexique | X | X | X | X |
| coherence | X | X | X | X |
| voix | X | X | X | X |
| emotion | X | X | X | X |
| sensoriel | X | X | X | X |
| structure | X | X | X | X |
| tension | X | X | X | X |
| originalite | X | X | X | X |
| **SCORE FINAL** | | | | **X/10** |

### Points forts (à conserver)
- ...

### Points faibles (à corriger)
- ...

### Recommandations pour iter suivante
1. ...
2. ...

### Décision
[ ] Iter suivante | [ ] Meilleure version livrée | [ ] Alerte auteur
```

---

## Historique

| Date | Événement |
|------|-----------|
| Avril 2026 | Pipeline construit pour *Les Pages manquantes* (projet maria-valtorta) |
| Avril 2026 | 40 unités rédigées avec ce pipeline |
| 12 avril 2026 | Pipeline formalisé dans ce fichier |
| 13 avril 2026 | Mis à jour d'après schéma complet : Orchestrateur, Contrôle de cohérence/5 seeds, Agent Publication |
