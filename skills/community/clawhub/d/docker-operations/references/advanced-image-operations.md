# Advanced Image Operations

Advanced commands for extracting, manipulating, and analyzing Docker images.

## Extract Image Filesystem to Directory

Export a Docker image's filesystem contents to a local directory. This is useful for inspecting, debugging, or modifying image contents.

### Method 1: Using docker image save + tar

```bash
# Save image to tar and extract to directory
docker image save <image>:<tag> -o /tmp/image.tar
mkdir -p ./image-contents
tar -xf /tmp/image.tar -C ./image-contents
rm /tmp/image.tar
```

### Method 2: Using docker run with volume mount

```bash
# Create a container and copy its filesystem
docker create --name temp-container <image>:<tag>
docker cp temp-container:/ ./image-contents
docker rm temp-container
```

### Method 3: Using docker run --rm (one-liner)

```bash
# Extract using a temporary container
docker run --rm -v $(pwd)/output:/output <image>:<tag> sh -c 'cp -r /* /output 2>/dev/null || true'
```

> Note: Method 3 may include some non filesystem files (like /dev, /proc, /sys) that need cleanup.

## Extract Specific Layers from Image

Extract contents from specific image layers.

```bash
# Inspect image layer digests
docker image inspect --format '{{json .RootFS.Layers}}' <image>:<tag>

# Save only specific layers
docker image save <image>:<tag> | tar -xf - -C ./output <layer-tar-file>
```

## Image Filesystem Analysis

Analyze image contents without extracting full filesystem.

```bash
# List image contents using docker history
docker history <image>:<tag>

# Show image layers with sizes
docker image inspect --format '{{json .RootFS.Layers}}' <image>:<tag> | jq

# Get total image size
docker image inspect --format '{{.Size}}' <image>:<tag>
```

## Create Image from Extracted Filesystem

Create a new image from modified filesystem contents.

```bash
# Package extracted contents back to tar
cd ./image-contents && tar -cf ../modified-image.tar .
cd .. && docker import modified-image.tar my-custom-image:latest
```

## Difference Between docker export vs docker image save

| Aspect | `docker export` | `docker image save` |
|--------|-----------------|----------------------|
| Target | Container filesystem | Image and all layers |
| Output | Single tar of container | Tar containing layer files |
| Includes | Only container changes | Full image with history |
| Use case | Container migration | Image backup/transfer |

## Quick Reference

| Operation | Command |
|-----------|---------|
| Extract to directory | `docker image save <img> -o . && tar -xf - -C ./out` |
| Copy from container | `docker cp <container>:/ .` |
| List image layers | `docker image inspect --format '{{json .RootFS.Layers}}' <img>` |
| Package extracted back | `tar -cf img.tar . && docker import img.tar <new-img>` |
