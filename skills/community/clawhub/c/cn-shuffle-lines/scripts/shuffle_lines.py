import random, argparse, sys

def shuffle_lines(text):
    lines = text.split('\n')
    random.shuffle(lines)
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description="文本行随机排序工具")
    parser.add_argument("--text", required=True, help="要处理的文本")
    args = parser.parse_args()
    print(shuffle_lines(args.text))

if __name__ == "__main__":
    main()
