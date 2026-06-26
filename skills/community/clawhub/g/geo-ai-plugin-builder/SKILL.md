---
name: geo-ai-plugin-builder
description: >
  Master orchestrator for turning high-value GEO content and capabilities
  into AI plugins/tools across ChatGPT, Claude, Perplexity, Gemini and other
  ecosystems. Use this skill whenever the user mentions building, designing,
  packaging, or standardizing AI plugins/tools around their content, APIs,
  or GEO assets, or wants to move from being passively cited to actively
  embedded inside AI workflows.
---

# GEO AI Plugin Builder

This skill helps you design and standardize AI plugins/tools that wrap
your highest-value GEO content and capabilities, so they can be embedded
directly into AI ecosystems (ChatGPT, Claude, Perplexity, Gemini, etc.).

The core goal is to shift from **"waiting to be cited"** to
**"being a first-class tool inside AI workflows"**, while staying aligned
with GEO (Generative Engine Optimization) strategy.

---

## When to use this skill

Use this skill whenever:

- You want to **turn content, data, or services into AI plugins/tools**.
- You want to **increase brand exposure inside AI tool flows**, not just in
  plain-text answers.
- You are **mapping website/GEO assets to structured tool endpoints**.
- You are **designing or refactoring an AI plugin catalog** for your brand.
- You need **standard templates** for OpenAI-style tools, Claude Tools,
  function calling, or custom internal agents.
- You want to **prioritize which content should become a plugin first**.

Do **not** use this skill when the user only wants:

- Simple content rewrites for GEO (use their GEO content skills instead).
- Pure analytics/reporting about GEO performance (metrics-only work).
- Low-level SDK usage without any GEO or plugin strategy involved.

---

## Mindset and principles

- **Tool-first GEO**: Treat your top content and capabilities as *services*
  that can be invoked as tools, not just pages to be cited.
- **User journey > endpoints**: Begin from real end-to-end tasks users want
  to完成 with AI, then design tools that make those workflows smooth.
- **Cross-ecosystem thinking**: Design schemas and naming so your plugin
  concepts map cleanly across multiple AI platforms.
- **Small, composable tools**: Prefer a set of focused tools that can be
  combined, rather than one mega-tool that does everything.
- **Explainability for AIs**: Include clear descriptions, examples, and
  constraints so AI models can reliably choose and call tools.

---

## High-level workflow

When the user asks for help, follow this 5-step workflow unless they
explicitly request a narrower slice:

1. **Clarify goals and context**
   - Understand the brand, target users, and GEO priorities.
   - Identify which AI ecosystems matter most (e.g., ChatGPT plugins,
     Claude Tools, Perplexity collections, internal agents).
   - Clarify what "success" looks like: visibility, conversions, leads,
     authority, usage of specific tools, etc.

2. **Inventory candidate assets**
   - Ask for or infer a list of high-value assets:
     - Evergreen content, calculators, wizards, internal tools.
     - Datasets, pricing engines, recommendation logic.
     - Workflows sales or support teams execute repeatedly.
   - Group assets by use case and by stage in the customer journey
     (discovery, evaluation, decision, post-purchase, retention).

3. **Design plugin concepts and tool set**
   - Propose a **plugin catalog**: 3–10 core plugin ideas or tool groups.
   - For each plugin/tool, define:
     - Primary user jobs-to-be-done.
     - Input parameters and output structure.
     - GEO role (discovery, trust building, conversion, retention).
   - Prioritize plugins by potential impact and implementation effort.

4. **Generate detailed tool specifications**
   - For the **highest-priority plugin(s)**, generate detailed specs:
     - Tool name, description, and rationale.
     - JSON schema for inputs and outputs.
     - Example calls and example responses.
     - Mapping to backend endpoints or content sources.
     - GEO hooks (links, snippets, brand voice guidance).

5. **Produce implementation-ready artifacts**
   - Output one or more of:
     - **Technical blueprints** (OpenAI tools, Claude Tools, HTTP
       endpoints, or internal APIs).
     - **Developer handoff docs** with clear TODOs and edge cases.
     - **Backlog / roadmap** outlining order of implementation.

Whenever possible, structure outputs so the user can copy-paste directly
into their codebase or internal specs.

---

## Information to ask from the user

When the initial information is incomplete, explicitly ask the user for:

- **Business and brand**
  - Industry, main products or services.
  - Primary GEO/AI goals (visibility, conversions, retention, authority).
- **Target AI ecosystems**
  - Which AI platforms and tool surfaces matter most.
  - Internal vs public tools (e.g., sales-assist, support-assist).
- **Existing assets**
  - URLs for core content, tools, or APIs.
  - Any existing plugins, agents, or integrations.
- **Constraints**
  - Technical stack and data sources.
  - Compliance/privacy constraints (PII, regulated data, etc.).
  - Resource constraints (team size, timelines).

If the user cannot provide all details, make **reasonable assumptions**,
but document them clearly in the output.

---

## Output formats

Adapt to the user's request, but default to these structured formats:

- **Plugin catalog overview**
  - A table or bullet list summarizing each proposed plugin/tool with:
    - Name
    - Primary user job
    - Main AI surfaces/platforms
    - GEO role
    - Implementation difficulty (rough)
    - Priority (high/medium/low)

- **Detailed plugin specification**
  - For each selected plugin, provide:
    - High-level description and purpose.
    - User stories / example prompts that should call this tool.
    - Tool schema:
      - `name`
      - `description`
      - `parameters` JSON schema
      - `response` JSON schema
    - 2–4 **example calls and responses**.
    - GEO notes:
      - Key URLs/content to surface.
      - Brand and messaging constraints.
      - Tracking/telemetry suggestions.

- **Implementation checklist / roadmap**
  - Ordered list of steps for developers:
    - API design / implementation.
    - Authentication / permissions.
    - Logging, analytics, and monitoring.
    - Security and compliance checks.
  - Include clear "Done when…" criteria.

When the user wants code snippets (e.g., OpenAI, Node, Python), generate
idiomatic examples but keep them as **implementation guidance**, not as
the primary output of the skill.

---

## GEO-specific guidance

When designing plugins and tools, always connect back to GEO strategy:

- **Exposure inside AI tools**
  - Prefer tools that solve high-frequency, high-intent problems.
  - Make descriptions explicit about when they should be chosen by
    the model (e.g., "Use this tool whenever the user asks for…").

- **Authority and trust**
  - Tie outputs back to authoritative sources:
    - Official docs, research, internal datasets, or calculators.
  - Suggest how to surface citations or reference links when allowed.

- **Conversion paths**
  - For tools near purchase or signup decisions, include:
    - Next-step suggestions ("book a demo", "see pricing").
    - Structured fields that map to CRM or analytics events.

- **Lifecycle coverage**
  - Encourage a mix of plugins across the customer lifecycle:
    - Discovery (educational, comparison, diagnostics).
    - Evaluation (calculators, configurators, ROI models).
    - Decision (quote builders, plan selectors).
    - Post-purchase (onboarding, troubleshooting, optimization).

---

## Using bundled scripts and references

This skill may ship with helper scripts and reference guides under:

- `scripts/` — reusable helpers to generate JSON schemas, boilerplate
  plugin specs, or check consistency across a plugin catalog.
- `references/` — conceptual guides and best practices for GEO-aware
  plugin and tool design.

When you need more detailed patterns or want to generate many similar
tools at once, first:

1. Check `references/geo-ai-plugin-patterns.md` for archetypes and
   naming conventions.
2. Use `scripts/plugin_blueprint_generator.py` as a mental model for
   how to turn an abstract "job" into one or more tool specs.

You do **not** need to literally run these scripts inside the model,
but you should imitate their behavior and structures when helpful.

---

## Example use cases

Here are a few example tasks where this skill should be used end-to-end:

- "We run a B2B SaaS for marketing analytics. Help us design a set of
  AI tools so that ChatGPT or Claude can analyze a client's data and
  recommend campaigns using our platform."

- "We have a library of in-depth medical articles and calculators. Turn
  them into a plugin catalog for AI assistants that doctors or patients
  might use, with clear safety and disclaimers."

- "Our ecommerce brand has rich buying guides and fit finders. Design
  AI tools that help shoppers choose products and that we can expose as
  plugins in multiple AI platforms."

---

## Working style

When using this skill:

- Stay **strategic first, then technical**:
  - Clarify positioning, value, and GEO role before writing schemas.
- Be **explicit about assumptions** and clearly flag trade-offs.
- Optimize for **reuse and extendability**:
  - Make it easy to add more tools or platforms later.
- Keep outputs **copy-paste friendly**:
  - Use consistent headings, JSON blocks, and formatting.

If the user asks to iterate on a previous catalog or spec, treat the old
version as a baseline, highlight key changes, and explain why the new
design is stronger for GEO + AI plugin exposure.

