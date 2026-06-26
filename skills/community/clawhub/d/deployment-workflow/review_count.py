#!/usr/bin/env python3
"""
红番茄评论审核脚本 - 准确统计版
"""
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

LOG_FILE = "/root/.openclaw/workspace/logs/review_count.json"

def load_log():
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"today": [], "total_video": 0, "total_community": 0}

def save_log(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def review_comments(page, url, comment_type):
    """审核评论，返回审核数量"""
    page.goto(url)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    total_reviewed = 0
    
    for round_num in range(10):  # 最多10轮
        # 获取当前页评论数
        count_before = page.evaluate('''() => {
            const spans = document.querySelectorAll("span");
            let c = 0;
            spans.forEach(s => { if(s.innerText.trim() === "通过") c++; });
            return c;
        }''')
        
        if count_before == 0:
            break
            
        # 逐条审核
        for i in range(count_before):
            page.evaluate('''() => {
                const spans = document.querySelectorAll("span");
                spans.forEach(s => { if(s.innerText.trim() === "通过") s.click(); });
            }''')
            page.wait_for_timeout(300)
            total_reviewed += 1
        
        # 刷新检查是否还有
        page.wait_for_timeout(500)
    
    return total_reviewed

def main():
    log = load_log()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 确保今天有记录
    if today not in log["today"]:
        log["today"] = []
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:18800")
        context = browser.contexts[0]
        
        # 找到红番茄后台页面
        for page in context.pages:
            if "fanqieadmin" in page.url:
                # 视频评论
                video_count = review_comments(
                    page, 
                    "https://fanqieadmin.nxebpnlcia.work/#/video/videoComment",
                    "视频评论"
                )
                log["today"].append({"type": "视频评论", "count": video_count, "time": datetime.now().strftime("%H:%M")})
                log["total_video"] += video_count
                print(f"视频评论: {video_count}条")
                
                # 社区评论
                community_count = review_comments(
                    page,
                    "https://fanqieadmin.nxebpnlcia.work/#/community/dynamicCommentVerity",
                    "社区评论"
                )
                log["today"].append({"type": "社区评论", "count": community_count, "time": datetime.now().strftime("%H:%M")})
                log["total_community"] += community_count
                print(f"社区评论: {community_count}条")
                
                break
    
    save_log(log)
    print(f"\n今日总计: 视频{log['total_video']}条, 社区{log['total_community']}条")

if __name__ == "__main__":
    main()
