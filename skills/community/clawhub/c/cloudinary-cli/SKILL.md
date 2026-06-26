---
name: cloudinary-cli
description: Upload files and images to Cloudinary via CLI. Use when user wants to upload local files or images to Cloudinary CDN, especially when needing automatic image compression or batch uploads. Triggers on phrases like "upload to cloudinary", "传图到cloudinary", "上传图片", "cloudinary上传".
---

# Cloudinary CLI Uploader

Upload local files or remote URLs to Cloudinary with automatic image compression support.

## Workflow

### 1. Check Installation

Check if the CLI binary exists at `./cloudinary-cli` (project root). If not, run the install script:

```bash
bash .agents/skills/cloudinary-cli/scripts/install.sh
```

If Go is not installed, prompt the user to install Go first.

### 2. Check Configuration (`.env`)

Check if `cmd/cli/.env` exists and contains all required variables. If any are missing, prompt the user for the missing values and write them to `cmd/cli/.env`.

**Required variables:**
- `CLOUDINARY_CLOUD` - Cloudinary cloud name
- `CLOUDINARY_KEY` - API key
- `CLOUDINARY_SECRET` - API secret

**Optional variables:**
- `CLOUDINARY_DIRECTORY` - Upload folder (default: root)
- `CLOUDINARY_COMPRESS` - Auto-compress images: `true`/`false` (default: `true`)

### 3. Upload Files

Run the upload script with file paths:

```bash
bash .agents/skills/cloudinary-cli/scripts/upload.sh <file1> [file2] ...
```

Or run the CLI directly:

```bash
cd cmd/cli && ../../cloudinary-cli file1.jpg file2.png
```

The CLI automatically:
- Compresses images when `CLOUDINARY_COMPRESS=true`
- Leaves non-image files untouched
- Supports both local paths and remote URLs

## Image Compression

When `CLOUDINARY_COMPRESS` is `true` (default), images are uploaded with Cloudinary `q_auto` transformation for automatic quality optimization. Supported image formats: jpg, jpeg, png, gif, webp, bmp, tiff, svg, ico, heic, heif, avif.

To disable compression for a specific upload, temporarily set `CLOUDINARY_COMPRESS=false` in `.env`.
