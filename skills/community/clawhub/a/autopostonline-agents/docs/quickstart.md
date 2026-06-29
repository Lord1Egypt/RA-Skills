# Quickstart

## 1. Subscribe

Go to:

```text
https://autopostonline.com/agents/
```

Subscribe to Agent Unlimited.

## 2. Connect the owner account

Open:

```text
https://app.autopostonline.com
```

Create or log in to the AutoPostOnline account.

## 3. Connect social channels

The owner connects the social accounts the agent is allowed to use.

The agent should not receive social passwords.

## 4. Create an API key

Create an AutoPostOnline API key.

This is the key the autonomous agent will use.

## 5. Configure the agent

```bash
export POSTIZ_API_URL="https://app.autopostonline.com/api"
export POSTIZ_API_KEY="your_api_key"
```

## 6. Test integrations

```bash
curl -sS \
  -H "Authorization: Bearer $POSTIZ_API_KEY" \
  "$POSTIZ_API_URL/public/v1/integrations"
```

Fallback:

```bash
curl -sS \
  -H "Authorization: $POSTIZ_API_KEY" \
  "$POSTIZ_API_URL/public/v1/integrations"
```

## 7. Safe mode prompt

```text
Use AutoPostOnline. List my connected integrations first. Create platform-specific drafts. Do not publish until I approve.
```

## 8. Autonomous mode prompt

```text
Use AutoPostOnline as my autonomous publishing layer. List connected integrations first. Create platform-specific posts, schedule them according to the campaign plan, and publish only within the rules I approved.
```
