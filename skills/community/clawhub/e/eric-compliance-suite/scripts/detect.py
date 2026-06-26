#!/usr/bin/env python3
"""睿观 ERiC 合规检测套件 - 统一入口
子命令: d001, i001, l001, t001, t002, c001, p001, p002, p004, p005, p006, p007
"""

import sys, os, json, base64

# Windows 中文环境默认使用 GBK 编码，无法输出 emoji 字符，强制切换到 UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower().replace("-", "") != "utf8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = "https://saas.eric-bot.com/v1.0/eric-api"

# 扣点配置表
POINT_COSTS = {
    "d001": {"base": 10, "radar": 15, "has_radar": True},
    "i001": {"base": 10, "radar": 10, "has_radar": False},
    "l001": {"base": 10, "radar": 15, "has_radar": True},
    "t001": {"base": 1, "radar": 1, "has_radar": False},
    "t002": {"base": 1, "radar": 1, "has_radar": False},
    "c001": {"base": 1, "radar": 2, "has_radar": True},  # 雷达+1
    "p001": {"base": 1, "radar": 1, "has_radar": False},
    "p002": {"base": 5, "radar": 5, "has_radar": False},  # 图文同时检测仍为5点
}

# 默认站点配置
DEFAULT_REGIONS = {
    "d001": ["US"],
    "i001": ["US"],
    "l001": None,  # None 表示全部
    "t001": ["US"],
    "p002": ["us"],
}

def _calc_points(cmd, enable_radar=False, enable_scan=False):
    """根据命令和选项计算扣点数"""
    cost_info = POINT_COSTS.get(cmd, {})
    if enable_radar and enable_scan and "radar_scan" in cost_info:
        return cost_info["radar_scan"]
    if enable_scan and "scan" in cost_info:
        return cost_info["scan"]
    if enable_radar:
        return cost_info.get("radar", cost_info.get("base", 0))
    return cost_info.get("base", 0)

def show_pre_deduct(cmd, enable_radar=False, extra_info="", enable_scan=False):
    """检测开始前展示预扣点信息"""
    cost_info = POINT_COSTS.get(cmd, {})
    points = _calc_points(cmd, enable_radar, enable_scan)
    notes = []
    if enable_radar and cost_info.get("has_radar"):
        notes.append("含雷达分析")
    if enable_scan:
        notes.append("含全网扫描")
    note_str = f"（{'，'.join(notes)}）" if notes else ""
    print(f"📊 本次预扣 {points} 点{note_str}")
    if extra_info:
        print(f"   {extra_info}")
    print()

def show_actual_deduct(cmd, enable_radar=False, retry_count=0, enable_scan=False):
    """检测完成后展示实际扣点信息"""
    cost_info = POINT_COSTS.get(cmd, {})
    points = _calc_points(cmd, enable_radar, enable_scan)
    total = points * (retry_count + 1) if retry_count > 0 else points
    if retry_count > 0:
        print(f"\n💰 本次检测实际扣点: {total} 点（含 {retry_count} 次超时重试，每次 {points} 点）")
    else:
        print(f"\n💰 本次检测实际扣点: {total} 点")

def show_default_regions(cmd, regions):
    """展示默认检测国家站点"""
    default = DEFAULT_REGIONS.get(cmd)
    if regions is None and default is not None:
        print(f"📍 检测站点: {', '.join(default)}（默认）")
    elif regions is None and default is None:
        print(f"📍 检测站点: 全部国家/地区")
    else:
        print(f"📍 检测站点: {', '.join(regions)}")

def check_token():
    token = os.environ.get("ERIC_API_TOKEN")
    if not token:
        print("错误: 未设置 ERIC_API_TOKEN 环境变量。")
        print("请先获取 Token：登录 https://eric-bot.com → API Token")
        print("然后设置环境变量：export ERIC_API_TOKEN=your_token")
        sys.exit(1)
    return token

def ensure_requests():
    try:
        import requests
        return requests
    except ImportError:
        import subprocess
        print("正在安装 requests...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "requests", "-q"],
            check=True,
            capture_output=True
        )
        import requests
        return requests

def api_call(token, path, payload, timeout=120):
    requests = ensure_requests()
    resp = requests.post(
        f"{BASE}/{path}",
        headers={"Content-Type": "application/json", "Token": token},
        json=payload,
        timeout=timeout,
    )
    return resp.json()

def load_image(source):
    """加载图片并返回 base64 字符串。支持三种输入：
    1. 本地文件路径: /path/to/image.png
    2. URL: https://example.com/image.jpg
    3. base64 字符串: 直接返回
    """
    # URL
    if source.startswith(("http://", "https://")):
        requests = ensure_requests()
        try:
            resp = requests.get(source, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            return base64.b64encode(resp.content).decode()
        except Exception as e:
            print(f"错误: 下载图片失败: {e}")
            sys.exit(1)
    # 本地文件
    if os.path.isfile(source):
        with open(source, "rb") as f:
            return base64.b64encode(f.read()).decode()
    # 尝试当作 base64 字符串
    try:
        base64.b64decode(source[:64], validate=True)
        return source
    except Exception:
        pass
    print(f"错误: 无法识别图片来源: {source}")
    print("支持: 本地文件路径 / URL / base64 字符串")
    sys.exit(1)

# ── D001 外观专利检测 ──────────────────────────────────────────

def cmd_d001(args, token):
    # 默认开启雷达，使用 --no-radar 关闭
    enable_radar = not getattr(args, 'no_radar', False)

    # 展示预扣点和检测站点
    show_default_regions("d001", args.regions)
    show_pre_deduct("d001", enable_radar)

    img_b64 = load_image(args.image)
    payload = {
        "product_title": args.title,
        "product_description": args.description,
        "regions": args.regions,
        "img_64lis": [img_b64],
        "top_loc": args.loc,
        "patent_status": args.patent_status,
        "top_number": args.top,
        "enable_tro": not args.no_tro,
        "source_language": args.lang,
        "query_mode": args.mode,
        "enable_radar": enable_radar,
    }
    result = api_call(token, "patent/design/v1/detection", payload)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("d001", enable_radar)
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    patents = result.get("data", {}).get("list", [])
    print(f"共找到 {len(patents)} 条相似外观专利\n")
    for i, p in enumerate(patents[:20], 1):
        sim = float(p.get("similarity", 0))
        risk = "🔴高风险" if sim > 0.8 else ("🟡中风险" if sim > 0.5 else "🟢低风险")
        tro = " [TRO]" if p.get("tro_holder") or p.get("tro_case") else ""
        radar = ""
        if args.enable_radar and p.get("radar_result", {}).get("same"):
            radar = " [雷达:疑似侵权]"
            risk = "🔴高风险"
        print(f"{i}. {risk}{tro}{radar}")
        print(f"   相似度: {sim:.4f} | 公开号: {p.get('publication_number', '')}")
        print(f"   专利标题: {p.get('patent_prod', '')} / {p.get('patent_prod_cn', '')}")
        print(f"   有效性: {p.get('patent_validity', '')} | 受理局: {p.get('registration_office_code', '')}")
        print()
    if len(patents) > 20:
        print(f"... 还有 {len(patents) - 20} 条结果未显示，使用 --json 查看完整结果")

    show_actual_deduct("d001", enable_radar)

# ── I001 发明专利检测 ──────────────────────────────────────────

def cmd_i001(args, token):
    # 展示预扣点和检测站点
    show_default_regions("i001", args.regions)
    show_pre_deduct("i001")

    result = api_call(token, "patent/utility/v1/detection", {
        "product_title": args.title,
        "product_description": args.description,
        "regions": args.regions,
        "top_number": args.top,
    })

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("i001")
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    patents = result.get("data", {}).get("data", [])
    print(f"共找到 {len(patents)} 条相似发明专利\n")
    for i, p in enumerate(patents[:20], 1):
        sim = float(p.get("similarity", 0))
        risk = "🔴高风险" if sim > 0.8 else ("🟡中风险" if sim > 0.5 else "🟢低风险")
        tro = " [TRO]" if p.get("tro_holder") or p.get("tro_case") else ""
        print(f"{i}. {risk}{tro}")
        print(f"   相似度: {sim:.4f} | 公开号: {p.get('publication_number', '')}")
        print(f"   标题: {p.get('title', '')} / {p.get('title_cn', '')}")
        print(f"   有效性: {p.get('patent_validity', '')}")
        print()
    if len(patents) > 20:
        print(f"... 还有 {len(patents) - 20} 条结果未显示，使用 --json 查看完整结果")

    show_actual_deduct("i001")

# ── L001 图形商标检测 ──────────────────────────────────────────

def cmd_l001(args, token):
    # 默认开启雷达，使用 --no-radar 关闭
    enable_radar = not getattr(args, 'no_radar', False)

    # 展示预扣点和检测站点
    show_default_regions("l001", args.regions)
    show_pre_deduct("l001", enable_radar)

    img_b64 = load_image(args.image)
    payload = {
        "product_title": args.title,
        "base64_image": img_b64,
        "trademark_name": args.trademark_name,
        "top_number": args.top,
        "enable_localizing": args.enable_localizing,
        "enable_radar": enable_radar,
    }
    if args.regions:
        payload["regions"] = args.regions

    result = api_call(token, "trademark/graphic/v1/detection", payload)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("l001", enable_radar)
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    data = result.get("data", {})
    print(f"检测到 {data.get('bounding_box_count', 0)} 个logo区域")
    if data.get("radar_result"):
        print(f"整体雷达风险: {data['radar_result']}\n")

    for dr in data.get("detection_results", []):
        idx = dr.get("index", 0)
        total = dr.get("total_detection_result_count", 0)
        print(f"--- 区域 {idx} (召回: {total}条) ---")
        for rg in dr.get("top_graphic_trademarks", []):
            region = rg.get("region", "")
            tms = rg.get("graphic_trademarks", [])
            print(f"\n  国家/地区: {region} ({len(tms)} 条)")
            for j, tm in enumerate(tms[:10], 1):
                sim = float(tm.get("similarity", 0))
                risk = "🔴高" if sim > 0.8 else ("🟡中" if sim > 0.5 else "🟢低")
                sub_r = f" [{tm.get('sub_radar_result')}]" if tm.get("sub_radar_result") else ""
                print(f"  {j}. {risk}{sub_r} 相似度:{sim:.4f} | {tm.get('trademark_name','')} | 权利人:{tm.get('applicant_name','')} | 状态:{tm.get('trade_mark_status','')}")
            if len(tms) > 10:
                print(f"  ... 还有 {len(tms) - 10} 条")
        print()

    show_actual_deduct("l001", enable_radar)

# ── T001 文本商标检测 ──────────────────────────────────────────

def cmd_t001(args, token):
    # 展示预扣点和检测站点
    show_default_regions("t001", args.regions)
    # 首次检测只调 T001，不自动调 T002
    auto_safe = args.auto_safe_words if hasattr(args, 'auto_safe_words') else False
    extra_info = "（使用 --auto-safe-words 可自动获取高风险词替换建议，每词额外扣 1 点）" if not auto_safe else ""
    show_pre_deduct("t001", extra_info=extra_info)

    result = api_call(token, "trademark/text/v1/detection", {
        "product_title": args.title,
        "product_text": args.text,
        "regions": args.regions,
    }, timeout=90)  # 超时配置为90秒

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("t001")
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    data = result.get("data", {})
    radar = data.get("text_trademark_radar", 0)
    radar_labels = {0: "🟢低风险", 1: "🟡待人工核查", 2: "🔴高风险"}
    print(f"整体风险等级: {radar_labels.get(radar, radar)}\n")

    trademarks = data.get("text_trademarks", [])
    if not trademarks:
        print("未检测到商标词风险")
        show_actual_deduct("t001")
        return

    trademarks.sort(key=lambda x: x.get("highest_mode_score", 0), reverse=True)
    for i, tm in enumerate(trademarks, 1):
        score = tm.get("highest_mode_score", 0)
        risk = "🔴" if score >= 3 else ("🟡" if score >= 1 else "🟢")
        flags = []
        if tm.get("is_famous"): flags.append("著名商标")
        if tm.get("is_active_holder"): flags.append("活跃维权人")
        if tm.get("is_amazon_brand"): flags.append("Amazon品牌")
        if tm.get("is_common_sense"): flags.append("常用词")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"{i}. {risk} {tm.get('trademark_name', '')} (分数:{score}/5, 状态:{tm.get('status', '')}){flag_str}")
        rs = tm.get("region_score", [])
        if rs:
            scores_str = ", ".join(f"{r.get('region','')}:{r.get('score',0)}" for r in rs)
            print(f"   各国风险: {scores_str}")

    # 统计实际扣点（T001 固定 1 点）
    t002_count = 0

    # 自动获取替换词（仅当用户显式指定 --auto-safe-words 时）
    if auto_safe:
        high_risk = [tm for tm in trademarks if tm.get("highest_mode_score", 0) >= 3]
        for tm in high_risk:
            _get_safe_words(token, args.title, args.text, tm.get("trademark_name", ""))
            t002_count += 1

    # 展示实际扣点
    total_points = 1 + t002_count  # T001 1点 + T002 每次1点
    if t002_count > 0:
        print(f"\n💰 本次检测实际扣点: {total_points} 点（T001: 1点 + T002替换词: {t002_count}点）")
    else:
        show_actual_deduct("t001")

# ── T002 商标替换词 ────────────────────────────────────────────

def _get_safe_words(token, title, text, trademark_name, output_json=False):
    result = api_call(token, "trademark/text/v1/safe-words-generation", {
        "product_title": title,
        "product_text": text,
        "trademark_name": trademark_name,
    }, timeout=60)
    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        return
    words = result.get("data", {}).get("words", [])
    if words:
        print(f"\n「{trademark_name}」的安全替换词: {', '.join(words)}")
    else:
        print(f"\n未找到「{trademark_name}」的合适替换词")

def cmd_t002(args, token):
    _get_safe_words(token, args.title, args.text, args.trademark, args.json)

# ── C001 版权检测 ──────────────────────────────────────────────

def cmd_c001(args, token):
    # 默认开启雷达，使用 --no-radar 关闭
    enable_radar = not getattr(args, 'no_radar', False)

    # 展示预扣点
    print("📍 版权库匹配检测")
    show_pre_deduct("c001", enable_radar)

    img_b64 = load_image(args.image)
    result = api_call(token, "copyright/v1/detection", {
        "img_64lis": [img_b64],
        "top_number": args.top,
        "enable_radar": enable_radar,
    })

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("c001", enable_radar)
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    items = result.get("data", {}).get("list", [])
    print(f"共找到 {len(items)} 条相似版权画作\n")
    for i, item in enumerate(items[:20], 1):
        sim = float(item.get("similarity") or item.get("cosine") or 0)
        if isinstance(sim, str): sim = float(sim)
        risk = "🔴高风险" if sim > 0.8 else ("🟡中风险" if sim > 0.5 else "🟢低风险")
        radar_info = f" [雷达:{item.get('sub_radar_result')}]" if item.get("sub_radar_result") else ""
        tro = " [TRO维权人]" if item.get("tro_holder") else ""
        print(f"{i}. {risk}{radar_info}{tro}")
        print(f"   相似度: {sim:.4f} | 权利人: {item.get('rights_owner', '')}")
        print(f"   版权标识码: {item.get('copyright_code', '')}")
        if item.get("path"):
            print(f"   版权画图片: {item.get('path')}")
        print()
    if len(items) > 20:
        print(f"... 还有 {len(items) - 20} 条结果未显示，使用 --json 查看完整结果")

    show_actual_deduct("c001", enable_radar)

# ── P001 纯图检测 ──────────────────────────────────────────────

def cmd_p001(args, token):
    # 展示预扣点
    show_pre_deduct("p001")

    img_b64 = load_image(args.image)
    result = api_call(token, "policy-compliance/v1/gun-parts-search",
                      {"base64_image": img_b64, "type": ["gun_parts"]})

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("p001")
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    items = result.get("data", {}).get("list", [])
    # API 可能返回字符串消息而非对象列表
    real_items = [it for it in items if isinstance(it, dict)]
    if not real_items:
        print("未找到相似违规产品，产品图片可能无违禁品风险")
        for it in items:
            if isinstance(it, str):
                print(f"  {it}")
        return

    print(f"找到 {len(real_items)} 条相似违规产品:\n")
    for i, item in enumerate(real_items, 1):
        cosine = float(item.get("cosine", 0))
        print(f"{i}. 相似度: {cosine:.4f}")
        print(f"   标题: {item.get('pd_title', '')}")
        print(f"   中文: {item.get('pd_title_CHN_censored', '')}")
        print()

    if any(float(it.get("cosine", 0)) >= 0.4 for it in real_items):
        print("建议: 存在高相似度违规产品，建议继续使用 p002 确认具体违反的政策")

    show_actual_deduct("p001")

# ── P002 纯文本检测 ────────────────────────────────────────────

def cmd_p002(args, token):
    # 展示预扣点和检测站点（图文同时入参仍为5点，不分开计费）
    sites = args.sites if args.sites else ["us"]
    show_default_regions("p002", sites)
    extra = "（图文同时入参检测仍为 5 点）" if args.feature_image else ""
    show_pre_deduct("p002", extra_info=extra)

    # 解析用户输入的 JSON 参数，带异常处理
    try:
        platform_sites = json.loads(args.platform_sites) if args.platform_sites else {"amazon": args.sites}
    except json.JSONDecodeError as e:
        print(f"错误: --platform-sites 参数 JSON 格式无效: {e}")
        sys.exit(1)

    try:
        feature_word_ids = json.loads(args.feature_word_ids) if args.feature_word_ids else []
    except json.JSONDecodeError as e:
        print(f"错误: --feature-word-ids 参数 JSON 格式无效: {e}")
        sys.exit(1)

    payload = {
        "product_title": args.title,
        "product_description": args.description or "",
        "product_title_suspected": args.suspected or "",
        "platform_sites": platform_sites,
        "feature_detect": {
            "enable": args.enable_feature,
            "features": {
                "feature_word_ids": feature_word_ids,
                "image": args.feature_image or "",
            },
        },
    }
    if args.type:
        payload["type"] = args.type

    result = api_call(token, "policy-compliance/v1/detection", payload, timeout=60)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        show_actual_deduct("p002")
        return
    if not result.get("success"):
        print(f"API 错误 [{result.get('code')}]: {result.get('message')}")
        sys.exit(1)

    items = result.get("data", {}).get("list", [])
    if not items:
        print("未检测到政策合规风险")
        show_actual_deduct("p002")
        return

    print(f"检测到 {len(items)} 条政策匹配:\n")
    for i, item in enumerate(items, 1):
        prohibited = item.get("prohibited", 0)
        compliance = item.get("compliance", 0)
        if prohibited:
            status = "🔴 禁售"
        elif compliance:
            status = "🟡 限售"
        else:
            status = "🟢 无风险"
        print(f"{i}. {status}")
        print(f"   平台: {item.get('platform', '')} | 地区: {item.get('site', '')}")
        print(f"   政策: {item.get('name_cn', '')} ({item.get('name', '')})")
        if item.get("reason"):
            print(f"   原因: {item.get('reason')}")
        print()

    show_actual_deduct("p002")

# ── P004-P007 风险特征词管理 ───────────────────────────────────

def cmd_p004(args, token):
    result = api_call(token, "policy-compliance/feature/v1/suggestion", {"word": args.word}, timeout=30)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if not result.get("success"):
        print(f"API 错误: {result.get('message')}")
        sys.exit(1)
    data = result.get("data", {})
    status_labels = {-2: "含糊无关", -1: "已够清晰，可直接保存", 0: "已匹配出多个清晰词"}
    print(f"状态: {status_labels.get(data.get('status', 0), data.get('status'))}")
    words = data.get("word_arr", [])
    if words:
        print(f"联想词: {', '.join(words)}")

def cmd_p005(args, token):
    result = api_call(token, "policy-compliance/feature/v1/save", {"word": args.word}, timeout=30)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if not result.get("success"):
        print(f"API 错误: {result.get('message')}")
        sys.exit(1)
    print(f"保存成功，ID: {result.get('data', {}).get('id')}")

def cmd_p006(args, token):
    result = api_call(token, "policy-compliance/feature/v1/delete", {"id": args.id}, timeout=30)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if not result.get("success"):
        print(f"API 错误: {result.get('message')}")
        sys.exit(1)
    print(f"删除成功，ID: {result.get('data', {}).get('id')}")

def cmd_p007(args, token):
    result = api_call(token, "policy-compliance/feature/v1/list",
                      {"per_page": args.per_page, "page": args.page}, timeout=30)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if not result.get("success"):
        print(f"API 错误: {result.get('message')}")
        sys.exit(1)
    data = result.get("data", {})
    items = data.get("data", [])
    print(f"共 {data.get('total', 0)} 条特征词 (第{args.page}页):\n")
    for item in items:
        ps_labels = {0: "未拉取", 1: "可用", 2: "拉取失败"}
        ps = ps_labels.get(item.get("pull_status", 0), "未知")
        print(f"  ID:{item.get('id')} | {item.get('words', '')} | 状态:{ps} | {item.get('create_time', '')}")

# ── 主入口 ─────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="睿观 ERiC 合规检测套件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""子命令说明:
  d001        D001 外观专利检测 (图片)
  i001        I001 发明专利检测 (文本)
  l001        L001 图形商标检测 (图片)
  t001        T001 文本商标检测 (文本)
  t002        T002 商标替换词 (文本)
  c001        C001 版权检测 (图片)
  p001        P001 政策合规-纯图检测 (图片)
  p002        P002 政策合规-纯文本检测 (文本)
  p004        P004 风险特征词联想
  p005        P005 风险特征词保存
  p006        P006 风险特征词删除
  p007        P007 风险特征词列表""",
    )
    sub = parser.add_subparsers(dest="command", help="检测类型")

    # D001
    d = sub.add_parser("d001", help="D001 外观专利检测")
    d.add_argument("image", help="图片来源: 文件路径 / URL / base64字符串")
    d.add_argument("--regions", nargs="+", default=["US"], help="国家代码 (默认 US)")
    d.add_argument("--top", type=int, default=50, help="召回数量 1-500 (默认 50)")
    d.add_argument("--mode", choices=["hybrid", "physical", "line"], default="hybrid", help="检索模式")
    d.add_argument("--title", default="", help="产品标题")
    d.add_argument("--description", default="", help="产品描述")
    d.add_argument("--enable-radar", action="store_true", default=True, help="开启雷达分析（默认开启）")
    d.add_argument("--no-radar", action="store_true", help="关闭雷达分析")
    d.add_argument("--no-tro", action="store_true", help="关闭TRO增强")
    d.add_argument("--loc", nargs="+", default=None, help="LOC分类范围")
    d.add_argument("--patent-status", nargs="+", type=int, default=[], help="专利有效性 (1=有效, 0=失效)")
    d.add_argument("--lang", default="", help="原文语言代码")
    d.add_argument("--json", action="store_true", help="输出原始JSON")

    # I001
    i = sub.add_parser("i001", help="I001 发明专利检测")
    i.add_argument("--title", required=True, help="产品标题 (最大500字符)")
    i.add_argument("--description", required=True, help="产品描述 (最大30000字符)")
    i.add_argument("--regions", nargs="+", default=["US"], help="国家代码 (当前仅 US)")
    i.add_argument("--top", type=int, default=100, help="召回数量 1-500 (默认 100)")
    i.add_argument("--json", action="store_true", help="输出原始JSON")

    # L001
    l = sub.add_parser("l001", help="L001 图形商标检测")
    l.add_argument("image", help="图片来源: 文件路径 / URL / base64字符串")
    l.add_argument("--top", type=int, default=20, help="召回数量 1-100 (默认 20)")
    l.add_argument("--regions", nargs="+", default=None, help="检测国家/地区")
    l.add_argument("--title", default="", help="产品标题")
    l.add_argument("--trademark-name", default="", help="可能的logo名称")
    l.add_argument("--enable-localizing", action="store_true", help="开启切图")
    l.add_argument("--enable-radar", action="store_true", default=True, help="开启雷达分析（默认开启）")
    l.add_argument("--no-radar", action="store_true", help="关闭雷达分析")
    l.add_argument("--json", action="store_true", help="输出原始JSON")

    # T001
    t1 = sub.add_parser("t001", help="T001 文本商标检测")
    t1.add_argument("--title", required=True, help="产品标题 (最大300字符)")
    t1.add_argument("--text", default="", help="产品文本 (最大5000字符)")
    t1.add_argument("--regions", nargs="+", default=["US"], help="国家/地区 (默认 US)")
    t1.add_argument("--auto-safe-words", action="store_true", help="自动为高风险词获取替换词")
    t1.add_argument("--json", action="store_true", help="输出原始JSON")

    # T002
    t2 = sub.add_parser("t002", help="T002 商标替换词")
    t2.add_argument("--title", required=True, help="产品标题")
    t2.add_argument("--text", required=True, help="产品描述")
    t2.add_argument("--trademark", required=True, help="商标词")
    t2.add_argument("--json", action="store_true", help="输出原始JSON")

    # C001
    c = sub.add_parser("c001", help="C001 版权检测")
    c.add_argument("image", help="图片来源: 文件路径 / URL / base64字符串")
    c.add_argument("--top", type=int, default=100, help="召回数量 1-200 (默认 100)")
    c.add_argument("--enable-radar", action="store_true", default=True, help="开启雷达检测（默认开启，+1点）")
    c.add_argument("--no-radar", action="store_true", help="关闭雷达检测")
    c.add_argument("--json", action="store_true", help="输出原始JSON")

    # P001
    p1 = sub.add_parser("p001", help="P001 政策合规-纯图检测")
    p1.add_argument("image", help="图片来源: 文件路径 / URL / base64字符串")
    p1.add_argument("--json", action="store_true", help="输出原始JSON")

    # P002
    p2 = sub.add_parser("p002", help="P002 政策合规-纯文本检测")
    p2.add_argument("--title", required=True, help="产品标题")
    p2.add_argument("--description", default="", help="产品描述")
    p2.add_argument("--sites", nargs="+", default=["us"], help="国家/地区 (默认 us, 支持: br,fr,au,us,uk,jp,it,es,mx,de,ca)")
    p2.add_argument("--platform-sites", default=None, help='平台国家JSON (如 \'{"amazon":["us"]}\')')
    p2.add_argument("--type", nargs="+", default=None, help="检测类型 (如 gun_parts)")
    p2.add_argument("--suspected", default="", help="疑似违规产品标题")
    p2.add_argument("--enable-feature", action="store_true", help="启用风险特征词检测")
    p2.add_argument("--feature-word-ids", default=None, help="风险特征词ID列表JSON")
    p2.add_argument("--feature-image", default="", help="检测图片URL")
    p2.add_argument("--json", action="store_true", help="输出原始JSON")

    # P004
    p4 = sub.add_parser("p004", help="P004 风险特征词联想")
    p4.add_argument("word", help="模糊词")
    p4.add_argument("--json", action="store_true", help="输出原始JSON")

    # P005
    p5 = sub.add_parser("p005", help="P005 风险特征词保存")
    p5.add_argument("word", help="特征词")
    p5.add_argument("--json", action="store_true", help="输出原始JSON")

    # P006
    p6 = sub.add_parser("p006", help="P006 风险特征词删除")
    p6.add_argument("id", type=int, help="特征词ID")
    p6.add_argument("--json", action="store_true", help="输出原始JSON")

    # P007
    p7 = sub.add_parser("p007", help="P007 风险特征词列表")
    p7.add_argument("--per-page", type=int, default=100, help="每页数量 (默认 100)")
    p7.add_argument("--page", type=int, default=1, help="页码 (默认 1)")
    p7.add_argument("--json", action="store_true", help="输出原始JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    token = check_token()
    cmds = {
        "d001": cmd_d001, "i001": cmd_i001, "l001": cmd_l001,
        "t001": cmd_t001, "t002": cmd_t002, "c001": cmd_c001,
        "p001": cmd_p001, "p002": cmd_p002,
        "p004": cmd_p004, "p005": cmd_p005, "p006": cmd_p006, "p007": cmd_p007,
    }
    cmds[args.command](args, token)

if __name__ == "__main__":
    main()
