---
name: screenshot
description: Capture a screenshot of the current browser page or a specific URL. Use when the user wants to see what a page looks like, take a screenshot, capture the screen, get a visual snapshot, preview a website, or check the appearance of a page. 截图、截屏、页面快照、网页预览、查看页面外观、屏幕捕获、全页截图。
allowed-tools: Bash, Read, Write
---

# Screenshot

Capture visual screenshots of web pages.

## Modes

### Current Page
1. Capture a screenshot of the current viewport

### Specific URL
1. Navigate to the URL
2. Wait for the page to load
3. Capture a screenshot

### Full Page (scroll capture)
1. Capture the current viewport
2. Scroll down
3. Capture again
4. Repeat until page bottom

### Custom Viewport
1. Resize the browser to the target dimensions
2. Navigate (if needed)
3. Capture screenshot

### Common Resolutions
- Mobile: 375×667
- Tablet: 768×1024
- Desktop: 1920×1080

## After Capture

1. View the screenshot file to verify success
2. Report or embed the result

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
