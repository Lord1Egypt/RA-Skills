# Calendly access policy

An access policy limits which endpoints Calendly connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/calendly#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Calendly: its 49 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create calendly --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "activity_log_entries"},
    {"method": "GET", "path": "event_type_availability_schedules"},
    {"method": "GET", "path": "user_availability_schedules"},
    {"method": "GET", "path": "user_availability_schedules/{id}"},
    {"method": "GET", "path": "user_busy_times"},
    {"method": "GET", "path": "user_meeting_limits"},
    {"method": "GET", "path": "contact_lists"},
    {"method": "GET", "path": "contact_lists/{id}"},
    {"method": "GET", "path": "contacts"},
    {"method": "GET", "path": "contacts/custom_field_definitions"},
    {"method": "GET", "path": "contacts/custom_field_definitions/{id}"},
    {"method": "GET", "path": "contacts/{id}"},
    {"method": "GET", "path": "notes"},
    {"method": "GET", "path": "notes/{id}"},
    {"method": "GET", "path": "event_type_available_times"},
    {"method": "GET", "path": "event_type_memberships"},
    {"method": "GET", "path": "event_types"},
    {"method": "GET", "path": "event_types/{id}"},
    {"method": "GET", "path": "group_relationships"},
    {"method": "GET", "path": "group_relationships/{id}"},
    {"method": "GET", "path": "groups"},
    {"method": "GET", "path": "groups/{id}"},
    {"method": "GET", "path": "locations"},
    {"method": "GET", "path": "meeting_recaps"},
    {"method": "GET", "path": "meeting_recaps/{id}"},
    {"method": "GET", "path": "meeting_recaps/{id}/transcript"},
    {"method": "GET", "path": "organization_memberships"},
    {"method": "GET", "path": "organization_memberships/{id}"},
    {"method": "GET", "path": "organizations/{id}"},
    {"method": "GET", "path": "organizations/{id}/invitations"},
    {"method": "GET", "path": "organizations/{id}/invitations/{id}"},
    {"method": "GET", "path": "teams"},
    {"method": "GET", "path": "teams/{id}"},
    {"method": "GET", "path": "outgoing_communications"},
    {"method": "GET", "path": "routing_form_submissions"},
    {"method": "GET", "path": "routing_form_submissions/{id}"},
    {"method": "GET", "path": "routing_forms"},
    {"method": "GET", "path": "routing_forms/{id}"},
    {"method": "GET", "path": "invitee_no_shows/{id}"},
    {"method": "GET", "path": "scheduled_events"},
    {"method": "GET", "path": "scheduled_events/{id}"},
    {"method": "GET", "path": "scheduled_events/{id}/invitees"},
    {"method": "GET", "path": "scheduled_events/{id}/invitees/{id}"},
    {"method": "GET", "path": "shares"},
    {"method": "GET", "path": "users/me"},
    {"method": "GET", "path": "users/{id}"},
    {"method": "GET", "path": "sample_webhook_data"},
    {"method": "GET", "path": "webhook_subscriptions"},
    {"method": "GET", "path": "webhook_subscriptions/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Calendly endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | activity_log_entries | read | activity log | List activity log entries. |
| GET | event_type_availability_schedules | read | availability | Return the availability for an event type. |
| PATCH | event_type_availability_schedules | write | availability | Update an event type availability schedule. |
| GET | user_availability_schedules | read | availability | Returns the availability schedules of the given user. |
| POST | user_availability_schedules | write | availability | Creates a new availability schedule for the authenticated user. |
| GET | user_availability_schedules/{id} | read | availability | This will return the availability schedule of the given UUID. |
| PATCH | user_availability_schedules/{id} | write | availability | Renames a schedule, changes its timezone or rules, or makes it the default. |
| GET | user_busy_times | read | availability | Returns an ascending list of user internal and external scheduled events within a specified date range. |
| GET | user_meeting_limits | read | availability | Returns a user's host-level meeting limits (daily, weekly, and monthly caps across all Event Types). |
| PATCH | user_meeting_limits | write | availability | Sets or removes the authenticated user's host-level meeting limits (daily, weekly, and monthly caps across all Event Types). |
| GET | contact_lists | read | contacts | Returns the user's saved contact groupings: Lists (static_list) and Views (dynamic_view). |
| POST | contact_lists | write | contacts | Creates a List (static_list) and, optionally, adds contacts to it. |
| GET | contact_lists/{id} | read | contacts | Returns one List or View. |
| PATCH | contact_lists/{id} | write | contacts | Renames a List or View. |
| POST | contact_lists/{id}/memberships | write | contacts | Adds contacts to a List. |
| POST | contact_lists/{id}/memberships/removal | write | contacts | Removes contacts from a List. |
| GET | contacts | read | contacts | List contacts. |
| POST | contacts | write | contacts | Create a contact. |
| GET | contacts/custom_field_definitions | read | contacts | Returns all custom field definitions available to the authenticated user or organization. |
| POST | contacts/custom_field_definitions | write | contacts | Creates a contact custom field definition. |
| GET | contacts/custom_field_definitions/{id} | read | contacts | Returns a single custom field definition by uuid. |
| GET | contacts/{id} | read | contacts | Returns the details of a specified Contact. |
| PATCH | contacts/{id} | write | contacts | Update an existing Contact. |
| DELETE | contacts/{id} | write | contacts | Delete an existing Contact. |
| GET | notes | read | contacts | Returns a list of notes. |
| POST | notes | write | contacts | Creates a note about one contact. |
| GET | notes/{id} | read | contacts | Returns one note that the authenticated user owns. |
| POST | data_compliance/deletion/events | write | data compliance | Delete scheduled event data for an organization. |
| POST | data_compliance/deletion/invitees | write | data compliance | Submit a request to remove invitee data from previously booked events. |
| GET | event_type_available_times | read | event types | Returns a list of available times for an event type within a specified date range. |
| GET | event_type_memberships | read | event types | Fetch list of event type hosts. |
| GET | event_types | read | event types | Returns all Event Types associated with a specified User. |
| POST | event_types | write | event types | Create a new Event Type. |
| GET | event_types/{id} | read | event types | Returns information about a specified Event Type. |
| PATCH | event_types/{id} | write | event types | Update an existing Event Type. |
| POST | one_off_event_types | write | event types | Creates One-Off Event Type. |
| GET | group_relationships | read | groups | List group relationships (a group owner has one membership record, but can have multiple admin records). |
| GET | group_relationships/{id} | read | groups | Returns a group relationship by uuid. |
| GET | groups | read | groups | Returns a list of groups. |
| GET | groups/{id} | read | groups | Returns information about a specified Group. |
| GET | locations | read | locations | Returns configured location information for a given user. |
| GET | meeting_recaps | read | meeting recaps | Returns a paginated list of meeting recaps accessible to the authenticated user. |
| GET | meeting_recaps/{id} | read | meeting recaps | Returns the recap associated with a meeting if it is available. |
| PATCH | meeting_recaps/{id} | write | meeting recaps | Update an existing Recap. |
| DELETE | meeting_recaps/{id} | write | meeting recaps | Delete an existing Recap. |
| GET | meeting_recaps/{id}/transcript | read | meeting recaps | Returns the transcript associated with a meeting recap if it is available. |
| GET | organization_memberships | read | organizations | List organization memberships, filtered by user or organization. |
| GET | organization_memberships/{id} | read | organizations | Returns information about a user's Organization Membership. |
| DELETE | organization_memberships/{id} | write | organizations | Removes a user from an organization. |
| GET | organizations/{id} | read | organizations | Returns the details of a specified Organization. |
| GET | organizations/{id}/invitations | read | organizations | Returns a list of Organization Invitations that were sent to the organization's members. |
| POST | organizations/{id}/invitations | write | organizations | Invites a user to an organization. |
| GET | organizations/{id}/invitations/{id} | read | organizations | Returns an Organization Invitation that was sent to the organization's members. |
| DELETE | organizations/{id}/invitations/{id} | write | organizations | Use this to revoke an Organization Invitation to an organization. |
| GET | teams | read | organizations | Returns a paginated list of Teams matching the requested user. |
| GET | teams/{id} | read | organizations | Returns a single Team. |
| GET | outgoing_communications | read | outgoing communications | List outgoing communications. |
| GET | routing_form_submissions | read | routing forms | Get a list of Routing Form Submissions for a specified Routing Form. |
| GET | routing_form_submissions/{id} | read | routing forms | Get a specified Routing Form Submission. |
| GET | routing_forms | read | routing forms | Get a list of Routing Forms for a specified Organization. |
| GET | routing_forms/{id} | read | routing forms | Get a specified Routing Form. |
| POST | invitee_no_shows | write | scheduled events | Marks an Invitee as a No Show. |
| GET | invitee_no_shows/{id} | read | scheduled events | Returns information about a specified Invitee No Show. |
| DELETE | invitee_no_shows/{id} | write | scheduled events | Undoes marking an Invitee as a No Show. |
| POST | invitees | write | scheduled events | Creates a new booking for an event invitee. |
| GET | scheduled_events | read | scheduled events | List scheduled events. |
| GET | scheduled_events/{id} | read | scheduled events | Returns information about a specified Event. |
| POST | scheduled_events/{id}/cancellation | write | scheduled events | Cancels specified event. |
| GET | scheduled_events/{id}/invitees | read | scheduled events | Returns a list of Invitees for an event. |
| GET | scheduled_events/{id}/invitees/{id} | read | scheduled events | Returns information about a specified Invitee (person invited to an event). |
| POST | scheduling_links | write | scheduling links | Creates a single-use scheduling link. |
| GET | shares | read | shares | Returns the user's Shares, newest first. |
| POST | shares | write | shares | Create a customized one-time share of an event type. |
| PATCH | shares/{id} | write | shares | Update a specified Share. |
| DELETE | shares/{id} | write | shares | Deletes a single-use scheduling link (share). |
| GET | users/me | read | users | Returns basic information about your user account. |
| GET | users/{id} | read | users | Returns information about a specified User. |
| GET | sample_webhook_data | read | webhooks | Return sample webhook payload data for testing a webhook subscription. |
| GET | webhook_subscriptions | read | webhooks | Get a list of Webhook Subscriptions for a specified Organization, User, or Group. |
| POST | webhook_subscriptions | write | webhooks | Create a Webhook Subscription for an Organization, User, or Group. |
| GET | webhook_subscriptions/{id} | read | webhooks | Get a specified Webhook Subscription. |
| DELETE | webhook_subscriptions/{id} | write | webhooks | Delete a Webhook Subscription. |
