- ---
  name: docx-pdf-knowledge-parser
  description: parse local docx and pdf files into report-first knowledge artifacts. use when chatgpt needs to extract text from uploaded or locally available attachments, generate ingest-report.md, kb-items.jsonl, failed-items.jsonl, and memory.candidate.md without directly writing memory.md.
  ---

  # Docx PDF Knowledge Parser

  Use this skill to turn local or uploaded `.docx` and `.pdf` files into structured, reviewable knowledge outputs.

  ## What this skill does
  - Accept local or already-available `.docx` and `.pdf` files.
  - Classify files into parseable, manual-review, or failed.
  - Parse `.docx` and `.pdf` in v1.0.
  - Produce report-first outputs instead of writing `MEMORY.md` directly.
  - Preserve failures and uncertainty instead of guessing content.

  ## Supported v1.0 scope
  ### Inputs
  - Local `.docx` file path
  - Local `.pdf` file path
  - A batch of local `.docx` and `.pdf` files in one directory

  ### Parsing
  - `.docx`
  - `.pdf`

  ### Outputs
  - `ingest-report.md`
  - `kb-items.jsonl`
  - `failed-items.jsonl`
  - `MEMORY.candidate.md`

  ## Required behavior
  1. Only process files that are already available locally or have already been provided to the runtime.
  2. Do not claim file content was learned unless text was actually extracted.
  3. Default to report-first. Do not write `MEMORY.md` in v1.0.
  4. Record every failed file with a concrete reason.
  5. Prefer plain-text summaries over complex cards when reporting progress.

  ## File routing rules
  ### Parseable
  Treat these as parseable in v1.0:
  - `.docx`
  - `.pdf`

  ### Manual-review
  Route here when the file is out of scope or low-confidence in v1.0:
  - `.pptx`
  - images
  - scans with no extractable text
  - archives
  - unusual file types

  ### Failed
  Route here when the file cannot be opened, parsed, or extracted successfully.

  ## Standard workflow
  1. Resolve input type.
     - Single file path -> process one file
     - Directory path -> enumerate supported files
  2. Create a batch record.
     - Generate `batch_id`
     - Record `started_at`
  3. Build a manifest.
     - File name
     - File path
     - File type
     - Route decision
  4. Attempt extraction.
     - `.docx` -> use `parsers/parse_docx.py`
     - `.pdf` -> use `parsers/parse_pdf.py`
  5. Produce structured outputs.
     - success -> append to `kb-items.jsonl`
     - failure -> append to `failed-items.jsonl`
  6. Summarize the batch.
     - Write `ingest-report.md`
     - Write `MEMORY.candidate.md`
  7. Finish the batch.
     - Record `finished_at`
     - Never auto-write `MEMORY.md`

  ## Output contracts
  ### kb-items.jsonl
  Write one JSON object per successfully extracted knowledge item with at least:
  - `batch_id`
  - `source_file`
  - `source_path`
  - `file_type`
  - `topic`
  - `content_type`
  - `summary`
  - `extracted_at`
  - `confidence`

  ### failed-items.jsonl
  Write one JSON object per failed file with at least:
  - `batch_id`
  - `source_file`
  - `source_path`
  - `file_type`
  - `failure_reason`
  - `error_detail`
  - `suggested_action`
  - `failed_at`

  ### MEMORY.candidate.md
  Include:
  - batch header (`batch_id`, `started_at`, `finished_at`, `source_directory` or `source_file`)
  - grouped knowledge summaries
  - source references
  - confidence notes
  - items needing review

  ### ingest-report.md
  Include:
  1. Batch summary
  2. Input scope
  3. File counts and routing counts
  4. Successful extraction summary
  5. Failures and risks
  6. Recommended next actions

  ## Safety rules
  - Never invent text that was not extracted.
  - If parsing fails, say so plainly and log it.
  - Treat filenames as hints only, never as proof of document contents.
  - Keep sensitive data out of `MEMORY.candidate.md` unless the workflow explicitly allows it.

  ## Included files
  - `run.py`: minimal batch runner for local testing
  - `parsers/parse_docx.py`: docx text extraction helper
  - `parsers/parse_pdf.py`: pdf text extraction helper
  - `references/output_examples.md`: sample output shapes and field guidance
  - `README.md`: setup and usage notes
