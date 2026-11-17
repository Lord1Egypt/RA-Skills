---
name: project-generate
version: 2.7.0
description: "项目编排层 — 首帧图生成、视频提交/轮询/拼接、状态查看/导出。提供 project_generate.py 作为统一入口，所有命令为子命令形式。图片生成走 Agnes AI（agnes-ai 子 skill），视频生成通过 Provider 路由（支持 Agnes / 小云雀 / LibTV 等）。"
---

# project-generate — 项目编排层

作为 `ai-video-auto-generator` 的子 skill，提供项目级的生成、提交、轮询、拼接全流程编排。

> **项目创建**请使用 `ai-video-auto-generator` 的 `create_project.py`（在 skill 根目录执行）：
> ```bash
> python3 scripts/create_project.py \
>   --project <路径> --template short_drama
> ```
> 创建完成后，本 skill 的所有命令都要求项目目录已存在并包含 `script.json`。

## 统一入口

```bash
# 在 skill 根目录执行
python3 skills/project-generate/scripts/project_generate.py
```

## 命令列表

所有命令通过子命令（subcommand）调用，`--project` 为全局必选参数：

```bash
project_generate.py --project <项目目录> <命令> [选项]
```

### 资产生成

| 命令 | 别名 | 说明 |
|------|:----:|------|
| `generate-characters` | `gc` | 读 `character_cards`，批量生成角色资产图（front/face/side/back/action/pose 多视图） |
| `generate-scenes` | `gs` | 读 `scene_cards`，批量生成场景资产图（广角/中景/特写 3 视角） |
| `generate-troops` | `gt` | 读 `troop_cards`，批量生成辅助资产图（白背景全身展示） |

### 首帧图生成

| 命令 | 别名 | 说明 |
|------|:----:|------|
| `build-first-frames` | `bff` | 读取 script.json，生成各 shot 的 first_frame 配置和 prompt 模板文件（不调 API）。生成后自动验证六段式格式 |
| `generate-images` | `gi` | 调 API 批量生成首帧图。对失败的首帧图自动重试（L1→L3 降敏），单次 API 调用 180s 超时保护 |
| `verify` | — | 用 Haar Cascade 验证首帧图质量 |
| `verify-scenes` | `ve-scenes` | 验证场景图是否包含人物 |

### 后台运行

| 命令 | 说明 |
|------|------|
| `bg <子命令>` | 后台启动子命令。用 `subprocess.STARTUPINFO(wShowWindow=0)` 隐藏 `python.exe` 的控制台窗口，进程完全脱离当前控制台，不会被 WorkBuddy 断开连接杀死。**不通过 cmd.exe /c 中转**（中文路径重定向会报错）。stdout 直接重定向到 `pipeline.log`。示例：`project_generate.py --project . bg auto` |

### 视频流水线

| 命令 | 说明 |
|------|------|
| `submit [--force [id...]]` | 提交视频任务。`--tracker local`（默认）用本地 JSON 记录，`--tracker feishu` 用飞书 Base |
| `poll` | 轮询视频完成状态 + 自动下载 + 全部完成后触发拼接。**持续轮询**每 10 分钟检查一次（代码 `time.sleep(600)`），全部完成自动进行音频+字幕叠加 |
| `stitch [--tracker local]` | **独立拼接子命令**：HF 无字幕渲染 → ffmpeg 烧录分段字幕(CRF18) → 叠加音频/BGM → 输出 `final.mp4`。脱离 `poll` 单独跑，用于只改字幕/编码后重拼（不重新提交/轮询视频） |
| `status` | 显示各 shot/segment 的视频状态 |
| `auto` | 全自动流水线。9 阶段（0→8）：脚本优化（含叙事修复）→构建prompt→角色资产→辅助资产→场景资产→首帧图→提交视频→轮询+拼接+音频。全部阶段支持断点续跑。 |

### BGM 管理

- 自定义 BGM：`sounds/bgm_custom.mp3` → `generate_bgm()` 优先使用，跳过 FreeSound 搜索
- 自动 BGM：`script.tone` 字段驱动 FreeSound 关键词搜索，按时长匹配最合适的音乐
- 多段拼接：可用 ffmpeg 将多个音乐片段交叉淡入淡出合成一个 BGM，匹配视频的叙事段落
- 详见 `references/prompt-rules.md §8 BGM 管理`

### Windows 注意事项

- **禁用 xfade 转场**：Windows 上 xfade + acrossfade 链式叠加有音视频漂移导致画面卡死，全部改用简单 concat
- **必须指定 yuv420p**：subtitles 滤镜默认输出 yuv444p 部分播放器不兼容
- **subtitles 中文路径**：libass 对中文路径支持不好，需复制到 ASCII 临时路径再引用
- **音频采样率**：强制输出 48kHz 立体声（`-ar 48000 -ac 2`）
- 详见 `references/prompt-rules.md §9 Windows ffmpeg 避坑`

### 项目管理

| 命令 | 别名 | 说明 |
|------|:----:|------|
| `preview` | — | 生成交互式 HTML 预览页（首帧图缩略图+视频状态+shot_groups 分组）|
| `report` | — | 生成 HTML 统计报告（模型分布、首帧图完成率、视频状态等）|
| `tracker-sync` | — | 从飞书 Base 反向同步任务进度到本地 task_tracker.json（仅 --tracker feishu 时有效）|

### script 优化

| 命令 | 别名 | 说明 |
|------|:----:|------|
| `optimize` | `opt` | 调用 `script-optimizer` 自动验证和优化 script.json（P0/P1/P2 分级）。支持 `--strict`、`--force`、`--dry-run`、`--report-only`、`--sync-type` |
| `build-prompts` | `bp` | 从 script.json 生成所有资产 prompt 文件到 `prompts/` 目录（角色/场景/辅助资产/视频），含 YAML frontmatter |
| `validate-script` | — | 验证 script.json 结构和关键字段完整性 |

### 诊断与修复

| 命令 | 别名 | 说明 |
|------|:----:|------|
| `diff --shot-id <id>` | — | 生成单个 shot 的首帧图新旧对比页（side-by-side + 滑块对比）|
| `diff-all` | — | 扫描 `images/storyboard/backup/` 或 `*_old.png`，批量生成对比页 + 索引页，输出到 `output/diff_index.html` |
| `repair` | — | 自动修复提示词文件：重建 assets prompts + 修复 first_frame/video 提示词 |
| `reset-prompts` | — | 删除所有提示词文件并重新生成 |
| `update-prompts <kv>` | — | 批量删除 prompt 文件中的指定段。格式: `段名:false` |

### 修复策略

生成结果不满足预期时，参考 [修复策略](../../references/repair-strategy.md) 判断改 script.json 还是改 prompt 文件。

## 通用选项

| 选项 | 说明 |
|------|------|
| `--project <path>` | 项目根目录（必选）|
| `--tracker local/feishu` | 任务追踪后端：local（本地 JSON）或 feishu（飞书 Base）|
| `--log-file <path>` | 日志文件路径（默认：`<project>/generate.log`），所有输出同时写入此文件 |
| `--verbose` | 详细输出 |
| `--quiet` | 静默模式 |

## 架构

```
project_generate.py            ← CLI 入口（子命令路由）
modules/
  ├── project_commands/        ← 包（所有 _cmd_* 业务命令，实际位于 modules/ 下）
  │     ├── __init__.py        ← 主入口 + 9 阶段流水线编排（状态持久化：__init__.py 内联）
  │     ├── 图片: _cmd_build_first_frames(), _cmd_generate_images()
  │     ├── 视频: _cmd_submit(), _cmd_poll(), _cmd_status()
  │     └── 管理: _cmd_preview() 等
  ├── provider_factory.py    ← Provider 工厂（按 script.json 选 Agnes/小云雀）
  ├── base_provider.py       ← 抽象基类（定义接口契约）
  ├── agnes_provider.py      ← Agnes AI Provider
  ├── xiaoyunqiao_provider.py ← 小云雀 Provider（含 segment 自动合并）
  ├── video_utils.py         ← 视频编排逻辑（批量提交/轮询/参考图解析）
  ├── task_tracker.py        ← 任务追踪门面
  ├── task_tracker_local.py  ← 本地 JSON 追踪
  ├── task_tracker_feishu.py ← 飞书 Base 追踪
  ├── config.py              ← 统一配置加载
  ├── feishu.py              ← 飞书 API 封装
  ├── stitch.py              ← ffmpeg 拼接
  ├── project_preview.py     ← HTML 预览
  ├── project_stats.py       ← HTML 统计
  ├── project_verify.py      ← 首帧图质量验证
  └── project_diff.py        ← 首帧图对比
```

## Provider 配置

在 `script.json` 的 `script` 块中配置：

```json
{
  "script": {
    "provider": "agnes",              // 图片生成工具（默认 agnes）
    "video_provider": "xiaoyunqiao"   // 视频生成工具（不设则同 provider）
  }
}
```

也支持从飞书文档标题自动检测：标题含"小云雀视频" → `video_provider: xiaoyunqiao`。

## 任务追踪

`--tracker` 参数选择后端：

| tracker | 后端类 | 优点 |
|---------|--------|------|
| `local`（默认）| `LocalJsonTracker` | 无依赖，所有操作在本地 |
| `feishu` | `FeishuTracker` | 可多人协作，Base 可视化 |

## 小云雀 Segment 模式

当 `video_provider=="xiaoyunqiao"` 时，`write-prompt-file` 会自动：
1. 按场景分组合并 shot 为 segment（15~45s 每段）
2. 生成 segment 级提示词文件
3. 写入 `xiaoyunqiao_segments[]` 到 script.json

`submit`/`poll` 自动检测 segments，切换为段级提交和轮询。
`stitch` 自动检测 segments，按 segment 文件拼接。

## 历史

本 skill 由 `batch_generate.py` + `batch_project.py` 合并为 `project_generate.py`，
目录名从 `batch-generate` 更名为 `project-generate`。
视频 API 函数原为 `video_api.py`（在 agnes-ai 模块中）的模块函数，逐步重构为 Provider 模式。

## 设计决策（bug 预防）

### 1. `project` 参数必须传递
所有资产生成函数（`generate_character`、`generate_scene`、`generate_image`）必须传递 `project` 参数。
- 漏传 → `upload_to_url()` 退化为 "default" → 参考图传到错误目录
- `upload_to_url()` 内部使用 `os.path.abspath(project)` 解析相对路径（如 `.` → 项目名）
- `img_host.upload_image()` 同理

### 2. API 重试封顶 + 错误感知修复
`agnes_provider.py` 中图片/场景生成采用「错误感知重试」：循环上限 `max_attempts=5`（`generate_image` / `generate_scene` 各独立计数），失败后用 `_classify_failure()` 分类并应用修复策略（软化提示词 / 换模型 / 原样重试），**仅 `rate_limit` 时固定 `sleep 30s`**，其余类别不 sleep。4xx non-429 由策略处理，不进入退避死循环。设上限、不设无限重试——5 次失败后上层 `project_commands` 自愈循环（`max_attempts=10`）接管降敏修复。

### 3. 场景验证不依赖激进 Haar 配置
`project_verify.py` 使用 Haar Cascade 多配置检测人脸。`scaleFactor=1.05/minNeighbors=3` 配置过于激进，会从废墟/火焰纹理中误报人脸。已移除，只保留 `1.1/5`、`1.2/3` 和 profile face。

### 4. 场景 prompt 模板必须 scene-aware
`prompt_builder.py` 的中景/特写 `view_desc` 不能硬编码特定场景描述（如 "cracked brickwork" 废墟模板）。必须从 scene card 的 `description` 动态派生，否则丛林场景会生成废墟砖墙。

### 5. agnes-ai 为唯一真相源（单副本）
`agnes-ai` 子 skill 是唯一的代码源。独立副本 `~/.workbuddy/skills/agnes-ai/` 已删除，**不再需要双副本同步**。所有改动只需在 `skills/agnes-ai/` 中完成，无需同步到其他位置。

### 6. bg 后台启动：STARTUPINFO + 直接 Popen，不用 cmd.exe
`launch_background.py` 的实现要点：
- 使用 `subprocess.STARTUPINFO(wShowWindow=0)` 隐藏 `python.exe` 的控制台窗口
- 不通过 `cmd.exe /c` 中转，因为中文路径（如"不死者"）在 `>` 重定向时 cmd.exe 会报错
- 直接用 `subprocess.Popen(cmd, stdout=open(log), startupinfo=si)` 启动
- 永远不要用 `pythonw.exe`——GUI 子系统下脚本的 stdout 行为异常
- 日志自动写入 `pipeline.log`

### 7. 首帧图生成：存在→验证→跳过 / 超时→降敏→重试
`generate-images` 的 `_generate_single_shot()` 实现如下自愈逻辑：

```
对每个 shot:
  1. 检查 output 路径 → 如果文件存在
     → 执行 verify_first_frame()
     → 通过: 跳过（"首帧图已存在，验证通过"）
     → 不通过: 记录问题，进入生成流程
  
  2. 生成流程（最多 4 次尝试 = 1 次初始 + 3 次重试）:
     a. 调 API 生成（180s 超时包裹）
        → 正常返回: 验证质量，通过则返回
        → API 超时/错误: 保存错误信息 → 进入下一轮重试
     
     b. 重试时:
        - 检测到 timeout / HTTP 400 / content_policy_violation
          → error_utils.soften_prompt 逐级降敏（先经 error_utils.classify 分类错误）:
            L1: 移除高风险动作词 + 武器关键词
            L2: 强制静态人像
            L3: 降级为空场景
        - 持久化修复后的 prompt 到文件
        - 继续下一轮 API 调用
  
  3. 4 次全部失败 → 标记为 ❌ 失败，汇总输出
```

关键点：
- 180s 超时防止 Agnes API 调用（由 `agnes_provider.generate_image` / `image_api.generate_image` 处理）的重试阻塞单 shot 处理
- `last_error` 在 except 中捕获并传递到下一轮重试的 auto_fix
- auto_fix 识别 "timeout"、"invalid input image"（武器类内容的误导性错误码）和 content_policy_violation
- 武器关键词（枪/手枪/步枪/瞄准/射击等）自动替换为中性描述
- 修复后的 prompt 持久化到文件，下次生成直接用修复版

### 8. HF 渲染：必须让 hyperframes 自动发现 headless shell，禁止注入浏览器 env var
`hyperframes_stitch.py` 的渲染入口**绝不能**设置 `HYPERFRAMES_BROWSER_PATH` / `PUPPETEER_EXECUTABLE_PATH` 强制指向系统 Edge。原因（2026-07-15 实证）：
- hyperframes 主渲染路径走 `resolveHeadlessShellPath`，自动发现 `~/.cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell.exe`（puppeteer 自动化构建，专为 CI 沙箱优化，无需 GUI/COM）。
- 一旦注入 Edge 路径，headed 浏览器发现链（`findFromEnv2`）会捕获它用于 GPU 探测 → 系统 Edge 单实例架构下新 msedge.exe 转交已运行实例后 Code:0 秒退 → GPU 探测失败 → worker 校准失败 → 渲染级联失败回退 ffmpeg。
- **正确做法**：不设置这两个 env var，让 hyperframes 自动发现 headless shell（约 2.7min 渲染 18 镜头 2258 帧）。Edge 在本机因会被系统/用户自动重开，实际不可用于渲染。

### 9. 字幕分段：按词边界（空格）切，绝不按时间/字数硬切
`_split_long_subtitle()` 按**空格分隔的完整词**累积切分，保证一个词不被劈开。不要按时间（会造成一句话分两段）或纯字数硬切（可能从词中间截断）。长文本按完整词累积到 `max_chars`(默认 15 字/行) 后切段；若整段 < min_seg_dur 则合并到最后一段。

### 10. 字幕字体/编码约定
- 烧录滤镜 `force_style='FontName=Microsoft YaHei,FontSize=14,PrimaryColour=&H00FFFFFF,Outline=1,Shadow=1'`（14px 适配 720 宽视频）。
- 必须指定 `yuv420p`（libass 默认 yuv444p 部分播放器不兼容）。
- 字幕时间轴使用 `actual_durations`（ffprobe 探测真实视频时长），不使用 script 的 `duration_seconds` 计划值（逐镜头偏差 0.04–0.4s 累积会偏移后段字幕）。
- 成片默认编码 `-crf 18`（高码率）。

### 11. safe-delete 沙箱坑：os.remove / os.unlink 必须 try/except
托管 Python 的 safe-delete 钩子在沙箱无回收站时会抛 `SAFE_DELETE_FAIL_CLOSED`。若直接调用 `os.remove(final_hf.mp4)` / `os.unlink(_temp.mp4)` 不上抛保护，异常会被 `run_first` 当成拼接致命错误 → 误报"拼接失败"（其实 final.mp4 已写好）。现已全部包 try/except，删不掉仅 `[warn]` 不致命。
