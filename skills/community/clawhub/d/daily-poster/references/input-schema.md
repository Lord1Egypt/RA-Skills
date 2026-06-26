# Input And Output Schema

## Entry

```bash
python scripts/render_poster.py --spec <spec.json> --output out/poster
```

可直接调用：

- `python scripts/render_daily_poster.py --spec ... --output ...`
- `python scripts/render_baidu_hot.py --spec ... --output ...`

## Shared Fields

- `poster_type`: `daily` 或 `baidu_hot`
- `base_date`: `today` 或 `YYYY-MM-DD`
- `personal_info`
- `output`

`poster_type` 语义映射：

- `daily` = `摸鱼日报` / `日报` / `日刊` / `今日简报` 风格海报
- `baidu_hot` = `百度热搜` / `百度热点` / `热搜榜` 风格海报

注意：

- JSON 输入里仍然使用英文枚举值 `daily` 和 `baidu_hot`
- 中文名称、中文别名主要用于提示词理解、AI 识别和文档阅读

## AI 识别提示

如果需求、提示词或说明文本里出现下面这些中文说法，可按以下规则理解：

| 中文说法 | 规范 `poster_type` | 说明 |
| --- | --- | --- |
| 摸鱼日报 | `daily` | 默认指中文日报风格海报 |
| 摸鱼海报 | `daily` | 常见口语表达，按日报模板处理 |
| 日报 / 日刊 / 今日简报 | `daily` | 指向 `daily` 版式 |
| 百度热搜 | `baidu_hot` | 默认指百度热搜榜海报 |
| 百度热点 | `baidu_hot` | 与百度热搜同义使用 |
| 热搜榜 | `baidu_hot` | 在本项目中默认映射到百度热搜模板 |

推荐理解规则：

- 用户提到 `摸鱼日报`、`日报`、`今日简报` 时，优先生成 `daily`
- 用户提到 `百度热搜`、`百度热点`、`热搜榜` 时，优先生成 `baidu_hot`
- 如果用户用中文描述需求，AI 在生成 JSON 时应输出英文字段值，不要把 `poster_type` 直接写成中文

`personal_info` 兼容：

- `name` / `title`
- `bio_lines` / `text_lines` / `bio` / `signature`

约束：

- `bio_lines` 和 `text_lines` 最多保留前 `2` 行非空内容

`output` 示例：

```json
{
  "output": {
    "formats": ["svg", "png"],
    "scale": 2,
    "quality": 92,
    "background": "#ffffff"
  }
}
```

- `formats` 支持 `svg`、`png`、`jpg`、`jpeg`、`webp`
- 渲染器总是先输出 SVG，再按需生成位图
- `scale` 影响 `png`、`jpg`、`jpeg`、`webp` 的尺寸倍率，不影响 SVG
- `quality` 只影响 `jpg`、`jpeg`、`webp`
- `background` 主要用于 `jpg`、`jpeg` 这类不透明输出，也可显式指定其他位图导出底色

## AI 生成图片提示

如果用户的目标不是“只要 SVG 源文件”，而是“要图片文件”“发 PNG”“导出 JPG”“给我 WEBP”，AI 应显式补全 `output` 字段。

推荐映射：

| 用户说法 | 推荐 `output` |
| --- | --- |
| 生成图片 / 导出图片 / 发我海报图 | `"formats": ["png"], "scale": 2` |
| 同时要 SVG 和 PNG | `"formats": ["svg", "png"], "scale": 2` |
| 导出 JPG / JPEG | `"formats": ["jpg"], "scale": 2, "quality": 92, "background": "#ffffff"` |
| 导出 WEBP | `"formats": ["webp"], "scale": 2, "quality": 92` |

推荐规则：

- 用户没有指定格式，但明确要“图片”时，优先用 `png`
- 用户要“源文件 + 图片”时，优先用 `["svg", "png"]`
- 用户要朋友圈、聊天发送、通用分享图时，优先用 `png`
- 用户要更小体积时，可考虑 `webp`
- 用户明确要 `jpg` / `jpeg` 时，记得补 `background`
- AI 生成 JSON 时，优先显式写 `output.formats`，不要只依赖命令行输出后缀推断

推荐 JSON 片段：

PNG：

```json
{
  "output": {
    "formats": ["png"],
    "scale": 2
  }
}
```

SVG + PNG：

```json
{
  "output": {
    "formats": ["svg", "png"],
    "scale": 2
  }
}
```

JPG：

```json
{
  "output": {
    "formats": ["jpg"],
    "scale": 2,
    "quality": 92,
    "background": "#ffffff"
  }
}
```

WEBP：

```json
{
  "output": {
    "formats": ["webp"],
    "scale": 2,
    "quality": 92
  }
}
```

命令建议：

- 当 `output.formats` 里只有一个格式时，可以用 `--output out/poster` 或 `--output out/poster.png`
- 当 `output.formats` 里有多个格式时，推荐用 `--output out/poster`，程序会生成同名不同后缀文件
- AI 如果需要给出完整命令，优先使用：

```bash
python scripts/render_poster.py --spec <spec.json> --output out/poster
```

## Stdout JSON

成功时统一输出：

```json
{
  "ok": true,
  "poster_type": "daily",
  "spec_path": "C:/.../references/daily-poster-spec.json",
  "requested_output": "C:/.../out/poster.svg",
  "output_formats": ["svg"],
  "primary_output": "C:/.../out/poster.svg",
  "rendered_files": [
    {
      "format": "svg",
      "path": "C:/.../out/poster.svg"
    }
  ]
}
```

## `daily`（摸鱼日报）

输入：

```json
{
  "poster_type": "daily",
  "personal_info": {
    "name": "智普虾🦐",
    "bio_lines": [
      "OpenClaw 驱动的 AI 助手，搭载 GLM5 模型，机智温暖有点俏皮"
    ]
  }
}
```

## `baidu_hot`（百度热搜）

输入：

```json
{
  "poster_type": "baidu_hot",
  "personal_info": {
    "name": "智普虾🦐",
    "bio_lines": [
      "OpenClaw 驱动的 AI 助手，搭载 GLM5 模型，机智温暖有点俏皮"
    ]
  }
}
```

