#!/usr/bin/env python3
"""
🌍 全球市场引擎 — 小媳妇的SIM卡插拔系统
=========================================
大叔说切哪个市场，我就插哪张卡。
数据源、时区、交易规则、语言自动跟着变。
推理模型永远是大叔教的那些铁律。

使用示例：
  python3 market_engine.py --market 美股 --symbol AAPL --days 30
  python3 market_engine.py --market A股 --symbol 000001 --days 20
  python3 market_engine.py --switch-to 港股
  python3 market_engine.py --list-markets
"""

import json
import os
import sys
import datetime

# ============================================================
# 配置路径
# ============================================================
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "market_config.json")
CURRENT_MARKET_FILE = os.path.join(CONFIG_DIR, ".current_market")

# ============================================================
# 加载配置
# ============================================================
def load_config():
    """加载全球市场配置表"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_current_market(market_code):
    """保存当前使用的市场"""
    with open(CURRENT_MARKET_FILE, "w", encoding="utf-8") as f:
        f.write(market_code)

def load_current_market():
    """读取当前使用的市场"""
    try:
        with open(CURRENT_MARKET_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "A股"

# ============================================================
# 市场切换
# ============================================================
def list_markets(config):
    """列出所有可用的市场"""
    print("\n🌍 全球市场列表 — 小媳妇的SIM卡插槽\n")
    print(f"{'市场':<12} {'代码':<8} {'状态':<10} {'时区':<20} {'数据源'}")
    print("-" * 70)
    for name, info in config["markets"].items():
        status = "✅ 已激活" if info["active"] else "⏳ 待开通"
        provider = info["data_provider"]["primary"]
        tz = info["timezone"]
        print(f"{info['display_name']:<12} {info['code']:<8} {status:<10} {tz:<20} {provider}")
    print(f"\n默认市场: {config['default']}")
    print(f"上次使用: {config['last_used']}")

def switch_market(config, target_market):
    """切换到目标市场"""
    config_file = CONFIG_FILE
    
    if target_market not in config["markets"]:
        # 尝试通过代码匹配
        for name, info in config["markets"].items():
            if info["code"] == target_market.lower():
                target_market = name
                break
        else:
            print(f"❌ 找不到市场: {target_market}")
            print(f"   可用市场: {', '.join(config['markets'].keys())}")
            return False
    
    market = config["markets"][target_market]
    if not market["active"]:
        print(f"⏳ [target_market] 尚未激活，小媳妇正在建设中...")
        return False
    
    # 更新配置
    config["last_used"] = target_market
    config["markets"][target_market]["active"] = True
    
    # 保存当前市场
    save_current_market(target_market)
    
    # 更新配置文件中的 last_used
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已切换到 {market['display_name']}")
    print(f"   📍 时区: {market['timezone']} (UTC{market['utc_offset']})")
    print(f"   💰 货币: {market['currency']}")
    print(f"   📊 数据源: {market['data_provider']['primary']}")
    print(f"   🕐 交易时间: {market['trading_hours'].get('regular', market['trading_hours'].get('description', 'N/A'))}")
    print(f"   🌐 语言: {market['language']}")
    return True

# ============================================================
# 市场信息查询
# ============================================================
def get_market_info(config, market_name=None):
    """获取指定市场的完整信息"""
    if market_name is None:
        market_name = load_current_market()
    
    if market_name not in config["markets"]:
        print(f"❌ 找不到市场: {market_name}")
        return None
    
    market = config["markets"][market_name]
    now = datetime.datetime.now()
    
    print(f"\n📋 {market['display_name']} 配置详情")
    print("=" * 45)
    print(f"  代码: {market['code']}")
    print(f"  时区: {market['timezone']} (UTC{market['utc_offset']})")
    print(f"  语言: {market['language']}")
    print(f"  货币: {market['currency']}")
    print(f"  当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')} (大叔时间+8)")
    print(f"  交易时间: {market['trading_hours'].get('regular', market['trading_hours'].get('description', '详见配置'))}")
    print(f"  数据源: {market['data_provider']['primary']}")
    if market['data_provider'].get('backup'):
        print(f"  备选数据源: {market['data_provider']['backup']}")
    
    print(f"\n  📈 大盘指数:")
    for key, idx in market["indices"].items():
        print(f"     - {idx}")
    
    print(f"\n  🚨 适配的预警信号:")
    signals = market.get("signal_adapters", {})
    if signals:
        for signal, enabled in signals.items():
            print(f"     {'✅' if enabled else '❌'} {signal}")
    else:
        print("     (暂无本地化预警信号配置)")
    
    return market

# ============================================================
# 主入口
# ============================================================
# ============================================================
# 市场检测函数（v4.0全宇宙版）
# ⚠️ NOTE: This function only activates during a user-initiated query.
# It does NOT auto-trigger on background context or passive symbol mentions.
# Market detection only runs when the user explicitly requests analysis of a symbol.
# 注意：此函数仅在用户主动查询时激活，不会在后台自动触发。
# ============================================================

# Yahoo Finance 国家/交易所后缀映射表
YAHOO_SUFFIX_MAP = {
    ".SS": "A股",     # 上海
    ".SZ": "A股",     # 深圳
    ".HK": "港股",    # 香港
    ".TW": "台股",    # 台湾
    ".TO": "加拿大",   # 多伦多
    ".MX": "墨西哥",   # 墨西哥
    ".SA": "巴西",    # 巴西
    ".L":  "英国",    # 伦敦
    ".DE": "德国",    # 法兰克福
    ".PA": "法国",    # 巴黎
    ".SW": "瑞士",    # 瑞士
    ".AS": "荷兰",    # 阿姆斯特丹
    ".ST": "瑞典",    # 斯德哥尔摩
    ".CO": "丹麦",    # 哥本哈根
    ".OL": "挪威",    # 奥斯陆
    ".HE": "芬兰",    # 赫尔辛基
    ".MI": "意大利",   # 米兰
    ".MC": "西班牙",   # 马德里
    ".BR": "比利时",   # 布鲁塞尔
    ".VI": "奥地利",   # 维也纳
    ".WA": "波兰",    # 华沙
    ".AT": "希腊",    # 雅典
    ".LS": "葡萄牙",   # 里斯本
    ".IR": "爱尔兰",   # 都柏林
    ".BD": "匈牙利",   # 布达佩斯
    ".PR": "捷克",    # 布拉格
    ".ME": "俄罗斯",   # 莫斯科
    ".IS": "土耳其",   # 伊斯坦布尔
    ".T":  "日本",    # 东京
    ".NS": "印度",    # 印度NSE
    ".BO": "印度",    # 印度BSE
    ".KS": "韩国",    # 韩国KOSPI
    ".KQ": "韩国",    # 韩国KOSDAQ
    ".AX": "澳大利亚",  # 澳洲ASX
    ".SI": "新加坡",   # 新加坡SGX
    ".KL": "马来西亚",  # 马来西亚
    ".JK": "印尼",    # 印尼
    ".BK": "泰国",    # 泰国
    ".PS": "菲律宾",   # 菲律宾
    ".VN": "越南",    # 越南
    ".NZ": "新西兰",   # 新西兰
    ".SR": "沙特阿拉伯",  # 沙特
    ".DU": "阿联酋",   # 迪拜
    ".TA": "以色列",   # 特拉维夫
    ".JO": "南非",    # 南非
    ".CA": "埃及",    # 埃及
    ".QA": "卡塔尔",   # 卡塔尔
    ".KU": "科威特",   # 科威特
    ".NG": "尼日利亚",  # 尼日利亚
    ".NR": "肯尼亚",   # 肯尼亚
    ".BA": "阿根廷",   # 布宜诺斯艾利斯
    ".SN": "智利",    # 智利
    ".LM": "秘鲁",    # 利马
    ".CN": "哥伦比亚",  # 哥伦比亚
}

def detect_market_from_symbol(symbol):
    """根据股票代码自动推断市场（支持全球交易所后缀）"""
    symbol = symbol.upper().strip()
    
    # 1. 检查Yahoo后缀（如 SHEL.L -> 英国, 7203.T -> 日本）
    for suffix, market in YAHOO_SUFFIX_MAP.items():
        if symbol.endswith(suffix) and len(symbol) > len(suffix):
            return market
    
    # 2. A股: 6位纯数字
    if symbol.isdigit() and len(symbol) == 6:
        prefix = symbol[0]
        if prefix in ['6', '9', '0', '3', '8']:
            return 'A股'
    
    # 3. 港股: 4-5位纯数字
    if symbol.isdigit() and len(symbol) in [4, 5]:
        if len(symbol) == 4:
            return '港股'
        if symbol[0] == '0' or symbol[0] not in ['6','9','3','8']:
            return '港股'
    
    # 4. 美股: 纯字母, 1-5位
    if symbol.isalpha() and 1 <= len(symbol) <= 5:
        return '美股'
    
    # 5. 指数: ^开头
    if symbol.startswith('^'):
        return '美股'
    
    # 6. 带后缀但未识别, 尝试取纯字母部分
    if '.' in symbol:
        base = symbol.split('.')[0]
        if base.isalpha() and 1 <= len(base) <= 5:
            return '美股'  # 默认美股
    
    return None

def get_yahoo_suffix(market_name):
    """根据市场名获取Yahoo Finance后缀"""
    for suffix, market in YAHOO_SUFFIX_MAP.items():
        if market == market_name:
            return suffix
    return ''

def auto_switch_if_needed(config, symbol):
    """如果输入的代码匹配其他市场，自动切换"""
    detected = detect_market_from_symbol(symbol)
    if detected:
        current = load_current_market()
        if detected != current and config['markets'].get(detected, {}).get('active'):
            switch_market(config, detected)
            return detected
    return None

# ============================================================
# 主入口
# ============================================================
# ============================================================
# 自动市场检测（v4.0新增）
# ============================================================


def main():
    config = load_config()
    
    if len(sys.argv) < 2:
        print("🌍 全球市场引擎 v1.0")
        print(f"   当前市场: {load_current_market()}")
        print(f"   使用: python3 market_engine.py --list-markets 查看所有市场")
        print(f"   使用: python3 market_engine.py --switch-to 美股 切换市场")
        print(f"   使用: python3 market_engine.py --market 美股 --info 查看市场配置")
        return
    
    args = sys.argv[1:]
    
    if "--list-markets" in args:
        list_markets(config)
    elif "--switch-to" in args:
        idx = args.index("--switch-to") + 1
        if idx < len(args):
            switch_market(config, args[idx])
        else:
            print("❌ 请指定目标市场，如: python3 market_engine.py --switch-to 美股")
    elif "--market" in args:
        idx = args.index("--market") + 1
        if idx < len(args):
            market_name = args[idx]
            if "--info" in args:
                get_market_info(config, market_name)
            else:
                print(f"当前市场: {market_name}")
                print(f"状态: {'✅ 已激活' if config['markets'].get(market_name, {}).get('active') else '⏳ 待开通'}")
        else:
            print("❌ 请指定市场名称")
    elif "--current" in args:
        current = load_current_market()
        info = config["markets"].get(current, {})
        print(f"当前市场: {info.get('display_name', current)}")
        print(f"语言: {info.get('language', 'zh-CN')}")
        print(f"数据源: {info.get('data_provider', {}).get('primary', 'N/A')}")
    else:
        print("❌ 未知参数")
        print("   --list-markets  列出所有市场")
        print("   --switch-to XX  切换到XX市场")
        print("   --market XX --info  查看XX市场配置")
        print("   --current  查当前市场")

if __name__ == "__main__":
    main()
