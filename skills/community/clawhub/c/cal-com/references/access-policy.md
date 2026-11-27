# Cal.com access policy

An access policy limits which endpoints Cal.com connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/calcom#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Cal.com: its 167 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create cal-com --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v2/allowlists"},
    {"method": "GET", "path": "v2/allowlists/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/assignments/{id}/history"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/options/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/slugs/{id}/options/assigned"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/sync-history"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/sync-history/user/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/{id}/options"},
    {"method": "GET", "path": "v2/organizations/{id}/attributes/{id}/options/assigned"},
    {"method": "GET", "path": "v2/teams/{id}/booking-limit-pools"},
    {"method": "GET", "path": "v2/teams/{id}/booking-limit-pools/{id}/hosts"},
    {"method": "GET", "path": "v2/bookings"},
    {"method": "GET", "path": "v2/bookings/by-seat/{id}"},
    {"method": "GET", "path": "v2/bookings/verification/email/check"},
    {"method": "GET", "path": "v2/bookings/{id}"},
    {"method": "GET", "path": "v2/bookings/{id}/attendees"},
    {"method": "GET", "path": "v2/bookings/{id}/attendees/{id}"},
    {"method": "GET", "path": "v2/bookings/{id}/calendar-links"},
    {"method": "GET", "path": "v2/bookings/{id}/conferencing-sessions"},
    {"method": "GET", "path": "v2/bookings/{id}/references"},
    {"method": "GET", "path": "v2/bookings/{id}/routing-trace"},
    {"method": "GET", "path": "v2/bookings/{id}/transcripts"},
    {"method": "GET", "path": "v2/organizations/{id}/bookings"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/bookings"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/bookings/{id}/references"},
    {"method": "GET", "path": "v2/organizations/{id}/users/{id}/bookings"},
    {"method": "GET", "path": "v2/teams/{id}/bookings"},
    {"method": "GET", "path": "v2/organizations/{id}/calendar-invites"},
    {"method": "GET", "path": "v2/calendars"},
    {"method": "GET", "path": "v2/calendars/busy-times"},
    {"method": "GET", "path": "v2/calendars/ics-feed/check"},
    {"method": "GET", "path": "v2/calendars/{id}/check"},
    {"method": "GET", "path": "v2/calendars/{id}/event/{id}"},
    {"method": "GET", "path": "v2/conferencing"},
    {"method": "GET", "path": "v2/conferencing/default"},
    {"method": "GET", "path": "v2/organizations/{id}/conferencing"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/conferencing"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/conferencing/default"},
    {"method": "GET", "path": "v2/organizations/{id}/users/{id}/conferencing"},
    {"method": "GET", "path": "v2/contacts"},
    {"method": "GET", "path": "v2/contacts/suggestions"},
    {"method": "GET", "path": "v2/contacts/tags"},
    {"method": "GET", "path": "v2/contacts/{id}/history"},
    {"method": "GET", "path": "v2/contacts/{id}/note"},
    {"method": "GET", "path": "v2/credits/available"},
    {"method": "GET", "path": "v2/discover/favorites"},
    {"method": "GET", "path": "v2/discover/listings"},
    {"method": "GET", "path": "v2/discover/listings/search"},
    {"method": "GET", "path": "v2/event-type-sequences/{id}"},
    {"method": "GET", "path": "v2/event-type-sequences/{id}/slots"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-type-sequences"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-type-sequences/{id}"},
    {"method": "GET", "path": "v2/event-types"},
    {"method": "GET", "path": "v2/event-types/{id}"},
    {"method": "GET", "path": "v2/event-types/{id}/booking-fields"},
    {"method": "GET", "path": "v2/event-types/{id}/calendar-invites"},
    {"method": "GET", "path": "v2/event-types/{id}/crm-sync-errors"},
    {"method": "GET", "path": "v2/event-types/{id}/history"},
    {"method": "GET", "path": "v2/event-types/{id}/private-links"},
    {"method": "GET", "path": "v2/event-types/{id}/scheduling-config"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/event-types"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-types"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-types/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-types/{id}/booking-fields"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-types/{id}/calendar-invites"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/event-types/{id}/private-links"},
    {"method": "GET", "path": "v2/teams/{id}/event-types"},
    {"method": "GET", "path": "v2/teams/{id}/event-types/{id}"},
    {"method": "GET", "path": "v2/teams/{id}/event-types/{id}/booking-fields"},
    {"method": "GET", "path": "v2/teams/{id}/event-types/{id}/calendar-invites"},
    {"method": "GET", "path": "v2/events"},
    {"method": "GET", "path": "v2/events/{id}"},
    {"method": "GET", "path": "v2/events/{id}/bookings"},
    {"method": "GET", "path": "v2/events/{id}/co-hosts"},
    {"method": "GET", "path": "v2/events/{id}/coordinates"},
    {"method": "GET", "path": "v2/events/{id}/host-candidates"},
    {"method": "GET", "path": "v2/events/{id}/locations"},
    {"method": "GET", "path": "v2/events/{id}/messages"},
    {"method": "GET", "path": "v2/events/{id}/registrations/counts"},
    {"method": "GET", "path": "v2/teams/{id}/events"},
    {"method": "POST", "path": "v2/insights/booking-limits/usage"},
    {"method": "POST", "path": "v2/insights/bookings/average-duration"},
    {"method": "POST", "path": "v2/insights/bookings/event-trends"},
    {"method": "POST", "path": "v2/insights/bookings/kpi-stats"},
    {"method": "POST", "path": "v2/insights/bookings/members"},
    {"method": "POST", "path": "v2/insights/routings/failed-bookings-by-field"},
    {"method": "POST", "path": "v2/insights/routings/form-field-options"},
    {"method": "POST", "path": "v2/insights/routings/form-response-headers"},
    {"method": "POST", "path": "v2/insights/routings/form-responses"},
    {"method": "POST", "path": "v2/insights/routings/forms-by-status"},
    {"method": "POST", "path": "v2/insights/routings/routed-to-per-period"},
    {"method": "GET", "path": "v2/links/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/memberships"},
    {"method": "GET", "path": "v2/organizations/{id}/memberships/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/memberships"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/memberships/{id}"},
    {"method": "GET", "path": "v2/teams/{id}/memberships"},
    {"method": "GET", "path": "v2/teams/{id}/memberships/{id}"},
    {"method": "GET", "path": "v2/notifications/agent-channels"},
    {"method": "GET", "path": "v2/oauth-clients/{id}/users"},
    {"method": "GET", "path": "v2/oauth-clients/{id}/users/{id}"},
    {"method": "GET", "path": "v2/auth/oauth2/clients/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/ooo"},
    {"method": "GET", "path": "v2/organizations/{id}/users/{id}/ooo"},
    {"method": "GET", "path": "v2/teams/{id}/users/{id}/ooo"},
    {"method": "GET", "path": "v2/organizations/{id}/organizations"},
    {"method": "GET", "path": "v2/organizations/{id}/organizations/{id}"},
    {"method": "GET", "path": "v2/me"},
    {"method": "GET", "path": "v2/me/booking-limits"},
    {"method": "GET", "path": "v2/me/ooo"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/me"},
    {"method": "GET", "path": "v2/organizations/{id}/roles"},
    {"method": "GET", "path": "v2/organizations/{id}/roles/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/roles/{id}/permissions"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/roles"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/roles/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/roles/{id}/permissions"},
    {"method": "GET", "path": "v2/organizations/{id}/routing-forms"},
    {"method": "GET", "path": "v2/organizations/{id}/routing-forms/{id}/responses"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/routing-forms"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/routing-forms/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/routing-forms/{id}/history"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/routing-forms/{id}/responses"},
    {"method": "POST", "path": "v2/routing-forms/{id}/calculate-slots"},
    {"method": "GET", "path": "v2/organizations/{id}/schedules"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/schedules"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/users/{id}/schedules"},
    {"method": "GET", "path": "v2/organizations/{id}/users/{id}/schedules"},
    {"method": "GET", "path": "v2/organizations/{id}/users/{id}/schedules/{id}"},
    {"method": "GET", "path": "v2/schedules"},
    {"method": "GET", "path": "v2/schedules/default"},
    {"method": "GET", "path": "v2/schedules/{id}"},
    {"method": "GET", "path": "v2/teams/{id}/schedules"},
    {"method": "GET", "path": "v2/organizations/{id}/secondary-domains"},
    {"method": "GET", "path": "v2/organizations/{id}/secondary-domains/{id}"},
    {"method": "GET", "path": "v2/slots"},
    {"method": "GET", "path": "v2/slots/reservations/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/stripe/check"},
    {"method": "GET", "path": "v2/stripe/check"},
    {"method": "GET", "path": "v2/organizations/{id}/teams"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}"},
    {"method": "GET", "path": "v2/teams"},
    {"method": "GET", "path": "v2/teams/{id}"},
    {"method": "GET", "path": "v2/timezones"},
    {"method": "GET", "path": "v2/organizations/{id}/users"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/verified-resources/emails"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/verified-resources/emails/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/verified-resources/phones"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/verified-resources/phones/{id}"},
    {"method": "GET", "path": "v2/teams/{id}/verified-resources/emails"},
    {"method": "GET", "path": "v2/teams/{id}/verified-resources/emails/{id}"},
    {"method": "GET", "path": "v2/teams/{id}/verified-resources/phones"},
    {"method": "GET", "path": "v2/teams/{id}/verified-resources/phones/{id}"},
    {"method": "GET", "path": "v2/verified-resources/emails"},
    {"method": "GET", "path": "v2/verified-resources/emails/{id}"},
    {"method": "GET", "path": "v2/verified-resources/phones"},
    {"method": "GET", "path": "v2/verified-resources/phones/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/workflows"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/workflows/routing-form"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/workflows/{id}"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/workflows/{id}/condition-fields"},
    {"method": "GET", "path": "v2/organizations/{id}/teams/{id}/workflows/{id}/routing-form"},
    {"method": "GET", "path": "v2/workflows"},
    {"method": "GET", "path": "v2/workflows/{id}"},
    {"method": "GET", "path": "v2/workflows/{id}/condition-fields"}
  ],
  "deny": []
}
```

## Endpoints

The Cal.com endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v2/allowlists | read | allowlists | Get the Cal.com IP allowlists. |
| GET | v2/allowlists/{id} | read | allowlists | Get the Cal.com IP allowlist of one service. |
| POST | v2/api-keys/refresh | write | api keys | Refresh API Key. |
| GET | v2/organizations/{id}/attributes | read | attributes | Get all attributes. |
| POST | v2/organizations/{id}/attributes | write | attributes | Create an attribute. |
| GET | v2/organizations/{id}/attributes/assignments/{id}/history | read | attributes | Get attribute assignment history for a user. |
| GET | v2/organizations/{id}/attributes/options/{id} | read | attributes | Get all attribute options for a user. |
| POST | v2/organizations/{id}/attributes/options/{id} | write | attributes | Assign an attribute to a user. |
| PATCH | v2/organizations/{id}/attributes/options/{id}/{id} | write | attributes | Update an attribute assignment for a user. |
| DELETE | v2/organizations/{id}/attributes/options/{id}/{id} | write | attributes | Unassign an attribute from a user. |
| GET | v2/organizations/{id}/attributes/slugs/{id}/options/assigned | read | attributes | Get all assigned attribute options by attribute slug. |
| GET | v2/organizations/{id}/attributes/sync-history | read | attributes | Get attribute sync history. |
| GET | v2/organizations/{id}/attributes/sync-history/user/{id} | read | attributes | Get sync history for a specific user. |
| GET | v2/organizations/{id}/attributes/{id} | read | attributes | Get an attribute. |
| PATCH | v2/organizations/{id}/attributes/{id} | write | attributes | Update an attribute. |
| DELETE | v2/organizations/{id}/attributes/{id} | write | attributes | Delete an attribute. |
| GET | v2/organizations/{id}/attributes/{id}/options | read | attributes | Get all attribute options. |
| POST | v2/organizations/{id}/attributes/{id}/options | write | attributes | Create an attribute option. |
| GET | v2/organizations/{id}/attributes/{id}/options/assigned | read | attributes | Get all assigned attribute options by attribute ID. |
| PATCH | v2/organizations/{id}/attributes/{id}/options/{id} | write | attributes | Update an attribute option. |
| DELETE | v2/organizations/{id}/attributes/{id}/options/{id} | write | attributes | Delete an attribute option. |
| GET | v2/teams/{id}/booking-limit-pools | read | booking limit pools | List booking limit pools. |
| POST | v2/teams/{id}/booking-limit-pools | write | booking limit pools | Create a booking limit pool. |
| PATCH | v2/teams/{id}/booking-limit-pools/{id} | write | booking limit pools | Update a booking limit pool. |
| DELETE | v2/teams/{id}/booking-limit-pools/{id} | write | booking limit pools | Delete a booking limit pool. |
| GET | v2/teams/{id}/booking-limit-pools/{id}/hosts | read | booking limit pools | List a pool's hosts and their limits. |
| PUT | v2/teams/{id}/booking-limit-pools/{id}/hosts/{id} | write | booking limit pools | Replace a host's limit for a pool. |
| PATCH | v2/teams/{id}/booking-limit-pools/{id}/hosts/{id} | write | booking limit pools | Set a host's limit for a pool. |
| DELETE | v2/teams/{id}/booking-limit-pools/{id}/hosts/{id} | write | booking limit pools | Clear a host's limit for a pool. |
| GET | v2/bookings | read | bookings | Get all bookings. |
| POST | v2/bookings | write | bookings | Create a booking. |
| GET | v2/bookings/by-seat/{id} | read | bookings | Get a booking by seat UID. |
| GET | v2/bookings/verification/email/check | read | bookings | Check if email verification is required. |
| POST | v2/bookings/verification/email/send-code | write | bookings | Send email verification code. |
| POST | v2/bookings/verification/email/verify-code | write | bookings | Verify email with code. |
| GET | v2/bookings/{id} | read | bookings | Get a booking. |
| GET | v2/bookings/{id}/attendees | read | bookings | Get all attendees for a booking. |
| POST | v2/bookings/{id}/attendees | write | bookings | Add an attendee to a booking. |
| GET | v2/bookings/{id}/attendees/{id} | read | bookings | Get a specific attendee for a booking. |
| GET | v2/bookings/{id}/calendar-links | read | bookings | Get 'Add to Calendar' links for a booking. |
| POST | v2/bookings/{id}/cancel | write | bookings | Cancel a booking. |
| GET | v2/bookings/{id}/conferencing-sessions | read | bookings | Get Video Meeting Sessions. Only supported for Cal Video. |
| POST | v2/bookings/{id}/confirm | write | bookings | Confirm a booking. |
| POST | v2/bookings/{id}/decline | write | bookings | Decline a booking. |
| POST | v2/bookings/{id}/guests | write | bookings | Add guests to an existing booking. |
| PATCH | v2/bookings/{id}/location | write | bookings | Update booking location for an existing booking. |
| POST | v2/bookings/{id}/mark-absent | write | bookings | Mark a booking absence. |
| POST | v2/bookings/{id}/reassign | write | bookings | Reassign a booking. |
| POST | v2/bookings/{id}/reassign/{id} | write | bookings | Reassign a booking to a specific host. |
| GET | v2/bookings/{id}/recordings | write | bookings | Get all the recordings for the booking. Kept out of read: response includes recording share tokens. |
| GET | v2/bookings/{id}/references | read | bookings | Get booking references. |
| POST | v2/bookings/{id}/request-reschedule | write | bookings | Request to reschedule a booking. |
| POST | v2/bookings/{id}/reschedule | write | bookings | Reschedule a booking. |
| GET | v2/bookings/{id}/routing-trace | read | bookings | Get the routing trace for a booking. |
| POST | v2/bookings/{id}/seats/confirm | write | bookings | Confirm booking seats. |
| POST | v2/bookings/{id}/seats/decline | write | bookings | Decline booking seats. |
| GET | v2/bookings/{id}/transcripts | read | bookings | Get Cal Video real time transcript download links for the booking. |
| GET | v2/organizations/{id}/bookings | read | bookings | Get organization bookings (cursor pagination). |
| POST | v2/organizations/{id}/bookings/block | write | bookings | Block an organization booking attendee. |
| POST | v2/organizations/{id}/bookings/report | write | bookings | Report an organization booking. |
| GET | v2/organizations/{id}/teams/{id}/bookings | read | bookings | Get organization team bookings. |
| GET | v2/organizations/{id}/teams/{id}/bookings/{id}/references | read | bookings | Get booking references. |
| GET | v2/organizations/{id}/users/{id}/bookings | read | bookings | Get all bookings for an organization user. |
| GET | v2/teams/{id}/bookings | read | bookings | Get team bookings. |
| GET | v2/organizations/{id}/calendar-invites | read | calendar invites | Get organization calendar-invite defaults. |
| PATCH | v2/organizations/{id}/calendar-invites | write | calendar invites | Update organization calendar-invite defaults. |
| GET | v2/calendars | read | calendars | Get all calendars. |
| GET | v2/calendars/busy-times | read | calendars | Get busy times. |
| GET | v2/calendars/ics-feed/check | read | calendars | Check an ICS feed. |
| POST | v2/calendars/ics-feed/save | write | calendars | Save an ICS feed. |
| GET | v2/calendars/{id}/check | read | calendars | Check a calendar connection. |
| GET | v2/calendars/{id}/connect | write | calendars | Get OAuth connect URL. Kept out of read: starts a provider connect flow. |
| POST | v2/calendars/{id}/credentials | write | calendars | Save Apple calendar credentials. |
| POST | v2/calendars/{id}/disconnect | write | calendars | Disconnect a calendar. |
| GET | v2/calendars/{id}/event/{id} | read | calendars | Get meeting details from calendar. |
| PATCH | v2/calendars/{id}/events/{id} | write | calendars | Update meeting details in calendar. |
| GET | v2/calendars/{id}/save | write | calendars | Save Google or Outlook calendar credentials. Kept out of read: saves provider credentials. |
| GET | v2/conferencing | read | conferencing | List your conferencing applications. |
| GET | v2/conferencing/default | read | conferencing | Get your default conferencing application. |
| POST | v2/conferencing/{id}/connect | write | conferencing | Connect your conferencing application. |
| POST | v2/conferencing/{id}/default | write | conferencing | Set your default conferencing application. |
| DELETE | v2/conferencing/{id}/disconnect | write | conferencing | Disconnect your conferencing application. |
| GET | v2/conferencing/{id}/oauth/auth-url | write | conferencing | Get OAuth conferencing app auth URL. Kept out of read: starts an OAuth connect flow for the app. |
| GET | v2/conferencing/{id}/oauth/callback | write | conferencing | Conferencing app OAuth callback. Kept out of read: saves OAuth credentials for the app. |
| GET | v2/organizations/{id}/conferencing | read | conferencing | List organization conferencing applications. |
| DELETE | v2/organizations/{id}/conferencing/{id}/disconnect | write | conferencing | Disconnect organization conferencing application. |
| GET | v2/organizations/{id}/conferencing/{id}/oauth/auth-url | write | conferencing | Get OAuth conferencing app's auth URL for an organization. Kept out of read: starts an OAuth connect flow for the app. |
| GET | v2/organizations/{id}/conferencing/{id}/oauth/callback | write | conferencing | Save organization conferencing app OAuth credentials. Kept out of read: saves OAuth credentials for the app. |
| GET | v2/organizations/{id}/teams/{id}/conferencing | read | conferencing | List team conferencing applications. |
| GET | v2/organizations/{id}/teams/{id}/conferencing/default | read | conferencing | Get team default conferencing application. |
| POST | v2/organizations/{id}/teams/{id}/conferencing/{id}/connect | write | conferencing | Connect your conferencing application to a team. |
| POST | v2/organizations/{id}/teams/{id}/conferencing/{id}/default | write | conferencing | Set team default conferencing application. |
| DELETE | v2/organizations/{id}/teams/{id}/conferencing/{id}/disconnect | write | conferencing | Disconnect team conferencing application. |
| GET | v2/organizations/{id}/teams/{id}/conferencing/{id}/oauth/auth-url | write | conferencing | Get OAuth conferencing app's auth URL for a team. Kept out of read: starts an OAuth connect flow for the app. |
| GET | v2/organizations/{id}/teams/{id}/conferencing/{id}/oauth/callback | write | conferencing | Save conferencing app OAuth credentials. Kept out of read: saves OAuth credentials for the app. |
| GET | v2/organizations/{id}/users/{id}/conferencing | read | conferencing | List conferencing apps of an organization user. |
| POST | v2/organizations/{id}/users/{id}/conferencing/default | write | conferencing | Set the default conferencing app for an organization user. |
| GET | v2/contacts | read | contacts | List personal contacts. |
| POST | v2/contacts | write | contacts | Add a personal contact. |
| GET | v2/contacts/suggestions | read | contacts | List suggested contacts. |
| POST | v2/contacts/suggestions/dismissals | write | contacts | Dismiss a suggested contact. |
| GET | v2/contacts/tags | read | contacts | List contact tags. |
| POST | v2/contacts/tags | write | contacts | Create a contact tag. |
| PATCH | v2/contacts/{id} | write | contacts | Update a personal contact. |
| DELETE | v2/contacts/{id} | write | contacts | Remove a personal contact. |
| GET | v2/contacts/{id}/history | read | contacts | Get a personal contact's meeting history. |
| GET | v2/contacts/{id}/note | read | contacts | Get a personal contact's note. |
| POST | v2/contacts/{id}/tags | write | contacts | Add a tag to a contact. |
| DELETE | v2/contacts/{id}/tags/{id} | write | contacts | Remove a tag from a contact. |
| GET | v2/credits/available | read | credits | Check available credits. |
| POST | v2/credits/charge | write | credits | Charge credits. |
| GET | v2/organizations/{id}/delegation-credentials | write | delegation credentials | Get all delegation credentials of your organization. Kept out of read: response includes the delegation credential secret. |
| POST | v2/organizations/{id}/delegation-credentials | write | delegation credentials | Save delegation credentials for your organization. |
| GET | v2/organizations/{id}/delegation-credentials/{id} | write | delegation credentials | Get a delegation credential of your organization. Kept out of read: response includes the delegation credential secret. |
| PATCH | v2/organizations/{id}/delegation-credentials/{id} | write | delegation credentials | Update delegation credentials of your organization. |
| DELETE | v2/organizations/{id}/delegation-credentials/{id} | write | delegation credentials | Delete delegation credentials of your organization. |
| POST | v2/organizations/{id}/delegation-credentials/{id}/reset-rotation | write | delegation credentials | Reset a blocked delegation credential's secret rotation state. |
| POST | v2/organizations/{id}/delegation-credentials/{id}/verify | write | delegation credentials | Verify a delegation credential's workspace setup. |
| PUT | v2/destination-calendars | write | destination calendars | Update destination calendars. |
| POST | v2/discover/booking-jobs | write | discover | Book a web-found business online. |
| POST | v2/discover/business-calls | write | discover | Call a web-found business to book. |
| GET | v2/discover/favorites | read | discover | List your Discover favorites. |
| GET | v2/discover/listings | read | discover | Get Discover listings by id. |
| GET | v2/discover/listings/search | read | discover | Search Discover listings. |
| POST | v2/discover/service-requests | write | discover | Ask to be told when a Discover provider joins. |
| GET | v2/event-type-sequences/{id} | read | event type sequences | Get a sequence's booking page. |
| GET | v2/event-type-sequences/{id}/slots | read | event type sequences | Get a sequence's available start times. |
| GET | v2/organizations/{id}/teams/{id}/event-type-sequences | read | event type sequences | List event type sequences. |
| POST | v2/organizations/{id}/teams/{id}/event-type-sequences | write | event type sequences | Create an event type sequence. |
| GET | v2/organizations/{id}/teams/{id}/event-type-sequences/{id} | read | event type sequences | Get an event type sequence. |
| PATCH | v2/organizations/{id}/teams/{id}/event-type-sequences/{id} | write | event type sequences | Update an event type sequence. |
| DELETE | v2/organizations/{id}/teams/{id}/event-type-sequences/{id} | write | event type sequences | Delete an event type sequence. |
| GET | v2/event-types | read | event types | List event types. |
| POST | v2/event-types | write | event types | Create an event type. |
| GET | v2/event-types/{id} | read | event types | Get an event type. |
| PATCH | v2/event-types/{id} | write | event types | Update an event type. |
| DELETE | v2/event-types/{id} | write | event types | Delete an event type. |
| GET | v2/event-types/{id}/booking-fields | read | event types | Get booking fields. |
| POST | v2/event-types/{id}/booking-fields | write | event types | Add custom booking fields. |
| PUT | v2/event-types/{id}/booking-fields | write | event types | Replace booking fields. |
| PATCH | v2/event-types/{id}/booking-fields | write | event types | Update booking fields. |
| DELETE | v2/event-types/{id}/booking-fields/{id} | write | event types | Delete a custom booking field. |
| GET | v2/event-types/{id}/calendar-invites | read | event types | Get event-type calendar-invite templates. |
| PATCH | v2/event-types/{id}/calendar-invites | write | event types | Update event-type calendar-invite templates. |
| GET | v2/event-types/{id}/crm-sync-errors | read | event types | List CRM sync errors for an event type. |
| GET | v2/event-types/{id}/history | read | event types | Get event type history. |
| GET | v2/event-types/{id}/private-links | read | event types | Get all private links for an event type. |
| POST | v2/event-types/{id}/private-links | write | event types | Create a private link for an event type. |
| PATCH | v2/event-types/{id}/private-links/{id} | write | event types | Update a private link for an event type. |
| DELETE | v2/event-types/{id}/private-links/{id} | write | event types | Delete a private link for an event type. |
| GET | v2/event-types/{id}/scheduling-config | read | event types | Get scheduling configuration. |
| GET | v2/event-types/{id}/webhooks | write | event types | Get all webhooks. Kept out of read: response includes the webhook signing secret. |
| POST | v2/event-types/{id}/webhooks | write | event types | Create a webhook. |
| DELETE | v2/event-types/{id}/webhooks | write | event types | Delete all webhooks. |
| GET | v2/event-types/{id}/webhooks/{id} | write | event types | Get a webhook. Kept out of read: response includes the webhook signing secret. |
| PATCH | v2/event-types/{id}/webhooks/{id} | write | event types | Update a webhook. |
| DELETE | v2/event-types/{id}/webhooks/{id} | write | event types | Delete a webhook. |
| GET | v2/organizations/{id}/teams/event-types | read | event types | Get all team event types. |
| GET | v2/organizations/{id}/teams/{id}/event-types | read | event types | List organization team event types. |
| POST | v2/organizations/{id}/teams/{id}/event-types | write | event types | Create an organization team event type. |
| GET | v2/organizations/{id}/teams/{id}/event-types/{id} | read | event types | Get an event type. |
| PATCH | v2/organizations/{id}/teams/{id}/event-types/{id} | write | event types | Update an organization team event type. |
| DELETE | v2/organizations/{id}/teams/{id}/event-types/{id} | write | event types | Delete an organization team event type. |
| GET | v2/organizations/{id}/teams/{id}/event-types/{id}/booking-fields | read | event types | Get organization team booking fields. |
| POST | v2/organizations/{id}/teams/{id}/event-types/{id}/booking-fields | write | event types | Add custom organization team booking fields. |
| PUT | v2/organizations/{id}/teams/{id}/event-types/{id}/booking-fields | write | event types | Replace organization team booking fields. |
| PATCH | v2/organizations/{id}/teams/{id}/event-types/{id}/booking-fields | write | event types | Update organization team booking fields. |
| DELETE | v2/organizations/{id}/teams/{id}/event-types/{id}/booking-fields/{id} | write | event types | Delete a custom organization team booking field. |
| GET | v2/organizations/{id}/teams/{id}/event-types/{id}/calendar-invites | read | event types | Get organization team event-type calendar-invite templates. |
| PATCH | v2/organizations/{id}/teams/{id}/event-types/{id}/calendar-invites | write | event types | Update organization team event-type calendar-invite templates. |
| POST | v2/organizations/{id}/teams/{id}/event-types/{id}/create-phone-call | write | event types | Create a phone call for an organization team event type. |
| POST | v2/organizations/{id}/teams/{id}/event-types/{id}/duplicate | write | event types | Duplicate an organization team event type. |
| GET | v2/organizations/{id}/teams/{id}/event-types/{id}/private-links | read | event types | Get all private links for a team event type. |
| POST | v2/organizations/{id}/teams/{id}/event-types/{id}/private-links | write | event types | Create a private link for a team event type. |
| PATCH | v2/organizations/{id}/teams/{id}/event-types/{id}/private-links/{id} | write | event types | Update a private link for a team event type. |
| DELETE | v2/organizations/{id}/teams/{id}/event-types/{id}/private-links/{id} | write | event types | Delete a private link for a team event type. |
| GET | v2/teams/{id}/event-types | read | event types | List team event types. |
| POST | v2/teams/{id}/event-types | write | event types | Create a team event type. |
| GET | v2/teams/{id}/event-types/{id} | read | event types | Get a team event type. |
| PATCH | v2/teams/{id}/event-types/{id} | write | event types | Update a team event type. |
| DELETE | v2/teams/{id}/event-types/{id} | write | event types | Delete a team event type. |
| GET | v2/teams/{id}/event-types/{id}/booking-fields | read | event types | Get team booking fields. |
| POST | v2/teams/{id}/event-types/{id}/booking-fields | write | event types | Add custom team booking fields. |
| PUT | v2/teams/{id}/event-types/{id}/booking-fields | write | event types | Replace team booking fields. |
| PATCH | v2/teams/{id}/event-types/{id}/booking-fields | write | event types | Update team booking fields. |
| DELETE | v2/teams/{id}/event-types/{id}/booking-fields/{id} | write | event types | Delete a custom team booking field. |
| GET | v2/teams/{id}/event-types/{id}/calendar-invites | read | event types | Get team event-type calendar-invite templates. |
| PATCH | v2/teams/{id}/event-types/{id}/calendar-invites | write | event types | Update team event-type calendar-invite templates. |
| POST | v2/teams/{id}/event-types/{id}/create-phone-call | write | event types | Create a phone call for a team event type. |
| GET | v2/teams/{id}/event-types/{id}/webhooks | write | event types | Get all webhooks for a team event type. Kept out of read: response includes the webhook signing secret. |
| POST | v2/teams/{id}/event-types/{id}/webhooks | write | event types | Create a webhook for a team event type. |
| DELETE | v2/teams/{id}/event-types/{id}/webhooks | write | event types | Delete all webhooks for a team event type. |
| GET | v2/teams/{id}/event-types/{id}/webhooks/{id} | write | event types | Get a webhook for a team event type. Kept out of read: response includes the webhook signing secret. |
| PATCH | v2/teams/{id}/event-types/{id}/webhooks/{id} | write | event types | Update a webhook for a team event type. |
| DELETE | v2/teams/{id}/event-types/{id}/webhooks/{id} | write | event types | Delete a webhook for a team event type. |
| GET | v2/events | read | events | List Events (cursor pagination). |
| POST | v2/events | write | events | Create an Event. |
| GET | v2/events/{id} | read | events | Get an Event. |
| PATCH | v2/events/{id} | write | events | Update an Event. |
| DELETE | v2/events/{id} | write | events | Delete an Event. |
| GET | v2/events/{id}/bookings | read | events | List an Event's bookings. |
| POST | v2/events/{id}/cancel | write | events | Cancel an Event. |
| POST | v2/events/{id}/check-ins | write | events | Check in a guest by scanned QR token. |
| GET | v2/events/{id}/co-hosts | read | events | List an Event's co-hosts. |
| POST | v2/events/{id}/co-hosts | write | events | Invite a co-host to an Event. |
| PATCH | v2/events/{id}/co-hosts/order | write | events | Reorder an Event's co-hosts. |
| DELETE | v2/events/{id}/co-hosts/{id} | write | events | Remove a co-host from an Event. |
| GET | v2/events/{id}/coordinates | read | events | Get an Event's coordinates. |
| PATCH | v2/events/{id}/coordinates | write | events | Update an Event's coordinates. |
| POST | v2/events/{id}/cover-image | write | events | Upload an Event cover image. |
| DELETE | v2/events/{id}/cover-image | write | events | Remove an Event cover image. |
| GET | v2/events/{id}/host-candidates | read | events | Search the team members who can host an Event. |
| POST | v2/events/{id}/invitations | write | events | Invite guests to an Event. |
| GET | v2/events/{id}/locations | read | events | Get an Event's locations. |
| POST | v2/events/{id}/locations | write | events | Add a location to an Event. |
| PATCH | v2/events/{id}/locations/{id} | write | events | Edit an Event's location. |
| DELETE | v2/events/{id}/locations/{id} | write | events | Remove a location from an Event. |
| GET | v2/events/{id}/messages | read | events | List the messages sent to an Event's guests. |
| POST | v2/events/{id}/messages | write | events | Message an Event's guests. |
| POST | v2/events/{id}/messages/{id}/cancel | write | events | Cancel a scheduled message. |
| POST | v2/events/{id}/person-avatar | write | events | Upload an Event person avatar. |
| POST | v2/events/{id}/publish | write | events | Publish an Event. |
| POST | v2/events/{id}/registrations/approve-all | write | events | Approve every pending guest. |
| GET | v2/events/{id}/registrations/counts | read | events | Count an Event's guests. |
| POST | v2/events/{id}/registrations/{id}/approve | write | events | Approve a guest. |
| POST | v2/events/{id}/registrations/{id}/check-in | write | events | Check in a guest by registration id. |
| DELETE | v2/events/{id}/registrations/{id}/check-in | write | events | Undo a guest's check-in. |
| POST | v2/events/{id}/registrations/{id}/decline | write | events | Decline a guest. |
| GET | v2/teams/{id}/events | read | events | List a team's Events (cursor pagination). |
| POST | v2/teams/{id}/events | write | events | Create a team Event. |
| POST | v2/feedback | write | feedback | Report MCP feedback. |
| POST | v2/insights/booking-limits/usage | read | insights | Get booking limits usage. |
| POST | v2/insights/bookings/average-duration | read | insights | Get average booking duration. |
| POST | v2/insights/bookings/event-trends | read | insights | Get booking event trends. |
| POST | v2/insights/bookings/kpi-stats | read | insights | Get booking KPI stats. |
| POST | v2/insights/bookings/members | read | insights | Get booking member stats. |
| POST | v2/insights/routings/failed-bookings-by-field | read | insights | Get failed bookings by routing field. |
| POST | v2/insights/routings/form-field-options | read | insights | Get routing form field options. |
| POST | v2/insights/routings/form-response-headers | read | insights | Get routing form response headers. |
| POST | v2/insights/routings/form-responses | read | insights | Get routing form responses. |
| POST | v2/insights/routings/forms-by-status | read | insights | Get routing forms by status. |
| POST | v2/insights/routings/routed-to-per-period | read | insights | Get routed-to users per period. |
| POST | v2/organizations/{id}/teams/{id}/invite | write | invite | Create team invite link. |
| POST | v2/teams/{id}/invite | write | invite | Create team invite link. |
| GET | v2/links/{id} | read | links | Get a link. |
| DELETE | v2/links/{id} | write | links | Delete a link. |
| GET | v2/organizations/{id}/memberships | read | memberships | Get all memberships. |
| POST | v2/organizations/{id}/memberships | write | memberships | Create a membership. |
| GET | v2/organizations/{id}/memberships/{id} | read | memberships | Get a membership. |
| PATCH | v2/organizations/{id}/memberships/{id} | write | memberships | Update a membership. |
| DELETE | v2/organizations/{id}/memberships/{id} | write | memberships | Delete a membership. |
| GET | v2/organizations/{id}/teams/{id}/memberships | read | memberships | Get all memberships. |
| POST | v2/organizations/{id}/teams/{id}/memberships | write | memberships | Create a membership. |
| GET | v2/organizations/{id}/teams/{id}/memberships/{id} | read | memberships | Get a membership. |
| PATCH | v2/organizations/{id}/teams/{id}/memberships/{id} | write | memberships | Update a membership. |
| DELETE | v2/organizations/{id}/teams/{id}/memberships/{id} | write | memberships | Delete a membership. |
| GET | v2/teams/{id}/memberships | read | memberships | Get all memberships. |
| POST | v2/teams/{id}/memberships | write | memberships | Create a membership. |
| GET | v2/teams/{id}/memberships/{id} | read | memberships | Get a membership. |
| PATCH | v2/teams/{id}/memberships/{id} | write | memberships | Update membership. |
| DELETE | v2/teams/{id}/memberships/{id} | write | memberships | Delete a membership. |
| GET | v2/notifications/agent-channels | read | notifications | Get the agent notification channel selection. |
| PATCH | v2/notifications/agent-channels/{id} | write | notifications | Enable or disable an agent notification channel. |
| POST | v2/notifications/subscriptions/app-push | write | notifications | Register an app push subscription. |
| DELETE | v2/notifications/subscriptions/app-push | write | notifications | Remove an app push subscription. |
| DELETE | v2/notifications/subscriptions/imessage | write | notifications | Remove an iMessage push subscription. |
| POST | v2/notifications/subscriptions/imessage/link-intents | write | notifications | Create an iMessage push linking intent. |
| DELETE | v2/notifications/subscriptions/slack | write | notifications | Remove a Slack push subscription. |
| POST | v2/notifications/subscriptions/slack/link-intents | write | notifications | Create a Slack push linking intent. |
| DELETE | v2/notifications/subscriptions/telegram | write | notifications | Remove a Telegram push subscription. |
| POST | v2/notifications/subscriptions/telegram/link-intents | write | notifications | Create a Telegram push linking intent. |
| POST | v2/oauth/{id}/refresh | write | oauth | Refresh managed user tokens. |
| GET | v2/oauth-clients | write | oauth clients | Get all OAuth clients. Kept out of read: response includes the OAuth client secret. |
| POST | v2/oauth-clients | write | oauth clients | Create an OAuth client. |
| GET | v2/oauth-clients/{id} | write | oauth clients | Get an OAuth client. Kept out of read: response includes the OAuth client secret. |
| PATCH | v2/oauth-clients/{id} | write | oauth clients | Update an OAuth client. |
| DELETE | v2/oauth-clients/{id} | write | oauth clients | Delete an OAuth client. |
| GET | v2/oauth-clients/{id}/users | read | oauth clients | Get all managed users. |
| POST | v2/oauth-clients/{id}/users | write | oauth clients | Create a managed user. |
| GET | v2/oauth-clients/{id}/users/{id} | read | oauth clients | Get a managed user. |
| PATCH | v2/oauth-clients/{id}/users/{id} | write | oauth clients | Update a managed user. |
| DELETE | v2/oauth-clients/{id}/users/{id} | write | oauth clients | Delete a managed user. |
| POST | v2/oauth-clients/{id}/users/{id}/force-refresh | write | oauth clients | Force refresh tokens. |
| GET | v2/oauth-clients/{id}/webhooks | write | oauth clients | Get all webhooks. Kept out of read: response includes the webhook signing secret. |
| POST | v2/oauth-clients/{id}/webhooks | write | oauth clients | Create a webhook. |
| DELETE | v2/oauth-clients/{id}/webhooks | write | oauth clients | Delete all webhooks. |
| GET | v2/oauth-clients/{id}/webhooks/{id} | write | oauth clients | Get a webhook. Kept out of read: response includes the webhook signing secret. |
| PATCH | v2/oauth-clients/{id}/webhooks/{id} | write | oauth clients | Update a webhook. |
| DELETE | v2/oauth-clients/{id}/webhooks/{id} | write | oauth clients | Delete a webhook. |
| GET | v2/auth/oauth2/clients/{id} | read | oauth2 | Get OAuth2 client. |
| POST | v2/auth/oauth2/token | write | oauth2 | Exchange authorization code or refresh token for tokens. |
| GET | v2/organizations/{id}/ooo | read | ooo | Get all out-of-office entries for organization users. |
| GET | v2/organizations/{id}/users/{id}/ooo | read | ooo | Get all out-of-office entries for a user. |
| POST | v2/organizations/{id}/users/{id}/ooo | write | ooo | Create an out-of-office entry for a user. |
| PATCH | v2/organizations/{id}/users/{id}/ooo/{id} | write | ooo | Update an out-of-office entry for a user. |
| DELETE | v2/organizations/{id}/users/{id}/ooo/{id} | write | ooo | Delete an out-of-office entry for a user. |
| GET | v2/teams/{id}/users/{id}/ooo | read | ooo | Get all out-of-office entries for a team member. |
| POST | v2/teams/{id}/users/{id}/ooo | write | ooo | Create an out-of-office entry for a team member. |
| PATCH | v2/teams/{id}/users/{id}/ooo/{id} | write | ooo | Update an out-of-office entry for a team member. |
| DELETE | v2/teams/{id}/users/{id}/ooo/{id} | write | ooo | Delete an out-of-office entry for a team member. |
| GET | v2/organizations/{id}/organizations | read | organizations | Get all organizations within an organization. |
| POST | v2/organizations/{id}/organizations | write | organizations | Create an organization within an organization. |
| GET | v2/organizations/{id}/organizations/{id} | read | organizations | Get an organization within an organization. |
| PATCH | v2/organizations/{id}/organizations/{id} | write | organizations | Update an organization within an organization. |
| DELETE | v2/organizations/{id}/organizations/{id} | write | organizations | Delete an organization within an organization. |
| GET | v2/me | read | profile | Get my profile. |
| PATCH | v2/me | write | profile | Update my profile. |
| GET | v2/me/booking-limits | read | profile | Get my booking limits. |
| PATCH | v2/me/booking-limits | write | profile | Update my booking limits. |
| DELETE | v2/me/booking-limits | write | profile | Clear my booking limits. |
| GET | v2/me/ooo | read | profile | Get all out-of-office entries for the authenticated user. |
| POST | v2/me/ooo | write | profile | Create an out-of-office entry for the authenticated user. |
| PATCH | v2/me/ooo/{id} | write | profile | Update an out-of-office entry for the authenticated user. |
| DELETE | v2/me/ooo/{id} | write | profile | Delete an out-of-office entry for the authenticated user. |
| GET | v2/organizations/{id}/teams/me | read | profile | Get teams membership for user. |
| GET | v2/organizations/{id}/roles | read | roles | Get all organization roles. |
| POST | v2/organizations/{id}/roles | write | roles | Create a new organization role. |
| GET | v2/organizations/{id}/roles/{id} | read | roles | Get a specific organization role. |
| PATCH | v2/organizations/{id}/roles/{id} | write | roles | Update an organization role. |
| DELETE | v2/organizations/{id}/roles/{id} | write | roles | Delete an organization role. |
| GET | v2/organizations/{id}/roles/{id}/permissions | read | roles | List permissions for an organization role. |
| POST | v2/organizations/{id}/roles/{id}/permissions | write | roles | Add permissions to an organization role (single or batch). |
| PUT | v2/organizations/{id}/roles/{id}/permissions | write | roles | Replace all permissions for an organization role. |
| DELETE | v2/organizations/{id}/roles/{id}/permissions | write | roles | Remove multiple permissions from an organization role. |
| DELETE | v2/organizations/{id}/roles/{id}/permissions/{id} | write | roles | Remove a permission from an organization role. |
| GET | v2/organizations/{id}/teams/{id}/roles | read | roles | Get all organization team roles. |
| POST | v2/organizations/{id}/teams/{id}/roles | write | roles | Create a new organization team role. |
| GET | v2/organizations/{id}/teams/{id}/roles/{id} | read | roles | Get a specific organization team role. |
| PATCH | v2/organizations/{id}/teams/{id}/roles/{id} | write | roles | Update an organization team role. |
| DELETE | v2/organizations/{id}/teams/{id}/roles/{id} | write | roles | Delete an organization team role. |
| GET | v2/organizations/{id}/teams/{id}/roles/{id}/permissions | read | roles | List permissions for an organization team role. |
| POST | v2/organizations/{id}/teams/{id}/roles/{id}/permissions | write | roles | Add permissions to an organization team role (single or batch). |
| PUT | v2/organizations/{id}/teams/{id}/roles/{id}/permissions | write | roles | Replace all permissions for an organization team role. |
| DELETE | v2/organizations/{id}/teams/{id}/roles/{id}/permissions | write | roles | Remove multiple permissions from an organization team role. |
| DELETE | v2/organizations/{id}/teams/{id}/roles/{id}/permissions/{id} | write | roles | Remove a permission from an organization team role. |
| GET | v2/organizations/{id}/routing-forms | read | routing forms | Get organization routing forms. |
| GET | v2/organizations/{id}/routing-forms/{id}/responses | read | routing forms | Get routing form responses. |
| POST | v2/organizations/{id}/routing-forms/{id}/responses | write | routing forms | Create routing form response and get available slots. |
| PATCH | v2/organizations/{id}/routing-forms/{id}/responses/{id} | write | routing forms | Update routing form response. |
| GET | v2/organizations/{id}/teams/{id}/routing-forms | read | routing forms | Get team routing forms. |
| POST | v2/organizations/{id}/teams/{id}/routing-forms | write | routing forms | Create team routing form. |
| GET | v2/organizations/{id}/teams/{id}/routing-forms/{id} | read | routing forms | Get team routing form. |
| PATCH | v2/organizations/{id}/teams/{id}/routing-forms/{id}/fields | write | routing forms | Edit team routing form fields. |
| GET | v2/organizations/{id}/teams/{id}/routing-forms/{id}/history | read | routing forms | Get team routing form history. |
| GET | v2/organizations/{id}/teams/{id}/routing-forms/{id}/responses | read | routing forms | Get organization team routing form responses. |
| POST | v2/organizations/{id}/teams/{id}/routing-forms/{id}/responses | write | routing forms | Create routing form response and get available slots. |
| PATCH | v2/organizations/{id}/teams/{id}/routing-forms/{id}/responses/{id} | write | routing forms | Update routing form response. |
| PATCH | v2/organizations/{id}/teams/{id}/routing-forms/{id}/routes | write | routing forms | Edit team routing form routes. |
| POST | v2/routing-forms/{id}/calculate-slots | read | routing forms | Calculate slots based on routing form response. |
| POST | v2/teams/{id}/routing-forms/{id}/responses | write | routing forms | Create routing form response and get available slots. |
| GET | v2/organizations/{id}/schedules | read | schedules | Get all schedules. |
| GET | v2/organizations/{id}/teams/{id}/schedules | read | schedules | Get all team member schedules. |
| GET | v2/organizations/{id}/teams/{id}/users/{id}/schedules | read | schedules | Get schedules of a team member. |
| GET | v2/organizations/{id}/users/{id}/schedules | read | schedules | Get all schedules. |
| POST | v2/organizations/{id}/users/{id}/schedules | write | schedules | Create a schedule. |
| GET | v2/organizations/{id}/users/{id}/schedules/{id} | read | schedules | Get a schedule. |
| PATCH | v2/organizations/{id}/users/{id}/schedules/{id} | write | schedules | Update a schedule. |
| DELETE | v2/organizations/{id}/users/{id}/schedules/{id} | write | schedules | Delete a schedule. |
| GET | v2/schedules | read | schedules | Get all schedules. |
| POST | v2/schedules | write | schedules | Create a schedule. |
| GET | v2/schedules/default | read | schedules | Get default schedule. |
| GET | v2/schedules/{id} | read | schedules | Get a schedule. |
| PATCH | v2/schedules/{id} | write | schedules | Update a schedule. |
| DELETE | v2/schedules/{id} | write | schedules | Delete a schedule. |
| GET | v2/teams/{id}/schedules | read | schedules | Get all team member schedules. |
| GET | v2/organizations/{id}/secondary-domains | read | secondary domains | Get all secondary domains of an organization. |
| POST | v2/organizations/{id}/secondary-domains | write | secondary domains | Add a secondary domain to an organization. |
| GET | v2/organizations/{id}/secondary-domains/{id} | read | secondary domains | Get a secondary domain of an organization. |
| DELETE | v2/organizations/{id}/secondary-domains/{id} | write | secondary domains | Remove a secondary domain from an organization. |
| POST | v2/organizations/{id}/secondary-domains/{id}/verify | write | secondary domains | Verify a secondary domain of an organization. |
| POST | v2/selected-calendars | write | selected calendars | Add a selected calendar. |
| DELETE | v2/selected-calendars | write | selected calendars | Delete a selected calendar. |
| GET | v2/slots | read | slots | Get available time slots for an event type. |
| POST | v2/slots/reservations | write | slots | Reserve a slot. |
| GET | v2/slots/reservations/{id} | read | slots | Get reserved slot. |
| PATCH | v2/slots/reservations/{id} | write | slots | Update a reserved slot. |
| DELETE | v2/slots/reservations/{id} | write | slots | Delete a reserved slot. |
| GET | v2/organizations/{id}/teams/{id}/stripe/check | read | stripe | Check team Stripe connection. |
| GET | v2/organizations/{id}/teams/{id}/stripe/connect | write | stripe | Get Stripe connect URL for a team. Kept out of read: starts a provider connect flow. |
| GET | v2/organizations/{id}/teams/{id}/stripe/save | write | stripe | Save Stripe credentials. Kept out of read: saves provider credentials. |
| GET | v2/stripe/check | read | stripe | Check Stripe connection. |
| GET | v2/stripe/connect | write | stripe | Get Stripe connect URL. Kept out of read: starts a provider connect flow. |
| GET | v2/stripe/save | write | stripe | Save Stripe credentials. Kept out of read: saves provider credentials. |
| GET | v2/organizations/{id}/teams | read | teams | Get all teams. |
| POST | v2/organizations/{id}/teams | write | teams | Create a team. |
| GET | v2/organizations/{id}/teams/{id} | read | teams | Get a team. |
| PATCH | v2/organizations/{id}/teams/{id} | write | teams | Update a team. |
| DELETE | v2/organizations/{id}/teams/{id} | write | teams | Delete a team. |
| GET | v2/teams | read | teams | Get teams. |
| GET | v2/teams/{id} | read | teams | Get a team. |
| PATCH | v2/teams/{id} | write | teams | Update a team. |
| DELETE | v2/teams/{id} | write | teams | Delete a team. |
| GET | v2/timezones | read | timezones | Get timezones. |
| GET | v2/organizations/{id}/users | read | users | Get all users. |
| POST | v2/organizations/{id}/users | write | users | Create a user. |
| PATCH | v2/organizations/{id}/users/{id} | write | users | Update a user. |
| DELETE | v2/organizations/{id}/users/{id} | write | users | Delete a user. |
| GET | v2/organizations/{id}/teams/{id}/verified-resources/emails | read | verified resources | Get list of verified emails of an org team. |
| POST | v2/organizations/{id}/teams/{id}/verified-resources/emails/verification-code/request | write | verified resources | Request email verification code. |
| POST | v2/organizations/{id}/teams/{id}/verified-resources/emails/verification-code/verify | write | verified resources | Verify an email for an org team. |
| GET | v2/organizations/{id}/teams/{id}/verified-resources/emails/{id} | read | verified resources | Get verified email of an org team by id. |
| GET | v2/organizations/{id}/teams/{id}/verified-resources/phones | read | verified resources | Get list of verified phone numbers of an org team. |
| POST | v2/organizations/{id}/teams/{id}/verified-resources/phones/verification-code/request | write | verified resources | Request phone number verification code. |
| POST | v2/organizations/{id}/teams/{id}/verified-resources/phones/verification-code/verify | write | verified resources | Verify a phone number for an org team. |
| GET | v2/organizations/{id}/teams/{id}/verified-resources/phones/{id} | read | verified resources | Get verified phone number of an org team by id. |
| GET | v2/teams/{id}/verified-resources/emails | read | verified resources | Get list of verified emails of a team. |
| POST | v2/teams/{id}/verified-resources/emails/verification-code/request | write | verified resources | Request email verification code. |
| POST | v2/teams/{id}/verified-resources/emails/verification-code/verify | write | verified resources | Verify an email for a team. |
| GET | v2/teams/{id}/verified-resources/emails/{id} | read | verified resources | Get verified email of a team by id. |
| GET | v2/teams/{id}/verified-resources/phones | read | verified resources | Get list of verified phone numbers of a team. |
| POST | v2/teams/{id}/verified-resources/phones/verification-code/request | write | verified resources | Request phone number verification code. |
| POST | v2/teams/{id}/verified-resources/phones/verification-code/verify | write | verified resources | Verify a phone number for an org team. |
| GET | v2/teams/{id}/verified-resources/phones/{id} | read | verified resources | Get verified phone number of a team by id. |
| GET | v2/verified-resources/emails | read | verified resources | Get list of verified emails. |
| POST | v2/verified-resources/emails/verification-code/request | write | verified resources | Request email verification code. |
| POST | v2/verified-resources/emails/verification-code/verify | write | verified resources | Verify an email. |
| GET | v2/verified-resources/emails/{id} | read | verified resources | Get verified email by id. |
| GET | v2/verified-resources/phones | read | verified resources | Get list of verified phone numbers. |
| POST | v2/verified-resources/phones/verification-code/request | write | verified resources | Request phone number verification code. |
| POST | v2/verified-resources/phones/verification-code/verify | write | verified resources | Verify a phone number. |
| GET | v2/verified-resources/phones/{id} | read | verified resources | Get verified phone number by id. |
| GET | v2/organizations/{id}/webhooks | write | webhooks | Get all webhooks. Kept out of read: response includes the webhook signing secret. |
| POST | v2/organizations/{id}/webhooks | write | webhooks | Create a webhook. |
| GET | v2/organizations/{id}/webhooks/{id} | write | webhooks | Get a webhook. Kept out of read: response includes the webhook signing secret. |
| PATCH | v2/organizations/{id}/webhooks/{id} | write | webhooks | Update a webhook. |
| DELETE | v2/organizations/{id}/webhooks/{id} | write | webhooks | Delete a webhook. |
| GET | v2/webhooks | write | webhooks | Get all webhooks. Kept out of read: response includes the webhook signing secret. |
| POST | v2/webhooks | write | webhooks | Create a webhook. |
| GET | v2/webhooks/{id} | write | webhooks | Get a webhook. Kept out of read: response includes the webhook signing secret. |
| PATCH | v2/webhooks/{id} | write | webhooks | Update a webhook. |
| DELETE | v2/webhooks/{id} | write | webhooks | Delete a webhook. |
| GET | v2/organizations/{id}/teams/{id}/workflows | read | workflows | Get organization team workflows. |
| POST | v2/organizations/{id}/teams/{id}/workflows | write | workflows | Create organization team workflow for event-types. |
| GET | v2/organizations/{id}/teams/{id}/workflows/routing-form | read | workflows | Get organization team routing form workflows. |
| POST | v2/organizations/{id}/teams/{id}/workflows/routing-form | write | workflows | Create organization team workflow for routing-forms. |
| GET | v2/organizations/{id}/teams/{id}/workflows/{id} | read | workflows | Get organization team workflow. |
| PATCH | v2/organizations/{id}/teams/{id}/workflows/{id} | write | workflows | Update organization team workflow. |
| DELETE | v2/organizations/{id}/teams/{id}/workflows/{id} | write | workflows | Delete organization team workflow. |
| GET | v2/organizations/{id}/teams/{id}/workflows/{id}/condition-fields | read | workflows | Get organization team workflow condition fields. |
| GET | v2/organizations/{id}/teams/{id}/workflows/{id}/routing-form | read | workflows | Get organization team routing form workflow. |
| PATCH | v2/organizations/{id}/teams/{id}/workflows/{id}/routing-form | write | workflows | Update organization routing form team workflow. |
| DELETE | v2/organizations/{id}/teams/{id}/workflows/{id}/routing-form | write | workflows | Delete organization team routing-form workflow. |
| GET | v2/workflows | read | workflows | Get your workflows. |
| POST | v2/workflows | write | workflows | Create a workflow. |
| GET | v2/workflows/{id} | read | workflows | Get your workflow. |
| PATCH | v2/workflows/{id} | write | workflows | Update your workflow. |
| DELETE | v2/workflows/{id} | write | workflows | Delete your workflow. |
| GET | v2/workflows/{id}/condition-fields | read | workflows | Get the fields a workflow's conditions can read. |
