"""AgentMem 快速入门示例"""
from agent_mem.core.hot_cache import write_conversation, query_recent, status

# 1. 写入记忆
write_conversation("main", "webchat", "用户询问了记忆系统功能", importance=7)
write_conversation("main", "webchat", "用户偏好简洁的技术型回答", importance=8)

# 2. 跨通道查询
print("=== 跨通道记忆查询 ===")
memories = query_recent("main", limit=5)
for m in memories:
    print(f"  [{m['channel']}] {m['text']}")

# 3. 查看系统状态
print("\n=== HOT缓存状态 ===")
st = status()
print(f"  总Agent数: {st.get('agents', 0)}")
print(f"  总条目数: {st.get('total_entries', 0)}")
