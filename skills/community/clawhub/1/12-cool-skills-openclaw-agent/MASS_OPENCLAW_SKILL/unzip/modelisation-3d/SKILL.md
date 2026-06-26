---
name: modelisation-3d
description: Automatisation de la création de modèles 3D via Meshy.ai. Utilisez cette compétence pour transformer du texte ou des images en modèles 3D (STL/OBJ), appliquer des textures et livrer le fichier final.
---

# Modélisation 3D avec Meshy.ai

Cette compétence permet de générer des modèles 3D professionnels en utilisant l'intelligence artificielle de Meshy.ai. Elle automatise le workflow complet, de la conception initiale à l'exportation finale, en passant par la texturation avancée. L'objectif est de transformer des idées textuelles ou des références visuelles en fichiers exploitables pour l'impression 3D, le développement de jeux ou la visualisation architecturale.

## Workflow de Génération et Configuration

Le processus commence par l'accès à l'interface de travail de Meshy.ai. Une fois connecté au [Workspace](https://www.meshy.ai/workspace), il est impératif de sélectionner la méthode de génération appropriée en fonction de l'entrée utilisateur. Le tableau ci-dessous détaille les configurations recommandées pour garantir des résultats optimaux avec le modèle **Meshy-4**.

| Paramètre | Option Recommandée | Description |
| :--- | :--- | :--- |
| **Méthode** | Text-to-3D / Image-to-3D | Dépend de la nature de la demande (description ou image). |
| **Modèle IA** | **Meshy-4** | Le modèle le plus récent et performant disponible gratuitement. |
| **Type de Maillage** | Standard | Utiliser par défaut pour une fidélité maximale des détails. |
| **Pose** | None / A-Pose / T-Pose | Utiliser A-Pose ou T-Pose uniquement pour les personnages. |
| **Format Export** | **STL** ou **OBJ** | Formats standards pour l'impression 3D et la modélisation. |

## Étapes de Production Détaillées

Une fois la configuration initiale établie, la génération du modèle de base est lancée. Il est essentiel de surveiller la progression dans l'interface. Une fois le maillage (mesh) généré, l'étape suivante consiste à appliquer des textures via l'outil **Texture** situé dans le menu latéral gauche. Cet outil utilise l'IA pour générer des matériaux réalistes ou stylisés basés sur le prompt initial.

| Étape | Action Requise | Résultat Attendu |
| :--- | :--- | :--- |
| **1. Génération** | Cliquer sur "Generate" | Création du maillage 3D brut. |
| **2. Texturation** | Activer l'outil "Texture" | Application des couleurs et matériaux IA. |
| **3. Finalisation** | Vérifier le rendu final | Modèle complet prêt pour l'exportation. |
| **4. Exportation** | Cliquer sur "Download" | Téléchargement du fichier dans `/home/ubuntu/Downloads/`. |

## Optimisation des Prompts et Qualité

Pour obtenir des modèles de haute qualité, la précision du prompt est fondamentale. Il est conseillé de mentionner explicitement les matériaux souhaités, tels que le **granite poli**, le **métal brossé** ou le **bois de chêne vieilli**. Le style artistique doit également être précisé pour guider l'IA vers un rendu **photoréaliste** ou au contraire un aspect **stylisé de jeu vidéo**. Pour les générations à partir d'images, l'utilisation de visuels clairs sur fond neutre améliore considérablement la fidélité de la réplique 3D produite.
