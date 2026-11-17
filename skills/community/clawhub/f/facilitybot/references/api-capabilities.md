# FacilityBot read-only API capabilities

Sources: [FacilityBot Public API documentation](https://portal.facilitybot.co/client-api), reviewed 2026-11-02; read-only endpoint index verified through the connected FacilityBot MCP on 2026-11-03.

The current MCP index exposes 29 GET endpoints. Only these read operations are in scope for this release. These operation IDs are REST documentation identifiers, not MCP tool names. Inspect the connected search/execute schemas for current parameters and response fields.

## Requests

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listRequestsV1` | `GET /api/client/v1/requests` | List requests |
| `listAllRequestStatusesV1` | `GET /api/client/v1/requests/all_status` | Get all request statuses |
| `getRequestByIdV1` | `GET /api/client/v1/requests/{id}` | Detail a request |

## Request Types

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listRequestTypesV1` | `GET /api/client/v1/request_types` | List available request types |
| `getRequestTypeByIdV1` | `GET /api/client/v1/request_types/{id}` | Show request type details |
| `listRequestTypeOrderItemsV1` | `GET /api/client/v1/request_types/{id}/order_items` | List order items for a request type |

## Facility Bookings

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listFacilityBookingsV1` | `GET /api/client/v1/facility_bookings` | Return all facility bookings |
| `getFacilityBookingCalendarV1` | `GET /api/client/v1/facility_bookings/get_calendar` | Return booked slots of a facility for calendar view |
| `checkFacilityBookingAvailableV1` | `GET /api/client/v1/facility_bookings/check_available` | Check if a facility is available for a booking period |
| `checkFacilityBookingDayAvailableV1` | `GET /api/client/v1/facility_bookings/check_day_available` | Check if a facility is available for a whole day |
| `getFacilityBookingByIdV1` | `GET /api/client/v1/facility_bookings/{id}` | Return details a facility booking |

## Facilities

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listFacilitySettingsV1` | `GET /api/client/v1/facility_settings` | Return all bookable facilities |
| `getFacilitySettingByIdV1` | `GET /api/client/v1/facility_settings/{id}` | Return details a bookable facility |

## Visitors

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listVisitorsV1` | `GET /api/client/v1/visitors` | Return all visitors |
| `getVisitorByIdV1` | `GET /api/client/v1/visitors/{id}` | Return details a visitor |

## Assets

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listAssetsV1` | `GET /api/client/v1/assets` | Return all asset trackings |
| `getAssetByIdV1` | `GET /api/client/v1/assets/{id}` | Details of an asset tracking |

## Checklists

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listChecklistsV1` | `GET /api/client/v1/checklists` | Return all checklists |
| `getChecklistByIdV1` | `GET /api/client/v1/checklists/{id}` | Return a checklist |

## Fault Types

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listFaultTypesV1` | `GET /api/client/v1/fault_types` | Return all fault types |
| `getFaultTypeByIdV1` | `GET /api/client/v1/fault_types/{id}` | Details of a fault type |

## Fault Location Tags

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listLocationTagsV1` | `GET /api/client/v1/location_tags` | Return all location tags |
| `getLocationTagByIdV1` | `GET /api/client/v1/location_tags/{id}` | Details of a location tag |

## Requestors

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listRequestorsV1` | `GET /api/client/v1/requestors` | Return all requestors |
| `getRequestorByUidV1` | `GET /api/client/v1/requestors/{uid}` | Return a requestor |
| `listRequestorRequestsV1` | `GET /api/client/v1/requestors/{uid}/requests` | Return all requests belongs to a requestor |

## Requestor Tags

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listRequestorTagsV1` | `GET /api/client/v1/requestor_tags` | Return all requestor tags |
| `getRequestorTagByIdV1` | `GET /api/client/v1/requestor_tags/{id}` | Details of a requestor tag |

## Toilet Feedbacks

| Operation ID | Method and path | Purpose |
|---|---|---|
| `listToiletFeedbacksV1` | `GET /api/client/v1/toilet_feedbacks` | Return list of toilet feedbacks |

## Important contracts

- Keep MCP credentials in the connection configuration. Follow the official setup instructions for the intended environment; do not put keys in prompts, source files, or examples.
- The connected MCP search tool discovers endpoint schemas; its execute tool calls GET endpoints. Tool names can vary by host. Never infer write support from the wider Public API.
- Standard responses have `code`, `message`, and `data`; paginated lists can include `page`, `per_page`, `total_pages`, and `count`. Verify each operation's actual schema. Use supported `fields` and `per_page` parameters to limit response size.
- `listAllRequestStatusesV1` returns lifecycle and configured custom statuses for the authenticated account. Resolve status codes before filtering; a custom label alone does not establish whether a request is closed.
- Preserve requestor UIDs as strings, including leading zeros. Resolve location tag hierarchies and distinguish tag IDs from free-text locations.
- Visitor access depends on the connection's permissions and restrictions. Do not equate Admin, Manager, Custom Manager, Responder, and Requestor access. An access error is not an empty result.
- Interpret date ranges and timezone according to the selected endpoint and trusted account context. Check whether a date filter requires both start and end values before using it.
- Availability checks do not reserve a facility. This skill does not create bookings, submit checklists, change statuses, assign work, or modify records.
- Error examples from the Public API: 401/10003 unauthorized; 404/20001 not found; 400/30001 invalid operation; 429/30002 limit exceeded; 400/40001 required field missing; 400/40002 invalid format; 400/40003 invalid value; 500/60001 unknown error. Inspect the actual response rather than treating every non-success as no records.
