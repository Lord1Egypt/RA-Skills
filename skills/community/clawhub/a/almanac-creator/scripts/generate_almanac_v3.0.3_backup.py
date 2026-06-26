#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄历生成脚本 V3.0.3 - 抖音优化版
升级内容：
1. 【V3.0.1 新增】节气计算通用化（支持 1900-2100 年）
2. 【V3.0.1 新增】批量生成功能（一次生成 7 天/30 天）
3. 【V3.0.1 新增】配置文件支持（config.yaml）
4. 集成 lunar-python 库（lunar-java 的 Python 版本）
5. 干支计算 - 使用 lunar-python 准确计算
6. 宜忌生成 - 使用 lunar-python 传统算法

版本：V3.0.3
日期：2026-04-18
"""

import sys
import io
from PIL import Image, ImageDraw, ImageFont
import os
import argparse
from datetime import datetime, timedelta
import yaml

# 导入 lunar-python（lunar-java 的 Python 版本）
from lunar_python import Lunar, Solar

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 图片规格
WIDTH = 1080
PAGE_HEIGHT = 1400
BACKGROUND_COLOR = '#F8F0E6'

# 【V2.3 新增】5 套模板配色方案
TEMPLATES = {
    'traditional': {
        'name': '传统中国风',
        'bg': '#F8F0E6',        # 米黄宣纸色
        'border_outer': '#8B0000',  # 中国红外框
        'border_inner': '#D4AF37',  # 金色内框
        'title': '#8B0000',     # 中国红标题
        'section': '#C41E3A',   # 亮红色栏目
        'text': '#2C2C2C',      # 墨黑色正文
        'small': '#999999',     # 浅灰色小字
        'separator': '#D4AF37', # 金色分隔线
        'decoration': 'double_border'  # 双层边框
    },
    'modern': {
        'name': '简约现代风',
        'bg': '#F0F4F8',        # 浅蓝灰背景
        'border_outer': '#2C5F8D',  # 深蓝色外框
        'border_inner': '#C9A961',  # 香槟金内框
        'title': '#1A3A52',     # 深蓝黑标题
        'section': '#2C5F8D',   # 深蓝色栏目
        'text': '#1A3A52',      # 深蓝黑正文
        'small': '#6B7280',     # 中灰色小字
        'separator': '#C9A961', # 香槟金分隔线
        'decoration': 'single_border'  # 单层边框
    },
    'festive': {
        'name': '喜庆吉祥风',
        'bg': '#FFF5E6',        # 暖白色背景
        'border_outer': '#D4AF37',  # 金色外框
        'border_inner': '#FF6B35',  # 橙红色内框
        'title': '#D4AF37',     # 金色标题
        'section': '#FF6B35',   # 橙红色栏目
        'text': '#8B0000',      # 深红色正文
        'small': '#B8860B',     # 暗金色小字
        'separator': '#FF6B35', # 橙红色分隔线
        'decoration': 'ornament'  # 装饰花纹
    },
    'elegant': {
        'name': '典雅古风',
        'bg': '#F5F5DC',        # 宣纸色背景
        'border_outer': '#4A5D4F',  # 墨绿色外框
        'border_inner': '#9A8B4F',  # 古铜金内框
        'title': '#2C3E36',     # 深绿黑标题
        'section': '#4A5D4F',   # 墨绿色栏目
        'text': '#2C3E36',      # 深绿黑正文
        'small': '#8B8680',     # 灰褐色小字
        'separator': '#9A8B4F', # 古铜金分隔线
        'decoration': 'cloud'   # 祥云装饰
    },
    'fresh': {
        'name': '清新自然风',
        'bg': '#F0F8E6',        # 浅绿色背景
        'border_outer': '#6B8E4E',  # 草绿色外框
        'border_inner': '#B8C99E',  # 嫩绿色内框
        'title': '#3A4F2E',     # 深绿色标题
        'section': '#6B8E4E',   # 草绿色栏目
        'text': '#3A4F2E',      # 深绿色正文
        'small': '#8FA885',     # 浅绿色小字
        'separator': '#B8C99E', # 嫩绿色分隔线
        'decoration': 'leaf'    # 叶子装饰
    }
}

# 颜色标准（默认使用 traditional 模板）
COLORS = TEMPLATES['traditional']

# 字体大小标准（V2.3 优化版 - 加大字号提升可读性）
FONT_SIZES = {
    'title': 90,
    'subtitle': 65,
    'section': 60,        # 55 → 60 (+5px) 栏目题加大
    'content': 48,        # 45 → 48 (+3px) 正文加大
    'content_large': 44,  # 40 → 44 (+4px) 故事/养生正文加大
    'small': 40           # 38 → 40 (+2px) 小字加大
}

# 间距设置（V2.3 优化版 - 增加行间距提升可读性）
SPACING = {
    'after_title': 10,
    'after_subtitle': 8,
    'after_lunar': 6,
    'after_ganzhi': 8,
    'after_special': 25,
    'after_section': 28,   # 25 → 28 (+3px) 栏目后间距加大
    'after_content': 20,   # 18 → 20 (+2px) 内容后间距加大
    'after_zodiac_title': 12,
    'after_zodiac_item': 6,
    'separator_after': 28, # 25 → 28 (+3px) 分隔线后间距加大
}

def load_config(config_path=None):
    """【V3.0.1 新增】加载配置文件"""
    if config_path is None:
        # 默认加载脚本同目录的 config.yaml
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '..', 'config.yaml')
    
    default_config = {
        'output': {'base_dir': './reports', 'quality': 95, 'overwrite': True},
        'font': FONT_SIZES,
        'spacing': SPACING,
        'template': {'default': 'traditional', 'rotation': True},
        'features': {'show_jieqi': True, 'show_story': True},
        'batch': {'default_days': 7, 'max_days': 365},
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                # 合并配置（配置文件优先）
                for key in default_config:
                    if key in config:
                        if isinstance(default_config[key], dict):
                            default_config[key].update(config[key])
                        else:
                            default_config[key] = config[key]
            print(f" 已加载配置文件：{config_path}")
        except Exception as e:
            print(f" 配置文件加载失败：{e}，使用默认配置")
    else:
        print(f"ℹ️ 未找到配置文件，使用默认配置")
    
    return default_config


def get_template(date_str, config=None):
    """【V2.3 新增】根据日期选择模板（每日轮换）"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # 从配置文件读取模板设置
    if config and 'template' in config:
        template_config = config['template']
        if not template_config.get('rotation', True):
            # 不启用轮换，使用默认模板
            default_name = template_config.get('default', 'traditional')
            return default_name, TEMPLATES.get(default_name, TEMPLATES['traditional'])
    
    # 按日期轮换模板（5 天一个循环）
    template_names = list(TEMPLATES.keys())
    rotation_days = config.get('template', {}).get('rotation_days', 5) if config else 5
    template_index = date_obj.day % len(template_names)
    template_name = template_names[template_index]
    return template_name, TEMPLATES[template_name]

def load_fonts(template_name='traditional'):
    """加载字体（统一使用黑体，保持可读性和品牌一致性）"""
    try:
        # 统一使用黑体（所有模板）
        font_file = 'C:/Windows/Fonts/simhei.ttf'
        
        fonts = {
            'title': ImageFont.truetype(font_file, FONT_SIZES['title']),
            'subtitle': ImageFont.truetype(font_file, FONT_SIZES['subtitle']),
            'section': ImageFont.truetype(font_file, FONT_SIZES['section']),
            'content': ImageFont.truetype(font_file, FONT_SIZES['content']),
            'small': ImageFont.truetype(font_file, FONT_SIZES['small'])
        }
        
        # 【V3.0.3 新增】加载 emoji 字体（Windows Segoe UI Emoji）
        try:
            emoji_font_file = 'C:/Windows/Fonts/seguiemj.ttf'
            fonts['emoji'] = ImageFont.truetype(emoji_font_file, FONT_SIZES['content'])
        except:
            # 如果找不到 emoji 字体，回退到黑体
            fonts['emoji'] = fonts['content']
            
    except:
        fonts = {size: ImageFont.load_default() for size in FONT_SIZES}
        fonts['emoji'] = fonts['content']
    return fonts

def draw_centered_text(draw, text, y, font, color):
    """居中绘制文字（支持颜色名称或色值）"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, y), text, fill=color, font=font)
    return y + (bbox[3] - bbox[1])

def get_color(template, color_name):
    """【V2.3 新增】获取模板颜色"""
    # 如果 color_name 是色值（以#开头），直接返回
    if color_name.startswith('#'):
        return color_name
    
    # 否则从模板中获取
    return template.get(color_name, '#2C2C2C')

def draw_decoration(draw, template_name, template):
    """【V2.3 新增】根据模板绘制装饰元素"""
    decoration_type = template.get('decoration', 'double_border')
    
    if decoration_type == 'double_border':
        # 传统双层边框
        draw.rectangle([10, 10, WIDTH-10, PAGE_HEIGHT-10], 
                       outline=template['border_outer'], width=8)
        draw.rectangle([22, 22, WIDTH-22, PAGE_HEIGHT-22], 
                       outline=template['border_inner'], width=2)
    
    elif decoration_type == 'single_border':
        # 简约单层边框
        draw.rectangle([15, 15, WIDTH-15, PAGE_HEIGHT-15], 
                       outline=template['border_outer'], width=4)
        draw.rectangle([25, 25, WIDTH-25, PAGE_HEIGHT-25], 
                       outline=template['border_inner'], width=1)
    
    elif decoration_type == 'ornament':
        # 喜庆装饰（添加角花）
        draw.rectangle([10, 10, WIDTH-10, PAGE_HEIGHT-10], 
                       outline=template['border_outer'], width=6)
        draw.rectangle([20, 20, WIDTH-20, PAGE_HEIGHT-20], 
                       outline=template['border_inner'], width=2)
        # 四角装饰
        corner_size = 40
        # 左上角
        draw.arc([10, 10, 10+corner_size, 10+corner_size], 0, 90, 
                 fill=template['border_inner'], width=3)
        # 右上角
        draw.arc([WIDTH-10-corner_size, 10, WIDTH-10, 10+corner_size], 90, 180, 
                 fill=template['border_inner'], width=3)
        # 左下角
        draw.arc([10, PAGE_HEIGHT-10-corner_size, 10+corner_size, PAGE_HEIGHT-10], 270, 360, 
                 fill=template['border_inner'], width=3)
        # 右下角
        draw.arc([WIDTH-10-corner_size, PAGE_HEIGHT-10-corner_size, WIDTH-10, PAGE_HEIGHT-10], 180, 270, 
                 fill=template['border_inner'], width=3)
    
    elif decoration_type == 'cloud':
        # 典雅古风（祥云装饰简化版）
        draw.rectangle([12, 12, WIDTH-12, PAGE_HEIGHT-12], 
                       outline=template['border_outer'], width=5)
        draw.rectangle([24, 24, WIDTH-24, PAGE_HEIGHT-24], 
                       outline=template['border_inner'], width=2)
        # 顶部祥云（简化为弧线）
        for i in range(5):
            x = 100 + i * 200
            draw.arc([x, 15, x+60, 75], 0, 180, 
                     fill=template['border_inner'], width=2)
    
    elif decoration_type == 'leaf':
        # 清新自然（叶子装饰简化版）
        draw.rectangle([10, 10, WIDTH-10, PAGE_HEIGHT-10], 
                       outline=template['border_outer'], width=4)
        draw.rectangle([22, 22, WIDTH-22, PAGE_HEIGHT-22], 
                       outline=template['border_inner'], width=2)
        # 四角叶子（简化为椭圆）
        leaf_size = 30
        # 左上角
        draw.ellipse([10, 10, 10+leaf_size, 10+leaf_size*2], 
                     outline=template['border_inner'], width=2)
        # 右上角
        draw.ellipse([WIDTH-10-leaf_size, 10, WIDTH-10, 10+leaf_size*2], 
                     outline=template['border_inner'], width=2)
        # 左下角
        draw.ellipse([10, PAGE_HEIGHT-10-leaf_size*2, 10+leaf_size, PAGE_HEIGHT-10], 
                     outline=template['border_inner'], width=2)
        # 右下角
        draw.ellipse([WIDTH-10-leaf_size, PAGE_HEIGHT-10-leaf_size*2, WIDTH-10, PAGE_HEIGHT-10], 
                     outline=template['border_inner'], width=2)

def draw_double_border(draw):
    """绘制双层边框（兼容旧版）"""
    draw.rectangle([10, 10, WIDTH-10, PAGE_HEIGHT-10], 
                   outline=COLORS['border_outer'], width=8)
    draw.rectangle([22, 22, WIDTH-22, PAGE_HEIGHT-22], 
                   outline=COLORS['border_inner'], width=2)

def draw_separator(draw, y, color='#D4AF37'):
    """绘制分隔线（支持自定义颜色）"""
    draw.line([(80, y), (WIDTH-80, y)], fill=color, width=2)
    return y + SPACING['separator_after']

def get_month_ganzhi_by_jieqi(year, month, day):
    """
    【V3.0.1 修复】根据节气计算月柱（替代 lunar-python 的农历月干支）
    
    节气月规则：
    - 寅月：立春 (2/4) - 惊蛰前
    - 卯月：惊蛰 (3/5) - 清明前
    - 辰月：清明 (4/5) - 立夏前
    - 巳月：立夏 (5/5) - 芒种前
    - ...
    """
    # 年干定月干（五虎遁元）
    # 甲己年起丙寅，乙庚年起戊寅，丙辛年起庚寅，丁壬年起壬寅，戊癸年起甲寅
    YEAR_GAN_START = {
        '甲': '丙', '己': '丙',
        '乙': '戊', '庚': '戊',
        '丙': '庚', '辛': '庚',
        '丁': '壬', '癸': '壬',
        '戊': '甲',
    }
    
    GAN = '甲乙丙丁戊己庚辛壬癸'
    ZHI = '寅卯辰巳午未申酉戌亥子丑'
    
    # 判断节气月支
    if month == 1:
        month_zhi = '丑' if day < 7 else '子'
    elif month == 2:
        month_zhi = '丑' if day < 4 else '寅'
    elif month == 3:
        month_zhi = '寅' if day < 5 else '卯'
    elif month == 4:
        month_zhi = '卯' if day < 5 else '辰'
    elif month == 5:
        month_zhi = '辰' if day < 5 else '巳'
    elif month == 6:
        month_zhi = '巳' if day < 5 else '午'
    elif month == 7:
        month_zhi = '午' if day < 7 else '未'
    elif month == 8:
        month_zhi = '未' if day < 7 else '申'
    elif month == 9:
        month_zhi = '申' if day < 7 else '酉'
    elif month == 10:
        month_zhi = '酉' if day < 8 else '戌'
    elif month == 11:
        month_zhi = '戌' if day < 7 else '亥'
    elif month == 12:
        month_zhi = '亥' if day < 7 else '子'
    
    # 获取年干
    lunar = Lunar.fromYmd(year, month, day)
    year_gz = lunar.getYearInGanZhi()
    year_gan = year_gz[0]
    
    # 计算月干
    start_gan = YEAR_GAN_START[year_gan]
    start_gan_idx = GAN.find(start_gan)
    month_zhi_idx = ZHI.find(month_zhi)
    month_gan_idx = (start_gan_idx + month_zhi_idx) % 10
    month_gan = GAN[month_gan_idx]
    
    return f"{month_gan}{month_zhi}"


def get_ganzhi(date_str):
    """
    【V3.0.1 升级】使用 lunar-python 计算干支 + 节气（支持 1900-2100 年）
    
    升级内容：
    1. 年柱：使用 Solar 转换（准确）
    2. 月柱：根据节气计算（修复 lunar-python 农历月问题）
    3. 日柱：使用 Solar 转换（准确）
    4. 节气：使用 Solar 转换（支持任意年份）
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # 【V3.0.1 修复】使用 Solar 转换公历到农历（不是 Lunar.fromYmd）
    solar = Solar.fromYmd(date_obj.year, date_obj.month, date_obj.day)
    lunar = solar.getLunar()
    
    # lunar-python 提供年柱和日柱（准确）
    year_gz = lunar.getYearInGanZhi()
    day_gz = lunar.getDayInGanZhi()
    
    # 【V3.0.1 修复】月柱根据节气计算（不用 lunar-python 的农历月）
    month_gz = get_month_ganzhi_by_jieqi(date_obj.year, date_obj.month, date_obj.day)
    
    # 【V3.0.1 新增】节气计算
    jieqi = lunar.getJieQi()
    
    ganzhi_data = {
        'year': year_gz,
        'month': month_gz,
        'day': day_gz,
        'jieqi': jieqi,
        'jieqi_text': f"今日{jieqi}" if jieqi else "",
    }
    
    return f"{year_gz}年 {month_gz}月 {day_gz}日", day_gz, ganzhi_data

def get_jishi(day_ganzhi):
    """【修复 2】使用十二神值时准确计算吉凶"""
    # 天干对应索引（五鼠遁元）
    tian_gan_map = {
        '甲': 0, '己': 0,  # 甲己日起甲子时
        '乙': 1, '庚': 1,  # 乙庚日起丙子时
        '丙': 2, '辛': 2,  # 丙辛日起戊子时
        '丁': 3, '壬': 3,  # 丁壬日起庚子时
        '戊': 4, '癸': 4,  # 戊癸日起壬子时
    }
    
    # 12 时辰
    shi_chen = [
        ('子时', '23-1 点'), ('丑时', '1-3 点'), ('寅时', '3-5 点'),
        ('卯时', '5-7 点'), ('辰时', '7-9 点'), ('巳时', '9-11 点'),
        ('午时', '11-13 点'), ('未时', '13-15 点'), ('申时', '15-17 点'),
        ('酉时', '17-19 点'), ('戌时', '19-21 点'), ('亥时', '21-23 点')
    ]
    
    # 十二神（固定顺序）
    shi_er_shen = [
        '青龙', '明堂', '天刑', '朱雀', '金匮', '天德',
        '白虎', '玉堂', '天牢', '玄武', '司命', '勾陈'
    ]
    
    # 吉凶属性
    shen_jixiong = {
        '青龙': '吉', '明堂': '吉', '金匮': '吉', 
        '天德': '吉', '玉堂': '吉', '司命': '吉',
        '天刑': '凶', '朱雀': '凶', '白虎': '凶',
        '天牢': '凶', '玄武': '凶', '勾陈': '凶'
    }
    
    # 根据日干确定起始神
    gan = day_ganzhi[0]
    start_index = tian_gan_map.get(gan, 0)
    
    # 计算 12 时辰对应的神
    ji_shi = []
    xiong_shi = []
    
    for i, (name, time) in enumerate(shi_chen):
        shen_index = (start_index + i) % 12
        shen_name = shi_er_shen[shen_index]
        jixiong = shen_jixiong[shen_name]
        
        if jixiong == '吉':
            ji_shi.append(f"{name} ({time})")
        else:
            xiong_shi.append(f"{name} ({time})")
    
    return {
        'ji': ji_shi,
        'xiong': xiong_shi
    }

def get_changyi(day_ganzhi):
    """根据日柱天干计算穿衣建议（五行颜色）"""
    wu_xing_map = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    color_map = {
        '木': {'lucky': '绿色、青色', 'avoid': '白色、金色'},
        '火': {'lucky': '红色、紫色', 'avoid': '黑色、蓝色'},
        '土': {'lucky': '黄色、棕色', 'avoid': '绿色、青色'},
        '金': {'lucky': '白色、金色', 'avoid': '红色、紫色'},
        '水': {'lucky': '黑色、蓝色', 'avoid': '黄色、棕色'}
    }
    
    gan = day_ganzhi[0]
    wx = wu_xing_map.get(gan, '火')
    return color_map.get(wx, {'lucky': '红色、紫色', 'avoid': '黑色、蓝色'})

def get_cai_shen(day_ganzhi):
    """【修复 3】根据日干准确计算财神方位"""
    cai_shen_map = {
        '甲': {'xi': "东南方", 'fu': "正南方", 'cai': "东北方", 'tai': "占门床外正南"},
        '乙': {'xi': "西北方", 'fu': "正北方", 'cai': "东北方", 'tai': "占厨灶厕外西南"},
        '丙': {'xi': "西南方", 'fu': "正东方", 'cai': "正西方", 'tai': "占门户碓磨外正南"},
        '丁': {'xi': "正南方", 'fu': "正东方", 'cai': "正西方", 'tai': "占房床厕外正南"},
        '戊': {'xi': "东南方", 'fu': "正南方", 'cai': "正北方", 'tai': "占门床外正南"},
        '己': {'xi': "东北方", 'fu': "正南方", 'cai': "正北方", 'tai': "占碓磨厕外东南"},
        '庚': {'xi': "西北方", 'fu': "西南方", 'cai': "正东方", 'tai': "占房床厕外东北"},
        '辛': {'xi': "西南方", 'fu': "东北方", 'cai': "正东方", 'tai': "占仓库厕外正东"},
        '壬': {'xi': "正北方", 'fu': "西南方", 'cai': "正南方", 'tai': "占门床外正南"},
        '癸': {'xi': "东南方", 'fu': "正西方", 'cai': "正南方", 'tai': "占房床厕外东北"}
    }
    
    gan = day_ganzhi[0]
    return cai_shen_map.get(gan, cai_shen_map['甲'])

def get_almanac_data(date_str):
    """获取黄历数据（修复版）"""
    from lunarcalendar import Converter, Solar
    from datetime import datetime
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    weekday = date_obj.weekday()
    weekday_names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    
    # 转换为农历
    solar = Solar(date_obj.year, date_obj.month, date_obj.day)
    lunar = Converter.Solar2Lunar(solar)
    
    # 农历日期
    lunar_months = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
    lunar_days = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                  '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                  '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
    
    lunar_month_name = lunar_months[lunar.month - 1]
    lunar_day_name = lunar_days[lunar.day - 1]
    lunar_date = f"农历{lunar.year}年{lunar_month_name}月{lunar_day_name}"
    
    # 【V3.0.1 升级】获取准确干支 + 节气
    ganzhi_full, day_gz, ganzhi_data = get_ganzhi(date_str)
    
    # 【V3.0.1 升级】节气信息（支持任意年份）
    jieqi_text = ganzhi_data['jieqi_text']  # 如"今日清明"或""
    jieqi = ganzhi_data['jieqi']  # 节气名或 None
    
    # 【V2.2 升级】使用 lunar-python 获取准确宜忌（替代本地池，代码简化 50+ 行）
    lunar = Lunar.fromYmd(date_obj.year, date_obj.month, date_obj.day)
    yi = lunar.getDayYi()[:8]  # 限制显示前 8 项，避免超出宽度
    ji = lunar.getDayJi()[:8]  # 限制显示前 8 项，避免超出宽度
    
    # 【V2.2 新增】获取传统黄历元素（可选）
    pengzu_gan = lunar.getPengZuGan()       # 彭祖百忌（天干）
    pengzu_zhi = lunar.getPengZuZhi()       # 彭祖百忌（地支）
    na_yin = lunar.getDayNaYin()            # 纳音
    xing_su = lunar.getXiu()                # 星宿
    zhi_xing = lunar.getZhiXing()           # 建除十二值星
    jiu_xing = lunar.getDayNineStar()       # 九星
    
    # 【修复 5】生肖运势 - 吉凶分离，逻辑正确
    # 根据地支计算六合、三合（红榜）和相冲、相害（黑榜）
    zodiac_map = {
        '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
        '辰': '龙', '巳': '蛇', '午': '马', '未': '羊',
        '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪'
    }
    
    # 六合关系
    liu_he = {
        '子': '丑', '丑': '子', '寅': '亥', '卯': '戌',
        '辰': '酉', '巳': '申', '午': '未', '未': '午',
        '申': '巳', '酉': '辰', '戌': '卯', '亥': '寅'
    }
    
    # 三合关系
    san_he = {
        '子': ['辰', '申'], '丑': ['巳', '酉'], '寅': ['午', '戌'],
        '卯': ['未', '亥'], '辰': ['子', '申'], '巳': ['丑', '酉'],
        '午': ['寅', '未'], '未': ['卯', '亥'], '申': ['子', '辰'],
        '酉': ['丑', '巳'], '戌': ['寅', '午'], '亥': ['卯', '未']
    }
    
    # 相冲关系
    xiang_chong = {
        '子': '午', '丑': '未', '寅': '申', '卯': '酉',
        '辰': '戌', '巳': '亥', '午': '子', '未': '丑',
        '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'
    }
    
    # 相害关系
    xiang_hai = {
        '子': '未', '丑': '午', '寅': '巳', '卯': '辰',
        '辰': '卯', '巳': '寅', '午': '丑', '未': '子',
        '申': '亥', '酉': '戌', '戌': '酉', '亥': '申'
    }
    
    # 获取当日地支
    day_zhi = day_gz[1]  # 如"酉"
    day_zodiac = zodiac_map[day_zhi]  # 如"鸡"
    
    # 红榜：六合 + 三合（3 个）
    he_zodiac = liu_he[day_zhi]
    he_zodiac_name = zodiac_map[he_zodiac]
    
    san_he_zodiacs = san_he[day_zhi]
    san_he_names = [zodiac_map[z] for z in san_he_zodiacs]
    
    # 红榜生肖描述（传统文化参考）
    zodiac_red = [
        f"{he_zodiac_name}：传统说法六合，贵人相助",
        f"{san_he_names[0]}：传统说法三合，合作顺利",
        f"{san_he_names[1]}：传统说法三合，家庭和睦"
    ]
    
    # 黑榜：相冲 + 相害 + 相刑（3 个，避免重复且不与红榜冲突）
    chong_zodiac = xiang_chong[day_zhi]
    chong_zodiac_name = zodiac_map[chong_zodiac]
    
    hai_zodiac = xiang_hai[day_zhi]
    hai_zodiac_name = zodiac_map[hai_zodiac]
    
    # 相刑关系
    xiang_xing = {
        '子': '卯', '丑': '戌', '寅': '巳', '卯': '子',
        '辰': '辰', '巳': '寅', '午': '午', '未': '丑',
        '申': '寅', '酉': '酉', '戌': '丑', '亥': '亥'
    }
    xing_zodiac = xiang_xing[day_zhi]
    
    # 【V2.3 修复】确保黑榜生肖不重复且不与红榜冲突
    red_zodiacs = [he_zodiac] + san_he_zodiacs
    black_zodiacs = [chong_zodiac, hai_zodiac]
    
    # 如果相刑与已有黑榜重复，或在红榜中，选择其他凶煞生肖
    if xing_zodiac in black_zodiacs or xing_zodiac in red_zodiacs:
        # 选择与三合生肖相冲的作为备选（也是凶煞）
        # 例如：寅日三合是午和戌，午冲子，戌冲辰
        # 选择子或辰作为第三个黑榜
        san_he_chong = {
            '子': '午', '丑': '未', '寅': '申', '卯': '酉',
            '辰': '戌', '巳': '亥', '午': '子', '未': '丑',
            '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'
        }
        # 取第一个三合生肖的对冲
        first_san_he = san_he_zodiacs[0]
        xing_zodiac = san_he_chong[first_san_he]
        
        # 如果还是重复，取第二个三合生肖的对冲
        if xing_zodiac in black_zodiacs or xing_zodiac in red_zodiacs:
            second_san_he = san_he_zodiacs[1]
            xing_zodiac = san_he_chong[second_san_he]
    
    xing_zodiac_name = zodiac_map[xing_zodiac]
    
    zodiac_black = [
        f"{chong_zodiac_name}：传统说法相冲，建议谨慎行事",
        f"{hai_zodiac_name}：传统说法相害，注意人际关系",
        f"{xing_zodiac_name}：传统说法相刑，注意健康"
    ]
    
    # 【修复 3】获取准确财神方位
    cai_shen = get_cai_shen(day_gz)
    
    # 【修复 2】获取准确吉时
    jishi = get_jishi(day_gz)
    
    # 穿衣建议
    changyi = get_changyi(day_gz)
    
    # 养生建议（6 组循环）
    yangsheng_pool = [
        {
            'diet_yi': "宜吃：菠菜 芹菜 百合 莲子 枸杞 菊花茶",
            'diet_ji': "忌吃：辛辣 油炸 生冷 过甜食物",
            'exercise': "早晨散步太极，舒展筋骨；下午健身游泳，增强体质",
            'sleep': "22:30 前入睡，保证充足睡眠，养肝护肝"
        },
        {
            'diet_yi': "宜吃：山药 红枣 黑芝麻 核桃 蜂蜜 银耳",
            'diet_ji': "忌吃：辣椒 羊肉 韭菜 大蒜 烈酒",
            'exercise': "晨练八段锦，活动关节；傍晚慢跑，增强心肺",
            'sleep': "23:00 前入睡，养心安神，避免熬夜"
        },
        {
            'diet_yi': "宜吃：绿豆 冬瓜 黄瓜 西瓜 苦瓜 荷叶",
            'diet_ji': "忌吃：生姜 胡椒 花椒 肉桂 荔枝",
            'exercise': "清晨瑜伽拉伸，放松身心；晚间游泳，清凉解暑",
            'sleep': "22:00 入睡，午休 30 分钟，养阴清热"
        },
        {
            'diet_yi': "宜吃：梨 苹果 葡萄 甘蔗 藕 蜂蜜",
            'diet_ji': "忌吃：烧烤 煎炸 烟酒 咖啡 浓茶",
            'exercise': "早晨登山远眺，润肺清心；傍晚散步，调畅气机",
            'sleep': "22:30 入睡，保持室内湿润，防秋燥"
        },
        {
            'diet_yi': "宜吃：羊肉 牛肉 韭菜 桂圆 栗子 核桃",
            'diet_ji': "忌吃：生冷 寒凉 西瓜 苦瓜 绿豆",
            'exercise': "晨练太极拳，温阳散寒；午后晒太阳，补充阳气",
            'sleep': "21:30 入睡，早睡晚起，养精蓄锐"
        },
        {
            'diet_yi': "宜吃：萝卜 白菜 豆腐 蘑菇 海带 紫菜",
            'diet_ji': "忌吃：油腻 粘硬 生冷 过咸食物",
            'exercise': "早晨快走，活动筋骨；晚间泡脚，温通经络",
            'sleep': "22:00 入睡，保暖防寒，养护阳气"
        }
    ]
    
    yangsheng_index = (date_obj.day + date_obj.month) % len(yangsheng_pool)
    yangsheng = yangsheng_pool[yangsheng_index]
    
    # 黄历科普（4 组循环）
    kepu_pool = [
        {
            'ganzhi': "天干地支纪日法，每日对应一个干支组合",
            'chongsha': "冲煞是指当日地支与某生肖相冲，需注意避让",
            'taishen': "胎神是保护胎儿的神灵，孕妇需避开其方位",
            'jishen': "吉神是当日的吉利神煞，宜在其方位行事",
            'xiongshen': "凶神是当日的不利神煞，需避开其方位"
        },
        {
            'ganzhi': "六十甲子循环纪日，每 60 天一个循环",
            'chongsha': "冲表示冲突，煞表示不利，需谨言慎行",
            'taishen': "胎神方位每日变化，孕妇搬家装修需避开",
            'jishen': "常见吉神有天德、月德、天赦、母仓等",
            'xiongshen': "常见凶神有月破、大耗、劫煞、灾煞等"
        },
        {
            'ganzhi': "天干十个：甲乙丙丁戊己庚辛壬癸",
            'chongsha': "地支十二个：子丑寅卯辰巳午未申酉戌亥",
            'taishen': "胎神每日轮转，占门床、占厨灶、占碓磨等",
            'jishen': "吉神宜：祭祀、祈福、嫁娶、开市等吉日",
            'xiongshen': "凶神忌：动土、安葬、行丧、词讼等凶日"
        },
        {
            'ganzhi': "干支纪日法从黄帝时代开始，已有四千多年历史",
            'chongsha': "属相冲煞：鼠马相冲、牛羊相冲、虎猴相冲等",
            'taishen': "孕妇注意事项：不搬家、不装修、不钉钉子",
            'jishen': "择吉日办事，趋吉避凶，是传统文化智慧",
            'xiongshen': "避开凶日，选择吉日，事半功倍"
        }
    ]
    
    kepu_index = date_obj.day % len(kepu_pool)
    kepu = kepu_pool[kepu_index]
    
    # 【V2.2 扩展】传统故事池（24 个节气故事 + 民俗故事 + 历史典故）
    story_pool = [
        # ========== 春季节气故事（6 个）==========
        {
            'title': "立春·咬春习俗",
            'season': '春',
            'content': [
                "立春是二十四节气之首，标志着春天开始。",
                "古代有'咬春'习俗，即立春之日吃春饼、春卷。",
                "春饼是用面粉烙制的薄饼，卷入新鲜蔬菜。",
                "咬春寓意咬住春天，祈求风调雨顺、五谷丰登。",
                "《燕京岁时记》记载：'立春之日，富家食春饼。'",
                "这一习俗至今在北方地区仍广泛流传。"
            ],
            'moral': "辞旧迎新、祈福丰收"
        },
        {
            'title': "雨水·春雨贵如油",
            'season': '春',
            'content': [
                "雨水节气标志着降雨开始，雨量渐增。",
                "农谚云：'春雨贵如油'，说明春雨对农作物的重要性。",
                "雨水时节，农民开始春耕备耕，准备播种。",
                "民间有'拉保保'习俗，为孩子祈求健康平安。",
                "雨水还讲究'回娘家'，出嫁女儿回家探望父母。",
                "这一节气体现了古人对自然规律的深刻认知。"
            ],
            'moral': "珍惜资源、感恩自然"
        },
        {
            'title': "惊蛰·春雷惊百虫",
            'season': '春',
            'content': [
                "惊蛰时节，春雷乍动，惊醒蛰伏的昆虫。",
                "古人认为春雷是上天唤醒万物的信号。",
                "民间有'打小人'习俗，用鞋底拍打纸人驱邪。",
                "惊蛰也是春耕的重要时节，农民开始播种。",
                "客家人有'炒虫'习俗，炒豆子寓意消灭害虫。",
                "这一节气反映了古人对生物节律的观察。"
            ],
            'moral': "顺应天时、驱邪纳福"
        },
        {
            'title': "春分·阴阳平衡",
            'season': '春',
            'content': [
                "春分之日，昼夜平分，阴阳平衡。",
                "古人认为春分是调节身体的好时机。",
                "民间有'竖蛋'游戏，春分之日最容易成功。",
                "春分还有'祭日'习俗，皇帝率群臣祭日神。",
                "农民忙着春灌、施肥，管理越冬作物。",
                "这一节气体现了古人'天人合一'的哲学思想。"
            ],
            'moral': "平衡和谐、顺应自然"
        },
        {
            'title': "清明·祭祖扫墓",
            'season': '春',
            'content': [
                "清明既是节气，也是传统节日。",
                "源于寒食节，纪念春秋时期介子推。",
                "清明扫墓，缅怀先人，表达哀思。",
                "清明踏青，亲近自然，感受春意。",
                "插柳、戴柳，寓意驱邪避灾。",
                "清明文化传承千年，是中华孝道的重要体现。"
            ],
            'moral': "慎终追远、孝道传承"
        },
        {
            'title': "谷雨·雨生百谷",
            'season': '春',
            'content': [
                "谷雨是春季最后一个节气。",
                "'雨生百谷'，雨水滋润万物，谷物茁壮成长。",
                "谷雨有'祭海'习俗，渔民祈求出海平安。",
                "喝谷雨茶，传说能清火明目。",
                "谷雨时节，农民忙着插秧、种豆。",
                "这一节气体现了农耕文明的智慧。"
            ],
            'moral': "感恩自然、勤劳致富"
        },
        
        # ========== 夏季节气故事（6 个）==========
        {
            'title': "立夏·称人习俗",
            'season': '夏',
            'content': [
                "立夏标志着夏季开始。",
                "民间有'称人'习俗，立夏之日称体重。",
                "传说称人后，夏天不会消瘦，健康度夏。",
                "立夏吃蛋，称为'立夏蛋'，寓意圆满。",
                "皇帝率群臣'迎夏'，祈求风调雨顺。",
                "这一习俗体现了古人对健康的重视。"
            ],
            'moral': "珍爱健康、顺应四时"
        },
        {
            'title': "小满·麦粒渐满",
            'season': '夏',
            'content': [
                "小满时节，麦粒开始饱满，但尚未成熟。",
                "'小满不满，麦有一险'，提醒农民注意防灾。",
                "小满有'祭车神'习俗，祈求灌溉顺利。",
                "吃苦菜，清热解暑，预防疾病。",
                "小满体现了古人'满招损，谦受益'的哲理。",
                "人生如节气，小满即安，不求全满。"
            ],
            'moral': "谦虚谨慎、知足常乐"
        },
        {
            'title': "芒种·忙收忙种",
            'season': '夏',
            'content': [
                "芒种是'有芒之谷可稼种'之意。",
                "此时麦子成熟，稻谷可种，农事繁忙。",
                "民间有'送花神'习俗，饯别春花。",
                "'芒种不种，再种无用'，强调农时重要。",
                "煮梅、吃梅，是芒种的传统习俗。",
                "这一节气体现了农耕的辛勤与智慧。"
            ],
            'moral': "珍惜时光、勤劳耕耘"
        },
        {
            'title': "夏至·日长之至",
            'season': '夏',
            'content': [
                "夏至之日，白昼最长，黑夜最短。",
                "古人认为夏至阳气最盛，需防暑降温。",
                "民间有'夏至面'习俗，吃面消暑。",
                "皇帝'祭地'，祈求国泰民安。",
                "妇女互赠香囊，驱蚊避邪。",
                "夏至体现了古人对天文现象的精准观测。"
            ],
            'moral': "阴阳转化、物极必反"
        },
        {
            'title': "小暑·炎热初现",
            'season': '夏',
            'content': [
                "小暑标志着炎热夏季正式到来。",
                "'小暑大暑，上蒸下煮'，形容天气炎热。",
                "民间有'晒伏'习俗，晒衣物防霉防虫。",
                "吃藕、吃黄鳝，是 small 暑的养生习俗。",
                "小暑时节，农民忙着田间管理。",
                "这一节气体现了古人的养生智慧。"
            ],
            'moral': "防暑降温、养生保健"
        },
        {
            'title': "大暑·酷热难耐",
            'season': '夏',
            'content': [
                "大暑是一年中最热的节气。",
                "'大暑大暑，热得无处躲'，形容酷热。",
                "民间有'送大暑船'习俗，祈求平安度夏。",
                "喝伏茶、吃仙草，清热解毒。",
                "大暑时节，早稻收获，晚稻插秧。",
                "这一节气体现了劳动人民的坚韧精神。"
            ],
            'moral': "不畏酷暑、坚韧不拔"
        },
        
        # ========== 秋季节气故事（6 个）==========
        {
            'title': "立秋·贴秋膘",
            'season': '秋',
            'content': [
                "立秋标志着秋季开始。",
                "民间有'贴秋膘'习俗，立秋之日吃肉。",
                "夏天清淡饮食，立秋补补身体。",
                "'咬秋'吃西瓜，寓意消除暑气。",
                "皇帝'迎秋'，祭祀秋神。",
                "这一习俗体现了古人的养生智慧。"
            ],
            'moral': "适时进补、调养身心"
        },
        {
            'title': "处暑·暑气消退",
            'season': '秋',
            'content': [
                "处暑意味着炎热暑气即将结束。",
                "'处暑天还暑，好似秋老虎'，提醒余热未消。",
                "民间有'放河灯'习俗，悼念逝者。",
                "处暑吃鸭子，滋阴养胃。",
                "农民开始收获早熟作物。",
                "这一节气体现了季节转换的规律。"
            ],
            'moral': "寒暑交替、自然规律"
        },
        {
            'title': "白露·露水凝结",
            'season': '秋',
            'content': [
                "白露时节，早晚露水凝结。",
                "'白露秋分夜，一夜冷一夜'，天气渐凉。",
                "民间有'白露茶'习俗，采白露时节的茶。",
                "喝白露米酒，是江浙地区的传统。",
                "白露时节，候鸟开始南飞。",
                "这一节气体现了物候变化的精妙。"
            ],
            'moral': "观察自然、顺应变化"
        },
        {
            'title': "秋分·昼夜平分",
            'season': '秋',
            'content': [
                "秋分之日，昼夜再次平分。",
                "秋分是传统的'祭月节'，后来演变为中秋。",
                "民间有'竖蛋'游戏，与春分类似。",
                "秋分吃秋菜，祈求身体健康。",
                "农民忙着秋收、秋耕、秋种。",
                "这一节气体现了古人的天文智慧。"
            ],
            'moral': "阴阳平衡、收获感恩"
        },
        {
            'title': "寒露·露水寒冷",
            'season': '秋',
            'content': [
                "寒露时节，露水增多且寒冷。",
                "'寒露寒露，遍地冷露'，形容天气转凉。",
                "民间有'登高'习俗，重阳节前后登山。",
                "赏菊花、饮菊花酒，是寒露的传统。",
                "寒露时节，晚稻收割，冬小麦播种。",
                "这一节气体现了季节的深刻变化。"
            ],
            'moral': "登高望远、胸怀开阔"
        },
        {
            'title': "霜降·霜冻降临",
            'season': '秋',
            'content': [
                "霜降是秋季最后一个节气。",
                "霜降之日，开始出现霜冻。",
                "民间有'补冬不如补霜降'的说法。",
                "吃柿子，是霜降的传统习俗。",
                "农民抢收晚稻，防止霜冻损害。",
                "这一节气体现了农事与节气的紧密联系。"
            ],
            'moral': "未雨绸缪、防患未然"
        },
        
        # ========== 冬季节气故事（6 个）==========
        {
            'title': "立冬·冬季开始",
            'season': '冬',
            'content': [
                "立冬标志着冬季正式开始。",
                "皇帝'迎冬'，祭祀冬神。",
                "民间有'补冬'习俗，立冬之日进补。",
                "吃饺子，是北方的立冬传统。",
                "农民开始冬闲，修缮农具。",
                "这一节气体现了古人的养生之道。"
            ],
            'moral': "养精蓄锐、待时而动"
        },
        {
            'title': "小雪·雪花初现",
            'season': '冬',
            'content': [
                "小雪时节，北方开始下雪。",
                "'小雪封地，大雪封河'，形容天气寒冷。",
                "民间有'腌菜'习俗，储备过冬蔬菜。",
                "小雪吃糍粑，是南方地区的传统。",
                "渔民开始晒鱼干，储备食物。",
                "这一节气体现了古人的生存智慧。"
            ],
            'moral': "未雨绸缪、储备过冬"
        },
        {
            'title': "大雪·雪花纷飞",
            'season': '冬',
            'content': [
                "大雪时节，降雪量增大。",
                "'瑞雪兆丰年'，冬雪预示来年丰收。",
                "民间有'进补'习俗，吃羊肉、狗肉。",
                "大雪腌肉，是传统习俗。",
                "农民修整农田，准备来年春耕。",
                "这一节气体现了劳动人民的乐观精神。"
            ],
            'moral': "乐观向上、期盼丰收"
        },
        {
            'title': "冬至·日短之至",
            'season': '冬',
            'content': [
                "冬至之日，白昼最短，黑夜最长。",
                "古人认为冬至是阴阳转化的关键节点。",
                "北方吃饺子，南方吃汤圆。",
                "'冬至大如年'，是重要的传统节日。",
                "皇帝'祭天'，祈求国泰民安。",
                "这一节气体现了古人的天文观测能力。"
            ],
            'moral': "阴阳转化、否极泰来"
        },
        {
            'title': "小寒·寒冷初现",
            'season': '冬',
            'content': [
                "小寒标志着一年中最冷时期到来。",
                "'小寒大寒，冷成冰团'，形容严寒。",
                "民间有'九九消寒图'习俗，记录寒冬。",
                "吃腊八粥，是 small 寒的传统。",
                "农民开始准备年货，迎接春节。",
                "这一节气体现了古人的乐观精神。"
            ],
            'moral': "不畏严寒、期盼春暖"
        },
        {
            'title': "大寒·严寒之极",
            'season': '冬',
            'content': [
                "大寒是一年中最冷的节气。",
                "大寒过后，春天即将到来。",
                "民间有'尾牙祭'习俗，祭祀土地神。",
                "吃八宝饭、年糕，寓意年年高。",
                "大寒时节，人们开始准备春节。",
                "这一节气体现了冬去春来的自然规律。"
            ],
            'moral': "严冬将过、春天不远"
        }
    ]
    
    # 【V2.3.1 修复】根据季节选择故事（避免春季显示秋季故事）
    # 1. 按月份确定季节
    month = date_obj.month
    if month in [3, 4, 5]:
        season = '春'
        season_name = '春季'
    elif month in [6, 7, 8]:
        season = '夏'
        season_name = '夏季'
    elif month in [9, 10, 11]:
        season = '秋'
        season_name = '秋季'
    else:
        season = '冬'
        season_name = '冬季'
    
    # 2. 筛选当季故事
    seasonal_stories = [s for s in story_pool if s.get('season') == season]
    
    # 3. 如果当季故事为空， fallback 到全部故事（兼容性）
    if not seasonal_stories:
        seasonal_stories = story_pool
    
    # 4. 按日期轮换（确保同一季节内不重复）
    # 使用 (day + month) 组合，避免每月同一天重复
    story_index = (date_obj.day + date_obj.month) % len(seasonal_stories)
    story = seasonal_stories[story_index]
    
    print(f"[INFO] 季节：{season_name}，故事池：{len(seasonal_stories)}个，选择：{story['title']}")
    
    # 【V3.0.1 升级】特殊节日显示（支持任意节气）
    if jieqi:
        special_day = f"今日{jieqi}"
    else:
        # 非节气日，不显示特殊信息（或可以显示距离下个节气的天数）
        special_day = ""
    
    return {
        'date_gregorian': f"{date_str} {weekday_names[weekday]}",
        'date_lunar': lunar_date,
        'ganzhi_full': ganzhi_full,
        'special_day': special_day,
        'yi': yi,
        'ji': ji,
        'zodiac_red': zodiac_red,
        'zodiac_black': zodiac_black,
        'cai_shen': cai_shen,
        'jishi': jishi,
        'changyi': changyi,
        'yangsheng': yangsheng,
        'kepu': kepu,
        'story': story
    }

def generate_page1(data, fonts, output_dir, date_str, template_name=None, template=None):
    """生成第 1 页：封面 + 宜忌 + 生肖"""
    # 【V2.3 新增】如果没有传入模板，自动选择
    if template_name is None or template is None:
        template_name, template = get_template(date_str)
    
    # 使用模板配色
    img = Image.new('RGB', (WIDTH, PAGE_HEIGHT), template['bg'])
    draw = ImageDraw.Draw(img)
    
    # 绘制装饰边框
    draw_decoration(draw, template_name, template)
    
    # 使用模板颜色绘制
    y = 40
    y = draw_centered_text(draw, "每日黄历", y, fonts['title'], template['title'])
    y += SPACING['after_title']
    y = draw_centered_text(draw, data['date_gregorian'], y, fonts['subtitle'], template['text'])
    y += SPACING['after_subtitle']
    y = draw_centered_text(draw, data['date_lunar'], y, fonts['section'], template['text'])
    y += SPACING['after_lunar']
    # 【V3.0.5 优化】干支和节气合并到一行
    ganzhi_with_jieqi = data['ganzhi_full']
    if data['special_day']:
        ganzhi_with_jieqi += f"  {data['special_day']}"
    y = draw_centered_text(draw, ganzhi_with_jieqi, y, fonts['content'], template['text'])
    
    y = draw_separator(draw, y + 25, template['separator'])
    
    y += 15
    y = draw_centered_text(draw, "传统习俗：适合", y, fonts['section'], template['section'])
    y += 8
    
    yi_line1 = " ".join(data['yi'][:4])
    yi_line2 = " ".join(data['yi'][4:])
    y = draw_centered_text(draw, yi_line1, y, fonts['content'], template['text'])
    y += 8
    y = draw_centered_text(draw, yi_line2, y, fonts['content'], template['text'])
    
    y += 18
    y = draw_centered_text(draw, "传统讲究：避免", y, fonts['section'], template['section'])
    y += 8
    y = draw_centered_text(draw, " ".join(data['ji']), y, fonts['content'], template['text'])
    
    y = draw_separator(draw, y + 25, template['separator'])
    
    y += 15
    y = draw_centered_text(draw, "今日生肖运势", y, fonts['section'], template['section'])
    
    y += SPACING['after_zodiac_title']
    y = draw_centered_text(draw, "今日吉生肖", y, fonts['content'], template['section'])
    y += SPACING['after_zodiac_item']
    
    # 【V3.0.5 修复】生肖运势使用纯文字，移除所有 emoji
    for zodiac in data['zodiac_red']:
        y = draw_centered_text(draw, zodiac, y, fonts['content'], template['text'])
        y += SPACING['after_zodiac_item']
    
    y += 8
    y = draw_centered_text(draw, "今日需注意生肖", y, fonts['content'], template['section'])
    y += SPACING['after_zodiac_item']
    
    for zodiac in data['zodiac_black']:
        y = draw_centered_text(draw, zodiac, y, fonts['content'], template['text'])
        y += SPACING['after_zodiac_item']
    
    y = draw_separator(draw, y + 18, template['separator'])
    
    y += 8
    # 【V2.3 整改】增加免责声明
    disclaimer_text = "传统文化参考 请理性看待 相信科学"
    y = draw_centered_text(draw, disclaimer_text, y, fonts['small'], template['small'])
    y += 15  # 【V3.0.3 优化】删除底部日期，增加边距
    # draw_centered_text(draw, data['date_gregorian'], y, fonts['small'], template['small'])  # 已删除
    
    date_only = date_str.replace('-', '')
    filename = f"{date_only}_黄历.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, 'PNG', quality=95, optimize=True)
    print(f"[OK] 第 1 页已保存：{filepath}")
    return filepath

def generate_page2(data, fonts, output_dir, date_str, template_name=None, template=None):
    """生成第 2 页：财神 + 养生"""
    # 【V2.3 新增】如果没有传入模板，自动选择
    if template_name is None or template is None:
        template_name, template = get_template(date_str)
    
    # 使用模板配色
    img = Image.new('RGB', (WIDTH, PAGE_HEIGHT), template['bg'])
    draw = ImageDraw.Draw(img)
    
    # 绘制装饰边框
    draw_decoration(draw, template_name, template)
    
    y = 50
    y = draw_centered_text(draw, "财神方位", y, fonts['section'], template['section'])
    y += 15
    
    cai_shen_info = [
        f"喜神：{data['cai_shen']['xi']}",
        f"福神：{data['cai_shen']['fu']}",
        f"财神：{data['cai_shen']['cai']}",
        f"胎神：{data['cai_shen']['tai']}"
    ]
    
    for info in cai_shen_info:
        y = draw_centered_text(draw, info, y, fonts['content'], template['text'])
        y += 8
    
    y += 10
    y = draw_centered_text(draw, "传统时辰", y, fonts['section'], template['section'])
    y += 10
    
    ji_names = [s.replace('时', '').split(' ')[0] for s in data['jishi']['ji'][:6]]
    xiong_names = [s.replace('时', '').split(' ')[0] for s in data['jishi']['xiong'][:6]]
    
    ji_str = "、".join(ji_names)
    xiong_str = "、".join(xiong_names)
    
    y += 8
    y = draw_centered_text(draw, f"传统吉时：{ji_str}", y, fonts['content'], template['section'])
    y += 8
    y = draw_centered_text(draw, f"传统讲究：{xiong_str}", y, fonts['content'], template['section'])
    
    y = draw_separator(draw, y + 20, template['separator'])
    
    y += 18
    y = draw_centered_text(draw, "春季养生", y, fonts['section'], template['section'])
    
    y += 12
    y = draw_centered_text(draw, "饮食调养", y, fonts['content'], template['section'])
    y += 8
    
    y = draw_centered_text(draw, data['yangsheng']['diet_yi'], y, fonts['content'], template['text'])
    y += 8
    y = draw_centered_text(draw, data['yangsheng']['diet_ji'], y, fonts['content'], template['text'])
    
    y += 15
    y = draw_centered_text(draw, "运动建议", y, fonts['content'], template['section'])
    y += 8
    
    y = draw_centered_text(draw, data['yangsheng']['exercise'], y, fonts['content'], template['text'])
    
    y += 15
    y = draw_centered_text(draw, "作息建议", y, fonts['content'], template['section'])
    y += 8
    
    y = draw_centered_text(draw, data['yangsheng']['sleep'], y, fonts['content'], template['text'])
    
    y = draw_separator(draw, y + 20, template['separator'])
    
    y += 15
    # 【V3.0.3 新增】抖音互动引导
    interaction_text = " 点赞接好运 | 评论留生肖 | 关注每日更新"
    y = draw_centered_text(draw, interaction_text, y, fonts['content'], template['section'])
    
    y += 15
    y = draw_centered_text(draw, "传统文化 仅供参考", y, fonts['small'], template['small'])
    y += 5
    draw_centered_text(draw, data['date_gregorian'], y, fonts['small'], template['small'])
    
    date_only = date_str.replace('-', '')
    filename = f"{date_only}_黄历_养生.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, 'PNG', quality=95, optimize=True)
    print(f"[OK] 第 2 页已保存：{filepath}")
    return filepath

def generate_page3(data, fonts, output_dir, date_str, template_name=None, template=None):
    """生成第 3 页：穿衣建议 + 科普 + 故事"""
    # 【V2.3 新增】如果没有传入模板，自动选择
    if template_name is None or template is None:
        template_name, template = get_template(date_str)
    
    # 使用模板配色
    img = Image.new('RGB', (WIDTH, PAGE_HEIGHT), template['bg'])
    draw = ImageDraw.Draw(img)
    
    # 绘制装饰边框
    draw_decoration(draw, template_name, template)
    
    y = 50
    
    y = draw_centered_text(draw, "今日穿衣建议", y, fonts['section'], template['section'])
    y += 15
    
    y = draw_centered_text(draw, f"幸运色：{data['changyi']['lucky']}", y, fonts['content'], template['section'])
    y += 8
    y = draw_centered_text(draw, f"忌讳色：{data['changyi']['avoid']}", y, fonts['content'], template['section'])
    
    y = draw_separator(draw, y + 20, template['separator'])
    
    y += 18
    y = draw_centered_text(draw, "黄历科普", y, fonts['section'], template['section'])
    y += 15
    
    y = draw_centered_text(draw, f"【天干地支】{data['kepu']['ganzhi']}", y, fonts['small'], template['text'])
    y += 6
    y = draw_centered_text(draw, f"【冲煞】{data['kepu']['chongsha']}", y, fonts['small'], template['text'])
    y += 6
    y = draw_centered_text(draw, f"【胎神】{data['kepu']['taishen']}", y, fonts['small'], template['text'])
    y += 6
    y = draw_centered_text(draw, f"【吉神】{data['kepu']['jishen']}", y, fonts['small'], template['text'])
    y += 6
    y = draw_centered_text(draw, f"【凶神】{data['kepu']['xiongshen']}", y, fonts['small'], template['text'])
    
    y = draw_separator(draw, y + 15, template['separator'])
    
    y += 15
    y = draw_centered_text(draw, f"传统故事·{data['story']['title']}", y, fonts['section'], template['section'])
    y += 5
    
    for line in data['story']['content']:
        y = draw_centered_text(draw, line, y, fonts['small'], template['text'])
        y += 5
    
    y += 12
    y = draw_centered_text(draw, f"启示：{data['story']['moral']}", y, fonts['content'], template['section'])
    
    y = draw_separator(draw, y + 15, template['separator'])
    
    y += 15
    # 【V3.0.3 新增】抖音互动引导
    interaction_text = " 点赞接好运 | 评论留生肖 | 关注每日更新"
    y = draw_centered_text(draw, interaction_text, y, fonts['content'], template['section'])
    
    y += 15
    y = draw_centered_text(draw, "传统文化 仅供参考", y, fonts['small'], template['small'])
    y += 5
    draw_centered_text(draw, data['date_gregorian'], y, fonts['small'], template['small'])
    
    date_only = date_str.replace('-', '')
    filename = f"{date_only}_黄历_故事.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, 'PNG', quality=95, optimize=True)
    print(f"[OK] 第 3 页已保存：{filepath}")
    return filepath

def get_default_output():
    """【V3.0.4 修复】固定输出到技能目录下的 output/ 文件夹"""
    # 1. 优先使用环境变量（用户可自定义）
    if 'OPENCLAW_OUTPUT' in os.environ:
        return os.environ['OPENCLAW_OUTPUT']
    
    # 2. 默认输出到技能目录的 output/ 文件夹（绝对路径）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    return os.path.join(skill_dir, 'output')

def generate_single_day(date_str, args, config):
    """【V3.0.1 新增】生成单日黄历"""
    # 获取模板
    if args.template:
        template_name = args.template
        template = TEMPLATES[template_name]
    else:
        template_name, template = get_template(date_str, config)
    
    fonts = load_fonts(template_name)
    
    print(f"\n[INFO] 正在生成 {date_str} 的黄历...")
    print(f"[INFO] 使用模板：{template['name']}")
    
    data = get_almanac_data(date_str)
    
    # 生成指定页数
    if args.pages >= 1:
        generate_page1(data, fonts, args.output, date_str, template_name, template)
    
    if args.pages >= 2:
        generate_page2(data, fonts, args.output, date_str, template_name, template)
    
    if args.pages >= 3:
        generate_page3(data, fonts, args.output, date_str, template_name, template)


def main():
    default_output = get_default_output()
    
    parser = argparse.ArgumentParser(description='生成黄历图片（V3.0.1 通用化版）')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), 
                        help='日期（YYYY-MM-DD 格式）')
    parser.add_argument('--batch', type=int, default=0,
                        help='批量生成天数（如--batch 7 生成 7 天）')
    parser.add_argument('--start-date', type=str, default=None,
                        help='批量生成起始日期（默认从--date 开始）')
    parser.add_argument('--pages', type=int, default=3, choices=[1, 2, 3], 
                        help='生成页数（1/2/3，默认 3）')
    parser.add_argument('--output', type=str, default=default_output, 
                        help=f'输出目录（默认：当前目录/reports/）')
    parser.add_argument('--template', type=str, default=None, 
                        choices=['traditional', 'modern', 'festive', 'elegant', 'fresh'],
                        help='指定模板（默认：自动轮换）')
    parser.add_argument('--config', type=str, default=None,
                        help='配置文件路径（默认：config.yaml）')
    
    args = parser.parse_args()
    
    # 【V3.0.1 新增】加载配置文件
    config = load_config(args.config)
    
    # 规范化路径并创建目录
    args.output = os.path.normpath(args.output)
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    print(f"[INFO] 输出目录：{args.output}")
    
    # 【V3.0.1 新增】批量生成模式
    if args.batch > 0:
        batch_days = min(args.batch, config.get('batch', {}).get('max_days', 365))
        start_date_str = args.start_date if args.start_date else args.date
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"[ERROR] 起始日期格式错误：{start_date_str}，应为 YYYY-MM-DD")
            return
        
        print(f"\n[INFO] 批量生成模式：从 {start_date_str} 开始，共 {batch_days} 天")
        print(f"[INFO] 预计输出目录：{args.output}/{start_date.strftime('%Y-%m')}/")
        
        # 按年月分组输出
        output_subdir = os.path.join(args.output, start_date.strftime('%Y-%m'))
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        args.output = output_subdir
        
        # 批量生成
        progress_bar = config.get('batch', {}).get('progress_bar', True)
        
        for i in range(batch_days):
            current_date = start_date + timedelta(days=i)
            current_date_str = current_date.strftime('%Y-%m-%d')
            
            if progress_bar:
                print(f"[{i+1}/{batch_days}] {current_date_str}", end='\r' if i < batch_days-1 else '\n')
            
            generate_single_day(current_date_str, args, config)
        
        print(f"\n[OK] 批量生成完成！共 {batch_days} 天，{batch_days * args.pages} 页图片")
        print(f"输出目录：{args.output}")
        return
    
    # 单日生成模式
    generate_single_day(args.date, args, config)
    
    print(f"\n[OK] 黄历图片生成完成！共 {args.pages} 页（V3.0.1 通用化版）")
    print(f"输出目录：{args.output}")

if __name__ == "__main__":
    main()
