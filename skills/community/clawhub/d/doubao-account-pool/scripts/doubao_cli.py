# -*- coding: utf-8 -*-
"""doubao_cli.py — 豆包多实例工作台统一 CLI 入口
子命令: doctor | status | up | down | login | check | nick | selfcheck | visible | ask | img | img-batch | vid | vid-regrab | fetch | trim
Python 3.9+ 兼容，中文注释，UTF-8。
"""
import argparse
import importlib
import json
import os
import sys
import time
import urllib.request

# 把 scripts/ 加入 path，确保 doubao_core 可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from doubao_core import (
    cfg, home, out_dir, port_of, udd_of, pidfile, alive, down,
    status, login_state, nick, http, log, find_chrome, find_ffmpeg, SITE, S,
)

SUBCOMMANDS = [
    'doctor', 'status', 'up', 'down', 'login', 'check', 'nick',
    'selfcheck', 'visible', 'ask', 'img', 'img-batch', 'vid',
    'vid-regrab', 'fetch', 'trim',
]


def _lazy_import(module_name: str):
    """惰性导入模块，失败时返回 None 并打印 @@ERR。"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        print(f'@@ERR 模块 {module_name} 未安装: {e}')
        return None


def cmd_doctor(args):
    """诊断环境：浏览器/ffmpeg/状态目录/依赖版本/实例。"""
    c = cfg()
    chrome = find_chrome()
    ffmpeg = find_ffmpeg()
    print(f'@@HOME {home()}')
    print(f'@@OUTDIR {out_dir()}')
    print(f'@@PORT_BASE {c["port_base"]}  MAX_SLOT {c["max_slot"]}')
    print(f'@@CHROME {chrome or "NOT FOUND"}')
    print(f'@@FFMPEG {ffmpeg or "NOT FOUND"}')

    # 依赖版本
    for pkg in ['websocket', 'PIL']:
        try:
            mod = importlib.import_module(pkg)
            ver = getattr(mod, '__version__', '?')
            print(f'@@DEP {pkg} {ver}')
        except ImportError:
            print(f'@@DEP {pkg} MISSING')

    # 实例状态
    for n in range(1, c['max_slot'] + 1):
        udd = udd_of(n)
        pf = pidfile(n)
        is_alive = alive(n)
        has_profile = os.path.isdir(udd)
        has_pid = os.path.isfile(pf)
        parts = [f'@@SLOT {n} port={port_of(n)}']
        parts.append(f'profile={"YES" if has_profile else "no"}')
        parts.append(f'pidfile={"YES" if has_pid else "no"}')
        parts.append(f'alive={"YES" if is_alive else "no"}')
        if has_profile:
            parts.append(f'udd={udd}')
        print(' '.join(parts))


def cmd_status(args):
    """显示所有实例状态。"""
    deep = getattr(args, 'deep', False)
    for item in status(deep=deep):
        logged_str = 'unknown'
        if item['logged'] is True:
            logged_str = 'YES'
        elif item['logged'] is False:
            logged_str = 'no'
        print(f'@@SLOT {item["slot"]} port={item["port"]} '
              f'alive={"YES" if item["alive"] else "no"} logged={logged_str}')


def cmd_up(args):
    """启动实例浏览器。"""
    n = int(args.slot)
    if alive(n):
        print(f'@@UP slot={n} ALREADY ALIVE')
        return
    c = cfg()
    chrome = find_chrome()
    if not chrome:
        print(f'@@ERR 未找到 Chrome/Chromium/Edge')
        return
    udd = udd_of(n)
    os.makedirs(udd, exist_ok=True)
    port = port_of(n)
    args_list = [
        chrome,
        f'--remote-debugging-port={port}',
        f'--user-data-dir={udd}',
        f'--window-size={c["window_width"]},{c["window_height"]}',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-background-networking',
        '--disable-sync',
        '--disable-translate',
        '--disable-extensions',
    ]
    # 额外参数
    for extra in c.get('chrome_args_extra', []):
        args_list.append(extra)
    args_list.append(SITE)

    try:
        if sys.platform == 'win32':
            proc = subprocess.Popen(args_list, creationflags=subprocess.DETACHED_PROCESS)
        else:
            proc = subprocess.Popen(args_list, start_new_session=True)
        # 写 pidfile
        pf = pidfile(n)
        os.makedirs(os.path.dirname(pf), exist_ok=True)
        with open(pf, 'w') as f:
            f.write(str(proc.pid))
        print(f'@@UP slot={n} port={port} pid={proc.pid}')
        # 等待端口就绪
        for _ in range(30):
            time.sleep(1)
            if alive(n):
                print(f'@@READY slot={n} port={port}')
                return
        print(f'@@WARN slot={n} 端口 {port} 30s 内未就绪')
    except Exception as e:
        print(f'@@ERR 启动失败: {e}')


def cmd_down(args):
    """关闭实例浏览器。"""
    n = int(args.slot)
    killed = down(n)
    print(f'@@DOWN slot={n} killed={killed}')


def cmd_login(args):
    """扫码登录。"""
    mod = _lazy_import('doubao_login')
    if mod:
        mod.cmd_login(args)


def cmd_check(args):
    """检查登录态。"""
    n = int(args.slot)
    if not alive(n):
        print(f'@@CHECK slot={n} ALIVE=NO')
        return
    try:
        s = S(port_of(n))
        r = s.ev(r"""(() => {
            const t = document.body.innerText || '';
            const hasLoginBtn = [...document.querySelectorAll('button,a,div,span')]
                .some(e => (e.innerText||'').trim() === '登录');
            const noLoginParam = location.href.indexOf('login') < 0;
            return JSON.stringify({hasLoginBtn, noLoginParam, url: location.href.slice(0,80), tlen: t.length});
        })()""", 4.0)
        s.close()
        data = json.loads(r)
        if data.get('hasLoginBtn'):
            print(f'@@CHECK slot={n} logged=NO url={data.get("url","")}')
        elif data.get('noLoginParam'):
            print(f'@@CHECK slot={n} logged=YES url={data.get("url","")}')
        else:
            print(f'@@CHECK slot={n} logged=UNKNOWN url={data.get("url","")}')
    except Exception as e:
        print(f'@@CHECK slot={n} ERR {str(e)[:120]}')


def cmd_nick(args):
    """读昵称。"""
    n = int(args.slot)
    result = nick(n)
    if result:
        print(f'@@NICK slot={n} {result}')
    else:
        print(f'@@NICK slot={n} NONE')


def cmd_selfcheck(args):
    """环境一致性自检。"""
    n = int(args.slot)
    if not alive(n):
        print(f'@@SELFCHECK slot={n} ALIVE=NO')
        return
    try:
        s = S(port_of(n))
        r = s.ev(r"""(() => {
            const r = {};
            r.webdriver = navigator.webdriver;
            r.plugins = navigator.plugins.length;
            r.langs = (navigator.languages || []).join(',');
            r.hasChrome = !!window.chrome;
            r.visibility = document.visibilityState;
            r.hasFocus = document.hasFocus();
            r.dpr = window.devicePixelRatio;
            r.screen = screen.width + 'x' + screen.height;
            r.outer = window.outerWidth + 'x' + window.outerHeight;
            r.inner = window.innerWidth + 'x' + window.innerHeight;
            r.url = location.href.slice(0, 60);
            const ed = document.querySelector('.tiptap.ProseMirror');
            r.editor = !!ed;
            r.sendBtn = !!document.getElementById('flow-end-msg-send');
            return JSON.stringify(r);
        })()""", 1.5)
        s.close()
        data = json.loads(r)
        for k, v in data.items():
            print(f'@@SELFCHECK slot={n} {k}={v}')
    except Exception as e:
        print(f'@@SELFCHECK slot={n} ERR {str(e)[:120]}')


def cmd_visible(args):
    """修复可见性。"""
    n = int(args.slot)
    if not alive(n):
        print(f'@@VISIBLE slot={n} ALIVE=NO')
        return
    try:
        s = S(port_of(n))
        r = s.ev(r"""(() => JSON.stringify({
            vis: document.visibilityState,
            focus: document.hasFocus(),
            outer: window.outerWidth + 'x' + window.outerHeight,
            inner: window.innerWidth + 'x' + window.innerHeight
        }))()""", 1.0)
        print(f'@@VISIBLE slot={n} BEFORE {r}')
        s.send('Page.bringToFront')
        time.sleep(1.5)
        r2 = s.ev(r"""(() => JSON.stringify({
            vis: document.visibilityState,
            focus: document.hasFocus(),
            outer: window.outerWidth + 'x' + window.outerHeight
        }))()""", 1.0)
        print(f'@@VISIBLE slot={n} AFTER {r2}')
        s.close()
    except Exception as e:
        print(f'@@VISIBLE slot={n} ERR {str(e)[:120]}')


def cmd_ask(args):
    """在豆包发消息并取回复。"""
    n = int(args.slot)
    msg = args.message
    if not alive(n):
        print(f'@@ERR slot={n} ALIVE=NO')
        return
    try:
        s = S(port_of(n))
        # 输入消息
        js_input = r"""(() => {
            const ed = document.querySelector('.tiptap.ProseMirror');
            if (!ed) return 'NO_EDITOR';
            ed.focus();
            ed.innerHTML = '<p>%s</p>';
            ed.dispatchEvent(new Event('input', {bubbles: true}));
            return 'INPUT_OK';
        })()""" % msg.replace("'", "\\'").replace('<', '&lt;')
        r = s.ev(js_input, 1.0)
        print(f'@@INPUT slot={n} {r}')
        time.sleep(0.5)
        # 点发送按钮
        r2 = s.ev(r"""(() => {
            const btn = document.getElementById('flow-end-msg-send');
            if (!btn) return 'NO_SEND_BTN';
            btn.click();
            return 'SENT';
        })()""", 2.0)
        print(f'@@SEND slot={n} {r2}')
        # 等待回复
        time.sleep(8)
        r3 = s.ev(r"""(() => {
            const msgs = document.querySelectorAll('[class*=message],[class*=Message]');
            const last = msgs[msgs.length - 1];
            return last ? last.innerText.slice(0, 500) : 'NO_REPLY';
        })()""", 2.0)
        print(f'@@REPLY slot={n} {(r3 or "")[:500]}')
        s.close()
    except Exception as e:
        print(f'@@ERR slot={n} {str(e)[:200]}')


def _delegate(subcmd, module_name, rest):
    """把子命令原样转给持有参数定义的模块（模块是各自命令行的唯一真源）。"""
    mod = _lazy_import(module_name)
    if not mod or not hasattr(mod, 'main'):
        return
    # 手写参数解析的模块（未引 argparse）不认 --help，原样转发会退化成「缺参」报错；
    # 这类模块在派发层就地打印它自带的 USAGE。模块依旧是各自命令行的唯一真源。
    if rest and rest[0] in ('-h', '--help'):
        if not hasattr(mod, 'argparse') and getattr(mod, 'USAGE', None):
            print(mod.USAGE)
            return
    sys.argv = [module_name, subcmd] + list(rest)
    mod.main()


def cmd_trim(args):
    """trim --slot N [--keep K]：关掉该实例多余的标签页，只留 K 个（默认 1）。"""
    n = int(args.slot)
    keep = int(getattr(args, 'keep', 1) or 1)
    if keep < 1:
        keep = 1
    if not alive(n):
        print(f'@@TRIM slot={n} ALIVE=NO')
        return
    port = port_of(n)
    try:
        targets = http(port, '/json/list')
    except Exception as e:
        print(f'@@TRIM slot={n} ERR {str(e)[:120]}')
        return
    pages = [t for t in targets if t.get('type') == 'page']
    pages.sort(key=lambda t: t.get('id', ''))
    closed = 0
    for t in pages[keep:]:
        tid = t.get('id')
        if not tid:
            continue
        try:
            urllib.request.urlopen(
                'http://127.0.0.1:%d/json/close/%s' % (port, tid), timeout=5).read()
            closed += 1
        except Exception:
            pass
    print(f'@@TRIM slot={n} closed={closed} kept={min(keep, len(pages))}')


# 这些子命令的参数由子模块自己定义，必须原样转发（模块是各自命令行的唯一真源）
DELEGATE = {
    'img': 'doubao_image',
    'img-batch': 'doubao_image',
    'vid': 'doubao_video',
    'vid-regrab': 'doubao_video',
    'fetch': 'doubao_fetch',
}


def main():
    argv = sys.argv[1:]
    if argv and argv[0] in DELEGATE:
        _delegate(argv[0], DELEGATE[argv[0]], argv[1:])
        return
    parser = argparse.ArgumentParser(
        prog='doubao_cli',
        description='豆包多实例工作台 CLI — 配置驱动、可移植',
    )
    sub = parser.add_subparsers(dest='command', help='可用子命令')

    # doctor
    sub.add_parser('doctor', help='诊断环境')

    # status
    p_status = sub.add_parser('status', help='实例状态')
    p_status.add_argument('--deep', action='store_true', help='深度检查（含登录态）')

    # up
    p_up = sub.add_parser('up', help='启动实例')
    p_up.add_argument('slot', help='实例编号')

    # down
    p_down = sub.add_parser('down', help='关闭实例')
    p_down.add_argument('slot', help='实例编号')

    # login
    p_login = sub.add_parser('login', help='扫码登录')
    p_login.add_argument('slot', help='实例编号')
    p_login.add_argument('--out', help='二维码输出路径')

    # check
    p_check = sub.add_parser('check', help='检查登录态')
    p_check.add_argument('slot', help='实例编号')

    # nick
    p_nick = sub.add_parser('nick', help='读昵称')
    p_nick.add_argument('slot', help='实例编号')

    # selfcheck
    p_selfcheck = sub.add_parser('selfcheck', help='环境一致性自检')
    p_selfcheck.add_argument('slot', help='实例编号')

    # visible
    p_visible = sub.add_parser('visible', help='修复可见性')
    p_visible.add_argument('slot', help='实例编号')

    # ask
    p_ask = sub.add_parser('ask', help='发消息')
    p_ask.add_argument('slot', help='实例编号')
    p_ask.add_argument('message', help='消息内容')

    # 惰性模块：参数由各自模块定义，main() 里原样转发（见 _delegate / DELEGATE）
    sub.add_parser('img', help='图像生成（参数见：doubao_cli.py img --help）')
    sub.add_parser('img-batch', help='批量图像生成（参数见：doubao_cli.py img-batch --help）')
    sub.add_parser('vid', help='视频生成（参数见：doubao_cli.py vid --help）')
    sub.add_parser('vid-regrab', help='视频重抓（参数见：doubao_cli.py vid-regrab --help）')
    sub.add_parser('fetch', help='数据抓取（参数见：doubao_cli.py fetch --help）')
    p_trim = sub.add_parser('trim', help='关掉多余标签页')
    p_trim.add_argument('slot', help='实例编号')
    p_trim.add_argument('--keep', type=int, default=1, help='保留的标签页数（默认 1）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cmd_map = {
        'doctor': cmd_doctor,
        'status': cmd_status,
        'up': cmd_up,
        'down': cmd_down,
        'login': cmd_login,
        'check': cmd_check,
        'nick': cmd_nick,
        'selfcheck': cmd_selfcheck,
        'visible': cmd_visible,
        'ask': cmd_ask,
        'trim': cmd_trim,
    }

    handler = cmd_map.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    import subprocess  # 延迟导入，up 命令需要
    main()
