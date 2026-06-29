# AutoClaw Browser Automation Skill

## Skill Overview

AutoClaw is a browser automation skill that provides comprehensive control over Chrome browser through MCP (Message Communication Protocol) communication with the browser extension.

## Prerequisites

Before starting MCP service, ensure the following files exist in the correct directory:
- `options.js` - Browser extension options page script
- `background.js` - Extension background script handling WebSocket connections

### File Location
```
%USERPROFILE%\.openclaw\skills\claw-browser\autoclaw-plugin\
```

## 🚀 v6.0.0 New Optimization Tools

### Simplified DOM Retrieval
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_get_indexed_elements` | Get page simplified DOM (indexed interactive elements), data reduced by 90%+ | `[useCache: boolean]` |

### Index Click
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_click_by_index` | Click element by index, more stable than CSS selector | `index: number` |

### Batch Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_batch_execute` | Batch execute multiple CDP commands, reduce network round trips | `commands: array` |

### Smart Wait
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_smart_wait` | Smart wait: support wait for element/text/URL | `element/text/urlPattern, timeout` |

## Available Tools

### ⌨️ Keyboard Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_press_key` | Press single key | `key: string` |
| `claw_press_combo` | Press key combination (e.g., Ctrl+C) | `keys: string` |
| `claw_type_text` | Type text with optional delay | `text: string, [delay: number]` |
| `claw_key_down` | Key down | `key: string` |
| `claw_key_up` | Key up | `key: string` |

### 📸 Screenshot & Content Extraction
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_take_screenshot` | Capture screenshot of current page | `[fullPage: boolean]` |
| `claw_get_page_content` | Get page HTML or text content | `[type: html\|text]` |
| `claw_get_text` | Get text content of element | `selector: string` |
| `claw_get_html` | Get HTML content of element | `selector: string` |
| `claw_get_attribute` | Get element attribute value | `selector, attribute` |
| `claw_is_visible` | Check if element is visible | `selector: string` |
| `claw_is_enabled` | Check if element is enabled | `selector: string` |

### 🖱️ Mouse & Scroll Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_mouse_move` | Move mouse to coordinates | `x, y` |
| `claw_mouse_click` | Left click at coordinates | `[x, y]` |
| `claw_mouse_right_click` | Right click at coordinates | `[x, y]` |
| `claw_mouse_double_click` | Double click at coordinates | `[x, y]` |
| `claw_mouse_down` | Mouse button down | `button, x, y` |
| `claw_mouse_up` | Mouse button up | `[button]` |
| `claw_mouse_wheel` | Mouse wheel scroll | `[deltaX, deltaY]` |
| `claw_scroll` | Scroll page | `[x, y]` |
| `claw_fast_scroll_down` | Fast scroll down one screen | `[speed: number]` |
| `claw_fast_scroll_up` | Fast scroll up one screen | `[speed: number]` |
| `claw_hover_element` | Hover over element | `selector: string` |
| `claw_scroll_to_element` | Scroll element to viewport center | `selector: string` |

### 📱 Touch & Swipe Operations (Mobile)
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_swipe_up` | Swipe up gesture (Douyin/TikTok) | `[distance: number]` |
| `claw_swipe_down` | Swipe down gesture | `[distance: number]` |
| `claw_swipe_left` | Swipe left gesture | `[distance: number]` |
| `claw_swipe_right` | Swipe right gesture | `[distance: number]` |
| `claw_tap` | Tap at specific position | `x, y` |

### 📑 Tab Management
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_tab_create` | Create new browser tab | `[url, active]` |
| `claw_tab_close` | Close browser tab | `[tabId]` |
| `claw_tab_list` | List all open tabs | - |
| `claw_tab_switch` | Switch to specific tab | `tabId: number` |
| `claw_tab_reload` | Reload tab content | `[tabId]` |
| `claw_get_active_tab` | Get active tab information | - |
| `claw_attach_all_tabs` | Attach all tabs for control | - |

### 📁 Bookmark Management
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_get_bookmarks` | Get all bookmarks (flat list) | - |
| `claw_get_bookmark_tree` | Get full bookmark tree structure | - |
| `claw_search_bookmarks` | Search bookmarks by keyword | `query: string` |
| `claw_create_bookmark` | Create new bookmark | `title, url, [parentId]` |
| `claw_update_bookmark` | Update bookmark title or URL | `id, [title, url]` |
| `claw_rename_bookmark` | Rename bookmark or folder | `id, title` |
| `claw_delete_bookmark` | Delete single bookmark | `id: string` |
| `claw_remove_folder` | Recursively delete bookmark folder | `id: string` |
| `claw_create_folder` | Create new bookmark folder | `title, [parentId]` |
| `claw_move_bookmark` | Move bookmark to another folder | `id, parentId` |

### 🍪 Storage & Cookies
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_get_cookies` | Get cookies for domain | `[domain: string]` |
| `claw_set_cookies` | Set cookies | `cookies: array` |
| `claw_get_storage` | Get localStorage/sessionStorage | `[type, origin]` |
| `claw_set_storage` | Set storage value | `type, key, value` |

### 🧪 JavaScript Execution
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_evaluate_js` | Execute JavaScript code in page | `expression: string` |

### ⏳ Wait Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_wait` | Wait specified milliseconds | `ms: number` |
| `claw_wait_for_element` | Wait for element to appear | `selector, [timeout]` |
| `claw_wait_for_text` | Wait for text to appear | `text, [timeout]` |
| `claw_wait_for_url` | Wait for URL pattern match | `urlPattern, [timeout]` |
| `claw_wait_for_navigation` | Wait for navigation completion | `[timeout]` |
| `claw_smart_wait` | Smart wait (NEW) | `element/text/urlPattern, timeout` |

### 🔧 Element Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_click_element` | Click page element (CSS selector) | `selector: string` |
| `claw_fill_input` | Fill input field with text | `selector, text` |
| `claw_clear_input` | Clear input field | `selector: string` |
| `claw_select_option` | Select dropdown option | `selector, value` |
| `claw_check` | Check checkbox | `selector: string` |
| `claw_uncheck` | Uncheck checkbox | `selector: string` |
| `claw_focus_element` | Focus on element | `selector: string` |
| `claw_upload_file` | Upload file to input | `selector, filePath` |

### 🧠 Smart Operations (Enhanced)
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_smart_click` | Smart click: try selector→text→coordinates | `selector/text/x+y, timeout` |
| `claw_find_elements` | Query all matching elements on page | `selector, [limit]` |
| `claw_wait_and_click` | Wait for element then click | `selector, timeout, scrollIntoView` |
| `claw_get_page_structure` | Get page key structure summary | `includeLinks/Buttons/Inputs, maxItems` |
| `claw_batch_extract` | Batch extract multiple selector contents | `selectors, options` |
| `claw_extract_table` | Extract HTML table to JSON | `[selector, includeHeader]` |
| `claw_extract_list` | Extract list-type data | `containerSelector, fields, limit` |

### 📊 Task & Log Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_new_task` | Create new task | `[name: string]` |
| `claw_complete_task` | Complete task | `[success: boolean]` |
| `claw_switch_task` | Switch to specified task | `taskId: number` |
| `claw_list_tasks` | List all tasks | - |
| `claw_get_task_logs` | Get specified task logs | `[taskId, limit]` |
| `claw_get_action_logs` | Get current task action logs | `[limit]` |

### ⚙️ Configuration & Status
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_get_status` | Get current system status | - |
| `claw_get_config` | Get full configuration | - |
| `claw_set_mode` | Set operation mode | `mode: local\|cloud\|auto` |
| `claw_health_check` | Perform health check | - |
| `claw_diagnose` | System diagnostics | `[full: boolean]` |

### 🌐 Navigation Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_navigate` | Open URL | `url, [newTab]` |
| `claw_open_urls` | Batch open multiple URLs | `urls, [delayMs]` |
| `claw_go_back` | Go back one page | - |
| `claw_go_forward` | Go forward one page | - |
| `claw_reload_page` | Reload page | `[hard: boolean]` |

### 💾 Login Session Management
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_save_login_session` | Save current page login state | `name, [domain]` |
| `claw_restore_login_session` | Restore saved login state | `name: string` |
| `claw_list_login_sessions` | List all saved sessions | - |

## Configuration

- **MCP Port**: 30000 (default, customizable)
- **Extension WebSocket**: `ws://127.0.0.1:{port}/extension`
- **Built-in Token**: `autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs`
- **Custom Token**: Supported (leave empty to use built-in)

## Installation Steps

### 1. Start MCP Server
```bash
cd %USERPROFILE%\.openclaw\skills\autoclaw_wboke\mcp
npm install  # First time only
npm start
```

### 2. Install Chrome Extension
1. Open `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `autoclaw-plugin/` directory

### 3. Configure Extension
1. Click extension icon → Settings
2. Set port (default: **30000**)
3. Enter custom Token (optional, leave empty for built-in)
4. Click "Save Settings" to authorize
5. Click "Attach All Tabs"

## v6.0.0 Performance Optimization

| Optimization | Before | After | Effect |
|--------------|--------|-------|--------|
| CDP Domain | Enable all 4 domains each time | Enable only 2 base domains, others on-demand | Resource ↓30% |
| Connection Poll | Check every 5 seconds | Check every 30 seconds | CPU/Network ↓40% |
| Popup Poll | Refresh every 3 seconds | Refresh every 10 seconds | Battery/Resource ↓ |
| DOM Cache | None | Reuse within 15 seconds | Repeat requests ↓50% |

## Project Structure

```
autoclaw_wboke/
├── SKILL.md                    # This documentation
├── README.md                   # Main documentation
├── mcp/                       # MCP Server
│   ├── package.json
│   ├── dist/server.js         # Compiled server (v5.2.0) ⭐
│   └── node_modules/
├── autoclaw-plugin/           # Chrome Extension
│   ├── manifest.json
│   ├── background.js          # Background script (v6.0.0) ⭐
│   ├── popup.js               # Popup UI
│   └── options.js             # Settings UI
└── scripts/                   # Automation script templates
    ├── 抖音点赞.json
    ├── 批量截图.json
    └── 自动搜索.json
```

## Log Management

- **Log Directory**: `~/.autoclaw/logs/`
- **Retention**: 30 days (auto-cleanup on server start)
- **Max Tasks**: 100

## Communication Protocol

- MCP service runs on customizable port (default: 30000)
- Browser extension communicates via WebSocket
- Message format: JSON

## Troubleshooting

### Extension Not Connected
1. Verify MCP server is running
2. Click extension icon → Settings → Test Connection
3. Ensure authorization is not expired

### "No Attached Tab" Error
1. Click "Attach All Tabs" in extension popup
2. Or manually click each tab to attach

### Authorization Expired
1. Click extension icon → Settings
2. Click "Save Settings" to re-authorize

### Performance Issues
- v6.0.0 has optimized resource usage
- Try restarting MCP service if issues persist

## Usage Example

```javascript
// Connect to MCP service
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:30000');

ws.on('open', function() {
    // Navigate to webpage
    ws.send(JSON.stringify({
        action: 'navigate',
        url: 'https://www.example.com'
    }));
    
    // Get simplified DOM (recommended)
    ws.send(JSON.stringify({
        name: 'claw_get_indexed_elements',
        arguments: { useCache: true }
    }));
});
```

## Error Handling

- **Connection Failure**: Check if MCP service is running and port is available
- **Extension Not Loaded**: Verify manifest.json exists and is properly formatted
- **Dependency Errors**: Re-run `npm install` to install dependencies
