---
name: automation_browser
description: Control Browser's kernel for web automation. Supports web navigation, element interaction, page scrolling, file/video downloading, and content extraction.
metadata: { "openclaw": { "emoji": "🌍", "developer": "QQ浏览器", "requires": { "bins": ["python3"]} } }
---

# QB X5 Use

Based on the Browser, providing comprehensive browser automation capabilities.

## Installation (one-time only)

Install QQ Browser and the x5use Python package.

```bash
bash skills/qb-x5-use/scripts/install_dep.sh
```

## Setup (run before each session)

Start the X5 background service on port 18009. Must be called after Installation. If the service is already running, it exits immediately without restarting.

```bash
bash skills/qb-x5-use/scripts/setup.sh
```

## Commands

### Navigation
```bash
python3 skills/qb-x5-use/scripts/go_to_url.py <url>    # Navigate to URL
python3 skills/qb-x5-use/scripts/go_back.py             # Go back
```

### Element interaction
```bash
python3 skills/qb-x5-use/scripts/click_element.py <index> [xpath]      # Click element by index
python3 skills/qb-x5-use/scripts/input_text.py <index> <text> [xpath]  # Fill input by index
python3 skills/qb-x5-use/scripts/get_dropdown_options.py <index>       # Get dropdown options
python3 skills/qb-x5-use/scripts/select_dropdown_option.py <index> <text>  # Select dropdown option
```

### Scrolling
```bash
python3 skills/qb-x5-use/scripts/scroll_down.py [amount]       # Scroll down
python3 skills/qb-x5-use/scripts/scroll_up.py [amount]         # Scroll up
python3 skills/qb-x5-use/scripts/scroll_to_text.py <text>      # Scroll to text
python3 skills/qb-x5-use/scripts/scroll_to_top.py              # Scroll to top
python3 skills/qb-x5-use/scripts/scroll_to_bottom.py           # Scroll to bottom
```

### Download
```bash
python3 skills/qb-x5-use/scripts/download_file.py <index>      # Download file by index
python3 skills/qb-x5-use/scripts/download_url.py <url>         # Download file by URL
```

### Content
```bash
python3 skills/qb-x5-use/scripts/get_content.py                # Get page content as Markdown
```

### Wait
```bash
python3 skills/qb-x5-use/scripts/wait.py [seconds]             # Wait specified time
```

## Core workflow

1. **Navigate**: `go_to_url.py <url>`
2. **Read result**: Check the returned interactive elements with refs like `[0]`, `[1]`
3. **Interact**: Use index from the result to click, fill, select, etc.
4. **Re-read result**: After navigation or interaction, check new interactive elements

## Return value

Every command returns the current page state, including action result and interactive elements.

### Structure

**Action Result**
- Success or Failed status
- Target URL and Content-Type

**Page Content**

| Field | Description |
|-------|-------------|
| Previous page | Title and URL of the previous page |
| Action | Action name and parameters |
| Action Result | Execution result (e.g. `navigation triggered`) |
| Current page | Title and URL of the current page |
| Interactive elements | All interactive elements in the viewport, each with `[index]<tag text/>` |

### Example output

Navigating to Baidu:

```bash
python3 skills/qb-x5-use/scripts/go_to_url.py https://www.baidu.com/
```

```
Action result: Success! Navigated to https://www.baidu.com/, The Content-Type of the url in response headers is 'text/html; charset=utf-8'

>>>>> Page Content
State of current webpage. NOTE that the following is one-time information!
[Start of state]
Previous page: 百度一下，你就知道 (https://www.baidu.com/)
Action: go_to_url ({"url":"https://www.baidu.com/"})
Action Result: navigation triggered.
Current page: [0] 百度一下，你就知道 (https://www.baidu.com/)
Interactive elements from top layer of current page inside the viewport: [Start of page]
[0]<a 新闻/>
[1]<a hao123/>
[2]<a 地图/>
[3]<a 贴吧/>
[5]<a 图片/>
[13]<textarea />
[29]<button 百度一下/>
[12]<a tj_login>登录/>
...
[End of page]
[End of state]
```

### Interactive element format

Each element: `[index]<tag text/>`

| Part | Description | Example |
|------|-------------|---------|
| `[index]` | Element index for `click_element`, `input_text`, etc. | `[13]` |
| `<tag>` | HTML element type (`a`, `button`, `textarea`, `div`, `img`, `span`) | `<textarea>` |
| `text` | Display text (may be empty) | `百度一下` |

## Example: Search on Baidu

```bash
# Navigate to Baidu
python3 skills/qb-x5-use/scripts/go_to_url.py https://www.baidu.com/
# Output shows: [13]<textarea />, [29]<button 百度一下/>

# Fill search box
python3 skills/qb-x5-use/scripts/input_text.py 13 "搜索词"

# Click search button
python3 skills/qb-x5-use/scripts/click_element.py 29

# Check result
python3 skills/qb-x5-use/scripts/get_content.py
```

## Example: Scroll and download

```bash
# Navigate to page
python3 skills/qb-x5-use/scripts/go_to_url.py https://example.com/files

# Scroll to find more content
python3 skills/qb-x5-use/scripts/scroll_down.py 500

# Download file by index from interactive elements
python3 skills/qb-x5-use/scripts/download_file.py 5

# Or download by direct URL
python3 skills/qb-x5-use/scripts/download_url.py https://example.com/file.pdf
```

## Troubleshooting
- If an element is not found, use the returned interactive elements list to find the correct index.
- If the page is not fully loaded, add a `wait.py` command after navigation.

