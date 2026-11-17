#!/usr/bin/env python3
"""客户列表查询 CLI入口"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import JsonArgumentParser, print_output, print_error
from capabilities.customer_list.service import customer_list

COMMAND_NAME = "alibaba.1688.customer.list"
COMMAND_DESC = "分页查询客户列表（支持筛选+排序）"


def _safe(val):
    if val is None or val == "":
        return "—"
    return str(val)


def _extract_list_and_total(obj):
    """递归解包嵌套 data 字段，找到客户列表和 total"""
    if not isinstance(obj, dict):
        return (obj if isinstance(obj, list) else []), 0
    inner = obj.get("data")
    if isinstance(inner, list):
        return inner, obj.get("total") or len(inner)
    if isinstance(inner, dict):
        return _extract_list_and_total(inner)
    return [], obj.get("total") or 0


# 页级噪声字段（仅剔除明确的技术字段）
_PAGE_NOISE = {"eagleTraceId", "class"}
# 客户级噪声字段（licenseCode 不可筛选，不对外输出）
# city / province / district 为合规受限字段：禁止筛选也禁止透出，
# 网关仍可能返回，这里统一剔除，避免进入 markdown 或 --raw 输出。
_CUSTOMER_NOISE = {
    "class", "id", "sellerId", "sortId", "licenseCode",
    "city", "province", "district",
}

# 客户级驼峰字段名 → alibaba.1688.customer.attr.field.config 的下划线 attrKey 映射
# 统一以 field_config 返回的字段名为准，避免 --raw 输出的驼峰字段名让模型困惑；
# extraAttrs 内的键接口已是下划线风格，无需映射。
_CUSTOMER_FIELD_RENAME = {
    "buyerNick": "buyer_nick",
    "siteFlag": "site_flag",
    "recent30dActivityScore": "recent_30d_activity_score",
    "recent30dPurchaseAmount": "recent_30d_purchase_amount",
    "shopIds": "shop_ids",
    "lastInquiryTime": "last_inquiry_time",
    "gmtCreate": "gmt_create",
    "gmtModified": "gmt_modified",
    # lastOrderTime 已在 activeAttrs 中声明（最近下单时间），可筛选、可排序
    # （2026-08-31 预发复验：筛选与 asc/desc 排序均生效），这里仅做命名对齐
    "lastOrderTime": "last_order_time",
    # 出参名与入参名对齐：filters 用 source，但网关返回 customerRelation
    "customerRelation": "source",
    # 网关同时返回 importChannel 与 import_channel（实测 300 条取值完全一致），
    # 映射到同一个键上自然合并，只保留 import_channel
    "importChannel": "import_channel",
}

# ─── 参数校验常量 ───────────────────────────────────────────────────────────────

# 允许的 filter op 操作符（SKILL.md 用户友好格式 + 1688 CRM API 标准格式）
_VALID_OPS = {"=", ">", "<", ">=", "<=", "like", "in", "not in"}

_VALID_OPS_LOWER = {op.lower() for op in _VALID_OPS}

# 允许的 sort order 值
_VALID_ORDERS = {"asc", "desc"}


def _slim_customer(item: dict) -> dict:
    """黑名单剔除客户级噪声字段，并将驼峰字段名统一为 field_config 的下划线 attrKey"""
    if not isinstance(item, dict):
        return item
    # siteFlag 为 Y 时禁止透出手机号（基于原始字段判断）
    phone_hidden = str(item.get("siteFlag") or "").upper() == "Y"
    slim = {}
    for k, v in item.items():
        if k in _CUSTOMER_NOISE:
            continue
        slim[_CUSTOMER_FIELD_RENAME.get(k, k)] = v
    if phone_hidden:
        slim["phone"] = None
    return slim


def _slim_result(result: dict) -> dict:
    """下钻至 PageResult 节点，去掉多层信封与噪声字段，其余保留"""
    page = _find_page_result(result)
    if not isinstance(page, dict):
        return result  # 结构异常时原样返回
    slim = {k: v for k, v in page.items() if k not in _PAGE_NOISE}
    slim["items"] = [_slim_customer(x) for x in page.get("data") or []]
    slim.pop("data", None)
    return slim


def _find_page_result(obj):
    """向下钻取到包含客户列表（data 为 list）的 PageResult 节点"""
    if not isinstance(obj, dict):
        return None
    inner = obj.get("data")
    if isinstance(inner, list):
        return obj
    if isinstance(inner, dict):
        return _find_page_result(inner)
    return None


def _render_markdown(result: dict, page_size: int, page_num: int = 1) -> str:
    page = _find_page_result(result)
    data, total = _extract_list_and_total(result)

    # 提取分页统计信息
    record_count = total
    page_no = page_num
    total_page = 1
    if isinstance(page, dict):
        record_count = page.get("recordCount") or page.get("totalCount") or total
        page_no = page.get("pageNo") or page_num
        total_page = page.get("totalPage") or (max(1, -(-record_count // page_size)) if record_count else 1)

    if not data:
        return "# 📋 查询结果\n\n> 暂无匹配的客户数据"

    lines = [
        "# 📋 查询结果",
        "",
        f"> 总匹配 **{record_count}** 条 | 第 {page_no}/{total_page} 页 | 当前展示 {len(data)} 条",
        "",
        "| 买家昵称 | 手机号 | 采购意愿 | 标签 | 近30天平台活跃度 | 最近询盘时间 | 近30天店铺合作关系| 店铺首次付款日期 | 周付款商品数 |",
        "|----------|--------|----------|------|--------|----------|---------------|--------------|-------------|",
    ]

    for item in data:
        nick = _safe(item.get("buyerNick"))
        # siteFlag 为 Y 时禁止展示手机号
        phone = "—" if str(item.get("siteFlag") or "").upper() == "Y" else _safe(item.get("phone"))
        tags = ", ".join(item.get("tags") or []) or "—"
        score = _safe(item.get("recent30dActivityScore"))
        inquiry = _safe(item.get("lastInquiryTime"))
        # extraAttrs 关键字段
        attrs = item.get("extraAttrs") or {}
        # 采购意愿：平台字段（过滤索引），与被筛维度保持一致，
        # 避免商家自维护标签（tags）里的旧意愿值造成"没筛"错觉
        interest = _safe(attrs.get("user_interest_level"))
        procurement_mode = _safe(attrs.get("procurement_mode_30d"))
        fst_pay_date = _safe(attrs.get("fst_pay_ord_date"))
        pay_mord_cnt = _safe(attrs.get("pay_mord_cnt_1w"))
        lines.append(f"| {nick} | {phone} | {interest} | {tags} | {score} | {inquiry} | {procurement_mode} | {fst_pay_date} | {pay_mord_cnt} |")

    lines.append("")
    lines.append("---")
    return "\n".join(lines)


def _build_file_not_found_hint(path: str) -> str:
    """构建文件未找到时的诊断提示，帮助区分目录错配 vs 写未落盘。"""
    scratch = os.environ.get('NEWTON_SCRATCH_DIR') or ""
    temp = os.environ.get('TEMP') or ""

    parts = [
        "。可能原因：",
        "1) 写文件与调用使用了不同的临时目录（NEWTON_SCRATCH_DIR 与 %TEMP% 指向不同路径）；",
        "2) 写文件命令未成功落盘（exit≠0/超时），但下一步未检查直接读取；",
        "3) 使用了相对路径、/tmp 或 %TEMP% 字面量，未使用写入时输出的绝对路径。",
        f"当前 NEWTON_SCRATCH_DIR={scratch or '未设置'}；TEMP={temp or '未设置'}。",
    ]

    # 列出目标路径所在目录的现有文件，帮助定位是目录错配还是写未落盘
    try:
        dir_path = os.path.dirname(os.path.abspath(path)) if os.path.isabs(path) else os.getcwd()
        files = sorted(os.listdir(dir_path))
        if files:
            sample = files[:20]
            parts.append(f"目标目录 {dir_path} 现有文件：{', '.join(sample)}{' 等' if len(files) > 20 else ''}。")
        else:
            parts.append(f"目标目录 {dir_path} 为空目录。")
    except Exception as e:
        parts.append(f"无法列出目标目录内容：{e}。")

    parts.append("推荐：在同一条 python -c 内完成写文件和调用；若必须分步，请先 print(绝对路径) 并使用该路径。")
    return "".join(parts)


def _reject_json_as_file_path(value: str, option: str) -> bool:
    """拒绝把 JSON 内容误传给 --*-file，避免落入冗长的文件不存在诊断。"""
    if not value.lstrip().startswith(("[", "{")):
        return False
    direct_option = option[:-5] if option.endswith("-file") else option
    if sys.platform == "win32":
        action = "请先将 JSON 写入文件，再把文件路径传给该参数（Windows 不支持直接传 JSON）"
    else:
        action = f"请改用 --{direct_option}，或先将 JSON 写入文件再传文件路径"
    print_output(
        False,
        f"❌ --{option} 的参数是 JSON，不是文件路径；{action}",
        {},
    )
    return True


def _parse_json_arg(raw: str, name: str):
    """
    解析 JSON 参数，兼容：
    1. 裸 JSON 字符串
    2. @path / path 指向的 JSON 文件
    3. Windows cmd 外层包裹的单/双引号自动剥离后重试
    """
    if raw is None:
        return None, None
    raw = raw.strip()

    # @path 语法：显式从文件读取
    if raw.startswith("@"):
        path = raw[1:]
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), None
        except Exception as e:
            return None, f"❌ 无法读取 --{name} 文件 {path}: {e}"

    # 直接解析 JSON
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        pass

    # Windows shell 可能把外层引号一并传入，尝试剥离后重试
    if len(raw) >= 2 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
        try:
            return json.loads(raw[1:-1]), None
        except json.JSONDecodeError:
            pass

    # 如果 raw 是一个存在的文件路径，则读取文件
    if os.path.isfile(raw):
        try:
            with open(raw, "r", encoding="utf-8") as f:
                return json.load(f), None
        except Exception as e:
            return None, f"❌ --{name} 不是有效的 JSON 或文件: {e}"

    return None, f"❌ --{name} 格式错误，需要有效的 JSON 数组"


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未注入，请检查框架环境变量 ALI_1688_AK 是否已配置", {})
        return 2

    parser = JsonArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--filters-file", help='筛选条件 JSON 文件路径（推荐；Windows 必须）')
    parser.add_argument("--sorts-file", help='排序规则 JSON 文件路径（推荐；Windows 必须）')
    parser.add_argument("--filters", help='筛选条件 JSON 数组（仅 Unix/macOS 兼容，推荐改用 --filters-file）')
    parser.add_argument("--sorts", help='排序规则 JSON 数组（仅 Unix/macOS 兼容，推荐改用 --sorts-file）')
    parser.add_argument("--page-num", type=int, default=1, help="页码，从1开始")
    parser.add_argument("--page-size", type=int, default=20, help="每页条数，默认20")
    parser.add_argument("--raw", action="store_true", default=False, help="输出完整 data 字段（默认仅输出 markdown）")
    args = parser.parse_args()

    # Windows 下必须走文件入参，彻底避免 cmd 把 >/< 等字符当成重定向符
    if sys.platform == "win32" and (args.filters is not None or args.sorts is not None):
        print_output(
            False,
            "❌ Windows 环境下 customer_list 必须使用 --filters-file / --sorts-file 传入 JSON 文件，禁止直接传 JSON 字符串",
            {},
        )
        return 1

    if args.filters and args.filters_file:
        print_output(False, "❌ --filters 与 --filters-file 不能同时使用", {})
        return 1
    if args.sorts and args.sorts_file:
        print_output(False, "❌ --sorts 与 --sorts-file 不能同时使用", {})
        return 1

    if args.filters_file and _reject_json_as_file_path(args.filters_file, "filters-file"):
        return 1
    if args.sorts_file and _reject_json_as_file_path(args.sorts_file, "sorts-file"):
        return 1

    filters = None
    if args.filters:
        filters, err = _parse_json_arg(args.filters, "filters")
        if err:
            print_output(False, err, {})
            return 1
    elif args.filters_file:
        try:
            with open(args.filters_file, "r", encoding="utf-8") as f:
                filters = json.load(f)
        except Exception as e:
            print_output(False, f"❌ 无法读取 --filters-file {args.filters_file}: {e}{_build_file_not_found_hint(args.filters_file)}", {})
            return 1

    sorts = None
    if args.sorts:
        sorts, err = _parse_json_arg(args.sorts, "sorts")
        if err:
            print_output(False, err, {})
            return 1
    elif args.sorts_file:
        try:
            with open(args.sorts_file, "r", encoding="utf-8") as f:
                sorts = json.load(f)
        except Exception as e:
            print_output(False, f"❌ 无法读取 --sorts-file {args.sorts_file}: {e}{_build_file_not_found_hint(args.sorts_file)}", {})
            return 1

    # 基本格式校验：防止 shell 把 op 吃掉后出现空操作符
    if filters is not None:
        if not isinstance(filters, list):
            print_output(False, "❌ --filters 必须是 JSON 数组", {})
            return 1
        for i, item in enumerate(filters):
            if not isinstance(item, dict) or not item.get("field") or not item.get("op"):
                print_output(False, f"❌ filters[{i}] 必须包含非空的 field 和 op", {})
                return 1
    if sorts is not None:
        if not isinstance(sorts, list):
            print_output(False, "❌ --sorts 必须是 JSON 数组", {})
            return 1
        for i, item in enumerate(sorts):
            if not isinstance(item, dict) or not item.get("field") or not item.get("order"):
                print_output(False, f"❌ sorts[{i}] 必须包含非空的 field 和 order", {})
                return 1

    # ─── 增强校验：page_size / page_num 范围 ──────────────────────────────────
    if args.page_size < 1 or args.page_size > 100:
        print_output(False, f"❌ page_size 必须在 1~100 之间，当前值: {args.page_size}", {})
        return 1
    if args.page_num < 1:
        print_output(False, f"❌ page_num 必须 >= 1，当前值: {args.page_num}", {})
        return 1

    # ─── 增强校验：filter op 值 ───────────────────────────────────────────────
    if filters is not None:
        for i, item in enumerate(filters):
            op_val = str(item.get("op", "")).strip()
            if op_val.lower() not in _VALID_OPS_LOWER:
                print_output(
                    False,
                    f"❌ filters[{i}].op 值无效: \"{op_val}\"，允许的操作符: {', '.join(sorted(_VALID_OPS))}",
                    {},
                )
                return 1

    # ─── 增强校验：sort order 值 ──────────────────────────────────────────────
    if sorts is not None:
        for i, item in enumerate(sorts):
            order_val = str(item.get("order", "")).strip()
            if order_val.lower() not in _VALID_ORDERS:
                print_output(
                    False,
                    f"❌ sorts[{i}].order 值无效: \"{order_val}\"，只允许 \"asc\" 或 \"desc\"",
                    {},
                )
                return 1

    try:
        result = customer_list(
            filters=filters,
            sorts=sorts,
            page_num=args.page_num,
            page_size=args.page_size,
        )
        if args.raw:
            # --raw 模式：data 直接承载分页结果，客户数组统一命名为 items。
            print(json.dumps({
                "success": True,
                "data": _slim_result(result),
                "__state_update__": True,
                "filters": filters or [],
                "sorts": sorts or [],
                "action": "alibaba.1688.customer.list",
            }, ensure_ascii=False, indent=2))
        else:
            # 默认模式：轻量 data（分页元数据）+ markdown，减少 token 消耗
            markdown = _render_markdown(result, args.page_size, args.page_num)
            page = _find_page_result(result)
            _, total = _extract_list_and_total(result)
            record_count = total
            page_no = args.page_num
            total_page = 1
            if isinstance(page, dict):
                record_count = page.get("recordCount") or page.get("totalCount") or total
                page_no = page.get("pageNo") or args.page_num
                total_page = page.get("totalPage") or (max(1, -(-record_count // args.page_size)) if record_count else 1)
            output = {
                "success": True,
                "markdown": markdown,
                "data": {
                "recordCount": record_count,
                "pageNo": page_no,
                "totalPage": total_page,
                },
                "__state_update__": True,
                "filters": filters or [],
                "sorts": sorts or [],
                "action": "alibaba.1688.customer.list"
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        return print_error(e, {})


if __name__ == "__main__":
    sys.exit(main())
