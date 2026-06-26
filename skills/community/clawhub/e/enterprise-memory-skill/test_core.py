import time
from vectorstorage import VectorStorage

def run_core_test():
    print("🚀 启动脱机版向量引擎测试 (绕过 OpenClaw 框架)...")
    
    # 1. 直接初始化底层的 VectorStorage (不依赖任何 OpenClaw 库)
    storage = VectorStorage(config_path="memory_config.yaml")
    
    print("⏳ 正在预热 BGE 向量模型 (首次可能需要下载)...")
    storage.initialize_model()
    
    # 2. 准备测试数据
    test_texts = [
        "Project Digital Craftsman 的核心理念是将材质美学与工程逻辑结合，首期项目使用了 Moonlight Beige 材质。",
        "由于 Youpin898 接口限流策略变更，量化交易机器人的轮询间隔从 3 秒调整为了 5.5 秒。",
        "2026年5月，发现 Name Shadowing 错误导致导入失败，脚本从 duckduckgo_search.py 更名为了 ddg_skill.py 解决。"
    ]
    
    # 3. 写入测试记忆
    print("\n📥 [阶段 1] 正在注入长期记忆...")
    for text in test_texts:
        # 注意：这里我们直接调用 storage 的方法
        uid = storage.add_text(text)
        print(f"  -> 写入成功, UUID: {uid}")
        
    print("\n⏳ 确保写入磁盘...\n")
    time.sleep(1)
    
    # 4. 语义检索测试
    print("🔍 [阶段 2] 极限语义召回测试...")
    queries = [
        "那个关于数字工匠的项目，最开始用了什么颜色的材料？",  
        "为什么 API 抓取速度变慢了？现在隔几秒抓一次？"
    ]
    
    for q in queries:
        print(f"\n❓ [提问]: {q}")
        results = storage.retrieve_similar(q, top_k=1)
        
        if results:
            for uid, text, score in results:
                print(f"  ✅ [命中记忆] (置信度得分: {score:.4f}):")
                print(f"     {text}")
        else:
            print("  ❌ [未命中或检索失败]")

    print("\n🛑 测试完成！")

if __name__ == "__main__":
    run_core_test()