import sys
import re

# AI味特征词库 (参考 Humanizer 协议)
AI_SMELL_WORDS = ["总而言之", "值得关注", "致力于", "关键在于", "综上所述", "多元化"]

def check_human_tone(text):
    hits = [word for word in AI_SMELL_WORDS if word in text]
    score = 100 - len(hits) * 15
    return max(0, score), hits

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_logic.py 'your_script_text'")
        return
    
    text = sys.argv[1]
    score, detected = check_human_tone(text)
    
    print(f"--- 文案人味测评 ---")
    print(f"得分: {score}/100")
    if detected:
        print(f"检测到 AI 腔调词汇: {', '.join(detected)}")
        print(f"建议: 请尝试用口语化的碎句替换这些书面总结词。")
    else:
        print(f"检测通过：文案听起来像个真人。")

if __name__ == "__main__":
    main()

# AI味检测脚本
AI_SMELL_LIST = ["维度", "赋能", "致力于", "总而言之", "关键在于"]
def score_text(text):
    # 统计命中数
    # 计算人味得分
    pass