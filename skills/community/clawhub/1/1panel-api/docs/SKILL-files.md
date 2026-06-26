# File - 1Panel API

## 模块说明
File 模块接口，提供文件管理功能，包括上传、下载、复制、移动、压缩等操作。

## 文件路径说明

### 1Panel 目录结构

| 路径类型 | 说明 | 默认位置 |
|----------|------|----------|
| **网站根目录** | 网站文件存放目录 | `/opt/1panel/www/sites/{网站名称}/index` |
| **应用目录** | 已安装应用的目录 | `/opt/1panel/apps/{应用Key}/{应用名称}` |
| **备份目录** | 备份文件存放目录 | `/opt/1panel/backup/{类型}` |
| **日志目录** | 系统和应用日志目录 | `/opt/1panel/logs/{类型}` |
| **数据库目录** | 数据库数据存放目录 | `/opt/1panel/mysql/{数据库名称}` |
| **Redis 目录** | Redis 数据存放目录 | `/opt/1panel/redis/{实例名称}` |

### 常用文件操作路径

| 操作类型 | API | 说明 |
|----------|-----|------|
| **下载文件** | `GET /files/download` | 通过 `path` 参数指定文件路径 |
| **上传文件** | `POST /files/upload` | 上传到指定目录 |
| **批量下载** | `POST /files/chunkdownload` | 支持大文件分块下载 |
| **批量上传** | `POST /files/chunkupload` | 支持大文件分块上传 |
| **读取文件** | `POST /files/content` | 获取文件内容 |
| **保存文件** | `POST /files/save` | 保存或创建文件 |

### 路径参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| path | 文件或目录的完整绝对路径 | `/opt/1panel/www/mywebsite/index.html` |
| name | 文件或目录名称 | `index.html` |
| dir | 目录路径 | `/opt/1panel/www/mywebsite` |

### 源码位置

- **路由**: `/agent/router/ro_file.go`
- **API Handler**: `/agent/app/api/v2/file.go`
- **DTO**: `/agent/app/dto/file.go`, `/agent/app/dto/request/file.go`

## 接口列表 (37 个)

---

### GET /files/download
**功能**: Download file

**Query 参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件路径 | 任意有效文件路径 |

---

### GET /files/recycle/status
**功能**: Get RecycleBin status

**参数**: 无

---

### POST /files
**功能**: Create file

**Body 参数** (FileCreate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件或目录的完整路径 | 任意有效路径 |
| content | string | 否 | 文件内容 | 任意文本内容 |
| isDir | bool | 否 | 是否创建目录 | true/false |
| mode | int64 | 否 | 权限模式 | 八进制权限值，如 0755 |
| isLink | bool | 否 | 是否为链接 | true/false |
| isSymlink | bool | 否 | 是否为符号链接 | true/false |
| linkPath | string | 否 | 符号链接目标路径 | 任意有效路径 |
| sub | bool | 否 | 是否包含子目录/文件 | true/false |

---

### POST /files/batch/check
**功能**: Batch check file exist

**Body 参数** (FilePathsCheck):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| paths | []string | 是 | 要检查的文件路径列表 | 任意有效路径数组 |

---

### POST /files/batch/del
**功能**: Batch delete file

**Body 参数** (FileBatchDelete):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| paths | []string | 是 | 要删除的文件路径列表 | 任意有效路径数组 |
| isDir | bool | 否 | 路径是否为目录 | true/false |

---

### POST /files/batch/role
**功能**: Batch change file mode and owner

**Body 参数** (FileRoleReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| paths | []string | 是 | 要修改的文件路径列表 | 任意有效路径数组 |
| mode | int64 | 是 | 权限模式 | 八进制权限值，如 0755 |
| user | string | 是 | 用户名 | 系统存在的用户 |
| group | string | 是 | 用户组名 | 系统存在的用户组 |
| sub | bool | 否 | 是否包含子目录/文件 | true/false |

---

### POST /files/check
**功能**: Check file exist

**Body 参数** (FilePathCheck):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 要检查的文件路径 | 任意有效路径 |
| withInit | bool | 否 | 路径不存在时是否自动创建 | true/false |

---

### POST /files/chunkdownload
**功能**: Chunk Download file

**Body 参数** (FileChunkDownload):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 要下载的文件路径 | 任意有效文件路径 |
| name | string | 是 | 下载时的文件名 | 任意文件名 |

---

### POST /files/chunkupload
**功能**: ChunkUpload file

**FormData 参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| chunk | file | 是 | 分片文件数据 | 文件二进制数据 |
| chunkIndex | int | 是 | 当前分片索引 | 从 0 开始的整数 |
| chunkCount | int | 是 | 总分片数量 | 大于 0 的整数 |
| filename | string | 是 | 原始文件名 | 任意文件名 |
| path | string | 是 | 上传目标目录 | 任意有效目录路径 |
| overwrite | bool | 否 | 是否覆盖已存在文件 | true/false (默认 true) |

---

### POST /files/compress
**功能**: Compress file

**Body 参数** (FileCompress):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| files | []string | 是 | 要压缩的文件/目录路径列表 | 任意有效路径数组 |
| dst | string | 是 | 压缩文件目标目录 | 任意有效目录路径 |
| type | string | 是 | 压缩类型 | zip/gz/bz2/tar/tar.gz/tgz/xz/tar.xz/7z |
| name | string | 是 | 压缩文件名(不含扩展名) | 任意文件名 |
| replace | bool | 否 | 是否覆盖已存在的压缩文件 | true/false |
| secret | string | 否 | 压缩密码(加密压缩时使用) | 任意密码字符串 |

---

### POST /files/content
**功能**: Load file content

**Body 参数** (FileContentReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件路径 | 任意有效文件路径 |
| isDetail | bool | 否 | 是否获取详细信息 | true/false |

---

### POST /files/convert
**功能**: Convert file

**Body 参数** (FileConvertRequest):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| files | []FileConvert | 是 | 要转换的文件列表 | 至少一个文件 |
| outputPath | string | 是 | 输出目录路径 | 任意有效目录路径 |
| deleteSource | bool | 否 | 转换后是否删除源文件 | true/false |
| taskID | string | 否 | 任务 ID | 任意字符串 |

**FileConvert 子参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件路径 | 任意有效文件路径 |
| type | string | 是 | 转换类型 | 转换类型标识 |
| inputFile | string | 是 | 输入文件名 | 任意文件名 |
| extension | string | 是 | 目标扩展名 | 目标文件扩展名 |
| outputFormat | string | 是 | 输出格式 | 输出格式标识 |
| status | string | 否 | 状态 | 状态标识 |

---

### POST /files/convert/log
**功能**: Convert file

**Body 参数** (PageInfo):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | 大于 0 的整数 |
| pageSize | int | 是 | 每页数量 | 1-100 |

---

### POST /files/decompress
**功能**: Decompress file

**Body 参数** (FileDeCompress):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| dst | string | 是 | 解压目标目录 | 任意有效目录路径 |
| type | string | 是 | 压缩文件类型 | zip/gz/bz2/tar/tar.gz/tgz/xz/tar.xz/7z |
| path | string | 是 | 压缩文件路径 | 任意有效的压缩文件路径 |
| secret | string | 否 | 解压密码 | 任意密码字符串 |

---

### POST /files/del
**功能**: Delete file

**Body 参数** (FileDelete):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 要删除的文件/目录路径 | 任意有效路径 |
| isDir | bool | 否 | 路径是否为目录 | true/false |
| forceDelete | bool | 否 | 是否强制删除(不经过回收站) | true/false |

---

### POST /files/depth/size
**功能**: Multi file size

**Body 参数** (DirSizeReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 目录路径 | 任意有效目录路径 |

---

### POST /files/favorite
**功能**: Create favorite

**Body 参数** (FavoriteCreate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 要收藏的文件/目录路径 | 任意有效路径 |

---

### POST /files/favorite/del
**功能**: Delete favorite

**Body 参数** (FavoriteDelete):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 收藏记录 ID | 收藏记录的主键 ID |

---

### POST /files/favorite/search
**功能**: List favorites

**Body 参数** (SearchUploadWithPage):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 搜索路径(收藏夹固定路径) | 收藏夹路径 |
| page | int | 是 | 页码 | 大于 0 的整数 |
| pageSize | int | 是 | 每页数量 | 1-100 |

---

### POST /files/mode
**功能**: Change file mode

**Body 参数** (FileCreate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件/目录路径 | 任意有效路径 |
| mode | int64 | 否 | 权限模式 | 八进制权限值，如 0755 |

---

### POST /files/mount
**功能**: system mount

**参数**: 无

---

### POST /files/move
**功能**: Move file

**Body 参数** (FileMove):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 移动类型 | move/copy |
| oldPaths | []string | 是 | 原路径列表 | 任意有效路径数组 |
| newPath | string | 是 | 目标目录路径 | 任意有效目录路径 |
| name | string | 否 | 重命名时的新名称 | 任意文件名 |
| cover | bool | 否 | 是否覆盖已存在的文件 | true/false |
| coverPaths | []string | 否 | 需要覆盖的路径列表 | 路径数组 |

---

### POST /files/owner
**功能**: Change file owner

**Body 参数** (FileRoleUpdate):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件/目录路径 | 任意有效路径 |
| user | string | 是 | 用户名 | 系统存在的用户 |
| group | string | 是 | 用户组名 | 系统存在的用户组 |
| sub | bool | 否 | 是否包含子目录/文件 | true/false |

---

### POST /files/preview
**功能**: Preview file content

**Body 参数** (FileContentReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件路径 | 任意有效文件路径 |
| isDetail | bool | 否 | 是否获取详细信息 | true/false |

---

### POST /files/read
**功能**: Read file by Line

**Body 参数** (FileReadByLineReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | 大于 0 的整数 |
| pageSize | int | 是 | 每页行数 | 1-1000 |
| type | string | 是 | 文件类型 | 文件类型标识 |
| ID | uint | 否 | 资源 ID | 资源主键 ID |
| name | string | 否 | 文件名 | 任意文件名 |
| latest | bool | 否 | 是否只读取最新内容 | true/false |
| taskID | string | 否 | 任务 ID | 任意字符串 |
| taskType | string | 否 | 任务类型 | 任务类型标识 |
| taskOperate | string | 否 | 任务操作 | 操作标识 |
| resourceID | uint | 否 | 资源 ID | 资源主键 ID |

---

### POST /files/recycle/clear
**功能**: Clear RecycleBin files

**参数**: 无

---

### POST /files/recycle/reduce
**功能**: Reduce RecycleBin files

**Body 参数** (RecycleBinReduce):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| from | string | 是 | 回收站中的原始路径 | 回收站记录路径 |
| rName | string | 是 | 回收站中的文件名 | 回收站文件名 |
| name | string | 否 | 恢复后的文件名 | 任意文件名 |

---

### POST /files/recycle/search
**功能**: List RecycleBin files

**Body 参数** (SearchUploadWithPage):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 搜索路径(回收站固定路径) | 回收站路径 |
| page | int | 是 | 页码 | 大于 0 的整数 |
| pageSize | int | 是 | 每页数量 | 1-100 |

---

### POST /files/rename
**功能**: Change file name

**Body 参数** (FileRename):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| oldName | string | 是 | 原文件名(完整路径) | 任意有效文件路径 |
| newName | string | 是 | 新文件名(完整路径) | 任意有效文件路径 |

---

### POST /files/save
**功能**: Update file content

**Body 参数** (FileEdit):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 文件路径 | 任意有效文件路径 |
| content | string | 否 | 文件内容 | 任意文本内容 |

---

### POST /files/search
**功能**: List files

**Body 参数** (FileOption):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 否 | 目录路径 | 任意有效目录路径 |
| search | string | 否 | 搜索关键字 | 任意搜索字符串 |
| containSub | bool | 否 | 是否包含子目录搜索 | true/false |
| expand | bool | 否 | 是否展开子目录 | true/false |
| dir | bool | 否 | 是否只显示目录 | true/false |
| showHidden | bool | 否 | 是否显示隐藏文件 | true/false |
| page | int | 否 | 页码 | 大于 0 的整数 |
| pageSize | int | 否 | 每页数量 | 1-100 |
| sortBy | string | 否 | 排序字段 | name/size/modTime |
| sortOrder | string | 否 | 排序方式 | ascending/descending |
| isDetail | bool | 否 | 是否获取详细信息 | true/false |

---

### POST /files/size
**功能**: Load file size

**Body 参数** (DirSizeReq):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 目录路径 | 任意有效目录路径 |

---

### POST /files/tree
**功能**: Load files tree

**Body 参数** (FileOption):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 否 | 目录路径 | 任意有效目录路径 |
| search | string | 否 | 搜索关键字 | 任意搜索字符串 |
| containSub | bool | 否 | 是否包含子目录搜索 | true/false |
| expand | bool | 否 | 是否展开子目录 | true/false |
| dir | bool | 否 | 是否只显示目录 | true/false |
| showHidden | bool | 否 | 是否显示隐藏文件 | true/false |
| page | int | 否 | 页码 | 大于 0 的整数 |
| pageSize | int | 否 | 每页数量 | 1-100 |
| sortBy | string | 否 | 排序字段 | name/size/modTime |
| sortOrder | string | 否 | 排序方式 | ascending/descending |
| isDetail | bool | 否 | 是否获取详细信息 | true/false |

---

### POST /files/upload
**功能**: Upload file

**FormData 参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| file | file | 是 | 上传的文件 | 文件二进制数据 |
| path | string | 是 | 上传目标目录 | 任意有效目录路径 |
| overwrite | bool | 否 | 是否覆盖已存在文件 | true/false (默认 true) |

---

### POST /files/upload/search
**功能**: Page file

**Body 参数** (SearchUploadWithPage):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| path | string | 是 | 搜索目录路径 | 任意有效目录路径 |
| page | int | 是 | 页码 | 大于 0 的整数 |
| pageSize | int | 是 | 每页数量 | 1-100 |

---

### POST /files/user/group
**功能**: system user and group

**参数**: 无

---

### POST /files/wget
**功能**: Wget file

**Body 参数** (FileWget):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| url | string | 是 | 下载 URL | HTTP/HTTPS URL |
| path | string | 是 | 下载保存目录 | 任意有效目录路径 |
| name | string | 是 | 保存的文件名 | 任意文件名 |
| ignoreCertificate | bool | 否 | 是否忽略 SSL 证书错误 | true/false |

---

## 压缩类型参考

| 类型 | 说明 |
|------|------|
| zip | ZIP 压缩 |
| gz | Gzip 压缩 |
| bz2 | Bzip2 压缩 |
| tar | Tar 打包 |
| tar.gz / tgz | Tar + Gzip 压缩 |
| xz | XZ 压缩 |
| tar.xz | Tar + XZ 压缩 |
| 7z | 7-Zip 压缩 |

## 排序字段参考

| 字段 | 说明 |
|------|------|
| name | 按名称排序 |
| size | 按大小排序 |
| modTime | 按修改时间排序 |
