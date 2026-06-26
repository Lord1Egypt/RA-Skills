#!/usr/bin/env python3
"""66天班主任成长助手 - CLI入口"""
import json, sys, os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMMANDS = {
    "status": "显示当前在66天路线图中的位置",
    "day": "查看某一天的成长内容：66days day <数字>",
    "case": "按主题查找案例：66days case <关键词>（支持：家长/情绪/课堂/纪律/ERT/共情）",
    "check": "自我评估问卷",
    "plan": "生成特定场景的行动方案：66days plan <场景>（支持：第一次家长会/第一次班会/问题学生/情绪崩溃）",
    "help": "显示所有命令帮助"
}

def cmd_help():
    print("📋 66天班主任成长助手 - 可用命令")
    print("="*40)
    for name, desc in COMMANDS.items():
        print(f"  {name:10s}  {desc}")
    print()
    print("示例: 66days day 1 | 66days case 家长 | 66days plan 第一次家长会")

def cmd_status():
    print("📊 66天路线图总览")
    print("="*40)
    print("阶段1 (Day 1-10): 建立关系")
    print("  Day 1-3: 观察班级生态")
    print("  Day 4-7: 逐个认识学生")
    print("  Day 8-10: 建立初步信任")
    print()
    print("阶段2 (Day 11-25): 立规矩")
    print("  Day 11-15: 制定班级公约")
    print("  Day 16-20: 执行与反馈")
    print("  Day 21-25: 适应与调整")
    print()
    print("阶段3 (Day 26-40): 教学与沟通")
    print("  Day 26-30: 家长分类沟通策略")
    print("  Day 31-35: 学生圈层语言")
    print("  Day 36-40: 情绪管理")
    print()
    print("阶段4 (Day 41-55): 深化与突破")
    print("  Day 41-45: ERT框架实践")
    print("  Day 46-50: 问题学生转化")
    print("  Day 51-55: 班级文化建设")
    print()
    print("阶段5 (Day 56-66): 收尾与复盘")
    print("  Day 56-60: 中期评估")
    print("  Day 61-66: 形成自己的方法")
    print()
    print("使用 66days day <数字> 查看具体内容")

def cmd_day(day_str):
    try:
        day = int(day_str)
    except:
        print(f"❌ 请输入数字，如: 66days day 1")
        return
    if day < 1 or day > 66:
        print(f"❌ 有效范围: 1-66")
        return
    
    days_data = {
        1: ("建立关系", "今天目标：不着急立规矩，先记住全班每个学生的名字。进教室前深呼吸三次。"),
        2: ("建立关系", "今天目标：课间找一个学生闲聊，不谈学习，只聊ta最近在做什么。"),
        3: ("建立关系", "今天目标：观察班级里最安静和最活跃的两个学生，记录他们的行为模式。"),
        4: ("建立关系", "今天目标：给三个学生各写一句具体的表扬（不是'表现不错'，而是'你今天回答那个问题时思路很清晰'）。"),
        5: ("建立关系", "今天目标：找一位搭班老师了解班级情况，获取第三方视角。"),
    }
    
    if day in days_data:
        phase, content = days_data[day]
        print(f"📅 第{day}天 · {phase}")
        print("="*40)
        print(content)
    else:
        phase_map = {1:"建立关系", 2:"立规矩", 3:"教学与沟通", 4:"深化与突破", 5:"收尾与复盘"}
        phase = phase_map.get((day-1)//13 + 1, "成长中")
        print(f"📅 第{day}天 · {phase}")
        print("="*40)
        print(f"详细内容请参考 SKILL.md 或运行 66days status 查看路线图总览。")

def cmd_case(topic):
    cases = {
        "家长": "**案例：焦虑型家长**\n家长每次沟通时称呼15岁的孩子为'小朋友'——光是这个称呼就判断出关注点在日常状态而非学业。调整策略：先讲情绪和日常，再谈学习。\n\n**心法**：不是每个家长都用同一种方式沟通。先观察，再开口。",
        "情绪": "**案例：一天崩溃三次的学生**\n早自习后、午休后、下课后——同一个学生三次找到你。第三次时你已经快要尖叫了，但脸上不能有一丝不耐烦。第二天主动追上去问：'今天感觉怎么样？'\n学生说：'老师，我今天一整天都很开心。'\n**心法**：你可以崩溃，但不能让学生有负罪感。",
        "课堂": "**案例：原神648**\n学生算错题答案是648，Estelle笑着问：'怎么，着急拿钱去充原神648是吧？'全班都笑了。\n讲侧面描写时用《进击的巨人》——学生听得入迷。\n**心法**：了解学生的圈层，是教学基本功。",
        "共情": "学生不接受你之前，规矩没有意义。但共情不是为了做朋友——你的接近是有目的性的。",
        "ERT": "ERT框架：环境(Environment)→关系(Relationship)→转变(Transformation)，顺序不能乱。\n转化环：关系建立信任→信任让惩罚变成教育→教育需要成功支点→成功支点来自阳性事件的发现和放大。",
        "纪律": "先共情，再立规矩。学生不接受你之前，规矩没有意义。"
    }
    for key, content in cases.items():
        if key in topic:
            print(f"🔍 找到案例：{key}")
            print("="*40)
            print(content)
            return
    print(f"❌ 没有找到关于'{topic}'的案例。试试：家长、情绪、课堂、共情、ERT、纪律")

def cmd_check():
    print("📝 班主任能力自评")
    print("="*40)
    print("请如实回答以下问题（是/否）：")
    questions = [
        "你能叫出全班每个学生的名字吗？",
        "你知道每个学生的大致家庭情况吗？",
        "你上周和每位家长都沟通过一次吗？",
        "你用过学生圈子的语言上课吗？",
        "你有情绪失控后向学生发火的经历吗？",
        "你知道班级里谁和谁关系好、谁被孤立吗？",
        "你有一个明确的班级管理框架吗？",
        "你上周找到过一个学生的'阳性事件'（做得好的事）并表扬了吗？"
    ]
    print()
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    print()
    print("回答完毕后，对比Estelle的方法看看差距。")

def cmd_plan(scene):
    plans = {
        "第一次家长会": "**家长会方案框架**\n1. 开场：介绍班级理念（3分钟）\n2. 学科情况：各科老师发言（10分钟）\n3. 学生表现：不点名批评，只说共性问题（5分钟）\n4. 家长交流：预留家长提问时间（10分钟）\n5. 个别沟通：会后留下需要单独聊的家长\n\n**话术建议**：'我不是来告状的，是来和您一起帮孩子变得更好的。'",
        "第一次班会": "**班会方案框架**\n1. 自我介绍：让学生知道你是谁（3分钟）\n2. 班级愿景：'我们想成为一个什么样的班级'（5分钟）\n3. 共同约定：让学生参与制定规则（10分钟）\n4. 破冰活动：让同学互相认识（10分钟）\n5. 总结：'从今天开始，我们是彼此的人了。'",
        "问题学生": "**问题学生转化流程**\n第一步（E）：看清学生的环境——家庭、朋友圈、课堂位置\n第二步（R）：建立信任关系——找到共同话题，先做朋友再当老师\n第三步（T）：创造成功体验——给学生一个新角色、新标签、新任务\n第四步：持续跟进——至少跟踪2周，每天给一次正面反馈",
        "情绪崩溃": "**当情绪来临时**\n1. 先深呼吸3次，数到10再开口\n2. 区分'学生的问题'和'我的问题'\n3. 如果实在撑不住：'老师现在需要冷静一下，5分钟后我们再谈。'\n4. 第二天主动追上去问：'今天感觉怎么样？'\n\n**记住**：一个不稳定的人，知道该怎么做也做不好。"
    }
    for key, content in plans.items():
        if key in scene:
            print(f"📋 方案：{key}")
            print("="*40)
            print(content)
            return
    print(f"❌ 没有找到'{scene}'的方案。试试：第一次家长会、第一次班会、问题学生、情绪崩溃")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "--help", "-h"):
        cmd_help()
        return
    
    cmd = sys.argv[1]
    if cmd == "status":
        cmd_status()
    elif cmd == "day":
        cmd_day(sys.argv[2] if len(sys.argv) > 2 else "")
    elif cmd == "case":
        cmd_case(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "")
    elif cmd == "check":
        cmd_check()
    elif cmd == "plan":
        cmd_plan(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "")
    else:
        cmd_help()

if __name__ == "__main__":
    main()
