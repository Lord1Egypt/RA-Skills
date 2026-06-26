---
name: dynamics-365-crm
description: Work with Microsoft Dynamics 365 CRM records, accounts, contacts, leads, opportunities, and activities - powered by ClawLink.
---

# Dynamics 365

![Dynamics 365](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/dynamics-365.svg)

Work with Dynamics 365 from chat — manage CRM records, accounts, contacts, leads, opportunities, and activities.

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dynamics-365-crm), an integration hub for OpenClaw that handles hosted connection flows and credentials so you don't need to configure Dynamics 365 API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Dynamics 365 |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Dynamics 365 |

## Connection flow

```
User → ClawLink OAuth → Microsoft Dynamics 365 account
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

**Step 3** — Connect Dynamics 365:
Open [claw-link.dev/dashboard?add=dynamics-365](https://claw-link.dev/dashboard?add=dynamics-365), complete the OAuth flow, then confirm.

*App-specific connection GIF coming soon*

**Step 4** — Verify and discover:
```javascript
// 1. Verify Dynamics 365 is connected
clawlink_list_integrations()

// 2. List available tools
clawlink_list_tools({ integration: "dynamics-365" })

// 3. Search tools if needed
clawlink_search_tools({ query: "lead", integration: "dynamics-365" })
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
│         Microsoft Dynamics 365 Web API                  │
│              (user's CRM account)                       │
└─────────────────────────────────────────────────────────┘
```

## Tool reference

### Create operations

| Tool | Description | Risk |
|------|-------------|------|
| `dynamics365_dynamicscrm_create_account` | Create a new account entity record | confirm |
| `dynamics365_dynamicscrm_create_case` | Create a new case (incident) entity record | confirm |
| `dynamics365_dynamicscrm_create_contact` | Create a new contact entity record | confirm |
| `dynamics365_dynamicscrm_create_invoice` | Create a new invoice entity record | confirm |
| `dynamics365_dynamicscrm_create_lead` | Create a new lead entity record | confirm |
| `dynamics365_dynamicscrm_create_opportunity` | Create a new opportunity entity record | confirm |
| `dynamics365_dynamicscrm_create_sales_order` | Create a new sales order entity record | confirm |

### Read operations

| Tool | Description | Risk |
|------|-------------|------|
| `dynamics365_dynamicscrm_get_a_invoice` | Get a specific invoice by ID | safe |
| `dynamics365_dynamicscrm_get_a_lead` | Get a specific lead by ID | safe |
| `dynamics365_dynamicscrm_get_all_leads` | Get all leads from the CRM | safe |
| `dynamics365_get_all_invoices_action` | Get all invoices | safe |

### Update operations

| Tool | Description | Risk |
|------|-------------|------|
| `dynamics365_dynamicscrm_update_case` | Update an existing case (incident) | confirm |
| `dynamics365_dynamicscrm_update_invoice` | Update an existing invoice | confirm |
| `dynamics365_dynamicscrm_update_lead` | Update an existing lead | confirm |
| `dynamics365_dynamicscrm_update_opportunity` | Update an existing opportunity | confirm |
| `dynamics365_dynamicscrm_update_sales_order` | Update an existing sales order | confirm |

## Code examples

### Example 1: Create and manage leads

```javascript
// Create a new lead
const lead = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_create_lead",
  parameters: {
    subject: "New product inquiry",
    firstname: "Jane",
    lastname: "Doe",
    emailaddress1: "jane.doe@example.com",
    companyname: "Acme Corp"
  }
});

// Get a specific lead
const specificLead = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_get_a_lead",
  parameters: { lead_id: "abc123" }
});

// Get all leads
const allLeads = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_get_all_leads",
  parameters: {}
});

// Update a lead
await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_update_lead",
  parameters: {
    lead_id: "abc123",
    subject: "Updated subject line",
    telephone1: "+1-555-0100"
  }
});
```

### Example 2: Manage accounts and contacts

```javascript
// Create an account
const account = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_create_account",
  parameters: {
    name: "Acme Corporation",
    telephone1: "+1-555-0100",
    address1_city: "Seattle"
  }
});

// Create a contact
const contact = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_create_contact",
  parameters: {
    firstname: "John",
    lastname: "Smith",
    emailaddress1: "john.smith@acme.com",
    parentcustomerid_account: account.id
  }
});
```

### Example 3: Manage opportunities and sales orders

```javascript
// Create an opportunity
const opportunity = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_create_opportunity",
  parameters: {
    name: "Enterprise deal - Acme Corp",
    estimatedvalue: 50000,
    estimatedclosedate: "2024-06-30"
  }
});

// Update an opportunity
await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_update_opportunity",
  parameters: {
    opportunity_id: "opportunity123",
    estimatedvalue: 75000,
    description: "Expanded scope"
  }
});

// Create a sales order
const order = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_create_sales_order",
  parameters: {
    name: "SO-001",
    customerid_account: "account123"
  }
});
```

### Example 4: Handle cases and invoices

```javascript
// Create a case
const case = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_create_case",
  parameters: {
    title: "Technical support request",
    customerid_account: "account123",
    caseorigincode: "Web"
  }
});

// Update a case
await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_update_case",
  parameters: {
    incident_id: "case123",
    description: "Issue resolved"
  }
});

// Get all invoices
const invoices = await clawlink_call_tool({
  tool: "dynamics365_get_all_invoices_action",
  parameters: {}
});

// Get a specific invoice
const invoice = await clawlink_call_tool({
  tool: "dynamics365_dynamicscrm_get_a_invoice",
  parameters: { invoice_id: "inv123" }
});
```

## Error handling

| Error pattern | Likely cause | Resolution |
|---------------|--------------|------------|
| `estimatedclosedate required` | Server-side requirement for opportunity | Include `estimatedclosedate` when creating opportunities |
| `transactioncurrency required` | Server-side requirement for some entities | Ensure transaction currency is set at server level |
| `entity not found` | Wrong entity ID or type | Verify entity ID format and type |
| `permission denied` | Missing Dynamics 365 permissions | User may need to reconnect with proper CRM roles |

## Security & Permissions

- ClawLink stores only the OAuth token for Dynamics 365
- Device credentials are stored locally in OpenClaw plugin config
- CRM permissions depend on the user's assigned Dynamics 365 roles
- Some entities may require specific field-level permissions

## Troubleshooting

**Tools not showing up after install:**
- Start a fresh OpenClaw chat to reload the plugin catalog
- Call `clawlink_list_integrations` to confirm ClawLink is paired

**"Permission denied" errors:**
- User needs appropriate Dynamics 365 roles assigned in Azure AD
- Some CRM operations require specific security roles

**Opportunity/invoice creation fails:**
- Some CRM configurations enforce fields not exposed in the schema
- Check `estimatedclosedate` for opportunities
- Check transaction currency requirements for invoicing

---

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dynamics-365-crm) — your OpenClaw integration hub for Dynamics 365.