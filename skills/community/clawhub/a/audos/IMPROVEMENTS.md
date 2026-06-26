# Audos Skill — Roadmap & Ideas

## Done ✅
- **Better polling UX** — 15-20s intervals, immediate progress updates, visual status icons (✅🔄⏳)
- **Poll helper script** — `poll-with-updates.sh` for formatted terminal output

## Ideas 🔄

### Edit-in-place Progress Messages
Instead of sending a new message each poll, edit the same message with updated progress. Cleaner chat, less spam.

### Completion Celebration
Rich completion message with inline buttons: [View Landing Page] [Open Workspace] [Chat with Otto]

### Error Recovery
Detect `status: failed`, offer automatic rebuild with one click.

### Returning User Detection
Store authTokens by email — skip OTP for returning users. "Welcome back! [Open workspace] or [Create new]"

### Otto Chat Integration
After build completes, proactively offer: "Want me to ask Otto what to focus on first?"

### Multi-workspace Support
Track multiple workspaces per email. "You have 3 workspaces: [FitGenius] [PodFlow] [SnackBox]"

### Webhook Support
Use `callbackUrl` for push-based progress updates instead of polling.

---

*Contributions welcome!*
