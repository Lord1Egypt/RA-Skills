# Sources

This skill's wording is original. It synthesizes ideas from the agent skills and literature below; no large passages were copied. Popularity figures were read from each platform on 2026-10-17 and differ in meaning per platform (installs vs downloads vs repository stars), so they are context, not a quality ranking.

## Agent skills studied (top 10 by popularity for refactor / rewrite / migration / clean-code / simplify)

| # | Skill | Platform metric (2026-10-17) | Source | License | Ideas adopted |
|---|---|---|---|---|---|
| 1 | improve-codebase-architecture (mattpocock) | skills.sh 1,122,574 installs | https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture | MIT | Scope by change hot spots (git history) before scanning; deletion test for shallow modules; candidates with problem/solution/benefit and strength; don't re-litigate recorded decisions |
| 2 | request-refactor-plan (mattpocock, removed from repo 2026-08 but still listed) | skills.sh 202,430 installs | https://github.com/mattpocock/skills (history: skills/deprecated/request-refactor-plan) | MIT | Interview + verify claims in the repo; explicit in/out of scope; check coverage before planning; plan as tiny commits that each keep the code working |
| 3 | safe-refactor (caveman) | skills.sh 96,955 installs | https://github.com/juliusbrussee/caveman/tree/main/skills/safe-refactor | Apache-2.0 | Define the behavior-preservation boundary first; one ownership boundary at a time; preserve failure behavior and ordering; no dependency growth; same proof before and after |
| 4 | deprecation-and-migration (addyosmani) | skills.sh 50,761 installs | https://github.com/addyosmani/agent-skills/tree/main/skills/deprecation-and-migration | MIT | Hyrum's law; build the replacement before removing; strangler / adapter / feature-flag migration; expand-contract; verify zero usage before deletion; no permanent dual systems |
| 5 | golang-modernize (samber) | skills.sh 38,875 installs | https://github.com/samber/cc-skills-golang/tree/main/skills/golang-modernize | MIT | Inline vs full-scan modes (don't bury the user's task under unrelated churn); apply sweeping changes in isolation; prioritize safety/correctness changes first; remember rejected suggestions |
| 6 | refactor (github/awesome-copilot) | skills.sh 22,201 installs; LobeHub 166 installs | https://github.com/github/awesome-copilot/tree/main/skills/refactor | MIT | Golden rules (behavior preserved, small steps, tests essential, one thing at a time); when not to refactor; smell catalog. Counter-lesson: some of its examples change behavior while claiming not to — this skill makes "find the input that differs" an explicit check |
| 7 | simplify (brianlovin) | skills.sh 19,353 installs | https://github.com/brianlovin/agent-config/tree/main/skills/simplify | not stated in repo | Clarity over brevity; limit scope to recently touched code; don't remove helpful abstractions |
| 8 | refactor-plan (github/awesome-copilot) | skills.sh 12,954 installs | https://github.com/github/awesome-copilot/tree/main/skills/refactor-plan | MIT | No edits while planning; order: types → implementations → callers → tests → cleanup; verification between phases; rollback for risky phases; stop for confirmation |
| 9 | clean-code (sickn33 agentic-awesome-skills) | skills.sh 12,240 installs; Smithery repo 8,021★ | https://github.com/sickn33/agentic-awesome-skills/tree/main/skills/clean-code | MIT | Naming/function/class heuristics (left to simplify-code); explicit limitations section |
| 10 | clean-code-review (wpank) | SkillHub 11,283 downloads; ClawHub 5,604 downloads | https://clawhub.ai/wpank/skills/clean-code-review | not stated (ClawHub listing) | Pre-edit dependency check (who imports this, what tests cover it); edit dependents in the same task; self-check before completion |

## Language-port references (lower popularity, read for port guidance)

| Skill | Metric | Source | License | Ideas adopted |
|---|---|---|---|---|
| port-to-rust (rewrite-rs) | skills.sh 20 installs | https://github.com/rewrite-rs/skills/tree/main/skills/porting/port-to-rust | BSD-3-Clause | Parity contract (unit, acceptable/unacceptable differences, measurement); end states A/B/C; five phases leaf-first; differential proof with denominator; port anti-patterns |
| port-c-module (RediSearch) | skills.sh 53 installs; Smithery repo 6,080★ | https://github.com/RediSearch/RediSearch/tree/master/.skills/port-c-module | RSALv2/SSPLv1/AGPLv3 (repo) — ideas only | Analyze header exposure and type passing before porting; plan file; compare Rust vs C API; FFI crate with SAFETY comments; delete C after wiring |
| compiler-port (React) | SkillsMP repo 251,184★ | https://github.com/react/react/tree/main/compiler/.claude/skills/compiler-port | MIT | Source-folder → target-crate mapping table; plan before porting; test-fix loop to zero failures; review loop; no auto-commit |
| golang-refactoring (samber) | skills.sh 9,928 installs | https://github.com/samber/cc-skills-golang/tree/main/skills/golang-refactoring | MIT | Coverage-adaptive safety net; never mix structural and behavioral commits; separate move from optimization; tool-driven transforms; type aliases for gradual moves; revert instead of debugging forward |
| clean-code (davila7/claude-code-templates, aitmpl.com) | aitmpl 6,995 downloads | https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/development/clean-code | MIT | Checked for overlap; content left to simplify-code |

Platforms searched: skills.sh, SkillsMP, aitmpl.com, LobeHub, Smithery, MCP Market, SkillHub, ClawHub.

## Literature and articles
- Martin Fowler, *Refactoring* (2nd ed., 2018) and catalog — https://refactoring.com/catalog/
- Michael Feathers, *Working Effectively with Legacy Code* (2004) — characterization tests, seams, sprout/wrap
- Martin Fowler (Danilo Sato), *Parallel Change* — https://martinfowler.com/bliki/ParallelChange.html
- Martin Fowler, *Branch By Abstraction* — https://martinfowler.com/bliki/BranchByAbstraction.html
- Martin Fowler, *Strangler Fig Application* — https://martinfowler.com/bliki/StranglerFigApplication.html
- Ola Ellnestam & Daniel Brolund, *The Mikado Method* (2014)
- Joel Spolsky, *Things You Should Never Do, Part I* — https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/
- Hyrum's Law — https://www.hyrumslaw.com/
- Kent Beck, *Tidy First?* (2023) — separating structure changes from behavior changes
- PyO3 user guide (https://pyo3.rs/) and maturin (https://www.maturin.rs/) — Python↔Rust bindings; Go 1.27 release notes (https://go.dev/doc/go1.27) — generic methods; Go `encoding/json` docs (https://pkg.go.dev/encoding/json) — HTML escaping, nil slices, map key order
- Language references used for port tables: Go spec and Effective Go (https://go.dev/ref/spec, https://go.dev/doc/effective_go), Python docs (https://docs.python.org/3/), The Rust Reference and API Guidelines (https://doc.rust-lang.org/reference/, https://rust-lang.github.io/api-guidelines/), Kotlin Java interop docs (https://kotlinlang.org/docs/java-to-kotlin-interop.html), MDN JavaScript reference (https://developer.mozilla.org/docs/Web/JavaScript), serde_json docs (https://docs.rs/serde_json)

## Relation to simplify-code
`simplify-code` (same repository) owns local, behavior-preserving cleanup and its detailed behavior-trap list. This skill links to it instead of repeating it and focuses on multi-file restructuring, rewrites, and cross-language ports.
