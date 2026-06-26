---
name: cleanup-properties
description: "Archive or delete unused custom properties across all HubSpot object types (contacts, companies, deals). Identifies Salesforce sync properties, test/temp properties, and obsolete form fields."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: ongoing-maintenance
---

# Cleanup Properties

Remove or archive unused custom properties. Property bloat slows down forms, confuses users, and makes data mapping harder.

## Prerequisites

- HubSpot API token in `.env`
- Python with `hubspot-api-client` installed via `uv`

## Step-by-Step Instructions

### Stage 1: Before — Inventory All Custom Properties

Pull properties for each object type:

```python
from hubspot import HubSpot

api_client = HubSpot(access_token=os.getenv("HUBSPOT_API_TOKEN"))

for obj_type in ["contacts", "companies", "deals"]:
    props = api_client.crm.properties.core_api.get_all(
        object_type=obj_type
    )
    custom_props = [p for p in props.results if not p.hubspot_defined]
```

For each custom property, record: name, label, object type, type, group, number of records with a value (requires search queries), whether it is used in any form/workflow/list.

### Stage 2: Execute — Identify Candidates for Deletion

**Safe to delete:**
- Properties with zero populated records and not used in any form, workflow, or list
- Properties with names containing "test", "temp", "old_", "copy_of"
- Properties created by deactivated integrations

**Handle with care:**
- **Salesforce sync properties** (`hs_salesforce_*` prefix or mapped in sync settings) — do not delete without coordinating with the Salesforce admin
- **Form fields** — check if the property is used on any active form before deleting
- **Workflow dependencies** — check if any workflow reads or sets this property
- **Calculated properties** — check if other calculated properties reference this one

**Archive instead of delete** when:
- The property has historical data that might be needed for reporting
- You are unsure whether anything depends on it

### Stage 3: After — Delete or Archive

1. Archive properties first (HubSpot supports property archiving).
2. Wait 30 days, then delete archived properties that caused no issues.
3. Document all changes in a cleanup log.

### Stage 4: Rollback

- Archived properties can be unarchived at any time.
- Deleted properties cannot be restored. The property definition and all associated data are permanently lost.
- Always archive before deleting to provide a safety window.

## Tips

- Run this quarterly as part of the database cleanup routine.
- Establish a property naming convention going forward (e.g., `team_purpose_detail`).
- Limit who can create custom properties to prevent sprawl.
- HubSpot has a property limit per object type — cleanup prevents hitting it.
