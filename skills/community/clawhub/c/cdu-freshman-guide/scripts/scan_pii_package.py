#!/usr/bin/env python3
"""对发布包内所有文件做 PII 残留扫描（手机号/QQ/学号/身份证/邮箱/微信号/银行卡）。"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ZIP = Path(sys.argv[1] if len(sys.argv) > 1 else 'cdu-freshman-guide-v1.0.0-skillhub.zip')

RE_PHONE = re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)')
RE_ID = re.compile(r'(?<!\d)\d{17}[\dXx](?!\d)')
RE_EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
RE_QQ = re.compile(r'(?<!\d)[1-9]\d{4,11}(?!\d)')
RE_STUDENT = re.compile(r'(?<!\d)\d{10,12}(?!\d)')
RE_WECHAT = re.compile(r'(?:[Vv]|[薇微])\+?\d{5,12}')
RE_BANK = re.compile(r'(?<!\d)\d{16,19}(?!\d)')
# 座机号码（区号-号码，如 028-84616550），非个人 PII
RE_LANDLINE = re.compile(r'0\d{2,3}-\d{7,8}')

# 允许出现的数字上下文（如年份 2026、门禁时间 23:00、价格 380 元等）
ALLOWED_CONTEXT = ('2026', '2025', '2024', '2023', '2022', '2021', '2020',
                   '380', '800', '710', '39', '49', '29', '1200', '500', '750',
                   '23:00', '6:00', '16:30', '7:00', '12:00', '13:00', '13:30',
                   '23:30', '1101', '9栋', '10栋', '15栋', '17栋', '19栋', '20栋',
                   '成洛大道2025号', '800W', '800w')

# 误报上下文：消息条数统计、URL 路径、正则示例
FALSE_POSITIVE = (
    '条', '→', '16053', '223124', '2415', '3076', '1041', '184', '148', '76',
    'info/', '.htm', '.cn/', 'http', 'abc@test.com', 'test.com',
)


def check_text(name: str, text: str) -> list[str]:
    problems = []
    # 座机号码（官方热线）不属于个人 PII，先剔除再校验
    text = RE_LANDLINE.sub('', text)
    for label, pat in (('手机号', RE_PHONE), ('身份证', RE_ID), ('邮箱', RE_EMAIL),
                       ('QQ号', RE_QQ), ('学号', RE_STUDENT), ('微信号', RE_WECHAT),
                       ('银行卡', RE_BANK)):
        for m in pat.finditer(text):
            ctx = text[max(0, m.start() - 15):m.end() + 15]
            if any(a in ctx for a in ALLOWED_CONTEXT):
                continue
            if any(fp in ctx for fp in FALSE_POSITIVE):
                continue
            problems.append(f'  {name}: [{label}] {ctx}')
    return problems


def main() -> int:
    total = 0
    with zipfile.ZipFile(ZIP) as zf:
        for info in zf.infolist():
            if info.is_dir() or not info.filename.endswith(('.md', '.json', '.py')):
                continue
            try:
                text = zf.read(info).decode('utf-8')
            except Exception:
                continue
            probs = check_text(info.filename, text)
            for p in probs:
                print(p)
                total += 1
    if total:
        print(f'\n❌ 发现 {total} 处疑似 PII 残留')
        return 1
    print('✅ 发布包无 PII 残留')
    return 0


if __name__ == '__main__':
    sys.exit(main())
