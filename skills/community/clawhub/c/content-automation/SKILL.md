---
name: content-automation
description: 内容创作自动化工具 Skill。支持社交媒体内容生成、视频脚本创作、定时发布任务管理。当用户需要批量生成内容、自动化社交媒体运营或创建视频脚本时触发。
version: 1.0.0
---

# Content Automation Skill

内容创作自动化工具，帮助创作者和运营人员提高效率。支持社交媒体内容生成、视频脚本创作、定时任务管理等功能。

**注意**：本 Skill 专注于**内容创作辅助**，用户需遵守各平台的使用条款和社区规范。

## 前置要求

```bash
# 克隆仓库
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
cd MoneyPrinterV2

# 需要 Python 3.12+
python --version

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp config.example.json config.json
```

## 配置

编辑 `config.json`：

```json
{
  "openai_api_key": "your-key",
  "twitter": {
    "enabled": false,
    "username": "",
    "password": "",
    "email": ""
  },
  "youtube": {
    "enabled": false,
    "client_secrets_file": "client_secrets.json"
  },
  "affiliate": {
    "enabled": false,
    "amazon_tag": ""
  }
}
```

## 核心功能

### 1. 内容生成器

```python
from src.classes.ContentGenerator import ContentGenerator

# 初始化生成器
generator = ContentGenerator()

# 生成社交媒体帖子
post = generator.generate_post(
    topic="人工智能趋势",
    platform="twitter",
    tone="professional",
    length="short"
)
print(post)

# 生成视频脚本
script = generator.generate_video_script(
    topic="如何学习编程",
    duration_seconds=60,
    style="educational"
)
print(script)

# 生成内容创意
ideas = generator.generate_content_ideas(
    niche="科技评测",
    count=10
)
for idea in ideas:
    print(f"- {idea}")
```

### 2. 视频创作辅助

```bash
# 生成短视频脚本
python -c "
from src.classes.VideoGenerator import VideoGenerator

vg = VideoGenerator()
script = vg.generate_script(
    topic='5个Python技巧',
    style='fast-paced',
    duration=60
)
print(script)
"

# 生成视频描述和标签
python -c "
from src.classes.VideoGenerator import VideoGenerator

vg = VideoGenerator()
metadata = vg.generate_metadata(
    title='Python编程入门',
    keywords=['python', 'programming', 'tutorial']
)
print(f'描述: {metadata[\"description\"]}')
print(f'标签: {metadata[\"tags\"]}')
"
```

### 3. 定时任务调度

```python
from src.classes.Scheduler import Scheduler
from datetime import datetime, timedelta

# 创建调度器
scheduler = Scheduler()

# 添加定时发布任务
scheduler.add_job(
    func=post_to_twitter,
    trigger='cron',
    hour=9,
    minute=0,
    args=["早安推文内容"]
)

# 添加延时任务
scheduler.add_job(
    func=generate_daily_content,
    trigger='date',
    run_date=datetime.now() + timedelta(hours=2)
)

# 启动调度器
scheduler.start()
```

### 4. 内容日历管理

```python
from src.classes.ContentCalendar import ContentCalendar

# 创建内容日历
calendar = ContentCalendar()

# 添加内容计划
calendar.add_content(
    date="2024-03-25",
    platform="twitter",
    topic="产品发布",
    status="planned"
)

# 查看本周计划
weekly_plan = calendar.get_weekly_plan()
for item in weekly_plan:
    print(f"{item['date']}: {item['topic']} ({item['platform']})")

# 导出日历
calendar.export_to_csv("content_calendar.csv")
```

## 完整工作流示例

### 批量生成一周社交媒体内容

```python
#!/usr/bin/env python3
"""
批量生成一周社交媒体内容
"""

from src.classes.ContentGenerator import ContentGenerator
from src.classes.ContentCalendar import ContentCalendar
import json

def generate_weekly_content(niche: str, platforms: list):
    """为指定领域生成一周内容"""
    
    generator = ContentGenerator()
    calendar = ContentCalendar()
    
    # 内容主题池
    topics = [
        "周一灵感",
        "周二技巧",
        "周三案例",
        "周四趋势",
        "周五总结",
        "周末轻松话题"
    ]
    
    content_plan = []
    
    for i, topic in enumerate(topics):
        for platform in platforms:
            # 生成内容
            content = generator.generate_post(
                topic=f"{niche} - {topic}",
                platform=platform,
                tone="casual" if i >= 5 else "professional"
            )
            
            # 添加到日历
            calendar.add_content(
                day=i,
                platform=platform,
                content=content,
                topic=topic
            )
            
            content_plan.append({
                "day": i,
                "platform": platform,
                "topic": topic,
                "content": content
            })
    
    # 保存计划
    with open("weekly_content.json", "w", encoding="utf-8") as f:
        json.dump(content_plan, f, ensure_ascii=False, indent=2)
    
    # 导出日历
    calendar.export_to_csv("weekly_calendar.csv")
    
    print(f"✅ 已生成 {len(content_plan)} 条内容")
    print(f"📅 日历已保存至 weekly_calendar.csv")
    print(f"📝 详细计划已保存至 weekly_content.json")
    
    return content_plan

# 执行
if __name__ == "__main__":
    generate_weekly_content(
        niche="人工智能",
        platforms=["twitter", "linkedin"]
    )
```

### 视频内容生产线

```python
#!/usr/bin/env python3
"""
视频内容自动化生产流程
"""

from src.classes.VideoGenerator import VideoGenerator
from src.classes.ContentGenerator import ContentGenerator
import os

def create_video_pipeline(topic: str, output_dir: str = "./output"):
    """创建完整视频制作流程"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    vg = VideoGenerator()
    cg = ContentGenerator()
    
    print(f"🎬 开始制作视频: {topic}")
    
    # 1. 生成脚本
    print("📝 生成脚本...")
    script = vg.generate_script(
        topic=topic,
        style="educational",
        duration=90
    )
    
    with open(f"{output_dir}/script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    
    # 2. 生成视频描述
    print("📄 生成视频描述...")
    metadata = vg.generate_metadata(
        title=topic,
        keywords=["教程", "教育", topic]
    )
    
    with open(f"{output_dir}/metadata.json", "w", encoding="utf-8") as f:
        import json
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # 3. 生成缩略图描述
    print("🎨 生成缩略图创意...")
    thumbnail_ideas = cg.generate_content_ideas(
        niche=f"视频缩略图: {topic}",
        count=3
    )
    
    with open(f"{output_dir}/thumbnail_ideas.txt", "w", encoding="utf-8") as f:
        for idea in thumbnail_ideas:
            f.write(f"- {idea}\n")
    
    print(f"✅ 视频制作素材已保存至 {output_dir}/")
    print(f"   - 脚本: script.txt")
    print(f"   - 元数据: metadata.json")
    print(f"   - 缩略图创意: thumbnail_ideas.txt")
    
    return {
        "script": script,
        "metadata": metadata,
        "thumbnail_ideas": thumbnail_ideas
    }

# 执行
if __name__ == "__main__":
    create_video_pipeline("Python异步编程入门")
```

### 内容分析与优化

```python
#!/usr/bin/env python3
"""
分析内容表现并生成优化建议
"""

from src.classes.Analytics import Analytics
from src.classes.ContentGenerator import ContentGenerator

def analyze_and_optimize(content_history: list):
    """分析历史内容表现并生成优化建议"""
    
    analytics = Analytics()
    generator = ContentGenerator()
    
    # 分析表现
    print("📊 分析内容表现...")
    insights = analytics.analyze_performance(content_history)
    
    print("\n🔍 关键洞察:")
    print(f"  最佳发布时间: {insights['best_posting_time']}")
    print(f"  高互动话题: {', '.join(insights['top_topics'])}")
    print(f"  最佳内容长度: {insights['optimal_length']}")
    
    # 生成优化建议
    print("\n💡 优化建议:")
    recommendations = generator.generate_recommendations(insights)
    for rec in recommendations:
        print(f"  - {rec}")
    
    # 生成下周期内容策略
    print("\n📅 下周期内容策略:")
    strategy = generator.generate_content_strategy(
        insights=insights,
        timeframe="下周"
    )
    print(strategy)
    
    return insights, recommendations

# 示例数据
sample_history = [
    {"topic": "AI趋势", "engagement": 150, "posted_at": "09:00"},
    {"topic": "编程技巧", "engagement": 230, "posted_at": "14:00"},
    {"topic": "行业新闻", "engagement": 89, "posted_at": "18:00"},
]

analyze_and_optimize(sample_history)
```

## 高级功能

### 批量脚本执行

项目提供了一系列便捷脚本：

```bash
# 从项目根目录运行

# 上传视频
bash scripts/upload_video.sh /path/to/video.mp4 "视频标题"

# 批量生成内容
bash scripts/generate_batch.sh topics.txt

# 发布定时内容
bash scripts/scheduled_post.sh
```

### 自定义内容模板

```python
from src.classes.TemplateManager import TemplateManager

# 创建模板管理器
tm = TemplateManager()

# 注册自定义模板
tm.register_template(
    name="product_launch",
    template="""
    🚀 新品发布！
    
    {product_name} 现已上线！
    
    ✨ 核心功能:
    {features}
    
    🎯 适合人群: {target_audience}
    
    了解更多: {link}
    """
)

# 使用模板生成内容
content = tm.render_template(
    "product_launch",
    product_name="AI助手Pro",
    features="- 智能回复\n- 多语言支持\n- 数据分析",
    target_audience="内容创作者",
    link="https://example.com"
)
print(content)
```

### 多平台内容适配

```python
from src.classes.ContentAdapter import ContentAdapter

# 创建适配器
adapter = ContentAdapter()

# 原始内容
original = """
人工智能正在改变内容创作的方式。
从文本生成到视频制作，AI 工具让创作者能够更高效地生产高质量内容。
"""

# 适配到不同平台
twitter_version = adapter.adapt_for_platform(original, "twitter")
linkedin_version = adapter.adapt_for_platform(original, "linkedin")
instagram_version = adapter.adapt_for_platform(original, "instagram")

print("Twitter:", twitter_version)
print("LinkedIn:", linkedin_version)
print("Instagram:", instagram_version)
```

## 最佳实践

### 内容质量控制

1. **人工审核**：自动生成的内容必须经过人工审核
2. **品牌一致性**：保持品牌语调和风格统一
3. **平台适配**：针对不同平台优化内容格式
4. **合规检查**：确保内容符合平台规则和法律法规

### 发布频率建议

| 平台 | 建议频率 | 最佳时段 |
|------|---------|---------|
| Twitter/X | 3-5次/天 | 9:00, 12:00, 18:00 |
| LinkedIn | 1-2次/天 | 8:00, 17:00 |
| Instagram | 1-3次/天 | 11:00, 14:00, 20:00 |

### 内容类型搭配

- **教育内容** (40%)：教程、技巧、知识分享
- **娱乐内容** (30%)：轻松话题、互动内容
- **推广内容** (20%)：产品、服务、活动
- **社区内容** (10%)：用户故事、互动问答

## 故障排查

### 依赖问题

```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 检查 Python 版本
python --version  # 需要 3.12+
```

### API 限制

- 监控 API 调用频率
- 实现指数退避重试机制
- 准备备用 API 密钥

### 内容生成失败

- 检查 API 密钥配置
- 简化输入提示词
- 查看详细错误日志

## 免责声明

本工具仅供学习和内容创作辅助使用：

- 遵守各平台的使用条款
- 尊重知识产权和版权
- 不得用于生成垃圾信息或滥用平台
- 用户对生成内容的使用负全部责任

## 许可证

本项目基于 AGPL-3.0 许可证开源。使用本 Skill 即表示你同意遵守相关许可条款。

## 相关资源

- [项目文档](https://github.com/FujiwaraChoki/MoneyPrinterV2/tree/main/docs)
- [开发路线图](https://github.com/FujiwaraChoki/MoneyPrinterV2/blob/main/docs/Roadmap.md)
- [贡献指南](https://github.com/FujiwaraChoki/MoneyPrinterV2/blob/main/CONTRIBUTING.md)
