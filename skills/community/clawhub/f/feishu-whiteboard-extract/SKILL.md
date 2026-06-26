---
name: feishu-whiteboard-extract
description: 从飞书白板（Whiteboard）中提取所有图片节点的 file_token，用于后续下载/OCR/归档。文档类补充能力。
---

# Feishu Whiteboard Extract

从飞书白板/画板（whiteboard）里**提取所有图片节点对应的 `file_token`**，便于后续把图片下载到本地做 OCR/归档。

> 定位：文档/资料处理链路的补充能力（不是会话发消息）。

## 用法

```bash
node skills/feishu-whiteboard-extract/extract_images.js <whiteboard_id>
# 说明：当前 SDK 调用路径为 client.board.v1.whiteboardNode.list
```

## 输出

脚本输出 JSON：

- `whiteboard_id`
- `count`
- `images[]`：每项包含 `node_id` 与 `file_token`

拿到 `file_token` 后，可用：

- `skills/feishu-drive-download/scripts/download.js <file_token>` 下载
- 或用官方 `feishu_drive` 工具下载

## 标准交付补充：整板全图导出（矢量优先）

- **整板全图（整板大图）是标准交付的第二部分**：
  1) 第一部分：逐节点图片提取（`extract_images.js`，用于下载/OCR）
  2) 第二部分：整板全图导出（`export_board_svg.js`，用于复核与归档）
- 这两部分是**互补关系**：节点提取便于结构化处理，整板导出保证全局上下文与可视化复查。

### 整板矢量导出

```bash
# 直接输出到 stdout（优先返回 SVG，若服务端降级则可能返回 PNG/JPG）
node skills/feishu-whiteboard-extract/export_board_svg.js <whiteboard_id>

# 输出到文件（会按响应 Content-Type 自动修正扩展名）
node skills/feishu-whiteboard-extract/export_board_svg.js <whiteboard_id> /tmp/board_full.svg
```

实现说明：

- 调用 OpenAPI：`GET /open-apis/board/v1/whiteboards/:whiteboard_id/download_as_image`
- `Accept` 优先请求 `image/svg+xml`，并兼容 png/jpeg fallback
- 若返回 `image/svg+xml`，保存为 `.svg`
- 否则按 content-type 推断扩展名（`.png`/`.jpg`/`.gif`）

### 归档到知识库附件目录（appendix）

建议将整板全图落盘到交付目录：

```bash
# 单白板交付
node skills/feishu-whiteboard-extract/export_board_svg.js <whiteboard_id> appendix/board_full.svg

# 多白板交付（避免覆盖）
node skills/feishu-whiteboard-extract/export_board_svg.js <whiteboard_id> appendix/<whiteboard_id>_full.svg
```

---

## Extraction Playbook（经验/踩坑）

这一节总结了**白板链接提取 ID、常见报错定位、以及推荐的端到端工作流**。

### 1) `whiteboard_id` / token 从哪里来？如何从链接中提取？

在飞书里，"白板/画板"通常以链接形式分享。脚本入参一般需要 `whiteboard_id`（或你在 SDK/API 里看到的 *whiteboard token*）。

#### 常见 URL 样式（尽量不依赖域名）

不同租户/环境的域名可能不一样，但路径形态通常类似：

- **直接白板链接**
  - `https://<host>/board/<whiteboard_id>`
  - `https://<host>/board/<whiteboard_id>?from=...`

- **带路由前缀/应用前缀**（本质仍然能在路径中找到板子的 token）
  - `https://<host>/base/board/<whiteboard_id>`
  - `https://<host>/workspace/board/<whiteboard_id>`

- **分享链接（share）/短链跳转**
  - `https://<host>/board/share/<share_token>`
  - `https://<host>/s/<short_token>`

> 经验：**能从链接里直接看到的那段"看起来像 ID/token"的字符串**，优先当作候选。

#### 提取方法（实用优先）

1. **优先从路径段提取**：
   - 把 URL 的 path 按 `/` 分割，找到 `board` 或 `whiteboard` 后面的那一段。
2. **其次从 query 参数提取**：
   - 少数场景会把 token 放在 `?whiteboard_id=...` / `?token=...` 之类的参数里。
3. **遇到 share/短链**：
   - share token 往往 **不是** `whiteboard_id`。
   - 处理方式：让用户提供"打开后地址栏里的真实白板链接"，或在浏览器里完成跳转后再取最终 URL 中的 ID。

> 建议：让用户直接粘贴**浏览器地址栏最终落地的 URL**，比转发的分享卡片/短链更稳定。

### 与 Docx 嵌入白板联动（block_type=43）

当白板是**作为 Docx 的嵌入块**出现时，`feishu_doc.read` 可能读到的正文几乎为空。这时最稳定的做法是：

1) 对 Docx 调用 `feishu_doc.list_blocks`
2) 在返回的 blocks 里找到 `block_type = 43` 的块（whiteboard embed）
3) 从该 block 的 JSON 中取出 `whiteboard_id` / `whiteboard.token`（字段名可能因版本不同略有差异）
4) 把这个 token 作为脚本入参执行提取

示例（伪代码/思路）：

- Docx：
  - `feishu_doc.list_blocks(doc_token)` → 找到 `block_type == 43` → 复制里面的 whiteboard token
- Whiteboard：

```bash
node skills/feishu-whiteboard-extract/extract_images.js <whiteboard_id> > images.json
```

> 典型坑：**分享链接里的 share token 不是 whiteboard_id**。
> - 表现：用 share token 跑脚本经常 404 / 看起来"找不到"
> - 修复：用"最终落地的白板 URL"里的真实 id，或直接从 Docx 的 `block_type=43` block 里取 token

拿到 `images.json` 后，把 `images[].file_token` 接到下载链路：

```bash
# 下载单个：
node skills/feishu-drive-download/scripts/download.js <file_token>

# 批量下载（示例）：
# jq -r '.images[].file_token' images.json | while read -r t; do node skills/feishu-drive-download/scripts/download.js "$t"; done
```

### 2) 常见错误与定位

#### ⚠️ 节点图片下载必须用 `medias` 接口，不是 `files` 接口！

这是一个**高频踩坑点**，已实际触发过 403：

| 接口 | 路径 | 白板节点图 |
|------|------|-----------|
| ❌ 错误 | `drive/v1/files/{file_token}/download` | → **403 Forbidden** |
| ✅ 正确 | `drive/v1/medias/{file_token}/download` | → **200 OK** |

白板节点图片的 `file_token` 属于**媒体文件**，必须走 `medias` 端点。  
`download_media.js` 已修复为直接 HTTP 调用（而非 SDK，规避 SDK 内部路由歧义）。  
**无需用户级 token，tenant_access_token 即可下载。**

#### 403 / 404（权限 / 分享 / 可见性）

- **403 Forbidden**：通常是权限不足
  - 白板未分享给应用（bot）
  - 应用未在对应文档/空间有访问权限
  - ⚠️ 或者用了 `files` 端点而不是 `medias` 端点（见上方）
- **404 Not Found**：通常是对象不可见/不存在
  - `whiteboard_id` 提取错了（拿了 share token 当 whiteboard_id）
  - 目标白板被删除/迁移，或当前凭证无权"看到"它（有时也会表现为 404）

排查要点：

- **先检查是否用了正确的下载端点**（`medias` vs `files`）。
- 再确认 `whiteboard_id` 是否来自**最终落地链接**。
- 再确认白板（或所在空间/文档）是否已对应用开放访问（见下文"权限/授权"）。

#### 400（id 格式 / 字段校验）

常见原因：

- `whiteboard_id` 格式不合法（包含多余字符、截断、把整段 URL 当 ID 传入）
- 请求字段校验失败（比如分页参数、父节点参数等）

排查要点：

- 确保传入的是纯 token/id 字符串，而不是 URL。
- 把脚本日志里请求参数打印到 debug（但不要打印敏感信息），逐项对照 SDK 的参数定义。

#### `method undefined` / `xxx is not a function`（SDK path 版本差异）

这类错误通常不是权限问题，而是 **SDK 调用路径/版本差异**：

- 你以为是 `client.xxx.yyy.list()`，但当前 SDK 版本实际是另一条路径
- 本技能已踩坑修复过：应使用 `client.board.v1.whiteboardNode.list`

排查要点：

- 先检查本地 `@larksuiteoapi/node-sdk` 版本与代码里的调用路径是否匹配。
- 若升级/降级 SDK，重新确认对应 API 的挂载路径（v1/v2、命名空间差异）。

### 3) 推荐工作流（extract_images → 下载 → OCR → 结构化输出/回填）

目标：**白板 → 图片节点 → 下载图片 → OCR → 结构化输出/回填**。

1. **提取图片 token**

   ```bash
   node skills/feishu-whiteboard-extract/extract_images.js <whiteboard_id> > images.json
   ```

2. **拿 `file_token` 下载图片**

   - 从 `images.json` 里取出 `images[].file_token`
   - 下载（使用修复后的脚本，走 `medias` 端点）：

     ```bash
     # 推荐：download_media.js（已修复为 medias 端点，tenant token 即可）
     node skills/feishu-whiteboard-extract/download_media.js <file_token> <save_path>

     # 批量下载示例：
     jq -r '.images[].file_token' images.json | while read -r t; do
       node skills/feishu-whiteboard-extract/download_media.js "$t" "output/$t.png"
     done
     ```

   > ⚠️ 不要用 `feishu-drive-download/scripts/download.js` 下载白板节点图——那个脚本走 `files` 端点，白板图片会 403。

3. **OCR / 图像理解**

   - 将下载到本地的图片交给 `image` 工具做 OCR/识别
   - 建议输出结构：
     - `node_id`
     - `file_token`
     - `local_path`
     - `ocr_text`
     - `key_points` / `todo` / `entities`（按你的业务需要）

4. **回填/结构化输出**

   - 将识别结果写回到你的知识库/文档（例如 Feishu Doc、Wiki、Bitable），或导出 Markdown/JSON 归档。

### 4) 权限 / 授权（让用户怎么做）

只描述操作要点（不涉及任何凭证）：

- **确保白板对应用可见**：
  - 在白板的"分享/权限"设置中，把对应的 **机器人/应用**（或应用关联的帐号）加入协作者，至少赋予"可查看"。
- **若白板隶属某个空间/知识库**：
  - 需要在空间/知识库层面也把应用加入成员，避免出现"空间不可见导致 403/404"。
- **确认应用权限范围（scope）**：
  - 若一直 403，除了分享外，也要确认应用在开发者后台已开通白板/云文档/云空间相关权限。

> 经验：**"分享给我个人能打开"不代表"分享给 bot/app 能访问"**。需要明确把应用加入协作。

### 5) 安全注意事项

- 不要在聊天里粘贴/暴露：webhook、appSecret、token、cookie 等敏感信息。
- 脚本日志/调试输出：
  - 只打印必要的请求参数与错误摘要
  - **不要打印 `appSecret`**（包括从环境变量或 `~/.openclaw/openclaw.json` 读取到的值）
- 如果需要用户提供链接用于排查：
  - 让用户尽量提供不包含敏感 query 的"干净链接"（必要时可让其打码）。
