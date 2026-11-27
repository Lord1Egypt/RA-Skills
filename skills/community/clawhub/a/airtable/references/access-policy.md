# Airtable access policy

An access policy limits which endpoints Airtable connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/airtable#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Airtable: its 33 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create airtable --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v0/meta/bases"},
    {"method": "GET", "path": "v0/meta/bases/{id}"},
    {"method": "GET", "path": "v0/meta/bases/{id}/blockInstallations"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/auditLogEvents"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/auditLogs"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/auditLogs/{id}"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/changeEvents"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/exports"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/exports/{id}"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/packages"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/personalAccessTokens"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/users"},
    {"method": "GET", "path": "v0/meta/enterpriseAccounts/{id}/users/{id}"},
    {"method": "GET", "path": "v0/meta/groups/{id}"},
    {"method": "POST", "path": "v0/{id}/{id}/getRecords"},
    {"method": "GET", "path": "v0/meta/bases/{id}/interfaces/{id}"},
    {"method": "GET", "path": "v0/meta/bases/{id}/portalCollaborators"},
    {"method": "GET", "path": "v0/{id}/{id}"},
    {"method": "POST", "path": "v0/{id}/{id}/listRecords"},
    {"method": "GET", "path": "v0/{id}/{id}/{id}"},
    {"method": "GET", "path": "v0/{id}/{id}/{id}/comments"},
    {"method": "GET", "path": "scim/v2/Groups"},
    {"method": "GET", "path": "scim/v2/Groups/{id}"},
    {"method": "GET", "path": "scim/v2/Users"},
    {"method": "GET", "path": "scim/v2/Users/{id}"},
    {"method": "GET", "path": "v0/meta/bases/{id}/shares"},
    {"method": "GET", "path": "v0/meta/bases/{id}/tables"},
    {"method": "GET", "path": "v0/meta/whoami"},
    {"method": "GET", "path": "v0/meta/bases/{id}/views"},
    {"method": "GET", "path": "v0/meta/bases/{id}/views/{id}"},
    {"method": "GET", "path": "v0/bases/{id}/webhooks"},
    {"method": "GET", "path": "v0/meta/workspaces/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Airtable endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v0/meta/bases | read | bases | Returns the list of bases the token can access, 1000 bases at a time. |
| POST | v0/meta/bases | write | bases | Creates a new base with the provided tables and returns the schema for the newly created base. |
| GET | v0/meta/bases/{id} | read | bases | Returns basic information on the base. |
| DELETE | v0/meta/bases/{id} | write | bases | Deletes the specified base. |
| GET | v0/meta/bases/{id}/blockInstallations | read | block_installations | Lists basic information of base block installations. |
| PATCH | v0/meta/bases/{id}/blockInstallations/{id} | write | block_installations | Manages block installation state. |
| DELETE | v0/meta/bases/{id}/blockInstallations/{id} | write | block_installations | Deletes a block installation (recoverable). |
| POST | v0/meta/bases/{id}/collaborators | write | collaborators | Add a new base collaborator. |
| PATCH | v0/meta/bases/{id}/collaborators/{id} | write | collaborators | Updates the permission level of a collaborator on a base. |
| DELETE | v0/meta/bases/{id}/collaborators/{id} | write | collaborators | Delete a base collaborator. |
| GET | v0/meta/enterpriseAccounts/{id} | read | enterprise | Returns basic information relevant to the enterprise account. |
| GET | v0/meta/enterpriseAccounts/{id}/auditLogEvents | read | enterprise | Retrieve audit log events for an enterprise. |
| GET | v0/meta/enterpriseAccounts/{id}/auditLogs | read | enterprise | List audit log requests. |
| POST | v0/meta/enterpriseAccounts/{id}/auditLogs | write | enterprise | Create audit log request. |
| GET | v0/meta/enterpriseAccounts/{id}/auditLogs/{id} | read | enterprise | Get audit log request. |
| GET | v0/meta/enterpriseAccounts/{id}/changeEvents | read | enterprise | Retrieve change events for enterprise bases. |
| POST | v0/meta/enterpriseAccounts/{id}/descendants | write | enterprise | Creates a descendant enterprise account of the enterprise account. |
| GET | v0/meta/enterpriseAccounts/{id}/exports | read | enterprise | Get the status and result of all eDiscovery exports. |
| POST | v0/meta/enterpriseAccounts/{id}/exports | write | enterprise | Create an eDiscovery export request. |
| GET | v0/meta/enterpriseAccounts/{id}/exports/{id} | read | enterprise | Get the status and result of an eDiscovery export. |
| POST | v0/meta/enterpriseAccounts/{id}/moveGroups | write | enterprise | Batch move user groups between two enterprise accounts belonging to the same organization. |
| POST | v0/meta/enterpriseAccounts/{id}/moveWorkspaces | write | enterprise | Batch move workspaces between two enterprise accounts belonging to the same organization. |
| GET | v0/meta/enterpriseAccounts/{id}/packages | read | enterprise | List all packages for an enterprise account. |
| POST | v0/meta/enterpriseAccounts/{id}/packages/{id}/install | write | enterprise | Creates a new base by installing a package template for an enterprise account, and returns the schema for the newly created base. |
| GET | v0/meta/enterpriseAccounts/{id}/personalAccessTokens | read | enterprise | List personal access tokens for users administered by this enterprise account. |
| POST | v0/meta/enterpriseAccounts/{id}/personalAccessTokens/revoke | write | enterprise | Revoke personal access tokens for users administered by this enterprise account. |
| GET | v0/meta/enterpriseAccounts/{id}/users | read | enterprise | Returns basic information relevant to both internal and external user. |
| PATCH | v0/meta/enterpriseAccounts/{id}/users | write | enterprise | Batch manage enterprise account users. |
| DELETE | v0/meta/enterpriseAccounts/{id}/users | write | enterprise | Delete multiple users by email. |
| POST | v0/meta/enterpriseAccounts/{id}/users/claim | write | enterprise | Batch manage organizations enterprise account users. |
| POST | v0/meta/enterpriseAccounts/{id}/users/grantAdminAccess | write | enterprise | Grant admin access to users. |
| POST | v0/meta/enterpriseAccounts/{id}/users/revokeAdminAccess | write | enterprise | Revokes admin access from users. |
| GET | v0/meta/enterpriseAccounts/{id}/users/{id} | read | enterprise | Returns basic information relevant to both internal and external user. |
| PATCH | v0/meta/enterpriseAccounts/{id}/users/{id} | write | enterprise | Manage enterprise account managed users. |
| DELETE | v0/meta/enterpriseAccounts/{id}/users/{id} | write | enterprise | Delete ELA enterprise account internal users and "claiming" enterprise account managed users. |
| POST | v0/meta/enterpriseAccounts/{id}/users/{id}/logout | write | enterprise | Logout the user. |
| POST | v0/meta/enterpriseAccounts/{id}/users/{id}/remove | write | enterprise | Unshare a user from all enterprise workspaces, bases, interfaces, and user groups. |
| POST | v0/meta/enterpriseAccounts/{id}/workspaceAiAllowlist | write | enterprise | Add or remove workspaces from the enterprise AI allowlist. |
| GET | v0/meta/groups/{id} | read | groups | Returns basic information relevant to the user group. |
| POST | v0/{id}/{id}/deleteRecords | write | hyperdb | Delete records from a HyperDB table with primary keys matching specified primary keys. |
| POST | v0/{id}/{id}/getRecords | read | hyperdb | Read records from a HyperDB table. |
| PUT | v0/{id}/{id}/upsertRecords | write | hyperdb | Update or insert records from a HyperDB table with primary keys matching specified primary keys. |
| GET | v0/meta/bases/{id}/interfaces/{id} | read | interfaces | Returns general information about the interface. |
| POST | v0/meta/bases/{id}/interfaces/{id}/collaborators | write | interfaces | Use this to add a collaborator to an interface. |
| PATCH | v0/meta/bases/{id}/interfaces/{id}/collaborators/{id} | write | interfaces | Use this to update permissions for an interface-only collaborator. |
| DELETE | v0/meta/bases/{id}/interfaces/{id}/collaborators/{id} | write | interfaces | Delete an interface collaborator. |
| DELETE | v0/meta/bases/{id}/interfaces/{id}/invites/{id} | write | interfaces | Delete an interface invite. |
| POST | v0/meta/bases/{id}/interfaces/{id}/portalCollaborators | write | interfaces | Use this to add external users to an interface through the base's portal. |
| PATCH | v0/meta/bases/{id}/interfaces/{id}/portalCollaborators/{id} | write | interfaces | Use this to change the permission level of a user who has access to an interface through the base's portal. |
| DELETE | v0/meta/bases/{id}/interfaces/{id}/portalCollaborators/{id} | write | interfaces | Use this to remove a user's access to an interface through the base's portal, or to cancel a pending portal invite to it. |
| DELETE | v0/meta/bases/{id}/invites/{id} | write | invites | Delete a base invite. |
| GET | v0/meta/bases/{id}/portalCollaborators | read | portal_collaborators | Lists the users who can access interfaces through the base's portal, with the interfaces each one can access and their license type, and the pending portal invites. |
| DELETE | v0/meta/bases/{id}/portalCollaborators/{id} | write | portal_collaborators | Use this to remove a user's access to every interface they can access through the base's portal, like removing them from the portal in the interface's Manage access dialog, or to cancel a pending portal invite. |
| GET | v0/{id}/{id} | read | records | List records in a table. |
| POST | v0/{id}/{id} | write | records | Creates multiple records. |
| PUT | v0/{id}/{id} | write | records | Update multiple records. |
| PATCH | v0/{id}/{id} | write | records | Updates records, or upserts them when performUpsert is set (see below). |
| DELETE | v0/{id}/{id} | write | records | Deletes records given an array of record ids. |
| POST | v0/{id}/{id}/listRecords | read | records | Lists records in a table using a POST body, for queries too long for a URL. |
| POST | v0/{id}/{id}/sync/{id} | write | records | Syncs raw CSV data into a Sync API table. |
| GET | v0/{id}/{id}/{id} | read | records | Retrieve a single record. |
| PUT | v0/{id}/{id}/{id} | write | records | Updates a single record. |
| PATCH | v0/{id}/{id}/{id} | write | records | Updates a single record. |
| DELETE | v0/{id}/{id}/{id} | write | records | Deletes a single record. |
| GET | v0/{id}/{id}/{id}/comments | read | records | Returns a list of comments for the record from newest to oldest. |
| POST | v0/{id}/{id}/{id}/comments | write | records | Creates a comment on a record. |
| PATCH | v0/{id}/{id}/{id}/comments/{id} | write | records | Updates a comment on a record. |
| DELETE | v0/{id}/{id}/{id}/comments/{id} | write | records | Deletes a comment from a record. |
| PATCH | v0/{id}/{id}/{id}/dateDependencyMetadata | write | records | Update date dependency metadata for a linked predecessor on a successor record. |
| POST | v0/{id}/{id}/{id}/uploadAttachment | write | records | Upload an attachment up to 5 MB to an attachment cell via the file bytes directly. |
| GET | scim/v2/Groups | read | scim | List groups as SCIM Groups objects. |
| POST | scim/v2/Groups | write | scim | Create a new group from a SCIM Group object. |
| GET | scim/v2/Groups/{id} | read | scim | Get a single group as a SCIM Group object. |
| PUT | scim/v2/Groups/{id} | write | scim | Replace a Groups's attributes with all new values. |
| PATCH | scim/v2/Groups/{id} | write | scim | SCIM patch an array of operations to a Group and applies them sequentially. |
| DELETE | scim/v2/Groups/{id} | write | scim | Delete a single SCIM Group. |
| GET | scim/v2/Users | read | scim | List users as SCIM User objects. |
| POST | scim/v2/Users | write | scim | Create a new user from a SCIM User object. |
| GET | scim/v2/Users/{id} | read | scim | Get a single user as a SCIM User object. |
| PUT | scim/v2/Users/{id} | write | scim | Replace a user's attributes with all new values. |
| PATCH | scim/v2/Users/{id} | write | scim | Perform a list of SCIM patch operations in sequence on an existing user. |
| DELETE | scim/v2/Users/{id} | write | scim | Delete a single SCIM user. |
| GET | v0/meta/bases/{id}/shares | read | shares | Lists basic information of base shares. |
| PATCH | v0/meta/bases/{id}/shares/{id} | write | shares | Manages share state. |
| DELETE | v0/meta/bases/{id}/shares/{id} | write | shares | Deletes a base share. |
| GET | v0/meta/bases/{id}/tables | read | tables | Returns the schema of the tables in the specified base. |
| POST | v0/meta/bases/{id}/tables | write | tables | Creates a new table and returns the schema for the newly created table. |
| PATCH | v0/meta/bases/{id}/tables/{id} | write | tables | Updates the name, description, and/or date dependency settings of a table. |
| POST | v0/meta/bases/{id}/tables/{id}/fields | write | tables | Creates a new column and returns the schema for the newly created column. |
| PATCH | v0/meta/bases/{id}/tables/{id}/fields/{id} | write | tables | Updates the name, description, and/or options of a field. |
| POST | v0/meta/revoke | write | tokens | Revoke the personal access token used to authenticate this request. |
| GET | v0/meta/whoami | read | users | Retrieve the user's ID. |
| GET | v0/meta/bases/{id}/views | read | views | Lists basic information of base views. |
| GET | v0/meta/bases/{id}/views/{id} | read | views | Get basic information of base view. |
| DELETE | v0/meta/bases/{id}/views/{id} | write | views | Delete a view. |
| GET | v0/bases/{id}/webhooks | read | webhooks | Lists all webhooks that are registered for a base, along with their statuses. |
| POST | v0/bases/{id}/webhooks | write | webhooks | Creates a new webhook in the specified base. |
| DELETE | v0/bases/{id}/webhooks/{id} | write | webhooks | Deletes a webhook. |
| POST | v0/bases/{id}/webhooks/{id}/enableNotifications | write | webhooks | Enables or disables notification pings for a webhook. |
| GET | v0/bases/{id}/webhooks/{id}/payloads | write | webhooks | Enumerate the update messages for a client to consume. Kept out of read: listing payloads extends the webhook expiration. |
| POST | v0/bases/{id}/webhooks/{id}/refresh | write | webhooks | Extend the life of a webhook. |
| POST | v0/meta/workspaces | write | workspaces | Creates a new workspace with the provided name within the specified enterprise account and returns the workspace id. |
| GET | v0/meta/workspaces/{id} | read | workspaces | Returns basic information on the workspace. |
| DELETE | v0/meta/workspaces/{id} | write | workspaces | Deletes the specified workspace. |
| POST | v0/meta/workspaces/{id}/collaborators | write | workspaces | Add a new workspace collaborator. |
| PATCH | v0/meta/workspaces/{id}/collaborators/{id} | write | workspaces | Updates the permission level of a collaborator on a workspace. |
| DELETE | v0/meta/workspaces/{id}/collaborators/{id} | write | workspaces | Delete a workspace collaborator. |
| DELETE | v0/meta/workspaces/{id}/invites/{id} | write | workspaces | Delete a workspace invite. |
| POST | v0/meta/workspaces/{id}/moveBase | write | workspaces | Move a base between two workspaces owned by the enterprise. |
| POST | v0/meta/workspaces/{id}/updateRestrictions | write | workspaces | Update sharing restrictions settings for the workspace. |
