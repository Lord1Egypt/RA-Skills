---
name: doubao-opencli
description: >-
  豆包（Doubao）AI 助手 OpenCLI 技能包。通过 opencli browser 桥接复用 Edge 浏览器登录态，
  提供豆包对话、AI 播客生成（文字/网页链接/PDF 三种输入方式，自动裁剪广告）、
  PPT 生成、图像生成（文生图）、会议摘要、批量提问、对话备份等功能。
  使用场景：(1) 需要通过 CLI 或脚本自动化操作豆包时；(2) 需要批量生成播客/图片/PPT时；
  (3) 需要备份豆包对话记录时。前置条件：Edge 已登录 https://www.doubao.com/chat，opencli 已安装。
---

# 豆包 OpenCLI 技能包

通过 `opencli` 浏览器桥接复用 Edge 中已登录的豆包会话，提供 CLI 自动化操作。

## 功能一览

| 功能 | 脚本 | 说明 |
|------|------|------|
| ✅ 提问 | `doubao_toolkit.ps1 ask` | 向豆包提问 |
| ✅ 对话 | `doubao_toolkit.ps1 chat` | 交互式对话 |
| ✅ 图像生成 | `doubao_image_gen.ps1` | 文生图 + 自动下载 |
| ✅ AI 播客 | `doubao_podcast_gen.ps1` | 播客生成 + 自动下载 |
| 🆕 PPT 生成 | `doubao_ppt_gen.ps1` | PPT 生成 + 自动下载 |
| ⚠️ 会议 | `doubao_toolkit.ps1 meetings` | 依赖 history，新版UI可能不可用 |
| ⚠️ 备份 | `doubao_toolkit.ps1 backup` | 依赖 history，新版UI可能不可用 |
| ✅ 批量 | `doubao_toolkit.ps1 batch` | 批量提问 |

## 前置条件

- **Edge** 已登录 [https://www.doubao.com/chat](https://www.doubao.com/chat)
- **opencli** 已安装（`npm install -g @jackwener/opencli`）
- **opencli 浏览器桥接扩展** 已在 Edge 中安装

> ⚠️ 用户默认浏览器是 **Microsoft Edge**（非 Chrome），记录在 `TOOLS.md`。

## 脚本说明

### 1. `doubao_toolkit.ps1` — 工具箱

多功能 CLI 工具箱，包装 `opencli doubao` 命令：

```powershell
# 检查连接状态
.\scripts\doubao_toolkit.ps1 status

# 向豆包提问
.\scripts\doubao_toolkit.ps1 ask "你的问题"

# 交互式对话
.\scripts\doubao_toolkit.ps1 chat

# 图像生成（自动下载到 output/doubao_images/）
.\scripts\doubao_toolkit.ps1 image "一只橘猫，水彩风格"

# 会议相关
.\scripts\doubao_toolkit.ps1 meetings            # 查看会议列表
.\scripts\doubao_toolkit.ps1 summary <id>        # 获取会议摘要

# 备份 / 批量
.\scripts\doubao_toolkit.ps1 backup              # 备份所有对话
.\scripts\doubao_toolkit.ps1 batch <file.txt>    # 批量提问
```

**注意**：`history` 命令在豆包新版 UI 下可能不可用，会影响 `meetings`、`summary`、`backup` 等依赖 `history` 的功能。

### 2. `doubao_image_gen.ps1` — 图像生成

独立的图像生成脚本，通过 opencli browser 自动化豆包 AI 创作页面的文生图流程：

```powershell
.\scripts\doubao_image_gen.ps1 "提示词"              # 仅生成，显示链接
.\scripts\doubao_image_gen.ps1 "提示词" -download     # 生成并下载到本地
```

**工作流程**：
1. 打开 `https://www.doubao.com/chat/create-image`
2. 自动定位输入框（动态 ref 号）
3. 填入提示词，点击 `#flow-end-msg-send` 发送按钮
4. 等待 ~15-20s 生成完成
5. 从页面提取 4 张图片的 URL
6. 用 `Invoke-WebRequest` 下载到 `output/doubao_images/`

**输出文件**：
- `output/doubao_images/doubao_YYYYMMDD_HHmmss_N.jpg` — 下载的图片
- `output/doubao_images/gen_log_YYYYMMDD_HHmmss.md` — 生成记录（含图片链接）

### 3. `doubao_podcast_gen.ps1` — AI 播客生成

独立的 AI 播客生成脚本，通过 opencli browser 自动化豆包 AI 播客的生成和下载，**自动裁剪开头广告**：

```powershell
# 📝 文字模式（主题/文章/大纲/脚本）
.\scripts\doubao_podcast_gen.ps1 -Text "介绍人工智能的发展历史"
.\scripts\doubao_podcast_gen.ps1 -Text "IaaS PaaS SaaS 三种云计算服务模式的区别和应用场景"

# 🔗 网页模式（输入链接，豆包自动抓取）
.\scripts\doubao_podcast_gen.ps1 -Url "https://example.com/article"

# 📄 文件模式（上传 PDF，仅支持 .pdf）
.\scripts\doubao_podcast_gen.ps1 -File "C:\docs\我的文章.pdf"

# 自定义参数
.\scripts\doubao_podcast_gen.ps1 -Text "你的主题" -WaitPlay 30 -TrimSeconds 0
```

**输入方式**（三选一）：
- `-Text`：文字输入，支持主题、完整文章、大纲、脚本
- `-Url`：网页链接输入，豆包自动抓取网页内容生成播客
- `-File`：PDF 文件上传（仅 .pdf），豆包根据文档内容生成播客

**工作流程**：
1. 打开 `https://www.doubao.com/chat`
2. 自动定位并点击 **AI 播客** 按钮（动态 ref）
3. 输入内容（文字/网页链接/PDF文件，三选一）
4. 点击发送按钮 `#flow-end-msg-send`
5. 等待播客生成完成（~10-60秒，文件模式可能更久）
6. 自动点击播放按钮
7. 持续播放等待下载按钮可用（默认等待 40 秒）
8. 点击下载按钮 [593]/[591]（向下箭头 SVG）
9. 文件自动保存到 Edge 默认下载目录
10. 搬运到 `output/doubao_podcasts/`
11. **自动裁剪开头 4 秒广告**（使用 ffmpeg）

**重要发现**：
- 下载按钮的 class 包含 `downloadBtn-Iyn2FU`，通过 `span[role=img]` 的父 `div[tabindex]` 定位
- ⚠️ **关键**：opencli browser click 命令无法触发下载按钮，必须使用 JS 原生事件（dispatchEvent 触发 mousedown + mouseup + click + pointerdown）
- 点击下载后 **自动保存** 到系统 Downloads 目录，不弹出保存对话框
- 下载文件格式为 **.wav**，文件名以播客标题命名
- 下载按钮需要播放 20-40 秒后才变为可用（不可用时点击无反应）
- 输出文件使用时间戳命名（`AI新闻播客_20260511_173500.wav`），避免覆盖旧文件
- 下载检测改用文件快照对比（名称+大小+修改时间），不再依赖文件名比对
- 示例输出：`output/doubao_podcasts/云计算服务模式的差异与场景.wav`（28MB，9分51秒）

**自动裁剪广告**：
- 脚本默认使用 ffmpeg 裁剪音频开头 **4 秒**（豆包播客开头通常有品牌广告）
- 通过 `-TrimSeconds` 参数自定义裁剪秒数，设为 `0` 则跳过裁剪
- 裁剪后原文件被替换，最终输出的就是去广告版本
- 需要系统已安装 ffmpeg（否则跳过裁剪，保留原文件）

**输出文件**：
- `output/doubao_podcasts/<播客标题>.wav` — 下载的播客音频文件（已自动裁剪开头广告）

### 4. `doubao_ppt_gen.ps1` — PPT 生成（实测验证 ✅）

AI PPT 生成脚本，通过 opencli browser 自动化豆包 PPT 生成与下载流程。

```powershell
# 按主题生成（推荐）
.\scripts\doubao_ppt_gen.ps1 -Topic "人工智能发展史"

# 按大纲生成
.\scripts\doubao_ppt_gen.ps1 -Outline "1. 引言`n2. 技术原理`n3. 应用场景`n4. 未来展望"

# 按草稿文档生成
.\scripts\doubao_ppt_gen.ps1 -DraftFile "C:\docs\my_draft.md"

# 通过工具箱
.\scripts\doubao_toolkit.ps1 ppt "人工智能发展史"
```

**实测数据**（2026-05-11）：
- 生成 20 页 PPT 耗时：**15 分 47 秒**
- 生成 23 页 PPT 耗时：**13 分 01 秒**
- 下载文件大小：**~3.4 MB**（PPTX 格式）
- 下载方式：工具栏下载按钮 → 选择 PPTX → **自动保存到 Downloads**



**PPT 工作流程**（实测验证）：
1. 打开 `https://www.doubao.com/chat`
2. **不要点击 PPT 快捷按钮** — 直接在普通聊天模式的 textarea 中输入提示词
3. 点击发送按钮 `#flow-end-msg-send`（**只在普通聊天模式存在**，PPT 快捷模式无发送按钮）
4. **5 阶段进度监控**（每 15 秒检查一次）：
   - 阶段 1：思考状态 + 素材收集（最长阶段，AI 联网搜索参考资料）
   - 阶段 2：思考优化 + 补充收集（1-2 分钟）
   - 阶段 3：生成原创图片（1-5 分钟，AI 生成封面/背景/配图）
   - 阶段 4：PPT 合成与渲染（5-6 分钟，左右分栏模式）
   - 阶段 5：已完成（检测到 "已完成PPT生成" 标志）
5. 生成完成后，**点击 PPT 卡片**（封面图或标题区域）→ 打开左右分栏编辑器
6. **点击工具栏"下载"按钮** → 弹出菜单（PPTX / PDF）
7. **选择 PPTX** → 文件自动保存到系统 Downloads 目录
8. 搬运到 `output/doubao_ppt/` 目录

**关键发现**（实测）：
- ⚠️ **PPT 快捷按钮模式没有发送按钮** — 必须在普通聊天模式发送
- 发送按钮 ID：`#flow-end-msg-send`（普通聊天模式）
- PPT 编辑器是一个 iframe（`/partner/ccm-slides-v3/`），但**下载按钮在主页面的 DOM 中**，不在 iframe 内
- 下载按钮特征：`data-dbx-name="button"`，文本"下载"，`aria-haspopup="menu"`
- 格式选择菜单项特征：`role="menuitem"`，文本"PPTX"
- **不需要确认保存对话框** — 文件自动保存到 `Downloads` 目录
- 每次页面加载后元素 ref 号会变化，脚本使用动态查找而非硬编码

**参数说明**：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-Topic` | PPT 主题 | — |
| `-Outline` | PPT 大纲文本 | — |
| `-DraftFile` | 草稿文档路径（.txt/.md） | — |
| `-WaitTimeout` | 总等待超时（秒） | 1200（20 分钟） |
| `-MonitorInterval` | 监控间隔（秒） | 15 |
| `-OutputDir` | 输出目录 | `output/doubao_ppt/` |

**播客脚本 `doubao_podcast_gen.ps1` 参数说明**：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-Text` | 播客文字内容（主题/文章/大纲/脚本），与 `-Url`、`-File` 三选一 | — |
| `-Url` | 网页链接，豆包自动抓取生成播客，与 `-Text`、`-File` 三选一 | — |
| `-File` | PDF 文件路径（仅 .pdf），与 `-Text`、`-Url` 三选一 | — |
| `-OutputDir` | 输出目录 | `output/doubao_podcasts/` |
| `-WaitPlay` | 播放等待秒数（下载按钮需播放后才可用） | 40 |
| `-TrimSeconds` | 裁剪音频开头N秒（去广告，设为0则不裁剪） | 4 |

**阶段日志示例**：
```
[11:15:30] [PHASE] [1/5] 打开豆包聊天页...
[11:15:35] [PHASE] [2/5] 触发 PPT 生成...
[11:15:40] [PHASE] [3/5] 监控生成进度...
[11:15:55]  ┌─ 进入阶段1: 思考状态 + 素材收集 [11:15:55]
[11:17:30]  └─ 阶段1完成，耗时 95s
[11:17:30]  ┌─ 进入阶段2: 思考优化 + 补充收集 [11:17:30]
[11:18:45]  └─ 阶段2完成，耗时 75s
[11:18:45]  ┌─ 进入阶段3: 生成原创图片 [11:18:45]
[11:22:10]  └─ 阶段3完成，耗时 205s
[11:22:10]  ┌─ 进入阶段4: PPT合成与渲染 [11:22:10]
[11:28:30]  ✅ PPT 生成完成！总耗时 765s
[11:28:33] [4/5] 下载 PPT...
[11:28:36]  -> 点击 PPT 标题打开编辑器...
[11:28:41]  -> 找下载按钮...
[11:28:41]  -> 点击下载按钮...
[11:28:43]  -> 选择 PPTX 格式...
[11:28:46]  ✅ 下载成功: C:\Users\xxx\Downloads\xxx.pptx
[11:28:46] [5/5] 搬运到输出目录...
[11:28:46]  ✅ 已搬运到: output/doubao_ppt/ppt_20260511_112846.pptx
```

**输出文件**：
- `output/doubao_ppt/ppt_YYYYMMDD_HHmmss.pptx` — 下载的 PPT 文件
- `output/doubao_ppt/logs/ppt_log_YYYYMMDD_HHmmss.md` — 详细阶段日志

## 已知问题

- **`history` 命令不可用**：豆包新版 UI 下 `opencli doubao history` 返回空，导致 `meetings`、`summary`、`backup` 等功能受限。
- **图像生成页面的发送按钮 ID**：`#flow-end-msg-send`，在页面重新加载后输入框 ref 号会变化，脚本使用正则动态匹配。
- **`ask` 命令的 JSON 输出**：`opencli doubao ask -f json` 的输出可能包含更新提示等非 JSON 文本，已使用 `2>$null` 过滤。

## ⚠️ 经验教训（后续修改务必注意）

> 完整经验文档见 [`knowledge/doubao-podcast-bug-fix.md`](../../knowledge/doubao-podcast-bug-fix.md)

### 1. 不要信任 ref 号
opencli browser 的 ref 号是**动态分配**的，每次页面加载都不同。永远用 class/文本/位置定位元素，而非硬编码 ref。

### 2. 不要信任 click 返回值
`clicked: true` 不代表操作生效了。对于复杂 UI（如下载按钮），用 JS 原生事件更可靠：
```javascript
el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
el.dispatchEvent(new MouseEvent('click', {bubbles: true}));
el.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true}));
```

### 3. 输出文件永远用时间戳命名
避免同名文件覆盖导致内容混淆。格式：`AI新闻播客_20260511_173500.wav`

### 4. 下载检测用快照对比
仅靠文件名不够，要同时检查大小和修改时间。记录下载前的快照，对比真正的变化。

### 5. JS eval 比 ref 号更可靠
`opencli browser eval` 直接操作真实 DOM，不受 ref 号变化影响。

### 6. 窗口必须最大化
豆包页面在窗口不够大时部分按钮（如 AI 播客）可能不显示。用 JS 最大化：
```javascript
window.moveTo(0,0); window.resizeTo(window.screen.availWidth, window.screen.availHeight);
```

## 未来扩展方向

- 支持比例/风格/模型参数的自定义
- 参考图上传功能
- AI 抠图/擦除/重绘等图片编辑模式
- 视频生成（豆包已支持）
- 批量图片生成