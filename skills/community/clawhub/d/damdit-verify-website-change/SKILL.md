---
name: verified-website-change
description: Verify a change to a website with Damdit audits before calling it done. Use when you build, change or fix a website (code in a repository, Webflow, a CMS), when the user asks to verify a fix after the deploy or to check that nothing broke on the site, or wants a verification step in their workflow. The result is confirmed on the rendered site, not from the code. Needs the `damdit` skill and Damdit CLI or Damdit for Mac.
---

# Verified website change

A change to a website is done when an audit of the rendered site confirms it, not when the code looks right. This skill adds that step to an implementation workflow such as `engineering-orchestrator`: an audit before the change, the change, an audit after the deploy, and a handoff that says what the audits showed.

It uses Damdit through the `damdit` skill, which has every command and what the results mean. The commands below are written as `damdit-cli`; with Damdit for Mac type `damdit`. If neither is installed, say so and hand off as `unverified`. Never replace the audit with your own reading of the code or of a page you opened.

## Do the whole loop yourself when you can

Don't hand the work back between the steps. If you are allowed to push and to see the deployment, push, wait for the deploy and audit without asking. If a step is not yours to take (you can't push, the staging site is locked, Docker isn't running), do everything else first, then say once and exactly what you need, and continue from there when you get it. Either way the report at the end says only what the audits showed.

## When it applies

- You are about to change what a website serves: templates, components, content, redirects, headers, metadata, a Webflow or CMS change.
- The user asked to fix what an audit found.

It doesn't apply to changes the rendered site cannot show (build tooling, tests, internal scripts).

**The verifying audit is part of the task.** Other Damdit instructions say to run an audit only when the user asks. A user who works with this skill has asked: when they give you a website change to make, the audits of that project's own address before and after the change are included, and you don't wait for a separate go-ahead. This covers the project the task names, nothing else: don't audit other websites or create a project without asking.

## 1. Baseline

Before you change anything, know the state you start from.

- Find the project: `damdit-cli projects`. If the site has none, ask the user before you create one.
- Read the current audit with `damdit-cli summary <project>` and note when it ran. If it is older than the last deploy, or the user wants fresh results, run `damdit-cli audit <project>` (add `--target staging` when you work against staging).
- Write down the audit's `runId`. Everything after is compared with it.
- For a fix, read the issues you are asked to fix with `damdit-cli issues` and `damdit-cli occurrences`: each one names the page and the element. Those are your acceptance criteria.

## 2. Change

Make the smallest change that removes the cause, on the element and page the audit named. Don't fix issues nobody asked about; report them as out of scope.

A site running on this computer can be checked once before the deploy with `damdit-cli check http://localhost:<port>`. It answers only what the page itself decides. It is a quick look, not the verification.

## 3. Verify on the deployed site

The verification is an audit of the address people will open.

- **Confirm the deploy first.** An audit of the old deploy proves nothing and shows up as a false "Still detected". Before you audit, show that the address serves your change: fetch one changed page and find the changed markup in it, or check the host's deployment status for your commit (for example `vercel inspect`, the deployments API, or the pipeline run). If neither is possible, ask the user to confirm; when the user tells you it is deployed, that is the confirmation, and the audit follows at once.
- **A locked staging site needs access.** If the site is behind a login, the audit stops while preparing and says what the site needs. Damdit CLI reads the access from the environment: HTTP Basic (`DAMDIT_SITE_USERNAME`, `DAMDIT_SITE_PASSWORD`), Vercel Deployment Protection (`DAMDIT_VERCEL_BYPASS`), Cloudflare Access (`DAMDIT_CF_ACCESS_CLIENT_ID`, `DAMDIT_CF_ACCESS_CLIENT_SECRET`) or a Webflow site password (`DAMDIT_WEBFLOW_PASSWORD`). The user sets these; never ask them to paste a secret into the conversation, and never print one. Without access, hand off as `unverified`.
- Run `damdit-cli audit <project>` on the same target as the baseline, then `damdit-cli compare <project>`.
- Read each issue you worked on:

| The comparison says | What it means for your change |
|---|---|
| Resolved | The audit no longer finds it. This, and only this, is "fixed". |
| Still detected | Not fixed. Read the occurrences again; the cause is elsewhere or the deploy is old. |
| Inconclusive | The audit couldn't check it this time. Neither fixed nor broken: say why (`reasonCodes`) and what would let it be checked. |
| New | Your change, or something deployed with it, introduced it. Fix it or report it before the handoff. |
| Reappeared | It was resolved before and is back. Treat it as New. |

- If `methodologyChanged` is true, or the scope of pages changed, say so: differences may not come from your change.

One more round is normal. Don't loop without a new idea: after two audits that still detect the issue, stop and report what you tried.

## 4. Handoff

Report in the workflow's own handoff format, with these facts:

- the baseline `runId` and the verifying `runId`, with their times and the target;
- per issue: Resolved, Still detected, Inconclusive, with the page;
- anything New or Reappeared;
- the score before and after, only as the comparison gives it;
- what the audit did not cover (its Coverage limits).

Status is `complete` only when every issue in scope is Resolved and nothing is New. With an Inconclusive issue or an audit you couldn't run, the status is `unverified`, with the reason.

## Without skills: a block for AGENTS.md

For an agent that reads only `AGENTS.md` or `CLAUDE.md`, this block carries the same rule:

```markdown
## Definition of done for website changes

A change to what the website serves is done only when a Damdit audit of the deployed site confirms it.

1. Before the change: `damdit-cli summary <project>` (run `damdit-cli audit <project>` if it is older than the last deploy). Note the runId.
2. Make the smallest change on the page and element the audit named.
3. After the deploy is live (check that the address serves the change): `damdit-cli audit <project>`, then `damdit-cli compare <project>`.
4. Report per issue: Resolved, Still detected, Inconclusive, plus anything New or Reappeared.

Say "fixed" only for Resolved. Inconclusive means not verified. If the audit can't run, say the change is unverified and why. Never judge the result from the code alone.
```

## In a pipeline

The same check without an agent: `damdit-cli ci audit <url> --baseline previous.dpk --out current.dpk --fail-on new,reappeared` fails the build only when an issue is new or came back. Keep `current.dpk` as the next run's baseline.
