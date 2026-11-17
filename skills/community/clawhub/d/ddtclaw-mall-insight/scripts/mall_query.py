#!/usr/bin/env python3
"""Download a complete mall package using the account's open-platform key."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://gotoshop-ai.com/ddtclaw/v1/malls"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search")
    search.add_argument("--name", required=True)
    search.add_argument("--city", default="")
    bundle = commands.add_parser("bundle")
    bundle.add_argument("--mall-id", required=True)
    bundle.add_argument("--radius", type=int, choices=(500,1000,2000,3000), default=1000)
    bundle.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    key = os.environ.get("DDT_API_KEY", "").strip()
    if not key:
        parser.error("请先设置 DDT_API_KEY")
    if args.command == "bundle":
        if args.output.exists():
            parser.error("目标文件已存在，请选择新的输出路径")
        if not args.output.parent.is_dir():
            parser.error("输出目录不存在")
    params = {"q":args.name,"city":args.city} if args.command=="search" else {"mall_id":args.mall_id,"radius_m":args.radius}
    request = urllib.request.Request(BASE+"/"+args.command+"?"+urllib.parse.urlencode(params),headers={"Authorization":"Bearer "+key,"Accept":"application/json"})
    try:
        with urllib.request.build_opener(NoRedirect).open(request,timeout=120) as response:
            raw=response.read()
            payload=json.loads(raw)
    except urllib.error.HTTPError as exc:
        print(json.dumps({"ok":False,"http_status":exc.code,"request_id":exc.headers.get("X-Request-Id", "")},ensure_ascii=False))
        return 1
    except (OSError, ValueError):
        print(json.dumps({"ok":False,"error":"获取失败，付费查询请先核对调用记录再重试"},ensure_ascii=False))
        return 1
    if payload.get("ok") is not True:
        print(json.dumps({"ok":False,"request_id":payload.get("request_id"),"error":"未取得完整数据"},ensure_ascii=False))
        return 1
    if args.command=="search":
        print(json.dumps(payload,ensure_ascii=False))
    else:
        if payload.get("data",{}).get("coverage",{}).get("shops_complete") is not True:
            raise RuntimeError("返回数据缺少完整性标记")
        descriptor=os.open(args.output,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        with os.fdopen(descriptor,"wb") as handle:
            handle.write(raw)
        print(json.dumps({"ok":True,"file":str(args.output.resolve()),"request_id":payload.get("request_id"),"charged_points":payload.get("charged_points"),"modules":list(payload['data']),"coverage":payload['data']['coverage']},ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
