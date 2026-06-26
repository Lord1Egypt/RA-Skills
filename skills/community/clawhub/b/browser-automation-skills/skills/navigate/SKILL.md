---
name: navigate
description: Navigate to a URL and read web page content. Use when opening websites, loading pages, browsing URLs, visiting links, or going to a web address. Also useful when the user says "open", "go to", "visit", "browse", "load page", or provides a URL. 打开网页、访问网站、浏览器导航、加载页面、跳转链接、读取网页内容、访问URL。
allowed-tools: Bash, Read, Write
---

# Navigate

Open a URL in the browser and read the page content.

## Steps

1. **Navigate** to the target URL
2. **Capture screenshot** to verify the page loaded
3. **Read page content** (text or DOM)
4. **Report** the page title, URL, and content summary to the user

## Error Handling

- If the page fails to load, report the error
- If the browser is not connected, inform the user

## Key Points

- Always screenshot after navigation for verification
- If the page needs scrolling, scroll down and capture more screenshots
- Report both visual state and text content

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
