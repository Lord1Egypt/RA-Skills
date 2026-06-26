#!/usr/bin/env python3
"""
verify_logos.py
自动核验下载的公司 Logo 是否与公司匹配

核验逻辑：
1. 图片质量检查（过滤空白/截图/过小图）
2. OCR 文字识别（若已安装 pytesseract）
3. 关键词匹配评分
4. 低分或失败的自动重新搜索

用法：
  python3 verify_logos.py \
    --logos-dir ./logos \
    --companies companies.json \
    [--threshold 0.3] \
    [--retry]
"""

import os
import sys
import json
import re
import argparse
import subprocess
import urllib.request
import urllib.parse
import ssl
import time

# ── 依赖检测 ──────────────────────────────────────────────────
try:
    from PIL import Image
    import numpy as np
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

AGENT_BROWSER = os.environ.get('AGENT_BROWSER', 'agent-browser')  # 可通过环境变量指定路径
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def check_image_quality(img_path):
    """检查图片质量，返回 (ok, reason)"""
    size = os.path.getsize(img_path)
    if size < 1000:
        return False, f"文件过小({size}b)"

    if not PIL_AVAILABLE:
        return True, "PIL不可用，跳过质量检查"

    try:
        img = Image.open(img_path).convert('RGB')
        w, h = img.size

        # 尺寸检查：过小或异常比例
        if w < 30 or h < 30:
            return False, f"图片尺寸过小({w}x{h})"
        if w > 5000 or h > 5000:
            return False, f"图片尺寸过大({w}x{h})，可能是截图页面"

        # 纯色检查：超大图且颜色过于单一 → 可能是截图
        if w > 800 and h > 600:
            import random
            pixels = [img.getpixel((random.randint(0, w-1), random.randint(0, h-1))) for _ in range(100)]
            # 计算颜色方差
            r_vals = [p[0] for p in pixels]
            g_vals = [p[1] for p in pixels]
            b_vals = [p[2] for p in pixels]
            variance = (max(r_vals)-min(r_vals)) + (max(g_vals)-min(g_vals)) + (max(b_vals)-min(b_vals))
            if variance < 50:
                return False, "图片颜色过于单一（可能是空白图）"

        return True, "OK"
    except Exception as e:
        return False, f"图片打开失败: {str(e)[:60]}"


def extract_text_ocr(img_path):
    """OCR 提取图片文字"""
    if not TESSERACT_AVAILABLE or not PIL_AVAILABLE:
        return ""
    try:
        img = Image.open(img_path)
        # 尝试中英文识别
        text = pytesseract.image_to_string(img, lang='chi_sim+eng', config='--psm 11')
        return text.strip()
    except Exception:
        try:
            text = pytesseract.image_to_string(img, lang='eng', config='--psm 11')
            return text.strip()
        except Exception:
            return ""


def compute_match_score(text, company):
    """计算图片文字与公司名的匹配分（0~1）"""
    if not text:
        return 0.0

    text_lower = text.lower()
    score = 0.0

    # 提取中文名的关键词（去掉常见后缀）
    cn_name = company.get('cn', '') or company.get('name', '')
    en_name = company.get('en', '') or ''

    # 中文关键词匹配
    cn_keywords = re.sub(r'(有限公司|股份有限公司|集团|控股|企业|科技|管理|咨询|代理|银行|航空|酒店)', '', cn_name).strip()
    if cn_keywords and len(cn_keywords) >= 2:
        for kw in [cn_keywords, cn_keywords[:2]]:
            if kw in text:
                score = max(score, 0.8)
                break

    # 英文关键词匹配（取前2个单词）
    en_words = [w for w in re.sub(r'[^a-zA-Z0-9 ]', ' ', en_name).split() if len(w) > 2]
    en_words = [w for w in en_words if w.lower() not in ('the','limited','limited','holdings','company','group','management','services','co','ltd','inc','corp')]
    for word in en_words[:2]:
        if word.lower() in text_lower:
            score = max(score, 0.7)
            break

    return score


def verify_company_logo(company, logos_dir, threshold=0.3):
    """核验单个公司的 logo，返回 (ok, score, reason)"""
    logo_file = company.get('file', '')
    if not logo_file:
        return False, 0.0, "无文件名"

    logo_path = os.path.join(logos_dir, logo_file)
    if not os.path.exists(logo_path):
        return False, 0.0, "文件不存在"

    # 1. 质量检查
    quality_ok, quality_reason = check_image_quality(logo_path)
    if not quality_ok:
        return False, 0.0, f"质量检查失败: {quality_reason}"

    # 2. OCR + 匹配
    if TESSERACT_AVAILABLE:
        ocr_text = extract_text_ocr(logo_path)
        score = compute_match_score(ocr_text, company)

        if score >= threshold:
            return True, score, f"OCR匹配({score:.2f})"
        else:
            # 没识别到文字可能是纯图形Logo（很常见），不算失败
            if not ocr_text.strip():
                return True, 0.5, "无文字Logo（图形类）"
            return False, score, f"OCR匹配度低({score:.2f}), 识别文字: {ocr_text[:50]!r}"
    else:
        # 没有 OCR，只做质量检查
        return True, 0.5, "OCR不可用，仅质量检查通过"


def redownload_logo(company, logos_dir):
    """用 agent-browser 重新搜索下载 logo"""
    name = company.get('cn') or company.get('name', '')
    en = company.get('en', '')
    file = company.get('file', '')
    dest = os.path.join(logos_dir, file)

    # 换用不同关键词重试
    queries = [
        f"{name} logo 官方",
        f"{en} logo official",
        f"{name} {en} 品牌标志",
    ]

    env = os.environ.copy()
    env['AGENT_BROWSER_ENGINE'] = 'chrome'

    for query in queries:
        url = f"https://image.baidu.com/search/index?tn=baiduimage&word={urllib.parse.quote(query)}"
        subprocess.run([AGENT_BROWSER, 'open', url], capture_output=True, env=env)
        time.sleep(3)

        js = "JSON.stringify([...document.querySelectorAll('[data-objurl]')].map(e=>e.getAttribute('data-objurl')).filter(u=>u&&u.startsWith('http')).slice(0,8))"
        out = subprocess.run([AGENT_BROWSER, 'eval', js], capture_output=True, text=True, env=env).stdout

        import re
        raw_urls = re.findall(r'https?://[^\\"]+', out)
        urls = [u for u in raw_urls if not u.includes('baidu.com/img/')] if False else raw_urls

        for url in urls[:6]:
            try:
                headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://image.baidu.com/'}
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, context=SSL_CTX, timeout=15) as resp:
                    data = resp.read()
                    if len(data) > 1000:
                        with open(dest, 'wb') as f:
                            f.write(data)
                        return True
            except Exception:
                pass

    return False


def main():
    parser = argparse.ArgumentParser(description='自动核验公司 Logo')
    parser.add_argument('--logos-dir', required=True, help='Logo 目录')
    parser.add_argument('--companies', required=True, help='公司 JSON 文件路径')
    parser.add_argument('--threshold', type=float, default=0.3, help='匹配分阈值（默认0.3）')
    parser.add_argument('--retry', action='store_true', help='核验失败时自动重新下载')
    args = parser.parse_args()

    # 加载公司列表
    with open(args.companies) as f:
        companies = json.load(f)

    if not TESSERACT_AVAILABLE:
        print("⚠️  pytesseract 未安装，仅做图片质量检查（无 OCR 核验）")
        print("   安装方法: pip install pytesseract && brew install tesseract tesseract-lang\n")

    results = {'ok': [], 'failed': [], 'no_logo': []}

    for c in companies:
        name = c.get('cn') or c.get('name', '')
        if not c.get('file'):
            results['no_logo'].append(name)
            continue

        ok, score, reason = verify_company_logo(c, args.logos_dir, args.threshold)
        status = '✅' if ok else '❌'
        print(f"  {status} {name}: {reason}")

        if not ok:
            if args.retry:
                print(f"     → 自动重试...")
                retry_ok = redownload_logo(c, args.logos_dir)
                if retry_ok:
                    ok2, score2, reason2 = verify_company_logo(c, args.logos_dir, args.threshold)
                    if ok2:
                        print(f"     ✅ 重试成功: {reason2}")
                        results['ok'].append(name)
                        continue
                print(f"     ❌ 重试失败")
            results['failed'].append(name)
        else:
            results['ok'].append(name)

    print(f"\n{'='*50}")
    print(f"✅ 核验通过: {len(results['ok'])} 家")
    print(f"❌ 核验失败: {len(results['failed'])} 家 → {', '.join(results['failed'])}")
    print(f"⬜ 无Logo:   {len(results['no_logo'])} 家 → {', '.join(results['no_logo'])}")

    # 保存核验结果
    out_path = os.path.join(args.logos_dir, '_verify_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"结果已保存至: {out_path}")


if __name__ == '__main__':
    main()
