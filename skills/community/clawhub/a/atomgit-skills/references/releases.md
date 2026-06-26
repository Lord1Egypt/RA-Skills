# Releases

Read this file for version publishing, release inspection, release updates, and release asset flows.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List releases | `atomgit_get_repository_releases` |
| Inspect one release | `atomgit_get_repository_release` |
| Inspect latest release | `atomgit_get_latest_release` |
| Inspect release by tag | `atomgit_get_release_by_tag` |
| Create a release | `atomgit_create_repository_release` |
| Update a release | `atomgit_update_repository_release` |
| Get release upload URL | `atomgit_get_release_upload_url` |
| Download a release asset | `atomgit_download_release_asset` |

## Typical Flow

1. Confirm the repository and target tag.
2. Check whether the release already exists.
3. Create or update the release.
4. Use the upload or download endpoint only after the release target is confirmed.
