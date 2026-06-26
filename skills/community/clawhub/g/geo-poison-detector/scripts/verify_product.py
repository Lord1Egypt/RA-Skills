#!/usr/bin/env python3
"""
GEO Poison Detector — Product Authenticity Verifier
Usage: python3 verify_product.py "<product name>" [--market cn|global|auto]

Generates manual verification links and checklist.
Supports CN (Chinese) and Global (US/EU/international) markets.
No API key required.
"""

import sys
import urllib.parse


def generate_cn_links(product_name: str) -> dict:
    enc = urllib.parse.quote(product_name)
    return {
        "京东搜索":   f"https://search.jd.com/Search?keyword={enc}",
        "淘宝搜索":   f"https://s.taobao.com/search?q={enc}",
        "企查查":     f"https://www.qichacha.com/search?key={enc}",
        "天眼查":     f"https://www.tianyancha.com/cloud-other-information/companySearch.html#keyword={enc}",
        "国家专利局": f"https://pss-system.cponline.cnipa.gov.cn/conventionalSearch?searchWord={enc}",
        "国家标准":   f"https://std.samr.gov.cn/search/gbDetailed?keyword={enc}",
    }


def generate_global_links(product_name: str) -> dict:
    enc = urllib.parse.quote(product_name)
    enc_en = urllib.parse.quote(f"{product_name} review")
    return {
        "Amazon":         f"https://www.amazon.com/s?k={enc}",
        "Google Shopping": f"https://www.google.com/search?q={enc}&tbm=shop",
        "BBB (US)": f"https://www.bbb.org/search?find_text={enc}",
        "Trustpilot":     f"https://www.trustpilot.com/search?query={enc}",
        "USPTO Patents":  f"https://ppubs.uspto.gov/pubwebapp/external.html?q={enc}",
        "EU RAPEX":       f"https://ec.europa.eu/consumers/consumers_safety/safety_products/rapex/alerts/repository/content/pages/rapex/index_en.htm",
        "Reddit Reviews": f"https://www.reddit.com/search/?q={enc_en}",
    }


def detect_market(product_name: str) -> str:
    """Heuristic: if name contains CJK characters, default to CN; else global."""
    has_cjk = any('\u4e00' <= c <= '\u9fff' for c in product_name)
    return "cn" if has_cjk else "global"


def cn_checklist() -> list:
    return [
        "[ ] 品牌在京东/天猫有官方旗舰店（非第三方卖家）",
        "[ ] 产品规格参数与AI描述完全一致",
        "[ ] 企查查/天眼查可查到品牌公司（注册资本、成立时间合理）",
        "[ ] 有真实用户评价（非清一色5星好评，有差评回复）",
        "[ ] 产品有明确执行标准编号（如GB/T XXXXX）",
        "[ ] 宣传的专利可在国家知识产权局查到（有专利号）",
        "[ ] 产品名称无伪科技词汇（量子/黑洞级/石墨烯/纳米等）",
        "[ ] 主要信息来源非纯自媒体（百家号/头条号/微信）",
    ]


def global_checklist() -> list:
    return [
        "[ ] Product sold on Amazon/major retailers (not brand site only)",
        "[ ] Reviews exist on Trustpilot/Reddit/independent sites",
        "[ ] Company registered and verifiable (BBB or Companies House)",
        "[ ] Specific patent numbers are real (check USPTO/EPO)",
        "[ ] FDA/CE claims have certificate numbers (not just logos)",
        "[ ] No 'doctors hate this' / 'one weird trick' language",
        "[ ] Specs are verifiable (model numbers, test standards cited)",
        "[ ] No affiliate-only distribution (available in physical stores)",
    ]


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 verify_product.py \"<product name>\" [--market cn|global|auto]")
        print("Example: python3 verify_product.py \"Dyson V15\" --market global")
        print("Example: python3 verify_product.py \"小米空气净化器\" --market cn")
        sys.exit(1)

    # Parse --market flag
    market = "auto"
    if "--market" in args:
        idx = args.index("--market")
        if idx + 1 < len(args):
            market = args[idx + 1]
            args = args[:idx] + args[idx+2:]

    product_name = " ".join(args).strip('"\'')

    if market == "auto":
        market = detect_market(product_name)

    print(f"\n🔍 产品验证 / Product Verify: {product_name}")
    print(f"🌐 市场 / Market: {'🇨🇳 中国市场 (CN)' if market == 'cn' else '🌍 国际市场 (Global)'}")
    print("=" * 55)

    if market == "cn":
        links = generate_cn_links(product_name)
        checklist = cn_checklist()
        print("\n🔗 验证链接：")
    else:
        links = generate_global_links(product_name)
        checklist = global_checklist()
        print("\n🔗 Verification Links:")

    for label, url in links.items():
        print(f"  {label:<16} {url}")

    print()
    if market == "cn":
        print("✅ 手动核查清单：")
    else:
        print("✅ Manual Verification Checklist:")

    for item in checklist:
        print(f"  {item}")

    print()
    if market == "cn":
        print("💡 提示：同时检查 references/pseudo-tech-terms.md 中的高风险词汇")
    else:
        print("💡 Tip: Also check references/pseudo-tech-terms.md for high-risk buzzwords")
    print()


if __name__ == "__main__":
    main()
