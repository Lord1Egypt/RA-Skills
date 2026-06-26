#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
Flexible color schemes for doc2slides.
Each scheme defines: background, card, text colors, accent colors.
"""

# 预定义配色方案
COLOR_SCHEMES = {
    # 商务蓝黑（默认）
    "corporate": {
        "name": "商务蓝黑",
        "description": "McKinsey/BCG 风格，适合商务报告、财务分析",
        "background": "#0B1221",
        "card": "#1A2332",
        "text_primary": "#FFFFFF",
        "text_secondary": "#94A3B8",
        "accent": ["#F59E0B", "#EA580C", "#10B981", "#3B82F6"],
        "grid_stroke": "#4B5563",
    },
    
    # 科技感
    "tech": {
        "name": "科技感",
        "description": "适合科技产品、互联网公司、AI/ML 主题",
        "background": "#0F172A",
        "card": "#1E293B",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "accent": ["#06B6D4", "#8B5CF6", "#EC4899", "#10B981"],
        "grid_stroke": "#334155",
    },
    
    # 清新绿
    "nature": {
        "name": "清新绿",
        "description": "适合环保、健康、生活方式主题",
        "background": "#F0FDF4",
        "card": "#FFFFFF",
        "text_primary": "#166534",
        "text_secondary": "#6B7280",
        "accent": ["#10B981", "#059669", "#34D399", "#FBBF24"],
        "grid_stroke": "#D1D5DB",
    },
    
    # 温暖橙
    "warm": {
        "name": "温暖橙",
        "description": "适合教育、公益、社区主题",
        "background": "#FFF7ED",
        "card": "#FFFFFF",
        "text_primary": "#7C2D12",
        "text_secondary": "#78716C",
        "accent": ["#F97316", "#EA580C", "#FBBF24", "#EF4444"],
        "grid_stroke": "#E5E7EB",
    },
    
    # 极简白
    "minimal": {
        "name": "极简白",
        "description": "适合学术报告、研究论文、简洁展示",
        "background": "#FFFFFF",
        "card": "#F9FAFB",
        "text_primary": "#111827",
        "text_secondary": "#6B7280",
        "accent": ["#3B82F6", "#1D4ED8", "#60A5FA", "#93C5FD"],
        "grid_stroke": "#E5E7EB",
    },
    
    # 深紫
    "dark_purple": {
        "name": "深紫",
        "description": "适合创意、设计、品牌展示",
        "background": "#1E1B4B",
        "card": "#312E81",
        "text_primary": "#F5F3FF",
        "text_secondary": "#A5B4FC",
        "accent": ["#8B5CF6", "#A78BFA", "#C4B5FD", "#F472B6"],
        "grid_stroke": "#4C1D95",
    },
    
    # 金融红
    "finance": {
        "name": "金融红",
        "description": "适合金融、投资、银行业",
        "background": "#FEF2F2",
        "card": "#FFFFFF",
        "text_primary": "#7F1D1D",
        "text_secondary": "#6B7280",
        "accent": ["#DC2626", "#B91C1C", "#EF4444", "#F97316"],
        "grid_stroke": "#FCA5A5",
    },
    
    # 高端深蓝
    "executive": {
        "name": "高端深蓝",
        "description": "适合高管汇报、董事会演示",
        "background": "#0A1628",
        "card": "#132040",
        "text_primary": "#F1F5F9",
        "text_secondary": "#8B9DC3",
        "accent": ["#FFB800", "#FF6B35", "#00D4AA", "#4C8BF5"],
        "grid_stroke": "#1E3A5F",
    },
    
    # 现代浅灰
    "modern_light": {
        "name": "现代浅灰",
        "description": "适合 SaaS 产品、初创公司、科技汇报",
        "background": "#F8FAFC",
        "card": "#FFFFFF",
        "text_primary": "#0F172A",
        "text_secondary": "#64748B",
        "accent": ["#6366F1", "#8B5CF6", "#EC4899", "#14B8A6"],
        "grid_stroke": "#E2E8F0",
    },
    
    # 暗夜绿
    "dark_green": {
        "name": "暗夜绿",
        "description": "适合可持续发展、新能源、环保科技",
        "background": "#0C1A14",
        "card": "#162B20",
        "text_primary": "#ECFDF5",
        "text_secondary": "#86EFAC",
        "accent": ["#22C55E", "#4ADE80", "#FACC15", "#38BDF8"],
        "grid_stroke": "#1E3A2E",
    },
}


def get_color_scheme(style: str = None, theme: str = None) -> dict:
    """
    Get color scheme based on style name or document theme.
    
    Args:
        style: Explicit style name (e.g., "tech", "nature")
        theme: Document theme/industry (e.g., "AI", "finance", "health")
    
    Returns:
        Color scheme dict
    """
    # 1. 如果明确指定了 style，直接返回
    if style and style in COLOR_SCHEMES:
        return COLOR_SCHEMES[style]
    
    # 2. 根据主题关键词匹配
    if theme:
        theme_lower = theme.lower()
        
        # 主题映射
        theme_mapping = {
            # 科技类
            "ai": "tech",
            "ml": "tech",
            "人工智能": "tech",
            "科技": "tech",
            "互联网": "tech",
            "软件": "tech",
            "saas": "modern_light",
            "初创": "modern_light",
            
            # 商务类
            "商务": "corporate",
            "咨询": "corporate",
            "战略": "corporate",
            "管理": "corporate",
            "高管": "executive",
            "董事会": "executive",
            
            # 金融类
            "金融": "finance",
            "投资": "finance",
            "银行": "finance",
            "理财": "finance",
            "基金": "finance",
            
            # 健康/环保
            "健康": "nature",
            "医疗": "nature",
            "环保": "dark_green",
            "绿色": "dark_green",
            "能源": "dark_green",
            "可持续发展": "dark_green",
            
            # 教育/公益
            "教育": "warm",
            "培训": "warm",
            "公益": "warm",
            "社区": "warm",
            
            # 学术
            "学术": "minimal",
            "论文": "minimal",
            "研究": "minimal",
            
            # 创意
            "创意": "dark_purple",
            "设计": "dark_purple",
            "品牌": "dark_purple",
        }
        
        for keyword, scheme_name in theme_mapping.items():
            if keyword in theme_lower:
                return COLOR_SCHEMES[scheme_name]
    
    # 3. 默认返回商务风格
    return COLOR_SCHEMES["corporate"]


def apply_colors_to_prompt(prompt: str, scheme: dict) -> str:
    """
    Apply color scheme to prompt template.
    
    Replaces fixed color values with scheme-specific values.
    """
    # 构建配色方案说明
    color_section = f"""
## 配色方案：{scheme['name']}
{scheme['description']}

### 颜色值
- 背景：{scheme['background']}
- 卡片：{scheme['card']}
- 主文字：{scheme['text_primary']}
- 次要文字：{scheme['text_secondary']}
- 强调色：{', '.join(scheme['accent'])}
- 网格线：{scheme['grid_stroke']}
"""
    
    # 替换 prompt 中的配色方案部分
    if "### 配色方案" in prompt:
        # 找到配色方案部分并替换
        lines = prompt.split('\n')
        new_lines = []
        in_color_section = False
        
        for line in lines:
            if line.startswith("### 配色方案"):
                in_color_section = True
                new_lines.append(color_section)
                continue
            
            if in_color_section and line.startswith("### "):
                in_color_section = False
            
            if not in_color_section:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    else:
        # 在设计规范部分添加配色方案
        return prompt.replace(
            "## 设计规范",
            f"## 设计规范\n{color_section}"
        )


if __name__ == "__main__":
    # 测试
    print("配色方案列表：")
    for name, scheme in COLOR_SCHEMES.items():
        print(f"  {name}: {scheme['name']} - {scheme['description']}")
    
    print("\n主题匹配测试：")
    test_themes = ["AI产品介绍", "金融行业报告", "健康生活方式", "学术论文"]
    for theme in test_themes:
        scheme = get_color_scheme(theme=theme)
        print(f"  {theme} → {scheme['name']}")
