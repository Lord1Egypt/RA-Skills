# Dashboard Offer Workflow

Post-operation step: Offer to launch the visual task dashboard after completing task operations.

## When to Offer

Offer dashboard after these operations:
- ✅ Add task (any level)
- ✅ Complete task
- ✅ Move task between quadrants
- ✅ Bulk operations (multiple tasks)

Skip for:
- ❌ Simple queries (view tasks, check numbering)
- ❌ Silent operations (heartbeats, auto-fixes)

## Offer Format

```markdown
✅ [Operation] Completed

**Summary:**
- Operation: Add Task
- Task: [Task Name]
- Location: Q2 #15

📊 View task dashboard?
Type 'yes' to open, or press Enter to skip.
```

## User Response Handling

### User Approves ("yes", "y", "open", "dashboard")

```bash
# 1. Navigate to dashboard directory
cd ~/.openclaw/workspace/skills/eisenhower-task-manager/dashboard

# 2. Check if already running
if pgrep -f "node server.js" > /dev/null; then
    echo "[Dashboard] Already running"
    # Just open browser
    open http://localhost:$(cat port.conf 2>/dev/null || echo 8080)
else
    # 3. Start dashboard
    ./start.sh &
    
    # 4. Wait for server to start
    sleep 3
    
    # 5. Open browser
    PORT=$(cat port.conf 2>/dev/null || echo 8080)
    open http://localhost:$PORT
fi
```

### User Declines ("no", "n", empty, any other input)

```markdown
Skipped. You can open the dashboard anytime with:
cd dashboard && ./start.sh
```

## Implementation Example

```javascript
// Pseudo-code for skill implementation
async function offerDashboard(operation, taskInfo) {
  console.log(`✅ ${operation} Completed`);
  console.log(`\nTask: ${taskInfo.name}`);
  console.log(`Location: ${taskInfo.location}`);
  
  const response = await askUser("📊 View task dashboard? (yes/no)");
  
  if (response.match(/^(yes|y|open|dashboard)$/i)) {
    await launchDashboard();
    console.log("🌐 Dashboard opened in browser");
  } else {
    console.log("Skipped. Run 'cd dashboard && ./start.sh' anytime.");
  }
}
```

## Auto-Launch Considerations

**Current Design: Opt-in (User must approve)**
- ✅ Respects user control
- ✅ Prevents unexpected browser tabs
- ✅ Works in both interactive and scripted modes

**Alternative: Configurable Auto-launch**
If users want automatic launch, add to config:
```json
{
  "autoOpenDashboard": true
}
```

Then skip the prompt and auto-launch.

## Port Management

Dashboard remembers the last used port in `port.conf`:
- First run: Default 8080
- User specifies: `--port 3000` → saves 3000
- Subsequent runs: Uses saved port automatically

If port is in use, server will error - user should specify a different port.

## Browser Opening

Use platform-appropriate command:
- **macOS**: `open http://localhost:PORT`
- **Linux**: `xdg-open http://localhost:PORT`
- **Windows**: `start http://localhost:PORT`

Or let user manually open the URL.
