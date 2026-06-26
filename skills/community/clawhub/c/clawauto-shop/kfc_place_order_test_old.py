#!/usr/bin/env python3
import argparse
import asyncio
import json
import re
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


async def wait_any_text(page, texts, timeout_ms=2500) -> str:
    for text in texts:
        try:
            await page.get_by_text(text, exact=False).first.wait_for(timeout=timeout_ms)
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


async def click_last_confirm_button(page) -> bool:
    try:
        loc = page.get_by_text("确认", exact=True)
        count = await loc.count()
        if count <= 0:
            return False
        # In this page there are multiple "确认". The modal's confirm button is usually the last visible one.
        await loc.nth(count - 1).click(timeout=2500, force=True)
        return True
    except Exception:
        return False


async def main():
    parser = argparse.ArgumentParser(description="KFC order-link flow tester")
    parser.add_argument("--url", required=True, help="Order link")
    parser.add_argument("--store-keyword", required=True, help="Store keyword")
    parser.add_argument("--store-name", default="", help="Expected store text (optional)")
    parser.add_argument("--pickup-type", default="外带", help="Pickup type")
    parser.add_argument("--pickup-time", default="", help="Pickup time; empty means immediate pickup")
    parser.add_argument("--city", required=True, help="City text")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--hold-seconds", type=int, default=0, help="Keep browser open for inspection")
    parser.add_argument("--wait-taskslist-seconds", type=int, default=90, help="Wait timeout after final confirm")
    parser.add_argument(
        "--no-submit",
        action="store_true",
        help="Stop at final modal confirm button and do not click it",
    )
    args = parser.parse_args()
    args.city = args.city.strip()
    args.store_keyword = args.store_keyword.strip()
    args.store_name = args.store_name.strip()
    args.pickup_time = args.pickup_time.strip()
    if not args.city or not args.store_keyword:
        print("error: --city and --store-keyword are required", file=sys.stderr)
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
        "pickup_type": args.pickup_type,
        "pickup_time": args.pickup_time,
        "city": args.city,
        "food_confirm_page_reached": False,
        "final_confirm_visible": False,
        "final_confirm_clicked": False,
        "tasks_list_reached": False,
        "submitted": False,
        "pickup_code": "",
        "order_no": "",
        "success_markers": [],
        "detail_lines": [],
        "steps": [],
        "error": "",
        "error_code": "",
        "screenshots": [],
    }

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

            shot0 = out_dir / f"kfc_step0_open_{tag}.png"
            await page.screenshot(path=str(shot0), full_page=True)
            result["screenshots"].append(str(shot0))

            _ = await wait_and_click_text(page, ["我知道了", "知道了", "确认", "关闭", "开始点餐"], 1200)

            if "citySelect" in page.url:
                city_clicked = await wait_and_click_text(page, [args.city, "上海市"], 4500)
                if city_clicked:
                    result["steps"].append(f"select_city:{city_clicked}")
                    await page.wait_for_timeout(1200)

            # Store search
            store_input = None
            for sel in [
                "input[placeholder*='搜索']",
                "input[placeholder*='门店']",
                "input[type='search']",
                "input[type='text']",
            ]:
                try:
                    loc = page.locator(sel).first
                    await loc.wait_for(timeout=1800)
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

            _ = await wait_and_click_text(page, ["去搜索", "搜索"], 1200)
            await page.wait_for_timeout(1200)

            store_text_candidates = [args.store_keyword]
            if args.store_name:
                store_text_candidates.insert(0, args.store_name)
            store_clicked = await wait_and_click_text(page, store_text_candidates, 5000)
            if not store_clicked:
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
            else:
                result["steps"].append(f"select_store:{store_clicked}")

            await page.wait_for_timeout(1500)
            shot1 = out_dir / f"kfc_step1_store_{tag}.png"
            await page.screenshot(path=str(shot1), full_page=True)
            result["screenshots"].append(str(shot1))

            # Enter ordering flow
            mid = await wait_and_click_text(page, ["去点餐", "预约点餐", "立即点餐"], 3500)
            if mid:
                result["steps"].append(f"enter_order_flow:{mid}")
                await page.wait_for_timeout(1500)

            # Step A: time page confirm
            _ = await wait_and_click_text(page, [args.pickup_type, "外带", "自取", "到店自取"], 2200)
            pickup_time = args.pickup_time.strip()
            if pickup_time:
                times = [pickup_time]
                if ":" in pickup_time and not pickup_time.startswith("0"):
                    times.append("0" + pickup_time)
                if ":" in pickup_time and pickup_time.startswith("0"):
                    times.append(pickup_time[1:])
                picked_time = await wait_and_click_text(page, times, 3500)
                if picked_time:
                    result["steps"].append(f"pickup_time:{picked_time}")
            else:
                instant = await wait_and_click_text(
                    page,
                    ["立即取餐", "尽快取餐", "马上取餐", "实时取餐", "现在取餐"],
                    3000,
                )
                if instant:
                    result["steps"].append(f"pickup_time_immediate:{instant}")

            time_confirm = await wait_and_click_text(page, ["确认", "下一步", "确认时间"], 3500)
            if time_confirm:
                result["steps"].append(f"time_confirm:{time_confirm}")
                await page.wait_for_timeout(1600)

            # Step B: food confirm page
            food_marker = await wait_any_text(page, ["餐品确认", "确认餐品", "确认提交", "提交订单"], 3500)
            if food_marker:
                result["food_confirm_page_reached"] = True
                result["steps"].append(f"food_confirm_page_marker:{food_marker}")

            food_pickup = await wait_and_click_text(page, [args.pickup_type, "外带", "自取", "到店自取"], 2600)
            if food_pickup:
                result["steps"].append(f"food_page_pickup:{food_pickup}")

            shot2 = out_dir / f"kfc_step2_food_confirm_{tag}.png"
            await page.screenshot(path=str(shot2), full_page=True)
            result["screenshots"].append(str(shot2))

            submit_entry = await wait_and_click_text(page, ["确认提交", "提交订单", "确认下单"], 5000)
            if submit_entry:
                result["steps"].append(f"submit_entry_clicked:{submit_entry}")
                await page.wait_for_timeout(1200)
            else:
                result["steps"].append("submit_entry_not_found")

            # Step C: final modal confirm
            final_confirm = await wait_and_click_text(
                page,
                ["确认", "确认提交", "确定"],
                5000,
                do_click=not args.no_submit,
            )
            if not final_confirm and not args.no_submit:
                if await click_last_confirm_button(page):
                    final_confirm = "确认(兜底:last)"
            if final_confirm:
                result["final_confirm_visible"] = True
                result["steps"].append(f"final_confirm_visible:{final_confirm}")
                if args.no_submit:
                    result["steps"].append("final_confirm_skipped")
                else:
                    result["final_confirm_clicked"] = True
                    result["submitted"] = True
                    result["steps"].append("final_confirm_clicked")
                    await page.wait_for_timeout(2500)

                    # Wait until tasks list page appears; keep refreshing if needed.
                    deadline = time.monotonic() + max(5, args.wait_taskslist_seconds)
                    refresh_round = 0
                    while time.monotonic() < deadline:
                        if "tasksList" in page.url:
                            result["tasks_list_reached"] = True
                            result["steps"].append("tasks_list_reached")
                            break
                        await page.wait_for_timeout(1800)
                        refresh_round += 1
                        try:
                            await page.reload(wait_until="domcontentloaded", timeout=15000)
                            result["steps"].append(f"refresh_after_submit:{refresh_round}")
                        except Exception:
                            # Keep waiting even if one refresh attempt fails.
                            pass
            else:
                result["steps"].append("final_confirm_not_found")

            result["final_url"] = page.url
            if "tasksList" in result["final_url"]:
                result["tasks_list_reached"] = True
                if "tasks_list_reached" not in result["steps"]:
                    result["steps"].append("tasks_list_reached(final_url)")
            body = await page.inner_text("body")
            markers = ["下单成功", "取餐码", "取餐号", "订单号", "订单详情"]
            result["success_markers"] = [m for m in markers if m in body]
            match = re.search(r"(取餐码|取餐号)\s*[:：]?\s*([A-Za-z0-9]{3,12})", body)
            if match:
                result["pickup_code"] = match.group(2)
            order_match = re.search(r"(订单号)\s*[:：]?\s*([A-Za-z0-9\-]{4,30})", body)
            if order_match:
                result["order_no"] = order_match.group(2)

            # Extract concise detail lines for chat report.
            lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
            key_words = ("取餐", "订单", "门店", "时间", "外带", "金额", "餐品", "成功")
            picked = []
            for ln in lines:
                if any(k in ln for k in key_words):
                    picked.append(ln)
                if len(picked) >= 12:
                    break
            result["detail_lines"] = picked

            shot3 = out_dir / f"kfc_step3_final_{tag}.png"
            await page.screenshot(path=str(shot3), full_page=True)
            result["screenshots"].append(str(shot3))

            if args.hold_seconds > 0:
                result["steps"].append(f"hold_for_inspection:{args.hold_seconds}s")
                await page.wait_for_timeout(args.hold_seconds * 1000)

            if args.no_submit:
                if result["final_confirm_visible"]:
                    result["status"] = "success"
                elif result["food_confirm_page_reached"]:
                    result["status"] = "partial_success"
                else:
                    result["status"] = "failed"
            else:
                if result["tasks_list_reached"]:
                    result["status"] = "success"
                elif result["submitted"] and ("下单成功" in result["success_markers"] or result["pickup_code"]):
                    result["status"] = "success"
                elif result["submitted"]:
                    result["status"] = "partial_success"
                else:
                    result["status"] = "failed"

        except PlaywrightTimeoutError as exc:
            result["error"] = f"timeout: {exc}"
        except Exception as exc:
            result["error"] = str(exc)
            result["error_code"] = "TIMEOUT" if "timeout" in str(exc).lower() else "RESULT_READ_ERROR"
        finally:
            out = out_dir / f"kfc_order_test_result_{tag}.json"
            out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            await context.close()
            await browser.close()
            try:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except Exception:
                print(json.dumps(result, ensure_ascii=True, indent=2))
            print(f"result_file: {out}")


if __name__ == "__main__":
    asyncio.run(main())
