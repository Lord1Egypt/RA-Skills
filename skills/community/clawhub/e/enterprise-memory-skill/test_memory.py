import time
from main_skill import EnterpriseMemorySkill

def run_memory_test():
    print("🚀 启动 Enterprise Memory 引擎测试...")
    
    # 1. 初始化引擎
    skill = EnterpriseMemorySkill()
    skill.on_startup() # 触发配置加载和向量模型预热
    
    # 2. 准备“虚构事实”，避免与 LLM 自身预训练知识混淆
    test_memories = [
        {"text": "Project Digital Craftsman 的核心理念是将材质美学与工程逻辑结合，首期项目使用了 Moonlight Beige 材质。", "confidence": 0.95},
        {"text": "由于 Youpin898 接口限流策略变更，量化交易机器人的轮询间隔从 3 秒调整为了 5.5 秒。", "confidence": 0.90},
        {"text": "2026年5月，发现 Name Shadowing 错误导致导入失败，脚本从 duckduckgo_search.py 更名为了 ddg_skill.py 解决。", "confidence": 0.99}
    ]
    
    # 3. 写入测试记忆
    print("\n📥 [阶段 1] 正在注入长期记忆...")
    for mem in test_memories:
        res = skill.execute_action("remember", mem)
        print(f"  -> 写入状态: {res.get('status')}, ID: {res.get('id')}")
        
    print("\n⏳ 模拟时间流逝 (确保写入磁盘)...\n")
    time.sleep(1)
    
    # 4. 语义检索测试 (故意使用口语化、不包含原关键词的提问)
    print("🔍 [阶段 2] 极限语义召回测试...")
    
    queries = [
        "那个关于数字工匠的项目，最开始用了什么颜色的材料？",  # 测试: 跨语种/同义词映射 (材料 -> 材质/Moonlight Beige)
        "为什么 API 抓取速度变慢了？现在隔几秒抓一次？",         # 测试: 业务逻辑理解 (限流/轮询间隔 -> 速度/隔几秒)
        "之前那个变量名冲突的 Bug 是咋修复的？"                  # 测试: 抽象概念 (变量名冲突 -> Name Shadowing)
    ]
    
    for q in queries:
        print(f"\n❓ [提问]: {q}")
        # 测试提取 Top 1 的最相关记忆
        recall_res = skill.execute_action("recall", {"query": q, "top_k": 1})
        
        if recall_res.get("status") == "success" and recall_res.get("results"):
            for item in recall_res.get("results"):
                print(f"  ✅ [命中记忆] (置信度得分: {item['score']:.4f}):")
                print(f"     {item['text']}")
        else:
            print("  ❌ [未命中或检索失败]")

    # 5. 关闭引擎，测试优雅退出
    skill.on_shutdown()
    print("\n🛑 测试完成，数据已持久化至 vectors.db")

if __name__ == "__main__":
    run_memory_test()