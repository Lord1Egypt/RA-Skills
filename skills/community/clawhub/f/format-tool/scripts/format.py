#!/usr/bin/env python3
"""Format Tool - Text formatting utilities."""

import argparse
import sys
import textwrap


def upper(text: str) -> str:
    return text.upper()


def lower(text: str) -> str:
    return text.lower()


def title(text: str) -> str:
    return text.title()


def capitalize(text: str) -> str:
    return text.capitalize()


def reverse(text: str) -> str:
    return text[::-1]


def sort_lines(text: str) -> str:
    lines = text.splitlines()
    lines.sort()
    return '\n'.join(lines)


def unique_lines(text: str) -> str:
    lines = text.splitlines()
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return '\n'.join(result)


def wrap_text(text: str, width: int = 80) -> str:
    return textwrap.fill(text, width)


def trim(text: str) -> str:
    return text.strip()


def remove_whitespace(text: str) -> str:
    return ''.join(text.split())


def main():
    parser = argparse.ArgumentParser(description='Text formatting tool')
    parser.add_argument('command', choices=['upper', 'lower', 'title', 'capitalize', 
                                           'reverse', 'sort', 'unique', 'wrap', 
                                           'trim', 'remove-whitespace'])
    parser.add_argument('text', nargs='?', help='Text to format (or use stdin)')
    parser.add_argument('--width', '-w', type=int, default=80, help='Wrap width')
    
    args = parser.parse_args()
    
    # Get text
    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()
    
    # Apply formatting
    if args.command == 'upper':
        result = upper(text)
    elif args.command == 'lower':
        result = lower(text)
    elif args.command == 'title':
        result = title(text)
    elif args.command == 'capitalize':
        result = capitalize(text)
    elif args.command == 'reverse':
        result = reverse(text)
    elif args.command == 'sort':
        result = sort_lines(text)
    elif args.command == 'unique':
        result = unique_lines(text)
    elif args.command == 'wrap':
        result = wrap_text(text, args.width)
    elif args.command == 'trim':
        result = trim(text)
    elif args.command == 'remove-whitespace':
        result = remove_whitespace(text)
    else:
        result = text
    
    print(result)


if __name__ == '__main__':
    main()
