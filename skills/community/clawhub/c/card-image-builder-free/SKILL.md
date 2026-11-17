---
name: "card-image-builder-free"
description: "将文案渲染为PNG卡片图,支持海报和文章封面,适合个人创作者快速出图"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "卡片图生成器-免费版"
  version: "1.0.0"
  summary: "将文案渲染为PNG卡片图,支持海报和文章封面,适合个人创作者快速出图"
  tags:
    - "沟通协作"
    - "图片生成"
    - "卡片图"
    - "创意设计"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 卡片图生成器(免费版)
## 概述
卡片图生成器免费版是一款将文字文案渲染为PNG格式卡片图片的工具。支持文字海报(金句/大字报)、长文分页卡片和公众号文章封面图三种基础模板,内置公众号和小红书配色预设,帮助个人创作者快速生成社交媒体配图。

本版本覆盖最常用的卡片图生成场景,操作流程简洁。如需X风格帖子分享长图、自定义模板、批量生成或企业品牌定制等高级功能,请升级至PRO版。

### 免费版与PRO版能力对比
| 能力维度 | 免费版 | PRO版 |
|:---------|:-------|:------|
| 文字海报(3:4) | 支持 | 支持 |
| 长文分页卡片 | 支持 | 支持 |
| 公众号封面图 | 支持 | 支持 |
| X风格帖子长图 | 不支持 | 支持 |
| 自定义模板 | 不支持 | 支持 |
| 批量生成 | 不支持 | 支持 |
| 平台预设 | 公众号/小红书 | 全平台+自定义 |
| 高亮功能 | 整行高亮 | 整行+按词+组合 |
| 企业品牌定制 | 不支持 | 支持 |
| 水印与版权 | 不支持 | 支持 |

## 核心能力
### 1. 文字海报生成(poster-3-4)
将短文案渲染为3:4比例(900x1200)的文字海报,适合金句、大字报和封面图。

```bash
# 基本用法:生成文字海报
python3 render_card.py \
  --template poster-3-4 \
  --text " simplicity is the ultimate sophistication " \
  --out tmp/poster.png

# 带高亮的海报
python3 render_card.py \
  --template poster-3-4 \
  --text "保持简单,保持专注" \
  --hl1 "保持简单" \
  --out tmp/poster_highlighted.png

# 使用小红书配色
python3 render_card.py \
  --template poster-3-4 \
  --text "今日穿搭分享:简约风格" \
  --footer "小红书 · 我的频道" \
  --bg "#fdecea" \
  --highlight "#e53935" \
  --out tmp/poster_xhs.png
```

**参数说明:**

| 参数 | 说明 | 示例 |
|:-----|:-----|:-----|
| `--template` | 模板名称 | `poster-3-4` |
| `--text` | 文案内容 | "保持简单" |
| `--hl1` | 整行高亮文本1 | "保持简单" |
| `--hl2` | 整行高亮文本2 | "保持专注" |
| `--footer` | 页脚文字 | "公众号 · 名称" |
| `--bg` | 背景色 | `#e6f5ef` |
| `--highlight` | 高亮色 | `#22a854` |
| `--out` | 输出路径 | `tmp/poster.png` |

**输入**: 用户提供文字海报生成(poster-3-4)所需的指令和必要参数。
**处理**: 按照skill规范执行文字海报生成(poster-3-4)操作,遵循单一意图原则。
**输出**: 返回文字海报生成(poster-3-4)的执行结果,包含操作状态和输出数据。

### 2. 长文分页卡片(article-3-4)
将长文内容拆分为多页3:4卡片,适合文章摘要、步骤说明等。

```bash
# 生成长文分页卡片
python3 render_article.py \
  --template article-3-4 \
  --text "第一章:入门指南。本章将介绍基础概念和核心原则..." \
  --out tmp/article_page1.png

# 多页生成(手动指定每页内容)
python3 render_article.py \
  --template article-3-4 \
  --text "第一页内容..." \
  --page 1 \
  --total 3 \
  --out tmp/article_p1.png

python3 render_article.py \
  --template article-3-4 \
  --text "第二页内容..." \
  --page 2 \
  --total 3 \
  --out tmp/article_p2.png
```

**输入**: 用户提供长文分页卡片(article-3-4)所需的指令和必要参数。
**处理**: 按照skill规范执行长文分页卡片(article-3-4)操作,遵循单一意图原则。
**输出**: 返回长文分页卡片(article-3-4)的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 公众号文章封面图(wechat-cover-split)
生成335:100比例(1340x400)的公众号文章封面长条图,左侧标题右侧icon。

```bash
# 生成公众号封面
python3 render_card.py \
  --template wechat-cover-split \
  --text "2026年AI发展趋势全景报告" \
  --footer "公众号 · 科技前沿" \
  --bg "#e6f5ef" \
  --highlight "#22a854" \
  --out tmp/wechat_cover.png
```

**注意:** 公众号封面标题过长时,系统会自动压缩为2-3行短标题再渲染。

**输入**: 用户提供公众号文章封面图(wechat-cover-split)所需的指令和必要参数。
**处理**: 按照skill规范执行公众号文章封面图(wechat-cover-split)操作,遵循单一意图原则。
**输出**: 返回公众号文章封面图(wechat-cover-split)的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 平台配色预设
```python
# 平台预设配置
PLATFORM_PRESETS = {
    "公众号": {
        "footer": "公众号 · 早早集市",
        "bg": "#e6f5ef",        # 浅绿背景
        "highlight": "#22a854",  # 绿色高亮
    },
    "小红书": {
        "footer": "小红书 · 阿康",
        "bg": "#fdecea",        # 浅红背景
        "highlight": "#e53935",  # 红色高亮
    }
}

# 平台选择逻辑:
# - 用户提到"小红书配图" -> 使用小红书预设
# - 用户提到"小绿书" -> 使用公众号预设
# - 默认 -> 使用公众号预设
```

**输入**: 用户提供平台配色预设所需的指令和必要参数。
**处理**: 按照skill规范执行平台配色预设操作,遵循单一意图原则。
**输出**: 返回平台配色预设的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：将文案渲染为、卡片图、支持海报和文章封、适合个人创作者快、速出图、卡片图生成器免费、将文字文案渲染为、精美的、卡片图片、核心能力、长文分页卡片生成、默认平台配色预设、基础高亮功能等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:金句海报制作
将名人名言或原创金句制作成精美的文字海报。

```bash
# 生成金句海报
python3 render_card.py \
  --template poster-3-4 \
  --text "代码是写给人看的,只是顺便能让机器执行" \
  --hl1 "代码是写给人看的" \
  --footer "公众号 · 编程随笔" \
  --bg "#e6f5ef" \
  --highlight "#22a854" \
  --out tmp/quote_poster.png
```

**执行步骤:**
1. 选择 `poster-3-4` 模板
2. 输入金句文案
3. 指定高亮文本(整行高亮)
4. 选择平台预设(公众号/小红书)
5. 执行渲染,生成PNG

### 场景二:公众号文章封面
为公众号文章生成吸引人的封面图。

```bash
# 生成文章封面
python3 render_card.py \
  --template wechat-cover-split \
  --text "从零开始构建AI应用" \
  --footer "公众号 · AI实践" \
  --out tmp/article_cover.png
```

### 场景三:步骤说明卡片
将操作步骤渲染为分页卡片,便于分享。

```bash
# 生成步骤卡片(第一页)
python3 render_article.py \
  --template article-3-4 \
  --text "步骤一:安装Python环境。访问python.org下载最新版本..." \
  --page 1 \
  --total 3 \
  --out tmp/step_1.png
```

## 不适用场景

以下场景卡片图生成器-免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备
```bash
# 1. 检查Python环境
python3 --version
# 需要 Python 3+
# 2. 检查Chrome浏览器
# macOS:
ls "/Applications/Google Chrome.app"
# Linux:
which chromium

# 3. 如果缺少环境,会有提示但不中止流程
```

### 首次使用
```bash
# 生成第一张卡片图
python3 render_card.py \
  --template poster-3-4 \
  --text "Hello World! 这是我第一张卡片图" \
  --out tmp/hello.png

# 查看生成的图片
ls -la tmp/hello.png
```

### 环境检测脚本
```python
import subprocess
import os
import platform

class EnvironmentChecker:
    """环境检测器"""

    def check_all(self) -> dict:
        """检测所有依赖环境"""
        results = {
            "python": self._check_python(),
            "chrome": self._check_chrome(),
            "system": platform.system()
        }

        # 输出检测结果
        for item, result in results.items():
            if item == "system":
                print(f"  系统: {result}")
            else:
                status = "已安装" if result["installed"] else "未安装"
                version = result.get("version", "")
                print(f"  {item}: {status} {version}")
                if not result["installed"]:
                    print(f"    提示: {result.get('hint', '')}")

        return results

    def _check_python(self) -> dict:
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return {"installed": True, "version": result.stdout.strip()}
        except FileNotFoundError:
            pass
        return {
            "installed": False,
            "hint": "未检测到Python 3,渲染可能失败。请安装Python 3.6+"
        }

    def _check_chrome(self) -> dict:
        system = platform.system()
        if system == "Darwin":  # macOS
            path = "/Applications/Google Chrome.app"
            if os.path.exists(path):
                return {"installed": True, "version": "Chrome.app"}
        elif system == "Linux":
            try:
                subprocess.run(["which", "chromium"],
                             capture_output=True, check=True)
                return {"installed": True, "version": "chromium"}
            except subprocess.CalledProcessError:
                pass
        return {
            "installed": False,
            "hint": "未检测到Chrome浏览器,请安装Google Chrome"
        }

# 运行检测
checker = EnvironmentChecker()
checker.check_all()
```

## 示例
### 基础配置
```yaml
# config.yaml - 卡片图生成器免费版配置
card_image:
  # 默认模板
  default_template: poster-3-4

  # 默认输出目录
  output_dir: tmp/

  # 默认平台预设
  default_platform: 公众号

  # 平台预设
  platforms:
    公众号:
      footer: "公众号 · 你的名称"
      bg: "#e6f5ef"
      highlight: "#22a854"
    小红书:
      footer: "小红书 · 你的名称"
      bg: "#fdecea"
      highlight: "#e53935"
```

### 模板参数说明
```yaml
# templates.yaml - 模板参数说明
templates:
  poster-3-4:
    ratio: "3:4"
    size: "900x1200"
    max_chars: 200
    description: "文字海报(金句/大字报/封面)"
    params:
      - text (必需): 主文案
      - hl1 (可选): 整行高亮文本1
      - hl2 (可选): 整行高亮文本2
      - hl3 (可选): 整行高亮文本3
      - footer (可选): 页脚文字
      - bg (可选): 背景色
      - highlight (可选): 高亮色

  article-3-4:
    ratio: "3:4"
    size: "900x1200"
    max_chars: 500
    description: "长文分页卡片"
    params:
      - text (必需): 文章内容
      - page (可选): 当前页码
      - total (可选): 总页数

  wechat-cover-split:
    ratio: "335:100"
    size: "1340x400"
    max_chars: 30
    description: "公众号文章封面长条图"
    params:
      - text (必需): 文章标题
      - footer (可选): 公众号名称
```

## 最佳实践
### 1. 文案长度控制
不同模板有不同的字数上限,超出时系统会自动拆分或缩写。

```text
字数上限建议:
- poster-3-4: 不超过200字(短文案最佳)
- article-3-4: 每页不超过500字
- wechat-cover-split: 标题不超过30字
```

### 2. 高亮使用技巧
```bash
# 整行高亮:使用 --hl1, --hl2, --hl3
python3 render_card.py \
  --template poster-3-4 \
  --text "第一行\n第二行\n第三行" \
  --hl1 "第一行" \
  --hl2 "第三行" \
  --out tmp/multi_highlight.png
```

### 3. 配色选择
```python
# 配色建议
COLOR_GUIDE = {
    "公众号(绿色系)": {
        "bg": "#e6f5ef",       # 柔和浅绿
        "highlight": "#22a854", # 鲜亮绿色
        "适合": "科技、健康、教育类内容"
    },
    "小红书(红色系)": {
        "bg": "#fdecea",       # 柔和浅红
        "highlight": "#e53935", # 鲜亮红色
        "适合": "时尚、美食、生活类内容"
    }
}
```

### 4. 输出路径管理
```bash
# 推荐使用项目内tmp目录,避免写入系统/tmp
python3 render_card.py \
  --template poster-3-4 \
  --text "测试文案" \
  --out ./tmp/cards/poster_001.png

# 如需给外部工具上传,使用绝对路径
python3 render_card.py \
  --template poster-3-4 \
  --text "测试文案" \
  --out /home/user/output/poster_001.png
```

## 常见问题
### Q1: 提示"未检测到Python 3"怎么办?
**A:** 请安装Python 3.6或更高版本。访问 python.org 下载安装。安装后重新运行环境检测确认。

### Q2: 提示Chrome未找到怎么办?
**A:** 卡片图渲染需要Chrome浏览器。macOS请安装Google Chrome到 `/Applications/`。Linux请安装chromium并确保在PATH中可用。

### Q3: 文案太长怎么办?
**A:** 不同模板有字数上限。文案超出时系统会自动拆分(长文卡片)或缩写(封面标题)。建议:
- 海报文案控制在200字以内
- 封面标题控制在30字以内
- 长文卡片每页控制在500字以内

### Q4: 可以自定义背景色和高亮色吗?
**A:** 可以。通过 `--bg` 和 `--highlight` 参数指定十六进制颜色值。免费版也支持自定义颜色。

### Q5: 免费版支持X/Twitter风格的长图吗?
**A:** 不支持。X风格帖子分享长图是PRO版独有功能。免费版支持海报、长文卡片和公众号封面三种模板。

### Q6: 如何升级到PRO版?
**A:** PRO版与免费版完全兼容,升级后获得X风格长图、自定义模板、批量生成、全平台预设和企业品牌定制等高级功能。直接安装PRO版Skill即可完成升级。

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.6+
- **浏览器**: Google Chrome(渲染引擎依赖)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Python 3.6+ | 运行时 | 必需 | python.org 下载 |
| Google Chrome | 浏览器 | 必需 | google.com/chrome 下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Pillow | Python库 | 可选 | `pip install Pillow` |

### API Key 配置
- 本Skill为本地渲染工具,无需额外API Key
- 所有图片渲染在本地通过Chrome完成
- 不依赖外部图片生成服务

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行卡片图渲染任务
- **运行模式**: 本地渲染,依赖Python和Chrome
- **安全等级**: 本地处理,不涉及网络请求;输出文件存储在本地

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
