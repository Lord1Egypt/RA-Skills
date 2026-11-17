---
name: applysent
description: Search jobs that fit the user's résumé, tailor the résumé to a job and apply on the employer's own form through the ApplySent MCP server, one job at a time and only after the user says yes. Use when the user wants to find jobs, apply to a job, check application status or answer an employer's application question.
---

# ApplySent: job search and applications with approval

ApplySent finds jobs that fit the user's résumé, tailors the résumé to each job and submits the employer's own application form (Workday, Greenhouse, Lever, Ashby and 8 more hiring systems), keeping a receipt of exactly what was sent.

**The one rule:** never send an application the user has not approved in this conversation. Each application needs its own yes. There is no bulk or automatic applying.

## 1. Connect

Need an account first? Sign up at https://applysent.com/signup (plans at https://applysent.com/pricing).


Add the remote MCP server if it isn't connected yet:

- URL: `https://applysent.com/api/mcp`
- Transport: Streamable HTTP
- Auth: OAuth. The client opens an ApplySent sign-in page on first use.

```json
{ "mcpServers": { "applysent": { "type": "streamable-http", "url": "https://applysent.com/api/mcp" } } }
```

In OpenClaw, add it as a remote MCP server with the URL above. In Claude: Settings → Connectors → Add custom connector → paste the URL. The user needs an ApplySent account (plans at https://applysent.com/pricing). If a tool answers that a plan or trial is needed, tell the user and link the pricing page; don't retry.

## 2. Check the profile

Call `get_profile_status` first. If it lists missing items (for example a résumé or work authorisation), tell the user what to add in ApplySent before applying. Searching works without a complete profile; applying does not.

## 3. Find jobs

- `search_jobs`: jobs matching the résumé and filters, best match first, a page at a time. Pass the user's filters (role, location, remote) when they give them.
- `get_job`: full details for one job; `get_job_from_link`: a job from a posting URL the user pastes.
- Show a short list (title, company, location, why it fits) and let the user pick. Don't apply to anything just because it was in the results.
- `set_job_saved`, `set_job_feedback` and `set_company_blocked` let the user save, skip or hide companies.

## 4. Tailor the résumé

- `preview_tailored_resume`: the résumé tailored to the chosen job and what changed. It only rewrites facts already in the user's résumé.
- Show the changes. If the user wants another version, call `regenerate_tailored_resume`. If they're happy, `approve_tailored_resume`.

## 5. Apply, with approval for this one job

1. Call `preview_application` for the job. It sends nothing and returns what would be sent plus a single-use `confirmation_token`. The token is valid for this job only and expires after 10 minutes.
2. Show the user the preview: employer, role, the résumé, and the answers that would go on the form.
3. Ask plainly: "Send this application to {company} for {role}?" Wait for a clear yes.
4. Only after that yes, call `apply_to_job` with the `job_id` and the `confirmation_token`.
5. For the next job, repeat from step 1. A yes never carries over to another job.

If the user would rather review inside ApplySent, call `queue_application_for_review` instead. It sends nothing; the user approves it in the app. `cancel_application` stops an application before sending starts.

## 6. Questions only the user can answer

Some forms ask things only the user knows (visa sponsorship, notice period, salary). `list_pending_questions` shows them. Ask the user, then save their exact words with `answer_question`. Never guess or invent an answer, least of all on work-authorisation or sponsorship questions.

## 7. Track applications

- `get_application`: status and step. If it returns `poll_after_seconds`, wait that long before checking again.
- `get_application_receipt`: what was actually sent, with the employer's confirmation.
- `list_applications`, `get_application_board`, `list_inbox` (employer emails) and `list_notifications` give the overview.

A job already applied to, or one whose send outcome is uncertain, is never sent again. Don't try to work around that.

## Don'ts

- Don't call `apply_to_job` without a fresh `preview_application` and the user's yes for that exact job.
- Don't batch-apply, loop over search results or reuse a confirmation token.
- Don't invent answers, skills or experience.
- ApplySent doesn't apply through LinkedIn Easy Apply or Indeed. The supported hiring systems are listed at https://applysent.com/supported-ats.

Help: https://applysent.com/help · Support: support@applysent.com
