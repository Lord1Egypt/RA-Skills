#!/usr/bin/env python3
"""
ClawMate Invoice Validate API Client

查验发票真伪并返回结构化发票信息。

Usage:
    python invoice_validate_client.py --fphm "12345678" --kprq "20260424"
    python invoice_validate_client.py --fphm "12345678" --kprq "20260424" --fpdm "1100191320" --json
    python invoice_validate_client.py --fphm "12345678901234567890" --kprq "20260424" --verbose

API Key source:
    CLAWMATE_API_KEY environment variable
"""

import argparse
import json
import sys
import os

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("Error: urllib not available. Please ensure Python is properly installed.")
    sys.exit(1)


DEFAULT_API_URL = "https://www.clawmate.net/server/test/Api/InvoiceValidate"
SKILL_CODE = ""cm-invoice-validate""
SKILL_VERSION = "1.0.2"


def utf8_print(text: str):
    """Print text with UTF-8 encoding (fixes Windows console encoding issues)."""
    sys.stdout.buffer.write(text.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


def get_env_var(name: str) -> str:
    return os.environ.get(name)


def get_api_key() -> str:
    return get_env_var("CLAWMATE_API_KEY")


def call_invoice_validate_api(
    api_key: str, fphm: str = None, kprq: str = None,
    fpdm: str = None, kjje: str = None, jshj: str = None, jym: str = None,
    validate_mode: int = None, file_base64: str = None,
    api_url: str = None, verbose: bool = False
) -> dict:
    """
    Call the ClawMate Invoice Validate API.

    Args:
        api_key: User's API key from SkillsMarket
        fphm: Invoice number (8 digits for traditional, 20 for 全电票)
        kprq: Invoice date in yyyyMMdd format
        fpdm: Invoice code (optional, not needed for 全电票)
        kjje: Amount without tax (optional)
        jshj: Total amount with tax (optional)
        jym: Check code, full or last 6 digits (optional)
        validate_mode: Validation mode (1=manual, 2=pdf, 3=image, 4=odf)
        file_base64: File content as base64 string (for validate_mode 2/3/4)
        api_url: API endpoint URL (default: DEFAULT_API_URL)
        verbose: Print request parameters for debugging

    Returns:
        API response as dictionary
    """
    if api_url is None:
        api_url = DEFAULT_API_URL

    # 构造请求体
    payload = {
        "platform": "api",
        "apiVersion": "1",
        "skillCode": SKILL_CODE,
        "skillVersion": SKILL_VERSION,
    }

    if validate_mode is not None:
        payload["validateMode"] = validate_mode

    if validate_mode is not None and validate_mode >= 2:
        # 文件方式查验：只需 fileBase64
        if file_base64:
            payload["fileBase64"] = file_base64
    else:
        # 发票信息方式查验
        payload["fphm"] = fphm
        payload["kprq"] = kprq
        if fpdm:
            payload["fpdm"] = fpdm
        if kjje:
            payload["kjje"] = kjje
        if jshj:
            payload["jshj"] = jshj
        if jym:
            payload["jym"] = jym

    headers = {
        "Content-Type": "application/json",
        "apiKey": api_key,
    }

    # 调试模式输出
    if verbose:
        print("=" * 60, file=sys.stderr)
        print("Invoice Validate API Request", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"Endpoint: {api_url}", file=sys.stderr)
        print(f"Method: POST", file=sys.stderr)
        print(f"Headers:", file=sys.stderr)
        for key, value in headers.items():
            if key.lower() == "apikey":
                masked_value = (
                    value[:4] + "****" + value[-4:] if len(value) > 8 else "****"
                )
                print(f"  {key}: {masked_value}", file=sys.stderr)
            else:
                print(f"  {key}: {value}", file=sys.stderr)
        print(f"Payload:", file=sys.stderr)
        print(f"  {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

    request_data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        api_url, data=request_data, headers=headers, method="POST"
    )

    # 发送请求，网络错误在内部捕获并返回 dict（resCode=0）
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        try:
            return json.loads(error_body)
        except json.JSONDecodeError:
            return {
                "resCode": e.code,
                "msg": f"HTTP Error: {e.code} {e.reason}",
                "data": None,
            }
    except urllib.error.URLError as e:
        return {"resCode": 0, "msg": f"Network Error: {e.reason}", "data": None}
    except Exception as e:
        return {"resCode": 0, "msg": f"Error: {str(e)}", "data": None}


def determine_exit_code(result: dict) -> tuple:
    """
    按优先级判定退出码，返回 (exit_code, reason_text)。

    网络错误通过 result 中 resCode==0 + msg 含 Network/Error 判断
    （由 call_invoice_validate_api 内部捕获返回）。

    优先级顺序：7(网络) → 4(余额) → 5(次数) → 2(服务异常) → 1(查验不通过) → 0(通过) → 8(兜底)
    Exit 3(认证) 和 Exit 6(参数) 在 main() 调用前处理，不在本函数中。
    """
    res_code = result.get("resCode")
    msg = result.get("msg", "")
    data = result.get("data")

    # Exit 7: 网络错误（resCode==0 表示请求本身失败，非 API 响应）
    if res_code == 0 and data is None:
        if "Network Error" in msg or "HTTP Error" in msg or "Error" in msg:
            return 7, "网络错误，请检查连接后重试"
        return 7, "请求失败：" + msg

    # 文件方式暂不支持提示（后端返回 resCode=200, msg 含"暂不支持"）
    if "暂不支持" in msg:
        return 6, msg

    # Exit 4: 余额不足
    if res_code == 402:
        return 4, "余额不足，请充值"

    # Exit 5: 次数超限
    if res_code == 403:
        return 5, "次数已用完，请购买套餐或等待重置"

    # Exit 2: 服务异常
    # resCode=400 + data==null，或 resCode=200 + data==null
    if (res_code == 400 and data is None) or (res_code == 200 and data is None):
        return 2, "查验服务异常：" + msg
    # resCode=400 + data!=null + isSuccess 非 false（缺失或非 false 视为异常）
    if res_code == 400 and data is not None:
        is_success = data.get("isSuccess")
        if is_success is not False:
            return 2, "查验服务异常：" + msg

    # Exit 1: 查验不通过
    if data is not None:
        is_success = data.get("isSuccess")
        if is_success is False:
            validate_msg = data.get("validateMessage", "")
            return 1, "查验未通过：" + validate_msg

    # Exit 0: 查验通过（isSuccess==True 且 validateCode==0 表示发票信息一致）
    if res_code == 200 and data is not None and data.get("isSuccess") is True:
        validate_code = data.get("validateCode")
        if validate_code == 0:
            validate_msg = data.get("validateMessage", "经查验，发票信息一致")
            return 0, validate_msg
        else:
            # isSuccess==True 但 validateCode!=0：查验操作成功，但发票不通过（如"查无此票"）
            validate_msg = data.get("validateMessage", "查验结果不一致")
            return 1, "查验未通过：" + validate_msg

    # Exit 8: 兜底
    return 8, "响应异常：" + msg


def format_output(result: dict, exit_code: int, reason: str, json_mode: bool = False) -> str:
    """
    格式化输出，reason 来自 determine_exit_code() 的中文消息。
    """
    if json_mode:
        return json.dumps(result, indent=2, ensure_ascii=False)

    if exit_code == 0:
        # 查验通过：结论 + 完整发票表格 + 查询状态
        data = result.get("data", {})
        invoice = data.get("invoice", {}) or {}
        lines = [
            "=" * 40,
            f"✅ 查验通过 — {reason}",
            "=" * 40,
            "",
            "📋 发票信息",
            "| 字段 | 值 |",
            "|------|-----|",
        ]

        def has_value(v):
            return v is not None and v != "" and v != "null"

        def safe_str(v):
            if isinstance(v, float) or isinstance(v, int):
                return str(v)
            return str(v) if v else ""

        def add_row(label, value):
            if has_value(value):
                lines.append(f"| {label} | {value} |")

        add_row("发票类型", invoice.get("InvoiceCategory"))
        add_row("发票代码", invoice.get("InvoiceCode"))
        add_row("发票号码", invoice.get("InvoiceNumber"))
        add_row("开票日期", invoice.get("InvoiceDate"))

        amount = invoice.get("Amount")
        if has_value(amount):
            add_row("价税合计", safe_str(amount) + " 元")

        total_price = invoice.get("TotalPrice")
        if has_value(total_price):
            add_row("不含税金额", safe_str(total_price) + " 元")

        buyer_parts = []
        for sub_field in ["BuyerCompany", "BuyerTaxCode", "BuyerAddress", "BuyerTelephone"]:
            v = invoice.get(sub_field)
            if has_value(v):
                buyer_parts.append(safe_str(v))
        if buyer_parts:
            add_row("购方", " / ".join(buyer_parts))

        seller_parts = []
        for sub_field in ["SellerCompany", "SellerTaxCode", "SellerAddress", "SellerTelephone"]:
            v = invoice.get(sub_field)
            if has_value(v):
                seller_parts.append(safe_str(v))
        if seller_parts:
            add_row("销方", " / ".join(seller_parts))

        add_row("银行账号", invoice.get("BankAccount"))
        add_row("备注", invoice.get("InvoiceComment"))

        lines.append("")
        lines.append("═" * 45)
        lines.append(f"  ✅ 查询状态：{reason}")
        lines.append("═" * 45)

        return "\n".join(lines)

    elif exit_code == 1:
        # 查验不通过：结论 + 可能原因
        lines = [
            "=" * 40,
            f"❌ {reason}",
            "=" * 40,
            "",
            "可能原因：",
            "1. 发票信息输入有误（号码/日期/代码与税局记录不匹配）",
            "2. 该发票为伪造或无效发票",
            "3. 税局系统中未查到该发票",
            "",
            "请核实发票原件信息后重试。",
        ]
        return "\n".join(lines)

    elif exit_code == 2:
        # 服务异常
        lines = [
            "=" * 40,
            f"⚠️ {reason}",
            "=" * 40,
            "",
            "请稍后重试。如持续出现此问题，可能是税局服务波动。",
        ]
        return "\n".join(lines)

    elif exit_code in (4, 5):
        # 余额不足 / 次数超限
        action = "充值" if exit_code == 4 else "购买套餐或等待重置"
        lines = [
            "=" * 40,
            f"⚠️ {reason}",
            "=" * 40,
            "",
            f"请前往 https://www.clawmate.net/user {action}。",
        ]
        return "\n".join(lines)

    elif exit_code == 7:
        # 网络错误
        lines = [
            "=" * 40,
            f"⚠️ {reason}",
            "=" * 40,
            "",
            "请检查网络连接后重试。",
        ]
        return "\n".join(lines)

    else:
        # exit 3, 6, 8 及其他：直接展示 reason
        return reason


def main():
    parser = argparse.ArgumentParser(
        description="ClawMate Invoice Validate API Client - 查验发票真伪",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --fphm "12345678" --kprq "20260424"
  %(prog)s --fphm "12345678" --kprq "20260424" --fpdm "1100191320" --json
  %(prog)s --fphm "12345678901234567890" --kprq "20260424" --verbose
  %(prog)s --validate-mode 2 --file "/path/to/invoice.pdf"
  %(prog)s --validate-mode 2 --file "/path/to/invoice.pdf" --json

API Key Source:
  CLAWMATE_API_KEY env var (required)

Get your API key from: https://www.clawmate.net/user
        """
    )

    parser.add_argument(
        "--fphm",
        help="发票号码（传统票 8 位 / 全电票 20 位）",
    )
    parser.add_argument(
        "--kprq",
        help="开票日期（格式：yyyyMMdd，如 20260424）",
    )
    parser.add_argument(
        "--fpdm",
        help="发票代码（传统票需要，全电票不需要）",
    )
    parser.add_argument(
        "--kjje",
        help="不含税金额",
    )
    parser.add_argument(
        "--jshj",
        help="价税合计",
    )
    parser.add_argument(
        "--jym",
        help="校验码（完整值或后 6 位）",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="输出完整 JSON 响应",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细请求/响应信息",
    )
    parser.add_argument(
        "--api-url",
        help="接口地址（默认：https://www.clawmate.net/server/test/Api/InvoiceValidate）",
    )
    parser.add_argument(
        "--validate-mode", "-m",
        type=int,
        choices=[1, 2, 3, 4],
        help="查验方式: 1=发票信息, 2=PDF文件, 3=图片文件, 4=ODF文件",
    )
    parser.add_argument(
        "--file", "-f",
        help="文件路径（validate-mode=2/3/4 时使用）",
    )
    parser.add_argument(
        "--file-base64",
        help="文件 Base64 内容（validate-mode=2/3/4 时使用，优先级高于 --file）",
    )

    args = parser.parse_args()

    # 1. 获取 API Key（Exit 3: 认证失败）
    api_key = get_api_key()
    if not api_key:
        print(
            json.dumps(
                {"resCode": 401, "msg": "API Key 未设置", "data": None},
                ensure_ascii=False,
            )
        )
        print(
            "\n请设置 CLAWMATE_API_KEY 环境变量",
            file=sys.stderr,
        )
        print(
            "获取 Key: https://www.clawmate.net/user",
            file=sys.stderr,
        )
        sys.exit(3)

    # 2. 调用前参数校验（Exit 6: 参数错误）
    validate_mode = args.validate_mode

    if validate_mode is not None and validate_mode >= 2:
        # 文件方式查验
        file_base64 = args.file_base64
        if not file_base64 and args.file:
            import base64
            try:
                with open(args.file, "rb") as f:
                    file_base64 = base64.b64encode(f.read()).decode("utf-8")
            except FileNotFoundError:
                print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
                sys.exit(6)
            except Exception as e:
                print(f"错误: 读取文件失败: {e}", file=sys.stderr)
                sys.exit(6)

        if not file_base64:
            print(
                "错误: 文件方式查验需要提供 --file 或 --file-base64 参数",
                file=sys.stderr,
            )
            sys.exit(6)

        result = call_invoice_validate_api(
            api_key=api_key,
            validate_mode=validate_mode,
            file_base64=file_base64,
            api_url=args.api_url, verbose=args.verbose
        )
    else:
        # 发票信息方式
        if not args.fphm or not args.kprq:
            print(
                "错误: 发票信息方式需要 --fphm 和 --kprq 参数",
                file=sys.stderr,
            )
            sys.exit(6)

        if not args.kprq.isdigit() or len(args.kprq) != 8:
            print(
                "错误: 开票日期格式无效，请使用 yyyyMMdd 格式（如 20260424）",
                file=sys.stderr,
            )
            sys.exit(6)

        # 3. 调用 API（网络错误已在 call_invoice_validate_api 内部捕获，返回 resCode=0 的 dict）
        result = call_invoice_validate_api(
            api_key=api_key, fphm=args.fphm, kprq=args.kprq,
            fpdm=args.fpdm, kjje=args.kjje, jshj=args.jshj, jym=args.jym,
            validate_mode=validate_mode,
            api_url=args.api_url, verbose=args.verbose
        )

    # 4. 安全检查：确保 result 是 dict
    if not isinstance(result, dict):
        result = {"resCode": 0, "msg": "响应解析异常", "data": None}

    # 5. 判定退出码
    exit_code, reason = determine_exit_code(result)

    # 6. 输出并退出
    utf8_print(format_output(result, exit_code, reason, json_mode=args.json))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()