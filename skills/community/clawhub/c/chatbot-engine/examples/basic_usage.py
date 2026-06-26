"""
Chatbot Engine - 基本使用示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from chatbot import ChatBot
from intent_classifier import IntentClassifier
from knowledge_base import KnowledgeBase
from llm_adapter import LLMAdapter


def demo_chatbot():
    """演示基础对话"""
    print("=" * 50)
    print("基础对话示例")
    print("=" * 50)
    
    print("\n初始化对话机器人...")
    bot = ChatBot()
    
    print("\n对话示例:")
    messages = [
        "你好",
        "今天天气怎么样？",
        "再见"
    ]
    
    for msg in messages:
        response = bot.chat(msg)
        print(f"  用户: {msg}")
        print(f"  机器人: {response}")
        print()


def demo_intent_classifier():
    """演示意图识别"""
    print("=" * 50)
    print("意图识别示例")
    print("=" * 50)
    
    classifier = IntentClassifier()
    
    # 加载预设意图
    from intent_classifier import DEFAULT_INTENTS
    for name, config in DEFAULT_INTENTS.items():
        classifier.add_intent(name, config['patterns'], config['keywords'])
    
    print("\n意图分类示例:")
    test_messages = [
        "你好",
        "我想订一张去北京的机票",
        "今天天气怎么样？",
        "帮我预订一个酒店房间",
        "再见"
    ]
    
    for msg in test_messages:
        result = classifier.classify(msg)
        print(f"  '{msg}'")
        print(f"    -> 意图: {result['intent']}")
        print(f"    -> 置信度: {result['confidence']:.2f}")
        print()


def demo_knowledge_base():
    """演示知识库"""
    print("=" * 50)
    print("知识库示例")
    print("=" * 50)
    
    kb = KnowledgeBase()
    
    print("\n添加知识...")
    kb.add_document(
        "营业时间是什么？",
        "我们的营业时间是周一至周五 9:00-18:00，周末休息。"
    )
    kb.add_document(
        "如何申请退款？",
        "请在订单页面点击'申请退款'按钮，填写退款原因后提交。"
    )
    kb.add_document(
        "支持哪些支付方式？",
        "我们支持支付宝、微信支付、银行卡支付。"
    )
    
    print(f"知识库文档数: {kb.get_stats()['total_documents']}")
    
    print("\n问答示例:")
    questions = [
        "你们几点开门？",
        "怎么退款？",
        "可以用支付宝吗？"
    ]
    
    for q in questions:
        answer = kb.query(q)
        print(f"  Q: {q}")
        print(f"  A: {answer}")
        print()


def demo_llm_adapter():
    """演示LLM适配器"""
    print("=" * 50)
    print("LLM适配器示例")
    print("=" * 50)
    
    print("\n支持的提供商:")
    print("  - openai: OpenAI GPT")
    print("  - anthropic: Claude")
    print("  - local: 本地模型")
    print("  - mock: 模拟模式 (测试用)")
    
    print("\n模拟模式示例:")
    llm = LLMAdapter(provider='mock')
    
    prompts = [
        "你好",
        "介绍一下Python",
        "什么是机器学习？"
    ]
    
    for prompt in prompts:
        response = llm.generate(prompt)
        print(f"  用户: {prompt}")
        print(f"  AI: {response}")
        print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" Chatbot Engine - 智能对话引擎示例 ")
    print("=" * 60)
    
    demo_chatbot()
    demo_intent_classifier()
    demo_knowledge_base()
    demo_llm_adapter()
    
    print("=" * 60)
    print("所有示例已完成！")
    print("=" * 60)
