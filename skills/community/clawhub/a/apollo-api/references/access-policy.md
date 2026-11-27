# Apollo access policy

An access policy limits which endpoints Apollo connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/apollo#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Apollo: its 43 read-only endpoints, plus deny rules for the 1 write endpoint a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create apollo --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/account_stages"},
    {"method": "POST", "path": "v1/accounts/search"},
    {"method": "GET", "path": "v1/accounts/{id}"},
    {"method": "POST", "path": "v1/agents/poll_task"},
    {"method": "GET", "path": "v1/contact_stages"},
    {"method": "POST", "path": "v1/contacts/search"},
    {"method": "GET", "path": "v1/contacts/{id}"},
    {"method": "GET", "path": "v1/contacts/{id}/find_potential_duplicate"},
    {"method": "POST", "path": "v1/contacts/{id}/opportunities"},
    {"method": "GET", "path": "v1/conversations/export/{id}"},
    {"method": "POST", "path": "v1/conversations/search"},
    {"method": "GET", "path": "v1/conversations/{id}"},
    {"method": "GET", "path": "v1/duplicate_contacts/merge_jobs/{id}"},
    {"method": "GET", "path": "v1/email_accounts"},
    {"method": "POST", "path": "v1/emailer_campaigns/activity_feed"},
    {"method": "POST", "path": "v1/emailer_campaigns/search"},
    {"method": "POST", "path": "v1/emailer_messages/email_send_status"},
    {"method": "POST", "path": "v1/emailer_messages/get_content"},
    {"method": "GET", "path": "v1/emailer_messages/search"},
    {"method": "GET", "path": "v1/emailer_messages/{id}/activities"},
    {"method": "GET", "path": "v1/emailer_schedules"},
    {"method": "GET", "path": "v1/fields"},
    {"method": "GET", "path": "v1/labels"},
    {"method": "POST", "path": "v1/mixed_companies/search"},
    {"method": "POST", "path": "v1/mixed_people/api_search"},
    {"method": "POST", "path": "v1/news_articles/search"},
    {"method": "GET", "path": "v1/notes"},
    {"method": "GET", "path": "v1/opportunities/search"},
    {"method": "GET", "path": "v1/opportunities/{id}"},
    {"method": "GET", "path": "v1/opportunity_stages"},
    {"method": "GET", "path": "v1/organizations/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/job_postings"},
    {"method": "GET", "path": "v1/people/{id}"},
    {"method": "GET", "path": "v1/phone_calls/search"},
    {"method": "POST", "path": "v1/reports/sync_report"},
    {"method": "POST", "path": "v1/tasks/search"},
    {"method": "GET", "path": "v1/tasks/{id}"},
    {"method": "GET", "path": "v1/typed_custom_fields"},
    {"method": "POST", "path": "v1/usage_stats/api_usage_stats"},
    {"method": "POST", "path": "v1/usage_stats/credit_usage_stats"},
    {"method": "GET", "path": "v1/users/api_profile"},
    {"method": "GET", "path": "v1/users/search"},
    {"method": "GET", "path": "v1/webhook_result/{id}"}
  ],
  "deny": [
    {"method": "GET", "path": "v1/organizations/enrich"}
  ]
}
```

## Endpoints

The Apollo endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/account_stages | read | account_stages | List account stages. |
| POST | v1/accounts | write | accounts | Create an account. |
| POST | v1/accounts/bulk_create | write | accounts | Bulk create accounts. |
| POST | v1/accounts/bulk_update | write | accounts | Bulk update accounts. |
| POST | v1/accounts/search | read | accounts | Search for accounts. |
| POST | v1/accounts/update_owners | write | accounts | Update account owner for multiple accounts. |
| GET | v1/accounts/{id} | read | accounts | View an account. |
| PATCH | v1/accounts/{id} | write | accounts | Update an account. |
| POST | v1/agents/poll_task | read | agents | Poll an Assistant task. |
| POST | v1/agents/task | write | agents | Run an Assistant task. |
| GET | v1/contact_stages | read | contact_stages | List contact stages. |
| POST | v1/contacts | write | contacts | Create a contact. |
| POST | v1/contacts/bulk_create | write | contacts | Bulk create contacts. |
| POST | v1/contacts/bulk_update | write | contacts | Bulk update contacts. |
| POST | v1/contacts/search | read | contacts | Search for contacts. |
| POST | v1/contacts/update_owners | write | contacts | Update contact owner for multiple contacts. |
| POST | v1/contacts/update_stages | write | contacts | Update contact stage for multiple contacts. |
| GET | v1/contacts/{id} | read | contacts | View a contact. |
| PATCH | v1/contacts/{id} | write | contacts | Update a contact. |
| GET | v1/contacts/{id}/find_potential_duplicate | read | contacts | Find a potential duplicate contact. |
| POST | v1/contacts/{id}/opportunities | read | contacts | View associated deals. |
| POST | v1/conversations/export | write | conversations | Export conversations. |
| GET | v1/conversations/export/{id} | read | conversations | Get conversations export. |
| POST | v1/conversations/search | read | conversations | Search conversations. |
| GET | v1/conversations/{id} | read | conversations | Get conversations info. |
| POST | v1/duplicate_contacts/merge | write | duplicate_contacts | [BETA] Merge duplicate contacts. |
| GET | v1/duplicate_contacts/merge_jobs/{id} | read | duplicate_contacts | [BETA] View a contact merge job. |
| GET | v1/email_accounts | read | email_accounts | Get a list of email accounts. |
| POST | v1/emailer_campaigns/activity_feed | read | emailer_campaigns | Get contact sequence activity. |
| POST | v1/emailer_campaigns/remove_or_stop_contact_ids | write | emailer_campaigns | Update contact status in a sequence. |
| POST | v1/emailer_campaigns/search | read | emailer_campaigns | Search for sequences. |
| POST | v1/emailer_campaigns/{id}/abort | write | emailer_campaigns | Deactivate a sequence. |
| POST | v1/emailer_campaigns/{id}/add_contact_ids | write | emailer_campaigns | Add contacts to a sequence. |
| POST | v1/emailer_campaigns/{id}/approve | write | emailer_campaigns | Activate a sequence. |
| POST | v1/emailer_campaigns/{id}/archive | write | emailer_campaigns | Archive a sequence. |
| POST | v1/emailer_messages | write | emailer_messages | Create an email draft. |
| POST | v1/emailer_messages/email_send_status | read | emailer_messages | Check email send status. |
| POST | v1/emailer_messages/get_content | read | emailer_messages | Get email content. |
| GET | v1/emailer_messages/search | read | emailer_messages | Search for outreach emails. |
| GET | v1/emailer_messages/{id}/activities | read | emailer_messages | Check email stats. |
| POST | v1/emailer_messages/{id}/send_now | write | emailer_messages | Send email now. |
| GET | v1/emailer_schedules | read | emailer_schedules | List email schedules. |
| POST | v1/enrich | write | enrich | Validate Email Addresses and Phone Numbers. |
| GET | v1/fields | read | fields | Get a list of fields. |
| POST | v1/fields | write | fields | Create a custom field. |
| PATCH | v1/fields | write | fields | Update a custom field. |
| GET | v1/labels | read | labels | Get a list of all lists. |
| POST | v1/labels | write | labels | Create a list. |
| POST | v1/labels/add_entity_ids_to_label_names | write | labels | Add records to a list. |
| POST | v1/labels/remove_entity_ids_from_label_names | write | labels | Remove records from a list. |
| PATCH | v1/labels/{id} | write | labels | Update a list. |
| POST | v1/mixed_companies/search | read | mixed_companies | Company search. |
| POST | v1/mixed_people/api_search | read | mixed_people | People API search. |
| POST | v1/news_articles/search | read | news_articles | News articles search. |
| GET | v1/notes | read | notes | Get a list of notes. |
| POST | v1/opportunities | write | opportunities | Create deal. |
| GET | v1/opportunities/search | read | opportunities | List all deals. |
| GET | v1/opportunities/{id} | read | opportunities | View deal. |
| PATCH | v1/opportunities/{id} | write | opportunities | Update deal. |
| GET | v1/opportunity_stages | read | opportunity_stages | List deal stages. |
| POST | v1/organizations/bulk_enrich | write | organizations | Bulk company enrichment. |
| GET | v1/organizations/enrich | write | organizations | Company enrichment. Kept out of read: consumes enrichment credits. |
| GET | v1/organizations/{id} | read | organizations | Get complete company info. |
| GET | v1/organizations/{id}/job_postings | read | organizations | Company job postings. |
| POST | v1/people/bulk_match | write | people | Bulk people enrichment. |
| POST | v1/people/match | write | people | People enrichment. |
| GET | v1/people/{id} | read | people | Get complete person info. |
| POST | v1/phone_calls | write | phone_calls | Create call records. |
| GET | v1/phone_calls/search | read | phone_calls | Search for calls. |
| PUT | v1/phone_calls/{id} | write | phone_calls | Update call records. |
| POST | v1/reports/sync_report | read | reports | Query analytics report. |
| POST | v1/sequences | write | sequences | Create a sequence. |
| PUT | v1/sequences/{id} | write | sequences | Update a sequence. |
| POST | v1/tasks | write | tasks | Create a task. |
| POST | v1/tasks/bulk_create | write | tasks | Bulk create tasks. |
| POST | v1/tasks/search | read | tasks | Search for tasks. |
| GET | v1/tasks/{id} | read | tasks | Get a task. |
| PATCH | v1/tasks/{id} | write | tasks | Update a task. |
| POST | v1/tasks/{id}/complete | write | tasks | Complete a task. |
| POST | v1/tasks/{id}/skip | write | tasks | Skip a task. |
| GET | v1/typed_custom_fields | read | typed_custom_fields | Get a list of all custom fields. |
| POST | v1/usage_stats/api_usage_stats | read | usage_stats | View API usage stats and rate limits. |
| POST | v1/usage_stats/credit_usage_stats | read | usage_stats | View credit usage stats. |
| GET | v1/users/api_profile | read | users | Get current user profile. |
| GET | v1/users/search | read | users | Get a list of users. |
| GET | v1/webhook_result/{id} | read | webhook_result | Poll webhook result. |
