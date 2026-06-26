"""
ChatBot - 智能对话机器人
"""

from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
import json
import os


@dataclass
class Message:
    """对话消息"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class ChatBot:
    """智能对话机器人"""
    
    def __init__(self, llm_adapter=None, knowledge_base=None,
                 context_length: int = 10):
        self.llm_adapter = llm_adapter
        self.knowledge_base = knowledge_base
        self.context_length = context_length
        self.history: List[Message] = []
        self.plugins: Dict[str, Any] = {}
        self.intent_classifier = None
    
    def chat(self, message: str) -> str:
        """
        发送消息并获取回复
        
        Args:
            message: 用户消息
        
        Returns:
            机器人回复
        """
        # 添加到历史
        self.history.append(Message('user', message))
        
        # 检查是否需要使用插件
        plugin_result = self._try_plugins(message)
        if plugin_result:
            self.history.append(Message('assistant', plugin_result))
            return plugin_result
        
        # 检查知识库
        if self.knowledge_base:
            kb_answer = self.knowledge_base.query(message)
            if kb_answer:
                response = kb_answer
                self.history.append(Message('assistant', response))
                return response
        
        # 使用LLM生成回复
        if self.llm_adapter:
            context = self._build_context()
            response = self.llm_adapter.generate(message, context=context)
        else:
            response = "我理解您的问题，但我需要更多信息来回答。"
        
        self.history.append(Message('assistant', response))
        return response
    
    def _build_context(self) -> List[Dict]:
        """构建上下文"""
        recent = self.history[-self.context_length * 2:]
        context = []
        for msg in recent:
            context.append({'role': msg.role, 'content': msg.content})
        return context
    
    def _try_plugins(self, message: str) -> Optional[str]:
        """尝试使用插件处理消息"""
        for name, plugin in self.plugins.items():
            if plugin.can_handle(message):
                return plugin.handle(message)
        return None
    
    def register_plugin(self, plugin: Any):
        """注册插件"""
        self.plugins[plugin.name] = plugin
        print(f"插件已注册: {plugin.name}")
    
    def clear_context(self):
        """清空上下文"""
        self.history = []
    
    def get_history(self) -> List[Message]:
        """获取对话历史"""
        return self.history
    
    def save_session(self, path: str):
        """保存对话会话"""
        data = [
            {'role': m.role, 'content': m.content, 'timestamp': m.timestamp}
            for m in self.history
        ]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"会话已保存: {path}")
    
    def load_session(self, path: str):
        """加载对话会话"""
        if not os.path.exists(path):
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.history = [
            Message(m['role'], m['content'], m.get('timestamp', 0))
            for m in data
        ]
        print(f"会话已加载: {path}")


if __name__ == '__main__':
    bot = ChatBot()
    response = bot.chat("你好")
    print(f"Bot: {response}")
