#!/usr/bin/env python3
import json, sys
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore').strip()


def main():
    if len(sys.argv) < 2:
        print('Usage: douyin_ad_plan_brief.py <input.txt>')
        sys.exit(1)
    p = Path(sys.argv[1])
    text = read_text(p)
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    title = lines[0][:32] if lines else '未命名抖音投放项目'
    result = {
        'project': title,
        'goal_guess': '私信 / 留资 / 加企微',
        'core_offer_guess': lines[0] if lines else '',
        'suggested_audiences': [
            '刷到相关内容但尚未行动的人',
            '已经意识到问题、正在找方案的人',
            '对结果敏感、对比方案中的人'
        ],
        'hook_angles': [
            '痛点型开头',
            '结果型开头',
            '反差型开头',
            '筛选型开头',
            '案例型开头'
        ],
        'budget_split_hint': {
            'test_phase': '先用小预算测 3-5 个开头角度',
            'scale_phase': '优先放量留资率高且线索质量好的组'
        },
        'cta_examples': [
            '先私信我，我发你一版案例',
            '评论区留“想看”，我发你完整方案',
            '先领清单，再决定要不要深入聊'
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
