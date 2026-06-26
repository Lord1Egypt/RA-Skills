---
name: scrape
description: Extract and scrape data from web pages, read page content, get DOM structure, parse HTML elements, extract text or structured data from websites. Use when the user wants to scrape a page, extract information, get page text, read web content, parse HTML, or collect data from a website. 抓取数据、提取信息、爬取网页、解析HTML、采集数据、读取网页内容、提取表格、获取页面文本。
allowed-tools: Bash, Read, Write
---

# Scrape

Extract structured content and data from web pages.

## Extraction Methods

| Method | Best For |
|--------|----------|
| Read page text | Quick text content |
| Read DOM/HTML | Structured data, tables, lists |
| Screenshot | Visual layout analysis |

## Patterns

### Extract All Text
1. Navigate to URL
2. Read page text content
3. Return in structured format

### Extract Structured Data (tables, lists, cards)
1. Navigate to URL
2. Read the DOM
3. Find target elements (table/list/card)
4. Extract data from each element
5. Return as structured JSON

### Multi-Page Scraping
1. Navigate to first page
2. Read content
3. Find "next page" link → click it
4. Read next page content
5. Repeat for N pages
6. Return all collected data

### Infinite Scroll Content
1. Navigate to URL
2. Read initial content
3. Scroll down, wait for new content to load
4. Read updated content
5. Repeat until no new content
6. Return accumulated data

## Post-Extraction

1. Parse and clean raw content
2. Structure into user's desired format (JSON, table, CSV)
3. Save to file for large datasets

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
