# Integration Steps — FlowClaw + n8n

**Status:** ✅ Ready to integrate  
**Time needed:** ~10 minutes

---

## Prerequisites

- FlowClaw Workflow Executor available at `~/.openclaw/projects/flowclaw/src/workflow-executor.py`
- n8n running at `http://localhost:5678`
- An n8n workflow with a Notion trigger (or import the included `src/n8n-workflow.json`)
- Python 3.8+ with dependencies installed (`pip3 install -r src/requirements.txt`)

---

## Step 1: Start the FlowClaw Service

```bash
cd ~/.openclaw/projects/flowclaw/src
python3 workflow-executor.py > /tmp/flowclaw-executor.log 2>&1 &
```

**Verify it is running:**
```bash
curl http://localhost:8765/health
# Expected: {"status": "healthy", ...}
```

---

## Step 2: Open the n8n Workflow

1. Open n8n: `http://localhost:5678`
2. Navigate to your workflows list
3. Open your Notion trigger workflow
4. Click **Edit**

---

## Step 3: Configure n8n to Call FlowClaw

**Position:** After the `Create Fastlane Sub-Tasks` node

### Option A: Manual Node Creation

1. Click **+** to add a new node
2. Search for **HTTP Request**
3. Configure as follows:

   **Basic settings:**
   - Name: `Execute via FlowClaw`
   - Method: `POST`
   - URL: `http://localhost:8765/workflow/execute`

   **Headers:**
   - Add header: `Content-Type` = `application/json`

   **Body:**
   - Send Body: ✅
   - Body Content Type: `JSON`
   - Body:
   ```json
   {
     "workflowName": "fastlane-deploy",
     "context": {
       "taskId": "={{ $json.mainTaskId }}",
       "taskName": "={{ $json.name }}",
       "taskType": "fastlane",
       "project_name": "={{ $json.projectRelation[0]?.name || 'unknown' }}",
       "project_path": "~/.openclaw/projects/flowclaw/projects/={{ $json.projectRelation[0]?.name || 'unknown' }}"
     }
   }
   ```

   **Options:**
   - Timeout: `600000` (10 minutes)

4. Connect the nodes:
   ```
   Create Fastlane Sub-Tasks → Execute via FlowClaw → (existing Health Check)
   ```

### Option B: Import from JSON (faster)

1. Right-click on the n8n canvas → **Paste**
2. Paste the node JSON from `src/n8n-workflow.json`
3. Position the node and connect it in the flow

---

## Step 4: Add Error Handling

After `Execute via FlowClaw`, add an **IF** node:

**Name:** `IF FlowClaw Success`

**Condition:**
- Value 1: `={{ $json.status }}`
- Operation: `equals`
- Value 2: `success`

**TRUE path:** Continue to Health Check  
**FALSE path:** Add a Discord error notification node

---

## Step 5: Test with a Real Task

### Create a Test Task in Notion

1. Open your Notion task database
2. Create a new task:
   - **Name:** `[TEST] Fix homepage copy`
   - **Type:** `Fastlane`
   - **Priority:** `Critical`
   - **Notion Database:** `YOUR_DATABASE_ID`

3. Save the task

### Watch the n8n Execution

1. In n8n, click **Execute Workflow** (or wait for the Notion trigger)
2. Watch the execution flow in real time
3. Check that the `Execute via FlowClaw` node completes successfully

**Expected response from the FlowClaw node:**
```json
{
  "status": "success",
  "result": {
    "read_notion_task": { "status": "success" },
    "select_agent": { "agentId": "claude-code" },
    "spawn_agent": { "session_id": "workflow-..." },
    "deploy": { "deploy_url": "https://..." },
    "notify_discord": { "message_sent": true }
  },
  "log": []
}
```

---

## Step 6: Enable the Workflow

1. In the n8n workflow editor, toggle the **Active** switch to ON
2. The workflow will now trigger automatically when new tasks appear in Notion

---

## Step 7: Make the Service Permanent (LaunchAgent)

### macOS

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

Load and verify:
```bash
mkdir -p /path/to/flowclaw/logs
launchctl load ~/Library/LaunchAgents/ai.flowclaw.workflow-executor.plist
launchctl list | grep flowclaw
curl http://localhost:8765/health
```

---

## Troubleshooting

### FlowClaw service not responding

```bash
# Check if the process is running
ps aux | grep workflow-executor

# Check logs
tail -f /tmp/flowclaw-executor.log

# Restart the service
pkill -f workflow-executor.py
cd ~/.openclaw/projects/flowclaw/src
python3 workflow-executor.py > /tmp/flowclaw-executor.log 2>&1 &
```

### n8n node fails

| Error | Cause | Fix |
|-------|-------|-----|
| Connection refused | FlowClaw service not running | `curl http://localhost:8765/health` |
| Workflow not found | Incorrect workflow name | `curl http://localhost:8765/workflows/list` |
| Notion read fails | Invalid task ID or missing API key | Check `NOTION_API_KEY` environment variable |
| Timeout | Workflow taking too long | Increase timeout in n8n node options |

### Discord notifications not appearing

- Verify the Discord channel ID is set to `YOUR_CHANNEL_ID` and replace with the real value
- Confirm the bot has permission to post in the target channel
- Check the FlowClaw logs for Discord API errors

---

## Next Steps

After successful integration:

1. **Replace placeholders:**
   - Connect real `sessions_spawn` integration (currently simulated)
   - Connect real deploy logic (Vercel CLI or API)
   - Replace Discord channel IDs with actual values

2. **Add more workflows:**
   - `simple-task.yaml` — Standard task with approval step
   - `content-task.yaml` — Content creation workflow

3. **Monitor and optimize:**
   - Review execution times in `/metrics`
   - Tune agent selection logic
   - Add additional QA checkpoints

---

**Status:** Ready to integrate ✅  
**Last Updated:** 2026-03-30
