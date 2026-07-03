"""
知识库 — 简易 RAG 检索引擎 (用于咨询类邮件增强回复)
"""
import os
import json
from typing import Optional
from .config_loader import get_config


class KnowledgeBase:
    """
    简易知识库：基于关键词匹配 + 可选向量检索
    MVP 阶段使用关键词匹配，后续可升级为 ChromaDB 向量检索
    """

    # 预置 FAQ 数据 (可扩展)
    DEFAULT_FAQ = {
        "zh-CN": {
            "配送": "我们支持全国配送，标准配送 3-5 个工作日到达，加急配送 1-2 个工作日。订单满 ¥99 免运费。",
            "退换货": "支持 14 天无理由退换货。商品需保持原包装完好。请在订单页面申请退换货，审核通过后 48 小时内发出退货标签。",
            "退款": "退款将在收到退货后 3-5 个工作日原路返回。信用卡/花呗支付退回原支付方式，余额退款到余额账户。",
            "尺码": "请参考商品页面的尺码表。如有疑问，建议测量后联系客服获取个性化推荐。",
            "保修": "电子产品享有 1 年质保。非人为损坏免费维修/换新。请保留订单号和产品序列号。",
            "库存": "页面显示「现货」即可立即发货。显示「预售」的商品预计 7-15 天发货。",
            "支付": "支持微信支付、支付宝、信用卡、花呗、银联。跨境订单支持 Visa/Mastercard/PayPal。",
        },
        "en": {
            "shipping": "We offer free standard shipping (3-5 business days) on orders over $49. Express shipping (1-2 business days) available for $9.99.",
            "returns": "14-day hassle-free returns. Items must be in original packaging. Initiate return from your order page and receive a return label within 48 hours.",
            "refund": "Refunds are processed within 3-5 business days after we receive the return. Refund goes back to the original payment method.",
            "warranty": "Electronics come with a 1-year warranty covering manufacturing defects. Keep your order number and serial number handy.",
            "sizing": "Please refer to the size chart on the product page. For personalized recommendations, measure yourself and contact support.",
            "stock": "Items marked 'In Stock' ship immediately. 'Pre-order' items ship in 7-15 days.",
            "payment": "We accept Visa, Mastercard, PayPal, Apple Pay, and Google Pay. All transactions are SSL-encrypted.",
        },
    }

    def __init__(self, config: dict = None):
        cfg = config or get_config()
        kb_cfg = cfg.get("knowledge_base", {})
        self.enabled = kb_cfg.get("enabled", True)
        self.faq = self.DEFAULT_FAQ.copy()
        self._load_faq_files(kb_cfg.get("faq_files", []))

    def search(self, query: str, language: str = "en", top_k: int = 3) -> str:
        """
        搜索知识库，返回格式化的知识片段

        返回空字符串表示未找到匹配
        """
        if not self.enabled:
            return ""

        # 选择语言
        faq_lang = language if language in self.faq else "en"
        faq_data = self.faq.get(faq_lang, self.faq["en"])

        # 关键词匹配
        query_lower = query.lower()
        matches = []

        for topic, answer in faq_data.items():
            # 检查 topic 关键词是否在 query 中
            topic_lower = topic.lower()
            if topic_lower in query_lower:
                matches.append((3.0, topic, answer))
            else:
                # 模糊匹配: 计算共同词
                query_words = set(query_lower.split())
                topic_words = set(topic_lower.split())
                overlap = query_words & topic_words
                if overlap:
                    score = len(overlap) / max(len(topic_words), 1)
                    if score > 0.3:
                        matches.append((score, topic, answer))

        # 按分数排序，取 top_k
        matches.sort(key=lambda x: x[0], reverse=True)
        matches = matches[:top_k]

        if not matches:
            return ""

        # 格式化为邮件引用
        snippets = []
        for score, topic, answer in matches:
            snippets.append(f"📌 **{topic}**: {answer}")

        return "\n\n".join(snippets)

    def _load_faq_files(self, faq_files: list[str]):
        """从外部文件加载 FAQ"""
        for filepath in faq_files:
            if not os.path.exists(filepath):
                continue
            try:
                ext = os.path.splitext(filepath)[1].lower()
                if ext == ".json":
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for lang, faqs in data.items():
                            if lang not in self.faq:
                                self.faq[lang] = {}
                            self.faq[lang].update(faqs)
                elif ext == ".md":
                    # 简易 Markdown FAQ 解析
                    with open(filepath, "r", encoding="utf-8") as f:
                        self._parse_md_faq(f.read())
            except Exception as e:
                print(f"[WARN] 加载 FAQ 文件失败 {filepath}: {e}")

    def _parse_md_faq(self, content: str):
        """解析 Markdown 格式的 FAQ"""
        import re
        # 查找 ## Q: ... \n A: ... 格式
        pattern = r'##\s*Q:\s*(.+?)\n+(?:A:\s*)?(.+?)(?=\n##|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        for question, answer in matches:
            q = question.strip()
            a = answer.strip()
            # 检测语言
            lang = "zh-CN" if any('\u4e00' <= c <= '\u9fff' for c in q) else "en"
            if lang not in self.faq:
                self.faq[lang] = {}
            self.faq[lang][q] = a
