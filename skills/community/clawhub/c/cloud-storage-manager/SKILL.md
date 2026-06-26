# cloud-storage-manager - 云存储管理器

SKILL.md for cloud-storage-manager

## Metadata

| Field | Value |
|-------|-------|
| **Name** | cloud-storage-manager |
| **Slug** | cloud-storage-manager |
| **Version** | 1.0.0 |
| **Homepage** | https://github.com/openclaw/cloud-storage-manager |
| **Category** | automation |
| **Tags** | cloud, storage, s3, oss, cos, aliyun, aws, azure, backup, sync |

## Description

### English
Universal cloud storage manager supporting multiple providers (AWS S3, Aliyun OSS, Tencent COS, Azure Blob). Features include file upload/download, bucket management, sync operations, multipart uploads, and CDN integration.

### 中文
通用云存储管理器，支持多种云服务商（AWS S3、阿里云OSS、腾讯云COS、Azure Blob）。功能包括文件上传下载、存储桶管理、同步操作、分片上传和CDN集成。

## Requirements

- Python 3.8+
- boto3 >= 1.26.0 (AWS S3)
- aliyun-python-sdk-oss >= 2.17.0 (Aliyun OSS)
- qcloud-cos-python-sdk-v5 >= 1.9.0 (Tencent COS)
- azure-storage-blob >= 12.14.0 (Azure Blob)

## Configuration

### Environment Variables
```bash
# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_BUCKET=my-bucket

# Aliyun OSS
ALIYUN_ACCESS_KEY_ID=your_key
ALIYUN_ACCESS_KEY_SECRET=your_secret
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
ALIYUN_OSS_BUCKET=my-bucket

# Tencent COS
TENCENT_SECRET_ID=your_id
TENCENT_SECRET_KEY=your_key
TENCENT_COS_REGION=ap-beijing
TENCENT_COS_BUCKET=my-bucket

# Azure
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_CONTAINER=my-container
```

## Usage

### Basic Example

```python
from cloud_storage_manager import StorageManager, Provider

# Initialize with Aliyun OSS
storage = StorageManager(Provider.ALIYUN_OSS)

# Upload file
storage.upload("local/file.txt", "remote/path/file.txt")

# Download file
storage.download("remote/path/file.txt", "local/downloaded.txt")

# List files
files = storage.list_objects(prefix="documents/")

# Delete file
storage.delete("remote/path/file.txt")

# Get signed URL (1 hour expiry)
url = storage.get_signed_url("private/file.txt", expires=3600)
```

### Sync Example

```python
from cloud_storage_manager import SyncManager

# Sync local directory to cloud
sync = SyncManager(storage)
sync.sync_to_cloud(
    local_dir="/path/to/local",
    remote_prefix="backup/2024/",
    exclude=["*.tmp", "*.log"],
    delete_remote=True  # Remove files not in local
)

# Sync from cloud to local
sync.sync_from_cloud(
    remote_prefix="data/",
    local_dir="/path/to/download",
    include=["*.csv", "*.json"]
)
```

### Multi-Provider Copy

```python
# Copy between different providers
source = StorageManager(Provider.AWS_S3)
dest = StorageManager(Provider.ALIYUN_OSS)

# Stream copy without downloading locally
from cloud_storage_manager import CrossProviderCopy
copier = CrossProviderCopy(source, dest)
copier.copy("s3/path/file.zip", "oss/path/file.zip")
```

## API Reference

### StorageManager
- `upload(local_path, remote_path)` - Upload file
- `download(remote_path, local_path)` - Download file
- `delete(remote_path)` - Delete file
- `exists(remote_path)` - Check if file exists
- `list_objects(prefix='')` - List files with prefix
- `get_size(remote_path)` - Get file size
- `get_signed_url(remote_path, expires)` - Get temporary URL
- `set_acl(remote_path, acl)` - Set access control

### SyncManager
- `sync_to_cloud(local_dir, remote_prefix, **options)` - Upload sync
- `sync_from_cloud(remote_prefix, local_dir, **options)` - Download sync
- `compare(local_dir, remote_prefix)` - Compare differences

## Examples

See `examples/` directory for complete examples.

## Testing

```bash
cd /root/.openclaw/workspace/skills/cloud-storage-manager
python -m pytest tests/ -v
```

## License

MIT License
