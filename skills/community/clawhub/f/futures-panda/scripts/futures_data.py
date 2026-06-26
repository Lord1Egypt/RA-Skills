#!/usr/bin/env python3
"""
期货数据获取脚本 (基于 AKShare)

本脚本封装了 AKShare 中主要的期货数据接口，支持通过命令行快速获取：
- 实时行情
- 历史行情（日线、分钟线）
- 注册仓单
- 现货价格与基差
- 会员持仓排名
- 手续费与保证金
- 交易日历
- 合约基础信息

依赖: akshare, pandas
用法示例:
    python futures_data.py spot RB2605
    python futures_data.py daily RB0
    python futures_data.py minute RB0 1
    python futures_data.py receipt DCE 20251027
    python futures_data.py basis 20240430
    python futures_data.py position DCE 20200513
    python futures_data.py fee "大连商品交易所"
    python futures_data.py calendar 20231205
    python futures_data.py contract shfe 20240513
"""
import sys
import json
import akshare as ak
import pandas as pd

# --- 辅助函数：将 DataFrame 转换为 JSON 兼容格式 ---
def df_to_json(df):
    """将 pandas DataFrame 转换为列表字典，处理可能的非序列化数据"""
    if df is None or df.empty:
        return []
    # 处理日期时间类型等，确保可 JSON 序列化
    return json.loads(df.to_json(orient='records', date_format='iso', force_ascii=False))

# ==================== 1. 期货实时数据 ====================
def get_futures_spot(symbol="RB2605", market="CF", adjust="0"):
    """获取期货实时行情"""
    try:
        df = ak.futures_zh_spot(symbol=symbol, market=market, adjust=adjust)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"实时行情获取失败: {e}"}

# ==================== 2. 期货历史行情 ====================
def get_futures_daily(symbol="RB0"):
    """获取期货历史日线数据（新浪）"""
    try:
        df = ak.futures_zh_daily_sina(symbol=symbol)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"日线历史数据获取失败: {e}"}

def get_futures_minute(symbol="RB0", period="1"):
    """获取期货分钟线数据
    period: "1"=1分钟, "5"=5分钟, "15"=15分钟, "30"=30分钟, "60"=60分钟
    """
    try:
        df = ak.futures_zh_minute_sina(symbol=symbol, period=period)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"分钟线数据获取失败: {e}"}

def get_futures_daily_exchange(start_date="20200701", end_date="20200716", market="DCE"):
    """获取指定交易所的历史日线数据"""
    try:
        # 注意：原 SKILL.md 中函数名为 get_futures_daily，但 AKShare 实际接口可能有变
        # 这里假设使用 ak.get_futures_daily，如不存在请替换为正确接口
        if hasattr(ak, 'get_futures_daily'):
            df = ak.get_futures_daily(start_date=start_date, end_date=end_date, market=market)
        else:
            # 备选方案：使用其他日线接口
            return {"error": "get_futures_daily 接口在当前 AKShare 版本中不可用，请使用 daily 命令"}
        return df_to_json(df)
    except Exception as e:
        return {"error": f"交易所历史数据获取失败: {e}"}


# ==================== 4. 现货价格和基差 ====================
def get_basis_recent(date="20240430"):
    """获取近期基差数据"""
    try:
        df = ak.futures_spot_price(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"近期基差数据获取失败: {e}"}

def get_basis_previous(date="20240430"):
    """获取历史基差数据"""
    try:
        df = ak.futures_spot_price_previous(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"历史基差数据获取失败: {e}"}

def get_basis_daily(start_day="20240415", end_day="20240418", vars_list=None):
    """获取历史区间内的基差数据"""
    if vars_list is None:
        vars_list = ["CU", "RB"]
    try:
        df = ak.futures_spot_price_daily(
            start_day=start_day,
            end_day=end_day,
            vars_list=vars_list
        )
        return df_to_json(df)
    except Exception as e:
        return {"error": f"历史区间基差数据获取失败: {e}"}

# ==================== 5. 会员持仓排名 ====================
def get_position_rank_dce(date="20200513"):
    """获取大商所席位持仓"""
    try:
        df = ak.futures_dce_position_rank(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"大商所持仓数据获取失败: {e}"}

def get_position_rank_gfex(date="20231113"):
    """获取广期所席位持仓"""
    try:
        df = ak.futures_gfex_position_rank(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"广期所持仓数据获取失败: {e}"}

# ==================== 6. 手续费与保证金 ====================
def get_fees_info():
    """获取期货交易费用参照表"""
    try:
        df = ak.futures_fees_info()
        return df_to_json(df)
    except Exception as e:
        return {"error": f"交易费用参照表获取失败: {e}"}

def get_commission_info(symbol="所有"):
    """按交易所查询手续费和保证金
    symbol: "所有", "上海期货交易所", "大连商品交易所", "郑州商品交易所", 
            "上海国际能源交易中心", "中国金融期货交易所", "广州期货交易所"
    """
    try:
        df = ak.futures_comm_info(symbol=symbol)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"手续费保证金数据获取失败: {e}"}

# ==================== 7. 交易日历 ====================
def get_trading_calendar(date="20231205"):
    """获取期货交易日历"""
    try:
        df = ak.futures_rule(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"交易日历获取失败: {e}"}

# ==================== 8. 合约信息 ====================
def get_contract_info_shfe(date="20240513"):
    """上期所期货合约"""
    try:
        df = ak.futures_contract_info_shfe(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"上期所合约信息获取失败: {e}"}

def get_contract_info_ine(date="20241129"):
    """国际能源中心期货合约"""
    try:
        df = ak.futures_contract_info_ine(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"能源中心合约信息获取失败: {e}"}

def get_contract_info_dce():
    """大商所期货合约"""
    try:
        df = ak.futures_contract_info_dce()
        return df_to_json(df)
    except Exception as e:
        return {"error": f"大商所合约信息获取失败: {e}"}

def get_contract_info_czce(date="20240228"):
    """郑商所期货合约"""
    try:
        df = ak.futures_contract_info_czce(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"郑商所合约信息获取失败: {e}"}

def get_contract_info_gfex():
    """广期所期货合约"""
    try:
        df = ak.futures_contract_info_gfex()
        return df_to_json(df)
    except Exception as e:
        return {"error": f"广期所合约信息获取失败: {e}"}

def get_contract_info_cffex(date="20240228"):
    """中金所期货合约"""
    try:
        df = ak.futures_contract_info_cffex(date=date)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"中金所合约信息获取失败: {e}"}

def get_main_contract_list():
    """连续合约品种一览表"""
    try:
        df = ak.futures_display_main_sina()
        return df_to_json(df)
    except Exception as e:
        return {"error": f"连续合约列表获取失败: {e}"}

# ==================== 9. 现货与股票关联 ====================
def get_spot_stock(symbol="能源"):
    """获取现货与股票关联数据
    symbol: '能源', '化工', '塑料', '纺织', '有色', '钢铁', '建材', '农副'
    """
    try:
        df = ak.futures_spot_stock(symbol=symbol)
        return df_to_json(df)
    except Exception as e:
        return {"error": f"现货股票关联数据获取失败: {e}"}

# ==================== 命令行参数解析 ====================
if __name__ == "__main__":
    # 定义命令与函数的映射关系
    commands = {
        # 实时数据
        "spot": get_futures_spot,
        # 历史行情
        "daily": get_futures_daily,
        "minute": get_futures_minute,
        "daily_ex": get_futures_daily_exchange,

        # 费用
        "fees": get_fees_info,
        # 日历
        "calendar": get_trading_calendar,
        # 合约
        "contract_shfe": get_contract_info_shfe,
        "contract_ine": get_contract_info_ine,
        "contract_dce": get_contract_info_dce,
        "contract_czce": get_contract_info_czce,
        "contract_gfex": get_contract_info_gfex,
        "contract_cffex": get_contract_info_cffex,
        "main_contracts": get_main_contract_list,
        # 现货股票
        "spot_stock": get_spot_stock,
    }

    # 无参数时显示帮助
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python futures_data.py <command> [args...]",
            "available_commands": list(commands.keys()),
            "example": "python futures_data.py spot RB2605"
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in commands:
        print(json.dumps({"error": f"未知命令: {cmd}，可用命令: {list(commands.keys())}"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 提取额外参数
    args = sys.argv[2:]
    func = commands[cmd]

    # 根据命令动态调用函数（部分命令需要特殊参数处理）
    try:
        if cmd == "spot":
            kwargs = {}
            if len(args) >= 1:
                kwargs["symbol"] = args[0]
            if len(args) >= 2:
                kwargs["market"] = args[1]
            if len(args) >= 3:
                kwargs["adjust"] = args[2]
            result = func(**kwargs)
        
        elif cmd == "daily":
            kwargs = {"symbol": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd == "minute":
            kwargs = {}
            if len(args) >= 1:
                kwargs["symbol"] = args[0]
            if len(args) >= 2:
                kwargs["period"] = args[1]
            result = func(**kwargs)
        
        elif cmd == "daily_ex":
            kwargs = {}
            if len(args) >= 1:
                kwargs["start_date"] = args[0]
            if len(args) >= 2:
                kwargs["end_date"] = args[1]
            if len(args) >= 3:
                kwargs["market"] = args[2]
            result = func(**kwargs)
        
        elif cmd == "receipt_gen":
            kwargs = {}
            if len(args) >= 1:
                kwargs["start_date"] = args[0]
            if len(args) >= 2:
                kwargs["end_date"] = args[1]
            if len(args) >= 3:
                kwargs["vars_list"] = args[2].split(",")
            result = func(**kwargs)
        
        elif cmd == "receipt":
            kwargs = {}
            if len(args) >= 1:
                kwargs["exchange"] = args[0]
            if len(args) >= 2:
                kwargs["date"] = args[1]
            result = func(**kwargs)
        
        elif cmd == "basis":
            kwargs = {"date": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd == "basis_prev":
            kwargs = {"date": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd == "basis_daily":
            kwargs = {}
            if len(args) >= 1:
                kwargs["start_day"] = args[0]
            if len(args) >= 2:
                kwargs["end_day"] = args[1]
            if len(args) >= 3:
                kwargs["vars_list"] = args[2].split(",")
            result = func(**kwargs)
        
        elif cmd == "position_dce":
            kwargs = {"date": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd == "position_gfex":
            kwargs = {"date": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd == "fees":
            result = func()
        
        elif cmd == "commission":
            kwargs = {"symbol": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd == "calendar":
            kwargs = {"date": args[0]} if args else {}
            result = func(**kwargs)
        
        elif cmd.startswith("contract_"):
            # 处理各种合约命令
            if cmd == "contract_dce" or cmd == "contract_gfex":
                result = func()  # 无参数
            else:
                # 需要日期参数的合约函数
                kwargs = {"date": args[0]} if args else {}
                result = func(**kwargs)
        
        elif cmd == "main_contracts":
            result = func()
        
        elif cmd == "spot_stock":
            kwargs = {"symbol": args[0]} if args else {}
            result = func(**kwargs)
        
        else:
            # 对于简单的无参数或有默认参数的函数，直接调用
            # 如果函数需要参数但没有提供，可能会出错
            result = func(*args) if args else func()
    
    except Exception as e:
        result = {"error": f"执行命令 {cmd} 时出错: {e}"}

    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))