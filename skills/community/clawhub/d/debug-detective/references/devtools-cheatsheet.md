# Chrome DevTools Cheatsheet

Keyboard shortcuts and panel reference for efficient debugging.

## Global Shortcuts

| Shortcut | Action |
|----------|--------|
| `F12` / `Ctrl+Shift+I` | Open/close DevTools |
| `Ctrl+Shift+J` | Open Console panel |
| `Ctrl+Shift+C` | Inspect element mode |
| `Ctrl+P` | Open file (Sources panel) |
| `Ctrl+Shift+P` | Command palette |
| `Ctrl+F` | Search in current panel |
| `Ctrl+Shift+F` | Search across all sources |
| `Esc` | Toggle Console drawer |

## Elements Panel

| Shortcut | Action |
|----------|--------|
| `Up/Down` | Navigate DOM tree |
| `Left/Right` | Collapse/expand node |
| `Enter` | Edit attribute |
| `F2` | Edit as HTML |
| `Delete` | Remove element |
| `H` | Toggle visibility (display: none) |
| `Ctrl+Z` | Undo DOM change |

### Useful tricks

- **$0** in Console = currently selected element
- **Right-click node → Break on** → subtree modifications / attribute changes
- **Computed tab** → shows final CSS values and which rule applied
- **Event Listeners tab** → shows all event handlers on the element
- **Force state** → right-click → Force state → :hover, :active, :focus

## Console Panel

| Command | Action |
|---------|--------|
| `$0` | Reference to selected element |
| `$_` | Last evaluated result |
| `$$('selector')` | `document.querySelectorAll` shortcut |
| `$x('xpath')` | XPath query |
| `copy(value)` | Copy to clipboard |
| `clear()` | Clear console |
| `dir(object)` | Interactive object tree |
| `table(array)` | Display as table |
| `monitor(fn)` | Log all calls to function |
| `unmonitor(fn)` | Stop monitoring |
| `monitorEvents(el)` | Log all events on element |
| `getEventListeners(el)` | List event listeners |
| `keys(obj)` / `values(obj)` | Object keys/values |
| `queryObjects(Constructor)` | Find all instances |

### Console API

| Method | Use case |
|--------|----------|
| `console.log()` | General output |
| `console.error()` | Error (red, with stack) |
| `console.warn()` | Warning (yellow) |
| `console.table(data, cols)` | Tabular display |
| `console.group('label')` | Start collapsible group |
| `console.groupEnd()` | End group |
| `console.time('label')` | Start timer |
| `console.timeEnd('label')` | End timer, print elapsed |
| `console.assert(cond, msg)` | Log only if condition fails |
| `console.trace()` | Print stack trace |
| `console.count('label')` | Increment and print counter |

## Sources Panel

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file |
| `Ctrl+G` | Go to line |
| `Ctrl+D` | Select next occurrence |
| `Ctrl+B` | Toggle breakpoint on line |
| `F8` | Resume / pause execution |
| `F10` | Step over |
| `F11` | Step into |
| `Shift+F11` | Step out |
| `Ctrl+'` | Toggle breakpoint enabled/disabled |

### Breakpoint types

| Type | How to set |
|------|-----------|
| Line | Click line number gutter |
| Conditional | Right-click gutter → "Add conditional breakpoint" |
| Logpoint | Right-click gutter → "Add logpoint" (prints to console without pausing) |
| Exception | Click pause icon → "Pause on caught/uncaught exceptions" |
| DOM | Elements panel → right-click element → "Break on" |
| XHR/Fetch | Sources → XHR/fetch Breakpoints → add URL contains |
| Event listener | Sources → Event Listener Breakpoints → expand category |

## Network Panel

| Shortcut | Action |
|----------|--------|
| `Ctrl+E` | Start/stop recording |
| `Ctrl+L` | Clear network log |

### Useful features

- **Filter bar** → type `status-code:500` or `method:POST` or `domain:api.example.com`
- **Throttling** → dropdown to simulate 3G, offline, custom speeds
- **Block request** → right-click → "Block request URL" (test error handling)
- **Copy** → right-click request → "Copy as cURL" / "Copy as fetch"
- **Override response** → right-click → "Override content" (mock APIs locally)

### Timing breakdown

```
DNS Lookup ──→ TCP Connect ──→ TLS Handshake ──→ Request Sent ──→ Waiting (TTFB) ──→ Content Download
```

## Performance Panel

| Shortcut | Action |
|----------|--------|
| `Ctrl+E` | Start/stop recording |
| `Ctrl+Shift+E` | Record + reload page |

### What to look for

| Issue | Where to check |
|-------|---------------|
| Long tasks (>50ms) | Main thread → red triangles |
| Layout thrashing | "Layout" events in flame chart |
| Forced synchronous layout | Purple bars with warning icon |
| Expensive paint | Green bars in "Frames" row |
| JavaScript bottleneck | Wide yellow bars in flame chart → zoom in |
| Idle time | Gray gaps between tasks |

## Memory Panel

### Heap Snapshot workflow

1. Take Snapshot 1 (baseline)
2. Do the suspected leaking action
3. Force GC (trash can icon)
4. Take Snapshot 2
5. Select Snapshot 2 → view: "Comparison" with Snapshot 1
6. Sort by "# Delta" or "Size Delta"

### What to look for

| Problem | How to identify |
|---------|----------------|
| Detached DOM nodes | Filter "Detached" in heap snapshot |
| Growing arrays | Compare snapshots → Array size increases |
| Event listener leaks | `getEventListeners($0)` shows unexpected listeners |
| Closure leaks | Retainer tree shows closure holding large objects |

## Application Panel

| Feature | What it shows |
|---------|--------------|
| Local Storage | Key-value pairs for the domain |
| Session Storage | Session-scoped key-value pairs |
| IndexedDB | Structured database contents |
| Cookies | All cookies with details |
| Service Workers | Registered workers, push subscriptions |
| Cache Storage | Cached resources from Service Worker |
