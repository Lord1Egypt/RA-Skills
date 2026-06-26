---
name: customer-logo-wall
version: 1.2.0
description: 处理客户表格并生成Logo墙PPT的自动化工具。当用户提到"客户表格"、"公司中文名"、"Logo墙"、"客户logo"或需要处理Excel中的客户数据并生成PPT时使用此技能。
---

# Customer Logo Wall — 客户Logo墙生成工具

## 技能概述

从 Excel 客户列表出发，自动完成：
1. 读取公司英文名 → 搜索/确认中文名
2. 按知名度分 Tier 排序
3. 用百度图片 + Bing 备选自动下载公司 Logo
4. **Logo 格式标准化**（JPEG/WEBP/SVG → 真正 PNG，防止 API 报错）
5. 自动核验 Logo 准确性（无需用户手动校对）
6. 生成专业 Logo 墙 PPT

## 工作流程

### Step 1：读取 Excel

读取用户提供的 Excel 文件，提取公司英文名列（通常为 "Customer" 列）。同时读取中文名列（若已有）。

### Step 2：确定中文名

若 Excel 中已有中文名列，直接使用。若没有，对每家公司进行网络搜索，获取官方中文名。
- 搜索策略：百度百科、企业官网、香港公司注册处
- 搜不到的公司保留英文名

### Step 2.5：将中文名写回原 Excel

确定中文名后，**必须**将结果写回用户的原始 Excel 文件，而不是只保存在中间 JSON 中。

**操作步骤：**
1. 在原 Excel 的 Customer 列（公司英文名）**紧后面插入一列**
2. 新列表头设为"公司中文名"
3. 按行匹配英文名，填入对应中文全称
4. 匹配时注意处理标点差异（如单引号 `'` vs 撇号 `'`）
5. 保存覆盖原文件，告知用户

> ⚠️ 这一步是必须的，用户需要中文名留在原始表格中。

### Step 3：Tier 分级排序

按以下标准将公司分为 4 个 Tier：

| Tier | 标准 |
|------|------|
| 1 | 全球知名企业：世界500强、行业绝对龙头（如台积电、摩根士丹利、国泰航空） |
| 2 | 行业领先：知名上市公司、区域一线品牌（如海信、三井住友、香港电讯） |
| 3 | 区域知名：有一定规模的上市/知名企业（如联影医疗、太古地产、德勤） |
| 4 | 其他客户：规模较小或知名度较低的企业 |

### Step 4：下载 Logo

使用 `scripts/download_logos.py` 自动下载 Logo。

**关键配置**（根据你的环境修改）：
- 浏览器路径：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`（或系统 Chrome 路径）
- Node路径：`<你的Node路径>/bin/node`
- Node模块：`<你的Node路径>/workspace/node_modules`
- playwright 需用上述 Node 环境执行

> 💡 快速获取路径：`which node` 和 `npm root -g`

**搜索策略**（按优先级）：
1. 百度图片搜索：`{公司中文名} {英文名} logo`
2. 若百度失败，尝试访问公司官网抓取 header 中的 logo img
3. 若仍失败，用 Bing 图片搜索（英文关键词，适合国际公司）

### Step 4.5：Logo 格式标准化（新增 v1.2.0）

使用 `scripts/normalize_logos.py` 将所有下载的 Logo 统一为真正的 PNG 格式。

**解决的问题**：
- 搜索引擎返回的图片实际是 JPEG/WEBP/SVG，但扩展名为 `.png`
- SVG 伪装为 PNG → Anthropic API 报错 `Could not process image`
- WEBP 格式在部分系统和 PowerPoint 中不支持

**转换策略**（自动检测文件头）：
| 实际格式 | 转换方式 |
|---------|---------|
| JPEG/WEBP | Pillow 转 RGBA → 保存 PNG |
| SVG | rsvg-convert → cairosvg → qlmanage（macOS）按优先级尝试 |
| 已是 PNG | 跳过，仅验证完整性 |

> ⚠️ `build_ppt.py` 也内置了运行时格式修复（`ensure_real_png`），但建议先跑一遍标准化脚本。

### Step 5：自动核验 Logo 准确性

**本步骤无需用户手动校对**，使用 `scripts/verify_logos.py` 自动核验：

1. **OCR 文字识别**：用 `pytesseract` 提取图片中的文字，检查是否包含公司名称关键词
2. **图片质量检查**：过滤纯色图、截图页面（非纯 logo）、文件过小的图
3. **相似度评分**：对识别出文字与公司名的匹配度打分（0-1），低于阈值（0.3）判定为错误
4. **不确定的自动重搜**：核验失败的公司自动换用其他搜索关键词重试（最多 3 次）

详见 `references/logo-verification.md`。

### Step 6：生成 PPT

使用 `scripts/build_ppt.py` 生成 Logo 墙 PPT。

**PPT 设计规范**（详见 `references/ppt-design.md`）：
- 幻灯片尺寸：10 × 5.625 英寸（16:9）
- 配色：深蓝主色 #1E2761，浅背景 #F5F7FA
- 每页最多 6 个公司（2列3行）
- 卡片结构：左侧 Tier 色条 + Logo 区（1×1英寸）+ 中文名 + 英文名

## 快速运行

```bash
# 设置环境变量（根据你的实际路径修改）
export NODE_PATH="<你的Node模块路径>"
export NODE_BIN="<你的Node可执行文件路径>"
export AGENT_BROWSER="<你的agent-browser路径>"

# 1. 下载 Logo（用 Node + playwright）
$NODE_BIN scripts/download_logos.js --output <输出目录> --companies <公司列表JSON>

# 2. Logo 格式标准化（确保全部是真正的 PNG）
python3 scripts/normalize_logos.py --logos-dir <logo目录> --companies <公司列表JSON>

# 3. 核验 Logo
python3 scripts/verify_logos.py --logos-dir <logo目录> --companies <公司列表JSON>

# 4. 生成 PPT
python3 scripts/build_ppt.py --logos-dir <logo目录> --companies <公司列表JSON> --output <输出路径>
```

## 脚本说明

| 脚本 | 作用 |
|------|------|
| `scripts/download_logos.js` | 用 playwright + 百度/Bing 图片批量下载 Logo（Node.js） |
| `scripts/normalize_logos.py` | Logo 格式标准化：JPEG/WEBP/SVG → 真正 PNG（Python） |
| `scripts/verify_logos.py` | 自动核验 Logo 准确性（Python） |
| `scripts/build_ppt.py` | 生成 Logo 墙 PPT，内置格式修复（Python + python-pptx） |

## 参考文档

- `references/logo-verification.md`：Logo 自动核验的详细逻辑与阈值说明
- `references/ppt-design.md`：PPT 设计规范与颜色定义
- `references/logo-format-issues.md`：Logo 格式常见问题与解决方案

## 依赖环境

- Python 3.9+：`python-pptx`, `pillow`, `pytesseract`（可选，用于 OCR 核验）
- Node 22.12.0（管理版本路径见上）
- playwright（安装在 Node 工作区）
- 系统 Chrome：`/Applications/Google Chrome.app`（供 playwright 使用）
