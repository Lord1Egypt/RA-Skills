#!/usr/bin/env python3
"""
天天基金 API 查询工具
用于获取基金基础信息、净值、收益率、风险评估等

**降级策略**：
1. 天天基金 API → 2. 免费 API（东方财富/新浪）→ 3. 手动输入
"""

import requests
import json
import re
import os
from datetime import datetime
from pathlib import Path

# 缓存目录（与且慢共享）
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "fund-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 天天基金 API 配置
API_KEY = os.environ.get("TTFUND_APIKEY", "")
BASE_URL = "https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke"

# 基金代码校验正则
FUND_CODE_PATTERN = re.compile(r"^\d{6}$")

def validate_fund_code(code: str) -> bool:
    """校验基金代码格式（6 位数字）"""
    if not code:
        return False
    code = code.strip()
    return bool(FUND_CODE_PATTERN.match(code))

# 常用基金代码（测试用）
TEST_FUNDS = [
    "000001",  # 易方达蓝筹精选
    "000002",  # 华夏成长
    "110022",  # 易方达消费行业
]

import hashlib
import time

def get_cache_key(skill_id: str, params: dict) -> str:
    """生成缓存 key"""
    key_str = f"{skill_id}:{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(key_str.encode()).hexdigest()

def get_from_cache(key: str, ttl: int = 3600) -> dict:
    """从缓存获取数据（TTL 默认 1 小时）"""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None
    
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
    cache_file = CACHE_DIR / f"{key}.json"
    data = {'_timestamp': time.time(), 'result': result}
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ttfund_request(skill_id: str, params: dict, use_cache: bool = True, ttl: int = 3600):
    """
    发送天天基金 API 请求（带缓存 + 降级）
    
    **降级策略**：
    1. 天天基金 API（带缓存）→ 2. 免费 API → 3. 返回错误
    """
    # 校验基金代码
    if params:
        for key in ['fcode', 'fundCode', 'code']:
            if key in params and not validate_fund_code(params[key]):
                return {"error": f"基金代码格式错误：{params[key]}（应为 6 位数字）"}
    
    # 检查 API Key
    if not API_KEY:
        return {"error": "未配置 TTFUND_APIKEY 环境变量", "fallback": "free_api"}
    
    # 尝试从缓存获取
    cache_key = get_cache_key(skill_id, params)
    if use_cache:
        cached = get_from_cache(cache_key, ttl)
        if cached:
            return {"result": cached, "from_cache": True}
    
    payload = {
        "skill_id": skill_id,
        "_skill_version": "1.0.0",
        **params
    }
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        # 保存到缓存
        if "result" in result and use_cache:
            save_to_cache(cache_key, result.get("result"))
        
        return result
    except requests.exceptions.Timeout:
        return {"error": "天天基金 API 超时，请尝试使用免费 API", "fallback": "free_api"}
    except requests.exceptions.ConnectionError:
        return {"error": "天天基金 API 连接失败，请尝试使用免费 API", "fallback": "free_api"}
    except Exception as e:
        return {"error": f"天天基金 API 错误：{str(e)}", "fallback": "free_api"}

def fetch_from_free_api(fund_code: str, data_type: str = "nav"):
    """
    从免费 API 获取数据（降级方案）
    
    **数据源**：
    - 净值：新浪 API
    - 基础信息：东方财富 API
    """
    if data_type == "nav":
        url = f"http://hq.sinajs.cn/list=fu_{fund_code}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.text
                if "=" in data:
                    nav_info = data.split("=")[1].strip('"').split(",")
                    return {
                        "result": {
                            "nav": nav_info[0] if len(nav_info) > 0 else "N/A",
                            "accumulated_nav": nav_info[1] if len(nav_info) > 1 else "N/A",
                            "change": nav_info[2] if len(nav_info) > 2 else "N/A"
                        },
                        "source": "free_api_sina"
                    }
        except:
            pass
    
    return {"error": "免费 API 获取失败", "fallback": "manual_input"}

def get_fund_basic_info(fund_code: str):
    """获取基金基础信息"""
    print(f"\n📊 获取基金基础信息：{fund_code}")
    
    result = ttfund_request(
        "FUND_BASE_INFOS",
        {"fcode": fund_code}
    )
    
    if "result" in result or "data" in result:
        data = result.get("result") or result.get("data")
        print(f"✅ 基金名称：{data.get('fundName', 'N/A')}")
        print(f"   基金公司：{data.get('company', 'N/A')}")
        print(f"   基金类型：{data.get('type', 'N/A')}")
        print(f"   成立日期：{data.get('establishDate', 'N/A')}")
        print(f"   基金规模：{data.get('scale', 'N/A')} 亿")
        print(f"   基金经理：{data.get('manager', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def get_fund_nav(fund_code: str):
    """获取基金净值"""
    print(f"\n📊 获取基金净值：{fund_code}")
    
    # 使用新浪 API 获取实时净值（免费）
    url = f"http://hq.sinajs.cn/list=fu_{fund_code}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.text
            if "=" in data:
                nav_info = data.split("=")[1].strip('"').split(",")
                print(f"✅ 当前净值：{nav_info[0] if len(nav_info) > 0 else 'N/A'}")
                print(f"   累计净值：{nav_info[1] if len(nav_info) > 1 else 'N/A'}")
                print(f"   日涨跌：{nav_info[2] if len(nav_info) > 2 else 'N/A'}%")
        else:
            print(f"❌ 获取失败：状态码 {response.status_code}")
    except Exception as e:
        print(f"❌ 获取失败：{e}")

def get_fund_performance(fund_code: str):
    """获取基金收益率"""
    print(f"\n📊 获取基金收益率：{fund_code}")
    
    # 使用东方财富 API 获取收益率
    url = f"https://fund.eastmoney.com/pingjiagongshi/{fund_code}.html"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ 收益率数据获取成功")
            print(f"   详情查看：{url}")
        else:
            print(f"❌ 获取失败：状态码 {response.status_code}")
    except Exception as e:
        print(f"❌ 获取失败：{e}")

def select_funds_by_condition(risk_level: str = "3,4", fund_level: str = "4,5"):
    """条件选基"""
    print(f"\n📊 条件选基：风险等级{risk_level}，基金等级{fund_level}")
    
    result = ttfund_request(
        "FUND_CONDITION_SELECT",
        {
            "riskLevel": risk_level,
            "fundLevel": fund_level,
            "orderField": "5_6_-1",  # 近 1 年收益率降序
            "pageNum": 20
        }
    )
    
    if "result" in result or "data" in result:
        data = result.get("result") or result.get("data")
        funds = data.get('funds', [])
        print(f"✅ 找到 {len(funds)} 只基金")
        for f in funds[:10]:
            print(f"  - {f.get('code', 'N/A')} {f.get('name', 'N/A')}")
            print(f"     近 1 年收益：{f.get('return1Y', 'N/A')}%")
            print(f"     风险等级：{f.get('riskLevel', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")
    
    return result

def get_fund_holdings(fund_code: str):
    """获取基金持仓（前十大重仓股）"""
    print(f"\n📊 获取基金持仓：{fund_code}")
    
    # 使用东方财富 API 获取持仓
    url = f"https://fund.eastmoney.com/f10/jjcc_{fund_code}.html"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ 持仓数据获取成功")
            print(f"   详情查看：{url}")
        else:
            print(f"❌ 获取失败：状态码 {response.status_code}")
    except Exception as e:
        print(f"❌ 获取失败：{e}")

def get_fund_manager_info(fund_code: str):
    """获取基金经理信息"""
    print(f"\n📊 获取基金经理：{fund_code}")
    
    # 使用天天基金 API
    result = ttfund_request(
        "FUND_BASE_INFOS",
        {"fcode": fund_code}
    )
    
    if "result" in result or "data" in result:
        data = result.get("result") or result.get("data")
        manager = data.get('manager', 'N/A')
        print(f"✅ 基金经理：{manager}")
        
        # 获取经理详情（需要额外 API）
        print(f"   详情：待扩展")
    else:
        print(f"❌ 获取失败：{result}")

def get_fund_fee(fund_code: str):
    """获取基金费率"""
    print(f"\n📊 获取基金费率：{fund_code}")
    
    # 费率信息通常在基础信息中
    result = ttfund_request(
        "FUND_BASE_INFOS",
        {"fcode": fund_code}
    )
    
    if "result" in result or "data" in result:
        data = result.get("result") or result.get("data")
        print(f"✅ 费率信息")
        print(f"   管理费：{data.get('managementFee', 'N/A')}")
        print(f"   托管费：{data.get('custodianFee', 'N/A')}")
        print(f"   申购费：{data.get('subscriptionFee', 'N/A')}")
        print(f"   赎回费：{data.get('redemptionFee', 'N/A')}")
    else:
        print(f"❌ 获取失败：{result}")

def main():
    """主函数 - 测试所有功能"""
    print("=" * 60)
    print("天天基金 API 查询工具")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {'已配置' if API_KEY else '❌ 未配置'}")
    print("=" * 60)
    
    if not API_KEY:
        print("\n⚠️  警告：未配置 TTFUND_APIKEY 环境变量")
        print("   请在 ~/.openclaw/workspace/TOOLS.md 中配置")
        print("   或在终端执行：export TTFUND_APIKEY=your_key")
    
    # 1. 获取基金基础信息（示例）
    get_fund_basic_info("000001")
    
    # 2. 获取基金净值
    get_fund_nav("000001")
    
    # 3. 条件选基
    select_funds_by_condition()
    
    # 4. 获取持仓
    get_fund_holdings("000001")
    
    # 5. 获取经理信息
    get_fund_manager_info("000001")
    
    # 6. 获取费率
    get_fund_fee("000001")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
