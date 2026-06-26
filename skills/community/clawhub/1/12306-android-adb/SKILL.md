---
name: 12306-android-adb
description: 12306-specific knowledge for booking train tickets via the Android app. Covers UC WebView virtual list behavior, proven booking flow, and common pitfalls. Uses appium-android-adb bridge OR direct uiautomator2 for all interaction.
---

# 12306 Train Booking (Android)

12306-specific knowledge, workflows, and pitfalls. The app uses Alipay Nebula UC WebView for the train list and booking pages, which has unique automation challenges.

## 🚨 Before Any 12306 Action

Ensure the app is running and on the correct page:

```bash
# Start Appium bridge (if using bridge_daemon.py approach):
bash ~/.openclaw/workspace/skills/appium-android-adb/start_bridge.sh

# Or use uiautomator2 directly (more reliable for WebView):
python3 -c "import uiautomator2 as u2; d = u2.connect(); d.app_start('com.MobileTicket')"
```

## ⚠️ Critical: UC WebView Virtual List Behavior

The train list uses a **virtual list** inside the UC WebView. This has extreme implications:

### What DOES work
| Method | Target | Reliability |
|--------|--------|-------------|
| `uiautomator2 text('预订').click()` | "预订" book buttons | ✅ Always works (proper persistent bounds) |
| `uiautomator2 text('查询车票').click()` | Native query button | ✅ Always works |
| `uiautomator2 text('选择乘车人').click()` | Native passenger selector | ✅ Always works |
| `uiautomator2.click(x, y)` on native views | Date tabs, bottom buttons | ✅ Always works |
| Screenshot + OCR + ADB tap | Any visible element | ✅ Works with good OCR |
| `Appium element.click()` on "预订" buttons | "预订" with proper bounds | ✅ Works |

### What DOES NOT work
| Method | Target | Why |
|--------|--------|-----|
| Clicking collapsed train name text | Train entry at y=407 or y=2255 (h=6) | Virtual list collapses ALL non-current items |
| ADB `input tap` | Any UC WebView content | UC WebView filters synthetic touch events |
| W3C Actions swipe | UC WebView scroll | Touch events filtered |
| `mobile: scrollGesture` | UC WebView element | Returns False consistently |
| `d.textContains('G 7 0 0 4').click()` | Train name in collapsed zone | Multiple trains share collapsed bounds |
| `tap_bounds` on collapsed element | Train name at y=2255 with h=6 | Event goes to WebView's virtual position, not visual |

### Key Insight: "预订" Buttons Have Proper Bounds

The ONLY reliable click targets in the UC WebView train list are the **"预订" action buttons**. Unlike the text content (train name, times, seat info) which gets collapsed by the virtual list, the "预订" button is:
- Always rendered with proper bounds (h=87px)
- Clickable via accessibility service
- Positioned consistently ~195px below each train card's top
- Unique per train card (find the one nearest your target train's y-position)

## Booking Flow

### Step 1: Home Page — Search Trains

```
dump the page → check for "查询车票" button
If on MainActivity:
  → tap "查询车票" (native button, always works)
  → wait for train list to load (H5Activity appears)
If on H5Activity (already on train list):
  → proceed to Step 2
```

### Step 2: Find Target Train's "预订" Button

**DO NOT try to click the train name or text content.** Instead:

1. **Scroll** the list until you see trains near your target departure time:
   ```python
   d.swipe_ext('up', scale=0.3)   # scroll forward
   d.swipe_ext('down', scale=0.3)  # scroll backward
   ```

2. **Check for G7004 in the DOM** (even collapsed):
   ```python
   xml = d.dump_hierarchy()
   if 'G 7 0 0 4' in xml:
       # G7004 is in the list — look for its "预订" button
       pass
   ```

3. **Find the "预订" button** associated with your train. "预订" buttons appear at regular y-intervals (~315px apart). The one closest to your target train's y-position belongs to that train:
   ```python
   # Get all "预订" buttons with positions
   buttons = d(text='预订')
   for btn in buttons:
       pos = btn.info['bounds']
       y_center = (pos['top'] + pos['bottom']) // 2
       print(f"预订 at y={y_center}")

   # G7004 at y=1793 → the "预订" at y=1988 is its book button
   ```

4. **Click "预订":**
   ```python
   d(text='预订').click()          # clicks first one
   # OR click specific one by position:
   for btn in d(text='预订'):
       if 1900 < btn.info['bounds']['top'] < 2100:
           btn.click()
           break
   ```

### Step 2b: OCR-Based Fallback (if DOM is unreliable)

If the WebView's DOM is too collapsed to find the right "预订":

```python
import subprocess, pytesseract
from PIL import Image

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/screen.png'], timeout=10)
subprocess.run(['adb', 'pull', '/sdcard/screen.png', '/tmp/screen.png'], timeout=10)

# OCR to find departure time
data = pytesseract.image_to_data(Image.open('/tmp/screen.png'),
    lang='chi_sim+eng', output_type=pytesseract.Output.DICT, config='--psm 6')

# Find "08:00" departure text on LEFT side (x < 300)
for i in range(len(data['text'])):
    if '08:00' in data['text'][i] and int(data['left'][i]) < 300:
        y = data['top'][i]
        # Tap "预订" position (~195px below departure time)
        import subprocess
        subprocess.run(['adb', 'shell', 'input', 'tap', '939', str(y + 195)])
        break
```

### Step 3: Quiet Carriage Dialog (if appears)

After clicking "预订", a dialog may appear:
- "选择该车次二等座可能候补到静音车厢席位，是否继续选择？" → tap "继续" or "选择"
- "温馨提示" with quiet carriage rules → tap "选择" (bottom-right button)

Use OCR to find the confirm button position, then ADB tap it.

### Step 4: Select Passenger

```
On order page, verify:
  → G7004 train info displayed
  → 二等座 selected (default)
  → Price ¥41 shown

If no passenger selected:
  → tap "选择乘车人" (native, works)
  → tap passenger name (e.g. "熊子慧")
  → tap "确认" (bottom button)
```

### Step 5: Submit Order

```
tap "提交订单" button
  → verify: order submission confirmation
  → if "温馨提示" with "车票信息已过期" → go back, re-search
  → if "立即支付" → proceed to payment
```

### Step 6: Payment (manual)

```
"立即支付" or "去支付" appears → user handles Alipay/WeChat
```

## Train List Navigation (Scrolling)

The UC WebView's virtual list has three zones:
- **Top collapsed** (y=407, h=6): Items scrolled past the top
- **Proper viewport** (y=500-2200, h=60-130): Currently visible items with real bounds
- **Bottom collapsed** (y=2255, h=6): Items below the viewport

Each scroll (scale=0.3) advances the list by approximately 2 train cards (~30-60 min of departures). To reach a specific train:
1. Start from the earliest visible time
2. Calculate approximate scrolls needed: `(target_hour - current_hour) * 60 / 15` (each scroll ≈ 15 min of departures)
3. Scroll, then check for target text in DOM (even collapsed)
4. Once target text appears in DOM, look for its "预订" button

## Decision Tree

```
dump / check current page:
  ├─ package != "com.MobileTicket"
  │   → app not running, start it
  ├─ ".ui.activity.MainActivity" in activity
  │   → HOME PAGE
  │   → verify stations are set → tap "查询车票"
  ├─ "H5Activity" in activity
  │   ├─ "提交订单" in text → ORDER CONFIRMATION
  │   │   → select passenger if needed → submit
  │   ├─ "预订" in text → TRAIN LIST (with "预订" buttons)
  │   │   → find target train → click its "预订" button
  │   ├─ "次列车" in text → TRAIN LIST (loading)
  │   │   → scroll until target appears → find "预订"
  │   └─ "立即支付" in text → PAYMENT
  │       → user handles payment
  └─ anything else → not 12306, investigate
```

## Common Pitfalls

1. **NEVER click collapsed train names** — they all share the same y=407 or y=2255 bounds. Click the "预订" button instead.
2. **"预订" buttons have proper bounds** — they're the only reliable WebView targets.
3. **Screen may auto-lock** — keep device awake: `adb shell svc power stayon true`
4. **Session conflicts** — Appium and uiautomator2 can't run simultaneously (both need AccessibilityService).
5. **Page may time out** — if no action for ~5 min, the list might need re-querying.
6. **Date tabs are native** — tapping "05月31日 周日" at bounds [189,257][312,383] always works.
7. **Train numbers have spaces** — search for `G 7 0 0 4` not `G7004`.
