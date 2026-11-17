---
name: douyin-download-webbridge
description: 免费下载抖音视频、图文图片和作品音轨，不用注册第三方下载站，也不需要 TikHub、redfox 等第三方 API Key。用户要求下载抖音作品、图文图片或音轨时使用；支持抖音作品长链、数字 ID，以及可在单次安全 HTTPS 响应中解析为受支持抖音长链的分享短链。通过 Easy WebBridge 复用用户明确选择或唯一在线的浏览器；遇到登录墙、验证墙或详情访问限制时停止，不切换环境、不绕过，并请用户自行处理。视频默认选择最高可用分辨率并优先 H.264；图文只保存详情接口确认属于当前作品的图片，无法确认时明确失败；音轨统一输出 48kHz 双声道 MP3。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# 免费抖音下载支持视频图片

## 先说亮点

- **免费**：开源使用，不按次数收费。
- **免额外登录**：不用注册第三方下载网站；公开作品可以直接处理，抖音出现登录墙时再登录抖音。
- **免 Key**：不需要申请 TikHub、redfox 或其他第三方内容接口的 API Key。
- **视频、图片都支持**：既能保存视频，也能按顺序保存多张图文图片。
- **图文配乐可提取**：`--audio-only` 直接读取作品音轨，不再要求图文先有 MP4。

通过 Easy WebBridge 复用用户已经明确选择或可无歧义确定的浏览器，把抖音作品保存到本地。发现登录墙、验证墙或详情接口访问限制时立即停止，不继续重试、切换账号或绕过；保留当前任务标签，并请用户自行登录/完成验证后重新运行。

## 1. 一键命令

```bash
python3 scripts/douyin_download.py "https://www.douyin.com/video/123456789012" # 默认下载目录
python3 scripts/douyin_download.py 7669474316672716066                    # 作品 ID 也认
python3 scripts/douyin_download.py "<链接>" -o /path/to/dir               # 指定输出目录
python3 scripts/douyin_download.py "<链接>" --browser 自媒体               # 指定浏览器
python3 scripts/douyin_download.py "<链接>" --quality worst               # 最小体积预览
python3 scripts/douyin_download.py "<链接>" --audio-only                 # 只提取作品音轨
```

**默认即最高清**，不用加任何参数：视频取最大分辨率且同分辨率优先 H.264，图文逐张取 `原图 > JPEG > WebP`。
`--quality worst` 只用于「快速看一眼」的预览场景。
`--audio-only` 对视频提取完整混音，对图文提取背景配乐，并统一转为 48kHz 双声道 MP3。

脚本自动完成：检查 EasyBR 内置 Bridge → 验证输入 → 打开目标浏览器页面 → 取可用媒体直链 → 下载 → 校验 → 关闭本次标签组。检测到登录/验证拦截或无法确认详情访问状态时保留标签并停止。

## 2. 前置门禁

执行前必须全部通过，任一失败即停止并报告原因：

1. **EasyBR 已启动**：macOS（Apple 芯片）或 Windows 上打开 EasyBR 即可，Easy WebBridge 已内置；脚本直接访问 `127.0.0.1:17777`，读取 `~/.easy-webbridge/bridge-token`，不需要单独安装 CLI 或 Node.js。
2. **选择目标浏览器**：指定 `--browser` 时只使用匹配的在线显示名或 `browserId`，找不到就停止，不访问其他浏览器。未指定时仅当一个浏览器在线才自动选择；两个或更多浏览器在线时，无论显示名称是什么，都列出名称和 `browserId` 并要求明确指定目标。
3. 其他操作系统按 README 的源码方式运行 Easy WebBridge。

服务未启动时不要手工拉起其他工具顶替，先按 `easy-webbridge` skill 的方式启动服务。

## 3. 输入解析

直接下载接受抖音作品长链、纯数字 modal_id，以及严格单独提供的 `https://v.douyin.com/...` 分享短链。短链只发送一次固定到已核验公网 IP 的 HTTPS 请求，读取响应中的 `Location` 并仅提取受支持抖音长链的作品 ID；绝不请求 Location 目标或跟随重定向。

- 短链仅接受一个 HTTPS `v.douyin.com` 链接；DNS 不可核验、请求失败、无单个有效 Location、Location 指向外站/短链/非作品页或无法提取 ID 时立即失败，请用户提供对应的抖音长链或数字 ID。
- 不请求 Location 目标，也不跟随用户提供 URL 的重定向，避免访问外站或内网地址；媒体下载请求也不跟随 HTTP 重定向。
- **`/note/` 是图文作品**，不是视频，走第 5 节分支。
- 提取不到作品 ID 立即失败，不猜、不兜底。

## 4. 视频下载

### 4.1 取直链（关键）

**禁止直接读 `video.src`** —— 页面默认只给 540p 档（576×1024）。必须在页面内 fetch detail 接口拿全量码率档位：

```javascript
(async () => {
  const url = `https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=${awemeId}`;
  const j = await (await fetch(url, { credentials: "include" })).json();
  const v = j.aweme_detail.video;
  return (v.bit_rate || []).map(b => ({
    gear: b.gear_name,
    w: b.play_addr.width,
    h: b.play_addr.height,
    url: b.play_addr.url_list[0],
  }));
})()
```

按 `w × h` 排序选最大档。抖音常见档位：`normal_1080_0`(1080×1920) / `normal_720_0` / `normal_540_0`。

### 4.2 下载

必须带移动端 UA 与 `Referer: https://www.douyin.com/`，否则可能 403。

媒体文件地址只允许公网 HTTPS：下载前解析并核验所有 DNS 地址，拒绝本机、内网、非公网地址及非 HTTPS 协议。若系统 DNS 返回 `198.18.0.0/15` fake-IP 或解析失败，会向固定的 AliDNS HTTPS 解析器只发送媒体主机名，核验所有 A/AAAA 结果均为公网地址后才继续；不会发送媒体 URL、路径或签名参数。curl 通过 `--connect-to` 固定到已核验 IP；即使使用环境代理，HTTPS CONNECT 目标也是该 IP，且 TLS 仍按原主机名校验证书。请求不会自动跟随重定向。若无法取得可核验的公网地址，脚本会停止。

### 4.3 校验

下载后若系统可找到 `ffprobe`，用它输出真实分辨率、编码、时长、体积。`ffmpeg`/`ffprobe` 从 PATH 查找；Apple Silicon macOS 另兼容 `/opt/homebrew/bin`。Windows 请将 ffmpeg 与 ffprobe 可执行文件所在目录加入 PATH。缺少 ffprobe 时下载仍可完成，但会跳过媒体信息检查；缺少 ffmpeg 时 `--audio-only` 无法转码并会明确失败。

## 5. 图文（note）下载

### 5.1 类型判定（不能只看链接）

**短链路径和首屏 DOM 都不可靠**：图文作品的分享链接可能走 `/share/video/{id}`，视频页面的 `<video>` 也可能延迟挂载。优先读取 detail 接口的 `aweme_type`、正文图片字段和可播放视频字段；详情响应无法确认时停止，不根据整页 DOM 推断内容类型。视频取流失败后可以尝试图文，但图文下载必须取得当前作品的 detail 图片清单；没有清单就失败，不从整页 DOM 推断图片归属。

```javascript
const d = detail.aweme_detail;
const hasImages = (d.images || []).length > 0;
const hasVideo = (d.video?.bit_rate || []).length > 0;
const kind = hasImages || d.aweme_type === 68 ? "note" : hasVideo ? "video" : null;
```

正文图片字段存在或 `aweme_type === 68` → 图文；存在可播放视频字段 → 视频。detail 响应本身不可用或媒体类型仍无法判断时停止；已确认视频但取流失败时可尝试图文分支，图文图片仍必须来自该作品的 detail 图片清单。

### 5.2 取图：detail 定清单 + DOM 补签名

**禁止从 DOM 直接生成待下载图片清单** —— 会混进推荐位、评论区的缩略图（实测抓到 11 张，正文其实只有 1 张）。detail 接口给出的当前作品图片清单是唯一下载来源：

1. detail 接口取 `aweme_detail.images[]`，拿到正文图片清单、宽高，以及每张图的全部 `url_list` 档位。
2. DOM 图片只可补充有效签名的 `~noop` 原图 URL；必须按图片 ID 与 detail 清单中的 URL 精确匹配，推荐图和评论图不会成为下载来源。
3. detail 清单缺失、为空或无法识别图片 URL 时明确失败，不回退到整页 `<img>` 抓取。

**绝不能自己把 `~tplv-xxx` 改写成 `~noop.jpeg`**：抖音的 `x-signature` 是针对完整 URL（含 `~tplv-` 段）计算的，改了必然 403。只有页面正在用的那个 URL 签名才有效。

### 5.3 单张图的档位选择：原图 > JPEG > WebP

`images[].url_list` 通常给 3 个 URL：`q75.webp`(p3) / `q75.webp`(p9) / `q75.jpeg`(p3)。
**只取 `url_list[0]` 会固定拿到体积最小、损失最大的 webp。**

实测同一张 1080×1440 图：

| 档位 | 体积 | 结论 |
|---|---|---|
| `~noop.jpeg` 原图 | 169 KB | 最优，但只有当前轮播显示的那张才有 |
| `q75.jpeg` | 113 KB | **常规最优解**，文字清晰、通用性最好 |
| `q75.webp` | 54 KB | 压缩损失明显，作兜底 |

选择逻辑见 `pick_image`：DOM 里有同 ID 的 `~noop` 就用它，否则退 `q75.jpeg`，再退 `q75.webp`。

**不要用 `images[].download_url_list`** —— 那是抖音「保存图片」用的**带水印**版本（`~tplv-dy-water-v2:...`）。

**原图拿不全的原因**：图文是懒加载轮播，只有当前显示的那张会渲染 `~noop` URL。实测轮播**翻不动**——JS `.click()`、键盘 `ArrowRight`、CDP `Input.dispatchMouseEvent` 全部无效（点击后累计 noop 数始终不变），所以多图作品通常只能拿到 `q75.jpeg` 档。脚本会打印每张图的档位分布，能直观看出是否拿到了原图。

### 5.4 落地

多张图按 `_01` `_02` 顺序编号，扩展名按 URL 后缀取 `.webp` / `.jpeg` / `.png`。

## 6. 输出合同

- 输出目录默认 `~/Downloads/DouyinDownloads`，不存在时自动创建。
- 文件名取作品 desc，清理规则：去 `#话题`、去 emoji 与非法字符、限长 40 字；清理后为空则用 modal_id。
- 视频扩展名 `.mp4`；图文按 URL 后缀取 `.jpeg` / `.png` / `.webp`。
- `--audio-only` 输出 `douyin-<作品ID>-<时间戳>-original.mp3`，并在末尾打印可供调用方读取的 `RESULT_JSON=`。
- 结束时打印实际保存的文件绝对路径。

## 7. 踩坑清单

| 坑 | 现象 | 处理 |
|---|---|---|
| ffmpeg/ffprobe 找不到 | 工具路径为空 | 安装 FFmpeg 并将其 bin 目录加入 PATH；Apple Silicon macOS 也会检查 `/opt/homebrew/bin` |
| 直接读 `video.src` | 只拿到 540p | 必须走 detail 接口取 `bit_rate[]` |
| 只按 `w×h` 选档 | 同分辨率选到 HEVC，剪辑软件兼容性差 | 同分辨率优先 `cs=0`（H.264），见 `_codec_rank` |
| 只看分享短链路径或首屏 `<video>` 判类型 | 短链仅检查一次直接 `Location`，视频元素可能延迟挂载 | 短链若需多跳或无法提取 ID，请换成长链或 ID；优先按 detail 媒体字段判型，详情状态不明就停止 |
| DOM 直抓 `<img>` | 混入推荐位小图（实测 11 张里只有 1 张是正文） | detail 的 `images[]` 是唯一清单；DOM 原图须按图片 ID 匹配，detail 不可用时失败 |
| 自己改写 `~noop.jpeg` | 签名失效，下载 403 | 只能用页面原有的 URL，按图片 ID 匹配 |
| 只取 `images[].url_list[0]` | 固定拿到 54KB 的 `q75.webp` | 遍历全部 url_list，优先 `.jpeg`（113KB，质量翻倍） |
| 用 `download_url_list` | 下下来的图**带抖音水印** | 那是「保存图片」专用，改用 `url_list` |
| 想翻轮播补齐原图 | JS 点击 / 键盘 / CDP 真实点击**全部无效** | 放弃，接受 `q75.jpeg` 档 |
| bridge network 抓包取响应体 | `responseBody` 恒为空 | 改用页面内 `fetch` |
| 下载报 403 | 直链过期或缺 Referer | 带移动端 UA + Referer |
| 直链有时效 | 隔一段时间后 403 | 重新跑一次脚本拿新链 |

## 8. 边界

- 只下载，不做剪辑、加水印或去水印；仅 `--audio-only` 为兼容播放器执行 48kHz 双声道 MP3 标准化。
- 不上传平台、不操作账号、不采集发布后数据。
- 遇到登录墙、验证码、滑块或其他验证页时立即停止，不继续请求、不切换浏览器，也不绕过；保留当前标签供用户手动处理。

## 9. 与工作台候选池协作

当素材来自“内容来源采集器”或工作台“热点候选池”时，遵循下面的边界：

1. 候选池只保存人工待筛选的抖音视频/图文，不是正式内容，也不会自动创建 `projects/` 目录。
2. 工作台的“加入下载队列”接口（`POST /api/source-candidates/batch-download`）目前只登记 `pending` 下载任务；它不会在接口请求中直接下载文件。下载 Skill 或后续 Worker 必须逐项读取候选的 `canonical_url`，调用本 Skill 的一键命令，并在完成后回写真实输出路径和结果。
3. 下载前必须由用户确认候选项。批量任务按候选逐项执行，不能把失败项标成成功；失败原因和路径要分别保留。
4. 视频候选使用 `content_type=video`，图文候选使用 `content_type=post`。图文按第 5 节落地多张图片，不能把图文当成空视频文件。
5. 建议输出到对应内容单元的 `assets/raw/` 或用户指定的素材目录；不得把素材、缓存或下载任务元数据写入正式 `发布成品/`。
6. 候选池支持抖音以外的平台字段，但本 Skill 只处理抖音。小红书、B 站等平台必须由各自下载 Skill 负责，不能套用抖音直链规则。

候选池状态与下载状态分离：`collected/shortlisted/promoted/rejected` 表示人工筛选进度；`none/queued/processing/completed/failed` 表示下载进度。只有实际文件通过 `ffprobe` 或图片完整性检查后，才能回写 `completed`。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)；Easy WebBridge 连接和系统要求见[官方指南](https://www.ebrower.com/helperdoc/easy-webbridge.html)。Apple 芯片 Mac 与 Windows 的 EasyBR 1.7.8 及以后内置 Bridge 与浏览器扩展，无需另行安装 Bridge。普通浏览器或其他系统才需要按官方指南安装完整 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
