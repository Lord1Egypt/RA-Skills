#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付宝异步通知中继 — 开发者 CLI

一站式完成：注册 → 监听 → 验签 → 查询

用法：
  python3 cli.py register           自助注册，获取凭证
  python3 cli.py listen             实时监听通知（SSE）
  python3 cli.py list               查询最近通知
  python3 cli.py get <id>           查看单条通知详情
  python3 cli.py verify <id>        验签指定通知
  python3 cli.py status             检查服务状态
  python3 cli.py config             查看当前配置
  python3 cli.py export <id>        导出原始报文到文件

⚠️  仅限联调 / 内部调试，不可用于生产。
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════════════
# ANSI 颜色（自动检测 TTY）
# ═══════════════════════════════════════════════════════════

_NO_COLOR = not sys.stdout.isatty() or os.environ.get("NO_COLOR")


def _c(code, text):
    if _NO_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def green(t):   return _c("32", t)
def red(t):     return _c("31", t)
def yellow(t):  return _c("33", t)
def cyan(t):    return _c("36", t)
def bold(t):    return _c("1", t)
def dim(t):     return _c("2", t)


# ═══════════════════════════════════════════════════════════
# 配置管理
# ═══════════════════════════════════════════════════════════

CONFIG_FILENAME = ".alipay-notify.json"


def _config_paths():
    """按优先级返回可能的配置文件路径。"""
    paths = []
    # 当前目录
    paths.append(os.path.join(os.getcwd(), CONFIG_FILENAME))
    # 项目根目录（向上找 .git）
    d = os.getcwd()
    for _ in range(10):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
        if os.path.isdir(os.path.join(d, ".git")):
            paths.append(os.path.join(d, CONFIG_FILENAME))
            break
    # HOME
    home = os.path.expanduser("~")
    paths.append(os.path.join(home, ".alipay-notify", "config.json"))
    return paths


def load_config():
    """
    加载配置，优先级：环境变量 > 配置文件。
    """
    cfg = {}

    # 从文件加载
    for p in _config_paths():
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            cfg["_config_path"] = p
            break

    # 环境变量覆盖
    if os.environ.get("NOTIFY_API_URL"):
        cfg["server_url"] = os.environ["NOTIFY_API_URL"].rstrip("/")
    if os.environ.get("NOTIFY_API_KEY"):
        cfg["api_key"] = os.environ["NOTIFY_API_KEY"]
    if os.environ.get("ALIPAY_PLATFORM_PUBLIC_KEY"):
        cfg["alipay_public_key"] = os.environ["ALIPAY_PLATFORM_PUBLIC_KEY"]

    return cfg


def save_config(cfg):
    """保存配置到当前目录的 .alipay-notify.json。"""
    path = os.path.join(os.getcwd(), CONFIG_FILENAME)
    save_data = {k: v for k, v in cfg.items() if not k.startswith("_")}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    return path


def require_config(cfg, *keys):
    """检查必要配置项，缺失时给出友好提示。"""
    missing = [k for k in keys if not cfg.get(k)]
    if missing:
        print(red("\n✗ 缺少配置项：") + ", ".join(missing))
        print(dim("  请先运行 ") + bold("python3 cli.py register") + dim(" 或手动设置环境变量"))
        print(dim("  参考: NOTIFY_API_URL, NOTIFY_API_KEY, ALIPAY_PLATFORM_PUBLIC_KEY\n"))
        sys.exit(1)


# ═══════════════════════════════════════════════════════════
# HTTP 客户端（仅用 stdlib，零额外依赖）
# ═══════════════════════════════════════════════════════════

def http_request(method, url, headers=None, body=None, stream=False, timeout=15):
    """统一 HTTP 请求封装。"""
    hdrs = headers or {}
    data = None
    if body is not None:
        if isinstance(body, dict):
            data = json.dumps(body).encode("utf-8")
            hdrs.setdefault("Content-Type", "application/json")
        elif isinstance(body, bytes):
            data = body
        else:
            data = str(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        if stream:
            return resp
        return {"status": resp.status, "body": resp.read().decode("utf-8")}
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8")
        except Exception:
            pass
        return {"status": e.code, "body": body_text}
    except urllib.error.URLError as e:
        print(red(f"\n✗ 连接失败: {e.reason}"))
        print(dim(f"  目标: {url}"))
        sys.exit(1)


def api_get(cfg, path, params=None):
    url = cfg["server_url"] + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return http_request("GET", url, headers={"Authorization": f"Bearer {cfg['api_key']}"})


def api_post(cfg, path, body=None):
    url = cfg["server_url"] + path
    return http_request("POST", url, headers={"Authorization": f"Bearer {cfg['api_key']}"}, body=body)


def api_json(resp):
    try:
        return json.loads(resp["body"])
    except (json.JSONDecodeError, KeyError):
        return None


# ═══════════════════════════════════════════════════════════
# RSA2 验签
# ═══════════════════════════════════════════════════════════

def _load_public_key(b64_key):
    """从 Base64 字符串加载支付宝 RSA 公钥。"""
    try:
        from cryptography.hazmat.primitives import serialization
        pem = f"-----BEGIN PUBLIC KEY-----\n{b64_key.strip()}\n-----END PUBLIC KEY-----"
        return serialization.load_pem_public_key(pem.encode("utf-8"))
    except ImportError:
        print(yellow("  ⚠ 未安装 cryptography 库，无法验签"))
        print(dim("    运行: pip install cryptography"))
        return None
    except Exception:
        return None


def verify_rsa2(raw_body, public_key):
    """对原始通知报文执行 RSA2(SHA256WithRSA) 验签。"""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    params = dict(urllib.parse.parse_qsl(raw_body, keep_blank_values=True))
    sign = params.get("sign", "")
    if not sign:
        return None, "通知中无 sign 字段"

    filtered = {k: v for k, v in params.items() if k not in ("sign", "sign_type") and v}
    sign_content = "&".join(f"{k}={v}" for k, v in sorted(filtered.items()))
    signature_bytes = base64.b64decode(sign)

    try:
        public_key.verify(
            signature_bytes,
            sign_content.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True, "RSA2/SHA256WithRSA 验证通过"
    except Exception:
        return False, "验签失败 — 请检查支付宝公钥是否正确"


# ═══════════════════════════════════════════════════════════
# 通知展示
# ═══════════════════════════════════════════════════════════

def _mask(s, keep=6):
    if not s or len(s) <= keep:
        return s
    return s[:keep] + "****"


def display_notification(item, public_key=None, show_raw=False):
    """格式化输出一条通知。"""
    ts = item.get("received_at") or item.get("notify_time") or ""
    status = item.get("trade_status", "")

    status_display = status
    if "SUCCESS" in status:
        status_display = green(f"● {status}")
    elif "CLOSED" in status:
        status_display = red(f"● {status}")
    elif "WAIT" in status:
        status_display = yellow(f"● {status}")
    else:
        status_display = dim(f"● {status}")

    amount = ""
    raw = item.get("raw_body", "")
    if raw:
        p = dict(urllib.parse.parse_qsl(raw, keep_blank_values=True))
        amount = p.get("total_amount", "")
    # SSE 推送也可能包含 total_amount
    if not amount:
        amount = item.get("total_amount", "")

    nid = item.get("id", "?")

    print()
    print(f"  {cyan('━' * 50)}")
    print(f"  {bold(f'#{nid}')}  {dim(ts)}")
    print(f"  {cyan('━' * 50)}")
    print(f"  {'订单号':　<8} {item.get('out_trade_no', '')}")
    print(f"  {'交易号':　<8} {item.get('trade_no', '')}")
    print(f"  {'状态':　<8} {status_display}")
    if amount:
        print(f"  {'金额':　<8} ¥{amount}")
    print(f"  {'APPID':　<8} {item.get('app_id', '')}")
    print(f"  {'通知ID':　<8} {_mask(item.get('notify_id', ''))}")
    print(f"  {'通知时间':　<8} {item.get('notify_time', '')}")

    # ack 状态
    acked = item.get("acked")
    if acked is not None:
        if acked:
            print(f"  {'确认':　<8} {green('✓ 已确认 (支付宝将停止重试)')}")
        else:
            print(f"  {'确认':　<8} {dim('待确认')}")

    # 验签
    if public_key and raw:
        ok, msg = verify_rsa2(raw, public_key)
        if ok is True:
            print(f"  {'验签':　<8} {green('✓ ' + msg)}")
        elif ok is False:
            print(f"  {'验签':　<8} {red('✗ ' + msg)}")
        else:
            print(f"  {'验签':　<8} {yellow('⚠ ' + msg)}")
    elif not public_key:
        print(f"  {'验签':　<8} {dim('未配置支付宝公钥，跳过')}")

    if show_raw and raw:
        print(f"\n  {dim('原始报文 (' + str(len(raw)) + ' bytes):')}")
        # 解码后逐参数展示
        decoded_params = dict(urllib.parse.parse_qsl(raw, keep_blank_values=True))
        for k, v in decoded_params.items():
            if k == "sign":
                v = v[:20] + "..." if len(v) > 20 else v
            print(f"    {dim(k + '=')} {v}")

    print(f"  {cyan('━' * 50)}")


# ═══════════════════════════════════════════════════════════
# 命令：register
# ═══════════════════════════════════════════════════════════

def cmd_register(args):
    cfg = load_config()

    print()
    print(f"  {bold('支付宝异步通知中继 · 注册')}")
    print(f"  {dim('─' * 40)}")
    print()

    # 交互式输入
    server_url = args.server or cfg.get("server_url") or ""
    if not server_url:
        server_url = input(f"  {cyan('服务地址')} (如 https://notify.example.com): ").strip()
    if not server_url:
        print(red("  ✗ 服务地址不能为空"))
        sys.exit(1)
    server_url = server_url.rstrip("/")

    name = args.name or ""
    if not name:
        name = input(f"  {cyan('你的名称')} (用于标识，如 dev-xiaoming): ").strip()
    if not name:
        print(red("  ✗ 名称不能为空"))
        sys.exit(1)

    # 先检查服务是否可达
    print(f"\n  {dim('正在连接...')}")
    health = http_request("GET", f"{server_url}/health")
    if health["status"] != 200:
        print(red(f"  ✗ 服务不可达 (HTTP {health['status']})"))
        sys.exit(1)

    # 注册
    resp = http_request("POST", f"{server_url}/api/register", body={"name": name})
    if resp["status"] not in (200, 201):
        err = api_json(resp) or {}
        print(red(f"  ✗ 注册失败: {err.get('message', resp['body'])}"))
        sys.exit(1)

    data = json.loads(resp["body"])
    notify_url = data["notify_url"]
    api_key = data["api_key"]
    is_existing = resp["status"] == 200

    # 服务端未配置 PUBLIC_URL 时会返回 localhost，用 server_url 自动修正
    if "://localhost" in notify_url or "://127.0.0.1" in notify_url:
        from urllib.parse import urlparse
        parsed = urlparse(notify_url)
        notify_url = server_url + parsed.path

    # 保存配置
    new_cfg = {
        "server_url": server_url,
        "api_key": api_key,
        "notify_token": data["notify_token"],
        "notify_url": notify_url,
    }
    if cfg.get("alipay_public_key"):
        new_cfg["alipay_public_key"] = cfg["alipay_public_key"]

    saved_path = save_config(new_cfg)

    # 输出结果（精简，详细引导由 SKILL.md 提供）
    if is_existing:
        msg = data.get("message", "已注册，返回已有凭证")
        print(f"\n  {yellow('⚠ ' + msg)}")
        print(f"  {dim('如需新凭证，请联系管理员重置。')}")
    else:
        print(f"\n  {green('✓ 注册成功！')}")
    print()
    print(f"  {bold('notify_url')}")
    print(f"  ┌{'─' * (len(notify_url) + 2)}┐")
    print(f"  │ {bold(notify_url)} │")
    print(f"  └{'─' * (len(notify_url) + 2)}┘")
    print()
    print(f"  {dim('api_key:  ')} {api_key[:16]}...{dim('(已保存)')}")
    print(f"  {dim('配置文件: ')} {saved_path}")
    print()
    print(f"  {bold('下一步:')}") 
    print(f"    1. 在调用支付下单接口时传入上面的 notify_url")
    print(f"    2. 运行 {cyan('python3 scripts/cli.py listen --auto-ack')} 实时监听")
    print()


# ═══════════════════════════════════════════════════════════
# 命令：listen（SSE 实时流）
# ═══════════════════════════════════════════════════════════

def cmd_listen(args):
    cfg = load_config()
    require_config(cfg, "server_url", "api_key")

    public_key = None
    pk_b64 = cfg.get("alipay_public_key", "")
    if pk_b64:
        public_key = _load_public_key(pk_b64)
        if not public_key:
            print(yellow("  ⚠ 支付宝公钥加载失败，将跳过验签"))
            print(dim("    请检查 alipay_public_key 格式是否正确\n"))

    server = cfg["server_url"]

    print()
    print(f"  {bold('支付宝异步通知中继 · 实时监听')}")
    print(f"  {dim('─' * 40)}")
    print(f"  {'服务':<8} {server}")
    print(f"  {'验签':<8} {green('✓ 已启用') if public_key else dim('未配置公钥')}")
    if args.auto_ack:
        print(f"  {'自动确认':<8} {green('✓ 已启用')} {dim('(收到即 ack，支付宝将停止重试)')}")
    if args.out_trade_no:
        print(f"  {'过滤':<8} out_trade_no = {args.out_trade_no}")
    print(f"  {dim('─' * 40)}")
    print()

    seen_notify_ids = set()
    total_received = 0
    reconnect_count = 0

    while True:
        try:
            url = f"{server}/api/stream"
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {cfg['api_key']}",
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache",
            })

            resp = urllib.request.urlopen(req, timeout=300)
            if reconnect_count == 0:
                print(f"  {green('● 已连接')}  {dim('等待通知...')}")
            else:
                print(f"\n  {green('● 已重连')}  {dim(f'(第 {reconnect_count} 次)')}")

            buffer = ""
            while True:
                line = resp.readline()
                if not line:
                    break
                buffer += line.decode("utf-8", errors="replace")

                while "\n\n" in buffer:
                    event_text, buffer = buffer.split("\n\n", 1)
                    data_lines = []
                    for line in event_text.strip().split("\n"):
                        if line.startswith("data: "):
                            data_lines.append(line[6:])
                        elif line.startswith(":"):
                            continue  # 心跳 / 注释

                    if not data_lines:
                        continue

                    try:
                        item = json.loads("".join(data_lines))
                    except json.JSONDecodeError:
                        continue

                    # 过滤
                    if args.out_trade_no and item.get("out_trade_no") != args.out_trade_no:
                        continue

                    # 去重（同一 notify_id 的支付宝重试）
                    nid = item.get("notify_id", "")
                    if nid and nid in seen_notify_ids:
                        ts = time.strftime("%H:%M:%S")
                        print(f"  {dim(f'[{ts}] ↩ 支付宝重试 notify_id={_mask(nid)} — 已接收，跳过')}")
                        continue
                    if nid:
                        seen_notify_ids.add(nid)

                    total_received += 1
                    display_notification(item, public_key)

                    # 自动确认：通知开发者已收到，通知云端让支付宝停止重试
                    if args.auto_ack and item.get("id"):
                        try:
                            ack_resp = api_post(cfg, f"/api/notifications/{item['id']}/ack")
                            if ack_resp.get("status") == 200:
                                print(f"  {dim('  ↳ 已自动确认 (ack)，支付宝将停止重试')}")  
                        except Exception:
                            pass  # ack 失败不影响主流程

        except KeyboardInterrupt:
            print(f"\n\n  {dim(f'已停止监听。共收到 {total_received} 条通知。')}\n")
            break
        except urllib.error.HTTPError as e:
            reconnect_count += 1
            if e.code == 403:
                print(f"\n  {red('✗ 凭证无效 (403 Forbidden)')}")  
                print(f"  {dim('请重新注册:')} {bold('python3 scripts/cli.py register')}")
                break
            print(f"\n  {yellow(f'连接断开: HTTP {e.code}')}")
            print(f"  {dim('3 秒后自动重连...')}")
            time.sleep(3)
        except Exception as e:
            reconnect_count += 1
            print(f"\n  {yellow(f'连接断开: {e}')}")
            print(f"  {dim('3 秒后自动重连...')}")
            time.sleep(3)


# ═══════════════════════════════════════════════════════════
# 命令：list
# ═══════════════════════════════════════════════════════════

def cmd_list(args):
    cfg = load_config()
    require_config(cfg, "server_url", "api_key")

    params = {"limit": str(args.limit)}
    if args.out_trade_no:
        params["out_trade_no"] = args.out_trade_no
    if args.trade_status:
        params["trade_status"] = args.trade_status

    resp = api_get(cfg, "/api/notifications", params)
    if resp["status"] != 200:
        print(red(f"  ✗ 查询失败 (HTTP {resp['status']})"))
        sys.exit(1)

    data = api_json(resp)
    items = data.get("items", [])
    total = data.get("total", 0)

    print()
    print(f"  {bold(f'共 {total} 条通知')}{dim(f'（显示最近 {len(items)} 条）')}")

    public_key = None
    pk_b64 = cfg.get("alipay_public_key", "")
    if pk_b64:
        public_key = _load_public_key(pk_b64)

    for item in items:
        display_notification(item, public_key)

    if not items:
        print(f"\n  {dim('暂无通知。请确认：')}")
        print(f"  {dim('  1. notify_url 已正确配置')}")
        print(f"  {dim('  2. 已完成支付')}")
    print()


# ═══════════════════════════════════════════════════════════
# 命令：get / verify
# ═══════════════════════════════════════════════════════════

def cmd_get(args):
    cfg = load_config()
    require_config(cfg, "server_url", "api_key")

    resp = api_get(cfg, f"/api/notifications/{args.id}")
    if resp["status"] == 404:
        print(red(f"  ✗ 通知 #{args.id} 不存在（或不属于你）"))
        sys.exit(1)
    if resp["status"] != 200:
        print(red(f"  ✗ 查询失败 (HTTP {resp['status']})"))
        sys.exit(1)

    item = api_json(resp)
    public_key = None
    pk_b64 = cfg.get("alipay_public_key", "")
    if pk_b64:
        public_key = _load_public_key(pk_b64)

    display_notification(item, public_key, show_raw=True)
    print()


def cmd_verify(args):
    cfg = load_config()
    require_config(cfg, "server_url", "api_key")

    pk_b64 = cfg.get("alipay_public_key", "")
    if not pk_b64:
        print(red("  ✗ 未配置支付宝公钥，无法验签"))
        print(dim(f"    编辑 {CONFIG_FILENAME} 添加 alipay_public_key"))
        sys.exit(1)

    public_key = _load_public_key(pk_b64)
    if not public_key:
        print(red("  ✗ 公钥加载失败"))
        sys.exit(1)

    resp = api_get(cfg, f"/api/notifications/{args.id}")
    if resp["status"] != 200:
        print(red(f"  ✗ 通知 #{args.id} 不存在"))
        sys.exit(1)

    item = api_json(resp)
    raw = item.get("raw_body", "")
    if not raw:
        print(red("  ✗ 通知无 raw_body"))
        sys.exit(1)

    ok, msg = verify_rsa2(raw, public_key)
    display_notification(item, public_key, show_raw=True)
    print()


# ═══════════════════════════════════════════════════════════
# 命令：export
# ═══════════════════════════════════════════════════════════

def cmd_ack(args):
    cfg = load_config()
    require_config(cfg, "server_url", "api_key")

    resp = api_post(cfg, f"/api/notifications/{args.id}/ack")
    data = api_json(resp)

    if resp["status"] == 200 and data:
        print(f"\n  {green('✓ 已确认')} notify_id={data.get('notify_id', '?')}")
        print(f"  {dim('支付宝下次重试时将收到 success，停止后续重试')}\n")
    elif resp["status"] == 404:
        print(f"\n  {red('✗ 未找到通知')} id={args.id}\n")
    elif resp["status"] == 400:
        print(f"\n  {yellow('⚠ 无法确认：')} {data.get('message', '该通知没有 notify_id')}\n")
    else:
        print(f"\n  {red('✗ 确认失败：')} HTTP {resp['status']}\n")


def cmd_export(args):
    cfg = load_config()
    require_config(cfg, "server_url", "api_key")

    resp = api_get(cfg, f"/api/notifications/{args.id}")
    if resp["status"] != 200:
        print(red(f"  ✗ 通知 #{args.id} 不存在"))
        sys.exit(1)

    item = api_json(resp)
    raw = item.get("raw_body", "")

    out_file = args.output or f"notify_{args.id}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(raw)

    print(f"  {green('✓')} 原始报文已导出到 {bold(out_file)} ({len(raw)} bytes)")
    print(f"  {dim('可用于手动验签测试或与其他工具对接')}")
    print()


# ═══════════════════════════════════════════════════════════
# 命令：status
# ═══════════════════════════════════════════════════════════

def cmd_status(args):
    cfg = load_config()
    require_config(cfg, "server_url")

    print()
    resp = http_request("GET", f"{cfg['server_url']}/health")
    if resp["status"] == 200:
        data = json.loads(resp["body"])
        print(f"  {green('● 服务正常')}")
        print(f"  {'地址':<8} {cfg['server_url']}")
        print(f"  {'时间':<8} {data.get('time', '')}")
        print(f"  {'SSE连接':<8} {data.get('sse_clients', 0)}")
    else:
        print(f"  {red('✗ 服务异常')} (HTTP {resp['status']})")

    if cfg.get("notify_url"):
        print(f"\n  {'notify_url':<12} {cfg['notify_url']}")
    if cfg.get("api_key"):
        print(f"  {'api_key':<12} {cfg['api_key'][:16]}...")
    if cfg.get("alipay_public_key"):
        print(f"  {'验签公钥':<12} {green('已配置')}")
    else:
        print(f"  {'验签公钥':<12} {dim('未配置')}")
    print()


# ═══════════════════════════════════════════════════════════
# 命令：config
# ═══════════════════════════════════════════════════════════

def cmd_config(args):
    cfg = load_config()
    path = cfg.get("_config_path", dim("(未找到配置文件)"))

    print()
    print(f"  {bold('当前配置')}")
    print(f"  {dim('─' * 40)}")
    print(f"  {'配置文件':<12} {path}")
    for key in ["server_url", "notify_url", "api_key", "notify_token", "alipay_public_key"]:
        val = cfg.get(key, "")
        if key == "api_key" and val:
            val = val[:16] + "..."
        elif key == "alipay_public_key" and val:
            val = val[:20] + "..." + f" ({len(val)} chars)"
        elif key == "notify_token" and val:
            val = val[:12] + "..."
        print(f"  {key:<12} {val or dim('(未设置)')}")
    print()

    if not cfg.get("server_url"):
        print(f"  {yellow('💡')} 运行 {cyan('python3 cli.py register')} 快速开始")
        print()


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="支付宝异步通知中继 — 开发者 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令示例:
  %(prog)s register                  自助注册
  %(prog)s listen                    实时监听
  %(prog)s listen --out-trade-no X   监听指定订单
  %(prog)s list                      查询最近通知
  %(prog)s list --limit 50           查询50条
  %(prog)s get 42                    查看 #42 详情
  %(prog)s verify 42                 验签 #42
  %(prog)s export 42                 导出 #42 原始报文
  %(prog)s status                    检查服务状态
  %(prog)s config                    查看当前配置

⚠️  仅限联调 / 内部调试，不可用于生产。
""",
    )

    sub = parser.add_subparsers(dest="command", title="命令")

    # register
    p_reg = sub.add_parser("register", help="自助注册，获取凭证")
    p_reg.add_argument("--server", help="服务地址 (如 https://notify.example.com)")
    p_reg.add_argument("--name", help="开发者名称")

    # listen
    p_listen = sub.add_parser("listen", help="实时监听通知 (SSE)")
    p_listen.add_argument("--out-trade-no", help="按订单号过滤")
    p_listen.add_argument("--auto-ack", action="store_true",
                          help="收到通知后自动确认 (ack)，让支付宝停止重试")

    # list
    p_list = sub.add_parser("list", help="查询最近通知")
    p_list.add_argument("--limit", type=int, default=10, help="条数 (默认10)")
    p_list.add_argument("--out-trade-no", help="按订单号过滤")
    p_list.add_argument("--trade-status", help="按交易状态过滤")

    # get
    p_get = sub.add_parser("get", help="查看单条通知详情")
    p_get.add_argument("id", type=int, help="通知 ID")

    # verify
    p_verify = sub.add_parser("verify", help="验签指定通知")
    p_verify.add_argument("id", type=int, help="通知 ID")

    # ack
    p_ack = sub.add_parser("ack", help="确认通知已处理，让支付宝停止重试")
    p_ack.add_argument("id", type=int, help="通知 ID")

    # export
    p_export = sub.add_parser("export", help="导出原始报文到文件")
    p_export.add_argument("id", type=int, help="通知 ID")
    p_export.add_argument("-o", "--output", help="输出文件名")

    # status
    sub.add_parser("status", help="检查服务状态")

    # config
    sub.add_parser("config", help="查看当前配置")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print()
        return

    cmds = {
        "register": cmd_register,
        "listen": cmd_listen,
        "list": cmd_list,
        "get": cmd_get,
        "verify": cmd_verify,
        "ack": cmd_ack,
        "export": cmd_export,
        "status": cmd_status,
        "config": cmd_config,
    }

    cmds[args.command](args)


if __name__ == "__main__":
    main()
