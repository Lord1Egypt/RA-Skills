# content-card 用户偏好配置

## 文件位置（优先级从高到低）

| 优先级 | 路径 | 范围 |
|--------|------|------|
| 1 | `.content-card/EXTEND.md` | 项目级 |
| 2 | `~/.config/content-card/EXTEND.md` | 用户级 |

## 支持的配置项

```yaml
# EXTEND.md 示例
default_style: morandi-warm          # 默认风格
default_layout: bento-grid           # 默认布局（仅 -i 模式）
default_aspect: portrait             # 默认比例：portrait / landscape / square
lang: zh                             # 默认语言
font_override:                       # 字体覆盖
  heading: "Noto Serif SC"
  body: "Noto Sans SC"
color_override:                      # 颜色覆盖（覆盖 style 默认值）
  accent: "#D4442A"
custom_footer: "© 2026 Your Name"         # 自定义页脚文字
```

## 规则
- 配置项都是可选的，缺失使用 SKILL.md 中的默认值
- `--style` / `--layout` 命令行参数优先级高于 EXTEND.md
- 首次使用时如果没有找到 EXTEND.md，不阻塞流程，使用默认值
