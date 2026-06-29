# AutoClaw Changelog

## AutoClaw - Browser Automation Enhancement Plugin

**Empower OpenClaw with complete browser control capabilities**

---

## v6.1.0 - 2026-03-15

### ✨ New Features

- **Operation Recording & Playback** - Record and replay user actions on pages
- **Workflow Templates** - Built-in automation templates (Douyin Like, Batch Screenshot, Auto Sign-in, Form Fill)
- **Debug Panel** - Real-time operation logs and error display
- **Element Picker** - Visual click to get element CSS selector
- **Enhanced Retry Mechanism** - Auto-retry failed element operations (up to 3 times)

### 🚀 Performance Optimization

- **CDP Domain On-demand** - No longer enable all domains at once, dynamically enable Network/Input as needed
- **Reduced Polling Frequency** - Connection monitoring changed from 5s to 30s, popup status check from 3s to 10s
- **DOM Caching** - Reuse cached DOM within 15 seconds, reduce duplicate requests
- **Simplified DOM Retrieval** - New `getSimplifiedDOM` method returns indexed interactive elements

### 🎨 UI Improvements

- **New Tab Interface**: Main / Record / Workflows / Debug
- **Redesigned Popup Interface**

### 🔧 Technical Improvements

- **Single Port Mode** - Removed complex dual-port mode
- **Custom Token** - No longer forced to use built-in Token
- **Code Cleanup** - Removed unused variables and legacy code

---

## v6.0.0 - 2026-03-01

### Major Updates

- **Single Port Configuration** - Simplified dual-port mode
- **Custom Token** - Users can configure their own auth token
- **Simplified Settings** - Port and Token directly editable

---

## v5.2.0 - 2026-02-15

### Performance Optimization

- CDP Domain On-demand Management
- DOM Caching Mechanism
- Simplified DOM Retrieval

---

## v5.0.0 - 2026-01-01

### Initial Release

- Basic Browser Control
- Bookmark Management
- CDP Deep Control

---

## Feature Comparison

| Feature | OpenClaw Native | AutoClaw Enhanced |
|---------|-----------------|-------------------|
| Open Webpages | ✅ | ✅ |
| Basic Click | ✅ | ✅ |
| **Bookmark Management** | ❌ | ✅ Full CRUD |
| **Page Screenshot** | ❌ | ✅ |
| **Precise Element Operations** | Limited | ✅ Click/Type/Hover |
| **JavaScript Execution** | ❌ | ✅ Any JS |
| **Cookies/Storage** | ❌ | ✅ Read/Write |
| **Operation Recording** | ❌ | ✅ |
| **Workflow Templates** | ❌ | ✅ |
| **Element Picker** | ❌ | ✅ |

---

## Quick Start

```bash
# 1. Start MCP Server
cd mcp
npm start

# 2. Install Chrome Extension
# chrome://extensions → Load unpacked → Select autoclaw-plugin

# 3. Use in OpenClaw
"Save this page to bookmarks"
"Open Baidu and take screenshot"
"Search bookmarks for Python"
```

---

## Available Tools by Category

### 📁 Bookmark Management (8)
- `claw_get_bookmarks` - Get all bookmarks
- `claw_create_bookmark` - Create bookmark
- `claw_delete_bookmark` - Delete bookmark
- `claw_create_folder` - Create folder
- `claw_move_bookmark` - Move bookmark
- `claw_search_bookmarks` - Search bookmarks
- `claw_get_bookmark_tree` - Get bookmark tree
- `claw_rename_bookmark` - Rename

### 📸 Screenshot & Content (7)
- `claw_take_screenshot` - Capture page
- `claw_get_page_content` - Get page content
- `claw_get_text` - Get element text
- `claw_get_html` - Get element HTML
- `claw_get_attribute` - Get element attribute
- `claw_is_visible` - Check element visible
- `claw_is_enabled` - Check element enabled

### 🖱️ Mouse Operations (12)
- `claw_mouse_click` - Mouse click
- `claw_mouse_right_click` - Right click
- `claw_mouse_double_click` - Double click
- `claw_mouse_move` - Move mouse
- `claw_mouse_wheel` - Mouse wheel
- `claw_scroll` - Page scroll
- `claw_hover_element` - Hover element
- `claw_scroll_to_element` - Scroll to element
- `claw_fast_scroll_down` - Fast scroll down
- `claw_fast_scroll_up` - Fast scroll up
- `claw_swipe_up` - Swipe up (Douyin)
- `claw_swipe_down` - Swipe down

### ⌨️ Keyboard Operations (5)
- `claw_press_key` - Press key
- `claw_press_combo` - Key combo
- `claw_type_text` - Type text
- `claw_key_down` - Key down
- `claw_key_up` - Key up

### 🔧 Element Operations (10)
- `claw_click_element` - Click element
- `claw_fill_input` - Fill input
- `claw_clear_input` - Clear input
- `claw_select_option` - Select option
- `claw_check` - Check
- `claw_uncheck` - Uncheck
- `claw_focus_element` - Focus element
- `claw_upload_file` - Upload file
- `claw_hover_element` - Hover
- `claw_wait_and_click` - Wait and click

### 📑 Tab Management (7)
- `claw_tab_create` - Create tab
- `claw_tab_close` - Close tab
- `claw_tab_list` - List tabs
- `claw_tab_switch` - Switch tab
- `claw_tab_reload` - Reload tab
- `claw_get_active_tab` - Get active tab
- `claw_attach_all_tabs` - Attach all tabs

### 🌐 Navigation (6)
- `claw_navigate` - Open URL
- `claw_open_urls` - Batch open
- `claw_go_back` - Go back
- `claw_go_forward` - Go forward
- `claw_reload_page` - Reload
- `claw_get_current_url` - Get current URL

### ⏳ Wait Operations (6)
- `claw_wait` - Wait milliseconds
- `claw_wait_for_element` - Wait element
- `claw_wait_for_text` - Wait text
- `claw_wait_for_url` - Wait URL
- `claw_wait_for_navigation` - Wait navigation
- `claw_smart_wait` - Smart wait

### 🧪 Advanced (5)
- `claw_evaluate_js` - Execute JavaScript
- `claw_smart_click` - Smart click
- `claw_find_elements` - Find elements
- `claw_batch_extract` - Batch extract
- `claw_extract_table` - Extract table

### 💾 Storage (4)
- `claw_get_cookies` - Get cookies
- `claw_set_cookies` - Set cookies
- `claw_get_storage` - Get storage
- `claw_set_storage` - Set storage

### ⚙️ Config & Status (5)
- `claw_get_status` - Get status
- `claw_get_config` - Get config
- `claw_set_mode` - Set mode
- `claw_health_check` - Health check
- `claw_diagnose` - Diagnose

### 📊 Task Management (6)
- `claw_new_task` - New task
- `claw_complete_task` - Complete task
- `claw_switch_task` - Switch task
- `claw_list_tasks` - List tasks
- `claw_get_task_logs` - Task logs
- `claw_get_action_logs` - Action logs

### ⚡ v6.1.0 New Tools (4)
- `claw_get_indexed_elements` - Simplified DOM
- `claw_click_by_index` - Index click
- `claw_batch_execute` - Batch execute
- `claw_smart_wait` - Smart wait

---

**Total: 100+ Tools**

---

## Technical Support

- MCP Server Port: 30000 (customizable)
- Built-in Token: `autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs`
- GitHub: (To be added)

---

Made with ❤️ for OpenClaw
