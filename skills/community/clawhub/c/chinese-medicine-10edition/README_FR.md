# Chinese Medicine — PMPH-10e édition
<div align="center">

> *« Un guide du XXIe siècle pour les étudiants en médecine chinoise »*

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-orange)](https://clawhub.ai)

<br>
> Manuel de compétences cliniques basé sur *Chinese Medicine* (10e édition, People's Medical Publishing House) — 172 compétences cliniques essentielles en MTC
<br>
<br>
<img src="assets/Chinese Medicine-10edition.jpg" width="260px">
<br>

Pourquoi s'acharner à lire un livre entier ?<br>
Il suffit de poser une question pour obtenir automatiquement une solution du manuel.

<br>

**Autres langues / Other Languages:**

[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md) · [Русский](README_RU.md)

</div>

---

## Présentation du projet

Ce projet intègre systématiquement les domaines fondamentaux de la médecine traditionnelle chinoise — théories de base, différenciation des syndromes et traitement, formules et pharmacologie, acupuncture et tuina, gynécologie et pédiatrie, maladies fébriles et lésions par le froid, oncologie, identification des constitutions, et l'intégration médecine chinoise-occidentale. Il couvre **172 compétences cliniques essentielles** réparties en **20 grandes catégories**.

**Public cible** : Praticiens en MTC, cliniciens en médecine intégrée chinoise-occidentale, étudiants en médecine, chercheurs en MTC, professionnels du bien-être et de la santé

**Manuel de référence** : *Chinese Medicine*, 10e édition, People's Medical Publishing House (PMPH) — Manuel national pour les programmes de médecine clinique de premier cycle quinquennaux

**⚠️ Risque ⚠️** : Les utilisateurs pourraient interpréter le contenu diagnostique, les formules, l'acupuncture ou les traitements topiques comme des avis médicaux indépendants.

**Atténuation** : Traitez toute sortie comme une référence éducative ou un matériel destiné à l'examen par un clinicien qualifié, et vérifiez que les recommandations sont conformes aux directives officielles et aux réglementations locales en vigueur.

**⚠️ Risque ⚠️** : Les procédures ou conseils thérapeutiques actionnables peuvent ne pas convenir à l'autodiagnostic, aux urgences, à la grossesse, aux hémorragies, aux affections respiratoires, à l'acupuncture, aux thérapies manuelles, aux procédures de type chirurgical, ou aux médicaments et examens de laboratoire.

**Atténuation** : Une politique de sécurité médicale indépendante est en place pour prévenir l'autotraitement et orienter les scénarios urgents, à haut risque ou procéduraux vers une supervision professionnelle qualifiée.

## Structure du projet

```
Chinese-Medicine-PMPH-10edition/
├── SKILL.md                    # Configuration centrale — Registre des 172 compétences
├── README.md                   # Ce document — Description du projet & guide d'utilisation (multilingue)
│   ├── README_EN.md            # Version anglaise
│   ├── README_JP.md            # Version japonaise
│   ├── README_FR.md            # Version française
│   └── README_RU.md            # Version russe
├── <skill-name>/               # Définitions détaillées de chaque compétence
│   └── SKILL.md                #   Détails de la compétence (quand l'utiliser, étapes, références)
├── index.md                    # Index de navigation des compétences
├── scripts/                    # Scripts d'outils exécutables
├── config/                     # Fichiers de configuration
├── tests/                      # Validation et tests
└── assets/                     # Fichiers de ressources du projet
```

## Aperçu des catégories de compétences

| Catégorie | Comp. | Description |
|-----------|-------|-------------|
| 🧬 Théorie fondamentale de la MTC | 18 | Yin-Yang & Cinq Phases, Zang-Fu & Méridiens, Qi-Sang-Liquides organiques, Constitution |
| 🔍 Principes de différenciation et de traitement | 8 | Principes fondamentaux de la différenciation des syndromes, méthodes thérapeutiques |
| 🫀 Zang-Fu, Méridiens, Physiologie & Pathologie | 13 | Cœur, Foie, Rate, Poumon, Rein — fonctions des méridiens et pathologie |
| 🔬 Méthodes diagnostiques & Quatre Examens | 6 | Diagnostic lingual, diagnostic du pouls, inspection, veinules digitales pédiatriques |
| 🌡️ Différenciation des maladies d'origine externe | 10 | Six Excès, maladies fébriles, syndromes de lésion par le froid |
| 🩺 Maladies diverses en médecine interne | 14 | Constipation, hémorroïdes, vertiges, insomnie, diarrhée, syndrome Bi, etc. |
| 👩 Maladies gynécologiques | 9 | Irrégularités menstruelles, leucorrhée, métrorragie, insuffisance de lait postpartum |
| 🚽 Troubles urinaires & Strangurie | 3 | Différenciation des six types de strangurie, hématurie |
| 💧 Soif épuisante & Œdème | 2 | Différenciation des trois soifs, œdème yang & œdème yin |
| 🟡 Ictère & Masses | 2 | Ictère yang & ictère yin, masses agrégées |
| 🩸 Stase sanguine & Hémorragie | 3 | Syndromes de stase sanguine, Xuefu Zhuyu |
| 💊 Formules & Application médicinale | 26 | Application des formules classiques, compatibilité des herbes, gestion de la toxicité |
| 📍 Acupuncture & Moxibustion | 8 | Aiguille fine, moxibustion, points auriculaires, acupoints |
| ✋ Techniques de Tuina | 5 | Huit méthodes, traction, tapotement, supplementation & drainage |
| 🫳 Thérapies externes & Autres modalités | 3 | Ventouses, Jinhuang San, thérapie topique par les herbes |
| 🤝 Intégration MTC-Médecine occidentale & Applications modernes | 7 | Synergie MTC-MO, intervention prédiabète |
| 📚 Littérature classique & Lignée académique | 4 | Quatre Grands Classiques, *Xinxiu Bencao*, Ge Hong |
| 🎗️ Oncologie & Conditions critiques complexes | 5 | Différenciation des syndromes cancéreux, soutenir le droit & chasser le mal, ascite maligne |
| 👶 Spécialités pédiatriques | 1 | Puberté précoce |
| ⚙️ Classification des méthodes thérapeutiques | 4 | Purgation, formules libérant l'extérieur, formules réchauffant l'intérieur, principe de descente |

## Démarrage rapide

### Installation

CLI :
```bash
openclaw skills install chinese-medicine-10edition
```

Invite (Claude Code) :
```bash
Avant d'installer quoi que ce soit, inspectez les métadonnées et les exigences de configuration de la compétence ClawHub.
Si la compétence vous demande d'installer un package ou un CLI tiers, vérifiez sa source, son mainteneur et le contenu du package avant d'exécuter la commande d'installation.
N'installez la compétence "Chinese Medicine 10e édition" (xllgreen/chinese-medicine-10edition) depuis ClawHub qu'après avoir effectué ces vérifications.
Page de la compétence : https://clawhub.ai/xllgreen/chinese-medicine-10edition
Limitez le travail à cette seule compétence.
Après l'installation, aidez-moi à terminer la configuration à partir des métadonnées vérifiées.
Utilisez uniquement les métadonnées que vous pouvez vérifier depuis ClawHub ; n'inventez pas d'exigences manquantes.
Demandez avant d'apporter des modifications plus larges à l'environnement.
```

### Utilisation

Chaque compétence se compose de quatre parties :
1. **Quand l'utiliser** — Déclencheurs pour invoquer la compétence
2. **Étapes d'exécution** — Procédure opératoire standardisée
3. **Précautions** — Contre-indications et avertissements
4. **Références** — Documents complémentaires détaillés

### Stratégies d'interrogation

#### 1. **Concept**
Question :
```bash
Quelles sont les cinq grandes fonctions physiologiques du Foie régissant la libre circulation ?
```
Réponse :
```bash
Selon la compétence « Le Foie régit la libre circulation — Cinq grandes fonctions physiologiques » : La fonction de libre circulation du Foie fait référence au rôle du qi hépatique dans le lissage et la libre circulation de la dynamique du qi dans tout le corps. Spécifiquement :
1. **Régulation de la dynamique du Qi** : Lisse le mécanisme du qi de tout le corps, le maintient libre et non obstrué
2. **Promotion de la circulation du Sang et des Liquides** : Le qi fait circuler le sang ; le qi fait circuler les liquides
3. **Promotion de la digestion Rate-Estomac et de la sécrétion/excrétion biliaire** : Assiste la montée et la descente du qi Rate-Estomac
4. **Régulation des émotions** : Une libre circulation normale harmonise le qi et le sang, stabilisant l'humeur
5. **Régulation de la fonction reproductive** : Étroitement liée aux menstruations et à la spermatogenèse
```

#### 2. **Analyse de cas clinique**
Question :
```bash
Homme de 45 ans présentant des distensions et douleurs hypochondriaques récurrentes depuis 3 ans, aggravées par le stress émotionnel, accompagnées d'oppression thoracique, soupirs fréquents, diminution de la prise alimentaire, et distension épigastrique. Langue : rouge pâle avec enduit fin blanc. Pouls : cordé. Veuillez procéder à une analyse de différenciation des syndromes.
```
Réponse :
```bash
Analyse et traitement basés sur la compétence « Différenciation du syndrome de Stagnation du Qi du Foie »...
```

#### 3. **Application de formule**
Question :
```bash
Patient présentant fièvre, légère aversion au vent-froid, céphalées, soif, mal de gorge, toux, pointe de langue rouge, enduit fin jaune, pouls flottant et rapide. Veuillez recommander une formule.
```
Réponse :
```bash
Basé sur la compétence « Application de la formule Yinqiao San » — Diagnostic : rhume vent-chaleur (stade Wei-phase au début d'une maladie fébrile). Recommandation : Yinqiao San avec modifications...
```

#### 4. **Sélection de points d'acupuncture**
Question :
```bash
Patient présentant des douleurs épigastriques récurrentes, pires à jeun, légèrement soulagées par la nourriture, accompagnées de reflux acide et d'éructations. Veuillez recommander une prescription d'acupuncture.
```
Réponse :
```bash
Basé sur les compétences « Classification des points d'acupuncture et principes d'indication » et « Principes de sélection des points d'acupuncture »...
```

## Index des compétences

Pour l'index complet des 172 compétences, veuillez consulter [index.md](index.md).

## À propos de l'auteur

**xllgreen (https://xllgreen.github.io)** — Étudiant en médecine à l'École de médecine clinique de l'Université de Jiujiang · Passionné de technologie

## Support technique
<br>
Projet PDF2App : https://pdf2app.cn
<br>
Microsoft Visual Studio Code : https://code.visualstudio.com/
<br>
Claude Code pour VS Code : https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API : https://platform.deepseek.com/
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API : https://platform.xiaomimimo.com/
Copyright © 2010 — 2026 Xiaomi. All Rights Reserved
<br>

## Licence

Le contenu de ce projet est organisé sur la base de la 10e édition de *Chinese Medicine* (People's Medical Publishing House) et est destiné uniquement à un usage éducatif de référence.

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FChinese-Medicine-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
 </picture>
</a>
