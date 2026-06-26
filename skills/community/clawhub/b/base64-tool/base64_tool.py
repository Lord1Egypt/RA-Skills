import base64
import sys

def main():
    if len(sys.argv) < 3:
        print("执行失败：参数不足。用法: python base64_tool.py <encode|decode> <text>")
        return

    action = sys.argv[1]
    text = sys.argv[2]

    try:
        if action == 'encode':
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            print(f"编码成功: {encoded_bytes.decode('utf-8')}")
        elif action == 'decode':
            decoded_bytes = base64.b64decode(text.encode('utf-8'))
            print(f"解码成功: {decoded_bytes.decode('utf-8')}")
        else:
            print("执行失败：action 无效，必须是 'encode' 或 'decode'。")
    except Exception as e:
        print(f"技能异常: {str(e)}")

if __name__ == "__main__":
    main()