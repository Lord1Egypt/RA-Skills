---
name: color-toolkit
data_dir: ../.standardization/color-toolkit/
license: MIT
description: 专业颜色工具集，支持颜色编码转换、对比度计算、智能颜色推荐、HTML预览生成。适用于UI设计、无障碍开发、配色方案生成等场景。
author: wUwproject
version: 1.1.0
tags: ['color', 'color-conversion', 'contrast', 'accessibility', 'design', 'wcag']
trigger: ['颜色转换', '对比度计算', '颜色推荐', '配色方案', '色彩空间', 'HEX.*RGB', 'HSL', 'HSV', 'CMYK', '色差', 'WCAG']
trigger_negative: ['不触发', '不需要颜色工具', '与其他无关']
sensitive_access: false
critical_write: false
permission_weight: LOW
external_data_dir: true
meta_field_sync: true
faq_unparsable: reformat
---
# Color Toolkit - 专业颜色工具集

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 渐进式文件索引

| 文件 | 说明 |
|------|------|
| `references/examples.md` | 输出格式示例 |
| `references/faq.md` | 常见问题 |
| `references/antipatterns.md` | 反模式与注意事项 |
| `references/changelog.md` | 更新日志 |

Color Toolkit 是一个通用的颜色处理工具包，提供：
- **颜色编码转换**：HEX ↔ RGB ↔ HSL ↔ HSV ↔ CMYK 全支持
- **对比度计算**：WCAG 2.1、APCA、CIELAB ΔE*ab、CIEDE2000 四种算法
- **智能颜色推荐**：根据用户描述生成配色方案
- **HTML预览生成**：实时预览颜色效果

## 触发场景
**正向触发（满足以下任意一条）：**
- 用户需要颜色转换、对比度计算或配色方案

**否定条件（满足以下任意一条，不触发）：**
- 简单问答、闲聊、问候（不需要本技能）
- 单步任务（不需要结构化执行）

## 核心功能

### 1. 颜色编码转换

```
输入格式支持：
- HEX: #FF5733, #F53
- RGB: rgb(255, 87, 51), 255, 87, 51
- HSL: hsl(11, 100%, 60%), 11, 100, 60
- HSV: 11, 100, 60
- CMYK: 0, 66, 100, 0

输出格式：
- HEX: #FF5733
- RGB: RGB(r=255, g=87, b=51)
- HSL: HSL(h=11.0, s=100.0, l=60.0)
- HSV: HSV(h=11, s=100, v=60)
- CMYK: CMYK(c=0, m=66, y=100, k=0)
```

### 2. 对比度计算（四种算法）

| 算法 | 用途 | 评估标准 |
|------|------|----------|
| WCAG 2.1 | 无障碍标准 | ≥4.5:1 (AA) / ≥7:1 (AAA) |
| APCA | 现代对比度 | ≥45 Lc (可读) / ≥75 Lc (优秀) |
| CIELAB ΔE*ab | 精确色差 | ≤2 (不可辨) / ≤10 (微小) |
| CIEDE2000 | 专业色差 | ≤1 (完美) / ≤2 (接近) |

### 3. 智能颜色推荐

**输入**：用户描述（中文/英文）
**处理**：LLM解析语义 → 提取关键词 → 映射到色彩空间
**输出**：
- 主色（1个）
- 辅助色（2-3个）
- 强调色（1个）
- 背景/文字色建议

### 4. HTML预览生成

生成的HTML包含：
- 颜色色块展示
- 渐变效果预览
- 对比度示例
- 文本可读性测试
- 无障碍合规提示

## 使用方式

### 方式一：直接对话（推荐）

```
用户：请帮我转换颜色 #3498db 到所有格式
用户：计算 #000000 和 #ffffff 的对比度
用户：推荐一套科技感的配色方案
用户：生成这个颜色的预览页面
```

### 方式二：AI 对话

直接描述需求即可，无需命令行操作。AI 会自动调用颜色转换、对比度计算等核心功能。

## 输出格式

### 颜色转换结果示例

> 输出格式详情 → 详见 `references/examples.md`

### 对比度计算结果示例

> 输出格式详情 → 详见 `references/examples.md`

### 颜色推荐结果示例

> 输出格式详情 → 详见 `references/examples.md`

## 技术实现

### 依赖
- Python 3.8+
- 仅使用标准库（math, re, random, dataclasses, typing）

### 文件结构

```
color-toolkit/
├── SKILL.md              # 本技能文档
└── references/           # 渐进式文档
    ├── examples.md       # 输出格式示例
    ├── faq.md            # 常见问题
    ├── antipatterns.md   # 反模式
    └── changelog.md      # 更新日志
```

## 使用限制

| 约束项 | 说明 |
|--------|------|
| **输入范围** | HEX 支持 3/6 位格式；RGB 值自动裁剪 0-255；HSL/HSV 角度 0-360 |
| **性能** | 颜色转换无外部依赖，毫秒级响应 |
| **环境要求** | Python ≥ 3.8，仅标准库，无额外依赖 |

> 常见使用误区 → 详见 [反模式](references/antipatterns.md)

## 示例对话

```
用户：#FF5733 是什么颜色？
助手：
- **HEX**: #FF5733
- **RGB**: RGB(r=255, g=87, b=51)
- **HSL**: HSL(h=11, s=100%, l=60%)
- **色系**: 暖色 / 橙红系
- **亮度**: 0.384（较高）
- **预览**: [生成HTML预览]

用户：计算这个颜色和白色的对比度
助手：
- **WCAG 2.1**: 3.97:1 (大文本AA级) ⚠️
- **APCA**: 58.2 Lc (良好)
- **结论**: 小文本可能不符合AA标准，建议增加对比度

用户：给我一套春天主题的配色
助手：
- **主色**: #4CAF50 (生机绿)
- **辅助**: #E8F5E9 (浅芽绿), #FF9800 (迎春黄)
- **强调**: #E91E63 (桃花粉)
- **预览**: [生成春意盎然的HTML预览]
```

> 详见 [反模式](references/antipatterns.md)

> 详见 [FAQ](references/faq.md)
