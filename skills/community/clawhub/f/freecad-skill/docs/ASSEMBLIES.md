# Assemblies

Read this before using `assembly` or `joint`.

## Assemblies

```json
{"op": "assembly", "name": "Hinge", "parts": [{"object": "Plate"}, {"object": "Pin"}]},
{"op": "joint", "assembly": "Hinge", "type": "revolute", "offset": -10,
 "a": {"part": "Plate", "edge": "%CIRCLE and >Z"}, "b": {"part": "Pin", "edge": "%CIRCLE and <Z"}}
```

- **Parts:**
  - Parts are links to existing solids or bodies. Editing the original updates every instance; add the same
    object twice under different `name`s.
  - The first part is grounded (fixed in place) unless you set `ground`.
  - A part keeps the position it was modelled at unless you give `position`/`rotation`. Joints then move it.
  - The result lists a bill of materials (`bom`: part, quantity, material, mass each); `inspect` the assembly
    to get it again. Exported as STEP, the assembly keeps its structure: each part once, with its name.
  - The assembly is the result: export or render the assembly itself. `measure` on the assembly compares its
    parts as assembled (or name single parts by their link, e.g. `Pin_Part`).
- **Joints:**
  - Each side gives a part and **exactly one** face or edge.
  - A face gives a frame at its centre, along its normal; a circular edge gives its centre and axis.
  - Part `b` moves to meet part `a`.
  - `offset` is the distance of `b` from `a`'s surface: positive moves it away, negative sinks it into the
    material (e.g. a pin into a hole).
  - Typical uses: a block on a plate is `fixed` face to face; a pin in a hole is `revolute` on circular
    edges; a shaft that also slides is `cylindrical`.
  - The two elements are placed on each other, so the choice of edges sets the layers. A hole's top edge on
    another part's top edge sinks it into that part; the top edge of `a`'s hole with the bottom edge of `b`'s
    hole stacks `b` on `a`; `offset` adds a gap (a washer).
  - Linkages: links in one plane overlap at every joint (`INTERFERENCE`), as they would in reality. Stack
    each link on the one it hinges on, e.g. crank on the ground plate, coupler on the crank, and the rocker
    under the coupler and on its own pivot.
  - Closed loops (four-bar, crank-slider) work: set `ground` on every fixed part and add the joints in
    order, the last one closing the loop. To get a particular pose (e.g. which way the crank points), give the
    moving parts an approximate `position`/`rotation` in `assembly`. A loop whose lengths can't close fails.
  - Selector extremes (`<X`, `>X`) are taken over all edges, so on a link with rounded ends they pick the end
    arc, not the hole: there, give hole edges by index (`inspect` with `topology: true`).
- **Checks:**
  - Every joint is verified after solving, so a joint that can't be satisfied, e.g. a conflicting one,
    fails the request.
  - Overlapping parts are reported as `INTERFERENCE` warnings with their overlap volume. Check them with
    `measure` too. Parts not joined yet are listed in `not_joined` and left out of that check.
- **After edits:** joints are re-resolved and the assembly re-solved after every edit, so parts follow
  dimension changes.
