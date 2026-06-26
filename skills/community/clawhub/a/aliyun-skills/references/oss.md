# OSS (Object Storage Service) Reference

OSS is best managed with the dedicated **ossutil** tool rather than `aliyun oss`.
Both are available after installing aliyun-cli, but ossutil has a richer feature set.

## Install ossutil

```bash
# macOS (Homebrew)
brew install ossutil

# Or download binary from:
# https://help.aliyun.com/zh/oss/developer-reference/install-and-configure-ossutil
```

## Configure ossutil

```bash
ossutil config
# Prompts for: endpoint, access key ID, access key secret, STS token (optional)
```

Common endpoint format: `https://oss-<region>.aliyuncs.com`
Example: `https://oss-cn-hangzhou.aliyuncs.com`

---

## Buckets

### List Buckets

```bash
ossutil ls
```

### Create a Bucket

```bash
ossutil mb oss://my-bucket --region cn-hangzhou
```

With ACL:
```bash
ossutil mb oss://my-bucket --region cn-hangzhou --acl private
```

### Delete a Bucket

> ⚠️ Delete all objects first, or use `--all-versions` for versioned buckets.

```bash
# Delete all objects first
ossutil rm oss://my-bucket --all-type --recursive --force

# Then delete the bucket
ossutil rb oss://my-bucket
```

### Get Bucket Info

```bash
ossutil stat oss://my-bucket
```

---

## Objects

### List Objects

```bash
# List root level
ossutil ls oss://my-bucket

# List recursively (all objects)
ossutil ls oss://my-bucket --recursive

# List a prefix
ossutil ls oss://my-bucket/logs/
```

### Upload a File

```bash
# Upload single file
ossutil cp /local/file.txt oss://my-bucket/file.txt

# Upload directory recursively
ossutil cp /local/dir/ oss://my-bucket/dir/ --recursive
```

With progress and parallel threads:
```bash
ossutil cp /local/large-file.tar.gz oss://my-bucket/ \
  --parallel 5 \
  --part-size 104857600
```

### Download a File

```bash
# Download single object
ossutil cp oss://my-bucket/file.txt /local/file.txt

# Download directory
ossutil cp oss://my-bucket/dir/ /local/dir/ --recursive
```

### Copy/Move Objects

```bash
# Copy within same bucket
ossutil cp oss://my-bucket/src.txt oss://my-bucket/dst.txt

# Copy across buckets
ossutil cp oss://bucket-a/file.txt oss://bucket-b/file.txt

# Move (copy + delete source)
ossutil mv oss://my-bucket/old.txt oss://my-bucket/new.txt
```

### Sync a Directory

```bash
# Upload (local → OSS)
ossutil sync /local/dir/ oss://my-bucket/dir/

# Download (OSS → local)
ossutil sync oss://my-bucket/dir/ /local/dir/

# Delete objects in destination that no longer exist in source
ossutil sync /local/dir/ oss://my-bucket/dir/ --delete
```

### Delete Objects

```bash
# Delete single object
ossutil rm oss://my-bucket/file.txt

# Delete all objects matching a prefix
ossutil rm oss://my-bucket/logs/ --recursive --force
```

### Object Metadata / Properties

```bash
# Show object metadata
ossutil stat oss://my-bucket/file.txt

# Set object ACL
ossutil set-acl oss://my-bucket/file.txt public-read

# Set storage class (change tier)
ossutil set-meta oss://my-bucket/file.txt \
  "X-Oss-Storage-Class:Archive" --update
```

---

## Presigned URLs

Generate a time-limited download URL (no auth required for downloader):

```bash
# Valid for 3600 seconds (1 hour)
ossutil sign oss://my-bucket/file.txt --timeout 3600
```

---

## Storage Classes

| Class | Use Case |
|-------|----------|
| `Standard` | Frequently accessed data |
| `IA` (Infrequent Access) | Monthly access, lower cost |
| `Archive` | Rarely accessed, lowest cost, needs restore |
| `ColdArchive` | Long-term archival |

### Restore an Archived Object

```bash
ossutil restore oss://my-bucket/archived-file.tar.gz
```

---

## Bucket ACL Values

| ACL | Meaning |
|-----|---------|
| `private` | Only owner can read/write |
| `public-read` | Anyone can read, only owner can write |
| `public-read-write` | Anyone can read and write |

---

## Using `aliyun oss` (Basic Operations)

For simple bucket/object operations when ossutil is not available:

```bash
# List buckets
aliyun oss ls

# List objects in a bucket
aliyun oss ls oss://my-bucket/

# Upload
aliyun oss cp /local/file.txt oss://my-bucket/

# Download
aliyun oss cp oss://my-bucket/file.txt /local/
```
