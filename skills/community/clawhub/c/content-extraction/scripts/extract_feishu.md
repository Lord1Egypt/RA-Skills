# Feishu Extraction Plan (OpenClaw)

## Target
Extract Feishu / Lark docs and wiki pages into Markdown.

## OpenClaw Execution Path
1. Detect whether the URL is doc / docx / wiki.
2. For wiki, resolve the underlying node/document first.
3. Use OpenClaw Feishu tools to fetch structured content.
4. Convert blocks to Markdown.
5. Preserve frontmatter metadata.

## Markdown Mapping
- Heading blocks → `#`
- Text blocks → plain text
- Ordered / bullet lists → markdown lists
- Code blocks → fenced code blocks
- Quote blocks → blockquotes
- Todo blocks → `- [ ]` / `- [x]`
- Images → image placeholders or URLs

## Failure Modes
- Missing permissions
- Invalid doc token
- Wiki node resolution failure
- API quota / auth issues

## Fallback Strategy
- Retry with resolved doc token
- If tool unavailable, use web_fetch as last resort for public docs