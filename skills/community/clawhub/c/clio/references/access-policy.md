# Clio access policy

An access policy limits which endpoints Clio connections may call through Maton. Clio doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/clio#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Clio: its 157 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create clio --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v4/activities"},
    {"method": "GET", "path": "api/v4/activities/{id}"},
    {"method": "GET", "path": "api/v4/activity_descriptions"},
    {"method": "GET", "path": "api/v4/activity_descriptions/{id}"},
    {"method": "GET", "path": "api/v4/activity_rates"},
    {"method": "GET", "path": "api/v4/activity_rates/{id}"},
    {"method": "GET", "path": "api/v4/allocations"},
    {"method": "GET", "path": "api/v4/allocations/{id}"},
    {"method": "GET", "path": "api/v4/bank_accounts"},
    {"method": "GET", "path": "api/v4/bank_accounts/{id}"},
    {"method": "GET", "path": "api/v4/bank_transactions"},
    {"method": "GET", "path": "api/v4/bank_transactions/{id}"},
    {"method": "GET", "path": "api/v4/bank_transfers/{id}"},
    {"method": "GET", "path": "api/v4/bill_themes"},
    {"method": "GET", "path": "api/v4/billable_clients"},
    {"method": "GET", "path": "api/v4/billable_matters"},
    {"method": "GET", "path": "api/v4/billable_matters/ids"},
    {"method": "GET", "path": "api/v4/settings/billing"},
    {"method": "GET", "path": "api/v4/bills"},
    {"method": "GET", "path": "api/v4/bills/{id}"},
    {"method": "GET", "path": "api/v4/bills/{id}/preview"},
    {"method": "GET", "path": "api/v4/calendar_entries"},
    {"method": "GET", "path": "api/v4/calendar_entries/{id}"},
    {"method": "GET", "path": "api/v4/calendar_entry_event_types"},
    {"method": "GET", "path": "api/v4/calendar_entry_event_types/{id}"},
    {"method": "GET", "path": "api/v4/task_calendars"},
    {"method": "GET", "path": "api/v4/task_calendars/{id}"},
    {"method": "GET", "path": "api/v4/calendars"},
    {"method": "GET", "path": "api/v4/calendars/{id}"},
    {"method": "GET", "path": "api/v4/lauk_civil_certificated_rates"},
    {"method": "GET", "path": "api/v4/lauk_civil_controlled_rates"},
    {"method": "GET", "path": "api/v4/matters/{id}/client"},
    {"method": "GET", "path": "api/v4/clio_payments/links"},
    {"method": "GET", "path": "api/v4/clio_payments/links/{id}"},
    {"method": "GET", "path": "api/v4/clio_payments/payments"},
    {"method": "GET", "path": "api/v4/clio_payments/payments/{id}"},
    {"method": "GET", "path": "api/v4/comments"},
    {"method": "GET", "path": "api/v4/comments/{id}"},
    {"method": "GET", "path": "api/v4/communications"},
    {"method": "GET", "path": "api/v4/communications/{id}"},
    {"method": "GET", "path": "api/v4/contacts"},
    {"method": "GET", "path": "api/v4/contacts/{id}"},
    {"method": "GET", "path": "api/v4/conversation_messages"},
    {"method": "GET", "path": "api/v4/conversation_messages/{id}"},
    {"method": "GET", "path": "api/v4/conversations"},
    {"method": "GET", "path": "api/v4/conversations/{id}"},
    {"method": "GET", "path": "api/v4/credit_memos"},
    {"method": "GET", "path": "api/v4/credit_memos/{id}"},
    {"method": "GET", "path": "api/v4/lauk_criminal_controlled_rates"},
    {"method": "GET", "path": "api/v4/currencies"},
    {"method": "GET", "path": "api/v4/custom_actions"},
    {"method": "GET", "path": "api/v4/custom_actions/{id}"},
    {"method": "GET", "path": "api/v4/custom_field_sets"},
    {"method": "GET", "path": "api/v4/custom_field_sets/{id}"},
    {"method": "GET", "path": "api/v4/custom_fields"},
    {"method": "GET", "path": "api/v4/custom_fields/{id}"},
    {"method": "GET", "path": "api/v4/damages"},
    {"method": "GET", "path": "api/v4/damages/{id}"},
    {"method": "GET", "path": "api/v4/document_archives/{id}"},
    {"method": "GET", "path": "api/v4/document_archives/{id}/download"},
    {"method": "GET", "path": "api/v4/document_automations"},
    {"method": "GET", "path": "api/v4/document_automations/{id}"},
    {"method": "GET", "path": "api/v4/document_categories"},
    {"method": "GET", "path": "api/v4/document_categories/{id}"},
    {"method": "GET", "path": "api/v4/document_templates"},
    {"method": "GET", "path": "api/v4/document_templates/{id}"},
    {"method": "GET", "path": "api/v4/document_templates/{id}/download"},
    {"method": "GET", "path": "api/v4/documents/{id}/versions"},
    {"method": "GET", "path": "api/v4/documents"},
    {"method": "GET", "path": "api/v4/documents/{id}"},
    {"method": "GET", "path": "api/v4/documents/{id}/download"},
    {"method": "GET", "path": "api/v4/contacts/{id}/email_addresses"},
    {"method": "GET", "path": "api/v4/internal_notifications/event_metrics"},
    {"method": "GET", "path": "api/v4/expense_categories"},
    {"method": "GET", "path": "api/v4/expense_categories/{id}"},
    {"method": "GET", "path": "api/v4/lauk_expense_categories"},
    {"method": "GET", "path": "api/v4/fixed_fee_categories"},
    {"method": "GET", "path": "api/v4/fixed_fee_categories/{id}"},
    {"method": "GET", "path": "api/v4/folders"},
    {"method": "GET", "path": "api/v4/folders/list"},
    {"method": "GET", "path": "api/v4/folders/{id}"},
    {"method": "GET", "path": "api/v4/grant_funding_sources"},
    {"method": "GET", "path": "api/v4/grants"},
    {"method": "GET", "path": "api/v4/grants/{id}"},
    {"method": "GET", "path": "api/v4/groups"},
    {"method": "GET", "path": "api/v4/groups/{id}"},
    {"method": "GET", "path": "api/v4/interest_charges"},
    {"method": "GET", "path": "api/v4/court_rules/jurisdictions"},
    {"method": "GET", "path": "api/v4/court_rules/jurisdictions/{id}"},
    {"method": "GET", "path": "api/v4/court_rules/jurisdictions/{id}/triggers"},
    {"method": "GET", "path": "api/v4/court_rules/jurisdictions/{id}/triggers/{id}"},
    {"method": "GET", "path": "api/v4/line_items"},
    {"method": "GET", "path": "api/v4/log_entries"},
    {"method": "GET", "path": "api/v4/matters/{id}/contacts"},
    {"method": "GET", "path": "api/v4/court_rules/matter_dockets"},
    {"method": "GET", "path": "api/v4/court_rules/matter_dockets/preview"},
    {"method": "GET", "path": "api/v4/court_rules/matter_dockets/{id}"},
    {"method": "GET", "path": "api/v4/matters/{id}/protected_funds"},
    {"method": "GET", "path": "api/v4/protected_funds"},
    {"method": "GET", "path": "api/v4/matter_stages"},
    {"method": "GET", "path": "api/v4/matter_transfers/{id}"},
    {"method": "GET", "path": "api/v4/matters"},
    {"method": "GET", "path": "api/v4/matters/{id}"},
    {"method": "GET", "path": "api/v4/medical_records_details"},
    {"method": "GET", "path": "api/v4/medical_records_details/{id}"},
    {"method": "GET", "path": "api/v4/internal_notifications/my_events"},
    {"method": "GET", "path": "api/v4/notes"},
    {"method": "GET", "path": "api/v4/notes/{id}"},
    {"method": "GET", "path": "api/v4/outstanding_client_balances"},
    {"method": "GET", "path": "api/v4/contacts/{id}/phone_numbers"},
    {"method": "GET", "path": "api/v4/practice_areas"},
    {"method": "GET", "path": "api/v4/practice_areas/{id}"},
    {"method": "GET", "path": "api/v4/rate_table_assignments"},
    {"method": "GET", "path": "api/v4/rate_table_timekeepers"},
    {"method": "GET", "path": "api/v4/rate_tables"},
    {"method": "GET", "path": "api/v4/rate_tables/{id}"},
    {"method": "GET", "path": "api/v4/matters/{id}/related_contacts"},
    {"method": "GET", "path": "api/v4/relationships"},
    {"method": "GET", "path": "api/v4/relationships/{id}"},
    {"method": "GET", "path": "api/v4/reminders"},
    {"method": "GET", "path": "api/v4/reminders/{id}"},
    {"method": "GET", "path": "api/v4/report_presets"},
    {"method": "GET", "path": "api/v4/report_presets/{id}"},
    {"method": "GET", "path": "api/v4/report_schedules"},
    {"method": "GET", "path": "api/v4/report_schedules/{id}"},
    {"method": "GET", "path": "api/v4/reports"},
    {"method": "GET", "path": "api/v4/reports/{id}"},
    {"method": "GET", "path": "api/v4/reports/{id}/download"},
    {"method": "GET", "path": "api/v4/safe_custody/locations"},
    {"method": "GET", "path": "api/v4/safe_custody/packets"},
    {"method": "GET", "path": "api/v4/safe_custody/packets/{id}"},
    {"method": "GET", "path": "api/v4/safe_custody/records"},
    {"method": "GET", "path": "api/v4/safe_custody/records/{id}"},
    {"method": "GET", "path": "api/v4/court_rules/service_types"},
    {"method": "GET", "path": "api/v4/court_rules/service_types/{id}"},
    {"method": "GET", "path": "api/v4/task_template_lists"},
    {"method": "GET", "path": "api/v4/task_template_lists/{id}"},
    {"method": "GET", "path": "api/v4/task_templates"},
    {"method": "GET", "path": "api/v4/task_templates/{id}"},
    {"method": "GET", "path": "api/v4/task_types"},
    {"method": "GET", "path": "api/v4/task_types/{id}"},
    {"method": "GET", "path": "api/v4/tasks"},
    {"method": "GET", "path": "api/v4/tasks/{id}"},
    {"method": "GET", "path": "api/v4/tax_rate_configurations"},
    {"method": "GET", "path": "api/v4/tax_rate_configurations/{id}"},
    {"method": "GET", "path": "api/v4/settings/text_snippets"},
    {"method": "GET", "path": "api/v4/settings/text_snippets/{id}"},
    {"method": "GET", "path": "api/v4/timer"},
    {"method": "GET", "path": "api/v4/trust_line_items"},
    {"method": "GET", "path": "api/v4/users"},
    {"method": "GET", "path": "api/v4/users/who_am_i"},
    {"method": "GET", "path": "api/v4/users/{id}"},
    {"method": "GET", "path": "api/v4/utbms/codes"},
    {"method": "GET", "path": "api/v4/utbms/codes/{id}"},
    {"method": "GET", "path": "api/v4/utbms/sets"},
    {"method": "GET", "path": "api/v4/webhooks"},
    {"method": "GET", "path": "api/v4/webhooks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Clio endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v4/activities | read | activities | List Activities. |
| POST | api/v4/activities | write | activities | Create a new Activity. |
| GET | api/v4/activities/{id} | read | activities | Get an Activity. |
| PATCH | api/v4/activities/{id} | write | activities | Update a single Activity. |
| DELETE | api/v4/activities/{id} | write | activities | Delete a single Activity. |
| GET | api/v4/activity_descriptions | read | activity descriptions | List ActivityDescriptions. |
| POST | api/v4/activity_descriptions | write | activity descriptions | Create a new ActivityDescription. |
| GET | api/v4/activity_descriptions/{id} | read | activity descriptions | Get an ActivityDescription. |
| PATCH | api/v4/activity_descriptions/{id} | write | activity descriptions | Update a single ActivityDescription. |
| DELETE | api/v4/activity_descriptions/{id} | write | activity descriptions | Delete a single ActivityDescription. |
| GET | api/v4/activity_rates | read | activity rates | List ActivityRates. |
| POST | api/v4/activity_rates | write | activity rates | Create a new ActivityRate. |
| GET | api/v4/activity_rates/{id} | read | activity rates | Get an ActivityRate. |
| PATCH | api/v4/activity_rates/{id} | write | activity rates | Update a single ActivityRate. |
| DELETE | api/v4/activity_rates/{id} | write | activity rates | Delete a single ActivityRate. |
| GET | api/v4/allocations | read | allocations | List Allocations. |
| GET | api/v4/allocations/{id} | read | allocations | Get an Allocation. |
| GET | api/v4/bank_accounts | read | bank accounts | List BankAccounts. |
| POST | api/v4/bank_accounts | write | bank accounts | Create a new BankAccount. |
| GET | api/v4/bank_accounts/{id} | read | bank accounts | Get a BankAccount. |
| PATCH | api/v4/bank_accounts/{id} | write | bank accounts | Update a single BankAccount. |
| DELETE | api/v4/bank_accounts/{id} | write | bank accounts | Delete a single BankAccount. |
| GET | api/v4/bank_transactions | read | bank transactions | List BankTransactions. |
| POST | api/v4/bank_transactions | write | bank transactions | Create a new BankTransaction. |
| GET | api/v4/bank_transactions/{id} | read | bank transactions | Get a BankTransaction. |
| PATCH | api/v4/bank_transactions/{id} | write | bank transactions | Update a single BankTransaction. |
| DELETE | api/v4/bank_transactions/{id} | write | bank transactions | Delete a single BankTransaction. |
| GET | api/v4/bank_transfers/{id} | read | bank transfers | Get a BankTransfer. |
| GET | api/v4/bill_themes | read | bill themes | List BillThemes. |
| PATCH | api/v4/bill_themes/{id} | write | bill themes | Update a single BillTheme. |
| GET | api/v4/billable_clients | read | billable clients | List BillableClients. |
| GET | api/v4/billable_matters | read | billable matters | List BillableMatters. |
| GET | api/v4/billable_matters/ids | read | billable matters | Returns the unique identifiers of all BillableMatter. |
| GET | api/v4/settings/billing | read | billing settings | Get the billing settings. |
| GET | api/v4/bills | read | bills | List Bills. |
| GET | api/v4/bills/{id} | read | bills | Get a Bill. |
| PATCH | api/v4/bills/{id} | write | bills | Update a single Bill. |
| DELETE | api/v4/bills/{id} | write | bills | Delete or void a Bill. |
| POST | api/v4/bills/{id}/mark_as_sent | write | bills | Mark a Bill as sent. |
| GET | api/v4/bills/{id}/preview | read | bills | Returns the pre-rendered html for the Bill. |
| GET | api/v4/calendar_entries | read | calendar entries | List CalendarEntries. |
| POST | api/v4/calendar_entries | write | calendar entries | Create a new CalendarEntry. |
| GET | api/v4/calendar_entries/{id} | read | calendar entries | Get a CalendarEntry. |
| PATCH | api/v4/calendar_entries/{id} | write | calendar entries | Update a single CalendarEntry. |
| DELETE | api/v4/calendar_entries/{id} | write | calendar entries | Delete a single CalendarEntry. |
| GET | api/v4/calendar_entry_event_types | read | calendar entry event types | List calendar entry event types. |
| POST | api/v4/calendar_entry_event_types | write | calendar entry event types | Create a new calendar entry event type. |
| GET | api/v4/calendar_entry_event_types/{id} | read | calendar entry event types | Get a calendar entry event type. |
| PATCH | api/v4/calendar_entry_event_types/{id} | write | calendar entry event types | Update a single calendar entry event type. |
| DELETE | api/v4/calendar_entry_event_types/{id} | write | calendar entry event types | Delete a single calendar entry event type. |
| GET | api/v4/task_calendars | read | calendar visibilities | List CalendarVisibilities. |
| GET | api/v4/task_calendars/{id} | read | calendar visibilities | Get a CalendarVisibility. |
| PATCH | api/v4/task_calendars/{id} | write | calendar visibilities | Update a single CalendarVisibility. |
| GET | api/v4/calendars | read | calendars | List Calendars. |
| POST | api/v4/calendars | write | calendars | Create a new Calendar. |
| GET | api/v4/calendars/{id} | read | calendars | Get a Calendar. |
| PATCH | api/v4/calendars/{id} | write | calendars | Update a single Calendar. |
| DELETE | api/v4/calendars/{id} | write | calendars | Delete a single Calendar. |
| GET | api/v4/lauk_civil_certificated_rates | read | civil certificated rates | List Civil Certificated Rates. |
| GET | api/v4/lauk_civil_controlled_rates | read | civil controlled rates | List Civil Controlled Rates. |
| GET | api/v4/matters/{id}/client | read | clients | Get the client data for a single matter. |
| GET | api/v4/clio_payments/links | read | clio payments links | List ClioPaymentsLinks. |
| POST | api/v4/clio_payments/links | write | clio payments links | Create a new ClioPaymentsLink. |
| GET | api/v4/clio_payments/links/{id} | read | clio payments links | Get a ClioPaymentsLink. |
| PATCH | api/v4/clio_payments/links/{id} | write | clio payments links | Update a single ClioPaymentsLink. |
| GET | api/v4/clio_payments/payments | read | clio payments payments | List ClioPaymentsPayments. |
| GET | api/v4/clio_payments/payments/{id} | read | clio payments payments | Get a ClioPaymentsPayment. |
| GET | api/v4/comments | read | comments | List Comments. |
| POST | api/v4/comments | write | comments | Create a new Comment. |
| GET | api/v4/comments/{id} | read | comments | Get a Comment. |
| PATCH | api/v4/comments/{id} | write | comments | Update a single Comment. |
| DELETE | api/v4/comments/{id} | write | comments | Delete a single Comment. |
| GET | api/v4/communications | read | communications | List Communications. |
| POST | api/v4/communications | write | communications | Create a new Communication. |
| GET | api/v4/communications/{id} | read | communications | Get a Communication. |
| PATCH | api/v4/communications/{id} | write | communications | Update a single Communication. |
| DELETE | api/v4/communications/{id} | write | communications | Delete a single Communication. |
| GET | api/v4/contacts | read | contacts | List Contacts. |
| POST | api/v4/contacts | write | contacts | Create a new Contact. |
| GET | api/v4/contacts/{id} | read | contacts | Get a Contact. |
| PATCH | api/v4/contacts/{id} | write | contacts | Update a single Contact. |
| DELETE | api/v4/contacts/{id} | write | contacts | Delete a single Contact. |
| GET | api/v4/conversation_messages | read | conversation messages | List ConversationMessages. |
| POST | api/v4/conversation_messages | write | conversation messages | Create a new ConversationMessage. |
| GET | api/v4/conversation_messages/{id} | read | conversation messages | Get a ConversationMessage. |
| GET | api/v4/conversations | read | conversations | List Conversations. |
| GET | api/v4/conversations/{id} | read | conversations | Get a Conversation. |
| PATCH | api/v4/conversations/{id} | write | conversations | Update a single Conversation. |
| GET | api/v4/credit_memos | read | credit memos | List CreditMemos. |
| GET | api/v4/credit_memos/{id} | read | credit memos | Get a CreditMemo. |
| GET | api/v4/lauk_criminal_controlled_rates | read | criminal controlled rates | List Criminal Controlled Rates. |
| GET | api/v4/currencies | read | currencies | List Currencies. |
| GET | api/v4/custom_actions | read | custom actions | List CustomActions. |
| POST | api/v4/custom_actions | write | custom actions | Create a new CustomAction. |
| GET | api/v4/custom_actions/{id} | read | custom actions | Get a CustomAction. |
| PATCH | api/v4/custom_actions/{id} | write | custom actions | Update a single CustomAction. |
| DELETE | api/v4/custom_actions/{id} | write | custom actions | Delete a single CustomAction. |
| GET | api/v4/custom_field_sets | read | custom field sets | List CustomFieldSets. |
| POST | api/v4/custom_field_sets | write | custom field sets | Create a new CustomFieldSet. |
| GET | api/v4/custom_field_sets/{id} | read | custom field sets | Get a CustomFieldSet. |
| PATCH | api/v4/custom_field_sets/{id} | write | custom field sets | Update a single CustomFieldSet. |
| DELETE | api/v4/custom_field_sets/{id} | write | custom field sets | Delete a single CustomFieldSet. |
| GET | api/v4/custom_fields | read | custom fields | List CustomFields. |
| POST | api/v4/custom_fields | write | custom fields | Create a new CustomField. |
| GET | api/v4/custom_fields/{id} | read | custom fields | Get a CustomField. |
| PATCH | api/v4/custom_fields/{id} | write | custom fields | Update a single CustomField. |
| DELETE | api/v4/custom_fields/{id} | write | custom fields | Delete a single CustomField. |
| GET | api/v4/damages | read | damages | List Damages. |
| POST | api/v4/damages | write | damages | Creating a Damage. |
| GET | api/v4/damages/{id} | read | damages | Get a specific Damage. |
| PATCH | api/v4/damages/{id} | write | damages | Updating a Damage. |
| DELETE | api/v4/damages/{id} | write | damages | Deleting a Damage. |
| POST | api/v4/document_archives | write | document archives | Create a new DocumentArchive. |
| GET | api/v4/document_archives/{id} | read | document archives | Get a DocumentArchive. |
| GET | api/v4/document_archives/{id}/download | read | document archives | Download the DocumentArchive. Will return a 303 See Other redirecting to the download URL for the DocumentArchive. |
| GET | api/v4/document_automations | read | document automations | List DocumentAutomations. |
| POST | api/v4/document_automations | write | document automations | Create a new DocumentAutomation. |
| GET | api/v4/document_automations/{id} | read | document automations | Get a DocumentAutomation. |
| GET | api/v4/document_categories | read | document categories | List DocumentCategories. |
| POST | api/v4/document_categories | write | document categories | Create a new DocumentCategory. |
| GET | api/v4/document_categories/{id} | read | document categories | Get a DocumentCategory. |
| PATCH | api/v4/document_categories/{id} | write | document categories | Update a single DocumentCategory. |
| DELETE | api/v4/document_categories/{id} | write | document categories | Delete a single DocumentCategory. |
| GET | api/v4/document_templates | read | document templates | List DocumentTemplates. |
| POST | api/v4/document_templates | write | document templates | Create a new DocumentTemplate. |
| GET | api/v4/document_templates/{id} | read | document templates | Get a DocumentTemplate. |
| PATCH | api/v4/document_templates/{id} | write | document templates | Update a single DocumentTemplate. |
| DELETE | api/v4/document_templates/{id} | write | document templates | Delete a single DocumentTemplate. |
| GET | api/v4/document_templates/{id}/download | read | document templates | Get the contents of the DocumentTemplate. |
| GET | api/v4/documents/{id}/versions | read | document versions | List DocumentVersions. |
| POST | api/v4/documents/{id}/versions/{id}/save_as_latest_version | write | document versions | Save a specific document version as the latest version of the document. |
| GET | api/v4/documents | read | documents | List Documents. |
| POST | api/v4/documents | write | documents | Create a new Document. |
| GET | api/v4/documents/{id} | read | documents | Get a Document. |
| PATCH | api/v4/documents/{id} | write | documents | Update a single Document. |
| DELETE | api/v4/documents/{id} | write | documents | Delete a single Document. |
| POST | api/v4/documents/{id}/copy | write | documents | Copy a Document. |
| GET | api/v4/documents/{id}/download | read | documents | Download the Document. Will return a 303 See Other redirecting to the download URL for the Document. |
| GET | api/v4/contacts/{id}/email_addresses | read | email addresses | List EmailAddresses. |
| GET | api/v4/internal_notifications/event_metrics | read | event metrics | Unread in-app notification events. |
| GET | api/v4/expense_categories | read | expense categories | List ExpenseCategories. |
| POST | api/v4/expense_categories | write | expense categories | Create a new ExpenseCategory. |
| GET | api/v4/expense_categories/{id} | read | expense categories | Get an ExpenseCategory. |
| PATCH | api/v4/expense_categories/{id} | write | expense categories | Update a single ExpenseCategory. |
| DELETE | api/v4/expense_categories/{id} | write | expense categories | Delete a single ExpenseCategory. |
| GET | api/v4/lauk_expense_categories | read | expense categories | List Expense Categories. |
| GET | api/v4/fixed_fee_categories | read | fixed fee categories | List FixedFeeCategories. |
| POST | api/v4/fixed_fee_categories | write | fixed fee categories | Create a new FixedFeeCategory. |
| GET | api/v4/fixed_fee_categories/{id} | read | fixed fee categories | Get a FixedFeeCategory. |
| PATCH | api/v4/fixed_fee_categories/{id} | write | fixed fee categories | Update a single FixedFeeCategory. |
| DELETE | api/v4/fixed_fee_categories/{id} | write | fixed fee categories | Delete a single FixedFeeCategory. |
| GET | api/v4/folders | read | folders | List Folders. |
| POST | api/v4/folders | write | folders | Create a new Folder. |
| GET | api/v4/folders/list | read | folders | Get the contents of a Folder. |
| GET | api/v4/folders/{id} | read | folders | Get a Folder. |
| PATCH | api/v4/folders/{id} | write | folders | Update a single Folder. |
| DELETE | api/v4/folders/{id} | write | folders | Delete a single Folder. |
| GET | api/v4/grant_funding_sources | read | grant funding sources | List grant funding sources. |
| POST | api/v4/grant_funding_sources | write | grant funding sources | Create a new grant funding source. |
| PATCH | api/v4/grant_funding_sources/{id} | write | grant funding sources | Update a single grant funding source. |
| DELETE | api/v4/grant_funding_sources/{id} | write | grant funding sources | Delete a single grant funding source. |
| GET | api/v4/grants | read | grants | List grants. |
| POST | api/v4/grants | write | grants | Create a new grant. |
| GET | api/v4/grants/{id} | read | grants | Get a grant. |
| PATCH | api/v4/grants/{id} | write | grants | Update a single grant. |
| DELETE | api/v4/grants/{id} | write | grants | Deletes a single grant. |
| GET | api/v4/groups | read | groups | List Groups. |
| POST | api/v4/groups | write | groups | Create a new Group. |
| GET | api/v4/groups/{id} | read | groups | Get a Group. |
| PATCH | api/v4/groups/{id} | write | groups | Update a single Group. |
| DELETE | api/v4/groups/{id} | write | groups | Delete a single Group. |
| GET | api/v4/interest_charges | read | interest charges | List InterestCharges. |
| DELETE | api/v4/interest_charges/{id} | write | interest charges | Delete a single InterestCharge. |
| GET | api/v4/court_rules/jurisdictions | read | jurisdictions | List jurisdictions. |
| GET | api/v4/court_rules/jurisdictions/{id} | read | jurisdictions | Get the jurisdiction. |
| GET | api/v4/court_rules/jurisdictions/{id}/triggers | read | jurisdictions to triggers | List triggers. |
| GET | api/v4/court_rules/jurisdictions/{id}/triggers/{id} | read | jurisdictions to triggers | Get the trigger. |
| GET | api/v4/line_items | read | line items | List LineItems. |
| PATCH | api/v4/line_items/{id} | write | line items | Update a single LineItem. |
| DELETE | api/v4/line_items/{id} | write | line items | Delete a single LineItem. |
| GET | api/v4/log_entries | read | log entries | List LogEntries. |
| GET | api/v4/matters/{id}/contacts | read | matter contacts | Get the related contact data for a single matter. |
| GET | api/v4/court_rules/matter_dockets | read | matter dockets | List matter dockets. |
| POST | api/v4/court_rules/matter_dockets | write | matter dockets | Creates a matter docket. |
| GET | api/v4/court_rules/matter_dockets/preview | read | matter dockets | Preview calendar dates for the docket. |
| GET | api/v4/court_rules/matter_dockets/{id} | read | matter dockets | Get the matter docket. |
| DELETE | api/v4/court_rules/matter_dockets/{id} | write | matter dockets | Deletes the requested matter docket. |
| GET | api/v4/matters/{id}/protected_funds | read | matter protected funds | Get the protected funds for a single matter. |
| GET | api/v4/protected_funds | read | matter protected funds | Get the protected funds across all matters the current user can access. |
| GET | api/v4/matter_stages | read | matter stages | List MatterStages. |
| POST | api/v4/matter_transfers | write | matter transfers | Create a new MatterTransfer. |
| GET | api/v4/matter_transfers/{id} | read | matter transfers | Get a MatterTransfer. |
| PATCH | api/v4/matter_transfers/{id} | write | matter transfers | Update a single MatterTransfer. |
| GET | api/v4/matters | read | matters | List Matters. |
| POST | api/v4/matters | write | matters | Create a new Matter. |
| GET | api/v4/matters/{id} | read | matters | Get a Matter. |
| PATCH | api/v4/matters/{id} | write | matters | Update a single Matter. |
| DELETE | api/v4/matters/{id} | write | matters | Delete a single Matter. |
| PATCH | api/v4/medical_bills/{id} | write | medical bills | Updating a Medical Bill. |
| DELETE | api/v4/medical_bills/{id} | write | medical bills | Destroying a Medical Bill. |
| PATCH | api/v4/medical_records/{id} | write | medical records | Updating a Medical Record. |
| DELETE | api/v4/medical_records/{id} | write | medical records | Destroying a Medical Record. |
| GET | api/v4/medical_records_details | read | medical records details | List Medical Records Details. |
| POST | api/v4/medical_records_details | write | medical records details | Creating a Medical Records Detail, Medical Records and Medical Bills. |
| GET | api/v4/medical_records_details/{id} | read | medical records details | Get a Medical Records Detail. |
| PATCH | api/v4/medical_records_details/{id} | write | medical records details | Updating a Medical Records Detail. |
| DELETE | api/v4/medical_records_details/{id} | write | medical records details | Destroying a Medical Records Detail. |
| GET | api/v4/internal_notifications/my_events | read | my events | List of my in-app notification events. |
| PATCH | api/v4/internal_notifications/my_events/{id} | write | my events | Mark a single in-app notification event as read/unread. |
| DELETE | api/v4/internal_notifications/my_events/{id} | write | my events | Clear (delete) a single in-app notification event. |
| GET | api/v4/notes | read | notes | List Notes. |
| POST | api/v4/notes | write | notes | Create a new Note. |
| GET | api/v4/notes/{id} | read | notes | Get a Note. |
| PATCH | api/v4/notes/{id} | write | notes | Update a single Note. |
| DELETE | api/v4/notes/{id} | write | notes | Delete a single Note. |
| GET | api/v4/outstanding_client_balances | read | outstanding client balances | List OutstandingClientBalances. |
| GET | api/v4/contacts/{id}/phone_numbers | read | phone numbers | List PhoneNumbers. |
| GET | api/v4/practice_areas | read | practice areas | List PracticeAreas. |
| POST | api/v4/practice_areas | write | practice areas | Create a new PracticeArea. |
| GET | api/v4/practice_areas/{id} | read | practice areas | Get a PracticeArea. |
| PATCH | api/v4/practice_areas/{id} | write | practice areas | Update a single PracticeArea. |
| DELETE | api/v4/practice_areas/{id} | write | practice areas | Delete a single PracticeArea. |
| GET | api/v4/rate_table_assignments | read | rate table assignments | Get the rate table assignments visible to the current user. |
| POST | api/v4/rate_table_categories | write | rate table categories | Add a category to a rate table. |
| PATCH | api/v4/rate_table_categories/{id} | write | rate table categories | Rename or move a rate table category. |
| DELETE | api/v4/rate_table_categories/{id} | write | rate table categories | Remove a rate table category. |
| POST | api/v4/rate_table_categories/{id}/adjust_rates | write | rate table categories | Adjust every rate in a rate table category. |
| POST | api/v4/rate_table_rates | write | rate table rates | Set a timekeeper's rate in a rate table category from a date. |
| GET | api/v4/rate_table_timekeepers | read | rate table timekeepers | Get the timekeepers on a rate table. |
| POST | api/v4/rate_table_timekeepers | write | rate table timekeepers | Add a timekeeper to a rate table. |
| POST | api/v4/rate_table_timekeepers/adjust_rates | write | rate table timekeepers | Adjust the rates of timekeepers on a rate table. |
| POST | api/v4/rate_table_timekeepers/reassign | write | rate table timekeepers | Move a timekeeper's rates on a rate table to another timekeeper. |
| DELETE | api/v4/rate_table_timekeepers/{id} | write | rate table timekeepers | Remove a timekeeper from a rate table. |
| GET | api/v4/rate_tables | read | rate tables | Get the rate tables visible to the current user. |
| POST | api/v4/rate_tables | write | rate tables | Create a new rate table. |
| GET | api/v4/rate_tables/{id} | read | rate tables | Get a single rate table. |
| PATCH | api/v4/rate_tables/{id} | write | rate tables | Update a rate table. |
| DELETE | api/v4/rate_tables/{id} | write | rate tables | Permanently delete a rate table. |
| PATCH | api/v4/rate_tables/{id}/activate | write | rate tables | Activate a draft rate table. |
| PATCH | api/v4/rate_tables/{id}/archive | write | rate tables | Archive a rate table. |
| POST | api/v4/rate_tables/{id}/copy | write | rate tables | Copy a rate table into a new draft. |
| PATCH | api/v4/rate_tables/{id}/deactivate | write | rate tables | Get an active rate table to draft. |
| PATCH | api/v4/rate_tables/{id}/unarchive | write | rate tables | Unarchive a rate table. |
| GET | api/v4/matters/{id}/related_contacts | read | related contacts | Get the related contact data for a single matter. |
| GET | api/v4/relationships | read | relationships | List Relationships. |
| POST | api/v4/relationships | write | relationships | Create a new Relationship. |
| GET | api/v4/relationships/{id} | read | relationships | Get a Relationship. |
| PATCH | api/v4/relationships/{id} | write | relationships | Update a single Relationship. |
| DELETE | api/v4/relationships/{id} | write | relationships | Delete a single Relationship. |
| GET | api/v4/reminders | read | reminders | List Reminders. |
| POST | api/v4/reminders | write | reminders | Create a new Reminder. |
| GET | api/v4/reminders/{id} | read | reminders | Get a Reminder. |
| PATCH | api/v4/reminders/{id} | write | reminders | Update a single Reminder. |
| DELETE | api/v4/reminders/{id} | write | reminders | Delete a single Reminder. |
| GET | api/v4/report_presets | read | report presets | List ReportPresets. |
| POST | api/v4/report_presets | write | report presets | Create a new ReportPreset. |
| GET | api/v4/report_presets/{id} | read | report presets | Get a ReportPreset. |
| PATCH | api/v4/report_presets/{id} | write | report presets | Update a single ReportPreset. |
| DELETE | api/v4/report_presets/{id} | write | report presets | Delete a single ReportPreset. |
| POST | api/v4/report_presets/{id}/generate_report | write | report presets | Generate a new report for a given preset. |
| GET | api/v4/report_schedules | read | report schedules | List ReportSchedules. |
| POST | api/v4/report_schedules | write | report schedules | Create a new ReportSchedule. |
| GET | api/v4/report_schedules/{id} | read | report schedules | Get a ReportSchedule. |
| PATCH | api/v4/report_schedules/{id} | write | report schedules | Update a single ReportSchedule. |
| DELETE | api/v4/report_schedules/{id} | write | report schedules | Delete a single ReportSchedule. |
| GET | api/v4/reports | read | reports | List Reports. |
| POST | api/v4/reports | write | reports | Create a new Report. |
| GET | api/v4/reports/{id} | read | reports | Get a Report. |
| GET | api/v4/reports/{id}/download | read | reports | Download the completed Report. |
| GET | api/v4/safe_custody/locations | read | safe custody packet locations | List SafeCustodyPacketLocations. |
| POST | api/v4/safe_custody/locations | write | safe custody packet locations | Create a new SafeCustodyPacketLocation. |
| GET | api/v4/safe_custody/packets | read | safe custody packets | List SafeCustodyPackets. |
| POST | api/v4/safe_custody/packets | write | safe custody packets | Create a new SafeCustodyPacket. |
| GET | api/v4/safe_custody/packets/{id} | read | safe custody packets | Get a SafeCustodyPacket. |
| PATCH | api/v4/safe_custody/packets/{id} | write | safe custody packets | Update a single SafeCustodyPacket. |
| GET | api/v4/safe_custody/records | read | safe custody records | List SafeCustodyRecords. |
| POST | api/v4/safe_custody/records | write | safe custody records | Create a new SafeCustodyRecord. |
| GET | api/v4/safe_custody/records/{id} | read | safe custody records | Get a SafeCustodyRecord. |
| PATCH | api/v4/safe_custody/records/{id} | write | safe custody records | Update a single SafeCustodyRecord. |
| POST | api/v4/safe_custody/records/{id}/state_changes | write | safe custody records | Transition the custody state of a SafeCustodyRecord. |
| GET | api/v4/court_rules/service_types | read | service types | List service types. |
| GET | api/v4/court_rules/service_types/{id} | read | service types | Get the service type. |
| GET | api/v4/task_template_lists | read | task template lists | List TaskTemplateLists. |
| POST | api/v4/task_template_lists | write | task template lists | Create a new TaskTemplateList. |
| GET | api/v4/task_template_lists/{id} | read | task template lists | Get a TaskTemplateList. |
| PATCH | api/v4/task_template_lists/{id} | write | task template lists | Update a single TaskTemplateList. |
| DELETE | api/v4/task_template_lists/{id} | write | task template lists | Delete a single TaskTemplateList. |
| POST | api/v4/task_template_lists/{id}/copy | write | task template lists | Copy a TaskTemplateList. |
| GET | api/v4/task_templates | read | task templates | List TaskTemplates. |
| POST | api/v4/task_templates | write | task templates | Create a new TaskTemplate. |
| GET | api/v4/task_templates/{id} | read | task templates | Get a TaskTemplate. |
| PATCH | api/v4/task_templates/{id} | write | task templates | Update a single TaskTemplate. |
| DELETE | api/v4/task_templates/{id} | write | task templates | Delete a single TaskTemplate. |
| GET | api/v4/task_types | read | task types | List TaskTypes. |
| POST | api/v4/task_types | write | task types | Create a new TaskType. |
| GET | api/v4/task_types/{id} | read | task types | Get a TaskType. |
| PATCH | api/v4/task_types/{id} | write | task types | Update a single TaskType. |
| GET | api/v4/tasks | read | tasks | List Tasks. |
| POST | api/v4/tasks | write | tasks | Create a new Task. |
| GET | api/v4/tasks/{id} | read | tasks | Get a Task. |
| PATCH | api/v4/tasks/{id} | write | tasks | Update a single Task. |
| DELETE | api/v4/tasks/{id} | write | tasks | Delete a single Task. |
| GET | api/v4/tax_rate_configurations | read | tax rate configurations | List TaxRateConfigurations. |
| POST | api/v4/tax_rate_configurations | write | tax rate configurations | Create a new TaxRateConfiguration. |
| GET | api/v4/tax_rate_configurations/{id} | read | tax rate configurations | Get a TaxRateConfiguration. |
| PATCH | api/v4/tax_rate_configurations/{id} | write | tax rate configurations | Update a single TaxRateConfiguration. |
| DELETE | api/v4/tax_rate_configurations/{id} | write | tax rate configurations | Delete a single TaxRateConfiguration. |
| GET | api/v4/settings/text_snippets | read | text snippets | Get all text snippets. |
| POST | api/v4/settings/text_snippets | write | text snippets | Create a text snippet. |
| GET | api/v4/settings/text_snippets/{id} | read | text snippets | Get the text snippet. |
| PATCH | api/v4/settings/text_snippets/{id} | write | text snippets | Update a text snippet. |
| DELETE | api/v4/settings/text_snippets/{id} | write | text snippets | Destroy a text snippet. |
| GET | api/v4/timer | read | timers | Get a Timer. |
| POST | api/v4/timer | write | timers | Create a new Timer. |
| DELETE | api/v4/timer | write | timers | Delete a single Timer. |
| GET | api/v4/trust_line_items | read | trust line items | List TrustLineItems. |
| PATCH | api/v4/trust_line_items/{id} | write | trust line items | Update a single TrustLineItem. |
| POST | api/v4/trust_requests | write | trust requests | Create a new TrustRequest. |
| GET | api/v4/users | read | users | List Users. |
| GET | api/v4/users/who_am_i | read | users | Get the current User. |
| GET | api/v4/users/{id} | read | users | Get an User. |
| GET | api/v4/utbms/codes | read | utbms codes | List UtbmsCodes. |
| GET | api/v4/utbms/codes/{id} | read | utbms codes | Get an UtbmsCode. |
| GET | api/v4/utbms/sets | read | utbms sets | List the utbms sets. |
| GET | api/v4/webhooks | read | webhooks | List Webhooks. |
| POST | api/v4/webhooks | write | webhooks | Create a new Webhook. |
| GET | api/v4/webhooks/{id} | read | webhooks | Get a Webhook. |
| PATCH | api/v4/webhooks/{id} | write | webhooks | Update a single Webhook. |
| DELETE | api/v4/webhooks/{id} | write | webhooks | Delete a single Webhook. |
