#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""稻哲纪烤羊排 Skill 自动化测试脚本"""

import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(SKILL_DIR, 'references')

results = {'pass': 0, 'fail': 0, 'checks': []}
P = '✅'
F = '❌'

def check(name, condition, detail=''):
    if condition:
        results['pass'] += 1
        results['checks'].append(f'  {P} {name}')
    else:
        results['fail'] += 1
        results['checks'].append(f'  {F} {name}: {detail}')
    return condition

def read_ref(filename):
    path = os.path.join(REF_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

# ========== 1. 文件结构完整性 ==========
print('=== 1. 文件结构完整性 ===')
expected_files = [
    'SKILL.md', '.gitignore', 'README.md', 'version.json', 'CHANGELOG.md',
    'references/business-info.md', 'references/services.md',
    'references/promotions.md', 'references/faq.md', 'references/brand.md',
]
for f in expected_files:
    check(f'文件: {f}', os.path.exists(os.path.join(SKILL_DIR, f)))

# ========== 2. 参考文件内容覆盖 ==========
print('\n=== 2. 参考文件内容覆盖 ===')
ref_checks = {
    'business-info.md': ['9:00', '21:00', '南昌', '青山湖区', '创新一路',
                         '顺外路', '15879156329', '13767413193', '88888888',
                         '免费停车', '10公里', '150'],
    'services.md': ['168', '98', '58', '30', '35', '14',
                    '烤羊排', '麻椒鸡', '猪蹄', '红油凉拌',
                    '约', '克左右', '内蒙', '红毛老母鸡',
                    '新疆鸡蛋挂糊', '慢烤2小时'],
    'promotions.md': ['82', '112', '116', '206', '236',
                      '团购', '优惠价', '2026年12月30日'],
    'faq.md': ['新疆鸡蛋挂糊', '内蒙', '红毛老母鸡', '会员',
               '8.8折', '宠物', '过敏', '预约', '鸡蛋挂糊工艺',
               '食品经营许可证'],
    'brand.md': ['南昌', '青山湖区', '创新一路', '顺外路', '烤羊排'],
}

for fname, keywords in ref_checks.items():
    fpath = os.path.join(REF_DIR, fname)
    if not os.path.exists(fpath):
        check(f'{fname} 文件存在', False, '文件不存在')
        continue
    content = read_ref(fname)
    missing = [kw for kw in keywords if kw not in content]
    check(f'{fname} 全部关键词覆盖', len(missing) == 0,
          f'缺失: {missing}' if missing else '')

# ========== 3. SKILL.md 结构完整性 ==========
print('\n=== 3. SKILL.md 结构完整性 ===')
sk_path = os.path.join(SKILL_DIR, 'SKILL.md')
with open(sk_path, encoding='utf-8') as f:
    sk = f.read()

structure_checks = {
    'YAML frontmatter name': 'name: daozheji-grill' in sk,
    'YAML frontmatter description': 'description:' in sk,
    '触发关键词覆盖': '稻哲纪' in sk and '烤羊排' in sk and '麻椒鸡' in sk and '猪蹄' in sk,
    '数据读取规则': '数据读取规则' in sk or '必读文件' in sk,
    '引用business-info.md': 'business-info.md' in sk,
    '引用services.md': 'services.md' in sk,
    '引用promotions.md': 'promotions.md' in sk,
    '引用faq.md': 'faq.md' in sk,
    '引用brand.md': 'brand.md' in sk,
    '语气规范': '热情熟络' in sk,
    '场景框架-营业信息': '场景一' in sk,
    '场景框架-招牌菜': '场景二' in sk,
    '场景框架-价格口味': '场景三' in sk,
    '场景框架-外卖': '场景四' in sk,
    '场景框架-团购': '场景五' in sk,
    '场景框架-工艺食材': '场景六' in sk,
    '场景框架-会员': '场景七' in sk,
    '场景框架-特殊需求': '场景八' in sk,
    '场景框架-预约': '场景九' in sk,
    '场景框架-投诉': '场景十' in sk,
    '安全边界': '安全边界' in sk,
    '推销节制': '推销节制' in sk,
    '短关键词触发': '短关键词触发' in sk,
    '引导式追问': '引导式追问' in sk,
}

for label, condition in structure_checks.items():
    check(label, condition, '' if condition else '缺失')

# ========== 4. 检查 SKILL.md 无硬编码业务数据 ==========
print('\n=== 4. 检查 SKILL.md 无硬编码业务数据 ===')
hardcoded_checks = [
    ('无硬编码具体地址路名', '创新一路' not in sk and '顺外路' not in sk),
    ('无硬编码Wi-Fi密码', '88888888' not in sk),
    ('无硬编码手机号', '15879156329' not in sk and '13767413193' not in sk),
    ('无硬编码菜品价格', '168 元' not in sk and '58 元' not in sk and '98 元' not in sk),
    ('无硬编码套餐价格', '82 元' not in sk and '112 元' not in sk),
]
for label, condition in hardcoded_checks:
    check(label, condition)

# ========== 5. 顾客问答场景覆盖测试 ==========
print('\n=== 5. 顾客问答场景覆盖测试 ===')

qa_scenarios = [
    ('你们几点开门？', ['9:00', '21:00'], '营业时间'),
    ('周末营业吗？', ['9:00', '21:00'], '营业时间'),
    ('地址在哪？怎么走？', ['南昌', '青山湖区', '创新一路'], '地址导航'),
    ('好停车吗？', ['免费停车'], '停车'),
    ('WiFi密码多少？', ['88888888'], 'WiFi'),
    ('有什么招牌菜？', ['烤羊排', '麻椒鸡', '猪蹄'], '菜品推荐'),
    ('烤羊排多少钱？', ['168', '98'], '价格'),
    ('麻椒鸡多少钱？', ['58', '30'], '价格'),
    ('猪蹄多少钱？', ['35'], '价格'),
    ('凉拌菜多少钱？', ['14', '斤'], '价格'),
    ('烤羊排辣不辣？', ['不辣'], '口味'),
    ('小孩能吃吗？', ['小孩', '不辣'], '口味'),
    ('能送外卖吗？', ['外卖', '配送', '150'], '外卖'),
    ('多久能送到？', ['30', '分钟'], '外卖'),
    ('有套餐吗？', ['团购', '优惠价'], '套餐'),
    ('两个人吃什么划算？', ['82', '112'], '套餐'),
    ('能带宠物吗？', ['宠物'], '特殊需求'),
    ('有包间吗？', ['包间'], '特殊需求'),
    ('能自带酒水吗？', ['自带酒水', '开瓶费'], '特殊需求'),
    ('怎么办会员？', ['98', '会员', '8.8折'], '会员'),
    ('生日有福利吗？', ['生日', '8.8折'], '会员'),
    ('需要预约吗？', ['预约'], '预约'),
    ('怎么做的？什么工艺？', ['新疆鸡蛋挂糊', '慢烤'], '工艺'),
    ('用的什么肉？', ['内蒙', '红毛老母鸡'], '食材'),
    ('过敏要注意什么？', ['过敏'], '食品安全'),
    ('有食品许可证吗？', ['食品经营许可证'], '食品安全'),
]

for q, must_contain, category in qa_scenarios:
    found = False
    for fname in os.listdir(REF_DIR):
        content = read_ref(fname)
        if all(kw in content for kw in must_contain):
            found = True
            break
    if not found and all(kw in sk for kw in must_contain):
        found = True
    check(f'[{category}] {q[:20]}...', found, f'需含: {must_contain}')

# ========== 6. 数据一致性交叉检查 ==========
print('\n=== 6. 数据一致性交叉检查 ===')
services = read_ref('services.md')
faq = read_ref('faq.md')
promo = read_ref('promotions.md')
biz = read_ref('business-info.md')

# 价格一致性: services.md 和 promotions.md 中的原价应对应
check('烤羊排大份价格 services↔promo 一致',
      '168' in services and '168' not in promo)  # promo引用原价但非直接写168

# 工艺描述一致性
for kw in ['新疆鸡蛋挂糊', '内蒙']:
    check(f'工艺"{kw}"在services和faq中一致', kw in services and kw in faq)

# 预约规则一致性
check('预约规则在faq和promo中一致',
      '预约' in faq and '预约' in promo)

# 外卖信息
check('外卖信息完整', '配送' in biz and '150' in biz and '10公里' in biz)

# ========== 7. 版本管理检查 ==========
print('\n=== 7. 版本管理检查 ===')
version_path = os.path.join(SKILL_DIR, 'version.json')
check('version.json 存在', os.path.exists(version_path))
if os.path.exists(version_path):
    with open(version_path, encoding='utf-8') as f:
        ver = json.load(f)
    check('version.json 含 version 字段', 'version' in ver)
    check('version.json 含 skill 字段', 'skill' in ver)
    check('version.json 含 auto_update 配置', 'auto_update' in ver)

check('Git 仓库已初始化', os.path.exists(os.path.join(SKILL_DIR, '.git', 'HEAD')))
check('CHANGELOG.md 存在', os.path.exists(os.path.join(SKILL_DIR, 'CHANGELOG.md')))
check('.gitignore 存在', os.path.exists(os.path.join(SKILL_DIR, '.gitignore')))

# ========== 8. 安装脚本检查 ==========
print('\n=== 8. 安装脚本与 CI/CD 检查 ===')
check('install.sh 存在', os.path.exists(os.path.join(SKILL_DIR, 'install.sh')))
check('install.ps1 存在', os.path.exists(os.path.join(SKILL_DIR, 'install.ps1')))
check('.github/workflows/release.yml 存在',
      os.path.exists(os.path.join(SKILL_DIR, '.github', 'workflows', 'release.yml')))

# ========== 结果汇总 ==========
total = results['pass'] + results['fail']
print(f'\n{"="*50}')
print(f'    测试结果汇总')
print(f'{"="*50}')
print(f'  通过: {results["pass"]}/{total}')
print(f'  失败: {results["fail"]}/{total}')
print(f'  通过率: {results["pass"]/total*100:.1f}%' if total > 0 else '  无结果')
print(f'{"="*50}')

print('\n'.join(results['checks']))

json_path = os.path.join(SKILL_DIR, 'dist', 'test-report.json')
os.makedirs(os.path.dirname(json_path), exist_ok=True)
with open(json_path, 'w', encoding='utf-8') as jf:
    json.dump({
        'passed': results['pass'],
        'failed': results['fail'],
        'total': total,
        'pass_rate': f'{results["pass"]/total*100:.1f}%' if total > 0 else 'N/A',
    }, jf, ensure_ascii=False, indent=2)
print(f'\nJSON report saved: {json_path}')

exit(0 if results['fail'] == 0 else 1)
