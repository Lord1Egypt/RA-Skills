---
name: email-approval-workflow
description: Draft external emails for human approval before sending. Use when communicating with external parties (support, competitions, businesses). Always draft first, send to Stef for approval, then send only after explicit approval.
---

# Email Approval Workflow

## Purpose

Ensure all external communications are reviewed and approved by Stef before sending. Prevents miscommunication, maintains professional standards, and allows for strategic input.

## When to Use This Workflow

**Use for:**
- Support tickets (Contabo, services, etc.)
- Competition entries
- Business inquiries
- Partnership discussions
- Any external communication

**Do NOT use for:**
- Internal agent communications
- System notifications
- Automated reports (unless specified)

## Workflow Steps

### Step 1: Draft Creation
```bash
# Create draft in drafts/ folder
mkdir -p /root/.openclaw/workspace/drafts/
cat > /root/.openclaw/workspace/drafts/{purpose}_draft.md << 'EOF'
TO: recipient@example.com
FROM: Appropriate Agent <agent@domain.com>
CC: Stef Ferreira <stef.personal@gmail.com>
SUBJECT: Clear, descriptive subject
DATE: $(date +"%B %d, %Y")

[Professional email content]

Best regards,

[Agent Name]
[Organization]
[Email]
EOF
```

### Step 2: Present for Approval
```
Present draft to Stef in current chat interface:
"Here's a draft email for [purpose]. Please review and approve:"

[Copy draft content]
```

### Step 3: Await Approval
- Wait for explicit "approved" or "send it" confirmation
- If edits requested, update draft and resubmit
- Never send without explicit approval

### Step 4: Send Email
```bash
# After approval, send using email system
cd /root/.openclaw/workspace && \
python3 email_manager.py send \
  --to "recipient@example.com" \
  --subject "Approved Subject" \
  --body "$(cat /root/.openclaw/workspace/drafts/{purpose}_draft.md | tail -n +7)"
```

### Step 5: Document
```bash
# Log sent email
echo "$(date -Iseconds)|{purpose}|{recipient}|SENT|APPROVED_BY_STEF" >> /root/.openclaw/workspace/email_log.csv
```

## Draft Template

```markdown
TO: [recipient@example.com]
FROM: [Agent Name] <[agent@domain.com]>
CC: Stef Ferreira <stef.personal@gmail.com>
SUBJECT: [Clear, descriptive subject]
DATE: [Month Day, Year]

[Professional greeting],

[Clear, concise message with:
1. Purpose/context
2. Specific request/information
3. Supporting details
4. Call to action
5. Appreciation]

[Professional closing],

[Agent Name]
[Organization/Role]
[Contact email]
```

## Approval Triggers

Stef must explicitly say one of:
- "Approved"
- "Send it"
- "Go ahead"
- "Yes, send that"

**NOT approved by:**
- "Looks good" (needs explicit send instruction)
- "OK" (ambiguous)
- Silence (never assume approval)

## Examples

### Example 1: Support Ticket Follow-up
```markdown
TO: support@contabo.com
FROM: Ace <ace@SupplyStoreAfrica.com>
CC: Stef Ferreira <stef.personal@gmail.com>
SUBJECT: Re: [#16240135688]: Network issues on our VPS
DATE: March 31, 2026

Dear Svitlana,

Thank you for your prompt response. To help us plan, could you provide:

1. Estimated timeline for resolution?
2. Will you provide proactive updates?
3. Any specific workarounds we should implement?

Current status: DNS workaround working, intermittent connectivity continues.

Thank you for your assistance.

Best regards,

Ace
Supply Store Africa
ace@SupplyStoreAfrica.com
```

### Example 2: Competition Entry
```markdown
TO: competitions@company.com
FROM: Ace <ace@SupplyStoreAfrica.com>
CC: Stef Ferreira <stef.personal@gmail.com>
SUBJECT: Entry: [Competition Name]
DATE: March 31, 2026

Dear Competition Team,

Please accept my entry for the [Competition Name].

[Required entry details]

Thank you for this opportunity.

Best regards,

Ace
Supply Store Africa
ace@SupplyStoreAfrica.com
```

## Error Handling

### If email fails to send:
1. Check network connectivity
2. Verify email credentials
3. Try alternative SMTP if configured
4. Report failure to Stef with error details

### If no response to approval request:
1. Wait minimum 1 hour
2. Send polite follow-up: "Just checking if you had a chance to review the draft?"
3. Never send without approval

## Integration with Agents

### Ace (Competitions Agent)
- Uses this workflow for all competition entries
- Maintains draft folder: `/root/.openclaw/workspace/agents/ace/drafts/`

### Lourens (SysAdmin)
- Uses for support tickets, infrastructure communications
- Maintains audit trail of all sent emails

### Facet (CAD Specialist)
- May use for technical inquiries with manufacturers/suppliers

## Audit Trail

All emails tracked in:
- `/root/.openclaw/workspace/email_log.csv`
- Individual agent logs
- Email system sent items

## Related Skills
- `gmail-gog-setup` - Email system configuration
- `secure-secret-sharing` - For sharing draft links if needed
- `telegram-multi-bot` - For approval notifications via Telegram