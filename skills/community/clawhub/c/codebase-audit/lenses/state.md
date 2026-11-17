# State and time

Fires: always

Leading word: **hostile clock**. Things run twice, out of order, at midnight, across a time zone, and outlive the screen that started them.

Artifact: a Mermaid `stateDiagram` per stateful entity, as the code implements it.

- **state-machine**: For each stateful entity (order, scan, subscription, sync job, onboarding), draw its states and transitions from the code, then what the product intends. Findings: transitions the code allows that the product forbids, intended transitions with no code, states with no way out.
- **runs-twice**: Double tap, client retry, re-delivered webhook, replayed offline queue, re-run cron, two devices. Delivery is at-least-once; exactly-once does not exist. For each write, is the second run harmless? Fix family: idempotency key plus a unique constraint, or a state transition that is a no-op when repeated.
- **out-of-order** (when clients sync offline or concurrent writes can interleave): Offline mutation B arrives before A; an old response lands after a new one. Does an old write win? Look for last-write-wins by arrival time, server `now()` stamped at replay, no version or sequence column, responses applied without checking they are still current.
- **calendar-adversary** (when the code computes dates, times, durations or schedules): Run each date computation at 23:59 and 00:00, on a DST change, on Feb 29, on Dec 31 (ISO week 53 vs calendar year), after the user flies east and west (Tel Aviv → LA), with a non-Gregorian device calendar, and in 12h and 24h locales. Expiry dates, streaks, weekly quotas and "today" live here.
- **truth-owner**: Find every fact stored twice: cache and DB, client enum and DB enum, a stored count and the rows it counts, local flag and server record. Which copy wins when they disagree, and what reconciles them?
- **lifetime**: Which caches never invalidate? Which tasks, subscriptions, timers and listeners outlive the view or request that started them?

Done: every stateful entity has a diagram, every write has a runs-twice and out-of-order answer, and every date computation went through the calendar adversary.
