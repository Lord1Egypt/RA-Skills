# Gateway Recovery Notification Skill

## Purpose
Automatically sends a notification message when the gateway restarts and recovers.

## How It Works

1. **Startup Hook**: Detects gateway restart and creates `~/.openclaw/recovery_flag`
2. **Heartbeat Check**: During heartbeat poll, secretary checks for recovery flag
3. **Send Notification**: If flag exists, sends "I'm back!" message and clears flag

## Configuration

- **Flag file**: `~/.openclaw/recovery_flag`
- **LaunchAgent**: `ai.openclaw.gateway-startup-hook.plist`
- **Log file**: `/Users/kazuni/.openclaw/workspace/memory/startup.log`

## Usage

The skill runs automatically during heartbeat checks. No manual intervention needed!

## Testing

To test manually:
1. Create flag: `touch ~/.openclaw/recovery_flag`
2. Secretary will detect it on next heartbeat
3. Send notification message
4. Clear flag automatically

---

*Created by Albedo - Mar 28, 2026 💕🌙*
