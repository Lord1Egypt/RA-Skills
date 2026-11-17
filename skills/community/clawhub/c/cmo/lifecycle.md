# Lifecycle — Email, Nurture, Onboarding, Retention Marketing

The owned channel (SKILL.md Rule 7). Everything here compounds only while inbox placement holds, so placement is the first check in any lifecycle problem, not the last (`diagnose.md`).

## The Lifecycle Map

| Stage | Job | Primary metric | Failure signature |
|-------|-----|----------------|-------------------|
| Subscribe / signup | Set expectation, deliver the promised thing immediately | Confirmation open rate | Welcome email arrives days later, or never |
| Onboard / activate | Reach the value moment fast | % reaching the activation event (`product-led.md`) | Feature tour instead of first outcome |
| Nurture | Stay useful until the trigger arrives (the 95%) | Reply and click rate; pipeline sourced later | Drip built as a product pitch in five parts |
| Convert | Remove the last objection | Conversion of engaged segment | Discount used as the only lever (`pricing.md`) |
| Expand | Sell the next use case to a happy account | Expansion revenue per account | Upsell mail to accounts with failing usage |
| Win back | Recover lapsed, or exit cleanly | Reactivation rate; complaint rate | Mailing dead addresses forever |

## Deliverability Comes First

- Authenticate everything: SPF, DKIM, and DMARC on the sending domain. Major mailbox providers require authentication and one-click unsubscribe from bulk senders, and treat a spam-complaint rate at or above **0.30%** as unacceptable — run under **0.10%** to keep margin.
- Send marketing mail from a subdomain (`news.example.com`), never from the domain that carries transactional and human mail. One bad campaign should not take invoices and password resets down with it.
- Warm a new domain or IP gradually, starting with the most engaged segment, and never import a purchased or scraped list: complaint spikes on a new domain are close to unrecoverable, and buying lists breaches consent law almost everywhere (`compliance.md`).
- Hard bounces suppress permanently and immediately. Chronic soft bounces suppress after a handful of attempts.
- **Sunset policy**: stop mailing addresses with no open or click over a defined window (90-180 days for high-frequency senders, longer for quarterly cadences), after one reactivation attempt. Engagement is the dominant placement signal — a large disengaged list actively suppresses delivery to the people who do want you.
- One-click unsubscribe in the header, an obvious link in the body, and honour it inside a day. Making unsubscribe hard converts a quiet exit into a spam complaint, which is far more expensive.

## Segmentation That Earns Its Complexity

Start with three axes and add only when a message would genuinely differ: lifecycle stage, ICP fit, and engagement recency. Most teams build 40 segments and send everyone the same email anyway.

- Suppression lists are as important as send lists: current customers, open opportunities, competitors, and anyone in a live support escalation.
- Global frequency cap across all senders (product, lifecycle, sales sequences, events). Without a shared cap, a single prospect receives five uncoordinated emails in a week and unsubscribes from all of it.
- Preference centre beats unsubscribe: offer topic and frequency choices before the exit.

## Nurture Design

- Write for the trigger, not the timer. The best nurture asks a question the reader can answer ("what is stopping this?") and routes on the answer; the worst is five product features on a fortnightly clock.
- Value-to-ask ratio: at least two useful sends before an ask, at every stage.
- Plain-text-looking emails from a person outperform designed templates for B2B nurture in most accounts — test it; the effect is large enough to matter and cheap enough to check.
- End every sequence somewhere. A nurture with no exit is a suppression list with extra steps; define the exit condition (converted, replied, sunsetted) before you build it.

## Onboarding Sequences

The only sequence with a hard deadline: value must land before attention does. Rules that survive most products:
- Sequence by *behaviour*, not by day. "Has not connected data on day 2" gets a different email from "connected data on day 1".
- One action per email, and the action is inside the product, not inside the email.
- Time the human touch to the moment the product cannot help: a stuck user at step three is worth a real message from a real person.
- Instrument the drop-off step and fix the product there before writing a fourth reminder about it.

## Churn Saves and Winback

- Cancellation flow: ask the reason with a short closed list plus free text, then offer the remedy that matches the reason — pause for "not using it right now", downgrade for price, a support session for "could not get it working". A blanket discount to everyone teaches customers to threaten cancellation.
- Involuntary churn (failed payments) is often the biggest and cheapest to fix: dunning emails plus card-updater retries recover revenue with no persuasion required. Fix this before building a winback campaign.
- Winback: one honest campaign to lapsed users naming what changed since they left, then suppress. Repeated winback attempts to the same silent addresses are pure deliverability cost.
- Exit interviews with churned accounts feed positioning as directly as win/loss does (`positioning.md`).

## SMS, Push, and In-App

Same discipline, tighter tolerances: consent is separately required per channel and per purpose in most jurisdictions (`compliance.md`), quiet hours are a legal issue in some markets and a trust issue everywhere, and frequency tolerance is roughly an order of magnitude lower than email. Use these channels for time-critical, personally relevant messages only — a promotional push has an unsubscribe cost measured in uninstalls.

## Reporting Lifecycle Honestly

Open rate is no longer a clean signal — privacy-protection features in major mail clients pre-fetch images and inflate opens. Judge lifecycle on clicks, replies, downstream conversions, and revenue per recipient; use opens only as a relative trend within the same segment and time period, never as a target or a KPI in a board deck (`measurement.md`).
