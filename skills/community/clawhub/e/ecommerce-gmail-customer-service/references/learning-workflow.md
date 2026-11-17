# One-time email history import and ongoing Draft-edit learning

## Table of contents

1. Authorization and privacy boundaries that cannot be bypassed
2. One-time 30-day onboarding history import
3. User confirmation tone scheme
4. Three-level classification processing plan
5. Continuous learning from manual modification of Draft
6. Retrieve memory before replying
7. Memory update JSON structure

## 1. Authorization and privacy boundaries that cannot be bypassed

- A historical-email import may start only once during onboarding, after the user explicitly agrees to the stated mailbox scope. It is not controlled by `learning.enabled`, and it must never be started later during ordinary email processing.
- `learning.enabled` is a separate, owner-confirmed setting for the formal operating period after onboarding. It controls only whether an owner’s later edits to an AI-generated Draft are automatically detected, compared, and summarized into new redacted memory.
- `memory.usage_enabled` is also separate. It controls only whether existing long-term `user_memory.md` may guide the content of a new Draft, and is enabled by default. Turning it off still permits a standard system-prompt, order-evidence, and policy-based Draft; it does not delete memory or change automatic-send approvals.
- Automatic sending is a third, independent rule: the owner may change the global automatic-send setting at any time, and every exact `intent_id::scenario_key` in an email must already have an enabled independent automatic-reply permission. A known sent AI Draft creates a confirmation event; only the owner's later category-specific confirmation enables that switch. The category gate does not read long-term memory.
- When the user rejects or does not answer the onboarding history question, do not search historical email. That choice does not enable or disable later Draft-edit learning, existing-memory use, or standard customer service processing.
- If the mailbox is not a dedicated customer service mailbox, first ask the user to provide the customer service label, sending domain, receiving alias or other Gmail query range; do not scan obvious personal or employee emails.
- The historical window is fixed to 30 days before the authorization time. By default, attachments are not downloaded, external links are not opened, the original text is not saved, or the complete email is exported.
- Only save the desensitization summary in the local running directory. Do not include name, email, phone number, address, order number, tracking number, payment information, identification, health information or other customer-specific information.
- Turning off ongoing Draft-edit learning only stops future baseline and memory writes from later edits; it does not erase prior memory or turn off `memory.usage_enabled`. Long-term memory has no automatic expiry. The owner may clear all of it only with the explicit whole-memory deletion command; independent category automatic-reply permissions remain unchanged.

## 2. One-time 30-day onboarding history import

After the mailbox reading verification is successful, ask as it is:

> Gmail can now be read normally. Do you allow me to read the emails from this customer service mailbox in the past 30 days to summarize your response tone, common words and how you handle different customer issues? By default, attachments are not downloaded and the original email is not saved. Only the desensitized summary is written to the local user_memory.md. You can decline or close anytime later.

After the user agrees:

1. Record the user’s current, explicit agreement to the stated scope in the onboarding record. Do not turn on `learning.enabled` merely because the user agreed to this one-time import.
2. For dedicated customer service emails, use `newer_than:30d` to pull all pages; for non-dedicated email addresses, first narrow the query to the label, alias or domain confirmed by the user.
3. Take the thread containing the reply sent by the merchant as the main sample, pull the receipt and sending text in the thread in the past 30 days, and reconstruct "Customer problem → Merchant reply → Follow-up results". Attachments are not downloaded.
4. Exclude automatic notifications, marketing mass mailings, internal emails, spam emails, pure system receipts, threads without customer questions and content that cannot be confirmed to be manual responses from the merchant.
5. Complete the analysis in memory; discard the original text after processing a batch, and do not create a corpus of original emails.
6. Output coverage: start and end dates, search query, number of threads, number of available manual replies, number of excluded items and reasons. Output and logs are desensitized.

## 3. User confirmation tone scheme

Summarize it first but don’t activate it directly. At least include:

- Address and opening method;
- Empathy intensity and apology usage conditions;
- Sentence length, paragraphs, bullet points and information density;
- Formality, intimacy, and initiative;
- Commonly used connecting sentences, endings, and signatures;
- Expressions of time, amount, commitment and uncertainty;
- Common words, words to avoid, and tone differences for customers with different emotions.

Show the desensitization summary to the user and explicitly ask if they want to continue using it. `user_memory.md` is written with `status=approved` only after the user confirms "inherit" or gives a revision and confirms it. If the user does not agree, continue to modify or keep `not_reviewed`, and cannot be enabled silently.

## 4. Three-level classification processing plan

Process historical cases after tone confirmation:

1. Break down each customer problem into atomic requests.
2. It must be classified according to the first, second and third levels of `intent-taxonomy.csv`; one thread can produce multiple third-level classification records.
3. Summarize each third-level intention: applicable scenarios, verification information, processing steps, available solutions, permissions or upgrade points, commonly used phrases, avoided phrases, amount of historical evidence, and confidence level.
4. Only summarize the handling methods actually used by merchants, and do not mistakenly write customer requirements, AI drafts, unexecuted commitments, or single exceptions as routine practices.
5. The same three-level intention can be split according to the scene key. For example, "cancel before shipment" and "cannot be canceled directly after delivery to the carrier" cannot be combined.
6. Use the stable key `intent_id::scenario_key` to merge duplicate content; array fields are deduplicated, and the number of evidence is only increased for new observation IDs.
7. When the historical practice conflicts with the current policy or security access control, it will be recorded as `candidate` and marked with the conflict, and will not be used as a callable solution.
8. `status=approved` permits a playbook to guide a draft, but never grants automatic-send permission. Automatic sending is a separate decision for each exact `intent_id::scenario_key`: a known sent Draft creates an event, followed by the owner's current category confirmation.

## 5. Continuous learning from manual modification of Draft

This applies only during normal operation after the owner has enabled `learning.enabled` with recorded consent. That setting is the owner’s authorization for this ongoing, automatic Draft-edit learning; do not ask for or require a new owner confirmation for every individual Draft.

1. After AI creates the Draft, use `scripts/draft_learning.py snapshot` to save the short-term desensitization baseline, Draft ID, thread ID, latest customer message ID and third-level intent; the unredacted text will not be saved.
2. Check the tracked draft and its thread first in each round. If the draft still exists, pull the current text and run `compare`; if it has been sent, use the text sent by the corresponding merchant in the thread for comparison.
3. Treat semantic changes only as learning signals. Ignore differences caused by Gmail's auto-formatting, citation history, signature position, whitespace, line breaks, and AI claims switches.
4. Divide the modifications into: tone preferences, structural preferences, fact corrections, treatment options changes, policy/authority changes, and this case only exceptions.
5. Tone and structure modifications can be incorporated into the style profile. Generalizable solution modifications are merged with scene keys by third-level intent. Instance values such as order number, name, amount, address, etc. cannot be written.
6. Fact correction only prompts that there may be problems with the connector or matching, and does not write the corrected specific facts into global memory. Policy changes must be updated back to the official policy source, and rules cannot be established solely through Draft modifications.
7. Modifications involving illegality, discrimination, deception, product safety, privacy, chargebacks, over-authorization refunds or bypassing platform rules shall not be used as executable memory; write an internal warning and transfer it to manual review.
8. For a generalizable safe update, pass the stable `observation_id` to `user_memory.py merge --source draft-edit --delete-input`; repeated runs must not repeatedly add evidence. The command verifies that ongoing Draft-edit learning remains enabled with recorded consent.
9. Clear the short-term baseline of the Draft after the merge is successful. Baselines are retained only for the configured `learning.draft_baseline_retention_days`, then are removed by `python3 scripts/draft_learning.py purge`.

### Category confirmation after a known sent AI Draft

This is not Draft-edit learning and does not require `learning.enabled`.

1. When an owner sends a known AI Draft in Gmail, or confirms an OpenClaw send, verify the merchant's sent message and the tracked Draft ID, thread ID, and sent message ID.
2. Create a short-lived event only; this does not enable a category:

   ```bash
   python3 scripts/auto_reply_permissions.py record-sent \
     --source gmail-sent \
     --draft-id <SENT_DRAFT_ID> \
     --thread-id <THREAD_ID> \
     --sent-message-id <SENT_MESSAGE_ID> \
     --input /controlled-temporary-directory/atomic-issues.json \
     --delete-input
   ```

3. For each exact category in that event, show the category and its redacted handling logic, then ask whether that category should use the same logic automatically in future. Do not infer a yes from the global setting and do not approve one category because another category in the same email was approved.
4. If the owner confirms, enable only that category in independent state:

   ```bash
   python3 scripts/auto_reply_permissions.py confirm \
     --event-id <EVENT_ID> \
     --intent-id <INTENT_ID> \
     --scenario-key <SCENARIO_KEY> \
     on \
     --confirm-owner-request
   ```

5. Store only the category key, safe identifiers, confirmation source, and timestamps in the permission/event files; never customer text or personal data. Unresolved events are removed after `retention.pending_category_confirmation_days` by `python3 scripts/auto_reply_permissions.py purge-events`. A later email containing only enabled categories can pass this category gate without another question; any new or disabled category returns the whole email to draft mode.

## 6. Retrieve memory before replying

After matching items to a full order and before pulling campaigns and policies, do steps 1–5 only when `memory.usage_enabled=true`:

1. Read `user_memory.md`, first search by three-level intent ID, and then narrow the scope by scenario key, sales channel, product type and order status.
2. Only load entries with `status=approved` and consistent with the current case; `candidate`, `retired`, conflicting or low-confidence entries are only used for internal prompts.
3. Add the hit content to `user_memory_matches` of the case bundle, and record the memory key, applicable reason and conflict check result.
4. When there is no hit, directly use the Skill standard solution and do not invent user conventions.
5. Current order facts, activities, current policies, platform rules, legal requirements and security access control take priority. Memory only affects expression and preference selection among compliance options.

If `memory.usage_enabled=false`, do not add a `user_memory.md` preference or playbook to the Draft-generation context; continue with the standard process.

If global automatic sending is enabled, submit every atomic issue in the email to `auto_reply_permissions.py check`. This is an independent category-permission check, not a permission to use long-term memory to write the Draft. The entire email may be sent only if every exact category has an enabled independent switch; otherwise it remains a draft.

## 7. Memory update JSON structure

For the one-time onboarding import, write the desensitized final summary into controlled temporary JSON and then execute:

```bash
python3 scripts/user_memory.py merge \
  --source onboarding \
  --input /controlled-temporary-directory/memory-update.json \
  --confirm-owner-request \
  --delete-input
```

For a safe update inferred from a later owner-edited Draft, use the same redacted JSON format but run `python3 scripts/user_memory.py merge --source draft-edit --input /controlled-temporary-directory/memory-update.json --delete-input`. This source requires `learning.enabled=true` with recorded consent and does not represent a second history import.

An owner may separately merge a generalized, redacted sent-Draft lesson through `user_memory.py merge --source sent-draft`, but this does not create or alter automatic-reply permissions.

Minimal example:

```json
{
  "style_profile": {
    "status": "approved",
    "items": [
      {
        "key": "opening",
"summary": "Restate the specific problem first, and then express a brief apology",
        "source": "history_30d",
        "observation_id": "history-2026-07-opening-v1",
        "evidence_count": 12,
        "confidence": "high",
        "status": "approved"
      }
    ]
  },
  "handling_playbooks": [
    {
      "intent_id": "FULFILLMENT-DELAY-CARRIER",
"l1_name": "Logistics and Fulfillment",
"l2_name": "Transportation delay",
"l3_name": "Carrier transportation delay",
      "scenario_key": "carrier-delay-with-valid-scan",
"scenario": "There is a valid scan but the estimated delivery time has exceeded",
"handling_steps": ["Check the last scan", "Give the next checkpoint", "Upgrade carrier investigation after exceeding the threshold"],
"preferred_phrasing": ["I will continue to follow up with the next logistics update"],
"avoid_phrasing": ["Definitely arriving tomorrow"],
"constraints": ["Unconfirmed arrival dates by carriers are not guaranteed"],
      "source": "draft_edit",
      "observation_id": "draft-abc123-rev2",
      "evidence_count": 1,
      "confidence": "medium",
      "status": "approved"
    }
  ]
}
```

Use `--delete-input` for controlled temporary update files. Don't put original email fragments into update JSON. Long-term memory does not expire automatically; to remove it, the owner must explicitly run:

```bash
python3 scripts/user_memory.py clear --confirm-owner-request --confirm-delete-all
```

This resets all long-term memory. It does not change independent category permission switches. The owner can turn off one category or all category switches with `auto_reply_permissions.py` without changing long-term memory.
