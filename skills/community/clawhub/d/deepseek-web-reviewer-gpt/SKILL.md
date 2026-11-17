---
name: chat.deepseek
description: GPT-only reviewer workflow for DeepSeek Web using the authenticated ChatGPT Work/Codex Cloud Browser. Requires GPT browser-control; not an OpenClaw-native integration.
---
> **Platform note:** This package depends on the GPT/ChatGPT Work Cloud Browser and its browser-control skill. It is not directly executable in a standard OpenClaw runtime unless equivalent browser capabilities are provided.


# chat.deepseek

Use DeepSeek Web at `chat.deepseek.com` through the authorized browser session. This is a visible web-interface workflow, not an API integration. Do not use a DeepSeek API, API key, paid endpoint, hidden network request, or an unapproved local browser workaround.

## Operating contract

- Use DeepSeek as an independent consultant when an important question is unclear, several interpretations are plausible, or a second opinion could reveal an error. Prefer the visible `Search` mode for this workflow so DeepSeek can check current information when appropriate.
- Ask DeepSeek to challenge assumptions, identify counterexamples, and separate evidence from speculation. Do not ask only for confirmation.
- DeepSeek's response is advisory evidence, not truth. The primary agent must compare it with the available facts and sources, explain conflicts, preserve uncertainty, and make the final decision.
- Keep user data minimal. Before transmitting sensitive personal, proprietary, medical, financial, credential, or confidential project information to DeepSeek, obtain explicit authorization for that material and destination. Never transmit passwords, OTPs, session tokens, cookies, or private browser data.
- Do not upload files unless the user explicitly asks DeepSeek to inspect them or clearly authorizes that transfer. Prefer a short, redacted text excerpt when sufficient.

## Browser and session

1. Use the available browser-control skill before interacting with DeepSeek. Reuse the existing DeepSeek tab when it is live; do not create unnecessary tabs or reload an active conversation.
2. Verify that the visible page is DeepSeek and that the account is signed in. A blank page, spinner, login form, CAPTCHA, bot check, or error is not proof of a valid session.
3. Use secure browser authentication for login or credential entry. Never request or enter a password, OTP, recovery code, or passkey through ordinary page automation.
4. If DeepSeek requests CAPTCHA, 2FA, re-authentication, or a security decision, stop at that step and offer a manual browser handoff. Do not solve or bypass a CAPTCHA.

## Attachments through the connected browser

Use this workflow only when the user asks DeepSeek to inspect an attachment or explicitly authorizes a file-transfer test.

- A local-file upload requires the Codex/ChatGPT browser extension's `Allow access to file URLs` permission. The Russian UI may call this `Разрешить открывать локальные файлы по ссылкам`; installing the extension alone is insufficient. If the user has just changed this setting, refresh the connected-browser inventory once because the extension may reconnect with a new browser ID. Then inspect the current user tabs and claim the existing DeepSeek tab; an empty agent-tab list does not mean the user tab or sign-in is missing.
- If browser policy blocks `brave://extensions` or another internal extension-settings URL, do not retry through another surface or raw browser commands. Ask the user to check the permission through Brave's normal UI.
- Read the browser's `file-uploads` documentation before attaching. Start `waitForEvent("filechooser")` before clicking the visible paperclip or upload menu item, then pass an absolute local path to the chooser. The input may be hidden, so do not force-click it or use unsupported `setInputFiles`.
- Inspect the live composer to identify the unique visible paperclip associated with the file input. In the observed DeepSeek layout, a broad selector for all buttons inside the attachment wrapper also matched the nested `Send` button and failed strict matching. Do not rely on that broad selector or a hashed CSS class; use the current DOM/visible UI to target only the attachment control.
- Verify the expected filename appears in the composer before sending. For an explicitly requested smoke test, use a harmless, small text file with a unique expected token and count success only after the completed reply matches the token. Inspect the current chat/main response rather than dumping the whole sidebar or chat history.

## Verify the visible model and Search mode

Inspect the live rendered UI immediately before sending the first task.

- Treat the visible interface as the source of truth for the selected mode. For this skill, ensure the visible `Search` control is selected before sending a review. Do not enable `DeepThink` unless the user explicitly asks for it.
- In the DeepSeek UI, a blue-highlighted control is active and a gray/unhighlighted control is inactive. Therefore the required state is `Search` blue and `DeepThink` gray. If `DeepThink` is blue, click it to turn it off; if `Search` is gray, click it to turn it on. Verify the colors after each change and immediately before sending.
- Record exact visible labels and selected states. If `Search` is visibly active, report `Search: enabled`; if `DeepThink` is gray, report `DeepThink: off`. If either state is ambiguous, stop and correct or report the ambiguity before sending.
- A response's self-description cannot override the visible `Search` state. If DeepSeek says it cannot see the mode or gives a conflicting description, treat that as a limitation of the reply and preserve the UI-based result.
- Do not infer that `DeepThink` was enabled merely because a completed response displays an internal-looking indicator such as `Thought for N seconds`. DeepSeek may show such an indicator while `DeepThink` is visibly off. Report `DeepThink: off/not selected` from the control state unless the user explicitly requested it and the control is visibly selected.
- Do not treat a model name stated only in DeepSeek's answer (for example, `DeepSeek-V3`) as verified. Record the model as `not visibly exposed` unless the interface itself shows the model name or version.
- If the interface exposes model names or versions, choose the newest suitable general-purpose model using visible labels, version numbers, dates, or explicit `Latest`/`Newest` badges. Never hard-code a model name as permanently current.
- If no model picker or version is visible, record `model: not visibly exposed` rather than guessing. If no reasoning control is visible, record `DeepThink/Thinking: not visibly available` and do not simulate it with prompt wording.
- Recheck and set the colors for `Search` and `DeepThink` immediately before every send because DeepSeek may reset or change the selected mode after a response or when a new chat is opened; leave `DeepThink` gray/off unless explicitly requested.

## Chat isolation and ChatGPT pairing

- Pair each new ChatGPT task/chat with a new DeepSeek chat whenever DeepSeek is used for that task. Do not continue an older DeepSeek conversation merely because the session or mode is still available.
- When a new ChatGPT chat is created or the subject changes, open a new DeepSeek chat through the visible control, verify that the conversation header or URL changed, and re-check the visible model and `Search` state.
- Keep each pair isolated. Do not paste or reuse context from an older DeepSeek chat unless the user explicitly asks to continue that same subject.
- For a follow-up in the same ChatGPT task, reuse the paired DeepSeek chat only when the subject, source material, assumptions, and reviewer role are unchanged.

## Run a review

1. Create a new DeepSeek chat for an independent task unless the user explicitly asks to continue an existing DeepSeek conversation.
2. Formulate a focused prompt with the question, facts, constraints, and reviewer role. Ask for missed errors, alternative interpretations, unsafe assumptions, and the minimum evidence needed to resolve uncertainty.
3. Send the prompt through the visible composer. Sending a task to DeepSeek is an external transmission; ensure the included material is authorized for that destination.
4. Wait until generation visibly completes. Read the complete response, including tables, code, citations, and continuation controls.
5. For difficult or disputed results, ask a targeted follow-up in the same paired chat: first request concise claims and evidence, then request a red-team critique. Stop when the answer becomes repetitive or produces no new evidence.
6. If the DOM, selectors, chat URL, or layout changes, stop and re-inspect the visible state. Do not loop on stale selectors or blindly resend prompts.

## Synthesis and reporting

Compare DeepSeek's output with the primary analysis and available sources. Classify findings as:

- `CONFIRMED`: independently supported by supplied material or a primary source.
- `DEEPSEEK_CANDIDATE`: useful lead that still needs verification.
- `CONFLICT`: DeepSeek and the primary analysis disagree; state what would resolve it.
- `NOT_CHECKED`: the required interface, source, or artifact was unavailable.

When DeepSeek was used, state briefly the visible model label (or that it was not exposed), DeepThink/Thinking status, number of rounds, and its role. Do not expose credentials, cookies, hidden reasoning, or session-bound URLs.

## Failure handling

Use `STOP -> CAPTURE -> MATCH -> RUN -> VERIFY`:

- `STOP`: stop after CAPTCHA, login failure, bot block, origin change, repeated timeout, or a changed UI.
- `CAPTURE`: record the current visible URL origin, page title, visible DOM, and screenshot when needed; redact sensitive values.
- `MATCH`: identify expired session, outage, rate limit, selector/layout change, incomplete generation, or browser transport failure.
- `RUN`: make at most one low-risk recovery attempt, such as waiting briefly or reloading once. Do not evade site safeguards.
- `VERIFY`: require a positive visible signal—signed-in DeepSeek, active visible `Search` mode, and completed response—before claiming the review was performed.

Never silently substitute a DeepSeek API, another account, another model, or a different service when the user requested DeepSeek Web. If the browser cannot reach DeepSeek or its quota is exhausted, report the exact blocking stage and continue the primary analysis without pretending DeepSeek was consulted.
