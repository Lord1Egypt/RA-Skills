# business-planner

> Auto-generate business plans, infrastructure diagrams, pitch decks  
> v1~v12 iterative refinement experience internalized (Doyak Package journey)

---

## 📋 Metadata

```yaml
name: business-planner
description: "Auto-generate business plans, infrastructure diagrams, pitch decks. Includes government funding (Doyak Package/TIPS/Startup Academy), investor IR, tech infrastructure design. Internalized v1~v12 iteration experience."
author: 무펭이 🐧
version: 1.0.0
created: 2026-02-14
triggers:
  - "business plan"
  - "pitch deck"
  - "infrastructure diagram"
  - "Doyak Package"
  - "TIPS"
  - "IR materials"
  - "investor materials"
  - "Startup Academy"
```

---

## 🎯 Core Features

### 1. Business Plan Generation (Government Funding)

Auto-generate business plans for government startup programs (Doyak Package, TIPS, Early Startup Package, Startup Academy).

**Supported Formats:**
- ✅ Startup Doyak Package (General/Regional)
- ✅ TIPS (R&D-focused)
- ✅ Early Startup Package
- ✅ Startup Academy

**Output Structure:**
```
Cover
├─ Application & General Info
├─ Startup Item Overview & Commercialization Plan (Summary)
│   ├─ Problem Definition (Hook)
│   ├─ Solution (Product/Service)
│   ├─ Customer Cases (before/after numbers)
│   └─ Key Differentiators
├─ Market Analysis
│   ├─ TAM/SAM/SOM
│   ├─ Competitor Analysis
│   └─ Trends (McKinsey, Gartner citations)
├─ Business Model
│   ├─ Pricing Strategy
│   ├─ Unit Economics (CAC, LTV)
│   └─ Revenue Structure
├─ Tech Infrastructure (if applicable)
│   ├─ Architecture Diagram
│   ├─ Hardware Specs
│   └─ Cost Breakdown
├─ Team Composition
├─ Financial Plan (3 years)
│   ├─ Income Statement
│   ├─ Fund Execution Plan
│   └─ Break-Even Point (BEP)
└─ Roadmap (Phase 0~4)
```

**Output Format:**
- HTML (A4 print-optimized, includes `@media print` styles)
- Can be opened in browser and converted to PDF
- Includes image insertion guide (SVG, PNG, JPG)

---

### 2. Infrastructure Diagram Generation

Visualize infrastructure architecture for tech startups.

**Generated Items:**
- **Architecture Diagram** (text-based ASCII art, Mermaid)
- **Hardware Spec Comparison** (Mac Mini, Raspberry Pi, Linux server, Cloud)
- **Cost Breakdown** (COGS, overhead, BEP)
- **Network Topology** (VPN, firewall, port config)
- **Security Checklist** (FileVault, SSH, API key isolation)

**Example Cases:**
- Mupeng Box (Mac Mini M4 Pro-based AI agent hardware)
- On-premise vs Cloud vs Hybrid comparison
- Product Lineup (Lite/Pro/Enterprise)

**Output Format:**
- Markdown (GitHub/Notion compatible)
- Mermaid diagrams (graph, flowchart, sequence)
- ASCII tables

---

### 3. Pitch Deck Generation (Investor IR)

Generate pitch decks for investors/accelerators in 10-15 slide structure.

**Slide Structure:**
```
1. Cover (Company name, one-liner)
2. Problem (Hook + field voices)
3. Solution (Product/service core)
4. Market Size (TAM/SAM/SOM, CAGR)
5. Product (Screenshots/demo/diagrams)
6. Business Model (Pricing, unit economics)
7. Traction (PMF signals, revenue, users)
8. Competitive Advantage (Moat, differentiation)
9. Team (Founders, key personnel)
10. Financials (3-year projections, break-even)
11. Roadmap (Milestones)
12. Ask (Funding needed, use, equity)
```

**Storytelling Principles:**
- **Hook → Resolve doubt → Product/visuals → Market/numbers**
- Don't use same visual twice
- Emphasize "expansion" (network effects) — not just tech refinement
- Number-focused (before/after, %, revenue, users)

**Output Format:**
- Markdown (section-separated by slide)
- Includes Google Slides/PowerPoint conversion guide

---

### 4. Iterative Revision Support

Version control, feedback incorporation, diff comparison with previous versions.

**Version Control:**
- `projects/gov-support/doyak-v1.html` → `v2.html` → ... → `v12.html`
- `git diff`-style change tracking
- Major changes summary (`CHANGELOG.md`)

**Feedback Incorporation:**
- Reviewer comments → revision direction suggestions
- Investor questions → add supplementary sections
- A/B testing (compare two versions)

---

## 🧠 Learned Lessons (v1~v12 Experience)

Insights from iterating Doyak Package business plan from v1 to v12:

### Storytelling

1. **Follow Hook → Resolve doubt → Product/visuals → Market/numbers order**
   - ❌ Bad: "Our tech uses AI..." (tech first)
   - ✅ Good: "Why do 72% abandon AI within 3 months?" (hook) → Present 3 barriers → Our solution

2. **Never use same visual twice**
   - Reviewers penalize "already seen this visual"
   - Prepare new visuals for each section

3. **"Expansion" is key — don't just talk about tech refinement**
   - ❌ "We'll train AI models more accurately"
   - ✅ "Customer A's skills → Customer B purchases → Network effects increase value"

### Framework

4. **Mupengism = Apple Analogy**
   - OpenClaw = Internet (base infrastructure, open-source)
   - LLM (Claude/GPT) = Semiconductors (compute engine)
   - Mupengism = Apple (OS + App Store + proprietary ecosystem)
   - **Message**: Share the foundation, build proprietary ecosystem on top

5. **Hardware is our infrastructure, not for sale**
   - ❌ "Sell racks to customers"
   - ✅ "Our racks = Skill Store central server, secure margins with own infrastructure instead of AWS"

### Numbers

6. **Before/After numbers mandatory**
   - Quote writing: 2 hours → 15 minutes
   - VC cold emails to 300 places: 1 week → 2 hours
   - SNS management: 3 hours/day → fully automated
   - Context explanation time: 90% reduction after 3 months

7. **Cite authoritative sources**
   - McKinsey 2025 AI Survey: "72% enterprise AI adoption, 72% abandonment within 3 months"
   - Gartner: "By 2028, agentic AI will support 15% of decisions"
   - MarketsandMarkets: "AI agent market $7.84B in 2025 → $52.6B in 2030 (CAGR 46%)"

---

## 📚 Reference Files

Files automatically referenced by skill (workspace-relative):

```
$WORKSPACE/
├─ projects/gov-support/
│   ├─ doyak-v10-img.html (latest business plan HTML)
│   ├─ doyak-v10-img2.html
│   ├─ doyak-v10.html
│   └─ doyak-v11.pdf (final submission)
├─ memory/consolidated/
│   └─ doyak-business-plan.md (core memories)
├─ memory/
│   ├─ [DATE]-mupeng-box-infra.md (infrastructure design)
│   └─ [DATE]-assoai-pitchdeck.md (pitch deck example)
└─ memory/research/
    └─ [DATE]-ai-agent-market.md (market research)
```

---

## 🚀 Usage

### Trigger Keywords

Auto-triggers on requests containing:

- **business plan**, pitch deck
- **infrastructure diagram**
- **Doyak Package**, TIPS, Startup Academy
- **IR materials**, investor materials

### Command Examples

#### 1. Business Plan Generation

```
"Write Doyak Package business plan. Company name [name], item [one-liner]."
```

**Generation Process:**
1. Receive basic info (company name, CEO, business registration, item intro)
2. Read reference files (`doyak-business-plan.md`, market research)
3. Generate from HTML template (`doyak-v10-img.html` structure ref)
4. Include image insertion guide
5. Save to `projects/gov-support/[company]-v1.html`
6. Provide browser opening guide

#### 2. Infrastructure Diagram Generation

```
"Create Mac Mini-based AI agent infrastructure diagram. Product lineup: Lite/Pro/Enterprise."
```

**Generation Process:**
1. Reference `mupeng-box-infra.md`
2. Generate Mermaid diagrams (architecture, network topology)
3. Hardware spec comparison table (Markdown table)
4. Cost breakdown (COGS, overhead, BEP)
5. Save to `projects/infra/[project]-infra.md`

#### 3. Pitch Deck Generation

```
"Create investor pitch deck. TAM $2B, SAM $200M, SOM $2M. Current: 2 customers, ARR 16.8M KRW."
```

**Generation Process:**
1. Reference `assoai-pitchdeck.md` structure
2. Generate 10-15 slide Markdown
3. Apply storytelling principles (hook → resolve → product → numbers)
4. Number-focused writing (TAM/SAM/SOM, CAC, LTV, BEP)
5. Save to `projects/pitch/[company]-pitchdeck.md`

#### 4. Version Comparison

```
"Show differences between doyak-v10.html and v11.html"
```

**Execution:**
- Read both files, summarize major changes
- Show section-by-section diff
- Suggest improvements

#### 5. Feedback Incorporation

```
"Reviewer feedback: 'Market expansion strategy is weak'. Improve this."
```

**Execution:**
1. Read existing business plan
2. Find "expansion" sections (business model, roadmap)
3. Add network effects, viral strategies
4. Generate `v[N+1].html`
5. Summarize changes

---

## 📐 Template Structures

(HTML and Mermaid templates included in original, maintained as-is for technical accuracy)

---

## 🔧 Tech Stack

Tools used internally by skill:

- **HTML Generation**: Template engine (Mustache/Handlebars style)
- **Diagrams**: Mermaid, ASCII art
- **Version Control**: Git diff logic
- **PDF Conversion**: Browser print API (user manual execution)
- **File I/O**: OpenClaw `read`, `write`, `edit` tools

---

## 📊 Output Examples

### Generated File Structure

```
$WORKSPACE/
└─ projects/
    ├─ gov-support/
    │   ├─ [company]-v1.html (draft)
    │   ├─ [company]-v2.html (feedback incorporated)
    │   └─ [company]-final.pdf (final submission)
    ├─ pitch/
    │   └─ [company]-pitchdeck.md
    └─ infra/
        └─ [project]-infra.md
```

### Event Bus

Event log saved when new version created:

```json
{
  "event": "business_plan_created",
  "timestamp": "2026-02-14T08:06:00Z",
  "version": "v1",
  "file": "projects/gov-support/mycompany-v1.html",
  "company": "MyCompany",
  "type": "doyak-package",
  "changes": "Initial draft created"
}
```

File location: `events/business-plan-2026-02-14.json`

---

## 🎓 Learning Resources

### Recommended Reading

- **Doyak Package Application Guide**: [K-Startup](https://www.k-startup.go.kr/)
- **TIPS Announcements**: [TIPS Town](https://www.tipstown.or.kr/)
- **Y Combinator Pitch Deck Guide**: [YC Library](https://www.ycombinator.com/library/2u-how-to-build-your-seed-round-pitch-deck)
- **McKinsey AI Survey**: [McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

### Internal References

- `memory/consolidated/doyak-business-plan.md` — v1~v12 iteration experience
- `memory/2026-02-09-mupeng-box-infra.md` — Infrastructure design case
- `memory/research/2026-02-14-ai-agent-market.md` — Market research data

---

## 🐧 Footer

> 🐧 Built by **무펭이** — [Mupengism](https://github.com/mupeng) ecosystem skill  
> 📅 Created: 2026-02-14  
> 📝 Version: 1.0.0  
> 🏷️ Tags: #business-plan #pitch-deck #infrastructure #government-funding #IR

---

## 🔄 Update Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-14 | Initial version created. v1~v12 experience internalized |

---

**License**: MIT  
**Contribute**: Pull requests welcome at [github.com/mupeng/workspace/skills/business-planner](https://github.com/mupeng/workspace)
