# Upload Guide - 3-Step File Upload Process

## Overview

Uploading files to DingTalk Drive requires 3 steps:
1. **Get upload credentials** - Request signed URL and headers from DingTalk
2. **Upload to OSS** - PUT the file content to the provided URL
3. **Commit the file** - Notify DingTalk that upload is complete

## Step 1: Get Upload Credentials

```bash
curl -X POST "https://api.dingtalk.com/v2.0/storage/spaces/files/{parentDentryUuid}/uploadInfos/query?unionId={unionId}" \
  -H "x-acs-dingtalk-access-token: {TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "protocol": "HEADER_SIGNATURE",
    "option": {
      "storageDriver": "DINGTALK",
      "preCheckParam": {
        "size": {fileSizeInBytes},
        "name": "{fileName}"
      }
    }
  }'
```

**Returns:**
- `uploadKey` - Unique identifier for this upload (used in Step 3)
- `headerSignatureInfo.resourceUrls[0]` - OSS upload URL
- `headerSignatureInfo.headers` - Required headers (Authorization, x-oss-date)
- `expirationSeconds` - Credentials expire in 900 seconds (15 minutes)

**Getting parentDentryUuid:**
- For root directory: Use the folder's `uuid` field from `dentries/listAll` or `dentries/query`
- Root directory uuid can be queried with `dentryId: "0"`

## Step 2: Upload to OSS

```bash
curl -X PUT "{resourceUrl}" \
  -H "Authorization: {headers.Authorization}" \
  -H "x-oss-date: {headers.x-oss-date}" \
  -H "Content-Type:" \
  --data-binary @localfile.ext
```

**Important:**
- `Content-Type` header must be set to empty string (no content type)
- Use `--data-binary` for binary files
- HTTP 200 = success
- Credentials expire in 15 minutes, complete Step 3 before then

## Step 3: Commit the File

```bash
curl -X POST "https://api.dingtalk.com/v2.0/storage/spaces/files/{parentDentryUuid}/commit?unionId={unionId}" \
  -H "x-acs-dingtalk-access-token: {TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "uploadKey": "{uploadKey from Step 1}",
    "name": "{fileName}",
    "option": {
      "conflictStrategy": "AUTO_RENAME"
    }
  }'
```

**conflictStrategy options:**
- `AUTO_RENAME` - Auto rename if file exists (default)
- `OVERWRITE` - Overwrite existing file

**Returns:** File entry with `id`, `uuid`, `path`, `size`, etc.

## Creating a Text File Example

```bash
# 1. Create content
echo "Hello World" > /tmp/test.txt

# 2. Get upload credentials
RESP=$(curl -s -X POST "https://api.dingtalk.com/v2.0/storage/spaces/files/{parentUuid}/uploadInfos/query?unionId={unionId}" \
  -H "x-acs-dingtalk-access-token: {TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{"protocol":"HEADER_SIGNATURE","option":{"storageDriver":"DINGTALK","preCheckParam":{"size":12,"name":"test.txt"}}}')

# 3. Extract values
UPLOAD_KEY=$(echo $RESP | python3 -c "import json,sys; print(json.load(sys.stdin)['uploadKey'])")
RESOURCE_URL=$(echo $RESP | python3 -c "import json,sys; print(json.load(sys.stdin)['headerSignatureInfo']['resourceUrls'][0])")
AUTH=$(echo $RESP | python3 -c "import json,sys; print(json.load(sys.stdin)['headerSignatureInfo']['headers']['Authorization'])")
DATE=$(echo $RESP | python3 -c "import json,sys; print(json.load(sys.stdin)['headerSignatureInfo']['headers']['x-oss-date'])")

# 4. Upload to OSS
curl -s -X PUT "$RESOURCE_URL" \
  -H "Authorization: $AUTH" \
  -H "x-oss-date: $DATE" \
  -H "Content-Type:" \
  --data-binary @/tmp/test.txt

# 5. Commit
curl -s -X POST "https://api.dingtalk.com/v2.0/storage/spaces/files/{parentUuid}/commit?unionId={unionId}" \
  -H "x-acs-dingtalk-access-token: {TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"uploadKey\": \"$UPLOAD_KEY\", \"name\": \"test.txt\", \"option\": {\"conflictStrategy\": \"AUTO_RENAME\"}}"
```

## Large File Support

For files larger than 8MB, use multipart upload:
1. Call `/v1.0/storage/spaces/{spaceId}/files/multiPartUploadInfos/init` to initialize
2. Upload parts sequentially
3. Call commit to finalize

## Error Handling

- `400 param.error` - Check file size, name, or parentDentryUuid
- `403 Forbidden.AccessDenied` - Missing `Storage.File.Write` or `Storage.UploadInfo.Read` permission
- `403 no.priviledge` - User doesn't have write access to the folder
- Credentials timeout - Re-do Step 1 if 15 minutes have passed