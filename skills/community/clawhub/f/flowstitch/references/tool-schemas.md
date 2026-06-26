# Stitch MCP Tool Schemas

Use these examples to format tool calls to the Stitch MCP server correctly.

**Important:** Always run `list_tools` first to find the active prefix (e.g., `stitch:` or `mcp_stitch:`).
Replace `[prefix]` below with whatever prefix `list_tools` returns.

---

## Project Management

### `[prefix]:list_projects`
Lists all Stitch projects accessible to you.
```json
{
  "filter": "view=owned"
}
```

### `[prefix]:get_project`
Retrieves full project details including `designTheme` metadata.
```json
{
  "name": "projects/4044680601076201931"
}
```
Note: Use the full `projects/{id}` path, not just the numeric ID.

### `[prefix]:create_project`
Creates a new Stitch project.
```json
{
  "title": "My New App"
}
```

---

## Screen Management

### `[prefix]:list_screens`
Lists all screens within a project.
```json
{
  "projectId": "4044680601076201931"
}
```
Note: Use the numeric ID only (not the full `projects/{id}` path).

### `[prefix]:get_screen`
Retrieves metadata + download URLs for a specific screen.
```json
{
  "projectId": "4044680601076201931",
  "screenId": "98b50e2ddc9943efb387052637738f61"
}
```
Returns:
- `screenshot.downloadUrl` — PNG screenshot (append `=w{width}` for full resolution)
- `htmlCode.downloadUrl` — Full HTML/CSS source
- `width`, `height` — Screen dimensions
- `deviceType` — MOBILE | DESKTOP | TABLET

---

## Design Generation

### `[prefix]:generate_screen_from_text`
Generates a new screen from a text description.
```json
{
  "projectId": "4044680601076201931",
  "prompt": "A modern landing page for a coffee shop with a hero section, menu, and contact form.\n\n**DESIGN SYSTEM (REQUIRED):**\n- Platform: Web, Desktop-first\n- Theme: Light, warm, artisanal\n- Background: Warm Cream (#faf5f0)\n- Primary Accent: Deep Brown (#4b2c20) for buttons and links\n- Text Primary: Near Black (#1a1a1a)\n- Buttons: Subtly rounded (8px), comfortable padding\n- Layout: Centered content, max-width container",
  "deviceType": "DESKTOP"
}
```
Returns `outputComponents` with AI text description and suggestions — always surface these to the user.

### `[prefix]:edit_screens`
Edits one or more existing screens with a text prompt.
```json
{
  "projectId": "4044680601076201931",
  "selectedScreenIds": ["98b50e2ddc9943efb387052637738f61"],
  "prompt": "Change the background color to white (#ffffff) and make the call-to-action button larger. Make no other changes."
}
```
Best practice: One targeted change per edit call for maximum precision.

---

## Asset Download Notes

### Full-Resolution Screenshots
Google CDN serves low-res thumbnails by default. Always append `=w{width}` to get full resolution:
```
https://lh3.googleusercontent.com/d/XXX=w1440
```
Where `{width}` is the `width` value from `get_screen` metadata.

### GCS Download (HTML files)
Internal AI fetch tools can fail on Google Cloud Storage URLs. Use `scripts/fetch-stitch.sh` for reliable downloads:
```bash
bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" ".stitch/designs/index.html"
bash scripts/fetch-stitch.sh "[screenshot.downloadUrl]=w1440" ".stitch/designs/index.png"
```

---

## metadata.json — Full Schema

Persist this file after project creation or screen generation. Call `[prefix]:get_project` to populate.

```json
{
  "name": "projects/6139132077804554844",
  "projectId": "6139132077804554844",
  "title": "My App",
  "visibility": "PRIVATE",
  "createTime": "2026-03-04T23:11:25.514932Z",
  "updateTime": "2026-03-04T23:34:40.400007Z",
  "projectType": "PROJECT_DESIGN",
  "deviceType": "DESKTOP",
  "designTheme": {
    "colorMode": "DARK",
    "font": "INTER",
    "roundness": "ROUND_EIGHT",
    "customColor": "#40baf7",
    "saturation": 3
  },
  "screens": {
    "index": {
      "id": "d7237c7d78f44befa4f60afb17c818c1",
      "sourceScreen": "projects/6139132077804554844/screens/d7237c7d78f44befa4f60afb17c818c1",
      "x": 0,
      "y": 0,
      "width": 1440,
      "height": 900
    },
    "about": {
      "id": "bf6a3fe5c75348e58cf21fc7a9ddeafb",
      "sourceScreen": "projects/6139132077804554844/screens/bf6a3fe5c75348e58cf21fc7a9ddeafb",
      "x": 1489,
      "y": 0,
      "width": 1440,
      "height": 1159
    }
  },
  "metadata": {
    "userRole": "OWNER"
  }
}
```
