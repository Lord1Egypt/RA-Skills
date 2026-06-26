# Storage Packs

This document describes packs in the `storage` category.

## Packs in this Category

- [AWS S3](#storages3)
- [Google Cloud Storage](#storagegcs)
- [MinIO](#storageminio)
- [Azure Blob Storage](#storageazure_blob)

---

## AWS S3

**Pack ID:** `storage.s3`

Protects against destructive S3 operations like bucket removal, recursive deletes, and sync --delete.

### Keywords

Commands containing these keywords are checked against this pack:

- `s3`
- `s3api`
- `rb`
- `delete-bucket`
- `delete-object`
- `delete-objects`
- `--delete`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `s3-list` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3\s+ls\b` |
| `s3-copy` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3\s+cp\b` |
| `s3-presign` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3\s+presign\b` |
| `s3-mb` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3\s+mb\b` |
| `s3api-list-objects` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3api\s+list-objects(?:-v2)?\b` |
| `s3api-get-object` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3api\s+get-object\b` |
| `s3api-head-object` | `aws(?:\s+--?\S+(?:\s+\S+)?)*\s+s3api\s+head-object\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `s3-rb` | aws s3 rb removes an S3 bucket and is destructive. | high |
| `s3-rm` | aws s3 rm deletes S3 objects and is destructive. | high |
| `s3-sync-delete` | aws s3 sync --delete removes destination objects not in source. | high |
| `s3api-delete-bucket` | aws s3api delete-bucket permanently deletes a bucket. | high |
| `s3api-delete-object` | aws s3api delete-object permanently deletes an object. | high |
| `s3api-delete-objects` | aws s3api delete-objects permanently deletes multiple objects. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "storage.s3:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "storage.s3:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Google Cloud Storage

**Pack ID:** `storage.gcs`

Protects against destructive GCS operations like bucket removal, object deletion, and recursive deletes.

### Keywords

Commands containing these keywords are checked against this pack:

- `gsutil`
- `gcloud storage`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `gsutil-ls` | `gsutil\s+(?:-[a-zA-Z]+\s+)*ls\b` |
| `gsutil-cat` | `gsutil\s+(?:-[a-zA-Z]+\s+)*cat\b` |
| `gsutil-stat` | `gsutil\s+(?:-[a-zA-Z]+\s+)*stat\b` |
| `gsutil-du` | `gsutil\s+(?:-[a-zA-Z]+\s+)*du\b` |
| `gsutil-hash` | `gsutil\s+(?:-[a-zA-Z]+\s+)*hash\b` |
| `gsutil-version` | `gsutil\s+(?:-[a-zA-Z]+\s+)*version\b` |
| `gsutil-help` | `gsutil\s+(?:-[a-zA-Z]+\s+)*help\b` |
| `gsutil-cp` | `gsutil\s+(?:-[a-zA-Z]+\s+)*cp\b` |
| `gcloud-storage-buckets-list` | `gcloud\s+storage\s+buckets\s+list\b` |
| `gcloud-storage-buckets-describe` | `gcloud\s+storage\s+buckets\s+describe\b` |
| `gcloud-storage-objects-list` | `gcloud\s+storage\s+objects\s+list\b` |
| `gcloud-storage-objects-describe` | `gcloud\s+storage\s+objects\s+describe\b` |
| `gcloud-storage-ls` | `gcloud\s+storage\s+ls\b` |
| `gcloud-storage-cat` | `gcloud\s+storage\s+cat\b` |
| `gcloud-storage-cp` | `gcloud\s+storage\s+cp\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `gsutil-rb` | gsutil rb removes a GCS bucket. | high |
| `gsutil-rm` | gsutil rm deletes objects from GCS. | high |
| `gsutil-rsync-delete` | gsutil rsync -d deletes destination objects not in source. | high |
| `gcloud-storage-buckets-delete` | gcloud storage buckets delete removes a GCS bucket. | high |
| `gcloud-storage-objects-delete` | gcloud storage objects delete removes objects from GCS. | high |
| `gcloud-storage-rm` | gcloud storage rm removes objects from GCS. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "storage.gcs:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "storage.gcs:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## MinIO

**Pack ID:** `storage.minio`

Protects against destructive MinIO Client (mc) operations like bucket removal, object deletion, and admin operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `mc`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `mc-ls` | `\bmc\s+(?:--\S+\s+)*ls\b` |
| `mc-cat` | `\bmc\s+(?:--\S+\s+)*cat\b` |
| `mc-head` | `\bmc\s+(?:--\S+\s+)*head\b` |
| `mc-stat` | `\bmc\s+(?:--\S+\s+)*stat\b` |
| `mc-cp` | `\bmc\s+(?:--\S+\s+)*cp\b` |
| `mc-diff` | `\bmc\s+(?:--\S+\s+)*diff\b` |
| `mc-find` | `\bmc\s+(?:--\S+\s+)*find\b` |
| `mc-du` | `\bmc\s+(?:--\S+\s+)*du\b` |
| `mc-version` | `\bmc\s+(?:--\S+\s+)*version\b` |
| `mc-help` | `\bmc\s+(?:--\S+\s+)*(?:--help\|-h)\b` |
| `mc-admin-info` | `\bmc\s+(?:--\S+\s+)*admin\s+info\b` |
| `mc-admin-user-list` | `\bmc\s+(?:--\S+\s+)*admin\s+user\s+list\b` |
| `mc-admin-policy-list` | `\bmc\s+(?:--\S+\s+)*admin\s+policy\s+list\b` |
| `mc-alias-list` | `\bmc\s+(?:--\S+\s+)*alias\s+list\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `mc-rb` | mc rb removes a MinIO bucket. | high |
| `mc-rm` | mc rm deletes objects from MinIO. | high |
| `mc-admin-bucket-delete` | mc admin bucket delete removes a bucket via admin API. | high |
| `mc-mirror-remove` | mc mirror --remove deletes destination objects not in source. | high |
| `mc-admin-user-remove` | mc admin user remove/disable affects user access. | high |
| `mc-admin-policy-remove` | mc admin policy remove/unset modifies access policies. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "storage.minio:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "storage.minio:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Azure Blob Storage

**Pack ID:** `storage.azure_blob`

Protects against destructive Azure Blob Storage operations like container deletion, blob deletion, and azcopy remove.

### Keywords

Commands containing these keywords are checked against this pack:

- `az storage`
- `azcopy`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `az-storage-container-list` | `\baz\s+storage\s+container\s+list\b` |
| `az-storage-container-show` | `\baz\s+storage\s+container\s+show\b` |
| `az-storage-container-exists` | `\baz\s+storage\s+container\s+exists\b` |
| `az-storage-blob-list` | `\baz\s+storage\s+blob\s+list\b` |
| `az-storage-blob-show` | `\baz\s+storage\s+blob\s+show\b` |
| `az-storage-blob-exists` | `\baz\s+storage\s+blob\s+exists\b` |
| `az-storage-blob-download` | `\baz\s+storage\s+blob\s+download\b` |
| `az-storage-blob-download-batch` | `\baz\s+storage\s+blob\s+download-batch\b` |
| `az-storage-blob-url` | `\baz\s+storage\s+blob\s+url\b` |
| `az-storage-blob-metadata-show` | `\baz\s+storage\s+blob\s+metadata\s+show\b` |
| `az-storage-account-list` | `\baz\s+storage\s+account\s+list\b` |
| `az-storage-account-show` | `\baz\s+storage\s+account\s+show\b` |
| `az-storage-account-keys-list` | `\baz\s+storage\s+account\s+keys\s+list\b` |
| `azcopy-list` | `\bazcopy\s+(?:--\S+\s+)*list\b` |
| `azcopy-copy` | `\bazcopy\s+(?:--\S+\s+)*copy\b` |
| `azcopy-jobs-list` | `\bazcopy\s+(?:--\S+\s+)*jobs\s+list\b` |
| `azcopy-jobs-show` | `\bazcopy\s+(?:--\S+\s+)*jobs\s+show\b` |
| `azcopy-login` | `\bazcopy\s+(?:--\S+\s+)*login\b` |
| `azcopy-env` | `\bazcopy\s+(?:--\S+\s+)*env\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `az-storage-container-delete` | az storage container delete removes an Azure storage container. | high |
| `az-storage-blob-delete-batch` | az storage blob delete-batch removes multiple blobs from Azure storage. | high |
| `az-storage-blob-delete` | az storage blob delete removes a blob from Azure storage. | high |
| `az-storage-account-delete` | az storage account delete removes an entire Azure storage account. | high |
| `azcopy-remove` | azcopy remove deletes files from Azure storage. | high |
| `azcopy-sync-delete` | azcopy sync --delete-destination removes destination files not in source. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "storage.azure_blob:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "storage.azure_blob:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

