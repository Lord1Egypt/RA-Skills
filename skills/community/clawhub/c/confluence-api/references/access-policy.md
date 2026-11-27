# Confluence access policy

An access policy limits which endpoints Confluence connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/confluence#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Confluence: its 217 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create confluence --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/analytics/content/{id}/viewers"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/analytics/content/{id}/views"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/ancestors"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}/ancestors"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/ancestors"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/ancestors"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/ancestors"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/app/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/app/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/thumbnail/download"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/attachments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/attachments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/labels/{id}/attachments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/attachments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/audit"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/audit/export"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/audit/retention"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/audit/since"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/labels/{id}/blogposts"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/blogposts"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/direct-children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}/direct-children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/direct-children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/direct-children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/direct-children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/classification-level"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/classification-levels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/classification-level"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/classification-level"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/classification-level/default"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/classification-level"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/footer-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/footer-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/inline-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/footer-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/children"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/footer-comments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/inline-comments"},
    {"method": "POST", "path": "ex/confluence/{id}/wiki/api/v2/content/convert-ids-to-types"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/search"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/child/attachment/{id}/download"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/bulk/tasks"},
    {"method": "POST", "path": "ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/bulk/tasks"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/{id}"},
    {"method": "POST", "path": "ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/descendant"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/descendant/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/history/{id}/macro/id/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/history/{id}/macro/id/{id}/convert/async/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/history/{id}/macro/id/{id}/convert/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/restriction-state"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/restriction-state"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/restriction-state"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/restriction-state"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/restriction-state"},
    {"method": "POST", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/permission/check"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/comments/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/comments/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/restriction"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/byGroupId/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/user"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content-states"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/state"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/state/available"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/state"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/state/content"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/state/settings"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/notification/child-created"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/content/{id}/notification/created"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/watch"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/watch/content/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/watch/label/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/watch/space/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/custom-content"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/custom-content"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/custom-content"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/data-policies/metadata"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/data-policies/spaces"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/entries"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/entries/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/fields"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/views"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/descendants"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}/descendants"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/descendants"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/descendants"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/descendants"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/label"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/group"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/group/by-id"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/group/picker"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/group/{id}/membersByGroupId"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/content/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/labels"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/label"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/likes/count"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/likes/users"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/likes/count"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/likes/users"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/likes/count"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/likes/users"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/likes/count"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/likes/users"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/longtask"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/longtask/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/databases/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/folders/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/operations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/labels/{id}/pages"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/pages"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/relation/{id}/from/{id}/{id}/to/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/relation/{id}/from/{id}/{id}/to/{id}/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/relation/{id}/to/{id}/{id}/from/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/search"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/search/user"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/settings/lookandfeel"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/settings/systemInfo"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/embeds/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/space-permissions/transition/combinations"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/space-permissions/transition/tasks/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/space-permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/permissions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/space-role-mode"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/space-roles"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/space-roles/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/spaces/{id}/role-assignments"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/settings"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/tasks"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/tasks/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/template/blueprint"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/template/page"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/template/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/settings/theme"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/settings/theme/selected"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/settings/theme/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/space/{id}/theme"},
    {"method": "POST", "path": "ex/confluence/{id}/wiki/api/v2/user/access/check-access-by-email"},
    {"method": "POST", "path": "ex/confluence/{id}/wiki/api/v2/users-bulk"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/{id}/property"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/{id}/property/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/anonymous"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/bulk"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/current"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/email"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/email/bulk"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/rest/api/user/memberof"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/versions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/attachments/{id}/versions/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/versions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/blogposts/{id}/versions/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/versions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/custom-content/{id}/versions/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/versions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/versions/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/versions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/versions/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/versions"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/pages/{id}/versions/{id}"},
    {"method": "GET", "path": "ex/confluence/{id}/wiki/api/v2/whiteboards/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Confluence endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | ex/confluence/{id}/wiki/api/v2/admin-key | write | admin-key | Get Admin Key. Kept out of read: returns the admin key and elevates privileges. |
| POST | ex/confluence/{id}/wiki/api/v2/admin-key | write | admin-key | Enable Admin Key. |
| DELETE | ex/confluence/{id}/wiki/api/v2/admin-key | write | admin-key | Disable Admin Key. |
| GET | ex/confluence/{id}/wiki/rest/api/analytics/content/{id}/viewers | read | analytics | Get viewers. |
| GET | ex/confluence/{id}/wiki/rest/api/analytics/content/{id}/views | read | analytics | Get views. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/ancestors | read | ancestors | Get all ancestors of database. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id}/ancestors | read | ancestors | Get all ancestors of Smart Link in content tree. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/ancestors | read | ancestors | Get all ancestors of folder. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/ancestors | read | ancestors | Get all ancestors of page. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/ancestors | read | ancestors | Get all ancestors of whiteboard. |
| GET | ex/confluence/{id}/wiki/api/v2/app/properties | read | app-properties | Get Forge app properties. |
| GET | ex/confluence/{id}/wiki/api/v2/app/properties/{id} | read | app-properties | Get a Forge app property by key. |
| PUT | ex/confluence/{id}/wiki/api/v2/app/properties/{id} | write | app-properties | Create or update a Forge app property. |
| DELETE | ex/confluence/{id}/wiki/api/v2/app/properties/{id} | write | app-properties | Deletes a Forge app property. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments | read | attachment | Get attachments. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id} | read | attachment | Get attachment by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/attachments/{id} | write | attachment | Delete attachment. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/thumbnail/download | read | attachment | Download attachment thumbnail by id. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/attachments | read | attachment | Get attachments for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/attachments | read | attachment | Get attachments for custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/labels/{id}/attachments | read | attachment | Get attachments for label. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/attachments | read | attachment | Get attachments for page. |
| GET | ex/confluence/{id}/wiki/rest/api/audit | read | audit | Get audit records. |
| POST | ex/confluence/{id}/wiki/rest/api/audit | write | audit | Create audit record. |
| GET | ex/confluence/{id}/wiki/rest/api/audit/export | read | audit | Export audit records. |
| GET | ex/confluence/{id}/wiki/rest/api/audit/retention | read | audit | Get retention period. |
| PUT | ex/confluence/{id}/wiki/rest/api/audit/retention | write | audit | Set retention period. |
| GET | ex/confluence/{id}/wiki/rest/api/audit/since | read | audit | Get audit records for time period. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts | read | blog-post | Get blog posts. |
| POST | ex/confluence/{id}/wiki/api/v2/blogposts | write | blog-post | Create blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id} | read | blog-post | Get blog post by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/blogposts/{id} | write | blog-post | Update blog post. |
| DELETE | ex/confluence/{id}/wiki/api/v2/blogposts/{id} | write | blog-post | Delete blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/labels/{id}/blogposts | read | blog-post | Get blog posts for label. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/blogposts | read | blog-post | Get blog posts in space. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/children | read | children | Get child custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/direct-children | read | children | Get direct children of a database. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id}/direct-children | read | children | Get direct children of a Smart Link. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/direct-children | read | children | Get direct children of a folder. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/children | read | children | Get child pages. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/direct-children | read | children | Get direct children of a page. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/direct-children | read | children | Get direct children of a whiteboard. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/classification-level | read | classification-level | Get blog post classification level. |
| PUT | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/classification-level | write | classification-level | Update blog post classification level. |
| POST | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/classification-level/reset | write | classification-level | Reset blog post classification level. |
| GET | ex/confluence/{id}/wiki/api/v2/classification-levels | read | classification-level | Get list of classification levels. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/classification-level | read | classification-level | Get database classification level. |
| PUT | ex/confluence/{id}/wiki/api/v2/databases/{id}/classification-level | write | classification-level | Update database classification level. |
| POST | ex/confluence/{id}/wiki/api/v2/databases/{id}/classification-level/reset | write | classification-level | Reset database classification level. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/classification-level | read | classification-level | Get page classification level. |
| PUT | ex/confluence/{id}/wiki/api/v2/pages/{id}/classification-level | write | classification-level | Update page classification level. |
| POST | ex/confluence/{id}/wiki/api/v2/pages/{id}/classification-level/reset | write | classification-level | Reset page classification level. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/classification-level/default | read | classification-level | Get space default classification level. |
| PUT | ex/confluence/{id}/wiki/api/v2/spaces/{id}/classification-level/default | write | classification-level | Update space default classification level. |
| DELETE | ex/confluence/{id}/wiki/api/v2/spaces/{id}/classification-level/default | write | classification-level | Delete space default classification level. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/classification-level | read | classification-level | Get whiteboard classification level. |
| PUT | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/classification-level | write | classification-level | Update whiteboard classification level. |
| POST | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/classification-level/reset | write | classification-level | Reset whiteboard classification level. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/footer-comments | read | comment | Get attachment comments. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/footer-comments | read | comment | Get footer comments for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/inline-comments | read | comment | Get inline comments for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/footer-comments | read | comment | Get custom content comments. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments | read | comment | Get footer comments. |
| POST | ex/confluence/{id}/wiki/api/v2/footer-comments | write | comment | Create footer comment. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id} | read | comment | Get footer comment by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/footer-comments/{id} | write | comment | Update footer comment. |
| DELETE | ex/confluence/{id}/wiki/api/v2/footer-comments/{id} | write | comment | Delete footer comment. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/children | read | comment | Get children footer comments. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments | read | comment | Get inline comments. |
| POST | ex/confluence/{id}/wiki/api/v2/inline-comments | write | comment | Create inline comment. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id} | read | comment | Get inline comment by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/inline-comments/{id} | write | comment | Update inline comment. |
| DELETE | ex/confluence/{id}/wiki/api/v2/inline-comments/{id} | write | comment | Delete inline comment. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/children | read | comment | Get children inline comments. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/footer-comments | read | comment | Get footer comments for page. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/inline-comments | read | comment | Get inline comments for page. |
| POST | ex/confluence/{id}/wiki/api/v2/content/convert-ids-to-types | read | content | Convert content ids to content types. |
| POST | ex/confluence/{id}/wiki/rest/api/content/archive | write | content | Archive pages. |
| POST | ex/confluence/{id}/wiki/rest/api/content/blueprint/instance/{id} | write | content | Publish legacy draft. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/blueprint/instance/{id} | write | content | Publish shared draft. |
| GET | ex/confluence/{id}/wiki/rest/api/content/search | read | content | Search content by CQL. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/child/attachment | write | content-attachments | Create attachment. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/child/attachment | write | content-attachments | Create or update attachment. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/child/attachment/{id} | write | content-attachments | Update attachment properties. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/child/attachment/{id}/data | write | content-attachments | Update attachment data. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/child/attachment/{id}/download | read | content-attachments | Get URI to download attachment. |
| GET | ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/bulk/tasks | read | content-body | Get asynchronous content body conversion task result in bulk. |
| POST | ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/bulk/tasks | read | content-body | Create asynchronous content body conversion tasks in bulk. |
| GET | ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/{id} | read | content-body | Get asynchronously converted content body from the id or the current status of the task. |
| POST | ex/confluence/{id}/wiki/rest/api/contentbody/convert/async/{id} | read | content-body | Asynchronously convert content body. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/copy | write | content-children-and-descendants | Copy single page. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/descendant | read | content-children-and-descendants | Get content descendants. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/descendant/{id} | read | content-children-and-descendants | Get content descendants by type. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/move/{id}/{id} | write | content-children-and-descendants | Move a page to a new location relative to a target page. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/pagehierarchy/copy | write | content-children-and-descendants | Copy page hierarchy. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/label | write | content-labels | Add labels to content. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/label | write | content-labels | Remove label from content using query parameter. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/label/{id} | write | content-labels | Remove label from content. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/history/{id}/macro/id/{id} | read | content-macro-body | Get macro body by macro ID. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/history/{id}/macro/id/{id}/convert/async/{id} | read | content-macro-body | Get macro body by macro ID and convert representation Asynchronously. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/history/{id}/macro/id/{id}/convert/{id} | read | content-macro-body | Get macro body by macro ID and convert the representation synchronously. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/permissions | read | content-permissions | Get blog post permissions. |
| POST | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/permissions | write | content-permissions | Add blog post permissions. |
| PUT | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/permissions | write | content-permissions | Set blog post permissions. |
| DELETE | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/permissions | write | content-permissions | Delete blog post permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/restriction-state | read | content-permissions | Get blog post restriction state. |
| PUT | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/restriction-state | write | content-permissions | Set blog post restriction state. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/permissions | read | content-permissions | Get database permissions. |
| POST | ex/confluence/{id}/wiki/api/v2/databases/{id}/permissions | write | content-permissions | Add database permissions. |
| PUT | ex/confluence/{id}/wiki/api/v2/databases/{id}/permissions | write | content-permissions | Set database permissions. |
| DELETE | ex/confluence/{id}/wiki/api/v2/databases/{id}/permissions | write | content-permissions | Delete database permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/restriction-state | read | content-permissions | Get database restriction state. |
| PUT | ex/confluence/{id}/wiki/api/v2/databases/{id}/restriction-state | write | content-permissions | Set database restriction state. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/permissions | read | content-permissions | Get folder permissions. |
| POST | ex/confluence/{id}/wiki/api/v2/folders/{id}/permissions | write | content-permissions | Add folder permissions. |
| PUT | ex/confluence/{id}/wiki/api/v2/folders/{id}/permissions | write | content-permissions | Set folder permissions. |
| DELETE | ex/confluence/{id}/wiki/api/v2/folders/{id}/permissions | write | content-permissions | Delete folder permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/restriction-state | read | content-permissions | Get folder restriction state. |
| PUT | ex/confluence/{id}/wiki/api/v2/folders/{id}/restriction-state | write | content-permissions | Set folder restriction state. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/permissions | read | content-permissions | Get page permissions. |
| POST | ex/confluence/{id}/wiki/api/v2/pages/{id}/permissions | write | content-permissions | Add page permissions. |
| PUT | ex/confluence/{id}/wiki/api/v2/pages/{id}/permissions | write | content-permissions | Set page permissions. |
| DELETE | ex/confluence/{id}/wiki/api/v2/pages/{id}/permissions | write | content-permissions | Delete page permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/restriction-state | read | content-permissions | Get page restriction state. |
| PUT | ex/confluence/{id}/wiki/api/v2/pages/{id}/restriction-state | write | content-permissions | Set page restriction state. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/permissions | read | content-permissions | Get whiteboard permissions. |
| POST | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/permissions | write | content-permissions | Add whiteboard permissions. |
| PUT | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/permissions | write | content-permissions | Set whiteboard permissions. |
| DELETE | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/permissions | write | content-permissions | Delete whiteboard permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/restriction-state | read | content-permissions | Get whiteboard restriction state. |
| PUT | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/restriction-state | write | content-permissions | Set whiteboard restriction state. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/permission/check | read | content-permissions | Check content permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties | read | content-properties | Get content properties for attachment. |
| POST | ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties | write | content-properties | Create content property for attachment. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties/{id} | read | content-properties | Get content property for attachment by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties/{id} | write | content-properties | Update content property for attachment by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/attachments/{id}/properties/{id} | write | content-properties | Delete content property for attachment by id. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties | read | content-properties | Get content properties for blog post. |
| POST | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties | write | content-properties | Create content property for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties/{id} | read | content-properties | Get content property for blog post by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties/{id} | write | content-properties | Update content property for blog post by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/properties/{id} | write | content-properties | Delete content property for blogpost by id. |
| GET | ex/confluence/{id}/wiki/api/v2/comments/{id}/properties | read | content-properties | Get content properties for comment. |
| POST | ex/confluence/{id}/wiki/api/v2/comments/{id}/properties | write | content-properties | Create content property for comment. |
| GET | ex/confluence/{id}/wiki/api/v2/comments/{id}/properties/{id} | read | content-properties | Get content property for comment by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/comments/{id}/properties/{id} | write | content-properties | Update content property for comment by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/comments/{id}/properties/{id} | write | content-properties | Delete content property for comment by id. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties | read | content-properties | Get content properties for custom content. |
| POST | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties | write | content-properties | Create content property for custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties/{id} | read | content-properties | Get content property for custom content by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties/{id} | write | content-properties | Update content property for custom content by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/properties/{id} | write | content-properties | Delete content property for custom content by id. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/properties | read | content-properties | Get content properties for database. |
| POST | ex/confluence/{id}/wiki/api/v2/databases/{id}/properties | write | content-properties | Create content property for database. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/properties/{id} | read | content-properties | Get content property for database by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/databases/{id}/properties/{id} | write | content-properties | Update content property for database by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/databases/{id}/properties/{id} | write | content-properties | Delete content property for database by id. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties | read | content-properties | Get content properties for Smart Link in the content tree. |
| POST | ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties | write | content-properties | Create content property for Smart Link in the content tree. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties/{id} | read | content-properties | Get content property for Smart Link in the content tree by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties/{id} | write | content-properties | Update content property for Smart Link in the content tree by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/embeds/{id}/properties/{id} | write | content-properties | Delete content property for Smart Link in the content tree by id. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/properties | read | content-properties | Get content properties for folder. |
| POST | ex/confluence/{id}/wiki/api/v2/folders/{id}/properties | write | content-properties | Create content property for folder. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/properties/{id} | read | content-properties | Get content property for folder by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/folders/{id}/properties/{id} | write | content-properties | Update content property for folder by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/folders/{id}/properties/{id} | write | content-properties | Delete content property for folder by id. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/properties | read | content-properties | Get content properties for page. |
| POST | ex/confluence/{id}/wiki/api/v2/pages/{id}/properties | write | content-properties | Create content property for page. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/properties/{id} | read | content-properties | Get content property for page by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/pages/{id}/properties/{id} | write | content-properties | Update content property for page by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/pages/{id}/properties/{id} | write | content-properties | Delete content property for page by id. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties | read | content-properties | Get content properties for whiteboard. |
| POST | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties | write | content-properties | Create content property for whiteboard. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties/{id} | read | content-properties | Get content property for whiteboard by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties/{id} | write | content-properties | Update content property for whiteboard by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/properties/{id} | write | content-properties | Delete content property for whiteboard by id. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction | read | content-restrictions | Get restrictions. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction | write | content-restrictions | Add restrictions. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction | write | content-restrictions | Update restrictions. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction | write | content-restrictions | Delete restrictions. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation | read | content-restrictions | Get restrictions by operation. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id} | read | content-restrictions | Get restrictions for operation. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/byGroupId/{id} | read | content-restrictions | Get content restriction status for group. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/byGroupId/{id} | write | content-restrictions | Add group to content restriction. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/byGroupId/{id} | write | content-restrictions | Remove group from content restriction. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/user | read | content-restrictions | Get content restriction status for user. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/user | write | content-restrictions | Add user to content restriction. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/restriction/byOperation/{id}/user | write | content-restrictions | Remove user from content restriction. |
| GET | ex/confluence/{id}/wiki/rest/api/content-states | read | content-states | Get Custom Content States. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/state | read | content-states | Get content state. |
| PUT | ex/confluence/{id}/wiki/rest/api/content/{id}/state | write | content-states | Set the content state of a content and publishes a new version of the content. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/state | write | content-states | Removes the content state of a content and publishes a new version. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/state/available | read | content-states | Gets available content states for content. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/state | read | content-states | Get space suggested content states. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/state/content | read | content-states | Get content in space with given content state. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/state/settings | read | content-states | Get content state settings for space. |
| POST | ex/confluence/{id}/wiki/rest/api/content/{id}/version | write | content-versions | Restore content version. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/version/{id} | write | content-versions | Delete content version. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/notification/child-created | read | content-watches | Get watches for page. |
| GET | ex/confluence/{id}/wiki/rest/api/content/{id}/notification/created | read | content-watches | Get watches for space. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/watch | read | content-watches | Get space watchers. |
| GET | ex/confluence/{id}/wiki/rest/api/user/watch/content/{id} | read | content-watches | Get content watch status. |
| POST | ex/confluence/{id}/wiki/rest/api/user/watch/content/{id} | write | content-watches | Add content watcher. |
| DELETE | ex/confluence/{id}/wiki/rest/api/user/watch/content/{id} | write | content-watches | Remove content watcher. |
| GET | ex/confluence/{id}/wiki/rest/api/user/watch/label/{id} | read | content-watches | Get label watch status. |
| POST | ex/confluence/{id}/wiki/rest/api/user/watch/label/{id} | write | content-watches | Add label watcher. |
| DELETE | ex/confluence/{id}/wiki/rest/api/user/watch/label/{id} | write | content-watches | Remove label watcher. |
| GET | ex/confluence/{id}/wiki/rest/api/user/watch/space/{id} | read | content-watches | Get space watch status. |
| POST | ex/confluence/{id}/wiki/rest/api/user/watch/space/{id} | write | content-watches | Add space watcher. |
| DELETE | ex/confluence/{id}/wiki/rest/api/user/watch/space/{id} | write | content-watches | Remove space watch. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/custom-content | read | custom-content | Get custom content by type in blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content | read | custom-content | Get custom content by type. |
| POST | ex/confluence/{id}/wiki/api/v2/custom-content | write | custom-content | Create custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id} | read | custom-content | Get custom content by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/custom-content/{id} | write | custom-content | Update custom content. |
| DELETE | ex/confluence/{id}/wiki/api/v2/custom-content/{id} | write | custom-content | Delete custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/custom-content | read | custom-content | Get custom content by type in page. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/custom-content | read | custom-content | Get custom content by type in space. |
| GET | ex/confluence/{id}/wiki/api/v2/data-policies/metadata | read | data-policies | Get data policy metadata for the workspace. |
| GET | ex/confluence/{id}/wiki/api/v2/data-policies/spaces | read | data-policies | Get spaces with data policies. |
| POST | ex/confluence/{id}/wiki/api/v2/databases | write | database | Create database. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id} | read | database | Get database by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/databases/{id} | write | database | Delete database. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/entries | read | database | Get entries for database. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/entries/{id} | read | database | Get entry by id. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/fields | read | database | Get fields for database. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/views | read | database | Get views for database. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/descendants | read | descendants | Get descendants of a database. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id}/descendants | read | descendants | Get descendants of a smart link. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/descendants | read | descendants | Get descendants of folder. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/descendants | read | descendants | Get descendants of page. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/descendants | read | descendants | Get descendants of a whiteboard. |
| DELETE | ex/confluence/{id}/wiki/rest/api/content/{id}/pageTree | write | experimental | Delete page tree. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/label | read | experimental | Get Space Labels. |
| POST | ex/confluence/{id}/wiki/rest/api/space/{id}/label | write | experimental | Add labels to a space. |
| DELETE | ex/confluence/{id}/wiki/rest/api/space/{id}/label | write | experimental | Remove label from a space. |
| POST | ex/confluence/{id}/wiki/api/v2/folders | write | folder | Create folder. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id} | read | folder | Get folder by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/folders/{id} | write | folder | Delete folder. |
| GET | ex/confluence/{id}/wiki/rest/api/group | read | group | Get groups. |
| POST | ex/confluence/{id}/wiki/rest/api/group | write | group | Create new user group. |
| GET | ex/confluence/{id}/wiki/rest/api/group/by-id | read | group | Get group. |
| DELETE | ex/confluence/{id}/wiki/rest/api/group/by-id | write | group | Delete user group. |
| GET | ex/confluence/{id}/wiki/rest/api/group/picker | read | group | Search groups by partial query. |
| POST | ex/confluence/{id}/wiki/rest/api/group/userByGroupId | write | group | Add member to group by groupId. |
| DELETE | ex/confluence/{id}/wiki/rest/api/group/userByGroupId | write | group | Remove member from group using group id. |
| GET | ex/confluence/{id}/wiki/rest/api/group/{id}/membersByGroupId | read | group | Get group members. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/labels | read | label | Get labels for attachment. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/labels | read | label | Get labels for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/labels | read | label | Get labels for custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/labels | read | label | Get labels. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/labels | read | label | Get labels for page. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/content/labels | read | label | Get labels for space content. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/labels | read | label | Get labels for space. |
| GET | ex/confluence/{id}/wiki/rest/api/label | read | label-info | Get label information. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/likes/count | read | like | Get like count for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/likes/users | read | like | Get account IDs of likes for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/likes/count | read | like | Get like count for footer comment. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/likes/users | read | like | Get account IDs of likes for footer comment. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/likes/count | read | like | Get like count for inline comment. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/likes/users | read | like | Get account IDs of likes for inline comment. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/likes/count | read | like | Get like count for page. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/likes/users | read | like | Get account IDs of likes for page. |
| GET | ex/confluence/{id}/wiki/rest/api/longtask | read | long-running-task | Get long-running tasks. |
| GET | ex/confluence/{id}/wiki/rest/api/longtask/{id} | read | long-running-task | Get long-running task. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/operations | read | operation | Get permitted operations for attachment. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/operations | read | operation | Get permitted operations for blog post. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/operations | read | operation | Get permitted operations for custom content. |
| GET | ex/confluence/{id}/wiki/api/v2/databases/{id}/operations | read | operation | Get permitted operations for a database. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id}/operations | read | operation | Get permitted operations for a Smart Link in the content tree. |
| GET | ex/confluence/{id}/wiki/api/v2/folders/{id}/operations | read | operation | Get permitted operations for a folder. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/operations | read | operation | Get permitted operations for footer comment. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/operations | read | operation | Get permitted operations for inline comment. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/operations | read | operation | Get permitted operations for page. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/operations | read | operation | Get permitted operations for space. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id}/operations | read | operation | Get permitted operations for a whiteboard. |
| GET | ex/confluence/{id}/wiki/api/v2/labels/{id}/pages | read | page | Get pages for label. |
| GET | ex/confluence/{id}/wiki/api/v2/pages | read | page | Get pages. |
| POST | ex/confluence/{id}/wiki/api/v2/pages | write | page | Create page. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id} | read | page | Get page by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/pages/{id} | write | page | Update page. |
| DELETE | ex/confluence/{id}/wiki/api/v2/pages/{id} | write | page | Delete page. |
| PUT | ex/confluence/{id}/wiki/api/v2/pages/{id}/title | write | page | Update page title. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/pages | read | page | Get pages in space. |
| POST | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/redact | write | redactions | Redact Content in a Confluence Blog Post. |
| POST | ex/confluence/{id}/wiki/api/v2/pages/{id}/redact | write | redactions | Redact Content in a Confluence Page. |
| GET | ex/confluence/{id}/wiki/rest/api/relation/{id}/from/{id}/{id}/to/{id} | read | relation | Find target entities related to a source entity. |
| GET | ex/confluence/{id}/wiki/rest/api/relation/{id}/from/{id}/{id}/to/{id}/{id} | read | relation | Find relationship from source to target. |
| PUT | ex/confluence/{id}/wiki/rest/api/relation/{id}/from/{id}/{id}/to/{id}/{id} | write | relation | Create relationship. |
| DELETE | ex/confluence/{id}/wiki/rest/api/relation/{id}/from/{id}/{id}/to/{id}/{id} | write | relation | Delete relationship. |
| GET | ex/confluence/{id}/wiki/rest/api/relation/{id}/to/{id}/{id}/from/{id} | read | relation | Find source entities related to a target entity. |
| GET | ex/confluence/{id}/wiki/rest/api/search | read | search | Search content. |
| GET | ex/confluence/{id}/wiki/rest/api/search/user | read | search | Search users. |
| GET | ex/confluence/{id}/wiki/rest/api/settings/lookandfeel | read | settings | Get look and feel settings. |
| PUT | ex/confluence/{id}/wiki/rest/api/settings/lookandfeel | write | settings | Select look and feel settings. |
| POST | ex/confluence/{id}/wiki/rest/api/settings/lookandfeel/custom | write | settings | Update look and feel settings. |
| DELETE | ex/confluence/{id}/wiki/rest/api/settings/lookandfeel/custom | write | settings | Reset look and feel settings. |
| GET | ex/confluence/{id}/wiki/rest/api/settings/systemInfo | read | settings | Get system info. |
| POST | ex/confluence/{id}/wiki/api/v2/embeds | write | smart-link | Create Smart Link in the content tree. |
| GET | ex/confluence/{id}/wiki/api/v2/embeds/{id} | read | smart-link | Get Smart Link in the content tree by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/embeds/{id} | write | smart-link | Delete Smart Link in the content tree. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces | read | space | Get spaces. |
| POST | ex/confluence/{id}/wiki/api/v2/spaces | write | space | Create space. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id} | read | space | Get space by id. |
| POST | ex/confluence/{id}/wiki/rest/api/space | write | space | Create space. |
| POST | ex/confluence/{id}/wiki/rest/api/space/_private | write | space | Create private space. |
| PUT | ex/confluence/{id}/wiki/rest/api/space/{id} | write | space | Update space. |
| DELETE | ex/confluence/{id}/wiki/rest/api/space/{id} | write | space | Delete space. |
| POST | ex/confluence/{id}/wiki/api/v2/space-permissions/transition/access-removals | write | space-permission-transition | Bulk remove space permission access. |
| GET | ex/confluence/{id}/wiki/api/v2/space-permissions/transition/combinations | read | space-permission-transition | List unassigned space permission combinations. |
| POST | ex/confluence/{id}/wiki/api/v2/space-permissions/transition/combinations | write | space-permission-transition | Generate space permission combinations. |
| POST | ex/confluence/{id}/wiki/api/v2/space-permissions/transition/role-assignments | write | space-permission-transition | Bulk assign space permission roles. |
| GET | ex/confluence/{id}/wiki/api/v2/space-permissions/transition/tasks/{id} | read | space-permission-transition | Get space permission transition task status. |
| GET | ex/confluence/{id}/wiki/api/v2/space-permissions | read | space-permissions | Get available space permissions. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/permissions | read | space-permissions | Get space permissions assignments. |
| POST | ex/confluence/{id}/wiki/rest/api/space/{id}/permission | write | space-permissions | Add new permission to space. |
| POST | ex/confluence/{id}/wiki/rest/api/space/{id}/permission/custom-content | write | space-permissions | Add new custom content permission to space. |
| DELETE | ex/confluence/{id}/wiki/rest/api/space/{id}/permission/{id} | write | space-permissions | Remove a space permission. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties | read | space-properties | Get space properties in space. |
| POST | ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties | write | space-properties | Create space property in space. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties/{id} | read | space-properties | Get space property by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties/{id} | write | space-properties | Update space property by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/spaces/{id}/properties/{id} | write | space-properties | Delete space property by id. |
| GET | ex/confluence/{id}/wiki/api/v2/space-role-mode | read | space-roles | Get space role mode. |
| GET | ex/confluence/{id}/wiki/api/v2/space-roles | read | space-roles | Get available space roles. |
| POST | ex/confluence/{id}/wiki/api/v2/space-roles | write | space-roles | Create a space role. |
| GET | ex/confluence/{id}/wiki/api/v2/space-roles/{id} | read | space-roles | Get space role by ID. |
| PUT | ex/confluence/{id}/wiki/api/v2/space-roles/{id} | write | space-roles | Update a space role. |
| DELETE | ex/confluence/{id}/wiki/api/v2/space-roles/{id} | write | space-roles | Delete a space role. |
| GET | ex/confluence/{id}/wiki/api/v2/spaces/{id}/role-assignments | read | space-roles | Get space role assignments. |
| POST | ex/confluence/{id}/wiki/api/v2/spaces/{id}/role-assignments | write | space-roles | Set space role assignments. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/settings | read | space-settings | Get space settings. |
| PUT | ex/confluence/{id}/wiki/rest/api/space/{id}/settings | write | space-settings | Update space settings. |
| GET | ex/confluence/{id}/wiki/api/v2/tasks | read | task | Get tasks. |
| GET | ex/confluence/{id}/wiki/api/v2/tasks/{id} | read | task | Get task by id. |
| PUT | ex/confluence/{id}/wiki/api/v2/tasks/{id} | write | task | Update task. |
| POST | ex/confluence/{id}/wiki/rest/api/template | write | template | Create content template. |
| PUT | ex/confluence/{id}/wiki/rest/api/template | write | template | Update content template. |
| GET | ex/confluence/{id}/wiki/rest/api/template/blueprint | read | template | Get blueprint templates. |
| GET | ex/confluence/{id}/wiki/rest/api/template/page | read | template | Get content templates. |
| GET | ex/confluence/{id}/wiki/rest/api/template/{id} | read | template | Get content template. |
| DELETE | ex/confluence/{id}/wiki/rest/api/template/{id} | write | template | Remove template. |
| GET | ex/confluence/{id}/wiki/rest/api/settings/theme | read | themes | Get themes. |
| GET | ex/confluence/{id}/wiki/rest/api/settings/theme/selected | read | themes | Get global theme. |
| GET | ex/confluence/{id}/wiki/rest/api/settings/theme/{id} | read | themes | Get theme. |
| GET | ex/confluence/{id}/wiki/rest/api/space/{id}/theme | read | themes | Get space theme. |
| PUT | ex/confluence/{id}/wiki/rest/api/space/{id}/theme | write | themes | Set space theme. |
| DELETE | ex/confluence/{id}/wiki/rest/api/space/{id}/theme | write | themes | Reset space theme. |
| POST | ex/confluence/{id}/wiki/api/v2/user/access/check-access-by-email | read | user | Check site access for a list of emails. |
| POST | ex/confluence/{id}/wiki/api/v2/user/access/invite-by-email | write | user | Invite a list of emails to the site. |
| POST | ex/confluence/{id}/wiki/api/v2/users-bulk | read | user | Create bulk user lookup using ids. |
| GET | ex/confluence/{id}/wiki/rest/api/user/{id}/property | read | user-properties | Get user properties. |
| GET | ex/confluence/{id}/wiki/rest/api/user/{id}/property/{id} | read | user-properties | Get user property. |
| POST | ex/confluence/{id}/wiki/rest/api/user/{id}/property/{id} | write | user-properties | Create user property by key. |
| PUT | ex/confluence/{id}/wiki/rest/api/user/{id}/property/{id} | write | user-properties | Update user property. |
| DELETE | ex/confluence/{id}/wiki/rest/api/user/{id}/property/{id} | write | user-properties | Delete user property. |
| GET | ex/confluence/{id}/wiki/rest/api/user | read | users | Get user. |
| GET | ex/confluence/{id}/wiki/rest/api/user/anonymous | read | users | Get anonymous user. |
| GET | ex/confluence/{id}/wiki/rest/api/user/bulk | read | users | Get multiple users using ids. |
| GET | ex/confluence/{id}/wiki/rest/api/user/current | read | users | Get current user. |
| GET | ex/confluence/{id}/wiki/rest/api/user/email | read | users | Get user email address. |
| GET | ex/confluence/{id}/wiki/rest/api/user/email/bulk | read | users | Get user email addresses in batch. |
| GET | ex/confluence/{id}/wiki/rest/api/user/memberof | read | users | Get group memberships for user. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/versions | read | version | Get attachment versions. |
| GET | ex/confluence/{id}/wiki/api/v2/attachments/{id}/versions/{id} | read | version | Get version details for attachment version. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/versions | read | version | Get blog post versions. |
| GET | ex/confluence/{id}/wiki/api/v2/blogposts/{id}/versions/{id} | read | version | Get version details for blog post version. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/versions | read | version | Get custom content versions. |
| GET | ex/confluence/{id}/wiki/api/v2/custom-content/{id}/versions/{id} | read | version | Get version details for custom content version. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/versions | read | version | Get footer comment versions. |
| GET | ex/confluence/{id}/wiki/api/v2/footer-comments/{id}/versions/{id} | read | version | Get version details for footer comment version. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/versions | read | version | Get inline comment versions. |
| GET | ex/confluence/{id}/wiki/api/v2/inline-comments/{id}/versions/{id} | read | version | Get version details for inline comment version. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/versions | read | version | Get page versions. |
| GET | ex/confluence/{id}/wiki/api/v2/pages/{id}/versions/{id} | read | version | Get version details for page version. |
| POST | ex/confluence/{id}/wiki/api/v2/whiteboards | write | whiteboard | Create whiteboard. |
| GET | ex/confluence/{id}/wiki/api/v2/whiteboards/{id} | read | whiteboard | Get whiteboard by id. |
| DELETE | ex/confluence/{id}/wiki/api/v2/whiteboards/{id} | write | whiteboard | Delete whiteboard. |
