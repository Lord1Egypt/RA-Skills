# AGENTS.md — Herbert

## Démarrage de session

Avant toute interaction :
1. Lire `SOUL.md` — la méthode et l'identité
2. Lire `MEMORY.md` — les projets en cours et les leçons apprises
3. Reprendre le contexte du projet en cours si disponible
4. Si un projet est actif : lire sa `bible.md`, son `outline.md`, et les seeds en cours

## Structure des projets

```
projects/
  {slug-projet}/
    bible-[personnage].md   ← une bible par fil narratif
    outline.md              ← sommaire validé avec unités numérotées
    seeds.md                ← graines de l'auteur (3-5 lignes par unité)
    pacte-narratif.md       ← le vrai sujet, tranché
    chapters/
      A01-titre.md          ← fil A, unité 1
      L01-titre.md          ← fil L, unité 1
      ...
```

## Règles de rédaction

- Ne jamais démarrer la passe 1 sans les graines de l'auteur
- Ne jamais passer à l'unité N+1 sans validation de l'unité N
- Signaler explicitement quand on change de passe (Passe 1 → Passe 2)
- Toujours préciser le modèle utilisé pour les tâches non-triviales

## Mémoire

- Notes de travail dans les fichiers du projet
- Mémoire long terme dans `MEMORY.md`
- Écrire, ne pas mémoriser mentalement

## Sécurité

- Ne pas exfiltrer le contenu des projets
- Demander confirmation avant toute suppression
- Règle des 3 échecs : arrêter et alerter l'auteur après 3 tentatives infructueuses
