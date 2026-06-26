---
name: fiches-clients
description: Skill propriétaire de la gestion des fiches clients du cabinet (lifecycle complet du dossier `clients/<slug>/` et de l'entrée `clients.json`). INVOKE SYSTEMATICALLY AND WITHOUT ASKING FOR PERMISSION whenever the user (a) demande de créer / ajouter / enregistrer un nouveau client ("crée un client", "crée moi un nouveau client X", "ajoute le client X", "nouveau client", "create a client", "register client X"), (b) demande de renommer, fusionner, archiver, suspendre ou supprimer un client, (c) demande de mettre à jour des infos client (SIREN, SIRET, raison sociale, e-mail, domaine, téléphone, adresse, IBAN, conditions de paiement, forme juridique, TVA intra), (d) demande de valider, compléter ou rejeter une fiche `draft-auto-created` produite par `organisation-documents`, (e) demande de lister, chercher, afficher ou exporter les clients. Owns `~/.openclaw/workspace/clients.json` and `~/.openclaw/workspace/clients/<slug>/{audit.log, index.json, company.json}`. Si l'utilisateur dit « crée moi un client Foo », ce skill est le seul à invoquer — pas `organisation-documents`.
license: Interne — usage privé OpenClaw
---

# Skill `fiches-clients`

> Skill maison du domaine comptable. Propriétaire unique des **fiches clients** (raison sociale, SIREN, contacts, domaines, statut) et du dossier physique `clients/<slug>/`.
> Détails techniques dans `references/` (chargés à la demande).

---

## Pourquoi ce skill existe

`organisation-documents` crée des fiches clients **en réflexe** quand une PJ entrante a un signal exploitable (auto-création silencieuse en `draft-auto-created`). C'est très bien pour le pipeline automatique, mais ça ne couvre **pas** :

1. Les demandes utilisateur explicites (« crée moi un client ACME », « renomme `foo-corp` en `foo-sa` », « fusionne ces deux fiches doublonnées »).
2. La **validation des drafts** auto-créés (passage de `draft-auto-created` → `active`).
3. Les mises à jour de fiche (ajout de SIREN après lookup INSEE, ajout d'un domaine secondaire, correction d'adresse).
4. Les opérations RGPD (archivage soft-delete, purge après grâce 30 j).

Ce skill est le **seul à écrire** dans `clients.json` et à créer/déplacer/archiver des dossiers `clients/<slug>/`. Tous les autres skills (`organisation-documents`, `rapprochement-bancaire`, `relances`, `facturation`) peuvent **lire** ces fichiers mais doivent passer par ce skill pour toute mutation au niveau fiche.

**Exception unique** : `organisation-documents` est autorisé à appeler ce skill (ou à exécuter sa procédure `create`) pour créer un draft auto. Voir [`references/cohabitation.md`](references/cohabitation.md).

---

## Quand utiliser ce skill

**Règle d'or** : dès que l'utilisateur prononce un verbe qui agit sur une **fiche client en tant qu'entité** (pas un document), c'est ce skill. Si le doute existe entre `fiches-clients` et `organisation-documents` : `organisation-documents` traite des **pièces** (factures, relevés…), `clients` traite des **fiches** (entités juridiques).

Déclencheurs explicites :

| Verbe utilisateur                                                     | Action                                            |
| --------------------------------------------------------------------- | ------------------------------------------------- |
| « crée un client », « ajoute le client », « nouveau client X »        | `create`                                          |
| « renomme `acme` en `acme-sa` »                                       | `rename`                                          |
| « fusionne `acme` et `acme-sa` »                                      | `merge`                                           |
| « archive le client », « supprime le client » (RGPD)                  | `archive` (soft-delete)                           |
| « valide la fiche de Foo », « confirme la fiche draft »               | `validate-draft`                                  |
| « rejette / ignore cette fiche draft »                                | `reject-draft`                                    |
| « ajoute le SIREN / SIRET / e-mail / domaine / IBAN à `acme` »        | `update`                                          |
| « liste les clients », « combien de clients », « cherche le client `foo` » | `list` / `find`                              |

Déclencheurs implicites :

- Après que `organisation-documents` a logué un `draft-auto-created` dans son rapport, si l'utilisateur répond « OK valide » ou « non c'est pas ce client » → `validate-draft` ou `reject-draft`.
- Si une pièce dans `.pending-attribution/` reçoit une réponse utilisateur « crée le client `nouveau-client` » → `create` (puis `organisation-documents` peut classer la pièce).

**Ne pas utiliser** pour : classer un document (→ `organisation-documents`), modifier `index.json` ou `audit.log` ailleurs que pour la création d'une fiche (chaque skill maintient ses propres logs métier), envoyer une relance (→ `relances`).

---

## Mode d'exécution

### Inline only

Toutes les opérations de ce skill sont **inline**. Pas de subagent, pas de TaskFlow. Une création de fiche prend < 5 s, une fusion < 10 s. Aucune raison de déléguer.

### Time budget

- `create` / `update` / `validate-draft` / `reject-draft` : ≤ 5 s.
- `rename` / `archive` : ≤ 10 s (renommage de dossier + propagation index).
- `merge` : ≤ 20 s (re-indexation des deux clients fusionnés).
- `list` / `find` : ≤ 2 s.

### Communication

Une ligne avant, une ligne après. Style **comptable**, pas développeur : « Client ACME SA créé » et non « Entry inserted into clients.json with slug acme-sa ». Voir section [Communication avec le comptable](#communication-avec-le-comptable).

---

## Procédures

### Procédure `create` — créer une fiche client

**Quand** : verbe utilisateur explicite (`crée`, `ajoute`, `nouveau client`) OU invocation par `organisation-documents` en auto-création.

**Étapes** :

1. **Identifier la source** : `user` (commande explicite) ou `auto` (organisation-documents). Affecte le statut initial.
2. **Extraire les signaux** depuis la commande utilisateur ou le contexte appelant :
   - Raison sociale obligatoire (au minimum un texte lisible).
   - Optionnels : SIREN, SIRET, forme juridique, e-mail de contact, domaine, téléphone, adresse, IBAN.
3. **Dériver le slug** (cf. [Slug et nommage](#slug-et-nommage)).
4. **Vérifier l'unicité** :
   - Le slug n'existe pas déjà dans `clients.json`. Sinon → demander à l'utilisateur s'il s'agit du même client (proposer `merge`) ou suggérer un suffixe (`acme-sa-2`).
   - Si SIREN fourni : aucun autre client n'a le même SIREN. Sinon → proposer `merge` ou erreur.
5. **Créer le dossier physique** :

   ```
   ~/.openclaw/workspace/clients/<slug>/
   ├── audit.log           # fichier vide créé immédiatement
   └── index.json          # { "documents": [] }
   ```

   **Pas** de sous-dossiers `<AAAA>/<MM>/…` à ce stade — ils sont créés à la demande par `organisation-documents` quand un document arrive. Pas de `company.json` non plus tant que l'utilisateur n'a pas fourni d'infos juridiques (créé en lazy par `update` ou par le skill `facturation`).

6. **Ajouter l'entrée dans `clients.json`** : voir le schéma complet dans [`references/schema-fiche-client.md`](references/schema-fiche-client.md). Champs minimums :

   ```jsonc
   {
     "slug": "acme-sa",
     "raisonSociale": "ACME SA",
     "statut": "active",          // ou "draft-auto-created" si source = auto
     "source": "user",            // ou "auto"
     "aValider": false,           // true si source = auto
     "confiance": 1.0,            // 1.0 si user, dégradée si auto
     "domains": [],
     "contacts": [],
     "siren": null,
     "siret": null,
     "formeJuridique": null,
     "adresse": null,
     "dateCreationFiche": "2026-05-27T14:23:11Z",
     "auteurCreation": "user"     // ou "organisation-documents"
   }
   ```

7. **Loguer la création** dans `clients/<slug>/audit.log` :

   ```
   2026-05-27T14:23:11Z create source=user actor=user slug=acme-sa raisonSociale="ACME SA"
   ```

8. **Rapporter** à l'utilisateur. Format : `✅ Client **<raisonSociale>** créé.` + une ligne si signaux manquants (« pense à compléter le SIREN »).

### Procédure `validate-draft` — confirmer une fiche `draft-auto-created`

**Quand** : utilisateur confirme un draft. Souvent juste après un rapport `organisation-documents` qui a auto-créé.

**Étapes** :

1. Charger l'entrée `clients.json` correspondante.
2. Vérifier que `statut === "draft-auto-created"` (sinon erreur : déjà active).
3. Mettre à jour : `statut: "active"`, `aValider: false`, `confiance: 1.0`, `dateValidation: <now>`, `auteurValidation: "user"`.
4. Loguer dans `audit.log` : `validate-draft actor=user slug=<slug>`.
5. Rapporter : `✅ Fiche **<raisonSociale>** validée.`

### Procédure `reject-draft` — rejeter une fiche `draft-auto-created`

**Quand** : utilisateur dit « non c'est pas un client », « ignore cette fiche ».

**Étapes** :

1. Vérifier qu'aucun document n'est déjà classé sous `clients/<slug>/` :
   - Si `clients/<slug>/index.json` contient des documents → **escalader** : « Cette fiche a déjà N documents classés, je dois savoir où les rattacher avant de supprimer. »
   - Si vide → continuer.
2. Supprimer le dossier `clients/<slug>/` (le draft n'a jamais été utilisé, on peut purger sans soft-delete).
3. Retirer l'entrée de `clients.json`.
4. Loguer (dans un audit log global du workspace, pas dans le dossier supprimé) : `reject-draft actor=user slug=<slug>`.
5. Rapporter : `✅ Fiche **<raisonSociale>** rejetée.`

### Procédure `update` — mettre à jour des champs

**Quand** : verbe utilisateur ciblé (« ajoute le SIREN », « change l'adresse », « ajoute un domaine »).

**Étapes** :

1. Charger l'entrée `clients.json`.
2. Appliquer les modifications **uniquement** sur les champs cités. Ne pas toucher au reste.
3. Si modification de `siren` : vérifier l'unicité (aucun autre client n'a ce SIREN). Optionnel : lookup INSEE via `scripts/fetch_company.py` de `organisation-documents` pour confirmer la raison sociale.
4. Si ajout d'un `domain` : vérifier qu'aucun autre client n'a ce domaine (sinon escalader).
5. Si ajout de champs juridiques (SIREN, SIRET, forme, capital, IBAN) → **créer ou mettre à jour** `clients/<slug>/company.json` (cf. schéma dans `organisation-documents/data/company.example.json`).
6. Loguer chaque champ modifié dans `audit.log` : `update field=siren old=null new=123456789 actor=user`.
7. Rapporter : `✅ Fiche **<raisonSociale>** mise à jour (SIREN ajouté).`

### Procédure `rename` — renommer un client (slug ou raison sociale)

**Quand** : « renomme `foo-corp` en `foo-sa` », « la raison sociale est en fait ACME SAS pas ACME SA ».

**Cas 1 — Renommage raison sociale uniquement** (slug inchangé) :

1. Mettre à jour `raisonSociale` dans `clients.json`.
2. Loguer.
3. Rapporter.

**Cas 2 — Renommage slug** (impacte le dossier physique) :

1. Vérifier que le nouveau slug n'existe pas déjà.
2. **Renommer le dossier** : `clients/<old-slug>/` → `clients/<new-slug>/`.
3. Mettre à jour `clients.json` : `slug` et tous les `cheminDrive` / `cheminLocal` dans les entrées d'index liées (cf. § Propagation ci-dessous).
4. Mettre à jour `index-global.json` : tous les `cheminDrive` qui commencent par `clients/<old-slug>/` → `clients/<new-slug>/`.
5. Loguer dans le nouveau `audit.log` : `rename old-slug=<old> new-slug=<new> actor=user`.
6. Rapporter : `✅ Client renommé : <old> → <new>.`

### Procédure `merge` — fusionner deux fiches doublonnées

**Quand** : « fusionne `acme` et `acme-sa` » (souvent après une auto-création doublonnée).

**Convention** : l'utilisateur indique la fiche **cible** (celle qui survit) et la fiche **source** (celle qui est absorbée). Par défaut, la fiche `active` est cible et la `draft-auto-created` est source. Si les deux sont actives, demander.

**Étapes** :

1. Vérifier que les deux fiches existent.
2. **Fusionner les champs** : pour chaque champ, garder la valeur de la cible si présente, sinon prendre celle de la source. Conserver l'union pour les listes (`domains`, `contacts`).
3. **Déplacer tous les documents** de `clients/<source>/` vers `clients/<cible>/` en préservant l'arborescence `<AAAA>/<MM>/…`. Conflits de nom (deux fichiers même chemin) → suffixer le second `_2`.
4. **Concaténer les index** : `clients/<cible>/index.json` reçoit les entrées de la source (avec `cheminDrive` mis à jour).
5. **Mettre à jour `index-global.json`** : tous les `clientId` = source → cible, tous les chemins recalculés.
6. **Supprimer** le dossier source et retirer son entrée de `clients.json`.
7. Loguer dans `clients/<cible>/audit.log` : `merge source=<source-slug> docs-moved=<N> actor=user`.
8. Rapporter : `✅ Fusion **<source> → <cible>** : N pièces réattachées.`

### Procédure `archive` — archiver une fiche (RGPD soft-delete)

**Quand** : « archive le client `foo` », « supprime le client `foo` » (jamais de hard-delete via cette voie ; la suppression hard est manuelle après les 30 j de grâce).

**Étapes** :

1. Mettre `statut: "archived"`, `dateArchivage: <now>`, `purgeNonPasseAvant: <now + 30j>` dans `clients.json`.
2. **Déplacer** le dossier `clients/<slug>/` → `clients/<slug>/_archive-suppression/` (soft-delete avec grâce 30 j, comme spécifié dans `organisation-documents/SKILL.md` § Garde-fous).
3. Loguer : `archive actor=user grace-until=<date>`.
4. Rapporter : `✅ Client **<raisonSociale>** archivé. Restauration possible jusqu'au <date>.`

**Pas de hard-delete automatique.** La purge effective après 30 j est un processus séparé (ops manuel ou cron skill futur), pas dans ce skill.

### Procédure `list` / `find`

**Quand** : « liste les clients », « cherche `foo` ».

**Étapes** :

1. Lire `clients.json`.
2. Filtrer (selon prompt) par slug / raison sociale / SIREN / statut.
3. Rapporter en tableau lisible (cf. [Communication](#communication-avec-le-comptable)).

---

## Slug et nommage

**Référence canonique** : [`organisation-documents/references/structure-cible.md`](../organisation-documents/references/structure-cible.md) § "Slug client". Ce skill **applique exactement la même convention** — il ne définit pas un nouveau standard :

- lowercase
- accents retirés (`é` → `e`, `ç` → `c`)
- espaces → `-`
- non-alphanumérique → `-`
- pas de `-` consécutifs, pas de `-` en début/fin
- préférer le **domaine** quand disponible (`trendex.tech` → `trendex-tech`), sinon raison sociale slugifiée (`ACME SA` → `acme-sa`)

**Pas de slug réservé**. Aucun dossier `_cabinet`, `_non-attribue`, `_temp` ne doit être créé via ce skill. Le parking technique `.pending-attribution/` vit hors `clients/` et n'est pas géré par ce skill (il appartient à `organisation-documents`).

**Collision** : si le slug dérivé existe déjà pour un **autre** client (SIREN différent, raison sociale différente), suffixer un numéro (`acme-sa-2`). Si même client, proposer `merge` et ne pas créer.

---

## Schéma de la fiche client

Schéma complet et stable de l'entrée dans `clients.json` : voir [`references/schema-fiche-client.md`](references/schema-fiche-client.md).

Exemple de fiche minimale : [`data/fiche-client.example.json`](data/fiche-client.example.json).

`clients/<slug>/company.json` (infos juridiques détaillées : capital, président, banques, paramètres facturation) reprend le schéma de [`organisation-documents/data/company.example.json`](../organisation-documents/data/company.example.json). Créé en lazy.

---

## Communication avec le comptable

Mêmes règles que `organisation-documents` (vocabulaire métier, pas de jargon technique). Voir `organisation-documents/SKILL.md` § Communication pour la doctrine complète. Spécificités de ce skill :

### Format de rapport

| Opération        | Message court                                                         |
| ---------------- | --------------------------------------------------------------------- |
| `create`         | `✅ Client **ACME SA** créé.`                                          |
| `create` + manques | `✅ Client **ACME SA** créé. Pensez à compléter le SIREN.`           |
| `validate-draft` | `✅ Fiche **ACME SA** validée.`                                        |
| `reject-draft`   | `✅ Fiche **ACME SA** rejetée.`                                        |
| `update`         | `✅ Fiche **ACME SA** mise à jour (SIREN, IBAN).`                      |
| `rename`         | `✅ Client renommé : *foo-corp* → *foo-sa*.`                           |
| `merge`          | `✅ Fusion **foo → foo-sa** : 12 pièces réattachées.`                  |
| `archive`        | `✅ Client **Foo** archivé. Restauration possible jusqu'au 26 juin.`   |
| `list`           | Tableau : *Raison sociale · SIREN · Statut · Nb pièces*                |

### Vocabulaire interdit

`slug`, `clients.json`, `index.json`, `audit.log`, `draft-auto-created`, chemins absolus, `UUID`, schéma JSON.

### Vocabulaire métier

Fiche client, dossier, raison sociale, SIREN, domaine, contact, statut, validation, fusion, archivage, restauration.

### Quand demander une validation

**Uniquement** :

- Collision de slug avec un autre client (SIREN différent) → proposer `merge` ou suffixe.
- Collision de SIREN sur deux fiches → escalader.
- Demande d'archivage d'un client qui a des relances en cours dans le mois → confirmer.

---

## Garde-fous

- **Pas de hard-delete** depuis ce skill. Toujours soft-delete avec grâce 30 j.
- **Pas de modification de documents** : ce skill ne renomme jamais une facture, ne déplace jamais un fichier dans `<AAAA>/<MM>/…` à l'unité — il déplace **uniquement** au niveau dossier client (rename, merge, archive).
- **Cohérence `clients.json` ↔ système de fichiers** : après chaque opération mutative, l'invariant `slug existe dans clients.json ⇔ dossier clients/<slug>/ existe` doit tenir. Vérifier en fin de procédure.
- **Audit trail systématique** : toute mutation (create, update, rename, merge, archive, validate-draft, reject-draft) est loguée dans `clients/<slug>/audit.log` (UTC + acteur + champs modifiés).
- **Aucune donnée client ne quitte le container LXD.** Mêmes contraintes RGPD que `organisation-documents`.
- **Lookup INSEE** : autorisé via `organisation-documents/scripts/fetch_company.py` pour résoudre une raison sociale en SIREN, mais avec consentement utilisateur si appelé en dehors d'un flux où l'utilisateur a déjà partagé la raison sociale.

---

## Cohabitation avec `organisation-documents`

Détail : [`references/cohabitation.md`](references/cohabitation.md).

Résumé :

| Action                          | Skill responsable                  |
| ------------------------------- | ---------------------------------- |
| Recevoir une PJ par e-mail      | `organisation-documents`           |
| Classer un document dans `<AAAA>/<MM>/…` | `organisation-documents`     |
| Auto-créer une fiche en draft   | `organisation-documents` (procédure embarquée) ou délégation à ce skill |
| Valider un draft auto-créé      | **`fiches-clients`**               |
| Rejeter un draft auto-créé      | **`fiches-clients`**               |
| Créer une fiche sur demande user | **`fiches-clients`**              |
| Mettre à jour une fiche         | **`fiches-clients`**               |
| Renommer / fusionner / archiver | **`fiches-clients`**               |
| Réattribuer une pièce mal classée | `organisation-documents` (sur la pièce) — la fiche source/cible existe déjà |

---

## Références complémentaires

- [`references/schema-fiche-client.md`](references/schema-fiche-client.md) — schéma JSON complet de `clients.json`, énumérations, contraintes.
- [`references/cohabitation.md`](references/cohabitation.md) — frontière exacte avec `organisation-documents` et règles de transition de statut.
- [`data/fiche-client.example.json`](data/fiche-client.example.json) — exemple de fiche minimale et fiche complète.

### Références externes (héritées)

- [`organisation-documents/references/structure-cible.md`](../organisation-documents/references/structure-cible.md) — convention de slug et arborescence cible.
- [`organisation-documents/data/company.example.json`](../organisation-documents/data/company.example.json) — schéma de `clients/<slug>/company.json` (créé en lazy).
- [`organisation-documents/scripts/fetch_company.py`](../organisation-documents/scripts/fetch_company.py) — lookup SIREN via API INSEE.
