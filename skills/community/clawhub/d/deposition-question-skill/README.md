# Relativity Deposition Question Builder

Codex skill for legal deposition question development from Relativity-exported PDFs.

The skill:
- asks for the legal theory first,
- extracts bottom-right page IDs from PDFs,
- selects the smaller ID when multiple numbers appear,
- evaluates relevance to the legal theory,
- drafts deposition questions grouped by document ID,
- includes a reason and supporting quote under each question.

## Skill Files

- `SKILL.md`
- `scripts/extract_relativity_pages.py`
- `references/deposition_output_template.md`

## Usage in Codex

Invoke directly:

```text
$relativity-deposition-question-builder analyze these PDFs for my legal theory and draft deposition questions.
```

Example prompt:

```text
Use $relativity-deposition-question-builder. My legal theory is that the defendant knew the defect before sale and concealed it. Analyze PDFs in C:\Cases\Production\RelativityExport and generate questions grouped by document ID with reason and denial quote under each question.
```

## Optional Pre-Extraction Command

```bash
python scripts/extract_relativity_pages.py \
  --input <pdf-folder-or-file> \
  --recurse \
  --output relativity_pages.json \
  --pretty
```

## Output Expectations

For each `Document ID <number>` section, each question includes:
1. `Reason why we ask this question`
2. `Quote from the document to use in deposition in case the opponent party denies`

Reference format: `references/deposition_output_template.md`

## Dependency

Install once if missing:

```bash
python -m pip install --user pdfplumber
```
