---
name: douyin-send-dm
description: Send a direct message (私信) to a specific Douyin user via the user's logged-in Chrome through OpenClaw's browser tool. Use whenever the user asks to send, DM, message, or 发私信 to someone on Douyin / 抖音 / douyin.com — even when they only describe the action ("tell @xyz hi", "ping that creator on Douyin"). Works for the web client only and only when sender and recipient are mutual followers (相互关注). Surface ban/block tips honestly instead of claiming success.
---

# Douyin: Send a DM via Chrome

Send a text DM to a Douyin user from the user's signed-in Chrome session, then verify the message actually delivered (Douyin will silently render bubbles even when DMs are banned — never claim success without checking).

## When to use

Trigger on any of:

- "send a message to <name> on Douyin / 抖音"
- "DM <name> on douyin.com"
- "tell <name> '<text>' on Douyin"
- 抖音 / 私信 / 发私信 mentioned alongside a target user

If the user wants to control the **desktop app** (`抖音聊天.app` / Douyin Chat for Mac) rather than the website, this skill does not apply — that requires macOS Accessibility automation, not browser control.

## Prerequisites (one-time setup)

1. **Chrome 144+ exposing CDP on `127.0.0.1:9222`.**
   The user can launch Chrome with `--remote-debugging-port=9222`, or open `chrome://inspect/#remote-debugging`, click *Configure…*, and follow the in-page steps until they see `Server running at: 127.0.0.1:9222`.
2. **OpenClaw `user` browser profile** (built-in: `driver=existing-session`, `transport=chrome-mcp`). No extra config needed — `browser action=start profile=user` will spawn `chrome-devtools-mcp` and attach.
3. **User logged into douyin.com** in that Chrome.
4. **Sender and recipient must be mutual followers (相互关注).** Douyin web blocks DMs to non-mutuals. If the target's profile shows only "关注" (follow) instead of "相互关注", stop and tell the user.
5. **Sender's DM privilege not banned.** If banned, the message bubble still renders locally with a tip "私信功能已被封禁" — see Verify step.

## Workflow

### 1. Attach to Chrome

```
browser action=start profile=user
browser action=tabs profile=user
```

Pick an empty tab from `tabs`, or be prepared to open a new one. Save its `targetId` — pass it on every subsequent call to keep the same tab.

### 2. Find the target user

Navigate the chosen tab to a user search:

```
browser action=navigate profile=user targetId=<id>
  url=https://www.douyin.com/search/<URL-encoded query>?type=user
```

Snapshot with `refs="aria"` and pick the result whose card shows **"相互关注"** and whose 抖音号 / bio matches what the user described. If multiple plausible results exist, ask the user to confirm before proceeding.

Click that result link by ref — it opens the profile in a **new tab**. Snapshot or `browser action=tabs` again to find the new `targetId` (URL pattern: `https://www.douyin.com/user/MS4wLj…`). Switch to that tab for the rest of the flow.

### 3. Open the DM panel from the profile

Critical: there are two `私信` controls on the page.

- Header `私信` (top-right, around x≈1542) opens the **global DM panel** with no conversation selected.
- Profile-page `私信` button (next to "相互关注", around x≈1562 y≈158) opens the panel **with the right conversation already selected**.

**Always click the profile-page button.** Find it via DOM filter, not by ref (the ref tree sometimes returns the wrong element):

```
browser action=act profile=user targetId=<profile-tab>
  request={"kind":"evaluate","fn":"() => { const btns=[...document.querySelectorAll('button')].filter(b=>(b.innerText||'').trim()==='私信' && b.offsetParent!==null); for (const b of btns){ const r=b.getBoundingClientRect(); if (r.width>30 && r.width<200 && r.height>20 && r.height<60 && r.x>200){ b.click(); return JSON.stringify({clicked:true,x:Math.round(r.x),y:Math.round(r.y)}); } } return JSON.stringify({found:btns.length}); }"}
```

Then wait for the panel to render:

```
browser action=act profile=user targetId=<id>
  request={"kind":"wait","timeMs":1500}
```

Verify the right conversation is selected by reading `.RightPanelHeadertitle`:

```
browser action=act profile=user targetId=<id>
  request={"kind":"evaluate","fn":"() => { const h=document.querySelector('.RightPanelHeadertitle'); return h?h.innerText:null; }"}
```

The result must equal the target user's display name. If null or wrong, the DM panel didn't open or the wrong row got selected — retry the click.

### 4. Type the message

The message editor is a `[contenteditable="true"]` with placeholder `发送消息`. Standard `act:type` rejects pure-coords focus on existing-session driver, so write the text via `execCommand`:

```
browser action=act profile=user targetId=<id>
  request={"kind":"evaluate","fn":"() => { const ed=[...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>{const r=e.getBoundingClientRect();return r.width>100 && r.height>20;}); if(!ed) return 'no-editor'; ed.focus(); const sel=window.getSelection(); const range=document.createRange(); range.selectNodeContents(ed); range.collapse(false); sel.removeAllRanges(); sel.addRange(range); document.execCommand('insertText',false,'<MESSAGE TEXT>'); return ed.innerText; }"}
```

Replace `<MESSAGE TEXT>` with the user's message. Escape single quotes (`'` → `\\'`). The returned innerText should match the message (a trailing zero-width char is fine).

### 5. Send

```
browser action=act profile=user targetId=<id>
  request={"kind":"press","key":"Enter"}
```

### 6. Verify delivery — do not skip

Inspect the DOM for both signals:

```
browser action=act profile=user targetId=<id>
  request={"kind":"evaluate","fn":"() => { const ed=[...document.querySelectorAll('[contenteditable=\"true\"]')].find(e=>{const r=e.getBoundingClientRect();return r.width>100 && r.height>20;}); const editorText=ed?ed.innerText.trim():null; const list=document.querySelector('.messageMessageListwrapper'); const listText=list?list.innerText.slice(0,400):''; const banned=/私信功能已被封禁|对方拒收|不是Ta的好友|无法发送/.test(listText); return JSON.stringify({editorEmpty:!editorText||editorText==='\u200b'||editorText==='', listText, banned}); }"}
```

Outcome matrix:

| editorEmpty | banned | Result |
|---|---|---|
| true | false | ✅ delivered — confirm to user |
| true | true | ⚠️ Sent locally but Douyin blocked it. Tell the user the bubble appears but the recipient won't receive it; they should check Douyin notifications for the ban reason. |
| false | – | ❌ Send didn't fire (Enter consumed by IME, no focus, etc.). Retry steps 4–5. |

Always quote the exact tip text Douyin shows when reporting a ban — don't paraphrase.

## Failure modes & recovery

- **Search returns multiple "相互关注" matches.** Ask the user to disambiguate by 抖音号 or bio before clicking.
- **No 私信 button on profile, only "关注" / "相互关注".** Not mutuals. Tell the user — Douyin web doesn't allow DMs to non-mutuals.
- **`browser action=screenshot` fails with `ENOENT … openclaw-chrome-mcp-…`.** Known existing-session driver quirk. Skip screenshots; rely on DOM inspection (`evaluate`) for verification.
- **Header 私信 click instead of profile button.** Closes / reopens the global panel without selecting a chat. Always re-check `.RightPanelHeadertitle` matches the target.
- **Massive `evaluate` blocks accidentally clicking page-wide containers.** Constrain queries with `getBoundingClientRect` size filters (e.g. `width<400 && height<100`).
- **`act:type` errors with "type requires ref or selector".** Existing-session driver doesn't accept coords-only focus. Use the `execCommand('insertText', …)` evaluate pattern in step 4.
- **Chrome MCP attach times out (`Chrome MCP existing-session attach … timed out`).** Verify `curl -s http://127.0.0.1:9222/json/version` returns JSON. If `404`, Chrome's `chrome://inspect` proxy is on but the actual DevTools endpoint isn't — relaunch Chrome with `--remote-debugging-port=9222`.

## Reuse on another machine

Copy this `SKILL.md` (and parent directory) to that machine's skills root (e.g. `~/.openclaw/workspace/skills/douyin-send-dm/` or `~/.agents/skills/douyin-send-dm/`). Then just say "send a Douyin DM to <user>: <text>" — OpenClaw's skill discovery will load it.

If the target user is not the same person as on this machine, redo step 2 (search + confirm 相互关注) before sending.

## Honest reporting rules

- Never say "message sent" based only on the bubble appearing. Always run the verify step.
- If banned/blocked, surface Douyin's exact tip in your reply and recommend the user check their Douyin notifications.
- If the user asks "did it actually send?", re-run the verify-step query and report the live DOM state.
