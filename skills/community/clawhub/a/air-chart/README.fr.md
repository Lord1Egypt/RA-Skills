<div align="center">

# Air-chart

**Une phrase. Votre IA vous dessine un graphique professionnel de qualité de l'air.**

English | [简体中文](README.zh.md) | [Español](README.es.md) | [हिन्दी](README.hi.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | **Français**

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## Que fait cette skill ?

Dites une phrase dans votre chat IA — elle **trouve la station, récupère les données et vous remet un lien vers le graphique**, grâce à [x-cmd Draw](https://x-cmd.com/draw) — données et graphique dans une seule URL :

> 💬 "Montre-moi la tendance PM2.5 de Pékin sur la semaine dernière"
> 💬 "Compare la qualité de l'air de Tokyo et Séoul sur les 7 derniers jours"
> 💬 "PM10 sur 30 jours à New Delhi, par rapport à la ligne directrice de l'OMS"
> 💬 "Ozone horaire à Singapour sur les dernières 48 heures"
> 💬 "Quelle station de Pékin est la pire en ce moment ?"

En coulisses, un pipeline entièrement automatisé : résout la ville → choisit une station **réellement active** sur **OpenAQ** (données gouvernementales de référence de plus de 100 pays) → nettoie valeurs aberrantes et lacunes → rend un graphique professionnel.

**Pourquoi vous allez l’adorer :**

- **Le graphique est une URL — l'URL est la donnée** — par défaut vous obtenez un lien `x-cmd.com/draw` qui à la fois rend le graphique et porte chaque valeur. Partagez-le, intégrez-le en Markdown comme image, ou modifiez un chiffre dans l'URL et le graphique se met à jour. Besoin d'un fichier ? `--out chart.svg` (ou `.png`) le télécharge.
- **Rendu par x-cmd Draw** — votre pipeline local reste en pur `bash`/`jq`/`awk`/`curl` ; le moteur de graphiques est [x-cmd Draw](https://x-cmd.com/draw), vous héritez donc d'une bibliothèque croissante de types de graphiques (courbes, barres, aires, camemberts, radar, jauges, sankey, Gantt, cartes mentales et plus), de thèmes clair/sombre, d'un rendu multilingue, d'un éditeur en ligne — et zéro code de rendu à maintenir. Rien à installer, rien à mettre à jour.
- **Fiable par conception** — privilégie les stations gouvernementales de référence ; les graphiques étiquettent la concentration physique (µg/m³) et superposent la **ligne directrice de 24 h de l'OMS** comme série de référence : la limite voyage avec la donnée au lieu d'être une réflexion après coup. Pas un nombre d'AQI ostentatoire — des données présentables dans un rapport.
- **Couverture mondiale, entrée tolérante** — coordonnées intégrées de plus de 250 villes ; les noms approximatifs (`delhi`, `tOKyo`, `中山`) fonctionnent tels quels, et les `lat,lon` bruts sont acceptés aussi.
- **Des données réelles, pas un jouet** — écarte les stations « zombies » silencieuses et les pics de défaillance de capteur ; les heures manquantes sont omises de l'axe, jamais comblées par 0.

## Vitrine

Chaque graphique ci-dessous est une **mesure OpenAQ réelle** rendue en direct depuis son URL qui porte les données — aucun fichier image n'est stocké dans ce dépôt. Cliquez sur un graphique pour l'ouvrir dans l'éditeur x-cmd Draw et ajuster les valeurs.

| PM2.5 multi-villes, 7 derniers jours (Tokyo · Séoul · Londres) | New Delhi PM2.5 / PM10, 14 derniers jours |
| --- | --- |
| [![PM2.5 multi-villes, 7 derniers jours (Tokyo · Séoul · Londres)][sc1] | [![New Delhi PM2.5 / PM10, 14 derniers jours][sc3] |

| Ozone (O₃) de Londres, dernières 48 heures | Instantané PM10 par station à New Delhi (en direct) |
| --- | --- |
| [![Ozone (O₃) de Londres, dernières 48 heures][sc2] | [![Instantané PM10 par station à New Delhi (en direct)][sc4] |

| Thème sombre : PM2.5 multi-villes | New Delhi PM2.5, 30 derniers jours |
| --- | --- |
| [![Thème sombre : PM2.5 multi-villes][sc5] | [![New Delhi PM2.5, 30 derniers jours][sc6] |

[sc1]: https://x-cmd.com/draw?type=line&title=Comparaison%20PM2.5%20%C2%B7%20derniers%207d%20%C2%B7%20multi-villes%20%C2%B7%20m%C3%AAme%20param%C3%A8tre&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=OMS%2024h:15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc2]: https://x-cmd.com/draw?type=line&title=Tendance%20London%20O3%20%C2%B7%20derniers%2048h%20%C2%B7%20heure%20locale%20%28Europe%2FLondon%29&unit=%C2%B5g%2Fm%C2%B3&labels=11-12%2001%3A00,11-12%2002%3A00,11-12%2003%3A00,11-12%2004%3A00,11-12%2005%3A00,11-12%2006%3A00,11-13%2000%3A00,11-13%2001%3A00,11-13%2002%3A00,11-13%2003%3A00,11-13%2004%3A00,11-13%2005%3A00,11-13%2006%3A00,11-13%2007%3A00&series=London%20O3:52.7,51.2,42.7,43.1,41,31.4,42.7,44.9,46.5,48.3,39.6,17.1,15.4,17&series=OMS%2024h:100,100,100,100,100,100,100,100,100,100,100,100,100,100&w=960&h=500&t=opendata
[sc3]: https://x-cmd.com/draw?type=line&title=Tendance%20New%20Delhi%20PM2.5%20%2F%20PM10%20%C2%B7%20derniers%2014d%20%C2%B7%20multi-param%C3%A8tres&unit=%C2%B5g%2Fm%C2%B3&labels=10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=OMS%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc4]: https://x-cmd.com/draw?type=hbar&title=Instantan%C3%A9%20New%20Delhi%20par%20station%20%C2%B7%20PM10%20%C2%B7%202026-11-14%2013%3A27%20IST%20%C2%B7%20rayon%20de%2025%20km&unit=%C2%B5g%2Fm%C2%B3&labels=Alipur,Anand%20Vihar,Ashok%20Vihar,Aya%20Nagar,Bawana,Burari%20Crossing&values=418.0,409.0,426.0,501.0,382.0,533.0&num=all&w=960&h=480&t=evil-glow
[sc5]: https://x-cmd.com/draw?type=line&title=Comparaison%20PM2.5%20%C2%B7%20derniers%207d%20%C2%B7%20multi-villes%20%C2%B7%20m%C3%AAme%20param%C3%A8tre&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=OMS%2024h:15,15,15,15,15,15,15&w=960&h=500&scheme=dark&t=opendata
[sc6]: https://x-cmd.com/draw?type=line&title=Tendance%20New%20Delhi%20PM2.5%20%C2%B7%20derniers%2030d%20%C2%B7%20heure%20locale%20%28Asia%2FKolkata%29&unit=%C2%B5g%2Fm%C2%B3&labels=10-15,10-16,10-17,10-18,10-19,10-20,10-21,10-22,10-23,10-27,10-28,10-29,10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:73.6,65.7,94,127,94,125,142,136,142,138,131,95,44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=OMS%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata

## Caractéristiques

- **Zéro dépendance lourde** — pur `bash` / `jq` / `awk` / `curl` ; le moteur SVG est écrit en awk.
- **Couverture mondiale** — coordonnées intégrées de plus de 200 villes majeures, ou passez `lat,lon` directement.
- **Sélection intelligente de station** — recherche dans un rayon de 25 km → écarte les stations « zombies » silencieuses depuis 24 h (repli à 72 h) → privilégie les moniteurs gouvernementaux de référence.
- **Visuels professionnels** — unités de concentration physique (µg/m³) clairement étiquetées, ligne directrice de 24 h de l'OMS superposée par défaut (verte si conforme, rouge si dépassée), thèmes clair/sombre.
- **Conçu pour le monde réel** — cache local (20 min horaires / 2 h journalières), recul exponentiel sur HTTP 429, rendu conscient des lacunes (les trous brisent la courbe — jamais comblés par 0), alignement UTC → heure locale de la station.

## Démarrage rapide

### 1. Obtenir une clé API (gratuite, ~1 minute)

1. Créez un compte ou connectez-vous sur [OpenAQ Explorer](https://explore.openaq.org/register) (compte existant : [se connecter](https://explore.openaq.org/login)).
2. Ouvrez votre [page de compte](https://explore.openaq.org/account) — votre clé API figure près du bas ; copiez-la.
3. Configurez-la — au choix :

```bash
export OPENAQ_API_KEY="your_key"                             # ephemeral / CI
echo 'OPENAQ_API_KEY=your_key' > ~/.config/air-chart/config  # persistent
```

Aucun trousseau système requis — un identifiant de service public et gratuit vit dans un simple fichier de configuration en clair. Sans clé, le mode `--demo` rend tout de même avec des données d'exemple.

### 2. Exécuter

```bash
# Ville unique, tendance PM2.5 sur 7 jours
./scripts/air_chart.sh --city Beijing --param pm25 --period 7d

# Comparaison multi-villes (jusqu’à 4 villes)
./scripts/air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d

# Ville unique, multi-paramètres (PM2.5 + PM10)
./scripts/air_chart.sh --city Beijing --param pm25 --param pm10 --period 30d

# Courbe horaire sur 48 heures (rythme jour/nuit)
./scripts/air_chart.sh --city Singapore --param o3 --period 48h

# Instantané en barres des stations en temps réel
./scripts/air_chart.sh --city Delhi --param pm10 --snapshot

# Thème sombre, sortie personnalisée
./scripts/air_chart.sh --city London --param no2 --period 14d --theme dark -o london.svg
```

### 3. Installer comme skill d'agent IA

```bash
git clone https://github.com/qiakai/air-chart.git ~/.claude/skills/air-chart
# or: npx skills add qiakai/air-chart
```

Puis demandez simplement à votre agent : *« Compare le PM2.5 de Tokyo et de Séoul sur les 7 derniers jours. »*

`SKILL.md` est rédigé en anglais pour une compatibilité maximale avec agents et registres ; une version chinoise est disponible à `SKILL.zh.md`. La sortie des graphiques accepte `--lang en|zh|es|hi|ja|ko|fr` (détection automatique depuis le locale du système par défaut).

## Référence CLI

| Flag | Description | Values |
| --- | --- | --- |
| `--city, -c` | Nom de ville (répétable, ≤4) ou coordonnées `"lat,lon"` | `Beijing`, `New Delhi`, `39.9,116.4` |
| `--param, -p` | Polluant (par défaut `pm25`) | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | Plage temporelle (par défaut `7d`) | `24h` `48h` (horaire) · `7d` `14d` `30d` (journalier) |
| `--snapshot` | Instantané en barres des stations actives de la ville | flag |
| `--theme` | Thème de couleur | `light` / `dark` |
| `--lang` | Langue de sortie (graphiques + messages) | `en` `zh` `es` `hi` `ja` `ko` `fr` (par défaut : auto-détection du locale) |
| `--out, -o` | Télécharge le graphique en `.svg` ou `.png` | par défaut : affiche uniquement l'URL x-cmd Draw |
| `--demo` | Mode démo, aucune clé API requise | flag |

## Architecture

```text
[city / pollutant / time range]
   │
   ▼
geo_resolve.sh      city name → coordinates + timezone (built-in gazetteer / raw lat,lon)
   │
   ▼
openaq_client.sh    OpenAQ API v3: auth, User-Agent, md5 cache,
                    429 exponential backoff, liveness filter (24h/72h),
                    sensor match by fixed parameter ID, reference-grade first
   │
   ▼
data_transform.awk  cleaning (negatives / physically impossible spikes),
                    gap detection (breaks, never zero-filled), stats, local-time labels
   │
   ▼
render_draw.sh      x-cmd Draw URL builder (URL-as-Data; optional .svg/.png download)
```

`data/parameters.tsv` est un dictionnaire statique de paramètres aligné sur les ID fixes de polluants de openaq-api : slug / param_id / nom / unité / ligne directrice 24 h OMS / plafond physique / couleur par paramètre — sans allers-retours redondants vers `/parameters`. Le visuel suit les conventions d'openaq-explorer : palette par paramètre (PM2.5 `#E65100`, PM10 `#6A1B9A`, O3 `#0277BD`, NO2 `#00838F`), palette multi-villes adaptée aux daltoniens, et ligne directrice OMS en vert de sécurité `#10B981` / rouge d'alerte `#EF4444`. Si une station rapporte des unités différentes du réglage par défaut du dictionnaire (p. ex. ppm), l'axe Y utilise les unités réelles et la ligne OMS est supprimée pour éviter toute confusion dimensionnelle.

## Codes de sortie

| Code | Meaning |
| --- | --- |
| 3 | Clé API non configurée (affiche le guide de configuration) |
| 4 | Erreur réseau / API / réessais de limite épuisés |
| 5 | Aucune station active ou aucune donnée valide |
| 2 | Nom de ville insoluble (affiche les candidats proches) |

## Licence

MIT
