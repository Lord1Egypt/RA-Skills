---
name: analyse-piece-comptable
description: Analyse UNE pièce comptable (facture, relevé bancaire ou note de frais) et en rend compte au comptable — sans la classer ni la déplacer. À utiliser dès que le comptable veut comprendre une pièce isolée : « regarde cette facture », « qu'est-ce que c'est ce document ? », « lis-moi ce relevé », « c'est quoi cette note de frais ? », « il y a un souci sur cette pièce ? », « combien de TVA sur cette facture ? », ou simplement quand une pièce jointe arrive et que le comptable veut un avis dessus avant tout classement. Extrait le type de pièce, les montants, la TVA, les dates, l'émetteur/destinataire (ou société/salarié pour une note de frais), et signale les incohérences (champ manquant, TVA fausse, total qui ne tombe pas juste, IBAN invalide, date aberrante). Lecture seule : ne range rien (le classement, c'est classement-document) et ne rapproche rien (c'est rapprochement-paiements).
license: Interne — usage privé OpenClaw
---

# Skill `analyse-piece-comptable`

> Analyse **une** pièce isolée et en parle au comptable. Rien d'autre.
> Lecture seule : **ne déplace, ne renomme, ne classe, ne rapproche aucun fichier.**
> Le travail d'extraction et de contrôle est fait par `scripts/analyse.py`.

C'est l'outil de réflexe quand le comptable a une pièce sous les yeux et veut savoir
ce qu'elle contient ou si quelque chose cloche — avant même de décider quoi en faire.

---

## Comment l'utiliser

Une seule commande par pièce :

```bash
python3 scripts/analyse.py <fichier> --date-ref <AAAA-MM-JJ>
```

`--date-ref` = la date du jour (sert à détecter les dates d'émission dans le futur).
Le script renvoie un JSON sur stdout. Tu le lis, puis tu en fais un compte-rendu métier.

### Pourquoi passer par le script

L'extraction des montants, numéros et dates est déterministe et déjà éprouvée.
La faire « à l'œil » en lisant le PDF produit des valeurs incohérentes d'une fois sur
l'autre (numéro de facture tronqué, montant à 0…). Le script ne fait pas ces erreurs.
**Réserve la lecture visuelle au seul cas où le script ne trouve aucun texte** (voir plus bas).

---

## Ce que renvoie le script

```jsonc
{
  "kind": "invoice | bank-statement | note-de-frais | other",
  "text_found": true,            // false → PDF scanné/photographié, sans couche texte
  "confidence": "haute | moyenne | faible",
  "fields": { /* champs extraits — null si introuvable, jamais inventé */ },
  "checks": [
    { "code": "...", "severity": "bloquant | alerte | info", "detail": "..." }
  ]
}
```

Le champ `checks` est le cœur de l'analyse : ce sont les contrôles de cohérence
faits sur la pièce seule. Voici ce qu'ils signifient.

| code | sens |
|------|------|
| `champ_manquant` | un champ essentiel n'a pas été trouvé (n° de facture, montant TTC, titulaire…) |
| `tva_incoherente` | la TVA déclarée ne correspond pas à HT × taux (écart > 5 %) |
| `montant_aberrant` | HT + TVA ≠ TTC affiché |
| `date_future` | date d'émission postérieure à aujourd'hui |
| `echeance_anterieure` | échéance avant la date d'émission |
| `iban_invalide` | l'IBAN du relevé échoue le contrôle de clé |
| `solde_incoherent` | solde d'ouverture + mouvements ≠ solde de clôture |
| `releve_non_parseable` | aucune opération lisible dans le relevé |
| `sans_texte` | la pièce ne contient aucun texte exploitable (scan/photo) |

`bloquant` = la pièce ne peut pas être tenue pour fiable telle quelle.
`alerte` = à vérifier mais exploitable. `info` = simple signalement.

---

## Si la pièce est un scan ou une photo (`text_found: false`)

Là, le moteur ne peut rien extraire — c'est une image. Dans ce cas seulement,
**lis la pièce toi-même** pour en donner la teneur au comptable. Mais comme
cette lecture visuelle est moins fiable qu'une extraction :

- annonce clairement que les valeurs sont **lues à l'œil, à confirmer** ;
- ne présente jamais ces chiffres avec la même assurance qu'une extraction propre ;
- conclus en proposant, si la pièce compte vraiment, de la faire repasser une fois
  océrisée pour une lecture certaine.

C'est volontaire : on préfère une lecture honnête « sous réserve » à un silence.

---

## Comment en rendre compte au comptable

Tu parles à un comptable, dans le ton habituel : précis, sobre, sans jargon technique.
Ne mentionne jamais le script, le JSON, l'OCR, les chemins de fichiers, les `checks`.
Traduis tout en langage métier.

Structure simple, dans cet ordre :

1. **Ce que c'est** — facture (à l'achat / à la vente), relevé bancaire, note de frais,
   ou pièce non reconnue. Pour une facture : émetteur → destinataire. Pour une note de
   frais : société (employeur) → salarié remboursé, et montant à rembourser.
2. **Les chiffres clés** — n° de pièce, date, montant TTC (et HT / TVA si utile),
   échéance. Pour un relevé : titulaire, banque, période, soldes, nombre d'opérations.
3. **Ce qui mérite attention** — chaque anomalie en une phrase claire, le plus
   important d'abord. Si rien ne cloche, dis-le franchement.

Reste bref : une pièce nette tient en trois ou quatre lignes. N'allonge que s'il y a
des points à signaler. Si un champ essentiel manque, dis-le simplement plutôt que de
combler le vide.

### Exemple

Sortie du script (facture saine) :

```json
{ "kind": "invoice", "confidence": "haute",
  "fields": { "invoice_id": "F3-2026-0001", "issue_date": "2026-03-02",
    "due_date": "2026-04-01", "total_ht": 2700.0, "tva_rate": 0.2,
    "tva_amount": 540.0, "total_ttc": 3240.0,
    "emitter": "Numérix Studio", "recipient": "Auberge du Vieux Port" },
  "checks": [] }
```

Compte-rendu au comptable :

> Facture de vente n° F3-2026-0001, émise le 2 mars 2026 par Numérix Studio à
> l'Auberge du Vieux Port. Montant : 3 240 € TTC (2 700 € HT + 540 € de TVA à 20 %),
> échéance au 1ᵉʳ avril. Tout est cohérent, rien à signaler.

Avec une anomalie (TVA incohérente) :

> Facture d'achat n° A-2026-114 de Tuyo SARL, 1 980 € TTC. **À vérifier** : la TVA
> indiquée (300 €) ne correspond pas au taux de 20 % sur le HT, qui donnerait
> environ 330 €. Je vous suggère de contrôler la pièce auprès du fournisseur avant
> de la comptabiliser.

---

## Limites assumées

- **Une pièce à la fois.** Pour traiter et classer un lot entrant, c'est
  `classement-document`. Pour rapprocher paiements et factures, c'est
  `rapprochement-paiements`. Ce skill ne fait qu'analyser et expliquer.
- **Lecture seule.** Aucune écriture, aucun déplacement, aucune mise à jour de
  `clients.json` ni de quoi que ce soit d'autre.
- Les contrôles portent sur la pièce seule. Un doublon, un paiement manquant ou un
  rapprochement ne se voient qu'au niveau du dossier — ce n'est pas ici qu'on les juge.
