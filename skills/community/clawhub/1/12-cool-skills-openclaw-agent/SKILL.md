---
name: ai-trading
description: "Assistant de trading automatisé pour l'analyse de marché, la détection de signaux et l'exécution de stratégies techniques (RSI, MA, Support/Résistance). À utiliser pour : analyser les cryptomonnaies, calculer la taille des positions, gérer le risque et générer des rapports de performance."
---

# AI Trading

Cette compétence transforme Manus en un assistant de trading discipliné, capable de suivre des stratégies techniques strictes tout en priorisant la gestion des risques.

## Fonctionnalités Principales

- **Analyse Technique Multi-Indicateurs** : Utilisation du RSI (période 14), des Moyennes Mobiles (MA20, MA50) et détection dynamique des supports et résistances.
- **Gestion des Risques Intégrée** : Calcul automatique de la taille de position pour limiter le risque par trade à 1-2% du capital total.
- **Filtrage des Signaux** : Validation des entrées par le volume et la tendance globale pour éviter les faux signaux.
- **Suivi de Performance** : Génération de rapports détaillés incluant le taux de victoire, le profit moyen et le maximum drawdown.

## Ressources de la Compétence

### Scripts

- `scripts/position_sizing.py` : Calcule la taille optimale de la position en fonction du capital, du risque souhaité et de la distance du Stop Loss.
  - Usage : `python3 scripts/position_sizing.py <balance> <risk_percent> <stop_loss_dist>`

### Références

- `references/trading_strategies.md` : Contient les règles détaillées pour les entrées ACHAT/VENTE, les paramètres des indicateurs et les contraintes de sécurité (max 3 trades simultanés).

### Templates

- `templates/performance_report.md` : Modèle pour la création de rapports de trading professionnels.

## Flux de Travail Recommandé

1. **Analyse de Marché** : Récupérer les données de prix (1m, 5m, 15m, 1h) et calculer les indicateurs techniques (RSI, MA).
2. **Détection de Tendance** : Vérifier la tendance avec les MA20/MA50. Ne trader que dans le sens de la tendance.
3. **Validation du Signal** : Attendre que le RSI, le volume et les niveaux de support/résistance confirment l'entrée.
4. **Calcul du Risque** : Utiliser `position_sizing.py` pour déterminer la taille de la position avant toute exécution.
5. **Exécution et Suivi** : Définir obligatoirement un Stop Loss et un Take Profit (Ratio R/R 1:2 minimum).
6. **Reporting** : Utiliser le template de rapport pour documenter chaque trade et analyser la performance globale.

## Contraintes de Sécurité

- **Stop Loss Obligatoire** : Aucun trade ne doit être ouvert sans un Stop Loss défini.
- **Limite de Risque** : Ne jamais dépasser 2% de risque par trade.
- **Mode Test** : Privilégier le "Paper Trading" pour valider de nouvelles stratégies sans risque financier réel.
- **Fail-Safe** : En cas de perte de connexion ou d'erreur API, fermer les positions ouvertes ou arrêter les nouveaux trades.
