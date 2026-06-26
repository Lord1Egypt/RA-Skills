#!/usr/bin/env python3
import asyncio
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

TEST_MESSAGE = "Roty Input Roty 3/12 Smith St veg tiffin 6 rotis normal Mon-Fri extra rice no onion"

LOGS = []

def log(msg):
    print(msg)
    LOGS.append(msg)

async def run():
    log('Starting real-browser dry-run')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        log('Launched Chromium (headless)')
        context = await browser.new_context()
        page = await context.new_page()
        url = 'https://app.bitely.com.au/order/roty/qfiDIvUSocQFrVPzM4zQ'
        log(f'Navigating to {url}')
        try:
            resp = await page.goto(url, wait_until='networkidle', timeout=30000)
            log(f'Navigation response: {resp.status} {resp.url}')
        except PlaywrightTimeoutError:
            log('Navigation timeout or networkidle not reached; proceeding')

        # 1. Select tiffin type (veg tiffin)
        try:
            # Try to find by text
            locator = page.locator("text=/veg\\s*tiffin/i")
            cnt = await locator.count()
            if cnt > 0:
                await locator.first.click()
                log(f'Clicked veg tiffin via text locator (text=/veg\\s*tiffin/i)')
            else:
                # try buttons with veg
                locator2 = page.locator("button:has-text('Veg')")
                if await locator2.count() > 0:
                    await locator2.first.click()
                    log("Clicked veg button: button:has-text('Veg')")
                else:
                    log('Could not find veg tiffin selector by text; please provide selector')
                    await browser.close()
                    return
        except Exception as e:
            log(f'Error selecting tiffin type: {e}')
            await browser.close()
            return

        # 2. Handle address if prompted: try to find an input with placeholder or name address
        address_to_type = '3/12 Smith St, Melbourne VIC 3000'
        try:
            addr_selectors = ["input[placeholder*='Address']", "input[name*='address']", "input[id*='address']", "input[aria-label*='address']"]
            found = False
            for sel in addr_selectors:
                elements = await page.locator(sel).all()
                if len(elements) > 0:
                    await page.fill(sel, '3/12 Smith St Melbourne')
                    log(f'Filled address input {sel} with "3/12 Smith St Melbourne"')
                    # wait for dropdown
                    await page.wait_for_timeout(1000)
                    # try selecting first autocomplete item
                    dd = page.locator('text=/\d+\/?\d*\s+Smith St/i')
                    if await dd.count() > 0:
                        await dd.first.click()
                        log('Selected autocomplete candidate matching Smith St via text locator')
                    else:
                        log('No autocomplete candidate matched; left typed address')
                    found = True
                    break
            if not found:
                log('No address input found on page (no selector matched)')
        except Exception as e:
            log(f'Error handling address: {e}')

        # 3. Select dates Mon-Fri 2026-03-09 .. 2026-03-13
        dates = ['2026-03-09','2026-03-10','2026-03-11','2026-03-12','2026-03-13']
        for d in dates:
            sel = f"[data-date='{d}']"
            try:
                if await page.locator(sel).count() > 0:
                    # single click
                    await page.locator(sel).first.click()
                    log(f'Clicked calendar cell {sel} for date {d}')
                else:
                    # try text match
                    txt = d.split('-')[2].lstrip('0')
                    alt = page.locator(f"text=^\\s*{txt}\\s*$")
                    if await alt.count() > 0:
                        await alt.first.click()
                        log(f'Clicked calendar cell by day text for {d} (day {txt})')
                    else:
                        log(f'Could not find calendar selector for date {d}; paused')
                        await browser.close()
                        return
            except Exception as e:
                log(f'Error selecting date {d}: {e}')
                await browser.close()
                return

        # 4. Select modifier1 (6 rotis)
        try:
            m1 = page.locator("text=/6\\s*rotis/i")
            if await m1.count() > 0:
                await m1.first.click()
                log('Clicked modifier1: 6 rotis (text=/6\\s*rotis/i)')
            else:
                log('Modifier1 "6 rotis" not found by text')
        except Exception as e:
            log(f'Error selecting modifier1: {e}')

        # 5. Select modifier2 (extra rice)
        try:
            m2 = page.locator("text=/extra\\s*rice/i")
            if await m2.count() > 0:
                await m2.first.click()
                log('Clicked modifier2: Extra Rice (text=/extra\\s*rice/i)')
            else:
                log('Modifier2 "extra rice" not found by text; will add to notes')
        except Exception as e:
            log(f'Error selecting modifier2: {e}')

        # 6. Add special requests
        try:
            notes_selectors = ["textarea[placeholder*='note']", "textarea[name*='note']", "textarea[id*='note']", "textarea[aria-label*='note']", "textarea"]
            filled = False
            for sel in notes_selectors:
                if await page.locator(sel).count() > 0:
                    await page.fill(sel, 'no onion')
                    log(f'Filled notes field {sel} with "no onion"')
                    filled = True
                    break
            if not filled:
                log('No notes textarea found; skipping notes fill')
        except Exception as e:
            log(f'Error filling notes: {e}')

        # 7. Add to cart
        try:
            add_sel_candidates = ["button:has-text('Add to cart')", "button:has-text('Add to Cart')", "button[aria-label*='add']", "button:has-text('Add')"]
            clicked = False
            for sel in add_sel_candidates:
                if await page.locator(sel).count() > 0:
                    await page.locator(sel).first.click()
                    log(f'Clicked add-to-cart via selector: {sel}')
                    clicked = True
                    break
            if not clicked:
                log('Add to cart button not found; paused')
                await browser.close()
                return
        except Exception as e:
            log(f'Error clicking add to cart: {e}')
            await browser.close()
            return

        # 8. Go to checkout
        try:
            checkout_sel = "button:has-text('Checkout')"
            if await page.locator(checkout_sel).count() > 0:
                await page.locator(checkout_sel).first.click()
                log(f'Clicked Checkout via selector: {checkout_sel}')
            else:
                cart_sel = "a:has-text('View cart')"
                if await page.locator(cart_sel).count() > 0:
                    await page.locator(cart_sel).first.click()
                    log(f'Clicked View cart via selector: {cart_sel}')
                    # then click proceed
                    proceed = "button:has-text('Proceed')"
                    if await page.locator(proceed).count() > 0:
                        await page.locator(proceed).first.click()
                        log(f'Clicked Proceed via selector: {proceed}')
                    else:
                        log('Proceed button not found after View cart; continuing')
                else:
                    log('Neither Checkout nor View cart found; continuing')
        except Exception as e:
            log(f'Error during checkout navigation: {e}')

        # 9. Login if prompted
        try:
            # detect login form
            email_sel = "input[type='email']"
            pass_sel = "input[type='password']"
            if await page.locator(email_sel).count() > 0 and await page.locator(pass_sel).count() > 0:
                await page.fill(email_sel, 'samwisethebot@gmail.com')
                await page.fill(pass_sel, 'Samwisethebot')
                log(f'Filled login email and password via selectors {email_sel} and {pass_sel}')
                # attempt to click login
                login_btn = "button:has-text('Login')"
                if await page.locator(login_btn).count() > 0:
                    await page.locator(login_btn).first.click()
                    log(f'Clicked login button: {login_btn}')
                else:
                    log('Login button not found; submitted credentials in form fields')
        except Exception as e:
            log(f'Error during login handling: {e}')

        # 10. In checkout: set name, phone, address
        try:
            name_sel = "input[name='name']"
            phone_sel = "input[name='phone']"
            addr_sel = "input[name='address']"
            if await page.locator(name_sel).count() > 0:
                await page.fill(name_sel, 'Roty')
                log(f'Filled name via {name_sel} with Roty')
            else:
                log('Name input selector not found (name_sel)')
            if await page.locator(phone_sel).count() > 0:
                await page.fill(phone_sel, '0412345678')
                log(f'Filled phone via {phone_sel} with 0412345678')
            else:
                log('Phone input selector not found; attempted other common selectors')
                alt_phone = page.locator("input[placeholder*='Phone']")
                if await alt_phone.count() > 0:
                    await alt_phone.first.fill('0412345678')
                    log('Filled phone via placeholder selector')
            if await page.locator(addr_sel).count() > 0:
                await page.fill(addr_sel, '3/12 Smith St, Melbourne VIC 3000')
                log(f'Filled address via {addr_sel} with canonical address')
            else:
                log('Checkout address input not found; skipped')
        except Exception as e:
            log(f'Error filling checkout fields: {e}')

        # 11. Select bank transfer
        try:
            bank_sel = page.locator("text=/bank transfer/i")
            if await bank_sel.count() > 0:
                await bank_sel.first.click()
                log('Selected payment method: Bank transfer (text=/bank transfer/i)')
            else:
                log('Bank transfer option not found by text')
        except Exception as e:
            log(f'Error selecting bank transfer: {e}')

        # STOP before confirm
        log('Reached final confirmation — Would click confirm here — STOP (safe dry-run). No order placed.')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
