#!/usr/bin/env python3
"""
Semantic segmentation v2 — split transcription text into natural topic-based paragraphs.

Algorithm: Jaccard vocabulary coherence + structural signals (reference words,
logical connectors, Q&A patterns, list markers) + adaptive length thresholds.

Usage:
    python3 semantic_segment.py transcripts/*.md
    python3 semantic_segment.py transcripts/*.md --force
"""
import sys, os, re, glob, math

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


# ── Structural signal patterns ──

# Reference/continuation word sets (first words of a sentence that signal "still on same topic")
REFERENCE_WORDS = {
    '这', '那', '它', '他', '她', '它们', '他们', '她们',
    '其', '该', '此', '这个', '那个', '这些', '那些',
    '这里', '那里', '此时', '那时', '这样', '那样',
    '其实', '也就是', '也就是说', '换句话说', '换言之',
    '同样', '此外', '另外', '以及', '还有', '同时',
    '其中', '这边', '那边', '此刻', '目前', '当前',
}

# Logical connector words - sentence starts that continue a chain of reasoning
LOGICAL_CONNECTORS = {
    '但是', '然而', '不过', '可是', '却', '但',
    '所以', '因此', '于是', '因而', '从而',
    '因为', '由于', '既然',
    '如果', '假如', '假设', '若',
    '虽然', '尽管', '即使', '即便',
    '不仅', '不但', '不只',
    '而且', '并且', '甚至', '更',
    '或者说', '或者说', '或者说',
    '尤其是', '特别是',
    '比如', '例如',
    '实际上', '事实上',
    '无论如何', '不管怎样',
    '首先', '其次', '然后', '最后',
    '一方面', '另一方面',
    '第一', '第二', '第三',
    '一是', '二是', '三是',
    '一是因为', '二是因为',
}

# Strong topic-shift signals - new paragraph should almost certainly start here
TOPIC_SHIFT_SIGNALS = {
    '接下来', '我们来看', '再看', '换个角度',
    '与此同时', '与此相对', '相反',
    '回过头来', '话说回来', '不过话说回来',
    '总而言之', '总的来说', '总之',
    '说白了', '简单来说', '简单讲',
    '值得一提的是', '值得注意的是',
    '有趣的是', '讽刺的是', '巧合的是',
    '那么问题来了', '问题在于',
    '至于', '关于',
}

# Sentence-ending patterns that can break a paragraph (queryish/summary endings)
BREAK_ENDINGS = re.compile(r'[？！。…]+$')


def tokenize(text):
    """Simple Chinese-character-based tokenizer with English word preservation"""
    tokens = []
    current_word = ''
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f':
            # Chinese character
            if current_word:
                tokens.append(current_word.lower())
                current_word = ''
            tokens.append(ch)
        elif ch.isalpha():
            current_word += ch
        elif ch.isdigit():
            current_word += ch
        else:
            if current_word:
                tokens.append(current_word.lower())
                current_word = ''
            tokens.append(ch)
    if current_word:
        tokens.append(current_word.lower())
    return tokens


def jaccard_similarity(s1_tokens, s2_tokens):
    """Jaccard similarity between two token sets"""
    set1, set2 = set(s1_tokens), set(s2_tokens)
    # Filter out punctuation for more meaningful comparison
    punct = set('，。？！、；：""''（）【】《》—…·,./;:[]{}()!?')
    set1 = {t for t in set1 if t not in punct}
    set2 = {t for t in set2 if t not in punct}

    if not set1 or not set2:
        return 0.0
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union)


def is_reference_start(sentence):
    """Check if sentence starts with a reference/continuation word"""
    for word in sorted(REFERENCE_WORDS | LOGICAL_CONNECTORS, key=len, reverse=True):
        if sentence.startswith(word):
            return True
    return False


def has_topic_shift(sentence):
    """Check if sentence starts with a strong topic shift signal"""
    for signal in sorted(TOPIC_SHIFT_SIGNALS, key=len, reverse=True):
        if sentence.startswith(signal):
            return True
    return False


def split_sentences(text):
    """Split text into sentences, handling Chinese punctuations"""
    # Split on period-like breaks, but keep the punctuation
    parts = re.split(r'(?<=[。！？\n])\s*', text)
    sentences = []
    for p in parts:
        p = p.strip()
        if p:
            sentences.append(p)
    return sentences


def segment_file(input_path, force=False):
    """Apply semantic segmentation v2 to a single .md file"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has ## paragraph markers
    has_segments = bool(re.search(r'^## ', content, re.MULTILINE))
    if has_segments and not force:
        print(f'  Skip (already segmented): {os.path.basename(input_path)}')
        return

    # Split header (metadata) from body
    lines = content.split('\n')
    header_lines = []
    body_start = 0

    for i, line in enumerate(lines):
        if i == 0 and line.startswith('# '):
            header_lines.append(line)
            continue
        if line.strip().startswith('> ') and body_start == 0:
            header_lines.append(line)
            continue
        if line.strip() == '' and i <= len(header_lines):
            header_lines.append(line)
            continue
        body_start = i
        break

    body = '\n'.join(lines[body_start:]).strip()
    if not body:
        return

    # Get header prefix
    header = '\n'.join(header_lines).strip()

    sentences = split_sentences(body)

    if len(sentences) <= 3:
        # Very short - no segmentation needed
        if has_segments:
            # Still clean up any existing segmentation markers
            body = re.sub(r'^## .*\n?', '', body, flags=re.MULTILINE).strip()
        result = header + '\n\n' + body + '\n'
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'  Done (short, {len(sentences)} sentences): {os.path.basename(input_path)}')
        return

    # Build segments
    segments = []
    current_segment = [sentences[0]]
    current_tokens = tokenize(sentences[0])

    for i in range(1, len(sentences)):
        sent = sentences[i]
        sent_tokens = tokenize(sent)

        if not sent.strip():
            continue

        # Check for strong topic shift signal
        if has_topic_shift(sent):
            # Close current segment, start a new one
            segments.append(current_segment)
            current_segment = [sent]
            current_tokens = sent_tokens
            continue

        # Compute coherence with current segment
        similarity = jaccard_similarity(current_tokens, sent_tokens)

        # Check if this sentence refers back to content in current segment
        is_continuation = is_reference_start(sent)

        # Length of current segment in chars
        current_len = sum(len(s) for s in current_segment)

        # Decision logic
        should_break = False

        if similarity < 0.03 and not is_continuation and current_len > 80:
            # Very low coherence + no continuation signal + segment not too short
            should_break = True
        elif similarity < 0.01 and current_len > 150:
            # Extremely low coherence even if it's a continuation
            should_break = True
        elif current_len > 400:
            # Hard cap on segment length
            should_break = True

        # Protect Q&A patterns: don't break between Q and A
        if len(current_segment) == 1 and ('?' in current_segment[0] or '？' in current_segment[0]):
            should_break = False

        # Protect rhetorical question + answer pairs
        if current_segment and ('?' in current_segment[-1] or '？' in current_segment[-1]):
            # If the previous sentence was a question, keep it with the answer
            should_break = False

        if should_break:
            segments.append(current_segment)
            current_segment = [sent]
            current_tokens = sent_tokens
        else:
            current_segment.append(sent)
            # Update running token set (use last ~3 sentences for comparison)
            recent = ' '.join(current_segment[-3:])
            current_tokens = tokenize(recent)

    if current_segment:
        segments.append(current_segment)

    # Build output
    result = header + '\n\n'
    for i, seg in enumerate(segments, 1):
        seg_text = ''.join(seg).strip()
        if seg_text:
            if i > 1:
                result += '\n\n---\n\n'
            result += f'## 段落{i}\n\n{seg_text}'

    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(result.strip() + '\n')

    print(f'  Done ({len(segments)} segments): {os.path.basename(input_path)}')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Semantic segmentation v2')
    parser.add_argument('files', nargs='+', help='.md files to segment')
    parser.add_argument('--force', action='store_true',
                        help='Force re-segment even if already segmented')
    args = parser.parse_args()

    files = []
    for pattern in args.files:
        matched = glob.glob(pattern)
        if matched:
            files.extend(matched)
        elif os.path.isfile(pattern):
            files.append(pattern)

    if not files:
        print('No files found')
        sys.exit(1)

    print(f'Segmenting {len(files)} files...')
    for f in files:
        segment_file(f, force=args.force)

    print(f'\nDone! Processed {len(files)} files.')


if __name__ == '__main__':
    main()
