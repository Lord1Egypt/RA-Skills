# Moteur de rapprochement — règles (implémentées dans `reconcile.py`)

Tu n'as pas à réimplémenter ceci : `reconcile.py` le fait. Cette page explique le **pourquoi**,
pour interpréter les résultats et régler les seuils (`normalize.py`).

## Sens (jamais ignoré)
- Facture `out` (vente) → encaissée par un **CRÉDIT** (montant positif).
- Facture `in` (achat) → réglée par un **DÉBIT** (montant négatif).
Une transaction du mauvais sens n'est jamais candidate.

## Score d'appariement
`score = 0.5·montant + 0.3·libellé + 0.2·date`, où :
- **montant** : 1.0 si égal à la tolérance près (`±1 €` ou `±1 %`), sinon dégressif.
- **libellé** : similarité de noms (contrepartie ↔ libellé bancaire), indépendante de
  l'ordre/casse.
- **date** : 1.0 si même jour, dégressif jusqu'à 0 à `±15 j` (fenêtre `DATE_WINDOW_DAYS`).

**Garde-fou : le montant ne décide JAMAIS seul.** Il faut un appui libellé OU date — sinon
deux factures du même montant deviendraient interchangeables. Match accepté si `score ≥ 0.62`.
Si deux candidats sont à moins de `0.08` d'écart → on départage par la date ; si toujours
indistinct → **ambigu, on n'écrit rien** (la facture reste en attente) plutôt que de risquer
un faux rapprochement.

## Passes
1. **Référence** : transaction dont le libellé/`invoice_ref` cite l'`invoice_id`. Le plus
   fiable. Gère l'**acompte + solde** (plusieurs transactions réf → on somme).
2. **Fuzzy 1↔1** : meilleur score. Cas **acompte/partiel** : si la contrepartie est
   franchement reconnue (≥0.7), la date proche, et le montant ≤ facture, on accepte même si
   le montant est nettement inférieur (→ `partial`).
3. **Paiement groupé** : une transaction solde plusieurs factures de même contrepartie/sens
   dont la somme = le montant (chaque transaction n'est consommée qu'une fois).

Chaque transaction est **consommée** au plus une fois (un virement ne solde pas deux factures
par erreur).

## Statuts résultants
- montant payé = montant facture (tol.) → `paid`.
- payé < facture → `partial` (`amount_paid` + `amount_remaining`).
- payé > facture → `paid` + `overpaid_by`.
- non rapprochée + échéance dépassée (vs `--today`) → `overdue`.
- non rapprochée + non échue → `unpaid`.

## Transactions non rapprochées (§5)
D'abord, les opérations **non facturables** sont écartées (voir ci-dessous) ; elles ne sont
ni candidates au matching ni des anomalies. Pour le reste :
- **débit** (sortant) sans facture → `facture_manquante` (montant négatif).
- **crédit** (entrant) non identifié → `paiement_orphelin` (montant positif).

## Opérations NON FACTURABLES → `excluded_bank_lines`
`classify_non_billable` (dans `normalize.py`) reconnaît 7 familles sur le libellé :
`frais_bancaires`, `rh_charges` (salaires), `prestations_sociales` (URSSAF/CPAM/retraite…),
`impots_taxes` (DGFIP/TVA/CFE…), `especes` (retraits/dépôts d'espèces), `transfert_interne`
(compte à compte/épargne), `virement_particulier`. Ces lignes :
- ne sont **jamais** rapprochées à une facture (exclues du pool de matching) ;
- ne deviennent **jamais** `facture_manquante`/`paiement_orphelin` (sinon flot de faux positifs) ;
- sortent dans `excluded_bank_lines` avec leur `category`, et **comptent dans l'invariant**
  (3ᵉ terme).

La détection est volontairement **conservatrice** (mieux vaut laisser passer une vraie
dépense que d'exclure à tort un paiement client). `virement_particulier` n'est pas
auto-détecté ; pour forcer une catégorie, pose `"category"` sur la transaction dans le
sidecar de relevé. Les listes de mots-clés sont éditables en tête de `normalize.py`.

## Anomalies factures
- `tva_incorrecte` : si `total_ht`, `tva_amount`, `tva_rate_pct` connus et
  `|TVA déclarée − HT·taux| / (HT·taux) > 5 %`. Neutralisée si le taux est inconnu
  (on ne juge pas une TVA qu'on ne peut pas recalculer).
- `invoice_overdue` : facture `overdue`, avec `days_late`.

## Relances (ancienneté du retard)
`≤30 j → 1`, `≤60 j → 2`, `≤90 j → 3`, `>90 j → "escalation"`. Pour un `partial`, la note
rappelle le solde restant dû.
