# Step-by-step guide after installation

Advance in stages when first configured. Each stage first explains the goal, then allows the user to complete or authorize the necessary actions, run verification, and only enters the next stage if it passes. Don’t throw all the questions to the user at once, and don’t ask the user to paste the contents of the authentication file into the chat.

## Phase 1: Initializing the running configuration

1. Run in the Skill directory:

   ```bash
   python3 scripts/configure.py init
   python3 scripts/configure.py status
   ```

   Existing installations should run the same `init` command once after upgrading the Skill. It adds newly introduced safe configuration fields and state files without replacing configured values or runtime files.

2. Ask and write the running configuration one by one: store name, public storefront URL, default language, time zone, customer service Gmail, merchant platform/OMS, and any separate policy source.
3. After the merchant provides the storefront URL, completely read [storefront-discovery.md](storefront-discovery.md), then run:

   ```bash
   python3 scripts/discover_store.py --url https://store.example --confirm-owner-request
   python3 scripts/configure.py path store-discovery
   python3 scripts/configure.py status
   ```

   Replace the example URL with the exact merchant-supplied public URL. This first discovery changes operator-owned runtime state, so do not run it until the current owner confirms the request. Show the detected platform, product count, policy sources, campaign evidence, warnings, and the public-only limitation. Ask the merchant to confirm the domain and findings, then run `python3 scripts/configure.py storefront confirmed --confirm-owner-request`. Do not request store admin credentials for discovery.
   If the script fails because the runtime cannot fetch or render the public site, follow the guarded browser fallback in `storefront-discovery.md`. Use OpenClaw's browser/browse capability only for read-only navigation to the same owner-approved merchant URL, show the fallback method and sources, then import the structured result only after a current owner request with `scripts/import_browser_discovery.py --confirm-owner-request`; show the imported result and complete `storefront confirmed --confirm-owner-request` separately.
4. Explain that URL discovery reads only public storefront pages. It cannot retrieve customer purchases, complete orders, payments, private inventory, unpublished promotions, or customer-specific eligibility; those still require the authorized connector in Phase 5.
5. If the merchant has no public storefront, obtain the current owner’s confirmation, run `python3 scripts/configure.py storefront none --confirm-owner-request`, and continue. Do not invent a URL or crawl a marketplace search result.
6. Explicitly default to `draft_only`. The owner may change the global automatic-send setting at any time, but it never enables any exact category by itself. A known sent Draft later creates a category-confirmation event.
7. Run `python3 scripts/configure.py verify`.

Passing criteria: the running directory exists; `config.json`, `system-prompt.md`, `workflow.md`, `persona.md`, `user_memory.md`, `auto_reply_permissions.json`, and `pending_category_confirmations.json` are readable; storefront discovery has produced a source-traceable `store-discovery.json` or the absence of a public storefront is recorded; the default prompt words are at least 100 rules; and the AI statement text is complete.

## Phase 2: Configuring OpenClaw

1. Check the machine:

   ```bash
   openclaw --version
   openclaw status
   openclaw doctor
   openclaw skills check
   ```

2. Guide the user to run `openclaw onboard` before completing the basic configuration; do not reset the existing configuration.
3. Confirm that the Gateway is available and the model and Agent are calling normally.
4. If the skill is not discovered, prefer the versioned registry release. Confirm the installed path before proceeding; do not install a second shared/global copy:

   ```bash
   openclaw skills install @ecomagenttools/ecommerce-gmail-customer-service --version 1.2.8
   openclaw skills info ecommerce-gmail-customer-service
   ```

   For a reviewed local checkout, use `openclaw skills install /absolute/path/ecommerce-gmail-customer-service` without `--global`.

Passing criteria: `openclaw status` No blocking errors, visible to Skill.

## Phase 3: Configure Google Cloud and Gmail OAuth

Only bootstraps one page at a time and does not create or upload keys for the user.

1. Install and verify `gog`:

   ```bash
   brew install gogcli
   gog --version
   ```

2. Open [Google Cloud Console](https://console.cloud.google.com/) and create or select a project dedicated to this customer service agent. Different projects should be used for testing and production.
3. Open the [Gmail API page](https://console.cloud.google.com/apis/library/gmail.googleapis.com) and enable the Gmail API.
4. Open [Google Auth Platform](https://console.cloud.google.com/auth/overview):
- Configure the application name, user support email and developer contact email.
- Select Internal (same Workspace organization only) or External (personal Gmail/external users).
- Add customer service Gmail to Test users in Testing state.
- Inform users: External + Testing authorizations requesting Gmail user data typically expire after 7 days; long-term automation requires configuration of publishing status and verification according to Google's current policies and cannot be bypassed through scripts.
5. Open [OAuth Clients](https://console.cloud.google.com/auth/clients), create an OAuth client of type `Desktop app`, and download JSON.
6. Users are required to save JSON in a private path on the local machine, and set the file permissions to readable only by themselves; never put it in the warehouse, cloud disk shared directory, Agent workspace or chat.

> **Need help before importing Google OAuth?** If the user encounters difficulties, they can consult the [OpenClaw Gmail customer-service workflow guide](https://ecomagenttools.com/blog/openclaw-gmail-customer-service-workflow) before continuing.

7. Import and authorize:

   ```bash
gog auth credentials set /absolute path/client_secret.json
   gog auth add support@example.com --services gmail --gmail-scope full --force-consent
   ```

If the browser callback is not available, check `gog auth add --help` first, and then use the `--manual` or `--remote` process provided by the current version.
8. Verification:

   ```bash
   gog auth status
   gog auth list --check
   gog gmail search 'newer_than:7d' --max 1 -a support@example.com -j
   ```

9. Explanation of permissions: Read + Tag + Create Draft + Send requires full Gmail permissions. If the user only wishes to authorize read-only, the Skill can only perform analysis and cannot automatically generate Gmail drafts or send them.

Passing criteria: Gmail search returns successful or legitimate empty results; OAuth JSON does not enter the workspace; token is saved in the system keychain/approved secret store.

## Phase 4: Ask and execute past 30 days email learning

After Gmail has successfully read it, ask as it is:

> Gmail can now be read normally. Do you allow me to read the emails from this customer service mailbox in the past 30 days to summarize your response tone, common words and how you handle different customer issues? By default, attachments are not downloaded and original emails are not saved. Only the desensitized summary is written to the local user_memory.md. You can decline or close anytime later.

### User disagrees

1. Record the user's refusal in the onboarding report. Do not change `learning.enabled` or `memory.usage_enabled`: each is a separate choice made later for normal operation.
2. Do not perform historical searches or write an onboarding history summary. This does not prevent the owner from later enabling ongoing Draft-edit learning, and it does not affect standard customer service classification, order matching, policy verification, or draft generation.
3. Continue with stage 5.

### User agrees

1. Completely read [learning-workflow.md](learning-workflow.md) and run:

   ```bash
   python3 scripts/configure.py path user-memory
   ```

2. First confirm that this is a dedicated customer service email. If it contains personal or employee emails, users are required to provide customer service labels, recipient aliases, sending domains or other ranges; full mailbox scanning is not allowed without a range.
3. Pull all pages in the past 30 days, and do not download attachments by default:

   ```bash
   gog gmail search 'newer_than:30d' --all -a support@example.com -j
   ```

Pull the complete thread for the results that can be identified as customer service contacts, and use the manual responses sent by the merchant as the main sample. Exclude automated notifications, marketing blasts, internal emails, spam, and system receipts.
4. First summarize the user's title, opening, empathy, formality, sentence length, structure, common words, avoid words, commitment expression, ending and signature. Show the desensitization results and ask: “Do you want to use this tone and style of speech?”
5. Only after the user confirms the inheritance or confirms the revision, the style profile is marked as `approved`. It cannot be enabled silently without confirmation.
6. Divide the customer issues in historical emails into atomic demands and classify them according to the first, second and third levels of `intent-taxonomy.csv`; use `intent_id::scenario_key` to summarize the verification items, processing steps, common phrases, restrictions, upgrade points and the number of historical evidence.
7. After the owner confirms the current write, write `user_memory.md` through the onboarding-only command below. This does not turn on ongoing Draft-edit learning or enable use of the memory for future Drafts. No original text, name, email, address, order number, tracking number, payment or identifying information shall be entered into memory.

   ```bash
   python3 scripts/user_memory.py merge \
     --source onboarding \
     --input <desensitization-update.json> \
     --confirm-owner-request \
     --delete-input
   ```

8. Explain to users: `user_memory.md` is a desensitized summary of their past customer service responses. It participates by default as a reference for expression and compliance solution selection; the owner may later turn `memory.usage_enabled` off. Orders, policies, laws and security access control always take priority. View it with:

   ```bash
   python3 scripts/configure.py path user-memory
   ```

   Do not manually edit individual classification playbooks. Controlled onboarding, sent-Draft, or Draft-edit merges update memory; automatic-reply permissions are stored separately and the owner may independently clear all long-term memory or disable one/all category switches.

Passing criteria: Agree or rejection has been recorded; if agreed, the search scope and sample statistics have been desensitized and reported, the tone has been confirmed by the user, historical cases have been written into `user_memory.md` according to three-level classification, and the original email and attachments have not been placed on disk. This one-time onboarding choice has not silently changed ongoing Draft-edit learning, memory-use, or automatic-send settings.

## Phase 5: Connect merchant orders, products, activities, and policies

1. Start with the detected public storefront platform as a hint, then ask the merchant to confirm every actual order system: Shopify, WooCommerce, Amazon, eBay, Etsy, Walmart, BigCommerce, Wix, other marketplaces, self-built ERP/OMS, or a combination. Detection must not be treated as authorization.
2. State the boundary before asking for a credential: public discovery can supply only public product, campaign, and policy evidence. Order lookup, private customer/order data, fulfillment/tracking, private inventory, historical entitlement, and customer-specific eligibility require an authorized API connector. Do not log in to or scrape an admin page as an alternative.
3. Completely read [platform-connectors.md](platform-connectors.md), then show the merchant the selected platform's official documentation links and capability row. Explain whether the platform has a first-party customer resource or only order-associated buyer data. The table describes vendor capabilities; this bundled Skill does not itself include a native connector, OAuth callback service, or secret store for any listed platform.
4. For each selected platform, guide the current owner through one choice:
   - **Existing approved connector:** open the linked official authorization path, authorize the connector with the minimum read capabilities, and confirm which contract operations it actually supports.
   - **Custom connector:** an authorized technical operator follows the linked official vendor guide to create/install the app or create/retrieve the platform credential. Request only the initial read permissions needed for `find_customer`, `list_recent_orders`, `get_order`, `get_product`, `list_campaigns`, and `list_policies` that the platform truly exposes.

   The Agent may provide the official links and explain the steps, but must not create the app, click consent, receive a secret, or copy a token from a portal. The merchant/operator must put raw credentials only in the approved connector's OS keychain, secret manager, or deployment-secret store. Never paste a client secret, API key, access token, refresh token, authorization code, private key, or password into chat, Gmail, `user_memory.md`, reports, the repository, the Agent workspace, `config.json`, commands, or browser-discovery files. Record only non-secret connection metadata and a secret-manager reference in controlled connector configuration.
5. Press [merchant-data-contract.md](merchant-data-contract.md) to configure the read-only connector. Initially allow only `find_customer`, `list_recent_orders`, `get_order`, `get_product`, `list_campaigns`, and `list_policies`. A marketplace connector may support `find_customer` and customer-scoped `list_recent_orders` only through a verified order-associated buyer match; it must not claim arbitrary email lookup or arbitrary customer-history lookup when the marketplace has no general customer API.
6. Connectors that put client input into shell, SQL, or URLs without parameterization are not accepted. All calls must be parameterized, return structured JSON, identify source/stable ID/retrieval time, and fail closed on missing permission, mismatch, timeout, or conflict.
7. Combine the public discovery snapshot with authenticated sources only under the precedence and applicability rules in [storefront-discovery.md](storefront-discovery.md). Public data may fill product descriptions and identify candidate policy or campaign sources, but it cannot prove purchases, order status, inventory, historical terms, or customer eligibility.
8. Verify with a masked, non-writing test client for each platform:
- Ability to pull recently purchased items and trace them back to a complete order;
- Ability to return fulfillment/tracking only when the chosen source actually provides it;
- Ability to state the customer-match method or a safe no-match/insufficient-permission result;
- Ability to pull current activities where a source exists;
- Ability to read the source, region and version of the refund/return policy;
- Correct platform, store/seller identifier, environment, scopes/capabilities, connector version, and secret-manager reference are recorded without the secret value.
9. Write operations (cancellation, refund, address change, shipment update, product update, etc.) remain closed. A later write connection needs a separately designed connector, explicit owner approval, and retesting; vendor support for writes does not enable it here.

Passing criteria: All four types of context have real sources and crawl times; every selected platform has passed the controlled read-only connector test or has an explicit limitation recorded; raw credentials have never entered the Skill runtime; and when a connection fails, the Agent turns to manual work instead of guessing.

## Phase 6: Create a dedicated Agent, name, and persona

1. Ask the user for the desired Agent name and service temperament. If the user does not modify it, use: Mia, energetic, patient, sincere, clear, not overly enthusiastic, and willing to handle complex problems step by step.
2. Make clear that the persona affects tone only. It must not introduce personal details, fabricate personal experience, or change facts, policies, permissions, or escalation rules.
3. Create an independent Agent workspace (the name and path can be changed by the user):

   ```bash
   openclaw agents add ecommerce-mail --workspace ~/.openclaw/workspace-ecommerce-mail
   openclaw agents set-identity --agent ecommerce-mail --name 'Mia' --emoji '📨'
   ```

4. Copy `assets/agent-AGENTS.template.md` to `AGENTS.md` of the new Agent workspace, and replace `<SKILL_DIR>` with the actual absolute path. Do not overwrite the existing `AGENTS.md`; if it already exists, show the differences first and merge them.
5. Review the running persona and show its local path with:

   ```bash
   python3 scripts/configure.py show persona
   python3 scripts/configure.py path persona
   ```

6. `openclaw agents set-identity` controls the interface name; the running version `persona.md` controls the email writing style. The two names should be consistent.

Passed criteria: The exclusive Agent can call this Skill; the name, personality and boundaries are confirmed by the user.

## Phase 7: Review system prompts, workflow, user memory and AI claims

1. Inform the user that the default system prompt word baseline is located at:

   ```text
   <SKILL_DIR>/assets/default-system-prompt.md
   ```

This baseline is read-only and must not be modified and is used for recovery.
2. The actual running version path is displayed by `python3 scripts/configure.py path system-prompt`. Review it read-only with:

   ```bash
   python3 scripts/configure.py show system-prompt
   python3 scripts/configure.py path system-prompt
   ```

3. Restore when the prompt word is changed:

   ```bash
   python3 scripts/configure.py restore system-prompt --confirm-owner-request
   ```

The current version will be automatically backed up before restoring.
4. Clearly tell users: The workflow for replying to customer emails is in the running version `workflow.md`; view it read-only and show its path with:

   ```bash
   python3 scripts/configure.py show workflow
   python3 scripts/configure.py path workflow
   ```

   If the owner wants to modify a runtime file manually, show its path and let the owner use their own desktop editor. This Skill never launches an editor or another external program.

5. Clearly tell users: past reply methods and later Draft-edit learning results are saved in the running version `user_memory.md`; view it read-only with:

   ```bash
   python3 scripts/configure.py show user-memory
   python3 scripts/configure.py path user-memory
   ```

   Do not manually edit individual classification playbooks. The controlled memory commands update or clear long-term memory. Independent category permissions are viewed with `python3 scripts/configure.py show auto-reply-permissions` or `python3 scripts/auto_reply_permissions.py status` and are enabled or disabled only through their own confirmation commands.

6. Ask the user whether to insert the following original text:

> This email is automatically processed by AI. If manual processing is required, please include the words "requires manual processing" in your reply.

Turn on or off:

   ```bash
   python3 scripts/configure.py set disclosure on --confirm-owner-request
   python3 scripts/configure.py set disclosure off --confirm-owner-request
   ```

7. Explain that existing long-term memory guides newly generated Drafts by default once it contains approved, applicable entries. Ask the owner whether to keep that default or turn it off. This setting affects only Draft-generation context; turning it off still permits a standard system-prompt, order-evidence, and policy-based Draft, and does not change automatic-send settings.

   ```bash
   python3 scripts/configure.py set memory-usage on --confirm-owner-request
   python3 scripts/configure.py set memory-usage off --confirm-owner-request
   ```

8. Separately ask the owner whether to enable ongoing Draft-edit learning after onboarding. The default is off. If enabled, a later owner edit to an AI-generated Draft may be automatically detected, redacted, compared, and summarized into long-term memory. It does not authorize another historical-email import and does not change memory-use or automatic-send settings.

   ```bash
   python3 scripts/configure.py set learning on --confirm-owner-request
   python3 scripts/configure.py set learning off --confirm-owner-request
   ```

9. Explain the global automatic-send switch. Recommend keeping it off until draft-only testing is complete, but make clear that the owner may explicitly change it at any time. There is no recipient or domain allowlist, and the global switch does **not** approve any category. This is independent of whether `memory.usage_enabled` is on for Draft generation.

   If the owner declines, record it explicitly:

   ```bash
   python3 scripts/configure.py set auto-send off --confirm-owner-request
   ```

   If the owner chooses to enable it now, turn on the global setting. It permits later category sends but does not send the first email in any category automatically:

   ```bash
   python3 scripts/configure.py set auto-send on --confirm-owner-request
   ```

   Do not approve historical or existing playbooks during onboarding. During later real use, a known AI Draft sent by the owner in Gmail, or sent after the owner confirms in OpenClaw, creates a short-lived category-confirmation event. It does not enable anything. Record the safe identifiers and categories:

   ```bash
   python3 scripts/auto_reply_permissions.py record-sent \
     --source gmail-sent \
     --draft-id <SENT_DRAFT_ID> \
     --thread-id <THREAD_ID> \
     --sent-message-id <SENT_MESSAGE_ID> \
     --input /controlled-temporary-directory/atomic-issues.json \
     --delete-input
   ```

   Then show every category separately and turn on only each category the owner explicitly confirms:

   ```bash
   python3 scripts/auto_reply_permissions.py confirm \
     --event-id <EVENT_ID> \
     --intent-id '<INTENT_ID>' \
     --scenario-key '<SCENARIO_KEY>' \
     on \
     --confirm-owner-request
   ```

   Per-category approval requires a current owner request and confirmation event; it does not require `learning.enabled` or an approved `user_memory` playbook. `status=approved` by itself never permits automatic sending, and no category is approved implicitly during onboarding, history import, or ordinary memory merge. A multi-issue Draft can lead to separate A and B confirmations; later emails containing A, B, or both need no new question only after each exact category has been confirmed. Categories are not deleted: the owner can disable one, or all, independent switches.
10. Long-term memory has no automatic retention limit. If the owner wants to remove it, explain that this clears all long-term memory and requires a second explicit confirmation. This does not disable or delete any category permission:

   ```bash
   python3 scripts/user_memory.py clear --confirm-owner-request --confirm-delete-all
   ```

11. Let users review the system prompts section by section, paying special attention to: regional policies, refund permissions, compensation ceilings, manual upgrades, privacy retention, one-time historical import, ongoing Draft-edit learning, existing-memory use, and the independent category-permission model.

Passing criteria: The user explicitly confirms the prompt words, workflow, memory, and category-permission file locations, ongoing Draft-edit learning status, existing-memory-use status, AI declaration switches, and the global automatic-send choice. If global automatic sending is on, no category is automatically approved during onboarding; each category requires its later owner-confirmed sent-Draft event. Running `python3 scripts/configure.py verify` is successful.

## Phase 8: Create Gmail labels and a disabled scheduled task

1. Press [gmail-operations.md](gmail-operations.md) to create `ECS/ToProcess`, `ECS/Drafted`, `ECS/Sent`, `ECS/Human`, `ECS/Error`, and list the existing tags before creating.
2. Ask users about pull frequency and quiet periods. Record an exact IANA timezone and the owner-approved quiet-hours policy. A timezone or quiet-hours value may never be inferred from the machine, the Skill author, or a previous merchant.
3. Before any cron command, ask the current owner to explicitly confirm both values, then record and verify them:

   ```bash
   python3 scripts/configure.py schedule \
     --timezone '<USER_CONFIRMED_IANA_TIMEZONE>' \
     --quiet-hours '<USER_CONFIRMED_QUIET_HOURS_OR_NONE>' \
     --confirm-owner-request
   python3 scripts/configure.py verify --require-schedule
   ```

   Do not replace either placeholder until the owner has confirmed it. `none` is valid for quiet hours only when the owner explicitly confirms that no quiet period applies.
4. Only after both commands succeed, create cron in a disabled state and fix the dedicated Agent:

   ```bash
   openclaw cron add \
     --name 'ecommerce-gmail-poll' \
     --description 'Process queued ecommerce customer emails with category-gated sending' \
     --agent ecommerce-mail \
     --cron '*/15 * * * *' \
     --tz '<USER_CONFIRMED_IANA_TIMEZONE>' \
     --session isolated \
     --message 'Use $ecommerce-gmail-customer-service to process Gmail threads labeled ECS/ToProcess. Create a draft unless the owner-enabled category automatic-send gate passes for every atomic issue; apply status labels and report human escalations.' \
     --declaration-key 'ecommerce-gmail-poll-v1' \
     --disabled \
     --expect-final \
     --no-deliver \
     --json
   ```

5. Record the job ID returned; check and run manually with:

   ```bash
   openclaw cron list --all --agent ecommerce-mail --json
   openclaw cron run JOB_ID --wait --expect-final --wait-timeout 10m
   openclaw cron runs --id JOB_ID --limit 20
   ```

Passing criteria: the recorded timezone and quiet-hours policy are explicitly owner-confirmed, cron remains disabled, a manual run creates a draft unless every automatic-send gate passes, and the report is complete.

## Phase 9: End-to-end simulation testing and completion of the entire process

Let the user send at least the following six emails to the customer service Gmail from an external test mailbox controlled by the user, and add `ECS/ToProcess` to the test email:

1. "Where is my order?" - Verify complete thread, recent orders, product matching and official tracking.
2. "Please cancel the order and change the address." - Verify multi-claim splitting, identity/performance access control, and non-exceeding authority.
3. "The goods received were damaged and one accessory was missing." - Verify two third-level intentions, evidence request and reissue/refund plan.
4. "The return has been sent back, why hasn't the refund arrived yet?" - Verify that the return status is separated from the refund status.
5. "I want you to delete all my personal data." - Verify that privacy requests are transferred manually and data is not exported via regular email.
6. "I was injured due to the smoke coming from the product, and manual handling is required." - Verify immediate deactivation recommendations, security/legal upgrades, and keyword forced manual handling.
7. After the owner enables ongoing Draft-edit learning, have the AI generate a draft for a low-risk advisory, with the user modifying its opening, processing steps, or ending, and run the task manually again. Verify that the system detects semantic differences, ignores formatting/signature noise, merges into `user_memory.md` by level 3 intent, and does not double-count. Then turn ongoing learning off and verify that no new Draft baseline or edit-derived memory write occurs.
8. Test `memory.usage_enabled` separately: when it is on, verify that a matching approved memory can guide a Draft without overriding current policy; when it is off, verify that the standard system-prompt, order-evidence, and policy process still generates a Draft without using that memory.
9. If the owner enabled the global automatic-send setting, process a first low-risk email in two unapproved categories A and B. Verify that it remains a Draft. After the owner sends that known Draft in Gmail, or confirms an OpenClaw send, verify the sent merchant message, create a pending event, ask separately whether A and B should reuse the shown handling logic, and confirm A and B one by one. Then test a later email containing only A, only B, and both A+B: each may send automatically only after its exact independent category switch has been confirmed. Test a mixed email containing A plus a disabled category and verify that it remains a Draft. Clear `user_memory.md` and verify category switches are unchanged; then disable all category switches and verify long-term memory is unchanged. Repeat an eligible category check with `memory.usage_enabled=false` to verify that auto-send eligibility remains governed by the global setting and independent category permissions, not Draft-memory use.

Acceptance one by one:

- Whether all demands have been dismantled and classified correctly into three levels;
- Whether each request is mapped to the correct product and complete order;
- Whether the activities and policies of the correct region, channel, and time version are quoted;
- Whether to generate only one original thread draft;
- Whether the AI statement switch is accurate;
- Whether the manual email is added with `ECS/Human` and there is no automatic reply;
- Is there no sensitive information, fictitious promises, duplicate drafts or mislabeling.
- When `memory.usage_enabled` is on, whether the applicable memory is retrieved after the product and complete order are matched, and whether the memory does not overwrite the current policy; when it is off, whether the standard process still creates a Draft without using memory.
- When ongoing Draft-edit learning is turned on, whether an owner edit is safely detected and generalized; when it is turned off, whether no new baseline or edit-derived memory write occurs.
- When automatic sending is globally enabled, whether the first unapproved category still remains a Draft, whether a known sent Draft only creates a pending event, whether every atomic issue must have its own owner-confirmed independent switch, whether memory clearing and permission disabling remain independent, and whether a mixed email with any disabled category remains a draft.

Retest all failed test cases after correction. All passed, and then obtain the user's explicit consent to enable cron:

```bash
openclaw cron enable JOB_ID
```

Cron does not itself enable automatic sending. If the owner enables the global setting, they must first confirm each eligible `intent_id::scenario_key` category separately after a known sent-Draft event, test both an eligible email and a mixed email with a disabled category, and confirm that all hard stops still return the thread to draft mode.

Finally report to the user: Gmail account, confirmed storefront URL and last public discovery time, Agent name, the running file and category-permission paths, learning status and historical scope, AI statement status, merchant connector, cron ID/frequency/time zone, test results, types that still require manual work and automatic sending status. No export of keys, tokens, original historical emails, or customer personal information is allowed.
