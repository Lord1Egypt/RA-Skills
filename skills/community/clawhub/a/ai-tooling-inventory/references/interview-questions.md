# AI Tooling Inventory — Interview Question Bank

**Version:** 2.0
**Status:** Reference file for the ai-tooling-inventory skill. Questions are bounded and fixed. The skill selects from this bank based on gaps. Within any bank question that fires, the skill may ask clarifying sub-questions to resolve the same gap — for example, following up on a specific vendor, platform, or workflow that the respondent mentions. It does not introduce new topical areas outside the bank.

**Framing to open every interview:** "I'm going to ask about tools the organization uses, not to identify who did what, but to find gaps in how we've documented and covered them. There are no wrong answers, and nothing you say here is about individual conduct."

---

## Role: IT / Administrator

Use with: IT lead, systems administrator, MSP contact. Covers paths 2, 3, 4 at the system level.

**IT-1** — Do you maintain a list of AI tools the organization has formally approved? What's on it?

**IT-2** — Do any of your SaaS subscriptions have more licensed seats than named users on your formal list? What are people using those extra seats for?

**IT-3** — For each of these platforms — [list known platforms from vendor register] — have you checked what third-party apps or integrations have been connected to it at the tenant level? What did you find?

**IT-4** — Has anyone filed a ticket or made an informal request to set up an AI assistant, connect a plugin, or automate a workflow in the last 12 months? What came of it?

**IT-5** — Which vendors on your approved list have shipped AI features in the last year that you didn't specifically buy? Did any of those roll out to your tenant?

**IT-6** — Do you have an MDM or browser policy that would catch browser extensions? If yes, what categories appear in the inventory? If no, is extension use on work machines unrestricted?

**IT-7** — Has anyone built something in-house — a script, a custom GPT, a workflow that calls an API — that touches patient records or administrative data?

**IT-8** — Are there any tools used only by one or two people that aren't in the formal system? Who tends to build their own shortcuts here?

---

## Role: Function Manager

Use with: intake supervisor, billing manager, care coordination lead, credentialing manager, compliance officer, practice manager. Covers paths 2, 3, 5.

**FM-1** — Which parts of your team's work involve the most repetitive document handling — intake packets, prior auth, billing denials, referrals, chart abstraction?

**FM-2** — Has anyone on your team automated any part of that? Even informally — a prompt they reuse, a template they paste into a tool?

**FM-3** — Is there someone on your team who tends to find technical shortcuts before anyone else? What have they built or set up recently?

**FM-4** — Has your team ever gotten tired of waiting for IT and found their own solution? What was the situation and what did they use?

**FM-5** — Does anyone maintain a shared prompt, a custom assistant, or a set of instructions that other team members also use? What does it do?

**FM-6** — Do you use [vendor X] — [list approved products relevant to function]? Has it shipped any AI features recently? Have you noticed any new buttons or features that summarize, suggest, or generate text?

**FM-7** — In the last year, has your team drafted any documents — policies, reports, patient letters, authorization forms — with help from an AI tool? Which tool, and what was submitted to it?

**FM-8** — Are there free tools — browser extensions, web apps, personal subscriptions — that you or your team use for work tasks? Anything you'd use on your own and wouldn't think to report?

---

## Role: Staff (self-report, no-consequence frame required)

Use with: front desk, billing staff, care coordinators, clinical support staff. Covers paths 4 and 5. This subset can also be handed over as a written script for the respondent to run with their own team.

**S-1** — Are there websites or apps you use for work tasks that aren't on an approved list — even free ones?

**S-2** — Have you ever signed up for a tool using your work email address? Does anything come to mind?

**S-3** — Do you use any browser extensions — things that add features to Chrome or Edge — while doing your work? Do any of them read the content of the pages you're on?

**S-4** — Has anyone shared a prompt, a template, or a custom AI assistant with you that you use for your work? Where does it come from?

**S-5** — Has a vendor product you already use added any AI features recently — a new button, a summary feature, a suggestion tool? Have you used it?

---

## Tier 0 Self-Inspection Walk-Through

For any respondent who can check their own account in the session. Run after the interview questions.

**OA-1 (Microsoft)** — "Can you open your My Apps portal? Hover over each app and click the ellipsis, then 'Manage your application,' then 'Permissions.' The top section shows apps you've personally authorized. What do you see?"

**OA-1a (Google)** — "Can you open myaccount.google.com, go to Security, then 'Third-party apps with account access'? What apps are listed there with access to your work account?"

**OA-2** — "For each app in that list: do you recognize it? Do you know who operates it and whether the organization has an agreement with them?"

**OA-3 (Inbox search)** — "Can you search your work inbox for 'verify your email'? What comes up? Now try 'welcome to' and 'confirm your account.'"

**OA-4 (Browser extensions)** — "Can you open chrome://extensions (or edge://extensions) right now? For each extension: does it say it can read the content of the sites you visit? Do you know who made it?"

---

## Authoring-Disclosure Questions

Fire these for any respondent who produces written deliverables (compliance officer, practice manager, function manager with document-heavy role).

**AD-1** — "In the last year, has any document your team produced — a policy, a notice, a report, a patient letter — been drafted with help from an AI tool?"

**AD-2** — "Which tool was it? Was it a free consumer account or an enterprise account? Do you know whether the organization has an agreement with that provider?"

**AD-3** — "What content was submitted to it — general structure and language, or did it include anything that identified the organization, specific patients, or specific clinical situations?"

---

## Notes on Use

- **Selection is gap-driven.** If the vendor register is thorough and covers path 1 completely, skip IT-5's vendor-feature line and jump directly to IT-4 and IT-7. If the spend export is already in hand, FM-8's free-tool line is still required — the spend export misses it structurally.
- **Adaptive in selection, never in generation.** The skill picks from this bank. It does not generate questions outside it.
- **Staff subset as handoff.** Questions S-1 through S-5 plus OA-1 through OA-4 can be formatted as a one-page self-check for staff. The skill cannot run a staff survey and should not pretend to. Framing: "Here are five things to check on your own machine and account. Nothing here is about getting in trouble; it's about finding gaps before they become problems."
