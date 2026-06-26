# Directus Flows & Automation

## Table of Contents
1. [Flows Overview](#flows-overview)
2. [Trigger Types](#trigger-types)
3. [Operations](#operations)
4. [The Data Chain](#the-data-chain)
5. [AI Content Generation](#ai-content-generation)
6. [Scheduled Content Publishing](#scheduled-content-publishing)
7. [Deployment Webhooks](#deployment-webhooks)
8. [Content Approval Workflows](#content-approval-workflows)
9. [External Service Integration](#external-service-integration)
10. [Managing Flows via API](#managing-flows-via-api)

---

## Flows Overview

Directus Flows (also called Directus Automate) provide a no-code visual interface for building event-driven automations. A Flow consists of a **trigger** (what starts it) and one or more **operations** (what it does), connected in a chain.

Flows are configured in the Data Studio under **Settings → Flows**.

Key concepts:
- **Triggers** start the flow — they can be events, schedules, webhooks, or manual actions
- **Operations** are individual steps — reading data, making API calls, sending emails, running code, etc.
- **Data Chain** — each operation's output is available to subsequent operations via template syntax `{{ $trigger.body }}`, `{{ operationName.result }}`
- **Permissions** — flows run with configurable permissions: `$public`, `$trigger` (same as triggering user), `$full` (admin), or a specific role UUID

---

## Trigger Types

### Event Hook
Fires when something happens in Directus (item created, updated, deleted, etc.).

```
Type: Event Hook
Scope: items.create, items.update, items.delete
Collections: posts, pages (select which collections trigger the flow)
Response: Action (Non-Blocking) — runs in background
         Filter (Blocking) — can modify or reject the operation
```

**Action (Non-Blocking)** — the triggering operation completes immediately; the flow runs asynchronously. Use for notifications, logging, external sync.

**Filter (Blocking)** — the flow runs before the operation completes and can modify the payload or throw an error to cancel it. Use for validation, data enrichment before save.

### Schedule (CRON)
Fires on a time-based schedule using CRON syntax.
```
Type: Schedule (CRON)
Interval examples:
  */5 * * * *     — every 5 minutes
  0 * * * *       — every hour
  0 9 * * 1-5     — 9 AM weekdays
  0 0 * * *       — midnight daily
  0 0 1 * *       — first of each month
```

### Webhook
Fires when an external service POSTs to the flow's webhook URL.
```
Type: Webhook
Method: GET or POST
Async: true/false (respond immediately or wait for flow to complete)
```

The webhook URL is: `{DIRECTUS_URL}/flows/trigger/{flow-id}`

### Manual
Triggered by a user clicking a button in the Data Studio on a specific item.
```
Type: Manual Trigger
Collections: posts (which collections show the button)
```

The trigger payload includes `{{ $trigger.body.keys }}` — an array of selected item IDs.

### Another Flow
Fires when called by another flow's "Trigger Flow" operation. Used for modular, reusable flows.

---

## Operations

### Read Data
Reads items from a collection.
```
Collection: posts
Permissions: Full Access / From Trigger / From Role
Query: filter, fields, sort, limit
Result key: {{ read_data_operation_name }}
```

### Create Data
Creates a new item in a collection.

### Update Data
Updates items by ID or filter.
- Check "Emit Events" if you want this update to trigger other event-based flows.

### Delete Data
Deletes items by ID or filter.

### Web Request
Makes an HTTP request to an external service.
```
Method: GET, POST, PUT, PATCH, DELETE
URL: https://api.example.com/endpoint
Headers: { "Authorization": "Bearer {{$env.API_KEY}}", "Content-Type": "application/json" }
Body: JSON with template variables
```

### Send Email
Sends an email using Directus's configured email transport.
```
To: recipient@example.com (or {{ $trigger.payload.user_email }})
Subject: New post published
Body: HTML template with variables
```

### Send Notification
Sends an in-app notification to a Directus user.

### Run Script
Executes custom JavaScript. Has access to the data chain via the `data` parameter:
```javascript
module.exports = async function(data) {
  const triggerData = data.$trigger;
  const previousStep = data.previous_operation_key;

  // Do processing
  const result = { processed: true, count: 42 };

  return result;  // Available as {{ this_operation_key }}
}
```

### Transform Payload
Transforms data using a JSON template with Liquid-style syntax.

### Condition
Branches the flow based on a condition. If true, runs the "success" branch; if false, runs the "reject" branch.
```
Rule: {{ $trigger.payload.status }} == "published"
```

### Log to Console
Logs data to the server console (useful for debugging).

### Trigger Flow
Calls another flow, enabling modular/reusable flow patterns.

### Sleep
Pauses execution for a specified duration (in milliseconds).

---

## The Data Chain

Every trigger and operation adds data to the flow's data chain. Access data from any previous step using template syntax:

```
{{ $trigger }}                          — Full trigger payload
{{ $trigger.body }}                     — Request body (webhooks)
{{ $trigger.body.keys[0] }}             — First selected item ID (manual triggers)
{{ $trigger.payload }}                  — The item data (event hooks)
{{ $trigger.payload.title }}            — Specific field from trigger payload
{{ $accountability.user }}              — ID of user who triggered

{{ operation_key }}                     — Full output of a named operation
{{ operation_key.field_name }}          — Specific field from operation output
{{ operation_key[0].title }}            — Array item access

{{ $env.MY_SECRET }}                    — Environment variable
{{ $now }}                              — Current ISO timestamp
{{ $last }}                             — Output of the immediately previous operation
```

---

## AI Content Generation

### Generate Social Posts with OpenAI

**Flow setup:**
1. **Trigger**: Manual, on the `posts` collection
2. **Read Data** (operation key: `article`): Read the triggered item from `posts` with full access
   - Collection: `posts`
   - Key: `{{ $trigger.body.keys[0] }}`
3. **Web Request** (key: `generate`): POST to OpenAI
   - URL: `https://api.openai.com/v1/chat/completions`
   - Headers: `{ "Authorization": "Bearer {{ $env.OPENAI_API_KEY }}", "Content-Type": "application/json" }`
   - Body:
   ```json
   {
     "model": "gpt-4",
     "messages": [
       {
         "role": "system",
         "content": "You are a social media manager. Write compelling promotional posts based on the content provided."
       },
       {
         "role": "user",
         "content": "Write a Twitter post for: {{ article.title }}"
       }
     ]
   }
   ```
4. **Update Data**: Save the result back to the post
   - Collection: `posts`
   - Key: `{{ $trigger.body.keys[0] }}`
   - Payload: `{ "social_output": "{{ generate.data.choices[0].message.content }}" }`

### Generate SEO Metadata

Same pattern, but the prompt asks for JSON output with `meta_title`, `meta_description`, and `keywords`. Use a **Run Script** operation to parse the JSON and then **Update Data** to save each field.

### Generate Images with DALL·E

**Web Request** to `https://api.openai.com/v1/images/generations`:
```json
{
  "model": "dall-e-3",
  "prompt": "A professional blog header image for an article about {{ article.title }}",
  "n": 1,
  "size": "1792x1024"
}
```

Then use another **Web Request** or **Run Script** to download the generated image URL and import it into Directus Files.

### Auto-Translate Content

Use a flow triggered on `items.create` or `items.update` for your content collection, then:
1. Read the source content
2. Web Request to a translation API (DeepL, Google Translate, or an LLM)
3. Create/Update items in the translations junction collection

---

## Scheduled Content Publishing

For SSG sites that need to publish content at a scheduled time:

### Flow: Publish Scheduled Articles

1. **Trigger**: Schedule (CRON) — e.g., `*/15 * * * *` (every 15 minutes)
2. **Update Data**: Update items in `posts` where:
   - Filter: `status` equals `scheduled` AND `date_published` is less than or equal to `$NOW`
   - Payload: `{ "status": "published" }`
   - Check "Emit Events" so downstream flows (like deploy hooks) are triggered
3. **Condition**: Check if any items were updated
4. **Web Request**: POST to your hosting deploy hook URL

### For SSR/Dynamic Sites
No flow needed — just filter in your frontend query:
```typescript
const posts = await client.request(readItems('posts', {
  filter: {
    _and: [
      { status: { _eq: 'published' } },
      { date_published: { _lte: '$NOW' } },
    ],
  },
}));
```

---

## Deployment Webhooks

### Trigger Rebuild on Content Change

1. **Trigger**: Event Hook, `items.create` / `items.update` on content collections, Action (Non-Blocking)
2. **Condition**: Check `{{ $trigger.payload.status }}` equals `published`
3. **Web Request**: POST to deploy hook

**Netlify:**
```
POST https://api.netlify.com/build_hooks/{your-hook-id}
```

**Vercel:**
```
POST https://api.vercel.com/v1/integrations/deploy/{your-hook-id}/{your-project-id}
```

**Cloudflare Pages:**
```
POST https://api.cloudflare.com/client/v4/pages/webhooks/deploy_hooks/{your-hook-id}
```

---

## Content Approval Workflows

### Multi-Stage Review

1. **Trigger**: Event Hook on `items.update` for `posts` (Filter/Blocking)
2. **Condition**: Status changed to `in_review`
3. **Read Data**: Get the editor/reviewer assigned to this post
4. **Send Email**: Notify the reviewer with a link to the item
5. **Send Notification**: Also send an in-app notification

### Prevent Publishing Without Approval
Use a Filter (Blocking) trigger:

1. **Trigger**: Event Hook on `items.update`, Filter (Blocking)
2. **Condition**: Status is being changed to `published`
3. **Read Data**: Check if the item has an `approved_by` field set
4. **Condition**: If `approved_by` is null, reject the operation (return an error)

---

## External Service Integration

### Sync to External Systems
When content is published, sync to Algolia, Elasticsearch, or a custom service:

1. **Trigger**: Event Hook on `items.create` / `items.update`
2. **Condition**: Status is `published`
3. **Transform Payload**: Shape data for the external API
4. **Web Request**: POST/PUT to external service

### Inbound Webhook Processing
Accept data from external services:

1. **Trigger**: Webhook (POST)
2. **Run Script**: Validate and transform incoming data
3. **Create Data**: Save to a Directus collection
4. **Send Notification**: Alert relevant users

---

## Managing Flows via API

Flows can also be managed programmatically:

```typescript
import { readFlows, readFlow, createFlow, updateFlow, deleteFlow } from '@directus/sdk';

// List all flows
const flows = await client.request(readFlows());

// Read a specific flow
const flow = await client.request(readFlow('flow-uuid'));

// Trigger a webhook flow
await fetch('https://directus.example.com/flows/trigger/flow-uuid', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' }),
});
```
