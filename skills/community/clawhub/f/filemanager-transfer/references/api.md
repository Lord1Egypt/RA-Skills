 `scripts/.env`下配置有url与appkey

```
FILEMANAGER_BASE_URL=http://localhost:8080
FILEMANAGER_APPKEY=fm_app_xxxxxxxxxxxxxxxxx
```

### 文件接口

#### GET /api/files?path=/

列出目录内容。

```
curl -H "Authorization: Bearer $APPKEY" "http://localhost:8080/api/files?path=/"
```

#### POST /api/files/upload?path=/target

上传文件。请求体为 `multipart/form-data`，文件字段名为 `file`，可选 `remark`。

```
curl -H "Authorization: Bearer $APPKEY" \
  -F "file=@demo.txt" \
  -F "remark=备注" \
  "http://localhost:8080/api/files/upload?path=/"
```

#### GET /api/files/download/{id}

下载文件。

```
curl -H "Authorization: Bearer $APPKEY" \
  -OJ "http://localhost:8080/api/files/download/{id}"
```

#### GET /api/files/info?id={id}

查看文件或目录信息。

```
curl -H "Authorization: Bearer $APPKEY" \
  "http://localhost:8080/api/files/info?id={id}"
```

#### PATCH /api/files/remark

修改文件或目录备注。

```
curl -X PATCH -H "Authorization: Bearer $APPKEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"file_id","remark":"备注"}' \
  "http://localhost:8080/api/files/remark"
```

### 分享接口

#### POST /api/share

创建带密码的文件分享。需要 AppKey，且 `password` 不能为空。

```
curl -X POST -H "Authorization: Bearer $APPKEY" \
  -H "Content-Type: application/json" \
  -d '{"file_id":"file_id","password":"share_password","expires_hours":24}' \
  "http://localhost:8080/api/share"
```

#### GET /api/share/{share_id}

查看公开分享信息。无需 AppKey。

#### POST /api/share/{share_id}/access

访问分享，成功后返回临时下载 token。无密码分享可传空 JSON；有密码分享传 `password`。

```
curl -X POST -H "Content-Type: application/json" \
  -d '{"password":"share_password"}' \
  "http://localhost:8080/api/share/{share_id}/access"
```

#### GET /api/share/{share_id}/download

下载分享文件。必须使用 `X-Share-Token` 请求头，不支持 URL 参数传 token。

```
curl -H "X-Share-Token: $TEMP_TOKEN" \
  -OJ "http://localhost:8080/api/share/{share_id}/download"
```