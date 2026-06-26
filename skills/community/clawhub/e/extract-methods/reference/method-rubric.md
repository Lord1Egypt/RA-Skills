# What makes a good method entry

A **method** is a reusable *way of doing research* that a paper uses or proposes — not a finding, not a problem, not a full idea. You are cataloguing the research toolkit, so that later agents can ask "what methods exist for X" and "which papers use method Y".

## The five kinds

| kind | 中文 | what it is | examples |
|------|------|------------|----------|
| `paradigm` | 研究范式 | an overarching framework / mode of inquiry | supervised learning · ab-initio simulation · high-throughput screening · randomized controlled trial |
| `approach` | 科研思路 | a strategy / line of attack within a paradigm | transfer learning · active learning · embed-then-cluster · ablation study |
| `technique` | 技术手段 | a concrete procedure / means | data augmentation · k-fold cross-validation · cyclic voltammetry · attention masking |
| `algorithm` | 算法 | a named, specifiable algorithm | gradient descent · MCTS · DBSCAN · beam search |
| `model` | 模型 | a named model / architecture | Transformer · diffusion model · B3LYP functional · random forest |

When a candidate could be two kinds, pick the one the paper leans on: a *named architecture* → `model`; a *named procedure* → `algorithm` or `technique`; a *broad mode of working* → `paradigm`/`approach`.

## Extraction bar (quality over quantity)

- Extract the methods that **carry the paper's work** — the ones it uses to get its results or the ones it proposes. A method merely cited in the related-work section is *not* this paper's method.
- A typical empirical paper yields a handful (1–5); a method/architecture paper may propose one central method plus a few supporting techniques; a pure survey may yield only the paradigm it surveys.
- Prefer the **specific** name over a vague umbrella ("self-attention" not "neural networks") — but not so specific it's unreusable ("Transformer" not "the 12-layer model in Table 3").

## Writing the fields

- **title** — the method's canonical name (e.g. "Diffusion model", "Cyclic voltammetry"). This is what others search and dedupe on, so use the established name.
- **data.kind** — one of the five above.
- **data.description** — one short paragraph: what the method *is* (so a reader unfamiliar with it gets the gist) **and** how *this paper* uses it. The first half makes the entry reusable; the second grounds it.
- **data.keywords** — search terms / aliases (e.g. ["self-attention", "scaled dot-product attention"] for Transformer) — this is the full-text de-dup signal, so include common aliases.
- **data.source_literature** — the paper id you extracted it from.
- **domains** (top level) — inherit the paper's domains.

## Per-kind cap

At most **one method per kind per paper**. When several candidates of the same kind appear, keep only the single most important / most load-bearing one. If a kind has no strong candidate, extract none — omission is fine; prefer quality over coverage.

## De-dup, don't duplicate

The same method recurs across papers. Before publishing, `search` methods by the name + aliases. If it already exists, **don't** publish a second copy — call `link_method_literature` with `{"params": {"method_id": "<existing id>", "literature_id": "<this paper id>"}}` to record that this paper also uses that method (adds the current paper to the method's associated-literature set; idempotent). Only publish when it's genuinely a new method or a distinct, named variant.
