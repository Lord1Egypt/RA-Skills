# functions/src/mcp/openclaw-skill/AUTOMATIONS.md

# Capital Equipment - Proactive Automations

Optional proactive workflows for equipment availability, pricing, and collaboration. These automations run on OpenClaw's heartbeat/cron system to deliver proactive value without the researcher asking.

## Important: User Consent & Privacy

**All automations are disabled by default.** Each must be explicitly enabled by the user. You can disable any automation at any time. No automation runs until you opt in.

| Automation           | Data Accessed              | Purpose                                   |
| -------------------- | -------------------------- | ----------------------------------------- |
| Morning Briefing     | Saved searches, bookings   | Upcoming reservations and new listings    |
| Price Alert          | Marketplace listings       | Notify when prices drop below threshold   |
| Availability Monitor | Booking calendars          | Alert when slots open on needed equipment |
| Collaboration Digest | Public researcher profiles | Weekly potential collaborators            |

_Note: No automation reads private messages, files, or data outside the Capital Equipment platform._

---

## 1. Equipment Scout (Every 6 hours)

Monitors marketplace and database for new equipment matching saved searches.

```yaml
name: equipment-scout
schedule: "0 */6 * * *"
description: "Check for new equipment matching your saved interests"
```
