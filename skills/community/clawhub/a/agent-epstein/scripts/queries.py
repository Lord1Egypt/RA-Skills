"""queries.py — ranked search plans for sources with loose or no tagging.

On a booru `yuri` is a tag: ask and you get exactly that. On X and Pixiv
there is no such guarantee — people post under a ship tag, a fandom
hashtag, or nothing at all. So a plan here is not one query but an ordered
list of candidates, ranked by expected yield, which the driver works
through while watching what actually returns.

    from queries import plan
    for q in plan("wuthering waves", ["jinhsi", "changli"]):
        print(q.text, q.weight, q.kind)

WHY RANKING MATTERS — measured, not assumed
------------------------------------------
X's media search ANDs every term. Adding one word can take a query from
five results to zero:

    "wuwa denrika"       ->  5 results
    "wuwa denrika art"   ->  0 results   <- "art" killed it

So the plan leads with the highest-precision form (a ship pair), and the
driver is expected to drop terms when a query comes back empty rather than
assume the art does not exist. That adaptive loop lives in harvest.py.

QUERY KINDS, in the order they are tried
----------------------------------------
  ship      "raiden x yae"          highest precision: a named pairing is
                                     almost always fanart of those two
  ship_tag  a pairing name the user supplied, used verbatim — never
            rewritten, because "Jinhli" and "jinhsi changli" are not the
            same search
  fandom    "wuthering waves yuri"  fandom + a term meaning two women
  hashtag   "#Jinhsi #Changli"      hashtag posts are disproportionately
                                     actual fanart, and are under-used
  generic   "yuri"                  last resort; mostly noise
"""
from __future__ import annotations

import itertools
import re
from dataclasses import dataclass, field

# Generic terms meaning "two+ women, romantically framed". Ordered by how
# often they actually appear in fan posts rather than by elegance.
CORE_TERMS = ("yuri", "girls love", "百合", "gl", "girls' love")

# Words that signal an actual pairing rather than a solo portrait.
PAIR_HINTS = ("ship", "pairing", "otp", "duo", "two girls")

# Fandom shorthand is often used instead of the full name.
SHIP_SEPARATORS = (" ", " x ", " / ", " & ")

# Booru tag syntax that means nothing in a social search box. Excluded by
# name so nobody re-adds it: X and Pixiv do not index tags.
NOT_SEARCH_TERMS = frozenset({"2girls", "2boys", "1girl", "1boy", "rating",
                             "absurdres", "highres", "wallpaper"})

# Weights, high = try first. Tuned by what the plan is for: precision
# first, then recall, with generic terms held back because they return
# almost nothing that survives vision verification.
WEIGHTS = {
    "ship_tag": 100,   # user-supplied, verbatim
    "ship": 90,        # generated character pair
    "hashtag": 70,     # aggressive mode only
    "fandom": 60,      # fandom + a relationship term
    "generic": 20,     # bare "yuri"
}


@dataclass(frozen=True)
class Query:
    """One candidate search, with why it is ranked where it is."""
    text: str
    kind: str
    weight: int = 0

    def __str__(self) -> str:                       # for logs
        return self.text


@dataclass
class Plan:
    """An ordered plan plus the bookkeeping the driver needs."""
    queries: list[Query] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def texts(self) -> list[str]:
        return [q.text for q in self.queries]

    def __len__(self) -> int:
        return len(self.queries)

    def __iter__(self):
        return iter(self.queries)


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def hashtagify(word: str) -> str:
    """'jinhsi' -> '#Jinhsi'. Already-hashed input is left alone."""
    w = _clean(word).replace(" ", "")
    return w if w.startswith("#") else "#" + w


def ship_pairs(chars: list[str], limit: int = 8) -> list[str]:
    """Pairwise ship queries, most conventional spelling first.

    Pairs every combination but caps the count: past a handful, the extra
    combinations are almost always characters nobody ships, and they crowd
    out the good queries in a small budget.
    """
    out: list[str] = []
    for a, b in itertools.combinations(chars, 2):
        for sep in SHIP_SEPARATORS:
            q = _clean(f"{a}{sep}{b}")
            if q and q not in out:
                out.append(q)
        if len(out) >= limit:
            break
    return out[:limit]


def plan(
    fandom: str = "",
    chars: list[str] | None = None,
    *,
    ship_tags: list[str] | None = None,
    aggressive: bool = False,
    extra_terms: tuple[str, ...] = (),
    max_queries: int = 24,
) -> Plan:
    """Build a ranked plan. Most precise first, never exceeding the cap.

    ship_tags  pairing names to use VERBATIM. These outrank everything
               because a real ship name is a better key than anything we
               could generate, and rewriting one changes what is found.
    aggressive additionally emit hashtag-compounded queries.
    """
    fandom = _clean(fandom)
    chars = [_clean(c) for c in (chars or []) if _clean(c)]
    tags = [_clean(t) for t in (ship_tags or []) if _clean(t)]
    terms = [t for t in dict.fromkeys(CORE_TERMS + tuple(extra_terms))
             if t.lower() not in NOT_SEARCH_TERMS]

    p = Plan()
    seen: set[str] = set()

    def add(text: str, kind: str) -> None:
        t = _clean(text)
        key = t.lower()
        if not t or key in seen or len(p.queries) >= max_queries:
            return
        seen.add(key)
        p.queries.append(Query(t, kind, WEIGHTS.get(kind, 50)))

    # 1. User-supplied ship tags, verbatim. Never rewritten.
    for t in tags:
        add(t, "ship_tag")
    if tags:
        p.notes.append(f"{len(tags)} user-supplied ship tag(s) used verbatim")

    # 2. Generated ship pairs — the highest-signal thing we can construct.
    if len(chars) >= 2:
        pairs = ship_pairs(chars)
        for pair in pairs:
            add(pair, "ship")
        if pairs:
            p.notes.append(f"{len(pairs)} generated ship pair(s) from "
                           f"{len(chars)} character(s)")
    elif len(chars) == 1:
        for t in terms[:2]:
            add(f"{chars[0]} {t}", "ship")
        add(f"{chars[0]} ship", "ship")

    # 3. Fandom + a relationship term. Fandom first, then term, because
    #    "wuthering waves yuri" is a far better query than "yuri wuthering
    #    waves" on sites that weight the leading term.
    if fandom:
        for t in terms[:3]:
            add(f"{fandom} {t}", "fandom")
        if len(chars) >= 2:
            add(f"{fandom} {' '.join(chars[:2])}", "fandom")
        add(f"{fandom} ship", "fandom")

    # 4. Hashtag compounding (aggressive only). People who hashtag their
    #    fanart are disproportionately posting fanart rather than reposts
    #    and screenshots, so this is worth its budget — but only when asked.
    if aggressive:
        if chars:
            add(" ".join(hashtagify(c) for c in chars[:2]), "hashtag")
            add(" ".join(hashtagify(c) for c in chars[:3]), "hashtag")
        if fandom and chars:
            add(f"{hashtagify(fandom)} {hashtagify(chars[0])}", "hashtag")
        for t in tags[:2]:
            add(hashtagify(t), "hashtag")
        p.notes.append("aggressive mode: hashtag-compounded queries included")

    # 5. Generic, last. Bare "yuri" returns plenty and almost none of it
    #    survives verification, so it only runs when nothing better did.
    for t in terms[:2]:
        add(t, "generic")

    if not p.queries:
        p.notes.append("plan is empty — give a fandom, characters or a tag")
    return p


def expand(
    fandom: str = "",
    chars: list[str] | None = None,
    extra_terms: tuple[str, ...] = (),
    max_queries: int = 24,
) -> list[str]:
    """Backwards-compatible flat list. Prefer `plan()` for new code.

    Kept because callers that only need the ordered strings should not have
    to care about weights.
    """
    return plan(fandom, chars, extra_terms=extra_terms,
                max_queries=max_queries).texts()


def relax(query: str) -> list[str]:
    """Progressively looser forms of a query, most specific first.

    Used when a query returns nothing. X ANDs its terms, so the fix for
    "wuwa denrika art" -> 0 results is usually to drop a word, not to give
    up. Each step drops or shortens something, so the caller can walk down
    this list until something comes back.

    Returns forms to try in order, excluding the original.
    """
    words = _clean(query).split()
    if not words:
        return []

    out: list[str] = []
    seen = {_clean(query).lower()}

    def push(text: str) -> None:
        t = _clean(text)
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)

    # Search-boilerplate words that carry no signal: dropping one of these
    # recovers results far more often than dropping a content word.
    noise = {"art", "arts", "fanart", "fan", "image", "images", "pic", "pics"}
    kept = [w for w in words if w.lower().strip("#@") not in noise]
    if len(kept) < len(words):
        push(" ".join(kept))

    # Drop trailing words one at a time, longest form first.
    for i in range(len(words) - 1, 0, -1):
        push(" ".join(words[:i]))

    # Hashtags alone often beat the hashtag plus words.
    hashes = [w for w in words if w.startswith("#")]
    if len(hashes) > 1:
        push(" ".join(hashes))
    elif len(hashes) == 1 and len(words) > 1:
        push(hashes[0])

    # Each character on its own, when the query was a pair.
    for w in words:
        if len(w) > 3 and not w.startswith("#"):
            push(w)

    return out


def x_filter_suffix(min_likes: int = 0) -> str:
    """X search operators that meaningfully cut noise.

    `min_faves:N` is applied server-side, so low-engagement posts never
    reach the page at all — much cheaper than fetching and discarding.
    """
    s = " filter:images -filter:replies -filter:retweets"
    if min_likes and min_likes > 0:
        s += f" min_faves:{int(min_likes)}"
    return s


def build_x_url(query: str, min_likes: int = 0) -> str:
    import urllib.parse
    q = query + x_filter_suffix(min_likes)
    return ("https://x.com/search?q=" + urllib.parse.quote(q)
            + "&src=typed_query&f=image")