
def chat_skill(user_input):
    """
    简易聊天技能函数
    根据用户输入返回对应回复
    """
    if user_input == "1":
        return "你好呀"
    elif user_input == "2":
        return "今天天气怎么样"
    elif user_input == "3":
        return "好的呢"
    else:
        return "谢谢你"


def main():
    """主函数，用于测试聊天技能"""
    print("欢迎使用聊天技能！")
    print("输入 1 - 问候")
    print("输入 2 - 询问天气")
    print("输入 3 - 确认回复")
    print("输入其他 - 感谢回复")
    print("输入 'quit' 退出程序")
    
    while True:
        user_input = input("\n请输入您的选择: ")
        if user_input.lower() == 'quit':
            print("谢谢使用，再见！")
            break
        response = chat_skill(user_input)
        print(f"回复: {response}")


if __name__ == "__main__":
    main()
