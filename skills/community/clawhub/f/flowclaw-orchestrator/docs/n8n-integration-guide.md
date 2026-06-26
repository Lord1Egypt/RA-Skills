# n8n Integration Guide — FlowClaw Workflow Executor

**Purpose:** n8n triggers FlowClaw, FlowClaw executes workflows, and reports results back to n8n.

---

## 1. Start the FlowClaw Service

```bash
cd ~/.openclaw/projects/flowclaw/src
python3 workflow-executor.py
```

**Runs on:** `http://localhost:8765`

**Available endpoints:**
- `GET /health` — Health check
- `POST /workflow/execute` — Execute a workflow
- `GET /workflows/list` — List available workflows
- `POST /workflow/approve` — Approve a pending step
- `POST /workflow/resume` — Resume a paused workflow
- `GET /metrics` — Execution metrics
- `GET /dashboard` — Web dashboard

---

## 2. Add the FlowClaw Node to n8n

### Notion Task Workflow

**Position:** After the `Create Fastlane Sub-Tasks` node

**New node configuration:**

```json
{
  "name": "Execute via FlowClaw",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://localhost:8765/workflow/execute",
    "method": "POST",
    "authentication": "none",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "workflowName",
          "value": "fastlane-deploy"
        },
        {
          "name": "context",
          "value": {
            "taskId": "={{ $json.mainTaskId }}",
            "taskName": "={{ $json.name }}",
            "taskType": "fastlane",
            "project_name": "={{ $json.projectRelation[0].name }}",
            "project_path": "~/.openclaw/projects/flowclaw/projects/={{ $json.projectRelation[0].name }}"
          }
        }
      ]
    },
    "options": {
      "timeout": 600000
    }
  }
}
```

**Node connection order:**
```
Create Fastlane Sub-Tasks
  → Execute via FlowClaw
    → IF Execution Success
      → Health Check (existing)
```

---

## 3. FlowClaw Callback Webhook (Optional)

For asynchronous execution, configure an n8n Webhook node to receive results from FlowClaw:

**n8n Webhook node:**
```json
{
  "name": "Webhook - FlowClaw Done",
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "flowclaw-done",
    "httpMethod": "POST"
  }
}
```

**FlowClaw sends a POST callback on completion:**
```python
requests.post(
    "http://localhost:5678/webhook/flowclaw-done",
    json={
        "status": "success",
        "result": {},
        "deployUrl": "https://your-deploy-url",
        "executionTime": "120s"
    }
)
```

---

## 4. Discord Notifications

FlowClaw can send Discord messages directly from workflow YAML definitions — no additional n8n node required.

**In your workflow YAML:**
```yaml
- notify_discord:
    channel: "project_updates"
    message: "✅ Deploy complete: {deploy_url}"
```

**Alternatively, via n8n when running asynchronously:**
```json
{
  "name": "Discord - FlowClaw Result",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://discord.com/api/v10/channels/YOUR_CHANNEL_ID/messages",
    "method": "POST",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "discordWebhookApi",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "content",
          "value": "✅ **Workflow Complete**\n\nTask: {{ $json.taskName }}\nStatus: {{ $json.status }}\nDeploy: {{ $json.deployUrl }}"
        }
      ]
    }
  }
}
```

---

## 5. Error Handling

Add an **IF** node after `Execute via FlowClaw` to branch on success or failure:

```json
{
  "name": "IF FlowClaw Success",
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json.status }}",
          "operation": "equals",
          "value2": "success"
        }
      ]
    }
  }
}
```

- **TRUE path:** Continue to Health Check
- **FALSE path:** Send error notification

**Error notification node:**
```json
{
  "name": "Discord - FlowClaw Error",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://discord.com/api/v10/channels/YOUR_CHANNEL_ID/messages",
    "method": "POST",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "content",
          "value": "❌ **Workflow Failed**\n\nTask: {{ $json.taskName }}\nError: {{ $json.error }}\n\nPlease investigate."
        }
      ]
    }
  }
}
```

---

## 6. Health Checks & Testing

### Test 1: Health Check
```bash
curl http://localhost:8765/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "flowclaw-workflow-executor",
  "version": "1.0.0"
}
```

### Test 2: List Available Workflows
```bash
curl http://localhost:8765/workflows/list
```

Expected response:
```json
{
  "status": "success",
  "workflows": [
    {"name": "fastlane-deploy", "path": "..."},
    {"name": "simple-task", "path": "..."}
  ],
  "count": 2
}
```

### Test 3: Execute a Workflow
```bash
curl -X POST http://localhost:8765/workflow/execute \
  -H "Content-Type: application/json" \
  -d '{
    "workflowName": "fastlane-deploy",
    "context": {
      "taskId": "test-123",
      "taskName": "Test Task",
      "project_name": "my-project"
    }
  }'
```

Expected response:
```json
{
  "status": "success",
  "result": {
    "read_notion_task": {},
    "select_agent": {},
    "spawn_agent": {}
  },
  "log": []
}
```

---

## 7. Production Deployment

### macOS LaunchAgent

Create the file `~/Library/LaunchAgents/ai.flowclaw.workflow-executor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.flowclaw.workflow-executor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/flowclaw/src/workflow-executor.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/flowclaw/src</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/flowclaw/logs/workflow-executor.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/flowclaw/logs/workflow-executor-error.log</string>
</dict>
</plist>
```

Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/ai.flowclaw.workflow-executor.plist
```

Monitor logs:
```bash
tail -f /path/to/flowclaw/logs/workflow-executor.log
```

### Linux (systemd)

Use the template at `config/workflow-executor.service`. Copy it to `/etc/systemd/system/`, update paths, then:

```bash
systemctl enable workflow-executor
systemctl start workflow-executor
```

---

## 8. Next Steps

- [ ] Verify FlowClaw service starts cleanly
- [ ] Add the HTTP node to your Notion trigger workflow in n8n
- [ ] Test with a real Notion task
- [ ] Connect Discord bot token for live notifications
- [ ] Enable the n8n workflow (`active: true`) for automatic triggers

---

**Status:** Ready for integration  
**Last Updated:** 2026-03-30
