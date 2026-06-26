# Contrat de sortie — `company.json` + `rapprochement.json`

> Le backend Pocket-Claw lit **exactement ces deux fichiers par client** et transmet leurs
> objets **VERBATIM** au front (snake_case exact, aucun remapping). Un champ mal nommé ou
> absent s'affiche « — ». **Un JSON malformé est ignoré EN SILENCE** → le client perd ses
> données. Donc : JSON valide impératif, écriture atomique (`.tmp` + rename, déjà gérée par
> `main.py`).

Emplacement : `<root>/<slug>/company.json` et `<root>/<slug>/rapprochement.json`
(slug = minuscules, mots séparés par tirets). Dossiers commençant par `_` = ignorés.

## company.json
Identité. Champs lus (tous optionnels, à remplir si dispo) :
`email, name, siren, siret, legal_form, address, city`. Tout autre champ est conservé brut
mais non affiché. `main.py` préserve l'existant et ne casse jamais ce fichier.

## rapprochement.json — schéma EXACT
```json
{ "periods": [ {
  "period": "2026-04",            // OBLIGATOIRE, "YYYY-MM" STRICT (sinon période ignorée)
  "locked": false,
  "bank_statements_count": 1,     // nb de relevés ; 0 => front affiche "En attente du relevé"
  "bank_transactions_count": 7,   // nb total de transactions du relevé (sert d'invariant)
  "invoices": [ {
    "invoice_id": "AQ-2026-041",
    "type": "in",                 // "in" = achat/fournisseur, "out" = vente/client
    "counterparty_name": "Aquatech Fournitures",
    "amount": 742.50,             // nombre, TTC
    "issued_date": "2026-04-09",  // sinon groupe "Sans date d'émission"
    "due_date": "2026-05-09",
    "status": "paid",             // "unpaid" | "paid" | "partial" | "overdue"
    "bank_matched": true,
    "amount_paid": 742.50,        // alimente "Encaissé sur la période"
    "amount_remaining": 0,        // affiché si status = "partial"
    "anomalies": []               // voir InvoiceAnomaly
    // optionnels: matched_tx, overpaid_by, source_file
  } ],
  "unmatched_bank_lines": [ {     // transactions NON rapprochées MAIS facturables — LES DEUX SENS
    "type": "paiement_orphelin",  // "paiement_orphelin" | "facture_manquante"
    "label": "VIR CLIENT HOTEL ALBA ROSSA",
    "amount": 1980.00,            // SIGNÉ : négatif pour un débit, positif pour un crédit
    "date": "2026-04-08",
    "invoice_ref": null           // réf citée dans le libellé, sinon null
  } ],
  "excluded_bank_lines": [ {      // opérations NON FACTURABLES (jamais une anomalie)
    "label": "VIR SALAIRE J ROSSI",
    "amount": -2400.00,           // SIGNÉ
    "date": "2026-04-28",
    "invoice_ref": null,
    "category": "rh_charges"      // famille non facturable (voir ci-dessous)
  } ],
  "period_anomalies": [],         // optionnel
  "relances": []                  // optionnel
} ] }
```

### InvoiceAnomaly (`invoices[].anomalies[]`)
`type`: `"tva_incorrecte"` | `"invoice_overdue"`
+ champs selon le type : `days_late, discrepancy_pct, total_ht, tva_declared, tva_expected, tva_rate_pct`.

### period_anomalies
`{ "type": "doublon_paiement" | "releve_non_parseable" | "facture_illisible", "label", "amount", "date", "source_file"? }`

### relances
`{ "invoice_id", "counterparty", "amount", "due_date", "days_late", "step": 1|2|3|"escalation", "status", "amount_remaining"?, "note"? }`

> ⚠️ **NE PAS produire de champ `blocking`.** La distinction bloquant/non-bloquant a été
> SUPPRIMÉE du produit ; tout `blocking` résiduel est ignoré.

## Champs minimaux à toujours renseigner
- Facture : `invoice_id, type, counterparty_name, amount, issued_date, due_date, status`.
- Ligne non rapprochée : `type, label, amount, date, invoice_ref` (ou `null`).

## Comment les données sont consommées (POURQUOI chaque champ compte)
Cartes du haut (calculées **uniquement** depuis `invoices[]`) :
- **Total à recouvrer** = Σ dus (paid→0, partial→`amount_remaining`, sinon `amount`).
- **Factures en retard** = nb de `status="overdue"`.
- **Retard maximum** = max des jours de retard (overdue via `due_date` + `relances.days_late`).
- **Encaissé sur la période** = Σ `amount_paid` (ou `amount` si `paid`). Les paiements
  orphelins NE comptent PAS dans « Encaissé » (par design).

Statut de rapprochement affiché par facture :
- `bank_statements_count == 0` → « En attente du relevé »
- `bank_matched=true` ET (`status="partial"` OU anomalie) → « À vérifier »
- `bank_matched=true` sinon → « Rapproché »
- `bank_matched=false` → « Paiement attendu »

Compteurs liste clients : `facture_manquante` → « Factures manquantes » ;
`paiement_orphelin` → « Opérations injustifiées » ; période avec factures et
`bank_statements_count==0` → « Relevés manquants ». Le client passe en
`documents_missing` dès qu'il y a facture manquante / paiement orphelin / relevé manquant /
facture non rapprochée.

## Catégories NON FACTURABLES (`excluded_bank_lines[].category`)
Une opération sans facture en face PAR NATURE n'est ni une `facture_manquante` ni un
`paiement_orphelin` : elle va dans `excluded_bank_lines` et n'est jamais matchée à une facture.
7 familles : `frais_bancaires`, `rh_charges` (salaires), `prestations_sociales`
(URSSAF/CPAM/retraite…), `impots_taxes` (DGFIP/TVA/CFE…), `especes` (retraits/dépôts),
`transfert_interne` (compte à compte/épargne), `virement_particulier`. La détection
(`normalize.classify_non_billable`) est conservatrice ; tu peux forcer une catégorie en
posant `"category"` sur la transaction d'un sidecar de relevé.

## INVARIANT (vérifié par `main.py`, ne JAMAIS finir en KO)
Pour chaque période, **toute transaction du relevé est représentée exactement une fois** :
```
(transactions de la période consommées par une facture)
    + len(unmatched_bank_lines) + len(excluded_bank_lines)
    == bank_transactions_count
```
Comptage **au niveau transaction** (robuste quand une facture est payée par un virement
d'une autre période). L'auto-contrôle affiche
`client | période | tx | rappr | unmat | exclu | somme | OK/KO`.
