#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""batch_fetch.py —— 按维度批量取数（一次 Bash 调用覆盖一个维度的全部接口）

存在理由（两条，缺一不可）：
  1. UI：workflow 连续发出 25 次 callTool('Bash')，平台会自动聚合成「执行 25 个步骤」步骤组，
     长列表淹没会话。合并成「每维度一次」后降到 ≤7 条，卡片少到不成组即可缓解。
  2. 截断安全：平台对单条 tool_result 有约 2~3 万字符的截断（按字符硬砍），砍出来的 JSON 残缺。
     单接口一卡时，一条被砍只毁一个接口；合并后一条被砍会毁整个维度，因此**必须**在本脚本内
     强制「信封级共享预算」，把整条 stdout 压在阈值之下，让平台的截断永不触发。

设计要点（与 wf_capture.py 的分工）：
  - 全量原始响应仍然逐接口落盘（`<out-dir>/_wf*.json`），只有摘要进 stdout —— 与 dataCapture
    的「引用传递」口径完全一致（见《店铺体检渲染进程卡死修复方案》3.3）。
  - 摘要规则直接复用 wf_capture.py 的 `_summarize`（单一真相），只是每个任务可各带 array_cap：
    广告明细类接口（/ad/item、/ad/customer）50 条就要 2 万字符以上，必须单独收紧。
  - 落盘文件名必须是 `_wf*.json` 且落在 `hc_run_<runId>` 目录内，否则 workflow 侧 cleanupRunDir
    的 `-name "_wf*.json"` 清不到 → 临时文件泄漏。

调用形式：
    python3 batch_fetch.py --out-dir <落盘目录绝对路径> --spec <JSON>

spec 以纯 JSON 作为命令行参数传入（与 freedom CLI 的 --params 同一条路径，已在双平台验证）。
argv 一律由 workflow 侧构造，本脚本只执行不拼参 —— 例如 rag_query 不得带 --NEWTON_SHOP_LOGIN_ID
这类特例必须留在 workflow 侧收口，避免参数逻辑两边各存一份而漂移：
    {
      "budget": 20000,          # 信封字符预算（整条 stdout 上限）
      "task_timeout": 100,      # 单接口硬超时（秒）
      "deadline": 150,          # 全批总 deadline（秒），必须 < workflow 侧 Bash timeout
      "tasks": [
        {"key": "trafficTrend", "argv": ["/abs/cli.py", "alibaba.1688.get.traffic.trend", "--days", "7"],
         "array_cap": 50}
      ]
    }

stdout（恒为合法 JSON，无论内部发生什么）：
    {"results": {key: <叶子>}, "__hc_batch": {...排障元信息...}}

叶子形状与 workflow 侧 parseCliOutput 的产出逐字一致（success/data/error/markdown/__hc_src），
下游 compactShopData 的 `'success' in value` 判定与 buildDataManifest 的 `__hc_src` 收集均不受影响。
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wf_capture import _summarize, ARRAY_CAP, RAW_CAP  # noqa: E402  摘要规则单一真相

DEFAULT_BUDGET = 20000     # 信封字符预算；来源为平台 tool_result 截断阈值 2~3 万字符的下界
DEFAULT_TASK_TIMEOUT = 100
DEFAULT_DEADLINE = 150
MIN_ARRAY_CAP = 5          # 降级时数组条数的下限，再小就直接丢 data
MAX_DEGRADE_ROUNDS = 40    # 降级循环硬上限，防御性护栏（正常路径远达不到）
TRUNCATED_ERR = '响应不是合法 JSON（疑似被截断），本项数据暂不可用'
OMIT_NOTE = '信封超出字符预算，本项明细已省略；完整数据见 __hc_src.file'


def _leaf_from_raw(raw_bytes, path, array_cap):
    """把一个接口的原始 stdout 转成叶子。

    等价链路 = wf_capture.py（摘要 + __hc_src）→ parseCliOutput 的 JSON 成功分支（解包 + 回填），
    两步顺序不可颠倒。摘要只截断数组与长字符串，不改字典结构，故不影响解包判定。
    """
    text = raw_bytes.decode('utf-8', 'replace')
    try:
        parsed = json.loads(text)
    except Exception:
        # 非 JSON：以 { 或 [ 开头却解析不了 → 极可能是被截断的 JSON，必须判失败而不是「成功但没数据」，
        # 否则一次数据丢失会被标成 success，静默进入分析与报告。其余情况是接口的纯文本响应，按原样透传。
        stripped = text.strip()
        if stripped[:1] in ('{', '['):
            return {'success': False, 'error': TRUNCATED_ERR, 'data': {}}
        return {'success': True, 'markdown': text[:RAW_CAP], 'data': {}}

    if not isinstance(parsed, dict):
        # CLI 正常态恒为对象；非对象时只做摘要、不附加 __hc_src（对齐 wf_capture.py）
        return {'success': True, 'data': _summarize(parsed, '', [], array_cap)}

    caps = []
    leaf = _summarize(parsed, '', caps, array_cap)
    leaf['__hc_src'] = {'file': path, 'bytes': len(raw_bytes), 'caps': caps}

    # ↓ parseCliOutput 的 JSON 成功分支：单层解包 data.data + error 回填
    inner = leaf.get('data')
    if isinstance(inner, dict) and 'data' in inner:
        leaf['data'] = inner['data']
    if not leaf.get('success') and not leaf.get('error'):
        markdown = leaf.get('markdown') or ''
        leaf['error'] = markdown[1:].strip() if markdown.startswith('❌') else (markdown or '未知错误')
    return leaf


def _run_task(task, out_dir, task_timeout):
    """执行单个接口：落盘全量 → 产出叶子。任何异常都收敛成失败叶子，绝不向上抛。"""
    key = task.get('key') or '?'
    argv = task.get('argv') or []
    array_cap = int(task.get('array_cap') or ARRAY_CAP)
    fname = '_wf%d%s.json' % (int(time.time() * 1000), os.urandom(3).hex())
    path = os.path.join(out_dir, fname)
    try:
        proc = subprocess.run(
            [sys.executable or 'python3'] + [str(a) for a in argv],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=task_timeout,
        )
    except subprocess.TimeoutExpired:
        return key, {'success': False, 'error': '取数超时（%d 秒）' % task_timeout,
                     'command': key, 'data': {}}, ''
    except Exception as exc:
        return key, {'success': False, 'error': '取数进程异常：%r' % (exc,),
                     'command': key, 'data': {}}, ''

    # 全量原始响应先落盘：报告链路（merge_shop_data.py）按 __hc_src.file 读它，绝不依赖 stdout
    try:
        with open(path, 'wb') as f:
            f.write(proc.stdout)
    except Exception:
        path = ''

    stderr_head = proc.stderr.decode('utf-8', 'replace')[:300].strip()
    if proc.returncode != 0:
        return key, {'success': False, 'error': stderr_head or '退出码 %d' % proc.returncode,
                     'command': key, 'data': {}}, stderr_head
    if not path:
        # 落盘失败：叶子不带 __hc_src，报告链路会原样内联摘要（有损但不静默）
        leaf = _leaf_from_raw(proc.stdout, '', array_cap)
        leaf.pop('__hc_src', None)
        return key, leaf, stderr_head
    return key, _leaf_from_raw(proc.stdout, path, array_cap), stderr_head


def _chars(obj):
    return len(json.dumps(obj, ensure_ascii=False))


def _apply_budget(results, caps_by_key, budget):
    """信封级共享预算：总字符超预算时，逐轮挑最大的叶子降级，直到达标或无可再降。

    降级顺序刻意是「最大者优先减半」而非按比例均摊：多个中等叶子（如询盘维度）时损失最小，
    单个巨无霸叶子（如广告明细）时又能快速收敛。
    """
    degraded = []
    for _ in range(MAX_DEGRADE_ROUNDS):
        total = _chars(results)
        if total <= budget:
            break
        ranked = sorted(results.items(), key=lambda kv: -_chars(kv[1]))
        victim = None
        for key, leaf in ranked:
            if isinstance(leaf, dict) and leaf.get('data') not in (None, {}, []):
                victim = key
                break
        if victim is None:
            break
        cur_cap = caps_by_key.get(victim, ARRAY_CAP)
        src = results[victim].get('__hc_src')
        if cur_cap > MIN_ARRAY_CAP and src and src.get('file'):
            new_cap = max(MIN_ARRAY_CAP, cur_cap // 2)
            caps_by_key[victim] = new_cap
            try:
                with open(src['file'], 'rb') as f:
                    results[victim] = _leaf_from_raw(f.read(), src['file'], new_cap)
                degraded.append('%s:cap=%d' % (victim, new_cap))
                continue
            except Exception:
                pass
        # 无法再收紧（无源文件 / 已到下限）→ 丢 data，只留判定位与文件路径
        slim = {'success': results[victim].get('success'), 'error': results[victim].get('error'),
                '__hc_note': OMIT_NOTE}
        if src:
            slim['__hc_src'] = src
        results[victim] = slim
        degraded.append('%s:data-omitted' % victim)
    return degraded


def main():
    parser = argparse.ArgumentParser(description='按维度批量取数（摘要回信封，全量落磁盘）')
    parser.add_argument('--out-dir', required=True, help='落盘目录绝对路径')
    parser.add_argument('--spec', required=True, help='spec JSON')
    opts = parser.parse_args()

    spec = json.loads(opts.spec)
    tasks = spec.get('tasks') or []
    budget = int(spec.get('budget') or DEFAULT_BUDGET)
    task_timeout = int(spec.get('task_timeout') or DEFAULT_TASK_TIMEOUT)
    deadline = int(spec.get('deadline') or DEFAULT_DEADLINE)

    out_dir = opts.out_dir
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception:
        pass

    started = time.time()
    results = {}
    caps_by_key = {}
    stderrs = {}
    for t in tasks:
        caps_by_key[t.get('key') or '?'] = int(t.get('array_cap') or ARRAY_CAP)

    # 全接口同时启动：与改造前 workflow 侧 parallel 的并发度一致，墙上时间不退化
    with ThreadPoolExecutor(max_workers=max(1, len(tasks))) as pool:
        futures = [pool.submit(_run_task, t, out_dir, task_timeout) for t in tasks]
        for fut in futures:
            left = deadline - (time.time() - started)
            try:
                key, leaf, err = fut.result(timeout=max(1, left))
            except Exception as exc:
                # 单个任务拖过总 deadline：只标它自己不可用，其余照常回传（失败半径守在接口级）
                key, leaf, err = '?', {'success': False, 'error': '取数未在时限内完成：%r' % (exc,),
                                       'data': {}}, ''
            results[key] = leaf
            if err:
                stderrs[key] = err

    # 未返回任何结果的 key 补占位，保证 results 的键集合与 spec 完全对应（下游按 key 取值不会拿到 undefined）
    for t in tasks:
        k = t.get('key') or '?'
        if k not in results:
            results[k] = {'success': False, 'error': '取数未返回结果', 'command': k, 'data': {}}

    degraded = _apply_budget(results, caps_by_key, budget)
    envelope = {
        'results': results,
        '__hc_batch': {
            'tasks': len(tasks),
            'chars': _chars(results),
            'budget': budget,
            'elapsed': round(time.time() - started, 2),
            'degraded': degraded,
            'stderr': stderrs,
        },
    }
    sys.stdout.write(json.dumps(envelope, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # 强制兜底：信封必须是合法 JSON，否则 workflow 侧 JSON.parse 失败 → 整个维度静默报废。
        # 这里宁可回一个「全部失败」的信封，也不能让 traceback 顶进 stdout。
        sys.stderr.write('[batch_fetch] fatal: %r\n' % (exc,))
        sys.stdout.write(json.dumps({
            'results': {},
            '__hc_batch': {'fatal': '%r' % (exc,)},
        }, ensure_ascii=False))
    sys.exit(0)
