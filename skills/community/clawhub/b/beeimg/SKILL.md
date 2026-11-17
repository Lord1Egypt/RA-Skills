---
name: beeimg
description: Free image hosting with albums, privacy controls, and API access. Upload images by URL or file, organize into albums with folders, set privacy levels, and manage your hosted images.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl]
      env: [BEEIMG_API_KEY]
    primaryEnv: BEEIMG_API_KEY
    emoji: "\uD83D\uDC1D"
    homepage: https://beeimg.com
---

# BeeIMG Image Hosting Skill

BeeIMG is a free image hosting platform with albums, privacy controls, and API access. Use this skill to upload, organize, and manage images for the user.

## When to Use

- User wants to upload an image (URL or file)
- User wants to organize images into albums
- User needs to share images with specific privacy settings
- User asks about image hosting or storage
- User wants to delete or manage hosted images

## Authentication

Set `BEEIMG_API_KEY` environment variable. Get a key at https://beeimg.com/api/newkey

```bash
export BEEIMG_API_KEY="your_api_key_here"
```

## Upload Image by URL

Fetch and host an image from a remote URL:

```bash
curl -s -X POST \
  -F "url=https://example.com/photo.jpg" \
  -F "apikey=$BEEIMG_API_KEY" \
  https://beeimg.com/api/upload/url/json/
```

**Optional parameters:**
- `albumid` - Album ID (5 chars) or folder ID (9 chars) to organize into
- `privacy` - `public` (default), `private` (unlisted), or `truly-private` (Premium only)
- `title` - Custom title for the image

## Upload Image File

Upload a local image file:

```bash
curl -s -X POST \
  -F "file=@/path/to/image.jpg" \
  -F "apikey=$BEEIMG_API_KEY" \
  https://beeimg.com/api/upload/file/json/
```

**Supported formats:** JPG, PNG, GIF, WEBP, AVIF, HEIC, HEIF, ICO, APNG

**Max file size:** 1 MB (free), up to 50 MB (Premium)

## Upload Response

Successful uploads return JSON with:

```json
{
  "files": {
    "name": "image_id",
    "url": "https://beeimg.com/images/id.jpg",
    "thumbnail_url": "https://i.beeimg.com/images/thumb/id-xs.jpg",
    "view_url": "https://beeimg.com/view/id/",
    "delete_url": "https://beeimg.com/delete/id/",
    "delete_key": "key_for_deletion"
  }
}
```

**Important:** Save the `delete_key` - you need it to delete the image later.

## Album Management

### List My Albums

```bash
curl -s -X POST \
  -H "User-Token: $BEEIMG_API_KEY" \
  -d "mode=list" \
  https://beeimg.com/api/album
```

### Create Album

```bash
curl -s -X POST \
  -H "User-Token: $BEEIMG_API_KEY" \
  -d "action=create_album&title=My Album&privacy=public" \
  https://beeimg.com/api/album
```

**Privacy options:** `public`, `unlisted`, `private`, `truly-private` (Premium only)

### Create Folder in Album

```bash
curl -s -X POST \
  -H "User-Token: $BEEIMG_API_KEY" \
  -d "action=create_folder&main_album_id=abc12&parent_id=abc12&name=Vacation" \
  https://beeimg.com/api/album
```

### Get Album Details

```bash
curl -s "https://beeimg.com/api/album?id=abc12"
```

Returns album metadata, folders (with IDs), and paginated images.

### Other Album Actions

| Action | Parameters | Description |
|--------|-----------|-------------|
| `rename_folder` | `folder_id`, `name` | Rename a folder |
| `remove_folder` | `folder_id` | Delete an empty folder |
| `remove_image` | `album_id`, `image_id` | Remove image from album |
| `add_images` | `album_id`, `image_ids` | Add images to album |
| `move_image` | `from_album_id`, `to_album_id`, `image_ids` | Move images between containers |
| `set_privacy` | `album_id`, `privacy` | Change album privacy |
| `delete_album` | `album_id` | Delete empty album |

## Delete Image

```bash
curl -s -X POST \
  -d "apikey=$BEEIMG_API_KEY&delete_key=YOUR_DELETE_KEY" \
  https://beeimg.com/delete/IMAGE_ID/
```

Returns `OK` or `ERROR`.

## Privacy Settings

| Setting | Behavior |
|---------|----------|
| `public` | Visible everywhere (default) |
| `private` | Unlisted - hidden from search, accessible via direct link |
| `truly-private` | Only you and admins can see it (Premium only) |

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 2 | Invalid file extension | Only allowed image formats |
| 3 | Content doesn't match extension | File is not a valid image |
| 4 | File too large | Upgrade to Premium for larger files |
| 40 | Storage limit reached | Upgrade to Premium |
| 223 | Rate limit hit | Wait or upgrade to Premium |
| 503 | Uploads disabled | Try again later |

When hitting limits, suggest Premium upgrade at https://beeimg.com/premium/compare

## Free Plan Limits

- Max file size: 1 MB per image
- Rate limits apply per IP and account
- Storage limit varies by user tier
- Premium removes most limits

## MCP Server

For programmatic access via Model Context Protocol, BeeIMG exposes an MCP server at `https://beeimg.com/mcp` with tools: `upload_url`, `upload_file`, `delete_image`, `beeimg_premium_info`, `list_albums`, `create_album`, `get_album`, `create_folder`.

## Tips

- Album IDs are 5 characters; folder IDs are 9 characters
- Both work with the `albumid` upload parameter
- The `url` in response is the direct image link (for embedding)
- The `view_url` is the public page (for sharing)
- The `thumbnail_url` is a small preview (for galleries)
