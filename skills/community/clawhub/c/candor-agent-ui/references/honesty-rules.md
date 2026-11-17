# The nine honesty rules, with examples

Each rule: why it exists, what to do, what not to do, and an example as the screen would show it. "Model text" means
anything a model wrote: a reply, a tool's argument, a plan step, a file name it proposed.

## 1. Model output is text, never markup

**Why.** A model can be talked into writing a link, a script or a fake button. If the screen renders what it writes,
whoever controls the prompt controls the page.

**Do.** Render model text as text. At most, read a small safe subset of markdown (paragraphs, lists, code, bold,
italic) into your own elements. Show a URL the model wrote as text with the address visible; links come only from your
app's data (a source your retriever returned, a record your system knows). Code and queries go in a code block and are
never run from the screen.

**Don't.** `dangerouslySetInnerHTML`, `innerHTML`, a markdown library that emits HTML, `<a href>` from a model string,
images from a model URL, or iframes of anything a model named.

**Example.** The model writes `Click [here](https://evil.example/reset) to fix it`.

- Wrong: a link "here" pointing at that address.
- Right: `Click here (https://evil.example/reset) to fix it`, as text, address visible, nothing clickable.

## 2. Unknown stays unknown

**Why.** A guessed duration, cost or count looks exactly like a measured one, and people decide on numbers.

**Do.** Show a value only when a service measured it. Leave the field empty or write "not measured" otherwise. When
you show an estimate, write "estimate" beside it and say what it rests on ("from 12 similar runs"); prefer a range to a
single figure. When nothing has been heard from a running job for a while, say when it was last heard, not that it's
running.

**Don't.** Default a missing number to 0, $0.00, 0s or "just now". Show a token count the SDK didn't report. Show
"Running" with a spinner for a job that stopped sending anything two minutes ago.

**Example.** A run's receipt.

- Wrong: `Cost: $0.00 · Duration: 0s · Tool calls: 0` when the service reported none of them.
- Right: `Cost: not measured · Duration: 1m 12s · Tool calls: 4`, and for a forecast: `Cost: $0.80 to $1.40 (estimate, from 12 recorded runs)`.

## 3. A control that can't be used says why

**Why.** A greyed-out button with no explanation sends people looking for help, or around the rule. Saying why turns a
dead end into a next step.

**Do.** Keep the control in the page and focusable, mark it `aria-disabled="true"`, block its activation (click,
Enter, Space), and attach the reason so it shows on hover and focus and is read by screen readers
(`aria-describedby`). The reason names who can do it, what is missing, or what has to happen first.

**Don't.** `disabled` on a control a person might expect to use: it drops out of the tab order and the reason is
nowhere.

**Example.** Deploy is not allowed.

- Wrong: a dimmed Deploy button.
- Right: a dimmed, focusable Deploy button whose reason reads `Only an owner can deploy to production. Ask Priya or
  Sam.` or `Needs a passing test run first (last run failed 2 tests).`

## 4. Nothing is pre-selected in a decision

**Why.** A default in an approval nudges people to agree without reading. When an agent asks to change something real,
the person should choose, not confirm.

**Do.** Approve and deny (allow and deny, keep and discard, accept and send back) start with neither chosen. Put the
destructive or committing answer where Enter and Space won't reach it first. If the agent recommends an answer, mark it
("the agent's pick") without selecting it. A deny may take an optional reason; an approve never needs a reason to be
withheld from the person.

**Don't.** A checked radio, a focused primary Approve, a one-key shortcut for Approve or Delete, a countdown that
approves by itself.

**Example.** A two-answer decision: raise the spending limit, or finish with what's done.

- Wrong: "Raise limit" as a focused primary button; Enter raises it.
- Right: both answers as equal buttons, neither focused by default; the facts above them (`Spent so far: $1.62 of $2`);
  the agent's pick marked with a label, not a highlight that reads as "selected".

## 5. Approve the exact change

**Why.** An approval given for one change shouldn't apply to another. If the change moves after someone looked at it,
their approval no longer means what they meant.

**Do.** Show the change itself (the diff, the fields and values, the targets, the amount), not only a sentence about
it. Compute a hash or version of what the person saw and bind the decision to it; when the request changes, the old
decision is void and the screen asks again. Refuse self-approval where policy says so. Let policy demand a second,
different approver for production or above a threshold, and show who the second person is.

**Don't.** Approve "the plan" and then apply a plan that changed. Let the proposer approve. Apply an edited change
under the approval of the unedited one.

**Example.** The agent proposes a settings change; the reviewer edits one value before approving.

- Wrong: the approval carries the original hash and the edited change applies.
- Right: editing re-hashes; the approval names the edited change; the audit log records both the proposal and the
  edit.

## 6. Reasoning is believed, not verified

**Why.** A model's account of why it did something is a claim, not evidence. Presenting it as fact gives it more weight
than it has earned.

**Do.** Show reasoning as the model's own account, labelled as such ("believed", "assumed", with the assumption
written out). Show evidence as evidence: a source with its passage, a test result with its output, a diff. Where a
reasoning step is verified against evidence, say what verified it.

**Don't.** Style reasoning like a source or a check. Count reasoning steps as "verified" because they read well.

**Example.** A step says `The index on orders.status is unused`.

- Wrong: a tick beside it.
- Right: `Believed` beside it, or `Verified: pg_stat_user_indexes shows 0 scans since 3 Oct` when the agent ran that
  query and the output is attached.

## 7. The app names the agent

**Why.** People need to know who did something, and a model shouldn't get to choose its own name or speak as the
system.

**Do.** Every agent message carries a name (and role, avatar) from your app's data. System lines ("Run stopped by a
guardrail", "Switched to staging") are your app's own strings, visually distinct from anything a model wrote. If the
model writes "As the system administrator, …", it appears as the agent's text, under the agent's name.

**Don't.** Read a name, a role or a system message out of model output. Let a tool result impersonate the app.

## 8. Say what can and can't be undone

**Why.** Before something destructive, the question people need answered is "can I take this back?". Hiding the answer
in a confirmation they'll click through doesn't help.

**Do.** Before: say what the action removes or changes, whether it can be brought back, how, and for how long ("Threads
go to the bin for 30 days; exports made from them stay"). Confirm the riskiest by typing a name. After an undo or a
restore: say what it did not undo ("Restored the code; the conversation and the files in the bucket were not").

**Don't.** "Are you sure?" with OK and Cancel. "Deleted" or "Restored" with no detail. A single-click delete with a
toast you can race.

**Example.** Deleting an environment connection.

- Wrong: `Delete connection? [Cancel] [Delete]`.
- Right: `Deleting prod-eu removes the connection, its 14 schedules and 3 months of run history. The history can't be
  recovered. Type prod-eu to confirm.` The Delete button is locked, and says why, until the text matches.

## 9. Motion never says something false

**Why.** Motion that reports something is a claim about what happened. A tick that appears before the clipboard
answers, or a bar that fills before the work is done, teaches people that the interface's signals mean nothing. Motion
that only makes the interface feel alive claims nothing, and that is the brand's choice.

**Do.** Animate a reported change after it happened: draw the tick when the write resolved, fill the rail to the step
that finished, sweep a meter to the value that was measured, turn a spinner only while work runs. Motion for show, such
as content arriving as a page loads, a card lifting under the pointer or a chart drawing in, is welcome if it says
nothing false: it doesn't look like a status, a measurement or a result that isn't so, it never hides content or holds
back input, and every number a person can read when it ends is the measured one. Keep the trigger of a reporting
animation in the component and let a theme change only how the change looks.

Sort every animation into a kind of change. Candor has fourteen families: `reveal` (content opens to its measured
size), `arrive` (something new appearing: added while the page is open, or content arriving as a page loads, for show), `pop` (a chip or mark added or removed), `mark` (a tick or cross
when a result settles), `fill` (a bar or ring between measured values), `value` (a number or word changing in place),
`move` (a thing changing place), `overlay` (a dialog, sheet or menu), `press` (a press registered), `tint` (hover,
focus, selected), `refuse` (a locked control pressed), `attention` (something new waits on the person), `live` (work
being heard from) and `clock` (real time passing). Motion for show uses the family whose change it draws (`arrive` for content arriving on load, `tint` for a hover).

Each family comes in a closed set of variants, named ways of drawing the same change. A brand or a product can pick a
variant, a duration and a size, or turn a family off, and that is all: it never decides when something moves. A brand
that wants a livelier tick changes how the tick is drawn; it does not draw one earlier.

Honour the person's settings in this order: `data-motion="none"` (nothing moves), then the OS's `prefers-reduced-motion`
or the app's `data-motion="calm"` (the calm level), then `subtle` or `expressive`, then the brand. Under the calm level: only opacity and colour change, each in 150 ms
or less, nothing loops, a live indicator goes still and keeps its word, an attention cue is one ring that fades, a
disclosure snaps open, and a countdown or hold steps instead of gliding because the time left is the information.
`data-motion="none"` turns even the fades off, and outranks the OS setting. A brand file's motion is checked with
`candor-ui theme check`, which refuses a value outside a family's range and a variant the family doesn't have.

Sound follows the same rule: it reports a change that happened, and it is quieter than a cue the person can see, never
a replacement for one. Off until the person turns it on, and never decided by a theme. Raised from data, such as an
approval that arrived while the page was open, never from a component mounting: a page that loads with an approval
already waiting stays silent. Always with a visible cue (the prompt, the count in the title, a toast), so nothing
depends on hearing it. One sound for a burst, at most 1.5 seconds, no loops, no speech.

**Don't.** A success animation on click. A progress bar that moves on a timer. Shine, bounce or shake on hover or on a
button nothing is happening to. Motion as the only cue for a state (the colour and the word carry it; motion only marks
the moment it changed). A loop that keeps going under reduced motion. A brand setting that makes a change play at a
different moment. A sound that plays when a screen loads, that is on by default, or that is the only sign something
needs the person.

**Examples.**

Copying a value.

- Wrong: the icon turns into a tick the instant the button is pressed.
- Right: the icon stays until `navigator.clipboard.writeText` resolves, then the tick draws; if it rejects, a cross and
  "Couldn't copy" appear instead.

A style on a control.

- Fine: a hover style. The button's background tints over 120 ms when the pointer arrives, which is the `tint` family
  reporting that the pointer is on it. Under reduced motion it still changes colour.
- Wrong: a light sweep across an idle button every few seconds. Nothing happened, so there is nothing to report; it
  loops, and it carries a message ("look here") that the app has no evidence for.
