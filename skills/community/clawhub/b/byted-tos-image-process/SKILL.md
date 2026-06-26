---
name: byted-tos-image-process
version: 1.0.0
description: Provides image processing capabilities for objects in Bytedance TOS using the official SDK. Supports getting image info, format conversion, resizing, and watermarking. Use when you need to analyze or transform images stored in TOS.
homepage: https://www.volcengine.com/docs/6349/153623
---

# Bytedance TOS Image Process Skill

This skill provides essential image processing functions for files stored in Bytedance's TOS (TeraObjectStore). It allows you to retrieve image metadata, convert formats, resize, and apply watermarks directly using the Volcengine TOS SDK.

## Quick Start

### 1. Client Initialization

The following Python snippet demonstrates how to initialize the `TosClientV2` from environment variables.

```python
import os
import tos
from tos.exceptions import TosClientError, TosServerError

def create_client() -> tos.TosClientV2:
    """Initializes a TosClientV2 using AK/SK (and optional STS token) from environment variables."""
    try:
        ak = os.getenv('TOS_ACCESS_KEY')
        sk = os.getenv('TOS_SECRET_KEY')
        endpoint = os.getenv('TOS_ENDPOINT')
        region = os.getenv('TOS_REGION')
        security_token = os.getenv('TOS_SECURITY_TOKEN') # Optional, for STS

        if not all([ak, sk, endpoint, region]):
            raise ValueError("Required environment variables are missing (AK, SK, Endpoint, Region).")

        return tos.TosClientV2(
            ak=ak,
            sk=sk,
            endpoint=endpoint,
            region=region,
            security_token=security_token,
        )
    except (ValueError, ImportError) as e:
        print(f"Error initializing client: {e}")
        return None

# Create the client
client = create_client()
```

### 2. Basic Workflow

```python
# (Assumes 'client' is initialized and 'bucket_name', 'object_key' are set)

# 1. Get Image Info
try:
    response = client.get_object(bucket_name, object_key, process="image/info")
    info_data = response.read()
    print("Image Info:", info_data.decode('utf-8'))
except TosServerError as e:
    print(f"Error getting image info: {e}")

# 2. Resize an Image and save locally
try:
    client.get_object_to_file(
        bucket_name,
        object_key,
        "resized_image.jpg",
        process="image/resize,w_500,m_lfit" # Resize to 500px width, lfit mode
    )
    print("Resized image saved to resized_image.jpg")
except TosServerError as e:
    print(f"Error resizing image: {e}")

# 3. Convert Image to WebP and save back to TOS
try:
    response = client.get_object(
        bucket_name,
        object_key,
        process="image/format,f_webp,q_80", # Convert to WebP, quality 80
        save_bucket="my-output-bucket",
        save_object="processed/image.webp"
    )
    save_result = response.read()
    print("Converted image saved to TOS:", save_result.decode('utf-8'))
except TosServerError as e:
    print(f"Error saving converted image to TOS: {e}")
```

## Core Operations

All image processing is achieved by passing a `process` string to the `get_object` or `get_object_to_file` SDK methods.

### 1. Get Image Info (`ImageInfo`)

Retrieves metadata of an image file, such as format, dimensions, and EXIF data.

**SDK Method**: `client.get_object(..., process="image/info")`

```python
response = client.get_object(bucket_name, object_key, process="image/info")
image_metadata = response.read().decode('utf-8')
print(image_metadata)
```

### 2. Convert Image Format (`ImageFormat`)

Converts an image to a different format (e.g., JPEG, PNG, WebP) and adjusts quality.

**SDK Method**: `client.get_object_to_file(..., process="image/format,f_webp,q_80")`

```python
# Convert to PNG format
client.get_object_to_file(
    bucket_name,
    object_key,
    "output.png",
    process="image/format,f_png"
)
```

### 3. Resize Image (`ImageResize`)

Resizes an image based on specified width, height, and resizing mode.

**SDK Method**: `client.get_object_to_file(..., process="image/resize,w_800,h_600,m_fill")`

```python
# Resize to a maximum width of 1024px, maintaining aspect ratio
client.get_object_to_file(
    bucket_name,
    object_key,
    "resized_1024.jpg",
    process="image/resize,w_1024"
)
```

### 4. Apply Watermark (`ImageWatermark` & `ImageBlindWatermark`)

Adds a visible or blind watermark to an image. Parameters are complex and should be constructed according to the official TOS documentation.

**SDK Method**: `client.get_object_to_file(..., process="image/watermark,...")`

```python
# Example for a text watermark (parameters must be Base64-encoded)
# This is a conceptual example. Refer to official docs for exact keys.
import base64
text_b64 = base64.b64encode("My Watermark".encode()).decode()
process_rule = f"image/watermark,type_1,text_{text_b64},size_40,p_9"

client.get_object_to_file(
    bucket_name,
    object_key,
    "watermarked.jpg",
    process=process_rule
)
```

### 5. Generic Image Processing (`ImageProcess`)

A flexible entry point that accepts any valid image processing string.

**SDK Method**: `client.get_object(..., process="<full-process-string>")`

```python
# Example: Apply a Gaussian blur (hypothetical parameters)
client.get_object_to_file(
    bucket_name,
    object_key,
    "blurred.jpg",
    process="image/blur,r_5,s_2"
)
```

## Authorization

Authentication is handled by `tos.TosClientV2`. Provide credentials via environment variables.

### Required Environment Variables
- `TOS_ACCESS_KEY`
- `TOS_SECRET_KEY`
- `TOS_ENDPOINT`
- `TOS_REGION`

### Optional for STS
- `TOS_SECURITY_TOKEN`

## Best Practices
- **Error Handling**: Wrap SDK calls in `try...except` blocks to handle `TosClientError` and `TosServerError`.
- **Parameter Construction**: For complex operations like watermarking, carefully construct the `process` string according to the official TOS documentation. Base64-encode parameter values where required.
- **Client Reuse**: Initialize the `TosClientV2` once and reuse it for multiple operations.

## Additional Resources

- For detailed parameters of each operation, see [REFERENCE.md](REFERENCE.md).
- For common end-to-end examples, see [WORKFLOWS.md](WORKFLOWS.md).
- For executable Python examples, see the `scripts/` directory.
- **For the definitive list of all processing parameters, always consult the official Volcengine TOS Image Processing documentation.**
