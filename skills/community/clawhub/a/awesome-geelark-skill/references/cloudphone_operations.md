# ADB Operations Guide

Complete guide to operating cloud phones using ADB and uiautomator2.

---

## Overview

After booting a cloud phone and enabling ADB, you can operate the device using ADB commands. Since this skill is designed for AI agents that need to recognize the current screen state, the recommended workflow is:

1. **Identify UI Structure**: Use `uiautomator2` to dump the current page hierarchy (`dump_hierarchy()`), enabling the agent to understand the screen layout.
2. **Prioritize uiautomator2 Operations**: If elements can be identified and interacted with via the UI hierarchy, use `uiautomator2` for clicks, inputs, and swipes.
3. **Fallback to ADB Screenshots**: If elements cannot be recognized or operated via `uiautomator2`, use ADB screenshots to visually confirm the state and perform coordinate-based operations.

Tools available:
- **ADB commands** - Screenshots, key events, coordinate-based tap/swipe
- **uiautomator2** - UI hierarchy extraction, element-based interactions

---

## Prerequisites

### 1. Install Dependencies

```bash
pip install uiautomator2 --break-system-packages
```

### 2. Boot Cloud Phone and Enable ADB

```python
from scripts.geelark_boot_helper import boot_and_connect

# Boot and get ADB connection info
adb_info = boot_and_connect("phone_id", "your_token")

if adb_info:
    print(f"ADB: {adb_info['ip']}:{adb_info['port']}, PWD: {adb_info['pwd']}")
else:
    print("❌ Failed to boot cloud phone")
    exit(1)
```

---

## ADB Connection

### Connect to Device

```python
import uiautomator2 as u2

# Connect using ADB info
d = u2.connect(f"{adb_info['ip']}:{adb_info['port']}")

print(f"✅ Connected to device")
```

### ⚠️ Authenticate with glogin (MUST DO IMMEDIATELY)

**Critical**: GeeLark requires `glogin` authentication **immediately after connection** before any ADB operations.

```python
import subprocess

# Authenticate using ADB password (must be done right after connecting)
r = subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'glogin', adb_info['pwd']
], capture_output=True, text=True)

if r.returncode == 0:
    print("✅ glogin successful - you can now perform operations")
else:
    print(f"❌ glogin failed: {r.stderr}")
    print(f"   stdout: {r.stdout}")
    exit(1)
```

**⚠️ Important**:
- Must be executed **immediately** after `u2.connect()`
- Without glogin, most ADB operations will fail or hang
- If connection drops, you need to re-authenticate

### Disconnect

```python
import subprocess

subprocess.run([
    'adb', 'disconnect', f"{adb_info['ip']}:{adb_info['port']}"
])
```

---

## Basic ADB Commands

### Tap (Click)

```python
import subprocess

subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'input', 'tap', '500', '1000'
])
```

### Input Text

```python
import subprocess

# ⚠️ Note: ADB input text does NOT support spaces or special characters
# For simple text without spaces:
subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'input', 'text', 'helloworld'
])

# For text with spaces/special characters, use uiautomator2 instead:
# d(text="Username").set_text("hello world")
# See uiautomator2 Operations → Input Text section below
```

### Swipe

```python
import subprocess

subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'input', 'swipe', '500', '1000', '500', '500'
])
```

### Key Events

```python
import subprocess

# Press Back button
subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'input', 'keyevent', '4'
])

# Press Home button
subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'input', 'keyevent', '3'
])

# Press Recent Apps button
subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'input', 'keyevent', '187'
])
```

**Common Key Codes**:
- `3` - Home
- `4` - Back
- `26` - Power
- `66` - Enter
- `67` - Delete (Backspace)
- `187` - Recent Apps
- `224` - Volume Up
- `225` - Volume Down

---

## uiautomator2 Operations

### Get UI Hierarchy

```python
# Get entire UI hierarchy as XML
xml = d.dump_hierarchy()

print(f"UI nodes: {xml.count('<node')}")

# Save to file
with open('/tmp/ui_hierarchy.xml', 'w') as f:
    f.write(xml)
```

### Find Element by Text

```python
# Find element with specific text
element = d(text="Submit")

if element.exists:
    print("✅ Found element")
else:
    print("❌ Element not found")
```

### Find Element by ID

```python
# Find element by resource ID
element = d(resourceId="com.android.settings:id/search")

if element.exists:
    print("✅ Found element")
else:
    print("❌ Element not found")
```

### Find Element by Content Description

```python
# Find element by content-desc
element = d(contentDesc="Navigate up")

if element.exists:
    print("✅ Found element")
else:
    print("❌ Element not found")
```

---

## UI Actions

### Click Element

```python
# Click element by text
d(text="Submit").click()

# Click element by ID
d(resourceId="com.android.settings:id/search").click()

# Click at specific coordinates
d.click(500, 1000)
```

### Long Press

```python
# Long press element
d(text="Item").long_click(duration=2)
```

### Input Text

```python
# Input text into field (recommended)
d(text="Username").set_text("my_username")

# Input text with special characters/spaces
d(resourceId="com.app:id/edit_text").set_text("hello world @123")

# Clear and input
element = d(text="Password")
element.clear_text()
element.set_text("my_secure_password")
```

**Note**: ADB `input text` command does NOT support spaces or special characters. Use uiautomator2 `set_text()` for complex text.
```

### Clear Text

```python
# Clear text field
d(text="Username").clear_text()
```

### Swipe

```python
# Swipe from bottom to top
d.swipe(500, 1000, 500, 500)

# Swipe from top to bottom
d.swipe(500, 500, 500, 1000)

# Swipe with steps (more precise)
d.swipe(500, 1000, 500, 500, steps=10)
```

### Scroll

```python
# Scroll down
d(scrollable=True).scroll.toEnd()

# Scroll up
d(scrollable=True).scroll.toBeginning()

# Scroll to specific text
d(scrollable=True).scroll.to(text="Target Text")
```

### Wait for Element

```python
# Wait up to 10 seconds for element
element = d(text="Submit").wait(timeout=10)

if element:
    print("✅ Element appeared")
else:
    print("❌ Element not found")
```

---

## Screenshot

### Take Screenshot with uiautomator2

```python
# Take screenshot
screenshot = d.screenshot()

# Save to file
screenshot.save("/tmp/screenshot.png")

# Or save directly
d.screenshot("/tmp/screenshot.png")
```

### Take Screenshot with ADB

```python
import subprocess

# Take screenshot on device
subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'screencap', '-p', '/sdcard/screenshot.png'
], capture_output=True)

# Pull to local
subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'pull', '/sdcard/screenshot.png', '/tmp/screenshot.png'
], capture_output=True)
```

---

## State-Aware Operations ⭐⭐⭐

**Core Principle**: Every operation should be: Get state → Act → Verify state.

### Get Page State Before Operation

```python
def get_page_structure(device):
    """Get current page structure"""
    return device.dump_hierarchy()

def find_element_coords(device, target_text):
    """Find element and get its coordinates"""
    xml = device.dump_hierarchy()
    element = device(text=target_text)

    if element.exists:
        bounds = element.info['bounds']
        center_x = (bounds['left'] + bounds['right']) // 2
        center_y = (bounds['top'] + bounds['bottom']) // 2
        return center_x, center_y
    return None
```

### Execute Operation

```python
def click_element(device, target_text):
    """Click element by text"""
    # 1. Get element coordinates
    coords = find_element_coords(device, target_text)

    if coords:
        # 2. Click at coordinates
        x, y = coords
        device.click(x, y)
        print(f"✅ Clicked: {target_text} ({x}, {y})")
        return True
    else:
        print(f"❌ Element not found: {target_text}")
        return False
```

### Verify Result

```python
def verify_element_appeared(device, target_text):
    """Verify element appeared after operation"""
    xml = device.dump_hierarchy()
    return target_text in xml

def verify_element_disappeared(device, target_text):
    """Verify element disappeared after operation"""
    xml = device.dump_hierarchy()
    return target_text not in xml
```

### Complete Example

```python
def click_and_verify(device, button_text, verify_text=None):
    """Click button and verify result"""
    # 1. 获取操作前状态（用于后续对比验证）
    # Note: dump_hierarchy() may take 1-3 seconds on complex UIs
    xml_before = device.dump_hierarchy()

    # 2. Check if button exists
    if button_text not in xml_before:
        print(f"❌ Button not found: {button_text}")
        return False

    # 3. Click button
    if not click_element(device, button_text):
        return False

    # 4. 获取操作后状态（验证是否达到预期）
    xml_after = device.dump_hierarchy()

    # 5. Verify result
    if verify_text:
        if verify_text in xml_after:
            print(f"✅ Verified: {verify_text}")
            return True
        else:
            print(f"❌ Verification failed: {verify_text}")
            return False
    else:
        print("✅ Operation completed (no verification)")
        return True

# Usage
success = click_and_verify(d, "Submit", "Success")
```

**Performance Note**: `dump_hierarchy()` can take 1-3 seconds on complex UIs. For frequent operations, consider:
- Caching XML when multiple checks are needed
- Using element selectors instead of string matching when possible
- Reducing verification steps for non-critical operations

---

## Common Patterns

### Fill Form and Submit

```python
def fill_and_submit_form(device, form_data):
    """Fill form and submit"""
    # 1. Get initial state
    xml_start = device.dump_hierarchy()

    # 2. Fill each field
    for field_label, input_value in form_data.items():
        # Check if field exists
        if field_label not in xml_start:
            print(f"❌ Field not found: {field_label}")
            return False

        # Find element and input text with error handling
        try:
            element = device(text=field_label)
            if not element.exists:
                print(f"❌ Element not found: {field_label}")
                return False
            
            element.set_text(input_value)
        except Exception as e:
            print(f"❌ Failed to input {field_label}: {e}")
            return False

        # Verify input (refresh XML)
        xml_after = device.dump_hierarchy()
        if input_value not in xml_after:
            print(f"❌ Input failed: {input_value}")
            return False

    # 3. Submit form
    success = click_and_verify(device, "Submit", "Success")

    return success

# Usage
form_data = {
    "Username": "my_username",
    "Password": "my_password",
    "Email": "test@example.com"
}

fill_and_submit_form(d, form_data)
```

### Navigate to Page

```python
def navigate_to_page(device, target_page_text, nav_strategy=None):
    """Navigate to specific page
    
    Args:
        device: uiautomator2 device instance
        target_page_text: Text that appears on target page
        nav_strategy: List of button texts to try in order (customizable)
                     Default: ["Menu", "Back", "Home"]
    """
    if nav_strategy is None:
        nav_strategy = ["Menu", "Back", "Home"]
    
    max_attempts = 3

    for attempt in range(max_attempts):
        # 1. Get current state
        xml = device.dump_hierarchy()

        # 2. Check if already on target page
        if target_page_text in xml:
            print(f"✅ Already on page: {target_page_text}")
            return True

        # 3. Find navigation element from strategy
        nav_element = None
        for btn in nav_strategy:
            if btn in xml:
                nav_element = btn
                break

        if not nav_element:
            print(f"❌ No navigation element found (attempt {attempt + 1}/{max_attempts})")
            return False

        # 4. Click navigation
        if not click_element(device, nav_element):
            print(f"❌ Click failed: {nav_element} (attempt {attempt + 1}/{max_attempts})")
            return False

        # 5. Verify navigation
        xml_after = device.dump_hierarchy()
        if target_page_text in xml_after:
            print(f"✅ Navigated to: {target_page_text} (attempt {attempt + 1}/{max_attempts})")
            return True

    print(f"❌ Navigation failed: {target_page_text}")
    return False

# Usage - with default strategy
navigate_to_page(d, "Settings")

# Usage - with custom strategy for specific app
navigate_to_page(d, "Profile", nav_strategy=["Navigation Drawer", "Back", "Home"])
```

**Note**: Navigation strategy should be customized based on the target application's UI structure.

### Handle Dialogs/Popups

```python
def handle_dialog(device, cancel_button_text="Cancel", timeout=3):
    """Handle unexpected dialogs or popups"""
    try:
        # Wait briefly for dialog to appear
        cancel_btn = device(text=cancel_button_text)
        if cancel_btn.wait(timeout=timeout):
            cancel_btn.click()
            print(f"✅ Closed dialog: {cancel_button_text}")
            return True
    except Exception as e:
        print(f"ℹ️ No dialog found or already closed: {e}")
    return False

def handle_permission_dialog(device):
    """Handle Android permission request dialogs"""
    # Common permission buttons
    allow_buttons = ["Allow", "ALLOW", "允许", "While using the app"]
    
    for btn_text in allow_buttons:
        element = device(text=btn_text)
        if element.exists:
            element.click()
            print(f"✅ Granted permission: {btn_text}")
            return True
    
    return False

# Usage - call before critical operations
handle_dialog(d, "Cancel")
handle_permission_dialog(d)
```

---

## Debug Mode

### Enable Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uiautomator2").setLevel(logging.DEBUG)

# Enable device debug
d = u2.connect(f"{adb_info['ip']}:{adb_info['port']}")
d.debug = True  # See HTTP request/response details
```

### Extend Timeout

```python
import uiautomator2 as u2

# Extend timeout for unstable connections
u2.HTTP_TIMEOUT = 120  # 120 seconds
```

---

## Common Issues

### ADB Connection Timeout

**Problem**: Connection times out or unstable.

**Solution**:
```python
import uiautomator2 as u2

# Extend timeout
u2.HTTP_TIMEOUT = 120

# Enable debug mode
d = u2.connect(f"{adb_info['ip']}:{adb_info['port']}")
d.debug = True
```

### Element Not Found

**Problem**: Element exists but `d(text="xxx")` doesn't find it.

**Solution**:
```python
# Try different selectors
d(text="Submit").click()  # By text
d(resourceId="com.app:id/button").click()  # By ID
d(contentDesc="Submit button").click()  # By content-desc

# Or use XPath (requires uiautomator2 XPath extension)
# Install: pip install uiautomator2[xpath] --break-system-packages
d.xpath('//android.widget.TextView[@text="Submit"]').click()
```

### glogin Failed

**Problem**: glogin authentication fails.

**Solution**:
```python
# Ensure you're using the correct password
r = subprocess.run([
    'adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
    'shell', 'glogin', adb_info['pwd']
], capture_output=True, text=True)

if r.returncode != 0:
    print(f"❌ glogin failed: {r.stderr}")
    print(f" stdout: {r.stdout}")
```

---

## Best Practices

### 1. Always Authenticate with glogin

```python
# Authenticate before any operation
r = subprocess.run(['adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
                   'shell', 'glogin', adb_info['pwd']], capture_output=True, text=True)

if r.returncode != 0:
    print("❌ glogin failed")
    exit(1)
```

### 2. Use State-Aware Operations

```python
# Get state → Act → Verify state
xml_before = device.dump_hierarchy()

# Check if element exists
if "Submit" not in xml_before:
    return False

# Perform action
device(text="Submit").click()

# Verify result
xml_after = device.dump_hierarchy()
if "Success" in xml_after:
    print("✅ Success")
```

### 3. Log All Operations

```python
from scripts.cloudphone_logger import CloudPhoneLogger

with CloudPhoneLogger("task_name", phone_id) as log:
    log.step("UI", "click", "text='Submit'")
    device(text="Submit").click()
    log.screenshot("/tmp/screen.png", 12345)
```

### 4. Handle Errors Gracefully

```python
try:
    device(text="Submit").click()
except Exception as e:
    print(f"❌ Click failed: {e}")
    # Handle error
```

---

## Last Updated

2026-04-25

**Related Documents**:
- [Best Practices](best_practices.md) - Safety and performance tips
- [Error Codes](error_codes.md) - Error handling guide