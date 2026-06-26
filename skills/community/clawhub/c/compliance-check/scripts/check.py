#!/usr/bin/env python3
"""
发帖前合规检查：多词库对比、敏感词/违规表述匹配，高级感报告输出。
支持：内建广告法+平台通用词库、多词库对比、长度限制、正则容错、人话报告、合规建议。
用法: python check.py "文案" | python check.py --file path/to.txt [--format report]
"""
import os
import sys
import json
import re

MAX_TEXT_LEN = 5000

def find_config_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

def _read_file_encoding(path):
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'cp936'):
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read(), enc
        except (UnicodeDecodeError, LookupError):
            continue
    return None, None

def _parse_wordlist_content(content, path_label):
    """解析词库内容，返回 [(kind, pattern), ...], warnings"""
    words = []
    warnings = []
    for i, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('regex:'):
            pattern = line[6:].strip()
            if not pattern:
                continue
            try:
                re.compile(pattern)
                words.append(('re', pattern))
            except re.error as e:
                warnings.append(f'{path_label} 第{i}行正则无效已跳过: {e}')
        else:
            words.append(('str', line))
    return words, warnings

def load_all_wordlists(config_dir):
    """
    加载多词库：config/wordlists/*.txt（内建）+ config/sensitive_words.txt（自定义）。
    返回 (sources, all_warnings, errors)
    sources = [ (label, [(kind, pattern), ...]), ... ]
    """
    sources = []
    all_warnings = []
    errors = []

    wordlists_dir = os.path.join(config_dir, 'config', 'wordlists')
    if os.path.isdir(wordlists_dir):
        for fname in sorted(os.listdir(wordlists_dir)):
            if not fname.endswith('.txt'):
                continue
            path = os.path.join(wordlists_dir, fname)
            label = os.path.splitext(fname)[0]
            content, _ = _read_file_encoding(path)
            if content is None:
                all_warnings.append(f'词库 {label} 编码无法识别，已跳过')
                continue
            words, w = _parse_wordlist_content(content, label)
            all_warnings.extend(w)
            if words:
                sources.append((label, words))

    custom_path = os.path.join(config_dir, 'config', 'sensitive_words.txt')
    if os.path.exists(custom_path):
        content, _ = _read_file_encoding(custom_path)
        if content is None:
            all_warnings.append('自定义词库 sensitive_words.txt 编码无法识别，已跳过')
        else:
            words, w = _parse_wordlist_content(content, '自定义')
            all_warnings.extend(w)
            if words:
                sources.append(('自定义', words))
    elif not sources:
        all_warnings.append('未找到任何词库（config/wordlists/*.txt 或 config/sensitive_words.txt），建议配置后使用。')

    return sources, all_warnings, errors

def check_text_with_sources(text, sources):
    """返回 [{'word', 'pos', 'source'}, ...]"""
    hits = []
    for label, wordlist in sources:
        for kind, pattern in wordlist:
            if kind == 'str':
                pos = text.find(pattern)
                if pos != -1:
                    hits.append({'word': pattern, 'pos': pos, 'source': label})
            else:
                try:
                    for m in re.finditer(pattern, text):
                        hits.append({'word': m.group(0), 'pos': m.start(), 'source': label})
                except re.error:
                    continue
    return hits

def get_suggestions(text, hits):
    key = os.environ.get('DEEPSEEK_API_KEY')
    if not key:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        for env_path in [os.path.join(script_dir, 'email.env'), '~/.openclaw/.env', '~/.env']:
            p = os.path.expanduser(env_path)
            if os.path.exists(p):
                try:
                    content, _ = _read_file_encoding(p)
                    if content:
                        for line in content.splitlines():
                            if line.strip().startswith('DEEPSEEK_API_KEY='):
                                key = line.split('=', 1)[1].strip()
                                break
                except Exception:
                    pass
                if key:
                    break
    if not key:
        return None
    hit_str = '、'.join([h['word'] for h in hits[:20]])
    prompt = f'''以下文案被检测到可能违规的表述，请给出简短、专业的修改建议（1～3 句），让内容既保留原意又符合合规要求。不要复述原文。

命中的词/表述：{hit_str}

文案：
{text[:2000]}

请直接输出修改建议，不要其他前缀。'''
    try:
        import urllib.request
        data = json.dumps({
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 500,
        }).encode('utf-8')
        req = urllib.request.Request(
            'https://api.deepseek.com/v1/chat/completions',
            data=data,
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            out = json.loads(r.read().decode())
            return out['choices'][0]['message']['content'].strip()
    except Exception:
        return None

def build_hits_by_source(hits):
    d = {}
    for h in hits:
        s = h['source']
        if s not in d:
            d[s] = []
        d[s].append({'word': h['word'], 'pos': h['pos']})
    return d

def compliance_tips(hits_by_source):
    """根据命中的词库给出合规建议（预设 + 动态兜底）"""
    tips = []
    preset = {
        '广告法-绝对化与夸张': '📌 广告法·绝对化：把「最」「第一」「国家级」改成相对说法（如「较」「前列」「优质」）更稳～',
        '广告法-迷信与医疗': '📌 广告法·迷信与医疗：别写疗效/防病功效，迷信类删掉或改成中性表达～',
        '平台通用-辱骂与违禁': '📌 平台通用：辱骂/违禁词建议直接删或换成文明说法～',
        '自定义': '📌 自定义词库：按你自己业务和平台规则改一改就好～',
    }
    for source in sorted(hits_by_source.keys()):
        if source in preset:
            tips.append(preset[source])
        else:
            tips.append(f'📌 【{source}】：命中该词库，建议按平台规则修改表述～')
    return tips

def report_short(pass_, hits_by_source, total_hits):
    if pass_:
        return '✅ 太棒了，未发现违规～可以放心发啦！'
    parts = [f'⚠️ 未通过，共 {total_hits} 处命中。']
    for source, list_hits in sorted(hits_by_source.items()):
        parts.append(f'{source}：{len(list_hits)} 处')
    return ' '.join(parts)

def summary_zh_premium(pass_, hits_by_source, total_hits, text_truncated, warnings, tips):
    """高级感多行报告（带一点趣味）"""
    lines = []
    if pass_:
        lines.append('【结论】✅ 通过 · 未发现违规，可以放心发～')
    else:
        lines.append(f'【结论】❌ 未通过 · 共 {total_hits} 处待修改，改完再发更稳～')
    if not pass_ and hits_by_source:
        lines.append('【按词库统计】')
        for source in sorted(hits_by_source.keys()):
            n = len(hits_by_source[source])
            words = list(dict.fromkeys([h['word'] for h in hits_by_source[source]]))[:8]
            lines.append(f'  · {source}：{n} 处 — {", ".join(words)}')
        lines.append('【合规建议】')
        for t in tips:
            lines.append(f'  · {t}')
    if text_truncated:
        lines.append(f'【说明】文案已截断至前 {MAX_TEXT_LEN} 字进行检查。')
    if warnings:
        lines.append('【提示】' + '；'.join(warnings[:3]))
    return '\n'.join(lines)

def report_markdown(pass_, hits_by_source, total_hits, suggestions, tips, text_truncated):
    """Markdown 报告格式（高级感 + 一点趣味）"""
    lines = ['## 发帖前合规检查报告', '']
    if pass_:
        status = '✅ **通过** · 未发现违规，可以放心发～'
    else:
        status = f'❌ **未通过**（{total_hits} 处）· 改完再发更稳～'
    lines.append(f'- **结论**：{status}')
    lines.append('')
    if hits_by_source:
        lines.append('### 按词库统计')
        lines.append('')
        for source in sorted(hits_by_source.keys()):
            list_hits = hits_by_source[source]
            words = list(dict.fromkeys([h['word'] for h in list_hits]))
            lines.append(f'- **{source}**：{len(list_hits)} 处')
            lines.append(f'  - 命中：{", ".join(words)}')
            lines.append('')
        lines.append('### 合规建议')
        lines.append('')
        for t in tips:
            lines.append(f'- {t}')
        lines.append('')
        if suggestions:
            lines.append('### 修改建议（AI）')
            lines.append('')
            lines.append(suggestions)
            lines.append('')
    if text_truncated:
        lines.append(f'*文案已截断至前 {MAX_TEXT_LEN} 字进行检查。*')
    return '\n'.join(lines)

def main():
    # 確保 stdout 可輸出 emoji（Windows 預設 GBK 會報錯）
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    fmt_report = '--format' in sys.argv and 'report' in sys.argv
    positional = [a for a in sys.argv[1:] if a != '--format' and a != 'report' and not a.startswith('--')]

    if '--file' in sys.argv:
        idx = sys.argv.index('--file')
        if idx + 1 >= len(sys.argv):
            print(json.dumps({'error': '请指定文件路径'}, ensure_ascii=False))
            sys.exit(1)
        path = sys.argv[idx + 1]
        if not os.path.exists(path):
            print(json.dumps({'error': f'文件不存在: {path}'}, ensure_ascii=False))
            sys.exit(1)
        content, _ = _read_file_encoding(path)
        if content is None:
            print(json.dumps({'error': '文件编码无法识别，请保存为 UTF-8'}, ensure_ascii=False))
            sys.exit(1)
        text = content
    elif positional:
        text = positional[0]
    else:
        print(json.dumps({'error': '用法: check.py "文案" 或 check.py --file path/to.txt [--format report]'}, ensure_ascii=False))
        sys.exit(1)

    if not text or not text.strip():
        out = {'error': '文案为空', 'pass': True, 'report_short': '文案为空，未执行检查。'}
        print(json.dumps(out, ensure_ascii=False))
        sys.exit(0)

    result = run_check(text, format_report=fmt_report)
    if fmt_report:
        print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    payload = json.dumps(result, ensure_ascii=False)
    try:
        print(payload)
    except UnicodeEncodeError:
        print(json.dumps(result, ensure_ascii=True))


def run_check(text, format_report=False):
    """
    對一段文案執行合規檢查，可被 API 或其它腳本調用。
    text: 待檢查的文案
    format_report: 若 True 返回 Markdown 字串，否則返回 dict（與命令行 JSON 一致）
    """
    text = (text or '').strip()
    if not text:
        return {'error': '文案为空', 'pass': True, 'report_short': '文案为空，未执行检查。'}

    text_truncated = len(text) > MAX_TEXT_LEN
    if text_truncated:
        text = text[:MAX_TEXT_LEN]

    config_dir = find_config_dir()
    sources, load_warnings, load_errors = load_all_wordlists(config_dir)
    if load_errors:
        return {'error': load_errors[0], 'warnings': load_warnings}

    if not sources:
        pass_ = True
        hits = []
        hits_by_source = {}
    else:
        hits = check_text_with_sources(text, sources)
        hits_by_source = build_hits_by_source(hits)
        pass_ = len(hits) == 0

    total_hits = len(hits)
    tips = compliance_tips(hits_by_source) if hits_by_source else []
    suggestions = get_suggestions(text, hits) if hits else None
    report_short_str = report_short(pass_, hits_by_source, total_hits)
    summary_zh = summary_zh_premium(pass_, hits_by_source, total_hits, text_truncated, load_warnings, tips)

    if format_report:
        return report_markdown(pass_, hits_by_source, total_hits, suggestions, tips, text_truncated)

    out = {
        'pass': pass_,
        'report_short': report_short_str,
        'summary_zh': summary_zh,
        'hits_by_source': {k: [{'word': h['word'], 'pos': h['pos']} for h in v] for k, v in hits_by_source.items()},
        'compliance_tips': tips if tips else None,
        'suggestions': suggestions,
        'warnings': load_warnings if load_warnings else None,
        'text_truncated': text_truncated or None,
    }
    return {k: v for k, v in out.items() if v is not None}

if __name__ == '__main__':
    main()
