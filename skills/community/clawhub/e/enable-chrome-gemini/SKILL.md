---
name: enable-chrome-gemini
description: Set up or repair Gemini in Chrome (Glic) on Windows, macOS, or Linux when enabling it for the first time outside the US or when the sidebar, floating panel, Alt+G shortcut, or top-bar entry disappears. Back up and patch Chrome Local State, restore region/eligibility fields, and check the required Glic flags and Chrome language.
---

# Enable Chrome Gemini

## Overview

Use this skill to set up Gemini in Chrome on Windows, macOS, or Linux for the first time in non-US regions, or to bring it back when it was previously working and the sidebar or floating panel no longer opens.

## Workflow

### 1. Close Chrome

- Close every Chrome window.
- If Chrome is still running, stop here before editing profile data.

### 2. Patch Local State

- Run `scripts/repair_chrome_gemini.py`.
- The script backs up `Local State` and patches the Gemini eligibility fields.
- It sets the variation country to `us`, marks Glic eligibility true, keeps the `glic@1` and `glic-side-panel@1` experiments, and normalizes the Chrome UI language to `en-US`.

### 3. Relaunch and verify

- Open Chrome again.
- Test `Alt + G`.
- If Gemini appears, the setup is complete.

### 4. Finish the native setup if needed

- If Gemini still does not appear, open `chrome://flags` and verify `Glic` and `Glic side panel`.
- Only use the manual flags step if the underlying profile state did not take effect.
- On macOS, the Chrome profile lives under `~/Library/Application Support/Google/Chrome`.

### 5. Confirm the result

- Use `Alt + G` one more time.
- Check that the Gemini sidebar or floating panel opens on the active Chrome profile.

## What The Script Changes

- Set Chrome variation country fields to `us`.
- Set `glic.is_glic_eligible = true`.
- Keep existing Glic experiments and ensure `glic@1` and `glic-side-panel@1` are present.
- Set `intl.app_locale`, `intl.selected_languages`, and `intl.accept_languages` to English values.
- Write a timestamped backup next to `Local State`.

## When To Use It

- First-time Gemini in Chrome setup outside the US.
- A fresh Chrome profile needs Gemini enabled.
- Gemini in Chrome worked before and stopped opening.
- The sidebar, floating panel, or `Alt + G` shortcut no longer appears.
- Chrome has the right version, but the entry is hidden or eligibility seems missing.
- A browser state from a prior tutorial or profile needs to be normalized into the native Gemini setup.

## What This Skill Covers

- Native Chrome Gemini / Glic setup.
- Windows, macOS, and Linux profile locations.
- Local State patching for region and eligibility.
- Flag and language checks that unblock the native UI.

## What This Skill Does Not Cover

- Third-party Gemini extensions.
- Non-Chrome browsers.
- Enterprise policy administration beyond detecting that policy may block the setup.

## Guardrails

- Only edit `Local State`.
- Do not touch unrelated Chrome profile files.
- If Chrome is still running, stop and ask the user to close it unless `--force` is requested.
- If the profile is managed by policy, stop and report that the fix may be blocked.

## Script Usage

```powershell
python scripts/repair_chrome_gemini.py --user-data-dir "%LOCALAPPDATA%\Google\Chrome\User Data"
```

```bash
python scripts/repair_chrome_gemini.py
```

Use `--dry-run` to preview changes, `--force` if Chrome is already open and you want to override the safety check, and `--language ""` to skip language normalization.

On macOS or Linux, the script defaults to the standard Chrome profile location, so the `--user-data-dir` flag is optional unless you use a custom profile path.
