# -*- coding: utf-8 -*-
# type_tokens.py —— 引擎产物字号令牌(唯一真源)。
#
# AE-FONT-UP(2026-11-18):引擎自己的 scaffold / scene / visualize 产物曾被 lint_page.py
# --floor(默认 12,SKILL.md:132 与 SKILL_ZH.md:135 同口径)判红 —— scaffold 产物 11.0、
# scene 产物 8.5(后者还是别场景的幽灵规则)。修法:把散在模板里的小 px 收拢到下面两档,
# 由各构建汇合点填成字面 px(产物里是真数字,静态闸和渲染探针都看得见,不是藏进 var())。
# 档位低于闸默认下限即 raise —— 放宽闸=没修,这里不给放宽的口子。
import re

FLOOR = 12.0
FS = {'micro': '12px', 'small': '12.5px'}
TOKENS = {'__FS_MICRO__': FS['micro'], '__FS_SMALL__': FS['small'],
          '@FS_MICRO@': FS['micro'], '@FS_SMALL@': FS['small']}


def assert_floor(tokens=None):
    # 负例真 raise:任何一档不是 Npx 且 >=FLOOR 就拒绝产出(不静默回落、不夹紧)
    t = TOKENS if tokens is None else tokens
    bad = {}
    for k, v in t.items():
        m = re.match(r'^(\d+(?:\.\d+)?)px$', str(v))
        if not m or float(m.group(1)) < FLOOR:
            bad[k] = v
    if bad:
        raise ValueError('type_tokens.assert_floor: 字号令牌低于 %gpx 下限: %s'
                         ' —— 拒绝产出(要过闸请提字号,不是提 --floor)' % (FLOOR, bad))
    return True


def fill(text):
    # 占位符 → 字面 px,顺手断言档位合规
    assert_floor()
    for k, v in TOKENS.items():
        text = text.replace(k, v)
    return text
