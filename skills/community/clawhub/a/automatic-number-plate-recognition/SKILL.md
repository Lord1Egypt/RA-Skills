---
name: trafficeye-license-plate
description: Detect and read the largest license plate from an image using the TrafficEye REST API. Use when the user wants ANPR, ALPR, license plate OCR, number plate reading, or to extract a plate from a local image file. You can obtain API key and tokens from https://trafficeye.ai.
metadata:
  openclaw:
    requires:
      env:
        - TRAFFICEYE_API_KEY
        - TRAFFICEYE_API_URL
        - TRAFFICEYE_API_KEY_MODE
        - TRAFFICEYE_API_KEY_NAME
        - TRAFFICEYE_FILE_FIELD
        - TRAFFICEYE_REQUEST_FIELD
        - TRAFFICEYE_REQUEST_JSON
        - TRAFFICEYE_TIMEOUT_S
      anyBins:
        - python3
        - python
    primaryEnv: TRAFFICEYE_API_KEY
    homepage: https://trafficeye.ai
    os:
      - linux
      - macos
      - windows
---

# TrafficEye License Plate Reader

Use this skill when the user wants to read a license plate from an image with the TrafficEye API.

## What This Skill Does

1. Accepts a local image path.
2. Uploads the image to the TrafficEye recognition API.
3. Optionally sends a `request` form field if `TRAFFICEYE_REQUEST_JSON` is configured.
4. Parses the API response.
5. Picks the largest detected plate by polygon area.
6. Returns the full selected plate payload to the user, including text, type (country), dimension, scores, occlusion, unreadable, and position.

## Expected Input

- A local image file path.
- If the user supplied an attachment instead of a path, first resolve it to a local file path and then run the helper.

## Default Runtime Assumptions

- The API endpoint defaults to `https://trafficeye.ai/recognition`.
- The default request payload is `{"tasks":["DETECTION","OCR"],"requestedDetectionTypes":["BOX","PLATE"]}`.
- The default API-key transport matches the TrafficEye public API example: header mode with header name `apikey`.
- Auth and request fields remain configurable in case your deployment differs.

## Environment Variables

- `TRAFFICEYE_API_KEY`: required unless passed explicitly to the helper.
- `TRAFFICEYE_API_URL`: optional, defaults to `https://trafficeye.ai/recognition`.
- `TRAFFICEYE_API_KEY_MODE`: one of `header`, `bearer`, `form`, `query`. Default: `header`.
- `TRAFFICEYE_API_KEY_NAME`: key name for `header`, `form`, or `query` mode. Default: `apikey`.
- `TRAFFICEYE_FILE_FIELD`: multipart field for the image. Default: `file`.
- `TRAFFICEYE_REQUEST_FIELD`: multipart field for the JSON request. Default: `request`.
- `TRAFFICEYE_REQUEST_JSON`: JSON string to include as the request field. By default this is `{"tasks":["DETECTION","OCR"],"requestedDetectionTypes":["BOX","PLATE"]}`.
- `TRAFFICEYE_TIMEOUT_S`: optional timeout in seconds. Default: `30`.

## How To Run

Setup your API key:
```bash
export TRAFFICEYE_API_KEY='YOUR_REAL_KEY'
```

Use the bundled helper:

```bash
python3 recognize_plate.py /absolute/path/to/image.jpg
```

For structured output:

```bash
python3 recognize_plate.py /absolute/path/to/image.jpg --format json
```

If the deployment expects Bearer auth:

```bash
TRAFFICEYE_API_KEY_MODE=bearer python3 recognize_plate.py /absolute/path/to/image.jpg
```

If the deployment needs an explicit request payload:

```bash
TRAFFICEYE_REQUEST_JSON='{"requestedDetectionTypes":["PLATE"]}' python3 recognize_plate.py /absolute/path/to/image.jpg --format json
```

Equivalent to the documented public API example:

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -H "apikey: YOUR_API_KEY_HERE" \
  -F "file=@image.jpg" \
  -F 'request={"tasks":["DETECTION","OCR"],"requestedDetectionTypes":["BOX","PLATE"]}' \
  https://trafficeye.ai/recognition
```

## Agent Workflow

1. Verify that the image path exists.
2. Run `python3 recognize_plate.py <image-path> --format json`.
3. Present the full selected plate payload to the user, especially `text`, `type`, `dimension`, `occlusion`, `unreadable`, and `position`.
4. If the API returns no readable text, explain that the largest plate was found but OCR text was missing.
5. If authentication fails, ask the user which auth mode their deployment expects and retry with the matching environment variables.

## Offline Validation

You can validate the selection logic without calling the API:

```bash
python3 recognize_plate.py --response-json-file examples/sample_response.json --format json
```

## Notes

- The helper intentionally chooses the largest plate by geometric area, not by detection confidence.
- The response parser first checks `combinations[].roadUsers[].plates[]`, then also supports `roadUsers[].plates[]`, top-level `plates[]`, and nested plate payloads discovered recursively.
- The default request and auth header mirror the public example at `https://www.trafficeye.ai/api`.
- The selected result now includes the original plate payload from the API so country/type and all scores are preserved.