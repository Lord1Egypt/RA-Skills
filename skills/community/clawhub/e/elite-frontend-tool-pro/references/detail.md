# 详细参考 - elite-frontend-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import json
from pathlib import Path

class DesignSystemGenerator:
    """设计系统生成器"""

    def __init__(self, brand_config):
        self.brand = brand_config

    def generate_tokens(self):
        """生成完整 Design Token"""
        return {
            "color": self._generate_color_tokens(),
            "typography": self._generate_typography_tokens(),
            "spacing": self._generate_spacing_tokens(),
            "radius": self._generate_radius_tokens(),
            "shadow": self._generate_shadow_tokens(),
            "motion": self._generate_motion_tokens(),
        }

    def _generate_color_tokens(self):
        return {
            "primary": {
                "bg": self.brand["colors"]["primary"],
                "bgSecondary": self.brand["colors"]["secondary"],
                "accent": self.brand["colors"]["accent"],
            },
            "text": {
                "primary": "#eeeeee",
                "muted": "#8892b0",
                "inverse": "#1a1a2e",
            },
            "semantic": {
                "success": "#50fa7b",
                "warning": "#f1fa8c",
                "error": "#ff5555",
                "info": "#8be9fd",
            }
        }

    def _generate_typography_tokens(self):
        return {
            "fontFamily": {
                "heading": self.brand["typography"]["heading"],
                "body": self.brand["typography"]["body"],
                "mono": self.brand["typography"]["mono"],
            },
            "fontSize": {
                "xs": "0.75rem", "sm": "0.875rem",
                "base": "1rem", "lg": "1.125rem",
                "xl": "1.25rem", "2xl": "1.5rem",
                "3xl": "2rem", "4xl": "2.5rem",
                "5xl": "3.5rem", "6xl": "4.5rem",
            },
            "fontWeight": {
                "thin": 100, "light": 300,
                "normal": 400, "medium": 500,
                "semibold": 600, "bold": 700,
                "extrabold": 800, "black": 900,
            },
            "lineHeight": {
                "tight": 1.1, "snug": 1.3,
                "normal": 1.5, "relaxed": 1.7,
            }
        }

    def _generate_spacing_tokens(self):
        base = 4
        return {f"s{i}": f"{base * i}px" for i in range(17)}

    def _generate_radius_tokens(self):
        return {"none": "0", "sm": "4px", "md": "8px",
                "lg": "12px", "xl": "16px", "full": "9999px"}

    def _generate_shadow_tokens(self):
        return {
            "sm": "0 1px 2px rgba(0,0,0,0.1)",
            "md": "0 4px 6px rgba(0,0,0,0.15)",
            "lg": "0 10px 25px rgba(0,0,0,0.2)",
            "glow": f"0 0 20px {self.brand['colors']['accent']}40",
        }

    def _generate_motion_tokens(self):
        return {
            "duration": {"fast": "0.2s", "normal": "0.4s", "slow": "0.6s"},
            "easing": {
                "easeOut": "cubic-bezier(0.22, 1, 0.36, 1)",
                "spring": "cubic-bezier(0.34, 1.56, 0.64, 1)",
            },
            "stagger": {"fast": 0.05, "normal": 0.1, "slow": 0.15},
        }

    def export(self, format="json"):
        """导出设计系统"""
        tokens = self.generate_tokens()
        if format == "json":
            return json.dumps(tokens, indent=2, ensure_ascii=False)
        elif format == "css":
            return self._to_css_variables(tokens)

    def _to_css_variables(self, tokens):
        lines = [":root {"]
        for category, values in tokens.items():
            for name, value in self._flatten(values).items():
                lines.append(f"  --{category}-{name}: {value};")
        lines.append("}")
        return "\n".join(lines)

    def _flatten(self, d, parent=""):
        items = {}
        for k, v in d.items():
            key = f"{parent}-{k}" if parent else k
            if isinstance(v, dict):
                items.update(self._flatten(v, key))
            else:
                items[key] = v
        return items

brand = {
    "colors": {"primary": "#1a1a2e", "secondary": "#16213e", "accent": "#e94560"},
    "typography": {"heading": "Playfair Display", "body": "IBM Plex Sans", "mono": "JetBrains Mono"},
}
generator = DesignSystemGenerator(brand)
print(generator.export("css"))
```

## 代码示例 (tsx)

```tsx
// React + TypeScript + Framer Motion 组件示例
import { motion } from 'framer-motion';
import { DesignToken } from './design-system';

// 设计令牌
export const token: DesignToken = {
  color: {
    bgPrimary: '#1a1a2e',
    bgSecondary: '#16213e',
    accent: '#e94560',
    accentAlt: '#0f3460',
    text: '#eeeeee',
    textMuted: '#8892b0',
  },
  typography: {
    heading: { family: 'Playfair Display', weights: [400, 900] },
    body: { family: 'IBM Plex Sans', weights: [300, 400, 600] },
    mono: { family: 'JetBrains Mono', weights: [400] },
  },
  spacing: { base: 4, scale: [0, 4, 8, 12, 16, 24, 32, 48, 64] },
  radius: { sm: 4, md: 8, lg: 12, full: 9999 },
};

// 带交错动效的卡片组件
interface CardProps {
  title: string;
  children: React.ReactNode;
  delay?: number;
}

export function Card({ title, children, delay = 0 }: CardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -4 }}
      style={{
        background: token.color.bgSecondary,
        border: `1px solid ${token.color.accent}33`,
        borderRadius: token.radius.lg,
        padding: token.spacing.scale[5],
      }}
    >
      <h3 style={{
        fontFamily: token.typography.heading.family,
        fontWeight: 900,
        fontSize: '1.5rem',
        marginBottom: token.spacing.scale[3],
      }}>{title}</h3>
      <div style={{ color: token.color.textMuted }}>{children}</div>
    </motion.div>
  );
}

// 页面级交错动效容器
export function StaggerContainer({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.1 } },
      }}
    >
      {children}
    </motion.div>
  );
}
```

