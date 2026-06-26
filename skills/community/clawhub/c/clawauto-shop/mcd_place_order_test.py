#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def now_tag() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


async def wait_and_click_text(page, texts, timeout_ms=2500, do_click=True) -> str:
    for text in texts:
        try:
            loc = page.get_by_text(text, exact=False).first
            await loc.wait_for(timeout=timeout_ms)
            if do_click:
                await loc.click(timeout=timeout_ms)
            return text
        except Exception:
            continue
    return ""


async def wait_and_click_selector(page, selectors, timeout_ms=2500) -> str:
    for selector in selectors:
        try:
            loc = page.locator(selector).first
            await loc.wait_for(timeout=timeout_ms)
            await loc.click(timeout=timeout_ms)
            return selector
        except Exception:
            continue
    return ""


def normalize_eat_type(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    mapping = {
        "外带": "店内自提",
        "自提": "店内自提",
        "堂食": "店内就餐",
    }
    return mapping.get(raw, raw)


async def main():
    parser = argparse.ArgumentParser(description="McDonald's order-link flow tester")
    parser.add_argument("--url", required=True, help="Order link")
    parser.add_argument("--store-keyword", required=True, help="Store keyword")
    parser.add_argument("--store-name", default="", help="Expected store text (optional)")
    parser.add_argument("--eat-type", default="店内就餐", help="Eat type")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--hold-seconds", type=int, default=0, help="Keep browser open for inspection")
    parser.add_argument(
        "--no-submit",
        action="store_true",
        help="Stop at final confirm UI and do not click it",
    )
    args = parser.parse_args()
    args.store_keyword = args.store_keyword.strip()
    args.store_name = args.store_name.strip()
    args.eat_type = normalize_eat_type(args.eat_type)
    if not args.store_keyword:
        print("error: --store-keyword is required", file=sys.stderr)
        return

    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = now_tag()

    result = {
        "status": "failed",
        "url": args.url,
        "final_url": "",
        "store_keyword": args.store_keyword,
        "store_name": args.store_name,
        "eat_type": args.eat_type,
        "store_selected": False,
        "eat_type_selected": False,
        "custom_product_reached": False,
        "final_confirm_visible": False,
        "final_confirm_clicked": False,
        "submitted": False,
        "detail_lines": [],
        "steps": [],
        "error": "",
        "screenshots": [],
    }

    danger_texts = [
        "确认下单",
        "提交订单",
        "立即兑换",
        "确认支付",
        "二次确认",
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=args.headless, slow_mo=250)
        context = await browser.new_context(
            locale="zh-CN",
            viewport={"width": 1366, "height": 900},
            permissions=["geolocation"],
            geolocation={"longitude": 121.4737, "latitude": 31.2304},
        )
        page = await context.new_page()
        try:
            await page.goto(args.url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(1500)
            result["steps"].append("open_link")

            shot0 = out_dir / f"mcd_step0_open_{tag}.png"
            await page.screenshot(path=str(shot0), full_page=True)
            result["screenshots"].append(str(shot0))

            _ = await wait_and_click_text(page, ["我知道了", "知道了", "确认", "关闭"], 1200)

            # Store search input
            store_input = None
            for sel in [
                "input[placeholder*='麦当劳']",
                "input[placeholder*='店名']",
                "input[placeholder*='关键词']",
                "input[type='search']",
                "input[type='text']",
            ]:
                try:
                    loc = page.locator(sel).first
                    await loc.wait_for(timeout=2200)
                    store_input = loc
                    break
                except Exception:
                    continue

            if store_input is not None:
                await store_input.fill(args.store_keyword)
                await store_input.press("Enter")
                result["steps"].append("search_store_input_enter")
            else:
                _ = await wait_and_click_text(page, ["搜索", "门店"], 1200)
                await page.keyboard.type(args.store_keyword)
                await page.keyboard.press("Enter")
                result["steps"].append("search_store_text_enter")

            _ = await wait_and_click_text(page, ["搜索", "去搜索"], 1200)
            await page.wait_for_timeout(1200)

            store_text_candidates = [args.store_keyword]
            if args.store_name:
                store_text_candidates.insert(0, args.store_name)
            store_clicked = await wait_and_click_text(page, store_text_candidates, 5000)
            if store_clicked:
                result["steps"].append(f"select_store:{store_clicked}")
                result["store_selected"] = True
            else:
                store_css = await wait_and_click_selector(
                    page,
                    [
                        f"[class*='store']:has-text('{args.store_keyword}')",
                        f"[class*='restaurant']:has-text('{args.store_keyword}')",
                    ],
                    3000,
                )
                if store_css:
                    result["steps"].append(f"select_store_css:{store_css}")
                    result["store_selected"] = True

            await page.wait_for_timeout(1200)
            shot1 = out_dir / f"mcd_step1_store_{tag}.png"
            await page.screenshot(path=str(shot1), full_page=True)
            result["screenshots"].append(str(shot1))

            # Eat type selection
            eat_candidates = []
            if args.eat_type:
                eat_candidates.append(args.eat_type)
            eat_candidates += ["店内就餐", "店内自提", "车道自提", "打包", "外带"]
            eat_clicked = await wait_and_click_text(page, eat_candidates, 3500)
            if eat_clicked:
                result["steps"].append(f"select_eat_type:{eat_clicked}")
                result["eat_type_selected"] = True

            await page.wait_for_timeout(1200)
            shot2 = out_dir / f"mcd_step2_eat_{tag}.png"
            await page.screenshot(path=str(shot2), full_page=True)
            result["screenshots"].append(str(shot2))

            # Wait for custom product page
            try:
                await page.wait_for_url("**customProduct**", timeout=8000)
                result["custom_product_reached"] = True
                result["steps"].append("enter_custom_product")
            except PlaywrightTimeoutError:
                pass

            if "customProduct" in page.url:
                result["custom_product_reached"] = True
                result["steps"].append("enter_custom_product")

            shot3 = out_dir / f"mcd_step3_custom_{tag}.png"
            await page.screenshot(path=str(shot3), full_page=True)
            result["screenshots"].append(str(shot3))

            # Detect final confirm UI
            for danger in danger_texts:
                try:
                    loc = page.get_by_text(danger, exact=False).first
                    if await loc.count() > 0:
                        result["final_confirm_visible"] = True
                        result["steps"].append(f"danger_visible:{danger}")
                        break
                except Exception:
                    continue

            if args.no_submit:
                result["status"] = "stopped_before_submit"
            else:
                # Safety: do not click final confirm automatically unless explicitly allowed.
                result["status"] = "stopped_before_submit"

            result["final_url"] = page.url

            if args.hold_seconds > 0:
                await page.wait_for_timeout(args.hold_seconds * 1000)
        except Exception as exc:
            result["error"] = str(exc)
            result["status"] = "failed"
        finally:
            try:
                await context.close()
            except Exception:
                pass
            await browser.close()

    result_file = out_dir / f"mcd_order_result_{tag}.json"
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"result_file: {result_file}")


if __name__ == "__main__":
    asyncio.run(main())
