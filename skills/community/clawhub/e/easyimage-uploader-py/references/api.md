# EasyImages 2.0 API notes

## Upload endpoint

Official upload API:

- Method: `POST`
- Path: `/api/index.php`
- Content-Type: `multipart/form-data`
- Fields:
  - `image`: the file to upload
  - `token`: EasyImages upload token

Base example:

```bash
curl -X POST https://your-easyimage-host/api/index.php \
  -F "image=@/path/to/file.jpg" \
  -F "token=YOUR_TOKEN"
```

## Success response

Typical JSON fields returned on success:

```json
{
  "result": "success",
  "code": 200,
  "url": "https://img.example.com/2023/01/24/example.webp",
  "srcName": "original-name",
  "thumb": "https://img.example.com/application/thumb.php?img=/i/2023/01/24/example.webp",
  "del": "https://img.example.com/application/del.php?hash=..."
}
```

Important fields:

- `url`: direct image URL to return to the user
- `thumb`: thumbnail URL when available
- `del`: delete URL, sensitive, usually avoid exposing unless the user asks

## Common status codes from EasyImages docs

Upload-related codes documented upstream:

- `200`: upload success
- `202`: upload limit exceeded
- `204`: no file selected
- `205`: uploader blocked by allowlist/denylist rules
- `400`: request or file problem
- `401`: login required by server policy
- `403`: bad upload signature or token problem
- `406`: illegal file

## Configuration expected by this skill

Provide both of these before uploading:

- `EASYIMAGE_URL`: EasyImages service base URL, for example `https://img.example.com`
- `EASYIMAGE_TOKEN`: upload token

The bundled script also accepts CLI flags:

- `--server`
- `--token`
