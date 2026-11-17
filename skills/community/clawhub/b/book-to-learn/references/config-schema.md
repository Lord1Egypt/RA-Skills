# 配置说明（config.json）— v1.6

> **兼容性承诺**：v1.4.1 的 config.json 无需改动即可继续使用。
> 本版所有新增键**均为可选**，缺失时走下列默认值；旧键（`template`、`cardPrefix`）保留并继续生效。
> **模式 C「资料拆卡」不使用 config.json**（见 §9）。

## 0. 首次启动的硬门禁（最高优先级）

> **使用本 skill 的第一步，永远是「与用户确认配置」，不是「开始拆解」。**

`config.confirmed.items` 中任一项为 `false` 时，**必须停下**，逐项与用户确认并把结果写回 config：

| 需确认项 | 确认什么 |
|---|---|
| `source` | 来源是「本地书文件」还是「网站」；站点模式还要确认**章节范围**与**卡片总数** |
| `language` | 原文语言；是否翻译（英文=需翻译，中文=无翻译） |
| `cardType` | 卡片类型（决定渲染引擎，见 §5） |
| `pushMethod` | 推送到哪里（IMA / 飞书 webhook / 飞书 API / 仅本地输出） |
| `naming` | 文件名模板、前缀、卡片内序号标记方式 |
| `notes` | 操作指南与进度笔记存放位置（本地目录；是否镜像到 IMA） |
| `notify` | 失败通知 webhook（**建议必填**：失败必须能通知到人） |

全部确认后写入 `confirmed.at` / `confirmed.by`（`by` 填确认人），再进入拆解。

## 1. 顶层

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `configVersion` | int | 2 | schema 版本 |
| `bookTitle` | str | slug | 展示用标题 |
| `bookSlug` | str | — | 数据目录名 `books/<slug>/` |
| `language` | `zh`\|`en` | `en` | `en` 走翻译流程；`zh` 跳过翻译 |
| `granularity` | `chapter`\|`section`\|`topic` | `chapter` | 拆解粒度（书模式） |
| `itemsLayout` | `single`\|`split` | `single` | 内容多时用 `split`（见 §4） |

## 2. source（来源）

| 键 | 说明 |
|---|---|
| `source.type` | `book`（本地文件）\| `site`（网站） |
| `source.file` | book 模式：源文件路径（PDF/DOCX/HTML/EPUB/TXT） |
| `source.bookSource` | 书来源链接（可选，写入卡片「来源」） |
| `source.site.url` | 站点根 URL |
| `source.site.sitemap` | `auto`（自动找 `/sitemap.xml`）或显式 URL |
| `source.site.include` / `exclude` | 路径前缀白/黑名单（**导航页务必排除**，如 `/`、`/hubs`） |
| `source.site.bodySuffix` | 正文抓取后缀，默认 `.md`（比抓 HTML 干净得多） |
| `source.site.sections` | 章节范围：`[{"name":"Agents","zh":"智能体","count":54}]`，确认后写入，用于清单核定与编号 |

## 3. pushMethod 与渠道

| 值 | 需要填写 | 说明 |
|---|---|---|
| `local` | `local.outDir` | **零依赖默认**：产物写到本地目录，任何环境都能跑 |
| `ima` | `ima.kbName` / `ima.folderName` + 环境变量 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` | 上传 PDF/PNG 到 IMA 知识库 |
| `feishu` | `feishu.webhook` | 飞书群机器人 webhook（交互卡片；图片需外链） |
| `feishu-api` | `feishuApi.appId/appSecret/chatId` | 飞书自建应用，支持原生图片/文件 |

> 凭据一律走**环境变量**，不写进 config。缺凭据时报错并提示替代方案（可退回 `local`）。

## 4. itemsLayout：大内容分文件

| 值 | 布局 | 适用 |
|---|---|---|
| `single` | `items.json` 单文件 | 卡片数少（默认，兼容旧版） |
| `split` | `items/index.json` + `items/ch01.json`、`ch02.json`… | 内容多、需要分章节编辑 |

- `split` 模式下 `items/index.json` 列出 `{"chapters":[{"file":"ch01.json","title":"…"}]}`，加载器按序合并；
- 读取侧统一调用 `load_items(slug)`，两种布局对上层**无差别**；
- 注意：这是**内容源**索引，与推送用的 `index.json`（卡片顺序）不是同一个文件。

## 5. cardType 与渲染引擎映射（按类型调用）

| cardType | 默认引擎 | 产物 |
|---|---|---|
| `pdf-standard` | `gen_card_pdf.py` | A4 标准卡片 PDF |
| `pdf-large` | `gen_card_pdf_large.py` | 大字闪卡 PDF |
| `long-image` | `gen_image.py` | 中文长图 PNG（移动端） |
| `tile-3x4` / `tile-9x16` / `tile-1x1` / `tile-4x3` / `tile-16x9` | `gen_card_tile.py` | **竖版知识卡片长图**（模式 C；参数用 `--cards/--outdir`，不是 `--payload/--out`） |
| `feishu-card` | `send_feishu.py` | 飞书交互卡片 |
| `feishu-card+image` | `gen_image.py` + `send_feishu_api.py` | 卡片 + 配图 |

- 调度入口：`python3 render.py --type <cardType> --payload <p> --zh <z> --out <o>`
- `config.renderer` 可覆盖上表（自定义引擎时加一条即可，不用改代码）；
- 引擎各自独立，**共享的只有纯工具函数**（`render_common.py`，不含版式决策）。

## 6. naming：双轨编号

| 键 | 说明 |
|---|---|
| `naming.filePrefix` | 文件名前缀（如 `OC`） |
| `naming.sectionZh` | 章节中文名（如「开始」） |
| `naming.fileTemplate` | 文件名模板：`{prefix}{seq:03d} {sectionZh}——{chainZh}` |
| `naming.markerTemplate` | 卡片内序号标记：`{idx}/{total}`（`idx`=清单绝对序号，跳过会跳号） |
| `naming.manifestIndex` | `true` 时按**清单绝对序号**给文件名编号；`false` 按推送顺序 |

> **两条轨道不要混**：文件名用「推送序号」（连续），卡片内标记与笔记录入用「清单绝对序号」（跳号留空）。

## 7. notes：操作指南与进度笔记

| 键 | 说明 |
|---|---|
| `notes.channel` | `local`（默认）\| `ima` \| `both` |
| `notes.dir` | 本地存放目录；留空 = `books/<slug>/docs/` |
| `notes.ima.*` | IMA 镜像目标（笔记本名 / 进度笔记 ID / 操作指南笔记 ID） |

- **本地文件为底**：`docs/guide.md`（操作指南）+ `docs/progress.md`（进度笔记）——不依赖任何平台；
- 检测到 IMA 环境且 `channel` 含 `ima` 时，追加镜像到 IMA 笔记；
- 用途：记忆被压缩 / 换设备 / 换 agent 后，读这两个文件即可恢复全部上下文。

## 8. batch 与其它

| 键 | 默认 | 说明 |
|---|---|---|
| `batch.listNextN` | 10 | 每次推送后列出接下来 N 张（供用户决定跳过） |
| `batch.translateParallel` | true | 大批量时并行翻译、集中推送（避免并发写状态） |
| `notifyWebhook` | — | 失败通知（**建议必填**） |
| `testPush` | false | 配置完成后是否试推一张 |

## 9. 模式 C（资料拆卡）不使用 config.json

拆卡模式的数据与配置都在**工作目录的任务文件夹**里，与 `books/<slug>/` 互不干扰：

| 文件 | 作用 |
|---|---|
| `GUIDE.md` | 操作手册（内嵌全部规则与踩坑，读它就能接手） |
| `PROGRESS.md` | 进度（只增不删，底部最新） |
| `cards.json` | 唯一事实源：顶层 `group` / `footer` / `ratio`；`cards[]` 每张含 id/index/filename/title/subtitle/accent/blocks |
| `src/` `refs/` `out/` | 原文提取 / 参考图 / 产物（含 `_check.json`、`_contact_sheet.png`） |

初始化与维护用 `tile_setup.py`（init / export-md / sheet / check / log / status）。
画布比例在 `cards.json` 的 `ratio`（或 `--ratio` 覆盖），默认 `3:4`；可选 `9:16` / `1:1` / `4:3` / `16:9`。
