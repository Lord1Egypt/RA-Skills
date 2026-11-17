"""search.py — the adaptive loop that works through a query plan.

A fixed fan-out list is the wrong shape for X and Pixiv. Measured on a
real session: "wuwa denrika" returned 5 results and "wuwa denrika art"
returned 0, because X ANDs every term. A list that treats those as two
independent shots either wastes the budget or reports a false zero.

So the driver here is a feedback loop:

    pick the highest-ranked untried query
      -> run it
      -> if it yielded, keep the rank and move on
      -> if it yielded nothing, relax it (drop search-boilerplate words,
         then trailing words) and try the looser forms
      -> stop when the target is met, the plan is exhausted, or the yield
         rate has decayed past a threshold for long enough that more
         scrolling is not worth it

Nothing here decides what CONTENT is acceptable. That stays with the vision
filter. This only decides where to look next.

    from search import SearchDriver
    d = SearchDriver(target=10)
    for batch in d.run(fetch):        # fetch(q, want) -> list[dict]
        ...
    print(d.summary())
"""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field

from queries import Query, plan, relax  # noqa: F401  (Query re-exported)


@dataclass
class Attempt:
    query: str
    kind: str
    found: int = 0
    relaxed_from: str = ""
    seconds: float = 0.0


@dataclass
class SearchDriver:
    """Works a ranked plan, reacting to what each query actually returns."""

    target: int = 10
    # Stop when this many consecutive queries in a row return nothing, even
    # after relaxing. Three is deliberate: one empty query is ordinary on X,
    # three in a row means the whole tail of the plan is dry.
    dry_streak_limit: int = 3
    # Stop when yield has decayed below this fraction of the best run so far.
    diminishing_ratio: float = 0.25
    min_attempts_before_stop: int = 3
    delay: float = 1.0
    verbose: bool = True

    plan: list[Query] = field(default_factory=list)
    attempts: list[Attempt] = field(default_factory=list)
    seen_keys: set = field(default_factory=set)
    rows: list[dict] = field(default_factory=list)
    stopped_because: str = ""

    # -- logging ---------------------------------------------------------
    def _say(self, msg: str) -> None:
        if self.verbose:
            print(f"    {msg}", flush=True)

    # -- the loop --------------------------------------------------------
    def run(self, fetch, *, key=None, target: int | None = None) -> list[dict]:
        """Drive the plan.

        fetch(query_text, want) -> list[dict]
        key(row) -> hashable identity, for cross-query dedupe

        Returns every row collected. Deduplicated across queries, so a
        post that appears under three queries is stored once.
        """
        want = self.target if target is None else target
        key = key or (lambda r: r.get("source_id") or r.get("file_url"))
        i = 0
        dry = 0
        best = 0

        while i < len(self.plan) and len(self.rows) < want:
            q = self.plan[i]
            i += 1
            remaining = want - len(self.rows)
            got = self._attempt(q.text, q.kind, min(remaining, 12), fetch, key)
            best = max(best, got)

            if got:
                dry = 0
                continue

            dry += 1
            # The query was dry. Try looser forms of THIS query before
            # abandoning it, because one over-specific term is the common
            # cause rather than genuine absence.
            for looser in relax(q.text):
                if len(self.rows) >= want:
                    break
                if self._try_budget_exhausted():
                    break
                got2 = self._attempt(
                    looser, f"{q.kind}+relaxed", min(want - len(self.rows), 12),
                    fetch, key)
                if got2:
                    dry = 0
                    break

            if dry >= self.dry_streak_limit:
                self.stopped_because = (
                    f"{dry} consecutive queries returned nothing after "
                    f"relaxing")
                break

            if (len(self.attempts) >= self.min_attempts_before_stop
                    and len(self.rows) and got < best * self.diminishing_ratio
                    and dry >= 2):
                self.stopped_because = (
                    f"yield decayed to {got} vs best {best} "
                    f"({len(self.rows)}/{want} collected)")
                break

        if not self.stopped_because:
            self.stopped_because = (
                f"plan exhausted ({len(self.attempts)} attempt(s))")
            if len(self.rows) < want:
                self.stopped_because += (
                    f", target of {want} not reached")
        return self.rows

    def _try_budget_exhausted(self) -> bool:
        return len(self.attempts) >= max(8, 4 * max(1, self.target))

    # -- one attempt -----------------------------------------------------
    def _attempt(self, text: str, kind: str, want: int, fetch, key) -> int:
        if want <= 0:
            return 0
        t0 = time.time()
        try:
            got = fetch(text, want) or []
        except Exception as e:                                   # noqa: BLE001
            self._say(f"{text!r} -> ERROR {type(e).__name__}: {e}")
            self.attempts.append(Attempt(text, kind, 0, "",
                                        time.time() - t0))
            return 0

        fresh = 0
        for r in got:
            try:
                k = key(r)
            except Exception:                                    # noqa: BLE001
                k = id(r)
            if k in self.seen_keys:
                continue
            self.seen_keys.add(k)
            self.rows.append(r)
            fresh += 1

        dt = time.time() - t0
        self.attempts.append(Attempt(text, kind, fresh, "", dt))
        self._say(f"{text!r:44} -> {fresh} new / {len(got)} returned")
        if self.delay and fresh and len(self.rows) < want:
            time.sleep(min(self.delay, 1.5))
        return fresh

    # -- reporting -------------------------------------------------------
    def summary(self) -> str:
        dry = [a for a in self.attempts if not a.found]
        lines = [
            f"searched {len(self.attempts)} quer(y/ies) "
            f"-> {len(self.rows)} unique item(s)",
            f"stopped because: {self.stopped_because}",
        ]
        if dry:
            lines.append(f"{len(dry)} quer(y/ies) returned nothing:")
            for a in dry[:8]:
                lines.append(f"    {a.query!r} ({a.kind})")
        return "\n".join(lines)

    def to_report(self) -> dict:
        return {
            "attempts": len(self.attempts),
            "collected": len(self.rows),
            "stopped_because": self.stopped_because,
            "dry_queries": [a.query for a in self.attempts if not a.found],
            "queries_tried": [a.query for a in self.attempts],
        }