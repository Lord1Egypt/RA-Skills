# 引文输入（中文说明）

宿主仍负责语义抽取。`prepare` 只把 quote 绑到证据字节范围，不解析 URL、不调用模型、不证明语义支持。

匹配顺序：1）原文精确字节；2）若失败，忽略表格 `|`、空白（含全角空格）、Markdown `#`/`*` 后再定位，并把命中映射回**原文**起止字节。EvidenceSpan / `span_sha256` 始终对应原文片段。歧义时仍须加长 quote 或给 `occurrence`。

宿主侧加长做法（回测 v2 实测）：若 quote 多处命中，先用宿主记录的页码筛出**引用页内唯一**的那一处（页内没有则看相邻页），再在正规化文本里向两侧逐步扩展该页的真实上下文，直到全文唯一，最后把对应的**原文逐字片段**作为 quote 交给 `prepare`。页内仍有多处或扩展到整页仍不唯一时丢弃，不得任选一处。

---

# Quote input: lower the extraction burden

The host still extracts semantics. `prepare` only binds exact quotes to evidence and copies supplied text; it never parses a URL, calls a model or proves support.

Start with [quote-draft.json](../assets/demo/quote-draft.json). All entities, definitions, scopes and assertion fields follow [knowledge-contract.md](knowledge-contract.md). Assertion `claim_kind` defaults to `reported` during `prepare`; any explicit other value is rejected. Source `sha256` may be omitted; the tool calculates it. Supplied hashes must match. Replace each evidence locator with:

```json
{"source_id":"source:r1","quote":"Exact parsed text, including whitespace.","role":"value_and_scope"}
```

The quote must occur exactly once. If repeated, include more context or add `"occurrence": 2` (1-based). Do not select an arbitrary occurrence merely to make validation pass. Unicode offsets are computed in UTF-8 bytes. Actual source page spans are reused only when they contain the entire quote; otherwise a text-range locator is emitted. Declared page/range overrides cannot disagree with the match.

```sh
python3 scripts/ontology.py prepare assets/demo/quote-draft.json --out /path/to/work/prepared
python3 scripts/ontology.py build /path/to/work/prepared/input.json --out /path/to/work/v1
```

`prepare` creates a new directory with `input.json` and immutable text copies. It preserves source metadata, validates the full schema and rejects traversal, changed hashes, missing/ambiguous quotes and injected review acceptance. It never overwrites an output directory.

For a financial table include separate evidence for row, unit/period headers and relevant footnotes. The shortest unique string is not always enough semantic evidence. Prefer precise rows plus headers over quoting a whole report. `query --with-evidence` and briefs return up to 400 characters per evidence range; `truncated: true` means consult the complete snapshot before relying on omitted qualifiers.
