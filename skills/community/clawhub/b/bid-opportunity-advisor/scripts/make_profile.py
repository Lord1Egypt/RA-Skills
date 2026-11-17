#!/usr/bin/env python3
"""
make_profile.py — 公司画像创建向导（stdlib only）

生成 `~/.bidprofile.json`，供 bid-opportunity-advisor 的画像匹配与机会评分使用。

两种用法：
  1) 交互式（无参数）：逐步提问，逐项确认后落盘。
     python make_profile.py

  2) CLI 一次性（参数式，适合脚本/agent 调用）：
     python make_profile.py --company "XX科技" --province 广东 \
         --qualifications "ISO9001,电子与智能化一级" \
         --products "安防监控,智慧校园平台" --tier medium

落盘位置：默认 ~/.bidprofile.json（可用 --out 覆盖）。

schema:
  company        : str   公司全称
  province       : str   所在省/直辖市（用于地域可达性计算）
  qualifications : [str] 已具备资质（匹配维度之一，启发式）
  products       : [str] 主营产品/服务关键词（用于项目文本匹配）
  capacity_tier  : micro|small|medium|large|mega  产能/规模档
"""

import argparse
import json
import sys
from pathlib import Path

TIERS = ['micro', 'small', 'medium', 'large', 'mega']
DEFAULT_OUT = Path.home() / '.bidprofile.json'


def parse_list(s):
    """'a, b, c' -> ['a','b','c']（去空白、去空项）"""
    if not s:
        return []
    return [x.strip() for x in s.split(',') if x.strip()]


def ask(prompt, default=''):
    try:
        val = input(f'{prompt}{(" [" + default + "]") if default else ""}: ').strip()
    except EOFError:
        val = ''
    return val or default


def build_interactive():
    print('=== 公司画像创建向导 ===')
    print('（直接回车用方括号里的默认值；资质/产品多项用逗号分隔）\n')
    company = ask('公司全称')
    province = ask('所在省/直辖市（如 广东 / 北京）')
    quals = ask('已具备资质（逗号分隔，如 ISO9001,电子与智能化一级）')
    products = ask('主营产品/服务关键词（逗号分隔，如 安防监控,智慧校园平台）')
    print('规模档：micro(微型) small(小型) medium(中型) large(大型) mega(巨型)')
    tier = ask('规模档', 'medium')
    return {
        'company': company,
        'province': province,
        'qualifications': parse_list(quals),
        'products': parse_list(products),
        'capacity_tier': tier,
    }


def validate(profile):
    errors = []
    if not profile.get('company'):
        errors.append('company 不能为空')
    if not profile.get('province'):
        errors.append('province 不能为空')
    t = profile.get('capacity_tier')
    if t not in TIERS:
        errors.append(f'capacity_tier 必须是 {TIERS} 之一，收到：{t!r}')
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--company', default=None)
    ap.add_argument('--province', default=None)
    ap.add_argument('--qualifications', default='', help='逗号分隔')
    ap.add_argument('--products', default='', help='逗号分隔')
    ap.add_argument('--tier', default=None, choices=TIERS)
    ap.add_argument('--out', default=str(DEFAULT_OUT), help='落盘路径，默认 ~/.bidprofile.json')
    args = ap.parse_args()

    # 交互式：无任何关键参数时进入向导
    if not (args.company and args.province and args.tier):
        prof = build_interactive()
    else:
        prof = {
            'company': args.company,
            'province': args.province,
            'qualifications': parse_list(args.qualifications),
            'products': parse_list(args.products),
            'capacity_tier': args.tier,
        }

    errs = validate(prof)
    if errs:
        print('校验失败：', file=sys.stderr)
        for e in errs:
            print('  - ' + e, file=sys.stderr)
        sys.exit(1)

    # 交互式默认不静默落盘：确认后写
    out_path = Path(args.out).expanduser()
    if not (args.company and args.province and args.tier):
        print('\n即将写入：')
        print(json.dumps(prof, ensure_ascii=False, indent=2))
        if ask('确认写入？(y/N)', 'n').lower() not in ('y', 'yes'):
            print('已取消，未写入任何文件。')
            sys.exit(0)
    else:
        print('\n画像内容：')
        print(json.dumps(prof, ensure_ascii=False, indent=2))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(prof, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n✅ 已写入 {out_path}')


if __name__ == '__main__':
    main()
