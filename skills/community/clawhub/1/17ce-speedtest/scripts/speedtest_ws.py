#!/usr/bin/env python3
"""
17CE WebSocket 实时测速脚本
接口：wss://wsapi.17ce.com:8001/socket

认证：api_pwd + user（无IP限制，实时返回多节点结果）
依赖：pip install websockets

用法：
  python speedtest_ws.py http://example.com \\
    --user huangwg@gmail.com \\
    --apipwd PVCYVIQEGF8Y6D1G

示例：
  # 北京+上海双省电信+联通
  python speedtest_ws.py http://example.com --user u@gmail.com --apipwd KEY --pro-ids 221,49

  # JSON 输出
  python speedtest_ws.py http://example.com --user u@gmail.com --apipwd KEY --json
"""

import argparse
import asyncio
import base64
import hashlib
import json
import ssl
import sys
import time

ISP_MAP = {"1": "电信", "2": "联通", "3": "移动", "4": "教育网", "5": "铁通", "6": "多线"}
PROVINCE_MAP = {
    "221": "北京", "49": "上海", "335": "广东", "277": "浙江", "50": "四川",
    "280": "江苏", "246": "重庆", "233": "天津", "238": "河北", "262": "山东",
    "162": "河南", "131": "湖北", "147": "湖南", "202": "福建", "210": "安徽",
    "292": "江西", "55":  "贵州", "116": "云南", "104": "黑龙江","36":  "吉林",
    "85":  "辽宁", "179": "陕西", "189": "甘肃", "18":  "宁夏", "65":  "青海",
    "26":  "新疆", "21":  "西藏", "73":  "海南", "317": "广西", "100": "内蒙古",
    "126": "山西"
}


try:
    import websockets
except ImportError:
    print("❌ 请先安装依赖：pip install websockets", file=sys.stderr)
    sys.exit(1)

WS_URL = "wss://wsapi.17ce.com:8001/socket/"


def _md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def _b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

def gen_code(api_pwd: str, user: str, ut: str) -> str:
    """生成认证 code：md5(base64(md5(api_pwd)[4:23] + user + ut))"""
    return _md5(_b64(_md5(api_pwd)[4:23] + user.strip() + ut))


def build_ws_url(user: str, api_pwd: str) -> str:
    ut = str(int(time.time()))
    code = gen_code(api_pwd, user, ut)
    return f"{WS_URL}?ut={ut}&code={code}&user={user}"


def build_task(url: str, isp_list: list, area_list: list, num: int,
               pro_ids: str = "221,49", rt: str = "GET",
               host: str = None, cookie: str = None, agent: str = None) -> dict:
    task = {
        "txnid": int(time.time()),
        "nodetype": isp_list,
        "num": num,
        "Url": url,
        "TestType": "HTTP",
        "Host": host or "",
        "TimeOut": 20,
        "Request": rt,
        "NoCache": True,
        "Speed": 0,
        "Cookie": cookie or "",
        "Trace": False,
        "Referer": url,
        "UserAgent": agent or "curl/7.47.0",
        "FollowLocation": 2,
        "GetMD5": False,
        "GetResponseHeader": False,
        "MaxDown": 1048576,
        "AutoDecompress": True,
        "type": 1,
        "isps": isp_list,
        "pro_ids": pro_ids,   # 必须是字符串格式，如 "221,49"
        "areas": area_list,
        "PingSize": 32,
        "PingCount": 10,
    }
    return task


async def run_speedtest(ws_url: str, task: dict, timeout: int, output_json: bool) -> list:
    results = []
    node_info_map = {}

    try:
        async with websockets.connect(ws_url, open_timeout=15) as ws:
            if not output_json:
                print(f"✅ 已连接，等待认证...")

            logged_in = False
            start = time.time()
            header_printed = False

            while time.time() - start < timeout:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=5)
                except asyncio.TimeoutError:
                    if logged_in and time.time() - start > 30:
                        break
                    continue

                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                # 收到 login ok 后才发任务
                if not logged_in and data.get("rt") == 1 and data.get("msg") == "login ok":
                    logged_in = True
                    await ws.send(json.dumps(task, ensure_ascii=False))
                    if not output_json:
                        print(f"🚀 测速任务已发送，等待节点响应...\n")
                    continue

                # 任务被接受：显示节点总数并保存节点省份/ISP映射
                if data.get("type") == "TaskAccept":
                    task_data = data.get("data", {})
                    for tid, info in task_data.items():
                        nodes = info.get("nodes", {})
                        for nid, ninfo in nodes.items():
                            ni = ninfo.get("nodeinfo", {})
                            node_info_map[str(nid)] = {
                                "isp": ni.get("isp"),
                                "pro_id": ni.get("pro_id"),
                                "ip": ni.get("ip")
                            }

                        count = info.get("nodeCount", "?")
                        if not output_json:
                            print(f"   任务ID: {info.get('TaskId', tid)}  节点数: {count}")
                            print(f"\n{'节点ID':<10} {'省份':<6} {'ISP':<4} {'总耗时ms':<10} {'首字节ms':<10} {'DNS ms':<8} {'HTTP'}")
                            print("-" * 65)
                            header_printed = True
                    continue

                # 新的测速结果
                if data.get("type") == "NewData":
                    d = data.get("data", {})
                    node_id = str(d.get("NodeID", ""))
                    http_code = d.get("HttpCode", 0)
                    total = d.get("TotalTime", 0) * 1000  # 秒→毫秒
                    ttfb  = d.get("TTFBTime", 0) * 1000
                    dns   = d.get("NsLookup", 0) * 1000
                    src_ip = d.get("SrcIP", "")
                    
                    ni = node_info_map.get(node_id, {})
                    prov = PROVINCE_MAP.get(str(ni.get("pro_id")), "未知")
                    isp_name = ISP_MAP.get(str(ni.get("isp")), "未知")

                    result = {
                        "NodeID": node_id,
                        "Province": prov,
                        "ISP": isp_name,
                        "HttpCode": http_code,
                        "TotalTime_ms": round(total, 1),
                        "TTFBTime_ms": round(ttfb, 1),
                        "DNS_ms": round(dns, 1),
                        "SrcIP": src_ip,
                        "TaskId": d.get("TaskId", ""),
                    }
                    results.append(result)

                    if not output_json:
                        if not header_printed:
                            print(f"\n{'节点ID':<10} {'省份':<6} {'ISP':<4} {'总耗时ms':<10} {'首字节ms':<10} {'DNS ms':<8} {'HTTP'}")
                            print("-" * 65)
                            header_printed = True
                        print(f"{node_id:<10} {prov:<6} {isp_name:<4} {total:<10.1f} {ttfb:<10.1f} {dns:<8.1f} {http_code}")
                    continue

                # 任务结束
                if data.get("type") == "TaskEnd":
                    d = data.get("data", {})
                    if not output_json:
                        ok  = d.get("TotalCountOK", 0)
                        err = d.get("TotalCountErr", 0)
                        tot = d.get("TotalCount", 0)
                        print(f"\n✅ 测速完成：{tot} 个节点，成功 {ok}，失败 {err}")
                    break

    except websockets.exceptions.WebSocketException as e:
        if not output_json:
            print(f"❌ WebSocket 错误: {e}", file=sys.stderr)
        else:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        if not output_json:
            print(f"❌ 错误: {e}", file=sys.stderr)
        else:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="17CE WebSocket 实时测速",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="Target URL to test (include http:// or https://)")
    parser.add_argument("--user", required=True, help="17CE Account Email (Required)")
    parser.add_argument("--apipwd", required=True, help="17CE API PWD (Required)")
    parser.add_argument("--isp", nargs="+", type=int, default=[1, 2, 3], metavar="N",
                        help="运营商 (1=电信 2=联通 3=移动)，默认 1 2 3")
    parser.add_argument("--area", nargs="+", type=int, default=[1], metavar="N",
                        help="区域 (1=大陆 2=港澳台 3=海外)，默认 1")
    parser.add_argument("--num", type=int, default=2, help="每ISP节点数，默认 2")
    parser.add_argument("--pro-ids", default="221,49",
                        help="省份ID字符串，逗号分隔，如 '221,49'（北京,上海），默认 '221,49'")
    parser.add_argument("--rt", default="GET", choices=["GET", "POST", "HEAD"],
                        help="HTTP 请求方式，默认 GET")
    parser.add_argument("--host", help="自定义 Host 头")
    parser.add_argument("--cookie", help="自定义 Cookie")
    parser.add_argument("--agent", help="自定义 User-Agent")
    parser.add_argument("--timeout", type=int, default=60, help="超时秒数，默认 60")
    parser.add_argument("--json", dest="output_json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--html", dest="output_html", action="store_true", help="HTML 格式输出")

    args = parser.parse_args()

    ws_url = build_ws_url(args.user, args.apipwd)
    task = build_task(
        url=args.url,
        isp_list=args.isp,
        area_list=args.area,
        num=args.num,
        pro_ids=args.pro_ids,
        rt=args.rt,
        host=args.host,
        cookie=args.cookie,
        agent=args.agent,
    )

    if not args.output_json and not args.output_html:
        print(f"🌐 17CE WebSocket 测速")
        print(f"   URL   : {args.url}")
        print(f"   ISP   : {args.isp}  区域: {args.area}  节点/ISP: {args.num}")
        print(f"   省份  : {args.pro_ids}")

    results = asyncio.run(run_speedtest(ws_url, task, args.timeout, args.output_json or args.output_html))

    if args.output_html:
        try:
            import report
            html = report.generate_html(results, args.url)
            print(html)
        except ImportError:
            print("❌ 缺少 report.py，无法生成 HTML 报表", file=sys.stderr)
            sys.exit(1)
    elif args.output_json:
        if results:
            avg = sum(r["TotalTime_ms"] for r in results) / len(results)
            print(json.dumps({
                "success": True,
                "count": len(results),
                "avg_ms": round(avg, 1),
                "results": results
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, "error": "未收到测速数据"}, ensure_ascii=False))
    else:
        if results:
            avg = sum(r["TotalTime_ms"] for r in results) / len(results)
            print(f"   平均响应时间: {avg:.0f} ms")


if __name__ == "__main__":
    main()
