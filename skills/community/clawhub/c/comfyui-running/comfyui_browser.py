#!/usr/bin/env python3
"""
ComfyUI 全自动运行脚本 - 修复版 v2

关键修复（2026-03-29）：
1. graphToPrompt() 返回空{} → 用 REST API /prompt 代替 Ctrl+Enter
2. UI 批次字段不控制 KSampler batch_size → 用 number=1 API 调用控制批次数
3. number=N 多次执行会共享文件名 → 改用 N 次 number=1 调用
4. Ctrl+Enter 可能添加陈旧队列条目 → 先清空队列再运行

用法:
    python3 comfyui_browser.py <TAB_ID> <action> [arg]

示例:
    # 完整流程：加载 → 设批次 → 运行
    python3 comfyui_browser.py <TAB_ID> run_workflow "fireredimage" 2

    # 单独步骤
    python3 comfyui_browser.py <TAB_ID> click_workflow "fireredimage"
    python3 comfyui_browser.py <TAB_ID> set_batch 2
    python3 comfyui_browser.py <TAB_ID> api_run 2
"""
import json, asyncio, websockets, base64, sys, urllib.request, os, time, random

# 清除所有代理环境变量
for k in list(os.environ.keys()):
    if 'proxy' in k.lower():
        del os.environ[k]

# 添加 lib 目录到 path
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(os.path.join(_SCRIPT_DIR, "lib")):
    sys.path.insert(0, os.path.join(_SCRIPT_DIR, "lib"))

from comfyui_config import get_comfyui_root, get_workflows_dir, get_cdp_port, get_comfyui_port

DEBUG_PORT = get_cdp_port()
COMFYUI_PORT = get_comfyui_port()


# ============ CDP 核心函数 ============

async def cdp(ws, method, params=None):
    nid = [0]
    async def send():
        nid[0] += 1
        await ws.send(json.dumps({"id": nid[0], "method": method, "params": params or {}}))
        return nid[0]
    async def recv(wait_id):
        while True:
            msg = await ws.recv()
            obj = json.loads(msg)
            if obj.get("id") == wait_id:
                return obj
    sid = await send()
    return await recv(sid)


def find_comfyui_tab(debug_port=DEBUG_PORT):
    try:
        url = f"http://127.0.0.1:{debug_port}/json"
        tabs = json.loads(urllib.request.urlopen(url, timeout=5).read())
        for t in tabs:
            if "127.0.0.1:8188" in t.get("url", "") and t.get("type") == "page":
                return t
    except Exception as e:
        print(f"Error finding tab: {e}", file=sys.stderr)
    return None


def get_all_tabs(debug_port=DEBUG_PORT):
    try:
        url = f"http://127.0.0.1:{debug_port}/json"
        return json.loads(urllib.request.urlopen(url, timeout=5).read())
    except:
        return []


def get_ws_url(tab_id, debug_port=DEBUG_PORT):
    return f"ws://127.0.0.1:{debug_port}/devtools/page/{tab_id}"


async def ws_connect_with_retry(ws_url, max_retries=3, delay=1.0):
    """WebSocket连接，带重试（处理瞬时500错误）"""
    last_err = None
    for attempt in range(max_retries):
        try:
            ws = await websockets.connect(ws_url, ping_interval=None, open_timeout=10)
            return ws
        except Exception as e:
            last_err = e
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (attempt + 1))
    raise last_err


async def screenshot(ws, path):
    result = await cdp(ws, "Page.captureScreenshot", {"format": "png"})
    if "result" in result and "data" in result["result"]:
        with open(path, "wb") as f:
            f.write(base64.b64decode(result["result"]["data"]))
        return True
    return False


async def press_key(ws, key):
    """发送按键（Enter=确认, Escape=关闭, w=打开侧边栏等）"""
    modifiers = 2 if key in ("Ctrl+Enter", "Control+Enter") else 0
    actual_key = {"Ctrl+Enter": "Enter", "Control+Enter": "Enter"}.get(key, key)
    code = f"Key{actual_key.upper()}" if len(actual_key) == 1 else actual_key

    await cdp(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "modifiers": modifiers, "key": actual_key, "code": code})
    await asyncio.sleep(0.05)
    await cdp(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "modifiers": modifiers, "key": actual_key, "code": code})
    return True


async def click_at(ws, x, y):
    await cdp(ws, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    await asyncio.sleep(0.05)
    await cdp(ws, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


# ============ 工作流点击（PrimeVue Tree）============

async def click_workflow(ws, name_fragment):
    """
    点击侧边栏中的工作流文件并加载。
    ComfyUI-aki 使用 PrimeVue Tree 组件，文件嵌套在文件夹中。
    """
    async def find_workflow_file():
        result = await cdp(ws, "Runtime.evaluate", {
            "expression": """
            (function(){
                var all = document.querySelectorAll('*');
                var result = null;
                all.forEach(function(el) {
                    var text = el.textContent.trim();
                    if (text.endsWith('.json')) {
                        var r = el.getBoundingClientRect();
                        if (r.width > 50 && r.height >= 15 && r.height < 60 && r.y < 2000) {
                            result = {
                                text: text,
                                x: Math.round(r.x + r.width/2),
                                y: Math.round(r.y + r.height/2),
                                y_abs: Math.round(r.y)
                            };
                        }
                    }
                });
                return result ? JSON.stringify(result) : 'null';
            })()
            """.replace("fireredimage", name_fragment),
            "returnByValue": True
        })
        raw = result.get("result", {}).get("result", {}).get("value", "null")
        if raw and raw != "null":
            try:
                return json.loads(raw)
            except:
                pass
        return None

    async def find_parent_folder(file_y):
        result = await cdp(ws, "Runtime.evaluate", {
            "expression": """
            (function(){
                var all = document.querySelectorAll('*');
                var result = null;
                var targetY = %d;
                all.forEach(function(el) {
                    var text = el.textContent.trim();
                    var cls = el.className || '';
                    var isFolder = cls.includes('tree-folder') || cls.includes('p-tree-node-content');
                    var r = el.getBoundingClientRect();
                    if (isFolder && r.width > 50 && r.height > 0 && r.y < targetY && r.y > 100) {
                        if (!result || r.y > result.y) {
                            result = {
                                text: text.substring(0, 60),
                                x: Math.round(r.x + 10),
                                y: Math.round(r.y + r.height/2),
                                y_abs: Math.round(r.y)
                            };
                        }
                    }
                });
                return result ? JSON.stringify(result) : 'null';
            })()
            """ % file_y,
            "returnByValue": True
        })
        raw = result.get("result", {}).get("result", {}).get("value", "null")
        if raw and raw != "null":
            try:
                return json.loads(raw)
            except:
                pass
        return None

    # 尝试直接找到文件
    file_info = await find_workflow_file()

    if not file_info:
        # 文件未找到？找并展开父文件夹
        keyword = name_fragment.split('-')[0].split('image')[0][:10]
        result = await cdp(ws, "Runtime.evaluate", {
            "expression": """
            (function(){
                var all = document.querySelectorAll('*');
                var candidates = [];
                all.forEach(function(el) {
                    var text = el.textContent.trim();
                    var cls = el.className || '';
                    var isFolder = cls.includes('tree-folder') || cls.includes('p-tree-node-content');
                    var r = el.getBoundingClientRect();
                    if (isFolder && r.width > 50 && r.height > 0 && r.y > 100 && r.y < 2000) {
                        candidates.push({
                            text: text.substring(0, 60),
                            x: Math.round(r.x + 10),
                            y: Math.round(r.y + r.height/2),
                            y_abs: Math.round(r.y)
                        });
                    }
                });
                if (candidates.length > 0) {
                    candidates.sort(function(a, b) { return b.y_abs - a.y_abs; });
                    return JSON.stringify(candidates[0]);
                }
                return 'null';
            })()
            """.replace("firered", keyword),
            "returnByValue": True
        })
        raw = result.get("result", {}).get("result", {}).get("value", "null")
        if raw and raw != "null":
            try:
                folder = json.loads(raw)
                await click_at(ws, folder["x"], folder["y"])
                await asyncio.sleep(1.5)
                file_info = await find_workflow_file()
            except:
                pass

    if not file_info:
        return False, f"工作流文件 '{name_fragment}' 未找到"

    # 点击文件
    click_result = await cdp(ws, "Runtime.evaluate", {
        "expression": json.dumps(
            """
            (function() {
                var all = document.querySelectorAll('*');
                for (var i = 0; i < all.length; i++) {
                    var el = all[i];
                    var r = el.getBoundingClientRect();
                    if (r.width > 50 && r.height >= 15 && r.height < 60 && r.y < 2000) {
                        var text = el.textContent.trim();
                        if (text === '%s') {
                            el.click();
                            return JSON.stringify({success: true, clicked: text});
                        }
                    }
                }
                return JSON.stringify({success: false});
            })()
            """ % file_info["text"]
        ),
        "returnByValue": True
    })
    val = click_result.get("result", {}).get("result", {}).get("value", "{}")
    try:
        val = json.loads(val)
    except:
        return False, "点击结果解析失败"

    if not val.get("success"):
        return False, "点击工作流文件失败"

    return True, val.get("clicked", "")


# ============ 工作流标签激活 ============

async def click_workflow_tab(ws):
    """点击左上角的工作流名称标签，激活当前工作流"""
    result = await cdp(ws, "Runtime.evaluate", {
        "expression": """
        (function() {
            var tabs = document.querySelectorAll('[class*="tab"]');
            for (var i = 0; i < tabs.length; i++) {
                var el = tabs[i];
                var r = el.getBoundingClientRect();
                var text = el.textContent.trim();
                if (r.y < 80 && r.width > 80 && r.height > 20 && text.length > 3) {
                    el.click();
                    return {success: true, text: text.substring(0, 60), x: Math.round(r.x), y: Math.round(r.y)};
                }
            }
            return {success: false};
        })()
        """,
        "returnByValue": True
    })
    val = result.get("result", {}).get("value", {})
    return val.get("success", False), val.get("text", "")


# ============ 批次设置（PrimeVue InputNumber）============

async def set_batch(ws, count=2):
    """设置批次数量。使用 PrimeVue nativeSetter 方法。"""
    result = await cdp(ws, "Runtime.evaluate", {
        "expression": """
        (function(){
            var input = document.querySelector('.p-inputnumber-input');
            if (!input) return 'null';
            var r = input.getBoundingClientRect();
            return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2), val: input.value});
        })()
        """,
        "returnByValue": True
    })
    raw = result.get("result", {}).get("result", {}).get("value", "null")
    try:
        data = json.loads(raw) if raw != 'null' else None
    except:
        data = None

    if not data:
        return False, {"error": "no batch input found"}

    current = int(data.get('val', '1'))
    if current == count:
        return True, {"method": "already_correct", "value": current}

    # PrimeVue 专用方法
    js_result = await cdp(ws, "Runtime.evaluate", {
        "expression": f"""
        (function(){{
            var input = document.querySelector('.p-inputnumber-input');
            if (!input) return 'no input';
            input.focus();
            input.select();
            var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
            nativeSetter.call(input, '');
            input.dispatchEvent(new Event('input', {{bubbles: true}}));
            nativeSetter.call(input, '{count}');
            input.dispatchEvent(new Event('input', {{bubbles: true}}));
            input.dispatchEvent(new Event('change', {{bubbles: true}}));
            input.blur();
            return input.value;
        }})()
        """
    })
    js_val = js_result.get("result", {}).get("result", {}).get("value", "")
    await asyncio.sleep(0.5)

    # 验证
    verify = await cdp(ws, "Runtime.evaluate", {
        "expression": "(function(){var el=document.querySelector('.p-inputnumber-input');return el?el.value:'not found';})()",
        "returnByValue": True
    })
    val = verify.get("result", {}).get("result", {}).get("value", "")
    ok = str(count) in str(val)
    return ok, {"method": "primevue_nativeSetter", "verified_value": val, "target": count}


# ============ API 运行（核心修复）============

def get_history_prompt(workflow_prefix="Firered"):
    """
    从历史中获取目标工作流的 prompt 结构。
    返回 (prompt_dict, history_id) 或 (None, None)
    """
    try:
        url = f"http://127.0.0.1:{COMFYUI_PORT}/history"
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read())

        for history_id, entry in data.items():
            prompt = entry.get("prompt", [])
            if isinstance(prompt, list) and len(prompt) >= 3 and len(prompt[2]) > 0:
                nodes = prompt[2]
                for nid, ndata in nodes.items():
                    if ndata.get("class_type") == "SaveImage":
                        prefix = ndata.get("inputs", {}).get("filename_prefix", "")
                        if workflow_prefix in str(prefix):
                            # 深拷贝避免修改原数据
                            import copy
                            prompt_copy = copy.deepcopy(nodes)
                            return prompt_copy, history_id
    except Exception as e:
        print(f"Error getting history: {e}", file=sys.stderr)
    return None, None


def randomize_seeds(prompt_nodes, seed_range=(10000000000000, 99999999999999)):
    """随机化所有 KSampler/KSamplerAdvanced 节点的种子"""
    for nid, ndata in prompt_nodes.items():
        ctype = ndata.get("class_type", "")
        if "Sampler" in ctype and "inputs" in ndata:
            if "seed" in ndata["inputs"]:
                ndata["inputs"]["seed"] = random.randint(*seed_range)


def clear_queue():
    """清空当前队列（删除 pending 状态的条目）"""
    try:
        # 获取队列
        url = f"http://127.0.0.1:{COMFYUI_PORT}/queue"
        resp = urllib.request.urlopen(url, timeout=5)
        queue_data = json.loads(resp.read())

        # 删除队列中的项目
        for item in queue_data.get("queue_pending", []):
            prompt_id = item.get("prompt_id")
            if prompt_id:
                try:
                    del_url = f"http://127.0.0.1:{COMFYUI_PORT}/queue/pending/{prompt_id}"
                    req = urllib.request.Request(del_url, method="DELETE")
                    urllib.request.urlopen(req, timeout=5)
                    print(f"Cleared stale queue entry: {prompt_id[:20]}")
                except:
                    pass
    except Exception as e:
        print(f"Queue clear warning: {e}", file=sys.stderr)


def api_run_workflow(prompt_nodes, batch_count=1):
    """
    通过 REST API 运行工作流（绕过 graphToPrompt 返回空的问题）。

    重要：必须使用 number=1 多次调用，而非 number=N！
    因为 number=N 的多次执行会共享 SaveImage 的文件名计数器，导致覆盖。

    Args:
        prompt_nodes: 从历史获取的 prompt 结构
        batch_count: 批次数（会调用 N 次 API）

    Returns:
        list of (success, prompt_id)
    """
    results = []

    # 清空陈旧队列条目
    clear_queue()

    for i in range(batch_count):
        # 每次调用都随机化种子
        prompt_copy = json.loads(json.dumps(prompt_nodes))
        randomize_seeds(prompt_copy)

        url = f"http://127.0.0.1:{COMFYUI_PORT}/prompt"
        payload = json.dumps({"number": 1, "prompt": prompt_copy}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

        try:
            resp = urllib.request.urlopen(req, timeout=30)
            result = json.loads(resp.read())
            prompt_id = result.get("prompt_id", "?")
            results.append((True, prompt_id))
            print(f"  Batch {i+1}/{batch_count}: prompt_id={prompt_id[:20]}, queued successfully")
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            results.append((False, f"HTTP {e.code}: {body}"))
            print(f"  Batch {i+1}/{batch_count}: FAILED {e.code}")
        except Exception as e:
            results.append((False, str(e)))
            print(f"  Batch {i+1}/{batch_count}: ERROR {e}")

        if i < batch_count - 1:
            time.sleep(1)  # 避免过快提交

    return results


async def wait_for_completion(prompt_ids, check_interval=30, timeout=600):
    """等待所有 prompt_ids 执行完成"""
    start = time.time()
    completed = set()

    while time.time() - start < timeout:
        try:
            url = f"http://127.0.0.1:{COMFYUI_PORT}/history"
            resp = urllib.request.urlopen(url, timeout=10)
            data = json.loads(resp.read())

            for pid in prompt_ids:
                if pid in completed:
                    continue
                entry = data.get(pid, {})
                status = entry.get("status", {}).get("status_str", "")
                if status in ("success", "failed"):
                    completed.add(pid)
                    print(f"  {pid[:20]}: {status}")

        except Exception as e:
            print(f"  Wait error: {e}")

        if len(completed) == len(prompt_ids):
            print(f"All {len(completed)} executions completed!")
            return True

        await asyncio.sleep(check_interval)

    print(f"Timeout: {len(completed)}/{len(prompt_ids)} completed")
    return False


# ============ 主命令处理 ============

async def main():
    if len(sys.argv) < 2:
        print("用法: comfyui_browser.py <TAB_ID> <action> [arg]")
        print("  find_tab                  发现 ComfyUI 标签页")
        print("  screenshot [path]          截图")
        print("  press_key <key>           按键（w/Escape/Enter/F11）")
        print("  click_workflow <name>      点击侧边栏工作流")
        print("  click_workflow_tab         点击工作流标签激活")
        print("  set_batch <n>             设置批次")
        print("  api_run <n>               用 REST API 运行 N 批次")
        print("  run_workflow <name> <n>   完整流程：点击→设批次→API运行N批次")
        print("  clear_queue               清空队列")
        print("  status                    队列状态")
        sys.exit(1)

    action = sys.argv[1]

    # Actions that don't require TAB_ID
    if action == "find_tab":
        tab = find_comfyui_tab()
        if tab:
            print(f"Found: {tab['id']} | {tab.get('title','?')[:50]}")
        else:
            print("ComfyUI tab not found")
            sys.exit(1)
        return

    if action == "clear_queue":
        clear_queue()
        print("Queue cleared")
        return

    if action == "status":
        try:
            url = f"http://127.0.0.1:{COMFYUI_PORT}/queue"
            resp = urllib.request.urlopen(url, timeout=5)
            data = json.loads(resp.read())
            running = len(data.get("queue_running", []))
            pending = len(data.get("queue_pending", []))
            print(f"Queue: running={running}, pending={pending}")
        except Exception as e:
            print(f"Error: {e}")
        return

    if action == "api_run":
        # api_run [batch]  - no tab_id needed, uses REST API directly
        if len(sys.argv) < 3:
            batch = 2
        else:
            batch = int(sys.argv[2])

        print(f"Running workflow with batch={batch} via REST API...")
        prompt_nodes, hist_id = get_history_prompt()
        if not prompt_nodes:
            print("ERROR: No workflow found in history. Please run the workflow once via UI first.")
            sys.exit(1)
        print(f"Using history entry: {hist_id[:30]}")

        results = api_run_workflow(prompt_nodes, batch)
        successes = sum(1 for ok, _ in results if ok)
        print(f"\nResults: {successes}/{len(results)} queued successfully")

        if successes > 0:
            prompt_ids = [pid for ok, pid in results if ok]
            await wait_for_completion(prompt_ids)

        return

    if action == "run_workflow":
        # run_workflow <TAB_ID> run_workflow <workflow_name> <batch_count>
        if len(sys.argv) < 5:
            print("Usage: comfyui_browser.py <TAB_ID> run_workflow <workflow_name> <batch_count>")
            sys.exit(1)
        tab_id = sys.argv[1]
        wf_name = sys.argv[3]
        batch_count = int(sys.argv[4])

        ws_url = get_ws_url(tab_id)
        async with await ws_connect_with_retry(ws_url) as ws:
            # 1. 打开侧边栏
            print("Step 1: Opening sidebar...")
            await press_key(ws, "w")
            await asyncio.sleep(2)

            # 2. 清空搜索（如有残留）
            await cdp(ws, "Runtime.evaluate", {
                "expression": """
                (function(){
                    var inputs = document.querySelectorAll('input');
                    for (var i = 0; i < inputs.length; i++) {
                        var ph = inputs[i].placeholder || '';
                        if (ph.includes('搜索') || ph.includes('search')) {
                            inputs[i].value = '';
                            inputs[i].dispatchEvent(new Event('input', {bubbles: true}));
                            return 'cleared';
                        }
                    }
                    return 'not found';
                })()
                """,
                "returnByValue": True
            })
            await asyncio.sleep(0.5)

            # 3. 点击工作流文件
            print(f"Step 2: Loading workflow '{wf_name}'...")
            ok, msg = await click_workflow(ws, wf_name)
            if not ok:
                print(f"WARNING: {msg}")
            else:
                print(f"  Clicked: {msg}")
            await asyncio.sleep(3)

            # 4. ESC 关闭侧边栏
            await press_key(ws, "Escape")
            await asyncio.sleep(1)

            # 5. 点击工作流标签激活
            print("Step 3: Activating workflow tab...")
            ok, text = await click_workflow_tab(ws)
            if ok:
                print(f"  Tab: {text}")
            await asyncio.sleep(1)

            # 6. 设置批次（仅修改 UI 显示，不影响实际执行）
            print(f"Step 4: Setting batch to {batch_count}...")
            ok, detail = await set_batch(ws, batch_count)
            print(f"  {'OK' if ok else 'FAILED'}: {detail}")
            await asyncio.sleep(0.5)

        # 7. 用 REST API 运行
        print(f"Step 5: Running {batch_count} batches via REST API...")
        prompt_nodes, hist_id = get_history_prompt()
        if not prompt_nodes:
            print("ERROR: No workflow found in history.")
            sys.exit(1)
        print(f"  Using history: {hist_id[:30]}")

        results = api_run_workflow(prompt_nodes, batch_count)
        successes = sum(1 for ok, _ in results if ok)
        print(f"\nResults: {successes}/{len(results)} queued")

        if successes > 0:
            prompt_ids = [pid for ok, pid in results if ok]
            await wait_for_completion(prompt_ids)

        return

    if len(sys.argv) < 3:
        print(f"Error: {action} requires TAB_ID")
        print("Usage:")
        print("  TAB_ID ACTION [ARG]:  python3 comfyui_browser.py <TAB_ID> <ACTION> [ARG]")
        print("  ACTION (no TAB):       python3 comfyui_browser.py find_tab|clear_queue|api_run [batch]")
        sys.exit(1)

    tab_id = sys.argv[1]  # sys.argv[1] = TAB_ID
    real_action = sys.argv[2]  # sys.argv[2] = ACTION
    real_arg = sys.argv[3] if len(sys.argv) > 3 else None  # sys.argv[3] = arg

    ws_url = get_ws_url(tab_id)
    try:
        ws = await ws_connect_with_retry(ws_url)
        async with ws:
            if real_action == "screenshot":
                path = real_arg or "/tmp/comfyui.png"
                ok = await screenshot(ws, path)
                print(f"{'OK' if ok else 'FAILED'}: {path}")

            elif real_action == "press_key":
                ok = await press_key(ws, real_arg or "Enter")
                print(f"Key sent: {real_arg}")

            elif real_action == "set_batch":
                count = int(real_arg) if real_arg else 2
                ok, detail = await set_batch(ws, count)
                print(f"Batch {'OK' if ok else 'FAILED'}: {detail}")

            elif real_action == "click_workflow":
                # 按 w 打开侧边栏
                await press_key(ws, "w")
                await asyncio.sleep(2)
                ok, clicked = await click_workflow(ws, real_arg or "")
                if ok:
                    await asyncio.sleep(3)
                    await press_key(ws, "Escape")
                    await asyncio.sleep(1)
                    ok2, text = await click_workflow_tab(ws)
                    print(f"OK: {clicked} loaded, tab={text}")
                else:
                    print(f"FAILED: {clicked}")

            elif real_action == "click_workflow_tab":
                ok, text = await click_workflow_tab(ws)
                print(f"{'OK' if ok else 'FAILED'}: {text}")

            elif real_action == "status":
                r = await cdp(ws, "Runtime.evaluate", {
                    "expression": "document.querySelector('.comfy-menu-header')?.textContent || 'not found'",
                    "returnByValue": True
                })
                print(f"Queue: {r.get('result',{}).get('result',{}).get('value')}")

            else:
                print(f"Unknown action: {real_action}")
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
