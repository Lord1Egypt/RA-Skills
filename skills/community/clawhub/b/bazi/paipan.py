#!/usr/bin/env python3
"""
八字排盘 CLI 工具
调用 bagezi.top 排盘 API 计算八字以及大运流年信息。
"""

import argparse
import json
import sys

import requests

API_ENDPOINT = "http://api.bagezi.top/api/paipan"
DEFAULT_NAME = "张三"
TIMEOUT = 15


def paipan_api(name, gender, birthday_str):
    """
    调用八字排盘 API。

    Args:
        name (str): 姓名。
        gender (str): 性别（男/女）。
        birthday_str (str): 出生日期，ISO 8601 格式，如 1990-01-01T12:00:00.000Z。

    Returns:
        dict: API 返回的 JSON 数据。

    Raises:
        ValueError: 必填参数缺失。
        requests.exceptions.RequestException: 网络请求异常。
        json.JSONDecodeError: JSON 解析异常。
    """
    if not gender:
        raise ValueError("gender 是必填参数")
    if not birthday_str:
        raise ValueError("birthday_str 是必填参数")

    payload = {
        "name": name,
        "gender": gender,
        "birthday_str": birthday_str,
    }

    response = requests.post(API_ENDPOINT, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="调用 bagezi.top 排盘 API 计算八字信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""使用示例:
  python paipan.py -g 男 -b "1990-01-01T12:00:00.000Z"
  python paipan.py -n 李四 -g 女 -b "1995-05-20T08:30:00.000Z"
  python paipan.py --gender 男 --birthday_str "1988-12-12T10:00:00.000Z"
""",
    )

    parser.add_argument(
        "-n", "--name",
        type=str,
        default=DEFAULT_NAME,
        help=f"姓名（默认: {DEFAULT_NAME}）",
    )
    parser.add_argument(
        "-g", "--gender",
        type=str,
        required=True,
        help='性别（必填，如: 男、女）',
    )
    parser.add_argument(
        "-b", "--birthday_str",
        type=str,
        required=True,
        help='出生日期字符串（必填，ISO 8601 格式，如: 1990-01-01T12:00:00.000Z）',
    )

    args = parser.parse_args()

    try:
        result = paipan_api(
            name=args.name,
            gender=args.gender,
            birthday_str=args.birthday_str,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(f"参数错误: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout as e:
        print(f"请求超时: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
