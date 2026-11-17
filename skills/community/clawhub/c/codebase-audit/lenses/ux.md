# Product and UX

Fires: when the project has a user interface

Leading word: **0, 1, many, too many**. Every screen at the edges: item counts, day 2 and day 30, an interrupted user, another locale, the largest text size with a screen reader on.

When you can run the app (simulator, emulator, browser, dev server), check each probe on screen and attach screenshots, marking those findings `CONFIRMED`. When you cannot, read the layout code.

Artifact: a screen list (screen → probes that apply → result).

- **cardinality**: Render each list or grid with 0, 1, 7 and 400 items, very long strings and emoji. Missing empty states, layouts that assume one item, unbounded lists.
- **day-2-day-30**: With no new input, what does the app show on day 2? On day 30? Stale "today" content, expired items shown as fresh, notifications about nothing, streaks that break silently.
- **copy-lie**: Copy that promises what the code does not guarantee: "Saved" before the write is confirmed, "Synced" with no server ack, "Fresh until" from a guess, "Deleted" for a soft delete, "Private" with nothing behind it.
- **dead-ends**: A screen with no next action, no way back, or two equally loud primary buttons; an error message with no next step.
- **no-undo**: Destructive actions (delete, clear, overwrite, cancel subscription, leave a shared space) with neither undo nor confirmation.
- **interrupted-user** (when the app runs on a phone or has multi-step flows): A phone call mid-flow, backgrounded and killed, state restoration after process death, permission denied then granted in Settings, offline, low storage, rotation, a deep link into the middle of a flow.
- **locale-adversary** (when the app takes or shows names, addresses, money, dates or translated text): The falsehoods programmers believe about names, addresses, phone numbers, currencies and time: a one-word name, no postcode, a 15-digit phone number, a comma decimal separator, right-to-left text, plurals beyond one/many, translations 40% longer than English, dates in another order.
- **a11y-extremes**: At the largest Dynamic Type or 200% font scale, with VoiceOver or TalkBack on: truncation that drops meaning, unlabeled controls and images, tap targets under 44pt/48dp, motion that ignores reduce-motion, contrast below WCAG AA.

Done: every screen in scope went through every probe that applies to it.
