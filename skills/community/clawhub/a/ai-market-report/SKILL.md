---
name: ai-market-report
description: |
  AI 陪伴软件市场调研日报全自动生成。适用场景：
  - 用户说「生成AI陪伴软件类产品市场调研报告」「做一份 AI 陪伴软件日报」
  - 用户说「调研 AI companion 市场」「生成 XX 产品的调研报告」
  - 用户说「生成AI陪伴市场报告」且涉及 App Store 数据、MAU、营收、估值
  - 用户要求「生成 AI陪伴 PDF 格式的市场报告」且指定 AI 陪伴/companion 相关
  技能涵盖：iTunes Search API 数据采集 → Tavily 深度搜索 → Markdown 文档生成 → HTML/PDF 精美报告渲染。
---

# AI 陪伴软件市场调研日报

## 任务概述

全自动调研全球 AI 陪伴类软件头部产品的核心数据，生成五章结构 Markdown + 精美 HTML/PDF 报告。

**输出路径**：`/root/.openclaw/workspace/myfiles/daily_report_data/files/`
- `AI陪伴软件调研日报_YYYYMMDDHHMMSS.md` — 原始数据文档
- `AI_Report_YYYYMMDDHHMMSS.html` — HTML 报告
- `AI_Report_YYYYMMDDHHMMSS.pdf` — PDF 报告

---

## 第一步：数据采集

读取 `references/data_collection.md`，严格按其中步骤执行。

核心数据源：
- **App Store 评分/评价数**：iTunes Search API（直接验证，★★★）
- **MAU/营收/估值**：Tavily 深度搜索 2025-2026 年报道（★★）
- **数据原则**：能搜到填真实数字并注明来源；搜不到填「未公开」，**禁止编造**

---

## 第二步：生成 Markdown 文档

生成的 Markdown 必须包含以下六个章节：

```markdown
### 1.1 App Store 核心数据
| 产品 | 评分 | 评价数 | 分类 | 产品定位 |

### 1.2 产品运营数据
| 产品 | MAU | 营收/ARR | 估值/融资 | 日均时长 | 最新动态 |

### 1.3 市场规模背景
| 指标 | 数据 | 来源 |

### 3.1 全球市场格局
| 区域 | 主导产品 | 关键特征 |

### 4.3 市场机会
1. **机会点标题**：机会点描述
...

### 4.4 市场风险
1. **风险点标题**：风险点描述
...

### 5.1 产品策略建议
- 策略建议...

### 5.3 用户画像
| 画像 | 特征 | 方向 |
```

---

## 第三步：渲染 HTML/PDF 报告

直接调用生成脚本：

```bash
SKILL_DIR="/root/.openclaw/workspace/skills/ai-market-report"
TS=$(date +%Y%m%d%H%M%S)
MD="/root/.openclaw/workspace/myfiles/daily_report_data/files/AI陪伴软件调研日报_${TS}.md"
OUT="/root/.openclaw/workspace/myfiles/daily_report_data/files"

python3 "${SKILL_DIR}/scripts/generate_report.py" "$MD" "$OUT" "$TS"
```

**脚本自动完成**：
1. 解析 Markdown 中所有表格和结构化数据
2. 注入市场规模、MAU、下载量、营收、估值到 HTML
3. 生成 6 页精美报告（封面 → 核心数据 → 产品分析 → 中国市场 → 市场格局 → 策略建议 → 结尾）
4. WeasyPrint 渲染 A4 landscape PDF

---

## 第四步：复制到工作区（方便查看）

```bash
TS=$(date +%Y%m%d%H%M%S)
OUT="/root/.openclaw/workspace/myfiles/daily_report_data/files"
cp "${OUT}/AI_Report_${TS}.html" /root/.openclaw/workspace/
cp "${OUT}/AI_Report_${TS}.pdf"  /root/.openclaw/workspace/
```

---

## 报告章节说明

| 章节 | 内容 |
|------|------|
| 封面 | 报告日期、产品数量、数据来源 |
| 第一章 | 市场规模 2025/2026、CAGR、Character.AI 访问/下载、App Store 评分表、运营数据表 |
| 第二章 | 6 款头部产品深度卡片（Character.AI、Replika、PolyBuzz、Chai、Nomi、Talkie） |
| 第三章 | 中国市场：豆包 120M、猫箱、星野、海螺AI、小冰；全球区域格局；近期动态 |
| 第四章 | 全球市场格局、关键数据变化、市场机会 5 条、风险提示 4 条 |
| 第五章 | 产品策略建议、用户画像、优先市场（欧美/东南亚/中东南美）、推广策略 |
