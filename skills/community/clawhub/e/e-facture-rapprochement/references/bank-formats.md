# Ingestion BANQUE — relevé → transactions normalisées

L'autre moitié du rapprochement. `main.py` traite tout seul les formats **structurés** ;
un relevé en **PDF/scan** part en extraction LLM (sidecar `.bank.json`), comme un ticket.

| Format | Extension | Traité par | Notes |
|--------|-----------|-----------|-------|
| CAMT.053 (ISO 20022) | `.xml` | `bank_parsers.py` | soldes OPBD/CLBD → gate de fiabilité |
| OFX / QFX | `.ofx` `.qfx` | `bank_parsers.py` | montants déjà signés |
| CSV | `.csv` `.tsv` | `bank_parsers.py` | délimiteur + colonnes auto-détectés |
| PDF / scan | `.pdf` `.jpg`… | **TOI (LLM)** | écrire un sidecar `.bank.json` |

## Schéma `normalized statement` (le sidecar à écrire pour un relevé PDF/scan)
```json
{
  "source": "llm_vision",
  "account_iban": "FR76...",          // si lisible
  "opening_balance": 1000.00,          // solde initial, si lisible
  "closing_balance": 880.00,           // solde final, si lisible
  "reconciled": true,                  // opening + Σ(transactions) == closing ? (sinon false)
  "transactions": [
    { "date": "2026-04-08",
      "amount": 1980.00,               // SIGNÉ : +crédit (entrée) / -débit (sortie)
      "label": "VIR CLIENT HOTEL ALBA ROSSA REF FV-2026-001",
      "invoice_ref": "FV-2026-001" }   // n° de facture cité dans le libellé, sinon null
  ]
}
```

### Règles de signe (cruciales)
- **Crédit** (argent qui ENTRE : virement reçu, encaissement) → montant **positif**.
- **Débit** (argent qui SORT : prélèvement, achat, frais) → montant **négatif**.
- Un libellé peut contenir un montant parasite (ex. « −88,48 EUR » = montant d'un
  prélèvement rejeté, PAS l'opération) — prends le montant de la COLONNE, pas du libellé.

### `reconciled` = gate de fiabilité
Si tu connais les soldes d'ouverture et de clôture, vérifie `opening + Σ amounts == closing`.
Si ça tombe juste → `reconciled: true` (relevé fiable). Sinon → `reconciled: false` : tu as
probablement un signe faux ou une ligne manquante ; corrige avant d'écrire le sidecar. Un
solde « SOLDE PRECEDENT » en colonne **Débit** signifie un compte débiteur → solde
d'ouverture **négatif**.

### Référence facture dans le libellé
Repère `REF <id>`, `FACT <id>`, `FACTURE: <id>`, ou un préfixe collé `FAC-2024-012`. Ne
prends PAS un mandat SEPA (RUM, ICS, BMS-…) pour une référence de facture. Mettre la bonne
`invoice_ref` rend le rapprochement quasi certain (passe 1 par référence).

### Forcer une catégorie non facturable
Le moteur reconnaît seul les opérations non facturables (salaire, impôt, frais, retrait…)
d'après le libellé. Si tu sais qu'une transaction l'est mais que le libellé est trop pauvre,
ajoute `"category"` à la transaction du sidecar (valeurs : `frais_bancaires`, `rh_charges`,
`prestations_sociales`, `impots_taxes`, `especes`, `transfert_interne`,
`virement_particulier`) — elle ira dans `excluded_bank_lines` sans risque de fausse anomalie.

## Pourquoi toute transaction compte
Le moteur garantit l'invariant : **chaque transaction est représentée exactement une fois** —
soit rapprochée à une facture, soit dans `unmatched_bank_lines` (débit sans facture →
`facture_manquante` ; crédit non identifié → `paiement_orphelin`), soit dans
`excluded_bank_lines` (non facturable). N'omets aucune ligne du relevé, débits inclus —
sinon l'invariant casse et la période finit en KO.
