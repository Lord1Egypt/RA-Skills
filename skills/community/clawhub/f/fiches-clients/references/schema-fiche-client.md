# Référence — Schéma de la fiche client

> Référence chargée à la demande par le skill `fiches-clients`. Schéma JSON complet de `clients.json` et conventions de validation.

---

## Localisation

Fichier unique : `~/.openclaw/workspace/clients.json`.

Structure :

```jsonc
{
  "version": "1.0",
  "clients": [
    { /* fiche client 1 */ },
    { /* fiche client 2 */ }
  ]
}
```

L'ordre dans le tableau n'a pas de sens métier — la clé de lookup est `slug`.

---

## Schéma d'une fiche

```jsonc
{
  // Identification
  "slug": "acme-sa",                            // obligatoire, unique, kebab-case
  "raisonSociale": "ACME SA",                   // obligatoire, lisible
  "formeJuridique": "SAS",                      // optionnel — SAS | SASU | SARL | EURL | SA | EI | SCI | Association | Autre
  "siren": "380129866",                         // optionnel mais unique si présent (9 chiffres)
  "siret": "38012986600015",                    // optionnel (14 chiffres, doit commencer par siren)
  "tvaIntra": "FR38380129866",                  // optionnel — clé mod 97
  "naf": "6201Z",                               // optionnel — code APE/NAF

  // Lifecycle
  "statut": "active",                           // active | draft-auto-created | draft-user-created | archived | suspended
  "source": "user",                             // user | auto (qui a déclenché la création)
  "aValider": false,                            // true si la fiche est en draft et attend validation
  "confiance": 1.0,                             // 0.0–1.0 — qualité des signaux d'identification (1.0 si user, dégradée si auto)
  "dateCreationFiche": "2026-05-27T14:23:11Z",  // ISO 8601 UTC
  "auteurCreation": "user",                     // user | organisation-documents | <autre-skill>
  "dateValidation": null,                       // ISO 8601 UTC, peuplé au passage active
  "auteurValidation": null,                     // user | <skill>
  "dateArchivage": null,                        // ISO 8601 UTC, peuplé si statut = archived
  "purgeNonPasseAvant": null,                   // ISO 8601 UTC = dateArchivage + 30j

  // Contacts & domaines (utilisés par la cascade d'identification de organisation-documents)
  "domains": ["acme.fr", "acme-corp.com"],      // domaines e-mail rattachés à ce client
  "contacts": [
    {
      "nom": "Marie Dupont",
      "role": "Directrice financière",          // libre — DAF, Gérant, Comptable interne, etc.
      "email": "marie.dupont@acme.fr",          // unique parmi tous les contacts de tous les clients (pour cascade)
      "telephone": "+33612345678",              // optionnel, format libre
      "principal": true                         // un seul contact principal par client
    }
  ],

  // Adresse
  "adresse": {
    "ligne1": "12 rue de la Paix",
    "ligne2": null,
    "codePostal": "75002",
    "ville": "Paris",
    "pays": "FR"                                // ISO 3166-1 alpha-2
  },

  // Paramètres comptables (résumé — détail complet dans clients/<slug>/company.json)
  "exerciceCloture": "12-31",                   // MM-JJ de clôture, défaut 12-31
  "regimeTVA": "reel-normal",                   // franchise | reel-simplifie | reel-normal | mini-reel
  "ibanFavori": null,                           // IBAN principal du client (mod 97 OK si présent)

  // Métadonnées techniques (jamais affichées au comptable)
  "id": "uuid-v4-de-la-fiche",                  // UUID stable, immuable même en cas de rename
  "schemaVersion": 1                            // pour migrations futures
}
```

---

## Énumérations

### `statut`

| Valeur                 | Sens                                                                                            | Transitions autorisées                            |
| ---------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `draft-auto-created`   | Créé par `organisation-documents` en auto-création. Attend validation.                          | → `active` (validate-draft), → ∅ (reject-draft)   |
| `draft-user-created`   | Créé par `clients` sur demande user mais marqué incomplet (signaux insuffisants par ex.).        | → `active` (update + validation), → `archived`    |
| `active`               | Fiche validée, traitement normal.                                                               | → `archived`, → `suspended`                       |
| `suspended`            | Client temporairement inactif (ex : a quitté le cabinet) mais on conserve les pièces classées.   | → `active`, → `archived`                          |
| `archived`             | Soft-delete RGPD. Dossier déplacé vers `_archive-suppression/`. Grâce 30 j avant purge possible. | → `active` (restauration manuelle dans la grâce)  |

### `formeJuridique`

`SAS` | `SASU` | `SARL` | `EURL` | `SA` | `SCA` | `SNC` | `SCI` | `SCM` | `SCP` | `EI` | `Micro-entreprise` | `Association` | `Autre`

### `source` / `auteurCreation`

- `source` : `user` | `auto`
- `auteurCreation` : `user` | `organisation-documents` | `<futur-skill>` (libre, mais doit pointer un skill réel)

### `regimeTVA`

`franchise` | `reel-simplifie` | `reel-normal` | `mini-reel`

---

## Contraintes d'unicité

| Champ          | Unicité                                                                |
| -------------- | ---------------------------------------------------------------------- |
| `slug`         | Unique dans `clients.json`                                             |
| `id`           | Unique (UUID v4)                                                       |
| `siren`        | Unique si présent (pas de doublon SIREN entre deux fiches actives)     |
| `siret`        | Unique si présent                                                      |
| `contacts[].email` | Unique sur l'ensemble des contacts de tous les clients (cascade d'identification de `organisation-documents` repose sur ça) |
| `domains[]`    | Un domaine appartient à un seul client. Domaines génériques (`gmail.com`, `outlook.com`, `yahoo.fr`) interdits dans la liste — ils ne sont pas exploitables comme signal |

Si une opération viole une contrainte d'unicité → escalader à l'utilisateur (proposer `merge` ou suffixe).

---

## Champs obligatoires à la création

| Source | Minimum requis                                  |
| ------ | ----------------------------------------------- |
| `user` | `slug` + `raisonSociale`                        |
| `auto` | `slug` + `raisonSociale` + au moins un signal exploitable (`domains[0]` OU `siren` OU `contacts[0].email`) |

Tous les autres champs peuvent être ajoutés en `update` ultérieur.

---

## Validation des champs

| Champ          | Règle de validation                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| `slug`         | `^[a-z0-9]+(-[a-z0-9]+)*$`, longueur 1–64                                                            |
| `siren`        | 9 chiffres, validation Luhn FR (algo SIREN)                                                          |
| `siret`        | 14 chiffres, commence par `siren`, validation Luhn FR                                                |
| `tvaIntra`     | Format `^[A-Z]{2}[0-9A-Z]{2,12}$`, clé mod 97 pour `FR`                                              |
| `ibanFavori`   | Validation mod 97                                                                                    |
| `codePostal`   | 5 chiffres pour `pays = FR`, libre sinon                                                             |
| `email` (contacts) | Format RFC 5322 simplifié, domaine non générique interdit dans `domains[]` mais autorisé pour un contact |

Échec de validation → ne pas écrire et rapporter l'erreur en termes métier (« Le SIREN saisi n'est pas valide »).

---

## Évolutions futures

- `schemaVersion: 2` réservé pour ajout de `representantLegal`, `actionnariat`, `comptesAnnuels`.
- Migration : skill `fiches-clients` doit gérer la lecture des deux versions et migrer en lazy à la prochaine écriture.
