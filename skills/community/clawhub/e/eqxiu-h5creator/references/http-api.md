# 易企秀 AIGC HTTP 接口说明

默认 API 根地址：`https://ai-api.eqxiu.com`（环境变量 `EQXIU_AIGC_API_BASE` 可覆盖）。

鉴权：请求头 `X-Openclaw-Token`。获取地址：<https://www.eqxiu.com/skillAccess/token>。

---

## 一键生成 H5（流式）

- **方法 / 路径**：`POST /aigc/draw/ai/create/stream`
- **请求头**：`Content-Type: application/json;`、`X-Openclaw-Token`、`Origin: https://ai.eqxiu.com`、`Referer: https://ai.eqxiu.com/`
- **Body**：

```json
{
  "userPrompt": "<用户需求全文>",
  "productCodeSub": "P010245"
}
```

- **响应**：SSE，`event:message` + `data:{json}`。进度示例：

  `正在匹配风格` → `正在生成内容` → `正在创建页面 n/5` → `组装最终作品` → `生成成功！`

- **成功时最后一条 `data` 中的 `data` 字段**（以实际返回为准）：

```json
{
  "id": 266508416,
  "code": "8Oq4jKkn",
  "editUrl": "https://www.eqxiu.com/c/266508416",
  "previewUrl": "https://h5.eqxiu.com/hs/8Oq4jKkn",
  "publish": true
}
```

- **错误**：某条 `data` 中 `success: false` 或 `code != 200`。

---

## 作品页：可编辑文本与配图（iaigc）

基路径：`{API_BASE}/iaigc/h5_scene/...`，均需 `X-Openclaw-Token`。

### 获取可编辑文本

- `GET /iaigc/h5_scene/get_editable_text?id={scene_id}`

### 更新可编辑文本并发布

- `POST /iaigc/h5_scene/update_editable_text?id={scene_id}&page_id={page_id}`
- **Body**：

```json
{
  "element_id": 123,
  "content": "更新后的文案",
  "css": { "fontSize": "32" }
}
```

`css` 可选。

### 查询正文配图

- `GET /iaigc/h5_scene/get_body_images?id={scene_id}`
- 可选查询参数：`page_id`

返回 `data` 为数组，含各页 `elements`（`id`、`src`、`src_url` 等）。

### 替换正文配图

- `POST /iaigc/h5_scene/replace_body_image?id={scene_id}&page_id={page_id}`
- **Body**：

```json
{
  "element_id": "<元素 id>",
  "src": "<新图 path 或 URL>",
  "sourceId": "<可选>"
}
```

---

## 素材库（material-api，非 iaigc）

默认根地址：`https://material-api.eqxiu.com`（`EQXIU_MATERIAL_API_BASE`）。

### 查询用户上传素材

- `GET …/m/material/user/upload/list2`
- 查询参数：`fileType`、`pageNo`、`pageSize`、`tagId` 等（与 CLI `material-list` 一致）

### 上传本地文件

流程：向 `emw-api.eqxiu.com` 取 COS 临时凭证 → 上传 COS → `saveFile` 登记素材。详见客户端 `upload` 实现；需 `cos-python-sdk-v5`。

---

## 认证校验

- 客户端 `auth status` 调用 passport 用户信息接口校验 token。
- `success: false` 且 `code: 1002` 表示认证失败，需重新获取 token。
