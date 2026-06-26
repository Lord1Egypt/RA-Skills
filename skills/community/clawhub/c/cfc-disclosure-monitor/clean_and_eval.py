#!/usr/bin/env python3
"""
Phase 2: 统一清洗 + 内容评估 + 图片 OCR
读取 Phase 1 产出，对图片正文公告执行 MiniMax M2.7 VLM OCR，
保底使用 collectors 提取的 _truncated 列表预览文本。
"""
import base64, hashlib, json, os, re, ssl, sys, time, urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

TODAY = "2026-04-14"
OUT = Path.home() / f".openclaw/workspace/cfc_raw_data/cleaned_{TODAY}"

# ─── MiniMax M2.7 VLM OCR ────────────────────────────────────────────
MINIMAX_KEY = os.environ.get(
    "MINIMAX_API_KEY",
    "sk-cp-CT_VXVxvL9Eu71Wnp5NjLO6RatHKPker4laUs67t24Cmhk56xEOSyeU5-pHkjxJkLiFCvK8_AA7QY0g3MBAPWkzXRl1AnZiQBjPdvOCSRVQq4GDWElDPEUY",
)
MINIMAX_TEXT_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"
MINIMAX_VLM_URL = "https://api.minimax.chat/v1/coding_plan/vlm"


def minimax_vision(image_path: str, retries: int = 2) -> str:
    """
    用 MiniMax coding plan VLM 识别图片文字。
    endpoint: https://api.minimax.chat/v1/coding_plan/vlm
    请求: {"prompt": "...", "image_url": "data:image/png;base64,..."}
    响应: {"content": "...", "base_resp": {"status_code": 0}}
    失败返回空字符串。
    """
    for attempt in range(retries):
        try:
            with open(image_path, "rb") as f:
                img_data = f.read()
            b64 = base64.b64encode(img_data).decode("utf-8")

            # 自动检测图片类型
            if img_data[:4] == b"\x89PNG":
                mime = "image/png"
            elif img_data[:2] == b"\xff\xd8":
                mime = "image/jpeg"
            elif img_data[:4] == b"GIF8":
                mime = "image/gif"
            elif img_data[:4] == b"RIFF" and img_data[8:12] == b"WEBP":
                mime = "image/webp"
            else:
                mime = "image/png"

            payload = {
                "prompt": "请完整识别图中所有文字，保持原文格式。",
                "image_url": f"data:{mime};base64,{b64}",
            }

            req = urllib.request.Request(
                MINIMAX_VLM_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {MINIMAX_KEY}",
                    "MM-API-Source": "OpenClaw",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())

            status = result.get("base_resp", {}).get("status_code", -1)
            if status != 0:
                return ""
            text = result.get("content", "").strip()
            return text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return ""


def download_image_for_ocr(url: str, co_name: str) -> str:
    """
    下载图片到 /tmp，返回本地路径。
    失败返回空字符串。
    """
    try:
        # 构造 Referer（从 URL 提取域名）
        parsed = urllib.request.urlparse(url)
        referer = f"{parsed.scheme}://{parsed.netloc}/"
        if not referer.startswith("http"):
            referer = "https://www.haiercash.com/"

        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": referer,
        })
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            data = r.read()

        # 用 URL hash 做文件名，保留扩展名
        suffix = ""
        if "PNG" in url.upper():
            suffix = ".png"
        elif ".jpg" in url.lower() or "JPEG" in url.upper():
            suffix = ".jpg"
        elif ".gif" in url.lower():
            suffix = ".gif"
        elif ".webp" in url.lower():
            suffix = ".webp"

        h = hashlib.md5(url.encode()).hexdigest()[:12]
        path = f"/tmp/ocr_{h}{suffix}"
        with open(path, "wb") as f:
            f.write(data)
        return path
    except Exception as e:
        return ""


# ─── 导航词黑名单 ────────────────────────────────────────────────────
NAV = {
    "首页", "产品介绍", "联系我们", "关于我们", "加入我们", "新闻公告", "新闻中心", "企业介绍",
    "合作伙伴", "消保专栏", "消保园地", "企业动态", "重要公告", "公告通知", "公司动态", "公司新闻",
    "公司公告", "旗下产品", "乡村振兴", "采购公告", "信息披露", "服务价目", "产品公示",
    "投诉渠道", "隐私政策", "消费者之家", "企业社会责任", "扫码关注", "扫码下载", "联系方式",
    "下载APP", "服务热线", "客服热线", "客服咨询", "联系地址", "Copyright", "copyright",
    "浙ICP备", "浙公网安备", "粤ICP备", "京ICP备", "沪ICP备", "ICP备",
    "回到顶部", "返回首页", "在线客服", "官方客服",
}

NAV_PATTERNS = [
    r"^\s*重置\s*声音开关.*语速.*放大.*缩小",
    r"^\s*视窗\s*×loading.*登录/注册",
    r"视窗\s*×loading.*?(?=北京阳光|根据国家监管|序号\s*合作)",
    r"\s*登录/注册\s*",
    r"\s*首页\s*>\s*消保宣传专区\s*>\s*信息公告\s*",
    r"\s*首页\s*>\s*新闻公告\s*>\s*服务公告\s*",
    r"^\s*\*本站点已支持IPv6访问\*",
    r"^\s*‹›",
    r"^\s*您的浏览器不支持javascript",
    r"^\s*We're sorry but",
    r"\s*回到顶部\s*",
    r"\s*首页\s*>\s*新闻中心\s*>\s*信息公告\s*",
    r"\s*首页\s*>\s*新闻公告\s*>\s*信息公告\s*",
]


def is_nav(s: str) -> bool:
    s = s.strip()
    if not s:
        return False
    if s in NAV:
        return True
    for p in NAV_PATTERNS:
        if re.match(p, s):
            return True
    return False


def clean_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    for pat in NAV_PATTERNS:
        cleaned = re.sub(pat, "\n", cleaned, flags=re.DOTALL)

    lines, skip = [], 0
    for line in cleaned.split("\n"):
        s = line.strip()
        if not s:
            continue
        if is_nav(s):
            skip += 1
            if skip > 5:
                continue
            continue
        skip = 0
        lines.append(s)
    result = "\n".join(lines).strip()
    result = re.sub(r"^.*?您的位置[：:]\s*", "", result, flags=re.DOTALL)
    return result


def extract_title(text: str, orig: str) -> tuple:
    for line in text.split("\n")[:30]:
        s = line.strip()
        if not s or len(s) > 200:
            continue
        if is_nav(s):
            continue
        if any(k in s.lower() for k in ["javascript", "loading", "enable", "sorry"]):
            continue
        if re.match(r"^\d{4}[-/]\d{2}[-/]\d{2}", s):
            continue
        if re.match(r"^[\s\d\-><:：/.]+$", s):
            continue
        if "您的位置" in s or s.startswith(">"):
            continue
        if any(w in s for w in ["声音开关", "指读", "退出服务"]):
            continue
        return s, s != orig
    return orig, False


def classify(title: str) -> str:
    t = title
    if any(k in t for k in ["假冒", "冒用", "诈骗", "打假", "声明"]):
        return "打假声明"
    if any(k in t for k in ["关联", "交易"]):
        return "关联交易"
    if any(k in t for k in ["消费", "保护", "投诉", "征信", "权益"]):
        return "消费者保护"
    if any(k in t for k in ["转让", "债权", "资产"]):
        return "债权转让"
    if any(k in t for k in ["资本", "监管", "指标", "拨备"]):
        return "资本信息"
    if any(k in t for k in ["年度", "季度", "信披", "披露"]):
        return "定期报告"
    if any(k in t for k in ["社会责任", "公益", "捐赠"]):
        return "社会责任"
    if any(k in t for k in ["合作", "机构", "催收"]):
        return "合作机构"
    if any(k in t for k in ["许可证", "金融", "牌照"]):
        return "许可证公示"
    if any(k in t for k in ["招聘", "人才", "岗位"]):
        return "招聘信息"
    if any(k in t for k in ["审计", "会计", "财务"]):
        return "财务信息"
    return "重要公告"


def get_fulltext_from_file(co_dir: Path, aid: str) -> tuple:
    """读取 fulltext.txt 或 .pdf_text.txt。返回 (text, src)。"""
    base = co_dir / aid
    for fname in ["fulltext.txt", ".pdf_text.txt"]:
        fp = base / fname
        if fp.exists():
            try:
                t = fp.read_text(encoding="utf-8", errors="replace")
                if t and len(t) > 20:
                    return t, fname
            except Exception:
                pass
    return "", None


def score_content(text: str) -> tuple:
    """内容质量打分"""
    if not text:
        return 0, "空"
    l = len(text)
    if l < 50:
        return 0, "太短"
    if "公告" in text and l < 200:
        return 1, "仅公告标题"
    if "列表" in text[:500] and "产品介绍" in text[:1000]:
        return 1, "列表页残留"
    if l < 300:
        return 2, "内容偏短"
    if l < 1000:
        return 3, "中等长度"
    if l < 5000:
        return 4, "完整内容"
    return 5, "长文/报告"


def ocr_image_announcement(url: str, co_name: str) -> str:
    """
    下载图片并用 MiniMax VLM OCR 提取文字。
    失败返回空字符串。
    """
    img_path = download_image_for_ocr(url, co_name)
    if not img_path:
        return ""
    text = minimax_vision(img_path)
    # 清理临时文件
    try:
        os.unlink(img_path)
    except Exception:
        pass
    return text


# ─── 主流程 ────────────────────────────────────────────────────────────
def clean_and_eval():
    base = Path.home() / ".openclaw/workspace/cfc_raw_data"
    dates = ["2026-04-14"]

    all_cleaned = []
    stats = defaultdict(lambda: defaultdict(int))
    ocr_stats = {"attempted": 0, "success": 0, "fallback_truncated": 0, "failed": 0}

    for date_dir in dates:
        dp = base / date_dir
        if not dp.exists():
            continue

        for co_dir in sorted(dp.glob("*/")):
            co = co_dir.name
            ann_file = co_dir / "announcements.json"
            if not ann_file.exists():
                continue

            with open(ann_file, encoding="utf-8") as f:
                anns = json.load(f)

            # URL 去重
            by_url = defaultdict(list)
            for ann in anns:
                url = ann.get("url", ann.get("_content_id", ""))
                by_url[url].append(ann)

            for url, url_anns in by_url.items():
                # 取正文最长那条
                best_ann = max(
                    url_anns,
                    key=lambda a: len(
                        get_fulltext_from_file(co_dir, a.get("_content_id", ""))[0]
                        or a.get("text", "")
                        or a.get("_truncated", "")
                    ),
                )

                aid = best_ann.get("_content_id", "")
                content_type = best_ann.get("_content_type", "")
                raw_text, src = get_fulltext_from_file(co_dir, aid)
                ann_text = best_ann.get("text", "")
                truncated = best_ann.get("_truncated", "")

                # ── 图片公告：尝试 MiniMax VLM OCR ──────────────────────
                # 装饰性PNG判断：_truncated ≥ 200字 → 正文已在列表页提取，PNG是装饰标题图，跳过OCR
                if content_type == "image" and len(raw_text) < 30:
                    if truncated and len(truncated) >= 200:
                        # PNG装饰性：列表页_truncated已有完整正文
                        raw_text = truncated
                        src = "_truncated"
                        ocr_stats["skipped_decorative"] = ocr_stats.get("skipped_decorative", 0) + 1
                        print(f"  [skip decorative PNG] {co} {aid[:8]} _truncated={len(raw_text)}字", flush=True)
                    else:
                        # PNG可能有真实内容，或_truncated不足200字 → 尝试VLM OCR
                        ocr_stats["attempted"] += 1
                        print(f"  [OCR] {co} {aid[:8]} {url[:60]}", flush=True)

                        vlm_text = ocr_image_announcement(url, co)
                        if vlm_text and len(vlm_text) > 10:
                            raw_text = vlm_text
                            src = "vlm_ocr"
                            ocr_stats["success"] += 1
                            print(f"    -> VLM OCR 成功: {len(raw_text)}字", flush=True)
                        elif truncated and len(truncated) > 20:
                            raw_text = truncated
                            src = "_truncated"
                            ocr_stats["fallback_truncated"] += 1
                            print(f"    -> VLM 失败，保底 _truncated: {len(raw_text)}字", flush=True)
                        else:
                            ocr_stats["failed"] += 1
                            print(f"    -> VLM + _truncated 均失败", flush=True)

                # collectors 提取了 _truncated 但 text 为空时使用
                if not raw_text and truncated and len(truncated) > 20:
                    raw_text = truncated
                    src = "_truncated"

                clean_t = clean_text(raw_text)
                title, title_chg = extract_title(clean_t, best_ann.get("title", ""))
                score, reason = score_content(clean_t)

                item = {
                    "company": co,
                    "date": best_ann.get("date", ""),
                    "title": title if title else best_ann.get("title", "公告"),
                    "title_raw": best_ann.get("title", ""),
                    "title_changed": title_chg,
                    "url": url,
                    "category": best_ann.get("category", classify(title)),
                    "source_date": date_dir,
                    "source": src or "none",
                    "text_length": len(clean_t),
                    "score": score,
                    "score_reason": reason,
                    "is_valid": score >= 2,
                    "is_dup_url": len(url_anns) > 1,
                    "url_group_size": len(url_anns),
                    "_content": clean_t[:500],
                }
                all_cleaned.append(item)

                stats[co][f"score_{score}"] += 1
                if score >= 2:
                    stats[co]["valid"] += 1
                if score >= 4:
                    stats[co]["high"] += 1
                if len(url_anns) > 1:
                    stats[co]["dup"] += 1

    # ── 统计输出 ────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print(f"{'公司':<20} {'总数':>5} {'有效':>5} {'高分':>5} {'重复':>5} {'均长':>7}")
    print(f"{'=' * 70}")
    for co in sorted(stats.keys()):
        s = stats[co]
        total = sum(v for k, v in s.items() if k.startswith("score_"))
        avg_len = sum(
            it["text_length"]
            for it in all_cleaned
            if it["company"] == co and it["is_valid"]
        ) / max(s.get("valid", 1), 1)
        print(
            f"{co:<20} {total:>5} {s.get('valid', 0):>5} "
            f"{s.get('high', 0):>5} {s.get('dup', 0):>5} {avg_len:>6.0f}字"
        )
    print(f"{'=' * 70}")
    total_all = len(all_cleaned)
    valid_all = sum(1 for it in all_cleaned if it["is_valid"])
    high_all = sum(1 for it in all_cleaned if it["score"] >= 4)
    print(f"{'合计':<20} {total_all:>5} {valid_all:>5} {high_all:>5}")

    print(f"\n{'=' * 50}")
    print(f"图片 OCR 统计（海尔的图片公告）")
    print(
        f"  装饰性跳过: {ocr_stats.get('skipped_decorative', 0)} | "
        f"尝试OCR: {ocr_stats['attempted']} | "
        f"VLM成功: {ocr_stats['success']} | "
        f"_truncated保底: {ocr_stats['fallback_truncated']} | "
        f"失败: {ocr_stats['failed']}"
    )

    # 分类统计
    print(f"\n{'=' * 50}")
    print("内容分类分布（有效公告）")
    cat_counts = defaultdict(int)
    for it in all_cleaned:
        if it["is_valid"]:
            cat_counts[it["category"]] += 1
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20} {cnt:>5}")

    # 保存结果
    OUT.mkdir(parents=True, exist_ok=True)

    meta_out = [{k: v for k, v in it.items() if k != "_content"} for it in all_cleaned]
    with open(OUT / "all_announcements_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta_out, f, ensure_ascii=False, indent=2)

    valid_out = [it for it in all_cleaned if it["is_valid"]]
    with open(OUT / "valid_announcements.json", "w", encoding="utf-8") as f:
        json.dump(valid_out, f, ensure_ascii=False, indent=2)

    # 按公司分目录保存 fulltext（只存有效内容）
    for it in valid_out:
        co = it["company"]
        uid = hashlib.md5(it["url"].encode()).hexdigest()[:8]
        co_dir_out = OUT / co
        co_dir_out.mkdir(parents=True, exist_ok=True)
        ft_path = co_dir_out / f"{uid}_fulltext.txt"
        ft_path.write_text(it["_content"] or it["title"], encoding="utf-8")

    print(f"\n结果已保存到: {OUT}/")
    print(f"  all_announcements_meta.json: {len(meta_out)} 条（元数据）")
    print(f"  valid_announcements.json: {len(valid_out)} 条（有效内容）")

    # 高分内容评估
    print(f"\n{'=' * 50}")
    print("内容价值评估（高分内容分类）")
    high_items = [it for it in all_cleaned if it["score"] >= 4]
    cat_high = defaultdict(list)
    for it in high_items:
        cat_high[it["category"]].append(it)

    for cat, items in sorted(cat_high.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"\n  【{cat}】{len(items)}条")
        for it in items[:3]:
            print(f"    [{it['company']}] {it['date']} | {it['title'][:50]}")
            print(f"      {it['text_length']}字 | {it['score_reason']}")
            print(f"      预览: {it['_content'][:150].strip()}")

    return all_cleaned, stats, ocr_stats


if __name__ == "__main__":
    all_cleaned, stats, ocr_stats = clean_and_eval()
