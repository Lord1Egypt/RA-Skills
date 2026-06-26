#!/usr/bin/env python3
"""
肯德基 VIP 兑换链接自动化流程（Playwright）：
- 打开 https://vip.woaicoffee.com/?outId=xxx
- 点击「下一步」；若有定位权限弹窗则点击「访问该网站时允许」
- 从当前访问链接中解析 productId，拼接 choose_specifications URL：
  https://vip.woaicoffee.com/kfc/choose_specifications?outId=xxx&productId=393&storeCode=SHA391&sendPhoneMsg=false
- 打开该链接后点击「下单」，弹窗二次确认点击「确认」，等待页面刷新出现取餐码后返回用户
"""
import argparse
import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

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


def parse_out_id(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    out_id = (qs.get("outId") or qs.get("outid") or [""])[0].strip()
    return out_id


def parse_product_id(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    pid = (qs.get("productId") or qs.get("productid") or [""])[0].strip()
    return pid


def build_choose_specifications_url(out_id: str, product_id: str, store_code: str) -> str:
    base = "https://vip.woaicoffee.com/kfc/choose_specifications"
    query = {
        "outId": out_id,
        "productId": product_id,
        "storeCode": store_code,
        "sendPhoneMsg": "false",
    }
    return f"{base}?{urlencode(query)}"


async def main():
    parser = argparse.ArgumentParser(
        description="KFC VIP outId flow: 下一步 -> 允许定位 -> 取 productId -> choose_specifications -> 下单 -> 确认 -> 取餐码"
    )
    parser.add_argument("--url", required=True, help="Original VIP URL (e.g. https://vip.woaicoffee.com/?outId=xxx)")
    parser.add_argument("--store-code", required=True, help="KFC store code (e.g. SHA391)")
    parser.add_argument("--wait-pickup-seconds", type=int, default=60, help="Max seconds to wait for pickup code")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--no-submit",
        action="store_true",
        help="Stop before clicking 确认 in confirm popup",
    )
    args = parser.parse_args()
    args.store_code = args.store_code.strip()

    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = now_tag()

    result = {
        "status": "failed",
        "url": args.url,
        "choose_spec_url": "",
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
            permissions=["geolocation"],
        )
        page = await context.new_page()
        try:
            await page.goto(args.url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)
            result["steps"].append("open_vip_link")

            # 1. 点击「下一步」
            next_btn = await wait_and_click_text(page, ["下一步", "下一步"], timeout_ms=6000)
            if not next_btn:
                result["error"] = "未找到「下一步」按钮"
                result["error_code"] = "ELEMENT_NOT_FOUND"
                result["final_url"] = page.url
                raise ValueError("ELEMENT_NOT_FOUND")
            result["steps"].append("click_next")
            await page.wait_for_timeout(2000)

            # 2. 若有定位弹窗：点击「访问该网站时允许」
            _ = await wait_and_click_text(
                page,
                ["访问该网站时允许", "允许", "确定", "知道了"],
                timeout_ms=3000,
            )
            await page.wait_for_timeout(2000)

            # 3. 从当前访问链接获取 productId（可能需等待跳转）
            current_url = page.url
            product_id = parse_product_id(current_url)
            for _ in range(5):
                if product_id:
                    break
                await page.wait_for_timeout(1500)
                current_url = page.url
                product_id = parse_product_id(current_url)
            if not product_id:
                result["error"] = f"当前链接中未解析到 productId: {current_url}"
                result["error_code"] = "INVALID_URL"
                result["final_url"] = current_url
                raise ValueError("INVALID_URL")
            out_id = parse_out_id(args.url)
            if not out_id:
                out_id = parse_out_id(current_url)
            if not out_id:
                result["error"] = "原始链接中未解析到 outId"
                result["error_code"] = "INVALID_URL"
                result["final_url"] = current_url
                raise ValueError("INVALID_URL")

            choose_url = build_choose_specifications_url(out_id, product_id, args.store_code)
            result["choose_spec_url"] = choose_url
            result["steps"].append("build_choose_spec")

            # 4. 打开 choose_specifications 页
            await page.goto(choose_url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2500)
            result["steps"].append("open_choose_spec")

            shot0 = out_dir / f"kfc_vip_choose_spec_{tag}.png"
            await page.screenshot(path=str(shot0), full_page=True)
            result["screenshots"].append(str(shot0))

            # 5. 点击「下单」
            order_btn = await wait_and_click_text(
                page,
                ["下单", "立即下单", "确认下单", "提交订单"],
                timeout_ms=8000,
            )
            if not order_btn:
                result["error"] = "未找到下单按钮"
                result["error_code"] = "ELEMENT_NOT_FOUND"
                result["final_url"] = page.url
                raise ValueError("ELEMENT_NOT_FOUND")
            result["steps"].append(f"click_order:{order_btn}")
            await page.wait_for_timeout(1500)

            if args.no_submit:
                result["status"] = "stopped_before_submit"
                result["final_url"] = page.url
            else:
                # 6. 二次确认弹窗点击「确认」
                confirm_btn = await wait_and_click_text(
                    page,
                    ["确认", "确定", "提交"],
                    timeout_ms=5000,
                )
                if not confirm_btn:
                    result["error"] = "未找到二次确认弹窗中的「确认」"
                    result["error_code"] = "ELEMENT_NOT_FOUND"
                    result["final_url"] = page.url
                    raise ValueError("ELEMENT_NOT_FOUND")
                result["steps"].append(f"click_confirm:{confirm_btn}")
                await page.wait_for_timeout(2000)

                # 7. 等待页面刷新出现取餐码
                for _ in range(max(1, args.wait_pickup_seconds // 5)):
                    try:
                        text_lower = (await page.inner_text("body")) or ""
                    except Exception:
                        text_lower = ""
                    pickup_match = re.search(r"取餐码[：:\s]*(\d+)", text_lower)
                    order_match = re.search(r"订单号?[：:\s]*([A-Za-z0-9_-]+)", text_lower)
                    if pickup_match:
                        result["pickup_code"] = pickup_match.group(1).strip()
                    if order_match:
                        result["order_no"] = order_match.group(1).strip()
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
                shot1 = out_dir / f"kfc_vip_pickup_{tag}.png"
                await page.screenshot(path=str(shot1), full_page=True)
                result["screenshots"].append(str(shot1))
                if result["status"] != "success":
                    result["status"] = "submitted_wait_pickup"

        except ValueError as e:
            if str(e) not in ("ELEMENT_NOT_FOUND", "INVALID_URL"):
                result["error"] = str(e)
                result["error_code"] = "RESULT_READ_ERROR"
            result["status"] = "failed"
        except Exception as exc:
            result["error"] = str(exc)
            result["status"] = "failed"
            result["error_code"] = "TIMEOUT" if "timeout" in str(exc).lower() else "RESULT_READ_ERROR"
            try:
                result["final_url"] = page.url
                shot_err = out_dir / f"kfc_vip_error_{tag}.png"
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

    result_file = out_dir / f"kfc_vip_choose_spec_result_{tag}.json"
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"result_file: {result_file}")
    return result


if __name__ == "__main__":
    res = asyncio.run(main())
    sys.exit(0 if res.get("status") == "success" else 1)
