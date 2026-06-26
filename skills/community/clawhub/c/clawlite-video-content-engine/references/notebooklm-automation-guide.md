# NotebookLM Automation Guide

Use this guide when the workflow includes **YouTube → NotebookLM** ingestion before generating ClawLite content outputs.

## Core principle

Always use a screenshot-first loop:

```text
Screenshot → Analyze → Target → Verify → Execute → Screenshot → Confirm
```

Do not assume NotebookLM UI state is correct without verification.

## What NotebookLM is for in this workflow

NotebookLM is the **source-ingestion layer**.
Use it to help extract:
- transcript understanding
- high-level summary
- major sections
- quotes or useful ideas
- working notes for later content packaging

Do not confuse NotebookLM output with the final content pack.
Your final outputs should still be:
- source note
- beginner translation
- short-video script
- X thread
- LinkedIn/Facebook post
- short blog summary
- soft ClawLite CTA bridge

## Main UI trap

NotebookLM has multiple textareas.
The most common failure is typing into the wrong one.

### Wrong target
- sidebar search textarea

### Correct targets
- URL input: `textarea[placeholder="Paste any links"]`
- text input: `textarea[placeholder="Paste text here"]`

Avoid generic selectors like:

```javascript
document.querySelector('textarea')
```

Use specific selectors instead.

## URL source entry pattern

```javascript
var urlTextarea = document.querySelector('textarea[placeholder="Paste any links"]');
if (urlTextarea) {
  var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  setter.call(urlTextarea, 'https://www.youtube.com/watch?v=VIDEO_ID');
  urlTextarea.dispatchEvent(new Event('input', { bubbles: true }));
  urlTextarea.dispatchEvent(new Event('change', { bubbles: true }));
}
```

## Text source entry pattern

```javascript
var pasteTextarea = document.querySelector('textarea[placeholder="Paste text here"]');
if (pasteTextarea) {
  var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  setter.call(pasteTextarea, RESEARCH_CONTENT);
  pasteTextarea.dispatchEvent(new Event('input', { bubbles: true }));
  pasteTextarea.dispatchEvent(new Event('change', { bubbles: true }));
}
```

## Angular / reactive UI rule

Simple assignment often does not work:

```javascript
textarea.value = 'content';
```

Prefer prototype setter + `input` / `change` dispatch so the app recognizes the change.

## Button click rule

Never click submit buttons blindly.
Check first:
- button exists
- button is enabled
- button does not look visually disabled

Example:

```javascript
var buttons = Array.from(document.querySelectorAll('button'));
var btn = buttons.find(b => b.textContent.includes('Insert'));
if (btn && !btn.disabled && !btn.className.includes('disabled')) {
  btn.click();
}
```

## Modal detection

Use modal presence to verify you are in the correct source-entry state.

```javascript
var modals = document.querySelectorAll('[role="dialog"], .mat-mdc-dialog-container');
var isModalOpen = modals.length > 0;
```

Then check which input exists:
- `Paste any links` → URL mode
- `Paste text here` → copied text mode

## Recommended wait times

- page navigation: 3s
- dialog open: 2s
- YouTube source processing: 8–10s
- text source processing: 5s
- audio generation: 5–10 minutes

Do not rush transitions.

## Error recovery

### If the wrong input field was targeted
- clear the accidental input
- re-run with the correct specific selector
- confirm the correct modal is open before retrying

### If the button is disabled
- re-dispatch input/change events
- confirm content actually entered the correct field
- wait and re-check state

### If the modal did not open
- wait longer
- reopen the source flow
- confirm with a screenshot before typing again

## Best practice in this skill

Use NotebookLM to create a better source note, then switch back to the ClawLite content engine workflow:
1. ingest video into NotebookLM
2. extract summary/transcript understanding
3. build the source note
4. choose the angle
5. generate the content pack

NotebookLM improves the **input quality**.
It should not replace the rest of the content workflow.
