#!/usr/bin/env python3
"""download_homework.py — 从超星学习通下载学生作业HTML（含客观题显示）

前置条件:
1. Chrome 以 --remote-debugging-port=9222 --remote-allow-origins=* 启动
2. 已手动登录超星（或脚本自动登录）

Usage:
    python download_homework.py --config config.json [--login] [--course "数据标注"]

    --login: 打开登录页等待手动登录
    --course: 只下载指定课程（不指定则全下）
    --students: 只下载指定学生（逗号分隔）
"""

import asyncio, websockets, json, time, urllib.request, os, re, sys, html

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    for i, a in enumerate(sys.argv):
        if a == '--config' and i + 1 < len(sys.argv):
            cfg_path = sys.argv[i+1]
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)
    raise FileNotFoundError('config.json not found')

CONFIG = load_config()
LOGIN = CONFIG['login']
DL = CONFIG['download']
CDP_PORT = LOGIN['chrome_port']
CDP_BASE = f'http://127.0.0.1:{CDP_PORT}'
WS_BASE = f'ws://127.0.0.1:{CDP_PORT}'
OUTPUT_DIR = DL['output_dir']
SCRIPT_BASE = LOGIN['script_base']

# Override target students from command line
TARGET_STUDENTS = set(DL.get('target_students', []))
for i, a in enumerate(sys.argv):
    if a == '--students' and i + 1 < len(sys.argv):
        TARGET_STUDENTS = set(s.strip() for s in sys.argv[i+1].split(','))
        break

# ---------- CDP helpers ----------

def cdp_raw(mid, method, params=None):
    return json.dumps({'id': mid, 'method': method, 'params': params or {}})

async def cdp(ws, mid, m, p=None, t=15):
    await ws.send(json.dumps({'id': mid, 'method': m, 'params': p or {}}))
    st = time.monotonic()
    while time.monotonic() - st < t:
        try:
            r = json.loads(await asyncio.wait_for(ws.recv(), 3))
            if r.get('id') == mid:
                return r
        except asyncio.TimeoutError:
            pass
        except json.JSONDecodeError:
            pass
    return None

async def js(ws, expr):
    """Evaluate JS and return value"""
    mid = int(time.time() * 1000) % 100000
    r = await cdp(ws, mid, 'Runtime.evaluate',
                  {'expression': expr, 'returnByValue': True})
    if r:
        return r.get('result', {}).get('result', {}).get('value')
    return None

async def js_void(ws, expr):
    """Evaluate JS that returns nothing"""
    mid = int(time.time() * 1000) % 100000
    await ws.send(json.dumps({'id': mid, 'method': 'Runtime.evaluate',
                              'params': {'expression': expr, 'returnByValue': False}}))

# ---------- Tab management ----------

async def new_tab(url='about:blank'):
    req = urllib.request.Request(f'{CDP_BASE}/json/new?{url}', method='PUT')
    return json.loads(urllib.request.urlopen(req).read())['id']

async def close_tab(tab_id):
    try:
        urllib.request.urlopen(urllib.request.Request(f'{CDP_BASE}/json/close/{tab_id}'))
    except:
        pass

# ---------- Core operations ----------

async def show_objective(ws):
    """勾选显示客观题 + 强制移除 display:none"""
    await js_void(ws, '''(() => {
        const cb = document.getElementById("keguanti");
        if (cb) {
            cb.checked = true;
            cb.dispatchEvent(new Event("change", {bubbles: true}));
            const p = cb.closest(".inputCheck");
            if (p && !p.classList.contains("inputChecked")) p.classList.add("inputChecked");
        }
    })()''')
    await asyncio.sleep(0.3)
    await js_void(ws,
        'document.querySelectorAll(".mark_item1.objective").forEach(d => d.style.display = "")')
    await asyncio.sleep(0.5)

async def get_page_html(ws):
    """获取当前页面完整HTML"""
    r = await js(ws, 'document.documentElement.outerHTML')
    return r or ''

async def download_student_review(main_ws, student_name, data_url, course_name, work_title):
    """在新标签页下载单个学生的批阅页面"""
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', f'{student_name}_{course_name}_{work_title}')
    fpath = os.path.join(OUTPUT_DIR, student_name, f'{safe_name}.html')
    
    if os.path.exists(fpath):
        return 'skip'
    
    tab_id = await new_tab('about:blank')
    try:
        async with websockets.connect(f'{WS_BASE}/devtools/page/{tab_id}', max_size=2**30) as ws:
            await ws.send(cdp_raw(1, 'Page.enable'))
            await ws.send(cdp_raw(2, 'Runtime.enable'))
            await asyncio.sleep(0.2)
            
            full_url = SCRIPT_BASE + data_url
            await ws.send(cdp_raw(3, 'Page.navigate', {'url': full_url}))
            await asyncio.sleep(3)
            
            await show_objective(ws)
            
            page_html = await get_page_html(ws)
            if not page_html:
                return 'fail'
            
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            obj_total = len(re.findall(r'mark_item1 objective', page_html))
            size_kb = len(page_html) // 1024
            print(f'    ✓ {student_name} {size_kb}KB 客观{obj_total}')
            return 'ok'
    except Exception as e:
        print(f'    ✗ {student_name}: {e}')
        return 'fail'
    finally:
        await close_tab(tab_id)

# ---------- Work list processing ----------

async def process_work_list(ws, course_name, courseid, clazzid):
    """处理一个班级的所有作业"""
    list_url = (f'https://mooc2-ans.chaoxing.com/mooc2-ans/work/list'
                f'?courseid={courseid}&clazzid={clazzid}&cpi={LOGIN["cpi"]}')
    
    print(f'\n📋 {course_name} clazzid={clazzid}')
    total = 0
    
    await ws.send(cdp_raw(0, 'Page.navigate', {'url': list_url}))
    await asyncio.sleep(4)
    
    list_page = 1
    while True:
        # Get work titles on current page
        titles = json.loads(await js(ws, '''JSON.stringify(
            [...document.querySelectorAll('a.piyueBtn')]
                .map(b => b.closest('li')?.querySelector('h2')?.innerText?.trim() || '')
        )''') or '[]')
        
        page_label = f'{course_name} 第{list_page}页' if list_page > 1 else course_name
        print(f'  📄 {page_label}: {len(titles)}个作业')
        
        for i, title in enumerate(titles):
            if not title:
                continue
            print(f'\n  [{i+1}/{len(titles)}] {title}')
            
            # Click "批阅" button
            await js(ws, f'document.querySelectorAll("a.piyueBtn")[{i}]?.click()')
            await asyncio.sleep(4)
            
            # Handle student pagination inside the mark page
            student_page = 1
            while True:
                students = json.loads(await js(ws, '''JSON.stringify(
                    [...document.querySelectorAll('[onclick*="toMarkWork"]')]
                        .map(a => {
                            const ul = a.closest('ul');
                            return {
                                name: ul?.querySelector('li.taskBody_name')?.innerText?.trim() || '',
                                data: a.getAttribute('data') || ''
                            };
                        })
                        .filter(s => s.name && s.data)
                )''') or '[]')
                
                for s in students:
                    if TARGET_STUDENTS and s['name'] not in TARGET_STUDENTS:
                        continue
                    
                    result = await download_student_review(
                        ws, s['name'], s['data'], course_name, title)
                    if result == 'ok':
                        total += 1
                
                # Check next page of students
                has_next = await js(ws,
                    'document.querySelector("li.xl-nextPage:not(.xl-disabled)") !== null')
                if not has_next:
                    break
                
                await js(ws, 'document.querySelector("li.xl-nextPage:not(.xl-disabled)")?.click()')
                await asyncio.sleep(3)
                student_page += 1
            
            # Back to work list, maintain current page
            await ws.send(cdp_raw(2, 'Page.navigate', {'url': list_url}))
            await asyncio.sleep(3)
            for _ in range(list_page - 1):
                await js(ws, 'document.querySelector("li.xl-nextPage:not(.xl-disabled)")?.click()')
                await asyncio.sleep(2)
        
        # Next page of work list
        has_next = await js(ws,
            'document.querySelector("li.xl-nextPage:not(.xl-disabled)") !== null')
        if not has_next:
            break
        
        await js(ws, 'document.querySelector("li.xl-nextPage:not(.xl-disabled)")?.click()')
        await asyncio.sleep(3)
        list_page += 1
    
    return total

async def login_auto(ws):
    """自动登录超星"""
    account = LOGIN.get('account', '')
    password = LOGIN.get('password', '')
    if not account or account == 'YOUR_PHONE':
        return False
    
    await cdp(ws, 1, 'Page.navigate', {'url': LOGIN['passport_url']})
    await asyncio.sleep(3)
    
    # Fill login form
    await js(ws, f'document.querySelector("#phone")?.click()')
    await js(ws, f'document.querySelector("#phone")?.value = "{account}"')
    await js(ws, f'document.querySelector("#pwd")?.value = "{password}"')
    await js(ws, 'document.querySelector("#loginBtn")?.click()')
    
    # Wait for redirect
    for _ in range(60):
        url = await js(ws, 'window.location.href')
        if url and 'mooc2-ans' in url and 'passport' not in url:
            return True
        await asyncio.sleep(1)
    return False

async def login_manual(ws):
    """等待用户在浏览器中手动登录"""
    print('\n🔑 请在打开的Chrome窗口中登录超星学习通')
    print(f'   账号: {LOGIN.get("account", "?")}')
    if LOGIN.get('password') and LOGIN['password'] != 'YOUR_PASSWORD':
        print(f'   密码已配置，自动填写中...')
        return await login_auto(ws)
    else:
        print(f'   密码未配置，请手动输入')
        await cdp(ws, 1, 'Page.navigate', {'url': LOGIN['passport_url']})
        await asyncio.sleep(3)
        print('   登录完成后自动继续...')
        for _ in range(180):
            url = await js(ws, 'window.location.href')
            if url and 'mooc2-ans' in url and 'passport' not in url:
                return True
            await asyncio.sleep(1)
        return False

# ---------- Main ----------

async def main():
    need_login = '--login' in sys.argv
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Filter courses
    filter_course = None
    for i, a in enumerate(sys.argv):
        if a == '--course' and i + 1 < len(sys.argv):
            filter_course = sys.argv[i+1]
            break
    
    courses = DL['courses']
    if filter_course:
        courses = [c for c in courses if filter_course.lower() in c['name'].lower()]
        if not courses:
            print(f'No course matching "{filter_course}"')
            return
    
    # Check Chrome CDP
    try:
        info = json.loads(urllib.request.urlopen(f'{CDP_BASE}/json/version').read())
        print(f'✅ Chrome CDP connected: {info.get("Browser", "?")}')
    except:
        print(f'❌ Cannot connect to Chrome CDP at {CDP_BASE}')
        print('   Start Chrome with: --remote-debugging-port=9222 --remote-allow-origins=*')
        return
    
    # Open main tab
    main_id = await new_tab('about:blank')
    try:
        async with websockets.connect(f'{WS_BASE}/devtools/page/{main_id}', max_size=2**30) as ws:
            await ws.send(cdp_raw(1, 'Page.enable'))
            await ws.send(cdp_raw(2, 'Runtime.enable'))
            await asyncio.sleep(0.3)
            
            if need_login:
                logged_in = await login_manual(ws)
                if not logged_in:
                    print('❌ 登录超时或失败')
                    return
                print('✅ 登录成功')
            else:
                # Verify we're logged in
                await cdp(ws, 0, 'Page.navigate', {'url': SCRIPT_BASE})
                await asyncio.sleep(3)
                url = await js(ws, 'window.location.href')
                if not url or 'passport' in (url or ''):
                    print('⚠️ 未登录，使用 --login 参数登录')
                    return
            
            grand_total = 0
            for course in courses:
                name = course['name']
                for cls in course['classes']:
                    total = await process_work_list(
                        ws, f"{name}{cls['name']}",
                        course['courseid'], cls['clazzid'])
                    grand_total += total
            
            print(f'\n{"="*40}')
            print(f'📊 总计下载: {grand_total}份')
            print(f'📁 保存至: {OUTPUT_DIR}')
    finally:
        await close_tab(main_id)

if __name__ == '__main__':
    asyncio.run(main())