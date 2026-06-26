# Cloudways UI Design

## Current UI locations

- **Controller:** `/home/charl/openclaw/ui/src/ui/controllers/cloudways.ts`
- **View:** `/home/charl/openclaw/ui/src/ui/views/cloudways.ts`

## Purpose

The Control UI exposes Cloudways as an operator workflow for WordPress review and maintenance preparation.

The UX is designed to let an operator:
- connect a Cloudways account
- load inventory
- choose a server and application
- store server-level and app-level credentials securely
- derive WordPress review metadata
- test SSH and DB access
- inspect DB data read-only
- perform tightly guarded write queries when necessary

## Layout

The page is a single-column stack of cards.

### 1. Cloudways account card
Contains:
- account status
- configure/edit toggle
- email field
- API key field
- default local review root
- preferred sync mode
- disconnect action

Design intent:
- separate account auth from app/server secrets
- keep account setup lightweight
- mask API key after save

### 2. Servers & Applications card
Contains:
- refresh inventory button
- notes from backend
- server list
- application list filtered by selected server

Design intent:
- inventory is primarily navigational
- selecting a server narrows applications
- selecting an app becomes the gateway into operational details

### 3. Server master credentials card
Contains:
- selected server summary
- SSH host/user/password/key fields
- save/cancel actions
- test connection action

Design intent:
- capture shared SSH defaults once per server
- let app-level credentials inherit when app fields are blank

### 4. WordPress review workflow card
Contains:
- derived metadata block
- suggested rsync/sftp commands
- app secret fields
- DB access fields
- test DB access button

Design intent:
- keep operational review context and secure secret entry together
- emphasize that WordPress admin credentials are manual secure inputs
- blend derived hints with editable secure fields

### 5. Read-only database inspection section
Contains:
- SQL textarea
- run read query button
- output pane

Design intent:
- provide quick safe inspection without leaving the UI
- constrain usage to read-only SQL

### 6. Guarded database write mode
Contains:
- write SQL textarea
- confirmation phrase input
- dry-run checkbox
- run write button
- output pane

Design intent:
- make write access explicit and frictionful
- discourage accidental production mutations
- explain the restrictions inline

## UX characteristics

### Strengths
- clear distinction between account auth, server secrets, and app secrets
- strong emphasis on secure storage
- practical WordPress-oriented operator workflow
- DB write path has meaningful friction and explanation
- inherited server credentials reduce duplicate entry

### Constraints
- page is dense and admin-oriented
- relies on manual credential entry for many real-world flows
- DB Manager automation may be brittle if remote UI changes
- no dedicated preview/diff for query impact beyond dry-run behavior
- not aimed at novice users

## Suggested future improvements

- add structured test result history for SSH/DB checks
- show audit-log summaries in UI instead of only file-based logging
- add richer query preview / affected-row feedback
- add clearer inheritance indicators when app secrets are blank but server secrets exist
- add export/scrubbed diagnostic bundle for support cases
