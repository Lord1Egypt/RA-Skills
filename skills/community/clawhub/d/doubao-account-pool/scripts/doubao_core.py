# -*- coding: utf-8 -*-
"""豆包实例底座（冻结 API）—— 真正实现，零 stub。

统一底座：配置解析 + CDP 会话 + 实例生命周期，供其余模块调用。
Python 3.9+，仅标准库 + websocket-client，UTF-8，中文注释。

冻结签名:
  S(port) -> s;  s.send(method, params=None);  s.ev(expr, wait=0.6);  s.ready(limit=25)
  s.navigate(url);  s.click_xy(x,y);  s.click_text(txt, exact=False);  s.shot(path=None) -> 路径;  s.close()

模块级 API:
  cfg() / home() / out_dir() / port_of(n) / udd_of(n) / pidfile(n)
  alive(n, timeout=1.5) / up(n, quiet=False) / up_all(quiet=False) / down(n)
  status(deep=False) / login_state(n) / nick(n) / http(port, path, method, timeout)
  log(msg) / find_chrome() / find_ffmpeg(name) / SITE
"""
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request

# ════════════════════════════════════════════════════════════════
# 常量
# ════════════════════════════════════════════════════════════════
SITE = 'https://www.doubao.com/chat/'

# 内置默认配置
_DEFAULTS = {
    'home': os.path.expanduser('~/.doubao_studio'),
    'out_dir': '',
    'port_base': 9230,
    'max_slot': 20,
    'chrome': '',
    'ffmpeg': '',
    'window_width': 1320,
    'window_height': 900,
    'headless': False,
}

# 环境变量名映射（env_name -> cfg_key）
_ENV_MAP = {
    'DOUBAO_HOME': 'home',
    'DOUBAO_CHROME': 'chrome',
    'DOUBAO_FFMPEG': 'ffmpeg',
    'DOUBAO_OUTDIR': 'out_dir',
    'DOUBAO_PORT_BASE': 'port_base',
    'DOUBAO_MAX_SLOT': 'max_slot',
}


# ════════════════════════════════════════════════════════════════
# 配置管理：环境变量 > ./doubao_config.json > home()/config.json > 内置默认
# ════════════════════════════════════════════════════════════════
_cached_cfg = None


def _deep_merge(base, override):
    """浅合并：override 覆盖 base，不递归嵌套 dict（本场景配置都是扁平的）。"""
    result = dict(base)
    for k, v in override.items():
        if v is not None and v != '':
            result[k] = v
    return result


def _load_json_cfg(path):
    """安全加载 JSON 配置文件；不存在或格式错则返回空 dict。"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def cfg():
    """返回合并后的配置 dict（无参调用）。"""
    global _cached_cfg
    if _cached_cfg is not None:
        return _cached_cfg

    # ① 内置默认
    merged = dict(_DEFAULTS)

    # ② home()/config.json（先算初始 home 以确定路径）
    init_home = os.environ.get('DOUBAO_HOME', merged['home'])
    home_cfg = _load_json_cfg(os.path.join(init_home, 'config.json'))
    merged = _deep_merge(merged, home_cfg)

    # ③ 当前目录 ./doubao_config.json
    cwd_cfg = _load_json_cfg(os.path.join(os.getcwd(), 'doubao_config.json'))
    merged = _deep_merge(merged, cwd_cfg)

    # ④ 环境变量（最高优先级）
    for env_name, cfg_key in _ENV_MAP.items():
        val = os.environ.get(env_name)
        if val is not None and val != '':
            merged[cfg_key] = val

    # 类型修正
    try:
        merged['port_base'] = int(merged['port_base'])
    except (ValueError, TypeError):
        merged['port_base'] = 9230
    try:
        merged['max_slot'] = int(merged['max_slot'])
    except (ValueError, TypeError):
        merged['max_slot'] = 20
    try:
        merged['window_width'] = int(merged['window_width'])
    except (ValueError, TypeError):
        merged['window_width'] = 1320
    try:
        merged['window_height'] = int(merged['window_height'])
    except (ValueError, TypeError):
        merged['window_height'] = 900

    # headless 布尔化
    if isinstance(merged['headless'], str):
        merged['headless'] = merged['headless'].lower() in ('1', 'true', 'yes')

    # out_dir 默认值：home()/out
    if not merged.get('out_dir'):
        merged['out_dir'] = os.path.join(merged['home'], 'out')

    _cached_cfg = merged
    return _cached_cfg


def _reset_cfg():
    """内部用：强制下次 cfg() 重新加载（测试用）。"""
    global _cached_cfg
    _cached_cfg = None


# 兼容模块级常量导出（doubao_fetch / doubao_image 的 import 需要）
DOUBAO_HOME = os.environ.get('DOUBAO_HOME', os.path.expanduser('~/.doubao_studio'))
DOUBAO_OUTDIR = os.environ.get('DOUBAO_OUTDIR', os.path.join(DOUBAO_HOME, 'out'))


# ════════════════════════════════════════════════════════════════
# 路径工具
# ════════════════════════════════════════════════════════════════
def home():
    """状态根目录。"""
    return cfg()['home']


def out_dir():
    """默认产出目录，不存在则创建。"""
    d = cfg()['out_dir']
    os.makedirs(d, exist_ok=True)
    return d


def port_of(n):
    """实例 n → CDP 调试端口。"""
    return cfg()['port_base'] + int(n)


def udd_of(n):
    """实例 n → user-data-dir 路径。"""
    return os.path.join(home(), 'doubao_p%d' % int(n))


def pidfile(n):
    """实例 n → pidfile 路径。"""
    return os.path.join(udd_of(n), '.slot_pid')


# ════════════════════════════════════════════════════════════════
# 日志
# ════════════════════════════════════════════════════════════════
def log(*args):
    """结构化短行日志（@@ 开头，截断 300 字符）。

    兼容两种调用形态：log("消息") 与 log("标签", "消息")——各模块混用，故用 *args。
    """
    msg = " ".join(str(a) for a in args if a is not None)
    line = '@@LOG %s %s' % (time.strftime('%H:%M:%S'), msg)
    print(line[:300], flush=True)


# ════════════════════════════════════════════════════════════════
# CDP HTTP 工具
# ════════════════════════════════════════════════════════════════
def http(port, path, method='GET', timeout=15):
    """向 CDP 端口发 HTTP 请求，返回解析后的 JSON。"""
    url = 'http://127.0.0.1:%d%s' % (port, path)
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8', 'replace'))


# ════════════════════════════════════════════════════════════════
# 进程检测与管理
# ════════════════════════════════════════════════════════════════
def alive(n, timeout=1.5):
    """实例 n 的 Chrome 是否在线（通过 /json/version 探活）。"""
    try:
        urllib.request.urlopen(
            'http://127.0.0.1:%d/json/version' % port_of(n),
            timeout=timeout,
        )
        return True
    except Exception:
        return False


def up(n, quiet=False):
    """启动实例 n 的 Chrome 浏览器。返回 True/False。"""
    n = int(n)
    if alive(n):
        if not quiet:
            log('up slot=%d ALREADY ALIVE port=%d' % (n, port_of(n)))
        return True

    c = cfg()
    chrome = _find_chrome_path()
    if not chrome:
        log('up slot=%d ERR 未找到 Chrome' % n)
        return False

    udd = udd_of(n)
    os.makedirs(udd, exist_ok=True)
    port = port_of(n)

    args = [
        chrome,
        '--remote-debugging-port=%d' % port,
        '--user-data-dir=%s' % udd,
        '--window-size=%d,%d' % (c['window_width'], c['window_height']),
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-background-networking',
        '--disable-sync',
        '--disable-translate',
        '--disable-extensions',
        '--remote-allow-origins=*',
    ]

    # headless 或窗口挪到屏幕外，绝不抢焦点
    if c.get('headless'):
        args.append('--headless=new')
    else:
        args.append('--window-position=-3000,-3000')

    # 额外参数
    for extra in c.get('chrome_args_extra', []):
        args.append(extra)

    args.append(SITE)

    try:
        if sys.platform == 'win32':
            proc = subprocess.Popen(
                args,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                close_fds=False,
            )
        else:
            proc = subprocess.Popen(args, start_new_session=True, close_fds=True)
    except Exception as e:
        log('up slot=%d ERR 启动失败: %s' % (n, str(e)[:100]))
        return False

    # 写 pidfile
    try:
        pf = pidfile(n)
        os.makedirs(os.path.dirname(pf), exist_ok=True)
        with open(pf, 'w') as f:
            f.write(str(proc.pid))
    except Exception:
        pass

    # 轮询 /json/version 等就绪
    ok = False
    for _ in range(50):
        time.sleep(0.5)
        if alive(n):
            ok = True
            break

    if ok:
        if not quiet:
            log('up slot=%d OK port=%d pid=%d' % (n, port, proc.pid))
    else:
        log('up slot=%d TIMEOUT port=%d' % (n, port))
    return ok


def up_all(quiet=False):
    """批量启动所有实例。返回 {slot: bool}。"""
    c = cfg()
    results = {}
    for n in range(1, c['max_slot'] + 1):
        results[n] = up(n, quiet=quiet)
    return results


def _find_chrome_path():
    """内部：寻找 Chrome 可执行文件路径。"""
    c = cfg()
    env_chrome = c.get('chrome', '')
    if env_chrome and os.path.isfile(env_chrome):
        return env_chrome

    # 常见路径
    candidates = []
    if sys.platform == 'win32':
        prog_files = os.environ.get('PROGRAMFILES', r'C:\Program Files')
        prog_files_x86 = os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)')
        local_app = os.environ.get('LOCALAPPDATA', '')
        for base in [prog_files, prog_files_x86, local_app]:
            candidates.append(os.path.join(base, r'Google\Chrome\Application\chrome.exe'))
            candidates.append(os.path.join(base, r'Microsoft\Edge\Application\msedge.exe'))
    else:
        candidates.extend([
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        ])

    for p in candidates:
        if os.path.isfile(p):
            return p

    # shutil.which 兜底
    for name in ('chrome', 'google-chrome', 'google-chrome-stable', 'chromium', 'msedge'):
        p = shutil.which(name)
        if p:
            return p

    return None


def find_chrome():
    """查找 Chrome/Chromium/Edge 可执行文件路径。找不到抛 RuntimeError。"""
    p = _find_chrome_path()
    if not p:
        raise RuntimeError('未找到 Chrome/Chromium/Edge，请设置 DOUBAO_CHROME 环境变量')
    return p


def find_ffmpeg(name='ffmpeg'):
    """查找 ffmpeg/ffprobe 可执行文件路径。找不到返回 None。"""
    c = cfg()

    if name == 'ffprobe':
        # 环境变量
        fp = c.get('ffprobe', '')
        if fp and os.path.isfile(fp):
            return fp
        # 同目录退化
        ff = c.get('ffmpeg', '')
        if ff:
            d = os.path.dirname(ff)
            ext = '.exe' if os.name == 'nt' else ''
            candidate = os.path.join(d, 'ffprobe' + ext)
            if os.path.isfile(candidate):
                return candidate
        # 系统 PATH
        p = shutil.which('ffprobe')
        return p
    else:
        ff = c.get('ffmpeg', '')
        if ff and os.path.isfile(ff):
            return ff
        p = shutil.which('ffmpeg')
        return p


# ════════════════════════════════════════════════════════════════
# 安全关闭（只杀本实例进程树）
# ════════════════════════════════════════════════════════════════
def _taskkill_tree_win(pid, udd_lower):
    """Windows：校验命令行含本实例目录后才 taskkill /PID <pid> /T /F。返回 0 或 1。"""
    try:
        ps_cmd = (
            "$p = Get-CimInstance Win32_Process -Filter \"ProcessId=%d\"; "
            "if($p -and $p.CommandLine -like '*%s*'){ 'MATCH' } else { 'NOTMINE' }"
            % (pid, udd_lower.replace("'", "''"))
        )
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command', ps_cmd],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20,
        )
        if 'MATCH' not in r.stdout.strip():
            return 0
        subprocess.run(
            ['taskkill', '/PID', str(pid), '/T', '/F'],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30,
        )
        time.sleep(1.2)
        return 1
    except Exception:
        return 0


def _kill_by_cmdline_unix(udd_path):
    """POSIX：按命令行含本实例目录匹配后 kill。返回被杀进程数。"""
    killed = 0
    try:
        out = subprocess.run(
            ['pgrep', '-f', udd_path],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=10,
        )
        for line in out.stdout.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                pid = int(line)
                subprocess.run(['kill', '-9', str(pid)], timeout=5)
                killed += 1
            except Exception:
                pass
    except Exception:
        pass
    return killed


def _kill_by_cmdline_win(udd_lower):
    """Windows：用 PowerShell 按命令行精确匹配 chrome.exe 本实例进程。返回被杀进程数。"""
    killed = 0
    try:
        ps_cmd = (
            "Get-CimInstance Win32_Process -Filter \"name='chrome.exe'\" | "
            "Where-Object { $_.CommandLine -like '*%s*' } | "
            "ForEach-Object { $_.ProcessId } | ConvertTo-Json -Compress"
            % udd_lower.replace("'", "''")
        )
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command', ps_cmd],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=25,
        )
        out = r.stdout.strip()
        if not out:
            return 0
        pids = json.loads(out)
        if isinstance(pids, int):
            pids = [pids]
        for pid in pids:
            killed += _taskkill_tree_win(int(pid), udd_lower)
    except Exception:
        pass
    return killed


def down(n):
    """只杀本实例 Chrome 进程树。返回被杀进程数。绝不碰用户的浏览器。"""
    n = int(n)
    udd_lower = udd_of(n).lower()
    killed = 0

    # ① pidfile 优先
    try:
        pf = pidfile(n)
        if os.path.isfile(pf):
            pid = int(open(pf, 'r').read().strip())
            if sys.platform == 'win32':
                killed += _taskkill_tree_win(pid, udd_lower)
            else:
                killed += _kill_by_cmdline_unix(udd_of(n))
    except Exception:
        pass

    # ② 兜底：按命令行精确匹配
    if sys.platform == 'win32':
        killed += _kill_by_cmdline_win(udd_lower)
    else:
        killed += _kill_by_cmdline_unix(udd_of(n))

    # 清理 pidfile
    try:
        os.remove(pidfile(n))
    except Exception:
        pass

    if killed > 0:
        log('down slot=%d killed=%d' % (n, killed))
    return killed


# ════════════════════════════════════════════════════════════════
# 状态
# ════════════════════════════════════════════════════════════════
def status(deep=False):
    """返回所有实例状态列表。兼容 status(deep=True) 和 status(True)。"""
    c = cfg()
    result = []
    for n in range(1, c['max_slot'] + 1):
        is_alive = alive(n)
        udd = udd_of(n)
        has_profile = os.path.isdir(udd)
        has_pid = os.path.isfile(pidfile(n))
        logged = None
        if deep and is_alive:
            logged = login_state(n)
        result.append({
            'slot': n,
            'port': port_of(n),
            'alive': is_alive,
            'logged': logged,
            'profile': has_profile,
            'pidfile': has_pid,
        })
    return result


# ════════════════════════════════════════════════════════════════
# 登录态三重校验
# ════════════════════════════════════════════════════════════════
_LOGIN_CHECK_JS = r"""(() => {
  try {
    var url = location.href || '';
    var t = document.body ? (document.body.innerText || '') : '';
    var urlNoLogin = url.indexOf('login') < 0;
    var noLoginEntry = !/立即登录|登录\/注册|扫码登录/.test(t.slice(0, 1200));
    var hasHistory = false;
    var sidebar = document.querySelector('[class*=conversation],[class*=sidebar],[class*=chat-list],[class*=session]');
    if (sidebar) {
      var items = sidebar.querySelectorAll('a,div,li,span');
      hasHistory = items.length > 2;
    }
    if (!hasHistory) {
      var allEls = document.querySelectorAll('*');
      for (var i = 0; i < allEls.length; i++) {
        var cls = (allEls[i].className || '').toString();
        if (/conversation|session|chat-list|history/.test(cls)) {
          hasHistory = true;
          break;
        }
      }
    }
    return JSON.stringify({urlNoLogin: urlNoLogin, noLoginEntry: noLoginEntry, hasHistory: hasHistory});
  } catch (e) {
    return JSON.stringify({err: e.message});
  }
})()"""


def login_state(n):
    """三重校验登录态。True=已登录，False=未登录，None=异常/不可达。"""
    n = int(n)
    if not alive(n):
        return None
    try:
        s = S(port_of(n))
        try:
            raw = s.ev(_LOGIN_CHECK_JS, 1.5)
            if isinstance(raw, str) and raw.startswith('{'):
                d = json.loads(raw)
            else:
                return None
            url_ok = d.get('urlNoLogin', False)
            entry_ok = d.get('noLoginEntry', False)
            history_ok = d.get('hasHistory', False)
            return url_ok and entry_ok and history_ok
        finally:
            s.close()
    except Exception:
        return None


# ════════════════════════════════════════════════════════════════
# 昵称提取
# ════════════════════════════════════════════════════════════════
_NICK_JS = r"""(() => {
  var t = document.body ? (document.body.innerText || '') : '';
  var m = t.match(/([^\n]{2,20})\n(标准套餐|免费|专业版|会员|套餐)/);
  var nick = m ? m[1].trim() : '';
  var plan = m ? m[2] : '';
  if (!nick) {
    var els = Array.prototype.slice.call(document.querySelectorAll('*')).filter(function(e) {
      return e.children.length === 0 && (e.innerText||'').trim().length >= 2 && (e.innerText||'').trim().length <= 16;
    });
    var cand = els.map(function(e) {
      return {t: (e.innerText||'').trim(), y: e.getBoundingClientRect().top, x: e.getBoundingClientRect().left};
    }).filter(function(o) { return o.y > 300 && o.x < 320; });
    if (cand.length) {
      cand.sort(function(a,b) { return b.y - a.y; });
      nick = cand[0].t;
    }
  }
  return JSON.stringify({nick: nick, plan: plan});
})()"""


def nick(n):
    """读取实例昵称。返回昵称字符串或 None。"""
    n = int(n)
    if not alive(n):
        return None
    try:
        s = S(port_of(n))
        try:
            raw = s.ev(_NICK_JS, 2.0)
            if isinstance(raw, str) and raw.startswith('{'):
                d = json.loads(raw)
                return d.get('nick') or None
            return None
        finally:
            s.close()
    except Exception:
        return None


# ════════════════════════════════════════════════════════════════
# class S — CDP 会话
# ════════════════════════════════════════════════════════════════
class S(object):
    """CDP 会话包装。连接 localhost:port，找 doubao.com 标签页，没有就新建。"""

    def __init__(self, port):
        self.port = int(port)
        self.i = 0
        self.ws = None

        # 查找已有 doubao.com 标签页
        tab = None
        try:
            tabs = http(self.port, '/json/list')
            for t in tabs:
                if t.get('type') == 'page' and 'doubao.com' in (t.get('url') or ''):
                    tab = t
                    break
        except Exception:
            pass

        # 没有就新建
        if not tab:
            try:
                new_url = '/json/new?url=' + urllib.parse.quote(SITE, safe='')
                tab = http(self.port, new_url, method='PUT')
                time.sleep(4)
            except Exception as e:
                raise RuntimeError('S(%d) 无法创建标签页: %s' % (self.port, str(e)[:80]))

        if not tab or not tab.get('webSocketDebuggerUrl'):
            raise RuntimeError('S(%d) 无有效标签页 WebSocket URL' % self.port)

        # 建立 WebSocket 连接
        from websocket import create_connection
        self.ws = create_connection(
            tab['webSocketDebuggerUrl'],
            timeout=90,
            suppress_origin=True,
        )
        self.send('Runtime.enable')
        self.send('Page.enable')

    def send(self, method, params=None):
        """发送 CDP 命令并等待对应 id 的响应。"""
        self.i += 1
        msg_id = self.i
        payload = json.dumps({
            'id': msg_id,
            'method': method,
            'params': params or {},
        })
        self.ws.send(payload)
        while True:
            raw = self.ws.recv()
            r = json.loads(raw)
            if r.get('id') == msg_id:
                return r
            # 其他消息（事件通知）跳过

    def ev(self, expr, wait=0.6):
        """执行 JS 表达式（Runtime.evaluate），returnByValue=True，awaitPromise=True。"""
        r = self.send('Runtime.evaluate', {
            'expression': expr,
            'returnByValue': True,
            'awaitPromise': True,
        })
        time.sleep(wait)
        result = r.get('result', {}).get('result', {})
        return result.get('value', json.dumps(r, ensure_ascii=False)[:200])

    def ready(self, limit=25):
        """轮询 document.readyState 直到 complete，超时返回实际值。返回秒数或 -1。"""
        t0 = time.time()
        while time.time() - t0 < limit:
            try:
                state = self.ev('document.readyState', 0)
                if state == 'complete':
                    time.sleep(1.0)
                    return round(time.time() - t0, 1)
            except Exception:
                pass
            time.sleep(0.3)
        # 超时，返回当前实际状态值
        try:
            return self.ev('document.readyState', 0)
        except Exception:
            return -1

    def navigate(self, url):
        """导航到指定 URL。"""
        return self.send('Page.navigate', {'url': url})

    def click_xy(self, x, y):
        """坐标点击（必须用 Input.dispatchMouseEvent，SPA 不认 JS 合成 click）。"""
        for typ in ('mousePressed', 'mouseReleased'):
            self.send('Input.dispatchMouseEvent', {
                'type': typ,
                'x': int(x),
                'y': int(y),
                'button': 'left',
                'clickCount': 1,
            })
        time.sleep(0.3)
        return 'OK'

    def click_text(self, txt, exact=False):
        """在候选元素里找文字命中，取其中心坐标再 click_xy。返回命中的文字或空串。"""
        if exact:
            js = r"""(() => {
  var all = document.querySelectorAll('*');
  var hits = [];
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    var t = (e.innerText || '').trim();
    if (t === %s && e.children.length === 0) {
      var r = e.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) {
        hits.push({text: t, x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2),
                    w: Math.round(r.width), h: Math.round(r.height)});
      }
    }
  }
  return JSON.stringify(hits.slice(0, 6));
})()""" % json.dumps(txt, ensure_ascii=False)
        else:
            js = r"""(() => {
  var all = document.querySelectorAll('*');
  var hits = [];
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    var t = (e.innerText || '').trim();
    if (t.indexOf(%s) >= 0 && e.children.length === 0) {
      var r = e.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) {
        hits.push({text: t, x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2),
                    w: Math.round(r.width), h: Math.round(r.height)});
      }
    }
  }
  return JSON.stringify(hits.slice(0, 6));
})()""" % json.dumps(txt, ensure_ascii=False)

        try:
            raw = self.ev(js, 0.8)
            if isinstance(raw, str) and raw.startswith('['):
                arr = json.loads(raw)
            else:
                arr = []
        except Exception:
            arr = []

        if not arr:
            return ''

        # 取最后一个匹配（通常是视觉上最靠后的元素）
        hit = arr[-1]
        self.click_xy(hit['x'], hit['y'])
        return hit.get('text', txt)

    def shot(self, path=None):
        """截图落盘。path 为空时用 out_dir()/shot_<port>_<ts>.png。返回路径或 None。"""
        try:
            r = self.send('Page.captureScreenshot', {'format': 'png'})
            data = r.get('result', {}).get('data')
            if not data:
                return None
            if not path:
                path = os.path.join(
                    out_dir(),
                    'shot_%d_%s.png' % (self.port, time.strftime('%H%M%S')),
                )
            img_bytes = base64.b64decode(data)
            with open(path, 'wb') as f:
                f.write(img_bytes)
            return path
        except Exception:
            return None

    def close(self):
        """关闭 WebSocket 连接。"""
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None


# ════════════════════════════════════════════════════════════════
# 模块级常量（向后兼容：部分模块直接 import 这些名字）
# 必须在所有函数定义之后求值，才能拿到已解析的配置。
# ════════════════════════════════════════════════════════════════
DOUBAO_HOME = home()
DOUBAO_OUTDIR = out_dir()
DOUBAO_FFMPEG = (cfg().get('ffmpeg') or os.environ.get('DOUBAO_FFMPEG', '') or '')
DOUBAO_CHROME = (cfg().get('chrome') or os.environ.get('DOUBAO_CHROME', '') or '')
DOUBAO_PORT_BASE = int(cfg().get('port_base', 9230))
DOUBAO_MAX_SLOT = int(cfg().get('max_slot', 20))
