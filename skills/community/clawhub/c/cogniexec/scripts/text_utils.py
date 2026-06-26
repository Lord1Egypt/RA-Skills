#!/usr/bin/env python3
"""
text_utils.py — 文本处理工具（纯标准库）
覆盖：Diff比较、正则提取/替换、文本统计、模板填充、编码检测/转换/Markdown转HTML

用法：
  python text_utils.py diff file_a.txt file_b.txt
  python text_utils.py diff "Hello World" "Hello Python" --text
  python text_utils.py regex-extract data.txt --pattern "\d+\.\d+"
  python text_utils.py regex-replace input.txt --pattern "\\b\\w+\\b" --replacement "[MATCH]" -o output.txt
  python text_utils.py stats article.md --words --chars --lines
  python text_utils.py fill-template template.jsonl data.json
  python text_utils.py encode-detect messy.txt
  python text_utils.py convert-encoding file.txt --from gb2312 --to utf-8
  python text_utils.py word-frequency essay.txt --top 20
  python text_utils.py extract-emails contacts.txt
  python text_utils.py wrap-text long_text.txt --width 80
  python text_utils.py md2html readme.md -o readme.html
"""

import sys
import os
import re
import json
import difflib
import string
import unicodedata
from collections import Counter, defaultdict
from typing import Optional


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36,
             'red_bg': 41, 'green_bg': 42}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


def read_file_or_text(source: str) -> str:
    """读取文件或直接返回文本"""
    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    return source


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def cmd_diff(args):
    """文本差异对比（类 unified diff）"""
    src_a = args['_pos'][0] if len(args.get('_pos', [])) > 0 else ''
    src_b = args['_pos'][1] if len(args.get('_pos', [])) > 1 else ''
    is_text = args.get('text', False)
    context_lines = int(args.get('context', 3))
    output_format = args.get('format', 'text')  # text, json, stats

    text_a = read_file_or_text(src_a) if not (is_text and src_a) else src_a
    text_b = read_file_or_text(src_b) if not (is_text and src_b) else src_b

    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)

    # 统计信息
    added = sum(1 for line in lines_b if line not in lines_a)
    removed = sum(1 for line in lines_a if line not in lines_b)
    unchanged = sum(1 for line in lines_b if line in lines_a)

    if output_format == 'stats':
        result = {
            'file_a': src_a, 'file_b': src_b,
            'lines_a': len(lines_a), 'lines_b': len(lines_b),
            'added': added, 'removed': removed, 'unchanged': unchanged,
            'similarity': difflib.SequenceMatcher(None, text_a, text_b).ratio(),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if output_format == 'json':
        differ = difflib.unified_diff(lines_a, lines_b,
                                       fromfile=src_a or 'a', tofile=src_b or 'b',
                                       n=context_lines)
        diff_lines = list(differ)
        print(json.dumps({
            'diff': ''.join(diff_lines),
            'stats': {'added': added, 'removed': removed, 'similarity': round(
                difflib.SequenceMatcher(None, text_a, text_b).ratio(), 4)},
        }, ensure_ascii=False, indent=2))
        return

    # 文本格式输出
    echo(f'=== 差异对比: "{src_a}" vs "{src_b}" ===', fg='cyan', bold=True)
    similarity = difflib.SequenceMatcher(None, text_a, text_b).ratio()
    echo(f'相似度: {similarity:.1%} | A:{len(lines_a)}行 B:{len(lines_b)}行 | '
         f'+{added} /-{removed}', fg='blue')
    print()

    differ = difflib.unified_diff(lines_a, lines_b,
                                   fromfile='A', tofile='B', n=context_lines)

    has_diff = False
    for line in differ:
        has_diff = True
        if line.startswith('+') and not line.startswith('+++'):
            print(color(line, 'green'))
        elif line.startswith('-') and not line.startswith('---'):
            print(color(line, 'red'))
        elif line.startswith('@'):
            print(color(line, 'cyan'))
        else:
            print(line, end='')

    if not has_diff:
        echo('✅ 完全相同，无差异', fg='green')


def cmd_regex_extract(args):
    """正则表达式提取"""
    source = args['_pos'][0] if args.get('_pos') else ''
    pattern = args.get('pattern', '')
    flags_str = args.get('flags', '')  # i, m, s, etc.
    group = int(args.get('group', 0))  # 提取的组号
    output = args.get('o', '')

    text = read_file_or_text(source)

    flags = 0
    for f in flags_str.lower():
        if f == 'i':
            flags |= re.IGNORECASE
        elif f == 'm':
            flags |= re.MULTILINE
        elif f == 's':
            flags |= re.DOTALL

    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        echo(f'❌ 正则语法错误: {e}', fg='red')
        sys.exit(1)

    matches = compiled.findall(text)
    flat_matches = []
    for m in matches:
        if isinstance(m, tuple):
            if group < len(m) and group >= 0:
                flat_matches.append(m[group])
            else:
                flat_matches.append(str(m))
        else:
            flat_matches.append(m)

    echo(f'🔍 找到 {len(flat_matches)} 个匹配:', fg='cyan')

    # 去重统计
    counter = Counter(flat_matches)
    from scripts.table_format import tabulate
    rows = [{'匹配': m, '出现次数': c} for m, c in counter.most_common(100)]
    print(tabulate(rows, tablefmt='grid'))

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(flat_matches, f, ensure_ascii=False, indent=2)


def cmd_regex_replace(args):
    """正则批量替换"""
    source = args['_pos'][0] if args.get('_pos') else ''
    pattern = args.get('pattern', '')
    replacement = args.get('replacement', '')
    flags_str = args.get('flags', '')
    output = args.get('o', '')

    if not pattern or replacement is None:
        echo('⚠️ 请提供 --pattern 和 --replacement', fg='yellow')
        return

    text = read_file_or_text(source)

    flags = 0
    for f in flags_str.lower():
        if f == 'i': flags |= re.IGNORECASE
        elif f == 'm': flags |= re.MULTILINE
        elif f == 's': flags |= re.DOTALL

    try:
        result, count = re.subn(pattern, replacement, text, flags=flags)
    except re.error as e:
        echo(f'❌ 正则错误: {e}', fg='red')
        return

    echo(f'🔄 替换了 {count} 处', fg='cyan')

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        echo(f'✅ 已写入: {output}', fg='green')
    else:
        print(result[:5000])


def cmd_stats(args):
    """文本统计分析"""
    source = args['_pos'][0] if args.get('_pos') else ''
    show_words = args.get('words', True)
    show_chars = args.get('chars', True)
    show_lines = args.get('lines', True)
    show_bytes = args.get('bytes', False)
    show_sentences = args.get('sentences', False)
    show_paragraphs = args.get('paragraphs', False)
    show_unique_words = args.get('unique', False)
    output = args.get('o', '')

    text = read_file_or_text(source)

    char_count = len(text)
    byte_count = len(text.encode('utf-8'))
    lines = [l for l in text.split('\n')]
    line_count = len(lines)
    non_empty_lines = [l for l in lines if l.strip()]
    words = re.findall(r'\S+', text)
    word_count = len(words)
    unique_word_count = len(set(w.lower() for w in words))

    # 句子数（中英文）
    sentences = re.split(r'[。！？.!?\n]+', text)
    sentence_count = len([s for s in sentences if s.strip()])

    # 段落数
    paragraphs = re.split(r'\n\s*\n', text)
    paragraph_count = len([p for p in paragraphs if p.strip()])

    # 字符类型分布
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_count = len(re.findall(r'[a-zA-Z]', text))
    digit_count = len(re.findall(r'[0-9]', text))
    punctuation_count = len(re.findall(r'[^\w\s\u4e00-\u9fff]', text))
    space_count = len(re.findall(r'\s', text))

    from scripts.table_format import tabulate
    rows = [
        ['字符数', f'{char_count:,}', f'其中中文{chinese_count} 英文{english_count} 数字{digit_count}'],
        ['字节数(UTF-8)', f'{byte_count:,}', ''],
        ['单词数', f'{word_count:,}', f'不重复词数: {unique_word_count}' if show_unique_words else ''],
        ['行数', f'{line_count:,}', f'非空行: {len(non_empty_lines):,}'],
        ['句子数', f'{sentence_count:,}', ''] if show_sentences else None,
        ['段落数', f'{paragraph_count:,}', ''] if show_paragraphs else None,
        ['标点符号', f'{punctuation_count:,}', ''],
        ['空白字符', f'{space_count:,}', ''],
    ]
    rows = [r for r in rows if r is not None]
    print(tabulate(rows, headers=['指标', '值', '备注'], tablefmt='grid'))

    # 频率最高的词
    if words:
        top_words = Counter(w.lower() for w in words).most_common(20)
        # 过滤停用词
        stopwords = set('the a an is are was were be have has had do does did will would shall can could may might should of in on at to for by with about from that this it its as but or not and so if then than also into over after before between through during under without'.split())
        meaningful = [(w, c) for w, c in top_words if w not in stopwords and len(w) > 1][:10]
        if meaningful:
            echo(f'\n📝 高频词汇 TOP 10:', fg='cyan')
            wf_rows = [{'词': w, '次数': c} for w, c in meaningful]
            print(tabulate(wf_rows, tablefmt='grid'))

    if output:
        stats_data = {
            'chars': char_count, 'bytes': byte_count,
            'words': word_count, 'unique_words': unique_word_count,
            'lines': line_count, 'non_empty_lines': len(non_empty_lines),
            'chinese': chinese_count, 'english': english_count,
            'digits': digit_count, 'punctuation': punctuation_count,
        }
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=2)
        echo(f'\n📄 统计数据已保存: {output}', fg='green')


def cmd_fill_template(args):
    """JSON 模板填充"""
    template_source = args['_pos'][0] if args.get('_pos') else ''
    data_source = args.get('data', '{}')
    output = args.get('o', '')

    # 读取模板（每行一个 JSON 对象或 JSONL）
    template_text = read_file_or_text(template_source)
    template_lines = template_text.split('\n')

    # 读取数据
    try:
        data = json.loads(data_source)
    except json.JSONDecodeError:
        with open(data_source, 'r', encoding='utf-8') as f:
            data = json.load(f)

    results = []
    for tmpl_line in template_lines:
        tmpl_line = tmpl_line.strip()
        if not tmpl_line:
            continue

        # 尝试解析为 JSON 模板
        try:
            tmpl_obj = json.loads(tmpl_line)
            filled = _deep_fill(tmpl_obj, data)
            results.append(json.dumps(filled, ensure_ascii=False))
        except json.JSONDecodeError:
            # 纯文本模板：用 {{key}} 占位符
            filled = tmpl_line
            def replacer(match):
                key = match.group(1).strip()
                keys = key.split('.')
                val = data
                try:
                    for k in keys:
                        val = val[k]
                    return str(val)
                except (KeyError, TypeError, IndexError):
                    return match.group(0)
            filled = re.sub(r'\{\{(.+?)\}\}', replacer, filled)
            results.append(filled)

    output_text = '\n'.join(results)
    print(output_text[:3000])

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(output_text)
        echo(f'✅ 已写入 {len(results)} 条 → {output}', fg='green')


def _deep_fill(obj: Any, context: dict) -> Any:
    """递归填充 JSON 模板中的占位符"""
    if isinstance(obj, str):
        def replacer(match):
            key = match.group(1).strip()
            keys = key.split('.')
            val = context
            try:
                for k in keys:
                    val = val[k]
                return str(val)
            except (KeyError, TypeError):
                return match.group(0)
        return re.sub(r'\{\{(.+?)\}\}', replacer, obj)
    elif isinstance(obj, dict):
        return {k: _deep_fill(v, context) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_deep_fill(item, context) for item in obj]
    return obj


def cmd_encode_detect(args):
    """编码检测与转换"""
    source = args['_pos'][0] if args.get('_pos') else ''

    if os.path.isfile(source):
        raw_bytes = None
        for enc_candidate in ('utf-8', 'gbk', 'gb18030', 'gb2312', 'big5', 'shift_jis',
                               'latin-1', 'cp1252', 'ascii'):
            try:
                with open(source, 'rb') as f:
                    sample = f.read(4096)
                    sample.decode(enc_candidate)
                # 进一步验证
                full_text = open(source, 'r', encoding=enc_candidate, errors='strict').read()
                raw_bytes = open(source, 'rb').read()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            with open(source, 'rb') as f:
                raw_bytes = f.read()

        from scripts.table_format import tabulate
        echo(f'🔍 编码检测: {source}', fg='cyan')
        echo(f'   文件大小: {len(raw_bytes)} bytes', fg='blue')

        encodings_tested = []
        for enc in ['utf-8', 'gbk', 'gb18030', 'big5', 'shift_jis', 'latin-1']:
            try:
                decoded = raw_bytes[:min(len(raw_bytes), 8192)].decode(enc)
                # 检查是否有大量乱码
                weird_ratio = sum(1 for ch in decoded if ord(ch) > 0xFFFF or
                                  (unicodedata.category(ch) in ('Co', 'Cc') and ch != '\n')) / max(len(decoded), 1)
                encodings_tested.append({
                    '编码': enc,
                    '状态': color('✅ 可读', 'green') if weird_ratio < 0.05 else color('⚠️ 可能乱码', 'yellow'),
                    '乱码率': f'{weird_ratio*100:.1f}%',
                    '预览': decoded[:50].replace('\n', '\\n'),
                })
            except Exception:
                encodings_tested.append({'编码': enc, '状态': '❌ 解码失败', '乱码率': '-', '预览': '-'})

        print(tabulate(encodings_tested, tablefmt='grid'))


def cmd_convert_encoding(args):
    """文件编码转换"""
    source = args['_pos'][0] if args.get('_pos') else ''
    from_enc = args.get('from', 'auto')
    to_enc = args.get('to', 'utf-8')
    output = args.get('o', '')

    if not os.path.isfile(source):
        echo(f'❌ 文件不存在: {source}', fg='red')
        sys.exit(1)

    if from_enc == 'auto':
        # 自动检测
        raw = open(source, 'rb').read()
        detected = 'utf-8'
        for enc in ('utf-8-sig', 'utf-8', 'gbk', 'gb18030', 'big5', 'latin-1'):
            try:
                raw.decode(enc)
                detected = enc
                break
            except UnicodeDecodeError:
                continue
        from_enc = detected
        echo(f'🔍 检测到编码: {from_enc}', fg='cyan')

    with open(source, 'r', encoding=from_enc, errors='replace') as f:
        content = f.read()

    dest = output or source + '.converted'
    with open(dest, 'w', encoding=to_enc) as f:
        f.write(content)

    echo(f'✅ {from_enc} → {to_enc}: {dest}', fg='green')


def cmd_word_frequency(args):
    """词频分析"""
    source = args['_pos'][0] if args.get('_pos') else ''
    top_n = int(args.get('top', 30))
    min_length = int(args.get('min_len', 2))
    stop_words_arg = args.get('stopwords', '')
    output = args.get('o', '')

    text = read_file_or_text(source)

    # 中英文分词
    # 英文：按单词拆分
    english_words = re.findall(r'[a-zA-Z]{%d,}' % min_length, text.lower())
    # 中文：简单拆分（逐字，实际应用建议用 jieba）
    chinese_words = []
    # 尝试按常见模式分词
    cn_segments = re.findall(r'[\u4e00-\u9fff]{%d,}' % min_length, text)
    for seg in cn_segments:
        # 简单二元分词
        if len(seg) >= 2:
            for i in range(len(seg)-1):
                chinese_words.append(seg[i:i+2])
        if len(seg) >= 1:
            chinese_words.extend(list(seg))

    all_words = english_words + chinese_words

    # 默认停用词
    default_stops = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall',
        'can', 'could', 'may', 'might', 'should', 'of', 'in', 'on', 'at', 'to',
        'for', 'by', 'with', 'about', 'from', 'that', 'this', 'it', 'its', 'as',
        'but', 'or', 'not', 'and', 'so', 'if', 'then', 'than', 'also', 'into',
        'over', 'after', 'before', 'between', 'through', 'during', 'under', 'without',
        '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
        '自己', '这', '他', '她', '它', '们', '什么', '怎么', '哪里', '哪个', '多少',
    }

    stops = set(default_stops)
    if stop_words_arg:
        stops.update(stop_words_arg.split(','))

    filtered = [w for w in all_words if w not in stops and len(w) >= min_length]
    freq = Counter(filtered)

    from scripts.table_format import tabulate
    rows = [
        {'排名': i+1, '词语': word, '频次': count,
         '占比': f'{count/len(all_words)*100:.2f}%'}
        for i, (word, count) in enumerate(freq.most_common(top_n))
    ]
    echo(f'📊 词频分析 (总词数: {len(all_words)}, 有效词: {len(filtered)}, TOP {top_n}):',
         fg='cyan')
    print(tabulate(rows, tablefmt='grid'))

    if output:
        export = {'total_words': len(all_words), 'unique_words': len(freq),
                  'filtered_words': len(filtered),
                  'frequency': dict(freq.most_common(top_n))}
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(export, f, ensure_ascii=False, indent=2)
        echo(f'\n📄 结果: {output}', fg='green')


def cmd_extract_emails(args):
    """提取邮件地址"""
    source = args['_pos'][0] if args.get('_pos') else ''
    dedup = args.get('unique', True)
    output = args.get('o', '')

    text = read_file_or_text(source)
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    if dedup:
        emails = list(dict.fromkeys(emails))

    echo(f'📧 找到 {len(emails)} 个邮箱:', fg='cyan')
    for email in emails:
        print(email)

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(emails))


def cmd_extract_urls(args):
    """提取 URL"""
    source = args['_pos'][0] if args.get('_pos') else ''
    dedup = args.get('unique', True)
    output = args.get('o', '')

    text = read_file_or_text(source)
    urls = re.findall(r'https?://[^\s<>"\'()]+', text)

    if dedup:
        urls = list(dict.fromkeys(urls))

    echo(f'🔗 找到 {len(urls)} 个 URL:', fg='cyan')
    for url in urls[:100]:
        print(url)

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(urls))


def cmd_wrap_text(args):
    """自动换行"""
    source = args['_pos'][0] if args.get('_pos') else ''
    width = int(args.get('width', 80))
    preserve_indent = args.get('indent', True)
    output = args.get('o', '')

    text = read_file_or_text(source)

    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:
        if not line.strip():
            wrapped_lines.append('')
            continue

        indent = ''
        if preserve_indent:
            indent_match = re.match(r'^(\s*)', line)
            indent = indent_match.group(1) if indent_match else ''
            effective_width = width - len(indent)
        else:
            effective_width = width

        content = line.lstrip()
        if len(content) <= effective_width:
            wrapped_lines.append(line)
            continue

        current = ''
        for word in content.replace('\t', '    ').split(' '):
            if not current:
                candidate = word
            else:
                candidate = current + ' ' + word
            if len(candidate) > effective_width:
                wrapped_lines.append(indent + current)
                current = word
            else:
                current = candidate
        if current:
            wrapped_lines.append(indent + current)

    result = '\n'.join(wrapped_lines)
    print(result[:5000])

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        echo(f'✅ 已写入: {output}', fg='green')


def cmd_trim_whitespace(args):
    """清理空白字符"""
    source = args['_pos'][0] if args.get('_pos') else ''
    trim_leading = args.get('leading', True)
    trim_trailing = args.get('trailing', True)
    collapse_spaces = args.get('collapse', False)
    remove_blank_lines = args.get('no_blank', False)
    output = args.get('o', '')

    text = read_file_or_text(source)
    lines = text.split('\n')

    cleaned = []
    for line in lines:
        if trim_trailing:
            line = line.rstrip()
        if trim_leading:
            line = line.lstrip() if not preserve_indent_check(line) else line
        if collapse_spaces:
            line = re.sub(r'[ \t]+', ' ', line)
        if remove_blank_lines and not line.strip():
            continue
        cleaned.append(line)

    result = '\n'.join(cleaned)
    print(result[:3000])

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        echo(f'✅ 已写入: {output}', fg='green')


def preserve_indent_check(line: str) -> bool:
    """检查是否应保留缩进（代码块等）"""
    return bool(line and (line[0].isspace() or line[0] in '#*-|>'))


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'diff': cmd_diff,
    'regex-extract': cmd_regex_extract,
    'regex-replace': cmd_regex_replace,
    'stats': cmd_stats,
    'fill-template': cmd_fill_template,
    'encode-detect': cmd_encode_detect,
    'convert-encoding': cmd_convert_encoding,
    'word-frequency': cmd_word_frequency,
    'extract-emails': cmd_extract_emails,
    'extract-urls': cmd_extract_urls,
    'wrap-text': cmd_wrap_text,
    'trim-whitespace': cmd_trim_whitespace,
    'md2html': cmd_md2html,
}

ALIASES = {
    'compare': 'diff', 'difftext': 'diff',
    'grep': 'regex-extract', 'extract': 'regex-extract',
    'replace': 'regex-replace', 'sed': 'regex-replace',
    'wc': 'stats', 'count': 'stats', 'analyze': 'stats',
    'template': 'fill-template', 'render': 'fill-template',
    'encoding': 'encode-detect', 'detect': 'encode-detect',
    'iconv': 'convert-encoding', 'convert': 'convert-encoding',
    'freq': 'word-frequency', 'word-count': 'word_frequency',
    'emails': 'extract-emails',
    'urls': 'extract-urls',
    'wrap': 'wrap-text', 'fold': 'wrap-text',
    'trim': 'trim-whitespace', 'clean': 'trim-whitespace',
    'md2html': 'md2html', 'markdown': 'md2html',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
