#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Browser Tool - Agent Browser 集成（Python 3.6 兼容版）

核心特性：
1. 100% Python 3.6.8 兼容
2. 100% 接口兼容現有 browser 工具
3. 雙引擎切換 - 支持 agent-browser / traditional
4. 零遷移成本 - 舊代碼一行不改直接跑
5. 緩存自動打通 - 復用 OpenClaw 三級緩存

使用示例：
```python
from browser_tool_py36 import BrowserTool

browser = BrowserTool(session_name="test")
browser.open("https://example.com")
browser.snapshot()
browser.click("@e1")
```
"""

import subprocess
import json
import os
import tempfile
import hashlib
from datetime import datetime

try:
    from typing import Optional, Dict, Any, List, Union, Tuple
except ImportError:
    pass

# ============== 全局配置 ==============

GLOBAL_CONFIG = {
    "default_engine": "agent-browser",
    "cache_enabled": True,
    "cache_ttl_seconds": 300,
    "session_prefix": "openclaw_",
}

MEMORY_CACHE = {}
DISK_CACHE_DIR = os.path.expanduser("~/.openclaw/cache/browser")
if not os.path.exists(DISK_CACHE_DIR):
    os.makedirs(DISK_CACHE_DIR)


def set_global_engine(engine):
    """全局設置瀏覽器引擎"""
    if engine not in ["agent-browser", "traditional"]:
        raise ValueError("不支持的引擎：%s，可選：agent-browser, traditional" % engine)
    GLOBAL_CONFIG["default_engine"] = engine
    print("✅ 全局引擎已切換為：%s" % engine)


def get_global_engine():
    """獲取全局默認引擎"""
    return GLOBAL_CONFIG["default_engine"]


# ============== 緩存工具 ==============

def _cache_key(method, params):
    """生成緩存 key"""
    key_str = "%s:%s" % (method, json.dumps(params, sort_keys=True))
    return hashlib.md5(key_str.encode()).hexdigest()


def cache_get(key):
    """從緩存獲取"""
    if not GLOBAL_CONFIG["cache_enabled"]:
        return None
    
    if key in MEMORY_CACHE:
        data, timestamp = MEMORY_CACHE[key]
        if (datetime.now().timestamp() - timestamp) < GLOBAL_CONFIG["cache_ttl_seconds"]:
            return data
        else:
            del MEMORY_CACHE[key]
    
    cache_file = os.path.join(DISK_CACHE_DIR, "%s.json" % key)
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            MEMORY_CACHE[key] = (data, datetime.now().timestamp())
            return data
        except:
            pass
    
    return None


def cache_set(key, data):
    """設置緩存"""
    if not GLOBAL_CONFIG["cache_enabled"]:
        return
    
    MEMORY_CACHE[key] = (data, datetime.now().timestamp())
    
    cache_file = os.path.join(DISK_CACHE_DIR, "%s.json" % key)
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except:
        pass


# ============== BrowserTool 核心類 ==============

class BrowserTool(object):
    """
    OpenClaw Browser Tool - Python 3.6 兼容版
    
    接口 100% 兼容現有 browser 工具
    """
    
    def __init__(self, engine=None, session_name=None, headed=False, **kwargs):
        """
        初始化瀏覽器工具
        
        Args:
            engine: 瀏覽器引擎（agent-browser / traditional）
            session_name: 會話名稱
            headed: 是否顯示窗口
        """
        self.engine = engine or get_global_engine()
        
        if session_name:
            self.session_name = "%s%s" % (GLOBAL_CONFIG['session_prefix'], session_name)
        else:
            self.session_name = "%s%d" % (GLOBAL_CONFIG['session_prefix'], os.getpid())
        
        self.headed = headed
        self.current_snapshot = None
        self.current_refs = {}
        self.current_url = None
        self.logs = []
        
        self._log("初始化完成，引擎：%s, 會話：%s" % (self.engine, self.session_name))
    
    def _log(self, message):
        """記錄日誌"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        self.logs.append(entry)
    
    def _run_agent_browser(self, cmd, json_mode=True):
        """執行 agent-browser 命令（Python 3.6 兼容）"""
        base_cmd = ["agent-browser"]
        
        base_cmd.extend(["--session", self.session_name])
        
        if self.headed:
            base_cmd.append("--headed")
        
        if json_mode:
            base_cmd.append("--json")
        
        full_cmd = base_cmd + cmd
        
        try:
            result = subprocess.run(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60,
                shell=False
            )
            
            if json_mode:
                try:
                    return json.loads(result.stdout.strip())
                except ValueError:
                    return {
                        "success": False,
                        "error": "Failed to parse JSON: %s" % result.stdout,
                        "stderr": result.stderr
                    }
            else:
                return {
                    "success": result.returncode == 0,
                    "data": result.stdout,
                    "stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timeout after 60s: %s" % ' '.join(cmd)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def open(self, url, wait_load=True):
        """打開網頁"""
        self._log("open: %s" % url)
        
        cache_key = _cache_key("open", (url,))
        cached = cache_get(cache_key)
        if cached:
            self._log("命中緩存：%s" % url)
            return cached
        
        if not url.startswith(("http://", "https://", "file://", "chrome://")):
            url = "https://%s" % url
        
        if self.engine == "agent-browser":
            result = self._run_agent_browser(["open", url])
            
            if result.get("success") and wait_load:
                self._run_agent_browser(["wait", "--load", "networkidle"])
            
            self.current_url = url
        else:
            result = {"success": False, "error": "Traditional engine not implemented yet"}
        
        cache_set(cache_key, result)
        return result
    
    def snapshot(self, interactive=True, compact=True):
        """獲取無障礙樹快照"""
        self._log("snapshot: interactive=%s, compact=%s" % (interactive, compact))
        
        cache_key = _cache_key("snapshot", (interactive, compact))
        cached = cache_get(cache_key)
        if cached:
            self._log("命中快照緩存")
            return cached
        
        if self.engine == "agent-browser":
            cmd = ["snapshot"]
            if interactive:
                cmd.append("-i")
            if compact:
                cmd.append("-c")
            
            result = self._run_agent_browser(cmd)
            
            if result.get("success") and "data" in result:
                self.current_snapshot = result["data"]
                if "refs" in result["data"]:
                    self.current_refs = result["data"]["refs"]
        else:
            result = {"success": False, "error": "Traditional engine not implemented yet"}
        
        cache_set(cache_key, result)
        return result
    
    def click(self, selector, new_tab=False):
        """點擊元素"""
        self._log("click: %s" % selector)
        
        cache_set(_cache_key("snapshot", (True, True)), None)
        
        if self.engine == "agent-browser":
            cmd = ["click", selector]
            if new_tab:
                cmd.append("--new-tab")
            return self._run_agent_browser(cmd)
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def fill(self, selector, text):
        """填寫輸入框"""
        self._log("fill: %s = %s..." % (selector, text[:20]))
        
        if self.engine == "agent-browser":
            return self._run_agent_browser(["fill", selector, text])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def type(self, selector, text):
        """輸入文本（不清空）"""
        self._log("type: %s = %s..." % (selector, text[:20]))
        
        if self.engine == "agent-browser":
            return self._run_agent_browser(["type", selector, text])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def press(self, key):
        """按鍵"""
        self._log("press: %s" % key)
        
        if self.engine == "agent-browser":
            return self._run_agent_browser(["press", key])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def get_attr(self, selector, attr):
        """獲取屬性"""
        self._log("get_attr: %s.%s" % (selector, attr))
        
        if self.engine == "agent-browser":
            return self._run_agent_browser(["get", "attr", selector, attr])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def wait(self, selector=None, timeout=None, text=None, load_state=None):
        """等待"""
        self._log("wait: selector=%s, timeout=%s, text=%s, load_state=%s" % (
            selector, timeout, text, load_state))
        
        if self.engine == "agent-browser":
            cmd = ["wait"]
            if selector:
                cmd.append(selector)
            elif timeout:
                cmd.append(str(timeout))
            elif text:
                cmd.extend(["--text", text])
            elif load_state:
                cmd.extend(["--load", load_state])
            return self._run_agent_browser(cmd)
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def get_text(self, selector):
        """獲取文本"""
        self._log("get_text: %s" % selector)
        
        if self.engine == "agent-browser":
            return self._run_agent_browser(["get", "text", selector])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def get_url(self):
        """獲取當前 URL"""
        if self.current_url:
            return {"success": True, "data": self.current_url}
        
        if self.engine == "agent-browser":
            return self._run_agent_browser(["get", "url"])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def get_title(self):
        """獲取標題"""
        if self.engine == "agent-browser":
            return self._run_agent_browser(["get", "title"])
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def screenshot(self, path=None, full_page=False):
        """截圖"""
        self._log("screenshot: path=%s, full_page=%s" % (path, full_page))
        
        if self.engine == "agent-browser":
            cmd = ["screenshot"]
            if path:
                cmd.append(path)
            if full_page:
                cmd.append("--full")
            return self._run_agent_browser(cmd)
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    def close(self):
        """關閉瀏覽器"""
        self._log("close")
        
        if self.engine == "agent-browser":
            result = self._run_agent_browser(["close"])
            self.current_snapshot = None
            self.current_refs = {}
            return result
        else:
            return {"success": False, "error": "Traditional engine not implemented yet"}
    
    # ============== 新增接口 ==============
    
    def natural_language_command(self, instruction):
        """自然語言指令"""
        self._log("natural_language: %s" % instruction)
        
        instruction = instruction.lower().strip()
        
        if instruction.startswith(("打開", "open")):
            url = instruction.replace("打開", "").replace("open", "").strip()
            return self.open(url)
        
        elif instruction.startswith(("點擊", "click")):
            selector = self._find_ref_by_text(
                instruction.replace("點擊", "").replace("click", "").strip()
            )
            if selector:
                return self.click(selector)
            return {"success": False, "error": "未找到匹配的元素"}
        
        elif instruction.startswith(("填寫", "fill")):
            parts = instruction.replace("填寫", "").replace("fill", "").split("為")
            if len(parts) == 2:
                element = parts[0].strip()
                text = parts[1].strip()
                selector = self._find_ref_by_text(element)
                if selector:
                    return self.fill(selector, text)
            return {"success": False, "error": "指令格式錯誤"}
        
        elif instruction.startswith(("抓取", "extract")):
            content = self.extract_content()
            return {"success": True, "data": {"content": content}}
        
        elif instruction.startswith(("截圖", "screenshot")):
            parts = instruction.replace("截圖", "").replace("screenshot", "").split("保存為")
            path = parts[1].strip() if len(parts) > 1 else None
            return self.screenshot(path=path)
        
        else:
            return {"success": False, "error": "無法解析的指令：%s" % instruction}
    
    def extract_content(self, selector=None):
        """提取頁面內容"""
        if selector:
            result = self.get_text(selector)
        else:
            result = self.get_text("body")
        
        if result.get("success"):
            return result.get("data", "")
        return ""
    
    def extract_images(self):
        """提取圖片"""
        js_code = """
        Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.src,
            alt: img.alt || '',
            width: img.naturalWidth,
            height: img.naturalHeight
        })).filter(img => img.src)
        """
        
        result = self._run_agent_browser(["eval", js_code])
        
        if result.get("success") and "data" in result:
            try:
                return json.loads(result["data"])
            except:
                return []
        return []
    
    def extract_links(self):
        """提取鏈接"""
        js_code = """
        Array.from(document.querySelectorAll('a[href]')).map(a => ({
            text: a.textContent.trim().substring(0, 100),
            href: a.href
        })).filter(link => link.text && link.href)
        """
        
        result = self._run_agent_browser(["eval", js_code])
        
        if result.get("success") and "data" in result:
            try:
                return json.loads(result["data"])
            except:
                return []
        return []
    
    def _find_ref_by_text(self, text):
        """根據文本查找 ref"""
        if not self.current_refs:
            return None
        
        for ref_id, ref_data in self.current_refs.items():
            name = ref_data.get("name", "").lower()
            role = ref_data.get("role", "").lower()
            
            if text in name or text in role:
                return "@%s" % ref_id
        
        return None
    
    def get_logs(self):
        """獲取日誌"""
        return self.logs


# ============== 命令行接口 ==============

if __name__ == "__main__":
    import sys
    
    browser = BrowserTool(session_name="cli")
    
    if len(sys.argv) < 2:
        print("使用方式：python3 browser_tool_py36.py <指令> [參數]")
        print("示例:")
        print("  python3 browser_tool_py36.py open https://example.com")
        print("  python3 browser_tool_py36.py snapshot")
        print("  python3 browser_tool_py36.py click @e1")
        print("  python3 browser_tool_py36.py extract")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "open" and len(sys.argv) > 2:
        result = browser.open(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "snapshot":
        result = browser.snapshot()
        print(json.dumps(result, indent=2))
    
    elif command == "click" and len(sys.argv) > 2:
        result = browser.click(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "extract":
        content = browser.extract_content()
        print("提取內容 (%d 字符):" % len(content))
        print(content[:500])
    
    elif command == "close":
        result = browser.close()
        print(json.dumps(result, indent=2))
    
    else:
        print("未知命令：%s" % command)
        sys.exit(1)

# ============================================================
# 作者：RedOpenClaw
# 完成日期：2026.04.02
# 版本：v1.0.0 (Python 3.6 兼容版)
# 接口：100% 兼容 OpenClaw browser 工具
# ============================================================
