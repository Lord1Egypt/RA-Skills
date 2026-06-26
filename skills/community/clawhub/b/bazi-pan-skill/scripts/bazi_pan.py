#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字排盘工具 v2.0.0
天工长老开发

功能：四柱八字排盘、十神计算、大运排法、流年推算、格局判断、用神选取、详细断语
v1.0.0 基础版：四柱排盘、十神显示、大运计算
v2.0.0 升级版：流年推算、格局判断、用神选取、增强断语库
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ============== 基础数据 ==============

# 十天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 十二地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干五行
GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 地支五行
ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 天干阴阳
GAN_YIN_YANG = {
    '甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
    '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'
}

# 地支阴阳
ZHI_YIN_YANG = {
    '子': '阳', '丑': '阴', '寅': '阳', '卯': '阴', '辰': '阳', '巳': '阴',
    '午': '阳', '未': '阴', '申': '阳', '酉': '阴', '戌': '阳', '亥': '阴'
}

# 地支藏干（简化版）
ZHI_CANG_GAN = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '戊', '庚'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲'],
}

# 十神
SHI_SHEN = {
    '比肩': '同我者，阴阳同',
    '劫财': '同我者，阴阳异',
    '食神': '我生者，阴阳同',
    '伤官': '我生者，阴阳异',
    '偏财': '我克者，阴阳同',
    '正财': '我克者，阴阳异',
    '七杀': '克我者，阴阳同',
    '正官': '克我者，阴阳异',
    '偏印': '生我者，阴阳同',
    '正印': '生我者，阴阳异',
}

# 六十甲子（用于日柱查询）
LIU_SHI_JIA_ZI = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
    '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥',
]

# 节气数据（简化版，用于月柱计算）
JIE_QI = {
    1: ('小寒', '大寒'),
    2: ('立春', '雨水'),
    3: ('惊蛰', '春分'),
    4: ('清明', '谷雨'),
    5: ('立夏', '小满'),
    6: ('芒种', '夏至'),
    7: ('小暑', '大暑'),
    8: ('立秋', '处暑'),
    9: ('白露', '秋分'),
    10: ('寒露', '霜降'),
    11: ('立冬', '小雪'),
    12: ('大雪', '冬至'),
}

# ============== v2.0.0 新增数据 ==============

# 格局判断规则
GE_JU_RULES = {
    '正官格': {'月令': ['正官'], '条件': '月令正官透干，无伤官见官'},
    '七杀格': {'月令': ['七杀'], '条件': '月令七杀，有制为吉'},
    '正印格': {'月令': ['正印'], '条件': '月令正印，主聪明智慧'},
    '偏印格': {'月令': ['偏印'], '条件': '月令偏印，主特殊才能'},
    '正财格': {'月令': ['正财'], '条件': '月令正财，主稳定收入'},
    '偏财格': {'月令': ['偏财'], '条件': '月令偏财，主投机财运'},
    '食神格': {'月令': ['食神'], '条件': '月令食神，主才华横溢'},
    '伤官格': {'月令': ['伤官'], '条件': '月令伤官，主创意叛逆'},
    '建禄格': {'月令': ['比肩'], '条件': '月令比肩，主独立自主'},
    '羊刃格': {'月令': ['劫财'], '条件': '月令劫财，主冲动破财'},
}

# 用神选取规则
YONG_SHEN_RULES = {
    '木': {'喜': ['水', '木'], '忌': ['金', '火'], '说明': '木旺宜火泄，木弱宜水生'},
    '火': {'喜': ['木', '火'], '忌': ['水', '土'], '说明': '火旺宜土泄，火弱宜木生'},
    '土': {'喜': ['火', '土'], '忌': ['木', '水'], '说明': '土旺宜金泄，土弱宜火生'},
    '金': {'喜': ['土', '金'], '忌': ['火', '木'], '说明': '金旺宜水泄，金弱宜土生'},
    '水': {'喜': ['金', '水'], '忌': ['土', '火'], '说明': '水旺宜木泄，水弱宜金生'},
}

# 流年天干地支计算
def get_liu_nian_gan_zhi(year: int) -> Tuple[str, str]:
    """获取流年干支"""
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    return TIAN_GAN[gan_index], DI_ZHI[zhi_index]

# 增强版断语库
DUAN_YU_KU = {
    # 事业断语
    '事业': {
        '正官': '事业稳定，宜公职或管理岗位',
        '七杀': '事业有冲劲，宜创业或开拓性工作',
        '正印': '学业有成，宜文化教育工作',
        '偏印': '特殊才能，宜技术或研究工作',
        '正财': '收入稳定，宜固定工作',
        '偏财': '财运波动，宜投资或副业',
        '食神': '才华横溢，宜艺术或创作',
        '伤官': '创意丰富，宜自由职业',
        '比肩': '独立自主，宜合作或创业',
        '劫财': '财运起伏，需谨慎理财',
    },
    # 婚姻断语
    '婚姻': {
        '男正财': '妻贤惠，婚姻稳定',
        '男偏财': '异性缘佳，需防感情波动',
        '女正官': '夫贵，婚姻美满',
        '女七杀': '夫强势，需多包容',
        '食伤旺': '重感情，易为情所困',
        '印旺': '重精神交流，晚婚为宜',
    },
    # 财运断语
    '财运': {
        '财旺': '财运亨通，宜把握机会',
        '财弱': '财运平平，宜勤俭持家',
        '食伤生财': '才华生财，宜发挥专长',
        '比劫夺财': '财运起伏，慎防破财',
        '官星护财': '财有守护，稳定增长',
    },
    # 健康断语
    '健康': {
        '木旺': '注意肝胆、筋骨',
        '火旺': '注意心脏、血液',
        '土旺': '注意脾胃、消化',
        '金旺': '注意肺部、呼吸',
        '水旺': '注意肾脏、泌尿',
        '木弱': '肝胆虚弱，宜养肝',
        '火弱': '心脏功能弱，宜养心',
        '土弱': '脾胃不佳，宜调养',
        '金弱': '肺气不足，宜润肺',
        '水弱': '肾气不足，宜补肾',
    },
}


class BaZiPan:
    """八字排盘类 v2.0.0"""
    
    @classmethod
    def get_year_gan_zhi(cls, year: int) -> Tuple[str, str]:
        """获取年柱干支"""
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        return TIAN_GAN[gan_index], DI_ZHI[zhi_index]
    
    @classmethod
    def get_month_gan_zhi(cls, year: int, month: int, day: int) -> Tuple[str, str]:
        """获取月柱干支"""
        month_zhi_index = (month + 2) % 12
        if month_zhi_index == 0:
            month_zhi_index = 12
        month_zhi = DI_ZHI[month_zhi_index - 1]
        
        year_gan, _ = cls.get_year_gan_zhi(year)
        year_gan_index = TIAN_GAN.index(year_gan)
        
        start_gan_map = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
        start_gan_index = start_gan_map.get(year_gan_index, 2)
        
        month_gan_index = (start_gan_index + month - 1) % 10
        month_gan = TIAN_GAN[month_gan_index]
        
        return month_gan, month_zhi
    
    @classmethod
    def get_day_gan_zhi(cls, year: int, month: int, day: int) -> Tuple[str, str]:
        """获取日柱干支"""
        base_date = datetime(1900, 1, 31)
        target_date = datetime(year, month, day)
        delta_days = (target_date - base_date).days
        
        jia_zi_index = (10 + delta_days) % 60
        if jia_zi_index < 0:
            jia_zi_index += 60
        
        gan_zhi = LIU_SHI_JIA_ZI[jia_zi_index]
        return gan_zhi[0], gan_zhi[1]
    
    @classmethod
    def get_hour_gan_zhi(cls, day_gan: str, hour: int) -> Tuple[str, str]:
        """获取时柱干支"""
        hour_zhi_index = ((hour + 1) % 24) // 2
        hour_zhi = DI_ZHI[hour_zhi_index]
        
        day_gan_index = TIAN_GAN.index(day_gan)
        
        start_gan_map = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
        start_gan_index = start_gan_map.get(day_gan_index, 0)
        
        hour_gan_index = (start_gan_index + hour_zhi_index) % 10
        hour_gan = TIAN_GAN[hour_gan_index]
        
        return hour_gan, hour_zhi
    
    @classmethod
    def get_shi_shen(cls, day_gan: str, other_gan: str) -> str:
        """根据日干计算十神"""
        day_wuxing = GAN_WUXING[day_gan]
        day_yin_yang = GAN_YIN_YANG[day_gan]
        
        other_wuxing = GAN_WUXING[other_gan]
        other_yin_yang = GAN_YIN_YANG[other_gan]
        
        if day_wuxing == other_wuxing:
            if day_yin_yang == other_yin_yang:
                return '比肩'
            else:
                return '劫财'
        
        wuxing_sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        if wuxing_sheng.get(day_wuxing) == other_wuxing:
            if day_yin_yang == other_yin_yang:
                return '食神'
            else:
                return '伤官'
        
        wuxing_ke = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
        if wuxing_ke.get(day_wuxing) == other_wuxing:
            if day_yin_yang == other_yin_yang:
                return '偏财'
            else:
                return '正财'
        
        reverse_ke = {'土': '木', '金': '火', '水': '土', '木': '金', '火': '水'}
        if reverse_ke.get(day_wuxing) == other_wuxing:
            if day_yin_yang == other_yin_yang:
                return '七杀'
            else:
                return '正官'
        
        reverse_sheng = {'火': '木', '土': '火', '金': '土', '水': '金', '木': '水'}
        if reverse_sheng.get(day_wuxing) == other_wuxing:
            if day_yin_yang == other_yin_yang:
                return '偏印'
            else:
                return '正印'
        
        return '未知'
    
    @classmethod
    def get_da_yun(cls, year: int, month: int, day: int, hour: int, gender: str = '男') -> List[Dict]:
        """计算大运"""
        year_gan, _ = cls.get_year_gan_zhi(year)
        year_yin_yang = GAN_YIN_YANG[year_gan]
        
        if (year_yin_yang == '阳' and gender == '男') or (year_yin_yang == '阴' and gender == '女'):
            shun_ni = '顺'
            direction = 1
        else:
            shun_ni = '逆'
            direction = -1
        
        month_gan, month_zhi = cls.get_month_gan_zhi(year, month, day)
        month_gan_index = TIAN_GAN.index(month_gan)
        month_zhi_index = DI_ZHI.index(month_zhi)
        
        da_yun = []
        for i in range(8):
            gan_index = (month_gan_index + (i + 1) * direction) % 10
            zhi_index = (month_zhi_index + (i + 1) * direction) % 12
            
            da_yun.append({
                '步数': i + 1,
                '干支': TIAN_GAN[gan_index] + DI_ZHI[zhi_index],
                '天干': TIAN_GAN[gan_index],
                '地支': DI_ZHI[zhi_index],
                '起始年龄': (i + 1) * 10 + 3,
            })
        
        return da_yun
    
    # ============== v2.0.0 新增功能 ==============
    
    @classmethod
    def get_ge_ju(cls, si_zhu: Dict, shi_shen: Dict) -> Optional[str]:
        """格局判断 v2.0.0"""
        # 以月令为主
        yue_zhu_shi_shen = shi_shen.get('月柱', '')
        
        for ge_ju, rule in GE_JU_RULES.items():
            if yue_zhu_shi_shen in rule['月令']:
                return ge_ju
        
        return None
    
    @classmethod
    def get_yong_shen(cls, day_gan: str, wuxing_count: Dict) -> Dict:
        """用神选取 v2.0.0"""
        day_wuxing = GAN_WUXING[day_gan]
        
        # 判断日主旺衰
        total = sum(wuxing_count.values())
        day_wuxing_count = wuxing_count[day_wuxing]
        
        # 简化判断：同党（生我 + 同我）vs 异党
        sheng_wo_wuxing = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        tong_dang = day_wuxing_count + wuxing_count.get(sheng_wo_wuxing[day_wuxing], 0)
        
        if tong_dang >= 4:
            wang_shuai = '旺'
            yong_shen_type = '泄耗'
        else:
            wang_shuai = '弱'
            yong_shen_type = '生扶'
        
        rule = YONG_SHEN_RULES[day_wuxing]
        
        return {
            '日主五行': day_wuxing,
            '旺衰': wang_shuai,
            '用神类型': yong_shen_type,
            '喜用': rule['喜'],
            '忌神': rule['忌'],
            '说明': rule['说明'],
        }
    
    @classmethod
    def get_liu_nian(cls, year: int, si_zhu: Dict, day_gan: str) -> Dict:
        """流年推算 v2.0.0"""
        liu_nian_gan, liu_nian_zhi = get_liu_nian_gan_zhi(year)
        
        # 流年十神
        liu_nian_shi_shen = cls.get_shi_shen(day_gan, liu_nian_gan)
        
        # 流年与四柱关系
        chong_ke = []
        
        # 检查冲克
        zhi_chong = {'子': '午', '丑': '未', '寅': '申', '卯': '酉', 
                     '辰': '戌', '巳': '亥', '午': '子', '未': '丑',
                     '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'}
        
        for zhu_name, (gan, zhi) in si_zhu.items():
            if zhi_chong.get(zhi) == liu_nian_zhi:
                chong_ke.append(f'{zhu_name}相冲')
            if GAN_WUXING[liu_nian_gan] == GAN_WUXING[gan] and liu_nian_gan != gan:
                chong_ke.append(f'{zhu_name}天干相克')
        
        # 流年断语
        duan_yu = DUAN_YU_KU['事业'].get(liu_nian_shi_shen, '流年平稳，顺势而为')
        
        return {
            '流年': f'{liu_nian_gan}{liu_nian_zhi}',
            '流年十神': liu_nian_shi_shen,
            '冲克': chong_ke if chong_ke else ['无重大冲克'],
            '断语': duan_yu,
        }
    
    @classmethod
    def get_zeng_qiang_duan_yu(cls, day_gan: str, si_zhu: Dict, shi_shen: Dict, 
                                wuxing_count: Dict, ge_ju: Optional[str], 
                                yong_shen: Dict) -> List[str]:
        """增强断语库 v2.0.0"""
        duan_yu = []
        
        # 日主断语
        ri_gan_duan_yu = {
            '甲': '甲木参天，正直仁慈，有上进心',
            '乙': '乙木柔顺，温和善良，适应力强',
            '丙': '丙火太阳，热情开朗，表现欲强',
            '丁': '丁火灯烛，温和内敛，心思细腻',
            '戊': '戊土大地，厚重诚实，包容力强',
            '己': '己土田园，细腻谨慎，善于谋划',
            '庚': '庚金刀剑，刚毅果断，执行力强',
            '辛': '辛金珠玉，温润秀气，重面子',
            '壬': '壬水江河，聪明灵活，适应力强',
            '癸': '癸水雨露，温柔内敛，直觉敏锐',
        }
        
        if day_gan in ri_gan_duan_yu:
            duan_yu.append(f"【日主】{ri_gan_duan_yu[day_gan]}")
        
        # 格局断语
        if ge_ju:
            ge_ju_duan = {
                '正官格': '【格局】正官格：事业稳定，宜公职管理',
                '七杀格': '【格局】七杀格：有冲劲魄力，宜开拓创业',
                '正印格': '【格局】正印格：聪明智慧，利学业文化',
                '偏印格': '【格局】偏印格：特殊才能，利技术研究',
                '正财格': '【格局】正财格：财运稳定，宜固定工作',
                '偏财格': '【格局】偏财格：财运波动，宜投资副业',
                '食神格': '【格局】食神格：才华横溢，利艺术创作',
                '伤官格': '【格局】伤官格：创意丰富，利自由职业',
                '建禄格': '【格局】建禄格：独立自主，利合作创业',
                '羊刃格': '【格局】羊刃格：性格刚烈，需修身养性',
            }
            if ge_ju in ge_ju_duan:
                duan_yu.append(ge_ju_duan[ge_ju])
        
        # 用神断语
        duan_yu.append(f"【用神】日主{yong_shen['日主五行']}{yong_shen['旺衰']}，喜{','.join(yong_shen['喜用'])}，忌{','.join(yong_shen['忌神'])}")
        
        # 五行断语
        for wx, count in wuxing_count.items():
            if count == 0:
                duan_yu.append(f"【五行】五行缺{wx}，需后天补救")
            elif count >= 3:
                duan_yu.append(f"【五行】{wx}过旺，需适当泄耗")
        
        # 健康断语
        for wx in ['木', '火', '土', '金', '水']:
            if wuxing_count[wx] <= 1:
                duan_yu.append(f"【健康】{wx}弱，{DUAN_YU_KU['健康'].get(f'{wx}弱', '')}")
        
        # 事业断语（基于月柱十神）
        yue_zhu_shi_shen = shi_shen.get('月柱', '')
        if yue_zhu_shi_shen in DUAN_YU_KU['事业']:
            duan_yu.append(f"【事业】{DUAN_YU_KU['事业'][yue_zhu_shi_shen]}")
        
        return duan_yu


def bazi_pan(
    date_str: str,
    hour: int,
    gender: str = '男',
    liu_nian_year: Optional[int] = None
) -> Dict:
    """
    八字排盘主函数 v2.0.0
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    year, month, day = dt.year, dt.month, dt.day
    
    # 四柱
    year_gan, year_zhi = BaZiPan.get_year_gan_zhi(year)
    month_gan, month_zhi = BaZiPan.get_month_gan_zhi(year, month, day)
    day_gan, day_zhi = BaZiPan.get_day_gan_zhi(year, month, day)
    hour_gan, hour_zhi = BaZiPan.get_hour_gan_zhi(day_gan, hour)
    
    si_zhu = {
        '年柱': (year_gan, year_zhi),
        '月柱': (month_gan, month_zhi),
        '日柱': (day_gan, day_zhi),
        '时柱': (hour_gan, hour_zhi),
    }
    
    # 十神
    shi_shen = {
        '年柱': BaZiPan.get_shi_shen(day_gan, year_gan),
        '月柱': BaZiPan.get_shi_shen(day_gan, month_gan),
        '日柱': '日主',
        '时柱': BaZiPan.get_shi_shen(day_gan, hour_gan),
    }
    
    # 大运
    da_yun = BaZiPan.get_da_yun(year, month, day, hour, gender)
    
    # 五行统计
    wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    for zhu in si_zhu.values():
        wuxing_count[GAN_WUXING[zhu[0]]] += 1
        wuxing_count[ZHI_WUXING[zhu[1]]] += 1
    
    # v2.0.0 新增功能
    ge_ju = BaZiPan.get_ge_ju(si_zhu, shi_shen)
    yong_shen = BaZiPan.get_yong_shen(day_gan, wuxing_count)
    duan_yu = BaZiPan.get_zeng_qiang_duan_yu(day_gan, si_zhu, shi_shen, wuxing_count, ge_ju, yong_shen)
    
    # 流年推算
    liu_nian = None
    if liu_nian_year:
        liu_nian = BaZiPan.get_liu_nian(liu_nian_year, si_zhu, day_gan)
    
    result = {
        '出生时间': f"{date_str} {hour:02d}:00",
        '性别': gender,
        '四柱': {k: f"{v[0]}{v[1]}" for k, v in si_zhu.items()},
        '十神': shi_shen,
        '五行统计': wuxing_count,
        '大运': da_yun,
        '日主': day_gan,
        '格局': ge_ju,
        '用神': yong_shen,
        '流年': liu_nian,
        '断语': duan_yu,
    }
    
    return result


def format_output(result: Dict) -> str:
    """格式化输出 v2.0.0"""
    output = []
    
    output.append("【八字排盘】v2.0.0")
    output.append(f"• 出生时间：{result['出生时间']}")
    output.append(f"• 性别：{result['性别']}")
    output.append("")
    output.append("【四柱】")
    output.append(f"    年柱    月柱    日柱    时柱")
    output.append(f"    {result['四柱']['年柱']}    {result['四柱']['月柱']}    {result['四柱']['日柱']}    {result['四柱']['时柱']}")
    output.append("")
    output.append("【十神】")
    output.append(f"    {result['十神']['年柱']}    {result['十神']['月柱']}    {result['十神']['日柱']}    {result['十神']['时柱']}")
    output.append("")
    output.append("【五行统计】")
    wuxing = result['五行统计']
    output.append(f"    木：{wuxing['木']}  火：{wuxing['火']}  土：{wuxing['土']}  金：{wuxing['金']}  水：{wuxing['水']}")
    
    que_shi = [k for k, v in wuxing.items() if v == 0]
    if que_shi:
        output.append(f"    ⚠️  五行缺：{', '.join(que_shi)}")
    
    output.append("")
    output.append("【大运】")
    for dy in result['大运']:
        output.append(f"    {dy['起始年龄']}岁：{dy['干支']}")
    
    # v2.0.0 新增
    if result['格局']:
        output.append("")
        output.append("【格局】")
        output.append(f"    {result['格局']}")
    
    if result['用神']:
        yong = result['用神']
        output.append("")
        output.append("【用神】")
        output.append(f"    日主{yong['日主五行']}{yong['旺衰']}，喜{','.join(yong['喜用'])}，忌{','.join(yong['忌神'])}")
        output.append(f"    {yong['说明']}")
    
    if result['流年']:
        ln = result['流年']
        output.append("")
        output.append(f"【{ln['流年']}流年】")
        output.append(f"    流年十神：{ln['流年十神']}")
        output.append(f"    冲克：{', '.join(ln['冲克'])}")
        output.append(f"    断语：{ln['断语']}")
    
    output.append("")
    output.append("【详细断语】")
    for duan in result['断语']:
        output.append(f"• {duan}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='八字排盘工具 v2.0.0')
    parser.add_argument('--date', '-d', type=str, required=True, help='出生日期 (YYYY-MM-DD)')
    parser.add_argument('--hour', '-H', type=int, required=True, help='出生时辰 (0-23)')
    parser.add_argument('--gender', '-g', type=str, default='男', choices=['男', '女'], help='性别')
    parser.add_argument('--liu-nian', '-l', type=int, help='流年年份（可选）')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        result = bazi_pan(args.date, args.hour, args.gender, args.liu_nian)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result))
            
    except Exception as e:
        print(f"排盘错误：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
