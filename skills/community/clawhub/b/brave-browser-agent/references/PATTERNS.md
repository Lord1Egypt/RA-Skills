# Brave Browser Agent - Common Patterns

This file contains common usage patterns for the Brave Browser Agent. Refer to this when you need specific examples of browser automation tasks.

## Quick Reference: Smart Interaction vs JS eval

| Task | Command | When to use |
|------|---------|-------------|
| Read content | `eval` | Always — no interaction needed |
| Navigate | `eval "location.href=..."` | Simple navigation |
| Click (anti-detection) | `interact` | Anti-bot sites, Xiaohongshu, etc. |
| Click (simple) | `eval "el.click()"` | Trusted sites, no anti-bot |
| Type text | `type` | Form filling, search input |
| Wait for load | `wait` | SPA pages, dynamic content |
| Scroll | `scroll` | Infinite scroll, lazy loading |
| Find elements | `elements` | Don't know page structure |
| Check pagination | `pagination` | Multi-page scraping |
| Highlight target | `highlight` | Debugging, screenshot confirmation |

## Smart Interaction Patterns

### Click Element by CSS Selector (CDP Native Events)

```bash
# Click first matching element — uses real mouse events (anti-detection)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector "button.submit"

# Click element at specific index
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector ".note-item" --index 2

# Click element containing specific text
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector "button" --text "Load More"

# Click at specific coordinates
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --x 400 --y 300
```

### Wait for Page State

```bash
# Wait for page to fully load
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --page-load --timeout 10

# Wait for specific element to appear
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --selector ".result-item" --timeout 10

# Wait for network idle (all requests complete)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --network-idle --timeout 15
```

### Smooth Scrolling

```bash
# Scroll down 3 steps
python3 {{SKILL_DIR}}/scripts/cdp_exec.py scroll <tab_id> --direction down --amount 300 --steps 3

# Scroll up
python3 {{SKILL_DIR}}/scripts/cdp_exec.py scroll <tab_id> --direction up --amount 500 --steps 2
```

### Type Text

```bash
# Quick insert (fast)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py type <tab_id> "hello world"

# Human-like typing (char by char, for anti-detection)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py type <tab_id> "search query" --human

# Press Enter key
python3 {{SKILL_DIR}}/scripts/cdp_exec.py key <tab_id> Enter
```

### Page State Analysis

```bash
# List all interactive elements on page
python3 {{SKILL_DIR}}/scripts/cdp_exec.py elements <tab_id>

# List specific elements
python3 {{SKILL_DIR}}/scripts/cdp_exec.py elements <tab_id> --selector "a.product" --limit 20

# Check page load status
python3 {{SKILL_DIR}}/scripts/cdp_exec.py page-status <tab_id>

# Detect pagination buttons
python3 {{SKILL_DIR}}/scripts/cdp_exec.py pagination <tab_id>

# Count elements matching selector
python3 {{SKILL_DIR}}/scripts/cdp_exec.py count <tab_id> --selector ".item"

# Get element coordinates
python3 {{SKILL_DIR}}/scripts/cdp_exec.py locate <tab_id> --selector "#submit-btn"

# DOM snapshot
python3 {{SKILL_DIR}}/scripts/cdp_exec.py snapshot <tab_id> --max-depth 4 --max-chars 3000
```

### Highlight Elements (for debugging)

```bash
# Highlight an element before screenshot
python3 {{SKILL_DIR}}/scripts/cdp_exec.py highlight <tab_id> --selector ".target-element"
python3 {{SKILL_DIR}}/scripts/cdp_exec.py screenshot <tab_id> debug.png
```

## Content Extraction Patterns

### Extract Article Content
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "JSON.stringify({title: document.title, url: location.href, text: (document.querySelector('article') || document.body).innerText.substring(0, 10000)})"
```

### Extract Page Text (First 5000 chars)
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.body.innerText.substring(0, 5000)"
```

### Extract Links (First 20)
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "Array.from(document.querySelectorAll('a')).slice(0, 20).map(a => ({text: a.textContent.trim().substring(0, 80), href: a.href}))"
```

### Extract All Images
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "Array.from(document.querySelectorAll('img')).map(img => ({src: img.src, alt: img.alt || ''}))"
```

## Dynamic Content Patterns

### Wait for Page Load Then Extract
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --page-load --timeout 10
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.body.innerText.substring(0, 5000)"
```

### Fetch API Data
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "fetch('https://api.example.com/data').then(r => r.json())" --await-promise
```

### Scroll to Load More Content
```bash
# Smart scroll (CDP mouse wheel events)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py scroll <tab_id> --direction down --amount 400 --steps 3
sleep 2
# Then extract
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.body.innerText.substring(0, 5000)"
```

### Scroll in Steps (for lazy loading)
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "for(let i=0;i<5;i++){setTimeout(()=>window.scrollTo(0,document.body.scrollHeight),i*500)}'scrolled 5 times'"
```

## Form Interaction Patterns

### Fill and Submit Search Form (Anti-Detection)
```bash
# 1. Click the search box
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector "#search"

# 2. Type the query (human-like)
python3 {{SKILL_DIR}}/scripts/cdp_exec.py type <tab_id> "search terms" --human

# 3. Press Enter
python3 {{SKILL_DIR}}/scripts/cdp_exec.py key <tab_id> Enter

# 4. Wait for results
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --selector ".results" --timeout 10
```

### Fill and Submit Search Form (Simple — JS eval)
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.querySelector('#search').value = 'hello'; document.querySelector('form').submit(); 'submitted'"
```

### Get Form Field Values
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({name: el.name, value: el.value, type: el.type}))"
```

## Navigation Patterns

### Navigate to New URL in Same Tab
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "window.location.href = 'https://example.com/page2'"
```

### Go Back
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "window.history.back(); 'went back'"
```

### Reload Page
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "location.reload(); 'reloaded'"
```

## Page State Patterns

### Get Page Title and URL
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "JSON.stringify({title: document.title, url: location.href})"
```

### Get Page Cookies
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.cookie"
```

### Get Local Storage
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "JSON.stringify({...localStorage})"
```

### Get Session Storage
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "JSON.stringify({...sessionStorage})"
```

## Debugging Patterns

### Check if Page is Fully Loaded
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.readyState"
```

### Get Network Requests
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "JSON.stringify(performance.getEntries().filter(e => e.entryType==='resource').map(r => ({name: r.name, type: r.initiatorType, duration: r.duration})))"
```

## Multi-Step Workflows

### Extract All Links from Multiple Pages
```bash
# 1. Open first page
python3 {{SKILL_DIR}}/scripts/cdp_exec.py open "https://example.com"

# 2. Get tab ID from the output, then extract links
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "Array.from(document.querySelectorAll('a')).map(a => a.href)"

# 3. Navigate to next page
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "window.location.href = 'https://example.com/page2'"

# 4. Extract links again
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "Array.from(document.querySelectorAll('a')).map(a => a.href)"
```

### Scrape with Auto-Pagination
```bash
# Loop: extract → check for next page → click → repeat
while true; do
    # Extract current page content
    python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "...extract..."
    
    # Check for next page button
    HAS_NEXT=$(python3 {{SKILL_DIR}}/scripts/cdp_exec.py pagination <tab_id> | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('paginationButtons',[])))")
    
    if [ "$HAS_NEXT" = "0" ]; then break; fi
    
    # Click next page
    python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --text "Next"
    python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --page-load --timeout 10
done
```

### Take Screenshot of Specific Element
```bash
# Highlight first, then screenshot
python3 {{SKILL_DIR}}/scripts/cdp_exec.py highlight <tab_id> --selector "#target"
python3 {{SKILL_DIR}}/scripts/cdp_exec.py screenshot <tab_id> output.png
```

## Anti-Detection Workflow

### Complete Safe Interaction Pattern
```bash
# 1. Navigate
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "location.href='https://example.com'"
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --page-load --timeout 10

# 2. Analyze page elements
python3 {{SKILL_DIR}}/scripts/cdp_exec.py elements <tab_id> --limit 20

# 3. Interact using CDP native events
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector "button.load-more"

# 4. Wait for new content
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --selector ".new-content" --timeout 5

# 5. Extract data
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "...extract JS..."
```

## Tips and Best Practices

- **Always use `{{SKILL_DIR}}/scripts/cdp_exec.py list` first** to get current tab IDs
- **For async operations**, always add `--await-promise` flag
- **Use `substring(0, N)`** to limit output size and avoid context overflow
- **Test JavaScript snippets manually** in Brave DevTools Console first
- **Use `JSON.stringify()`** when returning complex objects
- **Handle errors gracefully** by checking if elements exist before accessing them
- **For large pages**, consider extracting data in chunks rather than all at once
- **Use `interact` instead of JS `.click()`** for anti-detection sites
- **Use `wait` before extracting** to ensure content is loaded
- **Use `elements` to explore** unknown page structures before targeting specific selectors
- **Use `scroll` for infinite-scroll pages** instead of `window.scrollTo()`

## Site-Specific Patterns

For detailed anti-detection strategies and verified workflows for specific sites (Xiaohongshu, etc.), see [references/site-patterns.md](site-patterns.md).

## Error Recovery

### Retry Failed Operations
```bash
# If first attempt fails, wait and retry
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --page-load --timeout 5
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "document.body.innerText.substring(0, 5000)"
```

### Check if Element Exists Before Interaction
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval <tab_id> "if(document.querySelector('#btn')){document.querySelector('#btn').click();'clicked'}else{'not found'}"
```

### Smart Wait + Click Pattern
```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --selector "#btn" --timeout 5
python3 {{SKILL_DIR}}/scripts/cdp_exec.py interact <tab_id> --selector "#btn"
```
