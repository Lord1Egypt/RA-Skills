# 🦅 Context-Hawk

> **Gardien de Mémoire Contextuelle pour l'IA** — Arrêtez de perdre le fil, commencez à retenir ce qui compte.

*Donnez à n'importe quel agent IA une mémoire qui fonctionne vraiment — à travers les sessions, les sujets, le temps.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## Ce qu'il fait

La plupart des agents IA souffrent d'**amnésie** — chaque nouvelle session part de zéro. Context-Hawk résout cela avec un système de gestion de mémoire de qualité production qui capture automatiquement ce qui compte, laisse le bruit se dissiper, et rappelle la bonne mémoire au bon moment.

**Sans Context-Hawk :**
> "Je t'ai déjà dit — je préfère les réponses concises !"
> (session suivante, l'agent oublie encore)

**Avec Context-Hawk :**
> (applique silencieusement vos préférences de communication depuis la session 1)
> ✅ Réponse concise et directe à chaque fois

---

## ❌ Without vs ✅ With Context-Hawk (TODO: translate)

| Scenario | ❌ Without Context-Hawk | ✅ With Context-Hawk |
|----------|------------------------|---------------------|
| **New session starts** | Blank — knows nothing about you | ✅ Injects relevant memories automatically |
| **User repeats a preference** | "I told you before..." | Remembers from day 1 |
| **Long task runs for days** | Restart = start over | Task state persists via `hawk resume` |
| **Context gets large** | Token bill skyrockets | 5 compression strategies keep it lean |
| **Duplicate info** | Same fact stored 10 times | SimHash dedup — stored once |
| **Memory recall** | All similar, redundant injection | MMR diverse recall — no repetition |
| **Memory management** | Everything piles up forever | 4-tier decay — noise fades, signal stays |
| **Self-improvement** | Repeats the same mistakes | importance + access_count tracking → smart promotion |
| **Multi-agent team** | Each agent starts fresh | Shared memory via LanceDB |

---

## ✨ 12 Fonctionnalités Principales

---

## ✨ 12 Fonctionnalités Principales

| # | Fonctionnalité | Description |
|---|---------|-------|
| 1 | **Persistance de l'État des Tâches** | `hawk resume` — persiste l'état, reprend après redémarrage |
| 2 | **Mémoire à 4 Niveaux** | Working → Short → Long → Archive avec décroissance Weibull |
| 3 | **JSON Structuré** | Score d'importance (0-10), catégorie, niveau, couches L0/L1/L2 |
| 4 | **Score d'Importance IA** | Auto-score les souvenirs, élimine le contenu à faible valeur |
| 5 | **5 Stratégies d'Injection** | A(high-imp) / B(task) / C(recent) / D(top5) / E(full) |
| 6 | **5 Stratégies de Compression** | summarize / extract / delete / promote / archive |
| 7 | **Auto-Introspection** | Vérifie la clarté de la tâche, infos manquantes, détection de boucle |
| 8 | **Recherche Vectorielle LanceDB** | Optionnel — recherche hybride vectorielle + BM25 |
| 9 | **Fallback Mémoire Pure** | Fonctionne sans LanceDB, persistance JSONL |
| 10 | **Déduplication Auto** | Fusionne automatiquement les souvenirs en double |
| 11 | **MMR Recall** | Maximal Marginal Relevance — diverse recall, no repetition |
| 12 | **6-Category Extraction** | LLM-powered: fact / preference / decision / entity / task / other |

---

## 🚀 Installation Rapide

```bash
# Installation en une ligne (recommandé)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# Ou directement via pip
pip install context-hawk

# Avec toutes les fonctionnalités (y compris sentence-transformers)
pip install "context-hawk[all]"
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Session actuelle (5-10 derniers tours)  │
│       ↓ Décroissance Weibull                                  │
│  Short-term      ←── Contenu 24h, résumé                    │
│       ↓ access_count ≥ 10 + importance ≥ 0.7               │
│  Long-term       ←── Connaissance permanente, indexée        │
│       ↓ >90 jours ou decay_score < 0.15                    │
│  Archive          ←── Historique, chargé à la demande       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Persistant à travers les redémarrages│
│  - Tâche actuelle / étapes suivantes / progression / sorties  │
├──────────────────────────────────────────────────────────────┤
│  Moteur d'Injection  ←── Stratégie A/B/C/D/E décide le rappel│
│  Auto-Introspection ←── Chaque réponse vérifie le contexte    │
│  Déclenchement Auto ←── Tous les 10 tours (configurable)    │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Mémoire d'État de Tâche (Fonctionnalité la Plus Précieuse)

Même après redémarrage, coupure de courant ou changement de session, Context-Hawk reprend exactement où il s'était arrêté.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Compléter la documentation API",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Revoir le modèle d'architecture", "Rapport à l'utilisateur"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["La couverture doit atteindre 98%", "Les API doivent être versionnées"],
  "resumed_count": 3
}
```

```bash
hawk task "Compléter la documentation"  # Créer une tâche
hawk task --step 1 done             # Marquer étape terminée
hawk resume                           # Reprendre après redémarrage ← ESSENTIEL !
```

---

## 🧠 Mémoire Structurée

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Contenu original complet",
  "summary": "Résumé en une ligne",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Score d'Importance

| Score | Type | Action |
|-------|------|--------|
| 0.9-1.0 | Décisions/règles/erreurs | Permanent, décroissance la plus lente |
| 0.7-0.9 | Tâches/préférences/connaissances | Mémoire long terme |
| 0.4-0.7 | Dialogue/discussion | Court terme, décroissance vers archive |
| 0.0-0.4 | Chat/_messages de salutation | **Éliminer, ne jamais stocker** |

---

## 🎯 5 Stratégies d'Injection de Contexte

| Stratégie | Déclencheur | Économie |
|----------|-----------|----------|
| **A: Haute Importance** | `importance ≥ 0.7` | 60-70% |
| **B: Liée à la Tâche** | scope correspond | 30-40% ← défaut |
| **C: Récente** | 10 derniers tours | 50% |
| **D: Top5 Rappel** | top 5 `access_count` | 70% |
| **E: Complète** | pas de filtre | 100% |

---

## 🗜️ 5 Stratégies de Compression

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 Système d'Alerte à 4 Niveaux

| Niveau | Seuil | Action |
|-------|-------|--------|
| ✅ Normal | < 60% | Silencieux |
| 🟡 Surveiller | 60-79% | Suggestion de compression |
| 🔴 Critique | 80-94% | Pause écriture auto, forcer suggestion |
| 🚨 Danger | ≥ 95% | Bloquer écritures, compression obligatoire |

---

## 🚀 Démarrage Rapide

```bash
# Installer le plugin LanceDB (recommandé)
openclaw plugins install memory-lancedb-pro@beta

# Activer le skill
openclaw skills install ./context-hawk.skill

# Initialiser
hawk init

# Commandes essentielles
hawk task "Ma tâche"    # Créer une tâche
hawk resume             # Reprendre la dernière tâche ← TRÈS IMPORTANT
hawk status            # Voir l'utilisation du contexte
hawk compress          # Compresser la mémoire
hawk strategy B        # Passer en mode lié à la tâche
hawk introspect         # Rapport d'auto-introspection
```

---

## Déclenchement Auto : Tous les N Tours

Tous les **10 tours** (défaut, configurable), Context-Hawk automatiquement :

1. Vérifie le niveau d'eau du contexte
2. Évalue l'importance des souvenirs
3. Vous rapporte le statut
4. Suggère une compression si nécessaire

```bash
# Config (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,
  "keep_recent": 5,
  "auto_compress_threshold": 70
}
```

---

## Structure des Fichiers

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Outil CLI Python
└── references/
    ├── memory-system.md           # Architecture 4 niveaux
    ├── structured-memory.md      # Format mémoire et importance
    ├── task-state.md           # Persistance état de tâche
    ├── injection-strategies.md  # 5 stratégies d'injection
    ├── compression-strategies.md # 5 stratégies de compression
    ├── alerting.md             # Système d'alerte
    ├── self-introspection.md   # Auto-introspection
    ├── lancedb-integration.md  # Intégration LanceDB
    └── cli.md                  # Référence CLI
```

---

## Spécifications Techniques

| | |
|---|---|
| **Persistance** | Fichiers JSONL locaux, pas de base de données |
| **Recherche Vectorielle** | LanceDB (optionnel) + sentence-transformers embedding local, repli automatique vers fichiers |
| **Recherche** | BM25 + recherche vectorielle ANN + fusion RRF |
| **Fournisseurs d'Embedding** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | Universel, sans logique métier, fonctionne avec n'importe quel agent IA |
| **Zéro Config** | Fonctionne prêt à l'emploi (mode BM25-only) |
| **Python** | 3.12+ |

---

## Licence

MIT — libre d'utilisation, modification et distribution.
