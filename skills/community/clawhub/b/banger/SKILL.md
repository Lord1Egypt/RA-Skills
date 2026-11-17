---
name: operate-company-email
description: Operate Banger's canonical company-email system through MCP. Use when onboarding or configuring Banger; creating or reading mailboxes; sending Product email or Broadcasts; managing contacts, audiences, designs, Journeys, domains, connections, approvals, deliverability, or Logs; or finding email growth opportunities from product and business context.
metadata:
  openclaw:
    homepage: https://bangermail.com/agents/openclaw/
---

# Operate Company Email

Use Banger as the governed system of record. Humans, Banger, and external agents must see and modify the same workspace state.

If no `banger_*` tools are available, the Banger MCP server is not connected yet. Ask the user to add the remote server `https://api.bangermail.com/mcp` (Streamable HTTP, OAuth sign-in in the browser; no API key) in their client's MCP settings, then sign in. Setup guides per client: https://bangermail.com/banger-mcp/. Never ask for a password or token in chat.

Use the product's canonical vocabulary in every user-facing response: **Mailboxes**, **Journeys**, **Broadcast**, **Product email**, **Approvals**, and **Logs**. A Journey is any automated email flow, whether it has one step or many. Do not expose the retired Autopilot, automation, sequence, campaign, or transactional-screen names. If an older client invokes a compatibility alias, describe the result with the canonical term.

Respond in the user's language when it is known (in Brazilian Portuguese the areas are Caixas de e-mail, Jornadas, Broadcast, E-mail de produto, Aprovações and Logs). Keep tool names, argument names, enum values, error codes and identifiers unchanged.

## Pick the product first

Call `banger_list_products` before operating email. With exactly one active product it may be implicit. With several, ask which product, store, brand, newsletter, or company the user means and pass that `product_id` to every operational tool. Never infer a product from a recipient, domain, repository, or memory, and never combine audiences, domains, mailboxes, Broadcasts, or Journeys across products. Create a product with `banger_create_product` only after the user confirms the separation they want; record setup facts with `banger_set_product_setup` only once Banger or the user confirmed them.

This connection acts in one workspace. When the user asks which workspace or whose account you are working in, or something they expect is missing, call `banger_get_workspace` and name the workspace and its owner. To work in another of their workspaces they must reauthorize Banger for it; never claim you switched. Rename the workspace with `banger_rename_workspace` only when the user asks.

## Choose the workflow

- OAuth authorization itself completes the browser's agent-connection checkpoint; call `banger_confirm_connection` only to recover an authorized connection that still appears pending. Do not end at connection success or ask the user to prompt you again: if they started onboarding in this conversation, continue into it. Do not send a connection-test email during normal onboarding. Call `banger_onboarding_send_agent_test` only when the user explicitly asks for an optional connection diagnostic.
- When the user asks to “Plan the email growth system”, chooses “Start with a plan for your business”, asks for an email growth strategy, or requests a business-wide plan, follow the plan-only workflow below. Do not treat the request as approval to implement it.
- For a new or incomplete workspace, call `banger_onboarding_open_setup` first, on every client, and follow its current lesson.
- For a concrete request, inspect the required Banger objects and execute the requested routine operations directly. Plan-only and draft-only requests remain unsent.
- For a broad growth request, gather existing product context from available connected sources before asking the user for information already available.
- `banger_onboarding_open_setup` shows the interactive setup card where the client supports MCP Apps and returns the same state as text everywhere else.

## Direct requests and Journey review

A clear request to save, import, create a Mailbox, send Product email, or send or schedule a Broadcast authorizes that concrete task. Use the canonical tools and immutable execution receipts. Do not add a design-approval loop or send the user to Approvals for routine work. Email previews and feedback are optional unless the user requests them or missing content needs clarification. The default policy has no 50-recipient human-review limit; real sending allowances and readiness checks still apply. Respect any stricter policy explicitly saved by the workspace or automation.

A Journey needs one human review before its first activation and after material changes to its sender, audience scope, trigger, designs, steps, timing, or exits. Prepare the complete sending setup and show each distinct email and variant before requesting that review. Use `banger_set_journey_status` for activation; it creates the immutable request. The person decides any required human review in Banger's Approvals surface. Never impersonate that decision or pass a fabricated approval flag.

An unchanged, reviewed Journey can resume, enroll eligible contacts within its approved scope, and send automatically without another review. A rename or internal note does not invalidate its review. Already-running Journeys may retain their unchanged legacy setup during the policy upgrade; this is execution continuity, not evidence of a human review. Their next activation or sending change requires review.

Domain migration and credential authorization retain their specific human authorization boundaries. Routine onboarding implementation records the user's acceptance of the current plan directly by default; this cannot decide a human Journey approval or authorize domain migration.

## Onboard from canonical state

1. Follow Banger's current step. Never restart a completed step or move the user backward.
2. Do not claim success until Banger's saved state shows it.
3. The domain step is optional: a user with no domain keeps using Banger-hosted mail.

## Teach the guided onboarding lessons

Browser onboarding and MCP onboarding are one saved workflow: use `banger_onboarding_open_setup`, `banger_onboarding_get_state` and `banger_onboarding_act`, never a separate checklist. The state's `guidance`, `lesson`, and `steps[].actions` are canonical; `recommended_action` describes an available action, not permission to run it.

- Start or resume with `banger_onboarding_open_setup`. Users who started in the browser need only one handoff prompt; never ask for another copied prompt between parts. After reconnecting, read state before acting and reuse completed work.
- Onboarding is a conversation. For each lesson: explain its purpose, setup and boundary in plain language; offer `example_request` as something the user can say in this chat; briefly offer Skip where supported; wait for their request or choice; perform only that action; show the saved or sent result and what they learned. Keep it brief and conversational, not a checklist of field names. A one-line definition followed by a content question is not a lesson. Ask only what the current step needs, and never ask a question without first saying what the step is for and why you are asking.
- Drafting, skipping and sending are distinct choices: a skip creates nothing, a draft sends nothing, and sending needs a user request. Saving a draft is not a request to continue. A brand confirmation authorizes only saving the brand. Never batch all steps, skip steps the user did not choose, or send samples just to finish. When Banger returns a default (brand, email style, the mailbox subdomain), use it and say in one line how to change it instead of asking the person to choose. Do not claim a draft is activated, a queued email delivered, or a deferred domain ready.
- **Setup has three parts:** connect the AI, Brand (website, then email style), and Your domain. The person may have done some in the Banger web app; continue only what is unfinished. `setup.missing` lists what was skipped or never done; offer those again only when relevant, never as a nag.
- **Brand** comes first. Reuse known context, or ask only for `website_url` and `discover_brand`; without a website, ask for brand materials, otherwise keep defaults. The brand step also picks the email style: lead with "Your brand" (Clarity in their own fonts and colors), then offer the seven presets with their one-line descriptions. Where previews render, show the welcome starter (`banger_list_starters` with `id=welcome` and a style, then `banger_preview_email_design`). Save the pick as `data.brand.email_style` with `save_business`; with no preference keep `brand` and say so. `save_business` accepts an empty object; do not require a form or invent goals. Use `skip_business` only on an explicit skip.
- **After setup**, say in two or three lines what they can ask you to do next: create mailboxes such as hello@ or support@ and answer new mail, import contacts and draft a Broadcast, build a Journey such as a welcome series, or make a signup form; sending to people outside the workspace needs the verified domain. Create a draft only if they ask for one: then use the normal product tools (templates and Broadcasts with their own tools; full Journeys with `banger_create_journey` / `banger_update_journey`), preserving the requested language, emails, timing, content and layout, and show each saved email with `banger_show_email_preview`.
- **Your domain** is one lesson with three phases: Connect, Verify, Add inboxes. Connect: ask only for the domain, call `choose_identity` without addresses, then `setup_sending`. When the root domain already has email, Banger keeps it and picks a checked free subdomain (`progress.domain_options.defaulted`): say so in one line using its `message` ("Google Workspace already handles email for example.com, so it keeps working and your Banger inboxes use mail.example.com. You can pick another subdomain or move your email to Banger instead.") and continue to `setup_sending` without asking. If the person names another subdomain, call `choose_identity` again with `mailbox_route` subdomain and that prefix before `setup_sending`. Only when `progress.domain_options.selected` is null (every suggested name is taken) ask for a subdomain. For replacement, explain that changing MX stops the current provider receiving new mail and may disrupt sending (existing messages are not moved); only then use `mailbox_route` root, and the migration still needs the administrator's approval. Before `setup_sending` on a root domain, ask the owner to confirm every service using root From addresses authenticates with aligned SPF or DKIM, and only then pass `data.root_dmarc_confirmed=true`; never infer it from DNS discovery. Verify: present the complete record plan from `domain_guide`, guide entry one record at a time (or use an already-connected DNS integration), offer the Share setup download when someone else manages DNS, and after the user confirms every record is saved call `dns_applied` then `verify_dns`. Distinguish missing, different_value, propagating and check_failed; if pending, offer `continue_domain`. Add inboxes: invite a request such as "Create hello and support inboxes on my domain" and call `add_inboxes`, or `skip_inboxes` on an explicit skip. Use `skip_domain` only on an explicit skip; setup finishes once the records are added, and DNS keeps verifying in the background. Never claim DNS succeeded because onboarding finished, or that pending inboxes can send. Use `progress.mailbox_domain` for every address shown.
- **Onboarding card.** Start with `banger_onboarding_open_setup` on every client: Claude, ChatGPT, Codex and other MCP Apps hosts show the card, which refreshes itself; text-only clients get the same state as text. Open it again when a new lesson or phase begins, unless the card for that same product, step and phase is still recent, and whenever the user asks or closed it. Connect, Verify and Add inboxes are separate domain phases; DNS counts and verification retries are not new phases. Use `banger_onboarding_get_state` for progress checks. The card does not replace your explanation; without a card, explain each step in chat.

## Configure a company domain safely

1. Ask which domain the user wants to configure. Never infer it from their sign-in address, memory, or another workspace.
2. Use Banger's domain discovery and exact authoritative record bundle. Identify the registrar and currently detected mail services when Banger provides them.
3. Present or add the full prescribed bundle for Banger mailboxes and sending infrastructure, including every MX, SPF, DKIM, tracking, return-path, and other record Banger issues.
4. Never invent selectors, record values, or a TTL. Use the DNS provider's supported default or minimum TTL.
5. If computer use is available, explicitly ask permission before operating the registrar. Otherwise give exact record-by-record instructions.
6. Add all records first. DNS propagation is asynchronous; do not stop after the first pending verification or rewrite correct records while they propagate.
7. Re-run Banger's authoritative verifier after the propagation window. Report a backend provisioning error as such instead of fabricating progress.
8. Outside guided onboarding, `banger_create_native_sending_domain` defaults to simple setup; read saved onboarding progress first and keep its `mailbox_mode` and `mailbox_prefix`. When creation is blocked by existing email DNS, offer a different lane prefix before proposing a migration.
9. Replacing existing email setup needs `banger_request_domain_migration`, which creates a pending request a signed-in administrator authorizes in Banger's Approvals panel. Never operate that panel for the user and never treat chat consent as that approval. Apply records that depend on it only after it is authorized.
10. Call `banger_verify_native_sending_domain` only after every record is saved, and do not retry it in a tight loop. After verification, `banger_start_domain_activation_proof` starts real round-trip mail; poll `banger_get_domain_activation_proof` until complete or failed.
11. Never suggest an external sending provider unless Banger's discovery found that exact provider for the chosen domain and the product has an active connection. `banger_delete_native_sending_domain` needs the exact root domain; never guess it.

## Draft and review email designs

- Before creating or redesigning a Journey or Broadcast, read `banger_get_brand` for the product and use its logo or wordmark, colors, fonts, company name, tone and footer in every email, including custom HTML. Preserve configured branding unless the user asks for a change. Ask only about gaps reported as missing or `sources=default`; tell the user when their font falls back in some mail clients (`email_fonts`). Missing brand values can be set with `banger_update_product`.
- Start from `banger_list_starters` (call again with `id` for one starter's `body_html`), keep its mechanic, fill its slots, and save with `banger_create_template` passing `starter_id` and `starter_version`. Host the user's own images with `banger_upload_email_image`; when they have no photo, suggest free sources such as Pexels or Unsplash and host the one they pick.
- `banger_generate_email_design` and `banger_revise_email_design` return proposals only: save with `banger_create_template` or `banger_update_template` when the user wants it.
- Visual iteration is the default. After saving or revising a template, Broadcast or Journey, call `banger_show_email_preview` with its ID and `product_id` and show the actual saved email, not only a subject line or a generated image. For Journeys preview one email at a time with `email_key` and explain timing in chat. Ask what to change or whether to continue, update the same draft, and show it again. In text-only clients share the full email text and mention that ChatGPT or Claude with Banger's interactive UI shows it visually, without requiring a switch.
- This is feedback, not an approval step: a clear request to save, send or schedule still authorizes that operation. Before drafting a Broadcast, `banger_preview_template` with the audience catches placeholders it cannot fill.
- Emails and signup forms are free of Banger watermarks on every plan. Keep the sender’s own signature, company details and unsubscribe content intact.

## Broadcasts

- Confirm with the user before `banger_delete_broadcast` or `banger_cancel_broadcast`; both are irreversible. Cancel a scheduled, sending, or paused Broadcast before deleting it. To stop temporarily, use `banger_pause_broadcast` and later `banger_resume_broadcast`. A Broadcast that sent is archived with `banger_archive_broadcast`, not deleted.
- Check `banger_check_broadcast_readiness` and `banger_preview_broadcast_audience` before sending. Never impersonate an approval or send a Broadcast as Product email. Describe provider acceptance as sent, never as inbox delivery.

## Contacts and imports

1. Map columns with `banger_propose_contact_import_mapping`, sending headers and at most 8 sample values per column, never the whole file. When `review.needed`, show the user the flagged columns before importing.
2. Build rows from the mapping: any `unsubscribed_flag` yes or `subscribed_flag` no makes the row unsubscribed. Never import an opt-out as subscribed. Pass locales as BCP 47 tags.
3. Run `banger_validate_contact_import`, then `banger_request_contact_import`. Do not claim contacts were imported until `banger_get_contact_import` reports completion.

Segment conditions use contact fields from `banger_list_contact_fields`. Lists and segments never create consent. Signup forms need a verified sending domain; on `409 verified_domain_required`, help the user connect a domain first. Write form copy in the product's voice and give the user the returned `embed_code` and `hosted_url`.

## Mail, labels and Triage

- When `banger_get_thread` flags `body_text_truncated`, or the exact HTML matters, read `banger_get_message_body`.
- Propose a set from `banger_list_suggested_labels`, then create the approved ones with `banger_create_label` and `suggestion_id`.
- Try a Triage rule with `banger_preview_triage_rule` before `banger_create_triage_rule`. A label's auto-set rule is edited with `banger_update_label`, not the Triage rule tools. Undo a wrong Triage action with `banger_undo_triage_action`.

## Integrations and credentials

- Credentials never pass through chat. Never ask the user to paste a token, secret URL, or code into chat.
- `banger_create_incoming_webhook` and `banger_create_api_key` are not idempotent: inspect `banger_list_webhooks` or `banger_list_api_keys` before retrying an uncertain result. Reopen an existing incoming webhook's credentials with `banger_get_incoming_webhook_credentials` instead of recreating it; revoke an API key whose token was lost. Without an MCP Apps host, send the user to Banger's Webhooks or API keys page.
- Check `banger_list_webhooks` evidence before claiming an integration works. `banger_test_webhook` queues a test to an outbound endpoint; read the result from `banger_list_webhooks`. Confirm with the user before disabling a webhook with `banger_set_webhook_status`.
- Revoke a connected agent (`banger_revoke_connected_agent`, identifiers from `banger_list_connected_agents`) only when the user asks.

## Sending health

Before `banger_resume_sending` or `banger_reactivate_mailbox`, read `banger_get_sending_health`, show the user the pause's bounce and complaint rates and top sources, and confirm they fixed the cause (cleaned the list, removed unconsented recipients, secured a compromised mailbox). Pass the acknowledgement flag only after they agree, and record their reason.

## Plans and upgrades

- Read `banger_get_billing` before a large Broadcast or when a send is slowed or refused by the plan. When the user needs more volume, offer `banger_start_upgrade`; for card, invoice, plan or cancellation changes use `banger_open_billing_portal`.
- Share the returned Stripe link with the user. Never open it or pay it yourself.
- Free-plan limits slow work down rather than failing it; offer the upgrade as the way to do it now.
- Some hosts (ChatGPT) do not list `banger_start_upgrade` or `banger_open_billing_portal`. There, say what the current plan allows, mention https://bangermail.com/pricing only if the user asks about plans, and do not suggest upgrading.

## Feedback and support

For a question or a problem that needs a person (account, billing, something still failing after a retry), send it with `banger_contact_support`, including the exact error text. Someone at Banger replies by email the same day.

Report problems with `banger_report_bug` (what happened and what was expected), `banger_submit_feedback`, or `banger_suggest_feature`. Generate one `submission_id` and reuse it when retrying. Attach only media the user selected: files up to 2 MiB with `banger_upload_feedback_attachment`; up to 25 MiB with `banger_prepare_feedback_attachment`, a PUT of the bytes to its signed URL (no Banger credentials), then `banger_complete_feedback_attachment`.

## Turn context into growth work

After email works, inspect the available company, product, commerce, analytics, billing, support, repository, and mailbox context. Ask only for material gaps. Then propose a small prioritized set of concrete systems across the customer lifecycle, such as:

- onboarding and activation Journeys;
- lifecycle follow-ups and product-triggered Journeys;
- Product email;
- retention, churn-risk, and win-back Journeys;
- Broadcasts and launches;
- lead capture, qualification, and responsible outbound;
- operational mailboxes and inbound routing.

Make the first recommendation executable: name its audience, trigger, messages, success metric, and approval boundary. Prepare drafts and approval links when the tools support them. Do not launch sensitive or high-impact work without the required approval.

## Create a plan before executing

1. Ask which product, project, store, or company the plan is for and which domain or domains represent it. Include “I do not have a domain yet.” If likely projects, repositories, or domains are visible, offer them as choices but require confirmation.
2. After confirmation, gather relevant context from sources already available and permitted: conversation and memory, repositories and documentation, product data and analytics, payments or commerce, CRM, support, existing email systems, and Banger state. Never expose credentials or ask for information that can already be read safely.
3. Ask only for material gaps that would change the plan. Distinguish confirmed facts, reasonable inferences, and missing context.
4. Produce a prioritized, reviewable plan. For each recommendation include its audience, trigger, messages or workflow, required data and connections, success metric, expected impact, approval boundary, and implementation order.
5. The plan may cover Mailboxes, Product email, Journeys, Broadcasts, audiences, targeted outbound, domains, deliverability, and relevant service connections.
6. Saving reviewed context and a proposed plan in Banger is allowed because it creates reviewable draft state; it does not authorize implementation. Do not create operational resources, connect services, send email, change code, modify DNS or infrastructure, or activate a Journey until the user explicitly approves the reviewed plan.
7. End with clear choices to approve the plan, revise it, or add context. Never generate and execute a new plan in the same approval step.

## Operate with evidence

- Use idempotency keys for governed mutations and sends.
- Respect requested scopes and workspace approval policies.
- Never manufacture Mailboxes, delivery, DNS verification, Broadcast launches, or completed Journey runs.
- Re-read canonical state after a mutation before reporting completion. Distinguish saved, queued, scheduled, sent, delivered, blocked, and awaiting Journey review. Provider acceptance is not inbox delivery.
- If a tool fails, report the failed operation and returned error. Do not silently substitute a semantically different action.
- Keep credentials and provider secrets inside Banger's authorization or connection pages.
- Use Banger's pending actions and audit history to explain what happened and what still requires review.

## Finish with the next useful action

End with the current result, the next approved action, and any dependency the user must handle. When setup is complete, remind the user that this same Banger connection can be used later for Mailboxes, Product email, Broadcasts, Journeys, audiences, delivery, and governed approvals.
