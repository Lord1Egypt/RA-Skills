# Flickr workflow

## Local state

By default the script stores local state under the current user's home directory in `.openclaw`:

- App credentials: `~/.openclaw/flickr-app-credentials.json`
- Request token: `~/.openclaw/flickr-request-token-manual.txt`
- Access token: `~/.openclaw/flickr-access-token-manual.txt`

Credentials file format:

```json
{
  "api_key": "YOUR_FLICKR_API_KEY",
  "api_secret": "YOUR_FLICKR_API_SECRET"
}
```

## Dependency

Install the required Python package:

```bash
pip install requests-oauthlib
```

## Common commands

### Cross-platform form

```bash
python skills/flickr-claw/scripts/flickr_skill.py --check-auth
python skills/flickr-claw/scripts/flickr_skill.py --list-albums
python skills/flickr-claw/scripts/flickr_skill.py --album-photos --album-id ALBUM_ID --out ./flickr_album_photos.csv
python skills/flickr-claw/scripts/flickr_skill.py --download-album --album-id ALBUM_ID --out-dir ./flickr-album-downloads
python skills/flickr-claw/scripts/flickr_skill.py --start-auth --perms write
python skills/flickr-claw/scripts/flickr_skill.py --finish-auth --verifier CODE
python skills/flickr-claw/scripts/flickr_skill.py --audit --days 30 --out ./flickr_recent_uploads_audit.csv
python skills/flickr-claw/scripts/flickr_skill.py --download-latest --count 10 --days 30 --out-dir ./flickr-latest-downloads
python skills/flickr-claw/scripts/flickr_skill.py --add-tags --photo-id PHOTO_ID --tags "harbor, waterfront, blue-sky"
python skills/flickr-claw/scripts/flickr_skill.py --set-title --photo-id PHOTO_ID --title "Urban waterfront scene"
python skills/flickr-claw/scripts/flickr_skill.py --set-description --photo-id PHOTO_ID --description "View across an urban waterfront with clear weather and industrial details."
python skills/flickr-claw/scripts/flickr_skill.py --set-meta --photo-id PHOTO_ID --title "Urban waterfront scene" --description "View across an urban waterfront with clear weather and industrial details."
```

### Windows PowerShell form

```powershell
python .\skills\flickr-claw\scripts\flickr_skill.py --check-auth
python .\skills\flickr-claw\scripts\flickr_skill.py --list-albums
python .\skills\flickr-claw\scripts\flickr_skill.py --album-photos --album-id ALBUM_ID --out .\flickr_album_photos.csv
python .\skills\flickr-claw\scripts\flickr_skill.py --download-album --album-id ALBUM_ID --out-dir .\flickr-album-downloads
python .\skills\flickr-claw\scripts\flickr_skill.py --start-auth --perms write
python .\skills\flickr-claw\scripts\flickr_skill.py --finish-auth --verifier CODE
```

## Failure guide

- Missing credentials file: create `~/.openclaw/flickr-app-credentials.json` with `api_key` and `api_secret`.
- Missing token file: run `--start-auth`, approve the Flickr URL, then run `--finish-auth --verifier CODE`.
- `--check-auth` succeeds but write actions fail: the token likely has read access only; mint a new token with `--start-auth --perms write`.
- Album export/download fails: double-check the `--album-id` from `--list-albums`.
- Flickr UI does not show updates immediately: verify through API or refresh later.

## Notes

- `--check-auth` is the safest first command on a fresh install.
- Use `--list-albums` first when working from a specific Flickr album.
- Prefer `--add-tags` over `--set-tags` unless full replacement is intended.
- `--set-tags` overwrites the complete tag list.
- Write operations require a token minted with `--perms write`.
- Use `--download-latest` or `--download-album` before real image review so the agent can inspect actual image content locally.
- Delete downloaded local image copies after review/tagging unless the user explicitly asks to keep them.
- Override defaults with `--request-file`, `--access-file`, `--out`, or `--out-dir` when another location is needed.
