---
name: 12306-android-adb
description: Book train tickets on the 12306 Android app via USB ADB. Battle-tested 2026-08-30 (two successful bookings: G3314 上海→苏州 and D203 上海松江→杭州南). Primary method: direct uiautomator2 + RapidOCR via ocr_bridge.py, shipped by the appium-android-adb base skill (install it alongside — ClawHub has no dependency resolver). Covers the UC WebView virtual-list traps, the card-expand UI, departure-station filter (一车多站 time disorder), scroll-unsticking, clipboard Chinese input, and 车票信息已过期 (M0013) recovery.
---

# 12306 Train Booking (Android)

12306-specific knowledge, workflows, and pitfalls. The app (com.MobileTicket) uses Alipay Nebula UC WebView for the train list and booking pages, which has unique automation challenges. This doc reflects **two successful end-to-end bookings** on the current app version (2026-08-30, Realme RMX3350 1080x2400).

## 🚨 Setup (proven)

**Requires the `appium-android-adb` base skill.** It ships `ocr_bridge.py` — the OCR loop every
command below runs. ClawHub has no dependency resolver, so it will *not* be installed for you;
install it alongside:

```bash
clawhub install appium-android-adb
```

```bash
# venv (one-time, shared with the other *-android-adb skills). The pins ship
# with the base skill — that is the other reason to install it first.
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
test -f $BASE/ocr_bridge.py || echo "base skill missing — clawhub install appium-android-adb"
python3 -m venv ~/.openclaw/workspace/.venv-adb        # no-op if it already exists
$PY -m pip install -r $BASE/requirements-adb.txt
# App must be installed + logged in. If missing, see "Install & Login".
$PY -c "import uiautomator2 as u2; d=u2.connect(); d.app_start('com.MobileTicket')"
```

**Do NOT use the Appium bridge for 12306 on consumer phones** — Realme etc. block WRITE_SECURE_SETTINGS, so Appium settings/IME fail and the session never starts. Direct uiautomator2 + OCR works (atx-agent needs no special permission). All interaction goes through the OCR loop: `ocr_bridge.py` in the **appium-android-adb base skill** — screenshot → RapidOCR → click/swipe → re-OCR verify.

## ⚠️ Critical: UC WebView Virtual List Behavior

The train list uses a **virtual list** inside the UC WebView:

- Accessibility tree / DOM is mostly **collapsed** (all non-current items share y≈407 or y≈2255, h=6px) and intermittently renders. Never depend on it.
- **OCR is the dependable eye**: RapidOCR reads Chinese out of the box (no tesseract language packs needed).
- Raw `adb shell input tap` is **filtered** by the WebView. `d.click(x, y)` (uiautomator2) reliably delivers touches.
- The list **skips sections** when scrolling: a departure-time window (e.g. 06:32) can be jumped over repeatedly.

## New-App UI: Card Expansion + Per-Row 预订 (2026-08 version)

**Collapsed train cards have NO 预订 button.** The flow is:

1. Tap the **seat row** of a card (e.g. "二等" label area) → the card **expands** in place, showing seat rows: 二等 / 一等 / 商务 / 无座, each with price (e.g. `二等 ¥41 9折`).
2. Each expanded row has its own **预订 button on the right edge** (on 1080px width: x≈898–980, h≈48, at the row's y).
3. Tap that row's 预订 → 确认订单 page.

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
# after OCR shows target train card on screen:
$PY $BASE/ocr_bridge.py tap-text 二等                      # expand the card
$PY $BASE/ocr_bridge.py tap-text 预订 --y0 <row_top> --y1 <row_bottom>  # row's 预订
```

(Example coordinates from the real run: card row at (141, 2026) expanded; 二等 row 预订 at (939, 1987); order page followed.)

## ⚠️ Departure-Station Filter — Do This BEFORE Scrolling (一车多站)

**Without the filter, the list mixes departures from multiple stations and time order breaks.** A train that stops at several departure stations (一车多站, e.g. G7357) appears once per stop-time, all grouped adjacently — so you see 08:10 / 08:35 / 08:52 for the same train number and can't scan by time. Hit this in production (thought "no 08:16 train exists" — there was one).

**Fix: tap the departure-station filter chip at the top of the list first** (chips row, y≈669-708 on 1080x2400; e.g. 上海松江 / 杭州南 / 上海虹桥 / 上海南):

```python
chip = [x for x in t if '松江' in x[0] and x[2] < 600]   # OCR: station name near top
d.click((chip[0][1]+chip[0][3])//2, (chip[0][2]+chip[0][4])//2)
```

After filtering: one row per train, sorted by departure time, target times are findable by simple scrolling.

**⚠️ The filter resets after every re-query** (查询车票) — re-apply the chip each time.

## Booking Flow (proven end-to-end)

### Step 0: Install & Login (only if app missing)

- Download the official APK from the 12306 site (kyfw.12306.cn 下载页), e.g. `curl` the direct link → `adb install -r app.apk`
- The user must log in manually (SMS/face) — automation cannot do this step.

### Step 1: Home Page — Stations & Date

Stations: tap the station field → search box opens. **Chinese input via clipboard** (IME switching is blocked):

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py type 苏州 --x 400 --y 330   # set_clipboard + long-press field
$PY $BASE/ocr_bridge.py dump                        # find 粘贴 in OCR
$PY $BASE/ocr_bridge.py tap-text 粘贴               # paste → results appear
$PY $BASE/ocr_bridge.py tap-text 苏州站              # pick the main station
```

Date: the date picker opens with day cells — OCR the month grid and tap the day cell (e.g. tomorrow's cell right of 今天).

### Step 2: Query & Navigate the Train List

Tap 查询车票. The list loads with earliest departures first.

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py deps        # HH:MM markers at x<250 = which time window is visible
$PY $BASE/ocr_bridge.py swipe up --scale 0.35     # normal forward scroll (≈2 cards)
```

- Track position with `deps` — you always know where you are, DOM or not.
- **Apply the departure-station filter chip FIRST** (see section above) — without it the list is not time-ordered.
- **Filter further if available**: tap 只看高铁/动车 (or 只看高铁) to shorten the list.
- **List keeps skipping the target section**: `$PY $BASE/ocr_bridge.py jump --n 3` (3 rapid scale-0.5 swipes breaks the stuck point), then micro-swipes back: `swipe up --scale 0.25`, `micro down`, or `d.swipe(540, 1900, 540, 800, duration=0.4)`.
- Trains to your destination: match OCR train numbers with regex `^[GDCK]\d+` plus the destination name in the row text (ignore trains to other destinations, e.g. 太仓 when heading to 苏州).

### Step 3: Expand Card & Tap the Row's 预订

- Tap the target card's seat-row label (二等) to expand → verify expansion by OCR (prices ￥41 etc. appear).
- Tap the expanded row's 预订 on the right edge.
- If a quiet-carriage dialog appears (静音车厢 rules) → tap its confirm button (选择/继续).

### Step 4: Select Passenger

- On the 确认订单 page, verify train info + price via OCR markers.
- Tap 选择乘车人 → passenger list appears → `tap-text <name>` (e.g. 张三).
- Verify selection: OCR shows 已选 next to the name.
- Tap 确认 / 完成 (bottom button).

### Step 5: Submit Order & Verify

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py tap-text 提交订单
$PY $BASE/ocr_bridge.py wait-text 订单处理中      # order processing
$PY $BASE/ocr_bridge.py markers                   # look for 快速支付 / 立即支付
```

- `订单处理中` → wait and re-OCR (can take ~20-60s).
- `快速支付` or `立即支付` + countdown at top = **order locked, success**. Report: train, date, route, seat, price, passenger, seat number, countdown.
- **Payment is manual**: the user pays in Alipay/WeChat on the phone (指纹/密码 can't be automated). Typical lock window ≈19 minutes.

### 车票信息已过期 (M0013) — Recovery

If the list data sat too long before submitting, the order page throws **"车票信息已过期(M0013)"**. Detect it by polling markers after 提交订单:

```python
for i in range(8):
    time.sleep(4)
    markers = [x[0] for x in shot() if any(k in x[0] for k in
               ('立即支付','快速支付','订单处理','温馨提示','取消订单','已过期','确定'))]
    if any('已过期' in m or '确定' in m for m in markers): break   # ERROR
    if any('立即支付' in m for m in markers): break                # SUCCESS
```

Recovery (proven):

1. Tap **确定** on the dialog.
2. `d.press('back')` ×2 → home page. (Pull-to-refresh on the list did NOT refresh the data — don't bother.)
3. Tap **查询车票** for a full re-query → fresh list.
4. **Re-apply the departure-station filter chip** (it resets on re-query).
5. Scroll to the train → expand → 预订 → passenger → 提交订单. Fresh data submits without the error.

## Scroll Tactics Cheat Sheet

| Situation | Command |
|-----------|---------|
| Normal advance | `swipe up --scale 0.35` |
| Fine-tune position | `micro up` / `micro down` (scale 0.15) |
| Precise pixel scroll | `d.swipe(540, 1900, 540, 800, duration=0.4)` |
| List stuck / skips target window | `jump --n 3`, then micro back |
| Back up a little | `swipe down --scale 0.3` |

## Decision Tree

```
OCR markers:
  ├─ 查询车票                    → HOME — set stations/date → tap 查询车票
  ├─ 提交订单 / 选择乘车人        → ORDER PAGE — passenger → 提交订单
  ├─ 订单处理中                  → wait, re-OCR
  ├─ 车票信息已过期 / 确定对话框  → EXPIRED — 确定 → back → 查询车票 → re-filter → re-book
  ├─ 快速支付 / 立即支付          → SUCCESS — tell user to pay
  ├─ deps() times + train numbers → TRAIN LIST — scroll/find → expand → 预订
  ├─ 粘贴 menu visible           → after clipboard type, tap 粘贴
  └─ unknown                     → dump full OCR and re-orient
```

## 🛡️ Safety & Consent

- Use only when the user explicitly asks to book a ticket — never speculatively.
- **Confirm before submitting**: show the user the train, date, route, seat,
  price and passenger, and wait for confirmation before tapping 提交订单.
- Payment (立即支付, Alipay/WeChat, password/fingerprint) is ALWAYS done by the
  user on the phone — never automated.
- Screenshots may contain personal data; they are stored in a private 0700 dir
  (`~/.cache/ocr-bridge`) — see appium-android-adb for cleanup.

## Common Pitfalls (all hit in production)

1. **Never trust the DOM** — it collapses and lies. OCR every time.
2. **Raw ADB taps are filtered** by UC WebView — always `d.click`.
3. **Appium is dead on Realme** (WRITE_SECURE_SETTINGS blocked) — don't waste time on it.
4. **IME switching blocked** — Chinese input = `set_clipboard` + long-press 粘贴.
5. **The list skips departure windows** — `jump` past the stuck point, then micro-scroll.
6. **Clicking 二等 toggles the card** — if it collapsed again, re-expand and click the row's right-edge 预订, not the label.
7. **Screen auto-lock** — `adb shell svc power stayon true`.
8. **一车多站 mixes the time order** — same train number appears at multiple departure times (one per 发站), grouped adjacently. Always apply the departure-station filter chip before scanning for a time.
9. **Stale list → 车票信息已过期(M0013)** — list data expires while you sit on it. Recovery: 确定 → back → full re-query → **re-apply station filter** → re-book. Pull-to-refresh does NOT refresh the data.
10. **The station filter resets on re-query** — re-apply the chip every time after 查询车票.
11. **OCR misreads** — filter by region (x/y bounds), re-shoot after animations (sleep 2-3s).
12. **Train numbers**: OCR gives `G3314` (no spaces); DOM gives `G 3 3 1 4`. Regex on OCR text.
13. **USB/ADB can drop mid-session** — app state (filter + scroll position) survives; ask the user to replug, then continue where you left off.
