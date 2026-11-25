"""How a caption is said, counted and compared, in each language the narration can be in.

The recorder gives a caption as much time as saying it takes, and the narration says it by the same rules, so both
ask here. Mandarin and English have rules of their own for numbers and letters (what comes out is what the speech
engine is given, and `demo_voice.py lines` shows it). The other languages are given to the engine as written,
counted by a general rule and compared more loosely: write their numbers out in words where it matters.

A language is named by its code. The captions of a story are in one language (LANGUAGE in the story file), and
the narration reads the captions, so it is in that language too.
"""
from __future__ import annotations

import re

# code: its own name, the name the Qwen models and DashScope know it by, the locale the page is opened in, how fast it is
# spoken and how fast a caption is given to read (both in the units counted by units(): syllables, or morae for
# Japanese), what the band says while waiting is played fast, and what the narrated file is called after the video's name
LANGUAGES = {
    'zh': dict(name='普通话', english='Mandarin Chinese', qwen='Chinese', locale='zh-CN', pace=4.3, reading=5.5, fast='快进', narrated='配音版', unit='字', anchor=(34, 50),
               stock='下面按顺序介绍各项功能，每一步操作都会在画面上标出。', demo='这是一段功能演示。', title_demo='这是{title}的功能演示。'),
    'en': dict(name='English', english='English', qwen='English', locale='en-US', pace=4.0, reading=3.8, fast='Fast forward', narrated='narrated', unit='syllable', anchor=(28, 44),
               stock='Each step of the way is marked on the screen as it happens.', demo='This is a short demo of the app.', title_demo='This is a short demo of {title}.'),
    'ja': dict(name='日本語', english='Japanese', qwen='Japanese', locale='ja-JP', pace=7.0, reading=6.6, fast='早送り', narrated='narrated', unit='拍', anchor=(34, 52),
               stock='これから機能を順に紹介します。どの操作も画面の上で示されます。', demo='これは機能のデモです。', title_demo='これは{title}の機能デモです。'),
    'ko': dict(name='한국어', english='Korean', qwen='Korean', locale='ko-KR', pace=5.0, reading=4.7, fast='빨리 감기', narrated='narrated', unit='음절', anchor=(30, 48),
               stock='이제 기능을 차례로 소개합니다. 모든 동작은 화면에 표시됩니다.', demo='이것은 기능 시연입니다.', title_demo='이것은 {title} 기능 시연입니다.'),
    'de': dict(name='Deutsch', english='German', qwen='German', locale='de-DE', pace=4.2, reading=4.0, fast='Zeitraffer', narrated='narrated', unit='syllable', anchor=(30, 48),
               stock='Jeder Schritt wird auf dem Bildschirm markiert.', demo='Dies ist eine kurze Demo der App.', title_demo='Dies ist eine kurze Demo von {title}.'),
    'fr': dict(name='Français', english='French', qwen='French', locale='fr-FR', pace=4.8, reading=4.5, fast='Accéléré', narrated='narrated', unit='syllable', anchor=(30, 48),
               stock='Chaque étape est marquée à l’écran.', demo='Voici une courte démonstration de l’application.', title_demo='Voici une courte démonstration de {title}.'),
    'es': dict(name='Español', english='Spanish', qwen='Spanish', locale='es-ES', pace=5.2, reading=4.9, fast='Avance rápido', narrated='narrated', unit='syllable', anchor=(30, 48),
               stock='Cada paso se marca en la pantalla.', demo='Esta es una breve demostración de la aplicación.', title_demo='Esta es una breve demostración de {title}.'),
    'it': dict(name='Italiano', english='Italian', qwen='Italian', locale='it-IT', pace=5.2, reading=4.9, fast='Avanti veloce', narrated='narrated', unit='syllable', anchor=(30, 48),
               stock='Ogni passo viene segnato sullo schermo.', demo='Questa è una breve dimostrazione dell’app.', title_demo='Questa è una breve dimostrazione di {title}.'),
    'pt': dict(name='Português', english='Portuguese', qwen='Portuguese', locale='pt-BR', pace=5.0, reading=4.7, fast='Avanço rápido', narrated='narrated', unit='syllable', anchor=(30, 48),
               stock='Cada passo é marcado na tela.', demo='Esta é uma breve demonstração do aplicativo.', title_demo='Esta é uma breve demonstração de {title}.'),
    'ru': dict(name='Русский', english='Russian', qwen='Russian', locale='ru-RU', pace=4.8, reading=4.5, fast='Ускорено', narrated='narrated', unit='syllable', anchor=(30, 48),
               stock='Каждый шаг отмечается на экране.', demo='Это короткая демонстрация приложения.', title_demo='Это короткая демонстрация {title}.'),
}
OTHER_NAMES = {'中文': 'zh', '汉语': 'zh', '国语': 'zh', 'mandarin': 'zh', 'chinese': 'zh', 'cn': 'zh', '英语': 'en', '英文': 'en', '日语': 'ja', '日文': 'ja', 'jp': 'ja',
               '韩语': 'ko', '韩文': 'ko', 'kr': 'ko', '德语': 'de', '法语': 'fr', '西班牙语': 'es', '意大利语': 'it', '葡萄牙语': 'pt', '俄语': 'ru'}


def language(name):
    """The code of a language named by its code ('en', 'zh-CN'), its own name ('普通话') or its English name ('Chinese'). None stays None."""
    if not name:
        return None
    known = str(name).strip().lower()
    for code, facts in LANGUAGES.items():
        if known in (code, facts['name'].lower(), facts['english'].lower(), facts['qwen'].lower(), facts['locale'].lower()):
            return code
    if known in OTHER_NAMES or known.split('-')[0].split('_')[0] in LANGUAGES:
        return OTHER_NAMES.get(known) or known.split('-')[0].split('_')[0]
    raise SystemExit(f'不认识这种语言：{name}；能用的是 {"、".join(f"{code}（{facts[chr(110) + chr(97) + chr(109) + chr(101)]}）" for code, facts in LANGUAGES.items())}')


def chinese(text):
    """Is this text written in Chinese characters rather than in words with spaces between them?"""
    wide = sum(1 for ch in text if 0x2E80 <= ord(ch) <= 0x9FFF or 0xF900 <= ord(ch) <= 0xFAFF or 0xFF00 <= ord(ch) <= 0xFFEF)  # the characters and their punctuation
    return 2 * wide >= len(text.replace(' ', ''))


def guess(texts):
    """The language of captions whose story does not say: Mandarin if most of them are in Chinese characters, else English."""
    texts = [text for text in texts if text.strip()]
    return 'zh' if texts and 2 * sum(chinese(text) for text in texts) >= len(texts) else 'en'


# ---------- Mandarin ----------
DIGITS = '零一二三四五六七八九'
HAN = chr(0x4E00) + '-' + chr(0x9FFF)   # the Chinese characters, for use inside [...] of a pattern
COUNTED = '个|项|份|件|场|种|边|条|次|位|名|张|页|行|段|步|类|组|天|分钟|小时|秒|周|倍|处|遍|封|台|套|家|层|块|篇|本|句|批|轮|栏|列|人|户|笔|万|亿|千|百'
AMOUNT = re.compile(r'\s*(?:多|余|来)?(?:' + COUNTED + '|元|字|章|节|岁|米|度|帧|例|起|门|所|间|辆|道|题|单|票|分|年|月|日|号|像素|毫秒|公里|千克|公斤|毫米|厘米|GB|MB|KB|TB|ms|px|fps|Hz|kg|km|cm|mm)')
PAUSES = '，。；：、！？,.;:!?'


def cardinal(n, first=True):
    """A whole number read as an amount: 十二, 一百零五, 一千二百, 三万零五十."""
    if n < 10 ** 4:
        out, gap = '', False
        for power, unit in ((3, '千'), (2, '百'), (1, '十'), (0, '')):
            digit = n // 10 ** power % 10
            if digit:
                out += ('零' if gap else '') + ('' if (power, digit) == (1, 1) and first and not out else DIGITS[digit]) + unit
            gap = bool(out) and not digit
        return out or DIGITS[0]
    power, unit = (8, '亿') if n >= 10 ** 8 else (4, '万')
    head, rest = divmod(n, 10 ** power)
    return cardinal(head, first) + unit + (('零' if rest < 10 ** (power - 1) else '') + cardinal(rest, False) if rest else '')


def one_by_one(digits):
    return ''.join(DIGITS[int(digit)] for digit in digits)


def spoken_zh(text):
    """The rules: a date, a year (digit by digit), a per cent, a range, a decimal, 2 before a counting word (两), a whole
    number (below a hundred or before a unit as an amount, else digit by digit), a short word in capitals (letter by letter)."""
    amount = lambda number: cardinal(int(number.split('.')[0])) + ''.join('点' + one_by_one(part) for part in number.split('.')[1:])
    text = re.sub(r'(?<!\d)(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?!\d)', lambda m: f'{one_by_one(m[1])}年{cardinal(int(m[2]))}月{cardinal(int(m[3]))}日', text)
    text = re.sub(r'(?<!\d)(\d{4})\s*年', lambda m: one_by_one(m[1]) + '年', text)
    text = re.sub(r'(\d+(?:\.\d+)?)\s*[%％]', lambda m: '百分之' + amount(m[1]), text)
    text = re.sub(r'(?<![\d.-])(\d{1,3})\s*[-~～—–]\s*(\d{1,3})(?![\d.-])', lambda m: f'{m[1]}到{m[2]}', text)
    text = re.sub(r'\d+(?:\.\d+)+', lambda m: amount(m[0]), text)
    text = re.sub(r'(?<![\d.第])(?<!第\s)2(?![\d.])\s*(?=' + COUNTED + ')', '两', text)
    text = re.sub(r'\d+', lambda m: one_by_one(m[0]) if (m[0][0] == '0' and len(m[0]) > 1) or (len(m[0]) > 2 and not AMOUNT.match(m.string, m.end())) else cardinal(int(m[0])), text)
    text = re.sub(r'(?<![A-Za-z])[A-Z]{2,5}(?![A-Za-z])', lambda m: ' '.join(m[0]), text)
    return re.sub(r'(?<=[' + HAN + r'，。；：、”])\s+(?=[' + HAN + r'“])', '', text)


def syllables(text):
    """How many syllables saying a Mandarin text takes: one for each character, one for each letter said by its name, two for another word."""
    return len(re.findall('[' + HAN + ']', text)) + sum(len(word) if word.isupper() else 2 for word in re.findall(r'[A-Za-z]+', text))


# ---------- English ----------
SMALL = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = '- - twenty thirty forty fifty sixty seventy eighty ninety'.split()
NTH = {'one': 'first', 'two': 'second', 'three': 'third', 'five': 'fifth', 'eight': 'eighth', 'nine': 'ninth', 'twelve': 'twelfth'}
MONTHS = 'January February March April May June July August September October November December'.split()
MONEY = {'$': 'dollar', '€': 'euro', '£': 'pound', '¥': 'yen'}


def number(n):
    """A whole number in words: forty two, one hundred five, three thousand twenty. No hyphens: every word is one a dictionary has."""
    if n < 20:
        return SMALL[n]
    if n < 100:
        return TENS[n // 10] + (' ' + SMALL[n % 10] if n % 10 else '')
    if n < 1000:
        return SMALL[n // 100] + ' hundred' + (' ' + number(n % 100) if n % 100 else '')
    for power, name in ((9, 'billion'), (6, 'million'), (3, 'thousand')):
        if n >= 10 ** power:
            head, rest = divmod(n, 10 ** power)
            return number(head) + ' ' + name + (' ' + number(rest) if rest else '')


def digit_by_digit(digits):
    return ' '.join(SMALL[int(digit)] for digit in digits)


def amount(text):
    """A number as written, with or without a decimal part: 12, 2.5, 007, 1234567890123."""
    whole, _, rest = text.partition('.')
    said = digit_by_digit(whole) if (whole[0] == '0' and len(whole) > 1) or len(whole) > 12 else number(int(whole))
    return said + ''.join(' point ' + digit_by_digit(part) for part in rest.split('.') if part)


def nth(n):
    """first, twenty third, one hundredth."""
    words = number(n).split()
    last = words[-1]
    words[-1] = NTH.get(last) or (last[:-1] + 'ieth' if last.endswith('y') else last + 'th')
    return ' '.join(words)


def year(n):
    """A year the way it is said: nineteen ninety nine, two thousand five, twenty twenty six."""
    head, rest = divmod(n, 100)
    if rest == 0:
        return number(n) if head % 10 == 0 else number(head) + ' hundred'
    if head == 20 and rest < 10:
        return 'two thousand ' + SMALL[rest]
    return number(head) + (' oh ' + SMALL[rest] if rest < 10 else ' ' + number(rest))


def spoken_en(text):
    """The rules: thousands written with commas, money, a per cent, a date (2026-11-19), a time (10:30), 1st 2nd 3rd, a range,
    a decimal or a version number, a year, a whole number (digit by digit when it starts with a zero), a short word in
    capitals (letter by letter), and the signs & + = @."""
    text = re.sub(r'(?<![\d.,])(\d{1,3}(?:,\d{3})+(?:\.\d+)?)(?!\d)', lambda m: amount(m[1].replace(',', '')), text)   # 1,250 is a count, not a year

    def money(m):
        whole, _, cents = m[2].partition('.')
        unit = MONEY[m[1]]
        said = amount(whole) + ' ' + unit + ('' if whole == '1' or unit == 'yen' else 's')
        return said + (f' and {number(int(cents))} cent{"" if int(cents) == 1 else "s"}' if len(cents) == 2 and int(cents) and unit != 'yen' else ' point ' + digit_by_digit(cents) if cents and int(cents) else '')
    text = re.sub(r'([$€£¥])\s?(\d+(?:\.\d+)?)', money, text)
    text = re.sub(r'(\d+(?:\.\d+)?)\s?[%％]', lambda m: amount(m[1]) + ' percent', text)
    text = re.sub(r'(?<![\d.])(\d{4})-(\d{1,2})-(\d{1,2})(?![\d.])', lambda m: f'{MONTHS[int(m[2]) - 1]} {nth(int(m[3]))}, {year(int(m[1]))}' if 1 <= int(m[2]) <= 12 and 1 <= int(m[3]) <= 31 else m[0], text)
    text = re.sub(r'(?<![\d.:])(\d{1,2}):(\d{2})(?![\d:])', lambda m: number(int(m[1])) + (" o'clock" if m[2] == '00' else ' oh ' + SMALL[int(m[2])] if m[2][0] == '0' else ' ' + number(int(m[2]))), text)
    text = re.sub(r'(?<![\d.])(\d+)(?:st|nd|rd|th)\b', lambda m: nth(int(m[1])), text)
    text = re.sub(r'(?<![\d.-])(\d{1,4})\s?[-~–—]\s?(\d{1,4})(?![\d.-])', lambda m: f'{m[1]} to {m[2]}', text)
    text = re.sub(r'\d+(?:\.\d+)+', lambda m: amount(m[0]), text)
    text = re.sub(r'(?<![\d.])(1[1-9]\d\d|20\d\d)(?![\d.])', lambda m: year(int(m[1])), text)
    text = re.sub(r'\d+', lambda m: amount(m[0]), text)
    text = re.sub(r'(?<![A-Za-z])[A-Z]{2,5}(?![A-Za-z])', lambda m: ' '.join(m[0]), text)
    for sign, word in (('&', 'and'), ('+', 'plus'), ('=', 'equals'), ('@', 'at')):
        text = text.replace(sign, f' {word} ')
    return text


def syllables_en(word):
    """About how many syllables an English word has: its groups of vowels, less an e that is not said at its end."""
    if len(word) == 1 and word.isupper():
        return 3 if word == 'W' else 1   # a letter said by its name
    word = word.lower().strip("'")
    groups = len(re.findall(r'[aeiouy]+', word))
    if groups > 1 and re.search(r'[^aeiouy]es$|[^aeiouytd]ed$', word) and not re.search(r'(?:[sxzcg]|ch|sh)es$', word):
        groups -= 1   # saves, used: not sav-es, us-ed
    elif groups > 1 and word.endswith('e') and not re.search(r'[^aeiouy]le$', word):
        groups -= 1   # page, whole: but ta-ble
    return max(1, groups)


# ---------- every language ----------
LATIN_VOWELS = 'aeiouyàâäáãåæèéêëìíîïòóôöõœøùúûüýÿąęı'
CYRILLIC_VOWELS = 'аеёиоуыэюяіїє'
SMALL_KANA = 'ゃゅょぁぃぅぇぉゎャュョァィゥェォヮ'


def spoken(text, say=None, tongue='zh'):
    """A caption the way it is given to the speech engine in this language.

    `say` gives the reading of whatever the rules get wrong, e.g. {'WPS 365': 'W P S 三六五'} or {'GitHub': 'git hub'}:
    its keys are found whatever their case and with or without the blanks.
    """
    for key, value in sorted((say or {}).items(), key=lambda item: -len(item[0])):
        text = re.sub(r'\s*'.join(re.escape(part) for part in key.split()), lambda match: value, text, flags=re.IGNORECASE)
    text = spoken_zh(text) if tongue == 'zh' else spoken_en(text) if tongue == 'en' else text
    return re.sub(r'\s{2,}', ' ', text).strip()


def units(text, tongue='zh'):
    """How long saying a text takes, in what this language is counted in: syllables (morae for Japanese). An estimate for
    all but Mandarin, good enough to give a caption its time and to tell which lines are tight."""
    if tongue == 'zh':
        return syllables(text)
    if tongue == 'en':
        return sum(syllables_en(word) for word in re.findall(r"[A-Za-z][A-Za-z']*", text)) + 2 * len(re.findall(r'\d', text))
    latin = sum(max(1, len(re.findall(f'[{LATIN_VOWELS}]+', word.lower()))) for word in re.findall(r'[^\W\d_]+', text) if word[0].lower() <= 'ʯ')
    cyrillic = len(re.findall(f'[{CYRILLIC_VOWELS}]', text.lower()))
    kana = len(re.findall('[' + chr(0x3041) + '-' + chr(0x30FF) + ']', text)) - sum(text.count(ch) for ch in SMALL_KANA + '・')
    hangul = len(re.findall('[' + chr(0xAC00) + '-' + chr(0xD7A3) + ']', text))
    return latin + cyrillic + kana + hangul + 2 * len(re.findall('[' + HAN + ']', text)) + 2 * len(re.findall(r'\d', text))


def reading_time(text, tongue=None, a_second=None, say=None):
    """How long a caption is given before the next thing happens: long enough to be read, and to be read aloud."""
    tongue = tongue or ('zh' if chinese(text) else 'en')
    a_second = a_second or LANGUAGES[tongue]['reading']
    said = spoken(text, say, tongue)
    marks = sum(said.count(mark) for mark in PAUSES)
    if tongue == 'zh':  # by its characters, or by what saying it takes where numbers and letters make that longer
        return 1.2 + max(len(text), syllables(said) + marks) / a_second
    return 1.2 + (units(said, tongue) + marks) / a_second


CONTRACTIONS = [(r"(?i)\bcan't\b", 'can not'), (r"(?i)\bcannot\b", 'can not'), (r"(?i)\bwon't\b", 'will not'),
                (r"(?i)\b(\w+)n't\b", r'\1 not'), (r"(?i)'(re)\b", ' are'), (r"(?i)'(ve)\b", ' have'), (r"(?i)'(ll)\b", ' will'),
                (r"(?i)'(m)\b", ' am'), (r"(?i)'(d)\b", ' would'), (r"(?i)'(s)\b", ''), (r"'", '')]


def unwrapped(text):
    """A text as it sounds rather than as it is written: contractions written out (don't and do not are the same words),
    hyphens and apostrophes away."""
    for pattern, replacement in CONTRACTIONS:
        text = re.sub(pattern, replacement, text)
    return text.replace('-', ' ')


def sounds(text, tongue='zh', say=None):
    """A text as the row of what is heard in it, so that two texts that sound the same compare as equal: Mandarin by its
    syllables (a character that has several readings stands for all of them: which one is meant cannot be told from the
    writing, so that is left to the ear), Japanese and Korean by their characters, the other languages by their words."""
    said = spoken(text, say, tongue)
    if tongue not in ('zh', 'ja', 'ko'):
        said = unwrapped(said)
    if tongue == 'zh':
        from pypinyin import Style, pinyin
        out = []
        for part in re.findall('[' + HAN + ']+|[A-Za-z][A-Za-z ]*', said):
            out += [frozenset([part.replace(' ', '').lower()])] if part[0].isascii() else [frozenset(readings) for readings in pinyin(part, style=Style.NORMAL, heteronym=True)]
        return out
    said = re.sub(r"['’`]", '', said.casefold())
    if tongue in ('ja', 'ko'):
        return [frozenset([ch]) for ch in re.sub(r'[\W_]', '', said)]
    return [frozenset([word]) for word in re.findall(r'[^\W_]+', said)]


def distance(a, b):
    """How many of them have to be changed, dropped or added to get from one row to the other."""
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        previous, row[0] = row[0], i
        for j, y in enumerate(b, 1):
            previous, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, previous + (not x & y))
    return row[-1]


def differs(said, heard, tongue='zh', say=None):
    """How much of what was to be said is not in what was heard: (how many differ, out of how many). Words that are only
    cut up differently (to-do, todo, to do; A P I, API) do not count."""
    wanted, got = sounds(said, tongue, say), sounds(heard, tongue, say)
    if tongue != 'zh' and ''.join(min(part) for part in wanted) == ''.join(min(part) for part in got):
        return 0, len(wanted)
    return distance(wanted, got), len(wanted)
