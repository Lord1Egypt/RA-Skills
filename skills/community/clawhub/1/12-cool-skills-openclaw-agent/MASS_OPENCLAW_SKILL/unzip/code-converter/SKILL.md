---
name: code-converter
description: "Conversion automatique de code d'un langage à un autre (ex: Python → Go). Utilisez ce skill pour migrer des scripts, refactoriser du code dans un nouveau langage ou comparer des implémentations. Compatible avec OpenClaw."
---

# Code Converter

Ce skill permet de convertir du code source d'un langage de programmation à un autre de manière structurée et fiable.

## Fonctionnalités

1.  **Analyse du code source** : Identification automatique du langage source et des dépendances.
2.  **Conversion intelligente** : Traduction des idiomes, des structures de contrôle et des types de données.
3.  **Gestion des erreurs** : Adaptation des mécanismes de gestion d'erreurs (ex: `try/except` vers `if err != nil`).
4.  **Optimisation** : Utilisation des meilleures pratiques du langage cible.

## Utilisation

### Étape 1 : Préparation du code source
Utilisez le script de préparation pour ajouter des numéros de ligne et faciliter la référence lors de la conversion.

```bash
python3 /home/ubuntu/skills/code-converter/scripts/prepare_conversion.py <chemin_du_fichier>
```

### Étape 2 : Conversion
Lors de la conversion, référez-vous aux modèles de conversion courants pour éviter les pièges spécifiques à chaque langage.

-   **Python → Go** : Voir `/home/ubuntu/skills/code-converter/references/conversion-patterns.md` pour les détails sur le typage et la concurrence.
-   **JS/TS → Rust** : Voir les sections sur le "Borrow Checker" et la gestion de la mémoire.

### Étape 3 : Validation
Après la conversion, vérifiez la syntaxe et exécutez des tests unitaires dans le langage cible.

## Compatibilité OpenClaw

Ce skill est conçu pour être compatible avec OpenClaw. Pour l'utiliser dans OpenClaw :
1.  Copiez le dossier `code-converter` dans votre répertoire de skills OpenClaw (généralement `~/.openclaw/workspace/skills/`).
2.  Le fichier `SKILL.md` sera automatiquement détecté par l'agent OpenClaw.
3.  Les scripts et références sont accessibles via les chemins relatifs définis dans ce document.

## Conseils pour une meilleure conversion
-   **Modularité** : Convertissez de petits modules ou fonctions à la fois plutôt que des fichiers entiers très longs.
-   **Tests** : Fournissez toujours les tests unitaires originaux pour aider à valider la conversion.
-   **Documentation** : Conservez les commentaires originaux et adaptez-les si nécessaire.
