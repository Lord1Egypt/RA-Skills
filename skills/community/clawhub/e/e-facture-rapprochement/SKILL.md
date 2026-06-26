---
name: e-facture-rapprochement
description: >-
  Ingère les FACTURES (Factur-X / UBL / CII en fast-path, et surtout les PHOTOS DE TICKETS DE
  CAISSE et PDF par extraction LLM avec score de confiance) ET les RELEVÉS BANCAIRES
  (CAMT.053 / OFX / CSV), puis RAPPROCHE paiements ↔ factures et écrit company.json +
  rapprochement.json au contrat Pocket-Claw. Déclenche ce skill dès qu'il s'agit de
  rapprochement bancaire, de lettrage, de matcher des paiements avec des factures, d'ingérer
  des tickets/factures/relevés pour la compta, de produire rapprochement.json, ou de repérer
  les factures impayées / paiements orphelins / opérations injustifiées d'un client — même
  si l'utilisateur ne dit pas explicitement « rapprochement ». Le vrai travail est fait par
  scripts/main.py ; ne réimplémente jamais le moteur à la main et n'écris jamais le JSON à la main.
license: Interne — usage privé OpenClaw
---

# Skill `e-facture-rapprochement`

Pipeline complet **factures + banque → rapprochement → `rapprochement.json`**, pour un ou
plusieurs clients. Cas d'usage dominant : **photos de tickets de caisse et PDF** côté
factures, exports bancaires (CSV/CAMT/OFX) ou PDF côté banque.

> **Le moteur est dans `scripts/main.py`** : ingestion (`invoice_parsers.py`,
> `bank_parsers.py`) + extraction LLM des pièces non structurées. Le **RAPPROCHEMENT
> lui-même est délégué au moteur unique et audité du skill `rapprochement-paiements` (⑤)**
> — un seul moteur pour les deux skills, donc des sorties **identiques** à entrées
> identiques (politique conservatrice unique : « payé » seulement sur montant serré,
> exclusions prudentes). Ce skill = comment le lancer + faire l'extraction LLM + rendre
> compte. **Ne réimplémente pas le rapprochement** et **n'écris jamais `rapprochement.json`
> à la main** : le format est contractuel (le backend l'ignore en silence s'il est malformé
> → le client perd ses données). `main.py` garantit le format et l'invariant.
> (`reconcile.py` reste présent pour ses tests unitaires mais n'écrit plus la sortie.)

## Les 4 étapes (A → B → C → D)
- **A. Ingestion factures** — cascade : Factur-X (XML CII embarqué) → UBL/CII pur → **LLM
  (texte/vision)** pour les tickets/PDF, avec score de confiance + validation humaine au-delà
  d'un seuil. Voir `references/invoice-extraction.md`.
- **B. Ingestion banque** — CAMT.053 / OFX / CSV → transactions normalisées (montant signé).
  PDF de relevé → extraction LLM. Voir `references/bank-formats.md`.
- **C. Rapprochement** — délégué au **moteur partagé ⑤** (`rapprochement-paiements`) :
  match montant + (référence/contrepartie/date), jamais le montant seul ; non matché →
  `unmatched_bank_lines` ; non facturable (salaires, impôts, frais bancaires, retraits…) →
  `excluded_bank_lines`. Politique conservatrice. Voir `references/matching-rules.md`.
- **D. Sortie** — `company.json` + `rapprochement.json`, invariant vérifié. Voir
  `references/output-contract.md`.

## Disposition d'entrée (par client)
```
<root>/<slug>/invoices|factures/    → factures (pdf, jpg, png, xml…)
<root>/<slug>/bank|releves|banque/  → relevés  (xml CAMT, ofx, csv, pdf…)
<root>/<slug>/company.json          → identité (optionnel ; sert à déduire achat/vente)
```
`<root>` par défaut = **sandbox** `~/.openclaw/workspace/clients-test/` (pour ne pas écraser
d'autres sorties pendant la mise au point). Ajoute `--real` pour viser le vrai
`~/.openclaw/workspace/clients/`. Slug = minuscules-à-tirets ; dossiers `_*` ignorés.

## Exécution — boucle en DEUX temps
Les tickets/PDF passent par TON extraction LLM, donc le run se fait en deux passes.

**Passe 1 — lancer le moteur :**
```bash
python3 scripts/main.py [<root>] [--client <slug>] [--today AAAA-MM-JJ]
```
Le script ingère tout ce qui est structuré. S'il reste des documents non structurés (photos,
PDF sans XML), il **s'arrête** et imprime une **worklist** : pour chacun, un chemin `sidecar`
où écrire le JSON extrait.

**Passe 2 — extraire puis relancer :**
Pour CHAQUE entrée de la worklist :
1. Lis le document (`mode=text` → couche texte via `pdftotext -layout` ; `mode=vision` →
   lis l'image).
2. Extrais au schéma normalisé (`references/invoice-extraction.md` pour une facture,
   `references/bank-formats.md` pour un relevé), avec un `confidence` **honnête**.
3. Écris le JSON dans le chemin `sidecar` indiqué (`<doc>.<ext>.invoice.json` ou `.bank.json`).

Puis relance la même commande. Quand la worklist est vide, `main.py` rapproche, écrit les
2 fichiers, et imprime l'auto-contrôle. Les sidecars sont un cache : un doc déjà extrait
n'est pas redemandé.

## Après l'exécution — rendre compte
Lis l'auto-contrôle et relaie au comptable un tableau lisible **par client** : factures
payées / en attente / partielles / en retard, paiements orphelins et factures manquantes,
relances. **Mets en avant les factures listées pour validation humaine** (`_review.json` :
montant élevé ou extraction peu sûre) — un humain doit les confirmer. Jamais de chemins
techniques bruts.

## Règles critiques
- **Format de sortie = contrat.** N'écris pas `rapprochement.json`/`company.json` à la main ;
  laisse `main.py` le faire (écriture atomique, snake_case exact). Pas de champ `blocking`
  (supprimé du produit).
- **Invariant non négociable.** Pour chaque période,
  `rappr + unmatched + excluded == bank_transactions_count` (aucune transaction oubliée).
  `main.py` l'affiche (`OK/KO`) et **sort en erreur si une période est KO** — ne termine pas
  sur un KO ni sur un JSON invalide.
- **N'invente jamais un montant.** Ticket illisible → sidecar `confidence:0.0` sans montant →
  anomalie `facture_illisible` (pièce à re-fournir). Mieux vaut une anomalie qu'un faux chiffre.
- **Confiance honnête.** Elle pilote la validation humaine (seuils dans `normalize.py` :
  `HUMAN_REVIEW_AMOUNT`, `HUMAN_REVIEW_CONFIDENCE`).
- **Sandbox d'abord.** Sans `--real`, tout va dans `clients-test/` ; on bascule sur le vrai
  `clients/` une fois validé.
- **Si le script échoue**, signale l'erreur exacte (stderr) ; ne rejoue pas le rapprochement à la main.

## Tests
```bash
python3 scripts/test_reconcile.py   # moteur (montants, dates, matching, invariant, TVA)
python3 scripts/test_e2e.py         # bout-en-bout sur fixtures/ (UBL+CII+CAMT+CSV+ticket)
```

## Périmètre
Ce skill **produit seulement** `company.json` + `rapprochement.json` ; il ne touche ni au
backend, ni au front, ni aux e-mails. Il complète l'écosystème compta existant (voir README)
en se concentrant sur l'ingestion e-facture/ticket structurée + LLM.
