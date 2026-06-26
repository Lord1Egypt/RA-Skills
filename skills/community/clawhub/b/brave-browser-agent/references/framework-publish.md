# Framework-Aware Click Strategies

For React/Vue/Angular SPA sites where standard CDP mouse events fail.

## Quick Diagnosis

When a click doesn't work, first detect the framework:

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py detect-framework <tab_id>
# Returns: {react: true, overlays: [...], ...}
```

Then deep-analyze the button:

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py analyze-button <tab_id> --selector "button.submit"
# Returns: rect, hit-test results, disabled state, React/Vue props, etc.
```

## Smart Click (Auto-Fallback)

Single command that tries all strategies in order:

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --selector "button.submit"
```

**Strategy order:**
0. **editor_sync** — Auto-sync rich text editors (CKEditor 4/5, Lexical, ProseMirror, Quill, 语雀). **Critical for Vue/React editors where content is not synced to framework state**
1. **hit_test_click** — scrollIntoView + elementFromPoint check + CDP Input.dispatchMouseEvent
2. **react_fiber_click** — Directly invoke React's `onClick` via `__reactProps$`. **Fallback: React 18 root container event delegation** for ByteUI
3. **vue_emit_click** — **Enhanced**: component tree traversal, `$emit`, `$listeners`, setupState handlers, vnode event walk
4. **dispatch_event_click** — Create a native `MouseEvent(isTrusted=true)` + dispatchEvent
5. **enter_key_click** — Focus + Enter key + form submit (for form buttons)
6. **raw_cdp** — Original CDP Input.dispatchMouseEvent fallback

**Publish Validation**: auto-detects success via toast messages, URL changes, modal state, button state after all strategies.

## New Standalone Commands

```bash
# Validate if publish was successful
python3 {{SKILL_DIR}}/scripts/framework_click.py publish-validate <tab_id>

# Sync editor data only (without clicking)
python3 {{SKILL_DIR}}/scripts/framework_click.py editor-sync <tab_id>
```

Returns detailed JSON showing which strategy succeeded and why.

## Per-Platform Click Notes

### 头条号 (React ByteUI)
- Button: `发布` or `预览并发布`
- **Known issues**: Button disabled until form validation passes; check if title/content are filled
- **Strategy**: Click-smart auto-detects React — prefers CDP native events with proper hit-test
- **If fails**: `analyze-button` to check if `.ant-btn[disabled]` class is present
- **Enhanced**: React 18 root delegation + deep fiber traversal (up to 20 levels)
- **Diagnostic**: `onClick called but page doesn't respond` → likely missing editor state sync. Run `editor-sync` first

### 掘金 (Vue 2 + Element UI)
- Button: `确定并发布` in publish modal
- **Known issues**: `pointer-events` set by loading state; button disabled during async operations
- **Strategy**: Vue emit strategy triggers handler directly via `$listeners.click`
- **Enhanced**: Vue 2 `$dispatch`, `$parent` chain traversal, `_events.click` invocation
- **If fails**: Check loading overlay — try `wait --network-idle` first. Modal popup overlay may intercept clicks

### CSDN (Vue 3 + Element Plus + CKEditor iframe)
- Button: `发布文章`
- **Core problem**: CKEditor 5 inside iframe — content synced to editor DOM but NOT to Vue 3 component state
- **Solution**: `editor-sync` fires CKEditor `change:data`, `updateSourceElement`, `forceRender()` + iframe contenteditable input event
- **If fails**: Check if CKEditor instance is on parent window (not inside iframe). Run `analyze-button` on parent window buttons

### 百家号 (Lexical 编辑器)
- Button: `发布文章`
- **Known issues**: Requires封面图 — editor won't let you publish without one
- **Strategy**: Upload image first, then use click-smart
- **Enhanced**: `editor-sync` calls Lexical `update()` + triggers state synchronization

### 腾讯云开发者 (语雀编辑器)
- **Known issues**: `/create` and `/article/create` both 404 — entry point has changed
- **Strategy**: Use `elements` to find the "写文章" entry point dynamically
- **Enhanced**: `editor-sync` triggers lake-editor contenteditable input events

### 阿里云开发者
- **Known issues**: Custom rich text editor (not ProseMirror/Quill)
- **Strategy**: Use `snapshot` + `elements` to map the DOM structure

### Substack
- **Known issues**: Button says "Continue" not "Publish" (UI changed)
- **Strategy**: Use `--text "Continue"` to find the right button, or `elements | grep -i publish`

### 开源中国
- **Known issues**: Page restructured — `u/{id}/blog/write` 404s
- **Strategy**: Navigate to main page, use `elements` to find new blog entry point

### 微信公众号
- **Known issues**: QR code scan required — cannot fully automate
- **Strategy**: Still requires manual intervention for login

## Platform-Specific Click Recipes

### React Sites (General Pattern)
```bash
# 1. Detect React
python3 {{SKILL_DIR}}/scripts/cdp_exec.py detect-framework <tab_id>

# 2. Wait for button to be clickable
python3 {{SKILL_DIR}}/scripts/cdp_exec.py wait <tab_id> --selector "button:not([disabled])"

# 3. Smart click
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --selector "button.submit"
```

### Vue 3 + Element Plus Sites
```bash
# Vue buttons often have .el-button class
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> \
  --selector ".el-button--primary:not(.is-disabled)"
```

### Sites with Modals/Overlays
```bash
# First detect overlays
python3 {{SKILL_DIR}}/scripts/cdp_exec.py detect-framework <tab_id>
# If overlays found, try dismissing them first:
# Look for overlay close buttons
python3 {{SKILL_DIR}}/scripts/cdp_exec.py elements <tab_id> --selector ".modal .close, .modal-close, [aria-label='Close']"
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --selector ".modal-close" --index 0
# Then retry the main click
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --selector "button.submit"
```

## Debugging Failed Clicks

### Step-by-step diagnosis:

```bash
# 1. Check framework
python3 {{SKILL_DIR}}/scripts/cdp_exec.py detect-framework <tab_id>

# 2. Deep analyze the button
python3 {{SKILL_DIR}}/scripts/cdp_exec.py analyze-button <tab_id> --selector "button.submit"

# 3. Check page status
python3 {{SKILL_DIR}}/scripts/cdp_exec.py page-status <tab_id>

# 4. List interactive elements
python3 {{SKILL_DIR}}/scripts/cdp_exec.py elements <tab_id> --limit 10

# 5. Take screenshot
python3 {{SKILL_DIR}}/scripts/cdp_exec.py screenshot <tab_id> debug_before.png

# 6. Try smart click with verbose output
python3 {{SKILL_DIR}}/scripts/cdp_exec.py click-smart <tab_id> --selector "button.submit"

# 7. Take screenshot after
python3 {{SKILL_DIR}}/scripts/cdp_exec.py screenshot <tab_id> debug_after.png
```

## How Framework Detection Works

- **React**: Checks for `__reactFiber$` / `__reactProps$` properties on root elements
- **Vue 3**: Checks for `__vue_app__` on `[data-v-app]` elements
- **Vue 2**: Checks for `__vue__` property on elements
- **Angular**: Checks for `[ng-version]` attribute
- **SPA**: Checks for `[routerlink]` elements

## How React Fiber Click Works

```javascript
// 1. Find element's React props
const propsKey = Object.keys(el).find(k => k.startsWith('__reactProps$'));
const props = el[propsKey];

// 2. Look for onClick handler
if (props.onClick) {
  // 3. Create real MouseEvent and invoke handler directly
  const event = new MouseEvent('click', { bubbles: true, cancelable: true });
  Object.defineProperty(event, 'isTrusted', { value: true });
  props.onClick(event);
}
```

This bypasses React's event delegation entirely and calls the handler directly.
