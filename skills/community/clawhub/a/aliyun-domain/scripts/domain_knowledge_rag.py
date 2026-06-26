#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云域名知识库 RAG 检索工具

基于本地知识库（knowledge/aliyun-domain-help）进行语义检索，
为域名注册、交易、建站、备案等问题提供精准答案。
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json


class DomainKnowledgeRAG:
    """域名知识库 RAG 检索器"""

    def __init__(self, knowledge_base_path: str = None):
        """
        初始化检索器

        Args:
            knowledge_base_path: 知识库路径，默认为 knowledge/aliyun-domain-help
        """
        if knowledge_base_path is None:
            # 默认使用脚本所在目录的 knowledge/aliyun-domain-help
            script_dir = Path(__file__).parent
            self.knowledge_base_path = (
                script_dir.parent / "knowledge" / "aliyun-domain-help"
            )
        else:
            self.knowledge_base_path = Path(knowledge_base_path)

        self.documents = {}  # 存储所有文档内容 {file_path: content}
        self.document_index = {}  # 文档索引 {keyword: [file_paths]}
        self._load_all_documents()
        self._build_index()

    def _load_all_documents(self):
        """加载知识库中的所有 Markdown 文档"""
        if not self.knowledge_base_path.exists():
            print(f"⚠️  知识库路径不存在：{self.knowledge_base_path}")
            return

        md_files = list(self.knowledge_base_path.rglob("*.md"))

        for md_file in md_files:
            # 跳过 README.md
            if md_file.name == "README.md":
                continue

            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents[str(md_file)] = content
            except Exception as e:
                print(f"⚠️  读取文档失败 {md_file}: {e}")

    def _build_index(self):
        """构建关键词索引"""
        # 定义关键词映射（扩展版）
        self.keyword_mapping = {
            # ========== 域名注册相关 ==========
            "注册": [
                "域名注册",
                "注册流程",
                "注册指南",
                "如何注册",
                "注册域名",
                "新注册",
                "首次注册",
            ],
            "实名认证": [
                "实名认证",
                "实名审核",
                "资料上传",
                "审核时间",
                "证件审核",
                "身份验证",
                "实名认证",
                "审核通过",
            ],
            "过户": [
                "过户",
                "持有者修改",
                "信息修改",
                "所有人变更",
                "域名过户",
                "信息变更",
                "持有者变更",
                "所有人修改",
            ],
            "材料": [
                "材料",
                "资料",
                "证件",
                "文件",
                "证明",
                "身份证",
                "营业执照",
                "证件号",
                "所需材料",
                "准备材料",
            ],
            # ========== 域名交易相关 ==========
            "交易": [
                "域名交易",
                "购买域名",
                "出售域名",
                "交易平台",
                "买卖",
                "买入",
                "卖出",
                "二手域名",
                "域名购买",
            ],
            "一口价": [
                "一口价",
                "严选",
                "优选",
                "立即购买",
                "固定价格",
                "直接购买",
                "域名交易",
            ],
            "push": [
                "push",
                "带价 push",
                "域名推送",
                "域名 push",
                "推送",
                "转移",
                "账户间转移",
            ],
            "回购": ["回购", "域名回购", "域名收购", "回收"],
            "注意事项": [
                "注意事项",
                "注意",
                "提示",
                "提醒",
                "小心",
                "谨防",
                "防骗",
                "风险",
            ],
            # ========== 域名管理相关 ==========
            "续费": [
                "续费",
                "续费价格",
                "续费流程",
                "续期",
                "延长",
                "到期续费",
                "自动续费",
            ],
            "赎回": [
                "赎回",
                "赎回价格",
                "过期域名",
                "域名赎回",
                "过期",
                "失效",
                "过期处理",
                "过期了怎么办",
            ],
            "转移": [
                "转移",
                "转入",
                "转出",
                "转移密码",
                "域名转移",
                "转入阿里云",
                "转出阿里云",
                "转移条件",
            ],
            "dns": [
                "dns",
                "解析",
                "nameserver",
                "域名服务器",
                "dns 服务器",
                "修改 dns",
                "更换 dns",
                "绑定",
                "域名绑定",
                "服务器绑定",
                "指向",
                "解析配置",
            ],
            "锁定": [
                "锁定",
                "禁止转移",
                "禁止更新",
                "安全锁",
                "转移锁",
                "更新锁",
                "注册局安全锁",
                "域名锁定",
                "锁定域名",
                "保护",
                "安全保护",
                "防止转移",
            ],
            "管理": ["管理", "域名管理", "控制台", "操作", "设置", "配置", "维护"],
            # ========== 备案相关 ==========
            "备案": [
                "备案",
                "icp 备案",
                "网站备案",
                "备案流程",
                "icp",
                "工信备案",
                "管局备案",
                "备案申请",
                "个人备案",
                "企业备案",
                "备案材料",
                "备案条件",
            ],
            "备案时间": [
                "备案时间",
                "备案多久",
                "备案多长时间",
                "备案周期",
                "审核时间",
                "工作日",
                "备案时长",
                "多长时间",
            ],
            # ========== 建站相关 ==========
            "建站": [
                "建站",
                "网站搭建",
                "网站建设",
                "制作网站",
                "创建网站",
                "建立网站",
                "搭建网站",
                "建站流程",
            ],
            "万小智": [
                "万小智",
                "ai 建站",
                "智能建站",
                "零代码建站",
                "万小智 ai 建站",
                "云·速成美站",
            ],
            "服务器": [
                "服务器",
                "云服务器",
                "ecs",
                "虚拟主机",
                "云主机",
                "主机",
                "web 服务器",
                "服务端",
            ],
            # ========== 域名安全相关 ==========
            "安全": [
                "安全",
                "域名安全",
                "安全防护",
                "安全保障",
                "保护措施",
                "风险防范",
            ],
            "注册局安全锁": [
                "注册局安全锁",
                "安全锁",
                "高级安全锁",
                " Registry lock",
                "高端安全保护",
            ],
            # ========== 价格费用相关 ==========
            "价格": [
                "价格",
                "费用",
                "多少钱",
                "价格是多少",
                "价位",
                "资费",
                "收费标准",
                "价格表",
            ],
            "优惠": ["优惠", "折扣", "活动", "促销", "优惠券", "口令", "满减"],
            # ========== 常见问题 ==========
            "faq": ["faq", "常见问题", "问题解答", "常见疑问", "问答", "疑问", "解惑"],
            "错误": [
                "错误",
                "失败",
                "报错",
                "无法",
                "不能",
                "不行",
                "问题",
                "异常",
                "提示",
                "报错信息",
                "错误提示",
            ],
            "条件": ["条件", "要求", "需要", "必备", "前提", "资格", "资质"],
            "时间": [
                "时间",
                "多久",
                "多长时间",
                "何时",
                "什么时候",
                "几天",
                "工作日",
                "周期",
            ],
        }

        # 为每个文档建立关键词索引
        for file_path, content in self.documents.items():
            # 从文件路径提取分类信息
            parts = file_path.split("/")
            category = parts[-2] if len(parts) >= 2 else "unknown"

            # 提取文档标题
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else "Untitled"

            # 为每个关键词建立索引
            content_lower = content.lower()
            for keyword, related_terms in self.keyword_mapping.items():
                # 检查文档是否包含关键词或相关术语
                if (
                    any(term.lower() in content_lower for term in related_terms)
                    or keyword.lower() in content_lower
                ):
                    if keyword not in self.document_index:
                        self.document_index[keyword] = []
                    self.document_index[keyword].append(
                        {
                            "file_path": file_path,
                            "title": title,
                            "category": category,
                            "relevance": self._calculate_relevance(
                                content, related_terms + [keyword]
                            ),
                        }
                    )

    def _calculate_relevance(self, content: str, keywords: List[str]) -> float:
        """计算文档与关键词的相关性得分"""
        content_lower = content.lower()
        score = 0.0

        for keyword in keywords:
            # 标题中出现关键词权重更高
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match and keyword.lower() in title_match.group(1).lower():
                score += 10.0

            # 正文中出现关键词
            count = content_lower.count(keyword.lower())
            score += min(count * 0.5, 5.0)  # 最多 5 分

        return score

    def _expand_query(self, query: str) -> List[str]:
        """
        扩展查询，添加同义词和相关词

        Args:
            query: 原始查询

        Returns:
            扩展后的查询词列表
        """
        expanded = [query]
        query_lower = query.lower()

        # 同义词扩展
        synonym_rules = {
            # 锁定相关
            "锁定": ["禁止转移", "转移锁", "保护", "安全锁"],
            "禁止转移": ["锁定", "转移锁", "保护"],
            "转移锁": ["锁定", "禁止转移", "保护"],
            # 过户相关
            "过户": ["持有者修改", "信息修改", "变更", "转让"],
            "持有者修改": ["过户", "信息修改", "变更"],
            # 备案相关
            "备案": ["icp", "工信备案", "管局备案"],
            "icp": ["备案", "icp 备案"],
            # 材料相关
            "材料": ["资料", "证件", "文件", "证明", "身份证"],
            "资料": ["材料", "证件", "文件"],
            # 时间相关
            "多久": ["多长时间", "时间", "几天", "工作日", "周期"],
            "多长时间": ["多久", "时间", "几天", "工作日"],
            "时间": ["多久", "多长时间", "几天", "工作日"],
            # 价格相关
            "多少钱": ["价格", "费用", "资费", "多少元"],
            "价格": ["费用", "多少钱", "资费"],
            "费用": ["价格", "多少钱", "资费"],
            # 过期相关
            "过期": ["赎回", "失效", "到期", "过期了"],
            "赎回": ["过期", "赎回域名"],
            # 绑定相关
            "绑定": ["解析", "dns", "指向", "配置"],
            "解析": ["绑定", "dns", "指向"],
            # 二手相关
            "二手": ["购买", "交易", "买入", "域名交易"],
            "购买": ["买入", "交易", "二手"],
            # push 相关
            "push": ["推送", "转移", "带价 push"],
            "推送": ["push", "转移"],
            # 注册局安全锁相关
            "注册局安全锁": ["安全锁", "高级安全锁", "锁定"],
            "安全锁": ["注册局安全锁", "锁定", "保护"],
            # 疑问词扩展
            "怎么": ["方法", "流程", "步骤", "操作", "如何", "怎么做"],
            "怎么办": ["处理方法", "解决方案", "应对措施", "怎么处理", "如何解决"],
            "多久": ["时间", "时长", "周期", "几天", "工作日", "多长时间"],
            "什么": ["哪些", "内容", "详情", "何物"],
            "如何": ["怎么", "方法", "步骤", "流程"],
        }

        # 应用同义词扩展
        for original, synonyms in synonym_rules.items():
            if original in query_lower:
                expanded.extend(synonyms)

        # 特殊处理：去除疑问词，提取核心词
        question_words = ["怎么", "怎么办", "什么", "如何", "多久", "吗", "呢"]
        core_query = query_lower
        for qw in question_words:
            core_query = core_query.replace(qw, " ")
        core_query = core_query.strip()
        if core_query and len(core_query) >= 2:
            expanded.append(core_query)

        # 提取查询中的关键词（2-4 字）
        query_keywords = self._extract_chinese_words(query)
        for kw in query_keywords:
            if len(kw) >= 2 and len(kw) <= 4:
                expanded.append(kw)

        # 去重
        expanded = list(set(expanded))

        return expanded

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        搜索相关文档

        Args:
            query: 搜索查询
            top_k: 返回结果数量

        Returns:
            相关文档列表
        """
        results = []
        query_lower = query.lower()

        # 扩展查询
        expanded_queries = self._expand_query(query)

        # 提取查询中的关键词（包括扩展查询）
        query_keywords = []
        for keyword in self.document_index.keys():
            # 检查原始查询
            if keyword.lower() in query_lower:
                query_keywords.append(keyword)
            else:
                # 检查扩展查询中的关键词
                for exp_query in expanded_queries:
                    # 关键词在扩展查询中
                    if keyword.lower() in exp_query.lower():
                        if keyword not in query_keywords:
                            query_keywords.append(keyword)
                        break
                    # 扩展查询中的词在文档索引中（反向匹配）
                    for related_term in self.keyword_mapping.get(keyword, []):
                        if (
                            related_term.lower() in exp_query.lower()
                            or exp_query.lower() in related_term.lower()
                        ):
                            if keyword not in query_keywords:
                                query_keywords.append(keyword)
                            break

        # 如果没有匹配到预定义关键词，使用全文搜索
        if not query_keywords:
            return self._full_text_search(query, top_k)

        # 收集相关文档
        seen_files = set()
        for keyword in query_keywords:
            for doc_info in self.document_index.get(keyword, []):
                if doc_info["file_path"] not in seen_files:
                    seen_files.add(doc_info["file_path"])
                    # 计算查询相关性
                    with open(doc_info["file_path"], "r", encoding="utf-8") as f:
                        content = f.read()
                    doc_info["query_relevance"] = self._calculate_query_relevance(
                        content, query
                    )
                    results.append(doc_info)

        # 按相关性排序
        results.sort(key=lambda x: x["query_relevance"], reverse=True)

        return results[:top_k]

    def _calculate_query_relevance(self, content: str, query: str) -> float:
        """计算文档与查询的相关性（优化版）"""
        content_lower = content.lower()
        query_lower = query.lower()

        score = 0.0

        # ========== 1. 标题匹配（最高权重 +60 分）==========
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).lower()
            title_words = self._extract_chinese_words(title)

            # 标题中包含查询的完整词组
            query_words = self._extract_chinese_words(query)
            for word in query_words:
                if len(word) >= 3 and word in title:
                    score += 40.0  # 标题中包含 3 字以上词组
                elif len(word) >= 2 and word in title:
                    score += 20.0  # 标题中包含 2 字词组

            # 标题完整匹配查询（或部分匹配）
            if title in query_lower or query_lower in title:
                score += 30.0
            elif any(word in title for word in query_words if len(word) >= 2):
                score += 15.0

        # ========== 2. 完整查询匹配（+50 分）==========
        if query_lower in content_lower:
            score += 50.0

        # ========== 3. 提取查询中的 2-4 字词组进行匹配（每词 +2 分，上限 20 分）==========
        words = self._extract_chinese_words(query)
        word_match_score = 0.0
        for word in words:
            if len(word) >= 2 and word in content_lower:
                count = content_lower.count(word)
                word_match_score += min(count * 2.0, 10.0)  # 单个词最多 10 分
        score += min(word_match_score, 20.0)  # 词组匹配总分上限 20 分

        # ========== 4. 短文档精准匹配加成（最高 +30%）==========
        # 对于 1000-3000 字符的精准文档，给予额外加成
        content_len = len(content)
        if 800 <= content_len <= 3000:
            # 检查是否包含查询的核心关键词（前 5 个词）
            core_words = [w for w in query_words if len(w) >= 2][:5]
            if core_words and any(word in content_lower for word in core_words):
                # 计算匹配度
                match_ratio = sum(
                    1 for word in core_words if word in content_lower
                ) / len(core_words)
                if match_ratio >= 0.5:
                    score *= 1.0 + match_ratio * 0.3  # 最高 +30% 加成

        # ========== 5. 单字匹配（权重低，上限 5 分）==========
        char_score = 0.0
        for char in query_lower:
            if char.isalpha() or char.isdigit():
                count = content_lower.count(char)
                char_score += min(count * 0.1, 2.0)  # 单个字符最多 2 分
        score += min(char_score, 5.0)  # 单字匹配总分上限 5 分

        return score

    def _extract_chinese_words(self, text: str) -> List[str]:
        """
        提取中文文本中的词组（简单实现）

        策略：
        - 提取所有 2-4 个连续字符的组合
        - 过滤掉标点符号
        """
        words = []
        text = text.lower()

        # 移除标点
        clean_text = re.sub(r"[^\w\u4e00-\u9fff]", "", text)

        # 提取 2-4 字词组
        for i in range(len(clean_text) - 1):
            # 2 字词
            if i + 2 <= len(clean_text):
                words.append(clean_text[i : i + 2])
            # 3 字词
            if i + 3 <= len(clean_text):
                words.append(clean_text[i : i + 3])
            # 4 字词
            if i + 4 <= len(clean_text):
                words.append(clean_text[i : i + 4])

        # 去重
        return list(set(words))

    def _full_text_search(self, query: str, top_k: int) -> List[Dict]:
        """全文搜索"""
        results = []

        for file_path, content in self.documents.items():
            relevance = self._calculate_query_relevance(content, query)

            if relevance > 0:
                # 提取标题
                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else "Untitled"

                # 提取分类
                parts = file_path.split("/")
                category = parts[-2] if len(parts) >= 2 else "unknown"

                results.append(
                    {
                        "file_path": file_path,
                        "title": title,
                        "category": category,
                        "query_relevance": relevance,
                    }
                )

        results.sort(key=lambda x: x["query_relevance"], reverse=True)
        return results[:top_k]

    def get_document_content(self, file_path: str) -> str:
        """获取文档完整内容"""
        return self.documents.get(file_path, "")

    def get_relevant_sections(self, query: str, max_sections: int = 3) -> List[Dict]:
        """
        获取与查询最相关的文档片段

        Args:
            query: 搜索查询
            max_sections: 最大片段数量

        Returns:
            文档片段列表，包含文件路径、标题、相关片段
        """
        search_results = self.search(
            query, top_k=max_sections * 2
        )  # 多取一些，以便后续筛选

        if not search_results:
            return []

        sections = []
        for result in search_results:
            content = self.get_document_content(result["file_path"])

            # 重新计算查询相关性（更精确）
            query_relevance = self._calculate_query_relevance(content, query)

            # 提取标题
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = (
                title_match.group(1) if title_match else result.get("title", "Untitled")
            )

            # 提取分类
            parts = result["file_path"].split("/")
            category = (
                parts[-2] if len(parts) >= 2 else result.get("category", "unknown")
            )

            # 提取相关段落（简化版：返回前 500 字）
            excerpt = content[:500] + "..." if len(content) > 500 else content

            sections.append(
                {
                    "file_path": result["file_path"],
                    "title": title,
                    "category": category,
                    "excerpt": excerpt,
                    "full_content": content,
                    "query_relevance": query_relevance,
                }
            )

        # 按查询相关性重新排序
        sections.sort(key=lambda x: x["query_relevance"], reverse=True)

        return sections[:max_sections]


def format_search_results(sections: List[Dict]) -> str:
    """格式化搜索结果用于输出"""
    if not sections:
        return "未找到相关文档。"

    output = []
    output.append("📚 相关帮助文档：\n")

    for i, section in enumerate(sections, 1):
        output.append(f"{i}. **{section['title']}**")
        output.append(f"   分类：{section['category']}")
        output.append(f"   摘要：{section['excerpt'][:200]}...")
        output.append("")

    return "\n".join(output)


def answer_with_rag(query: str) -> str:
    """
    使用 RAG 检索知识库后回答问题

    Args:
        query: 用户问题

    Returns:
        基于知识库的回答
    """
    rag = DomainKnowledgeRAG()
    sections = rag.get_relevant_sections(query, max_sections=3)

    if not sections:
        return f'抱歉，未在本地知识库中找到与"{query}"相关的文档。\n\n建议：\n1. 访问阿里云帮助中心获取最新信息\n2. 检查问题描述是否清晰准确'

    # 构建回答
    answer = []
    answer.append(f'📚 根据阿里云帮助文档，关于"{query}"的相关信息：\n')

    for i, section in enumerate(sections, 1):
        answer.append(f"**{section['title']}** ({section['category']})")
        answer.append("-" * 60)

        # 提取文档的关键内容（简化版：返回前 800 字）
        content = section["full_content"]
        if len(content) > 800:
            # 尝试找到合适的截断点
            truncate_point = content.find("\n\n", 600, 800)
            if truncate_point == -1:
                truncate_point = 800
            content = content[:truncate_point] + "\n\n...（文档过长，仅显示部分内容）"

        answer.append(content)
        answer.append("")
        answer.append(f"📄 完整文档：{section['file_path']}")
        answer.append("")

    return "\n".join(answer)


# CLI 入口
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法：python3 domain_knowledge_rag.py <搜索关键词>")
        print("示例：python3 domain_knowledge_rag.py 域名注册流程")
        print("      python3 domain_knowledge_rag.py 备案需要什么材料")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"🔍 搜索：{query}\n")

    result = answer_with_rag(query)
    print(result)
