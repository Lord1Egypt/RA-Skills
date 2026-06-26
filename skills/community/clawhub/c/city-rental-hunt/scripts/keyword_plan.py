#!/usr/bin/env python3
import argparse


def split_csv(text):
    if not text:
        return []
    return [x.strip() for x in text.split(',') if x.strip()]


def build_keywords(zones, rooms, must_have, optional):
    lines = []
    for zone in zones:
        lines.append(f"## {zone}")
        base = [
            f"{zone} 整租 {rooms}",
            f"{zone} {rooms} 房东直租",
            f"{zone} {rooms} 转租",
        ]
        quality_tokens = ' '.join(must_have[:2]) if must_have else ''
        if quality_tokens:
            base.append(f"{zone} {quality_tokens} {rooms}".strip())
        for token in optional:
            base.append(f"{zone} {token} {rooms}".strip())
        seen = set()
        for item in base:
            if item not in seen:
                seen.add(item)
                lines.append(f"- {item}")
        lines.append("")
    return '\n'.join(lines).strip() + '\n'


def main():
    parser = argparse.ArgumentParser(description='Generate rental-hunt keyword plan by zone.')
    parser.add_argument('--city', required=True)
    parser.add_argument('--zones', required=True, help='Comma-separated zones')
    parser.add_argument('--budget', default='')
    parser.add_argument('--rooms', default='两居')
    parser.add_argument('--must', default='整租,电梯,次新')
    parser.add_argument('--optional', default='房东直租,转租,可养猫')
    args = parser.parse_args()

    zones = split_csv(args.zones)
    must_have = split_csv(args.must)
    optional = split_csv(args.optional)

    print(f"# Rental keyword plan | {args.city}")
    if args.budget:
        print(f"- 预算: {args.budget}")
    print(f"- 户型: {args.rooms}")
    if must_have:
        print(f"- 硬条件: {', '.join(must_have)}")
    if optional:
        print(f"- 软条件: {', '.join(optional)}")
    print()
    print(build_keywords(zones, args.rooms, must_have, optional), end='')


if __name__ == '__main__':
    main()
