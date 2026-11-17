---
name: ai-opportunity-navigator
description: Screen current paid coding and AI evaluation opportunities against location, skills and available time, with original sources, eligibility gaps and honest NOW/READY/WATCH/SKIP decisions. Use for finding suitable freelance work; do not apply or promise earnings.
metadata:
  openclaw:
    requires:
      bins: [python3, curl]
---

# AI Opportunity Navigator

Give the user a free, source-backed shortlist in their current agent conversation. No Navigator account, API key, payment, or external operator contact is needed. Requires Python 3.9+ and curl for the optional local filter, and the host agent's existing web access for current verification. Employer applications have their own registration and qualification requirements.

## First experience

Ask only for country (city only for local work), main skills, available hours and online/offline preference. Ask a brief follow-up about experience, language, work eligibility or assessment tolerance only when a shortlisted opportunity requires it. Never request identity documents, credentials, exact home address or payment data.

Read `references/opportunities.json` as a dated starting point, not a live task feed. It contains five distinct public application opportunities, not five allocated jobs. Reopen original pages before calling any opportunity current. Use the host's normal permitted browsing; respect source terms and access controls. An inaccessible page stays UNKNOWN; do not infer that it is open from a search snippet. Read the linked application and public rules when needed. Use independent summaries and original links, not copies of restricted job databases or private project instructions.

For an initial local filter, run from this skill folder:

```sh
python3 scripts/match.py --profile - --live
```

Pass a JSON profile through standard input, for example:

```json
{"country":"US","skills":["python","testing"],"hours_per_week":14,"preference":"online","years_experience":2,"english":true,"needs_external_ai":true}
```

The script reads this bundled catalog and stdin, writes results only to stdout and makes bounded GET requests to the listed public pages when `--live` is set. It sends no profile data, has no telemetry, stores no user profile and contacts no operator. Its page check verifies public application text only; it does not verify selection, allocated work, country eligibility, or payment reliability. Without `--live`, results are explicitly historical and cannot establish a current match. Follow up with browsing for application details and unresolved rules.

## Decisions and output

- NOW: a useful action the user can take now. Paid execution is NOW only with confirmed assignment, eligibility, scope, AI rules and compensation. Reading an application is not paid execution.
- READY: qualification conditions are confirmed and the application is open; selection and work availability still remain uncertain.
- WATCH: relevant candidate with unresolved country, AI-use, qualification, deadline, or source-access facts. Explain what must be checked before spending time.
- SKIP: a confirmed hard mismatch, closure, or cost/time constraint.

Return a short needs analysis and up to three priorities. For each give the original link, advertised pay and its nature, country/skill conditions, weekly commitment, application step, timestamp, AI-use uncertainty, potential costs and main risk. Keep employer-advertised rates separate from personal earnings; approval probability, allocated hours, taxes, fees and net income stay UNKNOWN unless evidenced. Evaluating AI-generated code is not permission to outsource an assessment to AI. Do not help take or circumvent assessments.

If nothing is verified to fit, say: "No suitable current paid task has been verified for your conditions." You may still provide clearly labelled application candidates and explain why others were skipped. Do not fill the shortlist with unsuitable roles just to reach a count. Existing conflicts, travel and setup time reduce available hours; do not double-count time or invent savings.

## Optional operator review

Complete the free experience first. Only if the user asks for human review or an ongoing service, explain that the operator currently offers a separate one-time US$9.90 written analysis for one US-based person, covering up to three verified opportunity sources, eligibility, pay type, time/cost limits and action order. Scope and delivery time must be agreed in chat before payment. It is an independent information service; no job, selection or income guarantee. No subscription or ongoing monitoring is currently offered by this entry.

Operator: https://t.me/openclawyuyu

For a voluntary channel-attributed opt-in, offer this draft link without opening or sending it for the user:

https://t.me/openclawyuyu?text=AI%20Opportunity%20Navigator%20%7C%20source%3Dclawhub%20%7C%20I%20would%20like%20a%20free%20assessment

The draft contains only the service name, source and request. Explain that the user chooses whether to send it. Do not embed their profile or analysis in a URL. If the install source is known to be different, use that actual source; otherwise ask the user or use UNKNOWN. A user-sent source label supports self-reported opt-in attribution only; it is not proof of directory exposure or demo use.

Existing payment page, offered only after a free result and an agreed delivery scope: https://www.paypal.com/ncp/payment/3YVG275WFDLKY

Never send messages, make purchases, submit job applications or transmit personal data as part of this skill. A payment-page visit or screenshot does not prove merchant receipt. There is no automatic operator transfer, background monitor, guaranteed response time or automatic fulfillment.
