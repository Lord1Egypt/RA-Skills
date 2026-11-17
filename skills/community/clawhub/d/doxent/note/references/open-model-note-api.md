# open-model-note API

## 必读约束

- 端口、默认入口和 health 检查规则统一见 `../shared/port-and-health.md`
- 高风险写操作与确认规则统一见 `../shared/write-and-sync.md`
- 文本请求体的编码约束统一见 `../shared/encoding-rules.md`

---

## 快速决策

| 用户意图 | 接口 |
| --- | --- |
| 「检查 note 能不能用」 | `GET /open-model-note/health` |
| 「按目录查看内容」「列出某个文件夹下的笔记」 | `GET /open-model-note/list` |
| 「只看笔记文件」「按关键词/时间筛笔记」 | `GET /open-model-note/fileList` |
| 「搜索笔记」「找名字里包含 XX 的笔记」 | `GET /open-model-note/search` |
| 「读取正文」「查看这篇笔记内容」 | `GET /open-model-note/file/content` |
| 「新建笔记」「从 Markdown 创建笔记」 | `POST /open-model-note/file/create` |
| 「新建文件夹」 | `POST /open-model-note/folder/create` |
| 「重命名笔记」 | `POST /open-model-note/file/rename` |
| 「重命名文件夹」 | `POST /open-model-note/folder/rename` |
| 「移动笔记」 | `POST /open-model-note/file/move` |
| 「移动文件夹」 | `POST /open-model-note/folder/move` |
| 「删除笔记」 | `POST /open-model-note/file/delete` |
| 「删除文件夹」 | `POST /open-model-note/folder/delete` |

---

## 通用返回

### 成功

```json
{
  "code": 200,
  "msg": "成功",
  "data": {}
}
```

### 失败

```json
{
  "code": 500,
  "msg": "错误信息"
}
```

---

## 数据结构

### OpenModelNoteItem

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 对象 id |
| `name` | string | 名称 |
| `type` | `folder \| file` | 对象类型 |
| `updateTime` | number | 更新时间 |

### OpenModelNoteFileContent

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 文件 id |
| `name` | string | 文件名 |
| `type` | `1 \| 2 \| 10 \| 20 \| 21 \| ...` | 笔记类型 |
| `content` | string | 规整后的正文文本 |

---

## 接口详情

### 1. 健康检查

GET `/open-model-note/health`

**触发场景**：用户要先确认本地 note 能力是否可用。

#### 请求参数

无

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | boolean | 是否启用 |
| `status` | string | 服务状态 |
| `service` | string | 服务名，通常为 `open-model-note` |
| `capabilities` | string[] | 当前可用接口列表 |

#### 返回示例

```json
{
  "enabled": true,
  "status": "ok",
  "service": "open-model-note",
  "capabilities": [
    "/open-model-note/health",
    "/open-model-note/list",
    "/open-model-note/fileList"
  ]
}
```

---

### 2. 列表

GET `/open-model-note/list`

**触发场景**：用户已知目录，想看某个文件夹下有哪些文件和文件夹。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `parentId` | string | 否 | 父文件夹 id，默认 `0` |
| `recursive` | boolean | 否 | 是否递归列出子文件夹中的文件和文件夹，默认 `false` |
| `startTime` | number | 否 | 修改时间开始 |
| `endTime` | number | 否 | 修改时间结束 |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `OpenModelNoteItem[]` | 当前目录下的文件夹和文件列表 |

#### 说明

- 根目录会合并 `dirId='0'` 和空目录下的笔记。
- `recursive=true` 时，会返回 `parentId` 目录下整棵子树中的文件夹和笔记，返回结果仍是扁平列表，不包含 `parentId` 自身。
- 已删除、已进回收站项会被过滤。
- 如果传了 `startTime` / `endTime`，会按 `updateTime` 做闭区间过滤。

---

### 3. 文件列表

GET `/open-model-note/fileList`

**触发场景**：用户只想看笔记文件，不需要文件夹；或者需要按关键词和时间范围做日报/周报素材筛选。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | string | 否 | 逗号分隔的关键词，匹配笔记名或摘要 |
| `keywords` | string | 否 | 同 `keyword` |
| `startTime` | number | 否 | 修改时间开始 |
| `endTime` | number | 否 | 修改时间结束 |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `OpenModelNoteItem[]` | 仅笔记文件列表 |

#### 说明

- 不返回文件夹。
- 多关键词采用“任一命中”策略。
- 搜索大小写不敏感。
- 如果传了 `startTime` / `endTime`，会按 `updateTime` 进一步过滤结果。

---

### 4. 搜索

GET `/open-model-note/search`

**触发场景**：用户按名字搜索笔记或文件夹。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | string | 是 | 搜索关键字 |
| `startTime` | number | 否 | 修改时间开始 |
| `endTime` | number | 否 | 修改时间结束 |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `OpenModelNoteItem[]` | 搜索命中的文件夹和文件 |

#### 说明

- 只按名称搜索。
- 文件夹和笔记都会命中。
- 搜索大小写不敏感。
- 如果传了 `startTime` / `endTime`，会按 `updateTime` 进一步过滤结果。

---

### 5. 获取文件内容

GET `/open-model-note/file/content`

**触发场景**：用户要读取笔记正文、做摘要或进一步分析。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件 id |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `OpenModelNoteFileContent` | 文件内容对象 |

#### 支持类型

| 类型 | 规整方式 |
| --- | --- |
| `RICH` | 优先 `contentText`，否则从 html 去标签 |
| `RECORD` | 读取文本转写文件并整理段落 |
| `COMPLEX` | 按页、按块提取文字 |
| `MIND` | 转成树状列表文本 |
| `MIXTURE` | 按页拼接，必要时回退到 regular 内容 |

---

### 6. 创建文件

POST `/open-model-note/file/create`

**触发场景**：用户要新建笔记，或把 Markdown 内容保存成笔记。

#### 请求格式

- 必须使用 `POST`。
- 请求头必须为 `Content-Type: application/json; charset=utf-8`。
- 请求体必须是 JSON 对象，不支持 URL 查询串、表单 body 或 `parentId=root` 这类裸字符串。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `parentId` | string | 否 | 父文件夹 id，默认 `0` |
| `name` | string | 是 | 文件名 |
| `markdown` | string | 否 | Markdown 内容，可为空 |

#### 请求示例

```json
{
  "parentId": "0",
  "name": "20260430 热点",
  "markdown": "# 今日热点\n\n- **美股**：示例内容"
}
```

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 新文件 id |
| `name` | string | 新文件名 |

#### 返回示例

```json
{
  "id": "noteId",
  "name": "noteName"
}
```

#### 说明

- `markdown` 必须是真 Markdown：标题用 `#`，列表用 `-`/`1.`，加粗用 `**文本**`，不要传 `<h1>`、`<ul>`、`<li>`、`<b>` 等 HTML 标签。
- 内部会把 markdown 转换成 html 后创建为笔记。

---

### 7. 创建文件夹

POST `/open-model-note/folder/create`

**触发场景**：用户要整理目录结构，创建新的文件夹。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `parentId` | string | 否 | 父文件夹 id，默认 `0` |
| `name` | string | 是 | 文件夹名 |

#### 说明

- 创建前会先校验父目录存在。

---

### 8. 重命名文件

POST `/open-model-note/file/rename`

**触发场景**：用户要修改笔记标题。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件 id |
| `name` | string | 是 | 新文件名 |

#### 说明

- 只更新笔记属性，不触发内容更新标记。

---

### 9. 重命名文件夹

POST `/open-model-note/folder/rename`

**触发场景**：用户要修改文件夹名称。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件夹 id |
| `name` | string | 是 | 新文件夹名 |

#### 说明

- 会同步更新该目录下直属笔记的 `dirName`。

---

### 10. 移动文件

POST `/open-model-note/file/move`

**触发场景**：用户要把一篇或多篇笔记移动到别的文件夹。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件 id，支持多个 id 用逗号分隔 |
| `parentId` | string | 否 | 目标文件夹 id，默认 `0` |

#### 说明

- 只切换所属目录，不处理排序。
- 批量移动时会顺序执行，其中一个失败会中断后续处理。

---

### 11. 移动文件夹

POST `/open-model-note/folder/move`

**触发场景**：用户要调整文件夹层级。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件夹 id，支持多个 id 用逗号分隔 |
| `parentId` | string | 否 | 目标文件夹 id，默认 `0` |

#### 说明

- 不支持移动根目录。
- 不允许移动到自己或自己的子孙目录。
- 如果目标目录下已存在同名文件夹，会自动重命名为 `名称(1)`、`名称(2)` 再移动。
- 批量移动时会顺序执行，其中一个失败会中断后续处理。

---

### 12. 删除文件

POST `/open-model-note/file/delete`

**触发场景**：用户明确确认后删除一篇或多篇笔记。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件 id，支持多个 id 用逗号分隔 |

#### 说明

- 实际调用的是回收站删除逻辑 `recycleNote`。
- 删除前应先确认对象存在。
- 批量删除时会顺序执行，其中一个失败会中断后续处理。

---

### 13. 删除文件夹

POST `/open-model-note/folder/delete`

**触发场景**：用户明确确认后删除整个文件夹树。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | 文件夹 id，支持多个 id 用逗号分隔 |

#### 说明

- 会递归删除子文件夹。
- 会将目录下所有笔记移入回收站/删除流程。
- 风险比删单文件高，调用前必须确认。
- 批量删除时会顺序执行，其中一个失败会中断后续处理。
