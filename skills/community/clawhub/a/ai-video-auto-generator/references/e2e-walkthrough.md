# 端到端案例：锈甲天凤（34秒古风短剧）

本文档展示 AI 视频流水线从飞书文档输入到最终成片的完整流程，以 **锈甲天凤** 项目为真实案例。

> **路径说明**：本文档使用 `<skill-root>` 作为 skill 安装根目录的占位符（含 `SKILL.md` 的目录）。
> 实际使用时，在 skill 根目录执行可省略前缀（如 `python3 scripts/create_project.py ...`），
> 或在项目目录下使用完整路径（如 `python3 <skill-root>/skills/project-generate/scripts/project_generate.py ...`）。
> 详情参见 `scripts/_paths.py` 的三层路径模型。

---

## 第 1 步：飞书文档输入

用户在飞书写需求文档，标题格式：`【AI视频】【短剧】锈甲天凤`

文档内容（精简版）：
```
标题：锈甲天凤
类型：古风短剧
时长：34秒
画幅：9:16（竖屏）
角色：
  - 墨雪（明龙国女元帅，冷冽沉稳）
  - 墨将（年轻副将，忠诚活泼）
场景：龙南战场、城楼议事堂、城墙之上
剧情：敌军压境，墨雪与墨将在议事堂密议破敌之策...
```

## 第 2 步：视频类型路由

AI 视频流水线检测到文档标题包含 `【AI视频】【短剧】`：

```json
{
  "type": "短剧",
  "project_name": "锈甲天凤",
  "project_dir": "$HOME/WorkBuddy/锈甲天凤/"
}
```

加载 `references/types/短剧.md` 中的类型规则。

## 第 3 步：创建项目目录

```bash
# 在 skill 根目录执行
python3 scripts/create_project.py \
  --project "$HOME/WorkBuddy/锈甲天凤" --template short_drama
```

自动创建 13 个标准目录并写入 `script.json` 模板。

创建后的结构：
```
$HOME/WorkBuddy/锈甲天凤/
├── script.json          (模板)
├── images/characters/   (角色资产)
├── images/scenes/       (场景资产)
├── images/storyboard/   (分镜首帧图)
├── images/style/        (风格参考)
├── images/props/        (道具资产)
├── videos/              (视频片段)
├── output/              (最终输出)
├── sounds/              (音效/配乐)
├── assets/              (资产清单)
├── prompts/             (提示词文件)
├── references/          (原始需求)
├── scripts/             (快捷入口)
└── tasks/               (任务追踪)
```

## 第 4 步：生成脚本 JSON

AI 视频流水线根据需求文档生成 `script.json`，包含角色卡、场景卡和分镜表。

```json
{
  "script": {
    "title": "锈甲天凤",
    "duration_seconds": 34,
    "aspect_ratio": "9:16",
    "type": "短剧",
    "provider": "agnes"
  },
  "character_cards": [ /* 墨雪 + 墨将 */ ],
  "scene_cards": [ /* 龙南战场 + 城楼议事堂 + 城墙之上 */ ],
  "shots": [ /* 9 个镜头 */ ],
  "shot_groups": [ /* 3 组镜头 */ ]
}
```

## 第 5 步：生成角色资产

```bash
cd "$HOME/WorkBuddy/锈甲天凤"

# 一键生成所有角色（标准 4 视图：正面全身 / 面部 / 侧面 / 背面；另按武器·动作动态生成持械与动作视图，数量随角色卡而定）
# <skill-root> 为 skill 安装根目录（含 SKILL.md），请替换为实际路径
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . generate-characters
# 别名：gc
```

## 第 6 步：生成场景资产

```bash
# 每场景 3 张变体（广角/中景/特写）
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . generate-scenes
# 别名：gs
```

## 第 7~8 步：生成首帧图

```bash
# 初始化各 shot 的 first_frame 配置和 prompt 模板（不调 API）
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . build-first-frames
# 别名：bff

# 调 API 批量生成首帧图
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . generate-images
# 别名：gi
```

## 第 9 步：提交 + 轮询 + 拼接

```bash
# 提交所有 shot 视频任务（自动按 provider 路由：Agnes / 小云雀）
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . submit

# 轮询完成状态，全部完成后自动触发 ffmpeg 拼接
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . poll

# 查看项目总状态
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . status
```

## 全自动模式

以上第 5~9 步可合并为一条命令：

```bash
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . auto

# 本地追踪模式（不依赖飞书）
python3 <skill-root>/skills/project-generate/scripts/project_generate.py \
  --project . auto --tracker local
```

`auto` 自动执行：角色资产 → 场景资产 → 首帧图 → 提交 → 轮询 → 拼接。

---

## 完整流程图

```
飞书需求文档
    │
    ▼
[1] 类型路由 ── 检测【AI视频】【短剧】→ 加载短剧规则
    │
    ▼
[2] 创建项目 ── create_project.py
    │
    ▼
[3] 生成 script.json ── 角色卡 + 场景卡 + 分镜（AI 驱动）
    │
    ──── 切换到 project-generate 流水线 ────
    │
    ▼
[4] 角色资产 ── gc（每角色视图数随角色卡而定）
    │
    ▼
[5] 场景资产 ── gs（每场景 3 张）
    │
    ▼
[6] 首帧配置 ── bff
    │
    ▼
[7] 首帧图生成 ── gi
    │
    ▼
[8] 视频提交 ── submit（按 provider 路由）
    │
    ▼
[9] 轮询 + 拼接 ── poll（ffmpeg 自动拼接）
    │
    ▼
[10] 交付 ── output/final.mp4
```

**快捷方式**：`create_project.py` → `auto`，2 个命令走完全流程。
