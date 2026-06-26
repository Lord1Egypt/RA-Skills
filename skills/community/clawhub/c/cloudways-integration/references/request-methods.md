# Cloudways Gateway Methods

These are the primary gateway methods exposed by the Cloudways integration.

## Account / status
- `cloudways.status`
  - Returns configured state, stored email, masked API key, local root, preferred sync mode.

- `cloudways.save`
  - Saves account email + API key to vault after validating credentials.

- `cloudways.disconnect`
  - Removes stored account credentials from the vault.

## Inventory
- `cloudways.inventory`
  - Returns normalized server/application inventory plus notes.

## Server secrets
- `cloudways.serverSecrets.get`
  - Input: `serverId`
  - Returns stored server-level SSH credentials.

- `cloudways.serverSecrets.set`
  - Input: `serverId`, `sshHost`, `sshUser`, `sshPassword`, `sshKey`
  - Stores server-level SSH credentials in vault.

- `cloudways.serverConnection.test`
  - Input: `serverId`
  - Tests server SSH connectivity using stored credentials.

## App secrets
- `cloudways.appSecrets.get`
  - Input: `appId`
  - Returns stored app-level SSH / WordPress / DB credentials.

- `cloudways.appSecrets.set`
  - Input: `appId` plus app secret fields
  - Stores app-level credentials in vault.

- `cloudways.appConnection.test`
  - Input: `appId`
  - Tests DB access through the stored DB Manager launcher URL and DB credentials.

## Metadata
- `cloudways.wordpressMetadata`
  - Input: `appId`
  - Returns derived operational metadata for local WordPress review/edit workflows.

## Database query methods
- `cloudways.appQuery.read`
  - Input: `appId`, `sql`
  - Executes read-only SQL through DB Manager after validation.

- `cloudways.appQuery.write`
  - Input: `appId`, `sql`, `confirmText`, `dryRun`
  - Executes guarded write SQL after validation and confirmation.

## Response behavior notes

Typical success shape:
```json
{ "success": true, "message": "..." }
```

Typical failure shape:
```json
{ "success": false, "error": "..." }
```

Query methods may also return:
- `output`
- `message`

Inventory methods may also return:
- `servers`
- `applications`
- `notes`

Metadata methods may also return:
- `metadata`

## Operational notes

- Some methods do live network operations and can fail due to auth, network, or remote platform changes.
- DB Manager login depends on a functioning launcher URL and compatible page structure.
- SSH testing depends on Python + Paramiko availability.
