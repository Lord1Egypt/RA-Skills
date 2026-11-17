# Design and structure

Fires: always

Leading word: **change together**. Ask of every pair of pieces: should these change together? There are only three ways the code gets it wrong (hidden links, needless links, surplus), plus the special cases that show where the design never accounted for a requirement. Every fact lives in a **single source of truth**; every module is **deep**: a lot of behavior behind a small **interface**, at a clean **seam**, giving callers **leverage** and maintainers **locality**.

Artifact: the import graph (what imports what, scripted so it can be rerun), the top pairs from `scripts/cochange.sh`, and the special-case list.

**Hidden links**: pieces that must change together, where the code does not show it.

- **copies**: The same logic, constant, enum, list or schema written in more than one place (client and server enums, a docs table and the code it describes, two validators). Change one and the others must change too, but nothing says so. Fix family: one source of truth that the others derive from or are generated from.
- **global-state**: A module reads a global, singleton, environment value or file that another module sets. Change that module and this one breaks, but nothing shows it.
- **scattered-feature**: One feature split across folders by layer, or related code in different folders, so one change needs all of them and the layout hides it. `cochange.sh` pairs with no import between them are the candidates. Fix family: colocate by domain.
- **implicit-protocol**: A call order or convention callers just have to know (init before use, call `track()` after every action). Change it and callers break with no warning. Fix family: make it explicit in the interface or impossible to skip.

**Needless links**: pieces tied together that change for different reasons.

- **internals-coupling**: Callers that depend on another module's internals, which then change for their own reasons and break them.
- **dependency-direction**: Stable code that imports something more volatile, so the stable code changes whenever the volatile code does. Read the import graph against how often each side changes.
- **caller-vocabulary**: A general function with a parameter or branch only one workflow understands, so the function changes whenever that workflow does.
- **shallow-module**: An interface nearly as complex as its implementation, so it changes whenever its internals do, and its callers change with it.

**Surplus**: pieces with no reason of their own to change.

- **pass-through**: Wrappers that only change when the thing they wrap does. Apply the **deletion test**: if deleting it makes complexity vanish rather than reappear across its callers, it is surplus.
- **speculative-generality**: Extension points, config and abstractions for things that never vary. One **adapter** means a hypothetical seam; two adapters mean a real one.
- **dead-code**: Nothing uses it, so nothing will ever need it to change. Confirm with a search across the repo, its scripts and its config before calling it dead.

**Special cases and readability**

- **special-cases**: Code that exists for one situation instead of following from how the system works: an `if` for one value, a parameter for a specific caller, a swallowed exception, a retry or sleep, a disabled test. Each is a requirement the design never accounted for; group them by the requirement they hide.
- **naming-drift**: One concept with several names, one name for several concepts, or names that disagree with `GLOSSARY.md` or lie about what the code does.
- **readability**: Functions a reader cannot hold in their head: several jobs in one body, deep nesting, flag arguments that switch behavior, a reader needing to jump across many files to follow one concept.
- **comments**: Comments that restate the implementation (`// sort first so the binary search works`) have no reason of their own to change: remove them, even when phrased as a why. Comments about something outside the code (`// the proxy drops websockets, so we poll`) carry what the code cannot show: keep them. Comments that explain a workaround in the codebase (`// wait 100ms because the cache isn't ready yet`) go when the problem behind the workaround does.
- **docs-drift**: README, `CLAUDE.md`, `AGENTS.md`, ADRs or API docs that state commands, paths, behavior or rules the code no longer has. Agents follow these literally, so each stale line is a hidden link between the doc and the code. Run the documented commands and check the documented paths exist.

Done: every pair in the `cochange.sh` top list has an answer, every import that points toward more volatile code is listed, and every special case is grouped under the requirement it hides.
