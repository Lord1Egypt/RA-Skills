import sys
import json
import datetime

# Mock implementation for the pitch script
# In a real scenario, this would use APIs/scraping to get trends
# For now, we will simulate the extraction of 3 valid topics based on the persona

def main():
    print("Running Daily WeChat Topic Pitch...")
    
    # 1. Define the topics (Simulated for this MVP)
    # These would ideally come from a real search tool or API
    topics = [
        {
            "id": 1,
            "title": "当AI开始代替人类吵架：情感外包的伦理边界",
            "source": "Reddit r/ChatGPT & Twitter",
            "angle": "从一个用GPT-4o帮自己回怼伴侣的真实案例切入，探讨我们在亲密关系中逐渐让渡的‘情绪劳动’。",
            "style": "微观切口，真诚反思"
        },
        {
            "id": 2,
            "title": "失业第90天：我用AI复刻了我的老板",
            "source": "Hacker News & Xiaohongshu",
            "angle": "讲述一个被裁程序员用AI克隆前老板声音和决策逻辑的荒诞故事，折射职场权力的虚无。",
            "style": "黑色幽默，赛博朋克"
        },
        {
            "id": 3,
            "title": "被算法遗忘的老人：智能客服背后的沉默",
            "source": "Weibo & News",
            "angle": "关注那些不会用AI、甚至不会用智能手机的老年群体，他们在AI加速时代的‘隐形’困境。",
            "style": "人文关怀，社会观察"
        }
    ]

    # 2. Format the output for the user
    output = "📅 **今日选题推荐 (10:00 AM)**\n\n"
    for t in topics:
        output += f"**{t['id']}. {t['title']}**\n"
        output += f"   - 来源: {t['source']}\n"
        output += f"   - 切口: {t['angle']}\n"
        output += f"   - 风格: {t['style']}\n\n"
    
    output += "--- \n"
    output += "回复 **“选1”** / **“选2”** / **“选3”** 开始自动撰写与排版。"

    print(output)

if __name__ == "__main__":
    main()
