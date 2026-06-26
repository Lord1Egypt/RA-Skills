"""
SEO & 流量优化器 🐱💰
帮你优化标题、标签、内容，让文章获得更多曝光喵！
"""

import re
from typing import Optional


class SEOOptimizer:
    """各平台 SEO / 流量优化器"""

    # 各平台标题最佳长度
    TITLE_LENGTH = {
        "juejin": {"min": 10, "max": 35, "best": "20-28字"},
        "zhihu": {"min": 8, "max": 30, "best": "15-25字"},
        "xiaohongshu": {"min": 10, "max": 20, "best": "15-20字，含emoji"},
        "wechat_mp": {"min": 10, "max": 64, "best": "20-30字"},
    }

    # 各平台热门标签推荐
    POPULAR_TAGS = {
        "juejin": [
            "前端", "后端", "Python", "JavaScript", "AI", "机器学习",
            "OpenAI", "自动", "DevOps", "微服务", "Vue", "React",
            "TypeScript", "Docker", "K8s", "数据库", "算法", "面试",
            "程序员", "效率工具", "开源", "低代码", "RPA",
        ],
        "zhihu": [
            "人工智能", "深度学习", "程序员", "互联网", "求职",
            "技术分享", "效率提升", "工具推荐", "Python", "数据分析",
        ],
        "xiaohongshu": [
            "效率工具", "AI神器", "打工人", "自我提升", "干货分享",
            "涨薪秘籍", "职场干货", "副业", "技能提升", "效率翻倍",
        ],
        "wechat_mp": [
            "技术干货", "职场", "AI前沿", "效率", "工具推荐",
            "程序员日常", "副业变现", "知识付费",
        ],
    }

    # 标题党公式
    TITLE_FORMULAS = {
        "curiosity": "为什么/如何/竟然——引发好奇",
        "number": "X个技巧/X分钟——数字吸引眼球",
        "contrast": "从X到X——对比制造冲击",
        "pain_point": "别再X了——痛点共鸣",
        "result": "我用X做到了X——结果导向",
        "authority": "XX大佬都推荐的——权威背书",
        "exclusivity": "99%人都不知道的——稀缺感",
        "emotion": "后悔没早发现/太香了——情绪触发",
    }

    def optimize_title(
        self,
        original_title: str,
        platform: str,
        content: str = "",
    ) -> dict:
        """优化标题
        
        返回多个方案供选择
        """
        length_info = self.TITLE_LENGTH.get(platform, self.TITLE_LENGTH["juejin"])

        results = {
            "original": original_title,
            "length_check": self._check_title_length(original_title, platform),
            "suggestions": [],
        }

        # 方案1：简洁优化版
        results["suggestions"].append(
            {
                "type": "简洁版",
                "title": self._clean_title(original_title, length_info),
                "reason": "去除冗余，突出核心信息",
            }
        )

        # 方案2：好奇驱动
        if content:
            results["suggestions"].append(
                {
                    "type": "好奇驱动",
                    "title": f"为什么越来越多的人用{self._extract_topic(content)}？真相是...",
                    "reason": "利用好奇心提升点击率",
                }
            )

        # 方案3：数字冲击
        results["suggestions"].append(
            {
                "type": "数字冲击",
                "title": f"我用{self._extract_tool(content)}，效率提升了300%！",
                "reason": "具体数字+结果，最具说服力",
            }
        )

        # 方案4：痛点共鸣
        results["suggestions"].append(
            {
                "type": "痛点共鸣",
                "title": f"别再手动{self._extract_action(content)}了！这个方法帮你省下一半时间",
                "reason": "痛点切入，引发共鸣",
            }
        )

        # 方案5：情绪触发
        results["suggestions"].append(
            {
                "type": "情绪触发",
                "title": f"后悔！早知道这个{self._extract_topic(content)}技巧，能少加多少班",
                "reason": "情绪词+场景，提升转发率",
            }
        )

        return results

    def optimize_tags(
        self,
        platform: str,
        content: str,
        existing_tags: list = None,
        max_tags: int = 5,
    ) -> list:
        """优化标签推荐
        
        结合热门趋势和内容关键词，推荐最佳标签
        """
        popular = self.POPULAR_TAGS.get(platform, [])
        existing = existing_tags or []

        # 从内容中提取关键词
        content_keywords = self._extract_content_keywords(content)

        # 合并去重
        all_tags = list(dict.fromkeys(existing + content_keywords + popular))

        # 按热度排序（热门 tag 靠前）
        result = []
        for tag in all_tags:
            if tag in popular:
                result.append(tag)
            else:
                result.append(tag)

        return list(set(result))[:max_tags]

    def get_posting_tips(self, platform: str) -> dict:
        """获取平台发布技巧"""
        tips = {
            "juejin": {
                "best_time": "工作日 9:00/12:00/18:00",
                "content_tips": [
                    "技术深度是核心，至少包含代码示例",
                    "配图很重要，流程/架构图能显著提升浏览量",
                    "标签选 3-5 个，不要太多",
                    "开头一段决定点击率，要精炼有吸引力",
                    "文末加互动：'你觉得呢？评论区见'",
                ],
                "seo_tips": [
                    "标题包含技术关键词（React/Vue/Python等）",
                    "首段前50字包含核心话题",
                    "代码块标注语言类型",
                ],
            },
            "zhihu": {
                "best_time": "早上8:00/中午12:30/晚上21:00",
                "content_tips": [
                    "问答式写作比文章式更受欢迎",
                    "多用'个人经历'增强可信度",
                    "长文（3000字+）更容易上热榜",
                    "善用引用格式和加粗",
                ],
                "seo_tips": [
                    "回答热门问题时更容易获得流量",
                    "开头前100字决定推荐量",
                    "善用知乎话题标签",
                ],
            },
            "xiaohongshu": {
                "best_time": "中午11:30/傍晚18:00/晚上22:00",
                "content_tips": [
                    "标题必须有 emoji！",
                    "短句+分段，别写长段落",
                    "配图质量决定生死",
                    "文末加 #话题# 标签，5-10个",
                    "善用'建议xxx都来试试'句式",
                ],
                "seo_tips": [
                    "标题前10个字最关键",
                    "标签选精准话题，不要泛泛的",
                    "关键词密度适中，重复2-3次最佳",
                ],
            },
            "wechat_mp": {
                "best_time": "早上7:00/中午12:00/傍晚18:00",
                "content_tips": [
                    "排版美观度极大影响打开率",
                    "封面图决定 80% 的打开率",
                    "摘要不超过 120 字，要有吸引力",
                    "善用引导关注话术",
                ],
                "seo_tips": [
                    "标题包含搜索关键词",
                    "公众号名称就是 SEO 品牌词",
                    "往期文章互相链接可提升阅读",
                ],
            },
        }

        return tips.get(platform, {})

    def generate_content_outline(
        self, topic: str, platform: str, word_count: int = 1500
    ) -> list:
        """生成内容大纲"""
        outlines = {
            "juejin": [
                f"## 引言（{int(word_count*0.1)}字）",
                f"- 问题/痛点引入",
                f"- 为什么这个问题值得关注",
                f"## 核心方案（{int(word_count*0.3)}字）",
                f"- 方案概述",
                f"- 实现原理",
                f"## 实战代码（{int(word_count*0.3)}字）",
                f"- 完整代码示例",
                f"- 运行结果展示",
                f"## 进阶优化（{int(word_count*0.15)}字）",
                f"- 性能优化建议",
                f"- 注意事项",
                f"## 总结（{int(word_count*0.05)}字）",
                f"- 核心要点回顾",
                f"- 延伸阅读推荐",
            ],
        }

        return outlines.get(platform, outlines["juejin"])

    def _check_title_length(self, title: str, platform: str) -> dict:
        """检查标题长度是否合适"""
        length_info = self.TITLE_LENGTH.get(platform, {})
        char_count = len(title)

        return {
            "length": char_count,
            "min": length_info.get("min", 10),
            "max": length_info.get("max", 64),
            "best": length_info.get("best", ""),
            "is_ok": length_info.get("min", 10) <= char_count <= length_info.get("max", 35),
        }

    def _clean_title(self, title: str, length_info: dict) -> str:
        """清理和优化标题"""
        # 去除冗余词汇
        clean = title.strip()
        # 去除多余符号
        clean = re.sub(r"[【\]〖〗\s]+", " ", clean)
        # 限制长度
        max_len = length_info.get("max", 35)
        if len(clean) > max_len:
            clean = clean[:max_len] + "…"
        return clean

    def _extract_topic(self, content: str) -> str:
        """从内容中提取主题关键词"""
        keywords = self._extract_content_keywords(content)
        return keywords[0] if keywords else "效率工具"

    def _extract_tool(self, content: str) -> str:
        return self._extract_topic(content)

    def _extract_action(self, content: str) -> str:
        return "处理工作"

    def _extract_content_keywords(self, content: str) -> list:
        """从内容中提取关键词"""
        keywords = []
        word_list = [
            "AI", "OpenClaw", "效率", "自动化", "工具", "赚钱", "副业",
            "教程", "技巧", "攻略", "Python", "JavaScript", "前端", "后端",
        ]
        for w in word_list:
            if w in content:
                keywords.append(w)
        return keywords
