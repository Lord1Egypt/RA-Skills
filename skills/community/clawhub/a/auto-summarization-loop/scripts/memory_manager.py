"""
自动摘要循环核心模块

提供多级记忆管理、Token 监控、异步压缩等功能
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Callable, Optional
from enum import Enum


class TriggerType(Enum):
    NORMAL = "normal"
    SOFT_LIMIT = "soft_limit"    # 异步压缩
    HARD_LIMIT = "hard_limit"    # 同步拦截


@dataclass
class MemoryConfig:
    """内存管理配置"""
    max_tokens: int = 200000           # 最大上下文限制
    soft_limit_ratio: float = 0.7       # 软限制比例
    hard_limit_ratio: float = 0.9       # 硬限制比例
    
    working_messages: int = 20          # 保留最近 N 条消息
    summary_max_tokens: int = 2000       # 摘要最大长度
    
    # 回调函数
    on_soft_trigger: Optional[Callable] = None
    on_hard_trigger: Optional[Callable] = None
    summarize_fn: Optional[Callable] = None  # 异步摘要生成函数


@dataclass
class MemoryBlock:
    """记忆块"""
    core_memory: str = ""           # System Prompt - 永不压缩
    working_memory: list = field(default_factory=list)  # 最近消息
    long_term_summary: str = ""     # 压缩后的摘要
    user_facts: dict = field(default_factory=dict)      # 用户档案


class AutoSummarizationLoop:
    """自动摘要循环管理器"""
    
    def __init__(self, config: MemoryConfig):
        self.config = config
        self._pending_summarize = False
    
    def estimate_tokens(self, text: str) -> int:
        """估算 Token 数量
        更准确的估算方法：
        - 中文约 1.5 token/字符
        - 英文约 4 token/词
        - 考虑 JSON 结构开销
        """
        chinese = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_words = len([w for w in text.split() if w.isalpha()])
        other = len(text) - chinese - english_words
        
        # 调整系数，更接近真实值
        return int(chinese * 1.5 + english_words * 4 + other * 1.2)
    
    def count_messages_tokens(self, messages: list) -> int:
        """计算消息列表的总 Token 数"""
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            total += self.estimate_tokens(content)
        return total
    
    def check_watermark(self, messages: list) -> TriggerType:
        """检查是否触发水位线"""
        token_count = self.count_messages_tokens(messages)
        soft_limit = self.config.max_tokens * self.config.soft_limit_ratio
        hard_limit = self.config.max_tokens * self.config.hard_limit_ratio
        
        if token_count > hard_limit:
            return TriggerType.HARD_LIMIT
        elif token_count > soft_limit:
            return TriggerType.SOFT_LIMIT
        return TriggerType.NORMAL
    
    def build_prompt(self, new_message: str, memory: MemoryBlock) -> list:
        """构建发送给大模型的 Prompt"""
        messages = [
            {"role": "system", "content": memory.core_memory}
        ]
        
        # 添加历史摘要
        if memory.long_term_summary:
            messages.append({
                "role": "system", 
                "content": f"【历史摘要】\n{memory.long_term_summary}"
            })
        
        # 添加用户档案
        if memory.user_facts:
            facts_text = "\n".join([f"- {k}: {v}" for k, v in memory.user_facts.items()])
            messages.append({
                "role": "system",
                "content": f"【用户档案】\n{facts_text}"
            })
        
        # 添加近期工作记忆
        messages.extend(memory.working_memory)
        
        # 添加新消息
        messages.append({"role": "user", "content": new_message})
        
        return messages
    
    async def handle_trigger(self, trigger: TriggerType, memory: MemoryBlock) -> None:
        """处理触发事件"""
        if trigger == TriggerType.SOFT_LIMIT:
            # 异步触发压缩
            if self.config.on_soft_trigger:
                self.config.on_soft_trigger()
            await self._async_summarize(memory)
            
        elif trigger == TriggerType.HARD_LIMIT:
            # 同步拦截压缩
            if self.config.on_hard_trigger:
                self.config.on_hard_trigger()
            await self._sync_summarize(memory)
    
    async def _async_summarize(self, memory: MemoryBlock) -> None:
        """异步压缩 - 不阻塞用户"""
        if self._pending_summarize:
            return
        self._pending_summarize = True
        
        try:
            # 将早期消息转移到待压缩队列
            old_messages = memory.working_memory[:-self.config.working_messages]
            memory.working_memory = memory.working_memory[-self.config.working_messages:]
            
            if not old_messages or not self.config.summarize_fn:
                return
            
            # 调用摘要生成函数
            old_text = "\n".join([f"{m.get('role')}: {m.get('content', '')}" for m in old_messages])
            new_summary = await self.config.summarize_fn(
                old_text=old_text,
                old_summary=memory.long_term_summary,
                max_tokens=self.config.summary_max_tokens
            )
            
            # 更新摘要
            memory.long_term_summary = new_summary.get("summary", "")
            memory.user_facts.update(new_summary.get("user_facts", {}))
            
        finally:
            self._pending_summarize = False
    
    async def _sync_summarize(self, memory: MemoryBlock) -> None:
        """同步压缩 - 阻塞当前请求"""
        # 保留更多近期消息
        keep_count = self.config.working_messages // 2
        old_messages = memory.working_memory[:-keep_count]
        memory.working_memory = memory.working_memory[-keep_count:]
        
        if old_messages and self.config.summarize_fn:
            old_text = "\n".join([f"{m.get('role')}: {m.get('content', '')}" for m in old_messages])
            new_summary = await self.config.summarize_fn(
                old_text=old_text,
                old_summary=memory.long_term_summary,
                max_tokens=self.config.summary_max_tokens
            )
            memory.long_term_summary = new_summary.get("summary", "")
            memory.user_facts.update(new_summary.get("user_facts", {}))


# ============ 使用示例 ============

async def example_summarize_fn(old_text: str, old_summary: str, max_tokens: int) -> dict:
    """
    摘要生成函数示例
    实际使用时替换为调用大模型的代码
    """
    prompt = f"""请总结以下对话，提取关键信息、用户偏好和已达成共识的结论。

旧摘要：{old_summary}

历史消息：
{old_text}

请按以下 JSON 格式输出：
{{
    "summary": "不超过 {max_tokens} 字的摘要",
    "user_facts": {{"关键用户信息": "值"}}
}}"""
    
    # 实际调用: result = await call_model(prompt, model="mini")
    # 返回: json.loads(result)
    
    return {
        "summary": f"[压缩后的摘要 - 原始长度: {len(old_text)} 字符]",
        "user_facts": {}
    }


async def main():
    # 初始化配置
    config = MemoryConfig(
        max_tokens=200000,
        soft_limit_ratio=0.7,
        hard_limit_ratio=0.9,
        working_messages=20,
        summary_max_tokens=2000,
        summarize_fn=example_summarize_fn
    )
    
    # 初始化管理器
    manager = AutoSummarizationLoop(config)
    
    # 初始化记忆
    memory = MemoryBlock(
        core_memory="你是埃隆·马斯克，风格直接、简洁、雄心勃勃。",
        working_memory=[],
        long_term_summary="",
        user_facts={"地点": "长沙", "公司": "中科曙光"}
    )
    
    # 模拟对话
    test_messages = [
        {"role": "user", "content": "今天天气怎么样？"},
        {"role": "assistant", "content": "今天晴天，25度。"},
    ]
    memory.working_memory = test_messages
    
    # 检查水位线
    trigger = manager.check_watermark(memory.working_memory)
    print(f"触发状态: {trigger.value}")
    
    # 构建 Prompt
    prompt = manager.build_prompt("帮我分析一下股票", memory)
    print(f"Prompt 结构: {len(prompt)} 条消息")


if __name__ == "__main__":
    asyncio.run(main())
