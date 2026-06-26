---
name: client-onboarding-checklist
version: 1.0.0
description: "Generate customized client onboarding checklists, welcome emails, and setup task lists for IT service providers, MSPs, and consultants. Covers network setup, software deployment, user provisioning, and documentation handoff."
triggers:
  - client onboarding
  - new client setup
  - onboarding checklist
  - new customer onboarding
  - client welcome
  - msp onboarding
  - it setup checklist
  - new account setup
  - client kickoff
tools:
  - read_file
  - write_file
metadata:
  openclaw:
    emoji: "📋"
    homepage: https://gaffneyits.com/openclaw
    os: ["darwin", "linux", "win32"]
    autostart: false
    tags:
      - onboarding
      - it-services
      - msp
      - checklist
      - client-management
      - project-management
---

# Client Onboarding Checklist

Generate structured onboarding checklists, welcome emails, and setup task lists for IT service providers, MSPs, and consultants bringing on new clients. Ensures nothing gets missed during the critical first 30 days.

## When to Use This Skill

Use when the user asks to:
- Create a checklist for onboarding a new client
- Generate a welcome email for a new client
- Build a setup task list for a new account
- Plan a client kickoff process
- Create an IT deployment checklist
- Set up a new managed services client

## Information to Gather

### Required
| Field | Description |
|-------|-------------|
| `client_name` | Company or individual name |
| `service_type` | What you're providing (managed IT, consulting, web services, etc.) |
| `provider_name` | Your company name |

### Optional (improves output)
| Field | Description |
|-------|-------------|
| `primary_contact` | Client's main point of contact |
| `primary_email` | Contact's email |
| `start_date` | Service start date |
| `user_count` | Number of users/seats |
| `services_list` | Specific services included in their plan |
| `tools_used` | Client's existing tools (Microsoft 365, Google Workspace, etc.) |
| `industry` | Client's industry (affects compliance needs) |
| `special_requirements` | Any unique needs mentioned |

## Service Type Detection

Determine the type from context and generate the appropriate checklist:

### Managed IT / MSP
Triggers: mentions of network, servers, workstations, helpdesk, monitoring, backup, antivirus, firewall, endpoint, RMM, PSA

### Web Services / Development
Triggers: mentions of website, hosting, domain, CMS, development, deployment, staging

### Consulting / Advisory
Triggers: mentions of assessment, audit, strategy, roadmap, advisory, planning

### General IT Services (default)
Use when the type isn't clear — covers the essentials that apply to any IT engagement.

## Output: Onboarding Checklist

Generate a checklist in markdown format with these sections. Include ONLY sections relevant to the detected service type. Each item should be a checkbox `[ ]`.

### Phase 1: Pre-Onboarding (Before Day 1)

```markdown
## Pre-Onboarding — {{client_name}}

### Administrative
- [ ] Signed service agreement / MSA on file
- [ ] Payment method and billing terms confirmed
- [ ] Primary contact info documented: {{primary_contact}}, {{primary_email}}
- [ ] Emergency contact info collected
- [ ] NDA executed (if applicable)
- [ ] Client added to PSA / billing system
- [ ] Welcome email sent (see template below)

### Discovery
- [ ] Current environment documented (devices, users, software)
- [ ] Existing vendor/provider list collected
- [ ] Login credentials and admin access transferred securely
- [ ] Network diagram obtained or site survey scheduled
- [ ] Current pain points and priorities noted
- [ ] Compliance requirements identified (HIPAA, PCI, etc.)
```

### Phase 2: Technical Setup (Days 1–7)

**For Managed IT / MSP:**
```markdown
## Technical Setup — Week 1

### Access & Credentials
- [ ] Admin access to all systems verified
- [ ] Password manager vault created for client
- [ ] Domain registrar access confirmed
- [ ] DNS management access confirmed
- [ ] Cloud admin consoles access (M365/Google/AWS)

### Monitoring & Management
- [ ] RMM agent deployed to all endpoints
- [ ] Monitoring alerts configured
- [ ] Antivirus/EDR deployed and reporting
- [ ] Backup solution deployed and first backup verified
- [ ] Firewall rules reviewed and documented
- [ ] Patch management policy applied

### User Setup
- [ ] User list verified ({{user_count}} users)
- [ ] User accounts created in your systems
- [ ] Helpdesk access / ticket submission method shared with users
- [ ] MFA enabled on all admin accounts
- [ ] Email security (SPF/DKIM/DMARC) verified
```

**For Web Services:**
```markdown
## Technical Setup — Week 1

### Hosting & Infrastructure
- [ ] Domain ownership verified
- [ ] DNS records documented
- [ ] Hosting environment provisioned
- [ ] SSL certificate installed and auto-renewing
- [ ] Staging environment created
- [ ] Deployment pipeline configured

### Application
- [ ] Current site backed up
- [ ] CMS admin access created
- [ ] Analytics tracking installed
- [ ] Contact forms tested
- [ ] Performance baseline recorded (Core Web Vitals)

### Access
- [ ] Client given appropriate CMS access
- [ ] Git repository access configured (if applicable)
- [ ] FTP/SFTP credentials secured
```

### Phase 3: Documentation & Training (Days 7–14)

```markdown
## Documentation & Training

### Documentation
- [ ] Client knowledge base article created
- [ ] Network diagram / architecture doc completed
- [ ] Escalation path documented
- [ ] SLA terms and response times documented
- [ ] Disaster recovery / business continuity plan drafted

### Training
- [ ] End-user training session scheduled
- [ ] Helpdesk usage walkthrough completed
- [ ] Key contact procedures shared (who to call for what)
- [ ] Self-service resources shared (portal, FAQ)
```

### Phase 4: Validation & Handoff (Days 14–30)

```markdown
## Validation & Handoff

### Verification
- [ ] All monitoring alerts tested (trigger and resolve one)
- [ ] Backup restore tested
- [ ] Helpdesk ticket flow tested end-to-end
- [ ] All services confirmed operational
- [ ] Client signs off on completed setup

### Ongoing
- [ ] First monthly report scheduled
- [ ] Quarterly business review (QBR) scheduled
- [ ] 30-day check-in call scheduled with {{primary_contact}}
- [ ] Internal team debrief on onboarding (lessons learned)
```

## Output: Welcome Email

When the user asks for a welcome email, generate this:

```
Subject: Welcome to {{provider_name}} — Getting Started

Hi {{primary_contact}},

Welcome to {{provider_name}}! We're excited to be working with {{client_name}} and want to make sure your transition is as smooth as possible.

Here's what happens next:

1. **This week:** We'll be setting up monitoring, security, and access to our support systems. You may see some brief notifications as we get everything connected — that's normal.

2. **How to reach us:**
   - Email: [support email]
   - Phone: [support phone]
   - Portal: [helpdesk URL]
   For urgent issues, always call.

3. **What we need from you:**
   - Admin credentials (sent securely via [method])
   - A list of current users and their roles
   - Any known issues you'd like us to prioritize

4. **First check-in:** We'll schedule a call in about 2 weeks to review the setup, answer questions, and confirm everything is running smoothly.

If you have any questions at all, don't hesitate to reach out. We're here to help.

Best,
{{provider_name}}
```

## Output: Kickoff Agenda

When the user asks for a kickoff meeting agenda:

```markdown
# Client Kickoff Meeting — {{client_name}}
**Date:** {{start_date}}
**Attendees:** {{provider_name}} team, {{primary_contact}}

## Agenda (60 minutes)

### 1. Introductions (5 min)
- Team members and roles
- Primary points of contact on both sides

### 2. Scope Review (10 min)
- Services included in the agreement
- What's in scope vs. out of scope
- SLA review (response times, escalation)

### 3. Technical Discovery (20 min)
- Current environment overview
- Known issues and priorities
- Upcoming projects or changes
- Compliance requirements

### 4. Onboarding Timeline (10 min)
- Walk through the 30-day onboarding plan
- Key milestones and what to expect
- What we need from the client (access, info)

### 5. Support Process (10 min)
- How to submit tickets
- Emergency procedures
- Communication preferences

### 6. Questions & Next Steps (5 min)
- Open Q&A
- Confirm next meeting / check-in date
```

## Stop Conditions

- Do NOT generate checklists for industries you don't have context for. If the user mentions a highly specialized field (e.g., "nuclear facility IT onboarding"), say: "I can generate a general IT onboarding checklist, but your industry likely has specific regulatory requirements I can't account for. Use this as a starting point and consult your compliance team."
- Do NOT include specific vendor names unless the user mentions them. Keep tool references generic (e.g., "RMM agent" not "ConnectWise Automate") unless the user specifies.
- Do NOT generate security credentials or passwords. If the user asks, say: "Use a password manager to generate and share credentials securely. Never send passwords in plain text email."
