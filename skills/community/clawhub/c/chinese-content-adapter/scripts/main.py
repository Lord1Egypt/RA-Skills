#!/usr/bin/env python3
"""
中文社交媒体多平台内容适配器 🐱
一篇内容 → 自动适配掘金/知乎/小红书/公众号格式
"""

from juejin_formatter import JuejinFormatter
from zhihu_formatter import ZhihuFormatter
from xiaohongshu import XiaohongshuConverter
from wechat_formatter import WeChatFormatter
from seo_optimizer import SEOOptimizer
import json


class ContentAdapter:
    def __init__(self):
        self.juejin = JuejinFormatter()
        self.zhihu = ZhihuFormatter()
        self.xhs = XiaohongshuConverter()
        self.wechat = WeChatFormatter()
        self.seo = SEOOptimizer()

    def adapt_all(self, title: str, content: str, platforms: list = None) -> dict:
        if platforms is None:
            platforms = ["juejin", "zhihu", "xiaohongshu", "wechat_mp"]

        results = {}

        if "juejin" in platforms:
            results["juejin"] = self.juejin.format_article(title, content)

        if "zhihu" in platforms:
            results["zhihu"] = self.zhihu.format_article(title, content)

        if "xiaohongshu" in platforms:
            from xiaohongshu import convert as xhs_convert
            results["xiaohongshu"] = xhs_convert(content, title)

        if "wechat_mp" in platforms:
            results["wechat_mp"] = self.wechat.format_article(title, content)

        return results

    def seo_report(self, title: str, content: str, platform: str) -> dict:
        title_analysis = self.seo.optimize_title(title, platform, content)
        tips = self.seo.get_posting_tips(platform)

        return {
            "platform": platform,
            "title_analysis": title_analysis,
            "posting_tips": tips,
        }


if __name__ == "__main__":
    adapter = ContentAdapter()

    # 演示
    title = "用 OpenClaw 自动化你的工作流"
    content = """# 用 OpenClaw 自动化你的工作流

## 背景
作为一名开发者，我每天需要重复处理很多任务...

## 解决方案
使用 OpenClaw 的 Skill 系统...

## 代码示例
```python
import openclaw

agent = openclaw.Agent()
agent.run("帮我检查邮件")
```

## 总结
效率提升了 300%！
"""

    results = adapter.adapt_all(title, content)
    print(json.dumps(results, ensure_ascii=False, indent=2))
