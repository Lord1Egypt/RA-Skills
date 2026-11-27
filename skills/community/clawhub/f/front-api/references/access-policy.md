# Front access policy

An access policy limits which endpoints Front connections may call through Maton. Front doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/front#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Front: its 124 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create front --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "accounts"},
    {"method": "GET", "path": "accounts/custom_fields"},
    {"method": "GET", "path": "accounts/{id}"},
    {"method": "GET", "path": "accounts/{id}/contacts"},
    {"method": "GET", "path": "analytics/exports/{id}"},
    {"method": "GET", "path": "analytics/reports/{id}"},
    {"method": "GET", "path": "download/{id}"},
    {"method": "GET", "path": "channels"},
    {"method": "GET", "path": "channels/{id}"},
    {"method": "GET", "path": "teammates/{id}/channels"},
    {"method": "GET", "path": "teams/{id}/channels"},
    {"method": "GET", "path": "comments/{id}"},
    {"method": "GET", "path": "comments/{id}/download/{id}"},
    {"method": "GET", "path": "comments/{id}/mentions"},
    {"method": "GET", "path": "company/rules"},
    {"method": "GET", "path": "company/statuses"},
    {"method": "GET", "path": "company/statuses/{id}"},
    {"method": "GET", "path": "company/tags"},
    {"method": "GET", "path": "me"},
    {"method": "GET", "path": "contact_groups"},
    {"method": "GET", "path": "contact_groups/{id}/contacts"},
    {"method": "GET", "path": "teammates/{id}/contact_groups"},
    {"method": "GET", "path": "teams/{id}/contact_groups"},
    {"method": "GET", "path": "contact_lists"},
    {"method": "GET", "path": "contact_lists/{id}/contacts"},
    {"method": "GET", "path": "teammates/{id}/contact_lists"},
    {"method": "GET", "path": "teams/{id}/contact_lists"},
    {"method": "GET", "path": "contacts"},
    {"method": "GET", "path": "contacts/custom_fields"},
    {"method": "GET", "path": "contacts/{id}"},
    {"method": "GET", "path": "contacts/{id}/conversations"},
    {"method": "GET", "path": "contacts/{id}/notes"},
    {"method": "GET", "path": "teammates/{id}/contacts"},
    {"method": "GET", "path": "teams/{id}/contacts"},
    {"method": "GET", "path": "conversations"},
    {"method": "GET", "path": "conversations/custom_fields"},
    {"method": "GET", "path": "conversations/search/{id}"},
    {"method": "GET", "path": "conversations/{id}"},
    {"method": "GET", "path": "conversations/{id}/comments"},
    {"method": "GET", "path": "conversations/{id}/drafts"},
    {"method": "GET", "path": "conversations/{id}/events"},
    {"method": "GET", "path": "conversations/{id}/followers"},
    {"method": "GET", "path": "conversations/{id}/inboxes"},
    {"method": "GET", "path": "conversations/{id}/linked_conversations"},
    {"method": "GET", "path": "conversations/{id}/messages"},
    {"method": "GET", "path": "teammates/{id}/conversations"},
    {"method": "GET", "path": "custom_fields"},
    {"method": "GET", "path": "events"},
    {"method": "GET", "path": "events/{id}"},
    {"method": "GET", "path": "inboxes"},
    {"method": "GET", "path": "inboxes/custom_fields"},
    {"method": "GET", "path": "inboxes/{id}"},
    {"method": "GET", "path": "inboxes/{id}/channels"},
    {"method": "GET", "path": "inboxes/{id}/conversations"},
    {"method": "GET", "path": "inboxes/{id}/teammates"},
    {"method": "GET", "path": "teammates/{id}/inboxes"},
    {"method": "GET", "path": "teams/{id}/inboxes"},
    {"method": "GET", "path": "knowledge_base_articles/{id}"},
    {"method": "GET", "path": "knowledge_base_articles/{id}/content"},
    {"method": "GET", "path": "knowledge_base_articles/{id}/download/{id}"},
    {"method": "GET", "path": "knowledge_base_articles/{id}/locales/{id}/content"},
    {"method": "GET", "path": "knowledge_base_categories/{id}"},
    {"method": "GET", "path": "knowledge_base_categories/{id}/articles"},
    {"method": "GET", "path": "knowledge_base_categories/{id}/content"},
    {"method": "GET", "path": "knowledge_base_categories/{id}/locales/{id}/content"},
    {"method": "GET", "path": "knowledge_bases"},
    {"method": "GET", "path": "knowledge_bases/{id}"},
    {"method": "GET", "path": "knowledge_bases/{id}/articles"},
    {"method": "GET", "path": "knowledge_bases/{id}/categories"},
    {"method": "GET", "path": "knowledge_bases/{id}/content"},
    {"method": "GET", "path": "knowledge_bases/{id}/locales/{id}/content"},
    {"method": "GET", "path": "links"},
    {"method": "GET", "path": "links/custom_fields"},
    {"method": "GET", "path": "links/{id}"},
    {"method": "GET", "path": "links/{id}/conversations"},
    {"method": "GET", "path": "message_template_folders"},
    {"method": "GET", "path": "message_template_folders/{id}"},
    {"method": "GET", "path": "message_template_folders/{id}/message_template_folders"},
    {"method": "GET", "path": "message_template_folders/{id}/message_templates"},
    {"method": "GET", "path": "teammates/{id}/message_template_folders"},
    {"method": "GET", "path": "teams/{id}/message_template_folders"},
    {"method": "GET", "path": "message_templates"},
    {"method": "GET", "path": "message_templates/{id}"},
    {"method": "GET", "path": "message_templates/{id}/download/{id}"},
    {"method": "GET", "path": "teammates/{id}/message_templates"},
    {"method": "GET", "path": "teams/{id}/message_templates"},
    {"method": "GET", "path": "messages/{id}"},
    {"method": "GET", "path": "messages/{id}/download/{id}"},
    {"method": "GET", "path": "messages/{id}/seen"},
    {"method": "GET", "path": "teammates/{id}/private_inboxes"},
    {"method": "GET", "path": "rules"},
    {"method": "GET", "path": "rules/{id}"},
    {"method": "GET", "path": "teammates/{id}/rules"},
    {"method": "GET", "path": "teams/{id}/rules"},
    {"method": "GET", "path": "shifts"},
    {"method": "GET", "path": "shifts/{id}"},
    {"method": "GET", "path": "shifts/{id}/teammates"},
    {"method": "GET", "path": "teammates/{id}/shifts"},
    {"method": "GET", "path": "teams/{id}/shifts"},
    {"method": "GET", "path": "signatures/{id}"},
    {"method": "GET", "path": "teammates/{id}/signatures"},
    {"method": "GET", "path": "teams/{id}/signatures"},
    {"method": "GET", "path": "tags"},
    {"method": "GET", "path": "tags/{id}"},
    {"method": "GET", "path": "tags/{id}/children"},
    {"method": "GET", "path": "tags/{id}/conversations"},
    {"method": "GET", "path": "teammates/{id}/tags"},
    {"method": "GET", "path": "teams/{id}/tags"},
    {"method": "GET", "path": "teammate_groups"},
    {"method": "GET", "path": "teammate_groups/{id}"},
    {"method": "GET", "path": "teammate_groups/{id}/inboxes"},
    {"method": "GET", "path": "teammate_groups/{id}/teammates"},
    {"method": "GET", "path": "teammate_groups/{id}/teams"},
    {"method": "GET", "path": "teammates"},
    {"method": "GET", "path": "teammates/custom_fields"},
    {"method": "GET", "path": "teammates/{id}"},
    {"method": "GET", "path": "teams"},
    {"method": "GET", "path": "teams/{id}"},
    {"method": "GET", "path": "teammates/{id}/time_offs"},
    {"method": "GET", "path": "teams/{id}/time_offs"},
    {"method": "GET", "path": "time_offs/{id}"},
    {"method": "GET", "path": "teams/{id}/views"},
    {"method": "GET", "path": "views"},
    {"method": "GET", "path": "views/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Front endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | accounts | read | accounts | List Accounts. |
| POST | accounts | write | accounts | Create account. |
| GET | accounts/custom_fields | read | accounts | List Account's custom fields. |
| GET | accounts/{id} | read | accounts | Fetch an account. |
| PATCH | accounts/{id} | write | accounts | Update account. |
| DELETE | accounts/{id} | write | accounts | Delete an account. |
| GET | accounts/{id}/contacts | read | accounts | List account contacts. |
| POST | accounts/{id}/contacts | write | accounts | Add contact to Account. |
| DELETE | accounts/{id}/contacts | write | accounts | Remove contact from Account. |
| POST | analytics/exports | write | analytics | Create a new analytics export. Kept out of read: starts an export job. |
| GET | analytics/exports/{id} | read | analytics | Fetch an analytics export. |
| POST | analytics/reports | write | analytics | Create a new analytics report. Kept out of read: starts a report job. |
| GET | analytics/reports/{id} | read | analytics | Fetch an analytics report. |
| POST | applications/{id}/events | write | applications | Trigger application event. |
| GET | download/{id} | read | attachments | Download attachment. |
| GET | channels | read | channels | List channels. |
| GET | channels/{id} | read | channels | Get channel. |
| PATCH | channels/{id} | write | channels | Update Channel. |
| POST | channels/{id}/drafts | write | channels | Create draft. |
| POST | channels/{id}/incoming_messages | write | channels | Receive custom messages. |
| POST | channels/{id}/messages | write | channels | Create message. |
| POST | channels/{id}/validate | write | channels | Validate channel. |
| GET | teammates/{id}/channels | read | channels | List teammate channels. |
| GET | teams/{id}/channels | read | channels | List team channels. |
| GET | comments/{id} | read | comments | Get comment. |
| PATCH | comments/{id} | write | comments | Update comment. |
| GET | comments/{id}/download/{id} | read | comments | Download attachment for a comment. |
| GET | comments/{id}/mentions | read | comments | List comment mentions. |
| POST | comments/{id}/replies | write | comments | Add comment reply. |
| GET | company/rules | read | company | List all company rules. |
| GET | company/statuses | read | company | List company ticket statuses. |
| GET | company/statuses/{id} | read | company | Get ticket status. |
| GET | company/tags | read | company | List company tags. |
| POST | company/tags | write | company | Create company tag. |
| GET | me | read | company | Fetch the details of the API token. |
| GET | contact_groups | read | contact groups | List groups. |
| POST | contact_groups | write | contact groups | Create group. |
| DELETE | contact_groups/{id} | write | contact groups | Delete group. |
| GET | contact_groups/{id}/contacts | read | contact groups | List contacts in group. |
| POST | contact_groups/{id}/contacts | write | contact groups | Add contacts to group. |
| DELETE | contact_groups/{id}/contacts | write | contact groups | Remove contacts from group. |
| GET | teammates/{id}/contact_groups | read | contact groups | List teammate groups. |
| POST | teammates/{id}/contact_groups | write | contact groups | Create teammate group. |
| GET | teams/{id}/contact_groups | read | contact groups | List team groups. |
| POST | teams/{id}/contact_groups | write | contact groups | Create team group. |
| GET | contact_lists | read | contact lists | List contact lists. |
| POST | contact_lists | write | contact lists | Create contact list. |
| DELETE | contact_lists/{id} | write | contact lists | Delete contact list. |
| GET | contact_lists/{id}/contacts | read | contact lists | List contacts in contact list. |
| POST | contact_lists/{id}/contacts | write | contact lists | Add contacts to contact list. |
| DELETE | contact_lists/{id}/contacts | write | contact lists | Remove contacts from contact list. |
| GET | teammates/{id}/contact_lists | read | contact lists | List teammate contact lists. |
| POST | teammates/{id}/contact_lists | write | contact lists | Create teammate contact list. |
| GET | teams/{id}/contact_lists | read | contact lists | List team contact lists. |
| POST | teams/{id}/contact_lists | write | contact lists | Create team contact list. |
| GET | contacts | read | contacts | List contacts. |
| POST | contacts | write | contacts | Create contact. |
| GET | contacts/custom_fields | read | contacts | List Contact's custom fields. |
| POST | contacts/merge | write | contacts | Merge contacts. |
| GET | contacts/{id} | read | contacts | Get contact. |
| PATCH | contacts/{id} | write | contacts | Update a contact. |
| DELETE | contacts/{id} | write | contacts | Delete a contact. |
| GET | contacts/{id}/conversations | read | contacts | List contact conversations. |
| POST | contacts/{id}/handles | write | contacts | Add contact handle. |
| DELETE | contacts/{id}/handles | write | contacts | Delete contact handle. |
| GET | contacts/{id}/notes | read | contacts | List notes. |
| POST | contacts/{id}/notes | write | contacts | Add note. |
| GET | teammates/{id}/contacts | read | contacts | List teammate contacts. |
| POST | teammates/{id}/contacts | write | contacts | Create teammate contact. |
| GET | teams/{id}/contacts | read | contacts | List team contacts. |
| POST | teams/{id}/contacts | write | contacts | Create team contact. |
| GET | conversations | read | conversations | List conversations. |
| POST | conversations | write | conversations | Create discussion/task conversation. |
| GET | conversations/custom_fields | read | conversations | List Conversation's custom fields. |
| GET | conversations/search/{id} | read | conversations | Search conversations. |
| GET | conversations/{id} | read | conversations | Get conversation. |
| PATCH | conversations/{id} | write | conversations | Update conversation. |
| DELETE | conversations/{id} | write | conversations | Delete conversation. |
| PUT | conversations/{id}/assignee | write | conversations | Update conversation assignee. |
| GET | conversations/{id}/comments | read | conversations | List conversation comments. |
| POST | conversations/{id}/comments | write | conversations | Add comment. |
| GET | conversations/{id}/drafts | read | conversations | List conversation drafts. |
| POST | conversations/{id}/drafts | write | conversations | Create draft reply. |
| GET | conversations/{id}/events | read | conversations | List conversation events. |
| GET | conversations/{id}/followers | read | conversations | List conversation followers. |
| POST | conversations/{id}/followers | write | conversations | Add conversation followers. |
| DELETE | conversations/{id}/followers | write | conversations | Delete conversation followers. |
| GET | conversations/{id}/inboxes | read | conversations | List conversation inboxes. |
| GET | conversations/{id}/linked_conversations | read | conversations | List linked conversations. |
| POST | conversations/{id}/linked_conversations | write | conversations | Link conversations. |
| POST | conversations/{id}/links | write | conversations | Add conversation link. |
| DELETE | conversations/{id}/links | write | conversations | Remove conversation links. |
| GET | conversations/{id}/messages | read | conversations | List conversation messages. |
| POST | conversations/{id}/messages | write | conversations | Create message reply. |
| PATCH | conversations/{id}/reminders | write | conversations | Update conversation reminders. |
| POST | conversations/{id}/tags | write | conversations | Add conversation tag. |
| DELETE | conversations/{id}/tags | write | conversations | Remove conversation tag. |
| GET | teammates/{id}/conversations | read | conversations | List assigned conversations. |
| GET | custom_fields | read | custom fields | List Contact's custom fields. |
| PATCH | drafts/{id} | write | drafts | Edit draft. |
| DELETE | drafts/{id} | write | drafts | Delete draft. |
| GET | events | read | events | List events. |
| GET | events/{id} | read | events | Get event. |
| GET | inboxes | read | inboxes | List inboxes. |
| POST | inboxes | write | inboxes | Create inbox. |
| GET | inboxes/custom_fields | read | inboxes | List Inbox's custom fields. |
| GET | inboxes/{id} | read | inboxes | Get inbox. |
| PATCH | inboxes/{id} | write | inboxes | Update inbox. |
| GET | inboxes/{id}/channels | read | inboxes | List inbox channels. |
| POST | inboxes/{id}/channels | write | inboxes | Create a channel. |
| GET | inboxes/{id}/conversations | read | inboxes | List inbox conversations. |
| POST | inboxes/{id}/imported_messages | write | inboxes | Import message. |
| GET | inboxes/{id}/teammates | read | inboxes | List inbox access. |
| POST | inboxes/{id}/teammates | write | inboxes | Add inbox access. |
| DELETE | inboxes/{id}/teammates | write | inboxes | Removes inbox access. |
| GET | teammates/{id}/inboxes | read | inboxes | List teammate inboxes. |
| GET | teams/{id}/inboxes | read | inboxes | List team inboxes. |
| POST | teams/{id}/inboxes | write | inboxes | Create team inbox. |
| GET | knowledge_base_articles/{id} | read | knowledge bases | Get a knowledge base article. |
| DELETE | knowledge_base_articles/{id} | write | knowledge bases | Delete an article. |
| GET | knowledge_base_articles/{id}/content | read | knowledge bases | Get knowledge base article with content in default locale. |
| PATCH | knowledge_base_articles/{id}/content | write | knowledge bases | Update article content in default locale. |
| GET | knowledge_base_articles/{id}/download/{id} | read | knowledge bases | Download attachment from an article. |
| GET | knowledge_base_articles/{id}/locales/{id}/content | read | knowledge bases | Get knowledge base article with content in specified locale. |
| PATCH | knowledge_base_articles/{id}/locales/{id}/content | write | knowledge bases | Update article content in specified locale. |
| GET | knowledge_base_categories/{id} | read | knowledge bases | Get a knowledge base category. |
| DELETE | knowledge_base_categories/{id} | write | knowledge bases | Delete a knowledge base category. |
| GET | knowledge_base_categories/{id}/articles | read | knowledge bases | List articles in a category. |
| GET | knowledge_base_categories/{id}/content | read | knowledge bases | Get knowledge base category content in default locale. |
| PATCH | knowledge_base_categories/{id}/content | write | knowledge bases | Update knowledge base category in default locale. |
| GET | knowledge_base_categories/{id}/locales/{id}/content | read | knowledge bases | Get knowledge base category with content in specified locale. |
| PATCH | knowledge_base_categories/{id}/locales/{id}/content | write | knowledge bases | Update knowledge base category in specified locale. |
| GET | knowledge_bases | read | knowledge bases | List knowledge bases. |
| POST | knowledge_bases | write | knowledge bases | Create a knowledge base. |
| GET | knowledge_bases/{id} | read | knowledge bases | Get a knowledge base. |
| GET | knowledge_bases/{id}/articles | read | knowledge bases | List articles in a knowledge base. |
| POST | knowledge_bases/{id}/articles | write | knowledge bases | Create article in a knowledge base in default locale. |
| GET | knowledge_bases/{id}/categories | read | knowledge bases | List categories in a knowledge base. |
| POST | knowledge_bases/{id}/categories | write | knowledge bases | Create knowledge base category in default locale. |
| GET | knowledge_bases/{id}/content | read | knowledge bases | Get a knowledge base with content in default locale. |
| PATCH | knowledge_bases/{id}/content | write | knowledge bases | Update knowledge base in default locale. |
| POST | knowledge_bases/{id}/locales/{id}/articles | write | knowledge bases | Create article in a knowledge base in specified locale. |
| POST | knowledge_bases/{id}/locales/{id}/categories | write | knowledge bases | Create knowledge base category in specified locale. |
| GET | knowledge_bases/{id}/locales/{id}/content | read | knowledge bases | Get a knowledge base with content in specified locale. |
| PATCH | knowledge_bases/{id}/locales/{id}/content | write | knowledge bases | Update knowledge base in specified locale. |
| GET | links | read | links | List links. |
| POST | links | write | links | Create link. |
| GET | links/custom_fields | read | links | List Link's custom fields. |
| GET | links/{id} | read | links | Get link. |
| PATCH | links/{id} | write | links | Update a link. |
| GET | links/{id}/conversations | read | links | List link conversations. |
| GET | message_template_folders | read | message template folders | List folders. |
| POST | message_template_folders | write | message template folders | Create folder. |
| GET | message_template_folders/{id} | read | message template folders | Get folder. |
| PATCH | message_template_folders/{id} | write | message template folders | Update folder. |
| DELETE | message_template_folders/{id} | write | message template folders | Delete folder. |
| GET | message_template_folders/{id}/message_template_folders | read | message template folders | Get child folders. |
| POST | message_template_folders/{id}/message_template_folders | write | message template folders | Create child folder. |
| GET | message_template_folders/{id}/message_templates | read | message template folders | Get child templates. |
| POST | message_template_folders/{id}/message_templates | write | message template folders | Create child template. |
| GET | teammates/{id}/message_template_folders | read | message template folders | List teammate folders. |
| POST | teammates/{id}/message_template_folders | write | message template folders | Create teammate folder. |
| GET | teams/{id}/message_template_folders | read | message template folders | List team folders. |
| POST | teams/{id}/message_template_folders | write | message template folders | Create team folder. |
| GET | message_templates | read | message templates | List message templates. |
| POST | message_templates | write | message templates | Create message template. |
| GET | message_templates/{id} | read | message templates | Get message template. |
| PATCH | message_templates/{id} | write | message templates | Update message template. |
| DELETE | message_templates/{id} | write | message templates | Delete message template. |
| GET | message_templates/{id}/download/{id} | read | message templates | Download attachment for a message template. |
| GET | teammates/{id}/message_templates | read | message templates | List teammate message templates. |
| POST | teammates/{id}/message_templates | write | message templates | Create teammate message template. |
| GET | teams/{id}/message_templates | read | message templates | List team message templates. |
| POST | teams/{id}/message_templates | write | message templates | Create team message template. |
| GET | messages/{id} | read | messages | Get message. |
| GET | messages/{id}/download/{id} | read | messages | Download attachment for a message. |
| GET | messages/{id}/seen | read | messages | Get message seen status. |
| POST | messages/{id}/seen | write | messages | Mark message seen. |
| GET | teammates/{id}/private_inboxes | read | private inboxes | List teammate private inboxes. |
| POST | teammates/{id}/private_inboxes | write | private inboxes | Create teammate private inbox. |
| GET | rules | read | rules | List rules. |
| GET | rules/{id} | read | rules | Get rule. |
| GET | teammates/{id}/rules | read | rules | List teammate rules. |
| GET | teams/{id}/rules | read | rules | List team rules. |
| GET | shifts | read | shifts | List Shifts. |
| POST | shifts | write | shifts | Create shift. |
| GET | shifts/{id} | read | shifts | Get shift. |
| PATCH | shifts/{id} | write | shifts | Update shift. |
| GET | shifts/{id}/teammates | read | shifts | List shift's teammates. |
| POST | shifts/{id}/teammates | write | shifts | Add teammates to shift. |
| DELETE | shifts/{id}/teammates | write | shifts | Remove teammates from shift. |
| GET | teammates/{id}/shifts | read | shifts | List Teammate Shifts. |
| GET | teams/{id}/shifts | read | shifts | List team Shifts. |
| POST | teams/{id}/shifts | write | shifts | Create team shift. |
| GET | signatures/{id} | read | signatures | Get signatures. |
| PATCH | signatures/{id} | write | signatures | Update signature. |
| DELETE | signatures/{id} | write | signatures | Delete signature. |
| GET | teammates/{id}/signatures | read | signatures | List teammate signatures. |
| POST | teammates/{id}/signatures | write | signatures | Create teammate signature. |
| GET | teams/{id}/signatures | read | signatures | List team signatures. |
| POST | teams/{id}/signatures | write | signatures | Create team signature. |
| GET | tags | read | tags | List tags. |
| POST | tags | write | tags | Create tag. |
| GET | tags/{id} | read | tags | Get tag. |
| PATCH | tags/{id} | write | tags | Update a tag. |
| DELETE | tags/{id} | write | tags | Delete tag. |
| GET | tags/{id}/children | read | tags | List tag children. |
| POST | tags/{id}/children | write | tags | Create child tag. |
| GET | tags/{id}/conversations | read | tags | List tagged conversations. |
| GET | teammates/{id}/tags | read | tags | List teammate tags. |
| POST | teammates/{id}/tags | write | tags | Create teammate tag. |
| GET | teams/{id}/tags | read | tags | List team tags. |
| POST | teams/{id}/tags | write | tags | Create team tag. |
| GET | teammate_groups | read | teammate groups | List teammate groups. |
| POST | teammate_groups | write | teammate groups | Create teammate group. |
| GET | teammate_groups/{id} | read | teammate groups | Get teammate group. |
| PATCH | teammate_groups/{id} | write | teammate groups | Update a teammate group. |
| DELETE | teammate_groups/{id} | write | teammate groups | Delete teammate group. |
| GET | teammate_groups/{id}/inboxes | read | teammate groups | List teammate group team inboxes. |
| POST | teammate_groups/{id}/inboxes | write | teammate groups | Add teammate group team inboxes. |
| DELETE | teammate_groups/{id}/inboxes | write | teammate groups | Remove teammate group team inboxes. |
| GET | teammate_groups/{id}/teammates | read | teammate groups | List teammate group teammates. |
| POST | teammate_groups/{id}/teammates | write | teammate groups | Add teammate group teammates. |
| DELETE | teammate_groups/{id}/teammates | write | teammate groups | Remove teammate group teammates. |
| GET | teammate_groups/{id}/teams | read | teammate groups | List teammate group teams. |
| POST | teammate_groups/{id}/teams | write | teammate groups | Add teammate group teams. |
| DELETE | teammate_groups/{id}/teams | write | teammate groups | Remove teammate group teams. |
| GET | teammates | read | teammates | List teammates. |
| GET | teammates/custom_fields | read | teammates | List Teammate's custom fields. |
| GET | teammates/{id} | read | teammates | Get teammate. |
| PATCH | teammates/{id} | write | teammates | Update teammate. |
| POST | teams/{id}/teammates | write | teammates | Add teammates to team. |
| DELETE | teams/{id}/teammates | write | teammates | Remove teammates from team. |
| GET | teams | read | teams | List teams. |
| GET | teams/{id} | read | teams | Get team. |
| GET | teammates/{id}/time_offs | read | time offs | List teammate time offs. |
| POST | teammates/{id}/time_offs | write | time offs | Create time off. |
| GET | teams/{id}/time_offs | read | time offs | List team time offs. |
| GET | time_offs/{id} | read | time offs | Get time off. |
| PATCH | time_offs/{id} | write | time offs | Update time off. |
| DELETE | time_offs/{id} | write | time offs | Delete time off. |
| GET | teams/{id}/views | read | views | List team views. |
| POST | teams/{id}/views | write | views | Create team view. |
| GET | views | read | views | List views. |
| GET | views/{id} | read | views | Get view. |
| PATCH | views/{id} | write | views | Update view. |
| POST | views/{id}/teammates | write | views | Add view to teammate sidebars. |
