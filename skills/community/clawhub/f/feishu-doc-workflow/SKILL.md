---
name: feishu-doc-workflow
description: Feishu 文档写作与排版工作流。处理飞书 docx 的正文改写、分段润色、插图、按块定位插入、补充链接、以及把文档权限改成“互联网获得链接的人可查看”等公开分享设置时使用。也用于排查“能读不能写”“插图位置不对”“文档写入 400/403”这类飞书文档问题。
---

# Feishu Doc Workflow

用这个 skill 处理 **飞书 docx 文档本体** 的写作、排版、插图、公开分享和排障。

## 这个 skill 能不能给别人用？

能。这个 skill 本质上是一套 **飞书文档工作流说明书**，不是绑定某个私人账号的硬编码脚本。

但它不是“裸技能包到处都能跑”的那种万能包。别人要正常使用，至少要满足：

- OpenClaw 环境里能用 `feishu_doc`
- 已配置飞书 channel（有 `appId` / `appSecret`）
- 具备本文档里列出的飞书权限
- 若要复用“公开分享给互联网可读”这一步，环境还需要允许通过 `exec` 调用 Feishu OpenAPI

## 是否必须安装新版飞书插件？

**不绝对要求“必须是最新版官方插件”**，但要求环境里已经具备等价能力。

更准确地说，这个 skill 依赖的是：

- 最近版本的 OpenClaw / Feishu 扩展
- `feishu_doc` 工具可用
- 飞书 app 凭证可用
- Drive public permission API 可调用

所以：

- 如果别人已经有一套能正常提供 `feishu_doc` 的飞书集成，这个 skill 就能复用
- 如果别人环境太老，或者根本没有 `feishu_doc`，那这个 skill 不能直接开箱即用

**最稳妥的发布建议**：默认面向“已接好飞书、且 `feishu_doc` 正常可用”的 OpenClaw 用户发布。

## 发布给别人前，最好写清楚的飞书权限

按当前这套 skill 的能力，建议至少写清下面这些 **最低测试通过权限**：

- `docx:document`
- `docx:document:readonly`
- `docx:document.block:convert`
- `drive:drive`

如果发布说明要写得更实用，再补两条环境前提：

- `channels.feishu.appId` 已配置
- `channels.feishu.appSecret` 已配置

其中：

- 文档读写、按块改写、插图定位，核心依赖 `docx:*` + `drive:drive`
- “互联网获得链接的人可查看” 这类公开分享设置，核心依赖 Drive public permission API；当前实测用 `drive:drive` 可完成

## 建议在发布页附的兼容性说明

可以直接写成：

> 本 skill 面向已完成飞书集成的 OpenClaw 用户。要求环境中 `feishu_doc` 工具可用，且飞书应用至少具备 `docx:document`、`docx:document:readonly`、`docx:document.block:convert`、`drive:drive` 权限。若需将文档开成“互联网获得链接的人可查看”，还需在当前环境允许通过 API 更新 Drive public permission。

## 推荐 OpenClaw 最低版本

建议写成：

- **推荐 OpenClaw 版本：2026.3.8 及以上**

原因不是“这个 skill 只认某个版本号”，而是当前内容已经按我这次实际验证通过的环境来写：

- OpenClaw `2026.3.8`
- 可用 `feishu_doc`
- 可通过 Feishu Drive API 更新 public permission

如果别人版本更老，但 `feishu_doc` 与相关权限链路都正常，也可能能用；只是**公开发布时最好写“推荐 2026.3.8+”**，避免踩旧环境坑。

## 推荐飞书插件形态

公开说明里建议明确：

- **优先推荐使用当前可正常提供 `feishu_doc` 能力的 Feishu 集成环境**
- 对 OpenClaw 用户来说，最稳妥的是：
  - 已启用当前内置 / stock `feishu` 扩展，或
  - 使用功能等价、已验证可提供 `feishu_doc` 的 Feishu 插件方案

不要把发布文案写成“必须安装某一个特定插件版本”，而应写成：

> 只要你的 OpenClaw 环境已经具备 `feishu_doc` 工具能力，并配置好了飞书 app 凭证，本 skill 就可使用。

## 安装前检查清单

发布时建议附这个 checklist：

- 已完成 OpenClaw 基础安装
- OpenClaw 版本建议 `2026.3.8+`
- `feishu_doc` 工具可用
- `channels.feishu.appId` 已配置
- `channels.feishu.appSecret` 已配置
- 飞书应用已开以下权限：
  - `docx:document`
  - `docx:document:readonly`
  - `docx:document.block:convert`
  - `drive:drive`
- 若需要“互联网获得链接的人可查看”：当前环境允许通过 API 调用 Feishu Drive public permission

## 常见报错速查表

### 1. `400` 写文档失败

先查：

- 是否缺 `docx:document.block:convert`

这是最常见根因。没有这个权限时，经常表现为：

- 能读文档
- 但 `write` / `append` / `update_block` / `insert` 报 `400`

### 2. `403` 能读不能写

先查：

- 这篇具体文档有没有给“小龙虾（应用）”开**可编辑**权限

也就是：

- scope 够，不代表对象权限一定够
- 应用有写权限 + 文档对象也允许编辑，这两层都得通

### 3. 图片插入成功但位置不对

先查：

- 有没有先 `list_blocks`
- `parent_block_id` / `index` 有没有按当前块顺序计算

解决原则：

- 插错了就直接 `delete_block`
- 再按正确位置重新 `upload_image`

### 4. 文档已经开了外部访问，但外网还是打不开

先查：

- `external_access_entity` 是否为 `open`
- `security_entity` 是否为 `anyone_can_view`
- `link_share_entity` 是否为 `anyone_readable`

不要只看 PATCH 成功，要再 GET 一次确认最终值。

## 快速判断

- **改正文内容** → 用 `feishu_doc` 的 `read` / `write` / `append` / `insert` / `update_block`
- **调整图片位置或补图** → 用 `feishu_doc` 的 `list_blocks` + `upload_image` + 必要时 `delete_block`
- **把文档开成互联网可读** → 走 Feishu Drive public permission 接口（见下文）
- **发送普通文件给用户**（HTML / ZIP / PDF / 代码文件）→ 不用本 skill，改看 `skills/feishu-send-file/SKILL.md`

## 推荐工作流

### 1. 先读，再改

编辑已有飞书文档时，优先按这个顺序：

1. `feishu_doc(action="read")` 看标题、正文摘要、块类型
2. 如果涉及图片、表格、精确位置插入，再 `feishu_doc(action="list_blocks")`
3. 再决定是：
   - 小改几段 → `update_block`
   - 在某段后面补内容 → `insert`
   - 文档尾部补内容 → `append`
   - 整篇重写 → `write`

不要一上来就整篇 `write`，除非你明确要整体重写。

### 2. 插图规则

插图时优先记住两件事：

- **位置靠 `parent_block_id + index` 控制**
- **结构改完后要再读一遍确认**

常用做法：

1. `list_blocks` 找到当前块顺序
2. 判断图片应插在谁前面/后面
3. `upload_image(file_path=..., parent_block_id=<doc_token 或父块>, index=<位置>)`
4. 如果插错了，不要硬忍，直接 `delete_block`
5. `read` 或 `list_blocks` 复查最终顺序

### 3. 长文排版规则

当用户说“别一大坨字堆一起”“花一点”“中间加图”时：

- 优先把图插在**两段长文字之间**
- 标题 / 小结附近可以补一张装饰图做呼吸点
- 不要为了花哨把图堆太密，正文仍要能顺着读
- 改完后复查一次全文，避免“图文意思已经变了，图还是旧的”

## 公开分享权限：开成“互联网获得链接的人可查看”

当用户明确要求：

- “允许互联网访问的人查看”
- “外网拿链接的人可读”
- “Anyone with link can read”

目标状态应设为：

- `external_access_entity = open`
- `security_entity = anyone_can_view`
- `link_share_entity = anyone_readable`
- `comment_entity = anyone_can_view`
- `share_entity = anyone`
- `manage_collaborator_entity = collaborator_can_view`
- `copy_entity = anyone_can_view`

### API 方式

用 Feishu Drive public permission 接口：

- `GET /open-apis/drive/v2/permissions/{token}/public?type=docx` 先看当前值
- `PATCH /open-apis/drive/v2/permissions/{token}/public?type=docx` 再更新

PATCH body 参考：

```json
{
  "external_access_entity": "open",
  "security_entity": "anyone_can_view",
  "comment_entity": "anyone_can_view",
  "share_entity": "anyone",
  "manage_collaborator_entity": "collaborator_can_view",
  "link_share_entity": "anyone_readable",
  "copy_entity": "anyone_can_view"
}
```

改完后一定再 `GET` 一次确认，不要只看 PATCH 成功。

## 飞书文档写入排障：先查这两层

这是最该记进 skill、而不是记忆的固定排障套路。

### 情况 A：写文档时报 400

第一优先检查：

- **应用 scope 是否缺 `docx:document.block:convert`**

如果缺这个权限，常见表现就是：

- 能读
- 但 `write` / `append` / `update_block` / `insert` 报 400

### 情况 B：能读但写时报 403

第二优先检查：

- **具体文档对象是否给“小龙虾（应用）”开了可编辑权限**

也就是两层要都通：

1. 应用 scope 允许写
2. 这篇文档本身也允许这个应用编辑

只通第一层、不通第二层，仍然会 403。

## 经验原则

- 用户给的是**原材料**，不是最终成稿时，先整理语言和结构，再写进文档
- 对文档做多轮精修时，避免每次都整篇覆盖；能局部改就局部改
- 涉及图文顺序时，优先把“语义对齐”放在“图片复用”前面；必要时重画图，而不是硬保留旧图
- 当用户说“这条不用记忆，放 skill 里就好”时，优先更新技能流程，不要塞进长期记忆
