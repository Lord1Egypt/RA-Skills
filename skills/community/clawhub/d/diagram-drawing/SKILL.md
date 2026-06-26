---
name: diagram-drawing
description: Generate production-quality SVG+PNG technical diagrams from natural language. Use when user wants to create any technical diagram — architecture, data flow, flowchart, sequence, agent/memory, UML, mind map, or concept map — and export as SVG+PNG. Triggers (EN): "generate diagram", "draw diagram", "create chart", "visualize", "architecture diagram", "flowchart", "sequence diagram", "data flow", "tech graph". Triggers (中文): "画图", "帮我画", "生成图", "做个图", "架构图", "流程图", "可视化", "出图", "技术图". Also triggers on any system/flow description the user wants illustrated, especially for AI/Agent systems (RAG, Agentic Search, Mem0, Multi-Agent, Tool Call).
---

# Diagram Drawing

Generate production-quality SVG+PNG technical diagrams from natural language descriptions.

## Quick Start

1. **Classify** diagram type from user request
2. **Extract** layers, nodes, edges, flows
3. **Plan** layout (top→bottom for most, left→right for wide flows)
4. **Generate** SVG with semantic shapes and arrows
5. **Export** PNG at 1920px width

## Diagram Types & Layout

### Architecture
Nodes = services/components. Group into **horizontal layers** (top→bottom or left→right).
- Typical: Client → Gateway → Services → Data/Storage
- Dashed `<rect>` containers group related services
- ViewBox: `0 0 960 600` or `0 0 960 800`

### Data Flow
Label every arrow with data type ("embeddings", "query", "context"). Wider arrows for primary paths.

### Flowchart / Process
Top-to-bottom preferred. Diamond = decision, rounded rect = process, parallelogram = I/O.

### Agent Architecture
5 layers: Input → Agent Core (LLM) → Memory → Tools → Output
- Show iterative reasoning with **loop arcs** (curved arrows)
- Separate memory read/write paths visually

### Memory Architecture (Mem0-style)
- Show memory **write path** and **read path** separately
- Tiers: Working → Short-term → Long-term → External Store
- Operations: `store()`, `retrieve()`, `forget()`, `consolidate()`

### Sequence Diagram
- Vertical **lifelines** (dashed lines)
- Horizontal arrows = messages, top-to-bottom time order
- Activation boxes (thin filled rects on lifeline)
- ViewBox height = 80 + (num_messages × 50)

### Comparison Matrix
- Column headers = systems, row headers = attributes
- Checked: `#dcfce7` fill + ✓; unsupported: `#f9fafb` fill

### Mind Map
- Central node at `cx=480, cy=280`
- Curved bezier branches, not straight lines
- First-level: 360/N degrees apart

### UML Diagrams
- **Class**: 3-compartment rect (name / attributes / methods)
- **Use Case**: Ellipse + stick figure actors
- **State Machine**: Rounded rects + transitions with guards
- **ER**: Rect entities + diamond relationships + cardinality

## Shape Vocabulary

| Concept | Shape |
|---------|-------|
| User / Human | Circle head + body path |
| LLM / Model | Rounded rect, double border, ⚡ |
| Agent | Hexagon or double-border rect |
| Memory (short-term) | Dashed-border rounded rect |
| Memory (long-term) | Solid cylinder |
| Vector Store | Cylinder with grid lines |
| Graph DB | 3 overlapping circles |
| Tool / Function | Rect with ⚙ icon |
| API Gateway | Hexagon |
| Queue / Stream | Horizontal pipe/tube |
| Document | Folded-corner rect |
| Browser / UI | Rect with 3-dot titlebar |
| Decision | Diamond |

## Arrow Semantics

| Flow Type | Color | Stroke | Dash |
|-----------|-------|--------|------|
| Primary data | `#2563eb` blue | 2px solid | none |
| Control/trigger | `#ea580c` orange | 1.5px solid | none |
| Memory read | `#059669` green | 1.5px solid | none |
| Memory write | `#059669` green | 1.5px | `5,3` |
| Async/event | `#6b7280` gray | 1.5px | `4,2` |
| Embedding | `#7c3aed` purple | 1px solid | none |
| Feedback/loop | `#7c3aed` purple | 1.5px curved | none |

**Always include a legend** when 2+ arrow types are used.

## Workflow (Always Follow)

1. Classify diagram type
2. Extract structure — layers, nodes, edges, flows
3. Plan layout
4. Load style reference from `references/styles.md` for exact colors
5. Map nodes to shapes
6. Check `references/icons.md` for known products
7. Generate SVG
8. Validate: run `python3 scripts/svg2png.py <file.svg>` or `rsvg-convert`
9. Export PNG at 1920px width
10. Report output paths

## SVG Generation Strategy

**Estimate complexity:**
- Count nodes: N, arrows: A
- Estimated SVG lines: L = 50 (header) + N×15 + A×3 + 20 (legend)

**Generation method:**
- **L < 150**: Write tool directly (single call, most reliable)
- **L ≥ 150**: Python script via exec tool (avoids heredoc issues)

**Python method (recommended for complex SVGs):**
```bash
python3 << 'EOF'
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600">
...complete SVG here...
</svg>'''

with open('/path/to/output.svg', 'w') as f:
    f.write(svg_content)
print("Generated output.svg")
EOF
```

## SVG Technical Rules

- ViewBox: `0 0 960 600` default; `0 0 960 800` tall; `0 0 1200 600` wide
- Fonts: `<style>font-family: system-ui, Helvetica, sans-serif</style>` — **no external @import**
- `<defs>`: arrow markers, gradients, filters, clip paths
- Text: minimum 12px, prefer 13-14px labels
- All arrows: `<marker>` with `markerEnd`, sized `markerWidth="10" markerHeight="7"`
- Drop shadows: `<feDropShadow>` sparingly
- Curved paths: `M x1,y1 C cx1,cy1 cx2,cy2 x2,y2` cubic bezier

## Built-in Patterns

**RAG Pipeline**: Query → Embed → VectorSearch → Retrieve → LLM → Response
**Agentic RAG**: Query → Embed → VectorSearch → Agent loop (Tool use) → LLM → Response
**Agentic Search**: Query → Planner → [Search / Calculator / Code] → Synthesizer → Response
**Mem0 Memory**: Input → Memory Manager → [Write: VectorDB + GraphDB] → [Read: Retrieve+Rank] → Context
**Multi-Agent**: Orchestrator → [SubAgent A / B / C] → Aggregator → Output
**Tool Call Flow**: LLM → Tool Selector → Tool Execution → Parser → LLM (loop)

## Error Recovery

| Problem | Fix |
|---------|-----|
| PNG blank/black | Remove `@import url()` — use system fonts only |
| rsvg-convert not found | Use `python3 scripts/svg2png.py` fallback |
| SVG cut off at bottom | Increase ViewBox height |
| Text overflowing | `text-anchor="middle"` + shorten label |
| Marker undefined | Ensure `<marker id="...">` in `<defs>` |
| Arrow crossing nodes | Use orthogonal routing or bezier detour |

## Output

- **Default**: `./[derived-name].svg` and `./[derived-name].png`
- **Custom**: user specifies `--output /path/`

## Styles

| # | Name | Background | Best For |
|---|------|-----------|----------|
| 1 | Flat Icon (default) | White | Blogs, docs, slides |
| 2 | Dark Terminal | `#0f0f1a` | GitHub, dev articles |
| 3 | Blueprint | `#0a1628` | Architecture docs |
| 4 | Notion Clean | White | Notion, wikis |
| 5 | Glassmorphism | `#0d1117` gradient | Product sites, keynotes |
| 6 | Claude Official | `#f8f6f3` warm cream | Anthropic-style diagrams |
| 7 | OpenAI Official | Pure white | OpenAI-style diagrams |

Load `references/styles.md` for exact color tokens and patterns.
