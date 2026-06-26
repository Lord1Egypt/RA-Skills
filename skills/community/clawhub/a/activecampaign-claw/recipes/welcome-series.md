# Recipe: Welcome Series

A structured onboarding email sequence for new subscribers, trial users, or customers. Designs the series as a spec that you build in the AC automation builder.

## When to use this

- "Build me a welcome series"
- "What should my onboarding emails look like?"
- "I need a drip campaign for new signups"
- "Design a welcome flow for trial users"
- New list or product launch needing first-touch sequence

## API limitation

ActiveCampaign's v3 API cannot create automations or send campaigns programmatically. This recipe produces a **design spec** — the email sequence blueprint with timing, content structure, and AC configuration steps. The user builds it in the AC automation builder.

If the automation already exists, the agent can enroll contacts using `POST /api/3/contactAutomations`.

## The 4-email welcome template

Parameterized: replace `[segment]`, `[product]`, `[tone]`, and `[CTA]` with account-specific values.

### Email 1 — The welcome (Day 0, immediate)

**Purpose:** Confirm the relationship, set expectations, deliver any promised asset.

| Element | Spec |
|---|---|
| Subject | "Welcome to [product] — here's what's next" |
| Preheader | "You're in. Here's how to get started." |
| Length | 100-150 words |
| Body | Welcome, what they signed up for, what to expect (frequency + content type), link to promised asset if any |
| CTA | Single button: "[Get started / Download the guide / Explore the dashboard]" |
| From | Real human name + real reply-to address |

**AC config:** Trigger = added to list [list] OR tag [tag] applied. Send immediately.

### Email 2 — The value demo (Day 2)

**Purpose:** Show the product/service in action. Reduce time-to-value.

| Element | Spec |
|---|---|
| Subject | "[First name], here's the fastest way to [key outcome]" |
| Preheader | "Most [segment] see results within [timeframe]." |
| Length | 150-200 words |
| Body | One specific use case or feature. Screenshot or short walkthrough. Social proof (one stat or testimonial). |
| CTA | "Try [specific feature] now" |

**AC config:** Wait 2 days. Condition: did NOT complete the activation goal.

### Email 3 — Social proof (Day 5)

**Purpose:** Overcome skepticism with evidence from peers.

| Element | Spec |
|---|---|
| Subject | "How [customer name] achieved [result] with [product]" |
| Preheader | "[Specific metric] in [timeframe]." |
| Length | 150-250 words |
| Body | Brief case study or testimonial. Specific numbers. Similar company/role to the subscriber. |
| CTA | "[See more customer stories / Start your free trial / Book a demo]" |

**AC config:** Wait 3 days after Email 2.

### Email 4 — The nudge (Day 10)

**Purpose:** Final onboarding push. Clear next step with mild urgency.

| Element | Spec |
|---|---|
| Subject | "Quick question about [product]" |
| Preheader | "Need help getting started?" |
| Length | 50-100 words |
| Body | Acknowledge they may be busy. One question: "What's holding you back?" Offer help (reply to this email, book a call, live chat). |
| CTA | "Reply to this email" or "Book a 15-min call" |

**AC config:** Wait 5 days after Email 3. Goal check: if converted, exit automation.

## Automation configuration in AC

Build this in Settings → Automations → Create Automation:

1. **Trigger:** Contact subscribes to list `[list_id from state.json]` or tag `[tag_id]` applied
2. **Email 1:** Send immediately
3. **Wait:** 2 days
4. **If/Else:** Has goal been reached? (e.g., tag `activated` applied, or deal created)
   - Yes → Exit automation
   - No → Continue
5. **Email 2:** Send
6. **Wait:** 3 days
7. **Email 3:** Send
8. **Wait:** 5 days
9. **If/Else:** Goal check again
10. **Email 4:** Send
11. **Apply tag:** `welcome-complete`

## Enrolling contacts via API

If the automation already exists:

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contactAutomation":{"contact":"[contact_id]","automation":"[automation_id from state.json]"}}' \
  "$AC_API_URL/api/3/contactAutomations" | jq
```

## Customization parameters

| Parameter | Default | Options |
|---|---|---|
| `segment` | "new subscribers" | trial users, customers, event attendees |
| `tone` | professional | casual, technical, executive |
| `email_count` | 4 | 3-7 (adjust wait times proportionally) |
| `total_days` | 10 | 7-30 |
| `goal` | tag applied | deal created, activation event, form submitted |
| `cta_type` | button | text link, reply-to |

## Best practices (from `frameworks/email-best-practices.md`)

- Read `state.json` baselines for send-time optimization
- One CTA per email — never split attention
- Subject lines under 50 characters
- Mobile-first design (single column, ≥44px buttons)
- Set preheader explicitly (don't leave it as browser fallback)
- Test merge tags with empty fields before activating

## Outcome logging

After the agent designs the series, log to `~/.activecampaign-skill/history.jsonl`:

```jsonl
{"ts":"...","action":"recipe_executed","recipe":"welcome-series","segment":"trial-users","email_count":4,"tone":"professional"}
```

## Suggested next steps

After presenting the welcome series design, offer the user these follow-ups:

1. **Always offer a list health check:** "Before activating this series, want me to run a list health audit to make sure your subscriber list is clean? Sending a welcome series to bouncing addresses hurts deliverability."
2. **If automation exists in state.json:** "I see you already have a '[automation name]' automation. Want me to enroll specific contacts or a tagged segment into it?"
3. **Review subject lines against calibration:** "Want me to compare your proposed subject lines against your top-performing ones from calibration? I can suggest tweaks based on what's worked for your audience."

## Related files

- `frameworks/email-best-practices.md` — copy and design guidance
- `frameworks/segmentation-theory.md` — who to target
- `references/contacts.md` — contact enrollment API
- `recipes/list-health-audit.md` — ensure list quality before sending
