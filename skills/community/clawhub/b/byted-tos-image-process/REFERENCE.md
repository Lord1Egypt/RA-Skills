# Bytedance TOS Image Process SDK Reference

This document provides a reference for the parameters and return values of the core image processing operations, as implemented via the Volcengine TOS Python SDK.

**Crucial Note**: The image processing capabilities of TOS are extensive. This document covers the high-level structure and common parameters. For an exhaustive list of all parameters, options, and their exact syntax (e.g., for watermarks, custom cuts), **you must refer to the official Volcengine TOS image processing documentation.**

## Table of Contents
- [Authentication](#authentication)
- [Core Operations](#core-operations)
  - [1. `ImageInfo`](#1-imageinfo)
  - [2. `ImageFormat`](#2-imageformat)
  - [3. `ImageResize`](#3-imageresize)
  - [4. `ImageWatermark`](#4-imagewatermark)
  - [5. `ImageBlindWatermark`](#5-imageblindwatermark)
  - [6. `ImageProcess` (Generic)](#6-imageprocess-generic)
- [Data Models](#data-models)
  - [ImageInfo Object](#imageinfo-object)
  - [ProcessSaveResult Object](#processsaveresult-object)

---

## Authentication

Authentication is handled automatically by the `tos.TosClientV2` client during initialization. Credentials should be provided via environment variables as described in the `README.md`.

---

## Core Operations

Image processing is invoked by passing a specially formatted `process` string to the `get_object`, `get_object_to_file`, or other relevant methods of the TOS SDK client.

### 1. `ImageInfo`

Retrieves metadata for a specified image object in TOS.

**Process String:** `image/info`

**SDK Method:** `client.get_object()`

**Key Parameters:**

| Parameter | Type   | Required | Description                                    |
|-----------|--------|----------|------------------------------------------------|
| `bucket`  | string | Yes      | The name of the bucket containing the image.   |
| `key`     | string | Yes      | The full object key (path) of the image file.  |
| `process` | string | Yes      | Must be the exact string `"image/info"`.       |

**Success Response:**
- The SDK response body contains a `bytes` object with a JSON string.
- This JSON string represents the [ImageInfo Object](#imageinfo-object).

### 2. `ImageFormat`

Converts the image to a different format and/or adjusts its quality.

**Process String:** `image/format,f_<format>,q_<quality>`

**Common Options:**

| Option | SDK Equivalent    | Description                                       |
|--------|-------------------|---------------------------------------------------|
| `f`    | `format` (string) | Target format. Common values: `jpg`, `png`, `webp`. |
| `q`    | `quality` (int)   | Quality for lossy formats (e.g., 1-100 for JPG).  |

**Example `process` string:** `"image/format,f_webp,q_85"`

### 3. `ImageResize`

Resizes an image with various scaling options.

**Process String:** `image/resize,w_<width>,h_<height>,m_<mode>`

**Common Options:**

| Option | SDK Equivalent | Description                                                               |
|--------|----------------|---------------------------------------------------------------------------|
| `w`    | `width` (int)  | Target width in pixels.                                                   |
| `h`    | `height` (int) | Target height in pixels.                                                  |
| `m`    | `mode` (string)| Resize mode (e.g., `lfit`, `mfit`, `fill`, `fixed`). See official docs for all modes. |

**Example `process` string:** `"image/resize,w_800,m_lfit"` (Resize to width 800, maintain aspect ratio)

### 4. `ImageWatermark`

Applies a visible watermark (text or image) to the image. The parameter set is extensive.

**Process String:** `image/watermark,<param1>_<value1>,<param2>_<value2>,...`

**Conceptual Parameters (refer to official docs for actual keys and values):**

- `type`: Type of watermark (e.g., text, image).
- `text`/`image`: The content of the watermark. **Values must be Base64-encoded.**
- `size`/`font`: Font size or image size.
- `color`/`fill`: Color of the text.
- `p`: Position of the watermark (e.g., `1` for top-left, `9` for bottom-right).
- `dx`/`dy`: Offsets in pixels.

**Example `process` string (conceptual):** `"image/watermark,type_1,text_SGVsbG8gV29ybGQ=,p_9,size_40"`

### 5. `ImageBlindWatermark`

Adds or extracts a blind (invisible) watermark.

**Process String:** `image/blindwatermark,<param1>_<value1>,...`

**Conceptual Parameters (refer to official docs):**

- `type`: Operation type (e.g., `1` for encoding, `2` for decoding).
- `text`/`image`: Watermark content to embed (Base64-encoded).

### 6. `ImageProcess` (Generic)

This is not a specific operation but a generic entry point to use any process string. It allows for combining operations or using newly introduced features not explicitly covered by the other scripts.

**Example `process` string (chaining resize and format):** `"image/resize,w_500|image/format,f_png"` (Syntax may vary, check official docs for chaining rules).

---

## Data Models

### ImageInfo Object

A JSON object containing detailed information about the image, as returned by the `image/info` process.

| Field       | Type   | Description                                   |
|-------------|--------|-----------------------------------------------|
| `Format`    | string | The format of the image (e.g., "jpeg", "png"). |
| `ImageWidth`| int    | The width of the image in pixels.             |
| `ImageHeight`| int   | The height of the image in pixels.            |
| `FileSize`  | int    | The size of the image file in bytes.          |
| `Orientation`| int   | The EXIF orientation tag.                     |
| `...`       | ...    | Other fields may be present (e.g., EXIF data).|

**Example Snippet:**
```json
{
  "FileSize": {
    "Value": "102400"
  },
  "Format": {
    "Value": "jpeg"
  },
  "ImageHeight": {
    "Value": "800"
  },
  "ImageWidth": {
    "Value": "1200"
  }
}
```

### ProcessSaveResult Object

A JSON object returned when an image processing operation is successfully saved directly to TOS using the `save_bucket` and `save_object` parameters.

| Field           | Type   | Description                                           |
|-----------------|--------|-------------------------------------------------------|
| `ETag`          | string | The ETag of the saved object.                         |
| `Bucket`        | string | The bucket where the result was saved.                |
| `Object`        | string | The object key of the saved result.                   |
| `VersionId`     | string | The version ID if the bucket has versioning enabled.  |
| `HashCrc64ecma` | string | The CRC64 checksum of the object.                     |
