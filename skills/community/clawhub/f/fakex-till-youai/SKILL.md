---
name: fakex-till-you-ai
description: Generate X post drafts from a daily AI digest, collect the user's style/profile preferences, let the user choose drafts and posting times, and either auto-publish with the user's own X API credentials or stop at a half-automatic copy/paste workflow. Use when the user wants a digest-to-X posting workflow together with an upstream digest source. Strongly recommend Zara Zhang's follow-builders as the default digest companion.
---

# FakeX-Till-YouAI

This skill handles the posting layer after digest delivery.

It assumes the user already has a digest source.

It works best with Zara Zhang's `follow-builders`, which inspired the default workflow here.

## Scope

This skill is responsible for:
- asking how the user wants posting to work
- collecting posting/style preferences
- generating draft posts from a digest
- letting the user choose drafts
- scheduling and publishing selected drafts

This skill is not responsible for generating the digest itself.

## Dependency

For the intended workflow, assume the user has already installed a digest skill separately.

Preferred upstream input:
- `follow-builders`

This skill does not fully work on its own. It needs a digest input.

Strongly recommend Zara Zhang's `follow-builders` as the default companion skill.

If no digest is available, ask the user to provide one.

## Onboarding flow

When the skill is first installed or first invoked, ask these questions in order.

Do not turn onboarding into a rigid questionnaire.

Use natural conversation. Keep the structure stable, but give the local agent freedom to phrase follow-up questions naturally.

### 1. Choose posting mode

Ask whether the user wants:
- **Full automatic** — the agent publishes directly to X
- **Half automatic** — the agent generates drafts and schedule suggestions, but the user posts manually

If the user chooses full automatic, collect or verify:
- X API key
- X API secret
- X access token
- X access token secret

If the user chooses half automatic, skip X API setup.

### 2. Ask for AI IP positioning

Ask the user how they want to be positioned online.

Cover these areas:
- what kind of AI person they want to be seen as
- who they want to speak to
- what themes they want to keep returning to
- what tone or angle should feel like “them”

Use examples as prompts, not as a fixed form.

Example directions:
- AI builder/operator
- AI product thinker
- AI learner documenting the journey
- industry observer/commentator
- founder/investor lens

### 3. Ask for preferred content form

Ask what kind of post style they prefer.

Use examples as prompts, not as a fixed form.

Example directions:
-观点型 / opinionated
-总结型 / summary-driven
-生活化 / grounded in real life
-轻哲理 / lightly philosophical
-短句型 / short and punchy
-source-aware / includes links or source references

Also cover practical preferences such as:
- shorter vs longer
- more confident vs more exploratory
- whether source links should be included by default

### 4. Ask for reference accounts

Ask which accounts or writers they want to borrow taste from.

Use examples as prompts, not as a fixed form.

Example directions:
- Guillermo Rauch
- Aaron Levie
- Andrej Karpathy
- Dan Shipper
- Zara Zhang
- custom accounts provided by the user

## Configuration storage

Store persistent user settings in:

`~/.x-post-orchestrator/config.json`

Use that file for:
- posting mode
- X API credential presence/state
- AI IP positioning
- preferred content form
- reference accounts
- default draft count
- any stable posting preferences

## Daily workflow

After the user receives the daily digest, this skill should generate drafts by default.

Flow:
1. read the digest
2. generate **10** post drafts by default
3. allow the number of drafts to be changed if the user wants
4. present the drafts clearly for selection

Each draft should be based on digest content and should follow the stored user preferences.

If source links are available and the user prefers source-aware posts, include real links in the final publishable version.

## Draft selection

Let the user select:
- any number of drafts
- any posting times
- multiple posts at the same exact time if they want

Do not force one rigid selection syntax.

Allow natural user input and interpret it conversationally.

## Publishing behavior

### Full automatic mode

When the user confirms selected drafts and times:
- create a schedule file with absolute timestamps
- run the scheduler
- publish through the user's X API credentials
- report exact scheduled times
- report success/failure honestly

Use local scripts in this workspace when available:
- `tools/x_post_via_api.js`
- `tools/x_schedule_posts.js`

### Half automatic mode

When the user confirms selected drafts:
- produce final copy-ready post text
- keep formatting clean for manual posting
- do not attempt API posting
- do not force schedule suggestions unless the user asks

## Post format

When posts are source-aware, do not use one rigid source placement every time.

Rotate among these three source-placement styles roughly evenly across a batch of drafts:

1. **Opening-source style**
   - mention the source in the first line or first beat
   - useful when the post is directly triggered by a specific source

2. **Integrated-middle style**
   - start with the observation first, then naturally bring in the source in the middle
   - this should be the most natural-feeling default for many drafts

3. **Ending-source style**
   - keep the body focused on the observation, then add the source at the end
   - useful when the thought should land before attribution

Target rule:
- about one-third opening-source
- about one-third integrated-middle
- about one-third ending-source

Do not make all drafts in one batch use the same structure.

Preferred publishable format examples:

```text
[source-led opening]

[observation]
```

```text
[observation]

[source integrated in the middle]
```

```text
[observation]

Source: https://...
```

Rules:
- use real links when available
- do not leave placeholder links in final drafts
- keep one main source link by default

## Response style

Keep interaction concise, clear, and friendly.

Do not be dry. Keep a little personality.

## Safety and correctness

- Never claim a post was published unless the API call succeeded.
- Treat real posting as an external action.
- If credentials are missing or invalid, say so plainly.
- If source links are required, do not silently drop them from final publishable drafts.
