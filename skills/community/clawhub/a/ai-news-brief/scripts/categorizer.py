#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资讯分类模块
按模块分类展示资讯
"""

import json


# 模块定义和关键词
MODULE_CONFIG = {
    "政策": {
        "keywords": ["政策", "通知", "公告", "意见", "方案", "规划", "纲要", "监管", "治理",
                    "国务院", "办公厅", "工信部", "科技部", "网信办", "发改委", "教育部",
                    "财政部", "办法", "规定", "实施细则", "工作方案", "AI治理"],
        "icon": "🔔",
        "priority": 1
    },
    "硬件": {
        "keywords": ["gpu", "nvidia", "amd", "intel", "cuda", "显卡", "显存", "RTX", "geforce",
                    "内存", "ddr5", "ddr4", "ddr6", "hbm", "gddr", "dram", "sram",
                    "存储", "固态", "ssd", "硬盘", "三星", "海力士", "美光",
                    "h100", "h200", "a100", "b100", "4090", "5080", "5090", "blackwell", "rubin",
                    "芯片", "半导体", "处理器", "cpu", "npu", "tpu"],
        "icon": "💻",
        "priority": 2
    },
    "市场": {
        "keywords": ["融资", "投资", "收购", "上市", "估值", "财报", "营收", "出货量",
                    "市场份额", "增长", "下降", "突破", "超过", "补贴", "专项资金",
                    "项目", "申报", "中标", "合作", "签约", "工厂", "产能"],
        "icon": "📈",
        "priority": 3
    },
    "行业": {
        "keywords": ["大模型", "gpt", "llm", "chatgpt", "openai", "claude", "gemini",
                    "deepseek", "模型", "训练", "推理", "部署", "参数", "token",
                    "AI模型", "语言模型", "多模态", "Sora", "视频生成",
                    "人工智能", "AI", "算法", "技术", "突破", "研究"],
        "icon": "🏛️",
        "priority": 4
    },
    "自动驾驶": {
        "keywords": ["自动驾驶", "智驾", "特斯拉", "fsd", "智驾", "无人驾驶",
                    "车载", "车机", "汽车", "电动车", "蔚来", "小鹏", "理想",
                    "比亚迪", "小米汽车", "华为车", "问界"],
        "icon": "🚗",
        "priority": 5
    }
}


def classify_article(title, summary=""):
    """
    根据标题和摘要对文章进行分类
    返回: 模块名称
    """
    text = (title + " " + (summary or "")).lower()
    
    # 按优先级顺序检查
    for module_name in ["政策", "硬件", "市场", "行业", "自动驾驶"]:
        config = MODULE_CONFIG[module_name]
        for keyword in config["keywords"]:
            if keyword.lower() in text:
                return module_name
    
    # 没有匹配到任何模块
    return "其他"


def categorize_articles(articles):
    """
    将文章列表按模块分类
    返回: {模块名: [文章列表], ...}
    """
    categorized = {
        "政策": [],
        "硬件": [],
        "市场": [],
        "行业": [],
        "自动驾驶": [],
        "其他": []
    }
    
    for article in articles:
        module = classify_article(
            article.get('title', ''),
            article.get('summary', '')
        )
        categorized[module].append(article)
    
    return categorized


def get_module_order():
    """获取模块显示顺序（按priority排序）"""
    modules = []
    for name, config in MODULE_CONFIG.items():
        modules.append((name, config["priority"], config["icon"]))
    modules.append(("其他", 99, "📋"))  # 其他放最后
    
    modules.sort(key=lambda x: x[1])
    return [(m[0], m[2]) for m in modules]


def generate_categorized_html(articles, date_range):
    """生成分模块的HTML报告"""
    categorized = categorize_articles(articles)
    module_order = get_module_order()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI资讯简报</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; 
               background: #f5f5f5; }}
        h1 {{ color: #1a73e8; border-bottom: 3px solid #1a73e8; padding-bottom: 15px; }}
        .info {{ background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .module {{ margin: 20px 0; }}
        .module h2 {{ color: #333; border-left: 5px solid #1a73e8; padding-left: 15px; 
                      background: white; padding: 10px 15px; border-radius: 8px; }}
        .article {{ background: white; border-radius: 8px; padding: 15px; margin: 10px 0; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .title {{ font-size: 16px; font-weight: bold; color: #1a73e8; }}
        .title a {{ color: inherit; text-decoration: none; }}
        .title a:hover {{ text-decoration: underline; }}
        .meta {{ font-size: 12px; color: #666; margin: 5px 0; }}
        .source {{ background: #e3f2fd; padding: 2px 8px; border-radius: 4px; }}
        .hot {{ background: #ea4335; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; }}
        .summary {{ color: #444; margin: 8px 0; font-size: 14px; }}
        .key-points {{ background: #e8f0fe; padding: 8px; border-radius: 4px; margin-top: 8px; }}
        .key-points li {{ font-size: 12px; color: #333; }}
        .cred-A {{ background: #34a853; color: white; }}
        .cred-B {{ background: #fbbc04; color: #333; }}
        .cred-C {{ background: #ea4335; color: white; }}
        .cred-D {{ background: #9e9e9e; color: white; }}
        .credibility {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 10px; }}
        .empty {{ color: #999; font-style: italic; padding: 20px; text-align: center; }}
    </style>
</head>
<body>
    <h1>🤖 AI 资讯简报</h1>
    <div class="info">
        <strong>📅 日期范围</strong>: {date_range}<br>
        <strong>📊 资讯总数</strong>: {len(articles)} 条
    </div>
"""
    
    # 按顺序生成各模块
    for module_name, icon in module_order:
        module_articles = categorized.get(module_name, [])
        
        if not module_articles:
            continue  # 跳过空的模块
        
        html += f'\n    <div class="module">\n'
        html += f'        <h2>{icon} {module_name} ({len(module_articles)}条)</h2>\n'
        
        for article in module_articles:
            title = article.get('title', '')
            url = article.get('url', '#')
            source = article.get('source', '')
            summary = article.get('summary', '')
            key_points = article.get('key_points', [])
            credibility = article.get('credibility', {})
            hot_score = article.get('hot_score', 0)
            
            level = credibility.get('level', 'D')
            
            html += f'''        <div class="article">
            <div class="title">
                <span class="hot">🔥{hot_score}</span>
                <a href="{url}" target="_blank">{title}</a>
            </div>
            <div class="meta">
                <span class="source">{source}</span>
                <span class="credibility cred-{level}">{level}</span>
            </div>
'''
            if summary and len(summary) > 10:
                html += f'            <div class="summary">{summary[:150]}...</div>\n'
            
            if key_points:
                html += '            <div class="key-points"><ul>\n'
                for kp in key_points[:2]:
                    html += f'                <li>{kp[:80]}</li>\n'
                html += '            </ul></div>\n'
            
            html += '        </div>\n'
        
        html += '    </div>\n'
    
    html += '''
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; 
                text-align: center; color: #666; font-size: 12px;">
        <p>🤖 由 AI 资讯简报自动生成</p>
    </div>
</body>
</html>'''
    
    return html


if __name__ == "__main__":
    # 测试
    test_articles = [
        {"title": "工信部发布AI新政策", "summary": "测试内容", "source": "36kr"},
        {"title": "NVIDIA发布RTX 5090", "summary": "显卡发布", "source": "驱动之家"},
        {"title": "某公司融资10亿", "summary": "融资新闻", "source": "36kr"},
        {"title": "GPT-5新模型发布", "summary": "大模型更新", "source": "量子位"},
    ]
    
    categorized = categorize_articles(test_articles)
    for module, articles in categorized.items():
        if articles:
            print(f"{module}: {len(articles)}条")