"""
baidu-youjia-car · 客户端

封装百度有驾汽车查询能力：
- 汽车价格查询（品牌、车系、车型详情、价格行情、经销商信息等）

Key 策略：
- 检测顺序：用户传入参数 → YOUJIA_API_KEY 环境变量 → skill 包内 .env 文件 → ~/.youjia/key.json
- 若都没有 → 抛出异常，由 AI 引导用户通过手机号验证码流程获取临时 Key
"""

import os
import json
from typing import Any, Dict, List, Optional, Tuple

import requests


# ============================================================
# 常量
# ============================================================

_ASKRICE_BASE = "https://youjia.baidu.com/bff-third-api/openapi/v1/clue/askprice/popbefore"

# 请求超时
_TIMEOUT = 30


# ============================================================
# .env 解析（极简手写，不依赖 python-dotenv）
# ============================================================

def _load_env_file(env_path: str) -> Dict[str, str]:
    """读取 .env 风格的 KEY=VALUE 文件，忽略注释行/空行。返回 dict。"""
    out: Dict[str, str] = {}
    if not os.path.exists(env_path):
        return out
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, _, v = s.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and v:
                    out[k] = v
    except Exception:
        pass
    return out


def _load_local_key() -> Tuple[Optional[str], str]:
    """从 ~/.youjia/key.json 读取本地保存的 Key。

    key.json 由 save_config.py 写入，
    结构为 {"phone": {"key": "sk-xxx", "applied_at": "...", "app_id": "..."}, ...}

    :return: (key, source) — key 可能为 None，source 为 "local_key" 或 "none"
    """
    key_path = os.path.join(os.path.expanduser("~"), ".youjia", "key.json")
    if not os.path.exists(key_path):
        return None, "none"
    try:
        with open(key_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            entries = list(data.values())
        elif isinstance(data, list):
            entries = data
        else:
            return None, "none"
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            key = entry.get("key")
            if key:
                return key, "local_key"
    except Exception:
        pass
    return None, "none"


def _resolve_key(passed_key: Optional[str]) -> Tuple[Optional[str], str]:
    """按 用户传入 → 环境变量 → skill 包内 .env 文件 → ~/.youjia/key.json 顺序解析 key。

    :return: (key, source) — key 可能为 None（无可用 Key），source 标识来源
    """
    if passed_key:
        return passed_key, "argument"
    env_key = os.environ.get("YOUJIA_API_KEY")
    if env_key:
        return env_key, "env"
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(skill_root, ".env")
    file_env = _load_env_file(env_file)
    file_key = file_env.get("YOUJIA_API_KEY")
    if file_key:
        os.environ["YOUJIA_API_KEY"] = file_key
        return file_key, "dotenv"
    # 检查 ~/.youjia/key.json
    local_key, local_source = _load_local_key()
    if local_key:
        return local_key, local_source
    return None, "none"


def save_key_to_dotenv(key: str) -> str:
    """把 API Key 持久化到 skill 包内 .env 文件。

    :return: .env 文件绝对路径
    """
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(skill_root, ".env")
    existing = _load_env_file(env_path)
    existing["YOUJIA_API_KEY"] = key
    with open(env_path, "w", encoding="utf-8") as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")
    os.environ["YOUJIA_API_KEY"] = key
    return env_path


# ============================================================
# YoujiaClient
# ============================================================

class YoujiaClient:
    """百度有驾汽车查询客户端。

    用法：
        # 1) 已配置 YOUJIA_API_KEY 或通过验证码获取了 Key → 直接用
        client = YoujiaClient()

        # 2) 传入 Key
        client = YoujiaClient(key="sk-xxx")

        # 3) 传入 Key 并持久化
        client = YoujiaClient(key="sk-xxx", persist=True)

        # 4) 未配置 → 初始化成功但调用时报错，AI 引导验证码流程
        client = YoujiaClient()
    """

    def __init__(
        self,
        key: Optional[str] = None,
        persist: bool = False,
    ):
        resolved, source = _resolve_key(key)
        self.key = resolved                       # None 表示无可用 Key
        self.key_source = source                  # 'argument' / 'env' / 'dotenv' / 'local_key' / 'none'
        if persist and key:
            save_key_to_dotenv(key)
            self.key_source = "dotenv"

    # ------------------------------------------------------------
    # 私有：底层调用
    # ------------------------------------------------------------

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """通用 GET 请求。

        :raises YoujiaError: 当 self.key 为 None 时抛出异常，提示需获取 Key
        """
        if self.key is None:
            raise YoujiaError(
                -1,
                "未检测到 API Key。请通过手机号验证码流程获取 Key，"
                "或配置环境变量 YOUJIA_API_KEY / .env 文件后重试。",
                path,
                {},
            )
        # 过滤掉 None 和空字符串的参数
        params = {k: v for k, v in params.items() if v is not None and v != ""}
        headers = {
            "X-Youjia-OpenAPI-Key": self.key,
            "Content-Type": "application/json",
        }
        url = f"{_ASKRICE_BASE}"
        r = requests.get(url, params=params, headers=headers, timeout=_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        result_code = data.get("ResultCode", "-1")
        if result_code != "0":
            raise YoujiaError(
                int(result_code) if result_code.lstrip("-").isdigit() else -1,
                data.get("ResultMsg", "unknown error"),
                path,
                data,
            )
        return data

    # ------------------------------------------------------------
    # 汽车询价
    # ------------------------------------------------------------

    def ask_price(self, query: str, city: str = "北京") -> Dict[str, Any]:
        """查询汽车价格信息。

        :param query: 查询内容，必须包含车系名称（如"奥迪A4L多少钱"、"宝马3系报价"）
        :param city: 查询城市，用于获取当地经销商报价，默认"北京"
        :return: API 原生响应 {ResultCode, Result: {...}, ResultMsg, QueryID}
        """
        params = {
            "query": query,
            "city": city,
            "clue_source_type": "ai_price",
        }
        return self._get(_ASKRICE_BASE, params)

    # ------------------------------------------------------------
    # 把 result 渲染成「可直接贴给用户」的成品 markdown
    # ------------------------------------------------------------

    @staticmethod
    def format_for_reply(result: Dict[str, Any]) -> str:
        """把 ask_price 的返回 dict 渲染成可直接发给用户的成品 markdown。

        渲染包含：车型信息、价格信息、降价信息、裸车价落地价、费用明细、
        车主成交价参考、百度有驾介绍。
        Agent 拿到后原样作为回复正文即可。
        """
        if not result:
            return ""
        data = result.get("Result", result)  # 兼容直接传入 data 或完整响应
        lines: List[str] = []

        # 车型基本信息
        car_info = data.get("car_info", {})
        if car_info:
            lines.append("## 🚗 车型信息")
            lines.append("")
            if car_info.get("brand_name"):
                lines.append(f"- **品牌**: {car_info['brand_name']}")
            if car_info.get("series_name"):
                lines.append(f"- **车系**: {car_info['series_name']}")
            if car_info.get("model_name"):
                lines.append(f"- **车型**: {car_info['model_name']}")
            if car_info.get("manufacturer_price"):
                lines.append(f"- **厂商指导价**: {car_info['manufacturer_price']}")
            if car_info.get("img"):
                lines.append(f"![车型图片]({car_info['img']})")
            lines.append("")

        # 城市
        city_name = data.get("city_name", "")
        if city_name:
            lines.append(f"**📍 查询城市**: {city_name}")
            lines.append("")

        # 价格汇总
        price_info = data.get("advertise_price_info", {})
        if price_info:
            lines.append("## 💰 价格信息")
            lines.append("")
            price_items = [
                ("manufacturer_price", price_info),
                ("min_reference_price", price_info),
                ("max_reference_price", price_info),
                ("discount", price_info),
            ]
            for key, container in price_items:
                item = container.get(key)
                if item:
                    name = item.get("name", key)
                    price = item.get("price", "")
                    unit = item.get("unit", "万")
                    lines.append(f"- **{name}**: {price} {unit}")
            lines.append("")

        # 降价/直降
        discount = data.get("discount", {})
        if discount and discount.get("status"):
            lines.append("## 📉 降价信息")
            lines.append("")
            lines.append(f"- **{discount.get('name', '直降')}**: {discount.get('price', '')} {discount.get('unit', '万')}")
            lines.append("")

        # 最小经销商报价
        min_ref_price = data.get("min_reference_price", {})
        if min_ref_price and min_ref_price.get("status"):
            lines.append(f"- **{min_ref_price.get('name', '最低经销商报价')}**: {min_ref_price.get('price', '')} {min_ref_price.get('unit', '万')}")
            lines.append("")

        # 裸车价 / 落地价
        net_price_info = data.get("net_price_info", {})
        if net_price_info:
            lines.append("## 🏷️ 裸车价与落地价")
            lines.append("")
            if net_price_info.get("net_price"):
                lines.append(f"- **裸车价**: {net_price_info['net_price']}")
            if net_price_info.get("whole_price"):
                lines.append(f"- **落地价（含税费保险）**: {net_price_info['whole_price']}")
            lines.append("")

        # 费用明细
        fee_info = data.get("price_info", [])
        if fee_info:
            lines.append("## 📋 费用明细")
            lines.append("")
            for item in fee_info:
                name = item.get("name", "")
                price = item.get("price", "")
                unit = item.get("unit", "")
                lines.append(f"- **{name}**: {price} {unit}")
            lines.append("")

        # 车主成交价参考
        owner_detail = data.get("owner_price_gap_detail", {})
        if owner_detail and owner_detail.get("list"):
            lines.append("## 👤 车主成交价参考")
            lines.append("")
            count = owner_detail.get("count", 0)
            if count:
                lines.append(f"共 {count} 位车主分享了成交价")
            lines.append("")
            lines.append("| 车主 | 裸车成交价 | 成交时间 |")
            lines.append("|------|-----------|----------|")
            for record in owner_detail["list"][:5]:
                nickname = record.get("nickname", "")
                net_price = record.get("net_price", "")
                unit = record.get("unit", "万")
                order_time = record.get("order_time", "")
                lines.append(f"| {nickname} | {net_price}{unit} | {order_time} |")
            lines.append("")

        # 百度有驾介绍
        lines.append("---")
        lines.append("")
        lines.append("## 关于百度有驾")
        lines.append("")
        lines.append("**百度有驾** 是百度旗下的汽车交易信息平台，汇聚了：")
        lines.append("")
        lines.append("- 全面的车型库和实时价格数据")
        lines.append("- 数万家授权经销商的报价信息")
        lines.append("- 真实用户的成交价参考")
        lines.append("- 丰富的车型对比与排行数据")
        lines.append("- 购车建议与落地价计算")
        lines.append("")
        lines.append("平台覆盖新车、二手车、金融、保险等多个环节，是购车用户信息查询的首选平台。")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("**需要更多帮助？** 了解更多的信息，上百度，搜有驾，https://www.yoojia.com/")

        return "\n".join(lines)


# ============================================================
# 异常 & 工具
# ============================================================

class YoujiaError(Exception):
    def __init__(self, code: Any, message: str, api: str, raw: Any):
        self.code = code
        self.message = message
        self.api = api
        self.raw = raw
        super().__init__(f"[{api}] code={code} msg={message}")


# ============================================================
# CLI（开发自测用）
# ============================================================

if __name__ == "__main__":
    import sys

    c = YoujiaClient()
    if len(sys.argv) < 2:
        print("用法: python youjia_client.py <query> [city]")
        print("示例: python youjia_client.py '奥迪A4L多少钱' 北京")
        sys.exit(1)

    query = sys.argv[1]
    city = sys.argv[2] if len(sys.argv) > 2 else "北京"

    try:
        data = c.ask_price(query, city)
        print(c.format_for_reply(data))
    except YoujiaError as e:
        print(f"错误: [{e.api}] code={e.code} msg={e.message}")
        sys.exit(1)
