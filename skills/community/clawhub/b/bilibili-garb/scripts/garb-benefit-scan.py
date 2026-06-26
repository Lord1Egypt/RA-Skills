#!/usr/bin/env python3
"""
B站个性装扮 benefit 子项批量采集脚本 (v2, sanitized)

从 decorations-database.json 读取装扮列表，逐条调用 benefit API
获取 suit_items 子项数据，结果追加写入 garb-benefit-results.ndjson。

所有认证信息从 configs/bili-api-creds.json 或环境变量读取。

v2 优化点：
- 只扫描 biz_type=1 装扮套装（跳过收藏集卡片/装扮/关联收藏集，省70%调用）
- 跳过 owned!=1（未拥有）和已有benefit数据的记录
- DIY套装自动检测 is_diy=1（item_id含横杠或非纯数字）
- 完整提取 properties 所有非空字段（横竖图/视频/粉丝牌/主题色/表情列表等）
- access_key 从 configs/bili-api-creds.json 动态读取

关键知识：
- part 参数只需 space_bg 一次，即可返回全部 9 种子项
- DIY套装：item_id参数必须传biz_id（原始item_id含横杠会报-400）
- 支持断点续传、--limit、--dry-run、Ctrl+C 优雅退出
"""

import json
import time
import hashlib
import urllib.parse
import urllib.request
import ssl
import sys
import signal
import argparse
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────────────────────
APPKEY = os.environ.get("BILI_APPKEY", "27eb53fc9058f8c3")
APPSECRET = os.environ.get("BILI_APPSECRET", "")  # Must be set via config or env var

BENEFIT_URL = "https://api.bilibili.com/x/garb/v2/user/suit/benefit"
PART = "space_bg"  # 一次即可返回全部子项

BASE_DIR = Path(os.environ.get("BILI_WORKSPACE", Path(__file__).resolve().parent.parent))
DATA_DIR = BASE_DIR / "data"
CREDS_FILE = BASE_DIR / "configs" / "bili-api-creds.json"
DB_FILE = DATA_DIR / "decorations-database.json"
PROGRESS_FILE = DATA_DIR / "garb-benefit-scan.progress.json"
RESULTS_FILE = DATA_DIR / "garb-benefit-results.ndjson"

REQ_INTERVAL = 1.0  # 秒
REQ_TIMEOUT = 15     # 秒
MAX_RETRIES = 1      # 超时重试次数

TZ_SHANGHAI = timezone(timedelta(hours=8))

# ── 凭证加载 ──────────────────────────────────────────────────────────
def load_creds():
    """从 configs/bili-api-creds.json 或环境变量加载凭证"""
    creds = {}
    
    # Try config file first
    if CREDS_FILE.exists():
        with open(CREDS_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
    else:
        # Fall back to environment variables
        creds = {
            "access_key": os.environ.get("BILI_ACCESS_KEY", ""),
            "csrf": os.environ.get("BILI_CSRF", ""),
            "DedeUserID": os.environ.get("BILI_UID", ""),
            "SESSDATA": os.environ.get("BILI_SESSDATA", ""),
        }
    
    if not creds.get("access_key"):
        print(f"[ERROR] No access_key found. Set BILI_ACCESS_KEY env var or create {CREDS_FILE}")
        sys.exit(1)
    if not creds.get("SESSDATA"):
        print(f"[ERROR] No SESSDATA found. Set BILI_SESSDATA env var or create {CREDS_FILE}")
        sys.exit(1)
    
    appsecret = creds.get("appsecret", APPSECRET)
    if not appsecret:
        print(f"[ERROR] No appsecret found. Set BILI_APPSECRET env var or add to {CREDS_FILE}")
        print("[HINT] APPSECRET can be obtained from Bilibili mobile client")
        sys.exit(1)
    
    return {
        "appkey": creds.get("appkey", APPKEY),
        "appsecret": appsecret,
        "access_key": creds["access_key"],
        "csrf": creds["csrf"],
        "uid": str(creds.get("DedeUserID", "")),
        "cookie": f'SESSDATA={creds["SESSDATA"]}; bili_jct={creds["csrf"]}; DedeUserID={creds.get("DedeUserID", "")}',
    }

# ── SSL ────────────────────────────────────────────────────────────────
ctx = ssl.create_default_context()

# ── 签名 ──────────────────────────────────────────────────────────────
def calc_sign(params_dict, creds):
    """B站移动端 API 签名：参数排序 → urlencode → 追加 APPSECRET → MD5"""
    ts = str(int(time.time()))
    all_params = dict(params_dict)
    all_params.update({
        "access_key": creds["access_key"],
        "appkey": creds["appkey"],
        "csrf": creds["csrf"],
        "mobi_app": "iphone",
        "platform": "ios",
        "ts": ts,
    })
    sorted_items = sorted(all_params.items())
    query = urllib.parse.urlencode(sorted_items)
    sign_str = query + creds["appsecret"]
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
    all_params["sign"] = sign
    return all_params

# ── HTTP 请求 ─────────────────────────────────────────────────────────
def api_get(params, creds, retry=MAX_RETRIES):
    """GET benefit API，签名 + Cookie，自动重试"""
    signed = calc_sign(params, creds)
    query = urllib.parse.urlencode(signed)
    full_url = f"{BENEFIT_URL}?{query}"

    req = urllib.request.Request(full_url)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 BiliDroid/7.37.0 (bbcallen@gmail.com) "
        "os/android model/M2012K11AC mobi_app/android build/7370300 "
        "channel/bili innerVer/7370300 osVer/12 network/2",
    )
    req.add_header("Referer", "https://www.bilibili.com/")
    req.add_header("Cookie", creds["cookie"])

    for attempt in range(retry + 1):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=REQ_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            return {"code": -e.code, "message": f"HTTP {e.code}: {body}"}
        except Exception as e:
            if attempt < retry:
                time.sleep(1)
                continue
            return {"code": -1, "message": str(e)}

# ── 完整子项提取 ──────────────────────────────────────────────────────
def extract_properties_value(val):
    """递归提取 properties 中的值，跳过空值和空容器"""
    if val is None:
        return None
    if isinstance(val, (str, int, float, bool)):
        if isinstance(val, str) and val.strip() == "":
            return None
        return val
    if isinstance(val, list):
        result = []
        for item in val:
            extracted = extract_properties_value(item)
            if extracted is not None:
                result.append(extracted)
        return result if result else None
    if isinstance(val, dict):
        result = {}
        for k, v in val.items():
            extracted = extract_properties_value(v)
            if extracted is not None:
                result[k] = extracted
        return result if result else None
    return None


def extract_benefit_items(suit_items):
    """从 suit_items 完整提取各子项数据，保留 item_id/name + properties 全部非空字段"""
    if not suit_items or not isinstance(suit_items, dict):
        return None

    result = {}
    for part_name, part_data in suit_items.items():
        if not part_data:
            continue
        items = part_data if isinstance(part_data, list) else [part_data]
        extracted = []
        for item in items:
            if not isinstance(item, dict):
                continue
            entry = {
                "item_id": item.get("item_id"),
                "name": item.get("name", ""),
            }
            props = item.get("properties")
            if props and isinstance(props, dict):
                for pk, pv in props.items():
                    extracted_val = extract_properties_value(pv)
                    if extracted_val is not None:
                        entry[pk] = extracted_val
            extracted.append(entry)
        if extracted:
            result[part_name] = extracted
    return result if result else None


def summarize_benefit(benefit_items):
    """生成简短的 benefit 摘要用于日志输出"""
    if not benefit_items:
        return "none"
    parts = []
    for part_name, items in benefit_items.items():
        extra_fields = set()
        for item in items:
            extra_fields.update(k for k in item if k not in ("item_id", "name"))
        if extra_fields:
            parts.append(f"{part_name}({len(items)}项,{len(extra_fields)}字段)")
        else:
            parts.append(f"{part_name}({len(items)}项)")
    return " ".join(parts)

# ── 已有结果加载（去重） ──────────────────────────────────────────────
def load_existing_biz_ids():
    """从已有的 ndjson 结果文件中加载已成功获取 benefit 的 biz_id 集合"""
    existing = set()
    if not RESULTS_FILE.exists():
        return existing
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("benefit_items"):
                        biz_id = rec.get("biz_id")
                        if biz_id is not None:
                            existing.add(biz_id)
                except (json.JSONDecodeError, KeyError):
                    continue
    except Exception:
        pass
    return existing

# ── 进度管理 ──────────────────────────────────────────────────────────
def load_progress():
    if PROGRESS_FILE.exists():
        try:
            return set(json.loads(PROGRESS_FILE.read_text("utf-8")))
        except Exception:
            return set()
    return set()


def save_progress(done_set):
    PROGRESS_FILE.write_text(
        json.dumps(sorted(done_set), ensure_ascii=False) + "\n", encoding="utf-8"
    )

# ── DIY 检测 ──────────────────────────────────────────────────────────
def is_diy_item(item_id):
    """判断是否为 DIY 套装：item_id 含横杠或非纯数字 → is_diy=1"""
    s = str(item_id)
    return "-" in s or not s.isdigit()

# ── 主逻辑 ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="B站装扮 benefit 子项批量采集 v2")
    parser.add_argument("--limit", type=int, default=0, help="限制处理数量（0=全部）")
    parser.add_argument("--dry-run", action="store_true", help="只打印不请求")
    parser.add_argument("--force", action="store_true", help="强制重新扫描已有benefit的记录")
    parser.add_argument("--debug", action="store_true", help="输出完整API响应（调试用）")
    args = parser.parse_args()

    # 1. 加载凭证
    creds = load_creds()
    print(f"[INFO] 凭证已加载: uid={creds['uid']}, access_key={creds['access_key'][:8]}...")

    # 2. 加载数据库
    if not DB_FILE.exists():
        print(f"[ERROR] 数据库文件不存在: {DB_FILE}")
        print(f"[HINT] Set BILI_WORKSPACE env var or ensure data/decorations-database.json exists")
        sys.exit(1)

    records = []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"[INFO] 数据库共 {len(records)} 条记录")

    # 3. 过滤：只保留装扮套装(biz_type=1)且 owned>=1
    filtered = []
    skipped_stats = {"biz_type": 0, "not_owned": 0}
    for rec in records:
        biz_type = rec.get("biz_type")
        if biz_type != 1:
            skipped_stats["biz_type"] += 1
            continue
        owned = rec.get("owned", 0)
        if not owned or owned < 1:
            skipped_stats["not_owned"] += 1
            continue
        filtered.append(rec)
    print(f"[INFO] 过滤后: {len(filtered)} 条装扮套装 (跳过: {skipped_stats['biz_type']}非套装, {skipped_stats['not_owned']}未拥有)")

    # 4. 去重
    existing_biz_ids = set() if args.force else load_existing_biz_ids()
    if existing_biz_ids:
        print(f"[INFO] 已有 benefit 数据: {len(existing_biz_ids)} 条，将跳过 (用 --force 强制重扫)")
    else:
        print(f"[INFO] 无已有 benefit 数据，将全量扫描")

    # 5. 加载进度（断点续传）
    done = load_progress()
    if done:
        print(f"[INFO] 断点续传: 已处理 {len(done)} 条")

    # 6. Ctrl+C 优雅退出
    interrupted = False

    def on_signal(sig, frame):
        nonlocal interrupted
        print("\n[INFO] 收到中断信号，正在保存进度...")
        interrupted = True

    signal.signal(signal.SIGINT, on_signal)

    # 7. 逐条处理
    processed = 0
    skipped_dedup = 0
    skipped_progress = 0
    ok_count = 0
    err_count = 0
    diy_count = 0
    results_fh = open(RESULTS_FILE, "a", encoding="utf-8") if not args.dry_run else None

    try:
        for rec in filtered:
            if interrupted:
                break

            biz_id = rec.get("biz_id")
            item_id = rec.get("item_id")
            title = rec.get("title", "")
            deco_type = rec.get("deco_type", "")

            # 去重
            if biz_id in existing_biz_ids:
                skipped_dedup += 1
                continue

            # 断点续传
            progress_key = f"{biz_id}"
            if progress_key in done:
                skipped_progress += 1
                continue

            if args.limit and processed >= args.limit:
                print(f"[INFO] 已达 --limit={args.limit}，停止")
                break

            # DIY 检测
            diy_flag = is_diy_item(item_id)
            is_diy_str = "1" if diy_flag else "0"
            diy_tag = " [DIY]" if diy_flag else ""
            if diy_flag:
                diy_count += 1

            print(
                f"[{processed+1}] {title}{diy_tag} "
                f"(biz_id={biz_id}, item_id={item_id}, is_diy={is_diy_str}) ... ",
                end="", flush=True,
            )

            if args.dry_run:
                print("DRY-RUN")
                processed += 1
                continue

            # 调用 benefit API
            # DIY套装必须用biz_id作为item_id参数（原始item_id含横杠会报-400）
            api_item_id = str(biz_id) if diy_flag else str(item_id)
            params = {
                "item_id": api_item_id,
                "part": PART,
                "is_diy": is_diy_str,
                "vmid": creds["uid"],
            }
            resp = api_get(params, creds)

            now = datetime.now(TZ_SHANGHAI).isoformat(timespec="seconds")
            result_record = {
                "biz_id": biz_id,
                "biz_type": rec.get("biz_type"),
                "title": title,
                "item_id": item_id,
                "is_diy": diy_flag,
                "deco_type": deco_type,
                "benefit_items": None,
                "scan_time": now,
            }

            if resp.get("code") != 0:
                msg = resp.get("message", str(resp))
                result_record["error"] = msg
                print(f"ERROR code={resp.get('code')} msg={msg[:80]}")
                err_count += 1
                if args.debug:
                    print(f"  [DEBUG] params={params}")
                    print(f"  [DEBUG] resp={json.dumps(resp, ensure_ascii=False)[:500]}")
            else:
                suit_items = (resp.get("data") or {}).get("suit_items")
                result_record["benefit_items"] = extract_benefit_items(suit_items)
                summary = summarize_benefit(result_record["benefit_items"])
                print(f"OK → {summary}")
                ok_count += 1

            # 追加写入结果
            results_fh.write(json.dumps(result_record, ensure_ascii=False) + "\n")
            results_fh.flush()

            # 更新进度
            done.add(progress_key)
            save_progress(done)
            processed += 1

            # 请求间隔
            time.sleep(REQ_INTERVAL)

    finally:
        if results_fh:
            results_fh.close()
        save_progress(done)
        print(f"\n{'='*60}")
        print(f"[DONE] 本次扫描: {processed} 条")
        print(f"  成功: {ok_count} | 失败: {err_count} | DIY套装: {diy_count}")
        print(f"  跳过(已有数据): {skipped_dedup} | 跳过(断点续传): {skipped_progress}")
        print(f"  累计已处理: {len(done)} 条")


if __name__ == "__main__":
    main()
