# ActiveCampaign access policy

An access policy limits which endpoints ActiveCampaign connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/active-campaign#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for ActiveCampaign: its 300 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create active-campaign --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/3/accountContacts"},
    {"method": "GET", "path": "api/3/accountContacts/{id}"},
    {"method": "GET", "path": "api/3/accountCustomFieldData"},
    {"method": "GET", "path": "api/3/accountCustomFieldData/{id}"},
    {"method": "GET", "path": "api/3/accountCustomFieldMeta"},
    {"method": "GET", "path": "api/3/accountCustomFieldMeta/{id}"},
    {"method": "GET", "path": "api/3/accounts"},
    {"method": "GET", "path": "api/3/accounts/{id}"},
    {"method": "GET", "path": "api/3/activities"},
    {"method": "GET", "path": "api/3/activities/{id}"},
    {"method": "GET", "path": "api/3/activityRecipients"},
    {"method": "GET", "path": "api/3/activityRecipients/{id}"},
    {"method": "GET", "path": "api/3/activityRecipients/{id}/activity"},
    {"method": "GET", "path": "api/3/activityRecipients/{id}/recipient"},
    {"method": "GET", "path": "api/3/addresses"},
    {"method": "GET", "path": "api/3/addresses/{id}"},
    {"method": "GET", "path": "api/3/addressGroups"},
    {"method": "GET", "path": "api/3/addressGroups/{id}"},
    {"method": "GET", "path": "api/3/addressLists"},
    {"method": "GET", "path": "api/3/addressLists/{id}"},
    {"method": "GET", "path": "api/3/ai/brand"},
    {"method": "GET", "path": "api/3/ai/brand/primary"},
    {"method": "GET", "path": "api/3/ai/brand/{id}"},
    {"method": "GET", "path": "api/3/ai/brand/{id}/brand-history"},
    {"method": "GET", "path": "api/3/ai/brand/{id}/competitors"},
    {"method": "GET", "path": "api/3/ai/brand/{id}/tone"},
    {"method": "GET", "path": "api/3/ai/customization/instructions"},
    {"method": "GET", "path": "api/3/ai/ecom/customerBehaviorSummary"},
    {"method": "GET", "path": "api/3/ai/ecom/orderStatusSummary"},
    {"method": "GET", "path": "api/3/ai/ecom/productRankings"},
    {"method": "GET", "path": "api/3/ai/ecom/revenueSummary"},
    {"method": "GET", "path": "api/3/ai/report_trends_activity"},
    {"method": "GET", "path": "api/3/audiences"},
    {"method": "GET", "path": "api/3/audiences/{id}"},
    {"method": "GET", "path": "api/3/automations"},
    {"method": "GET", "path": "api/3/automations/{id}"},
    {"method": "GET", "path": "api/3/automations/{id}/blocks"},
    {"method": "GET", "path": "api/3/automations/{id}/contactAutomations"},
    {"method": "GET", "path": "api/3/automations/{id}/contactAutomations/{id}/steps"},
    {"method": "GET", "path": "api/3/automations/{id}/triggers"},
    {"method": "GET", "path": "api/3/bounceLogs"},
    {"method": "GET", "path": "api/3/brandings"},
    {"method": "GET", "path": "api/3/brandings/{id}"},
    {"method": "GET", "path": "api/3/businessGoals/data"},
    {"method": "GET", "path": "api/3/businessGoals/data/{id}"},
    {"method": "GET", "path": "api/3/calendars"},
    {"method": "GET", "path": "api/3/calendars/{id}"},
    {"method": "GET", "path": "api/3/campaigns"},
    {"method": "GET", "path": "api/3/campaigns/{id}"},
    {"method": "GET", "path": "api/3/campaigns/{id}/campaignMessages"},
    {"method": "GET", "path": "api/3/campaigns/{id}/links"},
    {"method": "GET", "path": "api/3/campaigns/{id}/reportTotals"},
    {"method": "GET", "path": "api/3/campaigns/{id}/reports/bounces"},
    {"method": "GET", "path": "api/3/campaigns/{id}/reports/forwards"},
    {"method": "GET", "path": "api/3/campaigns/{id}/reports/opens"},
    {"method": "GET", "path": "api/3/campaigns/{id}/reports/unopens"},
    {"method": "GET", "path": "api/3/campaigns/{id}/reports/unsubscribes"},
    {"method": "GET", "path": "api/3/channel/whatsapp/channels/whatsapp/template"},
    {"method": "GET", "path": "api/3/channel/whatsapp/channels/whatsapp/template/{id}"},
    {"method": "GET", "path": "api/3/channel/whatsapp/flow-execution"},
    {"method": "GET", "path": "api/3/channel/whatsapp/flow-execution-contact"},
    {"method": "GET", "path": "api/3/channel/whatsapp/flow-execution-contact/{id}"},
    {"method": "GET", "path": "api/3/channel/whatsapp/flow-execution/{id}"},
    {"method": "GET", "path": "api/3/channel/whatsapp/inbox/conversation"},
    {"method": "GET", "path": "api/3/connections"},
    {"method": "GET", "path": "api/3/connections/{id}"},
    {"method": "GET", "path": "api/3/contactArchives"},
    {"method": "GET", "path": "api/3/contactArchives/restoreRequest"},
    {"method": "GET", "path": "api/3/contactArchives/restoreRequest/{id}"},
    {"method": "GET", "path": "api/3/contactArchives/{id}"},
    {"method": "GET", "path": "api/3/contactAutomationLogs"},
    {"method": "GET", "path": "api/3/contactAutomationLogs/{id}"},
    {"method": "GET", "path": "api/3/contactAutomations"},
    {"method": "GET", "path": "api/3/contactAutomations/{id}"},
    {"method": "GET", "path": "api/3/contactAutomations/{id}/automation"},
    {"method": "GET", "path": "api/3/contactAutomations/{id}/automationLogs"},
    {"method": "GET", "path": "api/3/contactAutomations/{id}/contact"},
    {"method": "GET", "path": "api/3/contactAutomations/{id}/contactGoals"},
    {"method": "GET", "path": "api/3/contactAutomations/{id}/subscriberSeriesEnd"},
    {"method": "GET", "path": "api/3/contactConversionPoints"},
    {"method": "GET", "path": "api/3/contactConversionPoints/{id}"},
    {"method": "GET", "path": "api/3/contactConversionPoints/{id}/attributions"},
    {"method": "GET", "path": "api/3/contactConversionPoints/{id}/contact"},
    {"method": "GET", "path": "api/3/contactConversions"},
    {"method": "GET", "path": "api/3/contactConversions/{id}"},
    {"method": "GET", "path": "api/3/contactConversions/{id}/activities"},
    {"method": "GET", "path": "api/3/contactConversions/{id}/attributions"},
    {"method": "GET", "path": "api/3/contactConversions/{id}/contact"},
    {"method": "GET", "path": "api/3/contactConversions/{id}/conversion"},
    {"method": "GET", "path": "api/3/contactConversions/{id}/conversiontrigger"},
    {"method": "GET", "path": "api/3/contactData"},
    {"method": "GET", "path": "api/3/contactData/{id}"},
    {"method": "GET", "path": "api/3/contactDeals"},
    {"method": "GET", "path": "api/3/contactDeals/{id}"},
    {"method": "GET", "path": "api/3/contactEmails"},
    {"method": "GET", "path": "api/3/contactEmails/{id}"},
    {"method": "GET", "path": "api/3/contactGoalLists"},
    {"method": "GET", "path": "api/3/contactGoalLists/{id}"},
    {"method": "GET", "path": "api/3/contactGoalLists/{id}/contactGoal"},
    {"method": "GET", "path": "api/3/contactGoalLists/{id}/list"},
    {"method": "GET", "path": "api/3/contactGoals"},
    {"method": "GET", "path": "api/3/contactGoals/{id}"},
    {"method": "GET", "path": "api/3/contactGoals/{id}/automation"},
    {"method": "GET", "path": "api/3/contactGoals/{id}/contact"},
    {"method": "GET", "path": "api/3/contactGoals/{id}/contactAutomation"},
    {"method": "GET", "path": "api/3/contactGoals/{id}/contactGoalLists"},
    {"method": "GET", "path": "api/3/contactGoals/{id}/contactGoalTags"},
    {"method": "GET", "path": "api/3/contactGoals/{id}/goal"},
    {"method": "GET", "path": "api/3/contactGoalTags"},
    {"method": "GET", "path": "api/3/contactGoalTags/{id}"},
    {"method": "GET", "path": "api/3/contactGoalTags/{id}/contactGoal"},
    {"method": "GET", "path": "api/3/contactGoalTags/{id}/tag"},
    {"method": "GET", "path": "api/3/contactImports"},
    {"method": "GET", "path": "api/3/contactImports/{id}"},
    {"method": "GET", "path": "api/3/contactLists"},
    {"method": "GET", "path": "api/3/contactLists/{id}"},
    {"method": "GET", "path": "api/3/contactLogs"},
    {"method": "GET", "path": "api/3/contactLogs/{id}"},
    {"method": "GET", "path": "api/3/contacts"},
    {"method": "GET", "path": "api/3/contacts/{id}"},
    {"method": "GET", "path": "api/3/contacts/{id}/accountContacts"},
    {"method": "GET", "path": "api/3/contacts/{id}/automationEntryCounts"},
    {"method": "GET", "path": "api/3/contacts/{id}/bounceLogs"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactAutomations"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactData"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactDeals"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactGoals"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactLists"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactLogs"},
    {"method": "GET", "path": "api/3/contacts/{id}/contactTags"},
    {"method": "GET", "path": "api/3/contacts/{id}/deals"},
    {"method": "GET", "path": "api/3/contacts/{id}/fieldValues"},
    {"method": "GET", "path": "api/3/contacts/{id}/geoIps"},
    {"method": "GET", "path": "api/3/contacts/{id}/notes"},
    {"method": "GET", "path": "api/3/contacts/{id}/organization"},
    {"method": "GET", "path": "api/3/contacts/{id}/plusAppend"},
    {"method": "GET", "path": "api/3/contacts/{id}/scoreValues"},
    {"method": "GET", "path": "api/3/contacts/{id}/trackingLogs"},
    {"method": "GET", "path": "api/3/contactTags"},
    {"method": "GET", "path": "api/3/contactTags/{id}"},
    {"method": "GET", "path": "api/3/content/domainAuth"},
    {"method": "GET", "path": "api/3/content/editorMarkup/{id}"},
    {"method": "GET", "path": "api/3/content-proxy/files"},
    {"method": "GET", "path": "api/3/content-proxy/files/{id}"},
    {"method": "GET", "path": "api/3/content-proxy/files/{id}/folders"},
    {"method": "GET", "path": "api/3/content-proxy/files/{id}/tags"},
    {"method": "GET", "path": "api/3/content-proxy/folders"},
    {"method": "GET", "path": "api/3/content-proxy/folders/{id}"},
    {"method": "GET", "path": "api/3/content-proxy/folders/{id}/files"},
    {"method": "GET", "path": "api/3/content-proxy/tags/{id}/files"},
    {"method": "GET", "path": "api/3/conversions"},
    {"method": "GET", "path": "api/3/conversions/data"},
    {"method": "GET", "path": "api/3/conversions/labels"},
    {"method": "GET", "path": "api/3/conversions/labels/{id}"},
    {"method": "GET", "path": "api/3/conversions/metrics"},
    {"method": "GET", "path": "api/3/conversions/{id}"},
    {"method": "GET", "path": "api/3/conversions/{id}/data"},
    {"method": "GET", "path": "api/3/conversions/{id}/metrics"},
    {"method": "GET", "path": "api/3/conversions/{id}/trends"},
    {"method": "GET", "path": "api/3/customObjects/records/{id}"},
    {"method": "GET", "path": "api/3/customObjects/records/{id}/external/{id}"},
    {"method": "GET", "path": "api/3/customObjects/records/{id}/{id}"},
    {"method": "GET", "path": "api/3/customObjects/schemas"},
    {"method": "GET", "path": "api/3/customObjects/schemas/{id}"},
    {"method": "GET", "path": "api/3/dealActivities"},
    {"method": "GET", "path": "api/3/dealCustomFieldData"},
    {"method": "GET", "path": "api/3/dealCustomFieldData/{id}"},
    {"method": "GET", "path": "api/3/dealCustomFieldMeta"},
    {"method": "GET", "path": "api/3/dealCustomFieldMeta/{id}"},
    {"method": "GET", "path": "api/3/dealGroup/get_inaccessible_deal_groups"},
    {"method": "GET", "path": "api/3/dealGroups"},
    {"method": "GET", "path": "api/3/dealGroups/{id}"},
    {"method": "GET", "path": "api/3/dealRoles"},
    {"method": "GET", "path": "api/3/deals"},
    {"method": "GET", "path": "api/3/deals/{id}"},
    {"method": "GET", "path": "api/3/deals/{id}/notes"},
    {"method": "GET", "path": "api/3/dealStages"},
    {"method": "GET", "path": "api/3/dealStages/{id}"},
    {"method": "GET", "path": "api/3/dealTasks"},
    {"method": "GET", "path": "api/3/dealTasks/{id}"},
    {"method": "GET", "path": "api/3/dealTasktypes"},
    {"method": "GET", "path": "api/3/dealTasktypes/{id}"},
    {"method": "GET", "path": "api/3/ecomCustomers"},
    {"method": "GET", "path": "api/3/ecomCustomers/{id}"},
    {"method": "GET", "path": "api/3/ecomOrderProducts"},
    {"method": "GET", "path": "api/3/ecomOrderProducts/{id}"},
    {"method": "GET", "path": "api/3/ecomOrders"},
    {"method": "GET", "path": "api/3/ecomOrders/{id}"},
    {"method": "GET", "path": "api/3/ecomOrders/{id}/orderProducts"},
    {"method": "GET", "path": "api/3/emailActivities"},
    {"method": "GET", "path": "api/3/eventTracking"},
    {"method": "GET", "path": "api/3/eventTrackingEvents"},
    {"method": "GET", "path": "api/3/fieldDetails"},
    {"method": "GET", "path": "api/3/fieldOptions"},
    {"method": "GET", "path": "api/3/fieldOptions/{id}"},
    {"method": "GET", "path": "api/3/fieldRels"},
    {"method": "GET", "path": "api/3/fieldRels/{id}"},
    {"method": "GET", "path": "api/3/fields"},
    {"method": "GET", "path": "api/3/fields/{id}"},
    {"method": "GET", "path": "api/3/fieldValues"},
    {"method": "GET", "path": "api/3/fieldValues/{id}"},
    {"method": "GET", "path": "api/3/forms"},
    {"method": "GET", "path": "api/3/forms/{id}"},
    {"method": "GET", "path": "api/3/forms/{id}/html"},
    {"method": "GET", "path": "api/3/geoAddresses"},
    {"method": "GET", "path": "api/3/geoAddresses/{id}"},
    {"method": "GET", "path": "api/3/geoIps"},
    {"method": "GET", "path": "api/3/geoIps/{id}"},
    {"method": "GET", "path": "api/3/geoIps/{id}/geoAddress"},
    {"method": "GET", "path": "api/3/goal/goalStats"},
    {"method": "GET", "path": "api/3/goal/showcase"},
    {"method": "GET", "path": "api/3/goals"},
    {"method": "GET", "path": "api/3/goals/{id}"},
    {"method": "GET", "path": "api/3/groupLimits"},
    {"method": "GET", "path": "api/3/groupMembers"},
    {"method": "GET", "path": "api/3/groupMembers/{id}"},
    {"method": "GET", "path": "api/3/groups"},
    {"method": "GET", "path": "api/3/groups/{id}"},
    {"method": "GET", "path": "api/3/import/bulk_import"},
    {"method": "GET", "path": "api/3/import/history"},
    {"method": "GET", "path": "api/3/import/history/{id}/{id}"},
    {"method": "GET", "path": "api/3/import/info"},
    {"method": "GET", "path": "api/3/initiatives"},
    {"method": "GET", "path": "api/3/initiatives/{id}"},
    {"method": "GET", "path": "api/3/listGroups"},
    {"method": "GET", "path": "api/3/listGroups/{id}"},
    {"method": "GET", "path": "api/3/lists"},
    {"method": "GET", "path": "api/3/lists/exclusions"},
    {"method": "GET", "path": "api/3/lists/exclusions/{id}"},
    {"method": "GET", "path": "api/3/lists/{id}"},
    {"method": "GET", "path": "api/3/message/source"},
    {"method": "GET", "path": "api/3/messages"},
    {"method": "GET", "path": "api/3/messages/{id}"},
    {"method": "GET", "path": "api/3/notes"},
    {"method": "GET", "path": "api/3/notes/{id}"},
    {"method": "GET", "path": "api/3/personalizations"},
    {"method": "GET", "path": "api/3/personalizations/{id}"},
    {"method": "GET", "path": "api/3/persTags"},
    {"method": "GET", "path": "api/3/plusAppends"},
    {"method": "GET", "path": "api/3/plusAppends/{id}"},
    {"method": "GET", "path": "api/3/prism/urlWhitelistings"},
    {"method": "GET", "path": "api/3/savedResponses"},
    {"method": "GET", "path": "api/3/savedResponses/{id}"},
    {"method": "GET", "path": "api/3/scores"},
    {"method": "GET", "path": "api/3/scores/{id}"},
    {"method": "GET", "path": "api/3/segmentMatch/{id}/{id}"},
    {"method": "GET", "path": "api/3/segmentMatch/{id}/{id}/{id}"},
    {"method": "GET", "path": "api/3/segmentMatchAll/{id}"},
    {"method": "GET", "path": "api/3/segmentMatchAll/{id}/{id}"},
    {"method": "GET", "path": "api/3/segmentMatchDetail/{id}/{id}"},
    {"method": "GET", "path": "api/3/segmentMatchDetail/{id}/{id}/{id}"},
    {"method": "GET", "path": "api/3/segmentMatchSome/{id}/{id}"},
    {"method": "GET", "path": "api/3/segmentsV2/{id}"},
    {"method": "GET", "path": "api/3/segmentsV2/{id}/createdDate/{id}"},
    {"method": "GET", "path": "api/3/segmentsV2/{id}/translate"},
    {"method": "GET", "path": "api/3/settings/account"},
    {"method": "GET", "path": "api/3/settings/dkim"},
    {"method": "GET", "path": "api/3/siteTracking"},
    {"method": "GET", "path": "api/3/siteTracking/code"},
    {"method": "GET", "path": "api/3/siteTrackingDomains"},
    {"method": "GET", "path": "api/3/sms"},
    {"method": "GET", "path": "api/3/sms/10dlc/areacode"},
    {"method": "GET", "path": "api/3/sms/10dlc/areacodes"},
    {"method": "GET", "path": "api/3/sms/10dlc/brand"},
    {"method": "GET", "path": "api/3/sms/10dlc/campaign"},
    {"method": "GET", "path": "api/3/sms/10dlc/campaign/{id}"},
    {"method": "GET", "path": "api/3/sms/broadcasts"},
    {"method": "GET", "path": "api/3/sms/broadcasts/ai/{id}"},
    {"method": "GET", "path": "api/3/sms/broadcasts/hours"},
    {"method": "POST", "path": "api/3/sms/broadcasts/metrics"},
    {"method": "GET", "path": "api/3/sms/broadcasts/metrics/snapshot"},
    {"method": "POST", "path": "api/3/sms/broadcasts/metrics/snapshot"},
    {"method": "GET", "path": "api/3/sms/broadcasts/metrics/{id}/failures"},
    {"method": "GET", "path": "api/3/sms/broadcasts/{id}"},
    {"method": "GET", "path": "api/3/sms/broadcasts/{id}/recipients"},
    {"method": "GET", "path": "api/3/sms/credits"},
    {"method": "GET", "path": "api/3/sms/lists"},
    {"method": "GET", "path": "api/3/sms/{id}"},
    {"method": "GET", "path": "api/3/statsActivityItem/get"},
    {"method": "GET", "path": "api/3/statsActivityItem/get_series"},
    {"method": "GET", "path": "api/3/tags"},
    {"method": "GET", "path": "api/3/tags/{id}"},
    {"method": "GET", "path": "api/3/taskNotifications"},
    {"method": "GET", "path": "api/3/taskOutcomes"},
    {"method": "GET", "path": "api/3/taskOutcomes/{id}"},
    {"method": "GET", "path": "api/3/tasktypeOutcomeRels"},
    {"method": "GET", "path": "api/3/tasktypeOutcomeRels/{id}"},
    {"method": "GET", "path": "api/3/templates"},
    {"method": "GET", "path": "api/3/templates/{id}"},
    {"method": "GET", "path": "api/3/trackingLogs"},
    {"method": "GET", "path": "api/3/trackingLogs/{id}"},
    {"method": "GET", "path": "api/3/trackingLogs/{id}/contact"},
    {"method": "GET", "path": "api/3/users"},
    {"method": "GET", "path": "api/3/users/email/{id}"},
    {"method": "GET", "path": "api/3/users/me"},
    {"method": "GET", "path": "api/3/users/username/{id}"},
    {"method": "GET", "path": "api/3/users/{id}"},
    {"method": "GET", "path": "api/3/webhook/events"},
    {"method": "GET", "path": "api/3/webhooks"},
    {"method": "GET", "path": "api/3/webhooks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The ActiveCampaign endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/3/accountContacts | read | accountcontacts | List all associations. |
| POST | api/3/accountContacts | write | accountcontacts | Create an association. |
| GET | api/3/accountContacts/{id} | read | accountcontacts | Retrieve an association. |
| PUT | api/3/accountContacts/{id} | write | accountcontacts | Update an association. |
| DELETE | api/3/accountContacts/{id} | write | accountcontacts | Delete an association. |
| GET | api/3/accountCustomFieldData | read | accountcustomfielddata | List account custom field values. |
| POST | api/3/accountCustomFieldData | write | accountcustomfielddata | Set an account custom field value. |
| POST | api/3/accountCustomFieldData/bulkCreate | write | accountcustomfielddata | Bulk create a custom account field value. |
| PATCH | api/3/accountCustomFieldData/bulkUpdate | write | accountcustomfielddata | Bulk update account custom field values. |
| GET | api/3/accountCustomFieldData/{id} | read | accountcustomfielddata | Retrieve an account custom field value. |
| PUT | api/3/accountCustomFieldData/{id} | write | accountcustomfielddata | Update an account custom field value. |
| DELETE | api/3/accountCustomFieldData/{id} | write | accountcustomfielddata | Delete an account custom field value. |
| GET | api/3/accountCustomFieldMeta | read | accountcustomfieldmeta | List account custom fields. |
| POST | api/3/accountCustomFieldMeta | write | accountcustomfieldmeta | Create an account custom field. |
| GET | api/3/accountCustomFieldMeta/{id} | read | accountcustomfieldmeta | Retrieve an account custom field. |
| PUT | api/3/accountCustomFieldMeta/{id} | write | accountcustomfieldmeta | Update an account custom field. |
| DELETE | api/3/accountCustomFieldMeta/{id} | write | accountcustomfieldmeta | Delete an account custom field. |
| GET | api/3/accounts | read | accounts | List all accounts. |
| POST | api/3/accounts | write | accounts | Create an account. |
| DELETE | api/3/accounts/bulk_delete | write | accounts | Bulk delete accounts. |
| GET | api/3/accounts/{id} | read | accounts | Retrieve an account. |
| PUT | api/3/accounts/{id} | write | accounts | Update an account. |
| DELETE | api/3/accounts/{id} | write | accounts | Delete an account. |
| POST | api/3/accounts/{id}/notes | write | accounts | Create an account note. |
| PUT | api/3/accounts/{id}/notes/{id} | write | accounts | Update an account note. |
| GET | api/3/activities | read | activities | List a contact's activity history: recent events such as campaign emails sent, link clicks, list and automation changes, notes. |
| GET | api/3/activities/{id} | read | activities | Retrieve one activity entry. |
| GET | api/3/activityRecipients | read | activityrecipients | List all activity recipients. |
| GET | api/3/activityRecipients/{id} | read | activityrecipients | Retrieve an activity recipient. |
| GET | api/3/activityRecipients/{id}/activity | read | activityrecipients | Retrieve the activity of an activity recipient. |
| GET | api/3/activityRecipients/{id}/recipient | read | activityrecipients | Retrieve the recipient of an activity recipient. |
| GET | api/3/addresses | read | addresses | List all addresses. |
| POST | api/3/addresses | write | addresses | Create an address. |
| GET | api/3/addresses/{id} | read | addresses | Retrieve an address. |
| PUT | api/3/addresses/{id} | write | addresses | Update an address. |
| DELETE | api/3/addresses/{id} | write | addresses | Delete an address. |
| GET | api/3/addressGroups | read | addressgroups | List all addressGroups. |
| POST | api/3/addressGroups | write | addressgroups | Create an addressGroup. |
| DELETE | api/3/addressGroups | write | addressgroups | Delete an addressGroup by address and group. |
| GET | api/3/addressGroups/{id} | read | addressgroups | Retrieve an addressGroup. |
| PUT | api/3/addressGroups/{id} | write | addressgroups | Update an addressGroup. |
| DELETE | api/3/addressGroups/{id} | write | addressgroups | Delete address associated with a specific user group. |
| GET | api/3/addressLists | read | addresslists | List all addressLists. |
| POST | api/3/addressLists | write | addresslists | Create an addressList. |
| DELETE | api/3/addressLists | write | addresslists | Delete an addressList by address and list. |
| GET | api/3/addressLists/{id} | read | addresslists | Retrieve an addressList. |
| PUT | api/3/addressLists/{id} | write | addresslists | Update an addressList. |
| DELETE | api/3/addressLists/{id} | write | addresslists | Delete address associated with a specific list. |
| POST | api/3/ai/automations/build | write | ai | Save an automation from a drafted schema. |
| POST | api/3/ai/automations/schema | write | ai | Draft an automation from a prompt. |
| GET | api/3/ai/brand | read | ai | List all brand kits. |
| POST | api/3/ai/brand | write | ai | Create a brand kit. |
| GET | api/3/ai/brand/primary | read | ai | Retrieve the default (primary) brand kit. |
| GET | api/3/ai/brand/{id} | read | ai | Retrieve a brand kit. |
| PATCH | api/3/ai/brand/{id} | write | ai | Update a brand kit. |
| DELETE | api/3/ai/brand/{id} | write | ai | Delete a brand kit. |
| GET | api/3/ai/brand/{id}/brand-history | read | ai | Retrieve a brand kit's website history. |
| GET | api/3/ai/brand/{id}/competitors | read | ai | Retrieve a brand kit's competitors. |
| PATCH | api/3/ai/brand/{id}/primary | write | ai | Set the default (primary) brand kit. |
| GET | api/3/ai/brand/{id}/tone | read | ai | Retrieve a brand kit's tone. |
| POST | api/3/ai/brand/{id}/tone | write | ai | Refresh a brand kit's tone. |
| POST | api/3/ai/customization/account-instructions | write | ai | Create the AI instruction of the account. |
| PUT | api/3/ai/customization/account-instructions | write | ai | Update the AI instruction of the account. |
| DELETE | api/3/ai/customization/account-instructions | write | ai | Delete the AI instruction of the account. |
| GET | api/3/ai/customization/instructions | read | ai | List the AI instructions of the account. |
| GET | api/3/ai/ecom/customerBehaviorSummary | read | ai | Retrieve an ecommerce customer behavior summary. |
| GET | api/3/ai/ecom/orderStatusSummary | read | ai | Retrieve an ecommerce order status summary. |
| GET | api/3/ai/ecom/productRankings | read | ai | Retrieve ranked ecommerce products. |
| GET | api/3/ai/ecom/revenueSummary | read | ai | Retrieve an ecommerce revenue summary. |
| GET | api/3/ai/report_trends_activity | read | ai | Retrieve contact trends for a list. |
| GET | api/3/audiences | read | audiences | List Summaries for Saved Segments. |
| GET | api/3/audiences/{id} | read | audiences | Retrieve a Saved Segment's Summary. |
| GET | api/3/automations | read | automations | List all automations. |
| POST | api/3/automations/bulk_edit | write | automations | Bulk edit automations. |
| GET | api/3/automations/{id} | read | automations | Retrieve an automation. |
| GET | api/3/automations/{id}/blocks | read | automations | Retrieve an automation's blocks. |
| GET | api/3/automations/{id}/contactAutomations | read | automations | List all contacts in an automation. |
| GET | api/3/automations/{id}/contactAutomations/{id}/steps | read | automations | Retrieve recorded steps for one contact automation run. |
| GET | api/3/automations/{id}/triggers | read | automations | Retrieve an automation's start triggers. |
| GET | api/3/bounceLogs | read | bouncelogs | List all bounce logs. |
| GET | api/3/brandings | read | brandings | List all brandings. |
| GET | api/3/brandings/{id} | read | brandings | Retrieve a branding. |
| PUT | api/3/brandings/{id} | write | brandings | Update a branding. |
| GET | api/3/businessGoals/data | read | businessgoals | List business goals (agent-oriented read). |
| GET | api/3/businessGoals/data/{id} | read | businessgoals | Retrieve a business goal (agent-oriented read). |
| GET | api/3/calendars | read | calendars | List all calendar feeds. |
| POST | api/3/calendars | write | calendars | Create a calendar feed. |
| GET | api/3/calendars/{id} | read | calendars | Retrieve a calendar feed. |
| PUT | api/3/calendars/{id} | write | calendars | Update a calendar feed. |
| DELETE | api/3/calendars/{id} | write | calendars | Delete a calendar feed. |
| POST | api/3/campaign | write | campaign | Create Campaign. |
| POST | api/3/campaignMessages | write | campaignmessages | Create a campaign message. |
| PUT | api/3/campaignMessages/{id} | write | campaignmessages | Update a campaign message. |
| DELETE | api/3/campaignMessages/{id} | write | campaignmessages | Delete a campaign message. |
| GET | api/3/campaigns | read | campaigns | List all campaigns. |
| DELETE | api/3/campaigns/bulk_delete | write | campaigns | Delete multiple campaigns. |
| POST | api/3/campaigns/test-preview | write | campaigns | Preview a campaign message. |
| POST | api/3/campaigns/test-send | write | campaigns | Send a test of a campaign. |
| GET | api/3/campaigns/{id} | read | campaigns | Retrieve a campaign. |
| GET | api/3/campaigns/{id}/campaignMessages | read | campaigns | Retrieve campaign messages associated to campaign. |
| POST | api/3/campaigns/{id}/copy | write | campaigns | Duplicate Campaign. |
| DELETE | api/3/campaigns/{id}/delete | write | campaigns | Delete a campaign. |
| PUT | api/3/campaigns/{id}/edit | write | campaigns | Edit campaign. |
| PUT | api/3/campaigns/{id}/enable | write | campaigns | Schedule a campaign. |
| GET | api/3/campaigns/{id}/links | read | campaigns | Retrieve links associated to campaign. |
| PUT | api/3/campaigns/{id}/pause | write | campaigns | Pause a sending campaign. |
| GET | api/3/campaigns/{id}/reportTotals | read | campaigns | Retrieve the report totals of a campaign. |
| GET | api/3/campaigns/{id}/reports/bounces | read | campaigns | List the contacts whose campaign email bounced. |
| GET | api/3/campaigns/{id}/reports/forwards | read | campaigns | List the forwards of a campaign. |
| GET | api/3/campaigns/{id}/reports/opens | read | campaigns | List the contacts who opened a campaign. |
| GET | api/3/campaigns/{id}/reports/unopens | read | campaigns | List the contacts who did not open a campaign. |
| GET | api/3/campaigns/{id}/reports/unsubscribes | read | campaigns | List the contacts who unsubscribed through a campaign. |
| PUT | api/3/campaigns/{id}/resume | write | campaigns | Resume a paused campaign. |
| PUT | api/3/campaigns/{id}/stop | write | campaigns | Stop a campaign. |
| GET | api/3/channel/whatsapp/channels/whatsapp/template | read | channel | List WhatsApp Templates. |
| GET | api/3/channel/whatsapp/channels/whatsapp/template/{id} | read | channel | Get WhatsApp Template. |
| PUT | api/3/channel/whatsapp/channels/whatsapp/template/{id} | write | channel | Update WhatsApp Template. |
| DELETE | api/3/channel/whatsapp/channels/whatsapp/template/{id} | write | channel | Delete WhatsApp Template. |
| POST | api/3/channel/whatsapp/channels/whatsapp/template/{id}/send | write | channel | Send a WhatsApp Template. |
| GET | api/3/channel/whatsapp/flow-execution | read | channel | List Flow Executions. |
| GET | api/3/channel/whatsapp/flow-execution-contact | read | channel | List Flow Execution Contacts. |
| GET | api/3/channel/whatsapp/flow-execution-contact/{id} | read | channel | Get Flow Execution Contact by Id. |
| GET | api/3/channel/whatsapp/flow-execution/{id} | read | channel | Get Flow Execution. |
| POST | api/3/channel/whatsapp/flow/{id}/run | write | channel | Create a Flow Execution. |
| GET | api/3/channel/whatsapp/inbox/conversation | read | channel | List Conversations. |
| PUT | api/3/channel/whatsapp/inbox/conversation/{id}/update | write | channel | Update a conversation. |
| PATCH | api/3/channel/whatsapp/inbox/conversation/{id}/update | write | channel | Partially Update a Conversation. |
| PUT | api/3/configs/{id} | write | configs | Update settings. |
| GET | api/3/connections | read | connections | List all connections. |
| POST | api/3/connections | write | connections | Create a connection. |
| GET | api/3/connections/{id} | read | connections | Retrieve a connection. |
| PUT | api/3/connections/{id} | write | connections | Update a connection. |
| DELETE | api/3/connections/{id} | write | connections | Delete a connection. |
| POST | api/3/contact/bulkSync | write | contact | Bulk sync contacts. |
| POST | api/3/contact/merge | write | contact | Merge two contacts. |
| POST | api/3/contact/sync | write | contact | Create or update a contact by email (upsert). |
| GET | api/3/contactArchives | read | contactarchives | List archived contacts. |
| POST | api/3/contactArchives/deleteList | write | contactarchives | Permanently delete several archived contacts. |
| POST | api/3/contactArchives/restoreAll | write | contactarchives | Restore all matching archived contacts. |
| GET | api/3/contactArchives/restoreRequest | read | contactarchives | List running contact restores. |
| POST | api/3/contactArchives/restoreRequest | write | contactarchives | Restore archived contacts by id. |
| GET | api/3/contactArchives/restoreRequest/{id} | read | contactarchives | Retrieve a contact restore. |
| GET | api/3/contactArchives/{id} | read | contactarchives | Retrieve an archived contact. |
| DELETE | api/3/contactArchives/{id} | write | contactarchives | Permanently delete an archived contact. |
| GET | api/3/contactAutomationLogs | read | contactautomationlogs | List all contact automation history entries. |
| GET | api/3/contactAutomationLogs/{id} | read | contactautomationlogs | Retrieve a contact automation history entry. |
| GET | api/3/contactAutomations | read | contactautomations | List all automations a contact is in. |
| POST | api/3/contactAutomations | write | contactautomations | Add a contact to an automation. |
| DELETE | api/3/contactAutomations | write | contactautomations | Remove a contact from an automation by contact and automation. |
| GET | api/3/contactAutomations/{id} | read | contactautomations | Retrieve an automation a contact is in. |
| PUT | api/3/contactAutomations/{id} | write | contactautomations | Update a contact automation. |
| DELETE | api/3/contactAutomations/{id} | write | contactautomations | Remove a contact from an automation. |
| GET | api/3/contactAutomations/{id}/automation | read | contactautomations | Retrieve the automation of a contact automation. |
| GET | api/3/contactAutomations/{id}/automationLogs | read | contactautomations | List the history of a contact automation. |
| GET | api/3/contactAutomations/{id}/contact | read | contactautomations | Retrieve the contact of a contact automation. |
| GET | api/3/contactAutomations/{id}/contactGoals | read | contactautomations | List the goals reached in a contact automation. |
| GET | api/3/contactAutomations/{id}/subscriberSeriesEnd | read | contactautomations | Retrieve how a contact automation ended. |
| GET | api/3/contactConversionPoints | read | contactconversionpoints | List all contact conversion points. |
| GET | api/3/contactConversionPoints/{id} | read | contactconversionpoints | Retrieve a contact conversion point. |
| GET | api/3/contactConversionPoints/{id}/attributions | read | contactconversionpoints | List the attributions of a contact conversion point. |
| GET | api/3/contactConversionPoints/{id}/contact | read | contactconversionpoints | Retrieve the contact of a contact conversion point. |
| GET | api/3/contactConversions | read | contactconversions | List all contact conversions. |
| GET | api/3/contactConversions/{id} | read | contactconversions | Retrieve a contact conversion. |
| GET | api/3/contactConversions/{id}/activities | read | contactconversions | List the activities of a contact conversion. |
| GET | api/3/contactConversions/{id}/attributions | read | contactconversions | List the attributions of a contact conversion. |
| GET | api/3/contactConversions/{id}/contact | read | contactconversions | Retrieve the contact of a contact conversion. |
| GET | api/3/contactConversions/{id}/conversion | read | contactconversions | Retrieve the conversion of a contact conversion. |
| GET | api/3/contactConversions/{id}/conversiontrigger | read | contactconversions | Retrieve the trigger of a contact conversion. |
| GET | api/3/contactData | read | contactdata | List contact data records. |
| GET | api/3/contactData/{id} | read | contactdata | Retrieve a contact data record. |
| GET | api/3/contactDeals | read | contactdeals | List all secondary contacts. |
| POST | api/3/contactDeals | write | contactdeals | Create a secondary contact. |
| GET | api/3/contactDeals/{id} | read | contactdeals | Retrieve a secondary contact. |
| PUT | api/3/contactDeals/{id} | write | contactdeals | Update a secondary contact. |
| DELETE | api/3/contactDeals/{id} | write | contactdeals | Delete a secondary contact. |
| GET | api/3/contactEmails | read | contactemails | List contact emails. |
| GET | api/3/contactEmails/{id} | read | contactemails | Retrieve a contact email. |
| GET | api/3/contactGoalLists | read | contactgoallists | List all contact goal list entries. |
| GET | api/3/contactGoalLists/{id} | read | contactgoallists | Retrieve a contact goal list entry. |
| GET | api/3/contactGoalLists/{id}/contactGoal | read | contactgoallists | Retrieve the reached goal of a contact goal list entry. |
| GET | api/3/contactGoalLists/{id}/list | read | contactgoallists | Retrieve the list of a contact goal list entry. |
| GET | api/3/contactGoals | read | contactgoals | List goal completions. |
| GET | api/3/contactGoals/{id} | read | contactgoals | Retrieve a goal completion. |
| GET | api/3/contactGoals/{id}/automation | read | contactgoals | Retrieve the automation of a goal completion. |
| GET | api/3/contactGoals/{id}/contact | read | contactgoals | Retrieve the contact of a goal completion. |
| GET | api/3/contactGoals/{id}/contactAutomation | read | contactgoals | Retrieve the contact automation of a goal completion. |
| GET | api/3/contactGoals/{id}/contactGoalLists | read | contactgoals | List the lists of a goal completion. |
| GET | api/3/contactGoals/{id}/contactGoalTags | read | contactgoals | List the tags of a goal completion. |
| GET | api/3/contactGoals/{id}/goal | read | contactgoals | Retrieve the goal of a goal completion. |
| GET | api/3/contactGoalTags | read | contactgoaltags | List all contact goal tag entries. |
| GET | api/3/contactGoalTags/{id} | read | contactgoaltags | Retrieve a contact goal tag entry. |
| GET | api/3/contactGoalTags/{id}/contactGoal | read | contactgoaltags | Retrieve the reached goal of a contact goal tag entry. |
| GET | api/3/contactGoalTags/{id}/tag | read | contactgoaltags | Retrieve the tag of a contact goal tag entry. |
| GET | api/3/contactImports | read | contactimports | List contact import log rows. |
| GET | api/3/contactImports/{id} | read | contactimports | Retrieve a contact import log row. |
| GET | api/3/contactLists | read | contactlists | List contact subscriptions to lists. |
| POST | api/3/contactLists | write | contactlists | Update list status for a contact. |
| GET | api/3/contactLists/{id} | read | contactlists | Retrieve a contact list subscription. |
| PUT | api/3/contactLists/{id} | write | contactlists | Update a contact list subscription. |
| GET | api/3/contactLogs | read | contactlogs | List all contact log entries. |
| GET | api/3/contactLogs/{id} | read | contactlogs | Retrieve a contact log entry. |
| GET | api/3/contacts | read | contacts | List, search, and filter contacts. |
| POST | api/3/contacts | write | contacts | Create a contact. |
| DELETE | api/3/contacts/bulk_delete | write | contacts | Delete multiple contacts. |
| GET | api/3/contacts/{id} | read | contacts | Retrieve a contact. |
| PUT | api/3/contacts/{id} | write | contacts | Update a contact. |
| DELETE | api/3/contacts/{id} | write | contacts | Delete a contact. |
| GET | api/3/contacts/{id}/accountContacts | read | contacts | Retrieve a contacts account contacts. |
| GET | api/3/contacts/{id}/automationEntryCounts | read | contacts | Retrieve a contacts automation entry counts. |
| GET | api/3/contacts/{id}/bounceLogs | read | contacts | Retrieve a contact's bounce logs. |
| GET | api/3/contacts/{id}/contactAutomations | read | contacts | List all automations the contact is in. |
| GET | api/3/contacts/{id}/contactData | read | contacts | Retrieve a contact's data. |
| GET | api/3/contacts/{id}/contactDeals | read | contacts | Retrieve a list of contact's deals. |
| GET | api/3/contacts/{id}/contactGoals | read | contacts | Retrieve a contact's goals. |
| GET | api/3/contacts/{id}/contactLists | read | contacts | Retrieve a contact's list memberships. |
| GET | api/3/contacts/{id}/contactLogs | read | contacts | Retrieve a contact's logs. |
| GET | api/3/contacts/{id}/contactTags | read | contacts | List the tags applied to a contact. |
| GET | api/3/contacts/{id}/deals | read | contacts | Retrieve a contact's deals. |
| GET | api/3/contacts/{id}/fieldValues | read | contacts | Retrieve a contact's field values. |
| GET | api/3/contacts/{id}/geoIps | read | contacts | Retrieve a contacts list of geo-ips. |
| GET | api/3/contacts/{id}/notes | read | contacts | Retrieve a contact's notes. |
| POST | api/3/contacts/{id}/notes | write | contacts | Create a note on a contact. |
| PUT | api/3/contacts/{id}/notes/{id} | write | contacts | Update a note on a contact. |
| DELETE | api/3/contacts/{id}/notes/{id} | write | contacts | Delete a note from a contact. |
| GET | api/3/contacts/{id}/organization | read | contacts | Retrieve a contacts organization. |
| GET | api/3/contacts/{id}/plusAppend | read | contacts | Retrieve a contacts plus append. |
| GET | api/3/contacts/{id}/scoreValues | read | contacts | Retrieve a contact's score value. |
| POST | api/3/contacts/{id}/tags | write | contacts | Apply tags to a contact. |
| DELETE | api/3/contacts/{id}/tags | write | contacts | Remove a tag from a contact by tag name. |
| DELETE | api/3/contacts/{id}/tags/{id} | write | contacts | Remove a tag from a contact by tag id. |
| GET | api/3/contacts/{id}/trackingLogs | read | contacts | Retrieve a contacts tracking logs. |
| GET | api/3/contactTags | read | contacttags | List all contact-tag associations. |
| POST | api/3/contactTags | write | contacttags | Add a tag to contact. |
| GET | api/3/contactTags/{id} | read | contacttags | Retrieve a contact tag. |
| DELETE | api/3/contactTags/{id} | write | contacttags | Remove a tag from a contact. |
| GET | api/3/content/domainAuth | read | content | Check the email authentication of a From address domain. |
| GET | api/3/content/editorMarkup/{id} | read | content | Get Editor Markup. |
| GET | api/3/content-proxy/files | read | content-proxy | Search the Content Manager for files. |
| GET | api/3/content-proxy/files/{id} | read | content-proxy | Retrieve a Content Manager file. |
| GET | api/3/content-proxy/files/{id}/folders | read | content-proxy | Show which folders a Content Manager file is in. |
| GET | api/3/content-proxy/files/{id}/tags | read | content-proxy | List the keywords on a Content Manager file. |
| GET | api/3/content-proxy/folders | read | content-proxy | List all Content Manager folders. |
| GET | api/3/content-proxy/folders/{id} | read | content-proxy | Retrieve a Content Manager folder. |
| GET | api/3/content-proxy/folders/{id}/files | read | content-proxy | List the files in a Content Manager folder. |
| GET | api/3/content-proxy/tags/{id}/files | read | content-proxy | List the files with a keyword. |
| GET | api/3/conversions | read | conversions | List conversions. |
| POST | api/3/conversions | write | conversions | Create a conversion. |
| GET | api/3/conversions/data | read | conversions | List conversion statistics. |
| GET | api/3/conversions/labels | read | conversions | List conversion labels. |
| POST | api/3/conversions/labels | write | conversions | Create a conversion label. |
| POST | api/3/conversions/labels/bulkCreate | write | conversions | Bulk-create conversion labels. |
| DELETE | api/3/conversions/labels/bulkDelete | write | conversions | Bulk-delete conversion labels. |
| PUT | api/3/conversions/labels/target | write | conversions | Set a conversion's target for a business goal. |
| GET | api/3/conversions/labels/{id} | read | conversions | Retrieve a conversion label. |
| PUT | api/3/conversions/labels/{id} | write | conversions | Update a conversion label. |
| DELETE | api/3/conversions/labels/{id} | write | conversions | Delete a conversion label. |
| DELETE | api/3/conversions/labels/{id}/goal | write | conversions | Disable a conversion label's business-goal target. |
| GET | api/3/conversions/metrics | read | conversions | List conversion metrics. |
| GET | api/3/conversions/{id} | read | conversions | Retrieve a conversion. |
| PUT | api/3/conversions/{id} | write | conversions | Update a conversion. |
| PATCH | api/3/conversions/{id} | write | conversions | Update a conversion (PATCH). |
| DELETE | api/3/conversions/{id} | write | conversions | Delete a conversion. |
| GET | api/3/conversions/{id}/data | read | conversions | Retrieve a conversion's statistics. |
| DELETE | api/3/conversions/{id}/goal/{id}/labels/target | write | conversions | Disable a conversion's target for a business goal. |
| GET | api/3/conversions/{id}/metrics | read | conversions | Retrieve a conversion's metrics. |
| GET | api/3/conversions/{id}/trends | read | conversions | Retrieve a conversion's daily trend data. |
| GET | api/3/customObjects/records/{id} | read | customobjects | List records by schema. |
| POST | api/3/customObjects/records/{id} | write | customobjects | Create or update record. |
| GET | api/3/customObjects/records/{id}/external/{id} | read | customobjects | Get a record by external id. |
| DELETE | api/3/customObjects/records/{id}/external/{id} | write | customobjects | Delete a record by external ID. |
| GET | api/3/customObjects/records/{id}/{id} | read | customobjects | Get a record by id. |
| DELETE | api/3/customObjects/records/{id}/{id} | write | customobjects | Delete a record by id. |
| GET | api/3/customObjects/schemas | read | customobjects | List all schemas. |
| POST | api/3/customObjects/schemas | write | customobjects | Create a schema. |
| POST | api/3/customObjects/schemas/public | write | customobjects | Create a public schema. |
| GET | api/3/customObjects/schemas/{id} | read | customobjects | Retrieve a schema. |
| PUT | api/3/customObjects/schemas/{id} | write | customobjects | Update a schema. |
| DELETE | api/3/customObjects/schemas/{id} | write | customobjects | Delete a schema. |
| POST | api/3/customObjects/schemas/{id}/child | write | customobjects | Create a child schema. |
| DELETE | api/3/customObjects/schemas/{id}/fields/{id} | write | customobjects | Delete a field. |
| GET | api/3/dealActivities | read | dealactivities | List all deal activities. |
| GET | api/3/dealCustomFieldData | read | dealcustomfielddata | List deal custom field values. |
| POST | api/3/dealCustomFieldData | write | dealcustomfielddata | Set a deal custom field value. |
| POST | api/3/dealCustomFieldData/bulkCreate | write | dealcustomfielddata | Bulk create a custom deal field value. |
| PATCH | api/3/dealCustomFieldData/bulkUpdate | write | dealcustomfielddata | Bulk update deal custom field values. |
| GET | api/3/dealCustomFieldData/{id} | read | dealcustomfielddata | Retrieve a deal custom field value. |
| PUT | api/3/dealCustomFieldData/{id} | write | dealcustomfielddata | Update a deal custom field value. |
| DELETE | api/3/dealCustomFieldData/{id} | write | dealcustomfielddata | Delete a deal custom field value. |
| GET | api/3/dealCustomFieldMeta | read | dealcustomfieldmeta | List deal custom fields. |
| POST | api/3/dealCustomFieldMeta | write | dealcustomfieldmeta | Create a deal custom field. |
| GET | api/3/dealCustomFieldMeta/{id} | read | dealcustomfieldmeta | Retrieve a deal custom field. |
| PUT | api/3/dealCustomFieldMeta/{id} | write | dealcustomfieldmeta | Update a deal custom field. |
| DELETE | api/3/dealCustomFieldMeta/{id} | write | dealcustomfieldmeta | Delete a deal custom field. |
| GET | api/3/dealGroup/get_inaccessible_deal_groups | read | dealgroup | Retrieve inaccessible pipelines by user. |
| GET | api/3/dealGroups | read | dealgroups | List all pipelines. |
| POST | api/3/dealGroups | write | dealgroups | Create a pipeline. |
| GET | api/3/dealGroups/{id} | read | dealgroups | Retrieve a pipeline. |
| PUT | api/3/dealGroups/{id} | write | dealgroups | Update a pipeline. |
| DELETE | api/3/dealGroups/{id} | write | dealgroups | Delete a pipeline. |
| GET | api/3/dealRoles | read | dealroles | List all deal roles. |
| POST | api/3/dealRoles | write | dealroles | Create a deal role. |
| DELETE | api/3/dealRoles/{id} | write | dealroles | Delete a deal role. |
| GET | api/3/deals | read | deals | List all deals. |
| POST | api/3/deals | write | deals | Create a deal. |
| PATCH | api/3/deals/bulkUpdate | write | deals | Bulk Update Deal Owners. |
| GET | api/3/deals/{id} | read | deals | Retrieve a deal. |
| PUT | api/3/deals/{id} | write | deals | Update a deal. |
| DELETE | api/3/deals/{id} | write | deals | Delete a deal. |
| GET | api/3/deals/{id}/notes | read | deals | Retrieve a deal's notes. |
| POST | api/3/deals/{id}/notes | write | deals | Create a deal note. |
| PUT | api/3/deals/{id}/notes/{id} | write | deals | Update a deal note. |
| GET | api/3/dealStages | read | dealstages | List all stages. |
| POST | api/3/dealStages | write | dealstages | Create a stage. |
| GET | api/3/dealStages/{id} | read | dealstages | Retrieve a stage. |
| PUT | api/3/dealStages/{id} | write | dealstages | Update a stage. |
| DELETE | api/3/dealStages/{id} | write | dealstages | Delete a stage. |
| PUT | api/3/dealStages/{id}/deals | write | dealstages | Move deals to another stage. |
| GET | api/3/dealTasks | read | dealtasks | List all tasks. |
| POST | api/3/dealTasks | write | dealtasks | Create a task. |
| GET | api/3/dealTasks/{id} | read | dealtasks | Retrieve a task. |
| PUT | api/3/dealTasks/{id} | write | dealtasks | Update a task. |
| DELETE | api/3/dealTasks/{id} | write | dealtasks | Delete a task. |
| GET | api/3/dealTasktypes | read | dealtasktypes | List all task types. |
| POST | api/3/dealTasktypes | write | dealtasktypes | Create a task type. |
| GET | api/3/dealTasktypes/{id} | read | dealtasktypes | Retrieve a task type. |
| PUT | api/3/dealTasktypes/{id} | write | dealtasktypes | Update a task type. |
| DELETE | api/3/dealTasktypes/{id} | write | dealtasktypes | Delete a task type. |
| PUT | api/3/dealTasktypes/{id}/dealTasks | write | dealtasktypes | Move tasks to another task type. |
| GET | api/3/ecomCustomers | read | ecomcustomers | List all customers. |
| POST | api/3/ecomCustomers | write | ecomcustomers | Create a customer. |
| GET | api/3/ecomCustomers/{id} | read | ecomcustomers | Retrieve a customer. |
| PUT | api/3/ecomCustomers/{id} | write | ecomcustomers | Update a customer. |
| DELETE | api/3/ecomCustomers/{id} | write | ecomcustomers | Delete a customer. |
| GET | api/3/ecomOrderProducts | read | ecomorderproducts | List EcomOrderProducts. |
| GET | api/3/ecomOrderProducts/{id} | read | ecomorderproducts | Retrieve an EcomOrderProduct. |
| GET | api/3/ecomOrders | read | ecomorders | List all orders. |
| POST | api/3/ecomOrders | write | ecomorders | Create an order. |
| GET | api/3/ecomOrders/{id} | read | ecomorders | Retrieve an order. |
| PUT | api/3/ecomOrders/{id} | write | ecomorders | Update an order. |
| DELETE | api/3/ecomOrders/{id} | write | ecomorders | Delete an order. |
| GET | api/3/ecomOrders/{id}/orderProducts | read | ecomorders | List EcomOrderProducts for a Specific EcomOrder. |
| GET | api/3/emailActivities | read | emailactivities | List all email activities. |
| GET | api/3/eventTracking | read | eventtracking | Retrieve Event Tracking Status. |
| PUT | api/3/eventTracking | write | eventtracking | Enable/disable. |
| GET | api/3/eventTrackingEvents | read | eventtrackingevents | List all events (names only). |
| POST | api/3/eventTrackingEvents | write | eventtrackingevents | Create a new event (name only). |
| DELETE | api/3/eventTrackingEvents/{id} | write | eventtrackingevents | Delete event (name only). |
| GET | api/3/fieldDetails | read | fielddetails | List the required and default-value settings of standard fields. |
| PUT | api/3/fieldDetails/{id} | write | fielddetails | Update the required and default-value setting of a standard field. |
| PATCH | api/3/fieldDetails/{id} | write | fielddetails | Update the required and default-value setting of a standard field (PATCH). |
| POST | api/3/fieldOption/bulk | write | fieldoption | Create custom field options. |
| PUT | api/3/fieldOption/bulk | write | fieldoption | Update custom field options. |
| GET | api/3/fieldOptions | read | fieldoptions | List all field options. |
| POST | api/3/fieldOptions | write | fieldoptions | Create a field option. |
| GET | api/3/fieldOptions/{id} | read | fieldoptions | Retrieve a field option. |
| PUT | api/3/fieldOptions/{id} | write | fieldoptions | Update a field option. |
| DELETE | api/3/fieldOptions/{id} | write | fieldoptions | Delete a field option. |
| POST | api/3/fieldRel/sync | write | fieldrel | Sync a field's list relationships. |
| POST | api/3/fieldRel/syncExcept | write | fieldrel | Sync a field's list relationships by exclusion. |
| GET | api/3/fieldRels | read | fieldrels | List all custom field relationships to lists. |
| POST | api/3/fieldRels | write | fieldrels | Create a custom field relationship to list(s). |
| GET | api/3/fieldRels/{id} | read | fieldrels | Retrieve a custom field relationship to lists. |
| PUT | api/3/fieldRels/{id} | write | fieldrels | Update a custom field relationship to lists. |
| DELETE | api/3/fieldRels/{id} | write | fieldrels | Delete a custom field relationship to list(s). |
| GET | api/3/fields | read | fields | List contact custom fields. |
| POST | api/3/fields | write | fields | Create a contact custom field. |
| GET | api/3/fields/{id} | read | fields | Get a custom field by ID. |
| PUT | api/3/fields/{id} | write | fields | Update a contact custom field. |
| DELETE | api/3/fields/{id} | write | fields | Delete a contact custom field. |
| GET | api/3/fieldValues | read | fieldvalues | List contact custom field values. |
| POST | api/3/fieldValues | write | fieldvalues | Set a contact custom field value. |
| GET | api/3/fieldValues/{id} | read | fieldvalues | Retrieve a contact custom field value. |
| PUT | api/3/fieldValues/{id} | write | fieldvalues | Update a custom field value for contact. |
| DELETE | api/3/fieldValues/{id} | write | fieldvalues | Delete a contact custom field value. |
| POST | api/3/form/optin | write | form | Create a form's opt-in email. |
| GET | api/3/forms | read | forms | List all forms. |
| POST | api/3/forms | write | forms | Create a form. |
| GET | api/3/forms/{id} | read | forms | Retrieve a form. |
| PUT | api/3/forms/{id} | write | forms | Update a form. |
| DELETE | api/3/forms/{id} | write | forms | Delete a form. |
| PUT | api/3/forms/{id}/allowPersonalEmailProviders | write | forms | Allow personal email addresses on a form. |
| PUT | api/3/forms/{id}/blockPersonalEmailProviders | write | forms | Block personal email addresses on a form. |
| POST | api/3/forms/{id}/blockedEmailDomains | write | forms | Block email domains on a form. |
| DELETE | api/3/forms/{id}/blockedEmailDomains | write | forms | Unblock an email domain on a form. |
| GET | api/3/forms/{id}/html | read | forms | Retrieve a form's HTML. |
| PUT | api/3/forms/{id}/pause | write | forms | Pause a form. |
| PUT | api/3/forms/{id}/resume | write | forms | Resume a paused form. |
| GET | api/3/geoAddresses | read | geoaddresses | List all geo addresses. |
| GET | api/3/geoAddresses/{id} | read | geoaddresses | Retrieve a geo address. |
| GET | api/3/geoIps | read | geoips | List all geo IP entries. |
| GET | api/3/geoIps/{id} | read | geoips | Retrieve a geo IP entry. |
| GET | api/3/geoIps/{id}/geoAddress | read | geoips | Retrieve the location of a geo IP entry. |
| GET | api/3/goal/goalStats | read | goal | Retrieve goal stats. |
| GET | api/3/goal/showcase | read | goal | Retrieve goal showcase. |
| GET | api/3/goals | read | goals | List all goals. |
| GET | api/3/goals/{id} | read | goals | Retrieve a goal. |
| DELETE | api/3/group/bulk_delete | write | group | Delete multiple groups. |
| POST | api/3/groupDefinitions | write | groupdefinitions | Create a Custom Field Group. |
| GET | api/3/groupLimits | read | grouplimits | List All Group Limits. |
| GET | api/3/groupMembers | read | groupmembers | Get All Custom Field Groups. |
| POST | api/3/groupMembers | write | groupmembers | Add Custom Field to Field Group. |
| GET | api/3/groupMembers/{id} | read | groupmembers | Get Custom Field Group by ID. |
| PUT | api/3/groupMembers/{id} | write | groupmembers | Update Custom Field Field Group. |
| DELETE | api/3/groupMembers/{id} | write | groupmembers | Delete Custom Field Field Group. |
| GET | api/3/groups | read | groups | List all groups. |
| POST | api/3/groups | write | groups | Create a group. |
| GET | api/3/groups/{id} | read | groups | Retrieve a group. |
| PUT | api/3/groups/{id} | write | groups | Update a group. |
| DELETE | api/3/groups/{id} | write | groups | Delete a group. |
| GET | api/3/import/bulk_import | read | import | Summarize recent API bulk imports by day. |
| POST | api/3/import/bulk_import | write | import | Bulk import contacts. |
| GET | api/3/import/history | read | import | List contact imports made from the app or by integrations. |
| GET | api/3/import/history/{id}/{id} | read | import | List the rows of an app or integration import that failed or were only partly imported, with reasons. |
| GET | api/3/import/info | read | import | Bulk import status info. |
| GET | api/3/initiatives | read | initiatives | List all business goals. |
| POST | api/3/initiatives | write | initiatives | Create a business goal. |
| POST | api/3/initiatives/buildbusinessgoal | write | initiatives | Build a business goal from a schema. |
| PUT | api/3/initiatives/bulkArchive | write | initiatives | Archive multiple business goals. |
| GET | api/3/initiatives/{id} | read | initiatives | Retrieve a business goal. |
| PUT | api/3/initiatives/{id} | write | initiatives | Update a business goal. |
| PUT | api/3/initiatives/{id}/archive | write | initiatives | Archive a business goal. |
| GET | api/3/listGroups | read | listgroups | List all list group permissions. |
| POST | api/3/listGroups | write | listgroups | Create a list group permission. |
| GET | api/3/listGroups/{id} | read | listgroups | Retrieve a list group permission. |
| PUT | api/3/listGroups/{id} | write | listgroups | Update a list group permission. |
| DELETE | api/3/listGroups/{id} | write | listgroups | Delete a list group permission. |
| GET | api/3/lists | read | lists | Retrieve all lists. |
| POST | api/3/lists | write | lists | Create a list. |
| GET | api/3/lists/exclusions | read | lists | Retrieve exclusions list. |
| GET | api/3/lists/exclusions/{id} | read | lists | Retrieve an exclusion. |
| PUT | api/3/lists/exclusions/{id} | write | lists | Update an exclusion. |
| GET | api/3/lists/{id} | read | lists | Retrieve a list. |
| PUT | api/3/lists/{id} | write | lists | Update a list. |
| DELETE | api/3/lists/{id} | write | lists | Delete a list. |
| GET | api/3/message/source | read | message | Retrieve the source of a campaign message. |
| GET | api/3/messages | read | messages | List all messages. |
| POST | api/3/messages | write | messages | Create a message. |
| DELETE | api/3/messages/bulk_delete | write | messages | Delete multiple messages. |
| GET | api/3/messages/{id} | read | messages | Retrieve a message. |
| PUT | api/3/messages/{id} | write | messages | Update a message. |
| DELETE | api/3/messages/{id} | write | messages | Delete a message. |
| GET | api/3/notes | read | notes | Retrieve list of all notes. |
| POST | api/3/notes | write | notes | Create a note on a contact, deal, task, activity, or account. |
| GET | api/3/notes/{id} | read | notes | Retrieve a note. |
| PUT | api/3/notes/{id} | write | notes | Update a note. |
| DELETE | api/3/notes/{id} | write | notes | Delete a note. |
| GET | api/3/personalizations | read | personalizations | List Variables. |
| POST | api/3/personalizations | write | personalizations | Create a Variable. |
| DELETE | api/3/personalizations/bulkdelete | write | personalizations | Bulk Delete Variables. |
| GET | api/3/personalizations/{id} | read | personalizations | Retrieve a Variable. |
| PUT | api/3/personalizations/{id} | write | personalizations | Edit a Variable. |
| DELETE | api/3/personalizations/{id} | write | personalizations | Delete a Variable. |
| PATCH | api/3/personalizations/{id}/lock | write | personalizations | . |
| PATCH | api/3/personalizations/{id}/unlock | write | personalizations | . |
| GET | api/3/persTags | read | perstags | List all personalization tags. |
| GET | api/3/plusAppends | read | plusappends | List contact social profile records. |
| GET | api/3/plusAppends/{id} | read | plusappends | Retrieve a contact social profile record. |
| GET | api/3/prism/urlWhitelistings | read | prism | List all whitelisted domains. |
| POST | api/3/prism/urlWhitelistings | write | prism | Add domain to whitelist. |
| DELETE | api/3/prism/urlWhitelistings/{id} | write | prism | Remove domain from whitelist. |
| GET | api/3/savedResponses | read | savedresponses | List all saved responses. |
| POST | api/3/savedResponses | write | savedresponses | Create a saved response. |
| GET | api/3/savedResponses/{id} | read | savedresponses | Retrieve a saved response. |
| PUT | api/3/savedResponses/{id} | write | savedresponses | Update a saved response. |
| DELETE | api/3/savedResponses/{id} | write | savedresponses | Delete a saved response. |
| GET | api/3/scores | read | scores | List all scores. |
| GET | api/3/scores/{id} | read | scores | Retrieve a score. |
| GET | api/3/segmentMatch/{id}/{id} | read | segmentmatch | Create a Match One Request. |
| GET | api/3/segmentMatch/{id}/{id}/{id} | read | segmentmatch | Check to see if a Contact matches a Segment using the given externalId. |
| POST | api/3/segmentMatchAll | write | segmentmatchall | Create a Match All Request for a new Segment. |
| GET | api/3/segmentMatchAll/{id} | read | segmentmatchall | Create a Match All Request. |
| GET | api/3/segmentMatchAll/{id}/{id} | read | segmentmatchall | Return Match All result-set. |
| GET | api/3/segmentMatchDetail/{id}/{id} | read | segmentmatchdetail | Explain whether a Contact matches a Segment. |
| GET | api/3/segmentMatchDetail/{id}/{id}/{id} | read | segmentmatchdetail | Explain whether a Contact matches a Segment, using the given externalId. |
| POST | api/3/segmentMatchSome/{id} | write | segmentmatchsome | Create a Match Some Request. |
| GET | api/3/segmentMatchSome/{id}/{id} | read | segmentmatchsome | Return a Match Some result-set. |
| POST | api/3/segmentsV2 | write | segmentsv2 | Create a Segment. |
| GET | api/3/segmentsV2/{id} | read | segmentsv2 | Retrieve a Segment. |
| PUT | api/3/segmentsV2/{id} | write | segmentsv2 | Update a Segment. |
| DELETE | api/3/segmentsV2/{id} | write | segmentsv2 | Delete a Segment by SegmentId including its historic versions. |
| GET | api/3/segmentsV2/{id}/createdDate/{id} | read | segmentsv2 | Retrieve a Segment's Historic Definition. |
| PUT | api/3/segmentsV2/{id}/createdDate/{id} | write | segmentsv2 | Revert a Segment to a Historic Definition. |
| GET | api/3/segmentsV2/{id}/translate | read | segmentsv2 | Translate a segment into human-readable text. |
| GET | api/3/settings/account | read | settings | Retrieve account information. |
| POST | api/3/settings/account | write | settings | Update account settings. |
| GET | api/3/settings/developer | write | settings | Retrieve API credentials. Kept out of read: returns the account API credentials. |
| POST | api/3/settings/developer | write | settings | Reset an API key. |
| GET | api/3/settings/dkim | read | settings | Check the DKIM records of a domain. |
| GET | api/3/siteTracking | read | sitetracking | Retrieve status. |
| PUT | api/3/siteTracking | write | sitetracking | Enable/disable. |
| GET | api/3/siteTracking/code | read | sitetracking | Retrieve site tracking code. |
| GET | api/3/siteTrackingDomains | read | sitetrackingdomains | List all site tracking domains. |
| POST | api/3/siteTrackingDomains | write | sitetrackingdomains | Add a site tracking domain. |
| DELETE | api/3/siteTrackingDomains/{id} | write | sitetrackingdomains | Remove a site tracking domain. |
| GET | api/3/sms | read | sms | List automation SMS blocks. |
| GET | api/3/sms/10dlc/areacode | read | sms | Get the account's saved or suggested 10DLC area code. |
| GET | api/3/sms/10dlc/areacodes | read | sms | List available 10DLC area codes. |
| GET | api/3/sms/10dlc/brand | read | sms | Get a brand form. |
| POST | api/3/sms/10dlc/brand | write | sms | Create a brand form. |
| PUT | api/3/sms/10dlc/brand | write | sms | Update a brand form. |
| GET | api/3/sms/10dlc/campaign | read | sms | List the campaign forms. |
| POST | api/3/sms/10dlc/campaign | write | sms | Create the campaign form. |
| GET | api/3/sms/10dlc/campaign/{id} | read | sms | Get a campaign form. |
| PUT | api/3/sms/10dlc/campaign/{id} | write | sms | Update a campaign form. |
| GET | api/3/sms/broadcasts | read | sms | Get all broadcast messages. |
| POST | api/3/sms/broadcasts | write | sms | Create a new broadcast message. |
| POST | api/3/sms/broadcasts/ai | write | sms | Create AI-generated broadcast. |
| PUT | api/3/sms/broadcasts/ai | write | sms | Update broadcast with AI. |
| GET | api/3/sms/broadcasts/ai/{id} | read | sms | Get AI broadcast request status. |
| POST | api/3/sms/broadcasts/export | write | sms | Export broadcast metrics. |
| GET | api/3/sms/broadcasts/hours | read | sms | List SMS quiet hours. |
| POST | api/3/sms/broadcasts/hours | write | sms | Create an SMS quiet-hours window. |
| PUT | api/3/sms/broadcasts/hours/{id} | write | sms | Update an SMS quiet-hours window. |
| POST | api/3/sms/broadcasts/metrics | read | sms | Get all broadcast metrics. |
| GET | api/3/sms/broadcasts/metrics/snapshot | read | sms | Get broadcast snapshot. |
| POST | api/3/sms/broadcasts/metrics/snapshot | read | sms | Get broadcast snapshot. |
| GET | api/3/sms/broadcasts/metrics/{id}/failures | read | sms | Get broadcast failure details. |
| GET | api/3/sms/broadcasts/{id} | read | sms | Get broadcast message. |
| PUT | api/3/sms/broadcasts/{id} | write | sms | Update broadcast message. |
| DELETE | api/3/sms/broadcasts/{id} | write | sms | Delete broadcast message. |
| GET | api/3/sms/broadcasts/{id}/recipients | read | sms | Get broadcast recipients. |
| POST | api/3/sms/broadcasts/{id}/recipients/export | write | sms | Export broadcast recipients. |
| GET | api/3/sms/credits | read | sms | Get current sms credit use data. |
| GET | api/3/sms/lists | read | sms | Get all broadcast lists. |
| GET | api/3/sms/{id} | read | sms | Retrieve an automation SMS block. |
| GET | api/3/statsActivityItem/get | read | statsactivityitem | List recent activity items. |
| GET | api/3/statsActivityItem/get_series | read | statsactivityitem | List recent automation entries. |
| GET | api/3/tags | read | tags | List all tags. |
| POST | api/3/tags | write | tags | Create a tag. |
| GET | api/3/tags/{id} | read | tags | Retrieve a tag. |
| PUT | api/3/tags/{id} | write | tags | Update a tag. |
| DELETE | api/3/tags/{id} | write | tags | Delete a tag. |
| GET | api/3/taskNotifications | read | tasknotifications | List task reminders. |
| POST | api/3/taskNotifications | write | tasknotifications | Create a task reminder. |
| GET | api/3/taskOutcomes | read | taskoutcomes | List all task outcomes. |
| POST | api/3/taskOutcomes | write | taskoutcomes | Create a task outcome. |
| GET | api/3/taskOutcomes/{id} | read | taskoutcomes | Retrieve a task outcome. |
| PUT | api/3/taskOutcomes/{id} | write | taskoutcomes | Update a task outcome. |
| DELETE | api/3/taskOutcomes/{id} | write | taskoutcomes | Delete a task outcome. |
| GET | api/3/tasktypeOutcomeRels | read | tasktypeoutcomerels | List all task type - outcome relations. |
| GET | api/3/tasktypeOutcomeRels/{id} | read | tasktypeoutcomerels | Retrieve a task type - outcome relation. |
| DELETE | api/3/tasktypeOutcomeRels/{id} | write | tasktypeoutcomerels | Delete a task type - outcome relation. |
| GET | api/2/template/share | write | template | Create Shareable Campaign Template Link. Kept out of read: creates a share link. |
| GET | api/3/templates | read | templates | List all templates. |
| POST | api/3/templates | write | templates | Create a template. |
| GET | api/3/templates/{id} | read | templates | Retrieve a template. |
| PUT | api/3/templates/{id} | write | templates | Update a template. |
| DELETE | api/3/templates/{id} | write | templates | Delete a template. |
| GET | api/3/trackingLogs | read | trackinglogs | List the tracked events that have fired, with their contacts. |
| GET | api/3/trackingLogs/{id} | read | trackinglogs | Retrieve a tracking log entry. |
| GET | api/3/trackingLogs/{id}/contact | read | trackinglogs | Get Contact By Event ID. |
| GET | api/3/users | read | users | List all users. |
| POST | api/3/users | write | users | Create a user. |
| GET | api/3/users/email/{id} | read | users | Retrieve a user by email. |
| GET | api/3/users/me | read | users | Retrieve logged-in user. |
| GET | api/3/users/username/{id} | read | users | Retrieve a user by username. |
| GET | api/3/users/{id} | read | users | Retrieve a user. |
| PUT | api/3/users/{id} | write | users | Update a user. |
| DELETE | api/3/users/{id} | write | users | Delete a user. |
| POST | api/3/users/{id}/singleSignOn | write | users | Create a single sign-on token for a user. |
| GET | api/3/webhook/events | read | webhook | List all webhook events. |
| GET | api/3/webhooks | read | webhooks | List all webhooks. |
| POST | api/3/webhooks | write | webhooks | Create a webhook. |
| GET | api/3/webhooks/{id} | read | webhooks | Retrieve a webhook. |
| PUT | api/3/webhooks/{id} | write | webhooks | Update a webhook. |
| DELETE | api/3/webhooks/{id} | write | webhooks | Delete a webhook. |
