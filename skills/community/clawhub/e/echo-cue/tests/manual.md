# completion-cue · manual verify checklist

Run after `bash apply.sh` says `✓ Patched`.

## 1. Marker in bundle
```bash
grep -c '__milly_cue_v1__' "$(ls $(npm root -g)/openclaw/ui/dist/assets/index-*.js | head -1)"
# expect: 1 or more
```

## 2. Refresh + console marker
- Refresh Control UI tab
- DevTools Console:
  ```js
  window.__milly_cue_v1__   // → true
  ```

## 3. Unlock AudioContext
- Click anywhere on the page once (or press a key).

## 4. Background-tab ding (default behaviour)
- Send a message that triggers a real LLM reply.
- Switch to another browser tab / app **before** the reply finishes.
- Expected: short "ding" when the assistant message lands.

## 5. Foreground stays silent (default)
- Stay on the OpenClaw tab.
- Send a normal question.
- Expected: **no** ding (because `onlyHidden` is on by default).

## 6. NO_REPLY / silent completions
- Trigger a `NO_REPLY` path (heartbeat poke or empty system event).
- Expected: **no** ding.

## 7. Disable + uninstall
```js
localStorage.setItem('milly.completionCue', 'off')
```
- Refresh, repeat step 4. Expected: **no** ding.
- Then:
  ```bash
  bash remove.sh
  ```
- Refresh. Console: `window.__milly_cue_v1__` → `undefined`.

## Bonus: foreground-also mode
```js
localStorage.removeItem('milly.completionCue')
localStorage.setItem('milly.completionCue.onlyHidden', 'off')
```
- Refresh, send a question while staying on tab. Expected: ding.
