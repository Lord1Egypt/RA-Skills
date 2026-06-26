# RenderCV Theme Presets

Five built-in themes are tuned to mimic RenderCV's visual language, not just its color palette. Each preset has its own header composition, section treatment, date column placement, and spacing density.

## Classic

- Reference: RenderCV `classic`
- Look: centered name, blue section rules, balanced two-column entries
- Best for: 通用型岗位、产品/研发、需要稳重但不老气的简历
- Signature details:
  - centered blue masthead
  - section titles with horizontal rule
  - right-aligned date column
  - sans-serif hierarchy with crisp blue accents

## ModernCV

- Reference: RenderCV `moderncv`
- Look: left-aligned serif masthead, thick blue bar before every section title, dates in the left column
- Best for: 技术岗、研究岗、希望简历更像出版物版式的候选人
- Signature details:
  - left-aligned name and connection line
  - section heading starts with a solid blue bar
  - content block indents after the bar
  - dates appear in a dedicated left rail

## Sb2nov

- Reference: RenderCV `sb2nov`
- Look: centered black serif name, academic typography, italic metadata
- Best for: 学术申请、研究工程师、偏论文/项目成果导向的简历
- Signature details:
  - centered serif masthead with bullet separators
  - thin black section rules
  - company/school secondary line in italics
  - right column uses stacked location/date styling

## Engineering Classic

- Reference: RenderCV `engineeringclassic`
- Look: lighter blue accents, left-aligned technical resume layout, tighter than Classic
- Best for: 后端/基础设施/平台工程师，想保留传统工程简历感的人
- Signature details:
  - left-aligned name and contacts
  - light-blue section rules
  - right-side date column
  - compact sans-serif rhythm with engineering-document feel

## Engineering Resumes

- Reference: RenderCV `engineeringresumes`
- Look: compact black serif layout, center masthead, dense but orderly content packing
- Best for: 需要在一页内容里塞入更多项目/经历的工程师
- Signature details:
  - centered serif masthead with `|` separators
  - black section rules and compact spacing
  - right-aligned date column
  - tighter bullets and reduced vertical whitespace

## Usage

Use the renderer directly for previews and final output:

```bash
python3 scripts/render_html.py resume_data.yaml output.html classic
python3 scripts/render_html.py resume_data.yaml output.html modern
python3 scripts/render_html.py resume_data.yaml output.html sb2nov
python3 scripts/render_html.py resume_data.yaml output.html engineeringclassic
python3 scripts/render_html.py resume_data.yaml output.html engineeringresumes
```
