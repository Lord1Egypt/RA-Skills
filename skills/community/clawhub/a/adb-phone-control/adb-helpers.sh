#!/usr/bin/env bash
# ADB Phone Control Helper Functions
# Compatible with macOS (BSD) and Linux
# Source this file before using: source adb-helpers.sh

ADB_DUMP_FILE="${ADB_OUTPUT_DIR:-/tmp}/ui_dump.xml"
ADB_SCREEN_FILE="${ADB_OUTPUT_DIR:-/tmp}/adb_screen.png"

# --- Core ---

adb_dump() {
  adb shell uiautomator dump /sdcard/ui_dump.xml 2>/dev/null
  adb pull /sdcard/ui_dump.xml "$ADB_DUMP_FILE" 2>/dev/null
  echo "UI dumped to $ADB_DUMP_FILE"
}

adb_screenshot() {
  adb shell screencap -p /sdcard/adb_screen.png
  adb pull /sdcard/adb_screen.png "$ADB_SCREEN_FILE" 2>/dev/null
  echo "Screenshot saved to $ADB_SCREEN_FILE"
}

adb_observe() {
  adb_dump
  adb_screenshot
}

adb_screen_size() {
  adb shell wm size | sed -n 's/.*: *\([0-9]*x[0-9]*\).*/\1/p'
}

adb_wait() {
  local seconds="${1:-1}"
  sleep "$seconds"
}

# --- Bounds Parsing ---

# Parse bounds string "[x1,y1][x2,y2]" and output center "cx cy"
adb_bounds_center() {
  local bounds="$1"
  local x1 y1 x2 y2
  x1=$(echo "$bounds" | sed 's/\[\([0-9]*\),\([0-9]*\)\]\[\([0-9]*\),\([0-9]*\)\]/\1/')
  y1=$(echo "$bounds" | sed 's/\[\([0-9]*\),\([0-9]*\)\]\[\([0-9]*\),\([0-9]*\)\]/\2/')
  x2=$(echo "$bounds" | sed 's/\[\([0-9]*\),\([0-9]*\)\]\[\([0-9]*\),\([0-9]*\)\]/\3/')
  y2=$(echo "$bounds" | sed 's/\[\([0-9]*\),\([0-9]*\)\]\[\([0-9]*\),\([0-9]*\)\]/\4/')
  echo "$(( (x1 + x2) / 2 )) $(( (y1 + y2) / 2 ))"
}

# --- Element Lookup ---

# Find bounds of element by text attribute (exact match first, then partial)
_adb_find_bounds_by_text() {
  local target="$1"
  adb_dump >/dev/null 2>&1
  local bounds=""
  # Use sed/awk for macOS compatibility instead of grep -P
  # Extract node containing target text, then extract bounds
  bounds=$(sed 's/></>\n</g' "$ADB_DUMP_FILE" \
    | grep "text=\"${target}\"" \
    | head -1 \
    | sed -n 's/.*bounds="\([^"]*\)".*/\1/p')
  if [ -z "$bounds" ]; then
    # Partial match
    bounds=$(sed 's/></>\n</g' "$ADB_DUMP_FILE" \
      | grep "text=\"[^\"]*${target}[^\"]*\"" \
      | head -1 \
      | sed -n 's/.*bounds="\([^"]*\)".*/\1/p')
  fi
  echo "$bounds"
}

# Find bounds of element by resource-id (partial match on id suffix)
_adb_find_bounds_by_id() {
  local target="$1"
  adb_dump >/dev/null 2>&1
  local bounds=""
  bounds=$(sed 's/></>\n</g' "$ADB_DUMP_FILE" \
    | grep "resource-id=\"[^\"]*${target}[^\"]*\"" \
    | head -1 \
    | sed -n 's/.*bounds="\([^"]*\)".*/\1/p')
  echo "$bounds"
}

# Find bounds of element by content-desc attribute
_adb_find_bounds_by_desc() {
  local target="$1"
  adb_dump >/dev/null 2>&1
  local bounds=""
  bounds=$(sed 's/></>\n</g' "$ADB_DUMP_FILE" \
    | grep "content-desc=\"[^\"]*${target}[^\"]*\"" \
    | head -1 \
    | sed -n 's/.*bounds="\([^"]*\)".*/\1/p')
  echo "$bounds"
}

# List all interactive elements (clickable=true) with their text and bounds
adb_list_clickable() {
  adb_dump >/dev/null 2>&1
  sed 's/></>\n</g' "$ADB_DUMP_FILE" \
    | grep 'clickable="true"' \
    | sed -n 's/.*text="\([^"]*\)".*resource-id="\([^"]*\)".*bounds="\([^"]*\)".*/text="\1" id="\2" bounds="\3"/p'
}

# Enhanced: list clickable elements with label resolution and center coordinates
# Resolves labels from text, content-desc, resource-id, or first child text
# Output: index | label | center_x,center_y | bounds
adb_clickable() {
  adb_dump >/dev/null 2>&1
  python3 -c "
import xml.etree.ElementTree as ET, sys

def get_label(node):
    t = node.get('text', '')
    if t: return t
    d = node.get('content-desc', '')
    if d: return d.split(chr(10))[0]  # first line of content-desc
    rid = node.get('resource-id', '')
    if rid: return rid.split('/')[-1]
    # look at children for text
    for child in node.iter():
        if child is node: continue
        ct = child.get('text', '')
        if ct: return '>' + ct
        cd = child.get('content-desc', '')
        if cd: return '>' + cd.split(chr(10))[0]
    return '(unknown)'

def parse_bounds(b):
    import re
    m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', b)
    if not m: return None
    x1,y1,x2,y2 = int(m[1]),int(m[2]),int(m[3]),int(m[4])
    return (x1+x2)//2, (y1+y2)//2, b

tree = ET.parse('$ADB_DUMP_FILE')
idx = 0
for node in tree.iter('node'):
    if node.get('clickable') != 'true': continue
    label = get_label(node)
    bounds = node.get('bounds', '')
    result = parse_bounds(bounds)
    if not result: continue
    cx, cy, raw = result
    print(f'{idx:>2}  {label:<40s}  center=({cx},{cy})  bounds={raw}')
    idx += 1
" 2>/dev/null
}

# JSON version: output clickable elements as JSON array for programmatic use
# Usage: adb_clickable_json          → print to stdout
#        adb_clickable_json file.json → write to file
adb_clickable_json() {
  adb_dump >/dev/null 2>&1
  local output
  output=$(python3 -c "
import xml.etree.ElementTree as ET, re, json

def get_label(node):
    t = node.get('text', '')
    if t: return t
    d = node.get('content-desc', '')
    if d: return d.split(chr(10))[0]
    rid = node.get('resource-id', '')
    if rid: return rid.split('/')[-1]
    for child in node.iter():
        if child is node: continue
        ct = child.get('text', '')
        if ct: return ct
        cd = child.get('content-desc', '')
        if cd: return cd.split(chr(10))[0]
    return ''

tree = ET.parse('$ADB_DUMP_FILE')
items = []
for node in tree.iter('node'):
    if node.get('clickable') != 'true': continue
    b = node.get('bounds', '')
    m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', b)
    if not m: continue
    x1,y1,x2,y2 = int(m[1]),int(m[2]),int(m[3]),int(m[4])
    items.append({
        'index': len(items),
        'label': get_label(node),
        'class': node.get('class',''),
        'id': node.get('resource-id',''),
        'center': [(x1+x2)//2, (y1+y2)//2],
        'bounds': [x1,y1,x2,y2],
        'enabled': node.get('enabled')=='true',
        'long_clickable': node.get('long-clickable')=='true',
    })
print(json.dumps(items, ensure_ascii=False, indent=2))
" 2>/dev/null)

  if [ -n "$1" ]; then
    echo "$output" > "$1"
    echo "Saved ${1} ($(echo "$output" | python3 -c 'import sys,json;print(len(json.load(sys.stdin)))' 2>/dev/null) elements)"
  else
    echo "$output"
  fi
}

# Explore app: recursively click all elements, screenshot each page, build tree
# Usage: adb_explore <package> [depth] [output_dir]
# Output: tree.json (programmatic), tree.md (human readable), screenshots
adb_explore() {
  local package="${1:?Usage: adb_explore <package> [depth] [output_dir]}"
  local depth="${2:-3}"
  local outdir="${3:-${ADB_OUTPUT_DIR:-/tmp}/explore_${package}}"
  local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  python3 "$script_dir/app_explorer.py" "$package" --depth "$depth" --output "$outdir"
}

# --- Tap Actions ---

adb_tap_xy() {
  local x="$1" y="$2"
  adb shell input tap "$x" "$y"
  echo "Tapped ($x, $y)"
}

adb_tap_text() {
  local target="$1"
  local bounds
  bounds=$(_adb_find_bounds_by_text "$target")
  if [ -z "$bounds" ]; then
    echo "ERROR: Element with text '$target' not found"
    return 1
  fi
  local center
  center=$(adb_bounds_center "$bounds")
  local cx cy
  cx=$(echo "$center" | cut -d' ' -f1)
  cy=$(echo "$center" | cut -d' ' -f2)
  adb shell input tap "$cx" "$cy"
  echo "Tapped '$target' at ($cx, $cy) [bounds: $bounds]"
}

adb_tap_id() {
  local target="$1"
  local bounds
  bounds=$(_adb_find_bounds_by_id "$target")
  if [ -z "$bounds" ]; then
    echo "ERROR: Element with id '$target' not found"
    return 1
  fi
  local center
  center=$(adb_bounds_center "$bounds")
  local cx cy
  cx=$(echo "$center" | cut -d' ' -f1)
  cy=$(echo "$center" | cut -d' ' -f2)
  adb shell input tap "$cx" "$cy"
  echo "Tapped id='$target' at ($cx, $cy) [bounds: $bounds]"
}

adb_tap_desc() {
  local target="$1"
  local bounds
  bounds=$(_adb_find_bounds_by_desc "$target")
  if [ -z "$bounds" ]; then
    echo "ERROR: Element with content-desc '$target' not found"
    return 1
  fi
  local center
  center=$(adb_bounds_center "$bounds")
  local cx cy
  cx=$(echo "$center" | cut -d' ' -f1)
  cy=$(echo "$center" | cut -d' ' -f2)
  adb shell input tap "$cx" "$cy"
  echo "Tapped desc='$target' at ($cx, $cy) [bounds: $bounds]"
}

# --- Swipe & Scroll ---

adb_swipe() {
  local x1="$1" y1="$2" x2="$3" y2="$4" duration="${5:-300}"
  adb shell input swipe "$x1" "$y1" "$x2" "$y2" "$duration"
  echo "Swiped ($x1,$y1) -> ($x2,$y2) in ${duration}ms"
}

adb_scroll_down() {
  local size
  size=$(adb_screen_size)
  local w h
  w=$(echo "$size" | cut -dx -f1)
  h=$(echo "$size" | cut -dx -f2)
  local cx=$(( w / 2 ))
  local from_y=$(( h * 3 / 4 ))
  local to_y=$(( h / 4 ))
  adb_swipe "$cx" "$from_y" "$cx" "$to_y" 400
}

adb_scroll_up() {
  local size
  size=$(adb_screen_size)
  local w h
  w=$(echo "$size" | cut -dx -f1)
  h=$(echo "$size" | cut -dx -f2)
  local cx=$(( w / 2 ))
  local from_y=$(( h / 4 ))
  local to_y=$(( h * 3 / 4 ))
  adb_swipe "$cx" "$from_y" "$cx" "$to_y" 400
}

# --- Text Input ---

adb_input_text() {
  local text="$1"
  # Check if ADB Keyboard is available
  local adb_kb
  adb_kb=$(adb shell ime list -s 2>/dev/null | grep -c "adbkeyboard")
  if [ "$adb_kb" -gt 0 ]; then
    # Use ADB Keyboard for full Unicode support
    adb shell am broadcast -a ADB_INPUT_TEXT --es msg "$text" 2>/dev/null
    echo "Typed (ADBKeyboard): $text"
  else
    # Fallback: replace spaces with %s for adb shell input text
    local escaped
    escaped=$(echo "$text" | sed 's/ /%s/g')
    # Check if text contains non-ASCII (CJK etc.) using LC_ALL=C
    if LC_ALL=C grep -q '[^[:print:][:space:]]' <<< "$text" 2>/dev/null; then
      # Use clipboard-based input for CJK
      adb shell "echo '$text' | am broadcast -a clipper.set" 2>/dev/null \
        || adb shell input text "$escaped"
      echo "Typed (clipboard fallback): $text"
    else
      adb shell input text "$escaped"
      echo "Typed: $text"
    fi
  fi
}

# --- Key Events ---

adb_key() {
  local key="$1"
  # Allow both "BACK" and "KEYCODE_BACK" formats
  if [[ "$key" != KEYCODE_* ]]; then
    key="KEYCODE_$key"
  fi
  adb shell input keyevent "$key"
  echo "Key: $key"
}

adb_hide_keyboard() {
  adb shell input keyevent KEYCODE_BACK
  echo "Keyboard dismissed"
}

# --- Long Press ---

adb_long_press() {
  local x="$1" y="$2" duration="${3:-1000}"
  adb shell input swipe "$x" "$y" "$x" "$y" "$duration"
  echo "Long pressed ($x, $y) for ${duration}ms"
}

# --- App Management ---

adb_find_package() {
  local keyword="$1"
  adb shell pm list packages | grep -i "$keyword" | sed 's/package://'
}

adb_launch_app() {
  local package="$1"
  adb shell monkey -p "$package" -c android.intent.category.LAUNCHER 1 2>/dev/null
  echo "Launched: $package"
}

echo "ADB helpers loaded. Use adb_observe to start."
