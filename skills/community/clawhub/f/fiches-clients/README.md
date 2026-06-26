# fiches-clients

> Claude skill for **French accounting firms** (`cabinets comptables`). Owns the full lifecycle of client records (`clients.json` and the per-client folder `clients/<slug>/`): create, validate drafts, update, rename, merge, archive.

## What it does

Triggered whenever the accountant performs an action **on a client record as an entity** (not on a document). Companion to `organisation-documents` which acts on incoming documents.

| Verb (FR / EN)                                                  | Procedure         |
| --------------------------------------------------------------- | ----------------- |
| "crée un client", "ajoute le client", "nouveau client X"        | `create`          |
| "valide la fiche draft de Foo"                                  | `validate-draft`  |
| "rejette cette fiche draft"                                     | `reject-draft`    |
| "ajoute le SIREN / e-mail / IBAN à `acme`"                      | `update`          |
| "renomme `foo-corp` en `foo-sa`"                                | `rename`          |
| "fusionne `acme` et `acme-sa`"                                  | `merge`           |
| "archive le client `foo`" (RGPD soft-delete, 30-day grace)      | `archive`         |
| "liste les clients", "cherche `foo`"                            | `list` / `find`   |

## Why it exists

`organisation-documents` auto-creates client records **in reflex** when an incoming attachment has an exploitable signal (domain / SIREN / readable raison sociale) — those drafts land as `statut: "draft-auto-created"`. But explicit user-driven CRUD on client records had no owner: this skill closes that gap and is the single writer of `clients.json` for everything except auto-creation.

See [`references/cohabitation.md`](references/cohabitation.md) for the exact boundary with `organisation-documents`.

## Output

```
~/.openclaw/workspace/
├── clients.json                            # owned by this skill (registry of all clients)
└── clients/
    └── <slug>/
        ├── audit.log                       # owned by this skill (mutations on the record)
        ├── index.json                      # owned by organisation-documents (list of classified docs)
        ├── company.json                    # owned by this skill, lazy-created on update (legal info)
        └── <AAAA>/<MM>/…                   # owned by organisation-documents (classified documents)
```

## Why French

Embeds French regulatory vocabulary (SIREN, SIRET, TVA intra, forme juridique, NAF, RGPD soft-delete). `SKILL.md` and `references/*.md` are in French; only this README and the frontmatter `description` are in English to fit the clawhub directory.

## Companion skills

- [`organisation-documents`](../organisation-documents/) — document pipeline; can auto-create drafts that this skill validates.
- [`rapprochement-bancaire`](../rapprochement-bancaire/) — bank reconciliation; reads `clients.json` for client metadata.
- `relances` *(planned)*, `facturation` *(planned)* — outgoing flows; read `clients.json`, write `relances.md` / `followup.md`.

All skills share the path/naming contract defined in [`../organisation-documents/references/structure-cible.md`](../organisation-documents/references/structure-cible.md).

## Files

| File                                       | Purpose                                                              |
| ------------------------------------------ | -------------------------------------------------------------------- |
| `SKILL.md`                                 | Main skill definition (French)                                       |
| `references/schema-fiche-client.md`        | Full JSON schema of `clients.json` entries, enums, constraints       |
| `references/cohabitation.md`               | Exact boundary with `organisation-documents`, state transitions      |
| `data/fiche-client.example.json`           | Example record (minimal + full)                                      |

## License

Internal — OpenClaw private use.
