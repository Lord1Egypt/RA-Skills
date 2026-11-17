# Making It Fast Enough

"Fast enough" is a number. Without one, optimization has no stopping condition and no way to fail. Profiler theory — sampling vs instrumentation, flame graph reading, allocation profiles — is `profiling`; this is the developer's route from "it's slow" to a measured win.

**Before optimizing**, read `## Baselines` in `~/Clawic/data/developer/repos/<repo>.md`. A previous measurement with its method and date is the difference between "we improved p95 by 40%" and "it feels faster now".

## The Sequence

1. **Reproduce the slowness** with a command you can repeat, on data of production shape and volume. Slow on 10 rows and slow on 10 million are different bugs.
2. **Measure the current number** and put it in `## Baselines` of the repo profile with how it was measured: p50/p95/p99 at a stated load, or wall time of the exact command.
3. **Set the target** and where it comes from: an SLO, a user-visible threshold, an upstream timeout. "Faster" is not a target.
4. **Find the dominant term** — profile, or count round trips. Optimizing anything else is a rounding error (Amdahl below).
5. **Change one thing**, re-measure the same way, and keep the number. If the change is under ~10%, it is inside measurement noise on most setups — prove it or drop it.
6. **Stop at the target.** Beyond it, you are trading readability for a number nobody asked for.

## Amdahl, as an Argument-Ender

Maximum speedup from making a part that is fraction `p` of runtime infinitely fast: `1 / (1 − p)`.

| Fraction of total time | Ceiling if made free |
|---|---|
| 5% | 1.05× |
| 30% | 1.43× |
| 50% | 2× |
| 80% | 5× |
| 95% | 20× |

Consequence: the 5% path is not worth touching however inefficient it looks, and a 2× improvement of a 30% term buys 15% overall. Compute the ceiling before starting, not after.

## Percentiles, Not Averages

The mean hides the users who leave. Report p50, p95, p99 — and know that the tail is where retries, timeouts and abandoned sessions live.

**Tail amplification** (Dean & Barroso, "The Tail at Scale"): if one request fans out to `n` independent calls and each has probability `q` of exceeding the p99 latency, the chance the slowest one does is `1 − (1 − q)ⁿ`. At n=100 and q=0.01 that is ~63% — a page composed of 100 backend calls hits its own p99 on most loads. Reduce the fan-out, or hedge the slow calls; tuning the mean will not move it.

## Where the Time Actually Goes

Ordered by how often each is the answer in application code:

| Cause | Signature | Fix |
|---|---|---|
| N+1 queries | Latency grows linearly with rows; query log shows the same statement repeated | Batch or eager-load: 1 + N at 200 rows and 2 ms each = 400 ms of pure round trips |
| Missing index | One query dominates; the plan shows a sequential scan on a large table | Index the predicate and the join column; verify with the plan, not with faith (`database-indexing`) |
| Serial calls that could be parallel | Total ≈ sum of the parts, and the parts are independent | Fan out concurrently, with a bound and a timeout each |
| Work inside a loop | Time per item is constant and the item count is the input | Hoist it out, or batch the whole set |
| Over-fetching | Payload much bigger than what is rendered | Select the columns and the fields you use |
| No caching on a repeated deterministic result | Same input, same expensive computation, many times | Cache with an explicit invalidation rule; `avg = h × fast + (1 − h) × slow`, so a 90% hit rate on a 200 ms call with a 2 ms cache gives ~22 ms |
| Wrong data structure | Cost grows faster than linearly; nested loops over the same collection | Index into a map; O(n²) at 10k items is 100M operations |
| Allocation and GC pressure | Sawtooth memory, pauses under load | Reuse buffers, stream instead of materializing (`profiling`) |
| Synchronous work in the request path | The endpoint waits for something the user does not need to wait for | Move it to a queue; the response returns before the work finishes |
| Cold start or lazy init | First request slow, rest fast | Warm at boot, or keep it warm |

## Benchmarks That Do Not Lie

- **Same machine, same data, same method**, before and after. A number measured differently is not a comparison.
- **Warm up** before measuring anything with a JIT, a cache, or a connection pool — the first iteration measures initialization.
- **Repeat and report the distribution**, not the best run. Report the median of ≥5 runs, and the spread.
- **Beware the optimizer**: a microbenchmark whose result is unused can be compiled away entirely. Consume the result.
- **Measure in the shape you ship**: release build, real serialization, real network hop. Local, unserialized, single-threaded numbers are a different program.
- **Load test with realistic concurrency**, because queueing is where systems fall over; throughput at 1 user says nothing about behavior at 200.

## Memory and Bundle Size

- Bundle/binary size is a latency budget on the client: state the budget in KB and check it in CI, or it grows monotonically.
- Memory leaks show as a rising floor after GC across hours, not as high usage. Compare heap snapshots at two idle points.
- Caches without bounds are leaks with better branding: every cache needs a max size or a TTL.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Optimizing without a profile | Intuition about bottlenecks is wrong more often than right | Measure, then Amdahl the candidate |
| Optimizing the readable code because it is easy to reach | Rarely the dominant term; you pay in clarity forever | Fix the round trips first |
| Reporting the average | Hides the tail that generates the complaints | p50/p95/p99 with the load stated |
| Comparing runs measured differently | Any result you want is available | Same method, written down with the number |
| Caching to fix a query you have not read | Adds an invalidation problem to the existing problem | Read the plan; index or batch first |
| Micro-optimizing inside an N+1 | Making 200 round trips 5% cheaper | Remove the round trips |
| Declaring victory from a local benchmark | Production has other tenants, cold caches, real network | Verify with production percentiles after rollout |
| Trading correctness for speed silently | The fast wrong answer is the expensive one | If precision or consistency is dropped, say so in the PR |

## Write Down the Numbers

- **Every measurement** — the before, the after, the method, the date → `## Baselines` in `~/Clawic/data/developer/repos/<repo>.md` (`memory-template.md`). Next quarter's "was it always this slow?" is answerable only if this row exists.
- **A performance decision with a rejected alternative** (denormalize, add a cache layer, move work to a queue) → `artifacts/adr-<topic>.md` with its `## Boxes` line.
- **A performance budget the team agreed to** (p95 under 300 ms, bundle under 250 KB) → the project file, and the check that enforces it into `## Conventions` of the repo profile.
