---
name: apple-swift-mcp
description: This skill should be used when the user asks about Apple app data via the native Swift MCP — Calendar, Reminders, Contacts, Maps, Mail, Messages, or Notes on macOS. Triggers on phrases like "check my calendar", "find contact", "send iMessage", "search my notes", "recent emails", or any macOS-native app automation. Requires macOS 14+ on Apple Silicon; faster than the AppleScript-backed Node variant.
---

# apple-swift-mcp

Native Swift MCP server for Apple apps. Compiled binary with embedded TCC usage descriptions — Calendar, Reminders, Contacts, and Maps talk to EventKit / Contacts / MapKit directly. Mail, Messages, Notes still go through AppleScript (no public framework exists) but run in-process via `NSAppleScript` instead of spawning `osascript`.

- **GitHub:** [github.com/chrischall/apple-swift-mcp](https://github.com/chrischall/apple-swift-mcp)

## Install

Download the latest `.mcpb` from [GitHub Releases](https://github.com/chrischall/apple-swift-mcp/releases) and double-click to install in Claude Desktop. First run prompts for TCC permissions (Calendar, Reminders, Contacts, full disk if reading `chat.db`).

Requires **macOS 14+ on Apple Silicon**. Intel users can build from source (`swift build -c release`).

## Tools

### Calendar / Reminders
- `calendar` — list, search, create, update, delete events
- `reminders` — list reminder lists and items; create, complete, delete

### Contacts / Maps
- `contacts` — search by name, phone, or email
- `maps` — directions, search nearby places

### Mail / Messages / Notes (AppleScript-backed)
- `mail` — search, read, send, reply, forward; Messages.app-style threading
- `messages` — send iMessage / SMS, query `chat.db` for history, group chats
- `notes` — list, search, read, create notes

## Environment

Optional user config (set in Claude Desktop → Settings → MCP):

- `APPLE_MCP_DEFAULT_CALENDAR` — default calendar name for event creation
- `APPLE_MCP_DEFAULT_REMINDER_LIST` — default list name for reminder creation

## Notes

- Binary is arm64-only because some transitive MCP SDK deps (swift-collections, swift-service-lifecycle) don't declare x86_64.
- EventKit / Contacts / MapKit-backed tools are orders of magnitude faster than the equivalent AppleScript path.
- Messages tool reads `chat.db` directly for history; sending uses AppleScript.
