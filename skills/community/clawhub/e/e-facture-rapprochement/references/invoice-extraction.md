# Ingestion FACTURES — cascade + extraction LLM (tier 3)

La cascade va de la confiance la plus haute (données structurées) à la plus variable
(photo de ticket). `main.py` fait les tiers 1-2 tout seul ; **le tier 3 est ton travail**
(toi, l'agent) : lire le document et écrire un sidecar JSON normalisé.

| Tier | Entrée | Traité par | Confiance |
|------|--------|-----------|-----------|
| 1 | Factur-X / ZUGFeRD (PDF/A-3 avec XML CII embarqué) | `invoice_parsers.py` (pdfdetach) | 1.0 |
| 2 | XML pur UBL (OASIS) ou CII (UN/CEFACT) | `invoice_parsers.py` | 1.0 |
| 3 | **PDF natif / scan / photo de ticket de caisse** | **TOI, par extraction LLM** | variable + score |

> Cas réel dominant : **des photos de tickets de caisse et des PDF**, pas du Factur-X.
> Le tier 3 est donc le chemin principal. Pas de regex sur le texte d'un ticket : tu LIS le
> document (texte si couche texte présente, sinon vision) et tu retournes les champs.

## Schéma `normalized invoice` (le sidecar à écrire)
Écris le JSON dans le chemin `sidecar` indiqué par la worklist (`<doc>.<ext>.invoice.json`,
à côté du document). `main.py` le relira au prochain run.

```json
{
  "invoice_id": "TIC-2026-0411",        // n° de facture / ticket ; sinon fabrique un id stable
  "type": "in",                          // "in" = achat (ce que le client A PAYÉ) ; "out" = vente
  "counterparty_name": "Brico Depot Ajaccio",
  "amount": 89.90,                       // TTC, nombre
  "total_ht": 74.92,                     // si lisible (sert au contrôle TVA)
  "tva_amount": 14.98,                   // TVA déclarée, si lisible
  "tva_rate_pct": 20,                    // taux, si lisible (sinon n'invente pas)
  "issued_date": "2026-04-11",           // date du ticket/facture (ISO)
  "due_date": "2026-04-11",              // échéance ; pour un ticket payé comptant = la date
  "currency": "EUR",
  "source": "llm_vision",                // "llm_vision" ou "llm_text"
  "confidence": 0.82                     // 0..1 : ta confiance HONNÊTE dans l'extraction
}
```

### Déterminer `type` (in/out) — important
- **Ticket de caisse / facture fournisseur reçue** = le client a ACHETÉ → `type: "in"`,
  la contrepartie est le commerçant/fournisseur.
- **Facture que le client a ÉMISE** (à son propre client) = VENTE → `type: "out"`,
  la contrepartie est le client destinataire.
- Indice : le client est-il l'émetteur (en-tête, SIREN du `company.json`) ou le destinataire ?
  Dans le doute pour une photo de ticket, c'est presque toujours un achat (`in`).

### `confidence` — sois honnête
La confiance pilote la **validation humaine**. Mets un score bas si : montant rogné/flou,
plusieurs totaux possibles, date ambiguë, contrepartie illisible. `main.py` signale pour
revue humaine toute facture dont `confidence < 0.75` **OU** `amount > 1000 €` (seuils
ajustables dans `normalize.py`). Ces factures restent dans la sortie — elles sont juste
listées dans `_review.json` pour qu'un humain confirme.

### Si le document est vraiment illisible
N'invente jamais de montant. Écris un sidecar minimal `{"source":"llm_vision","confidence":0.0}`
sans `invoice_id`/`amount` : `main.py` le classera en anomalie `facture_illisible` (et la
pièce sera à re-fournir), plutôt que de polluer le rapprochement avec des chiffres faux.

## Notes d'extraction par média
- **PDF avec couche texte** (`mode=text`) : `pdftotext -layout <doc> -` te donne le texte ;
  lis-le et extrais. Pas de regex fragile — comprends la mise en page.
- **Photo / scan** (`mode=vision`) : lis l'image directement (vision). Les tickets ont
  souvent le TTC en bas (« TOTAL », « MONTANT DU », « NET À PAYER »).
- **Factur-X non détecté** : si `pdfdetach` n'a rien sorti, le PDF n'a pas d'XML embarqué →
  c'est un tier 3 normal, extrais par lecture.
