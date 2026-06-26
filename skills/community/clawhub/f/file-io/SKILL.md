---
name: file-io
description: >
  Upload local files to filebin.net for quick sharing.
  Use when the user asks to upload a file, share a file via link, host a file,
  or says "upload to filebin" / "put on filebin.net".
  NOT for downloading or general file management.
---

# File Upload via filebin.net

Upload local files to filebin.net so the user gets a shareable link.

## Rules

- Bin ID must be 15–26 characters (shorter → "the bin is too short"; longer → "the bin is too long").
- Filebin bins auto-expire after 7 days.

## Steps

1. **Find the file provided by user** Locate the target file in the ~/.openclaw/workspace/.
2. **Generate bin ID.**   
  ```
    import uuid
    u = uuid.uuid4().hex  # hex string (32 chars)
    bin_id = f"my-upload{u[-6:]}"
    print(bin_id)
  ```
3. **Upload via curl (PowerShell):**

   ```
   curl -si -X POST -H "Content-Type: application/octet-stream" -T "<FILEPATH>" "https://filebin.net/$binId/<FILENAME>"
   ```

4. **Extract the URL** from the response JSON. Construct:
   - File direct link: `https://filebin.net/<binId>/<filename>`
   - Bin page: `https://filebin.net/<binId>`

## Notes
- user should not upload a private file because file uploaded will be public.
- If upload returns `400 "the bin is too short/long"`, adjust bin ID length and retry.
- For large files (>100 MB), warn the user that filebin may reject them.
