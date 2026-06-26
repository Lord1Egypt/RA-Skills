#!/usr/bin/env python3
"""商机推荐查询服务"""

import json

from _http import api_post
from _errors import ServiceError

# 类目中文名 → ID 映射表
CATEGORY_NAME_TO_ID = {
    "办公、文化": "67",
    "鞋": "1038378",
    "童装": "311",
    "内衣": "312",
    "服饰配件、饰品": "54",
    "玩具": "1813",
    "女装": "10166",
    "食品酒水": "2",
    "宠物及园艺": "122916001",
    "汽车用品": "122916002",
    "灯饰照明": "58",
    "男装": "10165",
    "电子元器件": "57",
    "传媒、广电": "53",
    "安全、防护": "70",
    "包装": "68",
    "数码、电脑": "7",
    "电工电气": "5",
    "纺织、皮革": "4",
    "箱包皮具": "1042954",
    "机械及行业设备": "65",
    "五金、工具": "59",
    "化工": "8",
    "橡塑": "55",
    "建材": "201346017",
    "环保": "64",
    "仪器仪表": "10208",
    "居家日用品": "15",
    "日用餐厨饮具": "201547801",
    "收纳清洁用具": "201547901",
    "家纺家饰": "96",
    "美容护肤/彩妆": "97",
    "家用电器": "6",
    "家装建材": "13",
    "交通运输": "12",
    "能源": "10",
    "农业": "1",
    "汽摩及配件": "71",
    "通信产品": "509",
    "冶金矿产": "9",
    "医药、保养": "66",
    "印刷": "72",
    "运动户外": "18",
    "机床": "1426",
    "商务服务": "69",
    "二手设备转让": "2829",
    "加工": "2805",
    "个护/家清": "130822220",
    "成人用品": "130823000",
    "餐饮生鲜": "130822002",
    "钢铁": "123614001",
    "新能源": "202052814",
}

# 所有合法的类目 ID 集合（用于校验直接传入 ID 的场景）
VALID_CATEGORY_IDS = set(CATEGORY_NAME_TO_ID.values())


def resolve_category_id(category_input: str) -> str:
    """将类目中文名或 ID 解析为类目 ID

    Args:
        category_input: 类目中文名称或类目 ID

    Returns:
        类目 ID 字符串

    Raises:
        ValueError: 无法识别的类目
    """
    if category_input in VALID_CATEGORY_IDS:
        return category_input

    category_id = CATEGORY_NAME_TO_ID.get(category_input)
    if category_id:
        return category_id

    raise ValueError(
        f"无法识别的类目「{category_input}」，请输入类目 ID 或中文名称。"
        f"支持的类目名称如：女装、男装、鞋、童装 等"
    )


def _extract_opportunity(item: dict) -> dict:
    """从单条商机数据中提取关键字段

    Args:
        item: 原始商机数据

    Returns:
        精简后的商机字典
    """
    extend_info = {}
    raw_extend = item.get("extendInfo")
    if raw_extend and isinstance(raw_extend, str):
        try:
            extend_info = json.loads(raw_extend)
        except (json.JSONDecodeError, TypeError):
            pass

    pict_url_prefix = "https://cbu01.alicdn.com/"
    raw_pict_list = item.get("pictUrlList", [])
    full_pict_list = [
        url if url.startswith("https://") else pict_url_prefix + url
        for url in raw_pict_list
    ]

    return {
        "title": item.get("title", ""),
        "pictUrlList": full_pict_list,
        "demandCount": extend_info.get("expose_sum_30", ""),
        "averagePrice": extend_info.get("average_final_price", ""),
        "categoryName": item.get("cateLevel1Name", ""),
        "oppItemId": item.get("oppItemId", ""),
    }


# 默认 conditions，由代码自动注入
_DEFAULT_CONDITIONS = [
    {"nodeName": "画像类型", "nodeCode": "opp_type", "value": ["item"]},
    {"nodeName": "是否测试画像", "nodeCode": "is_test", "value": ["N"]},
    {"nodeName": "商机标签", "nodeCode": "tag_info", "value": [
        "xinpin_maijiaxuqiu", "xinpin_ifashion", "xinpin_xiaoheihe",
        "xinpin_xinpinqudong", "xinpin_fuzhuangteshu", "xinpin_chaoliuxinpin",
        "xinpin_taobao_new_tag", "real_new_cu", "xinpin_trend_hot",
        "nontb_263531_xinpin", "nontb_263531_aoxia",
    ]},
    {"nodeName": "画像状态", "nodeCode": "status", "value": ["ONLINE"]},
    {"nodeName": "商机状态", "nodeCode": "delivery_channel", "value": ["supply"]},
    {"nodeName": "排序方式", "nodeCode": "sort_field", "value": ["item_rank#desc#tpp"]},
]

# 默认主营类目列表
_DEFAULT_MAIN_CATEGORYS = ["1031910", "127372010", "10166", "1045520", "1813"]


def _merge_conditions(defaults: list[dict], extras: list[dict]) -> list[dict]:
    """合并 conditions 列表，extras 中同 nodeCode 的条目会覆盖 defaults 中的同名条目

    Args:
        defaults: 默认 conditions
        extras:   用户传入的额外 conditions

    Returns:
        合并后的 conditions 列表
    """
    merged = {item["nodeCode"]: item for item in defaults}
    for item in extras:
        merged[item["nodeCode"]] = item
    return list(merged.values())


def query_opportunities(page_no: int = 1,
                        page_size: int = 20,
                        keyword: str = "",
                        category_id: str = "") -> dict:
    """查询商机推荐列表

    Args:
        page_no:     页码，从 1 开始
        page_size:   每页条数，默认 20
        keyword:     按商机标题搜索的关键词（可选）
        category_id: 一级类目 ID 或中文名称（可选）

    Returns:
        包含 totalCnt, pageNo, pageSize, data(精简后) 的字典

    Raises:
        ValueError:    参数校验失败
        ServiceError:  API 返回结构异常
    """
    extra_conditions = []

    # 优先尝试将 keyword 转化为类目条件
    resolved_id = ""
    if category_id:
        resolved_id = resolve_category_id(category_id)
    elif keyword:
        matched_category_id = CATEGORY_NAME_TO_ID.get(keyword)
        if matched_category_id:
            resolved_id = matched_category_id

    if resolved_id:
        extra_conditions.append({
            "nodeName": "商机类目",
            "nodeCode": "category_id_path",
            "value": [resolved_id],
        })

    # keyword 未被类目消费时，作为标题搜索条件
    if keyword and not resolved_id:
        extra_conditions.append({
            "nodeName": "商机标题",
            "nodeCode": "title",
            "value": [keyword],
        })

    params = {
        "sceneCode": "realOpportunityPortraitViewNew",
        "sceneType": "offer_portrait",
        "pageNo": page_no,
        "pageSize": page_size,
        "conditions": _merge_conditions(_DEFAULT_CONDITIONS, extra_conditions),
    }
    if not resolved_id:
        params["cate_param_empty"] = True

    body = {"params": params}

    result = api_post("/api/1688_opp_recommend/1.0.0", body)

    if not isinstance(result, dict):
        raise ServiceError("格式异常，请稍后重试")

    model = result.get("model", result)
    raw_data = model.get("data", [])
    extracted = [_extract_opportunity(item) for item in raw_data] if isinstance(raw_data, list) else []

    return {
        "totalCnt": model.get("totalCnt", "0"),
        "pageNo": model.get("pageNo", page_no),
        "pageSize": model.get("pageSize", page_size),
        "data": extracted,
    }
