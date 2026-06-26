# aim-blog-write

SEO 博客生成 Skill —— 基于 AEP 网关自动生成 SEO 优化的博客文章，并输出为带配图的 Word 文档。

## 功能

- 输入主题、行业、语言，自动调用 SEO Agent 生成完整的博客内容
- 自动下载配图并嵌入 Word 文档
- 支持 Markdown 渲染（标题、列表、加粗、斜体、代码块、链接等）
- 输出结构化结果：`.docx` 文稿 + 原始图片 + JSON 原始数据

## 前置条件

### 1. 密钥配置

使用前需要获取 `aim-secret-key`：

1. 前往 [https://tools.mentarc.cn/aim-skills/](https://tools.mentarc.cn/aim-skills/) 注册账号
2. 获取你的 `aim-secret-key`
3. 复制配置模板并填入密钥：

```bash
cp .env.example .env
```

编辑 `.env`，将密钥填入：

```
aim-secret-key=你的密钥
```

### 2. Python 依赖

```bash
pip install requests python-docx
```

## 使用方式

### 一键生成 Word 文稿（推荐）

```bash
python3 scripts/blog_to_word.py \
  --theme "Global Supply Chain Trends" \
  --industry "electronics,fashion" \
  --language "en"
```

输出位置：`output/<task>_<timestamp>/`

| 文件 | 说明 |
|------|------|
| `<task>.docx` | 渲染后的 Word 文稿（标题、关键词、正文、配图） |
| `images/` | 下载的原图 |
| `raw.json` | 接口原始返回 |

可选参数：

| 参数 | 说明 |
|------|------|
| `--task-name <名字>` | 自定义任务名（默认从 theme 截取） |
| `--out-dir <路径>` | 自定义输出目录 |
| `--timeout <秒>` | 接口调用超时时间（默认 900） |

### 仅生成 JSON（不需要 Word）

```bash
bash scripts/seo_agent.sh '{
  "theme": "AI in Manufacturing",
  "industry": "tech",
  "language": "en"
}'
```

也支持管道输入：

```bash
echo '{"theme": "AI in Manufacturing", "industry": "tech", "language": "en"}' \
  | bash scripts/seo_agent.sh
```

## 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `theme` | string | 是 | 博客主题 |
| `industry` | string | 是 | 行业领域，多个用逗号分隔（如 `electronics,fashion`） |
| `language` | string | 是 | 目标语言（如 `en`、`zh`） |

## 输出示例

### blog_to_word.py

```json
{
  "success": true,
  "docx": "/path/to/output/<task>_<ts>/<task>.docx",
  "images_dir": "/path/to/output/<task>_<ts>/images",
  "image_count_downloaded": 2,
  "image_count_embedded": 2,
  "out_dir": "/path/to/output/<task>_<ts>"
}
```

### seo_agent.sh

```json
{
  "success": true,
  "data": {
    "blog_content": "# How Reusable Rockets Are Reshaping...\n\n...",
    "keywords": {"keyword1": "...", "...": "..."},
    "images": [
      {"image_url": "http://...", "rephraser_result": "...", "aspect_ratio": "16:9"}
    ]
  }
}
```

## 文件结构

```
aim-blog-write/
├── .env.example          # 密钥配置模板
├── .env                  # 密钥配置（需自行创建，已 gitignore）
├── SKILL.md              # Skill 详细文档
├── scripts/
│   ├── blog_to_word.py   # 主入口：生成 Word 文稿
│   ├── seo_agent.sh      # 调用 AEP 接口，解析 SSE 流
│   ├── env_guard.sh      # 密钥校验与加载
│   └── common.sh         # 公共函数库
└── output/               # 运行时生成（已 gitignore）
```

## 注意事项

- 三个必填字段（theme / industry / language）缺一不可，否则无法生成
- 图片来源于后端 FFS 链接，可能为内网地址，脚本已配置直连
- 单张图片下载失败不会阻塞整体生成，缺失图片会记录在日志中
- 请勿将 `.env` 中的密钥提交到代码仓库
