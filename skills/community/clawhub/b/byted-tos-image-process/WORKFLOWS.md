# Bytedance TOS Image Process Workflows

This document illustrates common end-to-end workflows for image processing using the TOS Python SDK and the scripts provided in this skill.

## Table of Contents
- [Workflow 1: Getting Image Information](#workflow-1-getting-image-information)
- [Workflow 2: Resizing an Image and Saving Locally](#workflow-2-resizing-an-image-and-saving-locally)
- [Workflow 3: Converting Format and Saving back to TOS](#workflow-3-converting-format-and-saving-back-to-tos)
- [Workflow 4: Applying a Text Watermark](#workflow-4-applying-a-text-watermark)
- [Workflow 5: Batch Processing Multiple Images](#workflow-5-batch-processing-multiple-images)
- [Workflow 6: Handling Errors](#workflow-6-handling-errors)

---

### Workflow 1: Getting Image Information

**Goal**: Retrieve the metadata (format, dimensions, etc.) of an image stored in TOS.

**Script**: `scripts/image_info.py`

1.  **Set Environment**:
    ```bash
    export TOS_ACCESS_KEY="YOUR_AK"
    export TOS_SECRET_KEY="YOUR_SK"
    export TOS_ENDPOINT="https://tos-cn-beijing.volces.com"
    export TOS_REGION="cn-beijing"
    export TOS_BUCKET="my-source-bucket"
    export TOS_OBJECT_KEY="images/archive/photo-01.jpg"
    ```

2.  **Execute**:
    ```bash
    python3 scripts/image_info.py
    ```

3.  **SDK Logic (`image_info.py`)**:
    ```python
    # Initializes client from env vars
    client = create_client()
    
    # Calls get_object with the specific process string
    response = client.get_object(
        bucket=os.getenv("TOS_BUCKET"),
        key=os.getenv("TOS_OBJECT_KEY"),
        process="image/info"
    )
    
    # Reads and parses the JSON response
    info = json.loads(response.read().decode('utf-8'))
    print(json.dumps(info, indent=2))
    ```

---

### Workflow 2: Resizing an Image and Saving Locally

**Goal**: Resize an image to a 500-pixel width and save the result to the local filesystem.

**Script**: `scripts/image_resize.py`

1.  **Set Environment**: (Same as Workflow 1)

2.  **Execute**:
    ```bash
    python3 scripts/image_resize.py --w 500 --output "resized_local.jpg"
    ```

3.  **SDK Logic (`image_resize.py`)**:
    ```python
    # Constructs the process string from CLI arguments
    process_rule = "image/resize,w_500"
    
    # Calls get_object_to_file to stream the result directly to a local file
    client.get_object_to_file(
        bucket=os.getenv("TOS_BUCKET"),
        key=os.getenv("TOS_OBJECT_KEY"),
        file_path="resized_local.jpg",
        process=process_rule
    )
    
    print("Image saved to resized_local.jpg")
    ```

---

### Workflow 3: Converting Format and Saving back to TOS

**Goal**: Convert an image to WebP format with 80% quality and save it to another location in TOS.

**Script**: `scripts/image_format.py`

1.  **Set Environment**: (Same as Workflow 1)

2.  **Execute**:
    ```bash
    python3 scripts/image_format.py \
      --f webp \
      --q 80 \
      --saveas-bucket "my-output-bucket" \
      --saveas-object "processed/photo-01.webp"
    ```

3.  **SDK Logic (`image_format.py`)**:
    ```python
    # Constructs the process string
    process_rule = "image/format,f_webp,q_80"
    
    # Calls get_object with save_bucket and save_object to persist in TOS
    response = client.get_object(
        bucket=os.getenv("TOS_BUCKET"),
        key=os.getenv("TOS_OBJECT_KEY"),
        process=process_rule,
        save_bucket="my-output-bucket",
        save_object="processed/photo-01.webp"
    )
    
    # The response contains JSON metadata about the saved object
    save_result = json.loads(response.read().decode('utf-8'))
    print("Save result:", save_result)
    ```

---

### Workflow 4: Applying a Text Watermark

**Goal**: Add a semi-transparent text watermark to the bottom-right corner of an image.

**Script**: `scripts/image_watermark.py`

1.  **Set Environment**: (Same as Workflow 1)

2.  **Prepare Parameters**: Watermark text and colors must be Base64-encoded.
    ```bash
    # Text: "© 2026 MyCorp"
    TEXT_B64=$(echo -n "© 2026 MyCorp" | base64)
    
    # Color: White (#FFFFFF)
    COLOR_B64=$(echo -n "#FFFFFF" | base64)
    ```

3.  **Execute**:
    ```bash
    python3 scripts/image_watermark.py \
      --kv type=1 \
      --kv text=${TEXT_B64} \
      --kv fill=${COLOR_B64} \
      --kv size=30 \
      --kv p=9 \
      --kv dx=20 \
      --kv dy=20 \
      --output "watermarked.jpg"
    ```
    *Note: The `kv` keys (`type`, `text`, `fill`, `size`, `p`, `dx`, `dy`) must match the official TOS documentation for text watermarks.*

4.  **SDK Logic (`image_watermark.py`)**:
    ```python
    # Constructs the process string from all --kv arguments
    process_rule = "image/watermark,type_1,text_wr...,fill_I0Z...,size_30,p_9,dx_20,dy_20"
    
    client.get_object_to_file(
        bucket=...,
        key=...,
        file_path="watermarked.jpg",
        process=process_rule
    )
    ```

---

### Workflow 5: Batch Processing Multiple Images

**Goal**: Resize a list of images from a source folder in TOS to a destination folder.

**This requires a custom script that iterates and calls the SDK.**

1.  **Set Environment**: (Same as Workflow 1, but `TOS_OBJECT_KEY` is not used).

2.  **Custom Batch Script (Conceptual)**:
    ```python
    import os
    import tos

    # Assumes client is initialized
    
    source_bucket = "my-source-bucket"
    dest_bucket = "my-output-bucket"
    image_keys = ["source/img1.jpg", "source/img2.jpg", "source/img3.jpg"]
    
    for key in image_keys:
        dest_key = key.replace("source/", "resized/")
        print(f"Processing {source_bucket}/{key} -> {dest_bucket}/{dest_key}")
        
        try:
            client.get_object(
                bucket=source_bucket,
                key=key,
                process="image/resize,w_1200",
                save_bucket=dest_bucket,
                save_object=dest_key
            )
        except tos.exceptions.TosServerError as e:
            print(f"  [ERROR] Failed for {key}: {e.message}")
    
    print("Batch processing complete.")
    ```

---

### Workflow 6: Handling Errors

**Goal**: Gracefully handle potential errors from the TOS SDK.

All provided scripts include `try...except` blocks to catch `TosServerError` and `TosClientError`.

**SDK Logic**:
```python
try:
    # ... SDK call ...
    client.get_object(bucket="non-existent-bucket", key="invalid-key", process="image/info")

except tos.exceptions.TosServerError as e:
    # For server-side errors (e.g., object not found, invalid parameters)
    print(f"TOS Server Error:")
    print(f"  - Status: {e.status_code}")
    print(f"  - Code: {e.code}")
    print(f"  - Message: {e.message}")
    print(f"  - Request ID: {e.request_id}")
    sys.exit(1)

except tos.exceptions.TosClientError as e:
    # For client-side issues (e.g., network error, invalid credentials)
    print(f"TOS Client Error: {e}")
    sys.exit(1)
```
This ensures that failures are caught and reported with meaningful diagnostic information, such as the `request_id`, which is crucial for troubleshooting with support teams.
