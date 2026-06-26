#!/usr/bin/env python3
"""
Password Generator - Generate secure passwords and passphrases
"""

import argparse
import os
import random
import string
import sys


# Word list for passphrases
PASSWORDS_WORDS = [
    'apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest', 'garden', 'harbor',
    'island', 'jungle', 'kitchen', 'lemon', 'mountain', 'nature', 'ocean', 'planet',
    'quantum', 'river', 'sunset', 'thunder', 'umbrella', 'violet', 'whisper', 'xylophone',
    'yellow', 'zebra', 'anchor', 'breeze', 'castle', 'diamond', 'ember', 'falcon',
    'glacier', 'horizon', 'ivory', 'jasper', 'kingdom', 'lantern', 'marble', 'nebula',
    'orchid', 'phoenix', 'quartz', 'rainbow', 'silver', 'tiger', 'universe', 'velvet',
    'winter', 'crystal', 'dawn', 'echo', 'flame', 'gravity', 'haven', 'inferno',
    'jupiter', 'kraken', 'lunar', 'mirage', 'nova', 'orbit', 'prism', 'quest',
    'rift', 'storm', 'twilight', 'ultra', 'vortex', 'wave', 'xenon', 'yonder',
    'zenith', 'aurora', 'blaze', 'cloud', 'dream', 'eclipse', 'frost', 'glory',
    'haven', 'inferno', 'joy', 'kindle', 'light', 'magic', 'night', 'oasis',
    'peace', 'quiet', 'radiant', 'spark', 'treasure', 'unity', 'vivid', 'wild',
    'xerox', 'youth', 'zeal'
]


def generate_password(length=16, use_numbers=True, use_symbols=True, 
                     use_uppercase=True, exclude=''):
    """Generate a random password."""
    chars = string.ascii_lowercase
    
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    # Remove excluded characters
    for c in exclude:
        chars = chars.replace(c, '')
    
    # Use secure random
    password = ''.join(random.choice(chars) for _ in range(length))
    return password


def generate_pin(length=4):
    """Generate a random PIN."""
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_passphrase(word_count=4, separator='-'):
    """Generate a memorable passphrase."""
    words = random.sample(PASSWORDS_WORDS, word_count)
    # Optionally capitalize first letter of each word
    # words = [w.capitalize() for w in words]
    return separator.join(words)


def main():
    parser = argparse.ArgumentParser(description='Password Generator')
    parser.add_argument('--length', type=int, default=16, help='Password length')
    parser.add_argument('--numbers', action='store_true', help='Include numbers')
    parser.add_argument('--symbols', action='store_true', help='Include special symbols')
    parser.add_argument('--uppercase', action='store_true', help='Include uppercase letters')
    parser.add_argument('--exclude', default='', help='Characters to exclude')
    parser.add_argument('--pin', action='store_true', help='Generate PIN')
    parser.add_argument('--pin-length', type=int, default=4, help='PIN length')
    parser.add_argument('--passphrase', action='store_true', help='Generate passphrase')
    parser.add_argument('--words', type=int, default=4, help='Words in passphrase')
    parser.add_argument('--separator', default='-', help='Passphrase separator')
    parser.add_argument('--count', type=int, default=1, help='Number of passwords to generate')
    
    args = parser.parse_args()
    
    # PIN mode
    if args.pin:
        for i in range(args.count):
            print(generate_pin(args.pin_length))
        return 0
    
    # Passphrase mode
    if args.passphrase:
        for i in range(args.count):
            print(generate_passphrase(args.words, args.separator))
        return 0
    
    # Password mode
    for i in range(args.count):
        password = generate_password(
            args.length,
            args.numbers,
            args.symbols,
            args.uppercase,
            args.exclude
        )
        print(password)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
