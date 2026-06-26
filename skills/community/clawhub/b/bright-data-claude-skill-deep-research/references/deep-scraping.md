# Deep Scraping Template

This template handles browser automation for JavaScript-rendered or interactive pages.

## When to Use Deep Scraping

Use browser automation when:
- Content requires JavaScript to render (React, Vue, Angular apps)
- Pages load data dynamically via AJAX
- Need to interact with the page (click, scroll, fill forms)
- Sites have strong anti-bot measures
- Need to handle pagination dynamically
- Content is behind login walls

## Process

### Step 1: Navigate to Page

```json
{
  "tool": "scraping_browser_navigate",
  "parameters": {
    "url": "{{url}}"
  }
}
```

**Expected Response**:
```
Successfully navigated to https://example.com
Title: Page Title
URL: https://example.com
```

**Wait Strategy**:
- Browser automatically waits for page load (up to 120 seconds)
- For dynamic content, add additional wait time
- Look for specific elements to appear

### Step 2: Discover Page Elements

Get all clickable elements and links:

```json
{
  "tool": "scraping_browser_links",
  "parameters": {}
}
```

**Expected Response**:
```json
[
  {
    "text": "Next Page",
    "href": "/page/2",
    "selector": "a.pagination-next"
  },
  {
    "text": "Load More",
    "href": "#",
    "selector": "button#load-more"
  }
]
```

### Step 3: Extract Content

After navigation, you can:
- Use `scrape_as_markdown` on the current page
- Extract content manually from page HTML
- Use `extract` with the current URL

### Step 4: Interact with Page

Click elements using CSS selectors:

```json
{
  "tool": "scraping_browser_click",
  "parameters": {
    "selector": "{{css_selector}}"
  }
}
```

**Common Interactions**:

**Pagination**:
```json
{
  "tool": "scraping_browser_click",
  "parameters": {
    "selector": "a.next-page"
  }
}
```

**Load More Buttons**:
```json
{
  "tool": "scraping_browser_click",
  "parameters": {
    "selector": "button.load-more"
  }
}
```

**Dropdowns/Filters**:
```json
{
  "tool": "scraping_browser_click",
  "parameters": {
    "selector": "select#sort-by option[value='price-desc']"
  }
}
```

### Step 5: Repeat for Multi-Page Content

For content spread across multiple pages:

1. Navigate to initial URL
2. Extract content from page 1
3. Click "Next" button
4. Wait for page load
5. Extract content from page 2
6. Repeat until no more pages

## Advanced Techniques

### Scrolling for Lazy Loading

Some pages load content as you scroll:

```markdown
1. Navigate to page
2. Scroll down (execute JavaScript)
3. Wait for new content to load
4. Repeat until no new content appears
5. Extract all content
```

### Handling Infinite Scroll

```markdown
1. Navigate to page
2. While true:
   - Get current height
   - Scroll to bottom
   - Wait 2 seconds
   - Check if height increased
   - If no increase, break
3. Extract all loaded content
```

### Waiting for Specific Elements

```markdown
1. Navigate to page
2. Wait for element with selector ".data-loaded" to appear
3. Extract content
```

### Handling Modals and Popups

```markdown
1. Navigate to page
2. Check for modal: ".modal" or ".popup"
3. If present, click close button: ".close-modal"
4. Wait for modal to disappear
5. Proceed with extraction
```

## CSS Selector Tips

### Basic Selectors
- `#id` - Element by ID
- `.class` - Element by class
- `tag` - Element by tag name
- `tag.class` - Tag with class

### Combinations
- `div.container > ul > li` - Direct children
- `div.container ul li` - Any descendants
- `button[type="submit"]` - Attribute selector

### Useful Patterns
- `a.next-page` - Next/prev buttons
- `button.load-more` - Load more buttons
- `.pagination a` - Pagination links
- `.item:nth-child(n)` - Specific item
- `[data-page="2"]` - Data attributes

### Testing Selectors
Before using in automation:
1. Open page in browser
2. Open DevTools (F12)
3. Use `document.querySelector('selector')` in console
4. Verify it returns the correct element

## Error Handling

### Navigation Failures
- **Timeout**: Page takes too long to load
  - Solution: Increase wait time or check if page is accessible
- **Blocked**: Site blocks automated browsers
  - Solution: Use different user agent or try scrape_as_markdown

### Click Failures
- **Element not found**: Selector doesn't match any element
  - Solution: Verify selector, check if element exists
- **Element not clickable**: Element is obscured or disabled
  - Solution: Wait for page to stabilize, check if element is enabled
- **Navigation doesn't occur**: Click doesn't navigate
  - Solution: Element might trigger JavaScript, handle accordingly

### Session Issues
- **Session lost**: Browser session disconnected
  - Solution: Navigate again to restore session
- **Cookie/State lost**: Page lost authentication or state
  - Solution: Re-navigate and re-authenticate if needed

## Best Practices

1. **Use Specific Selectors**: More specific = more reliable
2. **Wait for Stability**: Don't click immediately after page load
3. **Handle Errors Gracefully**: Have fallback strategies
4. **Log Everything**: Track navigation, clicks, and extractions
5. **Respect the Site**: Don't overwhelm with rapid actions
6. **Test First**: Manually test the workflow before automating
7. **Use Session Persistence**: Browser keeps cookies/state across calls

## Example Workflow: Multi-Page Product Listing

```markdown
Goal: Extract all products from a multi-page category page

1. Navigate to category page:
   scraping_browser_navigate("https://example.com/category")

2. Initialize: products = [], page = 1

3. While true:
   a. Extract product data from current page
   b. Add to products array
   c. Look for "Next" button
   d. If no "Next" button, break
   e. Click "Next" button
   f. Wait for page load
   g. page += 1

4. Return all products
```

## Output Format

```json
{
  "workflow": "multi_page_extraction",
  "starting_url": "https://example.com",
  "total_pages": {{number}},
  "total_items": {{number}},
  "data": [
    {
      "page": 1,
      "items": [ /* extracted items */ ]
    },
    {
      "page": 2,
      "items": [ /* extracted items */ ]
    }
  ],
  "actions_taken": [
    "navigate",
    "extract",
    "click .next-page",
    "extract"
  ],
  "duration_seconds": {{time}}
}
```

## Performance Considerations

- **Browser automation is slower**: 10-50x slower than direct scraping
- **Use only when necessary**: Prefer scrape_as_markdown when possible
- **Parallel sessions**: Can maintain multiple browser sessions for different domains
- **Timeout management**: Set appropriate timeouts to avoid hanging
- **Resource intensive**: Uses more memory and CPU than direct scraping
