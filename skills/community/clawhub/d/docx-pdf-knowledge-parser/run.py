#!/usr/bin/env python3
import argparse
import json
import os
import random
import string
from datetime import datetime, timezone
from pathlib import Path

from parsers.parse_docx import extract_docx_text
from parsers.parse_pdf import extract_pdf_text


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def make_batch_id() -> str:
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f'ingest-{stamp}-{suffix}'


def summarize_text(text: str, max_len: int = 220) -> str:
    clean = ' '.join(text.split())
    return clean[:max_len] + ('...' if len(clean) > max_len else '')


def detect_content_type(name: str) -> str:
    n = name.lower()
    if '制度' in name or '规定' in name or '管理' in name:
        return '制度'
    if '手册' in name or '说明' in name or '操作' in name or 'sop' in n:
        return '流程'
    return '其他'


def process_file(path: Path, batch_id: str):
    ext = path.suffix.lower()
    if ext == '.docx':
        text = extract_docx_text(path)
        file_type = 'docx'
    elif ext == '.pdf':
        text = extract_pdf_text(path)
        file_type = 'pdf'
    else:
        raise ValueError(f'unsupported extension: {ext}')

    if not text.strip():
        raise ValueError('empty extracted text')

    return {
        'batch_id': batch_id,
        'source_file': path.name,
        'source_token': '',
        'file_type': file_type,
        'topic': path.stem,
        'content_type': detect_content_type(path.name),
        'summary': summarize_text(text),
        'extracted_at': utc_now(),
        'confidence': 0.8,
    }


def write_jsonl(path: Path, rows):
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def write_report(output_dir: Path, batch_id: str, started_at: str, finished_at: str, source_dir: str, successes, failures):
    report = output_dir / 'ingest-report.md'
    with report.open('w', encoding='utf-8') as f:
        f.write(f'# Ingest Report\n\n')
        f.write(f'- batch_id: {batch_id}\n')
        f.write(f'- started_at: {started_at}\n')
        f.write(f'- finished_at: {finished_at}\n')
        f.write(f'- input_scope: {source_dir}\n')
        f.write(f'- success_count: {len(successes)}\n')
        f.write(f'- failed_count: {len(failures)}\n\n')
        f.write('## Successful extraction summary\n')
        for row in successes:
            f.write(f"- {row['source_file']}: {row['summary']}\n")
        f.write('\n## Failures and risks\n')
        for row in failures:
            f.write(f"- {row['source_file']}: {row['failure_reason']} ({row['error_detail']})\n")

    mem = output_dir / 'MEMORY.candidate.md'
    with mem.open('w', encoding='utf-8') as f:
        f.write('# MEMORY Candidate\n\n')
        f.write(f'- batch_id: {batch_id}\n')
        f.write(f'- started_at: {started_at}\n')
        f.write(f'- finished_at: {finished_at}\n')
        f.write(f'- source_directory: {source_dir}\n\n')
        f.write('## Candidate summaries\n')
        for row in successes:
            f.write(f"### {row['source_file']}\n")
            f.write(f"- topic: {row['topic']}\n")
            f.write(f"- content_type: {row['content_type']}\n")
            f.write(f"- summary: {row['summary']}\n")
            f.write(f"- confidence: {row['confidence']}\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    batch_id = make_batch_id()
    started_at = utc_now()
    successes = []
    failures = []

    for path in sorted(input_dir.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {'.docx', '.pdf'}:
            failures.append({
                'batch_id': batch_id,
                'source_file': path.name,
                'source_token': '',
                'file_type': path.suffix.lower().lstrip('.'),
                'failure_reason': 'out_of_scope',
                'error_detail': 'v0.1 only supports .docx and .pdf',
                'suggested_action': 'skip now or add parser in a later version',
                'failed_at': utc_now(),
            })
            continue
        try:
            successes.append(process_file(path, batch_id))
        except Exception as e:
            failures.append({
                'batch_id': batch_id,
                'source_file': path.name,
                'source_token': '',
                'file_type': path.suffix.lower().lstrip('.'),
                'failure_reason': 'parse_error',
                'error_detail': str(e),
                'suggested_action': 'retry parsing or inspect the file manually',
                'failed_at': utc_now(),
            })

    write_jsonl(output_dir / 'kb-items.jsonl', successes)
    write_jsonl(output_dir / 'failed-items.jsonl', failures)
    finished_at = utc_now()
    write_report(output_dir, batch_id, started_at, finished_at, str(input_dir), successes, failures)
    print(json.dumps({
        'batch_id': batch_id,
        'success_count': len(successes),
        'failed_count': len(failures),
        'output_dir': str(output_dir),
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
