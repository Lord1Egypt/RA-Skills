# Errand Routing — Model & Math Reference

## 1. The real problem

A day of errands is a **Traveling Salesperson Problem with Time Windows
(TSPTW)**:

- Nodes: your stops (post office, pharmacy, grocery, …) plus start/end.
- Edge weights: travel time between stops.
- Node service time: how long you spend inside ("dwell").
- Time windows: `[open, close]` per stop; arriving early means waiting,
  arriving late means the stop is impossible.

TSPTW is NP-hard in general — but errand runs have **n ≤ 10–12 stops**,
where construction heuristics + 2-opt local search produce routes within
a few percent of optimal in milliseconds, with zero dependencies.

## 2. Distance model

### Haversine (lat/lon input)

```
a = sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2)
d = 2R · asin(√a),  R = 6371 km
```

Accurate to ~0.5% at city scale. Good enough — routing errors at errand
scale come from traffic and parking, not geodesy.

### Local grid (x/y input)

Euclidean distance in whatever unit you supply (state units in the JSON:
`"units": "km-local"`). Useful when the user says "3 km north, 2 km east".

### Road factor

Straight-line × **1.3** → approximate street-network distance. This is the
widely used detour-index planning value (real urban networks run 1.2–1.4).
No routing engine available? 1.3 is the honest default.

### Travel time

```
t = d_road / v        v default 30 km/h
```

30 km/h is the door-to-door average for mixed urban driving including
traffic lights and parking. Highway-heavy routes: use 60–70 km/h.

## 3. Time-window feasibility

Given arrival time `A_i` at stop i with window `[o_i, c_i]` and dwell `s_i`:

```
service_start_i = max(A_i, o_i)
feasible_i      ⇔ service_start_i + s_i ≤ c_i
wait_i          = service_start_i − A_i
departure_i     = service_start_i + s_i
```

`close` is a **hard** constraint (route moves that violate it are
rejected); `open` is **soft** (you just wait — the tool reports wait time
so the user can decide whether waiting is worth it).

## 4. Solution algorithm

### Construction: nearest feasible neighbor

Start at the depot; repeatedly append the stop with the smallest
`travel_time(current, candidate)` among stops still feasible given the
running clock. If none is feasible, append the nearest infeasible stop
anyway and flag it — a flagged route is still information (tells the user
the plan cannot work as specified).

### Improvement: 2-opt with feasibility check

For a route `[0, 1, …, n, 0]`, a 2-opt move reverses a segment
`(i+1 … j)`:

```
before: … i, i+1, …, j, j+1 …
after:  … i, j, …, i+1, j+1 …
```

Accept the move iff (a) total travel time decreases and (b) the whole
route remains time-window feasible (re-simulate the clock — cheap at this
size). Iterate until no improving move exists. Typical errand instances
converge in < 100 moves.

Why not exact DP (Held-Karp)? It's O(n²·2ⁿ) — fine for n ≤ 12 too, but
2-opt + NN is simpler, and for errands the difference is rarely visible.
Upgrade path: if you need guaranteed optimality at n ≤ 12, add Held-Karp;
keep 2-opt for n > 12.

## 5. Interpreting the output

| Field | Meaning |
|---|---|
| `order` | visit sequence including start/end |
| `legs[].km` | road-factor distance for that leg |
| `legs[].drive_min` | driving time at the chosen speed |
| `arrival` / `departure` | clock at the stop (after any wait) |
| `wait_min` | time spent waiting for `open` |
| `violations` | stops where you'd arrive after `close` |
| `totals` | km, drive, dwell, wait, elapsed |

## 6. Extension points

- **Multiple days**: add a max-duration cutoff; stops that don't fit roll
  to day 2 automatically (re-run with the remaining set).
- **Priority stops**: give must-do stops a `required: true` flag; optional
  ones can be dropped by `--max-km` trimming.
- **Live traffic**: replace the constant speed with per-leg speeds from a
  maps API — the algorithm is unchanged; only the matrix changes.
- **Transit/walk/cycle mixes**: per-leg `mode` with per-mode speed
  (walk 5, cycle 15, transit 20 km/h effective incl. waits).

## 7. Validation values

- 1° latitude = 111.19 km (Berlin↔Munich ≈ 505 km haversine vs 585 road).
- 1° longitude at 52.5°N = 111.19 × cos(52.5°) ≈ 67.7 km.
- Two identical coordinates ⇒ distance 0, drive 0.
- A stop with `close` earlier than earliest possible arrival ⇒ always
  flagged, never silently dropped.
