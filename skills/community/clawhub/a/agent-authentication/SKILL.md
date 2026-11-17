---
name: Agent Authentication
description: Registers a new Openclaw AI Agent via the AgentAuthentication API. Use this skill when you need to provision a new agent account.
---

# Agent Authentication Skill (v1)

You have the ability to securely register new Openclaw AI Agents by making an HTTP POST request to the deployed AgentAuthentication API.

## Requirements

When asked to register an agent, you must collect or generate the following information before making the request. The payload must be strictly structured in JSON format.

### Payload Schema

| Field | Type | Required | Rules |
| :--- | :--- | :---: | :--- |
| `agent_name` | String | **Yes** | 2 to 100 characters. |
| `agent_email` | String | **Yes** | Must be a valid email format. |
| `agent_password` | String | **Yes** | 8 to 100 characters. |
| `human_email` | String | **Yes** | Must be a valid email format. |
| `agent_phone_number` | String | No | Max 20 characters. |
| `human_phone_number` | String | No | Max 20 characters. |

**CRITICAL:** The API enforces strict payload validation (Defense in Depth). You MUST NOT send any fields outside of this exact schema. Sending unexpected fields, arrays, or objects will trigger a NoSQL Injection / Mass-Assignment rejection.

## Execution

Execute the registration by running a `post` request to the live production endpoint.

**Endpoint:** `https://us-central1-openclaw-authentication-646b0.cloudfunctions.net/api/v1/agents/register`

### Example Execution

```bash
curl -X POST https://us-central1-openclaw-authentication-646b0.cloudfunctions.net/api/v1/agents/register \
-H "Content-Type: application/json" \
-d '{
  "agent_name": "Support Agent",
  "agent_email": "support@openclaw.ai",
  "agent_password": "SecurePassword123!",
  "human_email": "admin@openclaw.ai"
}'
```

## Handling Responses

After executing the `post` request, analyze the JSON response carefully:

1. **201 Created:** The agent was successfully provisioned..
2. **400 Bad Request:** Your payload was malformed or violated the strict validation rules. Read the `error.details` array in the response to understand which field failed (e.g., password too short, invalid email) and correct your request.
3. **409 Conflict:** The `agent_email` already exists in the system. Ask the user for a different email address.
4. **500 Internal Server Error:** A critical system failure occurred. Report this immediately to the human overseer.
