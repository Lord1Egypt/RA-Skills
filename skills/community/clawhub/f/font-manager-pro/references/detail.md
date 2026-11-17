# 详细参考 - font-manager-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (yaml)

```yaml
font_manager:
  version: "1.0"
  language: zh
  log_file: ~/font-manager.log

smart_pair:
  style: modern
  language: zh
  candidates:
    heading: ["Noto Serif SC", "Source Han Serif", "LXGW WenKai"]
    body: ["Noto Sans SC", "Source Han Sans", "Inter"]

subset:
  enabled: true
  charsets: [latin, latin-ext, zh-CN-common]
  output_format: woff2
  dynamic: true
  scan_pages: ["index.html", "about.html"]

design_system:
  enabled: true
  tokens_file: design-tokens.yaml
  sync_targets:
    - styles/typography.css
    - styles/variables.css
  audit: true

a11y:
  standard: WCAG-AA
  min_contrast_body: 4.5
  min_contrast_large: 3.0
  min_font_size: 16
  min_line_height: 1.4
  max_thin_weight: 400

i18n:
  languages: [zh-CN, en]
  auto_adjust: true
  zh_line_height: 1.7
  en_line_height: 1.6

cdn:
  strategy: multi-fallback
  primary: "https://cdn.example.com/fonts/"
  fallback:
    - "https://fonts.googleapis.com/"
    - "/fonts/local/"
  preload: ["heading-400", "body-400"]
  cache_max_age: 31536000

report:
  format: [html, pdf, json]
  output: ~/reports/typography/
  retention_days: 90
```

## 代码示例 (yaml)

```yaml
font_manager:
  version: "1.0"
  language: zh

smart_pair:
  style: modern
  language: zh
  heading_candidates: ["Playfair Display", "Noto Serif SC"]
  body_candidates: ["Inter", "Noto Sans SC"]

subset:
  enabled: true
  charsets:
    - latin
    - latin-ext
    - zh-CN-common  # 常用中文字符
  output_format: woff2

design_system:
  enabled: true
  tokens_file: design-tokens.json
  variables:
    --font-heading: "Noto Serif SC, serif"
    --font-body: "Noto Sans SC, sans-serif"
    --font-mono: "JetBrains Mono, monospace"

a11y:
  standard: WCAG-AA
  min_contrast: 4.5  # 正文最低对比度
  min_font_size: 16px
  check_line_height: true

cdn:
  primary: "https://cdn.example.com/fonts/"
  fallback:
    - "https://fonts.googleapis.com/"
    - "https://fonts.gstatic.com/"
  preload: ["heading-400", "body-400", "body-700"]

report:
  format: [html, pdf]
  output: ~/reports/typography/
```

## 代码示例 (yaml)

```yaml
tokens:
  font_family:
    heading: "Noto Serif SC, serif"
    body: "Noto Sans SC, sans-serif"
    mono: "JetBrains Mono, monospace"

  font_size:
    xs: 0.75rem    # 12px
    sm: 0.875rem   # 14px
    base: 1rem     # 16px
    lg: 1.125rem   # 18px
    xl: 1.25rem    # 20px
    2xl: 1.5rem    # 24px
    3xl: 1.875rem  # 30px
    4xl: 2.25rem   # 36px
  font_weight:
    regular: 400
    medium: 500
    semibold: 600
    bold: 700

  line_height:
    tight: 1.2
    normal: 1.5
    relaxed: 1.625

  letter_spacing:
    tighter: -0.05em
    normal: 0
    wide: 0.05em
    wider: 0.1em
```

## 代码示例 (yaml)

```yaml
tokens:
  font_family:
    heading: "Noto Serif SC, serif"
    body: "Noto Sans SC, sans-serif"
    mono: "JetBrains Mono, monospace"

  font_size:
    xs: 0.75rem
    sm: 0.875rem
    base: 1rem
    lg: 1.125rem
    xl: 1.25rem
    2xl: 1.5rem
    3xl: 1.875rem
    4xl: 2.25rem

  font_weight:
    regular: 400
    medium: 500
    semibold: 600
    bold: 700

  line_height:
    tight: 1.2
    normal: 1.6
    relaxed: 1.7  # 中文行高
  letter_spacing:
    tighter: -0.05em
    normal: 0
    wide: 0.05em
```

## 代码示例 (text)

```text
┌─────────────────────────────────────────────────────┐
│              字体管理专业版架构                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐   │
│  │  智能配对     │  │  子集化工具   │  │ 设计系统 │   │
│  │  Smart Pair │  │  Subset    │  │ DesignSys│   │
│  │              │  │              │  │          │   │
│  │ 特征分析     │  │ 自动子集     │  │ 变量联动 │   │
│  │ 最佳推荐     │  │ 字符裁剪     │  │ 主题管理 │   │
│  └──────────────┘  └──────────────┘  └──────────┘   │
│         │                │                │          │
│         └────────────────┼────────────────┘          │
│                          ▼                           │
│                  ┌──────────────┐                    │
│                  │  无障碍检查   │  ← WCAG对比度      │
│                  │  A11y Check │    字号合规         │
│                  └──────────────┘                    │
│                          │                           │
│           ┌──────────────┼──────────────┐            │
│           ▼              ▼              ▼            │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│    │ 多语言适配│  │ CDN优化  │  │ 审计报告 │         │
│    │ CJK     │  │ Multi-CDN│  │ Report   │         │
│    │ 中日韩   │  │ Fallback │  │ PDF/HTML │         │
│    └──────────┘  └──────────┘  └──────────┘         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

