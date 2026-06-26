"""
fix_ningyin_mengshang.py — 针对性修复宁银/蒙商/晋商的合作机构采集

问题分类：
1. 宁银(cfcbnb): Vue动态页面 → 用 data.json API 直接拿URL+标题
2. 蒙商(mengshangxiaofei): HTML正文被截断 → 重抓详情页全文
3. 晋商(jcfc): 已有URL但正文不完整 → 重抓验证

输出: 更新 announcements.json + 下载PDF + 提取文本
"""
import json
import re
import subprocess
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin
import httpx

SKILL_DIR = Path(__file__).parent
RAW_DIR = SKILL_DIR.parent.parent.parent / "cfc_raw_data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": ""
}


# ──────────────────────────────────────────────────────────────
# 1. 宁银消费金融: Vue data.json API
# ──────────────────────────────────────────────────────────────
async def fetch_ningyin_announcements() -> list[dict]:
    """从 data.json API 获取宁银所有公告列表。"""
    base_url = "https://www.cfcbnb.com/xwgg/zygg/"
    items = []
    page = 0
    seen_urls = set()
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        while True:
            if page == 0:
                api_url = f"{base_url}data.json"
            else:
                api_url = f"{base_url}data_{page}.json"
            
            try:
                r = await c.get(api_url, headers=HEADERS)
                if r.status_code != 200:
                    break
                data = r.json()
                records = data.get("list", [])
                if not records:
                    break
                for rec in records:
                    url = urljoin(base_url, rec.get("URL", ""))
                    title = rec.get("DOCTITLE", "").strip()
                    date = rec.get("DOCRELTIME", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        items.append({
                            "title": title,
                            "date": date,
                            "url": url,
                            "_content_type": "html" if ".pdf" not in url.lower() else "pdf",
                        })
                
                page_count = int(data.get("PAGE_COUNT", 0))
                print(f"  宁银 第{page+1}页: +{len(records)}条 (共{page_count}页)")
                page += 1
                if page >= page_count:
                    break
            except Exception as e:
                print(f"  宁银 API ERROR: {e}")
                break
    
    return items


async def fetch_ningyin_detail_text(url: str) -> str:
    """抓取宁银详情页正文。"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20) as c:
            r = await c.get(url, headers=HEADERS)
            if r.status_code != 200:
                return ""
            text = r.text
            # 提取纯文本
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:5000]
    except:
        return ""


# ──────────────────────────────────────────────────────────────
# 2. 蒙商消费金融: 重抓详情页全文
# ──────────────────────────────────────────────────────────────
async def fetch_mengshang_detail_text(url: str) -> str:
    """抓取蒙商详情页，提取正文全文。"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20) as c:
            r = await c.get(url, headers=HEADERS)
            if r.status_code != 200:
                return ""
            text = r.text
            # 提取 news-content div
            m = re.search(r'class="news-content"[^>]*>(.*?)</div>\s*<div[^>]*class="news-',
                         text, re.S)
            if m:
                content = m.group(1)
            else:
                content = text
            # 清理HTML
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content).strip()
            return content
    except:
        return ""


# ──────────────────────────────────────────────────────────────
# 3. 晋商消费金融: 已有URL，重抓验证 + 找合作机构PDF
# ──────────────────────────────────────────────────────────────
async def fetch_jinshang_cooperation(url: str) -> list[dict]:
    """晋商: 检查详情页是否有合作机构PDF链接"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20) as c:
            r = await c.get(url, headers=HEADERS)
            if r.status_code != 200:
                return []
            text = r.text
            # 找PDF链接
            pdfs = re.findall(r'href=["\']([^"\']*\.pdf)', text, re.I)
            return [urljoin(url, p) for p in pdfs]
    except:
        return []


# ──────────────────────────────────────────────────────────────
# 4. 通用: 下载PDF并提取文本
# ──────────────────────────────────────────────────────────────
def download_and_extract(pdf_url: str, dest_dir: Path, max_kb: int = 5000) -> tuple[str, str]:
    """下载PDF → 提取文本。返回 (text, dest_path)。"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    fname = pdf_url.split("/")[-1] or f"{hash(pdf_url) % 100000}.pdf"
    dest = dest_dir / fname
    try:
        if dest.exists() and dest.stat().st_size > 1000:
            pass  # already downloaded
        else:
            import urllib.request
            req = urllib.request.Request(pdf_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
                if content[:4] != b'%PDF':
                    return "", ""
                with open(dest, 'wb') as f:
                    f.write(content)
        if dest.stat().st_size > max_kb * 1024:
            return f"[PDF too large: {dest.stat().st_size//1024}KB, skipped]", str(dest)
        result = subprocess.run(['pdftotext', str(dest), '-'],
                               capture_output=True, text=True, timeout=60)
        return result.stdout, str(dest)
    except Exception as e:
        return "", ""


# ──────────────────────────────────────────────────────────────
# 5. 提取合作机构列表（从纯文本）
# ──────────────────────────────────────────────────────────────
def extract_entities_from_text(text: str, dtype_hints: list[str] = None) -> list[dict]:
    """
    从文本中提取公司名+电话对。
    处理格式:
      - 序号 公司名 电话  (如 "1 北京同邦卓益科技有限公司 400-xxx")
      - 公司名 + 下一行电话
    """
    if not text or len(text) < 50:
        return []
    
    # 找含序号的行（序号 机构名 模式）
    lines = text.split('\n')
    entities = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 序号开头
        m = re.match(r'^\d+\s+(.{4,30}(?:公司|集团|中心|事务所))', line)
        if m:
            name = m.group(1).strip()
            phone = ""
            # 同一行或下一行找电话
            rest = line[m.end():].strip()
            phone_m = re.search(r'(\d{3,4}[-\s]?\d{7,8}|400[-\s]?\d{3,4}[-\s]?\d{3,4}|1[3-9]\d{9})', rest)
            if not phone_m and i+1 < len(lines):
                nxt = lines[i+1].strip()
                phone_m = re.search(r'(\d{3,4}[-\s]?\d{7,8}|400[-\s]?\d{3,4}[-\s]?\d{3,4}|1[3-9]\d{9})', nxt)
                if phone_m:
                    i += 1
                    phone = phone_m.group()
            elif phone_m:
                phone = phone_m.group()
            
            # 跳过非机构名
            skip = ['尊敬', '客户', '互联网', '合作机构', '序号', '日期', '附录', '附件', '声明', '公告', '关于', '公司']
            if not any(s in name for s in skip) and len(name) >= 4:
                entities.append({'name': name, 'phone': phone})
        i += 1
    
    # 去重
    seen = set()
    unique = []
    for e in entities:
        if e['name'] not in seen:
            seen.add(e['name'])
            unique.append(e)
    return unique


# ──────────────────────────────────────────────────────────────
# Main: 处理三家
# ──────────────────────────────────────────────────────────────
async def fix_ningyin():
    """修复宁银: 重新采集完整公告列表+详情页全文"""
    print("\n=== 宁银消费金融 ===")
    items = await fetch_ningyin_announcements()
    print(f"  API获取 {len(items)} 条公告")
    
    # 合并现有（2026-04-14旧数据）+ 新数据
    out_dir = RAW_DIR / "2026-04-15" / "宁银消费金融"
    out_dir.mkdir(parents=True, exist_ok=True)
    ann_file = out_dir / "announcements.json"
    
    existing = []
    old_file = RAW_DIR / "2026-04-14" / "宁银消费金融" / "announcements.json"
    if old_file.exists():
        with open(old_file) as f:
            try:
                existing = json.load(f)
            except:
                existing = []
    existing_urls = {a.get('url', '') for a in existing}
    
    new_items = [it for it in items if it['url'] not in existing_urls]
    print(f"  新增 {len(new_items)} 条")
    
    # 抓详情页文本（只对合作机构类）
    coop_keywords = ['合作机构', '助贷', '催收', '担保', '增信', '债权转让']
    for item in new_items:
        if any(k in item['title'] for k in coop_keywords):
            print(f"  抓详情: {item['title'][:40]}")
            item['text'] = await fetch_ningyin_detail_text(item['url'])
            # 提取PDF
            if '.pdf' in item['url'].lower():
                att_dir = out_dir / "attachments"
                text, path = download_and_extract(item['url'], att_dir)
                if text:
                    item['text'] = text
                    print(f"    PDF提取: {len(text)}字符")
        else:
            item['text'] = ""
    
    all_items = existing + new_items
    # 按日期排序
    all_items.sort(key=lambda x: x.get('date', ''), reverse=True)
    with open(ann_file, 'w') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"  已保存 {len(all_items)} 条到 {ann_file}")
    
    # 提取合作机构
    for item in new_items:
        if any(k in item.get('title', '') for k in coop_keywords):
            entities = extract_entities_from_text(item.get('text', ''))
            if entities:
                date_str = item.get('date', '2026-04-01')
                fname = f"宁银消费金融_合作机构_{item['title'][:8]}_{date_str}.json"
                fpath = RAW_DIR / fname
                with open(fpath, 'w') as f:
                    json.dump(entities, f, ensure_ascii=False, indent=2)
                print(f"  提取: {fname} ({len(entities)}家)")
    
    return len(items)


async def fix_mengshang():
    """修复蒙商: 重抓详情页全文"""
    print("\n=== 蒙商消费金融 ===")
    ann_file_14 = RAW_DIR / "2026-04-14" / "蒙商消费金融" / "announcements.json"
    ann_file_15 = RAW_DIR / "2026-04-15" / "蒙商消费金融" / "announcements.json"
    
    announcements = []
    for f in [ann_file_14, ann_file_15]:
        if f.exists():
            try:
                with open(f) as fp:
                    data = json.load(fp)
                    if isinstance(data, list):
                        announcements.extend(data)
            except Exception as e:
                print(f"    加载失败 {f}: {e}")
    
    # 去重（按URL）
    seen_urls = {}
    for a in announcements:
        u = a.get('url', '')
        if u not in seen_urls:
            seen_urls[u] = a
    announcements = list(seen_urls.values())
    announcements.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    coop_keywords = ['合作机构', '催收', '助贷', '担保']
    
    updated = 0
    for a in announcements:
        if any(k in a.get('title', '') for k in coop_keywords):
            # 强制重抓（宁可多抓，不漏数据）
            print(f"  重抓: {a['title'][:50]}")
            text = await fetch_mengshang_detail_text(a['url'])
            if text:
                a['text'] = text
                a['_content_type'] = 'html'
                updated += 1
                entities = extract_entities_from_text(text)
                if entities:
                    date_str = a.get('date', '2026-04-01')
                    fname = f"蒙商消费金融_合作机构_{a['title'][:8]}_{date_str}.json"
                    fpath = RAW_DIR / fname
                    with open(fpath, 'w') as f:
                        json.dump(entities, f, ensure_ascii=False, indent=2)
                    print(f"    提取: {len(entities)}家")
            else:
                print(f"    重抓失败: {a['url']}")
    
    # 保存
    out_dir = RAW_DIR / "2026-04-15" / "蒙商消费金融"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "announcements.json", 'w') as f:
        json.dump(announcements, f, ensure_ascii=False, indent=2)
    print(f"  已更新 {updated} 条，共 {len(announcements)} 条")
    return len(announcements)


async def fix_jinshang():
    """修复晋商: 检查合作机构公告，提取PDF"""
    print("\n=== 晋商消费金融 ===")
    ann_file = RAW_DIR / "2026-04-15" / "晋商消费金融" / "announcements.json"
    
    announcements = []
    if ann_file.exists():
        with open(ann_file) as f:
            announcements = json.load(f)
    if not announcements:
        # 尝试2026-04-14
        ann_file = RAW_DIR / "2026-04-14" / "晋商消费金融" / "announcements.json"
        if ann_file.exists():
            with open(ann_file) as f:
                announcements = json.load(f)
    
    coop_keywords = ['合作机构', '催收', '助贷', '担保', '增信', '公示']
    
    for a in announcements:
        if any(k in a.get('title', '') for k in coop_keywords):
            if '.pdf' in a.get('url', '').lower():
                print(f"  PDF: {a['title'][:50]}")
                att_dir = ann_file.parent / "attachments"
                text, path = download_and_extract(a['url'], att_dir)
                if text and len(text) > 100:
                    entities = extract_entities_from_text(text)
                    if entities:
                        date_str = a.get('date', '2026-01-01')
                        fname = f"晋商消费金融_合作机构_{a['title'][:8]}_{date_str}.json"
                        fpath = RAW_DIR / fname
                        with open(fpath, 'w') as f:
                            json.dump(entities, f, ensure_ascii=False, indent=2)
                        print(f"    提取: {len(entities)}家")
    
    print(f"  晋商共 {len(announcements)} 条公告")
    return len(announcements)


async def main():
    await fix_ningyin()
    await fix_mengshang()
    await fix_jinshang()
    print("\n全部完成!")


if __name__ == "__main__":
    asyncio.run(main())
