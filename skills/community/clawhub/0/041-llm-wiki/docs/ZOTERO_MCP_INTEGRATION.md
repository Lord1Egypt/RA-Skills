# Zotero Literature Workflow Notes

> Status: historical analysis and workflow notes. llm-wiki no longer plans a native Zotero MCP/server wrapper; use an external Agent/Zotero skill as the literature layer instead.

## Goal

Use Zotero as the mature literature and attachment manager, and use llm-wiki as the distilled Markdown knowledge layer. Zotero should own bibliographic metadata, PDFs, annotations, collections, tags, citation keys, and related-item links. llm-wiki should own reusable concepts, cross-source synthesis, wiki links, temporal interpretation, and agent-maintained indexes.

## Available Zotero Skill

A recommended public source is the OpenAI Plugins Zotero skill:

- <https://github.com/openai/plugins/tree/main/plugins/zotero/skills/zotero>

Agents can use that skill, or an equivalent Zotero-capable skill, to operate Zotero Desktop. This avoids adding a Zotero client or MCP wrapper inside llm-wiki.

## Current Project Fit

llm-wiki already has the pieces needed for a conservative Zotero workflow:

- `sources/` is reserved for real original material and must not receive Agent-generated summaries.
- `wiki/*.md` pages already support YAML frontmatter and source lists.
- `agent-bridge.py` provides a single Agent entry point for status, lint, link, relink, query, merge, and index.
- Embedding and linking are already optional, so Zotero search can be used as a source-discovery layer without replacing the existing wiki retrieval path.

The main llm-wiki responsibilities are stable source metadata fields, Zotero identifiers in wiki pages, and a clear ingestion workflow for Zotero-sourced material.

## Historical Zotero MCP Capabilities Observed

Earlier analysis of a local `zotero-mcp` project found both MCP tools and a standalone CLI. Relevant capabilities included:

- Search: `zotero_search_items`, `zotero_advanced_search`, `zotero_search_by_tag`, `zotero_semantic_search`, `zotero_get_recent`.
- Library navigation: `zotero_get_collections`, `zotero_get_collection_items`, `zotero_get_tags`, `zotero_list_libraries`, `zotero_switch_library`.
- Content retrieval: `zotero_get_item_metadata`, `zotero_get_item_fulltext`, `zotero_get_item_children`, `zotero_get_attachment_path`.
- Notes and annotations: `zotero_get_annotations`, `zotero_get_notes`, `zotero_search_notes`, `zotero_create_note`.
- Import and management: `zotero_add_by_doi`, `zotero_add_by_url`, `zotero_add_from_file`, `zotero_update_item`, `zotero_manage_collections`, duplicate tools.
- Related items: `zotero_get_item_related`, `zotero_add_item_relation`, `zotero_remove_item_relation`.

The current preferred path is to use an external Zotero skill directly. A standalone `zotero-cli` or MCP server can still be useful in an environment that already has one, but llm-wiki should not depend on it.

## Recommended Architecture

### Phase 1: Read-Only Source Discovery

Add a protocol workflow, not a new runtime dependency:

1. User asks to ingest a Zotero collection, tag, item key, citation key, DOI, or topic.
2. Agent uses the Zotero skill, or an equivalent Zotero-capable tool, to find candidate items.
3. Agent reads metadata first, then full text or annotations only for selected items.
4. Agent creates or updates wiki pages through the existing protocol mode.
5. Agent runs `agent-bridge.py link` / `relink` to connect new pages.

This phase keeps llm-wiki lightweight and avoids building a second Zotero client inside `src/llm_wiki`.

### Phase 2: Stable Metadata Mapping

Extend page frontmatter with optional Zotero and temporal fields:

```yaml
sources_meta:
  - title: "Paper or Article Title"
    type: "academic_paper"
    published: "2025-02"
    collected: "2026-05-20"
    ingested: "2026-05-24"
    date_precision: "month"
    zotero_item_key: "ABCD1234"
    citation_key: "author2025title"
    library_id: "0"
    zotero_uri: "zotero://select/items/ABCD1234"
    doi: "10.xxxx/example"
    arxiv: "2502.00000"
```

Rules:

- `created` and `updated` remain wiki maintenance dates.
- `published` / `released` / `posted` describe the work itself.
- `collected` describes user/Zotero collection time.
- `ingested` describes llm-wiki processing time.
- `date_precision` prevents fabricated month/day values.

### Phase 3: Optional Backlink Sync

After wiki pages are stable, support controlled Zotero write-back:

- Add a Zotero tag such as `llm-wiki`.
- Add a page tag such as `wiki:Recommender-Systems`.
- Optionally create a Zotero note containing the wiki page title, slug, and local path.
- Optionally use Zotero related-item links when llm-wiki relation discovery finds strong relationships between two Zotero-backed items.

All write-back operations should be opt-in and should show a dry-run summary first.

## Ingest Workflows

### Ingest One Zotero Item

1. Locate item by key, citation key, DOI, URL, or title.
2. Read `zotero_get_item_metadata`.
3. Extract title, creators, date, DOI/arXiv, URL, abstract, tags, collection membership, and citation key.
4. Read annotations before full text when available; annotations are usually higher-signal.
5. Read full text only when the user requests detailed ingest or metadata/annotations are insufficient.
6. Create/update wiki page with `sources_meta`.
7. Run link discovery and review backward updates.
8. Append `log.md` with Zotero key and source time.

### Ingest a Zotero Collection or Tag

1. Resolve the collection/tag to item keys.
2. Produce a candidate list with title, author, date, item type, and Zotero key.
3. Batch by topic or time period rather than one page per item.
4. For each selected batch, process metadata first and read full text only for key works.
5. Add `## 时间线` to overview pages when multiple works form an evolution.

### Query Across Zotero and Wiki

1. Search wiki first when the question is about already distilled knowledge.
2. Search Zotero when the question asks for source coverage, recent additions, specific papers, annotations, or missing literature.
3. Synthesize with citations to wiki pages and Zotero identifiers.
4. Offer to archive new synthesis into wiki when it adds lasting value.

## Temporal Knowledge Design

The recent Zhihu collection ingest exposed a gap: pages captured semantic themes but not the historical order of works, posts, or methods. The integration should make time visible:

- Overview pages should include a `## 时间线` when they collect multiple works.
- Relation descriptions should say whether a source is an early work, follow-up, contemporary route, survey, replication, or retrospective.
- `agent-bridge.py link` can later use source dates as a tie-breaker for relation labels.
- Lint can later report pages with sources but no source-level date metadata.

## Safety Constraints

- Do not write Agent-generated summaries into `sources/`.
- Do not treat Zotero tool output as a verified original file unless it came from Zotero metadata, attachment text, annotation text, or a real fetched file.
- Do not overwrite Zotero metadata automatically.
- Do not import large full-text batches without user confirmation.
- Do not invent missing publication months or days.

## Implementation Options

### Option A: Protocol-Only Integration

Document Zotero skill workflows and let Agents call their installed Zotero-capable skill directly.

Pros: lowest complexity, no new llm-wiki dependency, works with current Agent skill systems.

Cons: less automation, harder to lint or batch.

Recommendation: start here.

### Option B: Agent Bridge Wrapper

Add `agent-bridge.py zotero-search`, `zotero-ingest-plan`, and `zotero-sync` commands that call an installed Zotero skill, shell out to `zotero-cli`, or use a small adapter.

Pros: consistent Agent UX and structured Markdown output.

Cons: adds dependency on Zotero tooling installation/config and requires more tests.

Recommendation: phase 2, after protocol-only usage stabilizes.

### Option C: Native MCP Client in llm-wiki

Use the MCP SDK inside llm-wiki to call Zotero MCP server directly.

Pros: clean integration for MCP-native hosts.

Cons: more moving parts, harder local setup, less aligned with this repo's lightweight design.

Recommendation: defer until there is repeated demand.

## Proposed Roadmap

1. Document the workflow and metadata schema.
2. Update templates and ingest rules to require source time metadata.
3. Trial manual Zotero skill ingest on a small collection.
4. Add lint checks for missing `sources_meta` dates.
5. Add optional `agent-bridge.py` helpers if the manual workflow repeats often.
6. Add opt-in Zotero tag/note backlink sync with dry-run output.
