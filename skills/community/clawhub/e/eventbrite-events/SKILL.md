---
name: eventbrite-events
description: Manage Eventbrite events, attendees, organizations, venues, orders, and ticketing data - powered by ClawLink.
---

# Eventbrite

![Eventbrite](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/eventbrite.png)

Work with Eventbrite from chat — manage events, attendees, organizations, venues, orders, and ticketing data.

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=eventbrite-events), an integration hub for OpenClaw that handles hosted connection flows and credentials so you don't need to configure Eventbrite API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Eventbrite |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Eventbrite |

## Connection flow

```
User → ClawLink OAuth → Eventbrite account
         ↓
    OpenClaw tools
    (via ClawLink)
```

**Step 1** — Install the ClawLink plugin:
```
openclaw plugins install clawhub:clawlink-plugin
```
Start a fresh chat after installing.

**Step 2** — Pair ClawLink:
1. Call `clawlink_begin_pairing`
2. Open the returned URL in your browser
3. Sign in to ClawLink and approve the device

**Step 3** — Connect Eventbrite:
Open [claw-link.dev/dashboard?add=eventbrite](https://claw-link.dev/dashboard?add=eventbrite), complete the OAuth flow, then confirm.

*App-specific connection GIF coming soon*

**Step 4** — Verify and discover:
```javascript
// 1. Verify Eventbrite is connected
clawlink_list_integrations()

// 2. List available tools
clawlink_list_tools({ integration: "eventbrite" })

// 3. Search tools if needed
clawlink_search_tools({ query: "event", integration: "eventbrite" })
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw (you)                       │
├─────────────────────────────────────────────────────────┤
│  ClawLink Plugin  →  clawlink_* tools                   │
├─────────────────────────────────────────────────────────┤
│                    ClawLink Cloud                       │
│         (credentials, connection state, routing)        │
├─────────────────────────────────────────────────────────┤
│            Eventbrite API (user's account)              │
└─────────────────────────────────────────────────────────┘
```

## Tool reference

### Events

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_event` | Get event details by ID (name, description, dates, venue) | safe |
| `eventbrite_get_event_description` | Get full HTML description for an event | safe |
| `eventbrite_get_display_settings` | Get what information is shown on event page | safe |
| `eventbrite_get_structured_content` | Get published structured content (modules, widgets) | safe |
| `eventbrite_get_structured_content_edit` | Get working (editable) version of structured content | safe |
| `eventbrite_list_organization_events` | List events owned by an organization | safe |
| `eventbrite_list_venue_events` | List all events at a specific venue | safe |
| `eventbrite_list_series_events` | List all events in a series | safe |
| `eventbrite_get_series` | Get parent event series details | safe |
| `eventbrite_get_event_categories` | List available event categories | safe |
| `eventbrite_get_event_subcategories` | List event subcategories | safe |
| `eventbrite_get_category` | Get a specific category by ID | safe |
| `eventbrite_get_subcategory` | Get a specific subcategory by ID | safe |
| `eventbrite_get_format` | Get a specific event format | safe |
| `eventbrite_get_event_formats` | List available event formats | safe |
| `eventbrite_create_event` | Create a new event or series parent | confirm |
| `eventbrite_create_event_schedule` | Add recurring occurrences to a series event | confirm |
| `eventbrite_copy_event` | Duplicate an existing event | confirm |
| `eventbrite_update_event` | Update event details | confirm |
| `eventbrite_set_structured_content` | Set structured content (create/update) | confirm |
| `eventbrite_update_display_settings` | Update what info is shown on event page | confirm |
| `eventbrite_publish_event` | Make event live and publicly accessible | confirm |
| `eventbrite_unpublish_event` | Remove event from public view (can republish) | confirm |
| `eventbrite_cancel_event` | Cancel an event (fails if orders exist) | high_impact |
| `eventbrite_delete_event` | Delete an event (fails if orders exist) | high_impact |

### Attendees & orders

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_list_event_attendees` | List attendees for an event (paginated) | safe |
| `eventbrite_list_event_orders` | List orders for an event (paginated) | safe |
| `eventbrite_list_org_attendees` | List attendees across all org events (paginated) | safe |
| `eventbrite_list_organization_orders` | List orders for all org events | safe |
| `eventbrite_list_user_orders` | List orders for a specific user | safe |
| `eventbrite_get_attendee_report` | Get aggregated attendee data and sales statistics | safe |
| `eventbrite_get_sales_report` | Get detailed sales data by event/status | safe |

### Ticket classes

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_ticket_class` | Get ticket class details by ID | safe |
| `eventbrite_list_ticket_classes` | List all ticket classes for an event | safe |
| `eventbrite_list_ticket_classes_for_sale` | List ticket classes currently on sale | safe |
| `eventbrite_create_ticket_class` | Create a new ticket class (GA, VIP, Early Bird, etc.) | confirm |
| `eventbrite_update_ticket_class` | Update ticket class details | confirm |
| `eventbrite_delete_ticket_class` | Delete a ticket class | high_impact |

### Inventory & capacity

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_capacity_tier` | Get event capacity tier info | safe |
| `eventbrite_update_capacity_tier` | Update event capacity tier settings | confirm |
| `eventbrite_get_inventory_tier` | Get inventory tier by ID | safe |
| `eventbrite_list_inventory_tiers` | List inventory tiers for an event | safe |
| `eventbrite_create_inventory_tier` | Create a new inventory tier | confirm |
| `eventbrite_update_inventory_tier` | Update an inventory tier | confirm |
| `eventbrite_delete_inventory_tier` | Mark inventory tier as deleted | high_impact |

### Ticket groups

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_ticket_group` | Get ticket group by ID | safe |
| `eventbrite_list_ticket_groups` | List ticket groups for an organization | safe |
| `eventbrite_create_ticket_group` | Create a new ticket group (max 300 live per org) | confirm |
| `eventbrite_update_ticket_group` | Update a ticket group | confirm |
| `eventbrite_delete_ticket_group` | Mark ticket group as deleted | high_impact |
| `eventbrite_add_ticket_to_group` | Add ticket class to ticket groups | confirm |
| `eventbrite_add_ticket_to_group_by_organization` | Add ticket to group by org/event IDs | confirm |

### Pricing & fees

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_calculate_price_for_item` | Calculate fees and taxes for a given price | safe |
| `eventbrite_list_pricing` | List available pricing fee rates by currency/country | safe |

### Discounts & access codes

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_discount` | Get discount details by ID | safe |
| `eventbrite_search_discounts_by_organization` | Search discounts by org (paginated) | safe |
| `eventbrite_create_discount` | Create a promotional discount or coupon | confirm |
| `eventbrite_update_discount` | Update a discount | confirm |
| `eventbrite_delete_discount` | Delete an unused discount | high_impact |
| `eventbrite_get_access_code` | Get access code details by ID | safe |
| `eventbrite_list_access_codes` | List all access codes for an event | safe |
| `eventbrite_create_access_code` | Create promotional/early bird/VIP codes | confirm |
| `eventbrite_update_access_code` | Update an access code | confirm |

### Venues

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_venue` | Get venue details by ID (name, location, capacity) | safe |
| `eventbrite_list_org_venues` | List venues owned by an organization | safe |
| `eventbrite_create_venue` | Create a new venue under an organization | confirm |
| `eventbrite_update_venue` | Update venue details | confirm |

### Organizers

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_organizer` | Get organizer details by ID | safe |
| `eventbrite_list_org_organizers` | List organizers for an organization | safe |
| `eventbrite_create_organizer` | Create a new organizer profile | confirm |
| `eventbrite_update_organizer` | Update organizer details | confirm |

### Questions

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_default_question` | Get a specific default (canned) question | safe |
| `eventbrite_list_default_questions` | List default questions for an event | safe |
| `eventbrite_update_default_question` | Update a default question | confirm |
| `eventbrite_delete_default_question` | Deactivate a default question | high_impact |
| `eventbrite_get_custom_question` | Get a specific custom question | safe |
| `eventbrite_list_custom_questions` | List custom questions for an event | safe |
| `eventbrite_create_custom_question` | Create a custom question for registration | confirm |

### Organizations

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_assortment` | Get organization plan type and version details | safe |
| `eventbrite_update_assortment` | Update organization plan type | confirm |
| `eventbrite_get_checkout_settings` | Get organization's checkout configuration | safe |
| `eventbrite_create_checkout_settings` | Create checkout settings for an org | confirm |
| `eventbrite_list_organization_roles` | List organization roles and permissions | safe |
| `eventbrite_list_organization_members` | List organization members | safe |
| `eventbrite_list_organization_webhooks` | List webhooks configured for an org | safe |

### Users

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_me` | Get authenticated user's account info | safe |
| `eventbrite_get_user` | Get user details by ID (use 'me' for current user) | safe |
| `eventbrite_list_user_organizations` | List orgs the user belongs to | safe |
| `eventbrite_list_user_orgs` | List organizations by user ID | safe |

### Tracking & analytics

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_tracking_beacon` | Get tracking beacon by ID | safe |
| `eventbrite_list_tracking_beacons` | List tracking beacons for an org | safe |
| `eventbrite_create_tracking_beacon` | Create a tracking beacon (GA, Facebook Pixel, etc.) | confirm |

### Webhooks

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_create_webhook` | Create a webhook for org events | confirm |

### Buyer settings

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_update_ticket_buyer_settings` | Update post-purchase redirect, survey settings | confirm |

### Media

| Tool | Description | Risk |
|------|-------------|------|
| `eventbrite_get_media_upload` | Check status of an uploaded media image | safe |
| `eventbrite_retrieve_media` | Get media details by ID | safe |

## Code examples

### Example 1: Create and manage events

```javascript
// Get the user's organizations first
const orgs = await clawlink_call_tool({
  tool: "eventbrite_list_user_organizations",
  parameters: {}
});

// List events for an organization
const events = await clawlink_call_tool({
  tool: "eventbrite_list_organization_events",
  parameters: { organization_id: orgs[0].id }
});

// Create a new event
const newEvent = await clawlink_call_tool({
  tool: "eventbrite_create_event",
  parameters: {
    organization_id: orgs[0].id,
    name: { text: "Tech Conference 2024" },
    start: { utc: "2024-09-15T09:00:00Z" },
    end: { utc: "2024-09-15T17:00:00Z" },
    currency: "USD"
  }
});

// Create a ticket class
const ticket = await clawlink_call_tool({
  tool: "eventbrite_create_ticket_class",
  parameters: {
    event_id: newEvent.id,
    name: "General Admission",
    quantity: 100,
    cost: "USD,2500"
  }
});
```

### Example 2: Manage attendees

```javascript
// List attendees for an event
const attendees = await clawlink_call_tool({
  tool: "eventbrite_list_event_attendees",
  parameters: { event_id: "123456" }
});

// List orders for an event
const orders = await clawlink_call_tool({
  tool: "eventbrite_list_event_orders",
  parameters: { event_id: "123456" }
});

// Get attendees across all organization events
const orgAttendees = await clawlink_call_tool({
  tool: "eventbrite_list_org_attendees",
  parameters: { organization_id: "org123" }
});

// Get a sales report
const salesReport = await clawlink_call_tool({
  tool: "eventbrite_get_sales_report",
  parameters: { event_id: "123456" }
});
```

### Example 3: Set up discounts and access codes

```javascript
// Create a discount
const discount = await clawlink_call_tool({
  tool: "eventbrite_create_discount",
  parameters: {
    event_id: "123456",
    code: "EARLYBIRD20",
    percent_off: "20"
  }
});

// Create an access code
const accessCode = await clawlink_call_tool({
  tool: "eventbrite_create_access_code",
  parameters: {
    event_id: "123456",
    code: "VIP2024"
  }
});
```

### Example 4: Manage venues and organizers

```javascript
// List organization's venues
const venues = await clawlink_call_tool({
  tool: "eventbrite_list_org_venues",
  parameters: { organization_id: "org123" }
});

// Create a venue
const newVenue = await clawlink_call_tool({
  tool: "eventbrite_create_venue",
  parameters: {
    organization_id: "org123",
    name: "Convention Center",
    address: {
      city: "San Francisco",
      region: "CA",
      country: "US"
    }
  }
});

// Create an organizer
const organizer = await clawlink_call_tool({
  tool: "eventbrite_create_organizer",
  parameters: {
    organization_id: "org123",
    name: "Tech Events Inc."
  }
});
```

## Error handling

| Error pattern | Likely cause | Resolution |
|---------------|--------------|------------|
| `Event has pending orders` | Cannot cancel/delete event with existing orders | Wait for orders to complete or cancel them first |
| `Discount not found` | Wrong discount ID or already used | Check discount ID or create a new discount |
| `Invalid ticket group` | Empty ticket_group_ids list | Call list ticket groups first to get valid IDs |
| `No ticket classes` | Event needs at least one ticket before publishing | Create a ticket class before publishing |
| `Venue capacity exceeded` | Trying to create event beyond venue limits | Check venue capacity and adjust event settings |

## Security & Permissions

- ClawLink stores only the OAuth token, never raw API keys
- Device credentials are stored locally in OpenClaw plugin config
- Organization-level operations require appropriate Eventbrite roles

## Troubleshooting

**Tools not showing up after install:**
- Start a fresh OpenClaw chat to reload the plugin catalog
- Call `clawlink_list_integrations` to confirm ClawLink is paired

**Cannot publish event:**
- Event must have a name, description, organizer, and at least one ticket
- Check all required fields are populated before publishing

**Cancel/delete event fails:**
- Event must have no pending or completed orders
- Consider unpublishing instead of deleting

---

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=eventbrite-events) — your OpenClaw integration hub for Eventbrite.