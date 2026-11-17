# 故障排查表

> SKILL.md 的扩展参考。遇到问题时查阅。

## 首次使用配置（环境检查）

按顺序检查，缺什么补什么：

1. **Python 3.9+**：`python --version`
2. **ffmpeg**：`ffmpeg -version`（缺失：`winget install Gyan.FFmpeg`）
3. **yt-dlp**（B站/YouTube 必需）：`yt-dlp --version`（缺失：`pip install -U yt-dlp`）
4. **agent-browser**（抖音必需）：`agent-browser --version`（缺失：`npm install -g agent-browser`）
5. **youtube-transcript-api**（YouTube 字幕优先）：`pip install youtube-transcript-api`
6. **Python 依赖**：`pip install faster-whisper opencc-python-reimplemented`
7. **HF 镜像**（首次下载模型加速）：`set HF_ENDPOINT=https://hf-mirror.com`
8. **YouTube 代理**（可选，仅 YouTube 需要）：
   - PowerShell：`$env:HTTPS_PROXY="http://127.0.0.1:7890"`（举例 Clash 默认端口）
   - 永久设置：`setx HTTPS_PROXY "http://127.0.0.1:7890"`

## 阶段 1：批量获取

### 抖音相关

| 问题 | 原因 | 解决 |
|------|------|------|
| CDN URL 提取失败 | 等待时间不够 / 视频已下架 | 手动延长等待到 60s；或跳过该视频继续处理 |
| MD5 重复 | network 累积旧 URL | 确保 __vid 匹配；重试提取 |
| agent-browser close 挂起 | subprocess 调用 close 会卡死 | 本 skill 已避免 close，直接 open 新 URL |
| agent-browser 未安装 | 未全局安装 | `npm install -g agent-browser` |
| 下载 403 | CDN URL 过期 | 重新提取 URL（重试 3 次后放弃） |

### B站相关

| 问题 | 原因 | 解决 |
|------|------|------|
| yt-dlp 下载失败 | 网络问题 / B站改版 | `pip install -U yt-dlp` 升级到最新版 |
| yt-dlp 未安装 | 未安装 | `pip install -U yt-dlp` |
| B站视频需要登录 | 1080P+ 需要大会员 | 本 skill 仅下载音频（bestaudio），不需要登录 |
| 分 P 下载错误 | p 参数解析错误 | 检查 URL 是否含 `?p=N`；脚本会自动提取 |
| 标题含特殊字符 | yt-dlp 输出标题含 `p01 001xxx` | 脚本已保留原始标题，输出时 safe_filename 会清理 |
| 下载速度慢 | B站限速 / 网络问题 | 耐心等待；或检查是否有代理影响 |

### 小宇宙相关

| 问题 | 原因 | 解决 |
|------|------|------|
| 抓取 HTML 失败 | 网络问题 / URL 无效 | 检查 URL 是否为 `https://www.xiaoyuzhoufm.com/episode/{id}` 格式 |
| HTML 中未找到 `<audio src>` 标签 | 页面结构变更 / 抓到的是重定向页 | 升级脚本的正则；或用浏览器手动检查页面结构 |
| 下载音频失败 | audio URL 过期 / CDN 限速 | 重新抓取 HTML 拿新的 audio URL；或增加超时时间 |
| 元数据缺失 | JSON-LD / og 标签结构变更 | 脚本已 3 层兜底（JSON-LD → og:title → `<title>`）；缺失时用 episode_id 作为标题 |
| 标题含网站名后缀 | `<title>` 含" - 小宇宙"等后缀 | 脚本已自动清理常见后缀分隔符 |
| podcast URL 误识别为 episode | `/podcast/` 路径 | 脚本已区分 `/podcast/` 和 `/episode/`，podcast 不会被当作 episode 处理 |

### YouTube 相关

| 问题 | 原因 | 解决 |
|------|------|------|
| 字幕获取失败 / `youtube-transcript-api` 报错 | 网络不通 / 无可用字幕 | 配置代理（`HTTPS_PROXY` 环境变量）；脚本会自动 fallback 到 yt-dlp 下载音频 |
| `youtube-transcript-api` 未安装 | 未安装 | `pip install youtube-transcript-api`；不装也能用（直接走 yt-dlp fallback） |
| yt-dlp 下载 YouTube 音频失败 | 网络不通 / 地区限制 | 配置代理：`setx HTTPS_PROXY "http://127.0.0.1:7890"`（举例 Clash 默认端口） |
| YouTube 视频需要登录 | 私密视频 / 会员视频 | 本 skill 不支持，跳过该视频 |
| 字幕是机器自动生成 | YouTube 自动字幕 | 仍然可用，但可能有同音错字；阶段 2 的 opencc 和错字修正字典会处理部分 |
| 字幕语言不对 | 优先级是 zh-Hans > zh > zh-CN > en | 脚本会 fallback 到自动字幕；或手动修改 `fetch_youtube.py` 中的 languages 列表 |
| yt-dlp --dump-json 失败 | 网络不通 / 视频不存在 | 检查 URL；配置代理；脚本会用 `YouTube_{video_id}` 作为兜底标题 |

### 通用

| 问题 | 原因 | 解决 |
|------|------|------|
| ffmpeg 未找到 | 未安装或不在 PATH | `winget install Gyan.FFmpeg`（Windows）/ `brew install ffmpeg`（Mac） |
| 链接非抖音/B站域名 | 输入文件混入其他链接 | 脚本自动跳过（detect_platform 返回 unknown） |

## 阶段 2：转录

| 问题 | 原因 | 解决 |
|------|------|------|
| faster-whisper 模型下载慢 | 默认从 HuggingFace 下载 | 设置环境变量 `HF_ENDPOINT=https://hf-mirror.com` |
| 输出繁体字 | Whisper small 默认输出繁体 | 已内置 opencc t2s 转换，若仍有繁体检查 `pip install opencc-python-reimplemented` |
| 同音错字 | Whisper 在中文上的常见错误 | 已内置错字修正字典（common.py 的 ERROR_CORRECTIONS），可自行扩展 |
| 转录速度慢 | CPU 模式 + small 模型 | 5 分钟视频约 3 分钟；如需更快可换 tiny 模型（精度下降） |
| 内存不足 | 模型加载占用 | 关闭其他大型程序；或换 tiny/base 模型 |
| 转录完全空白 | 音频文件损坏或时长为 0 | 检查 audio_N.mp3 是否可播放；重新下载 |

## 阶段 3：打包 + 工作表

| 问题 | 原因 | 解决 |
|------|------|------|
| boundary-review 路由建议不准 | 标题启发式判断局限 | 主对话可在阶段 4 调整路由 |
| takes_packed 窗口过多/过少 | 90 秒窗口不适合该视频 | 不影响最终切分，只是预打包给主对话读 |
| transcript 文件找不到 | 阶段 2 失败 | 检查 metadata.json 中哪些视频成功 |

## 阶段 4：主对话切分

| 问题 | 原因 | 解决 |
|------|------|------|
| 主对话切分场景太少 | 一刀切整个视频 | 按 Light-plus 原则，按语义完整性调整；建议 5-10 个场景 |
| 主对话切分场景太多 | 按每句话切 | 按"完整知识点/论点"切，不要按句切 |
| scene-boundaries.json 缺失 | 主对话忘记写 | 主对话必须为每个视频写一个 scene-boundaries_N.json |
| 场景之间有重叠或空隙 | start/end 计算错误 | 检查相邻场景：scene[i].end_sec == scene[i+1].start_sec |
| 最后一个 end_sec < 视频时长 | 边界未覆盖到结尾 | 最后一个 end_sec 必须 >= transcript 最后一个 segment 的 end |
| 遇到无清晰边界的内容 | 纯口播无结构 | 整段保留，标注"无清晰边界"在 reason 中 |

## 阶段 5：输出

| 问题 | 原因 | 解决 |
|------|------|------|
| 某场景无内容 | boundaries 的 start/end 不在 transcript 范围内 | 检查 start/end 是否在 [0, duration] 区间 |
| 输出 MD 中文字乱码 | 编码问题 | 脚本已强制 UTF-8 编码，若仍有问题检查文件读取方式 |
| 场景标题缺失 | scene-boundaries.json 中 scene 缺 title | 补充 title 字段 |
| 目录链接失效 | 标题含特殊字符 | safe_filename 已清理，若仍有问题检查正则 |

## 通用问题

| 问题 | 原因 | 解决 |
|------|------|------|
| Python 版本过低 | 需要 3.9+ | `python --version` 检查，升级到 3.9+ |
| 路径含空格 | Windows 路径问题 | 用引号包裹路径：`"D:\TRAE SOLO CN\..."` |
| 权限不足 | 输出目录不可写 | 检查 outputs/ 目录权限 |
| 磁盘空间不足 | 音频+模型+输出 | 至少预留 2GB 空间（模型 466MB + 音频 + 输出） |
