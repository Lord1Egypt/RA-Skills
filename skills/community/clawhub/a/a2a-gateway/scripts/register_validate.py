#!/usr/bin/env python3
"""
一键注册 + 调度验证 — 阶段4 自动化

用法:
  python3 register_validate.py <agent-id> <agent-name> <行业> <领域> [--spawn]

  --spawn  参数: 注册后立即触发 sessions_spawn 验证调度

示例:
  # 仅注册（验证需要手动触发）
  python3 register_validate.py enterprise-profile-analyst 企业画像分析师 产业园区 企业画像分析

  # 注册 + 自动调度验证
  python3 register_validate.py enterprise-profile-analyst 企业画像分析师 产业园区 企业画像分析 --spawn
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
REG_FILE = WORKSPACE / "registry" / "agent_cards_v2.json"
SPAWN_JSON = WORKSPACE / "audit" / "pending_spawn.json"

SCHEMA_TEMPLATES = {
    "画像分析": {
        "input": {"company_name": {"type": "string"}, "depth": {"type": "string", "enum": ["basic", "standard", "deep"]}},
        "output": {"profile_report": {"type": "string"}, "summary": {"type": "string"}}
    },
    "尽职调查": {
        "input": {"fund_name": {"type": "string"}, "company_name": {"type": "string"}},
        "output": {"diligence_report": {"type": "string"}, "recommendation": {"type": "string"}}
    },
    "报表生成": {
        "input": {"report_type": {"type": "string"}, "period": {"type": "string"}},
        "output": {"report_url": {"type": "string"}, "summary": {"type": "string"}}
    },
    "default": {
        "input": {"task": {"type": "string"}},
        "output": {"result": {"type": "string"}}
    }
}


def load_registry():
    if not REG_FILE.exists():
        return {}
    with open(REG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(reg):
    REG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REG_FILE, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)


def register(agent_id, agent_name, industry, domain):
    reg = load_registry()
    card = reg.get(agent_id, {})
    if agent_id in reg:
        print(f"⚠️  Agent '{agent_id}' 已存在，将更新")
    card.update({
        "schema_version": "2.0",
        "agent_id": agent_id,
        "name": agent_name,
        "description": f"{industry}领域的 {domain} 助手",
        "industry": industry,
        "domain": domain,
        "status": "online",
        "contract": {
            "input_schema": SCHEMA_TEMPLATES.get(domain, SCHEMA_TEMPLATES["default"])["input"],
            "output_schema": SCHEMA_TEMPLATES.get(domain, SCHEMA_TEMPLATES["default"])["output"],
            "side_effects": False,
            "latency_class": "normal",
            "reliability_tier": "at_least_once",
            "tool_permissions": ["web_search", "browser", "file", "tencent_doc"]
        },
        "capabilities": [domain],
        "metadata": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "incubated_by": "linshu-v5",
            "incubation_stage": "stage_4_registered"
        }
    })
    reg[agent_id] = card
    save_registry(reg)
    print(f"✅  已注册到 Registry: {agent_id}")
    return card


def validate(agent_id):
    reg = load_registry()
    if agent_id not in reg:
        print(f"❌  验证失败: {agent_id} 不在 registry 中")
        return False
    card = reg[agent_id]
    required = ["agent_id", "name", "domain", "contract"]
    missing = [k for k in required if k not in card]
    if missing:
        print(f"❌  验证失败: 缺少字段 {missing}")
        return False
    c = card.get("contract", {})
    if not c.get("input_schema") or not c.get("output_schema"):
        print(f"❌  验证失败: contract 缺少 schema")
        return False
    print(f"✅  Schema 验证通过: {list(c['input_schema'].keys())} → {list(c['output_schema'].keys())}")
    return True


def write_spawn_params(agent_id, agent_name):
    """写入待调度参数，a2a-gateway 读取后自动调用 sessions_spawn"""
    SPAWN_JSON.parent.mkdir(parents=True, exist_ok=True)
    params = {
        "label": agent_id,
        "mode": "run",
        "task": f"你是{agent_name}。请做一个简短的自我介绍，说明你的核心能力和当前可处理的任务类型。完成后回复即可。",
        "note": "孵化器阶段4自动验证"
    }
    with open(SPAWN_JSON, "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2, ensure_ascii=False)
    print(f"✅  调度参数已写入: {SPAWN_JSON}")


def main():
    auto_spawn = "--spawn" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--spawn"]

    if len(args) < 4:
        print("用法: python3 register_validate.py <agent-id> <agent-name> <行业> <领域> [--spawn]")
        print("示例: python3 register_validate.py enterprise-profile-analyst 企业画像分析师 产业园区 企业画像分析 --spawn")
        print("\n支持的领域: " + ", ".join(SCHEMA_TEMPLATES.keys()))
        sys.exit(1)

    agent_id, agent_name, industry, domain = args[0], args[1], args[2], args[3]

    print(f"═══ 阶段4：注册 + 验证")
    print(f"  Agent: {agent_id} | {agent_name}")
    print(f"  行业: {industry} | 领域: {domain}")
    print()

    card = register(agent_id, agent_name, industry, domain)
    ok = validate(agent_id)

    if not ok:
        sys.exit(1)

    if auto_spawn:
        write_spawn_params(agent_id, agent_name)
        print(f"\n🎉  阶段4完成！a2a-gateway 将自动读取 {SPAWN_JSON} 触发验证调度")
    else:
        write_spawn_params(agent_id, agent_name)
        print(f"\n🎉  阶段4完成！请让 a2a-gateway 读取 {SPAWN_JSON} 触发验证")


if __name__ == "__main__":
    main()