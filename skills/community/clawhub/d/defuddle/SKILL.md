
---
name: defuddle-web-cleaner
description: extract clean article content from web pages using defuddle. use when a user provides a url or html and wants the readable article text, markdown version, or structured metadata. helpful for web scraping, research workflows, note taking, obsidian clipping, and converting web pages to markdown.
---

# Defuddle Web Cleaner

Extract the main readable content from a web page.

This skill removes unnecessary elements such as:
- navigation bars
- sidebars
- ads
- comments
- footers
- social buttons

The result is clean article content.

## Supported Inputs

1. URL
2. Raw HTML
3. Web page text

## Output Format

Default output:

Title  
Author  
Site  
Published date  

Markdown article content

Alternative output (JSON):

{
  title,
  author,
  site,
  description,
  published,
  content,
  contentMarkdown
}

## Processing Steps

1. Detect input type
2. Load page HTML
3. Run Defuddle parser
4. Extract metadata
5. Convert to Markdown if requested
6. Return clean content

## Example

Input:

https://example.com/blog/ai

Output:

Title: AI is Changing Everything  
Author: Jane Smith  
Site: Example Blog  

Markdown:

# AI is Changing Everything

Artificial intelligence is transforming industries...

## Tips

Use this skill when:
- saving articles to Obsidian
- building research datasets
- cleaning webpages for LLM processing
- summarizing articles
