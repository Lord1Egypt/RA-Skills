---
name: apaleo
description: Apaleo hotel property management API integration with managed OAuth. Manage properties, units, unit groups, and unit attributes. Use this skill when users want to list hotel properties, create rooms and units, check availability, or manage property inventory in Apaleo.
---

# Apaleo

![Apaleo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/apaleo.png)

Apaleo is a cloud-based hotel property management system. This integration lets you manage properties, rooms (units), unit groups, and unit attributes through the Apaleo API via ClawLink's hosted OAuth flow -- no API keys to configure manually.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Apaleo |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Apaleo |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────>│   ClawLink   │────>│   Apaleo API     │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

1. **List all properties** -- `apaleo_get_a_properties_list`
2. **Get units for a property** -- `apaleo_get_a_units_list`
3. **Create a new unit** -- `apaleo_create_a_unit`

## Authentication

ClawLink handles OAuth automatically. When you connect Apaleo through the dashboard, ClawLink obtains and refreshes tokens on your behalf. No API keys or manual token management required.

Connect at: https://claw-link.dev/dashboard?add=apaleo

## Connection Management

- **List connections**: `clawlink_list_integrations`
- **Verify connection**: `clawlink_list_tools --integration apaleo`
- **Reconnect**: Visit https://claw-link.dev/dashboard?add=apaleo

## Security & Permissions

Read operations (listing properties, units, attributes) require authorization but no specific scopes. Write and delete operations require scopes like `properties.manage`, `units.create`, or `setup.manage`. The agent will ask for confirmation before executing any write or delete action.

## Tool Reference

### Property Operations

| Tool | Description | Mode |
|------|-------------|------|
| `apaleo_get_a_properties_list` | Get the list of properties | Read |
| `apaleo_get_a_property` | Get a property by id | Read |
| `apaleo_creates_a_property` | Create a new property | Write |
| `apaleo_archive_a_property` | Archive an existing live property | Write |
| `apaleo_clones_a_property` | Clone a specific property with inventory and rate plans | Write |
| `apaleo_move_property_to_live` | Move an existing test property to live | Write |
| `apaleo_reset_property_data` | Delete transactional data for a test property | Write |
| `apaleo_check_if_a_property_exists` | Check if a property exists by id | Read |
| `apaleo_return_total_count_of_properties` | Return total count of properties | Read |
| `apaleo_returns_a_list_of_supported_countries` | Returns ISO country codes for property creation | Read |

### Unit Operations

| Tool | Description | Mode |
|------|-------------|------|
| `apaleo_get_a_units_list` | Get the list of units | Read |
| `apaleo_get_a_unit` | Get a unit by id | Read |
| `apaleo_create_a_unit` | Create a new unit | Write |
| `apaleo_create_multiple_units` | Create multiple units following a naming rule | Write |
| `apaleo_delete_a_unit` | Delete a unit | Write |
| `apaleo_check_if_a_unit_exists` | Check if a unit exists by id | Read |
| `apaleo_returns_number_of_units` | Returns number of units matching filter criteria | Read |

### Unit Group Operations

| Tool | Description | Mode |
|------|-------------|------|
| `apaleo_list_unit_groups` | Get the list of unit groups | Read |
| `apaleo_get_a_unit_group` | Get a unit group by id | Read |
| `apaleo_create_a_unit_group` | Create a new unit group | Write |
| `apaleo_replace_a_unit_group` | Modify a unit group | Write |
| `apaleo_delete_a_unit_group` | Delete a unit group | Write |
| `apaleo_check_if_a_unit_group_exists` | Check if a unit group exists by id | Read |
| `apaleo_returns_number_of_unit_groups` | Returns number of unit groups matching filters | Read |

### Unit Attribute Operations

| Tool | Description | Mode |
|------|-------------|------|
| `apaleo_get_unit_attribute_list` | Get unit attribute list | Read |
| `apaleo_get_unit_attribute_by_id` | Get unit attribute by id | Read |
| `apaleo_create_a_unit_attribute` | Create a new unit attribute | Write |
| `apaleo_deletes_unit_attribute` | Delete a unit attribute | Write |
| `apaleo_check_if_a_unit_attribute_exists` | Check if a unit attribute exists | Read |

## Code Examples

**List all properties**
```json
{
  "tool": "apaleo_get_a_properties_list",
  "args": {}
}
```

**Get a specific unit**
```json
{
  "tool": "apaleo_get_a_unit",
  "args": { "unit_id": "U-001" }
}
```

**Create a new unit**
```json
{
  "tool": "apaleo_create_a_unit",
  "args": {
    "property_id": "P-001",
    "name": "Room 101",
    "unit_group_id": "UG-001"
  }
}
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm `apaleo` is connected.
2. Call `clawlink_list_tools --integration apaleo` to see the live catalog.
3. Use `apaleo_get_a_properties_list` to find your property IDs.
4. Use unit and attribute tools to explore and manage inventory.

## Execution Workflow

```
Read path:  User asks "Show me all properties"  -> apaleo_get_a_properties_list
Write path: User asks "Create a new room"       -> Confirm -> apaleo_create_a_unit
Delete path: User asks "Remove unit X"          -> Confirm -> apaleo_delete_a_unit
```

## Notes

- Properties have two statuses: Test and Live. Only Test properties can have their data reset.
- Some operations (clone, archive, move to live) require `properties.manage` or `setup.manage` scopes.
- Unit deletion is permanent and cannot be undone.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The Apaleo integration is not connected |
| Missing connection | Authenticate via https://claw-link.dev/dashboard?add=apaleo |
| 403 Forbidden | Missing required scope for the operation |
| 404 Not Found | Property, unit, or unit group ID does not exist |

## Troubleshooting

### Tools Not Visible
Run `clawlink_list_tools --integration apaleo` to confirm the connection is active and tools are loaded.

### Invalid Tool Call
Verify you are using the correct IDs (property_id, unit_id, unit_group_id). Use the list/read tools first to discover valid identifiers.

## Resources

- Apaleo API Docs: https://apaleo.com/api/
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apaleo
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apaleo)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
