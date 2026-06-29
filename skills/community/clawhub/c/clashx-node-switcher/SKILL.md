# ClashX Node Switcher

## Overview
Control ClashX VPN client via Peekaboo to switch between proxy nodes, prioritizing US nodes with lowest latency.

## Prerequisites
- Peekaboo installed and permissions granted
- ClashX running as menu bar app

## Key Coordinates (1920x1080)
- ClashX menu bar icon: `(1578, 12)` (found via `peekaboo menubar list`)
- "延迟测速" menu item: Y ~340 from menu top
- "国外流量" proxy group: Y ~65 from menu top

## Workflow

### 1. Open ClashX Menu
```bash
peekaboo click --coords 1578,12
```

### 2. Run Latency Test (Cmd+T)
```bash
peekaboo hotkey --keys "cmd,t" --app ClashX
sleep 3  # Wait for test to complete
```

### 3. Wait for Results Dialog
The dialog shows "延迟测速完成" (Latency test complete). Capture screenshot to see results.

### 4. Dismiss Results and See Node List
```bash
peekaboo press return  # Close dialog
sleep 0.3
peekaboo click --coords 1578,12  # Reopen menu
```

### 5. Expand "国外流量" Submenu
Hover over "国外流量" or its current node to reveal submenu with all nodes:
```bash
peekaboo move 900,65  # Approximate position of 国外流量 row
sleep 0.3
screencapture -x /tmp/clash_nodes.png
```

### 6. Identify US Nodes
US nodes typically have names containing:
- "美国" 
- "US"
- "USA"
- "美西" (US West)
- "美东" (US East)

### 7. Switch to US Node with Lowest Latency
```bash
# Click on the desired US node in the submenu
peekaboo click --coords X,Y  # Coordinates of target US node
```

## Notes
- The menu is a menu bar app (no window), requires specific coordinates
- Submenu appears to the right of the main menu when hovering
- Only one US node (SSR-美国 8 中转) was visible in testing
- Network issues may require trying multiple nodes

## Debugging
```bash
# List menu bar items to find ClashX
peekaboo menubar list

# See full UI elements
peekaboo see --mode screen --screen-index 0

# Capture current screen
screencapture -x /tmp/screen.png
```

## Error Handling
- If menu doesn't open: Try clicking again
- If submenu doesn't appear: Move mouse to trigger hover
- If dialog doesn't dismiss: Try pressing Escape