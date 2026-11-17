#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wf_capture.py —— 取数结果「摘要 + 文件引用」回灌脚本

替代 buildBashCommand（dataCapture 分支）命令末尾的 `cat`：把已落盘的 CLI 输出
转成「摘要 + 文件路径」打到 stdout，使全量业务数据不再以值传递方式进入会话通道。
设计依据：《店铺体检渲染进程卡死修复方案》3.1 / 3.8。

调用形式：python3 <skillDir>/scripts/wf_capture.py <落盘文件绝对路径>

行为要点（按顺序判定，无分支歧义）：
  0. 最外层 try/except 强制兜底：任何内部异常 → 退化为原样打印文件内容（等价于 cat），
     stderr 记一行，退出码 0。stdout 会直接成为 workflow 侧 parseCliOutput 的解析对象，
     若此处抛 traceback，traceback 会顶替摘要进入 stdout → 一次成功取数被静默降级。
  1. 读文件失败 → 打印空串，退出码 0（错误由已有的 exitCode / stderr 链路承载）。
  2. 非 JSON → 打印前 8192 字节，不附加 __hc_src。
  3. JSON → 递归摘要（数组 > 50 取前 50；字符串 > 2000 截断加 '...'），其余键 / 嵌套深度 /
     数值一律不动；口径刻意对齐 workflow 侧 _compactValue，不引入分析行为漂移。
  4. 顶层附加 __hc_src = { file, bytes, caps }；caps 仅用于排障与日志，不面向分析 LLM。
  5. 序列化后 > 262144 字节 → 丢弃 data，仅回标量 + __hc_src + __hc_note，并 stderr 告警。

注意：本脚本做截断（仅服务分析路径），merge_shop_data.py 绝不截断（服务报告保真），
两者职责严格分离，不得互相搬运逻辑。

`_summarize` 同时被 batch_fetch.py 直接 import 复用（摘要规则单一真相，避免两份实现漂移）；
那里需要按接口收紧数组条数，故 array_cap 做成可选参数，缺省时行为与本脚本原先逐字相同。
"""

import json
import os
import sys

ARRAY_CAP = 50        # 摘要数组上限，对齐 _compactValue 的 slice(0, 50)
STRING_CAP = 2000     # 摘要字符串上限，对齐 _compactValue
RAW_CAP = 8192        # 非 JSON 响应透传上限（字节）
PAYLOAD_CAP = 262144  # 摘要总字节硬上限（256 KB），最后兜底，正常路径不触发
OMIT_NOTE = 'payload 超过 256KB 上限，已省略；完整数据见 __hc_src.file'


def _summarize(val, path, caps, array_cap=ARRAY_CAP):
    """递归生成摘要副本：只截断数组与长字符串，不动其余键、嵌套深度与数值。

    摘要不做排序，保持与 _compactValue 现行「首 N 条」语义一致（榜单类接口由 API 侧已排序）。
    array_cap 缺省即模块级 ARRAY_CAP；batch_fetch.py 对广告明细类接口传更小的值。
    """
    if isinstance(val, dict):
        return dict(
            (k, _summarize(v, (path + '.' + k) if path else k, caps, array_cap))
            for k, v in val.items()
        )
    if isinstance(val, list):
        kept = val
        if len(val) > array_cap:
            caps.append({'path': path or '$', 'total': len(val), 'kept': array_cap})
            kept = val[:array_cap]
        item_path = (path or '$') + '[]'
        return [_summarize(v, item_path, caps, array_cap) for v in kept]
    if isinstance(val, str) and len(val) > STRING_CAP:
        caps.append({'path': path or '$', 'total': len(val), 'kept': STRING_CAP})
        return val[:STRING_CAP] + '...'
    return val


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else ''
    try:
        with open(src, 'rb') as f:
            raw_bytes = f.read()
    except Exception:
        # 读失败不得影响主流程判定：打印空串，错误由 exitCode / stderr 链路承载
        sys.stdout.write('')
        return

    text = raw_bytes.decode('utf-8', 'replace')
    try:
        parsed = json.loads(text)
    except Exception:
        # 非 JSON（错误态 / 纯文本）：透传前 8192 字节，不附加 __hc_src → 合并时原样内联
        sys.stdout.write(raw_bytes[:RAW_CAP].decode('utf-8', 'replace'))
        return

    caps = []
    if not isinstance(parsed, dict):
        # CLI 正常态恒为对象；非对象时只做摘要、不附加 __hc_src（避免截断后的 JSON 反而无法解析）
        sys.stdout.write(json.dumps(_summarize(parsed, '', caps), ensure_ascii=False))
        return

    summary = _summarize(parsed, '', caps)
    src_ref = {'file': os.path.abspath(src), 'bytes': len(raw_bytes), 'caps': caps}
    summary['__hc_src'] = src_ref
    out = json.dumps(summary, ensure_ascii=False)
    if len(out.encode('utf-8')) > PAYLOAD_CAP:
        sys.stderr.write('[wf_capture] payload over %d bytes, data omitted: %s\n' % (PAYLOAD_CAP, src))
        out = json.dumps({
            'success': parsed.get('success'),
            'error': parsed.get('error'),
            '__hc_src': src_ref,
            '__hc_note': OMIT_NOTE,
        }, ensure_ascii=False)
    sys.stdout.write(out)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:  # 强制兜底：最坏情况等于改造前行为（全量回灌），不产生新的数据失真路径
        sys.stderr.write('[wf_capture] fallback to raw passthrough: %r\n' % (exc,))
        try:
            with open(sys.argv[1], 'rb') as f:
                sys.stdout.buffer.write(f.read())
        except Exception:
            pass
    sys.exit(0)
