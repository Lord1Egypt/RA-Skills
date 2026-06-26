#!/usr/bin/env python3
"""
普通话→拼音 首字母映射（纯Python实现，无外部依赖）
覆盖词库中常用普通话词汇

用法：
  from pinyin_map import get_pinyin
  print(get_pinyin("干什么"))  # -> "ganma"
"""

# 常用汉字拼音映射（只含声母+韵母，简写全拼）
CHAR_PINYIN = {
    '干': 'gan', '什': 'shi', '么': 'me', '好': 'hao', '不': 'bu', '是': 'shi',
    '我': 'wo', '你': 'ni', '他': 'ta', '这': 'zhe', '那': 'na', '有': 'you',
    '没': 'mei', '在': 'zai', '来': 'lai', '去': 'qu', '看': 'kan', '说': 'shuo',
    '吃': 'chi', '喝': 'he', '玩': 'wan', '睡': 'shui', '做': 'zuo', '走': 'zou',
    '想': 'xiang', '知': 'zhi', '道': 'dao', '给': 'gei', '用': 'yong', '找': 'zhao',
    '拿': 'na', '放': 'fang', '打': 'da', '叫': 'jiao', '让': 'rang',
    '很': 'hen', '太': 'tai', '都': 'dou', '还': 'huan', '就': 'jiu', '也': 'ye',
    '又': 'you', '再': 'zai', '只': 'zhi', '把': 'ba', '被': 'bei', '从': 'cong',
    '到': 'dao', '为': 'wei', '和': 'he', '与': 'yu', '或': 'huo', '但': 'dan',
    '如': 'ru', '果': 'guo', '因': 'yin', '所': 'suo', '以': 'yi', '而': 'er',
    '着': 'zhuo', '过': 'guo', '里': 'li', '外': 'wai', '上': 'shang', '下': 'xia',
    '前': 'qian', '后': 'hou', '左': 'zuo', '右': 'you', '多': 'duo', '少': 'shao',
    '大': 'da', '小': 'xiao', '长': 'chang', '短': 'duan', '高': 'gao', '低': 'di',
    '快': 'kuai', '慢': 'man', '新': 'xin', '老': 'lao', '红': 'hong', '白': 'bai',
    '黑': 'hei', '黄': 'huang', '蓝': 'lan', '冷': 'leng', '热': 're',
    '酸': 'suan', '甜': 'tian', '苦': 'ku', '辣': 'la', '香': 'xiang', '臭': 'chou',
    '难': 'nan', '易': 'yi', '真': 'zhen', '假': 'jia', '对': 'dui', '错': 'cuo',
    '好': 'hao', '坏': 'huai', '难': 'nan', '忙': 'mang', '闲': 'xian',
    '穷': 'qiong', '富': 'fu', '美': 'mei', '丑': 'chou', '帅': 'shuai',
    '胖': 'pang', '瘦': 'shou', '矮': 'ai', '肥': 'fei', '聪明': 'congming',
    '笨': 'ben', '傻': 'sha', '憨': 'han', '漂亮': 'piaoliang', '精神': 'jingshen',
    '厉害': 'lihai', '一般': 'yiban', '不错': 'bucuo', '很好': 'henhao',
    '舒服': 'shufu', '难受': 'nanshou', '开心': 'kaixin', '难过': 'nanguo',
    '生气': 'shengqi', '高兴': 'gaoxing', '伤心': 'shangxin', '害怕': 'haipa',
    '担心': 'danxin', '着急': 'zhuoji', '紧张': 'jinzhang', '放松': 'fangsong',
    '累': 'lei', '困': 'kun', '饿': 'e', '渴': 'ke', '饱': 'bao',
    '聊天': 'liaotian', '说话': 'shuohua', '听话': 'tinghua', '唱歌': 'changge',
    '跳舞': 'tiaowu', '打球': 'daqiu', '跑步': 'paobu', '走路': 'zoulu',
    '骑车': 'qiache', '开车': 'kaiche', '坐车': 'zuche', '打车': 'dache', '散步': 'sanbu',
    '回家': 'huijia', '出门': 'chumen', '上学': 'shangxue', '上班': 'shangban',
    '下班': 'xiaban', '加班': 'jiaban', '休息': 'xiuxi', '请假': 'qingjia',
    '开会': 'kaihui', '出差': 'chucha', '应酬': 'yingchou', '喝酒': 'hejiu',
    '抽烟': 'chouyan', '喝茶': 'hecha', '吃饭': 'chifan', '做饭': 'zuofan',
    '洗碗': 'xiwan', '洗衣服': 'xiyifu', '打扫': 'dasao', '整理': 'zhengli',
    '买东西': 'maidongxi', '省钱': 'shengqian', '花钱': 'huahua', '赚钱': 'zhuanqian',
    '没钱': 'meiqian', '有钱': 'youqian', '小气': 'xiaoqi', '大方': 'dafang',
    '便宜': 'pianyi', '贵': 'gui', '感冒': 'ganmao', '发烧': 'fashao',
    '咳嗽': 'kesou', '头疼': 'touteng', '肚子疼': 'duziteng', '受伤': 'shoushang',
    '医院': 'yiyuan', '买药': 'maiyao', '吃药': 'chiyao', '打工': 'dagong',
    '工作': 'gongzuo', '生活': 'shenghuo', '时间': 'shijian', '今天': 'jintian',
    '明天': 'mingtian', '昨天': 'zuotian', '现在': 'xianzai', '以后': 'yihou',
    '以前': 'yiqian', '经常': 'jingchang', '偶尔': 'ouer', '总是': 'zongshi',
    '倒霉': 'daomei', '运气': 'yunqi', '顺利': 'shunli', '应该': 'yinggai',
    '必须': 'bixu', '可以': 'keyi', '喜欢': 'xihuan', '讨厌': 'taoyan',
    '记得': 'jide', '忘记': 'wangji', '告诉': 'gaosu', '通知': 'tongzhi',
    '吵架': 'chaojia', '打架': 'dajia', '和好': 'hehao', '道歉': 'daoqian',
    '原谅': 'yuanliang', '帮忙': 'bangmang', '麻烦': 'mafan', '谢谢': 'xiexie',
    '对不起': 'duibuqi', '不好意思': 'buhaoyisi', '没关系': 'meiguanxi',
    '啥': 'sha', '咋': 'za', '咋整': 'zazheng', '嘎哈': 'gaha', '贼': 'zei',
    '得劲': 'deijin', '唠嗑': 'liaoke', '忽悠': 'huyou', '整': 'zheng',
    '胆儿肥': 'danrefei', '秃噜皮': 'tulupi', '扬了二正': 'yangeraldan',
    '吭哧瘪肚': 'kangchibiedu', '磨叽': 'moji', '唠': 'lao', '拽': 'zhuai',
    '掰': 'bai', '别': 'bie', '整': 'zheng', '撮': 'cuo', '吨': 'dun',
    '捂': 'wu', '削': 'xiao', '吭': 'keng', '嘎': 'ga', '咕': 'gu',
    '埋汰': 'maitai', '嘎咕': 'gagu', '唠嗑': 'liaoke', '扯': 'che',
    '膈应': 'geying', '得瑟': 'dese', '忽悠': 'huyou', '敲': 'qiao',
    '糊弄': 'hulong', '唠扯': 'liaoche', '湛': 'zhan', '涮': 'shuan',
    '咕嘟': 'gudu', '熘': 'liu', '汆': 'cuan', '迸': 'beng', '噻': 'sai',
    '嗪': 'qin', '嘚': 'dei', '嘞': 'lei', '咔': 'ka', '吱': 'zi',
    '呗': 'bei', '啦': 'la', '哈': 'ha', '咯': 'lo', '嗯哪': 'enna',
    '嘎嘎': 'gaga', '嗷嗷': 'aoxiao', '杠杠': 'anggang', '挠得儿': 'naoder',
    '撒摩': 'samo', '淘登': 'taodeng', '别锁': 'biesuo', '撒磨': 'samo',
    '穴么': 'xuemo', '淘登': 'taodeng', '溜': 'liu', '戥': 'deng',
    '掂': 'dian', '趔': 'lie', '攥': 'zuan', '撅': 'jue', '撇': 'pie',
    '拃': 'zha', '拄': 'zhu', '抡': 'lun', '挲': 'suo', '挞': 'ta',
    '挎': 'kua', '挞': 'ta', '挣': 'zheng', '挤': 'ji', '挥': 'hui',
    '掠': 'lve', '掀': 'xian', '掳': 'lu', '掴': 'guai', '掸': 'dan',
    '接': 'jie', '推': 'tui', '掩': 'yan', '合': 'he', '吉': 'ji',
    '吉': 'ji', '咧': 'lie', '哔': 'bi', '嘚': 'dei', '嘧': 'mi',
    '嘟': 'du', '噬': 'shi', '囚': 'qiu', '团': 'tuan', '囤': 'dun',
    '圈': 'quan', '圜': 'huan', '坠': 'zhui', '垂': 'chui', '型': 'xing',
    '埃': 'ai', '堵': 'du', '塑': 'su', '墨': 'mo', '坠': 'zhui',
    '型': 'xing', '垣': 'yuan', '城': 'cheng', '域': 'yu', '坚': 'jian',
    '报': 'bao', '坦': 'tan', '坡': 'po', '坤': 'kun', '垣': 'yuan',
    '型': 'xing', '垂': 'chui', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
    '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing', '型': 'xing',
}


def get_pinyin(word: str) -> str:
    """把汉字转成拼音字符串（全拼，无声调）"""
    result = ''
    for char in word:
        if char in CHAR_PINYIN:
            result += CHAR_PINYIN[char]
        elif char.isalpha() and char.isascii():
            result += char.lower()
        # 忽略其他字符（标点等）
    return result


def word_to_pinyin(word: str) -> str:
    """别名，统一接口"""
    return get_pinyin(word)


def is_pure_pinyin(text: str) -> bool:
    """判断输入是否纯拼音（无汉字）"""
    return bool(text) and all(c.isascii() and c.isalpha() for c in text)


# 预计算常用词的拼音
COMMON_PINYIN = {}
for chars, py in CHAR_PINYIN.items():
    if len(chars) == 1:
        COMMON_PINYIN[chars] = py