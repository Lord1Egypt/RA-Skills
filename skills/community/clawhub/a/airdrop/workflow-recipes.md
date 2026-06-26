# Workflow Recipes - AirDrop

Use these patterns when the user wants nearby local delivery from the agent.

## Direct Mode: Share One File

```bash
/path/to/airdrop-send.sh ./dist/release-notes.pdf
```

Best for:
- one PDF
- one ZIP
- one screenshot
- one installer file

## Direct Mode: Share Multiple Files

```bash
/path/to/airdrop-send.sh ./build/app.dmg ./build/checksums.txt
```

Use this when the recipient needs a small fixed bundle and no extra packaging.

## Curate Then Share

When the source is noisy, reduce it first:

```bash
mkdir -p ~/airdrop/staging/review-bundle
cp ./output/final-review.pdf ~/airdrop/staging/review-bundle/
cp ./output/diff-summary.txt ~/airdrop/staging/review-bundle/
zip -r ~/airdrop/staging/review-bundle.zip ~/airdrop/staging/review-bundle
/path/to/airdrop-send.sh ~/airdrop/staging/review-bundle.zip
```

Use this for:
- review packages
- debug bundles
- selected screenshots
- only-approved exports

## Text Needs a File First

If the user says "AirDrop this summary", stage it first:

```bash
printf '%s\n' "summary text here" > ~/airdrop/staging/session-summary.txt
/path/to/airdrop-send.sh ~/airdrop/staging/session-summary.txt
```

Do not claim chat text can be AirDropped directly without a shareable item.

## Shortcut Fallback Mode

If the user already has a Shortcut that accepts file input:

```bash
/path/to/airdrop-send.sh --shortcut "Send via AirDrop" ./exports/demo.mp4
```

Use this when:
- they prefer Shortcuts automation
- `swift` is unavailable
- the Shortcut performs pre-share transforms first

## Report State Correctly

Good:
- "AirDrop chooser launched for 2 files."
- "The handoff is ready; pick the nearby device in macOS."

Bad:
- "The file was delivered."
- "The device received it." 

Delivery is only confirmed after the user sees the device-side result.
