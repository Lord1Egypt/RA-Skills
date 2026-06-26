#!/usr/bin/env python3
"""ASCII Art Tool - Text to ASCII art."""

import argparse


# Simple ASCII art fonts
FONTS = {
    'standard': {
        'A': ['  A  ', ' A A ', 'AAAAA', 'A   A', 'A   A'],
        'B': ['BBBB ', 'B   B', 'BBBB ', 'B   B', 'BBBB '],
        'C': [' CCC ', 'C    ', 'C    ', 'C    ', ' CCC '],
        'D': ['DDD  ', 'D  D ', 'D   D', 'D  D ', 'DDD  '],
        'E': ['EEEEE', 'E    ', 'EEE  ', 'E    ', 'EEEEE'],
        'F': ['FFFFF', 'F    ', 'FFF  ', 'F    ', 'F    '],
        'G': [' GGG ', 'G    ', 'G  GG', 'G   G', ' GGG '],
        'H': ['H   H', 'H   H', 'HHHHH', 'H   H', 'H   H'],
        'I': ['IIIII', '  I  ', '  I  ', '  I  ', 'IIIII'],
        'J': ['JJJJJ', '   J ', '   J ', 'J  J ', ' JJ  '],
        'K': ['K   K', 'K  K ', 'KKK  ', 'K  K ', 'K   K'],
        'L': ['L    ', 'L    ', 'L    ', 'L    ', 'LLLLL'],
        'M': ['M   M', 'MM MM', 'M M M', 'M   M', 'M   M'],
        'N': ['N   N', 'NN  N', 'N N N', 'N  NN', 'N   N'],
        'O': [' OOO ', 'O   O', 'O   O', 'O   O', ' OOO '],
        'P': ['PPPP ', 'P   P', 'PPPP ', 'P    ', 'P    '],
        'Q': [' QQQ ', 'Q   Q', 'Q Q Q', 'Q  Q ', ' QQ Q'],
        'R': ['RRRR ', 'R   R', 'RRRR ', 'R  R ', 'R   R'],
        'S': [' SSS ', 'S    ', ' SSS ', '    S', ' SSS '],
        'T': ['TTTTT', '  T  ', '  T  ', '  T  ', '  T  '],
        'U': ['U   U', 'U   U', 'U   U', 'U   U', ' UUU '],
        'V': ['V   V', 'V   V', 'V   V', ' V V ', '  V  '],
        'W': ['W   W', 'W   W', 'W W W', 'WW WW', 'W   W'],
        'X': ['X   X', ' X X ', '  X  ', ' X X ', 'X   X'],
        'Y': ['Y   Y', ' Y Y ', '  Y  ', '  Y  ', '  Y  '],
        'Z': ['ZZZZZ', '   Z ', '  Z  ', ' Z   ', 'ZZZZZ'],
        '0': ['0000 ', '0   0', '0   0', '0   0', '0000 '],
        '1': ['  1  ', ' 11  ', '  1  ', '  1  ', '11111'],
        '2': ['2222 ', '    2', '2222 ', '2    ', '22222'],
        '3': ['3333 ', '    3', ' 333 ', '    3', '3333 '],
        '4': ['4   4', '4   4', '44444', '    4', '    4'],
        '5': ['55555', '5    ', '5555 ', '    5', '5555 '],
        '6': [' 666 ', '6    ', '6666 ', '6   6', ' 666 '],
        '7': ['77777', '    7', '   7 ', '  7  ', '  7  '],
        '8': [' 888 ', '8   8', ' 888 ', '8   8', ' 888 '],
        '9': [' 999 ', '9   9', ' 9999', '    9', ' 999 '],
        ' ': ['     ', '     ', '     ', '     ', '     '],
    },
    'big': {
        'A': ['   A   ', '  A A  ', ' A   A ', 'AAAAAAA', 'A     A', 'A     A'],
        'B': ['BBBB   ', 'B   B  ', 'BBBB   ', 'B   B  ', 'B   B  ', 'BBBB   '],
        'C': [' CCCCC ', 'C      ', 'C      ', 'C      ', 'C      ', ' CCCCC '],
        # Add more as needed
    }
}


def get_char(char: str, font: str = 'standard') -> list:
    """Get ASCII art for character."""
    char = char.upper()
    if font in FONTS and char in FONTS[font]:
        return FONTS[font][char]
    elif char in FONTS['standard']:
        return FONTS['standard'][char]
    else:
        return ['  ', '  ', '  ', '  ', '  ']


def text_to_ascii(text: str, font: str = 'standard') -> str:
    """Convert text to ASCII art."""
    lines = []
    
    # Get max height for any character
    max_height = 5
    if font == 'big':
        max_height = 6
    
    for line_idx in range(max_height):
        line = ''
        for char in text:
            char_lines = get_char(char, font)
            if line_idx < len(char_lines):
                line += char_lines[line_idx] + ' '
            else:
                line += ' ' * len(char_lines[0]) + ' '
        lines.append(line)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='ASCII art generator')
    parser.add_argument('text', help='Text to convert')
    parser.add_argument('-f', '--font', default='standard', help='Font style')
    parser.add_argument('-w', '--width', type=int, help='Output width')
    
    args = parser.parse_args()
    
    result = text_to_ascii(args.text, args.font)
    print(result)


if __name__ == '__main__':
    main()
