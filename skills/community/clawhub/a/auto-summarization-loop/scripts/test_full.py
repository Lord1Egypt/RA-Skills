"""
完整测试脚本：模拟长对话触发自动摘要 - 更真实的测试
"""

import asyncio
import json
import sys
sys.path.insert(0, 'scripts')
from memory_manager import AutoSummarizationLoop, MemoryConfig, MemoryBlock, TriggerType


async def mock_summarize_fn(old_text: str, old_summary: str, max_tokens: int) -> dict:
    """模拟大模型生成摘要"""
    return {
        "summary": f"[摘要] 从 {len(old_text)} 字符压缩至 ~{max_tokens} tokens。关键点: AI发展、火星计划、Neuralink用户、Blindsight产品。",
        "user_facts": {"关注领域": "AI/航天/脑机接口", "测试": "通过"},
        "agreements": ["AGI 2027年实现", "Blindsight 2028年上市"],
        "pending_tasks": []
    }


async def test_real_scenario():
    print("=" * 60)
    print("🧪 自动摘要循环 - 真实场景测试")
    print("=" * 60)
    
    config = MemoryConfig(
        max_tokens=2000,           
        soft_limit_ratio=0.4,      # 800 tokens
        hard_limit_ratio=0.7,     # 1400 tokens
        working_messages=3,        
        summary_max_tokens=200,
        summarize_fn=mock_summarize_fn
    )
    
    manager = AutoSummarizationLoop(config)
    memory = MemoryBlock(
        core_memory="你是埃隆·马斯克，风格直接、简洁、雄心勃勃。第一性原理思考。",
        working_memory=[],
        long_term_summary=""
    )
    
    # 更长的消息内容
    long_messages = [
        "今天我们来深入讨论一下 AI 的发展趋势，你觉得未来 5 年最大的变化是什么？特别是通用人工智能的时间线。",
        "我认为 AGI 可能会在 2027-2028 年实现。关键突破点在于算力和算法的同步进化。但我们也需要考虑安全对齐问题。",
        "确实如此。SpaceX 的火星计划现在进展到什么阶段了？Starship 何时能完成首次载人任务？",
        "Starship 已经完成了多次 orbital test flight。下一次重大测试是星舰载人的演示任务。预计 2026 年底或 2027 年初。",
        "Neuralink 现在有多少用户植入了脑机接口？下一代产品的规划是怎样的？",
        "目前 Neuralink 已有约 1000 名植入者。下一代产品代号 Blindsight，针对失明患者，预计 2028 年上市。",
        "这是一个伟大的使命。关于 Optimus 人形机器人，目前的量产计划是什么？",
        "Optimus 已经在工厂进行实际工作了。预计 2026 年开始小规模量产，2027 年达到每年 1 万台。",
        "你对 xAI 和 Grok 有什么期待？",
        "Grok 3 已经展现了强大的推理能力。xAI 的目标是确保 AI 发展惠及全人类。",
        "最后一个问题，你认为人类何时能成为多行星物种？",
        "如果一切顺利，2030 年代末可能在火星建立第一个永久基地。",
        "好的，我已经记录下来。今天的讨论很有价值。",
        "谢谢。我们每次对话都在推动未来。",
    ]
    
    print(f"\n📊 max_tokens={config.max_tokens}, soft={config.soft_limit_ratio*100:.0f}%, hard={config.hard_limit_ratio*100:.0f}%")
    print(f"📊 软限制触发线: {int(config.max_tokens * config.soft_limit_ratio)} tokens\n")
    
    for i, msg in enumerate(long_messages):
        memory.working_memory.append({"role": "user", "content": msg})
        
        trigger = manager.check_watermark(memory.working_memory)
        tokens = manager.count_messages_tokens(memory.working_memory)
        
        emoji = {"normal": "✅", "soft_limit": "⚠️", "hard_limit": "🔴"}[trigger.value]
        
        # 只显示关键信息
        short_msg = msg[:30] + "..." if len(msg) > 30 else msg
        print(f"{emoji} [{tokens:>4}t] {short_msg}")
        
        if trigger != TriggerType.NORMAL:
            print(f"      → 触发 {trigger.value}! 执行压缩...")
            await manager.handle_trigger(trigger, memory)
            new_tokens = manager.count_messages_tokens(memory.working_memory)
            summary_len = len(memory.long_term_summary)
            print(f"      → 压缩后: {new_tokens} tokens, 摘要: {summary_len} chars")
        
        # 模拟助手回复
        memory.working_memory.append({"role": "assistant", "content": f"[埃隆回复]: {msg[:20]}..."})
    
    print("\n" + "=" * 60)
    print("📋 最终状态")
    print("=" * 60)
    print(f"工作记忆: {len(memory.working_memory)} 条 ({manager.count_messages_tokens(memory.working_memory)} tokens)")
    print(f"历史摘要: {memory.long_term_summary[:150]}..." if memory.long_term_summary else "无")
    print(f"用户档案: {memory.user_facts}")
    
    # 验证 Prompt 构建
    print("\n" + "=" * 60)
    print("📝 Prompt 结构预览")
    print("=" * 60)
    prompt = manager.build_prompt("下一条新消息", memory)
    print(f"共 {len(prompt)} 层:")
    for i, m in enumerate(prompt):
        role = m.get("role", "?")
        content = m.get("content", "")[:40]
        print(f"  {i+1}. [{role:8}] {content}...")


if __name__ == "__main__":
    asyncio.run(test_real_scenario())
