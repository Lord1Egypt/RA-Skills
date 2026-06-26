---
name: auto-router
description: Routage automatique vers le modèle optimal selon le type de question (local gratuit vs API payant)
---

# Auto-Router Skill

Route automatiquement chaque message vers le modèle le plus adapté et économique.

## Principe

🤖 **Analyse intelligente** → **Choix automatique** → **Exécution optimale**

| Type de question | Modèle choisi | Coût |
|-----------------|---------------|------|
| Questions simples | Llama 3.2 3B (local) | 🆓 Gratuit |
| Usage général | Qwen 2.5 7B (local) | 🆓 Gratuit |
| Code/technique | Qwen Coder 7B (local) | 🆓 Gratuit |
| Business/analyse | Claude Sonnet 4 (API) | 💰 Modéré |
| Très complexe | Claude Opus 4.5 (API) | 💰💰💰 Premium |

## Utilisation

### Activation manuelle

```bash
# Test d'un message
node /Users/thibaut/clawd/auto-router.js "Comment écrire une fonction Python ?"
```

### Intégration Clawdbot

Le skill analyse automatiquement tes messages et route vers le modèle optimal.

## Exemples de routage

```bash
# Question simple → Local gratuit
"Salut ça va ?" → Llama 3.2 3B

# Code → Local gratuit  
"Comment faire une boucle en Python ?" → Qwen Coder 7B

# Business → API modéré
"Quelle stratégie marketing adopter ?" → Claude Sonnet 4

# Très complexe → API premium
"Analyse macro-économique globale avec 20 variables" → Claude Opus 4.5
```

## Économies

- **~85% de réduction** sur les coûts d'IA
- **Questions simples/code** = 100% gratuit (local)
- **Analyses business** = modèle économique (Sonnet)
- **Recherche avancée** = modèle premium (Opus, justifié)

## Configuration

Modèles disponibles dans `/Users/thibaut/clawd/auto-router.js` :

```javascript
const MODELS = {
  'llama3.2:3b': { type: 'local', cost: 0 },
  'qwen2.5:7b': { type: 'local', cost: 0 }, 
  'qwen2.5-coder:7b': { type: 'local', cost: 0 },
  'claude-sonnet-4': { type: 'api', cost: 1 },
  'claude-opus-4.5': { type: 'api', cost: 3 }
};
```

## Notes

- Premier lancement des modèles locaux = plus lent (chargement)
- Modèles locaux restent chargés en mémoire après usage
- Timeouts configurables par modèle
- Règles de routage ajustables selon tes besoins