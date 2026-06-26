"""
Chatbot Engine - 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from chatbot import ChatBot, Message
from intent_classifier import IntentClassifier
from knowledge_base import KnowledgeBase, Document
from llm_adapter import LLMAdapter


class TestChatBot(unittest.TestCase):
    """测试对话机器人"""
    
    def setUp(self):
        self.bot = ChatBot()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.bot)
        self.assertEqual(len(self.bot.history), 0)
    
    def test_chat(self):
        """测试对话"""
        response = self.bot.chat("你好")
        self.assertIsInstance(response, str)
        self.assertEqual(len(self.bot.history), 2)  # user + assistant
    
    def test_clear_context(self):
        """测试清空上下文"""
        self.bot.chat("你好")
        self.bot.clear_context()
        self.assertEqual(len(self.bot.history), 0)


class TestIntentClassifier(unittest.TestCase):
    """测试意图分类器"""
    
    def setUp(self):
        self.classifier = IntentClassifier()
        self.classifier.add_intent('greeting', ['你好', '您好'], ['你好'])
        self.classifier.add_intent('farewell', ['再见', '拜拜'], ['再见'])
    
    def test_classify_greeting(self):
        """测试问候意图"""
        result = self.classifier.classify("你好")
        self.assertEqual(result['intent'], 'greeting')
        self.assertGreater(result['confidence'], 0)
    
    def test_classify_unknown(self):
        """测试未知意图"""
        result = self.classifier.classify("xyz123")
        self.assertEqual(result['intent'], 'unknown')


class TestKnowledgeBase(unittest.TestCase):
    """测试知识库"""
    
    def setUp(self):
        self.kb = KnowledgeBase()
    
    def test_add_document(self):
        """测试添加文档"""
        doc_id = self.kb.add_document("问题", "答案")
        self.assertIsNotNone(doc_id)
        self.assertEqual(self.kb.get_stats()['total_documents'], 1)
    
    def test_query(self):
        """测试查询"""
        self.kb.add_document("营业时间是什么？", "9:00-18:00")
        answer = self.kb.query("你们几点开门？")
        self.assertIsNotNone(answer)
    
    def test_query_empty(self):
        """测试空知识库查询"""
        answer = self.kb.query("问题")
        self.assertIsNone(answer)


class TestLLMAdapter(unittest.TestCase):
    """测试LLM适配器"""
    
    def test_mock_provider(self):
        """测试模拟提供商"""
        llm = LLMAdapter(provider='mock')
        response = llm.generate("你好")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
