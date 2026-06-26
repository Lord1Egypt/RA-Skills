#!/usr/bin/env python3
"""
cn-lorem-ipsum - 占位文本生成器
生成随机中文/英文文本、姓名、手机号、邮箱
"""
import random
import argparse

# 中文字符库
CN_CHARS = '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞'

# 常用词库
CN_WORDS = [
    '公司', '项目', '用户', '产品', '服务', '系统', '数据', '功能', '模块', '接口',
    '开发', '设计', '测试', '部署', '配置', '优化', '问题', '解决', '方案', '策略',
    '技术', '工具', '平台', '应用', '网站', 'APP', '小程序', '服务器', '数据库',
    '网络', '安全', '性能', '效率', '质量', '管理', '团队', '合作', '沟通', '需求',
    '分析', '研究', '学习', '经验', '分享', '总结', '文档', '报告', '会议', '讨论',
    '市场', '运营', '推广', '营销', '品牌', '客户', '业务', '收入', '利润', '成本',
    '发展', '创新', '趋势', '未来', '机会', '挑战', '竞争', '优势', '劣势', '策略',
]

# 英文单词库
EN_WORDS = [
    'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
    'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
    'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
    'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
    'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
    'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
    'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
    'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum', 'the', 'quick', 'brown',
    'fox', 'jumps', 'over', 'lazy', 'dog', 'hello', 'world', 'test', 'example',
]

# 姓氏
CN_SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗', '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧', '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕']

# 名字
CN_GIVEN_NAMES = ['伟', '芳', '娜', '秀', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀', '霞', '平', '刚', '桂英', '建华', '建国', '志强', '永强', '晓东', '晓峰', '晓华', '晓明']

# 邮箱域名
EMAIL_DOMAINS = ['gmail.com', 'qq.com', '163.com', '126.com', 'outlook.com', 'hotmail.com', 'sina.com', 'sohu.com', 'foxmail.com']

def generate_cn_paragraph(words=50):
    """生成中文段落"""
    result = []
    for _ in range(words):
        # 随机选择词汇
        phrase = ''.join(random.choices(CN_WORDS, k=random.randint(2, 6)))
        result.append(phrase)
    return ''.join(result)

def generate_en_paragraph(words=50):
    """生成英文段落"""
    result = random.choices(EN_WORDS, k=words)
    # 首字母大写
    result[0] = result[0].capitalize()
    return ' '.join(result)

def generate_cn_name():
    """生成中文姓名"""
    surname = random.choice(CN_SURNAMES)
    given = ''.join(random.choices(CN_GIVEN_NAMES, k=2))
    return surname + given

def generate_phone():
    """生成中国手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
                '198', '199']
    prefix = random.choice(prefixes)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return prefix + suffix

def generate_email(name=None):
    """生成邮箱"""
    if not name:
        name = generate_cn_name()
    # 转换姓名为拼音
    name_pinyin = ''.join(c for c in name if '\u4e00' <= c <= '\u9fff')
    if not name_pinyin:
        name_pinyin = 'user'
    domain = random.choice(EMAIL_DOMAINS)
    patterns = [
        name_pinyin,
        name_pinyin + str(random.randint(1, 999)),
        name_pinyin[0] + str(random.randint(10, 99)),
    ]
    return random.choice(patterns).lower() + '@' + domain

def main():
    parser = argparse.ArgumentParser(description='占位文本生成器')
    parser.add_argument('--cn', action='store_true', help='生成中文文本')
    parser.add_argument('--en', action='store_true', help='生成英文文本')
    parser.add_argument('--name', action='store_true', help='生成中文姓名')
    parser.add_argument('--phone', action='store_true', help='生成手机号')
    parser.add_argument('--email', action='store_true', help='生成邮箱')
    parser.add_argument('--count', type=int, default=1, help='生成数量')
    parser.add_argument('--words', type=int, default=50, help='英文单词数')
    parser.add_argument('--paragraphs', type=int, default=1, help='段落数')
    
    args = parser.parse_args()
    
    # 如果没有任何参数，默认生成中文
    if not any([args.cn, args.en, args.name, args.phone, args.email]):
        args.cn = True
    
    for i in range(args.count):
        if args.cn:
            for _ in range(args.paragraphs):
                print(generate_cn_paragraph(args.words))
            if args.count > 1 and i < args.count - 1:
                print()
        
        if args.en:
            for _ in range(args.paragraphs):
                print(generate_en_paragraph(args.words))
            if args.count > 1 and i < args.count - 1:
                print()
        
        if args.name:
            print(generate_cn_name())
        
        if args.phone:
            print(generate_phone())
        
        if args.email:
            print(generate_email())
        
        if args.count > 1 and i < args.count - 1:
            if not (args.cn or args.en):
                print('---')

if __name__ == '__main__':
    main()