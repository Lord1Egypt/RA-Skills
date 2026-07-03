# BlogStudio — Todo List

## ✅ Completed (2026-06-15)

### 1.1: Fix Publish path ✅
**File:** `electron/renderer/app.js`
**Issue:** `publishPost()` used `content/` path instead of `_posts/`
**Fix:** Changed to `_posts/${filename}`

### 1.2: Fix Edit Existing Post ✅
**File:** `electron/renderer/app.js`
**Issue:** Title/date/tags not populated when clicking a post
**Fix:** `parseFrontMatter()` extracts all fields, populates form on card click

### 1.3: Fix Cancel Edit ✅
**File:** `electron/renderer/app.js`
**Issue:** Cancel button had no handler
**Fix:** Added `cancelEdit()` that hides editor, shows list, clears currentPost

### 1.4: Fix Sync ✅
**File:** `electron/renderer/app.js`
**Issue:** Sync showed success immediately without waiting
**Fix:** `await loadContent(currentView)` — properly awaits before showing success

### 1.5: Fix Save Draft path ✅
**File:** `electron/renderer/app.js`
**Issue:** Save draft used `content/` path
**Fix:** Changed to `_posts/${filename}`

### 2.2: Add Delete Post ✅
**File:** `electron/main.js`, `electron/preload.js`, `electron/renderer/app.js`, `electron/renderer/index.html`
**Fix:** Added `githubDelete` handler in main.js, exposed in preload, added delete button (shows for existing posts only), `deletePost()` function

### 2.3: Add Markdown Preview ✅
**File:** `electron/renderer/app.js`, `electron/renderer/index.html`
**Fix:** `togglePreview()` creates full-screen overlay with rendered HTML. Live preview as you type (300ms debounce). Preview button shows/hides.

### 2.4: Fix View Switching ✅
**File:** `electron/renderer/app.js`
**Fix:** `currentView` state set on nav click, passed to `loadContent()`, filter applied

### 3.1: Populate Date Field When Editing ✅
**File:** `electron/renderer/app.js`
**Fix:** `postDate.value = meta.date` set in card click handler

### 3.2: Populate Tags Field When Editing ✅
**File:** `electron/renderer/app.js`
**Fix:** `postTags.value = meta.tags` set in card click handler

### 3.3: Add Keyboard Shortcuts ✅
**File:** `electron/renderer/app.js`
**Fix:** Ctrl+S = save draft, Ctrl+P = publish, Esc = cancel edit

### 3.4: Add GitHub Link to Post ✅
**File:** `electron/renderer/app.js`, `electron/renderer/index.html`
**Fix:** "View on GitHub" button appears when editing existing post, opens GitHub file URL

### 3.5: Status Messages ✅
**File:** `electron/renderer/app.js`
**Fix:** Status shown on: save, publish, sync, delete, errors

### New Post Button ✅
**File:** `electron/renderer/index.html`, `electron/renderer/app.js`
**Fix:** Added "New Post" button in main header, newPostBtn event listener

## Testing
- [x] Load BlogStudio — posts list appears ✅
- [x] Click post → editor opens with correct title/date/tags/content ✅
- [x] Edit title → changes reflected in preview ✅
- [x] Save Draft → saved to GitHub ✅
- [x] Publish → published to GitHub Pages (SHA returned) ✅
- [x] Cancel → returns to list ✅
- [x] Delete → post removed from GitHub ✅
- [x] Sync → list refreshes ✅
- [x] View switching → posts loaded by category ✅
- [x] Preview → markdown rendered correctly ✅
- [x] Keyboard shortcuts → work (Ctrl+S, Ctrl+P, Esc) ✅
- [x] View on GitHub → opens GitHub file URL ✅

## Remaining

### Priority 4: Local Git Fallback
- [ ] Add local git operations as fallback when GitHub API fails
- [ ] Detect offline mode and switch to local git
- [ ] Show "Local mode" indicator

### Priority 3: Polish (continued)
- [ ] Loading states (show "Loading..." while fetching)
- [ ] Empty states (better empty list messages)
- [ ] Error recovery (retry on failure)
- [ ] Refresh button in content list
- [ ] Sort posts by date (newest first)
