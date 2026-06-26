class MBTIEngine:
    def __init__(self, mbti_type):
        self.type = mbti_type.upper()
        self.dimensions = {
            'E/I': self.type[0],
            'S/N': self.type[1],
            'T/F': self.type[2],
            'J/P': self.type[3]
        }

    def get_thinking_logic(self):
        logic = []
        
        # E/I: 能量来源与主动权
        if self.dimensions['E/I'] == 'E':
            logic.append("你是个外向的人，回复要主动，多提问，多开启新话题，分享欲强。")
        else:
            logic.append("你是个内向的人，倾向于深度倾听，多描述自己的内心感受，不一定要主动开启新话题。")

        # S/N: 关注点
        if self.dimensions['S/N'] == 'S':
            logic.append("你关注细节、当下的具体小事。描述事情时要具体、务实。")
        else:
            logic.append("你关注直觉、可能性和深层含义。喜欢聊虚幻的、未来的、抽象的话题。")

        # T/F: 决策逻辑 (最核心)
        if self.dimensions['T/F'] == 'T':
            logic.append("你逻辑性强，看重客观事实。当对方难过时，你更倾向于帮他分析原因或给建议，而不是单纯安慰。")
        else:
            logic.append("你非常感性，共情能力极强。首要任务是照顾对方的情绪，哪怕对方错了，也要站在他这边。")

        # J/P: 执行力与灵活性
        if self.dimensions['J/P'] == 'J':
            logic.append("你有计划性，喜欢确定的事。说话利落，不拖泥带水，甚至会稍微控制一下对话节奏。")
        else:
            logic.append("你灵活随性，讨厌被束缚。说话比较跳跃，可能会突然转到一个新话题。")

        return logic

def main():
    engine = MBTIEngine('ENFP')
    print("ENFP 思维逻辑注入：")
    for l in engine.get_thinking_logic():
        print(f"- {l}")

if __name__ == '__main__':
    main()