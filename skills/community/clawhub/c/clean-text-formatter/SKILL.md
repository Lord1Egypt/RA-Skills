# Clean Text Formatter

## Name
`clean-text-formatter`

## Description
Removes Markdown formatting characters and excessive whitespace from AI-generated text. Produces clean, publication-ready plain text.

## Capabilities

### 1. Markdown Stripping
Strips the following while preserving content:
- Headers: `#`, `##`, `###` (removes markers, keeps text)
- Bold/italic markers: `**`, `__`, `*`, `_` (removes markers, keeps text)
- Links: `[text](url)` → keeps `text`
- Images: `![alt](url)` → keeps `alt`
- Blockquotes: `>` lines (removed)
- Code blocks: backticks removed, code content preserved
- List markers: `-`, `*`, `1.` (removed, list content preserved)
- Horizontal rules: `---`, `***` (removed)
- Footnotes: `[^1]` (removed)

### 2. Whitespace Cleaning Around Numbers
Fixes common AI spacing issues:
- `100 %` → `100%`
- `¥ 100` → `¥100`
- `USD 50` → `USD 50` (currency symbols kept with numbers)
- Numbers with leading/trailing spaces trimmed
- Thousand separators `,` preserved: `1,000,000`

### 3. Punctuation Spacing
- Removes spaces before punctuation: `，` `。` `！` `？`
- Removes spaces inside parentheses: `（ 文本 ）` → `（文本）`
- Normalizes multiple spaces to single space
- Trim leading/trailing whitespace from each line

### 4. Unicode Normalization
- Normalizes quotes: `"text"` → `"text"`, `'text'` → `'text'`
- Normalizes dashes: `—` `–` → `-`

## Triggers
- User pastes text and asks to "clean" or "remove Markdown"
- User shares AI-generated content and asks to "format for publication"
- Any content containing visible Markdown syntax

## Workflow
1. Receive raw text input (paste, file upload, or document content)
2. Detect content type and Markdown density
3. Apply cleaning rules in order:
   a. Structural (headers, lists, blockquotes)
   b. Inline formatting (links, images, emphasis)
   c. Whitespace normalization
   d. Punctuation spacing fix
4. Return clean text + optional export

## Input
- Plain text paste
- `.txt`, `.md`, `.docx`, `.html` files
- Direct document content

## Output
- Clean plain text (ready to copy/paste)
- Optional: `.txt` file export

## Limitations
- Does not preserve Markdown intended for re-use (strips permanently)
- Complex nested formatting may require manual review
- LaTeX math expressions: `$$...$$` and `$...$` are preserved

## Dependencies
- Python 3.8+ (for regex processing)
- No external packages required
