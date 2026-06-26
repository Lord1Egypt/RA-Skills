---
name: drawio
description: Generate professional draw.io diagrams (ERD/database tables, class diagrams, sequence diagrams, flowcharts, architecture diagrams) and export them as PNG. Use when the user requests any kind of diagram, database model, class structure, flow, or system visualization.
metadata:
  openclaw:
    requires:
      bins: ["drawio"]
---

# Draw.io Diagram Generation Skill

## When to use this skill
- User requests a database diagram, ERD, or entity-relationship diagram
- User requests a class diagram or UML class structure
- User requests a sequence diagram or interaction diagram
- User requests a flowchart or process flow
- User requests an architecture diagram or system overview
- User mentions "draw.io", "diagram", "table", "entity", "class", "sequence", "flow"

---

## ⚠️ MANDATORY RULES — READ BEFORE GENERATING ANYTHING

1. **ALWAYS detect the diagram type first** before writing any XML
2. **NEVER mix styles** between diagram types — each type has its own strict XML structure
3. **ALWAYS assign unique sequential IDs** to every `mxCell` starting from 0
4. **NEVER use `\n` inside a `value` attribute** — use separate rows/cells instead
5. **ALWAYS calculate table/class heights correctly** using the formulas provided
6. **ALWAYS validate the XML structure** before saving
7. **ALWAYS export to PNG and include the PNG in the response before asking about other formats** — this step is non-negotiable
8. **NEVER use generic rounded rectangles** for database tables or class entities
9. **ALWAYS apply consistent spacing between diagram elements**
   - Horizontal spacing between elements: **minimum 120px**
   - Vertical spacing between rows or steps: **minimum 100px**
   - Tables/classes must not overlap
   - Relationship lines must not cross through table headers

---

## STEP 0 — Diagram Type Detection

Before generating any XML, identify the diagram type from the user's request:

| User says... | Diagram type |
|---|---|
| "database", "ERD", "tables", "entities", "foreign key" | → **TYPE 1: ERD** |
| "class", "UML", "inheritance", "attributes", "methods" | → **TYPE 2: Class Diagram** |
| "sequence", "interaction", "lifeline", "actor calls" | → **TYPE 3: Sequence Diagram** |
| "flowchart", "flow", "process", "decision", "steps" | → **TYPE 4: Flowchart** |
| "architecture", "system", "services", "components" | → **TYPE 5: Architecture** |

---

## Diagram Type References
Use the detailed rules/templates in these files based on the detected type.

- ERD / Database: `ERD.md`
- UML Class: `CLASS.md`
- Sequence: `SEQUENCE.md`
- Flowchart: `FLOWCHART.md`
- Architecture: `LAYOUT.md`


---

## Generation Workflow — ALWAYS follow this exact order

### Step 1 — Identify diagram type
Determine TYPE 1–5 from the user's message before writing any XML.

### Step 2 — Plan all elements
List every entity/class/participant and all relationships before coding.

### Step 3 — Create output folder
```bash
mkdir -p ./diagrams
```

### Step 4 — Write and save the XML
Save to `./diagrams/<diagram-name>.drawio`

**Mandatory pre-save checklist:**
- [ ] All `mxCell` elements have unique sequential numeric IDs
- [ ] ERD tables use `shape=table` with `shape=tableRow` rows (never generic shapes)
- [ ] Class diagrams use `swimlane` with attribute block, divider line, and method block
- [ ] Sequence diagrams have lifelines, activation boxes, and correct arrow styles
- [ ] ERD relationship arrows connect to **row cell IDs**, not table container IDs
- [ ] Heights calculated correctly: `30 + (columns x 30)` for ERD tables
- [ ] No literal `\n` in value attributes (use `&#xa;` for multiline text cells only)
- [ ] XML is well-formed and all tags are closed

### Step 5 — Export to PNG
```bash
# macOS
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 2 -o ./diagrams/<name>.png ./diagrams/<name>.drawio

# Linux / headless
xvfb-run -a drawio -x -f png --scale 2 -o ./diagrams/<name>.png ./diagrams/<name>.drawio
```

### Step 6 — Verify output
```bash
ls -lh ./diagrams/<name>.png
```

### Step 7 — Show PNG first (MANDATORY)

Always respond with the PNG image first (embed/attach it in the response).

### Step 8 — Ask the user for delivery format (MANDATORY)

After showing the PNG, ALWAYS ask the user which additional format they want:

---
The diagram is ready! Which format would you like?

1 - PNG image (ready to view)
2 - .drawio file (editable in draw.io)
3 - SVG (scalable vector)
4 - PDF
5 - All of the above

Reply with the number(s) of your choice.
---

Then based on the response:
- **1** → send the PNG file
- **2** → send the .drawio file
- **3** → export SVG and send it
- **4** → export PDF and send it
- **5** → send all formats
- **Multiple numbers** (e.g. "1 2") → send all requested formats

---

## Other export formats
```bash
# SVG (scalable vector)
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f svg -o ./diagrams/<name>.svg ./diagrams/<name>.drawio

# PDF
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f pdf -o ./diagrams/<name>.pdf ./diagrams/<name>.drawio

# High-res PNG (scale 3)
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 3 -o ./diagrams/<name>_hd.png ./diagrams/<name>.drawio

# Transparent background
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -t --scale 2 -o ./diagrams/<name>_transparent.png ./diagrams/<name>.drawio
```
