# Guide the user through scanning

Guide users through a ClawGuard scan and export results.

---

## Scan Type Decision

| | L1 Browser Scan | L2 Local Scan |
|---|---|---|
| Speed | <5 seconds | ~30-60 seconds |
| Depth | 100+ config checks | Deeper analysis (file hashes, runtime state) |
| Privacy | Zero data leaves browser | Results sent to server for analysis |
| Checks | Config files in ~/.openclaw/ | Config + binaries, logs, permissions |
| Best for | Quick posture check | Thorough audit, inconclusive L1 results |

**Decision rule:** Start with L1. If many items show "needs more evidence," suggest L2.

---

## L1 Browser Scan Steps

1. Open [clawguardsecurity.ai](https://clawguardsecurity.ai).
2. Click the **Browser Scan** tab.
3. Click the folder picker and select the `~/.openclaw/` directory.
   - On macOS, press **Cmd+Shift+G** in the file dialog to type the path directly.
4. Wait for the scan to complete (<5 seconds).
5. Review results on screen before exporting.

---

## L2 Local Scan Steps

1. Open [clawguardsecurity.ai](https://clawguardsecurity.ai).
2. Click the **Local Scan** tab.
3. Copy the generated command from the appropriate tab:
   - **Bash** tab for macOS / Linux.
   - **PowerShell** tab for Windows.
4. Paste and run the command in a terminal.
5. Wait for results to appear on the web page.

---

## Export Instructions

After the scan completes, click the **Export** button and select **JSON** format.

- JSON is required for this skill to parse results.
- Optionally export PDF for a human-readable copy.
- Exported filename pattern: `clawguard-report-{timestamp}.json`

---

## Finding the Exported File

| OS | Default download path |
|---|---|
| macOS | `~/Downloads/` |
| Linux | `~/Downloads/` |
| Windows | `C:\Users\{username}\Downloads\` |

---

## After Export

Tell the user:

> Share the path to your exported JSON file and I will analyze it.

If the file is not found at the default download path, ask the user for the actual location.

---

## Returning Users

- Skip the scan type explanation. Ask directly: "L1 or L2?"
- If they already have a report file, skip scan guidance entirely and proceed to analysis.
