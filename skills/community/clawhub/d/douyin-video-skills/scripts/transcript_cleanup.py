#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def extract_body(md_text: str) -> str:
    marker = '## 文案内容'
    if marker in md_text:
        return md_text.split(marker, 1)[1].strip()
    return md_text.strip()


def normalize_text(text: str) -> str:
    text = text.replace('🎼', '').strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('。。', '。').replace('，，', '，')
    return text


def sentence_cleanup(text: str) -> str:
    replacements = [
        ('学学飞行原理', '学飞行原理'),
        ('靠挫力', '抗挫力'),
        ('一个能力', '能力'),
        ('在问题中成长，在挑战中去突破', '在问题中成长，在挑战中突破'),
        ('应用等技能拓展', '应用等技能拓展'),
        ('我要不要告诉他呢', '要不要告诉他呢'),
        ('都能学学', '都能学'),
        ('医生有保护圈', '机身有保护圈'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    # 常见断句修正
    text = text.replace('第一呢', '第一，')
    text = text.replace('第二，能够', '第二，能够')
    text = text.replace('第三，培养', '第三，培养')
    text = text.replace('第四，打开', '第四，打开')
    text = re.sub(r'([。！？])(?=[^\n])', r'\1\n', text)
    return text.strip()


def build_fixes(title: str, raw: str, clean: str) -> str:
    fixes = []
    if '学学飞行原理' in raw and '学飞行原理' in clean:
        fixes.append(('- 学学飞行原理', '+ 学飞行原理', '重复词，结合上下文修正', '高'))
    if '靠挫力' in raw and '抗挫力' in clean:
        fixes.append(('- 靠挫力', '+ 抗挫力', '高概率同音误识别，结合常见教育表达修正', '高'))
    if '一个能力' in raw and '能力' in clean:
        fixes.append(('- 建立系统化解决问题的一个能力', '+ 建立系统化解决问题的能力', '语序更自然，语义不变', '中'))
    if '我要不要告诉他呢' in raw and '要不要告诉他呢' in clean:
        fixes.append(('- 我要不要告诉他呢', '+ 要不要告诉他呢', '去除疑似冗余口语重复', '中'))
    if '医生有保护圈' in raw and '机身有保护圈' in clean:
        fixes.append(('- 医生有保护圈', '+ 机身有保护圈', '结合标题语境与无人机常识，判断为高概率同音误识别', '高'))

    lines = [f'# 文案修正说明', '', f'- 标题：{title}', '']
    if not fixes:
        lines += ['- 本次未发现高置信明显错误，或仅做了轻度标点整理。', '', '## 待确认', '- 无']
        return '\n'.join(lines)

    lines += ['## 已修正项']
    for old, new, reason, conf in fixes:
        lines += [old, new, f'  - 依据：{reason}', f'  - 置信度：{conf}', '']
    lines += ['## 待确认', '- 如原视频存在角色对白或反问句，开头口语句仍建议人工复核。']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', required=True)
    parser.add_argument('--raw', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    raw_path = Path(args.raw)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    raw_md = raw_path.read_text(encoding='utf-8')
    raw_body = normalize_text(extract_body(raw_md))
    clean_body = sentence_cleanup(raw_body)
    fixes_md = build_fixes(args.title, raw_body, clean_body)

    raw_out = outdir / 'transcript-raw.md'
    clean_out = outdir / 'transcript-clean.md'
    fixes_out = outdir / 'transcript-fixes.md'

    raw_out.write_text(f'# 原始转写稿\n\n- 标题：{args.title}\n\n## 文案内容\n\n{raw_body}\n', encoding='utf-8')
    clean_out.write_text(f'# 修正版文案\n\n- 标题：{args.title}\n\n## 文案内容\n\n{clean_body}\n', encoding='utf-8')
    fixes_out.write_text(fixes_md + '\n', encoding='utf-8')

    print(str(raw_out))
    print(str(clean_out))
    print(str(fixes_out))


if __name__ == '__main__':
    main()
