# 传输脚本

使用 `scripts/filemanager_transfer.py` 上传文件、创建带密码的分享链接，或按 FileManager 文件 ID 下载文件。

脚本会读取 `scripts/.env`，也支持从 `FILEMANAGER_*` 环境变量读取配置：

```env
FILEMANAGER_BASE_URL=http://localhost:8080
FILEMANAGER_APPKEY=fm_app_xxxxxxxxxxxxxxxxx
```

## 上传并创建分享

默认情况下，上传完成后会创建带密码的分享链接。必须提供非空 `--password`。

```bash
python scripts/filemanager_transfer.py upload /path/to/file --remote-dir / --password "share-password"
```

带备注、有效期和下载次数限制：

```bash
python scripts/filemanager_transfer.py upload /path/to/file --remote-dir /docs --remark "handoff" --password "share-password" --expires-hours 24 --max-downloads 5
```

成功后输出 JSON，包含：

- `uploaded`：上传后的文件信息，包括 ID、名称、路径和大小。
- `share.url`：可发给用户的分享链接。
- `share.password`：本次分享密码。
- `share.expires_at`：服务端返回的过期时间。
- `share.share_id`：服务端返回的分享 ID。

## 只上传不分享

仅当不需要分享链接时，才使用只上传模式：

```bash
python scripts/filemanager_transfer.py upload /path/to/file --remote-dir / --password "placeholder" --no-share
```

当前脚本仍然要求传入 `--password`，因为上传命令默认用于创建分享。

## 按文件 ID 下载

```bash
python scripts/filemanager_transfer.py download <file_id> --output /path/to/save
```

如果省略 `--output`，脚本会写入当前目录。如果 `--output` 是已存在目录，脚本会优先使用服务端返回的文件名。
