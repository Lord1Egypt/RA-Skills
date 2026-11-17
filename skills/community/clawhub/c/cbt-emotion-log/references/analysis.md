# Stats and review definitions

Read this file when the user asks "how many of my worries actually happened?", "what have I been angry about lately?", "give me a monthly review", and the like. Answer in the user's language.

## General rules

- **Empty means not filled in** — not 0, not "no emotion", and not "didn't happen". Leave records with missing data out of the stat concerned, and say how many were left out.
- **Every conclusion comes with its sample size.** With fewer than 5, say "the sample is still small; take it as a rough reference only".
- Stats reflect only what the user wrote down, not the whole of their life.
- Labels listed in `inferred` count by default; when the user wants, count only what the user has confirmed.
- Compute with code whenever you can, to avoid mental-arithmetic mistakes.
- Present results as observations — no diagnoses, no lecturing. Where there are no numbers, keep the self-reported change rather than converting it into a score. Keep the sources of factual support apart from the user's stance, and don't give anything more evidential weight because it has been mentioned repeatedly.

## 1. Predictions

- **Each prediction counts once**, however many follow-ups it had.
- **Occurrence rate** = `occurred` ÷ (`occurred` + `not_occurred`). List the counts of `partial`, `pending`, `insufficient_info` and `not_applicable` separately; they don't go into the denominator. If the denominator is 0, say "nothing to compute yet".
- **Calibration**: take the predictions settled as `occurred` or `not_occurred` that have a `probability`, and compare the average predicted probability with the actual occurrence rate. With more data, compare by probability band (0–30, 31–60, 61–100), each with its sample size.
- **Impact**: for predictions that occurred or partly occurred, compare `expected_impact` with `actual_impact`, and mention how the user actually coped.
- **Actions in the meantime**: say how many outcomes came after the user had taken action (`actions_meanwhile` not empty). These outcomes reflect "worry + coping"; on their own they can't prove that the worry was unnecessary, or that it was necessary.

## 2. Changes in emotion and confidence

- Per event and per emotion name, line up the intensity as a time series: initial record → each follow-up. Look at different emotions separately; don't add anxiety and anger together.
- Mark points with `emotions_recalled: true` separately; they are estimates from memory, not ratings made at the time.
- Line up the confidence in the original thought the same way; it always refers to the original sentence.
- With enough data points, you can give "the change from the first record to the latest" and "roughly how long it took to drop to half the initial level".
- Follow-ups with `before_after` can be looked at on their own for the immediate change from one sorting-out session, but say that this can't be separated from the effects of time passing and of real-world developments.

## 3. Rumination

- The number of `reason: recalled` follow-ups under an event, and how the `frequency_since_last` band changes over time.
- The share of rumination follow-ups with an empty `new_info`, and the number of times new understanding, decisions or actions appeared.
- Present two things separately: the same event being recalled again and again (the count of `recalled` follow-ups), and new events on the same theme recurring (counted by `themes` or `related_event_ids`). The first is replaying; the second is a real-world problem repeating.

## 4. Patterns

- **Cognitive distortions**: count by event; an event with several labels counts once for each. Give the few most common ones and the share of events they appear in.
- **Themes**: count by event, and see which themes appear across several events. Themes are more useful combined with emotions, e.g. "80% of the 'being ignored' theme is anger".
- **Domain distribution**: count by event.
- **Time distribution** (day of week, time of day): only when the user asks.

## 5. Review report

When the user wants a weekly or monthly review, go in this order, a sentence or two per part:

1. How many things were recorded this period, and which domains they touch.
2. How the predictions settled (with sample sizes).
3. Events with a clear change in emotion.
4. Recurring themes or cognitive distortions.
5. Good experiences the user is willing to look back on, existing positive support, and actions the user reported as helpful; don't treat things happening together as cause and effect, and don't measure worth by engagement.
6. The follow-ups and predictions still due that the user still wants to keep an eye on; don't press on topics the user has said to set aside.

Don't recount the records one by one. If the user wants the details of one thing, expand that one.
