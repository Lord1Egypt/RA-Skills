#!/usr/bin/env python3
"""
GitHub 知识库检索 - 从 wdndev/llm_interview_note 获取面试素材

功能：
- 搜索知识点
- 获取内容并生成面试题
- 与 interview.py 集成

使用方式：
python3 fetch.py "LoRA"                    # 搜索知识点
python3 fetch.py --list-topics            # 列出所有知识点
python3 fetch.py --random                 # 随机获取一个知识点
python3 fetch.py --questions "transformer" # 搜索并生成面试题
"""

import json
import random
import subprocess
import os
import re
from typing import List, Dict, Optional
from urllib.parse import quote


# ============================================================
# 配置
# ============================================================
GITHUB_REPO = "wdndev/llm_interview_note"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

# 章节分类映射
TOPIC_CATEGORIES = {
    "01": "大语言模型基础",
    "02": "大语言模型架构",
    "03": "训练数据集",
    "04": "分布式训练",
    "05": "有监督微调",
    "06": "推理",
    "07": "强化学习",
    "08": "检索增强RAG",
    "09": "大语言模型评估",
    "10": "大语言模型应用",
}

# 完整知识点列表（覆盖 01-10 全部章节）
HOT_TOPICS = [
    # ========== 01. 大语言模型基础 ==========
    {"id": "word2vec", "path": "01.大语言模型基础/Word2Vec/Word2Vec.md", "title": "Word2Vec", "category": "大语言模型基础"},
    {"id": "nlp_feature", "path": "01.大语言模型基础/NLP三大特征抽取器（CNN-RNN-TF）/NLP三大特征抽取器（CNN-RNN-TF）.md", "title": "NLP三大特征抽取器", "category": "大语言模型基础"},
    {"id": "decoder_only", "path": "01.大语言模型基础/LLM为什么Decoder only架构/LLM为什么Decoder only架构.md", "title": "LLM为什么Decoder only架构", "category": "大语言模型基础"},
    {"id": "lm", "path": "01.大语言模型基础/1.语言模型/语言模型.md", "title": "语言模型", "category": "大语言模型基础"},
    {"id": "token", "path": "01.大语言模型基础/分词/token/分词.md", "title": "分词", "category": "大语言模型基础"},
    {"id": "jieba", "path": "01.大语言模型基础/分词/jieba分词用法及原理/jieba分词用法及原理.md", "title": "jieba分词", "category": "大语言模型基础"},
    {"id": "pos", "path": "01.大语言模型基础/分词/词性标注/词性标注.md", "title": "词性标注", "category": "大语言模型基础"},
    {"id": "dep", "path": "01.大语言模型基础/分词/句法分析/句法分析.md", "title": "句法分析", "category": "大语言模型基础"},
    {"id": "embedding", "path": "01.大语言模型基础/分词/词向量/词向量.md", "title": "词向量", "category": "大语言模型基础"},
    {"id": "activation", "path": "01.大语言模型基础/深度学习/激活函数/激活函数.md", "title": "激活函数", "category": "大语言模型基础"},

    # ========== 02. 大语言模型架构 ==========
    {"id": "attention", "path": "02.大语言模型架构/1.attention/1.attention.md", "title": "Attention机制", "category": "大语言模型架构"},
    {"id": "layernorm", "path": "02.大语言模型架构/2.layer_normalization/2.layer_normalization.md", "title": "Layer Normalization", "category": "大语言模型架构"},
    {"id": "position_encoding", "path": "02.大语言模型架构/3.位置编码/3.位置编码.md", "title": "位置编码", "category": "大语言模型架构"},
    {"id": "tokenize", "path": "02.大语言模型架构/4.tokenize分词/4.tokenize分词.md", "title": "Tokenize分词", "category": "大语言模型架构"},
    {"id": "mha_mqa_gqa", "path": "02.大语言模型架构/MHA_MQA_GQA/MHA_MQA_GQA.md", "title": "MHA/MQA/GQA", "category": "大语言模型架构"},
    {"id": "decode_strategy", "path": "02.大语言模型架构/解码策略（Top-k & Top-p & Temperatu/解码策略（Top-k & Top-p & Temperature）.md", "title": "解码策略(Top-k/Top-p/Temperature)", "category": "大语言模型架构"},
    {"id": "bert", "path": "02.大语言模型架构/bert细节/bert细节.md", "title": "BERT细节", "category": "大语言模型架构"},
    {"id": "transformer", "path": "02.大语言模型架构/Transformer架构细节/Transformer架构细节.md", "title": "Transformer架构", "category": "大语言模型架构"},
    {"id": "llama", "path": "02.大语言模型架构/llama系列模型/llama系列模型.md", "title": "LLaMA系列模型", "category": "大语言模型架构"},
    {"id": "chatglm", "path": "02.大语言模型架构/chatglm系列模型/chatglm系列模型.md", "title": "ChatGLM系列模型", "category": "大语言模型架构"},
    {"id": "moe", "path": "02.大语言模型架构/1.MoE论文/1.MoE论文.md", "title": "MoE混合专家", "category": "大语言模型架构"},
    {"id": "switch_transformer", "path": "02.大语言模型架构/3.LLM MoE：Switch Transformers/3.LLM MoE：Switch Transformers.md", "title": "Switch Transformers", "category": "大语言模型架构"},

    # ========== 03. 训练数据集 ==========
    {"id": "dataset_format", "path": "03.训练数据集/数据格式/数据格式.md", "title": "训练数据格式", "category": "训练数据集"},
    {"id": "dataset_size", "path": "03.训练数据集/模型参数/模型参数.md", "title": "模型参数量与数据量", "category": "训练数据集"},

    # ========== 04. 分布式训练 ==========
    {"id": "dist_overview", "path": "04.分布式训练/1.概述/1.概述.md", "title": "分布式训练概述", "category": "分布式训练"},
    {"id": "dp", "path": "04.分布式训练/2.数据并行/2.数据并行.md", "title": "数据并行", "category": "分布式训练"},
    {"id": "pp", "path": "04.分布式训练/3.流水线并行/3.流水线并行.md", "title": "流水线并行", "category": "分布式训练"},
    {"id": "tp", "path": "04.分布式训练/4.张量并行/4.张量并行.md", "title": "张量并行", "category": "分布式训练"},
    {"id": "sp", "path": "04.分布式训练/5.序列并行/5.序列并行.md", "title": "序列并行", "category": "分布式训练"},
    {"id": "auto_parallel", "path": "04.分布式训练/7.自动并行/7.自动并行.md", "title": "自动并行", "category": "分布式训练"},
    {"id": "moe_parallel", "path": "04.分布式训练/8.moe并行/8.moe并行.md", "title": "MoE并行", "category": "分布式训练"},
    {"id": "deepspeed", "path": "04.分布式训练/deepspeed介绍/deepspeed介绍.md", "title": "DeepSpeed", "category": "分布式训练"},
    {"id": "megatron", "path": "04.分布式训练/Megatron/Megatron.md", "title": "Megatron", "category": "分布式训练"},
    {"id": "train_optimize", "path": "04.分布式训练/训练加速/训练加速.md", "title": "训练加速技术", "category": "分布式训练"},

    # ========== 05. 有监督微调 ==========
    {"id": "sft_basic", "path": "05.有监督微调/1.基本概念/1.基本概念.md", "title": "微调基本概念", "category": "有监督微调"},
    {"id": "prompting", "path": "05.有监督微调/2.prompting/2.prompting.md", "title": "Prompting", "category": "有监督微调"},
    {"id": "adapter", "path": "05.有监督微调/3.adapter-tuning/3.adapter-tuning.md", "title": "Adapter-Tuning", "category": "有监督微调"},
    {"id": "lora", "path": "05.有监督微调/4.lora/4.lora.md", "title": "LoRA", "category": "有监督微调"},
    {"id": "sft_summary", "path": "05.有监督微调/5.总结/5.总结.md", "title": "微调总结", "category": "有监督微调"},
    {"id": "llama_sft", "path": "05.有监督微调/llama2微调/llama2微调.md", "title": "LLaMA2微调", "category": "有监督微调"},
    {"id": "chatglm_sft", "path": "05.有监督微调/ChatGLM3微调/ChatGLM3微调.md", "title": "ChatGLM3微调", "category": "有监督微调"},

    # ========== 06. 推理 ==========
    {"id": "inference_framework", "path": "06.推理/0.llm推理框架简单总结/0.llm推理框架简单总结.md", "title": "LLM推理框架", "category": "推理"},
    {"id": "vllm", "path": "06.推理/1.vllm/1.vllm.md", "title": "vLLM", "category": "推理"},
    {"id": "tgi", "path": "06.推理/2.text_generation_inference/2.text_generation_inference.md", "title": "TGI", "category": "推理"},
    {"id": "faster_transformer", "path": "06.推理/3.faster_transformer/3.faster_transformer.md", "title": "FasterTransformer", "category": "推理"},
    {"id": "trt_llm", "path": "06.推理/4.trt_llm/4.trt_llm.md", "title": "TensorRT-LLM", "category": "推理"},
    {"id": "inference_optimize", "path": "06.推理/llm推理优化技术/llm推理优化技术.md", "title": "推理优化技术", "category": "推理"},
    {"id": "quantize", "path": "06.推理/量化/量化.md", "title": "量化技术", "category": "推理"},

    # ========== 07. 强化学习 ==========
    {"id": "pg", "path": "07.强化学习/策略梯度（pg）/策略梯度（pg）.md", "title": "策略梯度", "category": "强化学习"},
    {"id": "ppo", "path": "07.强化学习/近端策略优化(ppo)/近端策略优化(ppo).md", "title": "PPO近端策略优化", "category": "强化学习"},
    {"id": "rlhf", "path": "07.强化学习/RLHF/RLHF.md", "title": "RLHF原理", "category": "强化学习"},
    {"id": "dpo", "path": "07.强化学习/DPO/DPO.md", "title": "DPO", "category": "强化学习"},

    # ========== 08. 检索增强RAG ==========
    {"id": "rag", "path": "08.检索增强rag/检索增强llm/检索增强llm.md", "title": "检索增强LLM", "category": "检索增强RAG"},
    {"id": "rag_detail", "path": "08.检索增强rag/rag（检索增强生成）技术/rag（检索增强生成）技术.md", "title": "RAG技术详解", "category": "检索增强RAG"},
    {"id": "agent", "path": "08.检索增强rag/大模型agent技术/大模型agent技术.md", "title": "Agent技术", "category": "检索增强RAG"},

    # ========== 09. 大语言模型评估 ==========
    {"id": "llm_eval", "path": "09.大语言模型评估/1.评测/1.评测.md", "title": "LLM评测", "category": "大语言模型评估"},
    {"id": "hallucination", "path": "09.大语言模型评估/1.大模型幻觉/1.大模型幻觉.md", "title": "LLM幻觉", "category": "大语言模型评估"},
    {"id": "hallucination_source", "path": "09.大语言模型评估/2.幻觉来源与缓解/2.幻觉来源与缓解.md", "title": "幻觉来源与缓解", "category": "大语言模型评估"},

    # ========== 10. 大语言模型应用 ==========
    {"id": "cot", "path": "10.大语言模型应用/1.思维链提示/1.思维链（cot）.md", "title": "思维链(CoT)", "category": "大语言模型应用"},
    {"id": "langchain", "path": "10.大语言模型应用/2.LangChain框架/1.langchain/langchain.md", "title": "LangChain", "category": "大语言模型应用"},
]


# ============================================================
# 核心函数
# ============================================================

def fetch_github_content(path: str) -> Optional[str]:
    """
    从 GitHub Raw 获取文件内容

    Args:
        path: 文件路径（相对于仓库根目录）

    Returns:
        文件内容，失败返回 None
    """
    url = f"{GITHUB_RAW_BASE}/{quote(path)}"

    try:
        result = subprocess.run(
            ["curl", "-s", "-L", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            # 检查是否返回了 HTML（404 或重定向到页面）
            if "<html" in result.stdout.lower() or result.stdout.strip() == "404: Not Found":
                return None
            return result.stdout
    except Exception as e:
        print(f"获取内容失败: {e}")

    return None


def search_topics(keyword: str, limit: int = 5, category: str = None) -> List[Dict]:
    """
    改进的知识点搜索（支持章节路径匹配）

    Args:
        keyword: 搜索关键词
        limit: 返回数量
        category: 可选，限定分类

    Returns:
        匹配的知识点列表
    """
    keyword_lower = keyword.lower()
    results = []

    for topic in HOT_TOPICS:
        # 如果指定了分类，只搜索该分类
        if category and topic["category"] != category:
            continue

        title = topic["title"].lower()
        category_lower = topic["category"].lower()
        path = topic["path"].lower()

        score = 0

        # 1. 标题完全包含关键词（最高）
        if keyword_lower in title:
            score = 100
        # 2. 章节路径匹配
        elif keyword_lower in path:
            score = 90
        # 3. 分类匹配
        elif keyword_lower in category_lower:
            score = 80
        # 4. 关键词在标题的任意单词中
        elif any(word in title for word in keyword_lower.split()):
            score = 60
        # 5. 关键词的部分匹配
        else:
            # 检查关键词的每个字符是否在标题中
            match_chars = sum(1 for c in keyword_lower if c in title)
            if match_chars > len(keyword_lower) * 0.5:
                score = 30

        if score > 0:
            results.append({
                **topic,
                "similarity_score": score
            })

    # 按相似度排序
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return results[:limit]


def search_by_category(category_keyword: str, limit: int = 10) -> List[Dict]:
    """
    按分类搜索知识点

    Args:
        category_keyword: 分类关键词（如 "微调"、"分布式"）
        limit: 返回数量

    Returns:
        该分类下的知识点列表
    """
    results = []
    for topic in HOT_TOPICS:
        cat = topic["category"].lower()
        if category_keyword.lower() in cat:
            results.append(topic)

    return random.sample(results, min(limit, len(results))) if results else results


def get_topic_content(topic_id: str) -> Optional[Dict]:
    """
    获取知识点内容

    Args:
        topic_id: 知识点ID

    Returns:
        知识点详情（包含内容）
    """
    for topic in HOT_TOPICS:
        if topic["id"] == topic_id:
            content = fetch_github_content(topic["path"])
            return {
                **topic,
                "content": content,
                "url": f"https://github.com/{GITHUB_REPO}/blob/main/{topic['path']}"
            }
    return None


def get_random_topic() -> Dict:
    """
    随机获取一个知识点

    Returns:
        随机知识点详情
    """
    topic = random.choice(HOT_TOPICS)
    content = fetch_github_content(topic["path"])
    return {
        **topic,
        "content": content,
        "url": f"https://github.com/{GITHUB_REPO}/blob/main/{topic['path']}"
    }


def extract_key_points(content: str) -> List[str]:
    """
    从内容中提取关键知识点/术语

    Args:
        content: Markdown 内容

    Returns:
        关键知识点列表
    """
    if not content:
        return []

    key_points = []
    lines = content.split("\n")

    for line in lines:
        line = line.strip()
        # 提取 ## 标题作为关键点
        if line.startswith("## "):
            point = line.lstrip("#").strip()
            if len(point) > 2 and len(point) < 50:
                key_points.append(point)
        # 提取加粗文本
        elif line.startswith("**") and "**" in line[2:]:
            match = re.search(r'\*\*(.+?)\*\*', line)
            if match:
                point = match.group(1).strip()
                if len(point) > 1:
                    key_points.append(point)

    # 去重并限制数量
    seen = set()
    unique_points = []
    for p in key_points:
        p_lower = p.lower()
        if p_lower not in seen and len(p) < 100:
            seen.add(p_lower)
            unique_points.append(p)

    return unique_points[:10]


def extract_questions_from_content(content: str, max_questions: int = 5) -> List[Dict]:
    """
    从内容中提取可能的面试题

    Args:
        content: Markdown 内容
        max_questions: 最大题目数

    Returns:
        题目列表
    """
    if not content:
        return []

    questions = []
    lines = content.split("\n")

    for line in lines:
        line = line.strip()
        # 匹配 ## 或 ### 标题
        if line.startswith("## ") or line.startswith("### "):
            question = line.lstrip("#").strip()
            # 过滤太短的标题和参考/相关章节
            if (len(question) > 5 and
                not question.startswith("参考") and
                not question.startswith("相关") and
                not question.startswith("参考") and
                "参考链接" not in question):
                questions.append({
                    "question": question,
                    "type": "概念题"
                })

        if len(questions) >= max_questions:
            break

    return questions


def list_all_topics() -> List[Dict]:
    """
    列出所有知识点

    Returns:
        知识点列表
    """
    return HOT_TOPICS


def list_categories() -> Dict[str, int]:
    """
    列出所有分类及数量

    Returns:
        分类统计
    """
    categories = {}
    for topic in HOT_TOPICS:
        cat = topic["category"]
        categories[cat] = categories.get(cat, 0) + 1
    return categories


# ============================================================
# 与 interview.py 集成接口
# ============================================================

def github_search_questions(keyword: str, count: int = 3) -> List[Dict]:
    """
    搜索知识点并生成面试题格式（与 interview.py 对接）

    Args:
        keyword: 搜索关键词
        count: 返回题目数量

    Returns:
        面试题列表，格式与 interview.py 一致
    """
    results = search_topics(keyword, limit=count)
    questions = []

    for topic in results:
        content = fetch_github_content(topic["path"])
        key_points = extract_key_points(content or "")

        questions.append({
            "title": topic["title"],
            "key_points": key_points,
            "type": "八股",
            "category": topic["category"],
            "difficulty": _guess_difficulty(topic["category"]),
            "source": "github",
            "topic_id": topic["id"],
            "content_preview": (content or "")[:1500] if content else None,
            "url": f"https://github.com/{GITHUB_REPO}/blob/main/{topic['path']}"
        })

    return questions


def github_get_questions_by_category(category: str, count: int = 3) -> List[Dict]:
    """
    按分类获取面试题

    Args:
        category: 分类名称（如 "有监督微调"、"强化学习"）
        count: 返回题目数量

    Returns:
        面试题列表
    """
    # 先搜索该分类下的知识点
    topics = search_by_category(category, limit=count)
    return github_search_questions(topics[0]["title"] if topics else category, count=count)


def github_random_questions(count: int = 3) -> List[Dict]:
    """
    随机获取面试题

    Args:
        count: 返回题目数量

    Returns:
        面试题列表
    """
    questions = []
    for _ in range(count):
        topic = random.choice(HOT_TOPICS)
        content = fetch_github_content(topic["path"])
        key_points = extract_key_points(content or "")

        questions.append({
            "title": topic["title"],
            "key_points": key_points,
            "type": "八股",
            "category": topic["category"],
            "difficulty": _guess_difficulty(topic["category"]),
            "source": "github",
            "topic_id": topic["id"],
            "content_preview": (content or "")[:1500] if content else None,
            "url": f"https://github.com/{GITHUB_REPO}/blob/main/{topic['path']}"
        })

    return questions


def _guess_difficulty(category: str) -> str:
    """根据分类猜测难度"""
    hard_cats = ["分布式训练", "强化学习", "推理"]
    medium_cats = ["大语言模型架构", "有监督微调", "大语言模型评估"]

    if category in hard_cats:
        return "较难"
    elif category in medium_cats:
        return "中等"
    else:
        return "基础"


# ============================================================
# 命令行接口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GitHub 知识库检索 - LLM面试")
    parser.add_argument("keyword", nargs="?", help="搜索关键词")
    parser.add_argument("--limit", "-n", type=int, default=5, help="返回数量")
    parser.add_argument("--topic", "-t", help="获取指定知识点内容")
    parser.add_argument("--list-topics", action="store_true", help="列出所有知识点")
    parser.add_argument("--list-categories", action="store_true", help="列出所有分类")
    parser.add_argument("--random", action="store_true", help="随机获取一个知识点")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--questions", "-q", action="store_true", help="搜索并生成面试题")
    parser.add_argument("--by-category", "-c", help="按分类获取（如：强化学习）")

    args = parser.parse_args()

    if args.list_categories:
        categories = list_categories()
        print("📚 知识点分类统计：")
        for cat, count in categories.items():
            print(f"  - {cat}: {count} 个知识点")

    elif args.list_topics:
        topics = list_all_topics()
        if args.json:
            print(json.dumps(topics, ensure_ascii=False, indent=2))
        else:
            print("📚 所有知识点（共 {} 个）：".format(len(topics)))
            for topic in topics:
                print(f"  [{topic['id']}] {topic['title']} ({topic['category']})")

    elif args.random:
        if args.questions:
            questions = github_random_questions(args.limit)
            if args.json:
                print(json.dumps(questions, ensure_ascii=False, indent=2))
            else:
                for i, q in enumerate(questions, 1):
                    print(f"\n【题目{i}】{q['title']}")
                    print(f"分类: {q['category']} | 难度: {q['difficulty']}")
                    print(f"关键点: {', '.join(q['key_points'][:5])}")
        else:
            topic = get_random_topic()
            if args.json:
                output = {k: v for k, v in topic.items() if k != "content"}
                output["content_length"] = len(topic.get("content", "") or "")
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                print(f"\n{'='*50}")
                print(f"📖 {topic['title']}")
                print(f"{'='*50}")
                print(f"📂 分类: {topic['category']}")
                print(f"🔗 链接: {topic['url']}")
                if topic.get("content"):
                    print(f"\n{topic['content'][:2000]}...")

    elif args.by_category:
        topics = search_by_category(args.by_category, args.limit)
        if args.json:
            print(json.dumps(topics, ensure_ascii=False, indent=2))
        else:
            print(f"📚 分类「{args.by_category}」下的知识点：")
            for topic in topics:
                print(f"  [{topic['id']}] {topic['title']}")

    elif args.topic:
        topic = get_topic_content(args.topic)
        if topic:
            if args.json:
                output = {k: v for k, v in topic.items() if k != "content"}
                output["content_length"] = len(topic.get("content", "") or "")
                print(json.dumps(output, ensure_ascii=False, indent=2))
            elif args.questions:
                questions = extract_questions_from_content(topic.get("content", ""))
                print(f"\n📝 从「{topic['title']}」提取的面试题：")
                for i, q in enumerate(questions, 1):
                    print(f"{i}. {q['question']}")
            else:
                print(f"\n{'='*50}")
                print(f"📖 {topic['title']}")
                print(f"{'='*50}")
                print(f"📂 分类: {topic['category']}")
                print(f"🔗 链接: {topic['url']}")
                if topic.get("content"):
                    print(f"\n{topic['content']}")
        else:
            print(f"❌ 未找到知识点: {args.topic}")

    elif args.questions:
        questions = github_search_questions(args.keyword or "transformer", args.limit)
        if args.json:
            print(json.dumps(questions, ensure_ascii=False, indent=2))
        else:
            for i, q in enumerate(questions, 1):
                print(f"\n{'='*50}")
                print(f"【题目{i}】{q['title']}")
                print(f"{'='*50}")
                print(f"📂 分类: {q['category']} | 难度: {q['difficulty']}")
                print(f"🔗 链接: {q['url']}")
                print(f"\n关键点: {', '.join(q['key_points'][:5]) if q['key_points'] else '无'}")
                if q.get('content_preview'):
                    print(f"\n内容预览: {q['content_preview'][:300]}...")

    elif args.keyword:
        results = search_topics(args.keyword, args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"🔍 找到 {len(results)} 个相关知识点：\n")
            for i, topic in enumerate(results, 1):
                print(f"{i}. [{topic['id']}] {topic['title']}")
                print(f"   分类: {topic['category']} | 相似度: {topic['similarity_score']}%")
                print()

    else:
        parser.print_help()
