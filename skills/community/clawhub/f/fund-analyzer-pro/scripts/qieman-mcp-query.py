#!/usr/bin/env python3
"""
且慢 MCP 基金分析查询工具
用于获取基金投顾策略数据、持仓明细、收益归因等

**降级策略**：
1. 且慢 MCP → 2. 天天基金 API → 3. 免费 API（东方财富/新浪）→ 4. 手动输入
"""

import requests
import json
import re
import os
from datetime import datetime
from pathlib import Path

# 缓存目录
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "fund-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 且慢 MCP 配置
MCP_CONFIG = {
    "url": "https://stargate.yingmi.com/mcp/v2",
    "headers": {
        "x-api-key": "rySVkZpwsubI_uExeTZuGg",
        "Accept": "application/json, text/event-stream"
    }
}

# 基金代码校验正则
FUND_CODE_PATTERN = re.compile(r"^\d{6}$")

def validate_fund_code(code: str) -> bool:
    """校验基金代码格式（6 位数字）"""
    if not code:
        return False
    code = code.strip()
    return bool(FUND_CODE_PATTERN.match(code))

def get_cache_key(method: str, params: dict) -> str:
    """生成缓存 key"""
    import hashlib
    key_str = f"{method}:{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(key_str.encode()).hexdigest()

def get_from_cache(key: str, ttl: int = 3600) -> dict:
    """从缓存获取数据（TTL 默认 1 小时）"""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None
    
    import time
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if time.time() - data.get('_timestamp', 0) < ttl:
                return data.get('result')
    except:
        pass
    return None

def save_to_cache(key: str, result: dict):
    """保存到缓存"""
    import time
    cache_file = CACHE_DIR / f"{key}.json"
    data = {'_timestamp': time.time(), 'result': result}
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def mcp_request(method: str, params: dict = None, use_cache: bool = True, ttl: int = 3600):
    """
    发送 MCP 请求（带缓存 + 降级）
    
    **降级策略**：
    1. 且慢 MCP（带缓存）→ 2. 返回错误（由上层调用天天基金 API）
    """
    # 校验基金代码（如果参数中有）
    if params:
        for key in ['fundCode', 'strategyCode', 'fcode']:
            if key in params and not validate_fund_code(params[key]):
                return {"error": f"基金代码格式错误：{params[key]}（应为 6 位数字）"}
    
    # 尝试从缓存获取
    cache_key = get_cache_key(method, params or {})
    if use_cache:
        cached = get_from_cache(cache_key, ttl)
        if cached:
            return {"result": cached, "from_cache": True}
    
    # 发送请求
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    try:
        response = requests.post(
            MCP_CONFIG["url"],
            headers=MCP_CONFIG["headers"],
            json=payload,
            timeout=30
        )
        result = response.json()
        
        # 保存到缓存
        if "result" in result and use_cache:
            save_to_cache(cache_key, result.get("result"))
        
        return result
    except requests.exceptions.Timeout:
        return {"error": "且慢 MCP 超时，请尝试使用天天基金 API", "fallback": "ttfund"}
    except requests.exceptions.ConnectionError:
        return {"error": "且慢 MCP 连接失败，请尝试使用天天基金 API", "fallback": "ttfund"}
    except Exception as e:
        return {"error": f"且慢 MCP 错误：{str(e)}", "fallback": "ttfund"}

def list_tools():
    """列出 MCP 服务可用的工具"""
    print("🔍 正在连接且慢 MCP 服务...")
    result = mcp_request("tools/list")
    
    if "result" in result:
        print(f"✅ 可用工具数量：{len(result['result'].get('tools', []))}")
        for tool in result['result'].get('tools', []):
            print(f"  - {tool.get('name', 'Unknown')}")
    else:
        print(f"❌ 获取工具失败：{result}")
    
    return result

def search_strategies(keyword: str = ""):
    """搜索投顾策略"""
    print(f"\n📊 搜索投顾策略：{keyword or '全部'}")
    
    result = mcp_request(
        "StrategySearchByKeyword",
        {"keyword": keyword}
    )
    
    if "result" in result:
        strategies = result['result'].get('strategies', [])
        print(f"✅ 找到 {len(strategies)} 个策略")
        for s in strategies[:5]:  # 显示前 5 个
            print(f"  - {s.get('name', 'N/A')} ({s.get('code', 'N/A')})")
    else:
        print(f"❌ 搜索失败：{result}")
    
    return result

def get_strategy_details(strategy_code: str):
    """获取策略详情"""
    print(f"\n📊 获取策略详情：{strategy_code}")
    
    result = mcp_request(
        "GetStrategyDetails",
        {"strategyCode": strategy_code}
    )
    
    if "result" in result:
        data = result['result']
        print(f"✅ 策略名称：{data.get('name', 'N/A')}")
        print(f"   收益率：{data.get('returnRate', 'N/A')}")
        print(f"   最大回撤：{data.get('maxDrawdown', 'N/A')}")
        print(f"   管理人：{data.get('manager', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def get_strategy_composition(strategy_code: str):
    """获取策略持仓明细"""
    print(f"\n📊 获取策略持仓：{strategy_code}")
    
    result = mcp_request(
        "BatchGetStrategiesComposition",
        {"strategyCodes": [strategy_code]}
    )
    
    if "result" in result:
        data = result['result']
        print(f"✅ 持仓数据获取成功")
        # 打印持仓结构
        if 'holdings' in data:
            print(f"   持仓基金数：{len(data['holdings'])}")
            for h in data['holdings'][:5]:
                print(f"   - {h.get('fundName', 'N/A')}: {h.get('weight', 'N/A')}%")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def get_strategy_risk(strategy_code: str):
    """获取策略风险信息"""
    print(f"\n📊 获取策略风险：{strategy_code}")
    
    result = mcp_request(
        "GetStrategyRiskInfo",
        {"strategyCode": strategy_code}
    )
    
    if "result" in result:
        data = result['result']
        print(f"✅ 风险数据获取成功")
        print(f"   夏普比率：{data.get('sharpeRatio', 'N/A')}")
        print(f"   波动率：{data.get('volatility', 'N/A')}")
        print(f"   最大回撤：{data.get('maxDrawdown', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def get_fund_campisi(fund_code: str):
    """债券收益归因（Campisi）"""
    print(f"\n📊 债券收益归因：{fund_code}")
    
    result = mcp_request(
        "getFundCampisiIndicator",
        {"fundCode": fund_code}
    )
    
    if "result" in result:
        data = result['result']
        print(f"✅ Campisi 归因获取成功")
        print(f"   总收益：{data.get('totalReturn', 'N/A')}")
        print(f"   利率贡献：{data.get('rateContribution', 'N/A')}")
        print(f"   信用贡献：{data.get('creditContribution', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def get_fund_brinson(fund_code: str):
    """股票收益归因（Brinson）"""
    print(f"\n📊 股票收益归因：{fund_code}")
    
    result = mcp_request(
        "getFundBrinsonIndicator",
        {"fundCode": fund_code}
    )
    
    if "result" in result:
        data = result['result']
        print(f"✅ Brinson 归因获取成功")
        print(f"   总收益：{data.get('totalReturn', 'N/A')}")
        print(f"   配置贡献：{data.get('allocationContribution', 'N/A')}")
        print(f"   选股贡献：{data.get('selectionContribution', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def main():
    """主函数 - 测试所有功能"""
    print("=" * 60)
    print("且慢 MCP 基金分析查询工具")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 列出工具
    list_tools()
    
    # 2. 搜索策略（示例：搜索"稳健"）
    search_strategies("稳健")
    
    # 3. 获取策略详情（示例代码，需替换为真实代码）
    # get_strategy_details("XXXXXX")
    
    # 4. 获取持仓明细
    # get_strategy_composition("XXXXXX")
    
    # 5. 获取风险信息
    # get_strategy_risk("XXXXXX")
    
    # 6. 收益归因
    # get_fund_campisi("XXXXXX")
    # get_fund_brinson("XXXXXX")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
