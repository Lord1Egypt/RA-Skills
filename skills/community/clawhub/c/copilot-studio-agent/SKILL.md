# Skill: Create Copilot Studio Agents from Scratch

Create agents in Microsoft Copilot Studio using the web app. This skill guides you through the complete agent creation process based on Microsoft Learn documentation.

## Quick Reference

**Documentation:** https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-first-bot

**Key Limits:**
- Agent name: max 42 characters (no angle brackets `<` `>`)
- Description: max 1,024 characters
- Instructions: max 8,000 characters
- Icon: PNG format, <72KB, max 192×192 pixels

## Steps to Create an Agent

### 1. Start at Copilot Studio
1. Sign in to https://copilotstudio.microsoft.com/
2. Switch to the desired environment (if needed)
3. Optionally configure: primary language, solution, schema name

### 2. Create the Agent (3 Options)

**Option A - Natural Language:**
- On Home or Agents page, enter a brief description of what you want the agent to do (up to 1,024 chars)
- AI generates name, description, instructions, triggers, channels, knowledge sources, tools

**Option B - Create from Scratch:**
- Home page: Select **Create an agent** under "Start building from scratch"
- OR Agents page: Select **Create blank agent**

**Option C - Advanced Create:**
- Agents page: Select dropdown next to **Create blank agent** → **Advanced create**
- Configure primary language, solution, and schema name before creating

### 3. Configure Basic Features

After provisioning, configure:

| Feature | Description |
|---------|-------------|
| **Primary AI Model** | [Change agent model](authoring-select-agent-model) |
| **Triggers** | Define what activates the agent ([About triggers](authoring-triggers-about)) |
| **Knowledge Sources** | Add enterprise data, websites, SharePoint, Dataverse ([Knowledge](knowledge-copilot-studio)) |
| **Tools** | Add Power Automate flows, connectors ([Add tools](add-tools-custom-agent)) |
| **Other Agents** | Add sub-agents ([Add agents](authoring-add-other-agents)) |
| **Topics** | Define conversation flows ([Create topics](authoring-create-edit-topics)) |
| **Starter Prompts** | Add suggested prompts for users |

### 4. Edit Agent Basics

**Rename & Edit Description:**
1. Go to **Overview** page → **Details** section
2. Select **Edit** → enter name/description → **Save**

**Edit Instructions:**
1. **Overview** page → **Instructions** section
2. Select **Edit** → refine instructions → **Save**

**Change Icon:**
1. Select agent icon in top bar → **Change icon**
2. Choose PNG image → **Save**

**Change Language/Solution:**
1. Select gear icon in description box
2. Under Agent settings: select primary language
3. Advanced settings: choose solution and schema name
4. **Update**

⚠️ **Note:** Cannot change primary language after creation. Can change region or add secondary languages.

### 5. Test & Publish

1. [Test your agent](authoring-test-bot)
2. Improve based on testing
3. [Publish](publication-fundamentals-publish-channels) to channels

## Topic Types

| Node Type | Purpose |
|-----------|---------|
| **Message** | Send a message to user |
| **Question** | Ask user for input |
| **Adaptive Card** | Interactive cards with buttons/inputs |
| **Condition** | Branch conversation based on logic |
| **Variable** | Set, parse, or clear variables |
| **Topic Management** | Redirect, transfer, or end conversation |
| **Tool** | Call Power Automate flows, connectors |
| **Advanced** | Generative answers, HTTP requests, events |

## Topic Creation (Web App)

1. Go to **Topics** page → close test panel
2. **Add a topic** → **From blank**
3. Add trigger phrases (5-10 recommended)
   - Use **Add** icon or upload a file
   - Each phrase on separate line
4. Select **Details** → add name, display name, description
5. **Save**

## Knowledge Sources

| Source | Description |
|--------|-------------|
| **Public Website** | Bing search on provided URLs (max 25 in generative mode) |
| **Documents** | Uploaded to Dataverse |
| **SharePoint** | Connect via URL |
| **Dataverse** | Query tables in environment |
| **Enterprise Data** | Microsoft Search via connectors |

## Delete an Agent

**Web App:**
1. Go to **Agents** page
2. Select agent → **…** menu → **Delete**
3. Enter agent name to confirm

## Authentication

- Agents automatically use Microsoft Entra ID (Azure AD) authentication
- Can configure SSO so users don't need manual sign-in
- See: [Configure SSO](configure-sso)

## Event Triggers (Advanced)

Event triggers allow agents to act autonomously in response to external events—without user input.

### Requirements
- Agent must have **generative orchestration** enabled
- Can impact billing (see [Copilot Credits billing rates](requirements-messages-management))

### How Event Triggers Work

1. **Event occurs** → External system (SharePoint, Planner, etc.) triggers an event
2. **Trigger sends payload** → JSON/message containing event info + instructions
3. **Agent executes** → Agent reads payload and calls appropriate actions/topics

### Available Event Triggers

| Trigger | Source | Example |
|---------|--------|---------|
| When a row is added/modified/deleted | Dataverse | New record in table |
| When a file is created | OneDrive | New file uploaded |
| When an item is created | SharePoint | New list item |
| When a task is completed | Microsoft Planner | Task marked complete |
| Recurrence | Scheduled | Time-based trigger (every X minutes) |

### Add an Event Trigger

1. Go to **Overview** → **Triggers** section
2. Select **Add trigger**
3. Choose the desired trigger
4. Authenticate (uses agent maker's credentials)
5. Configure parameters and define trigger payload
6. Define actions/topics for the agent to call in response

### Trigger Payload

The payload is a JSON/plain text message sent to the agent containing:
- Event information (data from the source)
- Instructions on how to act

**Default payload example:** *"Use content from `Body`"*

**Custom payload example:** *"Summarize the changes and send to the user"*

### Agent Instructions vs Payload Instructions

| Approach | Use Case |
|----------|----------|
| **Agent Instructions** | General behavior, simple agents with few triggers |
| **Payload Instructions** | Complex agents with multiple triggers/goals |

### Test a Trigger

1. Run the triggering event (e.g., create a Planner task)
2. On **Overview** page, select **Test trigger icon** beside the trigger
3. Choose the instance → **Start testing**
4. Use **Activity Map** to see agent's reaction

⚠️ **Before publishing:** Agent won't react automatically until published.

### Modify a Trigger

1. **Overview** → locate trigger → **…** → **Edit in Power Automate**
2. Modify parameters, payload content, variables
3. Save changes in Power Automate

### Data Protection & Security

- Event triggers use **agent maker's credentials** only
- Users may access data using author's authorization
- Review [data protection best practices](authoring-triggers-about#data-protection-best-practices) before publishing

### Billing Note

Each trigger activation counts as a message toward Copilot Credits. A recurrence trigger running every 10 minutes = ~4,320 messages/month.

---

## Power Automate Integration (Tools)

Agents can call Power Automate cloud flows as **tools** to perform actions and get data.

### Requirements for Agent Flows

| Requirement | Details |
|------------|---------|
| **Trigger** | Must use `When an agent calls the flow` |
| **Response** | Must include `Respond to the agent` action |
| **Mode** | Real-time (Async toggle = Off) |
| **Timeout** | Must respond within 100 seconds |
| **Flow Run Limit** | Up to 30 days (after response) |

### Create an Agent Flow

**Option 1: From Topic**
1. Go to **Topics** → open your topic
2. Select **Add node** → **Add a tool**
3. **Basic tools** tab → **New Agent flow**
4. Template opens with required trigger + response action
5. **Publish** → **Go back to agent**
6. Action node added to topic → **Save**

**Option 2: From Overview**
1. **Overview** → **Tools** section → **Add tool**
2. Select **Agent flow** → create new or select existing

### Configure Flow Inputs

In the `When an agent calls the flow` trigger, add input parameters:

| Parameter | Type | Example |
|-----------|------|---------|
| City | Text | "Seattle" |
| ZIP code | Number | 98101 |
| Date | DateTime | "2024-01-15" |

### Configure Flow Outputs

In `Respond to the agent` action, define output parameters:

| Output Parameter | Type | Variable Name |
|-----------------|------|---------------|
| day_summary | Text | Day Summary |
| location | Text | Location |
| chance_of_rain | Number | Day Rain Chance |

### Use Flow in Topic

1. In topic authoring canvas, add **Tool** node
2. Select the flow
3. Map inputs (from user questions or variables)
4. Use outputs in subsequent nodes

### Modify Existing Flow for Agent Use

1. Open flow in Power Automate
2. Replace trigger with `When an agent calls the flow`
3. Add `Respond to the agent` action
4. Configure inputs/outputs as needed
5. Save and test

### Speed Up Flow Execution

- Use **Express Mode** for faster agent flow execution
- Optimize queries and logic
- Keep typical runs under 100 seconds
- Move long-running actions after `Respond to Copilot` action

### Connection Management

| Auth Type | Description |
|-----------|-------------|
| **Maker credentials** | Default - uses author's account |
| **User credentials** | Users run with their own permissions (generative orchestration) |

For user credentials: Configure flow's "Run-only permissions" to **Provided by run-only user**.

⚠️ **CMK Environments:** Cloud flows can't run with customer credentials. Use specific connections instead.

---

## Publishing with Triggers

### Pre-Publish Warning

When publishing an agent with event triggers, you'll see a warning about author credentials. Users may access data using the agent maker's authorization.

### After Publishing

- Agent reacts automatically when triggers activate
- Monitor via **Activity** page
- Each trigger event creates a log entry

### Test Mode vs Published

| Mode | Trigger Behavior |
|------|-------------------|
| **Test** | Manual activation required |
| **Published** | Automatic activation on events |

---

## Related Docs

- [Quickstart: Create and deploy an agent](fundamentals-get-started)
- [Build initial agent training](https://learn.microsoft.com/en-us/training/modules/create-copilots-copilot-studio/)
- [FAQ - Agent creation](faqs-agent-creation)
- [Event triggers overview](authoring-triggers-about)
- [Agent flow express mode](agent-flow-express-mode)

## Related Docs

- [Quickstart: Create and deploy an agent](fundamentals-get-started)
- [Build initial agent training](https://learn.microsoft.com/en-us/training/modules/create-copilots-copilot-studio/)
- [FAQ - Agent creation](faqs-agent-creation)
