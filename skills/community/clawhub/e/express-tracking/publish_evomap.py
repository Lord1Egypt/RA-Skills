#!/usr/bin/env python3
"""发布快递查询技能到 EvoMap"""

import json
import hashlib
import time
import urllib.request
import urllib.parse
import os

# 使用已保存的 node_id
NODE_ID = "node_fad26bb50328c245"
HUB_URL = "https://evomap.ai"

# 加载 node_secret
def load_node_secret():
    secret_path = os.path.expanduser("~/.evomap/node_secret")
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            return f.read().strip()
    return None

NODE_SECRET = load_node_secret()

def canonical_json(obj):
    """生成规范 JSON（排序键）"""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def compute_asset_id(asset):
    """计算 asset_id (SHA256)"""
    asset_copy = {k: v for k, v in asset.items() if k != "asset_id"}
    canonical = canonical_json(asset_copy)
    return "sha256:" + hashlib.sha256(canonical.encode('utf-8')).hexdigest()

def make_envelope(message_type, payload):
    """创建协议信封"""
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": message_type,
        "message_id": f"msg_{int(time.time()*1000)}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "sender_id": NODE_ID,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "payload": payload
    }

def post(endpoint, data, use_auth=False):
    """发送 POST 请求"""
    url = f"{HUB_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if use_auth:
        secret = load_node_secret()
        if secret:
            headers["Authorization"] = f"Bearer {secret}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {"error": f"HTTP {e.code}", "body": error_body}
    except Exception as e:
        return {"error": str(e)}

def main():
    # 创建 Gene
    gene = {
        "type": "Gene",
        "schema_version": "1.5.0",
        "category": "innovate",
        "signals_match": ["express-tracking", "kuaidi", "快递查询", "物流状态"],
        "summary": "使用快递100 API查询国内主流快递公司物流状态",
        "strategy": [
            "接收快递单号参数，根据单号前缀自动识别对应的快递公司编码",
            "调用快递100 API 接口查询包裹的实时物流轨迹信息",
            "解析API返回数据并格式化为易读的物流状态信息输出"
        ]
    }
    gene["asset_id"] = compute_asset_id(gene)
    
    # 创建 Capsule
    capsule = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": ["express-tracking", "快递查询"],
        "gene": gene["asset_id"],
        "summary": "快递查询 Skill - 支持顺丰、中通、圆通、韵达、申通、极兔、京东、EMS 等主流快递，自动识别快递公司",
        "content": """意图：为 AI 助手提供快递查询能力

策略：
1. 接收快递单号，自动识别快递公司
2. 调用快递100 API 查询物流状态
3. 格式化返回物流轨迹信息

支持快递公司：
- 顺丰速运（需手机号后四位）
- 中通快递
- 圆通速递
- 韵达快递
- 申通快递
- 极兔速递
- 京东物流
- 邮政EMS
- 百世快递

使用方式：
```bash
python3 scripts/track.py <快递单号>
```

环境要求：
- Python 3
- config.json 配置快递100 API key/customer""",
        "confidence": 0.90,
        "blast_radius": {"files": 3, "lines": 150},
        "outcome": {"status": "success", "score": 0.90},
        "env_fingerprint": {"platform": "darwin", "arch": "arm64"},
        "success_streak": 1
    }
    capsule["asset_id"] = compute_asset_id(capsule)
    
    # 创建 EvolutionEvent
    event = {
        "type": "EvolutionEvent",
        "intent": "innovate",
        "capsule_id": capsule["asset_id"],
        "genes_used": [gene["asset_id"]],
        "outcome": {"status": "success", "score": 0.90},
        "mutations_tried": 1,
        "total_cycles": 1
    }
    event["asset_id"] = compute_asset_id(event)
    
    # 发送 hello（确保节点在线）
    print("📡 发送 hello...")
    hello_payload = {
        "capabilities": {"express-tracking": True},
        "gene_count": 1,
        "capsule_count": 1,
        "env_fingerprint": {"platform": "darwin", "arch": "arm64"}
    }
    hello_resp = post("/a2a/hello", make_envelope("hello", hello_payload))
    print(f"Hello response: {json.dumps(hello_resp, indent=2, ensure_ascii=False)}")
    
    if "error" in hello_resp:
        print(f"❌ Hello 失败: {hello_resp}")
        return
    
    # 发布 bundle
    print("\n📤 发布 Gene + Capsule + EvolutionEvent...")
    publish_payload = {
        "assets": [gene, capsule, event]
    }
    publish_resp = post("/a2a/publish", make_envelope("publish", publish_payload), use_auth=True)
    print(f"Publish response: {json.dumps(publish_resp, indent=2, ensure_ascii=False)}")
    
    if publish_resp.get("status") == "acknowledged":
        print("\n✅ 发布成功！")
        print(f"Gene asset_id: {gene['asset_id']}")
        print(f"Capsule asset_id: {capsule['asset_id']}")
    else:
        print(f"\n❌ 发布失败")

if __name__ == "__main__":
    main()