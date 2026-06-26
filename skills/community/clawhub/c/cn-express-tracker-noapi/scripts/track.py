#!/usr/bin/env python3
"""
cn-express-tracker — 中国快递物流查询工具

查询中国主流快递公司的物流信息，无需 API Key。
基于快递100 (kuaidi100.com) 的免费查询接口。

用法:
  python3 track.py --num <快递单号> [--com <快递公司代码>]

示例:
  python3 track.py --num YT7450353838751
  python3 track.py --num SF1234567890 --com shunfeng
"""

import json
import sys
import urllib.request
import urllib.parse
import time

# 快递100查询接口
QUERY_URL = "https://www.kuaidi100.com/query"

# 常见快递公司代码与名称映射
COURIER_NAMES = {
    "shunfeng": "顺丰速运",
    "sf": "顺丰速运",
    "yuantong": "圆通速递",
    "yt": "圆通速递",
    "zhongtong": "中通快递",
    "zto": "中通快递",
    "shentong": "申通快递",
    "sto": "申通快递",
    "yunda": "韵达快递",
    "yundaex": "韵达快递",
    "ems": "EMS",
    "youzhengguonei": "中国邮政",
    "post": "中国邮政",
    "jd": "京东快递",
    "jingdong": "京东快递",
    "huitongkuaidi": "百世快递",
    "htky": "百世快递",
    "debangwuliu": "德邦物流",
    "deppon": "德邦物流",
    "ttkd": "天天快递",
    "zhaijisong": "宅急送",
    "yousu": "优速快递",
    "uc": "优速快递",
    "suer": "速尔快递",
    "sure": "速尔快递",
    "quanfengkuaidi": "全峰快递",
    "qfkd": "全峰快递",
    "kuaiyouda": "快优达",
    "annengwuliu": "安能物流",
    "ane": "安能物流",
    "tiantian": "天天快递",
    "guotong": "国通快递",
    "baishiwuliu": "百世快运",
    "best": "百世快运",
    "dhl": "DHL",
    "fedex": "FedEx",
    "fedexcn": "FedEx（国际）",
    "tnt": "TNT",
    "ups": "UPS",
    "shiyun": "十运物流",
    "zhimakaimen": "芝麻开门",
    "city100": "城市100",
    "coe": "COE",
    "dpex": "DPEX",
    "hre": "HRE（华人快递）",
    "jiaji": "佳吉快运",
    "jinyue": "晋越快递",
    "kcs": "KCS",
    "kuaijiesudi": "快捷快递",
    "longlangwuliu": "龙邦物流",
    "minsheng": "民生速递",
    "nengda": "能达速递",
    "peixing": "培行快递",
    "ruifeng": "瑞丰速递",
    "saiaodi": "赛奥递",
    "shengan": "圣安物流",
    "wanjia": "万家物流",
    "xinbangwuliu": "新邦物流",
    "yafeng": "亚风速递",
    "yibangwuliu": "一邦物流",
    "yishunhang": "亿顺航",
    "yuanchengwuliu": "远成物流",
    "yuefeng": "越丰物流",
    "zhengyi": "正义物流",
    "zhongtian": "中天万运",
    "zhongyou": "中邮物流",
    "zengyisudi": "增益速递",
    "yinjie": "银捷速递",
    "yuefengwuliu": "越丰物流",
    "yuantongkuaidi": "圆通速递",
    "yunda56": "韵达快递",
    "shunfengkuaiyun": "顺丰快运",
    "jiuye": "九曳供应链",
    "juexing": "爵星快递",
    "lianhaowuliu": "联昊通物流",
    "shenghuiwuliu": "盛辉物流",
    "wanxiangwuliu": "万象物流",
    "yintong": "银通快递",
    "yishunche": "一顺通车",
    "yongchangwuliu": "永昌物流",
    "youshuwuliu": "优速物流",
    "yuancheng": "远成物流",
    "yuantongjixie": "圆通机械",
    "yuefengwuliu": "越丰物流",
    "yunhe": "运和物流",
    "zhenxijie": "珍熙捷",
    "zhilan": "志兰快递",
    "zhongchuang": "众创快递",
    "zhongtiewuliu": "中铁物流",
    "zhongxing": "中兴快递",
    "zhongyouwuliu": "中邮物流",
    "zhuanhuan": "专环物流",
    "zhuoshikeji": "卓实科技",
    "ziti": "自提",
    "zuotian": "昨天快递",
}

# 状态码解释
STATE_MAP = {
    "0": "在途",
    "1": "已揽收",
    "2": "疑难",
    "3": "已签收",
    "4": "退签",
    "5": "派件中",
    "6": "退回",
    "7": "转单",
    "8": "清关",
    "9": "清关中",
    "10": "待清关",
    "11": "清关中",
    "12": "已清关",
    "13": "清关异常",
    "14": "收件人拒签",
}

# 常见单号前缀映射（在没有快递公司代码时自动猜测）
PREFIX_MAP = {
    "SF": "shunfeng",
    "YT": "yuantong",
    "ZTO": "zhongtong",
    "STO": "shentong",
    "YDA": "yunda",
    "JD": "jd",
    "JDX": "jd",
    "JT": "jd",
    "EMS": "ems",
    "DPK": "youzhengguonei",
    "HT": "huitongkuaidi",
    "DB": "debangwuliu",
    "TT": "ttkd",
    "UC": "yousu",
    "ANE": "annengwuliu",
    "AA": "annengwuliu",
    "SUE": "suer",
    "QF": "quanfengkuaidi",
    "DHL": "dhl",
}


def query_tracking(num: str, com: str = "") -> dict:
    """查询快递物流信息"""
    params = {"type": com, "postid": num}
    data = urllib.parse.urlencode(params).encode("utf-8")
    
    req = urllib.request.Request(QUERY_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except Exception as e:
        return {"error": str(e)}


def guess_courier(num: str) -> str:
    """根据单号前缀猜测快递公司"""
    upper = num.upper().strip()
    for prefix, com in PREFIX_MAP.items():
        if upper.startswith(prefix):
            return com
    return ""


def format_tracking(result: dict, com_code: str = "") -> str:
    """格式化查询结果为中文展示"""
    if "error" in result:
        return f"❌ 查询失败：{result['error']}"
    
    if not result.get("data"):
        if result.get("message") == "ok":
            return f"📦 没有查到该快递单号的物流信息（单号可能不存在或已过期）\n快递公司：{COURIER_NAMES.get(com_code, com_code or '未知')}\n单号：{result.get('nu', '')}"
        return f"❌ 查询失败：{result.get('message', '未知错误')}"
    
    nu = result.get("nu", "")
    com = result.get("com", com_code)
    state = result.get("state", "")
    ischeck = result.get("ischeck", "0")
    
    com_name = COURIER_NAMES.get(com, com)
    # 状态码可能是多位数（如"301"），取第一位为主状态
    primary_state = state[0] if len(state) > 1 else state
    state_name = STATE_MAP.get(primary_state, STATE_MAP.get(state, "未知"))
    
    lines = []
    lines.append(f"📦 快递查询结果")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"📌 快递公司：{com_name}")
    lines.append(f"🔢 快递单号：{nu}")
    lines.append(f"📊 当前状态：{state_name}{' ✅ 已签收' if ischeck == '1' else ''}")
    lines.append(f"")
    
    # 物流轨迹
    data = result.get("data", [])
    if data:
        lines.append(f"📍 物流轨迹（共 {len(data)} 条）：")
        lines.append(f"")
        for i, item in enumerate(data):
            time_str = item.get("ftime") or item.get("time", "")
            context = item.get("context", "")
            location = item.get("location", "")
            loc_str = f" [{location}]" if location else ""
            lines.append(f"  {time_str}{loc_str}")
            lines.append(f"  {context}")
            if i < len(data) - 1:
                lines.append(f"")
    
    lines.append(f"")
    lines.append(f"🔗 详情：https://www.kuaidi100.com/chaxun?com={com}&nu={nu}")
    
    return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="中国快递物流查询工具（基于快递100）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 track.py --num YT7450353838751
  python3 track.py --num SF1234567890 --com shunfeng
  python3 track.py --num JD1234567890
        
支持查询: 顺丰、圆通、中通、申通、韵达、京东、EMS、邮政、百世、德邦等
        """
    )
    parser.add_argument("--num", "-n", required=True, help="快递单号")
    parser.add_argument("--com", "-c", default="", help="快递公司代码（可选，自动识别）")
    
    args = parser.parse_args()
    
    num = args.num.strip()
    com = args.com.strip().lower()
    
    # 如果没有提供快递公司，尝试自动识别
    if not com:
        guessed = guess_courier(num)
        if guessed:
            com = guessed
    
    # 查询
    result = query_tracking(num, com)
    
    # 格式化输出
    output = format_tracking(result, com)
    print(output)


if __name__ == "__main__":
    main()
