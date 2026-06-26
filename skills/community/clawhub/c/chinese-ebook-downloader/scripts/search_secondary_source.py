#!/usr/bin/env python3
"""
Search secondary online book source for a Chinese ebook and extract file host download link + password.
Usage: python search_secondary_source.py "书名" ["作者"]
"""
import sys
import os
import re
import json
import asyncio
from typing import Optional, List
from urllib.parse import quote, urljoin

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Install playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

SOURCE_B_BASE_URL = os.environ.get("SOURCE_B_BASE_URL", "https://yabook.org")
FILE_HOST_BASE_URL = os.environ.get("FILE_HOST_BASE_URL", "https://z701.com")


async def search_yabook(title: str, author: str = "", headless: bool = True, browser=None) -> List[dict]:
    """Search secondary book source and return results with file host links."""
    query = f"{title} {author}".strip()
    results = []
    _owns_browser = browser is None
    if _owns_browser:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=headless)
    page = await browser.new_page()

    try:
        search_url = f"{SOURCE_B_BASE_URL}/?s={quote(query)}"
        print(f"Searching secondary source for: {query}")
        await page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(2)

        items = await page.query_selector_all('article .entry-title a')
        
        if not items:
            items = await page.query_selector_all('.excerpt a[title]')
        
        if not items:
            print("No search results found")
            return []

        for item in items[:5]:
            try:
                item_title = (await item.inner_text()).strip()
                item_href = await item.get_attribute('href')
                
                if not item_href:
                    continue
                
                full_url = urljoin(SOURCE_B_BASE_URL, item_href)
                
                print(f"  Checking: {item_title[:40]}...")
                await page.goto(full_url, wait_until='domcontentloaded', timeout=20000)
                await asyncio.sleep(2)

                file_link = await _extract_file_host_link(page)
                password = await _extract_password(page)
                
                if file_link:
                    print(f"  Found file host link + password: {password}")
                    results.append({
                        "title": item_title,
                        "url": full_url,
                        "ctfile_url": file_link,
                        "password": password
                    })
                    break
            except Exception as e:
                print(f"  Error: {e}")
                continue
    finally:
        await page.close()
        if _owns_browser:
            await browser.close()
            await p.stop()
    
    return results


async def _extract_file_host_link(page) -> Optional[str]:
    """Extract file host download link from page."""
    # Method 1: Direct link in page
    links = await page.query_selector_all('a[href*="ctfile.com"]')
    for link in links:
        href = await link.get_attribute('href')
        if href and '/f/' in href:
            return href
    
    # Method 2: In /go/ redirect links
    links = await page.query_selector_all('a[href*="/go/"]')
    for link in links:
        href = await link.get_attribute('href')
        if href:
            # Click to follow redirect
            try:
                resp = await link.evaluate('el => fetch(el.href).then(r => r.url)', link)
                if 'ctfile.com' in resp:
                    return resp
            except:
                pass
    
    return None


async def _extract_password(page) -> str:
    """Extract download password from page."""
    text = await (await page.query_selector('article') or await page.query_selector('main') or await page.query_selector('body')).inner_text()
    
    # Look for password pattern
    match = re.search(r'密码[：:]\s*(\d{4,8})', text)
    if match:
        return match.group(1)
    
    # Look for extraction code pattern
    match = re.search(r'提取码[：:]\s*(\w{4,6})', text)
    if match:
        return match.group(1)
    
    # Common default passwords (from env or fallback)
    default_pwd = os.environ.get("EBOOK_DEFAULT_PASSWORD", "")
    for pwd in ['202630', default_pwd, '1234', 'abcd']:
        if pwd in text:
            return pwd
    
    return ""


async def decrypt_ctfile(ctfile_url: str, password: str, headless: bool = True, browser=None) -> Optional[dict]:
    """Decrypt file host link and get download API variables."""
    _owns_browser = browser is None
    if _owns_browser:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=headless)
    page = await browser.new_page()

    try:
        print(f"Decrypting file host link: {ctfile_url[:50]}...")
        await page.goto(ctfile_url, wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(3)
        
        body_text = await (await page.query_selector('body')).inner_text()
        
        if '输入文件' in body_text or '访问密码' in body_text:
            input_box = await page.query_selector('input[type="text"], input[type="password"]')
            if input_box and password:
                await input_box.type(password, delay=50)
                btn = await page.query_selector('button:has-text("解密")')
                if not btn:
                    btn = await page.query_selector('input[type="submit"]')
                if btn:
                    await btn.click()
                    await asyncio.sleep(5)
        
        try:
            result = await page.evaluate("""() => {
                return JSON.stringify({
                    api_server: typeof api_server !== 'undefined' ? api_server : null,
                    userid: typeof userid !== 'undefined' ? userid : null,
                    file_id: typeof file_id !== 'undefined' ? file_id : null,
                    share_id: typeof share_id !== 'undefined' ? share_id : '',
                    file_chk: typeof file_chk !== 'undefined' ? file_chk : null,
                    start_time: typeof start_time !== 'undefined' ? start_time : null,
                    wait_seconds: typeof wait_seconds !== 'undefined' ? wait_seconds : 0,
                    verifycode: typeof verifycode !== 'undefined' ? verifycode : null
                });
            }""")
            data = json.loads(result)
            
            if data.get('api_server') and data.get('file_id'):
                print(f"  Got API variables (file_id: {data['file_id']})")
                return data
            else:
                print("  Could not extract API variables")
                return None
        except Exception as e:
            print(f"  Error extracting variables: {e}")
            return None
    finally:
        await page.close()
        if _owns_browser:
            await browser.close()
            await p.stop()


async def get_download_url(api_vars: dict, browser=None) -> Optional[str]:
    """Call file host API to get real download URL."""
    _owns_browser = browser is None
    if _owns_browser:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    try:
        ct_url = f"{FILE_HOST_BASE_URL}/f/{api_vars['userid']}-{api_vars['file_id']}"
        await page.goto(ct_url, wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(2)
        
        try:
            js_code = f"""(async () => {{
                try {{
                    var url = '{api_vars['api_server']}/get_file_url.php'
                        + '?uid={api_vars["userid"]}'
                        + '&fid={api_vars["file_id"]}'
                        + '&folder_id=0'
                        + '&share_id={api_vars.get("share_id", "")}'
                        + '&file_chk={api_vars["file_chk"]}'
                        + '&start_time={api_vars["start_time"]}'
                        + '&wait_seconds={api_vars.get("wait_seconds", 0)}'
                        + '&mb=0&app=0&acheck=0'
                        + '&verifycode={api_vars["verifycode"]}'
                        + '&rd=' + Math.random();
                    var headers = typeof getAjaxHeaders === 'function' ? getAjaxHeaders() : {{}};
                    var resp = await fetch(url, {{headers: headers}});
                    var data = await resp.json();
                    return JSON.stringify(data);
                }} catch(e) {{ return JSON.stringify({{error: e.message}}); }}
            }})()"""
            
            result = await page.evaluate(js_code)
            data = json.loads(result)
            
            if data.get('code') == 200 and data.get('downurl'):
                print(f"  Got download URL ({data.get('file_size', 0)} bytes)")
                return data['downurl']
            else:
                print(f"  API error: {data}")
                return None
        except Exception as e:
            print(f"  Error: {e}")
            return None
    finally:
        await page.close()
        if _owns_browser:
            await browser.close()
            await p.stop()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python search_secondary_source.py "书名" ["作者"]')
        sys.exit(1)
    
    title = sys.argv[1]
    author = sys.argv[2] if len(sys.argv) > 2 else ""
    
    results = asyncio.run(search_yabook(title, author))
    
    if results:
        print(f"\nFound {len(results)} result(s):")
        for i, r in enumerate(results):
            print(f"  [{i+1}] {r['title']}")
            print(f"      URL: {r['ctfile_url']}")
            print(f"      Password: {r['password']}")
    else:
        print("\nNo results found")
