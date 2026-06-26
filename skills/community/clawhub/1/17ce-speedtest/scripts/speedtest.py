#!/usr/bin/env python3
"""
17CE 网站测速脚本
用法：python speedtest.py <url> [选项]

支持两种认证方式：
  1. 账号密码 (appKey/appSecret)：调用 /api/site/http
  2. api_pwd Code 认证：调用 /apis/http（推荐）

示例：
  # 使用 api_pwd（推荐，不需要登录密码）
  python speedtest.py http://example.com --apikey yiqice@qq.com --apipwd OGIBKI978JEZZO2F

  # 使用账号密码
  python speedtest.py http://example.com --user admin --pass secret
"""

import argparse
import hashlib
import base64
import json
import sys
import time
import requests
import warnings

# 忽略OpenSSL警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

LEGACY_API_BASE = "http://www.17ce.com/api/site"
API_BASE = "http://www.17ce.com/apis"


def gen_code(api_pwd: str, username: str, timestamp: int) -> str:
    """
    根据 api_pwd 生成认证 code
    算法：md5(base64(substr(md5(api_pwd), 4, 19) + username + timestamp))
    与 ApisController::check_api 中 $decrypt2 逻辑一致
    """
    api_pwd_md5 = hashlib.md5(api_pwd.encode()).hexdigest()
    part = api_pwd_md5[4:23]          # substr($md5, 4, 19)
    raw = part + username.strip() + str(timestamp)
    code = hashlib.md5(base64.b64encode(raw.encode())).hexdigest()
    return code


def submit_with_apipwd(url: str, username: str, api_pwd: str,
                       isp_list: list = None, area_list: list = None,
                       sid_list: list = None, rt: int = 1,
                       host: str = None, referer: str = None,
                       cookie: str = None, agent: str = None,
                       nocache: int = 0) -> dict:
    """
    使用 api_pwd Code 认证提交测速 → /apis/http
    """
    t = int(time.time())
    code = gen_code(api_pwd, username, t)

    data = [
        ("user", username),
        ("t", str(t)),
        ("code", code),
        ("url", url),
        ("rt", str(rt)),
        ("nocache", str(nocache)),
    ]

    if sid_list:
        sid_str = ",".join(str(s) for s in sid_list[:3])
        data.append(("sid", sid_str))
    else:
        if isp_list is None:
            isp_list = [0]
        for isp in isp_list:
            data.append(("isp", str(isp)))
        if area_list:
            for area in area_list:
                data.append(("area", str(area)))

    if host:
        data.append(("host", host))
    if referer:
        data.append(("referer", referer))
    if cookie:
        data.append(("cookie", cookie))
    if agent:
        data.append(("agent", agent))

    try:
        response = requests.post(
            f"{API_BASE}/http",
            data=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "message": "请求超时，请检查网络连接"}
    except requests.exceptions.ConnectionError as e:
        return {"success": False, "message": f"连接失败: {e}"}
    except (json.JSONDecodeError, ValueError) as e:
        return {"success": False, "message": f"响应解析失败: {e}"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"请求错误: {e}"}

    return _parse_result(result)


def submit_speedtest(url: str, username: str, password: str,
                     isp_list: list = None, area_list: list = None,
                     sid_list: list = None, rt: int = 1,
                     host: str = None, referer: str = None,
                     cookie: str = None, agent: str = None,
                     nocache: int = 0) -> dict:
    """
    使用账号密码提交测速 → /api/site/http
    """
    data = [
        ("appKey", username),
        ("appSecret", password),
        ("url", url),
        ("rt", str(rt)),
        ("nocache", str(nocache)),
    ]

    if sid_list:
        sid_str = ",".join(str(s) for s in sid_list[:3])
        data.append(("sid", sid_str))
    else:
        if isp_list is None:
            isp_list = [0]
        for isp in isp_list:
            data.append(("isp[]", str(isp)))
        if area_list:
            for area in area_list:
                data.append(("area[]", str(area)))

    if host:
        data.append(("host", host))
    if referer:
        data.append(("referer", referer))
    if cookie:
        data.append(("cookie", cookie))
    if agent:
        data.append(("agent", agent))

    try:
        response = requests.post(
            f"{LEGACY_API_BASE}/http",
            data=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "message": "请求超时"}
    except requests.exceptions.ConnectionError as e:
        return {"success": False, "message": f"连接失败: {e}"}
    except (json.JSONDecodeError, ValueError) as e:
        return {"success": False, "message": f"响应解析失败: {e}"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"请求错误: {e}"}

    return _parse_result(result)


def _parse_result(result: dict) -> dict:
    """解析API响应"""
    # api_pwd 接口的错误码在 result['rt']==false 时
    if result.get("rt") is False or result.get("rt") == "false":
        code = str(result.get("code", ""))
        error_messages = {
            "10001": "用户名不能为空",
            "10002": "code不能为空",
            "10003": "时间戳不能为空",
            "10004": "时间戳超过有效范围（需在5分钟内）",
            "10005": "接口用户不存在",
            "10006": "接口未开通或被禁用",
            "10007": "非法请求（IP限制）",
            "10008": "用户验证失败（api_pwd 错误）",
            "10009": "积分不足，请充值",
            "10010": "测试URL不能为空",
            "10011": "ISP不能为空",
            "10012": "URL格式不正确",
        }
        msg = error_messages.get(code, result.get("error", str(result)))
        return {"success": False, "message": msg, "error_code": code}

    # 账号密码接口的错误码
    if result.get("error_code"):
        error_messages = {
            "1001": "用户名或密码为空",
            "1002": "账户或密码错误",
            "3002": "测试过于频繁，请稍后再试",
            "3003": "1分钟内检测超过50次",
            "3004": "30分钟内检测超过500次",
            "3005": "24小时内检测超过1000次",
            "3006": "请选择ISP运营商类型",
            "3007": "没有找到符合条件的监测点",
        }
        code = str(result.get("error_code", ""))
        msg = error_messages.get(code, result.get("error_message", "未知错误"))
        return {"success": False, "message": msg, "error_code": code}

    # 成功：新接口返回的数据格式
    if result.get("teststatus") == 1 or (result.get("rt") is True and result.get("data")):
        data = result.get("data", result)
        tid = data.get("tid", result.get("tid", ""))
        return {
            "success": True,
            "tid": tid,
            "id": data.get("id", result.get("id")),
            "result_url": f"https://www.17ce.com/v/{tid}",
            "message": "测速任务提交成功，约 60~120 秒后可查看结果"
        }

    return {"success": False, "message": result.get("message", str(result))}


def main():
    parser = argparse.ArgumentParser(
        description="17CE 网站测速工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
认证方式（二选一）：
  1. api_pwd 方式（推荐）：传 --apikey + --apipwd
  2. 账号密码方式：        传 --user  + --pass

示例：
  # 用 api_pwd（推荐）
  python speedtest.py http://example.com --apikey user@example.com --apipwd YOURKEY

  # 仅测电信+联通
  python speedtest.py http://example.com --apikey user@example.com --apipwd KEY --isp 1 2

  # 指定节点ID
  python speedtest.py http://example.com --apikey user@example.com --apipwd KEY --sid 1 3 58

  # 用账号密码
  python speedtest.py http://example.com --user admin --pass secret
        """
    )
    parser.add_argument("url", help="待测试的URL（含协议头）")

    # api_pwd 认证（推荐）
    auth_group = parser.add_argument_group("认证参数（二选一）")
    auth_group.add_argument("--apikey", help="17CE账号用户名（搭配 --apipwd 使用）")
    auth_group.add_argument("--apipwd", help="17CE API密码（api_pwd，推荐方式，不需要登录密码）")
    # 账号密码认证（兼容旧方式）
    auth_group.add_argument("--user", "-u", help="17CE账号用户名（搭配 --pass 使用）")
    auth_group.add_argument("--pass", "-p", dest="password", help="17CE账号密码")

    parser.add_argument("--isp", nargs="+", type=int, default=None, metavar="N",
                        help="运营商 (0=全部, 1=电信, 2=联通, 3=移动)")
    parser.add_argument("--area", nargs="+", type=int, default=None, metavar="N",
                        help="区域 (0=全部, 1=大陆, 2=港澳台, 3=海外)")
    parser.add_argument("--sid", nargs="+", type=int, default=None, metavar="N",
                        help="指定节点ID（最多3个）")
    parser.add_argument("--rt", type=int, default=1, choices=[1, 2, 3],
                        help="请求方式 (1=GET, 2=POST, 3=HEAD)")
    parser.add_argument("--host", help="自定义Host头")
    parser.add_argument("--referer", help="自定义Referer")
    parser.add_argument("--cookie", help="自定义Cookie")
    parser.add_argument("--agent", help="自定义User-Agent")
    parser.add_argument("--nocache", action="store_true", help="禁用缓存")
    parser.add_argument("--json", dest="output_json", action="store_true", help="以JSON格式输出")
    parser.add_argument("--wait", type=int, default=0, metavar="SECONDS",
                        help="等待N秒后提示查看结果（0=不等待）")

    args = parser.parse_args()

    # 选择认证方式
    if args.apikey and args.apipwd:
        result = submit_with_apipwd(
            url=args.url,
            username=args.apikey,
            api_pwd=args.apipwd,
            isp_list=args.isp,
            area_list=args.area,
            sid_list=args.sid,
            rt=args.rt,
            host=args.host,
            referer=args.referer,
            cookie=args.cookie,
            agent=args.agent,
            nocache=1 if args.nocache else 0,
        )
    elif args.user and args.password:
        result = submit_speedtest(
            url=args.url,
            username=args.user,
            password=args.password,
            isp_list=args.isp,
            area_list=args.area,
            sid_list=args.sid,
            rt=args.rt,
            host=args.host,
            referer=args.referer,
            cookie=args.cookie,
            agent=args.agent,
            nocache=1 if args.nocache else 0,
        )
    else:
        parser.error("请提供认证信息：--apikey + --apipwd  或  --user + --pass")

    if args.output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   任务ID   : {result['tid']}")
            print(f"   结果链接 : {result['result_url']}")
            if args.wait > 0:
                print(f"\n⏳ 等待 {args.wait} 秒...", end="", flush=True)
                time.sleep(args.wait)
                print(f"\n🔗 请访问查看结果：{result['result_url']}")
        else:
            print(f"❌ 测速失败: {result['message']}")
            if result.get("error_code"):
                print(f"   错误码: {result['error_code']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
