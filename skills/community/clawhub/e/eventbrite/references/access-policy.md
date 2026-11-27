# Eventbrite access policy

An access policy limits which endpoints Eventbrite connections may call through Maton. Eventbrite doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/eventbrite#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Eventbrite: its 66 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create eventbrite --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v3/events/{id}/attendees/"},
    {"method": "GET", "path": "v3/events/{id}/attendees/{id}/"},
    {"method": "GET", "path": "v3/organizations/{id}/attendees/"},
    {"method": "GET", "path": "v3/categories/"},
    {"method": "GET", "path": "v3/categories/{id}/"},
    {"method": "GET", "path": "v3/discounts/{id}/"},
    {"method": "GET", "path": "v3/organizations/{id}/discounts/"},
    {"method": "GET", "path": "v3/balance/{id}/events/{id}/"},
    {"method": "GET", "path": "v3/events/search/"},
    {"method": "GET", "path": "v3/events/{id}/"},
    {"method": "GET", "path": "v3/events/{id}/capacity_tier/"},
    {"method": "GET", "path": "v3/events/{id}/description/"},
    {"method": "GET", "path": "v3/events/{id}/display_settings/"},
    {"method": "GET", "path": "v3/events/{id}/ticket_buyer_settings/"},
    {"method": "GET", "path": "v3/organizations/{id}/events/"},
    {"method": "GET", "path": "v3/formats/"},
    {"method": "GET", "path": "v3/formats/{id}/"},
    {"method": "GET", "path": "v3/events/{id}/inventory_tiers/"},
    {"method": "GET", "path": "v3/events/{id}/inventory_tiers/{id}/"},
    {"method": "GET", "path": "v3/media/upload/"},
    {"method": "GET", "path": "v3/media/{id}/"},
    {"method": "GET", "path": "v3/organizations/{id}/members/"},
    {"method": "GET", "path": "v3/events/{id}/orders/"},
    {"method": "GET", "path": "v3/orders/{id}/"},
    {"method": "GET", "path": "v3/orders/{id}/get_retention_policy_information/"},
    {"method": "GET", "path": "v3/organizations/{id}/orders/"},
    {"method": "POST", "path": "v3/pricing/calculate_price_for_item/"},
    {"method": "GET", "path": "v3/pricing/fee_rates/"},
    {"method": "GET", "path": "v3/events/{id}/canned_questions/"},
    {"method": "GET", "path": "v3/events/{id}/canned_questions/{id}/"},
    {"method": "GET", "path": "v3/events/{id}/questions/"},
    {"method": "GET", "path": "v3/events/{id}/questions/{id}/"},
    {"method": "GET", "path": "v3/reports/attendees/"},
    {"method": "GET", "path": "v3/reports/sales/"},
    {"method": "GET", "path": "v3/organizations/{id}/roles/"},
    {"method": "GET", "path": "v3/organizations/{id}/seatmaps/"},
    {"method": "GET", "path": "v3/series/{id}/"},
    {"method": "GET", "path": "v3/series/{id}/events/"},
    {"method": "GET", "path": "v3/events/{id}/structured_content/"},
    {"method": "GET", "path": "v3/events/{id}/structured_content/edit/"},
    {"method": "GET", "path": "v3/subcategories/"},
    {"method": "GET", "path": "v3/subcategories/{id}/"},
    {"method": "GET", "path": "v3/system/countries/"},
    {"method": "GET", "path": "v3/system/regions/"},
    {"method": "GET", "path": "v3/events/{id}/teams/"},
    {"method": "GET", "path": "v3/events/{id}/teams/search/"},
    {"method": "GET", "path": "v3/events/{id}/teams/{id}/"},
    {"method": "GET", "path": "v3/events/{id}/teams/{id}/attendees/"},
    {"method": "GET", "path": "v3/organizations/{id}/text_overrides/"},
    {"method": "GET", "path": "v3/events/{id}/ticket_classes/"},
    {"method": "GET", "path": "v3/events/{id}/ticket_classes/for_sale/"},
    {"method": "GET", "path": "v3/events/{id}/ticket_classes/{id}/"},
    {"method": "GET", "path": "v3/organizations/{id}/ticket_groups/"},
    {"method": "GET", "path": "v3/ticket_groups/{id}/"},
    {"method": "GET", "path": "v3/users/me/"},
    {"method": "GET", "path": "v3/users/me/orders/"},
    {"method": "GET", "path": "v3/users/me/organizations/"},
    {"method": "GET", "path": "v3/users/me/owned_events/"},
    {"method": "GET", "path": "v3/users/{id}/"},
    {"method": "GET", "path": "v3/users/{id}/orders/"},
    {"method": "GET", "path": "v3/users/{id}/organizations/"},
    {"method": "GET", "path": "v3/organizations/{id}/venues/"},
    {"method": "GET", "path": "v3/venues/{id}/"},
    {"method": "GET", "path": "v3/venues/{id}/events/"},
    {"method": "GET", "path": "v3/organizations/{id}/webhooks/"},
    {"method": "GET", "path": "v3/webhooks/"}
  ],
  "deny": []
}
```

## Endpoints

The Eventbrite endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v3/events/{id}/attendees/ | read | attendees | List Attendees by Event ID. |
| GET | v3/events/{id}/attendees/{id}/ | read | attendees | Retrieve an Attendee by Attendee ID. |
| GET | v3/organizations/{id}/attendees/ | read | attendees | List Attendees of an Organization's Events by Organization ID. |
| GET | v3/categories/ | read | categories | Returns a list of Category as categories, including subcategories nested. |
| GET | v3/categories/{id}/ | read | categories | Retrieve a category by ID. |
| GET | v3/discounts/{id}/ | read | discounts | Retrieve a Discount by Discount ID. |
| POST | v3/discounts/{id}/ | write | discounts | Update a Discount by Discount ID. |
| DELETE | v3/discounts/{id}/ | write | discounts | Delete a Discount. |
| GET | v3/organizations/{id}/discounts/ | read | discounts | List Discounts by Organization ID. |
| POST | v3/organizations/{id}/discounts/ | write | discounts | Create a new Discount. |
| GET | v3/balance/{id}/events/{id}/ | read | events | Return the event-level balance at the time of the call. |
| GET | v3/events/search/ | read | events | List public Events from Eventbrite. |
| GET | v3/events/{id}/ | read | events | Retrieve an Event by Event ID. |
| POST | v3/events/{id}/ | write | events | Update Event by Event ID. |
| DELETE | v3/events/{id}/ | write | events | Delete an Event if the delete is permitted. |
| POST | v3/events/{id}/cancel/ | write | events | Cancel an Event. |
| GET | v3/events/{id}/capacity_tier/ | read | events | Retrieve the capacity tier for an event. |
| POST | v3/events/{id}/capacity_tier/ | write | events | Update the capacity tier for an event. |
| POST | v3/events/{id}/copy/ | write | events | Copy the Event, creating a duplicate version of the Event with a new Event ID. |
| GET | v3/events/{id}/description/ | read | events | Returns the fully rendered description for an Event as a string of HTML. |
| GET | v3/events/{id}/display_settings/ | read | events | Retrieve the Display Settings for an Event by Event ID. |
| POST | v3/events/{id}/display_settings/ | write | events | Update Display Settings for an Event by Event ID. |
| POST | v3/events/{id}/publish/ | write | events | Publish an Event. |
| POST | v3/events/{id}/schedules/ | write | events | Create an event schedule for an existing series parent event. |
| GET | v3/events/{id}/ticket_buyer_settings/ | read | events | Retrieve Ticket Buyer Settings by Event ID. |
| POST | v3/events/{id}/ticket_buyer_settings/ | write | events | Update Ticket Buyer Settings by Event ID. |
| POST | v3/events/{id}/unpublish/ | write | events | Unpublish an Event. |
| GET | v3/organizations/{id}/events/ | read | events | List Events by Organization ID. |
| POST | v3/organizations/{id}/events/ | write | events | Create a new Event. |
| GET | v3/formats/ | read | formats | List all available Formats. |
| GET | v3/formats/{id}/ | read | formats | Retrieve a Format by Format ID. |
| GET | v3/events/{id}/inventory_tiers/ | read | inventory_tiers | Retrieves inventory tiers for an event. |
| POST | v3/events/{id}/inventory_tiers/ | write | inventory_tiers | Create one or more inventory tiers for an event, or update multiple existing tiers. |
| GET | v3/events/{id}/inventory_tiers/{id}/ | read | inventory_tiers | Retrieve an Inventory Tier by ID for an Event. |
| POST | v3/events/{id}/inventory_tiers/{id}/ | write | inventory_tiers | Update an existing Inventory Tier by ID for an Event. |
| DELETE | v3/events/{id}/inventory_tiers/{id}/ | write | inventory_tiers | Mark an existing Inventory Tier as deleted. |
| GET | v3/media/upload/ | read | media | Retrieve information on a Media image upload. |
| POST | v3/media/upload/ | write | media | Upload a Media image file. |
| GET | v3/media/{id}/ | read | media | Retrieve Media by Media ID. |
| GET | v3/organizations/{id}/members/ | read | members | List an Organization's Members by Organization ID. |
| GET | v3/events/{id}/orders/ | read | orders | List Orders by Event ID. |
| GET | v3/orders/{id}/ | read | orders | Retrieve an Order by Order ID. |
| GET | v3/orders/{id}/get_retention_policy_information/ | read | orders | Get the refund retention policy information for an order. |
| POST | v3/orders/{id}/refunds/ | write | orders | Refund an order. |
| GET | v3/organizations/{id}/orders/ | read | orders | List orders placed against any of the organization events. |
| POST | v3/pricing/calculate_price_for_item/ | read | pricing | Calculate the fees Eventbrite would charge for a given ticket price. |
| GET | v3/pricing/fee_rates/ | read | pricing | List all available Pricing rates. |
| GET | v3/events/{id}/canned_questions/ | read | questions | List default Questions by Event ID. |
| POST | v3/events/{id}/canned_questions/ | write | questions | Create a default Question for an Event. |
| GET | v3/events/{id}/canned_questions/{id}/ | read | questions | Retrieve a Canned Question by Event and Question ID. |
| POST | v3/events/{id}/canned_questions/{id}/ | write | questions | Modify details of the canned question of the event. |
| DELETE | v3/events/{id}/canned_questions/{id}/ | write | questions | Deactivate a canned question for the event. |
| GET | v3/events/{id}/questions/ | read | questions | List custom Questions by Event ID. |
| POST | v3/events/{id}/questions/ | write | questions | Create a custom Question for an Event. |
| GET | v3/events/{id}/questions/{id}/ | read | questions | Retrieve a Custom Question by Event and Question ID. |
| DELETE | v3/events/{id}/questions/{id}/ | write | questions | Delete a custom Question by Event and Question ID. |
| GET | v3/reports/attendees/ | read | reports | Retrieve an Attendee Report by Event ID or Event status. |
| GET | v3/reports/sales/ | read | reports | Retrieve a sales Report by Event ID or Event status. |
| GET | v3/organizations/{id}/roles/ | read | roles | List an Organization's Roles by Organization ID. |
| POST | v3/events/{id}/seatmaps/ | write | seatmaps | Create a Seat Map for a new reserved seating event by copying an existing seat map. |
| GET | v3/organizations/{id}/seatmaps/ | read | seatmaps | List Seat Maps of an Organization. |
| GET | v3/series/{id}/ | read | series | Retrieve the parent Event Series by Event Series ID. |
| GET | v3/series/{id}/events/ | read | series | List Events by Event Series ID. |
| GET | v3/events/{id}/structured_content/ | read | structured_content | Retrieve a paginated response of structured content for the given event id. |
| GET | v3/events/{id}/structured_content/edit/ | read | structured_content | Retrieve a paginated response of structured content for the given event. |
| POST | v3/events/{id}/structured_content/{id}/ | write | structured_content | Add new structured content to an event for a given version. |
| GET | v3/subcategories/ | read | subcategories | List all available Subcategories. |
| GET | v3/subcategories/{id}/ | read | subcategories | Retrieve a Subcategory by Subcategory ID. |
| GET | v3/system/countries/ | read | system | List countries. |
| GET | v3/system/regions/ | read | system | List regions. |
| GET | v3/events/{id}/teams/ | read | teams | Returns a list of teams for the event. |
| POST | v3/events/{id}/teams/create/ | write | teams | Create and returns a team. |
| GET | v3/events/{id}/teams/search/ | read | teams | Returns the teams of an event searched by name. |
| GET | v3/events/{id}/teams/{id}/ | read | teams | Returns information for a single team. |
| GET | v3/events/{id}/teams/{id}/attendees/ | read | teams | Returns attendee for a single team. |
| POST | v3/events/{id}/teams/{id}/check_password/ | write | teams | Verify that the password of a team is correct, and if so, and returns the token of the team. |
| GET | v3/organizations/{id}/text_overrides/ | read | text_overrides | Retrieve text overrides for a locale, optionally filtered by event, venue or text code. |
| POST | v3/organizations/{id}/text_overrides/ | write | text_overrides | Create the Text Overrides for an organization, Venue, or Event. |
| GET | v3/events/{id}/ticket_classes/ | read | ticket_classes | List Ticket Classes by Event ID. |
| POST | v3/events/{id}/ticket_classes/ | write | ticket_classes | Create a new Ticket Class. |
| GET | v3/events/{id}/ticket_classes/for_sale/ | read | ticket_classes | List Ticket Classes available for sale by Event ID for use in the purchase flow. |
| GET | v3/events/{id}/ticket_classes/{id}/ | read | ticket_classes | Retrieve a Ticket Class by Ticket Class ID. |
| POST | v3/events/{id}/ticket_classes/{id}/ | write | ticket_classes | Update Ticket Class by Ticket Class ID. |
| DELETE | v3/events/{id}/ticket_classes/{id}/ | write | ticket_classes | Delete a ticket class. |
| POST | v3/organizations/{id}/events/{id}/ticket_classes/{id}/ticket_groups/ | write | ticket_groups | Add a Ticket Class to Ticket Groups by Organization ID and Event ID. |
| GET | v3/organizations/{id}/ticket_groups/ | read | ticket_groups | List Ticket Groups by Organization ID. |
| POST | v3/organizations/{id}/ticket_groups/ | write | ticket_groups | Create a new ticket group for an organization. |
| GET | v3/ticket_groups/{id}/ | read | ticket_groups | Retrieve a Ticket Group by Ticket Group ID. |
| POST | v3/ticket_groups/{id}/ | write | ticket_groups | Update Ticket Group by Ticket Group ID. |
| DELETE | v3/ticket_groups/{id}/ | write | ticket_groups | Delete a Ticket Group. |
| GET | v3/users/me/ | read | users | Retrieve your User account information. |
| GET | v3/users/me/orders/ | read | users | List orders placed by the current user. |
| GET | v3/users/me/organizations/ | read | users | List the Organizations to which you are a Member. |
| GET | v3/users/me/owned_events/ | read | users | List events owned by the current user. |
| GET | v3/users/{id}/ | read | users | Returns a user for the specified user as user. |
| GET | v3/users/{id}/orders/ | read | users | List Orders by User ID. |
| GET | v3/users/{id}/organizations/ | read | users | List Organizations by User ID. |
| GET | v3/organizations/{id}/venues/ | read | venues | List Venues by Organization ID. |
| POST | v3/organizations/{id}/venues/ | write | venues | Create new Venue under an Organization. |
| GET | v3/venues/{id}/ | read | venues | Retrieve a Venue by Venue ID. |
| POST | v3/venues/{id}/ | write | venues | Update a Venue by Venue ID. |
| GET | v3/venues/{id}/events/ | read | venues | List Events by Venue ID. |
| GET | v3/organizations/{id}/webhooks/ | read | webhooks | List Webhooks by Organization ID. |
| POST | v3/organizations/{id}/webhooks/ | write | webhooks | Create a Webhook by Organization ID. |
| GET | v3/webhooks/ | read | webhooks | List Webhooks. |
| POST | v3/webhooks/ | write | webhooks | Create a Webhook. |
| DELETE | v3/webhooks/{id}/ | write | webhooks | Delete a Webhook by ID. |
