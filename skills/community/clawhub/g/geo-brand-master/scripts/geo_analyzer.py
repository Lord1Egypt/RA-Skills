#!/usr/bin/env python3
"""
GEO Monitor - AI原因分析模块
基于检测结果，调用AI分析"为什么没被推荐"
"""

import sys
import json
import time
import subprocess


class GeoAnalyzer:
    """GEO AI分析器"""

    def __init__(self, brand: str, search_results: dict, gem_score: int):
        self.brand = brand
        self.search_results = search_results
        self.gem_score = gem_score

    def analyze(self) -> str:
        """调用AI分析原因"""
        # 构造分析prompt
        platform_summary = self._summarize_results()

        prompt = f"""你是一个GEO（生成式引擎优化）专家。请分析以下品牌在AI搜索中不可见的原因，并给出具体的优化建议。

## 品牌信息
品牌名称：{self.brand}
GEM可见性评分：{self.gem_score}/100

## 各平台检测结果
{platform_summary}

## 请分析
1. 为什么这个品牌在AI搜索中不可见？
2. 品牌在AI可见性方面存在哪些问题？
3. 如何优化才能让AI在回答相关问题时主动推荐这个品牌？

请给出具体、可执行的建议，300字以内。"""

        # 调用MiniMax分析
        result = self._call_ai(prompt)
        return result

    def _summarize_results(self) -> str:
        """汇总搜索结果"""
        lines = []
        for platform, data in self.search_results.items():
            status = "已发现" if data.get("found") else "未发现"
            occ = data.get("occurrences", 0)
            snippets = data.get("snippets", [])
            error = data.get("error")

            if error:
                lines.append(f"- {platform}: 错误 - {error}")
            else:
                lines.append(f"- {platform}: {status}（出现{occ}次）")
                if snippets:
                    for s in snippets[:2]:
                        lines.append(f"  片段: {s[:100]}")

        return "\n".join(lines) if lines else "各平台均未检测到"

    def _call_ai(self, prompt: str) -> str:
        """调用外部AI分析（需配置有效的AI接口地址）"""
        # ⚠️ 如需启用AI分析功能，请在此填入您的AI接口地址
        # 例如：https://your-api-server.com/v1/chat/completions
        # 当前默认使用本地分析框架（见 _get_fallback_analysis）
        AI_ENDPOINT = ""  # <-- 填入AI接口地址，如 https://api.minimax.chat/v1/chat/completions

        if not AI_ENDPOINT:
            return self._get_fallback_analysis()

        cmd = [
            "curl", "-s", "-X", "POST",
            AI_ENDPOINT,
            "-H", "Content-Type: application/json",
            "-H", "Authorization: Bearer YOUR_TOKEN",  # <-- 替换为有效token
            "-d", json.dumps({
                "model": "minimax-m2.7",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.7
            })
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            resp = json.loads(result.stdout)
            return resp.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            return f"AI分析调用失败: {str(e)}\n\n建议：{self._get_fallback_analysis()}"

    def _get_fallback_analysis(self) -> str:
        """当AI调用失败时的预设分析框架"""
        total_found = sum(1 for r in self.search_results.values() if r.get("found"))
        total_platforms = len(self.search_results)

        analysis = f"""## {self.brand} AI可见性分析

### 当前状态
- GEM评分：{self.gem_score}/100
- 检测平台：{total_platforms}个
- 已有曝光：{total_found}个平台

### 可能原因

1. **品牌知名度不足** — 作为新品牌，AI训练数据中收录较少
2. **内容覆盖不足** — 在AI平台常用信息源（知乎/公众号/官网）中曝光不足
3. **关键词策略** — 品牌名与用户实际搜索词不匹配
4. **内容结构问题** — 缺乏AI容易理解和引用的结构化内容

### 优化建议

1. **内容矩阵建设**
   - 在知乎、公众号发布深度文章（1500字+）
   - 文章标题包含核心搜索词
   - 内容中多次自然提及品牌

2. **技术优化**
   - 确保官网有完整的Schema.org结构化数据
   - 页面标题、描述包含品牌关键词
   - 提交网站到AI平台认可的搜索引擎

3. **外部引用**
   - 争取在权威媒体/平台获得引用
   - 建立品牌在AI知识图谱中的实体关联

4. **持续监控**
   - 每周检测可见性变化
   - 记录优化动作与效果关系
"""

        return analysis


def main():
    """测试用主函数"""
    if len(sys.argv) < 2:
        print("用法: python geo_analyzer.py <品牌名> [GEM评分]")
        sys.exit(1)

    brand = sys.argv[1]
    score = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    # 模拟搜索结果
    mock_results = {
        "deepseek": {"found": False, "occurrences": 0, "snippets": []},
        "kimi": {"found": False, "occurrences": 0, "snippets": []},
        "yiyan": {"found": False, "occurrences": 0, "snippets": []},
    }

    analyzer = GeoAnalyzer(brand, mock_results, score)
    result = analyzer.analyze()

    print(result)


if __name__ == "__main__":
    main()
