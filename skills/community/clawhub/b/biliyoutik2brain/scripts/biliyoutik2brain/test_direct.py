import sys, os, time, json

# 保证 workspace 在路径中
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE = os.path.dirname(_SCRIPT_DIR)
if _WORKSPACE not in sys.path:
    sys.path.insert(0, _WORKSPACE)

# 禁用排队+槽位检查
import biliyoutik2brain.core.config as cfg
cfg.queue_light = lambda url: None
cfg.schedule_pending = lambda wf_id: None
cfg.acquire_light_slot = lambda: True
cfg.release_light_slot = lambda: None
cfg.dequeue_light = lambda: None

from biliyoutik2brain.core.pipeline import process

def run():
    url = "https://www.bilibili.com/video/BV1529aBSETF"
    print(f"[熊猫测试] {url}")
    
    # P1: 检查知识库
    know_file = os.path.expanduser("~/openclaw/workspace/storage/knowledge/熊猫技术分析社区.md")
    if os.path.exists(know_file):
        ksize = os.path.getsize(know_file)
        print(f"[P1] 知识库: 熊猫技术分析社区.md ({ksize}字节)")
    else:
        print("[P1] ⚠️ 知识库不存在")
    
    start = time.time()
    result = process(url)
    elapsed = time.time() - start
    
    if result and not result.error:
        print(f"\n✅ 完成: {elapsed:.1f}s")
        print(f"文本: {len(result.plain_text)}字")
        if result.analysis:
            print(f"分析: {json.dumps(result.analysis, ensure_ascii=False)[:300]}")
    else:
        print(f"\n❌ 失败: {result.error if result else 'None'}")

run()
