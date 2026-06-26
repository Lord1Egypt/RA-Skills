# Playwright Draft Flow

The automation script (`scripts/draft_to_csdn.example.py`) follows this exact sequence of events. 

## Flow sequence:
1. **Initialize**: Read the output files from `/output/csdn/` (Title, Markdown, Summary, Tags).
2. **Launch Browser**: Start Playwright with `headless=False` (browser UI must be visible).
3. **Navigate**: Go to the CSDN Markdown Editor page (`https://editor.csdn.net/md/`).
4. **Login Check**: Wait. If the user is not logged in, CSDN will present a login dialog. The script pauses and waits for the user to manually scan the QR code or enter credentials.
5. **Wait for Editor**: Once logged in, wait for the Markdown editor elements to load.
6. **Fill Title**: Locate the title input box and fill it with the chosen title.
7. **Fill Body**: Locate the Markdown editor text area and fill it with `csdn_markdown_ready.md`.
8. **Fill Summary (If accessible)**: Attempt to open the publish settings panel and fill the summary. If DOM elements are not found, log a warning and continue.
9. **Fill Tags (If accessible)**: Attempt to fill tags. If unstable, log a warning and let the user do it manually.
10. **Halt**: The script completely stops executing its routine and keeps the browser open.
11. **Manual Action**: The human user reviews the draft, makes adjustments, clicks "Save Draft" or "Publish Article".
12. **Close**: When the user closes the browser window, the Python script terminates.

## Error Handling
- If any CAPTCHA, slider verification, or security block appears, the script does NOT attempt to bypass it. It will timeout on the next element search and wait for human intervention.
- If DOM selectors change (CSDN updates their UI), the script will gracefully timeout and instruct the user to manually copy the content from the output folders.
