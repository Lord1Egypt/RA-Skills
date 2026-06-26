#!/usr/bin/env python3
"""
商业模式画布生成器
生成 Markdown 格式的商业模式画布
"""

def generate_canvas(data):
    """
    根据输入数据生成商业模式画布

    Args:
        data: 包含9大模块的字典

    Returns:
        Markdown 格式的画布文本
    """
    canvas = f"""# 商业模式画布

## 核心画布

```
┌─────────────────────────────────────────────────────────────────────┐
│                           价值主张                                  │
│  {data.get('value_proposition', '待填充')}                         │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────┤
│ 关键合作伙伴 │ 关键活动    │ 关键资源    │ 客户关系    │ 客户细分    │
│             │             │             │             │             │
│ {data.get('partners', '待填充')[:12]:<12} │ {data.get('activities', '待填充')[:12]:<12} │ {data.get('resources', '待填充')[:12]:<12} │ {data.get('relationships', '待填充')[:12]:<12} │ {data.get('segments', '待填充')[:12]:<12} │
├─────────────┴─────────────┼─────────────┼─────────────┴─────────────┤
│        成本结构           │          收入来源                       │
│  {data.get('costs', '待填充')[:24]:<24} │  {data.get('revenue', '待填充')[:24]:<24} │
└──────────────────────────┴──────────────────────────────────────────┘
```

## 详细说明

### 客户细分 (Customer Segments)
{data.get('segments', '待填充')}

### 价值主张 (Value Propositions)
{data.get('value_proposition', '待填充')}

### 渠道通路 (Channels)
{data.get('channels', '待填充')}

### 客户关系 (Customer Relationships)
{data.get('relationships', '待填充')}

### 收入来源 (Revenue Streams)
{data.get('revenue', '待填充')}

### 关键资源 (Key Resources)
{data.get('resources', '待填充')}

### 关键活动 (Key Activities)
{data.get('activities', '待填充')}

### 关键合作伙伴 (Key Partnerships)
{data.get('partners', '待填充')}

### 成本结构 (Cost Structure)
{data.get('costs', '待填充')}

---
*生成时间: {get_timestamp()}*
"""
    return canvas


def generate_comparison(models):
    """
    生成多模式对比表

    Args:
        models: 包含多个商业模式数据的列表

    Returns:
        Markdown 格式的对比表
    """
    comparison = """# 商业模式对比分析

| 维度 | """ + " | ".join([m.get('name', '模式'+str(i+1)) for i, m in enumerate(models)]) + """ |
|------|""" + "|".join(["------" for _ in models]) + """|
| 客户细分 | """ + " | ".join([m.get('segments', '-') for m in models]) + """ |
| 价值主张 | """ + " | ".join([m.get('value_proposition', '-') for m in models]) + """ |
| 收入模式 | """ + " | ".join([m.get('revenue', '-') for m in models]) + """ |
| 关键资源 | """ + " | ".join([m.get('resources', '-') for m in models]) + """ |
| 成本结构 | """ + " | ".join([m.get('costs', '-') for m in models]) + """ |
| 核心优势 | """ + " | ".join([m.get('advantage', '-') for m in models]) + """ |
| 主要风险 | """ + " | ".join([m.get('risk', '-') for m in models]) + """ |
"""
    return comparison


def get_timestamp():
    """获取当前时间戳"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 示例数据
if __name__ == "__main__":
    example_data = {
        "segments": "价格敏感型个人用户、专业创作者、团队/企业",
        "value_proposition": "云端存储与协作、跨设备同步、文件安全备份",
        "channels": "应用商店、SEO、口碑传播、企业销售",
        "relationships": "自助服务、社区支持、企业客户经理",
        "revenue": "个人订阅、企业订阅、存储扩容",
        "resources": "产品、服务器基础设施、用户数据、品牌",
        "activities": "产品开发、用户增长、转化优化、客户成功",
        "partners": "云服务商、支付渠道、推广平台",
        "costs": "研发人员、服务器带宽、营销获客"
    }

    print(generate_canvas(example_data))
