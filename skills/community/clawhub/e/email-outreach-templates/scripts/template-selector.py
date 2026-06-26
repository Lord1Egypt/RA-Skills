#!/usr/bin/env python3
# Email Template Selector

TEMPLATES = {
    'first_contact': ['F1', 'F2'],
    'followup_1_3': ['F11', 'F12'],
    'followup_7_14': ['F21', 'F22'],
    'followup_30': ['F31'],
}

def select_template(scenario, industry='tech'):
    """根据场景和行业选择模板"""
    return TEMPLATES.get(scenario, ['F1'])[0]

if __name__ == '__main__':
    print("模板选择器")
    print(f"首次联系：{select_template('first_contact')}")
    print(f"跟进 1-3 天：{select_template('followup_1_3')}")
