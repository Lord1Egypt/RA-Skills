#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta

QUESTION_RULES = {
    '呼吸与危重症医学科': ['这次症状更像感染、过敏还是慢性问题？', '是否需要做胸片/CT/肺功能？', '目前用药是否需要调整？'],
    '心血管科': ['这次胸闷胸痛的危险程度如何？', '是否需要心电图/动态心电图/超声？', '现有降压/心脏药是否要调整？'],
    '消化科': ['这次腹痛或反酸最可能的原因是什么？', '是否需要胃镜/幽门螺杆菌检查？', '饮食和用药上要注意什么？'],
    '妇产科': ['这次症状是否需要进一步检查？', '近期月经/妊娠情况会不会影响诊疗？', '是否需要做B超或激素相关检查？'],
    '皮肤科': ['最可能的诱因是什么？', '需要口服药还是外用药？', '哪些情况加重时要复诊？'],
    '综合科': ['这次最需要先排查什么？', '还需要转诊到哪个专科？', '我现在最需要做的检查是什么？'],
}

COMMON_ITEMS = ['身份证/医保卡', '既往病历或出院小结', '近期检查报告/化验单', '当前正在使用的药物清单']


def choose_questions(department: str):
    for key, items in QUESTION_RULES.items():
        if key in department or department in key:
            return items
    return QUESTION_RULES['综合科']


def main() -> int:
    p = argparse.ArgumentParser(description='Generate a structured pre-visit card')
    p.add_argument('--hospital', required=True)
    p.add_argument('--department', required=True)
    p.add_argument('--doctor', default='待定')
    p.add_argument('--appointment', required=True, help='YYYY-MM-DD HH:MM')
    p.add_argument('--symptoms', default='')
    p.add_argument('--history', default='')
    p.add_argument('--city', default='北京')
    args = p.parse_args()

    dt = datetime.strptime(args.appointment, '%Y-%m-%d %H:%M')
    arrive = dt - timedelta(minutes=60)
    card = {
        'hospital': args.hospital,
        'department': args.department,
        'doctor': args.doctor,
        'appointment': dt.strftime('%Y-%m-%d %H:%M'),
        'suggested_arrival_time': arrive.strftime('%Y-%m-%d %H:%M'),
        'city': args.city,
        'bring_items': COMMON_ITEMS,
        'symptom_summary': args.symptoms,
        'history_summary': args.history,
        'questions_for_doctor': choose_questions(args.department),
        'important_notes_to_tell_doctor': [
            '症状持续多久、是否加重',
            '既往慢病、近期用药、过敏史',
            '最近做过的检查和异常结果',
        ],
        'note': '如为检查类项目，请再次确认是否需要空腹、停药或家属陪同。'
    }
    print(json.dumps(card, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
