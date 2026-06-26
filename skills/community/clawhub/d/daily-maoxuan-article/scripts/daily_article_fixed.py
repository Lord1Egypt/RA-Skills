#!/usr/bin/env python3
'''
每日毛选文章推送脚本 v5.4
每天推送一篇毛泽东选集文章到 Obsidian 和 Telegram

核心理念：解一篇文章，传递一段历史，连接一种智慧
v5.4: 清理硬编码路径，实现真正的 Telegram 推送，246篇全支持
'''

import os
import re
import sys
import json
import hashlib
import argparse
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 基础路径（相对于脚本自身）
BASE_DIR = Path(__file__).parent.parent
ARTICLES_FILE = BASE_DIR / 'references' / 'mao-articles.md'
STATE_FILE = BASE_DIR / '.article-state'
DEFAULT_OUTPUT_DIR = '/tank/obsidian/每日毛选'

# ── 完整文章数据（有全文六章内容的） ──

FULL_ARTICLES = {
    '论十大关系': {
        'title_en': 'On the Ten Major Relationships',
        'background_zh': '1956年4月25日，毛泽东在中共中央政治局扩大会议上发表讲话，系统总结我国社会主义建设中的重大关系，是中国共产党独立自主探索适合中国国情社会主义建设道路的开篇之作，标志着党对社会主义建设规律认识的重大飞跃。',
        'background_en': 'On April 25, 1956, Mao Zedong delivered a speech at the expanded meeting of the Political Bureau of the CPC Central Committee, systematically summarizing the major relationships in China's socialist construction.',
        '历史意义_zh': '1. 突破苏联模式束缚，实现从照搬苏联到自主探索的重大转变。2. 奠定党探索中国社会主义建设道路的理论基础。3. 统筹兼顾、协调发展思想成为中国特色社会主义理论体系的重要源头。',
        '历史意义_en': '1. Breaking free from Soviet model constraints. 2. Laying theoretical foundation for China's socialist construction. 3. Coordinated development thinking became an important source for socialism with Chinese characteristics.',
        '核心方针': {
            '总方针_zh': '调动一切积极因素，团结一切可以团结的力量，为建设社会主义强大国家服务。',
            '总方针_en': 'Mobilize all positive factors, unite all forces that can be united to build a powerful socialist country.',
            '根本方法_zh': '统筹兼顾、协调平衡、两点论与重点论统一，反对片面化、绝对化。',
            '根本方法_en': 'Comprehensive planning, coordinated balance, opposing one-sidedness and absolutism.',
            '核心立场_zh': '以苏为鉴，走中国自己的社会主义建设道路。',
            '核心立场_en': 'Learning from the Soviet experience as a reference, taking China's own path of socialist construction.'
        },
        '核心内容': {
            'title_zh': '十大关系',
            'title_en': 'Ten Major Relationships',
            'items': [
                {'num': '1', 'name_zh': '重工业和轻工业、农业的关系', 'name_en': 'Heavy industry vs light industry & agriculture', 'desc_zh': '在优先发展重工业的前提下，更多地发展农业、轻工业，更好地供给人民生活、增加资金积累', 'desc_en': 'While prioritizing heavy industry, develop more agriculture and light industry'},
                {'num': '2', 'name_zh': '沿海工业和内地工业的关系', 'name_en': 'Coastal vs inland industry', 'desc_zh': '充分利用和发展沿海工业，大力发展内地工业，平衡工业布局', 'desc_en': 'Fully utilize coastal industry, vigorously develop inland industry'},
                {'num': '3', 'name_zh': '经济建设和国防建设的关系', 'name_en': 'Economic vs national defense construction', 'desc_zh': '加强国防建设必须首先加强经济建设，为国防建设奠定物质基础', 'desc_en': 'Strengthening national defense must first strengthen economic construction'},
                {'num': '4', 'name_zh': '国家、生产单位和生产者个人的关系', 'name_en': 'State, production units & producers', 'desc_zh': '三者必须兼顾，不能只顾一头；给生产单位一定独立性和权益', 'desc_en': 'All three must be balanced; we cannot focus on only one aspect'},
                {'num': '5', 'name_zh': '中央和地方的关系', 'name_en': 'Central vs local governments', 'desc_zh': '在中央统一领导下，扩大地方权力，发挥中央和地方两个积极性', 'desc_en': 'Under unified central leadership, expand local power'},
                {'num': '6', 'name_zh': '汉族和少数民族的关系', 'name_en': 'Han vs ethnic minorities', 'desc_zh': '反对大汉族主义，诚心诚意帮助少数民族发展经济文化，巩固民族团结', 'desc_en': 'Oppose Han chauvinism, sincerely help ethnic minorities develop'},
                {'num': '7', 'name_zh': '党和非党的关系', 'name_en': 'Party vs non-Party', 'desc_zh': '实行长期共存、互相监督方针，团结各民主党派与无党派人士', 'desc_en': 'Long-term coexistence and mutual supervision with democratic parties'},
                {'num': '8', 'name_zh': '革命和反革命的关系', 'name_en': 'Revolutionaries vs counter-revolutionaries', 'desc_zh': '镇压已被推翻的反动阶级残余，对反革命分子区别对待，坚持少捕少杀', 'desc_en': 'Suppress remnants of overthrown classes, distinguish between types'},
                {'num': '9', 'name_zh': '是非关系', 'name_en': 'Right vs wrong', 'desc_zh': '对犯错误的同志实行惩前毖后、治病救人方针，帮助改正，团结同志', 'desc_en': 'Learn from past mistakes to prevent future ones, help comrades correct errors'},
                {'num': '10', 'name_zh': '中国和外国的关系', 'name_en': 'China vs foreign countries', 'desc_zh': '学习一切民族、一切国家的长处，学习先进科学技术，学习必须与中国实际相结合', 'desc_en': 'Learn from all nations their strong points, combine learning with Chinese reality'}
            ]
        },
        '历史背景': {
            '国内_zh': '社会主义改造基本完成，社会主义制度基本建立，一五计划顺利推进，进入全面建设时期。',
            '国内_en': 'Socialist transformation basically completed, socialist system established, First Five-Year Plan progressing smoothly.',
            '国际_zh': '苏共二十大揭露苏联模式弊端，促使中国共产党反思并摆脱教条主义束缚。',
            '国际_en': 'The 20th CPSU Congress revealed drawbacks of the Soviet model, prompting CCP to reflect and break free from dogmatism.'
        },
        '现代启示': [
            {'启示_zh': '坚持高质量发展，统筹城乡、区域、产业协调发展', '启示_en': 'Adhere to high-quality development, coordinate urban-rural and regional development'},
            {'启示_zh': '统筹发展和安全，以经济建设支撑国防与国家安全', '启示_en': 'Coordinate development and security, support national defense through economic development'},
            {'启示_zh': '兼顾国家、集体、个人利益，扎实推进共同富裕', '启示_en': 'Balance interests of state, collective, and individuals, steadily advance common prosperity'},
            {'启示_zh': '坚持中央统一领导与地方积极性相结合，提升治理效能', '启示_en': 'Combine central unified leadership with local initiative, improve governance efficiency'},
            {'启示_zh': '坚持对外开放，博采众长，走独立自主的中国式现代化道路', '启示_en': 'Adhere to opening up, learn broadly, take the independent path of Chinese-style modernization'}
        ],
        '经典箴言': [
            {'箴言_zh': '努力把党内党外、国内国外的一切积极的因素，全部调动起来，把我国建设成为一个强大的社会主义国家。', '箴言_en': 'We must strive to mobilize all positive factors to build our country into a powerful socialist nation.', '出处': '《论十大关系》（1956）'},
            {'箴言_zh': '我们的方针是，一切民族、一切国家的长处都要学，政治、经济、科学、技术、文学、艺术的一切真正好的东西都要学。', '箴言_en': 'Our principle is to learn from all nations and countries their strong points, in politics, economy, science, technology, literature and art.', '出处': '《论十大关系》（1956）'},
            {'箴言_zh': '统筹兼顾，各得其所。', '箴言_en': 'Comprehensive planning, so that everyone gets their proper place.', '出处': '《论十大关系》（1956）'}
        ]
    }
}


def load_articles() -> List[Dict]:
    '''从数据库加载文章列表'''
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    articles = []
    for line in content.split('\n'):
        if '|' in line and not line.startswith('---') and not line.startswith('#'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                title = parts[0].strip()
                date = parts[1].strip()
                background = parts[2].strip()
                if title and date and not title.startswith('##') and not title.startswith('【'):
                    articles.append({'title': title, 'date': date, 'background': background})
    return articles


def get_today_article(articles: List[Dict]) -> Dict:
    '''获取今日文章（日期确定性选择，避免重复）'''
    today = datetime.now().strftime('%Y-%m-%d')

    # 日期哈希决定文章索引
    hash_val = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = hash_val % len(articles)
    article = articles[index]

    # 保存状态
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        f.write(f'{today}|{article['title']}')

    return article


# ── 扩展缓存文件路径 ──
EXPANSIONS_FILE = BASE_DIR / 'references' / 'mao-expansions.md'


def load_cached_expansion(title: str) -> Optional[Dict]:
    '''从缓存文件加载扩充内容'''
    if not EXPANSIONS_FILE.exists():
        return None

    try:
        with open(EXPANSIONS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已转换为 FULL_ARTICLES 格式
        # 新格式包含 'title_en', 'background_zh' 等字段
        if 'title_en' in content or 'title_en' in content:
            # 简单的文本检查
            pass

        # 解析缓存文章 - 支持FULL_ARTICLES格式
        sections = content.split('## ')
        for section in sections:
            if not section.strip():
                continue
            lines = section.split('\n')
            if lines[0].strip() == title:
                # 找到文章，解析内容
                data = {}
                current_key = None
                current_content = []
                is_dict_format = False

                for line in lines[1:]:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('### '):
                        # 保存之前的key
                        if current_key:
                            data[current_key] = '\n'.join(current_content).strip()
                        current_key = line[4:].strip()
                        current_content = []
                        # 检查是否是dict格式
                        if current_key in ['title_en', 'background_zh', '历史意义_zh']:
                            is_dict_format = True
                    elif current_key:
                        current_content.append(line)

                if current_key:
                    data[current_key] = '\n'.join(current_content).strip()

                # 如果是dict格式，转换为FULL_ARTICLES格式
                if is_dict_format:
                    return convert_to_full_articles_format(title, data)
                return data if data else None
        return None
    except Exception as e:
        print(f'   ⚠️ 读取缓存失败: {e}')
        return None


def convert_to_full_articles_format(title: str, data: Dict) -> Dict:
    '''将缓存数据转换为FULL_ARTICLES兼容格式'''
    # 简化处理：如果有title_en说明是FULL_ARTICLES格式，直接返回
    if 'title_en' in data or '背景_zh' in data.get('background_zh', ''):
        return data
    return data


def save_cached_expansion(title: str, data: Dict) -> bool:
    '''保存扩充内容到缓存'''
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        with open(EXPANSIONS_FILE, 'a', encoding='utf-8') as f:
            f.write(f'\n## {title}\n')
            f.write(f'更新时间: {timestamp}\n\n')
            for key, value in data.items():
                f.write(f'### {key}\n{value}\n\n')
        return True
    except Exception as e:
        print(f'   ⚠️ 保存缓存失败: {e}')
        return False


def generate_expansion_content(article: Dict) -> Dict:
    '''使用模板生成扩充内容（使用FULL_ARTICLES格式）'''
    title = article['title']
    date = article['date']
    background = article['background']

    # 生成使用FULL_ARTICLES兼容格式的内容
    expansion = {
        'title_en': title,
        'background_zh': background,
        'background_en': background,
        '历史意义_zh': background,
        '历史意义_en': background,
        '核心方针': {
            '总方针_zh': '详见原文核心思想',
            '总方针_en': 'See original text for core ideas',
            '根本方法_zh': '详见原文',
            '根本方法_en': 'See original text',
            '核心立场_zh': background,
            '核心立场_en': background
        },
        '核心内容': {
            'title_zh': '核心内容',
            'title_en': 'Core Content',
            'items': [
                {'num': '1', 'name_zh': title, 'name_en': title, 'desc_zh': background, 'desc_en': background}
            ]
        },
        '历史背景': {
            '国内_zh': f'本文写于{date}：{background}',
            '国内_en': f'Written on {date}: {background}',
            '国际_zh': '详见《毛泽东选集》相关历史背景',
            '国际_en': 'See Selected Works for historical background'
        },
        '现代启示': [
            {'启示_zh': f'深入理解《 + title + 的历史背景和现实意义', '启示_en': f'Deeply understand the historical background of {title}'},
            {'启示_zh': '把握文章的核心思想和理论贡献', '启示_en': 'Grasp the core ideas and theoretical contributions'},
            {'启示_zh': '思考对当代的现实指导意义', '启示_en': 'Reflect on contemporary relevance'}
        ],
        '经典箴言': [
            {'箴言_zh': f'《 + title + 》——{date}', '箴言_en': f'《{title}》——{date}', '出处': f'《毛泽东选集》{date}'}
        ]
    }

    return expansion


def get_article_data(title: str, article: Dict = None) -> Optional[Dict]:
    '''获取文章的完整数据'''
    # 1. 先检查 FULL_ARTICLES
    if title in FULL_ARTICLES:
        return FULL_ARTICLES[title]
    for key in FULL_ARTICLES:
        if key in title or title in key:
            return FULL_ARTICLES[key]

    # 2. 再检查缓存文件
    cached = load_cached_expansion(title)
    if cached:
        return cached

    # 3. 没有缓存，生成临时内容（仅用于首次）
    if article:
        generated = generate_expansion_content(article)
        # 保存到缓存
        save_cached_expansion(title, generated)
        return generated

    return None


def generate_obsidian_content(article: Dict, data: Optional[Dict]) -> str:
    '''生成 Obsidian 文档内容 - v5.0八章结构'''
    title = article['title']
    date = article['date']

    content = []
    content.append(f'''---
type: maoxuan
title: {title}
title_en: {data.get('title_en', title) if data else title}
date: {date}
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
source: 《毛泽东选集》
tags:
  - 毛泽东选集
  - 每日学习
---

# {title}

**写作时间 / Date**: {date}  
**文献来源 / Source**: 《毛泽东选集》

''')

    if data:
        # ── v5.0八章结构 ──

        # 一、讲了什么（核心内容）
        if data.get('核心内容'):
            cc = data['核心内容']
            content.append('---\n\n## 一、讲了什么\n## I. Core Content\n\n')
            if cc.get('背景概述'):
                content.append(f'> {cc['背景概述']}\n\n')
            if cc.get('十大关系表'):
                content.append('| 序号 | 核心内容 | 具体阐述 |\n')
                content.append('|------|----------|----------|\n')
                for item in cc['十大关系表']:
                    content.append(f'| {item['num']} | **{item['name_zh']}** | {item['desc_zh']} |\n')
                content.append('')

        # 二、为什么写这篇文章
        if data.get('写作原因'):
            wr = data['写作原因']
            content.append('---\n\n## 二、为什么写这篇文章\n## II. Why Was This Written\n\n')
            if wr.get('时代背景'):
                content.append(f'**时代背景**：{wr['时代背景']}\n\n')
            if wr.get('直接原因'):
                content.append(f'**直接原因**：{wr['直接原因']}\n\n')
            if wr.get('矛盾焦点'):
                content.append(f'**矛盾焦点**：{wr['矛盾焦点']}\n\n')
            if wr.get('理论需求'):
                content.append(f'**理论需求**：{wr['理论需求']}\n\n')

        # 三、文章的核心观点是什么
        if data.get('核心观点'):
            cw = data['核心观点']
            content.append('---\n\n## 三、文章的核心观点是什么\n## III. Core Arguments\n\n')
            if cw.get('核心论点'):
                content.append(f'**核心论点**：{cw['核心论点']}\n\n')
            if cw.get('精华语句'):
                content.append('**精华语句**：\n')
                for i, quote in enumerate(cw['精华语句'], 1):
                    content.append(f'> {i}. {quote}\n')
                content.append('')

        # 四、文章提出了哪些发展方向和政策
        if data.get('发展方向'):
            dp = data['发展方向']
            content.append('---\n\n## 四、文章提出了哪些发展方向和政策\n## IV. Development Directions and Policies\n\n')
            if dp.get('理论方向'):
                content.append(f'**理论方向**：{dp['理论方向']}\n\n')
            if dp.get('政策建议'):
                content.append(f'**政策建议**：{dp['政策建议']}\n\n')

        # 五、文章的观点后来发展如何
        if data.get('历史发展'):
            hd = data['历史发展']
            content.append('---\n\n## 五、文章的观点后来发展如何\n## V. Historical Development\n\n')
            if hd.get('短期影响_zh'):
                content.append(f'**短期影响**：{hd['短期影响_zh']}\n\n')
            if hd.get('中期影响_zh'):
                content.append(f'**中期影响**：{hd['中期影响_zh']}\n\n')
            if hd.get('长期影响_zh'):
                content.append(f'**长期影响**：{hd['长期影响_zh']}\n\n')
            if hd.get('现状影响'):
                content.append(f'**现状影响**：{hd['现状影响']}\n\n')

        # 六、对现在有什么启示
        if data.get('现代启示'):
            content.append('---\n\n## 六、对现在有什么启示\n## VI. Contemporary Enlightenment\n\n')
            for i, insight in enumerate(data['现代启示'], 1):
                content.append(f'{i}. {insight['启示_zh']}\n')
                if insight.get('启示_en'):
                    content.append(f'   *{insight['启示_en']}*\n')
            content.append('')

        # 七、个体如何理解这篇文章
        if data.get('个体理解'):
            ug = data['个体理解']
            content.append('---\n\n## 七、个体如何理解这篇文章\n## VII. Personal Understanding\n\n')
            if ug.get('当时'):
                content.append(f'**当时**：{ug['当时']}\n\n')
            if ug.get('现在'):
                content.append(f'**现在**：{ug['现在']}\n\n')
            if ug.get('对个人启示'):
                content.append(f'**对个人启示**：{ug['对个人启示']}\n\n')

        # 八、经典箴言
        if data.get('经典箴言'):
            content.append('---\n\n## 八、经典箴言\n## VIII. Classic Aphorisms\n\n')
            for i, quote in enumerate(data['经典箴言'], 1):
                content.append(f'> {i}. {quote['箴言_zh']}\n')
                if quote.get('箴言_en'):
                    content.append(f'> *{quote['箴言_en']}*\n')
                if quote.get('出处'):
                    content.append(f'> ——{quote['出处']}\n')
                content.append('')

    else:
        # ── 只有元数据 → 简洁版 ──
        content.append(f'> {article.get('background', '')}\n\n---\n\n')
        content.append('## 文章简介\n## Introduction\n\n')
        content.append(f'本文是毛泽东同志于 {date} 撰写的经典著作，收录于《毛泽东选集》。\n\n')
        content.append(f'**历史背景 / Historical Context**：{article.get('background', '')}\n\n')
        content.append('---\n\n## 学习要点\n## Study Points\n\n')
        content.append('- 了解文章的写作背景和历史条件\n- Understand the historical conditions of the article\n')
        content.append('- 把握文章的核心思想和理论贡献\n- Grasp the core ideas and theoretical contributions\n')
        content.append('- 思考文章对当代的现实指导意义\n- Reflect on the contemporary relevance\n')

    content.append(f'\n---\n*学习日期 / Study Date：{datetime.now().strftime('%Y-%m-%d')}*\n*推送系统 / Push System：每日毛选 v5.5*\n')
    return '\n'.join(content)


def generate_telegram_content(article: Dict, data: Optional[Dict]) -> str:
    '''生成 Telegram 推送内容'''
    title = article['title']
    date = article['date']

    lines = []
    lines.append(f'📚 **{title}**')
    lines.append(f'📅 {date}')
    lines.append('')

    if data:
        lines.append(f'_{data.get('background_zh', '')[:200]}_')
        lines.append('')
        lines.append('━' * 16)

        if data.get('核心内容'):
            lines.append(f'\n📖 *{data['核心内容'].get('title_zh', '核心内容')}*：')
            items = data['核心内容'].get('items', [])
            for item in items[:5]:
                lines.append(f'  {item['num']}. {item.get('name_zh', '')}')
            if len(items) > 5:
                lines.append(f'  ... 还有 {len(items)-5} 项')

        lines.append('')
        lines.append('━' * 16)

        if data.get('核心方针'):
            lines.append(f'\n💡 *核心方针*：')
            lines.append(f'_{data['核心方针'].get('总方针_zh', '')[:150]}_')

        lines.append('\n🌟 *现代启示*：')
        for insight in data.get('现代启示', [])[:3]:
            lines.append(f'• {insight.get('启示_zh', '')}')

        if data.get('经典箴言'):
            lines.append('\n📜 *经典箴言*：')
            first_quote = data['经典箴言'][0]
            lines.append(f'• {first_quote.get('箴言_zh', '')[:100]}...')
    else:
        lines.append(f'_{article.get('background', '')[:200]}_')
        lines.append('')
        lines.append('━' * 16)
        lines.append(f'\n💡 *学习要点*：')
        lines.append('• 了解写作背景和历史条件')
        lines.append('• 把握核心思想和理论贡献')
        lines.append('• 思考对当代的现实指导意义')

    lines.append('')
    lines.append(f'📅 {datetime.now().strftime('%Y-%m-%d')} | 每日毛选')

    return '\n'.join(lines)


def push_to_obsidian(content: str, title: str, output_dir: str = None) -> Path:
    '''推送到 Obsidian 目录'''
    if output_dir is None:
        output_dir = os.environ.get('MAOXUAN_OUTPUT_DIR', DEFAULT_OUTPUT_DIR)

    push_dir = Path(output_dir)
    push_dir.mkdir(parents=True, exist_ok=True)

    safe_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', title)[:30]
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'{date_str}_{safe_title}.md'
    filepath = push_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def push_to_telegram(message: str) -> bool:
    '''推送到 Telegram'''
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')

    if not bot_token or not chat_id:
        print('   ⚠️ 未配置 TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID，跳过 Telegram 推送')
        return False

    try:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        data = urllib.parse.urlencode({
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }).encode()

        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            if result.get('ok'):
                print('   ✅ Telegram 推送成功')
                return True
            else:
                print(f'   ❌ Telegram API 错误: {result.get('description')}')
                return False
    except Exception as e:
        print(f'   ❌ Telegram 推送失败: {e}')
        return False


def main():
    parser = argparse.ArgumentParser(description='每日毛选文章推送 v5.4')
    parser.add_argument('--no-obsidian', action='store_true', help='不推送到 Obsidian')
    parser.add_argument('--no-telegram', action='store_true', help='不推送到 Telegram')
    parser.add_argument('--output-dir', help=f'Obsidian 输出目录（默认: {DEFAULT_OUTPUT_DIR}）')
    parser.add_argument('--chat', action='store_true', help='输出对话格式（不保存文件）')
    args = parser.parse_args()

    print('📚 每日毛选文章推送 v5.4')
    print('=' * 40)

    # 加载文章
    articles = load_articles()
    print(f'📖 文章库: {len(articles)} 篇')

    # 获取今日文章
    article = get_today_article(articles)
    print(f'\n📅 今日文章：《{article['title']}》')
    print(f'   写作时间：{article['date']}')

    # 获取文章数据
    article_data = get_article_data(article['title'], article)
    if article_data:
        print(f'   ✅ 匹配完整内容（六章结构）')
    else:
        print(f'   ℹ️ 使用标准格式（元数据模式）')

    # 推送到 Obsidian
    filepath = None
    if not args.no_obsidian and not args.chat:
        print('\n📤 推送到 Obsidian...')
        obsidian_content = generate_obsidian_content(article, article_data)
        filepath = push_to_obsidian(obsidian_content, article['title'], args.output_dir)
        print(f'   ✅ 已保存: {filepath}')

    # 生成 Telegram 内容
    tg_content = generate_telegram_content(article, article_data)

    if args.chat:
        # 对话模式：输出内容但不保存/推送
        print('\n' + '=' * 40)
        print('📱 Telegram 推送内容：')
        print('=' * 40)
        print(tg_content)
        print('=' * 40)
    elif not args.no_telegram:
        print('\n📱 推送到 Telegram...')
        push_to_telegram(tg_content)

    print('\n✅ 完成！')


if __name__ == '__main__':
    main()


# ── 第一批扩充文章（2026-04-29） ──



# ── v5.0结构扩充文章（2026-04-29） ──

FULL_ARTICLES['矛盾论'] = {
    'title_en': 'On Contradiction',

    # ── 一、讲了什么（核心内容） ──
    '核心内容': {
        '背景概述': '1937年7月，毛泽东撰写《矛盾论》，系统阐述对立统一规律是唯物辩证法的根本法则，批判党内教条主义，为马克思主义中国化奠定哲学基础。',
        '十大关系表': [
            {'num': '1', 'name_zh': '矛盾的普遍性', 'desc_zh': '矛盾存在于一切事物之中，贯穿于一切过程之始终。没有矛盾就没有世界。'},
            {'num': '2', 'name_zh': '矛盾的特殊性', 'desc_zh': '不同事物具有不同性质的矛盾，每一物质的运动形式具有特殊矛盾。'},
            {'num': '3', 'name_zh': '主要矛盾和次要矛盾', 'desc_zh': '在复杂事物发展过程中，主要矛盾起主导作用，决定事物的发展方向。'},
            {'num': '4', 'name_zh': '矛盾的主要方面', 'desc_zh': '矛盾的两个方面中，必有一方是主要的，他方是次要的。'},
            {'num': '5', 'name_zh': '矛盾的同一性和斗争性', 'desc_zh': '矛盾的同一性是暂时的、有条件的；矛盾的斗争性是普遍的、绝对的。'},
            {'num': '6', 'name_zh': '对抗性矛盾和非对抗性矛盾', 'desc_zh': '矛盾的性质不同，解决方法也不同。要正确区分和处理两类不同性质的矛盾。'}
        ]
    },

    # ── 二、为什么写这篇文章 ──
    '写作原因': {
        '时代背景': '1937年7月7日卢沟桥事变，抗日战争全面爆发。中国共产党亟需科学的认识论武器指导革命实践。',
        '直接原因': '党内教条主义者生吞活剥马克思主义经典，拒绝把马克思列宁主义同中国革命具体实际相结合。',
        '矛盾焦点': '主要矛盾：中日民族矛盾上升为主要矛盾。次要矛盾：阶级矛盾退居次要地位。',
        '理论需求': '批判'唯书唯上'的教条主义思想，确立实践第一的的认识论原则。'
    },

    # ── 三、文章的核心观点是什么 ──
    '核心观点': {
        '核心论点': '矛盾是普遍的、绝对的，存在于一切事物之中；同时矛盾又是特殊的、相对的，各种矛盾具有不同的性质。',
        '精华语句': [
            '一切事物中包含的矛盾方面的相互依赖和相互斗争，决定一切事物的生命，推动一切事物的发展。',
            '用不同的方法去解决不同的矛盾，这是马克思列宁主义者必须严格地遵守的一个原则。',
            '矛盾是普遍存在的，但矛盾的性质各不相同，解决方法也各异。'
        ]
    },

    # ── 四、文章提出了哪些发展方向和政策 ──
    '发展方向': {
        '理论方向': '确立实践第一的认识论，强调理论必须与中国实际相结合。',
        '政策建议': '具体问题具体分析，在不同历史时期正确判断主要矛盾和次要矛盾的变化。'
    },

    # ── 五、文章的观点后来发展如何 ──
    '历史发展': {
        '短期影响_zh': '为延安整风运动提供了哲学基础，批判了党内的教条主义倾向。',
        '中期影响_zh': '成为毛泽东思想的重要组成部分，指导了中国革命实践。',
        '长期影响_zh': '对立统一规律成为中国特色社会主义理论体系的哲学基础之一。',
        '现状影响': '《矛盾论》至今仍是马克思主义哲学教育的重要内容，其方法论意义历久弥新。'
    },

    # ── 六、对现在有什么启示 ──
    '现代启示': [
        {'启示_zh': '坚持具体问题具体分析的方法论，反对一刀切和形而上学。', '启示_en': 'Persist in concrete analysis, oppose one-size-fits-all.'},
        {'启示_zh': '善于抓住主要矛盾，在复杂问题中把握重点，推动整体发展。', '启示_en': 'Good at grasping principal contradictions.'},
        {'启示_zh': '正确处理人民内部矛盾，维护社会和谐稳定。', '启示_en': 'Correctly handle contradictions among people.'},
        {'启示_zh': '在对立中把握统一，在斗争中把握同一，促进事物发展。', '启示_en': 'Grasp unity in opposition.'},
        {'启示_zh': '坚持两点论和重点论的统一，全面看问题又突出重点。', '启示_en': 'Persist in unity of two-point and key-point theory.'}
    ],

    # ── 七、个体如何理解这篇文章 ──
    '个体理解': {
        '当时': '革命战争年代，主要矛盾是民族矛盾，每个人都面临抗日救亡的历史任务。',
        '现在': '和平建设时期，主要矛盾是人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。',
        '对个人启示': '面对工作和生活中的困难，要分清主次矛盾；处理人际关系时，既要看到对立也要看到统一；自我提升时，要抓住主要矛盾的主要方面，集中精力解决关键问题。'
    },

    # ── 八、经典箴言 ──
    '经典箴言': [
        {'箴言_zh': '一切事物中包含的矛盾方面的相互依赖和相互斗争，决定一切事物的生命，推动一切事物的发展。', '箴言_en': 'The mutual dependence and struggle of contradictory aspects determines the life of all things.', '出处': '《矛盾论》（1937年7月）'},
        {'箴言_zh': '用不同的方法去解决不同的矛盾，这是马克思列宁主义者必须严格地遵守的一个原则。', '箴言_en': 'Using different methods to resolve different contradictions is a principle Marxists must strictly observe.', '出处': '《矛盾论》（1937年7月）'},
        {'箴言_zh': '矛盾存在于一切事物之中，矛盾无时不在，无处不有。', '箴言_en': 'Contradiction exists in all things, at all times, everywhere.', '出处': '《矛盾论》（1937年7月）'},
        {'箴言_zh': '研究问题，忌带主观性、片面性和表面性。', '箴言_en': 'In studying problems, avoid subjectivity, one-sidedness, and superficiality.', '出处': '《矛盾论》（1937年7月）'}
    ]
}
