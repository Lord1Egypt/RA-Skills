# Référence — Cohabitation avec `organisation-documents`

> Référence chargée à la demande. Définit la frontière exacte entre le skill `fiches-clients` et `organisation-documents`, et les règles de transition de statut des fiches.

---

## Principe

`organisation-documents` est un **moteur de pipeline** déclenché par l'arrivée d'un document. `clients` est un **moteur d'état** sur les fiches client. Les deux sont nécessaires : aucune fiche n'existerait sans `organisation-documents` (auto-création) ou sans `clients` (création explicite), et aucun document ne se classe sans `organisation-documents`.

**Règle frontière** :

> Si l'action est déclenchée par l'**arrivée d'un document** → `organisation-documents`.
> Si l'action est déclenchée par une **commande utilisateur sur une fiche** → `clients`.

---

## Cas concrets

### Cas 1 — Facture entrante d'un nouveau client

1. `organisation-documents` reçoit la PJ.
2. Cascade d'identification → aucun match.
3. Signal exploitable existant (domaine pro / SIREN extrait / raison sociale lisible) → **auto-création**.
4. `organisation-documents` écrit directement dans `clients.json` une entrée `statut: "draft-auto-created"`.
5. Le document est classé normalement sous `clients/<nouveau-slug>/<AAAA>/<MM>/…`.
6. Rapport batch en fin de traitement : « Nouveau client en cours de validation : **ACME SA**. »

**Le skill `fiches-clients` n'est pas invoqué dans ce flux.** L'écriture dans `clients.json` par `organisation-documents` est une exception explicitement autorisée (cf. § Exception ci-dessous).

### Cas 2 — Utilisateur valide le draft

Suite au Cas 1, l'utilisateur dit : « OK valide la fiche ACME ».

1. `clients` est invoqué (verbe explicite sur une fiche).
2. Procédure `validate-draft` : `statut: "draft-auto-created"` → `active`.
3. Rapport : `✅ Fiche **ACME SA** validée.`

### Cas 3 — Utilisateur crée explicitement un client sans aucun document

Utilisateur dit : « Crée moi un nouveau client : ACME SA, SIREN 380129866, contact marie@acme.fr ».

1. `clients` est invoqué (verbe explicite).
2. Procédure `create` avec `source: "user"`, `statut: "active"` (pas de draft puisque l'utilisateur a fourni les infos).
3. Création du dossier `clients/acme-sa/` (vide à part `audit.log` et `index.json`).
4. Rapport : `✅ Client **ACME SA** créé.`

**`organisation-documents` n'est pas invoqué** — il n'y a pas de document à classer.

### Cas 4 — Document non attribuable, escalade utilisateur

1. `organisation-documents` reçoit une PJ.
2. Cascade échoue (expéditeur générique, pas de SIREN, raison sociale illisible).
3. Document mis en `.pending-attribution/` avec entrée dans `pending-attribution.json`.
4. Fin de batch : `organisation-documents` demande « À quel client rattacher cette pièce ? »

Réponse utilisateur possible :

- **« Rattache-la à `acme-sa` »** → `organisation-documents` déplace le fichier vers `clients/acme-sa/<AAAA>/<MM>/…` et purge l'entrée pending. `clients` non invoqué (fiche existe déjà).
- **« Crée un nouveau client `Beta Corp` et rattache-la »** → `clients` invoqué d'abord (procédure `create`), puis `organisation-documents` reprend pour classer la pièce.

### Cas 5 — Doublon de fiche détecté

Suite à plusieurs auto-créations, l'utilisateur remarque deux fiches `acme` et `acme-sa` pour le même client.

1. Utilisateur dit : « Fusionne `acme` dans `acme-sa` ».
2. `clients` est invoqué — procédure `merge`.
3. Tous les documents du dossier `clients/acme/` sont déplacés vers `clients/acme-sa/`.
4. L'entrée `acme` est supprimée de `clients.json`.
5. `index-global.json` est mis à jour.

**`organisation-documents` n'est pas invoqué pendant la fusion**, mais `clients` doit respecter la convention de chemin définie par `organisation-documents/references/structure-cible.md` (les sous-dossiers `<AAAA>/<MM>/…` doivent rester intacts pendant le déplacement).

### Cas 6 — Reclassement d'un document mal attribué

Utilisateur dit : « Cette facture est mal classée, elle appartient à `foo-sa` pas à `bar-corp` ».

1. **`organisation-documents`** est invoqué (l'action porte sur une **pièce**, pas une fiche).
2. Étape 4 du SKILL.md `organisation-documents` : « Reclassement : correction client/nature → propage le déplacement et met à jour l'index. »

**`clients` n'est pas invoqué** — les deux fiches existent déjà.

---

## Exception : `organisation-documents` écrit dans `clients.json`

`clients` est normalement le seul à écrire dans `clients.json`. Mais `organisation-documents` est autorisé à écrire **uniquement** pour les opérations suivantes :

| Opération                       | Permission                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| Auto-création en draft          | ✅ Autorisé (cf. SKILL.md `organisation-documents` § Étape 2 — Auto-création)        |
| Mise à jour des signaux (ex : enrichir `domains[]` quand un nouveau domaine est observé pour un client existant) | ✅ Autorisé, mais limité à `domains` et `contacts` |
| Passage `draft-auto-created` → `active` | ❌ Interdit. Doit passer par `clients` (procédure `validate-draft`).         |
| Modification de SIREN / raison sociale / forme juridique | ❌ Interdit.                                              |
| Suppression / archivage         | ❌ Interdit.                                                                         |

L'auto-création par `organisation-documents` doit toujours déposer la fiche en `statut: "draft-auto-created"`, jamais directement en `active`. C'est la procédure `validate-draft` de `clients` qui contrôle la transition.

---

## Synchronisation des audit logs

Chaque skill maintient son propre log :

| Fichier                                | Maintenu par                  | Contenu                                                          |
| -------------------------------------- | ----------------------------- | ---------------------------------------------------------------- |
| `clients/<slug>/audit.log`             | `clients` (et `organisation-documents` pour `auto-create` initial) | Mutations sur la fiche (create, update, rename, merge, archive, validate, reject) |
| `clients/<slug>/index.json`            | `organisation-documents`      | Liste des documents classés (un objet par pièce)                 |
| `index-global.json`                    | `organisation-documents`      | Index plat tous clients confondus pour dédup hash globale        |
| `pending-attribution.json`             | `organisation-documents`      | Documents en attente de rattachement                             |
| `clients.json`                         | **`clients`** (exception : auto-create par `organisation-documents`) | Annuaire des fiches |

**Pas de chevauchement** : si `clients` doit s'assurer qu'une mutation est cohérente avec les index gérés par `organisation-documents` (cas `rename` et `merge`), il met à jour ces fichiers en respectant leur schéma défini dans `organisation-documents/references/contrat-io.md`. Toute autre interaction passe par invocation explicite de `organisation-documents`.

---

## Règles de transition de statut

```
              (organisation-documents)              (clients.validate-draft)
   ∅ ────────────────────────────────────► draft-auto-created ───────────────► active
                                                  │
                                                  │  (clients.reject-draft)
                                                  └──────────────────────────► ∅

       (clients.create avec signaux complets)
   ∅ ──────────────────────────────────────────────────────────────────────► active

       (clients.create avec signaux incomplets)        (clients.update + validation)
   ∅ ────────────────────────────────────► draft-user-created ──────────────► active

                                          (clients.archive)        (clients.restore, manuel)
   active ──────────────────────────────────────────► archived ────────────► active (si < 30j)

       (clients.suspend)                  (clients.activate)
   active ──────────────────────► suspended ───────────────────► active
```

**Invariant** : aucune transition ne peut être déclenchée par un autre skill que `clients` (sauf création initiale en `draft-auto-created` par `organisation-documents`).
