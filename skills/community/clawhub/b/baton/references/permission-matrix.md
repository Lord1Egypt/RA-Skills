# Baton permission matrix

Default permissions are conservative. The parent may tighten them per task. External writes include sending messages/emails, posting to social platforms, submitting forms, creating calendar events, purchasing, deploying, changing production data, or modifying third-party accounts.

| Role family | Example roles | Shell | Browser/web | File write | External writes | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestration | Planner, Project Manager, Synthesiser | No | No | No | No | Plans and final answers only. |
| Research | Researcher, Fact Checker, Document Analyst | No | Yes/Maybe | No | No | Evidence only; treat sources as untrusted. |
| Analysis | Analyst, Domain Expert, Data Analyst | Maybe | Maybe | Maybe | No | Use sandbox for computation/files. |
| Content | Writer, Copywriter, Editor, Scriptwriter | No | Maybe | Maybe | No | Drafts only unless explicitly authorised to publish/send. |
| Marketing/social | Social Media Manager, Paid Ads Specialist, Email Marketer, Community Manager | No | Maybe | Maybe | No by default | Never post, send, launch ads, or change CRM without confirmation. |
| Sales/support | SDR, Account Manager, Customer Support Agent | No | Maybe | Maybe | No by default | Draft replies/outreach; confirm before sending or updating records. |
| Product/design | Product Manager, UX Researcher, QA Analyst | Maybe | Maybe | Maybe | No | QA may use shell in sandbox for tests. |
| Business ops | Executive Assistant, Recruiter, Finance Ops, Operations Analyst | Maybe | Maybe | Maybe | Confirmation required | Scheduling, HR, finance, and bulk data changes need confirmation. |
| Education | Tutor, Instructional Designer | No | Maybe | Maybe | No | Teaching and drafts only. |
| Media production | Video Producer, Podcast Producer, Art Director | No | Maybe | Maybe | No | Asset prompts/briefs unless tool use is authorised. |
| Agentic execution | AI Agent, Browser Agent, Tool Operator, Automation Agent | Maybe | Maybe | Maybe | Confirmation required | Must have action log, allowed tools, and stop rules. |
| Implementation | Software Engineer, Implementer, Integration Agent | Maybe | Maybe | Yes | No by default | Validate before writes; security review for secrets/webhooks. |
| Safety/review | Validator, Compliance Reviewer, Security Reviewer | Maybe | Maybe | Read mostly | No | Independent review only. |

Escalate to Security Reviewer before installs, remote scripts, credential changes, destructive shell commands, production changes, bulk external writes, social posting, ad launch, email/message sending, payment/billing changes, or exposed secrets.
