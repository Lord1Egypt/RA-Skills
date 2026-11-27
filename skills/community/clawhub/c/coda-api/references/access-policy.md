# Coda access policy

An access policy limits which endpoints Coda connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/coda#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Coda: its 67 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create coda --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "apis/v1/resolveBrowserLink"},
    {"method": "GET", "path": "apis/v1/whoami"},
    {"method": "GET", "path": "apis/v1/go/tenants/{id}/agentInstances/{id}/agentSessionIds"},
    {"method": "GET", "path": "apis/v1/go/tenants/{id}/agentInstances/{id}/assistEvaluationLogs"},
    {"method": "GET", "path": "apis/v1/go/tenants/{id}/agentInstances/{id}/logs"},
    {"method": "GET", "path": "apis/v1/go/tenants/{id}/agentInstances/{id}/logs/{id}"},
    {"method": "GET", "path": "apis/v1/analytics/docs"},
    {"method": "GET", "path": "apis/v1/analytics/docs/summary"},
    {"method": "GET", "path": "apis/v1/analytics/docs/{id}/pages"},
    {"method": "GET", "path": "apis/v1/analytics/packs"},
    {"method": "GET", "path": "apis/v1/analytics/packs/summary"},
    {"method": "GET", "path": "apis/v1/analytics/packs/{id}/formulas"},
    {"method": "GET", "path": "apis/v1/analytics/updated"},
    {"method": "GET", "path": "apis/v1/categories"},
    {"method": "GET", "path": "apis/v1/docs/{id}/controls"},
    {"method": "GET", "path": "apis/v1/docs/{id}/controls/{id}"},
    {"method": "GET", "path": "apis/v1/docs"},
    {"method": "GET", "path": "apis/v1/docs/{id}"},
    {"method": "GET", "path": "apis/v1/docs/{id}/domains"},
    {"method": "GET", "path": "apis/v1/domains/provider/{id}"},
    {"method": "GET", "path": "apis/v1/folders"},
    {"method": "GET", "path": "apis/v1/folders/{id}"},
    {"method": "GET", "path": "apis/v1/folders/{id}/children"},
    {"method": "GET", "path": "apis/v1/docs/{id}/formulas"},
    {"method": "GET", "path": "apis/v1/docs/{id}/formulas/{id}"},
    {"method": "GET", "path": "apis/v1/mutationStatus/{id}"},
    {"method": "GET", "path": "apis/v1/packs"},
    {"method": "GET", "path": "apis/v1/packs/invitations"},
    {"method": "GET", "path": "apis/v1/packs/listings"},
    {"method": "GET", "path": "apis/v1/packs/{id}"},
    {"method": "GET", "path": "apis/v1/packs/{id}/categories"},
    {"method": "GET", "path": "apis/v1/packs/{id}/configurations/schema"},
    {"method": "GET", "path": "apis/v1/packs/{id}/docs/{id}/groupedLogs"},
    {"method": "GET", "path": "apis/v1/packs/{id}/docs/{id}/logs"},
    {"method": "GET", "path": "apis/v1/packs/{id}/featuredDocs"},
    {"method": "GET", "path": "apis/v1/packs/{id}/invitations"},
    {"method": "GET", "path": "apis/v1/packs/{id}/listing"},
    {"method": "GET", "path": "apis/v1/packs/{id}/listingDraft"},
    {"method": "GET", "path": "apis/v1/packs/{id}/makers"},
    {"method": "POST", "path": "apis/v1/packs/{id}/nextVersion"},
    {"method": "GET", "path": "apis/v1/packs/{id}/oauthConfig"},
    {"method": "GET", "path": "apis/v1/packs/{id}/permissions"},
    {"method": "GET", "path": "apis/v1/packs/{id}/releases"},
    {"method": "GET", "path": "apis/v1/packs/{id}/reviews"},
    {"method": "GET", "path": "apis/v1/packs/{id}/systemConnection"},
    {"method": "GET", "path": "apis/v1/packs/{id}/tenantId/{id}/rootIngestionId/{id}/ingestionBatchExecutions"},
    {"method": "GET", "path": "apis/v1/packs/{id}/tenantId/{id}/rootIngestionId/{id}/ingestionBatchExecutions/{id}/parentItems"},
    {"method": "GET", "path": "apis/v1/packs/{id}/tenantId/{id}/rootIngestionId/{id}/logs/{id}"},
    {"method": "GET", "path": "apis/v1/packs/{id}/versions"},
    {"method": "GET", "path": "apis/v1/packs/{id}/versions/{id}/diff/{id}"},
    {"method": "GET", "path": "apis/v1/packs/{id}/versions/{id}/sourceCode"},
    {"method": "GET", "path": "apis/v1/docs/{id}/pages"},
    {"method": "GET", "path": "apis/v1/docs/{id}/pages/{id}"},
    {"method": "GET", "path": "apis/v1/docs/{id}/pages/{id}/content"},
    {"method": "GET", "path": "apis/v1/docs/{id}/pages/{id}/export/{id}"},
    {"method": "GET", "path": "apis/v1/docs/{id}/acl/metadata"},
    {"method": "GET", "path": "apis/v1/docs/{id}/acl/permissions"},
    {"method": "GET", "path": "apis/v1/docs/{id}/acl/principals/search"},
    {"method": "GET", "path": "apis/v1/docs/{id}/acl/settings"},
    {"method": "GET", "path": "apis/v1/docs/{id}/tables"},
    {"method": "GET", "path": "apis/v1/docs/{id}/tables/{id}"},
    {"method": "GET", "path": "apis/v1/docs/{id}/tables/{id}/columns"},
    {"method": "GET", "path": "apis/v1/docs/{id}/tables/{id}/columns/{id}"},
    {"method": "GET", "path": "apis/v1/docs/{id}/tables/{id}/rows"},
    {"method": "GET", "path": "apis/v1/docs/{id}/tables/{id}/rows/{id}"},
    {"method": "GET", "path": "apis/v1/workspaces/{id}/roles"},
    {"method": "GET", "path": "apis/v1/workspaces/{id}/users"}
  ],
  "deny": []
}
```

## Endpoints

The Coda endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | apis/v1/resolveBrowserLink | read | account | Given a browser link to a Superhuman Docs object, attempts to find it and return metadata that can be used to get more info on it. |
| GET | apis/v1/whoami | read | account | Returns basic info about the current user. |
| GET | apis/v1/go/tenants/{id}/agentInstances/{id}/agentSessionIds | read | agents | Retrieve the chat sessions of an agent instance for debugging purpose. |
| GET | apis/v1/go/tenants/{id}/agentInstances/{id}/assistEvaluationLogs | read | agents | Lists every Assist trigger evaluation published for one agent instance, newest first. |
| GET | apis/v1/go/tenants/{id}/agentInstances/{id}/logs | read | agents | Retrieve the logs of an agent instance for debugging purpose. |
| GET | apis/v1/go/tenants/{id}/agentInstances/{id}/logs/{id} | read | agents | Retrieve the log details of given logId. |
| GET | apis/v1/analytics/docs | read | analytics | Returns analytics data for available docs per day. |
| GET | apis/v1/analytics/docs/summary | read | analytics | Returns summarized analytics data for available docs. |
| GET | apis/v1/analytics/docs/{id}/pages | read | analytics | Returns analytics data for a given doc within the day. |
| GET | apis/v1/analytics/packs | read | analytics | Returns analytics data for Packs the user can edit. |
| GET | apis/v1/analytics/packs/summary | read | analytics | Returns summarized analytics data for Packs the user can edit. |
| GET | apis/v1/analytics/packs/{id}/formulas | read | analytics | Returns analytics data for Pack formulas. |
| GET | apis/v1/analytics/updated | read | analytics | Returns days based on Pacific Standard Time when analytics were last updated. |
| POST | apis/v1/docs/{id}/hooks/automation/{id} | write | automations | Triggers webhook-invoked automation. |
| GET | apis/v1/categories | read | categories | Gets all available doc categories. |
| GET | apis/v1/docs/{id}/controls | read | controls | Returns a list of controls in a document. |
| GET | apis/v1/docs/{id}/controls/{id} | read | controls | Returns info on a control. |
| GET | apis/v1/docs | read | docs | Returns a list of documents accessible by the user, and which they have opened at least once. |
| POST | apis/v1/docs | write | docs | Creates a new document, optionally copying an existing document. |
| GET | apis/v1/docs/{id} | read | docs | Returns metadata for the specified doc. |
| PATCH | apis/v1/docs/{id} | write | docs | Updates metadata for a doc. |
| DELETE | apis/v1/docs/{id} | write | docs | Deletes a doc. |
| GET | apis/v1/docs/{id}/domains | read | domains | List all custom domains for a published doc. |
| POST | apis/v1/docs/{id}/domains | write | domains | Add a custom domain to a published doc. |
| PATCH | apis/v1/docs/{id}/domains/{id} | write | domains | Updates properties of a document's custom domain. |
| DELETE | apis/v1/docs/{id}/domains/{id} | write | domains | Deletes a custom domain from a published doc. |
| GET | apis/v1/domains/provider/{id} | read | domains | Gets the provider (ie. |
| GET | apis/v1/folders | read | folders | Returns a list of folders the user has access to. |
| POST | apis/v1/folders | write | folders | Creates a new folder. |
| GET | apis/v1/folders/{id} | read | folders | Returns the requested folder. |
| PATCH | apis/v1/folders/{id} | write | folders | Updates metadata for a folder. |
| DELETE | apis/v1/folders/{id} | write | folders | Deletes a folder. |
| GET | apis/v1/folders/{id}/children | read | folders | Returns the direct child folders of a folder. |
| GET | apis/v1/docs/{id}/formulas | read | formulas | Returns a list of named formulas in a document. |
| GET | apis/v1/docs/{id}/formulas/{id} | read | formulas | Returns info on a formula. |
| POST | apis/v1/organizations/{id}/goLinks | write | golinks | Adds a new go link for the organization. |
| GET | apis/v1/mutationStatus/{id} | read | mutations | Get the status for an asynchronous mutation to know whether or not it has been completed. |
| GET | apis/v1/packs | read | packs | Get the list of accessible Packs. |
| POST | apis/v1/packs | write | packs | Creates a new Pack, essentially registering a new Pack ID. |
| GET | apis/v1/packs/invitations | read | packs | Get pending Pack invitations for the authenticated user. |
| POST | apis/v1/packs/invitations/{id}/reply | write | packs | Reply to a Pack invitation (accept or reject). |
| GET | apis/v1/packs/listings | read | packs | Get listings of public Packs and Packs created by you. |
| GET | apis/v1/packs/{id} | read | packs | Returns a single Pack. |
| PATCH | apis/v1/packs/{id} | write | packs | Update an existing Pack for non-versioned fields. |
| DELETE | apis/v1/packs/{id} | write | packs | Delete a given Pack. |
| POST | apis/v1/packs/{id}/assets/{id}/assetType/{id}/uploadComplete | write | packs | Note the completion of the upload of a Pack asset. |
| GET | apis/v1/packs/{id}/categories | read | packs | List publishing categories for a given Pack. |
| POST | apis/v1/packs/{id}/category | write | packs | Add a publishing category for a given Pack. |
| DELETE | apis/v1/packs/{id}/category/{id} | write | packs | Delete a publishing category for a given Pack. |
| GET | apis/v1/packs/{id}/configurations/schema | read | packs | Returns a JSON Schema applicable for customizing the Pack using Pack configurations. |
| GET | apis/v1/packs/{id}/docs/{id}/groupedLogs | read | packs | Retrieve the grouped logs of a Pack for debugging purpose. |
| GET | apis/v1/packs/{id}/docs/{id}/logs | read | packs | Retrieve the logs of a Pack for debugging purpose. |
| GET | apis/v1/packs/{id}/featuredDocs | read | packs | Returns a list of featured doc ids for a Pack. |
| PUT | apis/v1/packs/{id}/featuredDocs | write | packs | Create or replace the featured docs for a Pack. |
| GET | apis/v1/packs/{id}/invitations | read | packs | Get pending invitations for a given Pack. |
| POST | apis/v1/packs/{id}/invitations | write | packs | Create an invitation for a user to access a Pack. |
| PUT | apis/v1/packs/{id}/invitations/{id} | write | packs | Update the access level of an existing Pack invitation. |
| DELETE | apis/v1/packs/{id}/invitations/{id} | write | packs | Revoke a pending Pack invitation. |
| GET | apis/v1/packs/{id}/listing | read | packs | Get detailed listing information for a Pack. |
| GET | apis/v1/packs/{id}/listingDraft | read | packs | Get the current listing draft for a Pack. |
| PUT | apis/v1/packs/{id}/listingDraft | write | packs | Create or update the listing draft for a Pack. |
| DELETE | apis/v1/packs/{id}/listingDraft | write | packs | Delete the listing draft for a Pack, discarding any unsaved changes. |
| POST | apis/v1/packs/{id}/maker | write | packs | Set a maker for a given Pack. |
| DELETE | apis/v1/packs/{id}/maker/{id} | write | packs | Delete a maker for a given Pack, who will not be displayed in the corresponding Packs page. |
| GET | apis/v1/packs/{id}/makers | read | packs | List makers for a given Pack. |
| POST | apis/v1/packs/{id}/nextVersion | read | packs | Get the next valid version based on the proposed metadata. |
| GET | apis/v1/packs/{id}/oauthConfig | read | packs | Retrieve the OAuth configuration of the Pack for display purpose. |
| PUT | apis/v1/packs/{id}/oauthConfig | write | packs | Set the OAuth configurations of the Pack, including client id and secret. |
| GET | apis/v1/packs/{id}/permissions | read | packs | Get user, workspace, and/or global permissions for a given Pack. |
| POST | apis/v1/packs/{id}/permissions | write | packs | Create or modify user, workspace, organization, group, or global permissions for a given Pack. |
| DELETE | apis/v1/packs/{id}/permissions | write | packs | Delete a user's own permissions for a given Pack. |
| DELETE | apis/v1/packs/{id}/permissions/{id} | write | packs | Delete user, workspace, or global permissions for a given Pack. |
| GET | apis/v1/packs/{id}/releases | read | packs | Get the list of releases of a Pack. |
| POST | apis/v1/packs/{id}/releases | write | packs | Creates a new Pack release based on an existing Pack version. |
| PUT | apis/v1/packs/{id}/releases/{id} | write | packs | Update details of a Pack release. |
| GET | apis/v1/packs/{id}/reviews | read | packs | List reviews for a specific Pack. |
| POST | apis/v1/packs/{id}/reviews | write | packs | Submit a Pack for review in Superhuman GO. |
| POST | apis/v1/packs/{id}/reviews/pending/cancel | write | packs | Cancel the pending Pack review for this Pack. |
| GET | apis/v1/packs/{id}/systemConnection | read | packs | Retrieve the system connection metadata of the Pack. |
| PUT | apis/v1/packs/{id}/systemConnection | write | packs | Set the system connection credentials of the Pack. |
| PATCH | apis/v1/packs/{id}/systemConnection | write | packs | Patch the system connection credentials of the Pack. |
| GET | apis/v1/packs/{id}/tenantId/{id}/rootIngestionId/{id}/ingestionBatchExecutions | read | packs | Retrieve the ingestion batch executions of a root ingestion for debugging purpose. |
| GET | apis/v1/packs/{id}/tenantId/{id}/rootIngestionId/{id}/ingestionBatchExecutions/{id}/parentItems | read | packs | Retrieve the parent items of a ingestion batch execution for debugging purpose. |
| GET | apis/v1/packs/{id}/tenantId/{id}/rootIngestionId/{id}/logs/{id} | read | packs | Retrieve the ingestion execution ids of a root ingestion for debugging purpose. |
| POST | apis/v1/packs/{id}/uploadAsset | write | packs | Request a signed s3 URL to upload your Pack asset. |
| POST | apis/v1/packs/{id}/uploadSourceCode | write | packs | Request a signed s3 URL to upload your Pack source code. |
| GET | apis/v1/packs/{id}/versions | read | packs | Get the list of versions of a Pack. |
| GET | apis/v1/packs/{id}/versions/{id}/diff/{id} | read | packs | Gets information about the difference between the specified previous version and next version of a Pack. |
| POST | apis/v1/packs/{id}/versions/{id}/register | write | packs | Registers a new Pack version. |
| GET | apis/v1/packs/{id}/versions/{id}/sourceCode | read | packs | Get temporary links used to download the source code for the given packId and version. |
| POST | apis/v1/packs/{id}/versions/{id}/sourceCode/uploadComplete | write | packs | Note the completion of the upload of a Pack source code. |
| POST | apis/v1/packs/{id}/versions/{id}/uploadComplete | write | packs | Note the completion of the upload of a Pack version bundle in order to create that Pack version. |
| GET | apis/v1/docs/{id}/pages | read | pages | Returns a list of pages in a document. |
| POST | apis/v1/docs/{id}/pages | write | pages | Create a new page in a doc. |
| GET | apis/v1/docs/{id}/pages/{id} | read | pages | Returns details about a page. |
| PUT | apis/v1/docs/{id}/pages/{id} | write | pages | Update properties for a page. |
| DELETE | apis/v1/docs/{id}/pages/{id} | write | pages | Deletes the specified page. |
| GET | apis/v1/docs/{id}/pages/{id}/content | read | pages | Returns a list of content elements in a page. |
| DELETE | apis/v1/docs/{id}/pages/{id}/content | write | pages | Delete content from a page. |
| POST | apis/v1/docs/{id}/pages/{id}/export | write | pages | Initiate an export of content for the given page. |
| GET | apis/v1/docs/{id}/pages/{id}/export/{id} | read | pages | Check the status of a page content export. |
| GET | apis/v1/docs/{id}/acl/metadata | read | permissions | Returns metadata associated with sharing for this document. |
| GET | apis/v1/docs/{id}/acl/permissions | read | permissions | Returns a list of permissions for this document. |
| POST | apis/v1/docs/{id}/acl/permissions | write | permissions | Adds a new permission to the doc. |
| DELETE | apis/v1/docs/{id}/acl/permissions/{id} | write | permissions | Deletes an existing permission. |
| GET | apis/v1/docs/{id}/acl/principals/search | read | permissions | Searches for user and group principals matching the query that this doc can be shared with. |
| GET | apis/v1/docs/{id}/acl/settings | read | permissions | Returns settings associated with ACLs for this document. |
| PATCH | apis/v1/docs/{id}/acl/settings | write | permissions | Update settings associated with ACLs for this document. |
| PUT | apis/v1/docs/{id}/publish | write | publish | Update publish settings for a doc. |
| DELETE | apis/v1/docs/{id}/publish | write | publish | Unpublishes a doc. |
| GET | apis/v1/docs/{id}/tables | read | tables | Returns a list of tables in a document. |
| GET | apis/v1/docs/{id}/tables/{id} | read | tables | Returns details about a specific table or view. |
| GET | apis/v1/docs/{id}/tables/{id}/columns | read | tables | Returns a list of columns in a table. |
| GET | apis/v1/docs/{id}/tables/{id}/columns/{id} | read | tables | Returns details about a column in a table. |
| GET | apis/v1/docs/{id}/tables/{id}/rows | read | tables | Returns a list of rows in a table. |
| POST | apis/v1/docs/{id}/tables/{id}/rows | write | tables | Inserts rows into a table, optionally updating existing rows if any upsert key columns are provided. |
| DELETE | apis/v1/docs/{id}/tables/{id}/rows | write | tables | Deletes the specified rows from the table or view. |
| GET | apis/v1/docs/{id}/tables/{id}/rows/{id} | read | tables | Returns details about a row in a table. |
| PUT | apis/v1/docs/{id}/tables/{id}/rows/{id} | write | tables | Updates the specified row in the table. |
| DELETE | apis/v1/docs/{id}/tables/{id}/rows/{id} | write | tables | Deletes the specified row from the table or view. |
| POST | apis/v1/docs/{id}/tables/{id}/rows/{id}/buttons/{id} | write | tables | Pushes a button on a row in a table. |
| GET | apis/v1/workspaces/{id}/roles | read | workspaces | Returns a list of the counts of users over time by role for the workspace. |
| GET | apis/v1/workspaces/{id}/users | read | workspaces | Returns a list of members in the given workspace. |
| POST | apis/v1/workspaces/{id}/users/role | write | workspaces | Updates the workspace user role of a user that matches the parameters. |
