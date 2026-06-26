#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

DEFAULT_SERVER = 'caocao-chuxing'
DEFAULT_CONFIG = Path.cwd() / 'config' / 'mcporter.json'
BASE_TEMPLATE = 'https://mcp.caocaokeji.cn/mcp/api?key={api_key}'


def load_config(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {'mcpServers': {}, 'imports': []}


def save_config(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def configure(api_key: str, config_path: Path, server_name: str) -> None:
    data = load_config(config_path)
    data.setdefault('mcpServers', {})[server_name] = {
        'baseUrl': BASE_TEMPLATE.format(api_key=api_key),
        'description': '曹操出行 MCP',
    }
    save_config(config_path, data)
    print(f'Configured {server_name} in {config_path}')


def find_base_url(config_path: Path, server_name: str) -> str:
    data = load_config(config_path)
    server = (data.get('mcpServers') or {}).get(server_name) or {}
    url = server.get('baseUrl') or server.get('url')
    if not url:
        raise SystemExit(f'未找到 {server_name} 配置，请先执行 configure')
    return url


def rpc_call(base_url: str, tool_name: str, arguments: dict, request_id: int = 1) -> dict:
    payload = {
        'jsonrpc': '2.0',
        'id': request_id,
        'method': 'tools/call',
        'params': {'name': tool_name, 'arguments': arguments},
    }
    req = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def extract_text(resp: dict) -> str:
    return (((resp.get('result') or {}).get('content') or [{}])[0].get('text') or '').strip()


def parse_json_maybe(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


def parse_estimate_text(text: str) -> dict:
    models = []
    for line in text.splitlines():
        m = re.search(r'\d+\.(.+?):\s*约\s*(\d+)\s*元\s*\(品类代码:\s*(\d+)\)', line)
        if m:
            models.append({
                'name': m.group(1).strip(),
                'estimatedPrice': int(m.group(2)),
                'callOrderServiceType': m.group(3),
            })
    estimate_id_match = re.search(r'预估流程ID:\s*(\d+)', text)
    return {
        'estimateId': estimate_id_match.group(1) if estimate_id_match else None,
        'models': models,
        'rawText': text,
    }


def command_maps(args):
    base = find_base_url(args.config, args.server_name)
    resp = rpc_call(base, 'maps_text_poi', {'keywords': args.keywords, 'cityName': args.city_name} if args.city_name else {'keywords': args.keywords})
    txt = extract_text(resp)
    parsed = parse_json_maybe(txt)
    print(json.dumps(parsed if parsed is not None else {'rawText': txt}, ensure_ascii=False, indent=2))


def command_estimate(args):
    base = find_base_url(args.config, args.server_name)
    resp = rpc_call(base, 'trip_estimate', {
        'fromLat': str(args.from_lat), 'fromLng': str(args.from_lng),
        'fromName': args.from_name,
        'toLat': str(args.to_lat), 'toLng': str(args.to_lng),
        'toName': args.to_name,
    })
    txt = extract_text(resp)
    print(json.dumps(parse_estimate_text(txt), ensure_ascii=False, indent=2))


def command_link(args):
    base = find_base_url(args.config, args.server_name)
    resp = rpc_call(base, 'trip_generate_ride_link', {
        'fromLat': str(args.from_lat), 'fromLng': str(args.from_lng),
        'fromName': args.from_name,
        'toLat': str(args.to_lat), 'toLng': str(args.to_lng),
        'toName': args.to_name,
    })
    print(extract_text(resp))


def command_create(args):
    base = find_base_url(args.config, args.server_name)
    resp = rpc_call(base, 'trip_create_order', {
        'estimateId': str(args.estimate_id),
        'callOrderServiceType': str(args.call_order_service_type),
    })
    print(extract_text(resp))


def command_query(args):
    base = find_base_url(args.config, args.server_name)
    resp = rpc_call(base, 'trip_query_order', {'orderNo': str(args.order_no)})
    print(extract_text(resp))


def command_cancel(args):
    base = find_base_url(args.config, args.server_name)
    body = {'orderNo': str(args.order_no)}
    if args.cancel_reason:
        body['cancelReason'] = args.cancel_reason
    resp = rpc_call(base, 'trip_cancel_order', body)
    print(extract_text(resp))


def command_ride_flow(args):
    base = find_base_url(args.config, args.server_name)

    start_resp = rpc_call(base, 'maps_text_poi', {'keywords': args.from_keywords, 'cityName': args.city_name} if args.city_name else {'keywords': args.from_keywords}, 1)
    end_resp = rpc_call(base, 'maps_text_poi', {'keywords': args.to_keywords, 'cityName': args.city_name} if args.city_name else {'keywords': args.to_keywords}, 2)

    start_candidates = parse_json_maybe(extract_text(start_resp)) or []
    end_candidates = parse_json_maybe(extract_text(end_resp)) or []
    if not start_candidates or not end_candidates:
        raise SystemExit('起点或终点未搜到结果')

    start = start_candidates[0]
    end = end_candidates[0]

    estimate_resp = rpc_call(base, 'trip_estimate', {
        'fromLat': str(start['location']['lat']), 'fromLng': str(start['location']['lng']),
        'fromName': start['displayName'],
        'toLat': str(end['location']['lat']), 'toLng': str(end['location']['lng']),
        'toName': end['displayName'],
    }, 3)
    estimate = parse_estimate_text(extract_text(estimate_resp))

    result = {
        'start': start,
        'end': end,
        'estimate': estimate,
    }

    if args.action == 'estimate':
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    models = estimate.get('models') or []
    if not models:
        raise SystemExit('未获取到可用车型')

    if args.service_type:
        chosen = next((m for m in models if str(m['callOrderServiceType']) == str(args.service_type)), None)
        if not chosen:
            raise SystemExit(f'未找到 service_type={args.service_type} 对应车型')
    else:
        chosen = sorted(models, key=lambda x: x['estimatedPrice'])[0]

    result['chosenModel'] = chosen

    if args.action == 'link':
        link_resp = rpc_call(base, 'trip_generate_ride_link', {
            'fromLat': str(start['location']['lat']), 'fromLng': str(start['location']['lng']),
            'fromName': start['displayName'],
            'toLat': str(end['location']['lat']), 'toLng': str(end['location']['lng']),
            'toName': end['displayName'],
        }, 4)
        result['linkText'] = extract_text(link_resp)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    create_resp = rpc_call(base, 'trip_create_order', {
        'estimateId': str(estimate['estimateId']),
        'callOrderServiceType': str(chosen['callOrderServiceType']),
    }, 5)
    result['createOrderText'] = extract_text(create_resp)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='曹操出行 MCP helper')
    p.add_argument('--config', type=Path, default=DEFAULT_CONFIG, help='mcporter.json 路径')
    p.add_argument('--server-name', default=DEFAULT_SERVER, help='服务名')
    sub = p.add_subparsers(dest='cmd', required=True)

    c = sub.add_parser('configure', help='写入 MCP 配置')
    c.add_argument('--api-key', required=True)

    m = sub.add_parser('maps_text_poi', help='地址搜索')
    m.add_argument('--keywords', required=True)
    m.add_argument('--city-name')

    e = sub.add_parser('trip_estimate', help='价格预估')
    for name in ['from-lat', 'from-lng', 'to-lat', 'to-lng']:
        e.add_argument(f'--{name}', required=True)
    e.add_argument('--from-name', required=True)
    e.add_argument('--to-name', required=True)

    l = sub.add_parser('trip_generate_ride_link', help='生成打车链接')
    for name in ['from-lat', 'from-lng', 'to-lat', 'to-lng']:
        l.add_argument(f'--{name}', required=True)
    l.add_argument('--from-name', required=True)
    l.add_argument('--to-name', required=True)

    co = sub.add_parser('trip_create_order', help='直接下单')
    co.add_argument('--estimate-id', required=True)
    co.add_argument('--call-order-service-type', required=True)

    q = sub.add_parser('trip_query_order', help='查询订单')
    q.add_argument('--order-no', required=True)

    ca = sub.add_parser('trip_cancel_order', help='取消订单')
    ca.add_argument('--order-no', required=True)
    ca.add_argument('--cancel-reason')

    rf = sub.add_parser('ride_flow', help='高层打车流程：搜地点 -> 估价 -> 生成链接/下单')
    rf.add_argument('--from-keywords', required=True)
    rf.add_argument('--to-keywords', required=True)
    rf.add_argument('--city-name')
    rf.add_argument('--action', choices=['estimate', 'link', 'create-order'], default='estimate')
    rf.add_argument('--service-type', help='指定车型；不填则默认最便宜')
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == 'configure':
        configure(args.api_key, args.config, args.server_name)
    elif args.cmd == 'maps_text_poi':
        command_maps(args)
    elif args.cmd == 'trip_estimate':
        command_estimate(args)
    elif args.cmd == 'trip_generate_ride_link':
        command_link(args)
    elif args.cmd == 'trip_create_order':
        command_create(args)
    elif args.cmd == 'trip_query_order':
        command_query(args)
    elif args.cmd == 'trip_cancel_order':
        command_cancel(args)
    elif args.cmd == 'ride_flow':
        command_ride_flow(args)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
