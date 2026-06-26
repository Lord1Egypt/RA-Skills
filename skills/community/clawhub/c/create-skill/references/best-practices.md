# Skill Writing Best Practices

A comprehensive guide for writing effective skills that Agents can successfully discover and use.

## Core Principles

### Brevity is Key

Context window is a shared resource. Your skill shares it with conversation history, other skills' metadata, and the actual request. Be concise and challenge every piece of information.

**Default Assumption**: The Agent is already very smart. Only add context the Agent doesn't already have.

**Good Example: Concise** (~50 tokens):
````markdown
## Extract PDF Text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Bad Example: Too Verbose** (~150 tokens):
```markdown
## Extract PDF Text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from PDFs, you need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you need to install it using pip. Then you can use the code below...
```

### Set Appropriate Degrees of Freedom

Match specificity to the task's fragility and variability.

**High Freedom** (text-based instructions):
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

**Medium Freedom** (pseudocode or scripts with parameters):
- Preferred patterns exist
- Some variation is acceptable
- Configuration affects behavior

**Low Freedom** (specific scripts with few or no parameters):
- Operations are fragile and error-prone
- Consistency is critical
- Must follow specific sequence

### Test with All Models

Skills complement models, so effectiveness depends on the underlying model. Test your skills with all models you plan to use.

## Naming Conventions

Use consistent naming patterns. We recommend **gerund form** (verb + -ing) for skill names.

**Good Naming Examples (Gerund Form)**:
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**Acceptable Alternatives**:
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Action-oriented: `process-pdfs`, `analyze-spreadsheets`

**Avoid**:
- Vague names: `helper`, `utils`, `tools`
- Too generic: `documents`, `data`, `files`
- Inconsistent patterns across skill sets

## Writing Effective Descriptions

The `description` field enables skill discovery and should include what the skill does and when to use it.

**Always use third person**. Descriptions are injected into system prompts.

- **Good:** "Processes Excel files and generates reports"
- **Avoid:** "I can help you process Excel files"
- **Avoid:** "You can use it to process Excel files"

**Be specific and include key terms**. Include what the skill does and specific triggers/contexts for when to use it.

**Effective Examples:**

```yaml
description: Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF files or when users mention PDFs, forms, or document extraction.
```

```yaml
description: Analyzes Excel spreadsheets, creates pivot tables, generates charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Avoid Vague Descriptions:**
```yaml
description: Helps with documents  # Too vague
```

## Progressive Disclosure Patterns

### Pattern 1: High-Level Guide with References

````markdown
# PDF Processing

## Quick Start

Use pdfplumber to extract text:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced Features

**Form Filling**: See [FORMS.md](FORMS.md) for complete guide
**API Reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

### Pattern 2: Domain-Specific Organization

For skills with multiple domains, organize content by domain:

```
bigquery-skill/
├── SKILL.md (Overview and navigation)
└── reference/
    ├── finance.md (Revenue, billing metrics)
    ├── sales.md (Opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (Campaigns, attribution)
```

### Pattern 3: Conditional Details

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating Documents

Use docx-js to create new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing Documents

For simple edits, modify XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

### Avoid Deeply Nested References

Keep reference files one level deep from SKILL.md. All reference files should be directly linked from SKILL.md to ensure the Agent reads complete files when needed.

**Bad Example: Too Deep**:
```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Good Example: One Level Deep**:
```markdown
# SKILL.md

**Basic Usage**: [Instructions in SKILL.md]
**Advanced Features**: See [advanced.md](advanced.md)
**API Reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### Structure Longer Reference Files

For reference files over 100 lines, include a table of contents at the top. This ensures the Agent sees the full scope of available information even when reading partial previews.

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear sequential steps. For particularly complex workflows, provide a checklist that the Agent can copy into responses and check off as it proceeds.

**Example: PDF Form Filling Workflow**

````markdown
## PDF Form Filling Workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze Form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their positions, saving to `fields.json`.
````

### Implement Feedback Loops

**Common Pattern**: Run validator → Fix errors → Repeat

This pattern significantly improves output quality.

**Example: Document Editing Process**

```markdown
## Document Editing Process

1. Make edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review error messages carefully
   - Fix issues in XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test output document
```

## Content Guidelines

### Avoid Time-Sensitive Information

Don't include information that will become outdated:

**Bad Example: Time-Sensitive**:
```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Good Example** (using "Legacy Patterns" section):
```markdown
## Current Approach

Use v2 API endpoint: `api.example.com/v2/messages`

## Legacy Patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API uses: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

### Use Consistent Terminology

Choose one term and use it throughout the skill:

**Good - Consistent**:
- Always use "API endpoint"
- Always use "field"
- Always use "extract"

**Bad - Inconsistent**:
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
- Mix "extract", "pull", "get", "retrieve"

## Common Patterns

### Template Pattern

Provide templates for output formats. Match strictness to your needs.

**For Strict Requirements**:

````markdown
## Report Structure

Always use this exact template structure:

```markdown
# [Analysis Title]

## Executive Summary
[One paragraph overview of key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
```

**For Flexible Guidance**:

````markdown
## Report Structure

This is a reasonable default format, but use your best judgment:

```markdown
# [Analysis Title]

## Executive Summary
[Overview]

## Key Findings
[Adjust sections based on what you find]
```

Adapt sections as needed for the specific analysis type.
````

### Example Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

````markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Add user authentication with JWT tokens
Output:
```
feat(auth): Implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fix bug where dates display incorrectly in reports
Output:
```
fix(reports): Correct date formatting in timezone conversion

Use UTC timestamps consistently in report generation
```
````

## Anti-Patterns to Avoid

### Avoid Windows-Style Paths

Always use forward slashes in file paths, even on Windows:

- ✓ **Good**: `scripts/helper.py`, `reference/guide.md`
- ✗ **Avoid**: `scripts\helper.py`, `reference\guide.md`

### Avoid Providing Too Many Options

Don't provide multiple approaches unless necessary:

````markdown
**Bad Example: Too Many Choices**:
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good Example: Provide Default**:
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image and pytesseract instead."
````

## Evaluation and Iteration

### Build Evaluations First

**Create evaluations before writing extensive documentation.** This ensures your skill solves real problems, not imagined ones.

**Evaluation-Driven Development:**
1. **Identify Gaps**: Run the Agent on representative tasks without the skill. Document specific failures or missing context
2. **Create Evaluations**: Build three scenarios that test these gaps
3. **Establish Baseline**: Measure Agent performance without the skill
4. **Write Minimal Instructions**: Create just enough content to address the gaps and pass evaluations
5. **Iterate**: Run evaluations, compare to baseline, and refine

### Iteratively Develop Skills

Work with one Agent instance ("Agent A") to create a skill that will be used by other instances ("Agent B"). Agent A helps you design and refine instructions, while Agent B tests them on real tasks.

**Creating New Skills:**

1. **Complete Task Without Skill**: Solve the problem with Agent A using normal prompting. Note information you repeatedly provide.

2. **Identify Reusable Patterns**: After completing the task, identify which context you provided would be useful for similar future tasks.

3. **Ask Agent A to Create Skill**: "Create a skill that captures the patterns we just used. Include the patterns, naming conventions, and filtering rules."

4. **Check for Brevity**: Review whether Agent A added unnecessary explanations.

5. **Improve Information Architecture**: Ask Agent A to organize content more effectively.

6. **Test on Similar Tasks**: Use the skill with Agent B on related use cases.

7. **Iterate Based on Observations**: If Agent B struggles or misses something, return to Agent A with specific information.

## Effective Skill Checklist

Before sharing a skill, verify:

### Core Quality
- [ ] Description is specific and includes key terms
- [ ] Description includes what the skill does and when to use it
- [ ] SKILL.md body is less than 200 lines (ideally <500 for optimal performance)
- [ ] Additional details are in separate files (if needed)
- [ ] No time-sensitive information (or in "Legacy Patterns" section)
- [ ] Terminology is consistent throughout the skill
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Progressive disclosure is used appropriately
- [ ] Workflows have clear steps

### Code and Scripts
- [ ] Scripts solve problems rather than pushing to Agent
- [ ] Error handling is clear and helpful
- [ ] No "magic constants" (all values have rationale)
- [ ] Required packages are listed in instructions
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths (all forward slashes)
- [ ] Validation/verification steps for critical operations
- [ ] Quality-critical tasks include feedback loops
- [ ] Windows compatibility (use .ps1 or .bat instead of .sh)

### Testing
- [ ] At least three evaluations created
- [ ] Tested with different models (if applicable)
- [ ] Tested with real use cases
- [ ] Team feedback incorporated (if applicable)
