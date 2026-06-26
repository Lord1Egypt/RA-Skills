---
name: academic-paper-parse
description: Perform a dual-mode deep reading of any academic paper provided as a PDF attachment or URL. Use this skill when the user requests analysis, close reading, interpretation, or summarization of a scholarly paper. Produce two reports in a single pass: Part A is a rigorous in-depth academic analysis for researchers; Part B distills the core logic and essential value for rapid comprehension.
tools:
  - file
  - message
binaries:
  - name: pdftotext
    optional: true
    fallback: If pdftotext is not available in the runtime environment, use the `read` action of the `file` tool to extract PDF text instead.
---

# Paper Parse

Perform a professional, in-depth analysis of any academic paper and produce two reports at different levels of depth in a single pass.

## Core Principles

- **Academic Rigor**: All descriptions of research design, data, and reasoning must be strictly accurate and consistent with the norms of the relevant discipline.
- **Theoretical Depth**: Clearly reveal the paper's theoretical foundations and core assumptions, and articulate how it supplements, revises, or challenges the existing body of theory.
- **Complete Reproduction**: Faithfully present the full arc from problem statement to conclusion, with particular attention to methodology and key data — zero omission of critical information.
- **Beyond Translation**: The output must illuminate the paper's internal logic and innovations more clearly than a linear translation would.
- **Dual-Mode Output**: Always deliver both Part A and Part B together in a single final file.

## Workflow

Paper analysis is executed in five steps:

### Step 1: Read the Full Paper

Preferably use the `pdftotext` command to extract the full text; if unavailable, fall back to the `read` action of the `file` tool. For URL-sourced papers, attempt to download the PDF before extracting. Coverage must span from abstract to references without exception. For papers containing significant figures or charts, use the `view` action of the `file` tool to inspect key pages and save figure information to a text file.

### Step 2: Synthesize and Analyze

Create a temporary analysis file `temp_analysis.md` and extract and organize the following elements:
- Research questions, hypotheses, methodology, and data sources
- Core findings and key data points
- Theoretical contributions and practical implications
- The paper's fundamental tension, analytical angle, and methodological innovation

**This step must not be skipped.** It is the deliberate thinking process that guarantees the quality of the final report.

### Step 3: Write the Dual-Mode Report

Create the final deliverable file, named in the format `[paper-shortname]_reading-report.md`.

**Before writing Part A**, read the template: `./references/part-a-template.md`

**Before writing Part B**, read the template: `./references/part-b-template.md`

### Step 4: Deliver the Output

Use the `message` tool to deliver the final report file. In the message body, briefly summarize the paper's core innovation, key findings, and theoretical significance to guide the user to the attachment.

### Step 5: Clean Up Temporary Files

Use the `delete` action of the `file` tool to remove `temp_analysis.md` and keep the workspace clean.

## Writing Quality Standards

- Use full prose paragraphs rather than excessive bullet lists; alternate between paragraphs and tables to organize information
- Provide the original English term alongside any translation the first time a key term appears
- Cite specific data points and experimental results from the paper to support every claim
- Part A prioritizes professional completeness; Part B prioritizes insight and concision
- Separate Part A and Part B with a `---` divider in the final file

## Final Deliverable Structure

```markdown
# [Paper Title] — Dual-Mode Reading Report

---

## Part A: In-Depth Academic Analysis

(Full content generated following the structure of part-a-template.md)

---

## Part B: Core Logic Chain and Essential Value Distillation

(Full content generated following the structure of part-b-template.md)
```
