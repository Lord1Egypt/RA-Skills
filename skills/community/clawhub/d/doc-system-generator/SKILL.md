---
name: doc-system-generator
description: >
  Analyze any software project and generate a complete, well-structured documentation system
  with three-track philosophy (Intent/Contract/Constraint), intelligent grouping, template derivation,
  and 18-dimension completeness self-check. Use when: (1) Creating documentation system for a new project,
  (2) Redesigning existing documentation, (3) User says "generate docs", "文档系统", "document system",
  "setup docs", "文档生成", "创建文档体系". Trigger: "doc system", "document system", "generate docs",
  "文档系统", "文档生成", "setup documentation", "doc structure"
---

# Doc System Generator

Analyze any project → derive optimal grouping → generate complete Markdown documentation system → self-check completeness.

## Workflow

### Phase 0: Environment Probe

1. **Detect existing docs**: Check for `docs/`, `doc/`, `documentation/`, or any `.md` files at project root
2. **Detect entry file**: Check for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`
3. **Decision point**:
   - Existing docs found → present two **equal** options to user (no default):
     - **Option A**: Respect existing structure + suggest improvements
     - **Option B**: Full redesign from scratch
   - No existing docs → proceed directly to Phase 1
4. **Deploy tool**: Copy `scripts/md-sections.sh` to project's `scripts/` directory (create if needed)
   - **Fallback**: If md-sections.sh fails (corrupted Markdown, exotic separators), use AI Agent's native Read/Grep tools directly. No additional parser needed.
   - **Scope boundary**: Online documentation platforms (Notion, Confluence, GitBook) are out of scope — they require API tokens and have their own navigation

### Phase 1: Project Analysis

5. **Detect explicit boundaries** (🤖 automatic):
   - Scan build files → extract modules/packages/subprojects list
   - Scan directory structure → identify hierarchy pattern
   - Detect entry files → determine application boundaries
6. **Identify architecture pattern** (🤖👤 semi-automatic):
   - Analyze code organization → match pattern (layered/ECS/microservice/pipeline/plugin/SPA/embedded)
   - Analyze dependency direction → determine coupling style
   - Analyze test structure → identify concern separation
7. **Identify cross-cutting concerns** (🤖👤 semi-automatic):
   - Scan config files → extract concerns (CI, security, i18n, testing, deployment)
   - Analyze code patterns → identify concerns (error handling, logging, caching)
   - Analyze dependencies → list framework capabilities
8. **Optional field research**: If unfamiliar project type or user requests, search for industry documentation practices for this tech stack/domain. Use results as **hints only**, not mandates.

→ **Output**: Project Profile (JSON) containing: techStack, modules, architecture, concerns. Show Phase 1 reasoning to user before proceeding.

For detailed signal tables and detection methods, see [grouping-detection.md](references/grouping-detection.md).

### Phase 2: Grouping Derivation

9. **Derive grouping dimensions** from Phase 1 results:
   - Module boundaries → basis for "module" document grouping
   - Architecture pattern → basis for "architecture" document grouping
   - Cross-cutting concerns → basis for "standards/conventions" document grouping
10. **Quality check** (以职责为核心):
    - Cohesion: Do documents in each group answer the same class of questions?
    - Independence: Does each group carry a distinct documentation responsibility?
    - Discoverability: Can readers locate documents by intent?
11. **Present derivation** to user: Show reasoning process + result. User confirms or adjusts.

### Phase 3: Template Derivation

**Key principle: Three-track system is the foundation.** Read [three-track-philosophy.md](references/three-track-philosophy.md) for full philosophy.

12. **Classify each document group into tracks**:
    - 🔴 Intent: Records design intent (frozen after creation)
    - 🟢 Contract: Follows code (code → doc alignment)
    - 🔵 Constraint: Drives code (doc → code alignment)
13. **Determine template flexibility** for each group:

    ```
    Documents answer same class of questions?
    ├── No  → Flexibility 1: Fully Independent
    └── Yes → Reader expectations identical?
             ├── Yes → Flexibility 3: Fully Unified
             └── No  → Shared core but unique needs?
                      ├── Yes → Flexibility 4: Mixed (unified shell + free core)
                      └── No  → Flexibility 2: Shell Unified
    ```

14. **Generate fixed shell** (three tiers):
    - **Required**: Title + one-sentence purpose + 📋 TOC + track label (🔴/🟢/🔵)
    - **Recommended**: Overview/background + related docs
    - **Optional**: Change history (Contract track) / Checklist (Constraint track) / Mermaid diagram
15. **Derive core chapters**:
    - Primary path: Reader questions → chapter names (per track's typical reader questions)
    - Secondary path: Code patterns → supplementary technical chapters
    - Optional: Field research for domain-specific chapter conventions
16. **Present templates** to user: Show derived templates per group. User confirms or adjusts.

For detailed template derivation methods, see [template-derivation.md](references/template-derivation.md).

### Phase 4: Document Generation

17. **Generate entry file** (AGENTS.md or equivalent):
    - Documentation system overview (tech stack summary, module structure)
    - Core coding rules extracted from Constraint track
    - Document index with reference strength (⛔ MUST / ⚠️ SHOULD / 💡 MAY)
    - Layered disclosure rule as **highest priority constraint**
18. **Generate meta-system doc** (docs/README.md):
    - Three-track system definition
    - Seven writing principles (see Constraints below)
    - Template descriptions
    - Navigation index
    - Maintenance governance (🤖/🤖👤/👤 classification)
    - Anti-pattern warnings
19. **Generate group README** for each group directory:
    - Template description + writing guide
    - Document list with one-sentence purpose each
20. **Generate all documents** per derived templates:
    - Apply fixed shell + core chapters
    - Fill with analyzed project content
    - Add cross-references between related documents
    - Add track labels and reference strength annotations
21. **Write layered disclosure rule** into entry file:

    ```markdown
    ## ⛔ Documentation Loading Rules (Highest Priority)
    For documents exceeding 200 lines:
    Step 1: Run `scripts/md-sections.sh <file>` for JSON structure
    Step 2: Run `scripts/md-sections.sh <file> "Section Name"` to extract specific content
    PROHIBITED: Reading full document content in one operation
    ```

### Phase 5: Completeness Self-Check

22. **Run structural checks** (S1-S7, 🤖 automatic):
    - S1: Template compliance — all fixed sections present
    - S2: TOC accuracy — 📋 matches actual sections
    - S3: Cross-references — all links point to existing targets
    - S4: Entry index coverage — entry file references all documents
    - S5: Track labels — all documents labeled
    - S6: Reference strength — all index entries annotated
    - S7: Change history — all Contract-track docs have it
23. **Run content checks** (C1-C6, 🤖👤 semi-automatic):
    - C1: Code references exist — mentioned entities found in codebase
    - C2: API signatures match — documented APIs match code
    - C3: Data models match — documented models match code
    - C4: Config items match — documented configs match code
    - C5: Version numbers match — documented versions match build files
    - C6: Semantic consistency — documented behavior matches code (deep mode only)
    - Record detection methods derived for C2-C5 in project metadata (for contract-doc-sync reuse)
24. **Run system health checks** (H1-H5, 👤 human judgment):
    - H1: Module coverage — every code module has a document
    - H2: Concern coverage — every concern has a standards document
    - H3: Responsibility uniqueness — no two documents answer the same question
    - H4: No information islands — every document is referenced by at least one other
    - H5: Industry benchmark — field research coverage comparison
25. **Output self-check report** using fixed template (see [completeness-checklist.md](references/completeness-checklist.md) for full template).

### Phase 6: User Confirmation

26. **Present full results**: generated file list + self-check report
27. **Iterate on user feedback**: adjust grouping, templates, or content as needed

---

## Constraints

### Writing Principles (for all generated documents)

1. **Single Responsibility**: Every document has exactly one purpose, expressible in one sentence. If two documents answer the same question → merge or re-split.
2. **Layered Disclosure**: Documents exceeding 200 lines require structure-first access. Always include 📋 TOC section. Within a single session, parse the same file's structure only once — reuse the parsed tree for subsequent extractions.
3. **Hierarchy Limit**: Section depth must not exceed L3 (###). L3 for fine-grained subdivisions only.
4. **Link Over Copy**: When content from another document is needed, use Markdown links — never copy content.
5. **Positive Constraints**: Write rules as "do X" with specifics, not "don't do Y". Pair safety-critical negatives with positive alternatives.
6. **Track Labeling**: Every document carries a track label (🔴/🟢/🔵) in its header.
7. **Reference Strength**: Every document entry in index files carries a strength annotation (⛔/⚠️/💡).

### Maintenance Classification (for generated governance sections)

| Level | Marker | Trigger | Example |
|-------|--------|---------|---------|
| 🤖 Deterministic | Direct fix | 1:1 mappable from code | API signature change → update API reference |
| 🤖👤 Semi-deterministic | `[pending confirmation]` | Requires intent understanding | Business logic change → update description |
| 👤 Creative | Skip, report | Requires original thinking | New module → create new document |

### Format Rules

- All generated documents use Markdown format exclusively
- Use Mermaid diagrams for architecture and flow documentation
- Use numbered tables for API/configuration references
- Entry file (AGENTS.md): concise, constraint summary + document index only
- Meta-system doc (docs/README.md): self-describing, includes all governance rules

---

## Examples

### Example 1: Java Spring Boot multi-module project

→ 1. Phase 0: No existing docs → proceed directly
→ 2. Phase 1: Detect Maven modules (common, client-cache, client-oss, app), identify layered architecture, find concerns (auth, caching, storage, testing)
→ 3. Phase 2: Derive 3 groups: `architecture/` (by question), `conventions/` (by concern), `modules/` (by module)
→ 4. Phase 3: architecture=Flexibility 1, conventions=Flexibility 2, modules=Flexibility 3. Intent track in `openspec/specs/`, Contract in `docs/modules/`+`docs/architecture/`, Constraint in `docs/conventions/`+`AGENTS.md`
→ 5. Phase 4: Generate 22 documents + AGENTS.md + docs/README.md + group READMEs
→ 6. Phase 5: S1-S7 all pass. C2-C5 use Java-specific detection (annotations, pom.xml). H5: compare against Spring Boot doc conventions
→ 7. Phase 6: User confirms

### Example 2: React component library, existing messy docs/

→ 1. Phase 0: Existing `docs/` with disorganized files → present two options → user chooses "Full redesign"
→ 2. Phase 1: Detect npm workspaces, identify component structure, find concerns (styling, accessibility, testing, i18n)
→ 3. Phase 2: Derive groups: `components/` (by component), `guides/` (by concern), `architecture/` (by question)
→ 4. Phase 3: components=Flexibility 3 (all need Overview/Props/Events/Examples), guides=Flexibility 2, architecture=Flexibility 4
→ 5. Phase 4: Generate documents. Field research reveals Storybook conventions → incorporate Props/Events/Accessibility chapters
→ 6. Phase 5: S4 finds entry file missing 3 new docs → fix. H5: accessibility docs missing → flag
→ 7. Phase 6: User adds accessibility concern → regenerate

### Example 3: Game engine (Unreal)

→ 1. Phase 0: No existing docs
→ 2. Phase 1: Detect CMake/workspace modules, identify ECS + Game Loop pattern, find concerns (performance, memory, scripting, asset pipeline)
→ 3. Phase 2: Derive 4 groups: `systems/` (AI, rendering, physics, audio), `pipelines/` (asset, build, CI), `guides/` (scripting, performance, debugging), `architecture/` (overview, patterns, memory model)
→ 4. Phase 3: systems=Flexibility 4 (unified shell: Overview/Integration/Performance, but unique chapters: AI has Behavior Tree, Rendering has Shader Pipeline)
→ 5. Phase 4: Generate. Field research: Unreal docs commonly cover Blueprints, C++ API, Performance budgets → incorporate
→ 6. Phase 5: H1 finds 2 subsystems without docs → flag for user
→ 7. Phase 6: User confirms

---

## Verification

After completing the workflow:

1. **File existence**: All planned documents were created (check with `ls -la docs/` recursively)
2. **Structure valid**: Run `scripts/md-sections.sh <each-file>` → verify TOC sections exist
3. **Entry index complete**: Entry file references all generated documents
4. **Cross-references valid**: No broken Markdown links between documents
5. **Self-check report clean**: S1-S7 all pass; C1-C6 reviewed; H1-H5 acknowledged by user
6. **Track consistency**: Each document's track label matches its actual time/direction behavior

If any check fails → diagnose, fix, re-verify. If user disagrees with grouping/templates → iterate from corresponding Phase.

---

## Resources

| File | When to Read |
|------|-------------|
| [three-track-philosophy.md](references/three-track-philosophy.md) | Phase 3 — Need to explain track classification or writing philosophy to user |
| [grouping-detection.md](references/grouping-detection.md) | Phase 1-2 — Need detailed signal tables, architecture patterns, or quality criteria |
| [template-derivation.md](references/template-derivation.md) | Phase 3 — Need detailed flexibility judgment, fixed shell definition, or chapter derivation methods |
| [completeness-checklist.md](references/completeness-checklist.md) | Phase 5-6 — Need 18-dimension checklist details, dependency order, or report template |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/md-sections.sh` | Markdown chapter parser with three operations: (1) `md-sections.sh <file>` → JSON structure tree, (2) `md-sections.sh <file> "Section"` → extract section content, (3) `md-sections.sh <file> --line <N>` → locate section by line number. Deploy to project's `scripts/` in Phase 0 |

## Complementary Skills

| Skill | Relationship |
|-------|-------------|
| `contract-doc-sync` | **Maintenance partner**: This skill = architect (one-time generation), contract-doc-sync = property manager (ongoing drift detection + sync). This skill's generated detection configs can be reused by contract-doc-sync |
