#!/usr/bin/env python3
"""
chelaile-bus: 一句话查公交实时（MCP stdio 直连版，无 mcporter 依赖）
kimiclaw 适配修复（2026-09-22）: 原版走 `mcporter call chelaile.bus_*`，
kimiclaw 的 mcporter 无 chelaile server，改为直接 spawn MCP server 走 JSON-RPC stdio。

用法:
  python3 query-bus.py <线路号> [目标站名] [--city 027]
  python3 query-bus.py 311 展春园西路北口
  python3 query-bus.py 311          # 不指定站 → 列出线路详情+在线车辆
"""
import json, subprocess, sys, argparse, select, time

SERVER_CMD = ["npx", "-y", "chelaile-mcp-server"]

class MCPClient:
    def __init__(self):
        self.proc = subprocess.Popen(
            SERVER_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self._id = 0

    def _send(self, msg):
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def _recv(self, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if select.select([self.proc.stdout], [], [], 0.5)[0]:
                line = self.proc.stdout.readline()
                if not line:
                    raise RuntimeError("MCP server closed stdout")
                msg = json.loads(line)
                # 跳过 notification
                if "method" in msg and "id" not in msg:
                    continue
                return msg
        raise TimeoutError("MCP server response timeout")

    def _rpc(self, method, params=None):
        self._id += 1
        self._send({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}})
        resp = self._recv()
        if "error" in resp:
            raise RuntimeError(f"RPC error: {resp['error']}")
        return resp.get("result", {})

    def initialize(self):
        self._rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "chelaile-bus", "version": "1.1.0"}
        })
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def call(self, tool, args):
        result = self._rpc("tools/call", {"name": tool, "arguments": args})
        # MCP 返回 content[0].text，通常是 JSON 字符串
        for c in result.get("content", []):
            if c.get("type") == "text":
                try:
                    return json.loads(c["text"])
                except (json.JSONDecodeError, KeyError):
                    return c["text"]
        return result

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="公交实时查询")
    ap.add_argument("line", help="线路号，如 311")
    ap.add_argument("stop", nargs="?", default="", help="目标站名（可选）")
    ap.add_argument("--city", default="027", help="城市ID，默认 027 北京")
    args = ap.parse_args()

    print(f"🔍 查 {args.line} 路（city={args.city}）...")
    client = MCPClient()
    try:
        client.initialize()

        # 1. 搜线路
        search = client.call("bus_search", {"city_id": args.city, "keyword": args.line, "response_format": "json"})
        lines = search.get("lines", []) if isinstance(search, dict) else []
        if not lines:
            print(f"❌ 没找到线路 {args.line}")
            sys.exit(1)
        line0 = lines[0]
        line_id = line0["lineId"]
        dirs = line0.get("directions", [{}])
        d0 = dirs[0] if dirs else {}
        print(f"✅ {line0.get('name')}路 lineId={line_id} 方向0: {d0.get('startSn','?')} → {d0.get('endSn','?')}")

        # 2. 线路详情
        detail = client.call("bus_get_line_detail", {"city_id": args.city, "line_id": line_id, "response_format": "json"})
        line_info = detail.get("line", {})
        print(f"🕒 首末班 {line_info.get('firstTime','?')}-{line_info.get('lastTime','?')} 票价 {line_info.get('price','?')} 共 {line_info.get('stationsNum','?')} 站")

        stations = detail.get("stations", [])
        buses = detail.get("buses", [])
        print(f"🚌 线上车辆: {len(buses)} 辆")
        for b in buses:
            st = next((s["sn"] for s in stations if s["order"] == b.get("order")), f"order={b.get('order')}")
            print(f"   - 在 {st} 附近，速度 {b.get('speed','?')} km/h")

        # 3. 指定站 → 实时到站
        if args.stop:
            stn = next((s for s in stations if args.stop in s["sn"]), None)
            if not stn:
                print(f"❌ 没找到站点 '{args.stop}'，线路站点：")
                for s in stations:
                    print(f"   {s['order']}. {s['sn']}")
                sys.exit(1)
            print(f"\n🚏 {stn['sn']} (order={stn['order']}) 实时到站：")
            rt = client.call("bus_get_line_realtime", {
                "city_id": args.city, "line_id": line_id,
                "target_order": str(stn["order"]), "station_id": stn["sId"],
                "lat": str(stn["wgsLat"]), "lng": str(stn["wgsLng"]),
                "response_format": "json"
            })
            for b in rt.get("buses", []):
                eta = b.get("eta")
                if eta:
                    print(f"   ⏱ 约 {eta.get('travelTime','?')} 秒到站（{eta.get('displayTime','?')}）")
                else:
                    st = next((s["sn"] for s in stations if s["order"] == b.get("order")), f"order={b.get('order')}")
                    print(f"   - 在 {st} 附近，ETA 暂无（仅最近一辆有预测）")
            if not rt.get("buses"):
                print("   当前无在线车辆开往该站（可能已收班或未发车）")
    finally:
        client.close()


if __name__ == "__main__":
    main()
