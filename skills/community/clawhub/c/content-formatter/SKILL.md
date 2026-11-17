---
name: content-formatter
version: "1.0.0"
description: 统一内容排版引擎,支持29平台排版规则,4层排版策略(L0无需转换/L1通用HTML/L2平台专属/L3纯文本)。触发:内容排版/格式转换/平台适配
tools:
  - subprocess
dependencies: []
metadata:
  layer: plugin
  priority: P1
  category: content-creation
  requires:
    config: []
  bins:
    - python
  env: []
  os: [windows, linux]
---

> **核心功能**: 本技能提供/平台适配等能力。


# content-formatter 统一内容排版引擎

> 整合 base.py 的 `_ensure_content_format`、`format_converter.py`、`content_platform_adapter.py` 的 `_adapt_content_format` 三处分散排版入口,统一为单一排版引擎,支持 29 平台排版规则。

## 使用场景

- 内容发布前排版适配: 将 Markdown 原始内容转换为目标平台所需的格式(HTML/Markdown/纯文本)
- 多平台批量发布: 一次输入,按各平台规则分别输出对应格式
- 格式降级兜底: 当平台专属排版器不可用时,自动降级到通用 HTML 转换
- 统一排版入口: 消除三处分散排版逻辑(base.py/format_converter.py/content_platform_adapter.py),所有排版经由本引擎统一处理

## 4层排版策略

| 层级 | 说明 | 适用平台 | 处理方式 |
|:-----|:-----|:---------|:---------|
| L0 | 无需转换 | Markdown 原生平台(掘金/CSDN/思否等) | 保持 Markdown 原文输出 |
| L1 | 通用 HTML | 大多数 HTML 平台(搜狐/大鱼/网易等) | Markdown→HTML + 默认内联 CSS |
| L2 | 平台专属 | 微信公众号/知乎/百家号/微博 | 调用 format_converter 专属样式,失败降级 L1 |
| L3 | 纯文本 | Twitter/X 等短文本平台 | 去除 Markdown 标记 + 字符截断 |

## 工作流

1. 接收内容和平台参数
   - 输入: `--content`(Markdown 原始内容) `--platform`(目标平台) `--format`(可选,目标格式)
   - 支持 `--content-file` 从文件读取内容(替代 `--content`)
2. 查询平台排版规则
   - 从 `platform_styles.json` 加载平台配置(format/layer/style/inline_css/features/max_length)
   - 未知平台默认使用 L1 通用 HTML 排版
3. 执行排版转换
   - L0: 保持 Markdown 原文,不转换
   - L1: 调用 `_basic_md_to_html` 进行通用 Markdown→HTML 转换(可选内联 CSS)
   - L2: 调用 `_format_via_converter` 调用 format_converter.py 专属排版器,失败则降级 L1
   - L3: 调用 `_strip_markdown` 去除 Markdown 标记,按 max_length 截断
4. 返回格式化内容
   - 输出 JSON: `{success, data:{html, markdown, text, format_used, layer}, error}`

## 输入格式

```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 标题\n\n正文内容" \
  --platform wechat_official \
  --format html
```

参数说明:
- `--content`(必填): 原始内容(Markdown 格式)
- `--platform`(必填): 目标平台名称(如 juejin/wechat_official/zhihu/x_twitter 等)
- `--format`(可选): 目标格式(html/markdown/text),留空则按平台配置自动判断
- `--content-file`(可选): 内容文件路径,替代 `--content`(适合长文本)

## 输出格式

```json
{
  "success": true,
  "data": {
    "html": "<h1>标题</h1><p>正文内容</p>",
    "markdown": "# 标题\n\n正文内容",
    "text": "标题\n\n正文内容",
    "format_used": "html",
    "layer": "L1"
  },
  "error": null
}
```

字段说明:
- `html`: HTML 格式内容(L0/L3 平台为空字符串)
- `markdown`: Markdown 原文(L3 平台为转换后的纯文本)
- `text`: 纯文本内容(仅 L3 平台有值)
- `format_used`: 实际使用的格式(html/markdown/text)
- `layer`: 实际使用的排版层级(L0/L1/L2/L1(fallback))

## 异常处理

| 异常场景 | 处理方式 | 降级层级 |
|:---------|:---------|:---------|
| 未知平台 | 使用默认 L1 通用 HTML 排版 | L1 |
| L2 专属排版器不可用(format_converter.py 不存在) | 降级到 L1 通用 HTML | L1(fallback) |
| L2 专属排版器调用失败(超时/返回错误) | 降级到 L1 通用 HTML | L1(fallback) |
| markdown 库未安装 | 使用简单正则替换进行基础转换 | L1(基础) |
| 排版引擎内部异常 | 返回 `{success:false, error:..., code:...}` | 无 |

所有异常均通过 try/except 捕获,排版失败时返回结构化 JSON 错误信息,不抛出未捕获异常。

## 示例

### 示例1: Markdown 平台(掘金) - L0 无需转换

```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 测试标题" \
  --platform juejin
```

输出:
```json
{"success": true, "data": {"html": "", "markdown": "# 测试标题", "text": "", "format_used": "markdown", "layer": "L0"}, "error": null}
```

### 示例2: 微信公众号 - L2 平台专属排版

```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 测试标题" \
  --platform wechat_official
```

输出:
```json
{"success": true, "data": {"html": "<h1 style=\"...\">测试标题</h1>", "markdown": "# 测试标题", "text": "", "format_used": "html", "layer": "L2"}, "error": null}
```

### 示例3: Twitter/X - L3 纯文本截断

```bash
python skills/content-formatter/scripts/format_engine.py \
  --content "# 标题\n\n这是一段很长的正文内容..." \
  --platform x_twitter
```

输出:
```json
{"success": true, "data": {"html": "", "markdown": "标题\n\n这是一段很长的正文内容...", "text": "标题 这是一段很长的正文内容...", "format_used": "text", "layer": "L3"}, "error": null}
```

## 集成说明

本引擎被 `mcps/multi-publisher-mcp/publishers/base.py` 的 `_ensure_content_format` 方法调用,作为统一排版入口。调用方式为 subprocess 子进程调用,失败时降级到 base.py 内置的 format_converter 路径(P1-5 已有逻辑)。

### 29 平台清单

L0(Markdown 原生,9个): juejin, csdn, segmentfault, cnblogs, 51cto, oschina, yuque, imooc, jianshu, woshipm, bilibili_col
L1(通用 HTML,13个): toutiao, douban, sohu, dayu, netease, yidian, smzdm, xueqiu, eastmoney, douyin_img, sohufocus, wordpress, typecho
L2(平台专属,4个): wechat_official, zhihu, baijiahao, weibo
L3(纯文本,1个): x_twitter

### wenyan CSS 主题说明

> wenyan CSS 主题已随 wenyan-mcp 归档,如需使用从 mcps/wenyan-mcp/ 源码提取。
> R6复核修复(BUG-FAKE-121+): wenyan-mcp已归档,list_themes不再可用(如需CSS主题,执行npm pack @wenyan-md/mcp提取dist/themes/*.css)

wenyan-mcp(`@wenyan-md/mcp`, Node 运行时)的 CSS 主题文件内联在 npm 包源码中,本地 `mcps/wenyan-mcp/` 目录仅保留 `mcp.json`(工具声明: render_markdown/list_themes/register_theme/delete_theme/publish_draft)和 `.env.example`,不含独立 `.css` 文件。

如需获取 wenyan 内置主题 CSS:
1. 执行 `npm pack @wenyan-md/mcp` 解包后提取 `dist/themes/*.css`
2. 或调用 wenyan-mcp 的 `list_themes` 工具在线获取主题列表
3. 提取后将 CSS 放置到 `skills/content-formatter/assets/themes/` 目录(当前不存在,需创建)
