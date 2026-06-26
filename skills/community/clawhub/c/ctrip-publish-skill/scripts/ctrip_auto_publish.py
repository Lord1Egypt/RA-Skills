#!/usr/bin/env python3
"""
携程笔记全自动发布脚本 - 使用用户默认浏览器
功能：控制用户已打开的 Chrome 浏览器，自动填写内容
"""

import os
import sys
import time
import subprocess
from pathlib import Path

class CtripAutoPublisher:
    """携程自动发布器 - 使用 AppleScript 控制用户浏览器"""
    
    def __init__(self):
        self.title = ""
        self.content = ""
        self.destination = ""
        
    def check_chrome_running(self):
        """检查 Chrome 是否运行"""
        result = subprocess.run(
            ['pgrep', '-x', 'Google Chrome'],
            capture_output=True
        )
        return result.returncode == 0
        
    def open_chrome(self):
        """打开 Chrome 浏览器"""
        print("🌐 正在打开 Chrome...")
        subprocess.Popen(['open', '-a', 'Google Chrome'])
        time.sleep(3)
        
    def ensure_chrome_window(self):
        """确保 Chrome 有窗口"""
        # 检查是否有窗口
        script = '''
        tell application "Google Chrome"
            if (count of windows) = 0 then
                make new window
            end if
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(2)
        
    def navigate_to_publish_page(self):
        """导航到发布页面"""
        script = '''
        tell application "Google Chrome"
            activate
            if (count of windows) = 0 then
                make new window
            end if
            tell active tab of first window
                set URL to "https://we.ctrip.com/publish/publishPictureText"
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ 导航警告: {result.stderr}")
        print("🚀 已导航到携程发布页面")
        time.sleep(5)
        
    def execute_javascript(self, js_code):
        """在 Chrome 中执行 JavaScript"""
        # 将 JS 代码转义
        escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        
        script = f'''
        tell application "Google Chrome"
            tell active tab of first window
                execute javascript "{escaped_js}"
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return result.stdout.strip()
        
    def fill_title(self, title):
        """填写标题"""
        print(f"📝 填写标题...")
        
        js = f'''
        (function() {{
            let inputs = document.querySelectorAll('input');
            let titleInput = null;
            
            for (let input of inputs) {{
                if (input.placeholder && input.placeholder.includes('标题')) {{
                    titleInput = input;
                    break;
                }}
            }}
            
            if (!titleInput) {{
                for (let input of inputs) {{
                    let maxLen = input.getAttribute('maxlength');
                    if (maxLen && parseInt(maxLen) > 20 && parseInt(maxLen) < 100) {{
                        titleInput = input;
                        break;
                    }}
                }}
            }}
            
            if (!titleInput) {{
                for (let input of inputs) {{
                    if (input.type === 'text' && input.offsetParent !== null) {{
                        titleInput = input;
                        break;
                    }}
                }}
            }}
            
            if (titleInput) {{
                titleInput.value = "{title}";
                titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                titleInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return 'OK:标题已填写';
            }}
            
            return 'FAIL:未找到标题输入框';
        }})();
        '''
        
        result = self.execute_javascript(js)
        print(f"   {result}")
        return 'OK' in result
        
    def fill_content(self, content):
        """填写正文"""
        print("📝 填写正文...")
        
        content_escaped = content.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')
        
        js = f'''
        (function() {{
            let editor = document.querySelector('[contenteditable="true"]');
            
            if (!editor) {{
                let textareas = document.querySelectorAll('textarea');
                for (let ta of textareas) {{
                    if (ta.offsetParent !== null) {{
                        editor = ta;
                        break;
                    }}
                }}
            }}
            
            if (!editor) {{
                editor = document.querySelector('.editor-content') || 
                         document.querySelector('.rich-text-editor') ||
                         document.querySelector('[role="textbox"]');
            }}
            
            if (editor) {{
                if (editor.innerHTML !== undefined) {{
                    editor.innerHTML = "{content_escaped}";
                }} else {{
                    editor.value = "{content_escaped}";
                }}
                
                editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                editor.dispatchEvent(new Event('change', {{ bubbles: true }}));
                
                return 'OK:正文已填写';
            }}
            
            return 'FAIL:未找到编辑器';
        }})();
        '''
        
        result = self.execute_javascript(js)
        print(f"   {result}")
        return 'OK' in result
        
    def select_destination(self, destination):
        """选择目的地"""
        print(f"📍 选择目的地...")
        
        js = f'''
        (function() {{
            let inputs = document.querySelectorAll('input');
            let destInput = null;
            
            for (let input of inputs) {{
                if (input.placeholder && (input.placeholder.includes('目的地') || input.placeholder.includes('位置'))) {{
                    destInput = input;
                    break;
                }}
            }}
            
            if (destInput) {{
                destInput.value = "{destination}";
                destInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return 'OK:目的地已填写';
            }}
            
            return 'SKIP:未找到目的地输入框';
        }})();
        '''
        
        result = self.execute_javascript(js)
        print(f"   {result}")
        
    def click_publish(self):
        """点击发布按钮"""
        print("🚀 点击发布...")
        
        js = '''
        (function() {
            let buttons = document.querySelectorAll('button');
            let publishBtn = null;
            
            for (let btn of buttons) {
                let text = btn.textContent || btn.innerText;
                if (text && (text.includes('发布') || text.includes('提交'))) {
                    publishBtn = btn;
                    break;
                }
            }
            
            if (publishBtn) {
                publishBtn.click();
                return 'OK:已点击发布';
            }
            
            return 'FAIL:未找到发布按钮';
        })();
        '''
        
        result = self.execute_javascript(js)
        print(f"   {result}")
        return 'OK' in result
        
    def publish(self, title, content, destination=""):
        """全自动发布笔记"""
        print("=" * 60)
        print("🚀 携程笔记全自动发布")
        print("=" * 60)
        
        # 1. 检查 Chrome
        if not self.check_chrome_running():
            print("⚠️ Chrome 未运行，正在打开...")
            self.open_chrome()
        else:
            print("✅ Chrome 已在运行")
            
        # 2. 确保有窗口
        self.ensure_chrome_window()
        
        # 3. 导航到发布页面
        self.navigate_to_publish_page()
        
        # 4. 填写内容
        print("\n📝 开始填写内容...")
        self.fill_title(title)
        time.sleep(1)
        
        self.fill_content(content)
        time.sleep(1)
        
        if destination:
            self.select_destination(destination)
            time.sleep(1)
            
        # 5. 完成
        print("\n" + "=" * 60)
        print("✅ 内容已自动填写到携程发布页面！")
        print("=" * 60)
        print("\n📋 接下来请手动操作：")
        print("   1. 检查标题和正文是否正确")
        print("   2. 上传 9-12 张图片")
        print("   3. 点击发布按钮")
        print("\n🎉 脚本执行完成！")
        
        return True

def main():
    """主函数"""
    publisher = CtripAutoPublisher()
    
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
"不到长城非好汉"｜门票：40元
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
    
    publisher.publish(title, content, destination)

if __name__ == "__main__":
    main()