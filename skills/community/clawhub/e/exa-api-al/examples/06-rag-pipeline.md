# Example 06 — RAG Pipeline (Grounded Generation)

Use Exa `search`/`contents` as the retrieval layer of a Retrieval-Augmented Generation pipeline: retrieve, chunk, generate strictly from retrieved context, and cite chunks. Avoid hallucination by never asserting anything absent from the retrieved text.

## User request

> "Using only current documentation, explain how to configure rate limiting in the
> Acme API gateway, with code examples. Don't make anything up."

## Agent reasoning summary

- The user demands strict grounding ("don't make anything up") — this is RAG, not freeform answering.
- Retrieve with `search`, fetch authoritative full `text` with `contents`, chunk it, and generate only from those chunks.
- Cite each chunk; if the docs don't cover something, say so rather than inventing config.

## Exa operation to use

Use **`search`** (find the right docs pages) → **`contents`** (full `text` for chunking).

- Why: RAG needs faithful, complete source text to chunk and ground against. `search` locates the canonical docs; `contents` returns clean `text` suitable for chunking/embedding.
- Cost tradeoff: full `text` via `contents` on a few authoritative pages is the right spend for grounding. **Alternative single call: `/answer`** returns `{answer, citations}` in one request — cheaper and simpler when you do NOT need to own the chunking/retrieval layer (see note at end). Use the manual RAG path when you need control over chunk selection, custom prompts, or your own LLM.

## Request shape

Step 1 — locate the docs:

```json
POST /search
{ "query": "Acme API gateway rate limiting configuration",
  "type": "auto", "numResults": 5,
  "includeDomains": ["docs.acme.com"],
  "contents": { "highlights": { "numSentences": 2 } } }
```

Step 2 — fetch full text of the top docs page(s) for chunking:

```json
POST /contents
{ "urls": ["https://docs.acme.com/gateway/rate-limiting"],
  "text": { "maxCharacters": 8000 } }
```

Notes:
- `includeDomains` pins retrieval to the official docs, the single most effective anti-hallucination lever here.

## Response handling

1. **Select** the canonical docs URL (highest `score` on the official domain).
2. **Fetch full `text`** via `contents`.
3. **Chunk** the `text` into ~500-800 token passages on natural boundaries (headings, code fences). Keep each chunk's source `url` + a chunk index.
4. **Select relevant chunks** for the question (e.g. by keyword/embedding match to "rate limiting", "config", "code example").
5. **Generate strictly from selected chunks.** The generation prompt must instruct: *"Answer only using the provided context. If the context does not contain the answer, say so. Quote code examples verbatim from the context."*
6. **Coverage check**: if no chunk covers a requested sub-part (e.g. "code examples"), report the gap instead of fabricating code.

## Citation behavior

- Each chunk carries `(url, chunk_index)`; cite the chunk(s) a statement is drawn from with `[n]`.
- Code blocks are copied verbatim from a chunk and cited to that chunk — never paraphrased or "improved".
- If two chunks from the same page support different parts, they can share one source entry `[1]` with distinct inline placement.

## Final answer pattern

```
Rate limiting in the Acme API gateway is configured in the `rateLimit` block of
your gateway config [1].

Configuration fields [1]:
- `requestsPerSecond` — sustained allowed rate
- `burst` — short-term burst allowance

Example (verbatim from the docs) [1]:

    rateLimit:
      requestsPerSecond: 100
      burst: 200

Note: the retrieved docs do not describe per-API-key limits, so I can't cover that
here.

Sources:
[1] Acme docs — Rate limiting — https://docs.acme.com/gateway/rate-limiting
```

## Common failure mode

- **Hallucinated config keys / code**: the model fills gaps from prior training (e.g. inventing a `perKey:` field that isn't in the retrieved text), defeating the entire point of RAG.
- **Over-retrieval into the prompt**: dumping the full 8,000-char `text` instead of selected chunks, drowning the relevant passage and inflating cost/latency.
- **Citing the page but not the chunk**, so claims can't be traced to the supporting passage.

## Improved version

- Hard rule in the generation prompt: *only* use provided chunks; explicitly emit "not in the docs" for uncovered parts.
- Pin retrieval with `includeDomains` to the official source; reject off-domain chunks.
- Select and pass only the relevant chunks, each tagged with `(url, chunk_index)`; quote code verbatim.
- Mark any inference beyond the text:

```
> Verification needed: per-key rate limits were not found in the retrieved docs.
> Confirm on docs.acme.com directly, or see https://docs.exa.ai for retrieval options.
```

### One-call alternative: `/answer`

When you don't need a custom chunking/LLM layer, replace the whole pipeline with:

```json
POST /answer
{ "query": "How do I configure rate limiting in the Acme API gateway? Include code examples.",
  "text": true }
```

Returns `{ "answer": "...", "citations": [{ "id", "title", "url", "text" }], "costDollars": {...} }`.
It is cheaper and simpler, but you give up control over chunk selection and prompt design. Still pair it with `includeDomains`-scoped retrieval semantics by phrasing the query toward the official docs, and surface its `citations` to the user.
