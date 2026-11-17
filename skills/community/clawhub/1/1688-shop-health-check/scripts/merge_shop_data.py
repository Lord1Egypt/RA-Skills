#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_shop_data.py —— 按 manifest 在磁盘侧合并可视化数据文件

读 manifest（stdin），按路径加载全量原始响应，套用 workflow 侧 normalizeForViz 的等价规则，
产出与改造前**结构完全一致**的可视化数据文件。全量业务数据只在磁盘与本脚本之间流动，
不进会话通道。设计依据：《店铺体检渲染进程卡死修复方案》3.2 / 第四章。

调用形式：python3 <skillDir>/scripts/merge_shop_data.py --output <输出文件绝对路径>
         manifest 由 callTool('Bash', { stdinJson: manifest }) 从 stdin 传入。

manifest 结构：allShopData 的骨架副本，其中每个「已成功解析为 JSON」的取数叶子被整体替换为
`{ "__hc_load": "<绝对路径>" }`（不携带任何标量）；无 __hc_src 的叶子原样内联。

执行顺序不可颠倒：先按 4.2 从原始文件重建每个叶子（键序即 CLI 原始响应键序，保证与改造前
逐字节等价），再按 4.1 对整个 shop 对象做一次 _normalize_value。

⚠️ 红线：本脚本**绝不截断**任何数组或字符串，也不砍深度、不丢 meta 键与兄弟键——
截断只属于 wf_capture.py（服务分析路径）。审查判据：本文件中出现任何切片截断（如 50 条
数组上限、2000 字符串上限）即为错误。
若改动 workflow 侧 normalizeForViz 语义，必须同步改本脚本，否则两侧实现漂移。
"""

import argparse
import json
import re
import sys

LOAD_KEY = '__hc_load'
MISSING_LEAF = {'success': False, 'error': '数据文件缺失或解析失败', 'data': {}}
_ERR_PREFIX = re.compile(r'^❌\s*')


def _rebuild_leaf(raw):
    """叶子重建 ← parseCliOutput 的 JSON 成功分支（对照修复方案 4.2）。

    1. 单层解包：parsed.data 是对象且含 data 键 → parsed.data = parsed.data['data']；
       必须就地改写已有键（不得删后重建），否则键序变动、逐字节比对失败；只解一层。
    2. !success && !error → error = markdown 去首部 '❌ '，为空则 '未知错误'（尾部新增键）。
    3. 返回 raw 本体，不新建对象、不添加 command 键（command 仅存于非 JSON 失败分支）。
    """
    if not isinstance(raw, dict):
        return raw
    inner = raw.get('data')
    if isinstance(inner, dict) and 'data' in inner:
        raw['data'] = inner['data']
    if not raw.get('success') and not raw.get('error'):
        raw['error'] = _ERR_PREFIX.sub('', raw.get('markdown') or '') or '未知错误'
    return raw


def _load_refs(node):
    """深度遍历 manifest，遇到只含 __hc_load 的对象 → 读文件并重建为完整叶子。"""
    if isinstance(node, dict):
        if len(node) == 1 and LOAD_KEY in node:
            path = node[LOAD_KEY]
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
            except Exception:
                return dict(MISSING_LEAF)
            return _rebuild_leaf(raw)
        return dict((k, _load_refs(v)) for k, v in node.items())
    if isinstance(node, list):
        return [_load_refs(v) for v in node]
    return node


def _normalize_value(val):
    """无损规整 ← workflow 侧 normalizeForViz / _normalizeValue（对照修复方案 4.1）。

    只做两件零丢失的事：
      1. value 是可解析的 JSON 文本（trim 后以 { 或 [ 开头且解析结果为对象/数组）→ 递归替换；
      2. 仅当 data 是对象唯一键时解包 { data: X }（无兄弟键可丢 → 无损）。
    绝不做：丢 meta 键、丢兄弟键、砍深度、截断数组与字符串。
    wikiContext 等中文纯文本落在规则 1 的「非 {[ 开头」分支，原样透传。
    """
    if val is None:
        return val
    if isinstance(val, str):
        t = val.strip()
        if len(t) > 1 and t[0] in ('{', '['):
            try:
                parsed = json.loads(t)
            except Exception:
                parsed = None
            if isinstance(parsed, (dict, list)):
                return _normalize_value(parsed)
        return val
    if isinstance(val, list):
        return [_normalize_value(v) for v in val]
    if not isinstance(val, dict):
        return val
    # 仅当 data 是唯一键时解包；有兄弟键则原样保留全部键（这是保真的核心）
    cur = val
    while isinstance(cur, dict) and len(cur) == 1 and 'data' in cur:
        cur = cur['data']
    if cur is not val:
        return _normalize_value(cur)
    return dict((k, _normalize_value(v)) for k, v in val.items())


def main():
    parser = argparse.ArgumentParser(description='按 manifest 合并店铺诊断数据文件')
    parser.add_argument('--output', required=True, help='输出文件绝对路径')
    opts = parser.parse_args()

    manifest = json.load(sys.stdin)
    shops_in = manifest.get('shops') if isinstance(manifest, dict) else None
    if not isinstance(shops_in, list):
        shops_in = []

    shops_out = []
    for shop in shops_in:
        rebuilt = _load_refs(shop)
        shops_out.append({
            'shopName': rebuilt.get('shopName') if isinstance(rebuilt, dict) else '',
            'loginId': rebuilt.get('loginId') if isinstance(rebuilt, dict) else '',
            'data': _normalize_value(rebuilt),
        })

    # 序列化口径与改造前的内联写入脚本逐字一致（不加 separators），保证文件格式不变
    with open(opts.output, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'shops': shops_out}, ensure_ascii=False))
    print('OK')


if __name__ == '__main__':
    main()
