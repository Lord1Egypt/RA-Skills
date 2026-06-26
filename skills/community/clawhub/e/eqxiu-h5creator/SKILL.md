---
name: eqxiu-h5creator
description: |
  易企秀 AIGC H5 创作工具：用户用自然语言描述需求，通过 CLI `create` 一键生成翻页 H5（邀请函、海报、活动页等）。

  核心流程：
  1. 收集用户完整需求 → `create --prompt "..."`
  2. 交付 `previewUrl`、`editUrl`
  3. （可选）`editable-text` → `update-text`；或 `body-images` / `upload` / `replace-body-image`

  触发词：制作H5、生成H5、创建H5、做一个H5、易企秀、
  H5邀请函、年会H5、婚礼邀请函、会议邀请函、生日祝福H5、
  节日海报H5、H5页面生成、翻页H5怎么做、怎么做一个邀请函H5

summary: |
  易企秀 AIGC 创作 Skill：使用 `scripts/eqxiu_aigc_client.py` 子命令；HTTP 接口见 references/http-api.md。

read_when:
  - 用户提到"制作/生成/创建 H5"、"做个邀请函"、"做一张年会海报"
  - 用户想用易企秀生成翻页 H5
  - 用户要换 H5 里的图片、上传素材或修正文案
---

# 易企秀 AIGC CLI

入口：`python scripts/eqxiu_aigc_client.py <子命令> [参数]`（实现：`scripts/eqxiu_aigc/`）。

- 对话推荐流程：[references/workflow.md](references/workflow.md)
- HTTP 接口说明：[references/http-api.md](references/http-api.md)
- Token：先 `login`，或 `--access-token`；获取地址 <https://www.eqxiu.com/skillAccess/token>

## 全局参数（任意子命令前）

| 参数 | 默认 | 说明 |
|------|------|------|
| `--access-token` | `~/.eqxiu/config.json` | `X-Openclaw-Token`，覆盖配置文件 |

## `login`

交互式保存 token，无额外参数。

## `auth status`

验证 token 是否有效，无额外参数。`success: true` 有效；`code: 1002` 需重新登录。

## `create`

流式一键生成 H5。

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `--prompt` | 是 | — | 用户需求全文（活动主题、时间、地点、受众、风格等） |
| `--product-code-sub` | 否 | `P010245` | 产品子码（`EQXIU_PRODUCT_CODE_SUB`） |

stdout：JSON，含 `data`、`previewUrl`、`editUrl`、`progress`（进度文案列表）。`data.id` 即后续 `--scene-id`。

## `editable-text`

获取作品可编辑文本。

| 参数 | 必填 | 说明 |
|------|------|------|
| `--scene-id` | 是 | 作品 id（`create` 的 `data.id`） |

## `update-text`

更新某一文本元素并发布。

| 参数 | 必填 | 说明 |
|------|------|------|
| `--scene-id` | 是 | 作品 id |
| `--page-id` | 是 | 页 id（来自 `editable-text` 结果） |
| `--element-id` | 是 | 元素 id |
| `--content` | 是 | 更新后的文案 |
| `--css-json` | 否 | 元素样式 JSON 字符串，如 `'{"fontSize":"32"}'` |
| `--preview-url` | 否 | 原样写入 stdout JSON 的 `previewUrl` 字段 |

## `body-images`

查询作品中可替换的正文配图。

| 参数 | 必填 | 说明 |
|------|------|------|
| `--scene-id` | 是 | 作品 id |
| `--page-id` | 否 | 仅查询指定页 |

## `replace-body-image`

替换正文配图。

| 参数 | 必填 | 说明 |
|------|------|------|
| `--scene-id` | 是 | 作品 id |
| `--page-id` | 是 | 页 id |
| `--element-id` | 是 | 配图元素 id |
| `--src` | 是 | 新图 path 或 URL（可先 `upload` 取得） |
| `--source-id` | 否 | 写入 `properties.sourceId` |

## `material-list`

查询当前用户已上传素材。

| 参数 | 默认 | 说明 |
|------|------|------|
| `--file-type` | `1` | 文件类型（1 一般为图片） |
| `--page-no` | `1` | 页码 |
| `--page-size` | `30` | 每页条数 |
| `--tag-id` | `-1` | 标签 id |
| `--material-api-base` | `https://material-api.eqxiu.com` | 素材 API 根地址 |

## `upload`

本地文件上传 COS 并登记素材库（需 `pip install cos-python-sdk-v5`）。

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `--file` | 是 | — | 本地文件路径 |
| `--bucket` | 否 | `eqxiu` | COS bucket |
| `--prefix` | 否 | `/material/` | COS 路径前缀 |
| `--name` | 否 | 文件名 | COS 对象名 |
| `--tmb-path` | 否 | 同 key | saveFile 的 tmbPath |
| `--source` | 否 | `P010245` | saveFile 的 source（`EQXIU_MATERIAL_SOURCE`） |
| `--tag-id` | 否 | `-1` | saveFile tagId |
| `--file-type` | 否 | `1` | saveFile fileType |
| `--cos-api-base` | 否 | `https://emw-api.eqxiu.com` | COS 凭证接口根 |
| `--material-api-base` | 否 | `https://material-api.eqxiu.com` | saveFile 接口根 |
