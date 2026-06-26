# e-facture-rapprochement

Skill OpenClaw : ingestion **factures + relevés bancaires** → **rapprochement** →
`company.json` + `rapprochement.json` au contrat Pocket-Claw, par client.

## En bref
```
A. Factures   : Factur-X / UBL / CII (fast-path)  +  photos de tickets & PDF (extraction LLM, tier 3)
B. Banque     : CAMT.053 / OFX / CSV  (+ PDF de relevé via LLM)
C. Matching   : montant + date (±N j) + contrepartie/référence ; reste facturable → unmatched_bank_lines ;
                non facturable (salaires, impôts, frais, retraits…) → excluded_bank_lines
D. Sortie     : company.json + rapprochement.json (invariant 3 termes vérifié, écriture atomique)
```

Lancer : `python3 scripts/main.py [<root>] [--real] [--client <slug>] [--today AAAA-MM-JJ]`
(défaut = sandbox `~/.openclaw/workspace/clients-test/`). Boucle en deux temps : le script
liste les pièces non structurées à extraire (worklist), l'agent écrit les sidecars JSON, on
relance. Détails dans `SKILL.md`.

## Arborescence
```
e-facture-rapprochement/
├── SKILL.md                      instructions agent (quand/comment lancer, boucle worklist)
├── references/
│   ├── output-contract.md        schéma EXACT company.json + rapprochement.json + invariant
│   ├── invoice-extraction.md     cascade factures + schéma sidecar + extraction LLM
│   ├── bank-formats.md           CAMT.053 / OFX / CSV + schéma relevé normalisé
│   └── matching-rules.md         scoring, passes, classification, anomalies, relances
├── scripts/
│   ├── main.py                   orchestrateur (ingestion → worklist → rapprochement → sortie)
│   ├── invoice_parsers.py        Factur-X (pdfdetach) / UBL / CII
│   ├── bank_parsers.py           CAMT.053 / OFX / CSV
│   ├── reconcile.py              moteur de rapprochement + invariant + anomalies + relances
│   ├── normalize.py              argent/dates/slugs/similarité + SEUILS réglables
│   ├── test_reconcile.py         tests moteur (déterministes)
│   └── test_e2e.py               test bout-en-bout sur les fixtures
└── fixtures/demo-corse-plomberie/  jeu d'essai (UBL, CII, CAMT, CSV, photo de ticket + sidecar)
```

## Dépendances (présentes sur la VM)
`python3`, `lxml`, `pdftotext` + `pdfdetach` (poppler, pour le XML Factur-X embarqué),
`tesseract` (OCR de secours). Aucune dépendance réseau.

## Réglages (`scripts/normalize.py`)
Tolérance montant, fenêtre date, seuils de score, **seuils de validation humaine**
(`HUMAN_REVIEW_AMOUNT=1000 €`, `HUMAN_REVIEW_CONFIDENCE=0.75`), tolérance TVA, paliers de
relance — tout est regroupé en tête de fichier.

## Place dans l'écosystème compta
Le cabinet dispose par ailleurs d'une architecture modulaire (tri-courrier-entrant →
analyse-piece-comptable → identification-client → classement-document → **rapprochement-paiements**,
orchestrés par pipeline-comptable), centrée sur les relevés PDF scannés (gate + vision) et
qui utilise un bucket `excluded_bank_lines` (invariant à 3 termes).

**Ce skill-ci est une brique autonome et complémentaire**, focalisée sur l'**ingestion
e-facture structurée (Factur-X/UBL/CII) + photos de tickets**. Comme `rapprochement-paiements`,
il sépare les opérations non facturables dans `excluded_bank_lines` (invariant à 3 termes :
`rappr + unmatched + excluded == bank_transactions_count`). Il ne remplace pas
`rapprochement-paiements` ; les deux écrivent le même contrat de sortie — choisis lequel
exécuter selon la source des pièces.
