# Diagram Workflow SOP

## Core principle

The saved `.drawio` file is the source of truth. Local workspace files are draft/export surfaces only. Once a diagram is finalized, store it somewhere stable and share from there.

---

## Standard workflow

### 1. Choose the right destination first
Before building, decide where the final `.drawio` file lives:
- Cloud storage (Google Drive, Dropbox, etc.)
- A project folder in your repo or workspace
- A shared drive for the team

### 2. Draft locally first
Build the initial diagram in a local diagrams folder:
```
./diagrams/<name>.drawio
```
This is fine for rapid drafting before the final destination is decided.

### 3. Move the `.drawio` file to its destination
Once the location is ready, move the source file there. That file becomes the master from that point on — edit it in place, not a local copy.

### 4. Export PNGs locally for review
For sharing and delivery, export PNGs locally:
```bash
mkdir -p ./diagrams
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --output ./diagrams/<name>.png --scale 2 --border 30 ./diagrams/<name>.drawio

# Linux / headless
xvfb-run -a drawio --export --format png --output ./diagrams/<name>.png --scale 2 --border 30 ./diagrams/<name>.drawio
```
Review images are temporary — the `.drawio` file is the real asset.

### 5. Share the file
Generate a share link from wherever the `.drawio` file is stored (Google Drive, Dropbox share, repo URL, etc.) and send that to the user along with the PNG preview.

---

## Hyperlinking inside `.drawio` files

You can embed clickable hyperlinks into boxes within the `.drawio` file:
- Link process boxes to related documentation
- Keep box labels clean and human-readable
- Note: hyperlinks only work in the live `.drawio` file, not in PNG exports

---

## Naming conventions

Source files:
```
system-architecture-v1.drawio
onboarding-flow.drawio
database-schema.drawio
```

PNG review exports:
```
system-architecture-v1-review.png
system-architecture-v1-preview.png
```

Avoid `v1`, `v2`, `v3` proliferation — use semantic names and version numbers only when needed for history.

---

## Versioning rule

Keep one active master file. Only archive old versions when a major structural change is made. Label archived versions with `-archived` or `-speculative` suffix so they're clearly not the active file.

Example:
- `onboarding-flow-v1-archived.drawio` — parked, not active
- `onboarding-flow-v2.drawio` — current master
