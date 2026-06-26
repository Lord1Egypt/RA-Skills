# Family Steward - ClawHub Skill

This directory contains the ClawHub skill configuration for Family Steward.

## Files

- **SKILL.md** - Main skill documentation (markdown format for ClawHub display)
- **skill.json** - Comprehensive skill metadata and configuration
- **README.md** - This file

## Publishing to ClawHub

### Manual Upload

1. Visit: https://clawhub.ai/ZhenStaff/family-steward
2. Click "Edit" button
3. Upload `SKILL.md`
4. Fill in changelog
5. Set version and publish

### CLI Upload

```bash
clawhub publish /home/justin/openclaw-family-steward/openclaw-skill \
  --slug family-steward \
  --version 1.0.0 \
  --changelog "Initial release: Family member management, professional contact network, document management, task coordination, and AI agent integration. Privacy-first with local JSON storage."
```

## Skill Information

- **Name**: family-steward
- **Display Name**: Family Steward
- **Version**: 1.0.0
- **Author**: @ZhenStaff
- **Category**: Productivity
- **License**: MIT

## Installation (for users)

```bash
# Via ClawHub
clawhub install family-steward

# Via NPM
npm install -g openclaw-family-steward

# Via GitHub
git clone https://github.com/ZhenRobotics/openclaw-family-steward.git
cd openclaw-family-steward
npm install
```

## Quick Start

```bash
# View dashboard
family-steward dashboard

# List family members
family-steward family list

# Check upcoming birthdays
family-steward family birthdays

# List contacts
family-steward contact list

# View today's tasks
family-steward task today
```

## Agent Triggers

The skill is automatically triggered when user messages contain:

- Keywords: `family`, `steward`, `contact`, `document`, `task`, `家族`, `管家`, `联系人`, `文档`, `任务`
- Family office management requests
- Contact relationship tracking
- Document management needs
- Task coordination

## Tools Provided

1. **list_family_members** - List all family members
2. **get_upcoming_birthdays** - Get upcoming birthdays
3. **search_family_members** - Search family members
4. **get_family_member** - Get member details
5. **list_contacts** - List professional contacts
6. **get_contacts_needing_followup** - Get contacts needing follow-up
7. **search_contacts** - Search contacts
8. **get_contact_details** - Get contact details
9. **log_contact_interaction** - Log contact interaction
10. **list_documents** - List documents
11. **get_expiring_documents** - Get expiring documents
12. **get_documents_needing_review** - Get documents needing review
13. **search_documents** - Search documents
14. **list_tasks** - List tasks
15. **get_todays_tasks** - Get today's tasks
16. **get_upcoming_tasks** - Get upcoming tasks
17. **get_overdue_tasks** - Get overdue tasks
18. **complete_task** - Mark task as completed
19. **search_tasks** - Search tasks
20. **get_dashboard** - Get comprehensive dashboard

## Privacy & Security

- All data stored locally
- No cloud sync or external API calls
- No user tracking
- Open source, auditable code
- User has full control over data

## Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-family-steward
- **NPM**: https://www.npmjs.com/package/openclaw-family-steward
- **ClawHub**: https://clawhub.ai/ZhenStaff/family-steward
- **Issues**: https://github.com/ZhenRobotics/openclaw-family-steward/issues

## Version History

### v1.0.0 (2026-03-08)
- Initial release
- Family member management
- Professional contact network
- Document management system
- Task and schedule management
- AI agent integration (17 tools)
- CLI interface
- Local JSON storage

## Support

For issues or questions:
- GitHub Issues: https://github.com/ZhenRobotics/openclaw-family-steward/issues
- Email: code@zhenrobot.com

---

**License**: MIT
**Author**: @ZhenStaff / justin
**Organization**: ZhenRobotics
