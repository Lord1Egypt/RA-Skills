#!/usr/bin/env python3
"""
GEO Monitor - 核心爬虫模块
自动搜索多个AI平台，检测品牌关键词的可见性
"""

import asyncio
import json
import sys
import time
import re
from pathlib import Path

# 尝试导入playwright，不存在则给出提示
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install")
    sys.exit(1)


class GeoSearcher:
    """GEO搜索引擎"""

    # 搜索URL模板
    SEARCH_URLS = {
        "deepseek": "https://chat.deepseek.com",
        "kimi": "https://kimi.moonshot.cn",
        "xinhuo": "https://xinghuo.xfyun.cn/chat",
        "yiyan": "https://yiyan.baidu.com",
        "zhipu": "https://www.zhipuai.cn",
        "xunfei": "https://xinghuo.xfyun.cn/chat",
        "qianwen": "https://qianwen.aliyun.com",
    }

    # 搜索框CSS选择器（2026-04-16 简单刀修复）
    # xinhuo和xunfei是同一平台（讯飞星火），xunfei已在config.json禁用，避免重复
    # deepseek: 需要登录，暂时禁用
    # xinhuo: /chat会重定向到/desk，搜索框是裸textarea
    # yiyan: 使用div[contenteditable='true']
    # qianwen: 需要登录跳转，暂时禁用
    SEARCH_SELECTORS = {
        "deepseek": "textarea.dsb, #chat-input, textarea[placeholder*='搜索']",
        "kimi": "textarea, div[contenteditable='true'], input[type='text']",
        "xinhuo": "textarea",
        "yiyan": "div[contenteditable='true']",
        "zhipu": "textarea, input[type='text']",
        "xunfei": "textarea",
        "qianwen": "textarea, .ProseMirror, div[contenteditable='true']",
    }

    def __init__(self, keywords: list[str], config_path: str = None, enabled_platforms: list = None):
        self.keywords = keywords
        self.config = self._load_config(config_path)
        self.enabled_platforms = enabled_platforms  # None表示不限制
        self.results = {}

    def _load_config(self, config_path: str = None) -> dict:
        """加载配置"""
        default_config = {
            "platforms": {
                "deepseek": {"enabled": True, "weight": 1.0},
                "kimi": {"enabled": True, "weight": 1.0},
                "xinhuo": {"enabled": True, "weight": 0.9},
                "yiyan": {"enabled": True, "weight": 0.9},
                "zhipu": {"enabled": True, "weight": 0.8},
                "xunfei": {"enabled": True, "weight": 0.7},
                "qianwen": {"enabled": True, "weight": 0.8},
                "doubao": {"enabled": False, "weight": 0.8},
                "mita": {"enabled": False, "weight": 0.6},
                "hunyuan": {"enabled": False, "weight": 0.7},
            },
            "timeout": 30000,
            "wait_after_input": 3000,
        }

        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                user_config = json.load(f)
                # 合并配置
                for k, v in user_config.get("platforms", {}).items():
                    if k in default_config["platforms"]:
                        default_config["platforms"][k].update(v)

        return default_config

    async def search_platform(self, platform: str, browser) -> dict:
        """在单个平台搜索关键词"""
        result = {
            "platform": platform,
            "found": False,
            "occurrences": 0,
            "positions": [],
            "snippets": [],
            "error": None,
        }

        try:
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # 设置超时
            page.set_default_timeout(self.config.get("timeout", 30000))

            # 访问平台
            url = self.SEARCH_URLS.get(platform)
            if not url:
                result["error"] = f"No URL for platform: {platform}"
                await context.close()
                return result

            print(f"  -> 正在搜索 {platform}...")
            await page.goto(url, wait_until="domcontentloaded")

            # 等待页面加载 - 增加等待时间
            await asyncio.sleep(5)

            # 尝试找到搜索框
            selector = self.SEARCH_SELECTORS.get(platform, "textarea, input[type='text']")

            try:
                search_box = await page.wait_for_selector(selector, timeout=15000)
            except Exception:
                result["error"] = f"找不到搜索框: {selector}"
                await context.close()
                return result

            # 输入关键词
            keyword = self.keywords[0]  # 用第一个关键词
            await search_box.click()
            await search_box.fill(keyword)

            # 按回车搜索
            await search_box.press("Enter")

            # 等待结果
            await asyncio.sleep(self.config.get("wait_after_input", 3000) / 1000)

            # 尝试获取结果文本
            try:
                # 等待结果出现
                await page.wait_for_timeout(5000)

                # 获取页面文本
                content = await page.content()
                body_text = await page.inner_text("body")

                # 检查关键词出现次数
                occurrences = body_text.lower().count(keyword.lower())
                result["occurrences"] = occurrences

                if occurrences > 0:
                    result["found"] = True

                # 提取相关片段
                lines = body_text.split("\n")
                for line in lines:
                    if keyword.lower() in line.lower() and len(line.strip()) > 10:
                        result["snippets"].append(line.strip()[:200])

                result["snippets"] = result["snippets"][:5]  # 最多5条

            except Exception as e:
                result["error"] = f"获取结果失败: {str(e)}"

            await context.close()

        except Exception as e:
            result["error"] = str(e)

        return result

    async def search_all(self) -> dict:
        """在所有启用的平台搜索"""
        all_results = {}

        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=True)

            for platform, config in self.config["platforms"].items():
                if not config.get("enabled", False):
                    print(f"跳过 {platform}（已禁用）")
                    continue
                # 如果指定了enabled_platforms，只搜索这些平台
                if self.enabled_platforms is not None and platform not in self.enabled_platforms:
                    print(f"跳过 {platform}（未在配额范围内）")
                    continue

                result = await self.search_platform(platform, browser)
                all_results[platform] = result

                # 每个平台间隔2秒，避免被封
                await asyncio.sleep(2)

            await browser.close()

        self.results = all_results
        return all_results

    def calculate_gem_score(self) -> dict:
        """计算GEM可见性评分"""
        if not self.results:
            return {"score": 0, "grade": "未知", "details": {}}

        total_score = 0
        total_weight = 0
        details = {}

        for platform, result in self.results.items():
            cfg = self.config["platforms"].get(platform, {})
            weight = cfg.get("weight", 1.0)

            if result.get("error"):
                details[platform] = {"error": result["error"], "score": 0}
                continue

            occurrences = result.get("occurrences", 0)
            found = result.get("found", False)

            # 基础分：出现就有分
            base_score = 10 if found else 0
            # 加分：出现次数
            occurrence_score = min(occurrences * 2, 20)
            # 加分：snippet数量
            snippet_score = min(len(result.get("snippets", [])) * 5, 10)

            platform_score = (base_score + occurrence_score + snippet_score) * weight
            total_score += platform_score
            total_weight += weight

            details[platform] = {
                "found": found,
                "occurrences": occurrences,
                "snippets": len(result.get("snippets", [])),
                "score": round(platform_score, 1),
            }

        # 归一化到0-100
        normalized_score = int((total_score / total_weight) if total_weight > 0 else 0)
        normalized_score = max(0, min(100, normalized_score))

        # 等级
        if normalized_score >= 80:
            grade = "🟢 优秀"
        elif normalized_score >= 60:
            grade = "🟡 良好"
        elif normalized_score >= 30:
            grade = "🟠 一般"
        else:
            grade = "🔴 薄弱"

        return {
            "score": normalized_score,
            "grade": grade,
            "details": details,
            "keywords": self.keywords,
        }

    def format_report(self) -> str:
        """生成Markdown格式报告"""
        score_data = self.calculate_gem_score()

        lines = [
            f"# GEO可见性检测报告",
            f"",
            f"**检测品牌：** {', '.join(self.keywords)}",
            f"**检测时间：** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## GEM可见性评分",
            f"",
            f"**总分：{score_data['score']} / 100**  {score_data['grade']}",
            f"",
            f"## 各平台检测结果",
            f"",
        ]

        # 按分数排序
        sorted_details = sorted(
            score_data["details"].items(),
            key=lambda x: x[1].get("score", 0),
            reverse=True
        )

        for platform, detail in sorted_details:
            cfg = self.config["platforms"].get(platform, {})
            weight = cfg.get("weight", 1.0)
            status = "✅" if detail.get("found") else "❌"

            if "error" in detail:
                lines.append(f"- **{platform.upper()}** {status} 错误: {detail['error']}")
            else:
                lines.append(
                    f"- **{platform.upper()}** {status} "
                    f"出现{detail.get('occurrences', 0)}次 "
                    f"片段{detail.get('snippets', 0)}条 "
                    f"得分{detail.get('score', 0)}"
                )

        lines.extend([
            "",
            "## 各平台详情",
            "",
        ])

        for platform, result in self.results.items():
            lines.append(f"### {platform.upper()}")
            if result.get("error"):
                lines.append(f"❌ 错误: {result['error']}")
            else:
                lines.append(f"✅ {'已发现' if result.get('found') else '未发现'}")
                lines.append(f"出现次数: {result.get('occurrences', 0)}")
                if result.get("snippets"):
                    lines.append("相关片段:")
                    for s in result["snippets"][:3]:
                        lines.append(f"> {s}")
            lines.append("")

        return "\n".join(lines)


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python geo_searcher.py <关键词1> [关键词2] [关键词3] ...")
        print("示例: python geo_searcher.py 提分引擎AI 药常记")
        sys.exit(1)

    keywords = sys.argv[1:]

    print(f"=" * 50)
    print(f"GEO Monitor - AI可见性检测")
    print(f"检测关键词: {', '.join(keywords)}")
    print(f"=" * 50)

    searcher = GeoSearcher(keywords)

    print("\n开始搜索...\n")
    results = await searcher.search_all()

    print("\n" + "=" * 50)
    print("搜索完成，正在计算评分...\n")

    score_data = searcher.calculate_gem_score()
    print(f"GEM可见性评分: {score_data['score']} / 100")
    print(f"等级: {score_data['grade']}")

    report = searcher.format_report()

    # 保存报告
    import tempfile, os
    report_dir = os.path.join(os.path.expanduser("~"), "Desktop", "geo_reports")
    os.makedirs(report_dir, exist_ok=True)
    report_file = os.path.join(report_dir, f"geo_report_{int(time.time())}.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n报告已保存: {report_file}")

    # 打印摘要
    print("\n各平台结果:")
    for platform, detail in score_data["details"].items():
        if "error" in detail:
            print(f"  {platform}: 错误 - {detail['error']}")
        else:
            status = "✅" if detail.get("found") else "❌"
            print(f"  {platform}: {status} {detail.get('occurrences', 0)}次")


if __name__ == "__main__":
    asyncio.run(main())
