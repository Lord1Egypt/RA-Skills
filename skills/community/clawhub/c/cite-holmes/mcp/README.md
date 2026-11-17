# cite-holmes-mcp

**Mechanical citation verification as an MCP server** — feed it the references an
agent is about to cite, get back per-reference verdicts (`verified / partial /
unreachable / invalid`) against official registries (DOI.org, PubMed
E-utilities, arXiv API, Crossref/Retraction Watch, Wayback). Zero API keys
required, zero telemetry, local-first.

Three MCP primitives:

| Primitive | Name | What it does |
|---|---|---|
| tool | `verify_references` | Verify a batch of references (≤50); returns CiteScore 0–100 + per-item verdicts with evidence chain |
| tool | `check_document` | Context-level check: parse in-text markers ([12]/[1-4]/(Author, Year)/doi.org links), bind to the reference list, flag low anchor-word overlap as possible mis-citations |
| tool | `explain_verdict` | Plain-language explanation of one verdict (evidence steps + suggested action); zero network |
| resource | `cite-holmes://capability-matrix` | What the mechanical layer catches vs. what stays with the semantic layer |
| resource | `cite-holmes://changelog` | Version history |
| prompt | `fact_check_workflow` | Three-step research-then-verify workflow for agents |

## Install (three channels)

```bash
# 1) uvx from GitHub (recommended — always current)
uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp

# 2) uvx from a local checkout
git clone https://github.com/docsor1212/cite-holmes
uvx --from ./cite-holmes/mcp cite-holmes-mcp --help

# 3) pip install (module + console script)
pip install "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp"
cite-holmes-mcp --help
```

> This is a Python package (uv/pip ecosystem). There is no npm package — the
> uvx/git channel above is the canonical install for all MCP clients.

## Client configuration

**Claude Code**

```json
{
  "mcpServers": {
    "cite-holmes": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp",
               "cite-holmes-mcp"]
    }
  }
}
```

**Codex / any stdio MCP client**

```json
{
  "mcpServers": {
    "cite-holmes": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp",
               "cite-holmes-mcp", "--transport", "stdio"]
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`, same shape)

```json
{
  "mcpServers": {
    "cite-holmes": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp",
               "cite-holmes-mcp"]
    }
  }
}
```

HTTP mode (local): `cite-holmes-mcp --transport http --port 8760`.

## Bounds & behavior

- Batch ≤ 50 references per `verify_references` call (larger batches get a
  clear error — split them).
- Long output fields are clipped (800 chars + truncation marker) so MCP
  messages stay bounded; structure is preserved.
- Per-reference network timeout defaults to 15 s (configurable per call).
- Optional API keys via env: `OPENALEX_API_KEY` / `S2_API_KEY` /
  `NCBI_API_KEY` (only attach to the caller's own requests).

## Layout

```
mcp/
├── server.py          # FastMCP three-primitive server (engine-agnostic impl)
├── verify_refs.py     # embedded engine copy — synced from ../scripts/ by
│                      #   sync_engine.sh (sha-gated; never hand-edit here)
├── sync_engine.sh     # trunk↔mcp engine consistency gate (run before publish)
├── pyproject.toml
├── README.md
└── tests/
    ├── test_bounds.py        # batch/clip/bad-input unit tests
    └── e2e_transcript.md     # full MCP client session evidence
```

License: MIT. Author: SorSor. Repo: https://github.com/docsor1212/cite-holmes


## 作为任何 Deep Research agent 的核验后端（v5.4.0）

AI 研究工具生成的引用普遍不经注册库核验（业界实测错引率高企，核查责任
目前落在使用者身上）。本 MCP 让任何会调工具的深度研究 agent——Claude Code、
Codex、Cursor、自研 LangGraph/OpenClaw agent——零成本获得注册库级核验：

- `verify_references`：研究循环每收集一批引用就过一次五态判定（verified /
  partial / unreachable / invalid / unverified），invalid 立即触发重搜；
- `explain_verdict`：agent 对判定拿不准时取判定链人话解释；
- `check_document`：报告成稿后做全文上下文核验（in-text 绑定+锚词率）；
- `discover_references`（v5.6.0）：主题检索 PubMed+OpenAlex 并出生即核验——
  深度研究循环的检索步直接获得带五态判定的候选文献，invalid 立即重搜；
- `build_review_kit`（v5.6.0）：把核验结果转成综述就绪三件套（对比表/标注
  书目/即贴 GB/T），零网络。

推荐接线：在研究 agent 的 VERIFY 步骤后追加一次 `verify_references` 调用，
把 unverified/partial 条目排除出结论区（「未验证引用绝不进结论」自此有
机械兜底）。批量上限 50 条/次，超出请分批。
