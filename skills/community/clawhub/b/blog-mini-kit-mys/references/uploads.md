# 文件上传 API（4 端点）

路径前缀：`{base_url}` · 无认证

> 上传文件保存到服务器 `/uploads/` 目录，返回访问 URL。
> 已上传文件通过 `{base_url}/uploads/{filename}` 访问。

## 允许的文件类型

- 图片：.jpg .jpeg .png .gif .webp .bmp .svg
- 视频：.mp4 .webm .ogg .mov .avi .mkv
- 文档：.pdf .doc .docx .txt .zip .tar .gz .md

## 1. POST /api/upload — 上传单个文件

**子命令**：`upload-file`

Body（multipart/form-data，字段名 `file`）：

```bash
curl -s --max-time 30 -X POST -F "file=@/path/to/image.jpg" "{base_url}/api/upload"
```

响应：
```json
{"code":200,"data":{"url":"/uploads/abc123.jpg","filename":"image.jpg","type":"image","size":10240}}
```

> `type` 取值：image / video / file

## 2. POST /api/upload/multiple — 批量上传文件

**子命令**：`upload-files`

Body（multipart/form-data，字段名 `files`，多值）：

```bash
curl -s --max-time 30 -X POST -F "files=@a.jpg" -F "files=@b.png" "{base_url}/api/upload/multiple"
```

响应：
```json
{"code":200,"data":[{"url":"/uploads/x.jpg","filename":"a.jpg","type":"image","size":1024},{"url":"/uploads/y.png","filename":"b.png","type":"image","size":2048}]}
```

> 单个文件类型不支持时，该项返回 `{"filename":"...","error":"不支持的文件类型: .xxx"}`。

## 3. GET /api/uploads/list — 列出已上传文件

**子命令**：`list-uploads`

```bash
curl -s --max-time 30 "{base_url}/api/uploads/list"
```

响应：
```json
{"code":200,"data":[{"filename":"abc123.jpg","url":"/uploads/abc123.jpg","type":"image","size":10240}]}
```

## 4. DELETE /api/uploads/{filename} — 删除已上传文件

**子命令**：`delete-upload`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| filename | path | string | 是 | 文件名（仅 basename，防路径穿越） |

响应：`{"code":200,"message":"文件已删除"}` · 404 文件不存在
