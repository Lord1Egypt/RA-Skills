#!/usr/bin/env python3
"""
肯德基 customProduct 自动化流程（Playwright）：
- 打开已转换链接：https://kfc.woaicoffee.cn/index/index/customProduct?cdkey=...&store=...&booking_time=...
- 点击页面最下方红色「确认提交」-> 弹窗点「确认」完成下单
- 等待订单成功页，识别取餐码区域并截图，输出简要信息
"""
import argparse
import asyncio
import json
import re
import sys
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


async def main():
    parser = argparse.ArgumentParser(
        description="KFC customProduct flow: open link -> 确认提交 -> 确认 -> wait pickup"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="customProduct URL (cdkey, store, booking_time)",
    )
    parser.add_argument(
        "--wait-pickup-seconds",
        type=int,
        default=60,
        help="Max seconds to wait for pickup code",
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--no-submit",
        action="store_true",
        help="Stop before clicking 确认 in popup",
    )
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = now_tag()

    result = {
        "status": "failed",
        "url": args.url,
        "final_url": "",
        "steps": [],
        "pickup_code": "",
        "order_no": "",
        "detail_lines": [],
        "screenshots": [],
        "error": "",
        "error_code": "",
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=args.headless, slow_mo=200)
        context = await browser.new_context(
            locale="zh-CN",
            viewport={"width": 1366, "height": 900},
        )
        page = await context.new_page()
        try:
            await page.goto(args.url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)
            result["steps"].append("open_custom_product")

            shot0 = out_dir / f"kfc_cp_step0_{tag}.png"
            await page.screenshot(path=str(shot0), full_page=True)
            result["screenshots"].append(str(shot0))

            # 1. 点击页面最下方红色「确认提交」
            submit_btn = await wait_and_click_text(
                page,
                ["确认提交", "提交订单", "确认下单", "下单"],
                timeout_ms=8000,
            )
            if not submit_btn:
                result["error"] = "未找到「确认提交」按钮"
                result["error_code"] = "ELEMENT_NOT_FOUND"
                result["final_url"] = page.url
                raise ValueError("ELEMENT_NOT_FOUND")
            result["steps"].append(f"click_confirm_submit:{submit_btn}")
            await page.wait_for_timeout(1500)

            if args.no_submit:
                result["status"] = "stopped_before_submit"
                result["final_url"] = page.url
            else:
                # 2. 弹窗点「确认」
                confirm_btn = await wait_and_click_text(
                    page,
                    ["确认", "确定"],
                    timeout_ms=5000,
                )
                if not confirm_btn:
                    result["error"] = "未找到弹窗中「确认」按钮"
                    result["error_code"] = "ELEMENT_NOT_FOUND"
                    result["final_url"] = page.url
                    raise ValueError("ELEMENT_NOT_FOUND")
                result["steps"].append(f"click_confirm:{confirm_btn}")
                await page.wait_for_timeout(2000)

                # 3. 等待订单成功页、取餐码
                for _ in range(max(1, args.wait_pickup_seconds // 5)):
                    try:
                        text_lower = (await page.inner_text("body")) or ""
                    except Exception:
                        text_lower = ""
                    pickup_match = re.search(r"(取餐码|取餐号)\s*[：:\s]*(\d+)", text_lower)
                    order_match = re.search(r"订单号?[：:\s]*([A-Za-z0-9_-]+)", text_lower)
                    if pickup_match:
                        result["pickup_code"] = pickup_match.group(2).strip()
                    if order_match:
                        result["order_no"] = order_match.group(1).strip()  # 订单号
                    if result["pickup_code"] or result["order_no"]:
                        result["status"] = "success"
                        result["detail_lines"] = [
                            f"取餐码: {result['pickup_code']}" if result["pickup_code"] else "",
                            f"订单号: {result['order_no']}" if result["order_no"] else "",
                        ]
                        result["detail_lines"] = [x for x in result["detail_lines"] if x]
                        break
                    await page.wait_for_timeout(5000)

                result["final_url"] = page.url
                shot1 = out_dir / f"kfc_cp_step1_pickup_{tag}.png"
                await page.screenshot(path=str(shot1), full_page=True)
                result["screenshots"].append(str(shot1))
                if result["status"] != "success":
                    result["status"] = "submitted_wait_pickup"

        except ValueError as e:
            if str(e) != "ELEMENT_NOT_FOUND":
                result["error"] = str(e)
                result["error_code"] = "RESULT_READ_ERROR"
            result["status"] = "failed"
        except Exception as exc:
            result["error"] = str(exc)
            result["status"] = "failed"
            result["error_code"] = "TIMEOUT" if "timeout" in str(exc).lower() else "RESULT_READ_ERROR"
            try:
                result["final_url"] = page.url
                shot_err = out_dir / f"kfc_cp_error_{tag}.png"
                await page.screenshot(path=str(shot_err), full_page=True)
                result["screenshots"].append(str(shot_err))
            except Exception:
                pass
        finally:
            try:
                await context.close()
            except Exception:
                pass
            await browser.close()

    result_file = out_dir / f"kfc_custom_product_result_{tag}.json"
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"result_file: {result_file}")
    return result


if __name__ == "__main__":
    res = asyncio.run(main())
    sys.exit(0 if res.get("status") == "success" else 1)
