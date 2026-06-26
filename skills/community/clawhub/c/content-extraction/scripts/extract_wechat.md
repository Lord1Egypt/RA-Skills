# WeChat Extraction Plan (OpenClaw)

## Target
Extract WeChat public account articles into clean Markdown.

## OpenClaw Execution Path
1. Open URL with browser skill.
2. Wait for article body to render.
3. Read the DOM under the article container.
4. Preserve title / author / date / body / image links.
5. Normalize into Markdown frontmatter +正文。

## Recommended Selectors
- Title: article heading container
- Author: author metadata container
- Publish time: publish time container
- Body: article content container

## Conversion Rules
- Headings → Markdown headings
- Paragraphs → paragraphs
- Images → `![image](url)`
- Quotes → `> quote`
- Lists → markdown lists

## Failure Modes
- Login wall
- Anti-bot / blank page
- Missing content container

## Fallback Strategy
- Try browser with longer wait
- If still failing, try `r.jina.ai`
- Then `defuddle.md`
- Then local web_fetch fallback