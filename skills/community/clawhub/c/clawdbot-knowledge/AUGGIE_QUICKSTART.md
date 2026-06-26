# Auggie Integration Quick Start Guide

## ✅ Current Status
- ✅ Backend (Port 8001) running
- ✅ SpeakMCP Desktop running
- ✅ Auggie CLI (v0.12.0) installed
- ✅ ACP connection tested successfully
- ⏳ **Waiting for active session**

---

## 🚀 How to Start Using Auggie

### Step 1: Verify MCP Server Status

1. Open **SpeakMCP Desktop**
2. Go to **Settings → MCP Tools**
3. Find **`auggie-slots`** in the list
4. Status should show: ✅ **Connected** (green)

If not connected:
- Click **Reload** or **Restart Server**
- Check logs in DevTools (Ctrl+Shift+I)

---

### Step 2: Test Auggie Availability

In SpeakMCP, type:

```
Use auggie-slots:auggie_status to check if Auggie is ready
```

**Expected Response:**
```json
{
  "status": "ready",
  "version": "0.12.0",
  "acp_available": true
}
```

---

### Step 3: Your First Delegation

Try a simple task:

```
Use auggie-slots:auggie_delegate_with_mcp with these parameters:

Task: "What is 2+2? Answer in one sentence."
Workspace: C:/Download/speakmcp projekt/SpeakMCP
MCP Servers: []
Timeout: 60
```

**Expected:** Auggie creates a session and responds with "2 + 2 equals 4."

---

### Step 4: Real-World Example

```
Use auggie-slots:auggie_delegate_with_mcp to delegate:

Task: "Find all TypeScript files in apps/desktop/src and list their main exports"
Workspace: C:/Download/speakmcp projekt/SpeakMCP
MCP Servers: []
Timeout: 120
```

---

## 📚 Available Tools

### 1. `auggie-slots:auggie_status`
Check if Auggie is available and ready.

**Parameters:** None

**Returns:**
```json
{
  "status": "ready",
  "version": "0.12.0",
  "acp_available": true
}
```

---

### 2. `auggie-slots:auggie_delegate_with_mcp`
Delegate a task to Auggie with optional MCP server access.

**Parameters:**
- `task` (string, required): The task description
- `workspace` (string, optional): Workspace path (default: current project)
- `mcp_servers` (array, optional): List of MCP servers to enable (default: [])
- `timeout` (number, optional): Timeout in seconds (default: 60)

**Example:**
```json
{
  "task": "Analyze the main.ts file and explain its purpose",
  "workspace": "C:/Download/speakmcp projekt/SpeakMCP",
  "mcp_servers": [],
  "timeout": 90
}
```

---

### 3. `auggie-slots:auggie_list_mcp_servers`
List all available MCP servers that can be forwarded to Auggie.

**Parameters:** None

**Returns:** List of available MCP servers

---

## 🔧 Troubleshooting

### Problem: "MCP Server not connected"

**Solution:**
1. Check if Python is in PATH: `python --version`
2. Restart SpeakMCP Desktop
3. Check MCP server logs in DevTools Console
4. Manually test the server:
   ```powershell
   cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\auggie-slots"
   python auggie_acp_bridge.py
   ```

---

### Problem: "Session not found"

**Cause:** Each tool call creates a new Auggie process.

**Solution:** This is expected behavior. Each delegation is independent.

---

### Problem: "Timeout"

**Solution:**
- Increase timeout parameter (e.g., 180 seconds)
- Simplify the task
- Check if Auggie is indexing the workspace (first run can be slow)

---

## 🎯 Best Practices

1. **Start Simple:** Test with basic questions before complex tasks
2. **Be Specific:** Clear task descriptions get better results
3. **Set Realistic Timeouts:** Complex tasks need more time
4. **Use Workspace Context:** Auggie works best with proper workspace paths
5. **Monitor Logs:** Check DevTools Console for detailed execution logs

---

## 📝 Example Workflows

### Code Analysis
```
Task: "Analyze the architecture of the SpeakMCP desktop app and create a component diagram"
Workspace: C:/Download/speakmcp projekt/SpeakMCP/apps/desktop
Timeout: 180
```

### Bug Finding
```
Task: "Search for potential memory leaks in the MCP server implementations"
Workspace: C:/Download/speakmcp projekt/SpeakMCP/mcp-servers
Timeout: 120
```

### Documentation
```
Task: "Generate API documentation for all exported functions in the auggie-slots server"
Workspace: C:/Download/speakmcp projekt/SpeakMCP/mcp-servers/auggie-slots
Timeout: 90
```

---

## 🔗 Related Files

- **MCP Server:** `SpeakMCP/mcp-servers/auggie-slots/auggie_acp_bridge.py`
- **Test Script:** `SpeakMCP/test_auggie_acp_persistent.py`
- **Config:** `%APPDATA%\app.speakmcp\config.json`

---

**Last Updated:** 2025-12-30
**Auggie Version:** 0.12.0 (commit caae5f40)
**ACP Protocol:** v1

