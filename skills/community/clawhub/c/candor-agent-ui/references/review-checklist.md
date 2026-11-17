# Review checklist

Run this after each screen where an AI agent acts, before moving on. One line per check; the rule it keeps is in
brackets. Check the running screen, not the intention. Fix what fails first; a check you couldn't run stays unticked
and is named in your report.

## Model output

- [ ] No model text reaches `innerHTML`, `dangerouslySetInnerHTML` or a markdown renderer that emits HTML (model output is text)
- [ ] A URL the model wrote is shown as text, not a link; links come only from the app's own data (model output is text)
- [ ] Code and query text from the model is shown in a code block and never run or rendered from the screen (model output is text)

## Unknown stays unknown

- [ ] Every duration, cost, count and time shown was measured by a service; none is a placeholder such as 0, $0.00 or "just now" (unknown stays unknown)
- [ ] Every estimate has the word "estimate" beside it, with what it rests on (unknown stays unknown)
- [ ] A missing value renders as empty or "not measured", never as a default (unknown stays unknown)
- [ ] A running job heard from nothing past the threshold shows when it was last heard, not "Running" (unknown stays unknown)
- [ ] Every list and table has a loading, an empty and an error state in its own words (its `state` prop); a fetch that failed never shows as an empty list (unknown stays unknown)

## Locked controls

- [ ] No control a person might expect to use is `disabled`; each is locked, focusable, `aria-disabled`, with a reason reachable by keyboard and screen reader (a locked control says why)
- [ ] Each reason says who can, what is missing, or what must happen first (a locked control says why)

## Decisions

- [ ] No approve/deny, allow/deny or keep/discard answer is selected, checked or focused by default (nothing pre-selected)
- [ ] Enter, Space or a single key never approves or performs a destructive choice (nothing pre-selected)
- [ ] The agent's recommendation, where shown, is marked as its pick and not selected (nothing pre-selected)
- [ ] "Always allow" is never ticked for the person, and says what it skips and how to turn it off (nothing pre-selected)

## The exact change

- [ ] The approval shows the change itself (diff, fields and values, targets, amount), not only a description (approve the exact change)
- [ ] The decision is bound to the hash or version the person saw, and a changed request asks again (approve the exact change)
- [ ] Self-approval is refused where policy says so, and production or over-threshold changes show the second approver the policy names (approve the exact change)
- [ ] "Approved" shows only after the server recorded it; a failed decision keeps the answers available (approve the exact change)

## Reasoning

- [ ] Model reasoning is labelled as the model's account (believed or assumed), and verified steps point at their evidence (reasoning is believed, not verified)
- [ ] Reasoning is styled as a note, not like a source, test result or diff (reasoning is believed, not verified)

## Names and disclosure

- [ ] Every agent message names its agent from app data; no name or system line comes from model output (the app names the agent)
- [ ] The person is told they are dealing with an AI at first contact, in the app's words (AI disclosure)
- [ ] Content the agent made or changed is labelled from records, and "not recorded" when there is none (AI disclosure)

## Undo and blast radius

- [ ] Every destructive action says what it removes, whether it comes back, how and for how long (say what can and can't be undone)
- [ ] The riskiest actions confirm by typing a name; OK and Cancel alone is not enough (say what can and can't be undone)
- [ ] An undo or restore result says what it did not undo (say what can and can't be undone)
- [ ] Before a change, what it reaches is shown grouped by kind, from measured counts, with "not measured" where it can't be (blast radius)
- [ ] A stop or kill switch says it doesn't undo what was already done (say what can and can't be undone)

## Status and progress

- [ ] Every status is a word beside its colour or dot; nothing is colour alone (status vocabulary)
- [ ] Statuses map to the nine run statuses; failed ones carry an error, blocked ones name what blocks them (status vocabulary)
- [ ] A tool call shows what it did in plain words, its status, and a duration only once measured; its input and output are text (tool call states)
- [ ] Folded turns open; no approval, error or real change is hidden inside a fold (folding turns)
- [ ] While working, the screen shows the current step and what it's waiting on, and the person can stop (while it works)
- [ ] Work finished while away leads with what needs the person, then failures, then results; nothing is auto-dismissed (finishing while away)

## Motion

- [ ] A success mark, a filled step or a swept meter appears only after the result settled or the value was measured, never on the press (motion never says something false)
- [ ] A state that was already final when the screen drew does not animate as if it just happened; motion on hover for show is fine on an element that isn't a control, if it says nothing false and is off under reduced motion (motion never says something false)
- [ ] Reduced motion: only opacity and colour change, each in 150 ms or less, and nothing loops; a live indicator is still and keeps its word (motion never says something false)
- [ ] Every animation belongs to a family (reveal, arrive, pop, mark, fill, value, move, overlay, press, tint, refuse, attention, live, clock), not a raw duration; motion for show uses the family whose change it draws (motion never says something false)
- [ ] A brand file changes how a change looks, never when it plays; the moment is still the component's (motion never says something false)
- [ ] No state is carried by motion alone, and the person's setting beats the app's and the brand's (motion never says something false)
- [ ] A brand file's motion was checked with `candor-ui theme check`, not by eye (motion never says something false)

## Sound

- [ ] Sound is off until the person turns it on, and nothing in the theme or the app turns it on for them (motion never says something false)
- [ ] A sound is raised from data that arrived while the page was open, never from a component mounting; loading a page with an approval waiting is silent (motion never says something false)
- [ ] Every sound has a visible cue beside it (the prompt, the title count, a toast), and nothing is conveyed by sound alone (motion never says something false)
- [ ] A burst plays one sound, each is 1.5 seconds or less, and none loops or speaks (motion never says something false)

## Accessibility

- [ ] Every control is reachable and usable with the keyboard; dialogs keep focus and close on Escape (accessibility)
- [ ] Arrivals are announced once per message, polite for progress and results, assertive for errors; errors stay until dismissed (accessibility)
- [ ] Focus moves to a new approval prompt or question; a toast never covers or takes focus (accessibility)
- [ ] Icon-only buttons and groups of answers have accessible names that say what they do (accessibility)
- [ ] Text and status colours pass contrast in every theme the app supports; motion goes calm under reduced motion (accessibility)
- [ ] Targets meet the minimum size; relative times carry the exact time (accessibility)
- [ ] Every screen works narrow (320 px): nothing is cut off, and only a table or log scrolls sideways, in its own scroller (accessibility)
