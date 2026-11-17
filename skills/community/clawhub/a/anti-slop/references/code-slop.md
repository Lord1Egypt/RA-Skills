# Code Slop: The Full Reference

Slop in code isn't about word choice — it's about unjustified complexity and unverified confidence. Industry write-ups and peer-reviewed surveys of AI-assisted development converge on the same handful of patterns. Independent data backs the concern: one large-scale analysis of changed lines found code duplication rising sharply alongside AI-tool adoption and refactoring share dropping; a CMU study of real repositories after AI-tool adoption found static-analysis warnings and code complexity both climbing after initial velocity gains, with the added complexity persisting after the velocity gains faded. None of this means AI-written code is bad — it means these specific failure modes are common enough to check for deliberately.

## Table of contents
1. Over-engineering
2. Convention-blindness
3. Defensive-programming excess
4. Hallucinated APIs and unverified assumptions
5. Dead code and comment noise
6. Plausible-but-wrong logic
7. Self-edit checklist for code

---

## 1. Over-engineering

The most common pattern: building an abstraction layer, config system, or plugin architecture for a problem that needed a direct, ten-line solution. This happens because generic "good practice" (interfaces, dependency injection, configurability) is heavily represented in training data as a marker of quality, so it gets applied reflexively rather than when the actual requirements justify it.

Ask before adding any abstraction: is there a second real caller or use case *today*, or am I building for a hypothetical future one? If it's hypothetical, don't build it yet — YAGNI (you aren't gonna need it) is a real principle, not a compromise. A follow-up refactor when the second use case actually shows up is cheap; a wrong abstraction guessed in advance is expensive to unwind.

- Before: A `StorageStrategyFactory` with an abstract `StorageProvider` interface, three concrete implementations, and a config file, to read one CSV from local disk.
- After: A function that reads the CSV. Add the abstraction when there's an actual second storage backend to support.

## 2. Convention-blindness

Code that is "generically good" but ignores the patterns already established in the codebase it's being added to: different naming conventions, a different error-handling style, a different test framework than the one already in use, reinventing a helper that already exists elsewhere in the repo. This produces code that's individually fine but makes the codebase less consistent overall.

Before writing new code in an existing project, look at a neighboring file doing something similar and match its conventions — naming, error handling, import style, how it's tested — rather than defaulting to a generic textbook style.

## 3. Defensive-programming excess

Try/except (or try/catch) blocks added reflexively around code that either can't realistically fail in the ways being caught, or where failing loudly would actually help the person debugging it. Symptoms:
- Catching a broad exception type and silently swallowing it (`except Exception: pass`, or logging and continuing as if nothing happened) when the caller actually needs to know something went wrong.
- Wrapping every function in its own try/except "just in case," rather than handling errors at the boundary where there's actually something useful to do about them (retry, fallback, surface to the user).
- Adding excessive logging statements that don't correspond to any actual debugging need, cluttering the signal.

Fix: only catch exceptions you have a real plan for (retry, specific fallback, user-facing message). Let unexpected errors propagate and fail loudly during development rather than disappearing into a swallowed catch block — a silent failure is much more expensive to track down later than a crash with a stack trace now.

## 4. Hallucinated APIs and unverified assumptions

Confidently calling a library function, config option, or API endpoint that doesn't exist, is deprecated, or has a different signature than assumed — a well-documented failure mode of code-generating models, especially for less common libraries or fast-moving APIs. This is dangerous specifically *because* it looks completely plausible; syntactically valid code that references a nonexistent method passes a casual read.

Before relying on any API surface you're not certain about — a library method, a CLI flag, a config key — verify it: check the actual installed version's docs, grep the vendored source, or run a minimal test rather than trusting training-data recall for anything that could have changed. This matters more the more niche or fast-moving the dependency is.

## 5. Dead code and comment noise

- Leftover unused imports, unused variables, or commented-out old versions of code left in place "just in case."
- Comments that restate exactly what the line already says (`# increment i by 1` above `i += 1`) rather than explaining *why* something non-obvious is being done.
- Placeholder or stub code left in without being flagged as incomplete (a function that returns a hardcoded value instead of doing the real computation, with no `TODO` or comment marking it as a stub).

Fix: remove anything not being used. Reserve comments for the non-obvious — why this approach was chosen, what constraint it's working around, what would break if it were removed — not for narrating syntax.

## 6. Plausible-but-wrong logic

Code that has correct syntax, runs without erroring, and looks right on a quick read, but is subtly wrong: an off-by-one that only shows up at a boundary, a comparison that works for the happy path but not the edge cases, a fix that addresses the symptom mentioned in the request rather than the underlying cause. This is the hardest category to catch by eye, precisely because it doesn't look like a mistake.

Mitigation: for anything beyond trivial, actually run it — don't just reason about whether it should work. Check boundary conditions explicitly (empty input, single item, the largest expected size). If tests exist, run them; if they don't and the change is non-trivial, consider writing a minimal one rather than trusting a read-through.

## 7. Self-edit checklist for code

Before considering a non-trivial piece of code finished, check:

- [ ] Does every abstraction, config option, or extra layer have a real, current use case — not a hypothetical future one?
- [ ] Does this match the naming, structure, and error-handling conventions already used elsewhere in this codebase?
- [ ] Is every try/except block catching something specific, with a real plan for what happens next — not a broad catch-and-ignore?
- [ ] Is every library call, API, and config option I used something I've actually verified exists (checked docs/source), not recalled from general familiarity?
- [ ] Are there unused imports, dead variables, or commented-out code left behind?
- [ ] Do the comments explain *why*, not just restate *what* the code already says?
- [ ] Did I actually run this (or reason through concrete edge cases: empty, one item, max size) rather than just eyeballing that it looks right?
