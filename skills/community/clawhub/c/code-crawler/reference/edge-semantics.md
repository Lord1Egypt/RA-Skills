# Edge semantics

Three things cause most misreads of this graph: `confidence`, `external`, and phantom
nodes. Read this before reporting "no callers", "dead code", or "unresolved".

## Edge kinds

| Kind | Means |
| --- | --- |
| `CALLS` | A statically resolved call |
| `DYNAMIC_DISPATCH` | A call that reaches an implementation through an interface or superclass |
| `ADVISES` | Around/before/after advice intercepting a method |
| `DECLARED_IN` | Symbol to its containing type |
| `CONTAINS` | Type to its members, module to its declarations |
| `IMPLEMENTS` | Type to the interface it implements |
| `EXTENDS` | Type to its superclass |
| `IMPORTS` | File to the module it imports |
| `ANNOTATED_WITH` | Symbol to an annotation or decorator |
| `REFERENCES` | A non-call reference, such as a field or type use |
| `REFLECTS` | A runtime lookup that may reach a symbol |
| `INJECTS` | A DI-supplied dependency: a field or parameter the container fills |
| `ROUTES` | An HTTP route to its handler |
| `EMITS` | A published event or message to the listener it feeds |

A method reached only by `DYNAMIC_DISPATCH`, `ADVISES`, `ROUTES`, or `EMITS` **is still called**.
When asking "who calls this", look at all inbound edge kinds, not just `CALLS`.

Spring wiring is usually not annotated. The sole constructor of a `@Service` is autowired
without `@Autowired`, and a Lombok `@AllArgsConstructor` writes no constructor into the
source at all. `find_injections` reports these; grepping for `@Autowired` will not.

FastAPI wiring is named indirectly. `SessionDep = Annotated[Session, Depends(get_db)]` is
declared once and then used as a bare parameter type, and the handler may also take
`dependencies=[Depends(require_superuser)]` at the decorator. Both produce an `INJECTS`
edge; grepping a handler for `Depends` finds neither.

Read the two ends of an `INJECTS` edge carefully: the **source is what the framework
populates** - a constructor's type, or the function whose parameters are filled - and the
**target is the provider the framework calls**. So `service: OrderService =
Depends(get_service)` is an edge to `get_service`, not to `OrderService`: the container
invokes `get_service` and passes back whatever it returns. That distinction is what
`confidence` measures here: `1.0` when the provider is named at the injection site, `0.95`
when one project type matches the declared type, `0.85` when reached through a dependency
alias, `0.8` for a package outside the index, and `0` when the dependency exists but cannot
be named at all.

`ROUTES` confidence answers a narrower question - whether the attached handler is the one
dispatched to. The path and HTTP method are read from source and are exact; only the
handler lookup can be indirect, so `0.6` on a `ROUTES` edge means two handlers in the same
file matched equally and the first was kept.

Spring's event bus and messaging brokers are the same shape, with `EMITS`: the **source is
the publisher method** (the one that hands a message to the framework) and the **target is
the listener the framework then calls**. `OrderPublisher#place` publishing `OrderPlaced`
emits to every `@EventListener` for `OrderPlaced`; a Kafka `send("orders")` emits to every
`@KafkaListener(topics = "orders")`. This edge is the only link between the two - no
`CALLS` edge ever joins them, because the framework, not the code, makes the call. Turn it
off with `include_events: false` on `get_callers`, `get_callees`, and `trace_path`.

Only two things name a channel: a constructed event object (`new OrderPlaced(...)`, or a
local whose declared type is the event) and a literal topic/queue/destination string. A
channel computed at run time, or a published plain parameter, produces no edge - it is
reported as absent rather than guessed. An `EMITS` edge carries `channel`, `channelKind`
(`event-class` or `topic`), and `framework`. A `@TransactionalEventListener` additionally
carries `phase` (`BEFORE_COMMIT`, `AFTER_COMMIT`, `AFTER_ROLLBACK`, `AFTER_COMPLETION`):
that says *when* the listener runs, not whether the edge exists, so it does not lower
confidence - but an `AFTER_ROLLBACK` listener will not run on the happy path.

## `confidence` is a band, not a probability

Do not average it, threshold it, or present it as certainty. It is a coarse label telling
you *what kind of evidence* produced the edge.

Every edge that names an inferred target carries a number: `CALLS`, `DYNAMIC_DISPATCH`,
`ADVISES`, `INJECTS`, `ROUTES` and `EMITS`. Structural edges (`DECLARED_IN`, `CONTAINS`,
`IMPLEMENTS`, `EXTENDS`, `IMPORTS`, `ANNOTATED_WITH`, `REFERENCES`) do not - they are read
from a declaration, so there is nothing to be uncertain about.

| Value | Evidence |
| --- | --- |
| `1.0` | Resolved by construction - a constructor, overload, or event type matched exactly; a route handler declared in the type that registers it |
| `0.95` | One project declaration matches the name, with no rival in scope |
| `0.9` | Same-module declaration, typed local, or default constructor |
| `0.85` | Imported from a named module, or a literal topic/queue name |
| `0.8` | Inherited from a supertype, or an external target |
| `0.75` | Call to an imported class resolved through its import |
| `0.6` | Pointcut `args(...)` matched on arity only, an ambiguous overload tie, or a tie between handlers |
| `0.55` | Pointcut primitive matched by static approximation |
| `0.3` | Empty pointcut - the advice matches everything |
| `0` | Phantom - nothing was resolved |

The same numbers mean the same thing across kinds: for `CALLS` and `DYNAMIC_DISPATCH` they
describe the callee's identity, for `INJECTS` the **provider the container calls**, for
`ROUTES` the **handler the framework dispatches to**. None of them describe whether the
edge fires at run time - a `@Transactional` method marked `inert`, or a listener whose
publisher is outside the index, still has a confident edge.

Practical rule: `>= 0.75` is safe to report as fact, `0.5`-`0.7` deserves a hedge, and `0`
carries no information about the target at all.

## Ambiguous calls carry ranked candidates

Overload resolution is where a static graph most often reports a confidence it has not earned.
When a call site matches several overloads equally, the resolver keeps the first declaration as
the edge target and lists the rival ones on the edge instead of discarding them:

| Field | Where | Meaning |
| --- | --- | --- |
| `alternatives` | `CALLS` edge, `get_callers` / `get_callees` row, `trace_path` edge | other overloads the same call site could equally target |

An edge with `alternatives` is still `resolved: true`: the call site is proven, only the choice
among rivals is uncertain. Confidence is capped at `0.6` whenever alternatives exist, so it
always lands in the hedge band and never in the "safe to report as fact" band.

Report the ambiguity instead of picking one. Say "calls `Formatter#render`, could equally be
`Formatter#render(String)`", not "calls `Formatter#render`". Reading the argument's declared type
at the call site usually settles it.

Rivals are only detected within one declaration list. Once resolution reaches an inherited
method the pool has already been narrowed to a single candidate, so an inherited overload tie is
not reported. A missed rival never invents a wrong target - it only leaves the edge looking more
certain than it is.

## Proxy boundaries are node properties, not edges

`@Transactional`, `@Async` and `@Cacheable` do not add an edge. The proxy intercepts the
*same* invocation the `CALLS` edge already describes, so a separate edge kind would duplicate
the call graph and double-count every influenced call. The facts live on nodes and caller rows
instead:

| Field | Where | Meaning |
| --- | --- | --- |
| `proxies` | type and method node | proxy kinds declared on the declaration or inherited from the class |
| `proxy` | `get_callers` row | the proxy kinds in front of the callee for this call |
| `proxyBlocked` | method node, `get_callers` row | `private`, `static`, `final`, `final-type` — the container cannot honour the annotation |
| `inert` | `get_callers` row | self-invocation: the call never crosses the proxy |

These are categorical, not scored. A `proxyBlocked` value names the exact reason, which is
more useful than any confidence number: the annotation is present in source and provably does
nothing at run time. Report `inert: true` and `proxyBlocked` alongside the annotation, never
instead of it.

`inert` appears only on direct callers. A proxy wraps one invocation, so at depth 2 the
proxied call no longer exists and flagging it would describe a phantom.

Only annotations listed in the framework table are recognised, and only for Java: a custom
annotation meta-annotated with `@Transactional` is not followed, and neither is a proxy
declared in XML (`<tx:advice>`).

## `external` means outside the project

An edge with `external: true` points at a node like `ext:axios` or `ext:fastapi`, and its
`externalModule` names the package.

Consequences that are easy to get wrong:

- An external target is **not** dead code. It is a real dependency you do not index.
- An external target is **not** an unresolved call. It was resolved, just to the boundary.
- `find_dead_code` ignores external targets, so a method whose only caller is external can
  still look dead. Cross-check `find_external_dependencies`.

## Phantom nodes

A phantom target means the resolver saw a call but could not name its destination. Phantoms
carry `confidence: 0` and `resolved: false`, and their ids are prefixed:

| Prefix | Origin |
| --- | --- |
| `__phantom__:` | A call site with no resolvable target |
| `__reflect__:` | A runtime lookup whose type or method was not found |
| `__inject__:` | An injection marker that named neither a type nor a package |

An unresolved injection is still an edge. The placeholder is materialised as a node with
`reason: "unresolved injected type"` and the edge keeps `confidence: 0`, so the dependency
counts and reads as unresolved. It is never deleted from the graph for want of a target.

Phantoms are **inventory, not findings**. A phantom is a statement about the analyser, not
about the code. Never report one as "calls something unknown" without reading its `reason` -
that field says which lookup step failed.

## Why "no callers" can be legitimate and wrong at the same time

Five ways a real caller produces no inbound `CALLS` edge:

1. **The index is stale.** Always `index_status` first. This is the most common cause.
2. **Dynamic dispatch.** The call goes through an interface; look for
   `DYNAMIC_DISPATCH` inbound edges and use `find_implementations`.
3. **Framework invocation.** Routes, listeners, schedulers, and tests are entry points,
   not calls. Check `find_entry_points` and `find_routes`. A listener is reached from its
   publisher by `EMITS` - if the publisher is outside the index, the only inbound edge is
   missing, so check `find_event_flows` for the inbound side of a channel.
4. **Reflection.** `Class.forName`, `getattr`, `importlib`, and dynamic `import()` produce
   `REFLECTS` edges, not `CALLS`. Check `find_reflections`.
5. **The caller is external.** Only in-project call edges are recorded. Check
   `find_external_dependencies`.

So the correct phrasing is "no in-project static callers", not "unused".

## Stale indexes and `force`

Incremental crawls compare file content and mtime against a manifest. That covers normal
editing. It does **not** cover the working tree changing underneath the index:

- after a rebase, merge, or `git reset` that rewrote history
- after switching branches with a large diff
- after `git stash pop`

A file whose content changed but whose mtime was reset can be skipped, leaving edges that
point at declarations that no longer exist. Pass `force: true` to `crawl_project` in those
cases. If results look impossible, forcing a re-index is cheaper than debugging the graph.

## Token budgeting

List-returning tools accept `max_tokens` and `cursor`, adding a `page` block with
`totalCount`, `returnedCount`, `truncated`, `estimatedTokens`, and `nextCursor`.

Truncation is reported, never silent: if `truncated` is true the answer is incomplete and
you should either widen `max_tokens` or say so. Paging never returns an empty page while
items remain, so a continuation loop terminates.
