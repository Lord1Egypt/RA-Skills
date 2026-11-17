# cinematic-image-studio · 电影级图片制作（风格库驱动）

给一个**主体 / 主题 / 一句话 / 一段场景**，从 75 张风格卡里选一张，合成一条**可直接粘贴出图的「14 节电影级提示词」**，并按需调接口出图落盘。

> 一个 Agent Skill（Claude Code / OpenCode / ClawHub 通用）。零第三方依赖，纯 Python 标准库。

## 核心机制

```
主体 / 主题  +  风格卡（styles/NN-*.md）  ──►  14 节电影级提示词  ──►  出图落盘  ──►  样图库 index.html
                         ▲
                  固定节逐字照抄（保证同风格成系列）
```

- **风格卡注入**：每张卡把【光影】【色彩】【影像质感】【背景】【风格】【画幅】写成**逐字可照抄的固定节**，同一风格下任意主体共用同一套固定节 → 同风格出图**色调 / 质感 / 光位统一、成系列**；只有【主体】【次要元素】【构图】【镜头】逐图可变。
- **默认交付是提示词，不是图**：图通常拿到即梦 / Midjourney / 可灵等工具出；只有明确说「出图」才调接口。
- **风格是第一公民**：75 张卡 + 自定义风格（按 `references/风格卡规范.md` 现场新增，永久复用）。

## 目录

```
cinematic-image-studio/
├── SKILL.md                    # 总控 SOP
├── config.json                 # 出图接口配置（key 默认为空）
├── styles/                     # 75 张风格卡（一风格一卡）+ _索引.md + _测试主体.md
├── references/                 # 14 节画面规范 / 风格卡规范
├── scripts/
│   ├── generate.py             # 出图（API 优先 / 工具兜底 / --adopt）
│   ├── build_prompts.py        # 风格卡 + 变量 → 提示词.json
│   ├── export_md.py            # 提示词.json → 提示词.md
│   ├── normalize_output.py     # 命名规范化
│   ├── backfill_api.py         # 历史图出图 API 标签回填
│   ├── gallery.py              # 缩略图 + 样图库 index.html + README
│   └── count_features.py       # 可数特征本地核验
└── assets/output/              # 样图库：提示词.json / 提示词.md / 图片 / index.html
```

## 快速开始

```bash
# 0. 看下一张要出什么（不调接口、不花钱）
python3 scripts/generate.py --project . --dry-run

# 1. 出一张（必须显式 --yes；一次只出一张）
python3 scripts/generate.py --project . --yes

# 2. 整理输出：md + 缩略图 + 样图库
python3 scripts/export_md.py && python3 scripts/gallery.py
```

- 出图接口优先读 `config.json`，也支持 `--base-url/--key/--model` 与环境变量（`NEWAPI_IMAGE_BASE_URL` / `NEWAPI_IMAGE_KEY` / `ARK_API_KEY`）。
- **首次使用请先把 `newapi_image_base_url` 换成你自己的 OpenAI 兼容网关**（默认值留空，脚本回落到公开默认地址）。
- 没有 key / 网关不通时，脚本会写出 `图片/generate_image参数.json` 并以退出码 6 交回宿主工具（`generate_image` / `edit_image`）出图，出完用 `--adopt` 收位。

## 渠道

| 渠道 | 说明 |
|---|---|
| `newapi` | 任意 OpenAI 兼容中转（`/v1/images/generations`，支持 `quality`） |
| `ark` | 火山方舟 Seedream（`/api/v3/images/generations`，2K 档尺寸） |
| `tool` | 宿主工具兜底，不花钱、不需要 `--yes` |

## 合规红线

主体默认虚构化；当代真人一律不出现；零可读文字 / Logo / 水印；不渲染血腥暴力；无政治宗教敏感；正向无否定词（排除项只进【负向】）。

## 样图

`assets/output/index.html` 双击即开：列表 + 筛选 + 点开看大图与完整提示词（样图为压缩后的 web 版 JPEG）。

## 许可

MIT
