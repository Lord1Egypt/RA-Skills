#!/usr/bin/env python3
"""cli.py — BizyAir Skill 统一 CLI 入口。

子命令映射到 dispatch.py / app.py 的对应功能。
旧入口（dispatch.py / app.py）仍然可用，本文件是新增的统一入口。

用法：
  python3 scripts/cli.py check
  python3 scripts/cli.py wallet
  python3 scripts/cli.py image-menu
  python3 scripts/cli.py video-menu
  python3 scripts/cli.py browse --remote-source community --modality Application --sort "Most Used"
  python3 scripts/cli.py search "<关键词>" --remote
  python3 scripts/cli.py info <link_or_id>
  python3 scripts/cli.py prefill <link_or_id> --prompt "xxx"
  python3 scripts/cli.py run <app_id> --prompt "xxx"
  python3 scripts/cli.py pick-image "关键词" --remote
  python3 scripts/cli.py pick-video "关键词" --remote
  python3 scripts/cli.py batch-prefill --model <route> --batch-json '[...]'
  python3 scripts/cli.py batch-run --model <route> --batch-json '[...]' --confirm-run
  python3 scripts/cli.py modelzoo-list --keyword "flux"
  python3 scripts/cli.py modelzoo-detail <endpoint>
  python3 scripts/cli.py modelzoo-price <endpoint>
  python3 scripts/cli.py modelzoo-run <endpoint> --param key=value
  python3 scripts/cli.py modelzoo-status <request_id>
  python3 scripts/cli.py pick-modelzoo-image "<关键词>"
  python3 scripts/cli.py pick-modelzoo-video "<关键词>"
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    # ---- dispatch.py 命令 ----
    if cmd == "check":
        sys.argv = [str(SCRIPT_DIR / "dispatch.py"), "--check"] + rest
        import dispatch
        dispatch.main()
    elif cmd == "wallet":
        sys.argv = [str(SCRIPT_DIR / "dispatch.py"), "--wallet"] + rest
        import dispatch
        dispatch.main()
    elif cmd == "image-menu":
        sys.argv = [str(SCRIPT_DIR / "dispatch.py"), "--image-menu"] + rest
        import dispatch
        dispatch.main()
    elif cmd == "video-menu":
        sys.argv = [str(SCRIPT_DIR / "dispatch.py"), "--video-menu"] + rest
        import dispatch
        dispatch.main()
    elif cmd == "batch-prefill":
        sys.argv = [str(SCRIPT_DIR / "dispatch.py"), "--batch-prefill"] + rest
        import dispatch
        dispatch.main()
    elif cmd == "batch-run":
        sys.argv = [str(SCRIPT_DIR / "dispatch.py"), "--batch-run"] + rest
        import dispatch
        dispatch.main()

    # ---- app.py 命令 ----
    elif cmd == "info":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--info-from-link"] + rest
        import app
        app.main()
    elif cmd == "browse":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--browse", "--remote"] + rest
        import app
        app.main()
    elif cmd == "search":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--search"] + rest
        import app
        app.main()
    elif cmd == "prefill":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--prefill-card"] + rest
        import app
        app.main()
    elif cmd == "run":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--run"] + rest
        import app
        app.main()
    elif cmd == "pick-image":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--pick-image-candidates"] + rest
        import app
        app.main()
    elif cmd == "pick-video":
        sys.argv = [str(SCRIPT_DIR / "app.py"), "--pick-video-candidates"] + rest
        import app
        app.main()

    # ---- modelzoo 命令（新增）----
    elif cmd == "modelzoo-list":
        _modelzoo_list(rest)
    elif cmd == "modelzoo-detail":
        _modelzoo_detail(rest)
    elif cmd == "modelzoo-price":
        _modelzoo_price(rest)
    elif cmd == "modelzoo-run":
        _modelzoo_run(rest)
    elif cmd == "modelzoo-status":
        _modelzoo_status(rest)
    elif cmd == "pick-modelzoo-image":
        _modelzoo_pick(rest, modality="image")
    elif cmd == "pick-modelzoo-video":
        _modelzoo_pick(rest, modality="video")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


# ---- ModelZoo 子命令实现 ----

def _get_key(rest: list[str]) -> str:
    import api
    key_arg = None
    if "--api-key" in rest:
        idx = rest.index("--api-key")
        if idx + 1 < len(rest):
            key_arg = rest[idx + 1]
    return api.require_api_key(key_arg)


def _modelzoo_list(rest: list[str]):
    import modelzoo
    import api as _api

    key = _get_key(rest)
    keyword = ""
    if rest and not rest[0].startswith("--"):
        keyword = rest[0]
    elif "--keyword" in rest:
        idx = rest.index("--keyword")
        if idx + 1 < len(rest):
            keyword = rest[idx + 1]

    result = modelzoo.list_endpoints(key, keyword=keyword)
    data = (result.get("data") or {}).get("data") or result.get("data") or {}
    items = data.get("list") or []
    print(f"共 {data.get('total', len(items))} 个 endpoint：")
    for item in items:
        print(f"  {item.get('endpoint'):50} | {item.get('display_name')} | {item.get('category')}")


def _modelzoo_detail(rest: list[str]):
    import modelzoo

    key = _get_key(rest)
    endpoint = rest[0] if rest and not rest[0].startswith("--") else ""
    if not endpoint:
        print("用法: cli.py modelzoo-detail <endpoint>")
        sys.exit(1)

    result = modelzoo.get_detail(key, endpoint)
    data = (result.get("data") or {}).get("data") or result.get("data") or {}
    print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])


def _modelzoo_price(rest: list[str]):
    import modelzoo

    key = _get_key(rest)
    endpoint = rest[0] if rest and not rest[0].startswith("--") else ""
    if not endpoint:
        print("用法: cli.py modelzoo-price <endpoint>")
        sys.exit(1)

    result = modelzoo.get_price(key, endpoint)
    data = (result.get("data") or {}).get("data") or result.get("data") or {}
    simple = (data.get("price_table") or {}).get("simple_price_text")
    if simple:
        print(f"价格：{simple}")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])


def _modelzoo_run(rest: list[str]):
    import modelzoo
    import api as _api

    key = _get_key(rest)
    endpoint = rest[0] if rest and not rest[0].startswith("--") else ""
    if not endpoint:
        print("用法: cli.py modelzoo-run <endpoint> --param key=value [--image path ...] [--audio path ...] [--video path ...]")
        sys.exit(1)

    # 解析 --param / --image / --audio / --video
    params: dict[str, str] = {}
    images: list[str] = []
    audios: list[str] = []
    videos: list[str] = []
    i = 1
    while i < len(rest):
        if rest[i] == "--param" and i + 1 < len(rest):
            kv = rest[i + 1]
            if "=" in kv:
                k, v = kv.split("=", 1)
                params[k] = v
            i += 2
        elif rest[i] == "--image" and i + 1 < len(rest):
            images.append(rest[i + 1])
            i += 2
        elif rest[i] == "--audio" and i + 1 < len(rest):
            audios.append(rest[i + 1])
            i += 2
        elif rest[i] == "--video" and i + 1 < len(rest):
            videos.append(rest[i + 1])
            i += 2
        else:
            i += 1

    # 上传媒体文件 → 构建 media_overrides（整体替换默认示例素材）
    media_overrides: dict[str, list[str]] = {}
    if images:
        media_overrides["images"] = [_api.upload_input_file(key, p) for p in images]
    if audios:
        media_overrides["audios"] = [_api.upload_input_file(key, p) for p in audios]
    if videos:
        media_overrides["videos"] = [_api.upload_input_file(key, p) for p in videos]

    # 拿 detail 构建 payload
    detail_result = modelzoo.get_detail(key, endpoint)
    detail_data = (detail_result.get("data") or {}).get("data") or detail_result.get("data") or {}
    payload = modelzoo.build_task_payload(detail_data, params, media_overrides=media_overrides)

    print(f"提交任务: {endpoint}")
    print(f"参数: {json.dumps(payload, ensure_ascii=False)[:500]}")

    create_result = modelzoo.create_task(key, endpoint, payload)
    create_data = (create_result.get("data") or {}).get("data") or create_result.get("data") or {}
    request_id = create_data.get("request_id")

    if not request_id:
        print(f"创建失败: {json.dumps(create_result, ensure_ascii=False)[:500]}")
        sys.exit(1)

    print(f"request_id: {request_id}")
    print("轮询中...")

    final = modelzoo.poll_until_done(key, request_id)
    status = final.get("status")
    outputs = final.get("outputs") or {}

    if status == "Success":
        print(f"\n✅ 成功！")
        for media_type in ("texts", "images", "videos", "audios"):
            items = outputs.get(media_type) or []
            for url in items:
                print(f"  [{media_type}] {url}")
    else:
        print(f"\n❌ {status}: {final.get('message', '')}")


def _modelzoo_status(rest: list[str]):
    import modelzoo

    key = _get_key(rest)
    request_id = rest[0] if rest and not rest[0].startswith("--") else ""
    if not request_id:
        print("用法: cli.py modelzoo-status <request_id>")
        sys.exit(1)

    result = modelzoo.query_task(key, request_id)
    data = (result.get("data") or {}).get("data") or result.get("data") or {}
    print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])


def _modelzoo_pick(rest: list[str], *, modality: str):
    """ModelZoo endpoint 候选搜索（菜单 6 号 / v6）。

    支持 --reply-format json|markdown，默认 json（与 pick-image / pick-video 一致）。
    --limit 控制候选数量上限。
    """
    import modelzoo

    key = _get_key(rest)
    query = ""
    if rest and not rest[0].startswith("--"):
        query = rest[0]

    # 简单 flag 解析（与现有 _modelzoo_run 风格一致，不引入 argparse）
    reply_format = "json"
    limit = 10
    i = 0
    while i < len(rest):
        if rest[i] == "--reply-format" and i + 1 < len(rest):
            reply_format = rest[i + 1]
            i += 2
        elif rest[i] == "--limit" and i + 1 < len(rest):
            try:
                # 上限 30：picker 不再做模态过滤，全部召回，所以避免输出爆炸
                limit = max(1, min(30, int(rest[i + 1])))
            except ValueError:
                pass
            i += 2
        else:
            i += 1

    if not query:
        print("用法: cli.py pick-modelzoo-image|pick-modelzoo-video \"<关键词>\" [--limit N] [--reply-format json|markdown]")
        sys.exit(1)

    payload = modelzoo.pick_endpoint_candidates(key, query, modality, limit=limit)

    if reply_format == "markdown":
        print(payload.get("reply_markdown") or "")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
