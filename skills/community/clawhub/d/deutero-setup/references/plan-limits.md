# Plan limits and feature gates

Every Deutero organization sits on one of four plans. The plan decides which model tiers, modalities and features the API will accept — not the credit balance, which is a separate limit. A feature the plan does not cover is refused with **403 "Upgrade required"** no matter how many credits are sitting unused.

Check the plan before designing around a feature. Building a branching flow for a Hobby user, or a premium-tier study for a Solo user, wastes their time and yours. **Until you have checked, assume Hobby**: it is where every new account lands, and most users never leave it.

## The matrix

| | Hobby | Solo | Pro | Team |
|---|---|---|---|---|
| Price | free | $29/mo | $99/mo | $299/mo |
| Credits / month | 15 | 100 | 400 | 1,500 |
| Seats | 1 | 1 | 1 | 5 |
| Open (published) studies at once | 1 | 1 | 3 | unlimited |
| `open_weights` tier | ✓ | ✓ | ✓ | ✓ |
| `standard` tier | — | ✓ | ✓ | ✓ |
| `premium` tier | — | — | ✓ | ✓ |
| Simulations | — | ✓ | ✓ | ✓ |
| Text chat interviews | ✓ | ✓ | ✓ | unlimited* |
| On-device voice (`voice_engine: "local"`, priced as chat) | ✓ | ✓ | ✓ | ✓ |
| Cloud voice (`voice_engine: "cloud"`, +1 credit) | — | ✓ | ✓ | ✓ |
| Video interviews | — | — | ✓ | ✓ |
| WhatsApp interviews | — | — | ✓ | ✓ |
| Image questions (`present_images`, `image_upload`) | — | ✓ | ✓ | ✓ |
| Interview Flow (graph mode) | — | — | ✓ | ✓ |
| Brand theme (colours, fonts, hero image) | ✓ | ✓ | ✓ | ✓ |
| Custom CSS on the interview pages | — | — | ✓ | ✓ |
| Credit top-ups | — | ✓ | ✓ | ✓ |

\* On Team, text-only interviews keep running after the included credits are spent. Every other plan stops at its balance unless auto top-up is on.

**Hobby is text chat and on-device voice only, on the open-weights model, with no simulations.** That is the single most important line in the table, because it is the plan a new user lands on and it rules out most of what the other Deutero skills want to do.

Enterprise is Team plus unlimited seats, SSO, custom domains and custom credit packages; treat it as Team for feature purposes.

## Working out which plan you are on

Check at the start of any study work, before you offer a model tier, propose an Interview Flow, write an image question or promise a simulation. It is one call. Skip it only when you hold a record that this organization upgraded to a paid plan *and* nothing since has contradicted it. A 403 `upgrade_required` is a contradiction: the plan has changed (a cancellation, a complimentary plan that ended), so check again rather than trusting the record.

1. **`get_credit_balance`.** Its `plan` block is the answer, read from the same gates the API enforces:
   - `plan_tier` — `hobby`, `solo`, `pro` or `team`
   - `model_tiers` — the only `model_tier` values you may offer
   - `interview_flow` — whether graph mode exists at all on this plan
   - `interview_modalities` — `text` and `voice_local` (on-device voice) on every plan, `voice_cloud` from Solo, `video` from Pro; `whatsapp` from Pro
   - `image_questions`, `simulations`, `open_study_limit`
2. **No `plan` in that response** (a server that predates it): call `get_publication_status` on any study the organization already has (`list_projects` → `list_studies`). Its `plan_tier` is the plan; read the features off the matrix above.
3. **No `plan` and no study yet:** treat the organization as Hobby — `open_weights`, linear question list — and ask the user whether they have upgraded. Do not create a study just to find out.

**Do not infer the plan from `base_limit`.** It is the monthly credit allowance, and complimentary plans, trials and custom packages break any mapping from it: a Pro organization can show 100. `is_trial_active: true` means a trial with its own credit allowance.

When a user on a lower plan asks for a gated feature, say once that it needs an upgrade (and which plan), then build the version their plan supports. Do not design around the gated feature in the hope they will upgrade.

## What to do instead, per gate

- **A tier not in `plan.model_tiers`** (`standard` and `premium` on Hobby, `premium` on Solo) — use the best tier the plan has, and on `open_weights` compensate with much more detailed private `explanation` guidance on every question. The cheaper model probes more literally, so enumerate what a good answer covers instead of trusting it to find the thread.
- **No simulations on Hobby** — you cannot dry-run the instrument. Do a careful `validate_questions` pass instead, and have the user take the interview themselves with the **Preview** button in the dashboard, which works on a draft. It is a worse test, but it is a test.
- **No Interview Flow below Pro** — keep the study on the linear question list, which is where most studies belong on any plan. Source and participant IDs, embed metadata and answer-dependent follow-ups need no flow. Most branching can be flattened: ask the discriminating question, then write the follow-ups so they make sense for everyone, and let the interviewer's own probing do the adapting.
- **No image questions** — instead of asking for a picture, ask the participant to describe what they would have shown, in a `text` question with guidance naming the details you want. Instead of showing images, describe each concept in the question text.
- **No custom CSS below Pro**: the brand theme covers colours, fonts and weights, corner style and the default mode on every plan, and it is checked for readability, which custom CSS is not. Most branding requests need nothing more. A downgraded organization keeps its CSS but it is switched off; removing it works on any plan.
- **No cloud voice** — on-device voice: `voice_enabled: true` with `voice_engine: "local"`. Speech runs in the participant's browser, it works on every plan, and it is priced as chat. Natural-sounding server speech is what the upgrade buys.
- **No video/WhatsApp** — text chat or on-device voice, the two modalities with no credit surcharge. Offering a modality outside `plan.interview_modalities` (`voice_engine: "cloud"` with voice on, or `video_enabled`) is refused with 403 `upgrade_required` by `create_study` and `update_study`; switching one off always works. A study left offering one after a downgrade is blocked at publish (`modality_not_on_plan`) and its link for that modality is withheld; for cloud voice, `update_study {"voice_engine": "local"}` fixes it.
- **Open-study limit** — it limits *publishing*, not creating. Any number of drafts can exist. `publish_study` refuses with 402 `plan_limit_reached` and lists the open studies holding the slots. Only studies that are open and not yet full count. Ask the user which one to `pause_study` (it turns that study's participants away), or suggest upgrading. `get_publication_status` shows `open_count` / `open_limit` before you try. See `plan-interview-research/references/publishing.md`.

## A caution about where these numbers come from

This table is the published pricing. The running API enforces its own gates and the two can drift. **`get_credit_balance`'s `plan` block and a 403 are the authority; this table is the summary.** When a call is refused, report exactly what the message said rather than arguing from this page, and when a feature this table says is gated turns out to work, take the API's word for it.
