# -*- coding: utf-8 -*-
"""doubao_dom.py — 豆包页面探查三件套
clicktext（按文字点元素）、shot（截图落盘）、ax（AX 控件清单）、dismiss（关弹窗）。
Python 3.9+ 兼容，中文注释，UTF-8。
"""
import json
import os
import sys
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doubao_core import cfg, out_dir, port_of, S

# ---------------------------------------------------------------------------
# 弹窗关闭 JS
# ---------------------------------------------------------------------------
KILL_JS = r"""(() => {
  const vis = e => {
    const r = e.getBoundingClientRect();
    const st = getComputedStyle(e);
    return r.width > 4 && r.height > 4 && st.visibility !== 'hidden' && st.display !== 'none' && st.opacity !== '0';
  };
  const t = document.body.innerText || '';
  const hasModal = /下载电脑版|安全确认|充分授权|了解并继续|下次提醒我|我知道了|跳过/.test(t);
  if (!hasModal) return JSON.stringify({n: 0, hit: 'NONE'});
  let n = 0, hit = [];
  const kws = ['下次提醒我', '我知道了', '跳过', '暂不', '取消引导', '了解并继续'];
  for (const e of document.querySelectorAll('button,div[role=button],span,div,a')) {
    const tx = (e.innerText || '').trim();
    if (!kws.includes(tx)) continue;
    if (!vis(e)) continue;
    try { e.click(); n++; hit.push(tx); } catch (err) {}
  }
  const cands = [...document.querySelectorAll('button,div[role=button],svg,div')].filter(e => {
    const r = e.getBoundingClientRect();
    if (!vis(e)) return false;
    if (r.width > 60 || r.height > 60 || r.width < 14) return false;
    if (r.y > window.innerHeight * 0.8) return false;
    return true;
  });
  const xs = cands.filter(e => !(e.innerText || '').trim() && e.querySelector('svg'));
  xs.sort((a, b) => a.getBoundingClientRect().y - b.getBoundingClientRect().y);
  for (const e of xs.slice(0, 3)) {
    const r = e.getBoundingClientRect();
    if (r.y < 40) continue;
    try { e.click(); n++; hit.push('X@' + Math.round(r.x) + ',' + Math.round(r.y)); } catch (err) {}
  }
  if (n === 0) {
    try {
      document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', keyCode: 27, bubbles: true}));
      n++; hit.push('ESC');
    } catch (err) {}
  }
  return JSON.stringify({n: n, hit: hit});
})()"""


def clicktext(n: int, txt: str, exact: bool = False) -> str:
    """按可见文本点元素。返回 @@ 短行。"""
    try:
        s = S(port_of(n))
        r = s.click_text(txt, exact=exact)
        s.close()
        return f'@@CLICKTEXT slot={n} {r}'
    except Exception as e:
        return f'@@ERR slot={n} {str(e)[:120]}'


def shot(n: int, path: str = None) -> str:
    """截图落盘。返回 @@ 短行。"""
    try:
        s = S(port_of(n))
        if not path:
            path = os.path.join(out_dir(), f'shot_{n}_{int(time.time())}.png')
        result = s.shot(path)
        s.close()
        if result:
            return f'@@SHOT slot={n} {result} {os.path.getsize(result)}'
        return f'@@NOSHOT slot={n}'
    except Exception as e:
        return f'@@ERR slot={n} {str(e)[:120]}'


def ax(n: int, limit: int = 30) -> str:
    """CDP Accessibility.getFullAXTree 取控件清单。
    在 Python 里过滤后只回前 limit 条 @@ 短行，绝不打印全文。
    """
    try:
        s = S(port_of(n))
        r = s.send('Accessibility.getFullAXTree')
        nodes = r.get('result', {}).get('nodes', [])
        s.close()

        # 过滤：只保留有名称且可见的节点
        filtered = []
        for node in nodes:
            name = node.get('name', {})
            if isinstance(name, dict):
                name_val = name.get('value', '')
            else:
                name_val = str(name)
            if not name_val or len(name_val) > 80:
                continue
            role = node.get('role', {})
            if isinstance(role, dict):
                role_val = role.get('value', '')
            else:
                role_val = str(role)
            if not role_val:
                continue
            filtered.append({
                'role': role_val,
                'name': name_val[:60],
                'id': node.get('backendDOMNodeId', ''),
            })

        lines = [f'@@AX slot={n} total={len(nodes)} shown={min(len(filtered), limit)}']
        for item in filtered[:limit]:
            lines.append(f'  {item["role"]}: {item["name"]}')
        return '\n'.join(lines)
    except Exception as e:
        return f'@@ERR slot={n} {str(e)[:120]}'


def dismiss(n: int, loops: int = 4) -> str:
    """关弹窗/模态。返回 @@ 短行。"""
    try:
        s = S(port_of(n))
        total = 0
        for i in range(loops):
            try:
                r = s.ev(KILL_JS, 2.0)
                d = json.loads(r) if isinstance(r, str) and r.startswith('{') else {}
            except Exception:
                d = {}
            cnt = int(d.get('n') or 0)
            total += cnt
            time.sleep(1.5)
            if cnt == 0 and i >= 1:
                break
        tail = s.ev(
            r"""(() => {
                const t = document.body.innerText || '';
                return /下载电脑版|安全确认|下次提醒我/.test(t) ? t.slice(0, 120) : 'CLEAN';
            })()""", 1.5
        )
        s.close()
        return f'@@DISMISS slot={n} n={total} still={(tail or "")[:120]}'
    except Exception as e:
        return f'@@ERR slot={n} {str(e)[:120]}'


# ---------------------------------------------------------------------------
# CLI 入口（方便单独调试）
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='豆包页面探查工具')
    sub = parser.add_subparsers(dest='action')
    p_ct = sub.add_parser('clicktext', help='按文字点击')
    p_ct.add_argument('slot', type=int)
    p_ct.add_argument('txt')
    p_ct.add_argument('--exact', action='store_true')
    p_shot = sub.add_parser('shot', help='截图')
    p_shot.add_argument('slot', type=int)
    p_shot.add_argument('--out', default=None)
    p_ax = sub.add_parser('ax', help='控件清单')
    p_ax.add_argument('slot', type=int)
    p_ax.add_argument('--limit', type=int, default=30)
    p_dis = sub.add_parser('dismiss', help='关弹窗')
    p_dis.add_argument('slot', type=int)
    p_dis.add_argument('--loops', type=int, default=4)
    args = parser.parse_args()
    if args.action == 'clicktext':
        print(clicktext(args.slot, args.txt, exact=args.exact))
    elif args.action == 'shot':
        print(shot(args.slot, args.out))
    elif args.action == 'ax':
        print(ax(args.slot, limit=args.limit))
    elif args.action == 'dismiss':
        print(dismiss(args.slot, loops=args.loops))
    else:
        parser.print_help()
