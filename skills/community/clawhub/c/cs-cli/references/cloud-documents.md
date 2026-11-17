# Cloud Document Management Reference

### doc search — Search Cloud Documents

Search the user's CamScanner cloud documents. Supports keyword search, time range filtering, and document type filtering, which can be combined.

```bash
camscanner-cli doc search [keyword] [flags]
```

| Parameter/Flag | Description |
|----------------|-------------|
| `keyword` (positional) | Search keywords (multiple words separated by spaces; any match counts — OR semantics) |
| `-f, --filter` | Document type filter: pdf/word/excel/ppt/image/markdown/html |
| `-n, --limit` | Maximum number of results (default 5, max 50) |
| `-a, --after` | Start time (supports `2006-01-02`, `2006-01-02 15:04:05`, or unix timestamp) |
| `-b, --before` | End time (same formats as above) |
| `-s, --scope` | Search scope: `title` (default — title + page title + notes) or `full` (includes OCR full text) |

**Usage examples**:

```bash
# Search for documents containing "contract"
camscanner-cli doc search "contract"

# Search recent PDF documents
camscanner-cli doc search -f pdf -n 10

# Search documents within a time range
camscanner-cli doc search --after 2026-08-01 --before 2026-08-31

# Keyword + type + time combined search
camscanner-cli doc search "report" -f word --after 2026-08-01

# Full-text search (including OCR content)
camscanner-cli doc search "invoice number" -s full -n 20
```

**Output format**: The CLI displays search results in a table.

**Agent display rules (mandatory)**: When presenting search results to the user, the agent **must** include at least the following four columns:

| Column | Source | Description |
|--------|--------|-------------|
| Title | CLI output "标题" column | Document title |
| Type | Inferred from link URL path (see rules below) | Document type |
| Folder | CLI output "所在目录" column | Folder containing the document |
| Link | CLI output "链接" column | Clickable web page URL |

> **Type inference rules** (two-step):
> 1. **Prefer URL path inference**: `/pdfDetail` → PDF, `/markdownDetail` → Markdown, `/detail` → Scan/Image, `/htmlDetail` → HTML
> 2. **When the path is ambiguous, use cs_doc_id suffix**: `/officeDetail` covers Word, Excel, and PPT. Disambiguate using the Document ID suffix: `_word1` → Word, `_exce1` → Excel, `_pptx1` → PPT
>
> The agent must not omit the Type column or show only title and link.

> **cs_doc_id (internal use)**: The CLI output "文档ID" column contains the `cs_doc_id`, which is the required parameter for `doc download` and `doc move`. The agent should capture this value from search results for subsequent operations, but it **does not need to be displayed to the user**.

**Agent behavior rules**:
- When the user says "find/search/look up my documents", use `doc search` — **do not** enter the image/pdf processing flow.
- Multiple keywords are separated by spaces and use OR semantics (any match counts).
- When no keyword is provided, returns the most recent document list.
- Default returns 5 results; increase `-n` when the user needs more.

**Keyword tokenization strategy**:

The agent should reasonably tokenize the user's search description, separating words with spaces to improve hit probability (under OR semantics, more tokens means broader matching). However, tokenization must be careful:
- **Should tokenize**: user says "thesis formula HD" → split to `"thesis formula HD"`; user says "meeting notes August" → split to `"meeting notes August"`
- **Should not tokenize**: proper nouns, brand names, personal names, and fixed phrases must not be forcibly split. E.g., "CamScanner" stays as one token; "Zhang San's report" keeps "Zhang San" together.
- **When uncertain, do not tokenize**: if unsure whether splitting improves results, pass the user's original text as a single keyword.

**Semantic intent recognition**:

The agent must parse the user's query semantically, extracting time, type, and other structured intents into the corresponding parameters — **not as search keywords**:

- **Time intent → `--after` / `--before` parameters**: when the user mentions a time range, parse it as a time filter, not as a keyword.
  - "papers from last August" → `doc search "papers" --after 2025-08-01 --before 2025-08-31`
  - "meeting notes from last week" → `doc search "meeting notes" --after 2026-08-17 --before 2026-08-23`
  - "contracts from this year" → `doc search "contracts" --after 2026-01-01`
- **Type intent → `-f` parameter**: when the user mentions a document type, map it to the type filter.
  - "find my PDF invoices" → `doc search "invoices" -f pdf`
- **Quantity intent → `-n` parameter**: when the user says "recent ones", "find more", etc., adjust the return count.

> **Core principle**: The tokenization strategy applies only to **actual search keywords**. Time, type, quantity, and other structured semantics must be extracted into the corresponding command parameters and must never be mixed into keywords. Wrong example: `doc search "last August papers"` — this would match "last August" as literal text in document content instead of filtering by time.

**Search scope decision (`-s` parameter)**:

| User Intent | Parameter |
|-------------|-----------|
| Explicitly says "in the title", "in notes", "page title" | `-s title` |
| Explicitly says "in the content", "in the body", "full text search" | `-s full` |
| No explicit intent (default) | First search with `-s title`; if no results, automatically retry with `-s full` |

> **Two-step search strategy**: When the user does not specify a search scope, first search by title (faster), then search full text if no results (covers OCR content). If both return nothing, report that these searches found no matching document; do not conclude that it does not exist or that a cloud save did not occur.

### doc download — Download Cloud Document

Download a cloud document to local. Office documents (Word/Excel/PPT/PDF/Markdown/HTML) keep their original format; image-type documents default to PDF export, with an option to export as a JPG ZIP package.

```bash
camscanner-cli doc download <doc_id> [flags]
```

| Parameter/Flag | Description |
|----------------|-------------|
| `doc_id` (positional) | Document ID (required; obtainable from `doc search` results) |
| `-o, --output <path>` | Output file path (if omitted, auto-named from doc_id) |
| `-f, --format` | Image document export format: `pdf` (default) or `zip` (JPG archive) |

**Usage examples**:

```bash
# Download a Word document (auto-keeps .docx format)
camscanner-cli doc download 7DD6DB7134654A5Fbg9af7hS_word1

# Download an image document as PDF
camscanner-cli doc download D5BC4625B8A14F3EVX7tY9Hf

# Download an image document as JPG ZIP
camscanner-cli doc download D5BC4625B8A14F3EVX7tY9Hf -f zip

# Specify output path
camscanner-cli doc download D5BC4625B8A14F3EVX7tY9Hf -o ~/Downloads/scan.pdf
```

**Agent behavior rules**:
- `doc download` requires a `cs_doc_id` parameter (from the "Document ID" column in `doc search` results). **Without a cs_doc_id, downloading is not possible.**
- **Search results must be confirmed by the user before any operation**: even if only one document matches, the agent must present the result and wait for the user's explicit confirmation before downloading. **Do not** skip confirmation and auto-execute.
- **If the user has not provided a cs_doc_id and there are no search results in the current session**, the agent must first guide the user to run `doc search`, confirm the target document, then download.
  - Example: user says "download my contract" → Agent replies "Let me search for documents matching 'contract' first" → runs `doc search "contract"` → presents results for user confirmation → after confirmation, runs `doc download <cs_doc_id>`
- Office documents (doc_id suffix contains `_word1`, `_exce1`, `_pdfx0`, etc.) auto-keep their format; no need for `-f`
- Image-type documents (no known suffix) default to PDF export; use `-f zip` when the user needs original images
- Check whether the output path already exists before executing to avoid silent overwrites
- **Post-download guidance rules**: After a successful download, the Agent should suggest further processing options based on the file type. The processing flow fully reuses existing file processing capabilities (upload → process → save to cloud). Guidance rules:
  - **PDF files** (exported PDF from image documents or native PDF): suggest format conversion (to Word/Excel/Markdown/TXT), splitting into images, or adding/removing watermarks
  - **Image files** (JPGs extracted from `-f zip` export): suggest enhancement/upscaling/restoration, format conversion, OCR, translation, formula extraction, text editing, etc.
  - **TXT/Markdown files**: suggest converting to Word
  - **Word/Excel/PPT files**: use `office convert` to convert to PDF; legacy DOC/XLS/PPT files can also be upgraded to DOCX/XLSX/PPTX. See `references/office-processing.md` for parameters
  - **HTML files**: no processing capabilities available currently; do not offer guidance
  - Guidance style: after download, briefly inform the user "If you'd like to further process this file, you can..." and list 2-3 of the most common operations. **Do not force guidance** — if the user doesn't need it, simply end the interaction

### doc dirs — View Folder List

Query and display the user's cloud folder directory tree. Use this to obtain folder IDs for `doc move`, `--save-dir-id`, and similar commands.

```bash
camscanner-cli doc dirs
```

No parameters; just run it.

**Output format**: Tree-structured directory listing. Each line shows the folder name, document count, and folder ID:

```
Folder list (3 total):

├── Work Documents (5)  [EBC6aFh3WHgTP9VWWUeP2R4J]
│   └── Contracts (2)  [FCC7bGi4XIhUQ0WXXVfQ3S5K]
└── Personal Files (3)  [GDD8cHj5YJiVR1XYYWgR4T6L]
```

**Agent behavior rules**:
- When the user asks "what folders do I have", "view directories", "list folders", use `doc dirs`
- When you need a dir_id for `doc move` or `--save-dir-id`, first run `doc dirs` to get the list
- Preserve the tree structure when presenting results; the bracket content is the folder ID

### doc move — Move Documents

Move one or more cloud documents to a specified folder, or back to the root directory.

```bash
camscanner-cli doc move <doc_id> [doc_id...] --dir-id <folder_id>
camscanner-cli doc move <doc_id> [doc_id...] --root
```

| Parameter/Flag | Description |
|----------------|-------------|
| `doc_id` (positional) | Document ID(s), supports multiple (required) |
| `--dir-id <id>` | Target folder ID (obtain via `doc dirs`) |
| `--root` | Move to root directory (mutually exclusive with `--dir-id`) |

**Usage examples**:

```bash
# Move a single document to a folder
camscanner-cli doc move DOC_ID --dir-id EBC6aFh3WHgTP9VWWUeP2R4J

# Batch move multiple documents
camscanner-cli doc move DOC_ID_1 DOC_ID_2 --dir-id EBC6aFh3WHgTP9VWWUeP2R4J

# Move a document back to root
camscanner-cli doc move DOC_ID --root
```

**Agent behavior rules**:
- `doc move` requires specific `cs_doc_id`(s) (from `doc search` results). **Without cs_doc_id, moving is not possible.**
- `--dir-id` and `--root` are mutually exclusive — one must be specified
- **Moving is a dangerous operation that modifies the user's cloud data.** The agent must be extremely cautious:
  - **Do not** execute a move without the user confirming the specific document(s). Even if search returns matches, the agent must present results and get explicit confirmation before acting.
  - **Do not** batch-move documents the user has not individually confirmed. For example, if the user says "move my PDF documents to root", the agent must **never** search for all PDFs and move them all automatically.
  - If the user has not provided a cs_doc_id, the agent must first guide them to search, present results, and let them confirm which document(s) to move.
- Supports moving multiple documents at once; separate cs_doc_ids with spaces
- **Folder matching flow (mandatory when the user specifies a folder name)**:
  1. First run `doc dirs` to get the full folder list
  2. Match the user's folder name against the returned list
  3. **Exact match found**: use the corresponding dir_id to run `doc move --dir-id <dir_id>`
  4. **Similar folder names exist**: present the similar folder names to the user for confirmation. E.g., user says "Work Files" but only "Work Documents" and "Work Materials" exist — prompt: "Folder 'Work Files' not found. Did you mean one of these? 1. Work Documents 2. Work Materials"
  5. **No match at all**: inform the user the folder does not exist, list all available folders for them to choose from. **Never** silently fall back to root or guess
- **Post-move feedback**: The CLI output shows the target as a dir_id (e.g., `7KT73KB8DyCTr3LAgTbFUEHL`), which is meaningless to the user. Since the Agent already obtained folder names via `doc dirs` before the move, it **must** use the folder name when reporting the result to the user. Example: `Moved "Contract Document" to the "Work Documents" folder`. For nested folders, show the full path: `Moved to "Projects/tt1"`.
- **Typical multi-step flow**: user says "move the contract to Work Documents folder" → Agent replies "Let me search for 'contract' documents first" → runs `doc search "contract"` → presents results → user confirms "move #1" → runs `doc dirs` to get folder list → matches "Work Documents" in list → match found: runs `doc move <cs_doc_id> --dir-id <dir_id>` → reports to user: "Moved 'Contract' to 'Work Documents' folder"

### Cloud Document Workflow Combinations

**Search → Download**: The typical flow when a user needs to get a cloud document locally.

```bash
# Step 1: search for the target document
camscanner-cli doc search "contract"
# Step 2: Agent presents search results for user confirmation
# Step 3: use the confirmed cs_doc_id to download
camscanner-cli doc download <cs_doc_id> -o ~/Downloads/contract.pdf
```

**Process → Save to Folder**: Process a local file and auto-save to a specific folder.

```bash
# Convert an image to Word and save to the "Work Documents" folder
camscanner-cli image convert photo.jpg --format word -s --save-dir "Work Documents"
```

**Search → Move to Archive**: Organize existing cloud documents into folders. **Moving is a dangerous operation; user confirmation is required.**

```bash
# Step 1: search for target documents
camscanner-cli doc search "invoice"
# Step 2: Agent presents search results; user confirms which document(s) to move
# Step 3: list folders
camscanner-cli doc dirs
# Step 4: match the user's folder name against the folder list
#   - Exact match: use the corresponding dir_id
#   - Similar names exist: present similar folders for user to confirm
#   - No match: inform user the folder doesn't exist, list all available folders
# Step 5: use the confirmed cs_doc_id and matched dir_id to move
camscanner-cli doc move <cs_doc_id> --dir-id <folder_id>
```
