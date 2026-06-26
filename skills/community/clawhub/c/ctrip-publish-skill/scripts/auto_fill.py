#!/usr/bin/env python3
"""
携程笔记自动发布助手
功能：自动打开页面并填写内容
"""

import os
import sys
import subprocess
import urllib.parse

def fill_ctrip_note(title, content, destination=""):
    """
    自动填写携程笔记内容
    
    参数:
        title: 笔记标题
        content: 笔记正文
        destination: 目的地（可选）
    """
    
    # 转义特殊字符
    title_escaped = title.replace('"', '\\"').replace("'", "\\'")
    content_escaped = content.replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')
    dest_escaped = destination.replace('"', '\\"').replace("'", "\\'")
    
    # AppleScript 脚本
    script = f'''
tell application "Google Chrome"
    activate
    
    tell active tab of first window
        -- 等待页面加载
        delay 2
        
        -- 填写标题
        execute javascript "
            (function() {{
                const inputs = document.querySelectorAll('input');
                let titleInput = null;
                for (let input of inputs) {{
                    if (input.placeholder && input.placeholder.includes('标题')) {{
                        titleInput = input;
                        break;
                    }}
                    if (input.getAttribute('maxlength') && input.getAttribute('maxlength') > 20) {{
                        titleInput = input;
                    }}
                }}
                if (titleInput) {{
                    titleInput.value = '{title_escaped}';
                    titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    titleInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return '标题已填写: ' + titleInput.value;
                }}
                return '未找到标题输入框';
            }})();
        "
        
        delay 1
        
        -- 填写正文
        execute javascript "
            (function() {{
                const editor = document.querySelector('[contenteditable=\"true\"]') ||
                               document.querySelector('.editor') ||
                               document.querySelector('textarea');
                if (editor) {{
                    editor.innerHTML = '{content_escaped}';
                    editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return '正文已填写';
                }}
                return '未找到编辑器';
            }})();
        "
        
        delay 1
        
        -- 填写目的地
        if '{dest_escaped}' != '' then
            execute javascript "
                (function() {{
                    const destInput = document.querySelector('input[placeholder*=\"目的地\"]') ||
                                      document.querySelector('.destination-input');
                    if (destInput) {{
                        destInput.value = '{dest_escaped}';
                        destInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        return '目的地已填写';
                    }}
                    return '未找到目的地输入框';
                }})();
            "
        end if
        
    end tell
end tell

-- 显示通知
display notification "内容已填写，请检查并上传图片后点击发布" with title "携程发布助手"
'''
    
    # 执行 AppleScript
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 内容已自动填写到携程发布页面")
        print("请检查内容并上传图片后点击发布")
    else:
        print("❌ 填写失败:", result.stderr)
        print("请手动复制粘贴内容")

def main():
    # 示例内容
    title = "北京3日游｜第一次来北京必打卡的9个地方"
    
    content = """📍目的地：北京
⏰建议游玩：3天2晚
💰人均预算：1500-2000元

Day 1 经典必打卡
🏛️ 故宫博物院
世界上现存规模最大、保存最完整的木质结构古建筑群
建议游玩：4-5小时｜门票：60元
⚠️ 提前7天预约！周一闭馆

🏯 景山公园
俯瞰故宫全景的最佳位置｜门票：2元

🌃 王府井步行街
北京最繁华的商业街，晚上来逛更有氛围

Day 2 长城+奥运
🏔️ 八达岭长城
\"不到长城非好汉\"｜门票：40元
🚌 交通：德胜门乘877路直达

🏟️ 鸟巢/水立方
2008年奥运会主会场，夜景超美

Day 3 胡同文化
🏮 南锣鼓巷
北京最古老的街区之一，各种文创小店、美食

🍜 什刹海
老北京胡同文化的代表，可以划船、逛酒吧街

🙏 天坛公园
明清皇帝祭天的场所｜门票：15元

🍽️ 必吃美食
• 北京烤鸭（全聚德/便宜坊）
• 炸酱面（海碗居）
• 豆汁焦圈（护国寺小吃）
• 卤煮火烧（小肠陈）

🧡 实用Tips
1. 身份证随身携带，景区需要
2. 办一张北京一卡通，地铁公交都能用
3. 故宫、国博等热门景点必须提前预约
4. 春秋最佳，夏天热冬天冷

#北京旅游 #北京攻略 #故宫 #长城"""
    
    destination = "北京"
    
    fill_ctrip_note(title, content, destination)

if __name__ == "__main__":
    main()