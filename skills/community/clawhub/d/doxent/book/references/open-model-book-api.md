# open-model-book API

## 必读约束

- 端口、默认入口和 health 检查规则统一见 `../shared/port-and-health.md`
- 文本请求体的编码约束统一见 `../shared/encoding-rules.md`
- `/open-model/sync` 只在用户明确要求补同步，或排查跨模块同步时再使用

---

## 快速决策

| 用户意图 | 接口 |
| --- | --- |
| 「确认书架能力能不能用」 | `GET /open-model-book/health` |
| 「上传本地文件到书架」 | `POST /open-model-book/file/upload` |
| 「通过远程 URL 导入书架」 | `POST /open-model-book/file/upload` |
| 「补一次全量同步」 | `POST /open-model/sync` |

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

### UploadResult

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `localId` | string | 本地书籍记录 id |
| `name` | string | 最终书名 |
| `localPath` | string | 本地书籍目录中的实际文件路径 |
| `cloudId` | string | 云端书籍 id；如果上传未完成，可能为空 |
| `fileUrl` | string | 云端文件名 |
| `uploaded` | boolean | 是否已完成上传并拿到云端结果 |

---

## 接口详情

### 1. 健康检查

GET `/open-model-book/health`

**触发场景**：用户要先确认本地书架能力是否可用。

#### 请求参数

无

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | boolean | 是否启用 |
| `status` | string | 服务状态 |
| `service` | string | 服务名，通常为 `open-model-book` |
| `capabilityDetails` | array | 当前可用能力说明 |
| `message` | string | 未启用时的提示信息 |
| `configPath` | string | 配置文件路径 |

#### 说明

- 真实书籍导入、上传失败排查、接口启用检查时优先调用。
- 如果未启用、未授权或本地服务不可用，先提醒用户启动 Doxent/办公本客户端，并在客户端中开放本地接口授权。

---

### 2. 文件上传

POST `/open-model-book/file/upload`

**触发场景**：用户要把本地文件或远程 URL 导入到书架。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | string | 是 | 本地绝对路径，或远程 `http/https` URL |
| `name` | string | 否 | 文件名；如果远程 URL 没有扩展名，建议显式传入 |
| `localDirId` | string | 否 | 目标本地目录 id，默认 `0` |

#### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `UploadResult` | 上传结果对象 |

#### 返回示例

```json
{
  "localId": "string",
  "name": "AI基础.pdf",
  "localPath": "D:/.../books/<localId>/...pdf",
  "cloudId": "string",
  "fileUrl": "md5_timestamp.pdf",
  "uploaded": true
}
```

#### 说明

- 接口会先创建本地书籍记录。
- 然后把文件复制或下载到本地书籍目录。
- 再复用现有书籍上传链路，把文件上传到云端并保存书籍元数据。
- 默认放到书架根目录，不额外创建新分组。

#### 来源约束

| 场景 | 约束 |
| --- | --- |
| 本地路径 | 必须是绝对路径；如果文件不存在，会直接报错 |
| 远程 URL | 必须是 `http://` 或 `https://` |
| URL 无扩展名 | 如果无法识别扩展名且未传 `name`，不应猜测文件类型 |

---

### 3. 补同步

POST `/open-model/sync`

**触发场景**：用户明确要求“补一次全量同步”，或正在排查多模块同步状态。

#### 请求参数

无

#### 说明

- 对书籍上传来说通常不是必须步骤，因为 `file/upload` 已走现有上传链路。
- 返回成功只表示“已触发同步流程”，不等于所有数据已经在远端立即可见。
