# API Endpoint Analysis

## 邀请协作
**Endpoint**: `POST /v2/collab/invite`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `accessible_by` | `body` | `object` | 邀请对象 |
| `folder_id` | `body` | `int64` | 协作文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collab/invite' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 批量邀请协作
**Endpoint**: `POST /v2/collab/invite_batch`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `accessible_by` | `body` | `array<object>` | 邀请对象 |
| `folder_id` | `body` | `int64` | 协作文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collab/invite_batch' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除协作
**Endpoint**: `POST /v2/collab/{id}/delete`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 协作ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collab/{id}/delete' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取协作信息
**Endpoint**: `GET /v2/collab/{id}/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 协作ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/collab/{id}/info' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 批量移出协作
**Endpoint**: `POST /v2/collab/remove`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `collab_ids` | `body` | `array<int64>` | 需要被删除的协作用户（支持批量） |
| `folder_id` | `body` | `int64` | 协作文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collab/remove' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 更新协作
**Endpoint**: `POST /v2/collab/{id}/update`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 协作ID |
| `role` | `body` | `string` | 更新角色类型；coowner:共同所有者; editor:编辑者; online_collaborator:在线协作者; viewer_uploader:查看/上传者; viewer:查看者; previewer_uploader:预览+上传者; previewer:预览者; uploader:上传者; reset:禁止访问 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collab/{id}/update' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 添加评论
**Endpoint**: `POST /v2/comment/create`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `content` | `body` | `string` | 评论文本，长度不能超过1001个字符@[user_id:评论内容] |
| `file_id` | `body` | `int64` | 评论文件id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/comment/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除评论
**Endpoint**: `POST /v2/comment/{id}/delete`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 删除的评论id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/comment/{id}/delete' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取子部门列表
**Endpoint**: `GET /v2/department/{id}/children`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/department/{id}/children' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: permission_filter
```

---

## 获取部门信息
**Endpoint**: `GET /v2/department/{id}/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/department/{id}/info' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取自己所在的部门
**Endpoint**: `GET /v2/department/own_list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/department/own_list' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取部门成员列表
**Endpoint**: `GET /v2/department/{id}/users`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/department/{id}/users' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, page_id
```

---

## 加入同步
**Endpoint**: `POST /v2/device/{device_token}/add_sync`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `device_token` | `path` | `string` | 设备token |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/device/{device_token}/add_sync' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取设备同步状态
**Endpoint**: `GET /v2/device/{device_token}/synced_status`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `device_token` | `path` | `string` | 设备token |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/device/{device_token}/synced_status' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 移除同步
**Endpoint**: `POST /v2/device/{device_token}/remove_sync`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `device_token` | `path` | `string` | 设备token |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/device/{device_token}/remove_sync' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 拷贝文件
**Endpoint**: `POST /v2/file/{id}/copy`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件的ID |
| `target_folder_id` | `body` | `int64` | 目标文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/75003907526/copy' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "target_folder_id": 75000441887
  }'
```

---

## 按路径拷贝文件
**Endpoint**: `POST /v2/file/{id}/copy_by_path`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件的ID |
| `target_folder_path` | `body` | `string` | 路径名，以/划分文件夹，根目录在个人文件下，文件夹名称必须是1到222个字符，并且不能含有/ ? : * " > < \|且末尾不能为“.” |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/75003907526/copy_by_path' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "target_folder_path": "75000441887" 
  }'
```

---

## 创建空白文件，支持office类型
**Endpoint**: `POST /v2/file/create_blank_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `departmentId` | `body` | `int64` | 部门id |
| `name` | `body` | `string` | 新文件文件名 |
| `nameConflictResolveStrategy` | `body` | `string` | 命名冲突解决策略(固定传2)；2：系统自动重命名（当前仅支持这种） |
| `parentEnterpriseId` | `body` | `int64` | 企业id，若为外协文件夹需要填写对应企业id |
| `parentFolderId` | `body` | `int64` | 父文件夹Id |
| `type` | `body` | `string` | 文件类型；1：doc类型; 2：ppt类型; 3：xls类型 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/create_blank_file' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer a2a192ea-cb37-4c0c-b8d5-574232fa853b' \
--header 'Cookie: lang=zh-CN' \
--data-raw '{
	"departmentId":0,
	"name":"111",
	"parentEnterpriseId":21791,
	"nameConflictResolveStrategy":"2",
	"parentFolderId":0,
	"type":"1" 
	}'
```

---

## 删除文件,被删除的文件将进入回收站
**Endpoint**: `POST /v2/file/{id}/delete`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 删除文件的ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/delete' \
 --header 'Authorization: Bearer bdd88b1c-aa8a-4126-b380-a1e64f9348a5'
```

---

## 从回收站中彻底删除文件,或者清空回收站
**Endpoint**: `POST /v2/file/{id}/delete_from_trash`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 从回收站删除文件的ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/delete_from_trash' \
 --header 'Authorization: Bearer bdd88b1c-aa8a-4126-b380-a1e64f9348a5'
```

---

## 下载文件
**Endpoint**: `GET /v2/file/{id}/download_v2`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件的ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/file/75003903551/download?version=0&valid_period=100' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件特定版本信息
**Endpoint**: `GET /v2/file/{id}/version/{version_id}/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |
| `version_id` | `path` | `int64` | 文件版本id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/file/75003907526/version/75000911769/info' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 删除文件版本
**Endpoint**: `POST /v2/file/{id}/version/{version_id}/delete`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |
| `version_id` | `path` | `int64` | 文件版本id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/75003907526/version/75000911810/delete' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件版本列表
**Endpoint**: `GET /v2/file/{id}/versions`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/file/75003907526/versions' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 提升版本为当前版本
**Endpoint**: `POST /v2/file/{id}/version/{version_id}/promote`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |
| `version_id` | `path` | `int64` | 文件版本id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/75003907526/version/75000911769/promote' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取回收站中的文件信息
**Endpoint**: `GET /v2/file/{id}/trash`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |

**Curl Command**:
```bash
curl --location 'https://open.fangcloud.com/api/v2/file/75003624924/trash' \
 --header 'Authorization: Bearer bdd88b1c-aa8a-4126-b380-a1e64f9348a5'
```

---

## 获取文件详细信息
**Endpoint**: `GET /v2/file/{id}/info_v2`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |

**Curl Command**:
```bash
curl --location 'https://open.fangcloud.com/api/v2/file/75003903445/info_v2' \
 --header 'Authorization: Bearer bc326c4a-6eb0-4790-8cf3-3d19232af711'
```

---

## 获取最近使用文件列表
**Endpoint**: `GET /v2/file/recent_items`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `limit` | `query` | `int32` | 获取的条数 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/file/recent_items?limit=1' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件的评论列表
**Endpoint**: `GET /v2/file/{id}/comments`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/file/75003907071/comments' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件的分享链接列表
**Endpoint**: `GET /v2/file/{id}/share_links`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/file/75003907526/share_links' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 标记最近使用
**Endpoint**: `POST /v2/file/{item_id}/mark_as_used`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `item_id` | `path` | `int64` | 文件id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/126000100472/mark_as_used' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 移动文件到目标文件夹
**Endpoint**: `POST /v2/file/{id}/move`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 移动文件的ID |
| `target_folder_id` | `body` | `int64` | 目标文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/move' \
  --header 'Authorization: Bearer d8ec3bc7-c7f2-40b6-a591-7b03c134478f' \
  --header 'Content-Type: application/json' \
  --data-raw '{    
    "target_folder_id": 179000000178,    
    "target_space": {        
        "type": "department",        
        "id": 179000000178    
        }
    }'
```

---

## 上传文件新版本
**Endpoint**: `POST /v2/file/{id}/new_version_v2`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件id |
| `name` | `body` | `string` | 文件名称，文件名称必须是1到222个字符，并且不能含有/ ? : * " > < \ |
| `upload_type` | `body` | `string` | 上传类型；固定传api |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/75003685568/new_version_v2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 1cd9081c-aa2c-4f30-a619-f32663dc57cc' \
--data '{
  "name": "报表v1.0.pdf",
  "upload_type": "api",
  "remark": "新版本",
}'  

该接口会返回上传地址，获取到上传地址后，上传文件示例：

curl --location 'https://upload01.fangcloud.com/upload/d125644c2e43449a8becbcf9217c5dcf/ae03113d47ed2732cc40480906705861869c2e7f7687528e29feee5c3ae1793c' \
--header 'Cookie: lang=zh-CN' \
--form 'file=@"/Users/liangxiaosheng/FangcloudV2/personal_space.localized/个人工作文件/个人/开放平台/开放平台使用文档/token介绍.jpg"'
```

---

## 批量下载文件
**Endpoint**: `POST /v2/file/pack_download`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `item_typed_ids` | `body` | `array<string>` | 文件id或文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/pack_download' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "item_typed_ids": [
      "file_203003511640",
      "folder_203000428376"
    ]
  }'
```

---

## 从回收站中取回文件
**Endpoint**: `POST /v2/file/{id}/restore_from_trash`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 从回收站回复的文件的ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/restore_from_trash' \
 --header 'Authorization: Bearer bdd88b1c-aa8a-4126-b380-a1e64f9348a5'
```

---

## 更新文件信息
**Endpoint**: `POST /v2/file/{id}/update`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 更新文件的ID |

**Curl Command**:
```bash
curl --location 'https://open.fangcloud.com/api/v2/folder/179000000087/update' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{  
	"name": "new name" 
}'
```

---

## 按路径上传文件
**Endpoint**: `POST /v2/file/upload_by_path`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 文件名称，文件名称必须是1到222个字符，并且不能含有/ ? : * " > < \ |
| `target_folder_path` | `body` | `string` | 路径名，以/划分文件夹，根目录在个人文件下，文件夹名称必须是1到222个字符，并且不能含有/ ? : * " > < \|且末尾不能为“.” |
| `upload_type` | `body` | `string` | 上传类型；固定传api |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/upload_by_path' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 003504d9-9a1e-4fc5-8b3e-188ee866b557' \
--header 'Cookie: lang=zh-CN' \
--data '{
  "target_folder_path": "123/123",
  "name": "text.tar",
  "upload_type": "api"
}' 

该接口会返回上传地址，获取到上传地址后，上传文件示例：

curl --location 'https://upload01.fangcloud.com/upload/d125644c2e43449a8becbcf9217c5dcf/ae03113d47ed2732cc40480906705861869c2e7f7687528e29feee5c3ae1793c' \
--header 'Cookie: lang=zh-CN' \
--form 'file=@"/Users/liangxiaosheng/FangcloudV2/personal_space.localized/个人工作文件/个人/开放平台/开放平台使用文档/token介绍.jpg"'
```

---

## 上传文件
**Endpoint**: `POST /v2/file/upload_v2`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 准备上传的文件的名称，文件名称必须是1到222个字符，并且不能含有/ ? : * " > < \ |
| `parent_id` | `body` | `int64` | 上传至的文件夹id |
| `upload_type` | `body` | `string` | 上传类型；固定传api |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/file/upload_v2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 1cd9081c-aa2c-4f30-a619-f32663dc57cc' \
--data '{
  "parent_id": "501002634212",
  "name": "报表v1.0.pdf",
  "upload_type": "api"
}'  

该接口会返回上传地址，获取到上传地址后，上传文件示例：

curl --location 'https://upload01.fangcloud.com/upload/d125644c2e43449a8becbcf9217c5dcf/ae03113d47ed2732cc40480906705861869c2e7f7687528e29feee5c3ae1793c' \
--header 'Cookie: lang=zh-CN' \
--form 'file=@"/Users/liangxiaosheng/FangcloudV2/personal_space.localized/个人工作文件/个人/开放平台/开放平台使用文档/token介绍.jpg"'
```

---

## 拷贝文件夹
**Endpoint**: `POST /v2/folder/{id}/copy`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |
| `target_folder_id` | `body` | `int64` | 目标文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/copy' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "target_folder_id": 179000000178 
  }'
```

---

## 创建文件夹
**Endpoint**: `POST /v2/folder/create`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 文件夹名，文件夹名称必须是1到222个字符，并且不能含有/ ? : * " > < \ |
| `parent_id` | `body` | `int64` | 父文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/create' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "name": "new folders" 
    "parent_id": 75000441887 
  }'
```

---

## 按路径创建文件夹
**Endpoint**: `POST /v2/folder/create_by_path`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `target_folder_path` | `body` | `string` | 路径名，以/划分文件夹，根目录在个人文件下，文件夹名称必须是1到222个字符，并且不能含有/ ? : * " > < \|且末尾不能为“.” |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/create_by_path' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "target_folder_path": "会议测试/9.25/研发" 
    "department_id": 894823 
  }'
```

---

## 从回收站中删除文件夹
**Endpoint**: `POST /v2/folder/{id}/delete_from_trash`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/delete_from_trash' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 删除文件夹
**Endpoint**: `POST /v2/folder/{id}/delete`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/delete' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取回收站中的文件夹信息
**Endpoint**: `GET /v2/folder/{id}/trash`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/179000000087/trash' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件夹下的单层文件和文件夹列表
**Endpoint**: `GET /v2/folder/{id}/children`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/293001037960/children?folder_id=293001037960&type=all&page_capacity=100&page_id=1' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取与我协作的文件夹列表
**Endpoint**: `GET /v2/folder/collab_folders`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/collab_folders?page_id=0&page_capacity=10&sort_by=name&sort_direction=desc' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取部门首层文件夹列表
**Endpoint**: `GET /v2/folder/department_folders`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `department_id` | `query` | `int64` | 部门ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/department_folders?department_id=596371' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件夹详细信息
**Endpoint**: `GET /v2/folder/{id}/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/293001037960/info' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取个人首层文件夹与文件列表
**Endpoint**: `GET /v2/folder/personal_items`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/personal_items?page_id=1&page_capacity=2&sort_by=name&sort_direction=asc' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件夹协作成员
**Endpoint**: `GET /v2/folder/{id}/collabs`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/203000425147/collabs' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 获取文件夹的分享链接列表
**Endpoint**: `GET /v2/folder/{id}/share_links`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/folder/203000425147/share_links?page_id=0' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 移动文件夹
**Endpoint**: `POST /v2/folder/{id}/move`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |
| `target_folder_id` | `body` | `int64` | 目标文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/move' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "target_folder_id": 179000000178 
  }'
```

---

## 从回收站中取回文件夹
**Endpoint**: `POST /v2/folder/{id}/restore_from_trash`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/restore_from_trash' \
--header 'Authorization: Bearer 775eb65c-8545-419d-823c-ffb5d42d75c0'
```

---

## 更新文件夹详细信息
**Endpoint**: `POST /v2/folder/{id}/update`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 文件夹id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/folder/179000000087/update' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "name": "ew name" 
  }'
```

---

## 添加常用
**Endpoint**: `POST /v2/frequent/add`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/frequent/add' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除常用
**Endpoint**: `POST /v2/frequent/delete`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/frequent/delete' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取常用列表
**Endpoint**: `GET /v2/frequent/list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/frequent/list' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: page_id
```

---

## 获取公司可见群组
**Endpoint**: `GET /v2/group/list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/group/list' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words
```

---

## 获取群组成员列表
**Endpoint**: `GET /v2/group/{id}/users`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/group/{id}/users' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, page_id
```

---

## 搜索文件
**Endpoint**: `GET /v2/item/search`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `query_words` | `query` | `string` | 搜索关键词，不能为空 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/item/search' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, type, sort_by, sort_direction, page_id, search_in_folder, fields, query_filter, updated_time_range, department_id, precise_search
```

---

## 知识库添加用户
**Endpoint**: `POST /v2/kbase/add_library_user`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `library_id` | `body` | `string` | 知识库id |
| `user_roles` | `body` | `array<object>` | 用户角色列表 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/add_library_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库对话接口
**Endpoint**: `POST /v2/kbase/chatStream`

**Description**:
默认请求地址：https://open.fangcloud.com/api/v2/knowledge/chatStream 

私有化部署请求地址：云盘域名/platform/api/v2/knowledge/chatStream 
- **请求参数说明**

  |    参数字段    |  字段类型  | 是否必须 | 字段说明                                                     |
  | :------------: | :--------: | :------: | ------------------------------------------------------------ |
  | messages       | List[Dict] |    是    | 包含迄今为止对话消息列表，这是一个结构体的列表，每个元素类似如下：`{"role": "user", "content": "你好"}` role 只支持 `user` , `assistant` 其一，content 不得为空，`user` 为用户角色，`assistant` 为知识库角色 |
  | chatType |   string   |    是   | 对话类型，固定填：AI_LIBRARY |
  |   sessionId    |   string   |   否   | 会话id，首次对话不需要传，结果会返回，后续对话需要传返回的值                                                     |
  |    search    |   string   |    是   | 是否开启联网搜索 |
  |    gptType    |   string   |    是    | 模型类型 |
  |    libraryIds    |   list<string>   |    是    | 知识库id列表 |

  > 请求示例

**Curl Command**:
```bash
curl --location 'https://open.fangcloud.com/api/v2/knowledge/chatStream' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer de74b292-3dbf-446a-9d30-c0e89106a682' \
  --data '{
      "chatType": "AI_LIBRARY",
      "messages": [
          {
              "role": "user",
              "content": "你是谁"
          }
      ],
      "search": false,
      "gptType": "deepseek",
      "libraryIds": [
          "63df81213d4bb9c55d3d9dac51dbe8d9"
      ],
      "sessionId": "531_1757403170386_490"
  }'
```

---

## 创建知识目录
**Endpoint**: `POST /v2/kbase/create_document`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `library_id` | `body` | `string` | 知识库id |
| `name` | `body` | `string` | 知识目录名称 |
| `parent_document_id` | `body` | `string` | 上级知识目录id，若为根目录则传：0 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/create_document' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 创建知识库
**Endpoint**: `POST /v2/kbase/create_library`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `content` | `body` | `string` | 知识库简介 |
| `name` | `body` | `string` | 知识库名称 |
| `pic_file_id` | `body` | `string` | 知识库图标地址，可填默认值：https://s0.ssl.qhres2.com/static/a3e6a8389f34868e.svg |
| `questions` | `body` | `array<string>` | 知识库推荐问题 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/create_library' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除知识目录
**Endpoint**: `POST /v2/kbase/delete_document`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `document_ids` | `body` | `array<string>` | 删除知识目录id列表 |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/delete_document' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库删除文件
**Endpoint**: `POST /v2/kbase/delete_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `book_ids` | `body` | `array<string>` | 删除文件id列表 |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/delete_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除知识库
**Endpoint**: `POST /v2/kbase/delete_library`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/delete_library' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库删除用户
**Endpoint**: `POST /v2/kbase/delete_library_user`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `library_id` | `body` | `string` | 知识库id |
| `user_id` | `body` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/delete_library_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库下载文件
**Endpoint**: `POST /v2/kbase/download_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `book_id` | `body` | `string` | 知识库文件id |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/download_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 查询知识库文件训练片段
**Endpoint**: `POST /v2/kbase/get_book_segment_list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `book_id` | `body` | `string` | 知识库文件id |
| `library_id` | `body` | `string` | 知识库id |
| `page_no` | `body` | `int64` | 页码 |
| `page_size` | `body` | `int64` | 页容量 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/get_book_segment_list' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "page_no": 1 
    "page_size": 10 
    "library_id": "21b9c123e95200691bd6d4a73a9994f" 
    "book_id": "11711877123888819810" 
  }'
```

---

## 查询训练文件训练状态
**Endpoint**: `POST /v2/kbase/get_train_file_status`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `train_file_ids` | `body` | `array<int64>` | 训练文件id列表 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/get_train_file_status' \
--header 'Authorization: Bearer 583fad43-3265-45df-9e13-91fa5a22a2ca' \
--header 'Content-Type: application/json' \
--data '{
    "train_file_ids": [123] 
  }'
```

---

## 获取知识目录列表
**Endpoint**: `POST /v2/kbase/list_document`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `document_id` | `body` | `string` | 知识目录id，顶级目录id时候传0 |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/list_document' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 查询知识目录用户列表
**Endpoint**: `POST /v2/kbase/list_document_user`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `document_id` | `body` | `string` | 知识目录id |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/list_document_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取知识库列表
**Endpoint**: `POST /v2/kbase/list_library`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `page_number` | `body` | `int64` | 查询页数 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/list_library' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取知识库角色列表
**Endpoint**: `POST /v2/kbase/list_library_role`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/list_library_role' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取知识库用户列表
**Endpoint**: `POST /v2/kbase/list_library_user`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `library_id` | `body` | `string` | 知识库id |
| `page_num` | `body` | `int64` | 页码 |
| `page_size` | `body` | `int64` | 页容量 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/list_library_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库打包下载文件
**Endpoint**: `POST /v2/kbase/pack_download_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `book_ids` | `body` | `array<string>` | 知识库文件列表 |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/pack_download_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库发布文件
**Endpoint**: `POST /v2/kbase/publish_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `files` | `body` | `array<object>` | 发布文件列表 |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/publish_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取知识库文件列表
**Endpoint**: `POST /v2/kbase/search_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `document_id` | `body` | `string` | 知识目录id |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/search_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 更新知识目录详情
**Endpoint**: `POST /v2/kbase/update_document`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `document_id` | `body` | `string` | 知识目录id |
| `library_id` | `body` | `string` | 知识库id |
| `name` | `body` | `string` | 知识目录名称 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/update_document' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库更新用户
**Endpoint**: `POST /v2/kbase/update_library_user`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `library_id` | `body` | `string` | 知识库id |
| `role_id` | `body` | `string` | 知识库角色id |
| `user_id` | `body` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/kbase/update_library_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库上传文件
**Endpoint**: `POST /v2/kbase/upload_file`

**Description**:
获取上传地址后，需要调用上传接口进行真正的上传(header中需要传x-file-name字段：文件的名称)，真正上传完成之后，需要再调用发布接口，才能在知识库中看到文件，上传文件示例：

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `document_id` | `body` | `string` | 知识目录id |
| `file_name` | `body` | `string` | 文件名称 |
| `file_size` | `body` | `int64` | 文件大小 |
| `library_id` | `body` | `string` | 知识库id |

**Curl Command**:
```bash
curl --location 'https://upload01.fangcloud.net/upload/18843c714d4d4216a8ae7fd247a0e261/b9afe9f13fb09e54d4863fe697b60188518cbcd036cdbb71b4d82d824dcff01b' \
--header 'x-file-name: 1758513460275_%E3%80%8A%E6%99%BA%E8%83%BD%E4%BD%93%E8%9C%82%E7%BE%A4%E5%AE%9E%E6%88%98%E5%9F%B9%E8%AE%AD%E3%80%8B%E7%90%86%E8%AE%BA%E9%83%A8%E5%88%86%E8%B5%84%E6%96%99.pdf' \
--form 'file=@"1758513460275_《智能体蜂群实战培训》理论部分资料.pdf"'
```

---

## 新增Ai文件
**Endpoint**: `POST /v2/knowledge/add_ai_file`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `data_type` | `body` | `string` | 数据类型；url（类型为url时：data_value传url地址） file（类型为url时：data_value传云盘文件id） |
| `data_value` | `body` | `string` | 数据值，url地址或者云盘文件id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/add_ai_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 数据集添加训练任务
**Endpoint**: `POST /v2/knowledge/add_train_file`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `analysis_method` | `body` | `string` | 解析类型；direct_segment（通用文本类型，支持云盘文件或者文件夹，支持文件类型：docx、txt、pdf、md） qa（问答，只支持云盘文件，支持文件类型：csv、xlsx） table（表格类型，只支持云盘文件，支持文件类型：xlsx） |
| `data_id` | `body` | `int64` | 数据集id |
| `file_id` | `body` | `int64` | 文件夹或文件夹id |
| `file_type` | `body` | `string` | 文件类型；file（文件） folder（文件夹） |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/add_train_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 智能体对话接口
**Endpoint**: `POST /v2/knowledge/chatStream`

**Description**:
默认请求地址：https://open.fangcloud.com/api/v2/knowledge/chatStream 

私有化部署请求地址：云盘域名/platform/api/v2/knowledge/chatStream 
- **请求参数说明**

  |    参数字段    |  字段类型  | 是否必须 | 字段说明                                                     |
  | :------------: | :--------: | :------: | ------------------------------------------------------------ |
  | messages       | List[Dict] |    是    | 包含迄今为止对话消息列表，这是一个结构体的列表，每个元素类似如下：`{"role": "user", "content": "你好"}` role 只支持 `user` , `assistant` 其一，content 不得为空，`user` 为用户角色，`assistant` 为知识号角色 |
  | knowledgeGptId |   string   |    否    | 智能体id，从智能体对话页面的url地址中获取 |
  |   sessionId    |   string   |    是    | 对话标识                                                     |
  |    chatType    |   string   |    是    | 固定为：ZSH_CHAT        |

  > 请求示例

**Curl Command**:
```bash
curl --location 'https://open.fangcloud.com/api/v2/knowledge/chatStream' \
  --header 'Authorization: Bearer cb806f3c-8d68-49ab-9925-4eefe3c8ec96' \
  --header 'Content-Type: application/json' \
  --data '{
      "messages": [
          {"role": "user", "content": "如何调用开放平台？"}
      ],
      "knowledgeGptId": "321",
      "sessionId": "1721706231962_7248294",
      "chatType":"ZSH_CHAT"
  }'
```

---

## 创建数据集
**Endpoint**: `POST /v2/knowledge/create_data`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 数据集名称 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/create_data' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 数据集匹配测试
**Endpoint**: `POST /v2/knowledge/data_match_test`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `data_id` | `body` | `int64` | 数据集id |
| `question` | `body` | `string` | 问题 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/data_match_test' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 创建智能体
**Endpoint**: `POST /v2/knowledge/create_gpt`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 知识员工名称 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/create_gpt' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除数据集
**Endpoint**: `POST /v2/knowledge/delete_data`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `data_id` | `body` | `int64` | 数据集id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/delete_data' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除训练任务
**Endpoint**: `POST /v2/knowledge/delete_train_file`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `file_train_id` | `body` | `int64` | 训练任务id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/delete_train_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除智能体
**Endpoint**: `POST /v2/knowledge/delete_gpt`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `knowledge_gpt_id` | `body` | `int64` | 知识员工id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/delete_gpt' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 编辑智能体详情
**Endpoint**: `POST /v2/knowledge/edit_gpt_info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `knowledge_gpt_id` | `body` | `int64` | 知识员工id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/edit_gpt_info' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取Ai文件详情
**Endpoint**: `POST /v2/knowledge/get_ai_file_detail`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `ai_file_id` | `body` | `int64` | ai文件训练得到的数据集id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/get_ai_file_detail' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取ai搜索推荐问题
**Endpoint**: `POST /v2/knowledge/get_ai_search_recommend`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `question` | `body` | `string` | 问题 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/get_ai_search_recommend' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取智能体地址
**Endpoint**: `POST /v2/knowledge/getChatUrl`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `knowledge_gpt_id` | `body` | `int64` | 知识员工id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/getChatUrl' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 查询智能体详情
**Endpoint**: `POST /v2/knowledge/get_gpt_info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `knowledge_gpt_id` | `body` | `int64` | 知识员工id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/get_gpt_info' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取知识员工token
**Endpoint**: `POST /v2/knowledge/get_gpt_token`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `gpt_id` | `body` | `int64` | 知识员工id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/get_gpt_token' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 知识库召回
**Endpoint**: `POST /v2/knowledge/retrieval`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `query` | `body` | `string` | 问题 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/retrieval' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取智能体列表
**Endpoint**: `GET /v2/knowledge/list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/knowledge/list' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取智能体分类列表
**Endpoint**: `GET /v2/knowledge/list_category`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/knowledge/list_category' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 查询数据集列表
**Endpoint**: `POST /v2/knowledge/list_data`

**Description**:
AI知识库版本不支持

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/list_data' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 查询数据集问答对列表
**Endpoint**: `POST /v2/knowledge/list_data_qa`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `data_id` | `body` | `int64` | 数据集id |
| `page_no` | `body` | `int64` | 页码 |
| `page_size` | `body` | `int64` | 页容量 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/list_data_qa' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 查询数据集知识片段列表
**Endpoint**: `POST /v2/knowledge/list_data_segment`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `data_id` | `body` | `int64` | 数据集id |
| `page_no` | `body` | `int64` | 页码 |
| `page_size` | `body` | `int64` | 页容量 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/list_data_segment' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取智能体广场分类列表
**Endpoint**: `POST /v2/knowledge/list_square_gpt`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `type` | `body` | `string` | 类型 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/list_square_gpt' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 查询训练任务详情列表
**Endpoint**: `POST /v2/knowledge/list_train_file`

**Description**:
AI知识库版本不支持

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `data_id` | `body` | `int64` | 数据集id |
| `task_type` | `body` | `string` | 类型；direct_segment（文件，直接分段） csv_qa_import（CSV问答导入） |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/knowledge/list_train_file' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 结束一个审阅
**Endpoint**: `GET /v2/review/complete/{id}`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 审阅id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/review/complete/{id}' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 添加审阅
**Endpoint**: `POST /v2/review/create`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/review/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 编辑审阅
**Endpoint**: `POST /v2/review/edit/{id}`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 审阅id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/review/edit/{id}' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获得审阅评论列表
**Endpoint**: `GET /v2/review/comment_list/{id}`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 审阅id |
| `page_id` | `query` | `int32` | 页码 |
| `page_capacity` | `query` | `int32` | 每页容量 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/review/comment_list/{id}' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: page_id, page_capacity
```

---

## 获取审阅信息
**Endpoint**: `GET /v2/review/info/{id}`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 审阅id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/review/info/{id}' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 添加审阅评论
**Endpoint**: `POST /v2/review_comment/create`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `content` | `body` | `string` | 审阅评论内容 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/review_comment/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除审阅评论
**Endpoint**: `DELETE /v2/review_comment/delete/{id}`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 删除的审阅评论id |

**Curl Command**:
```bash
curl --location --request DELETE 'https://open.fangcloud.com/api/v2/review_comment/delete/{id}' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 创建分享链接
**Endpoint**: `POST /v2/share_link/create`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `access` | `body` | `string` | 权限范围；company：公司范围内的; public：所有人; collaborators：指定的成员或指定的群组 |
| `due_time` | `body` | `string` | 到期时间(格式如:2018-10-17) / never_expire 表示用不过期 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/share_link/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
    "access": "",
    "closed": false,
    "description": "",
    "disable_download": false,
    "download_limit_v2": 0,
    "due_time": "",
    "file_id": 0,
    "folder_id": 0,
    "group_ids": [
      0
    ],
    "invited_user_ids": [
      0
    ],
    "is_download_limit_v2": false,
    "is_open_share_receiver": false,
    "is_preview_limit": false,
    "is_support_share_management": false,
    "is_watermark_customize_content": false,
    "open_share_creator_name": "",
    "password": "",
    "password_protected": false,
    "preview_limit": 0,
    "watermark_customize_content": ""
  }'
```

---

## 获得分享链接信息
**Endpoint**: `GET /v2/share_link/{unique_name}/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `unique_name` | `path` | `string` | 分享标识符（分享链接最后面的唯一标识符） |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/share_link/{unique_name}/info' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: password
```

---

## 获得分享链接详情信息
**Endpoint**: `GET /v2/share_link/{unique_name}/info_detail`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `unique_name` | `path` | `string` | 分享标识符（分享链接最后面的唯一标识符） |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/share_link/{unique_name}/info_detail' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 删除分享链接
**Endpoint**: `POST /v2/share_link/{unique_name}/close`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `unique_name` | `path` | `string` | 分享标识符（分享链接最后面的唯一标识符） |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/share_link/{unique_name}/close' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 更新分享链接
**Endpoint**: `POST /v2/share_link/{unique_name}/update`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `unique_name` | `path` | `string` | 分享标识符（分享链接最后面的唯一标识符） |
| `access` | `body` | `string` | 权限范围；company：公司范围内的; public：所有人; collaborators：指定的成员或指定的群组 |
| `due_time` | `body` | `string` | 到期时间(格式如:2018-10-17) / never_expire 表示用不过期 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/share_link/{unique_name}/update' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
  "unique_name": "<unique_name>",
  "body": {
    "access": "",
    "closed": false,
    "description": "",
    "disable_download": false,
    "download_limit_v2": 0,
    "due_time": "",
    "file_id": 0,
    "folder_id": 0,
    "group_ids": [
      0
    ],
    "invited_user_ids": [
      0
    ],
    "is_download_limit_v2": false,
    "is_open_share_receiver": false,
    "is_preview_limit": false,
    "is_support_share_management": false,
    "is_watermark_customize_content": false,
    "open_share_creator_name": "",
    "password": "",
    "password_protected": false,
    "preview_limit": 0,
    "watermark_customize_content": ""
  }
}'
```

---

## 常用标签列表添加标签
**Endpoint**: `POST /v2/tag/add_common_list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `tag_names` | `body` | `array<string>` | 常用标签名称列表 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/tag/add_common_list' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取常用标签列表
**Endpoint**: `GET /v2/tag/common_list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/tag/common_list' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 根据标签名称过滤项目
**Endpoint**: `GET /v2/tag/filter_items_by_tag_name`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `tag_name` | `query` | `string` | 标签名称 |
| `sort_by` | `query` | `string` | 排序方式；示例: `name, date, size` |
| `sort_direction` | `query` | `string` | 排序顺序；示例: `desc, asc` |
| `page_id` | `query` | `int32` | 页码，从1开始 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/tag/filter_items_by_tag_name' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: tag_name, sort_by, sort_direction, page_id
```

---

## 项目新增标签
**Endpoint**: `POST /v2/tag/item_add_tags`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `body` | `string` | 项目id；文件或者文件夹id |
| `type` | `body` | `string` | 项目类型；file:文件类型; folder:文件夹类型 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/tag/item_add_tags' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 项目移除标签
**Endpoint**: `POST /v2/tag/item_remove_tags`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `body` | `string` | 项目id；文件或者文件夹id |
| `tag_ids` | `body` | `array<int64>` | 标签id列表 |
| `type` | `body` | `string` | 项目类型；file:文件类型; folder:文件夹类型 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/tag/item_remove_tags' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取项目最近使用标签列表（最近十个）
**Endpoint**: `GET /v2/tag/list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/tag/list' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 常用标签列表移出标签
**Endpoint**: `POST /v2/tag/remove_common_list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `common_tag_ids` | `body` | `array<int64>` | 常用标签id列表 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/tag/remove_common_list' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 清空回收站
**Endpoint**: `POST /v2/trash/clear`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/trash/clear' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 恢复回收站
**Endpoint**: `POST /v2/trash/restore_all`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/trash/restore_all' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取回收站列表
**Endpoint**: `GET /v2/trash/list`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/trash/list' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: type, sort_by, sort_direction, page_id, page_capacity
```

---

## 获取用户授权code
**Endpoint**: `GET /v2/user/as_user_code`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `url` | `query` | `string` | 授权的url |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/as_user_code' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: url
```

---

## 获取自己的信息
**Endpoint**: `GET /v2/user/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/info' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取用户直属部门
**Endpoint**: `GET /v2/user/departments`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/departments' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取用户信息
**Endpoint**: `GET /v2/user/{id}/info`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/{id}/info' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 用户空间使用情况
**Endpoint**: `GET /v2/user/space_usage`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/space_usage' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取用户头像
**Endpoint**: `GET /v2/user/{id}/profile_pic_download`

**Description**:
该接口的返回结果是一个头像文件 

 **需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 该用户的id |
| `profile_pic_key` | `query` | `string` | 获取头像的key，可以通过https://open.fangcloud.com/api/v2/user/info（获取自身用户信息）的接口获得 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/{id}/profile_pic_download' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: profile_pic_key
```

---

## 企业用户搜索
**Endpoint**: `GET /v2/user/search`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/user/search' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, page_id
```

---

## 更新用户信息
**Endpoint**: `POST /v2/user/update`

**Description**:
**需要使用用户token，根据用户id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 新名字，长度不能超过30个字符 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/user/update' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 添加部门成员
**Endpoint**: `POST /v2/admin/department/{id}/add_user`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |
| `user_id` | `body` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/{id}/add_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 创建部门
**Endpoint**: `POST /v2/admin/department/create`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 部门名称，长度不能超过30个字符 |
| `parent_id` | `body` | `int64` | 父部门id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除部门
**Endpoint**: `POST /v2/admin/department/{id}/delete`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/{id}/delete' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取子部门列表
**Endpoint**: `GET /v2/admin/department/{id}/children`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/department/{id}/children' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取子部门空间列表
**Endpoint**: `GET /v2/admin/department/space_list`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `operator_id` | `query` | `int32` | 操作人user_id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/department/space_list' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: operator_id
```

---

## 获取部门的文件管理员信息
**Endpoint**: `POST /v2/admin/department/{platform_id}/get_file_manager_info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `platform_id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/{platform_id}/get_file_manager_info' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取仅管理员可见的部门信息
**Endpoint**: `GET /v2/admin/department/{id}/info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/department/{id}/info' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 移除部门成员
**Endpoint**: `POST /v2/admin/department/{id}/remove_user`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |
| `user_id` | `body` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/{id}/remove_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 修改部门
**Endpoint**: `POST /v2/admin/department/{id}/update`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门id |
| `name` | `body` | `string` | 部门名称，长度不能超过30个字符 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/{id}/update' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 修改部门空间大小
**Endpoint**: `POST /v2/admin/department/{id}/update_space`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/department/{id}/update_space' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取详细的部门成员列表
**Endpoint**: `GET /v2/admin/department/{id}/users`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 部门ID |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/department/{id}/users' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, page_id
```

---

## 添加群组成员
**Endpoint**: `POST /v2/admin/group/{id}/add_user`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |
| `user_id` | `body` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/group/{id}/add_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 创建群组
**Endpoint**: `POST /v2/admin/group/create`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `name` | `body` | `string` | 群组名称，长度不能超过30个字符 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/group/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除群组
**Endpoint**: `POST /v2/admin/group/{id}/delete`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/group/{id}/delete' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 获取公司可见群组
**Endpoint**: `GET /v2/admin/group/list`

**Description**:
获取该公司的可见的群组列表 

 **需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/group/list' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, page_id
```

---

## 获取仅管理员可见的部门信息
**Endpoint**: `GET /v2/admin/group/{id}/info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/group/{id}/info' \
--header 'Authorization: Bearer <TOKEN>'
```

---

## 移除群组成员
**Endpoint**: `POST /v2/admin/group/{id}/remove_user`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |
| `user_id` | `body` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/group/{id}/remove_user' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 修改群组
**Endpoint**: `POST /v2/admin/group/{id}/update`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/group/{id}/update' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取群组成员列表
**Endpoint**: `GET /v2/admin/group/{id}/users`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 群组id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/group/{id}/users' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: query_words, page_id
```

---

## 获取日志操作类型信息
**Endpoint**: `POST /v2/admin/log/action_type_info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/log/action_type_info' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取日志信息
**Endpoint**: `POST /v2/admin/log/log_info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `end_date` | `body` | `string` | 截止时间，格式为：yyyy-MM-dd, 不得迟于今日 |
| `start_date` | `body` | `string` | 起始时间，格式为：yyyy-MM-dd, 不得早于今日前90天 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/log/log_info' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取日志信息列表
**Endpoint**: `POST /v2/admin/log/log_list`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `end_date` | `body` | `string` | 截止时间，格式为：yyyy-MM-dd, 不得迟于今日 |
| `start_date` | `body` | `string` | 起始时间，格式为：yyyy-MM-dd, 不得早于今日前90天 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/log/log_list' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 分页获取日志信息
**Endpoint**: `POST /v2/admin/log/log_list_by_pagination`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `date` | `body` | `string` | 日期，格式为：yyyy-MM-dd |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/log/log_list_by_pagination' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取关联部门
**Endpoint**: `GET /v2/admin/platform/{id}/mapping_department`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |
| `department_id` | `query` | `string` | 部门个性化id |
| `yfy_department_id` | `query` | `int64` | 亿方云平台上的部门id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/platform/{id}/mapping_department' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: department_id, yfy_department_id
```

---

## 获取关联群组
**Endpoint**: `GET /v2/admin/platform/{id}/mapping_group`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |
| `group_id` | `query` | `string` | 群组个性化id |
| `yfy_group_id` | `query` | `int64` | 亿方云平台上的群组id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/platform/{id}/mapping_group' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: group_id, yfy_group_id
```

---

## 获取关联用户
**Endpoint**: `GET /v2/admin/platform/{id}/mapping_user`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |
| `user_id` | `query` | `string` | 用户个性化id，user_id和yfy_user_id两个参数二选一，若都传则使用user_id |
| `yfy_user_id` | `query` | `int64` | 亿方云平台上的用户id，user_id和yfy_user_id两个参数二选一，若都传则使用user_id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/platform/{id}/mapping_user' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: user_id, yfy_user_id
```

---

## 批量同步部门
**Endpoint**: `POST /v2/admin/platform/{id}/sync_departments`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |
| `departments` | `body` | `array<object>` | 同步的部门信息 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/platform/{id}/sync_departments' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 批量同步群组
**Endpoint**: `POST /v2/admin/platform/{id}/sync_groups`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |
| `groups` | `body` | `array<object>` | 同步的群组信息 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/platform/{id}/sync_groups' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 批量同步用户
**Endpoint**: `POST /v2/admin/platform/{id}/sync_users`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 平台id，私有部署一般默认为：2 |
| `users` | `body` | `array<object>` | 同步的用户信息 |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/platform/{id}/sync_users' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 创建用户
**Endpoint**: `POST /v2/admin/user/create`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/user/create' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 删除用户
**Endpoint**: `POST /v2/admin/user/{id}/delete`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 用户ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/user/{id}/delete' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---

## 获取用户登录参数
**Endpoint**: `GET /v2/admin/user/get_login_params`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `identifier` | `query` | `string` | 用户标识，type为simple_phone_or_email时传手机或者邮箱，type为user_ticket时传第三方id |
| `type` | `query` | `string` | 用户标识类型；示例: `simple_phone_or_email(手机号或者邮箱), user_ticket(第三方id)` |
| `platform_id` | `query` | `int64` | 平台id，私有部署一般默认为：2 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/user/get_login_params' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: identifier, type, platform_id
```

---

## 获取用户登录链接
**Endpoint**: `GET /v2/admin/user/get_login_url`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `identifier` | `query` | `string` | 用户标识，type为simple_phone_or_email时传手机或者邮箱，type为user_ticket时传第三方id |
| `type` | `query` | `string` | 用户标识类型；示例: `simple_phone_or_email(手机号或者邮箱), user_ticket(第三方id)` |
| `platform_id` | `query` | `int64` | 平台id，私有部署一般默认为：2 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/user/get_login_url' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: identifier, type, platform_id
```

---

## 获取用户信息
**Endpoint**: `GET /v2/admin/user/get_user_info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `identifier` | `query` | `string` | 用户标识，type为simple_phone_or_email时传手机或者邮箱，type为user_ticket时传第三方id |
| `type` | `query` | `string` | 用户标识类型；示例: `simple_phone_or_email(手机号或者邮箱), user_ticket(第三方id)` |
| `platform_id` | `query` | `int64` | 平台id，私有部署一般默认为：2 |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/user/get_user_info' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: identifier, type, platform_id
```

---

## 获取仅管理员可见的用户信息
**Endpoint**: `GET /v2/admin/user/{id}/info`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 用户id |

**Curl Command**:
```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/admin/user/{id}/info' \
--header 'Authorization: Bearer <TOKEN>' # Query Params: last_login_flag
```

---

## 修改用户
**Endpoint**: `POST /v2/admin/user/{id}/update`

**Description**:
**需要使用企业token，根据企业id生成，详情参考上面生成的token文档**

**Required Parameters**:

| Name | In | Type | Description |
| --- | --- | --- | --- |
| `id` | `path` | `int64` | 用户ID |

**Curl Command**:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/admin/user/{id}/update' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{}'
```

---
## 新建文件收集
Endpoint: POST /v2/collection/create

Description: 新建一个文件收集任务。需要使用用户token，根据用户id生成，详情参考上面生成的token文档

Curl Command:

```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collection/create' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "typed_id": "folder_179000000087",
    "name": "2024年度总结收集",
    "description": "请大家在截止日期前提交",
    "is_anonymous": true,
    "invited_user_ids": ["123", "456"],
    "expired": 1735660800,
    "type": 1,
    "group_ids": ["789"],
    "template_file_id": "file_xxx",
    "template_file_version": "1",
    "name_rules": ["name", "id"],
    "keep_file_name": 1,
    "reminder_time": 1735574400
}'

接口必填字段 typed_id， name，expired
expired 默认过期时间 当前时间+15天
```
---

## 修改文件收集
Endpoint: POST /v2/collection/update

Description: 修改已有的文件收集任务设置。需要使用用户token，根据用户id生成，详情参考上面生成的token文档

Curl Command:
```bash
curl --location --request POST 'https://open.fangcloud.com/api/v2/collection/update' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "10001",
    "name": "2024年度总结收集(已更新)",
    "description": "补充了模板说明",
    "closed": false,
    "expired": 1735660800,
    "added_members": [111, 222],
    "deleted_members": [333],
    "added_group_ids": [444],
    "template_file_id": "file_yyy",
    "template_file_version": "2",
    "name_rules": ["department", "name"],
    "keep_file_name": 0
}'
```
---

## 获取公网收集未同步的文件信息
Endpoint: GET /v2/collection/get_files_info

Description: 获取公网收集任务中未同步的文件详情。需要使用用户token，根据用户id生成，详情参考上面生成的token文档

Curl Command:

```bash
curl --location --request GET 'https://open.fangcloud.com/api/v2/collection/get_files_info?process_id=987654321&create_time=1704067200' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN'

```

