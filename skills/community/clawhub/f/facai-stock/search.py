"""股票名称搜索（带本地缓存）"""

import akshare as ak

import cache


def get_all_stocks() -> list[dict]:
    """
    获取全量A股代码/名称列表。
    优先命中本地缓存（stock_id.info），过期后自动刷新。
    返回: [{"code": "000001", "name": "平安银行"}, ...]
    """
    data = cache.load()
    if data is not None:
        return data

    df = ak.stock_info_a_code_name()
    data = [{"code": str(row["code"]), "name": str(row["name"])} for _, row in df.iterrows()]
    cache.save(data)
    return data


def search_by_name(name: str) -> list[dict]:
    """
    按名称关键字模糊搜索股票。
    返回: [{"code": "000001", "name": "平安银行"}, ...]
    """
    all_stocks = get_all_stocks()
    return [s for s in all_stocks if name in s["name"]]


def find_by_code(code: str) -> dict | None:
    """从缓存中根据6位代码精确查找股票基本信息"""
    all_stocks = get_all_stocks()
    result = next((s for s in all_stocks if s["code"] == code), None)
    return result
