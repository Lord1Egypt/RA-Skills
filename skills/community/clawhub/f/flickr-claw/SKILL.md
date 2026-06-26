---
name: flickr-claw
description: Access Flickr with user-supplied local API credentials and OAuth tokens, verify authorization, export recent-upload or album metadata, download recent or album images for local visual review, and edit Flickr tags, titles, and descriptions. Use when working with a user's Flickr account, checking auth status, exporting metadata, pulling photos from a specific Flickr album, downloading Flickr images locally, or writing reviewed metadata back to Flickr.
metadata:
  version: "1.5.0"
  tags:
    - flickr
    - photo
    - tagging
    - metadata
    - oauth
    - albums
---

# Flickr Claw

Use the bundled script for Flickr authentication, export, download, and metadata editing.

## Security & Privacy

- This skill keeps Flickr credentials and OAuth tokens on the local machine.
- The bundled script talks only to official Flickr OAuth and REST endpoints.
- The skill does not send Flickr credentials, tokens, album data, or photo metadata to any third-party service by itself.
- Review the bundled Python script before trusting it in your environment, especially before using write-capable tokens.

## Requirements

Have these available before using the skill:

- A Flickr API key and secret from the user's own Flickr app
- Python
- `requests-oauthlib`
- A local credentials file at `~/.openclaw/flickr-app-credentials.json`

Install the Python dependency with:

```bash
pip install requests-oauthlib
```

Credentials file format:

```json
{
  "api_key": "YOUR_FLICKR_API_KEY",
  "api_secret": "YOUR_FLICKR_API_SECRET"
}
```

## Quick start

Run from the workspace root:

### Cross-platform form

```bash
python skills/flickr-claw/scripts/flickr_skill.py --check-auth
python skills/flickr-claw/scripts/flickr_skill.py --list-albums
python skills/flickr-claw/scripts/flickr_skill.py --album-photos --album-id ALBUM_ID --out ./flickr_album_photos.csv
```

### Windows PowerShell form

```powershell
python .\skills\flickr-claw\scripts\flickr_skill.py --check-auth
python .\skills\flickr-claw\scripts\flickr_skill.py --list-albums
python .\skills\flickr-claw\scripts\flickr_skill.py --album-photos --album-id ALBUM_ID --out .\flickr_album_photos.csv
```

If `--check-auth` fails because credentials or tokens are missing, use the authorization flow in `references/workflow.md`.

## Workflow

1. Confirm credentials exist at `~/.openclaw/flickr-app-credentials.json`.
2. Run `--check-auth` before larger operations.
3. Use `--list-albums` to find the album/photoset ID you want.
4. Use `--album-photos` or `--download-album` when you want to work from a specific album instead of recent uploads.
5. Use a read token for export-only work.
6. Use a write token for tags, titles, or descriptions.
7. Prefer `--add-tags` over `--set-tags` unless full replacement is intended.
8. Use `--download-latest` or `--download-album` before real image review.
9. Delete local downloaded image copies after tagging/review unless the user explicitly wants to keep them.
10. Expect occasional Flickr UI lag after writes; verify through API or refresh later if needed.

## Metadata guidance

- Preserve useful existing location and event tags unless cleanup is requested.
- Add subject/content tags from real image review when the user wants actual image understanding.
- Keep tags concrete and searchable: subject, scene, material, environment, light, place.
- Avoid speculative tags.
- Prefer short descriptive titles and plain factual descriptions unless the user asks for a different style.

## Commands

### Check auth

```bash
python skills/flickr-claw/scripts/flickr_skill.py --check-auth
```

### List albums

```bash
python skills/flickr-claw/scripts/flickr_skill.py --list-albums
```

### Export photos from one album

```bash
python skills/flickr-claw/scripts/flickr_skill.py --album-photos --album-id ALBUM_ID --out ./flickr_album_photos.csv
```

### Download one album for local review

```bash
python skills/flickr-claw/scripts/flickr_skill.py --download-album --album-id ALBUM_ID --out-dir ./flickr-album-downloads
```

### Start write auth

```bash
python skills/flickr-claw/scripts/flickr_skill.py --start-auth --perms write
```

### Finish auth

```bash
python skills/flickr-claw/scripts/flickr_skill.py --finish-auth --verifier CODE
```

### Audit recent uploads

```bash
python skills/flickr-claw/scripts/flickr_skill.py --audit --days 30 --out ./flickr_recent_uploads_audit.csv
```

### Download latest images for local review

```bash
python skills/flickr-claw/scripts/flickr_skill.py --download-latest --count 10 --days 30 --out-dir ./flickr-latest-downloads
```

### Add tags to a photo

```bash
python skills/flickr-claw/scripts/flickr_skill.py --add-tags --photo-id PHOTO_ID --tags "harbor, waterfront, blue-sky"
```

### Replace all tags on a photo

```bash
python skills/flickr-claw/scripts/flickr_skill.py --set-tags --photo-id PHOTO_ID --tags "harbor waterfront cityscape"
```

### Set title only

```bash
python skills/flickr-claw/scripts/flickr_skill.py --set-title --photo-id PHOTO_ID --title "Urban waterfront scene"
```

### Set description only

```bash
python skills/flickr-claw/scripts/flickr_skill.py --set-description --photo-id PHOTO_ID --description "View across an urban waterfront with clear weather and industrial details."
```

### Set title and description together

```bash
python skills/flickr-claw/scripts/flickr_skill.py --set-meta --photo-id PHOTO_ID --title "Urban waterfront scene" --description "View across an urban waterfront with clear weather and industrial details."
```

## Publication scope

Include:
- auth flow
- auth verification
- album listing/export/download
- recent-upload audit export
- recent-image download
- tag/title/description editing

Exclude:
- real API keys or secrets
- OAuth tokens
- request-token files
- user-specific audit CSVs, manifests, or downloaded images
- account-specific examples when generic ones work

## Resources

- `scripts/flickr_skill.py` — Flickr helper with auth, verification, album/recent export, download, and metadata editing support.
- `references/workflow.md` — setup details and command examples.
