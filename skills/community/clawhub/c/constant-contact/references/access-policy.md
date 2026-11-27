# Constant Contact access policy

An access policy limits which endpoints Constant Contact connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/constant-contact#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Constant Contact: its 62 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create constant-contact --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v3/account/emails"},
    {"method": "GET", "path": "v3/account/summary"},
    {"method": "GET", "path": "v3/account/summary/company_logo"},
    {"method": "GET", "path": "v3/account/summary/physical_address"},
    {"method": "GET", "path": "v3/account/user/privileges"},
    {"method": "GET", "path": "v3/automations/workflows"},
    {"method": "GET", "path": "v3/automations/workflows/{id}"},
    {"method": "GET", "path": "v3/activities"},
    {"method": "GET", "path": "v3/activities/{id}"},
    {"method": "GET", "path": "v3/contact_exports/{id}"},
    {"method": "GET", "path": "v3/contact_lists"},
    {"method": "GET", "path": "v3/contact_lists/list_id_xrefs"},
    {"method": "GET", "path": "v3/contact_lists/{id}"},
    {"method": "GET", "path": "v3/contact_tags"},
    {"method": "GET", "path": "v3/contact_tags/{id}"},
    {"method": "GET", "path": "v3/contacts"},
    {"method": "GET", "path": "v3/contacts/contact_id_xrefs"},
    {"method": "GET", "path": "v3/contacts/counts"},
    {"method": "GET", "path": "v3/contacts/sms_engagement_history/{id}"},
    {"method": "GET", "path": "v3/contacts/{id}"},
    {"method": "GET", "path": "v3/contact_custom_fields"},
    {"method": "GET", "path": "v3/contact_custom_fields/{id}"},
    {"method": "GET", "path": "v3/reports/contact_reports/{id}/activity_details"},
    {"method": "GET", "path": "v3/reports/contact_reports/{id}/activity_summary"},
    {"method": "GET", "path": "v3/reports/contact_reports/{id}/open_and_click_rates"},
    {"method": "GET", "path": "v3/reports/email_reports/campaign_performance"},
    {"method": "GET", "path": "v3/emails"},
    {"method": "GET", "path": "v3/emails/activities/{id}"},
    {"method": "GET", "path": "v3/emails/activities/{id}/non_opener_resends"},
    {"method": "GET", "path": "v3/emails/campaign_id_xrefs"},
    {"method": "GET", "path": "v3/emails/{id}"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/links"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/bounces"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/clicks"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/didnotopens"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/forwards"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/opens"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/optouts"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/sends"},
    {"method": "GET", "path": "v3/reports/email_reports/{id}/tracking/unique_opens"},
    {"method": "GET", "path": "v3/reports/stats/email_campaign_activities/{id}"},
    {"method": "GET", "path": "v3/reports/stats/email_campaigns/{id}"},
    {"method": "GET", "path": "v3/reports/summary_reports/email_campaign_summaries"},
    {"method": "GET", "path": "v3/emails/activities/{id}/previews"},
    {"method": "GET", "path": "v3/emails/activities/{id}/schedules"},
    {"method": "GET", "path": "v3/emails/activities/{id}/send_history"},
    {"method": "GET", "path": "v3/events"},
    {"method": "GET", "path": "v3/events/{id}"},
    {"method": "GET", "path": "v3/events/{id}/tracks/{id}/registrations"},
    {"method": "GET", "path": "v3/events/{id}/tracks/{id}/registrations/{id}"},
    {"method": "GET", "path": "v3/reports/landing_pages/campaign_details/{id}/p_contact_opens"},
    {"method": "GET", "path": "v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_adds"},
    {"method": "GET", "path": "v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_clicks"},
    {"method": "GET", "path": "v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_opens"},
    {"method": "GET", "path": "v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_sms_optins"},
    {"method": "GET", "path": "v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_updates"},
    {"method": "GET", "path": "v3/segments"},
    {"method": "GET", "path": "v3/segments/{id}"},
    {"method": "GET", "path": "v3/reports/summary_reports/sms_campaign_summaries"},
    {"method": "GET", "path": "v3/social/connections"},
    {"method": "GET", "path": "v3/social/hashtags/groups"},
    {"method": "GET", "path": "v3/social/profiles"}
  ],
  "deny": []
}
```

## Endpoints

The Constant Contact endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v3/account/emails | read | account-services | Use this method to return a collection of email addresses for the account associated with your access token. |
| POST | v3/account/emails | write | account-services | Use this method to add a new email address to a Constant Contact account. |
| GET | v3/account/summary | read | account-services | Get account related details for a Constant Contact user account. |
| PUT | v3/account/summary | write | account-services | Use this method to update account details for a Constant Contact account, such as the email address or phone number. |
| GET | v3/account/summary/company_logo | read | account-services | Use this method to get the company logo associated with a Constant Contact account. |
| PUT | v3/account/summary/company_logo | write | account-services | Use this method to set or replace the company logo for a Constant Contact account. |
| GET | v3/account/summary/physical_address | read | account-services | Use this method to get the address where the account's organization physically resides. |
| POST | v3/account/summary/physical_address | write | account-services | Use this method to add the address where the account's organization physically resides. |
| PUT | v3/account/summary/physical_address | write | account-services | Use this method to update the organization's physical address for the Constant Contact user account. |
| GET | v3/account/user/privileges | read | account-services | Use this method to return the user privileges associated with your access token as an array of objects. |
| GET | v3/automations/workflows | read | automations | Use this method to list all available automation workflows. |
| POST | v3/automations/workflows | write | automations | Use this method to create a new automation campaign workflow from scratch by providing trigger information. |
| GET | v3/automations/workflows/{id} | read | automations | Use this endpoint to retrieve an automation workflow by its workflow id. |
| PUT | v3/automations/workflows/{id} | write | automations | Use this method to update an automation workflow. |
| GET | v3/activities | read | bulk-activities | This endpoint returns a collection of activities. |
| POST | v3/activities/add_list_memberships | write | bulk-activities | Use this method to create an activity that adds contacts to one or more lists. |
| POST | v3/activities/contact_delete | write | bulk-activities | Use this endpoint to bulk delete contacts in an account. |
| POST | v3/activities/contact_exports | write | bulk-activities | Use this method to create an activity that exports contacts and contact details to a CSV file. |
| POST | v3/activities/contacts_file_import | write | bulk-activities | This multipart method creates an asynchronous background job that adds or updates contacts by importing a CSV file containing contact information. |
| POST | v3/activities/contacts_json_import | write | bulk-activities | Use this method to create an asynchronous background job that adds new contacts or updates existing contacts by importing a JSON payload. |
| POST | v3/activities/contacts_taggings_add | write | bulk-activities | Use this method to create an asynchronous activity that adds one or more tags to all contacts meeting your contact filtering criteria. |
| POST | v3/activities/contacts_taggings_remove | write | bulk-activities | Use this method to create an asynchronous activity that removes one or more tags from all contacts meeting your contact filtering criteria. |
| POST | v3/activities/contacts_tags_delete | write | bulk-activities | Use this method to create an asynchronous activity that deletes up to 500 tags. |
| POST | v3/activities/custom_fields_delete | write | bulk-activities | Use this endpoint to delete up to 100 custom fields for an account. |
| POST | v3/activities/list_delete | write | bulk-activities | Use this endpoint to delete up to 100 contact lists in an account. |
| POST | v3/activities/remove_list_memberships | write | bulk-activities | Use this method to create an activity that removes contacts from one or more contact lists. |
| GET | v3/activities/{id} | read | bulk-activities | This endpoint returns an activity status report. |
| GET | v3/contact_exports/{id} | read | bulk-activities | Use this endpoint to retrieve (GET) a CSV file containing exported contacts by providing the `activity_id` of a completed CSV export activity. |
| GET | v3/contact_lists | read | contact-lists | Use this method to return details about all contact lists for the account. |
| POST | v3/contact_lists | write | contact-lists | Create a new contact list resource. |
| GET | v3/contact_lists/list_id_xrefs | read | contact-lists | Use this endpoint to migrate your locally stored V2 contact list data to the new V3 format. |
| GET | v3/contact_lists/{id} | read | contact-lists | Use this method to get details about a specific contact list (`list_id`). |
| PUT | v3/contact_lists/{id} | write | contact-lists | Updates an existing contact list resource, specified by `list_id`. |
| DELETE | v3/contact_lists/{id} | write | contact-lists | Deletes the specified contact list and its membership. |
| GET | v3/contact_tags | read | contact-tags | Use this endpoint to get details for all tags in your account. |
| POST | v3/contact_tags | write | contact-tags | Use this method to create a new tag. |
| GET | v3/contact_tags/{id} | read | contact-tags | Use this method to get tag details for a specified `tag_id`. |
| PUT | v3/contact_tags/{id} | write | contact-tags | Use this method to rename an existing tag to a new unique tag name (`name`). |
| DELETE | v3/contact_tags/{id} | write | contact-tags | Use this method to create an activity used to un-assign a tag from all assigned contacts and delete the tag. |
| GET | v3/contacts | read | contacts | Use this method to return a collection of contacts. |
| POST | v3/contacts | write | contacts | POST (create) a Contact. |
| GET | v3/contacts/contact_id_xrefs | read | contacts | Use this endpoint to migrate your locally stored V2 contact ids to the new V3 format. |
| GET | v3/contacts/counts | read | contacts | Use to get the total contacts count for the account and the total contact-consent counts for each consent state. |
| PUT | v3/contacts/resubscribe/{id} | write | contacts | Use this endpoint to send a confirmation resubscribe email to a contact in order to get their confirmation to resubscribe. |
| POST | v3/contacts/sign_up_form | write | contacts | Use this method to create a new contact or update an existing contact. |
| GET | v3/contacts/sms_engagement_history/{id} | read | contacts | Use this method to return SMS engagement details for a contact, such as SMS consent and advertising frequency details. |
| GET | v3/contacts/{id} | read | contacts | This endpoint GETs a specific contact resource (contact_id). |
| PUT | v3/contacts/{id} | write | contacts | The PUT method updates an existing contact. |
| DELETE | v3/contacts/{id} | write | contacts | Deletes the contact identified by the contact_id path parameter. |
| GET | v3/contact_custom_fields | read | contacts-custom-fields | Get all custom fields defined in the user's account. |
| POST | v3/contact_custom_fields | write | contacts-custom-fields | Custom fields are extra data fields you create to store additional information about your contacts, such as preferences, membership levels, and interests. |
| GET | v3/contact_custom_fields/{id} | read | contacts-custom-fields | Get details for a specified custom field. |
| PUT | v3/contact_custom_fields/{id} | write | contacts-custom-fields | Update an existing custom field. |
| DELETE | v3/contact_custom_fields/{id} | write | contacts-custom-fields | Delete a custom field from the user's account. |
| GET | v3/reports/contact_reports/{id}/activity_details | read | contacts-reporting | Gets the tracking activity data for a single contact, sorted in descending activity date order. |
| GET | v3/reports/contact_reports/{id}/activity_summary | read | contacts-reporting | Get a list of the recent emails (aka, campaign activities) sent to a specific contact and a summary of the actions the contact took on that email for the most recent 200 campaigns. |
| GET | v3/reports/contact_reports/{id}/open_and_click_rates | read | contacts-reporting | Gets the average open and click rate for a given account and contact.Looks at all tracking activities for bulk emails from a given contact over the given date range. |
| GET | v3/reports/email_reports/campaign_performance | read | contacts-reporting | Retrieves campaign performance stats for one or more campaigns for a given date range. |
| GET | v3/emails | read | email-campaigns | Use this method to list and get details about your email campaigns. |
| POST | v3/emails | write | email-campaigns | Use this method to create a new email campaign. |
| GET | v3/emails/activities/{id} | read | email-campaigns | Use this method to return a specific email campaign activity. |
| PUT | v3/emails/activities/{id} | write | email-campaigns | Use this method to update an email campaign activity by including the complete email campaign activity with your changes in the request body. |
| GET | v3/emails/activities/{id}/non_opener_resends | read | email-campaigns | Get details about a resend to non-openers campaign activity. |
| POST | v3/emails/activities/{id}/non_opener_resends | write | email-campaigns | Use this POST method to resend a primary campaign activity to contacts that did not open a campaign activity that has a current `status` of `Draft`, `Scheduled`, or `Done`. |
| DELETE | v3/emails/activities/{id}/non_opener_resends/{id} | write | email-campaigns | Use this `DELETE` method to delete (unschedule) a resend to non openers activity. |
| GET | v3/emails/campaign_id_xrefs | read | email-campaigns | Use this endpoint to migrate your locally stored V2 email campaign data to the new V3 format. |
| GET | v3/emails/{id} | read | email-campaigns | Use this method to get details about a single email campaign and campaign related activities. |
| PATCH | v3/emails/{id} | write | email-campaigns | Use this method to rename an email campaign. |
| DELETE | v3/emails/{id} | write | email-campaigns | Use this method to delete an email campaign and the email campaign activities associated with the email campaign. |
| GET | v3/reports/email_reports/{id}/links | read | email-reporting | Use this method to return link details, including the number of unique contacts that clicked each link in an email campaign activity, and the type of action associated with clicking each link. |
| GET | v3/reports/email_reports/{id}/tracking/bounces | read | email-reporting | Use this method to get a report listing contact bounce data for the specified email campaign activity. |
| GET | v3/reports/email_reports/{id}/tracking/clicks | read | email-reporting | Use this method to get each time a contact clicked a link, the click date and time, and the device type they used. |
| GET | v3/reports/email_reports/{id}/tracking/didnotopens | read | email-reporting | Use this method to get a report listing each contact that was sent, but did not open the specified email campaign activity. |
| GET | v3/reports/email_reports/{id}/tracking/forwards | read | email-reporting | Use this method to get a report listing each time a contact forwarded the email campaign activity using the forwarding link in the email footer. |
| GET | v3/reports/email_reports/{id}/tracking/opens | read | email-reporting | Use this method to get each time a contact opened a specific email campaign activity. |
| GET | v3/reports/email_reports/{id}/tracking/optouts | read | email-reporting | Use this method to get a report listing each contact that clicked the unsubscribe link in the email campaign activity to opt-out from receiving emails sent from your Constant Contact account. |
| GET | v3/reports/email_reports/{id}/tracking/sends | read | email-reporting | Use this method to get each contact that was sent a specific email campaign activity. |
| GET | v3/reports/email_reports/{id}/tracking/unique_opens | read | email-reporting | Use this method to get a unique opens report that provides details about the last time that each contact opened the specified email campaign activity. |
| GET | v3/reports/stats/email_campaign_activities/{id} | read | email-reporting | Use this method to get performance tracking statistics for up to ten email campaign activities. |
| GET | v3/reports/stats/email_campaigns/{id} | read | email-reporting | Use this method to get email campaign performance tracking statistics for one or more campaigns, including the total number of times contacts interacted with your campaigns and how. |
| GET | v3/reports/summary_reports/email_campaign_summaries | read | email-reporting | Use this method to get aggregate email campaign statistics for up to five hundred email campaigns. |
| GET | v3/emails/activities/{id}/previews | read | email-scheduling | Use this method to get the HTML preview of an email campaign activity. |
| GET | v3/emails/activities/{id}/schedules | read | email-scheduling | Use this method to return the current schedule for an email campaign activity. |
| POST | v3/emails/activities/{id}/schedules | write | email-scheduling | Use this method to send an email campaign activity to contacts either immediately or on a specific date. |
| DELETE | v3/emails/activities/{id}/schedules | write | email-scheduling | Use this method to unschedule an email campaign activity by deleting the schedule. |
| GET | v3/emails/activities/{id}/send_history | read | email-scheduling | Use this method to return the send history of an email campaign activity. |
| POST | v3/emails/activities/{id}/tests | write | email-scheduling | Use this method to send a test email to specific email addresses. |
| GET | v3/events | read | events | Retrieve a collection of events with event details. |
| POST | v3/events/default | write | events | Creates a new event with default settings, registration form, and landing page. |
| GET | v3/events/{id} | read | events | Specify the `event_id` path parameter to retrieve the event's details. |
| PATCH | v3/events/{id} | write | events | Partially updates an event with the provided fields. |
| POST | v3/events/{id}/check_in/tickets | write | events | Use this endpoint to mark one or more tickets as checked in. |
| POST | v3/events/{id}/copy | write | events | Creates a deep copy of an existing event with all its settings, registration forms, and landing pages. |
| GET | v3/events/{id}/tracks/{id}/registrations | read | events | Use the `event_id` and `track_id` path parameters to get a list of registrations for an event. |
| PUT | v3/events/{id}/tracks/{id}/registrations | write | events | Use this endpoint to update the registration status for one or more registrations within an event track. |
| PUT | v3/events/{id}/tracks/{id}/registrations/payment_status | write | events | Use this endpoint to update the payment status for one or more registrations. |
| GET | v3/events/{id}/tracks/{id}/registrations/{id} | read | events | Use the `event_id`, `registration_id`, and `track_id` path parameters to get registration details. |
| POST | v3/events/{id}/undo_check_in/tickets | write | events | Use this endpoint to undo check-in for one or more tickets, marking them as not checked in. |
| GET | v3/reports/landing_pages/campaign_details/{id}/p_contact_opens | read | landing-pages-reporting | Use this method get contact details for each time a contact opens a link on a landing page. |
| GET | v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_adds | read | landing-pages-reporting | Use this method to get details about each contact added to the account from a specified landing page. |
| GET | v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_clicks | read | landing-pages-reporting | Use this method get details about each contact that clicked a link on a landing page campaign activity. |
| GET | v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_opens | read | landing-pages-reporting | Use this method get details about each contact that opens a link on a landing page. |
| GET | v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_sms_optins | read | landing-pages-reporting | Use this method get details about unique contacts that click a link on a landing page to opt in to receiving SMS text messages. |
| GET | v3/reports/landing_pages/campaign_details/{id}/p_unique_contact_updates | read | landing-pages-reporting | Use this method to get contact details for each contact that updated their contact data from a landing page. |
| GET | v3/segments | read | segments | Use this method to get a list of all segments associated with the account. |
| POST | v3/segments | write | segments | Use this method to create a new segment. |
| GET | v3/segments/{id} | read | segments | Use this method to get details about a segment, including the segment criteria. |
| PUT | v3/segments/{id} | write | segments | Use this method to update an existing segment's name (`name`) and/or contact selection criteria (`segment_criteria`). |
| DELETE | v3/segments/{id} | write | segments | Use this method to delete a segment from your account. |
| PATCH | v3/segments/{id}/name | write | segments | Use this method to update an existing segment `name` with a new unique name in the request body. |
| GET | v3/reports/summary_reports/sms_campaign_summaries | read | sms-reporting | Use this method to get SMS campaign summary details, including the total number of times that each contact uniquely interacted with each tracked campaign activity and aggregate tracking statistics. |
| GET | v3/social/connections | read | social | Retrieves all social network accounts connected to the Constant Contact account, with support for multiple accounts per social network. |
| GET | v3/social/hashtags/groups | read | social | Retrieves a paginated list of saved hashtag groups for the account. |
| POST | v3/social/posts | write | social | Creates a new social media post that can be published immediately or scheduled for later publication. |
| GET | v3/social/profiles | read | social | Retrieves all social media profiles connected to the account. |
