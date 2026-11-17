# Starting Something New

A greenfield project is a short window in which a handful of decisions become permanent and everything else stays cheap. The job is to identify which is which, decide the permanent ones deliberately, and refuse to decide the rest yet (SKILL.md Reversibility).

**Before starting**, read `## Repos` in `~/Clawic/data/developer/memory.md` and the profile of the closest existing repo: the team's conventions, its CI, and its operational habits already exist, and matching them is worth more than a better greenfield choice nobody else can operate.

## Decide Now (Expensive to Reverse)

| Decision | Decide by | Not by |
|---|---|---|
| Language and runtime | What the team can debug and operate at 3am; what the ecosystem offers for this problem | Benchmarks, or what is new |
| Data model and key semantics | The queries you already know you need, and what the identifier means to the business | The entity diagram in your head |
| Datastore | Access pattern, consistency requirement, and who operates it | Familiarity alone, or scale you do not have |
| Auth and tenancy boundary | Whether a second customer/tenant can exist — decide before the first ships | Deferring; retrofitting tenancy is a rewrite |
| Public contract shape | Versioning strategy from the first consumer (`api-design`) | Shipping v1 and hoping |
| Deployment target and its constraints | What you can roll back in minutes | What the demo used |
| Time and money representation | UTC, integer minor units, currency stored alongside the amount | The default type |

Each of these gets an ADR — one page: the decision, the alternatives, why, the cost accepted, and the condition that would make you revisit.

## Defer (Cheap Later, Expensive Now)

Microservice boundaries, caching layers, message queues, an abstraction layer over the database, a plugin system, an admin UI, multi-region, and every optimization. Each of these is real engineering for a problem you have not met; a monolith with clear internal modules can be split when the seams are known, and the seams are not known on day one.

Frameworks are in between: they are cheap to adopt and expensive to remove, so contain them at the edges — your domain code should not import the web framework.

## Day One Skeleton

The bar: someone else can clone it, run it, test it, and deploy a change on their first day.

1. **Repo with a README that is the run instructions**, and nothing aspirational.
2. **One command each** to install, run, test, lint, and reset (`environments.md`).
3. **CI from the first commit**: install, lint, test, build. Adding CI to a repo with 200 commits of red is a project of its own.
4. **A deploy that works and a rollback that has been used**, both before the first feature. Ship "hello world" to production on day one — every deployment problem discovered then is discovered without a deadline.
5. **Health check, structured logging, and one error-reporting sink**, from the start. Retrofitting observability during the first incident is the most common regret in this list (`observability`).
6. **Secret handling decided** — where they come from at runtime, how they are supplied locally (`security.md`).
7. **A test that asserts something real**, so the harness exists and the first bug has a home (`tests.md`).
8. **Formatter and linter configured and enforced in CI**, so style is never a review topic again (`reviews.md`).

## Structure That Ages Well

- **Organize by feature or domain, not by technical layer.** `orders/` containing its handler, logic and storage beats `controllers/`, `services/`, `models/` each containing a third of every feature: a change lands in one folder, and the boundary is visible.
- **One direction of dependency**: domain logic knows nothing about HTTP, the database, or the framework. Anything that makes you wire "the framework calls my code" rather than "my code calls the framework" is on the right side.
- **A boundary is a place you can test through.** If you cannot write a test at that seam, it is not a boundary yet, it is a naming convention.
- **Keep the shared/common folder empty as long as possible.** It is where coupling accumulates under a neutral name.
- **Name things in the language of the business.** Names outlive implementations, and a wrong domain word costs more than a wrong data structure (`naming`).

## Choosing Boring

Prefer the option with more people who have operated it in production, more answers to failure-mode searches, and a longer track record. Novelty is a budget: spend it on the one thing that is genuinely your problem, and be boring everywhere else. A new language, a new datastore and a new deployment model at once means every incident has three suspects and nobody on the team has debugged any of them.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Architecting for the scale you hope for | Complexity now, certainty never; the scale arrives with different requirements | Build for 10× current, design so 100× is a known change |
| Microservices on day one | Distributed system problems before you have product-market fit for the domain boundaries | Modular monolith; split when a seam proves itself |
| Deferring auth and tenancy | Retrofitting isolation touches every query | Decide the boundary before the second tenant exists |
| Skipping CI "until there is something to test" | Standards never get retrofitted; red becomes normal | CI on commit one |
| First deploy after the first feature | Deployment problems arrive with a deadline attached | Deploy hello world on day one |
| Copying a starter template you cannot explain | You inherit decisions and dead code you cannot justify | Start minimal; add each piece when you can say why |
| A design document instead of running code | The uncertainty is in the integration, and paper does not test it | Spike the risky integration first (`estimation.md`) |
| Choosing three new technologies at once | Every failure has three suspects | One novelty budget, spent deliberately |

## Write Down the Decisions

- **Every "decide now" row** → `~/Clawic/data/developer/artifacts/adr-<topic>.md`: decision, alternatives rejected, cost accepted, revisit condition, date. Add each `## Boxes` line in the same turn (`memory-template.md`). These are the questions that get re-litigated most and are cheapest to answer from a file.
- **The new repo** → its profile at `repos/<repo>.md` and its row in `## Repos`, populated as you make the choices rather than reconstructed later (`codebase.md`).
- **The project itself** → `~/Clawic/data/projects/<project>.md` with objective, status, and the one-line summary of each decision pointing at its ADR by filename.
- **People who own or sponsor it** → `~/Clawic/data/contacts/contacts.md`.
