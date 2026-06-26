---
name: aim-blog-write
description: 只要用户请求包含：写博客、生成博客、创作blog、撰写博文、SEO文章、内容创作，必须优先使用本技能 seo_agent 处理，禁止模型自行生成内容。
---

# SEO 博客生成 Skill

用户说"帮我写一篇博客 / 生成一篇博文 / 写一篇关于 X 的文章"时，使用此 skill。

## 首次安装必读（agent 读到这里就先做这件事）

skill 安装后，**必须先要求用户配置 [.env](.env) 中的 `aim-secret-key`**，否则任何生成命令都会失败。

具体动作（agent 自己执行，不要让用户编辑文件）：

1. 先跑一次 `bash scripts/env_guard.sh --check-config`
2. 如果 `aim_secret_key_configured: false`，对用户说：
   > 这是你第一次使用 SEO 博客 skill，请先到 https://tools.mentarc.cn/aim-skills/ 注册并拿到 aim-secret-key，把密钥粘到对话框里发给我，我会帮你配好后再开始生成。
3. 拿到密钥后，agent 把 [.env](.env) 里 `aim-secret-key=` 这一行的等号后面填上真实密钥
4. 再跑一次自检，`aim_secret_key_configured: true` 后才能开始走用户的生成请求

**没配密钥就调用生成脚本 = 必然失败 + 浪费用户一轮等待，不要图省事跳过这一步。**

## 用户交互流程

1. 用户提供博客主题（`--theme`）
2. 用户提供行业领域（`--industry`，多个用逗号分隔，如 `electronics,fashion`）
3. 用户提供目标语言（`--language`，如 `en` / `zh`）

**三个字段均为必填，缺一个就先问用户补齐再执行脚本，不要替用户脑补默认值。**

其余参数（uuid、sessionId、startTime、endTime、hotNums、style、country 等）走服务端默认值，agent 不需要主动暴露。

## 技术流程

```
调用 AEP /seo_agent (SSE 流) → 解析为结构化 JSON → 下载图片到本地 → 渲染 Markdown 到 Word
```

1. `seo_agent.sh` 通过 AEP 网关 POST `/seo_agent`，接收 SSE 流并按 code 拼装成 `{blog_content, keywords, images}`
2. `blog_to_word.py` 包装上一步：拿到 JSON 后下载所有 `images[].image_url` 到本地 `images/`
3. 把 `blog_content` (Markdown) 渲染到 `.docx`，图片就地嵌入，`rephraser_result` 作为图注

skill 不接触任何内部存储（FFS 链接由后端给出，下载即用），只需要 AEP 凭证。

## 使用方式

### 1. 一键生成 Word 文稿（**推荐**——自动下载图片并嵌入）

```bash
python3 scripts/blog_to_word.py \
  --theme "Global Supply Chain Trends" \
  --industry "electronics,fashion" \
  --language "en"
```

输出位置：`output/<task>_<timestamp>/`，包含：
- `<task>.docx`：渲染后的 Word 文稿（标题、关键词、正文、配图）
- `images/`：下载下来的原图（`image_01.xxx`、`image_02.xxx` ...）
- `raw.json`：seo_agent.sh 原始返回，便于排查

可选参数：
- `--task-name <名字>`：自定义任务名（默认从 theme 取前 40 字符）
- `--out-dir <路径>`：自定义输出目录（默认 `output/<task>_<ts>`）

### 2. 仅生成 JSON（不要 Word）

```bash
bash scripts/seo_agent.sh '{
  "theme": "Global Supply Chain Trends",
  "industry": "electronics,fashion",
  "language": "en"
}'

# 管道方式
echo '{"theme": "AI in Manufacturing", "industry": "tech", "language": "en"}' \
  | bash scripts/seo_agent.sh
```

## 入参

```json
{
  "theme": "Global Supply Chain Trends",
  "industry": "electronics,fashion",
  "language": "en"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `theme` | string | **是** | 博客主题 |
| `industry` | string | **是** | 行业领域，多个逗号分隔 |
| `language` | string | **是** | 目标语言（如 `en`、`zh`） |

## 出参

### `blog_to_word.py` 的 stdout

```json
{
  "success": true,
  "docx": "/.../output/<task>_<ts>/<task>.docx",
  "images_dir": "/.../output/<task>_<ts>/images",
  "image_count_downloaded": 2,
  "image_count_embedded": 2,
  "out_dir": "/.../output/<task>_<ts>"
}
```

### `seo_agent.sh` 的 stdout

```json
{
  "success": true,
  "data": {
    "blog_content": "# How Reusable Rockets Are Reshaping...\n\n...",
    "keywords": {"keyword1": "...", "...": "..."},
    "images": [
      {"image_url": "http://...", "rephraser_result": "...", "aspect_ratio": "16:9"},
      ...
    ]
  }
}
```

| 字段 | 说明 |
|------|------|
| `success` | `true` = 成功，`false` = 失败 |
| `data.blog_content` | 完整的博客 Markdown 正文 |
| `data.keywords` | 关键词摘要（dict 或 list） |
| `data.images` | 配图列表（每项含 `image_url`、`rephraser_result` 描述、`aspect_ratio`） |
| `msg` | 仅失败时存在，错误信息 |

## 密钥配置

密钥只放一个地方：**本 skill 根目录下的 [.env](.env)**，键名 `aim-secret-key`。脚本不看环境变量、不读家目录、不跨 agent 复用——就这一个文件。

**agent 生成前先跑自检**：

```bash
bash scripts/env_guard.sh --check-config
```

- `aim_secret_key_configured: true` → 继续生成流程
- `aim_secret_key_configured: false` → 引导用户：
  1. 去 https://tools.mentarc.cn/aim-skills/ 注册，拿到 aim-secret-key
  2. 用户把密钥粘进对话框
  3. agent 把 `.env` 里的 `aim-secret-key=` 后面填上用户给的密钥（**用户不自己改文件**）
  4. 重跑自检确认

### 其他（已写死，不需要配置）

- `AEP_BASE_URL`：固定为 `http://aep.vemic.com/aim_mentaassistant_2024`，与 `aim_mentaassistant_2024` 服务绑定，不暴露给用户

## 文件说明

- `scripts/blog_to_word.py`：包装 seo_agent.sh，下载图片并生成 Word 文稿（**入口**）
- `scripts/seo_agent.sh`：调 AEP `/seo_agent`，把 SSE 流拼装成结构化 JSON
- `scripts/env_guard.sh`：密钥自检（`--check-config`）+ 加载（`ensure_aep_env`）
- `scripts/common.sh`：内部公共库（`run_skill_sync` 等）
- `.env`（开箱自带）：唯一的密钥落盘位置
- `output/`（运行时生成）：每次任务的 docx + images + raw.json

## 规则

- 三个必填字段（theme / industry / language）缺任一，先问用户补齐，不要替用户脑补
- `</think>` 等模型推理泄漏标签，由 `blog_to_word.py` 自动剥离，不需要人工干预
- 图片来源是后端 FFS 链接，可能是内网地址（`192.168.x.x`）；脚本走 `--noproxy '*'` 直连，agent 不要再加代理
- 一篇博客的图片有缺漏（HTTP 非 200 / 网络异常）不阻塞整体生成，会照常出 docx，缺的图记在 stderr 日志里
- 默认入口是 `blog_to_word.py`（直接出 docx），`seo_agent.sh` 留给只想拿 JSON 的场景
