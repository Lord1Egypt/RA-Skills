# AI disclosure and accessibility

## AI disclosure

People should know when they're dealing with an AI and when something was made by one. This is the product's
responsibility, in the product's own words; it helps with the EU AI Act's transparency duties but is not legal advice.

- **At first contact**, before the person's first message or on the first screen of a chat: a plain line, "Ada is an
  AI system, not a person", or an "AI" badge in the thread header that opens to the app's explanation of what it is,
  what it can do and who runs it. The name comes from the app.
- **Every agent message** carries the agent's name and a mark that distinguishes it from a person's message; a
  person and an agent in the same thread are never confused by styling alone.
- **Content the AI made or changed** (a draft reply, a document, an image, a summary) is labelled from the app's
  records: "AI-generated", "AI-modified", or "AI involvement not recorded" when there is no record. Never infer the
  label from the content.
- **Reasoning and confidence** are labelled as the model's own account (see `honesty-rules.md`, rule 6).
- **Handoff to a person** is announced in the thread: who took over, when. The agent stops replying until it's handed
  back, and that's visible.
- **Consent screens** name what flows where and how long it's kept; the acknowledgement is ticked by the person, never
  pre-ticked; how to take it back is on the same screen.
- Disclosure is asked once per version of the terms, not on every visit, and is recorded.

## Accessibility non-negotiables for agent screens

Beyond WCAG 2.2 AA, which applies as to any screen, these are the points agent screens get wrong most:

- **Status in words.** Every dot, bar or coloured chip has its word beside it or as its accessible name. Colour is
  never the only signal.
- **Locked, not disabled.** A control a person might expect to use stays focusable, is `aria-disabled`, blocks
  activation, and is described by its reason (`aria-describedby`), so keyboard and screen-reader users reach the
  explanation on the control itself.
- **Announcements.** New messages, finished steps and results arrive in a polite live region, one announcement per
  message, not per token. Errors and anything waiting on the person are assertive. Errors stay until dismissed;
  nothing that needs a decision times out.
- **Focus.** When an approval prompt or a question appears, focus moves to it (or it is announced and reachable with
  one keystroke). Dialogs keep focus inside and close on Escape. A toast never covers the focused control and never
  takes focus.
- **Keyboard.** Every control is reachable and usable. No destructive or committing action under a single key. Enter
  in the composer sends only if the person expects it; Enter never approves. Scrolling boxes with nothing focusable
  inside (logs, wide tables, code, diagrams) are tab stops so they can be scrolled.
- **Names.** Icon-only buttons have accessible names that say what they do ("Allow this tool call", not "Check").
  Groups of answers are a labelled group. Messages expose who said them.
- **Streaming.** Arriving text is visually marked and not announced piecemeal. A stop button is reachable during
  streaming.
- **Time.** Relative times ("5 minutes ago") carry the exact time (title or tooltip, and in the accessible name).
  Timestamps rendered on the server don't claim freshness they can't know.
- **Contrast.** Text and status colours pass contrast on every ground, in every theme the app supports, including the
  tinted grounds behind status text and the focus ring where it's drawn.
- **Motion.** Pulsing dots, shimmers and slide-ins stop or shorten under reduced motion. Nothing is understood only
  through motion.
- **Target size.** Controls meet the minimum target size, or have a hit area that does; dense rows of tool calls are
  the usual offender.
- **Right to left and text size.** Layouts hold at 200% text size and in right-to-left scripts; every string is
  replaceable.
- **Charts and diagrams** the agent produces have a table or text equivalent with the same values.
