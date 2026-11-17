# Phase 3: Emit Google OKF v0.1

OKF is the default target. Create one self-contained bundle:

```text
<bundle>/
  index.md
  facts/<fact>.md
  dimensions/<dimension>.md
  metrics/<measure>.md
  references/<operation>.md
  log.md                 # optional
```

Map the semantic catalog to root `index.md` with `okf_version: "0.1"`; facts to `Semantic Fact`,
dimensions to `Dimension`, measures to `Metric`, and source operations to `API Endpoint`. Fact
bodies contain Grain, Dimensions, Schema, and Citations; dimensions contain Schema and Citations;
metrics contain Definition and Citations; operations contain input/output Schema and Citations.

Each concept file has stable ID/path, type, name, description, and citations in frontmatter as
required by OKF. Use relative links and resolvable IDs. The root index is the only index with
frontmatter; child indexes list entries. Optional `log.md` uses dated newest-first sections.

Create cross-links from facts to dimensions and metrics, from metrics to facts and source fields,
and from every modeled field to operation/table evidence. Never add a concept whose supporting
decision is not approved.
