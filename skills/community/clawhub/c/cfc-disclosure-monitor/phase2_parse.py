"""
Phase 2: 披露内容解析
从 announcements.json 读取 → 下载 PDF → pdftotext 提取 → 保存结构化 JSON

职责:
  1. 扫描 announcements.json 中的 PDF 链接
  2. 下载 PDF → 保存到 cfc_raw_data/{公司}/attachments/
  3. pdftotext 提取文本 → 保存到 parsed/{公司}/{id}.txt
  4. 识别合作机构类型，提取公司名+电话 → 保存 {公司}_合作机构_{type}{date}.json

VLM OCR（扫描件）:
  对于 pdftotext 失败的 PDF（文本<50字），写入 vlm_queue.jsonl
  运行 python3 vlm_ocr.py 处理队列

用法:
  python3 phase2_parse.py                  # 全量
  python3 phase2_parse.py 中邮消费金融     # 单公司
"""
import json
import re
import subprocess
import sys
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse

# 共享配置路径
SKILL_DIR = Path(__file__).parent
RAW_DIR = Path(__file__).parent.parent.parent / "cfc_raw_data"
PARSED_DIR = SKILL_DIR / "parsed"
VLM_QUEUE = RAW_DIR / "vlm_queue.jsonl"


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def download_pdf(url: str, dest: Path, timeout: int = 30) -> bool:
    """下载 PDF 到 dest，返回是否成功。"""
    if dest.exists() and dest.stat().st_size > 100:
        return True  # 已存在，跳过
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            if content[:4] != b'%PDF':
                return False
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, 'wb') as f:
                f.write(content)
            return True
    except Exception:
        return False


def extract_pdf_text(pdf_path: Path) -> str:
    """用 pdftotext 提取 PDF 文本。"""
    try:
        result = subprocess.run(
            ['pdftotext', str(pdf_path), '-'],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout
    except Exception:
        return ""


def pdf_to_png_list(pdf_path: Path, out_dir: Path, max_pages: int = 5) -> list[Path]:
    """
    用 pdftoppm 将 PDF 转为 PNG 图片列表。
    返回图片路径列表。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ['pdftoppm', '-r', '150', '-l', str(max_pages),
             '-png', '-f', '1', str(pdf_path),
             str(out_dir / 'page')],
            capture_output=True, text=True, timeout=120
        )
        # pdftoppm 输出: page-1.png, page-2.png, ...
        pages = sorted(out_dir.glob('page-*.png'))
        return pages
    except Exception:
        return []


def queue_for_vlm(pdf_path: Path, dtype: str, date: str):
    """将 PDF 加入 VLM OCR 队列。"""
    with open(VLM_QUEUE, 'a') as f:
        f.write(json.dumps({
            "pdf_path": str(pdf_path),
            "dtype": dtype,
            "date": date,
        }, ensure_ascii=False) + '\n')


def queue_for_vlm_image(img_path: Path, dtype: str, date: str):
    """将图片加入 VLM OCR 队列。"""
    with open(VLM_QUEUE, 'a') as f:
        f.write(json.dumps({
            "image_path": str(img_path),
            "dtype": dtype,
            "date": date,
        }, ensure_ascii=False) + '\n')


def extract_table_pairs(text: str) -> list[dict]:
    """
    从 PDF 文本中提取公司名+电话对。
    返回 [{name, phone}, ...]
    """
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    pairs = []
    skip_keywords = ['合作公司名称', '联系电话', '尊敬的', '现将我司', '如有疑问',
                     '消费金融', '公告', '关于', '为落实', '附件',
                     '合作机构名称', '合作类型', '互联网助贷', '合作机构信息公示',
                     '有限公司互联网', '单如下', '份有限公司', '机构名单', '予以公示',
                     '具体名', '序号', '电话', '地址']

    i = 0
    while i < len(lines):
        name = lines[i].strip()
        if any(k in name for k in skip_keywords) or len(name) < 4:
            i += 1
            continue

        phone = ""
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            phone_clean = re.sub(r'[\s\-\(\)]+', '', nxt)
            if re.match(r'^(0\d{2,3}|1[3-9]|95\d{3,5}|400|800)\d', phone_clean) and len(phone_clean) >= 7:
                phone = nxt
                i += 2
            else:
                name_end = re.search(r'\d{3,4}[-\s]\d{7,8}', name)
                if name_end:
                    phone = name_end.group()
                    name = name[:name_end.start()].strip()
                i += 1
        else:
            i += 1

        # 修复换行断裂
        name = re.sub(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])', r'\1\2', name)
        name = re.sub(r'\d{7,}.*$', '', name).strip()

        if name and len(name) >= 4:
            pairs.append({'name': name, 'phone': phone})

    # 去重
    seen = set()
    unique = []
    for p in pairs:
        if p['name'] not in seen:
            seen.add(p['name'])
            unique.append(p)
    return unique


def detect_disclosure_type(title: str) -> str:
    if any(k in title for k in ['催收']):
        return '催收合作机构'
    if any(k in title for k in ['增信', '担保']):
        return '互联网贷款增信服务机构'
    if any(k in title for k in ['平台', '运营机构', '合作机构', '助贷']):
        return '互联网贷款平台运营机构'
    if '关联交易' in title:
        return '关联交易'
    if '不良资产' in title:
        return '不良资产转让'
    return '其他'


def extract_date_from_text(text: str) -> str:
    m = re.search(r'20\d{2}年\d{1,2}月\d{1,2}日', text)
    if m:
        return m.group().replace('年', '-').replace('月', '-').replace('日', '')
    return ""


def fetch_html_pdf_links(url: str, timeout: int = 15) -> list[str]:
    """抓取 HTML 页面，提取 <a href="*.pdf">"""
    try:
        import httpx
        headers = {"User-Agent": "Mozilla/5.0"}
        with httpx.Client(follow_redirects=True, timeout=timeout) as client:
            resp = client.get(url, headers=headers)
            html = resp.text
        from urllib.parse import urljoin
        pdf_links = re.findall(r'href=["\']([^"\']+\.pdf)', html, re.I)
        results = []
        for rel in pdf_links:
            results.append(urljoin(url, rel))
        return list(dict.fromkeys(results))
    except Exception:
        return []


def find_pdf_links(item: dict, base_url: str = "") -> list[str]:
    """从 announcement 中提取 PDF URL（_attachments > 绝对URL > 相对URL > HTML抓取）。"""
    urls = []
    text = item.get("text", "")
    attachments = item.get("_attachments", [])
    ann_url = item.get("url", "") or base_url

    # 1. _attachments
    for att in attachments:
        if isinstance(att, dict) and '.pdf' in att.get('url', '').lower():
            urls.append(att['url'])

    # 2. 绝对 URL
    abs_urls = re.findall(r'https?://[^\s\'"<>]+\.pdf', text, re.I)
    urls.extend(abs_urls)

    # 3. 正文提.pdf但无URL → 推断base
    if '.pdf' in text.lower():
        from urllib.parse import urljoin, urlparse
        if ann_url:
            parsed = urlparse(ann_url)
            base = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rsplit('/', 1)[0]}/"
            rel = re.findall(r'["\']([^"\']*\.pdf)', text)
            for r in rel:
                urls.append(urljoin(base, r))

    # 4. 仍未找到 → 跳过（HTML抓取容易超时，且大多数PDF链接已在文本中）
    #    如需启用，恢复下行并确保 timeout 短
    pass

    return list(dict.fromkeys(urls))


def process_company(company: str, announcements: list, base_url: str = "") -> dict:
    """处理单个公司所有公告，下载PDF+提取文本+识别合作机构。"""
    results = {
        "pdf_downloaded": 0,
        "text_extracted": 0,
        "vlm_queued": 0,
        "cooperation_entities": {},
    }

    for item in announcements:
        title = item.get("title", "")[:100]
        date = item.get("date", "")
        dtype = detect_disclosure_type(title)

        pdf_urls = find_pdf_links(item, base_url)

        for pdf_url in pdf_urls:
            url_hash = hashlib.md5(pdf_url.encode()).hexdigest()[:12]
            ext = Path(pdf_url).suffix or ".pdf"
            fname = f"{url_hash}{ext}"
            att_dir = ensure_dir(RAW_DIR / company / "attachments")
            pdf_path = att_dir / fname

            if not download_pdf(pdf_url, pdf_path):
                continue
            results["pdf_downloaded"] += 1

            text = extract_pdf_text(pdf_path)
            text_ok = bool(text and len(text.strip()) >= 50)

            if not text_ok:
                # 可能是扫描件，加入VLM队列
                queue_for_vlm(pdf_path, dtype, date)
                results["vlm_queued"] += 1
                print(f"    [VLM队列] {pdf_path.name} (size={pdf_path.stat().st_size//1024}KB)")
                continue

            # 保存文本
            txt_dir = ensure_dir(PARSED_DIR / company)
            txt_path = txt_dir / f"{url_hash}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            results["text_extracted"] += 1

            # 提取合作机构（仅当 dtype 关键词与 title 匹配时，防止误提取）
            dtype_keywords = ['催收', '增信', '担保', '平台', '互联网贷款', '合作机构', '助贷']
            title_has_coop = any(k in title for k in ['催收', '增信', '担保', '平台', '合作机构', '助贷', '消费贷'])
            if any(k in dtype for k in dtype_keywords) and title_has_coop:
                entities = extract_table_pairs(text)
                # 防垃圾：如果提取的条目数>300，说明是从非列表文本贪婪匹配，应丢弃
                if entities and len(entities) <= 300:
                    date_str = extract_date_from_text(text) or date
                    key = f"{dtype}_{date_str}"
                    results["cooperation_entities"][key] = entities

        # 处理图片附件（_content_type: image 的公告）
        content_type = item.get("_content_type", "")
        if content_type == "image":
            attachments = item.get("_attachments", [])
            for att in attachments:
                if isinstance(att, dict) and att.get("type") == "image":
                    img_path_str = att.get("path", "")
                    if img_path_str and Path(img_path_str).exists():
                        queue_for_vlm_image(Path(img_path_str), dtype, date)
                        results["vlm_queued"] += 1
                        print(f"    [VLM队列 image] {Path(img_path_str).name}")

    return results


def save_entities(company: str, entities_map: dict):
    """保存合作机构数据到顶层结构化文件。"""
    for key, entities in entities_map.items():
        parts = key.rsplit('_', 1)
        dtype = parts[0] if parts else "合作机构"
        fname = f"{company}_合作机构_{key}.json"
        fpath = RAW_DIR / fname
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(entities, f, ensure_ascii=False, indent=2)
        print(f"    Saved: {fname} ({len(entities)} entries)")


def run(company: str = None) -> dict:
    """
    Phase 2 主入口。
    扫描 raw_dir/{日期}/{公司}/announcements.json，
    对每家公司执行 PDF下载+文本提取+机构识别。
    扫描件自动写入 vlm_queue.jsonl，由 vlm_ocr.py 处理。
    """
    summary = {}

    for date_dir in sorted(RAW_DIR.iterdir()):
        if not date_dir.is_dir():
            continue
        if not re.match(r'^20\d{2}-\d{2}-\d{2}$', date_dir.name):
            continue

        for co_dir in sorted(date_dir.iterdir()):
            if not co_dir.is_dir():
                continue
            if company and co_dir.name != company:
                continue

            ann_file = co_dir / "announcements.json"
            if not ann_file.exists():
                continue

            with open(ann_file) as f:
                announcements = json.load(f)

            print(f"Phase 2: [{date_dir.name}] {co_dir.name} ({len(announcements)} announcements)")
            base_url = announcements[0].get("url", "") if announcements else ""

            results = process_company(co_dir.name, announcements, base_url)

            if results["cooperation_entities"]:
                save_entities(co_dir.name, results["cooperation_entities"])

            # 累加到 summary（同公司多日期目录时累加）
            key = f"{co_dir.name}"
            if key not in summary:
                summary[key] = results
            else:
                s = summary[key]
                s["pdf_downloaded"] += results["pdf_downloaded"]
                s["text_extracted"] += results["text_extracted"]
                s["vlm_queued"] += results["vlm_queued"]
                s["cooperation_entities"].update(results["cooperation_entities"])

    print(f"\nPhase 2 done. Summary:")
    total_pdfs = total_texts = total_vlm = 0
    for co, s in summary.items():
        print(f"  {co}: {s['pdf_downloaded']} PDFs, {s['text_extracted']} texts, {s['vlm_queued']} VLM, {list(s['cooperation_entities'].keys())}")
        total_pdfs += s['pdf_downloaded']
        total_texts += s['text_extracted']
        total_vlm += s['vlm_queued']
    print(f"  Total: {total_pdfs} PDFs, {total_texts} texts, {total_vlm} VLM queued")

    return summary


if __name__ == "__main__":
    co = sys.argv[1] if len(sys.argv) > 1 else None
    run(company=co)
