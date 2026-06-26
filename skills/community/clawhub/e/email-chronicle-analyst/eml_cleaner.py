#!/usr/bin/env python3
"""eml_cleaner.py - 预处理 .eml 文件，提取干净文本"""

import sys
import email
from email import policy
from email.parser import BytesParser

def extract_clean_text(eml_path, output_path=None):
    """从 .eml 提取纯文本内容"""
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    lines = []
    lines.append(f"【发件人】{msg.get('From', '未知')}")
    lines.append(f"【收件人】{msg.get('To', '未知')}")
    lines.append(f"【日期】{msg.get('Date', '未知')}")
    lines.append(f"【主题】{msg.get('Subject', '未知')}")
    lines.append("=" * 40)

    text_count = 0
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    text = part.get_payload(decode=True).decode(charset, errors='replace')
                    lines.append("--- plain text ---")
                    lines.append(text.strip())
                    text_count += 1
                except Exception:
                    pass
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            try:
                charset = msg.get_content_charset() or 'utf-8'
                text = msg.get_payload(decode=True).decode(charset, errors='replace')
                lines.append("--- plain text ---")
                lines.append(text.strip())
                text_count += 1
            except Exception:
                pass

    if text_count == 0:
        lines.append("(无可提纯的纯文本内容)")

    result = "\n".join(lines)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)

    print(f"[INFO] 共找到 {text_count} 段 text/plain 内容")
    print(f"[INFO] 输出长度: {len(result)} 字符")
    if output_path:
        print(f"✅ 已保存到: {output_path}")
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 eml_cleaner.py <eml文件> [输出文件]")
        sys.exit(1)
    extract_clean_text(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
