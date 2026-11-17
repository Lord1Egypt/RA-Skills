#!/usr/bin/env python3
"""成都大学新生群聊数据脱敏工具 v2。

读取 QQChatExporter 导出的群聊 JSON，对每条消息做个人信息脱敏：
  - QQ 号 / 手机号 / 身份证 / 邮箱 / 学号 / 微信号 / 银行卡 / 宿舍房间号
  - 发送者昵称（一律 → [同学]）
  - 正文中的真实姓名：仅当「常见姓氏 + 2-3 字 + 非常用词/专业名」判定为真实姓名才脱敏，
    避免把昵称、专业名、常用词误替换成 [同学] 而破坏知识库内容。
  - @提及中的真实姓名（含未在发送者名单中的老师/同学名）
  - URL 整体保留（链接是知识库价值，不脱敏内部数字）
输出脱敏后的 JSON（保持原结构）+ 脱敏统计报告。

用法:
  python scripts/desensitize.py --input <原始导出目录> --output <脱敏输出目录>
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

# ---------- 脱敏规则 ----------

# 手机号（11 位，1 开头）
RE_PHONE = re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)')
# 身份证（17 位数字 + 数字/X）
RE_ID = re.compile(r'(?<!\d)\d{17}[\dXx](?!\d)')
# 邮箱
RE_EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
# 学号（10-12 位纯数字，且非手机号/QQ 已覆盖）
RE_STUDENT_ID = re.compile(r'(?<!\d)\d{10,12}(?!\d)')
# QQ 号（5-12 位，非手机号开头）
RE_QQ = re.compile(r'(?<!\d)[1-9]\d{4,11}(?!\d)')
# 微信号（V+/薇+ 后跟数字，或纯微信号格式）
RE_WECHAT = re.compile(r'(?:[Vv]|[薇微])\+?\d{5,12}')
# 宿舍房间号（如 10栋123、10栋1单元201）
RE_DORM_ROOM = re.compile(r'(\d{1,2}栋)(\d{1,4}(?:单元)?\d{0,3})')
# 银行卡号（16-19 位）
RE_BANK = re.compile(r'(?<!\d)\d{16,19}(?!\d)')
# URL（保留不脱敏，含无协议前缀的裸域名，如 xsc.cdu.edu.cn/info/1015/11281.htm；
#      (?<!@) 避免吞掉邮箱的域名部分，如 abc@test.com 中的 test.com）
RE_URL = re.compile(
    r'(?<!@)(?:https?://|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
    r'[^\s\u4e00-\u9fa5，。；：！？、（）【】《》""''…—]*'
)
# @提及中的中文名
RE_AT_NAME = re.compile(r'@([\u4e00-\u9fa5]{2,3})')
# @提及中的房间号(+职务)+姓名（如 @123室长张三 / @456寝室室长李四），房间号一并脱敏
RE_AT_ROOM_NAME = re.compile(r'@(\d{1,4})(?:寝室)?(室长|室员|阿姨|同学)?([\u4e00-\u9fa5]{2,3})')

MASK_PHONE = '[手机号]'
MASK_ID = '[身份证]'
MASK_EMAIL = '[邮箱]'
MASK_STUDENT_ID = '[学号]'
MASK_QQ = '[QQ号]'
MASK_WECHAT = '[微信号]'
MASK_DORM_ROOM = r'\1[房间号]'
MASK_BANK = '[银行卡]'
MASK_NAME = '[同学]'

# 常见姓氏（用于判定"看起来像真实姓名"）
SURNAMES = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄'
    '和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁'
    '杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍'
    '虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚'
    '程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓'
    '牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙'
    '叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴胥能苍双闻'
    '莘党翟谭贡劳逄姬申扶堵冉宰郦雍却璩桑桂濮牛寿通边扈燕冀郏浦尚农温'
    '别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡'
    '国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾'
    '毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公'
)
SURNAME_SET = set(SURNAMES)

# 常用词/专业名/群聊角色 —— 禁止在正文中当作姓名脱敏（否则破坏知识库）
COMMON_WORDS = {
    # 专业/院系/班级
    '计算机', '车辆', '网新', '汉本', '广电', '环工', '社会学', '国教', '汉语言',
    '级汉本', '网新专业', '汉语言文学', '新闻传播', '广播电视',
    # 群聊角色 / @ 常见对象
    '全体成员', '全体', '所有人', '群主', '管理员', '群管理', '公告',
    # 首字恰好是姓氏的常用词（需显式排除）
    '左右', '江南', '白昼', '成都', '大学', '学院', '学校', '老师', '同学',
    '班长', '部长', '会长', '团长', '书记', '主任', '辅导员', '班主任',
    # 无姓氏首字的昵称/常用词（姓氏判定已排除，这里兜底）
    '微信', '二楼', '打篮球', '随便', '不知道', '差不多', '等等', '某某', '美女',
    '哈哈哈', '大聪明', '大愚', '梨花', '晚风', '寒林', '小五', '小鱼', '泡泡',
    '猪猪', '小柑橘', '困告羊', '呆小布', '炸年糕', '泡泡君', '酱酱酱', '唯潍糸',
    '圈幽幽', '嗷呜', '噜噜噜', '儿豁', '克星', '免疫体', '受害鱼', '叮叮',
    '启明', '不念', '不瘦', '不良玉', '不问', '么么', '七安', '九歌', '参辰',
    '流觞', '觉今是', '搽搽籽', '风吹猫', '小鱼儿', '炸炸炸', '大聪明',
}


def is_real_name(name: str) -> bool:
    """判定一个 2-3 字中文词是否"看起来像真实姓名"（常见姓氏开头 + 非常用词）。"""
    if len(name) < 2 or len(name) > 3:
        return False
    if name in COMMON_WORDS:
        return False
    if name[0] not in SURNAME_SET:
        return False
    # 以职务/称谓结尾的不算姓名
    if any(name.endswith(t) for t in ('老师', '同学', '班长', '部长', '会长', '团长',
                                      '书记', '主任', '辅导员', '班主任')):
        return False
    return True


def is_at_name(name: str) -> bool:
    """@提及中的名字判定：真实姓名，或"姓氏+职务/称谓"（如 王老师、张同学）。

    @提及是明确指向某个人，即使带职务/称谓也应脱敏。
    """
    if is_real_name(name):
        return True
    if len(name) in (2, 3) and name[0] in SURNAME_SET:
        if any(name.endswith(t) for t in ('老师', '同学', '班长', '部长', '会长',
                                          '团长', '书记', '主任', '辅导员', '班主任')):
            return True
    return False


def extract_name_from_sender(sender_name: str) -> str | None:
    """从发送者昵称中提取候选姓名（2-3 个汉字，排除广告/职务前缀）。"""
    ad_keywords = ('代', '论文', '毕设', '实习', '盖章', '网课', '驾校', '拼', '取', '跑腿',
                   '刷', '降重', '薇', 'V+', 'Lunwen', 'lunwen', '三方', '病例', '社会实践',
                   '回收', '甩卖', '毕业', '相机', '游戏机', '公路车', '米粉', '索尼', '充电',
                   '配送', '大疆', '拍立得', '社团', '媒体', '视频部', '微信部', '学生会')
    if any(k in sender_name for k in ad_keywords):
        return None
    segments = re.split(r'[\s\-、/（）()0-9]+', sender_name)
    for seg in segments:
        seg = seg.strip()
        for prefix in ('班主任', '辅导员', '老师', '部长', '会长', '团长', '书记'):
            if seg.startswith(prefix):
                seg = seg[len(prefix):]
        if re.fullmatch(r'[\u4e00-\u9fa5]{2,3}', seg):
            return seg
    return None


def mask_text(text: str, real_names: list[str]) -> tuple[str, Counter]:
    """对单段文本做脱敏，返回 (脱敏文本, 统计)。"""
    stats: Counter = Counter()

    # 1. 邮箱先脱敏（避免裸域名 URL 正则吞掉邮箱的域名部分，如 abc@test.com）
    text, c = RE_EMAIL.subn(MASK_EMAIL, text)
    stats['邮箱'] += c

    # 2. 保护 URL（链接是知识库价值，内部数字不脱敏）
    urls: list[str] = []

    def _hold(m: re.Match) -> str:
        urls.append(m.group(0))
        return f'\x00URL{len(urls) - 1}\x00'

    text = RE_URL.sub(_hold, text)

    # 3. PII 数字（先长后短，避免互相吞并）
    text, c = RE_ID.subn(MASK_ID, text)
    stats['身份证'] += c
    text, c = RE_BANK.subn(MASK_BANK, text)
    stats['银行卡'] += c
    text, c = RE_PHONE.subn(MASK_PHONE, text)
    stats['手机号'] += c
    text, c = RE_WECHAT.subn(MASK_WECHAT, text)
    stats['微信号'] += c
    text, c = RE_STUDENT_ID.subn(MASK_STUDENT_ID, text)
    stats['学号'] += c
    text, c = RE_QQ.subn(MASK_QQ, text)
    stats['QQ号'] += c
    text, c = RE_DORM_ROOM.subn(MASK_DORM_ROOM, text)
    stats['宿舍房间号'] += c

    # 4. @提及中的房间号(+职务)+姓名（如 @123室长张三 / @456室长李四）
    #    须在名单姓名替换之前执行，否则职务词会阻断房间号匹配
    def _at_room(m: re.Match) -> str:
        nm = m.group(3)
        if is_at_name(nm):
            stats['姓名'] += 1
            stats['宿舍房间号'] += 1
            return '@[房间号]' + (m.group(2) or '') + MASK_NAME
        return m.group(0)

    text = RE_AT_ROOM_NAME.sub(_at_room, text)

    # 5. 名单内的真实姓名（仅"像真实姓名"的才脱敏，保护知识库）
    for name in real_names:
        if name in text:
            text = text.replace(name, MASK_NAME)
            stats['姓名'] += 1

    # 6. @提及中的真实姓名（含未在名单中的老师/同学）
    def _at(m: re.Match) -> str:
        nm = m.group(1)
        if is_at_name(nm):
            stats['姓名'] += 1
            return '@' + MASK_NAME
        return m.group(0)

    text = RE_AT_NAME.sub(_at, text)

    # 7. 还原 URL
    for i, u in enumerate(urls):
        text = text.replace(f'\x00URL{i}\x00', u)

    return text, stats


def process_file(src: Path, dst: Path, real_names: list[str]) -> dict:
    """处理单个群文件，返回统计。"""
    report: dict = {}
    pii: Counter = Counter()
    d = json.load(open(src, encoding='utf-8'))
    ci = d.get('chatInfo', {})
    report['群'] = src.name
    report['群名'] = ci.get('name', '')

    messages = d.get('messages', [])
    report['原始消息数'] = len(messages)
    masked_msgs = 0
    for m in messages:
        content = m.get('content', {})
        if not isinstance(content, dict):
            continue
        text = content.get('text', '')
        if text:
            new_text, s = mask_text(text, real_names)
            if new_text != text:
                content['text'] = new_text
                masked_msgs += 1
            pii += s
        html = content.get('html', '')
        if html:
            new_html, s = mask_text(html, real_names)
            if new_html != html:
                content['html'] = new_html
                masked_msgs += 1
            pii += s
        for el in content.get('elements', []) or []:
            if isinstance(el, dict) and isinstance(el.get('data'), dict):
                t = el['data'].get('text', '')
                if t:
                    nt, s = mask_text(t, real_names)
                    if nt != t:
                        el['data']['text'] = nt
                    pii += s
        # 发送者昵称一律脱敏（身份保护）
        sender = m.get('sender', {})
        if isinstance(sender, dict) and sender.get('name'):
            sender['name'] = MASK_NAME
            pii['发送者昵称'] += 1

    # 统计中的发送者名单也脱敏
    for s in d.get('statistics', {}).get('senders', []) or []:
        if isinstance(s, dict) and s.get('name'):
            s['name'] = MASK_NAME

    report['脱敏消息数'] = masked_msgs
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    report.update(dict(pii))
    return report


def select_latest_exports(src_dir: Path) -> list[Path]:
    """按群 ID 去重，每个群只取时间戳最新的导出文件。

    文件名格式: group_{群ID}_{YYYYMMDD}_{HHMMSS}.json
    """
    by_group: dict[str, tuple[str, Path]] = {}
    for f in glob.glob(str(src_dir / 'group_*.json')):
        m = re.match(r'group_(\d+)_(\d{8})_(\d{6})\.json', Path(f).name)
        if not m:
            continue
        gid = m.group(1)
        ts = m.group(2) + m.group(3)
        if gid not in by_group or ts > by_group[gid][0]:
            by_group[gid] = (ts, Path(f))
    return sorted(p for _, p in by_group.values())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, help='原始导出目录（含 group_*.json）')
    parser.add_argument('--output', required=True, help='脱敏输出目录')
    args = parser.parse_args(argv)

    src_dir = Path(args.input)
    out_dir = Path(args.output)
    files = select_latest_exports(src_dir)
    print('按群 ID 去重后待处理 %d 个群:' % len(files))
    for f in files:
        print('  %s' % f.name)

    # 收集所有发送者昵称 → 候选名单 → 过滤出"像真实姓名"的
    all_names: set[str] = set()
    for f in files:
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for s in d.get('statistics', {}).get('senders', []) or []:
            if isinstance(s, dict) and s.get('name'):
                n = extract_name_from_sender(s['name'])
                if n:
                    all_names.add(n)
        for m in d.get('messages', []):
            sender = m.get('sender', {})
            if isinstance(sender, dict) and sender.get('name'):
                n = extract_name_from_sender(sender['name'])
                if n:
                    all_names.add(n)
    real_names = sorted(n for n in all_names if is_real_name(n))

    print('候选姓名 %d 个 → 判定为真实姓名 %d 个（仅这些在正文中脱敏）:'
          % (len(all_names), len(real_names)))
    print('  真实姓名: %s' % ', '.join(real_names))
    print('  排除（昵称/常用词/专业名）: %s'
          % ', '.join(sorted(all_names - set(real_names))))

    total: Counter = Counter()
    report_rows = []
    for f in files:
        dst = out_dir / f.name
        try:
            r = process_file(Path(f), dst, real_names)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            print('处理失败 %s: %s' % (os.path.basename(f), exc))
            continue
        report_rows.append(r)
        for k, v in r.items():
            if k not in ('群', '群名', '原始消息数', '脱敏消息数'):
                total[k] += v
        print('  %s (%s): %d 条消息，%d 条含脱敏' % (
            r['群名'], os.path.basename(f), r['原始消息数'], r['脱敏消息数']))

    report = {
        '生成时间': '2026-08-20',
        '输入目录': str(src_dir),
        '输出目录': str(out_dir),
        '处理群数': len(report_rows),
        '候选姓名数': len(all_names),
        '真实姓名数': len(real_names),
        '真实姓名清单': real_names,
        '排除名单': sorted(all_names - set(real_names)),
        '脱敏统计': dict(total),
        '逐群明细': report_rows,
    }
    report_path = out_dir / 'desensitize_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print('\n脱敏统计（全部群）:')
    for k, v in total.most_common():
        print('  %s: %d 处' % (k, v))
    print('报告: %s' % report_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
