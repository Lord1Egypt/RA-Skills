#!/usr/bin/env python3
"""
携程笔记自动发布助手
功能：生成可复制的 JavaScript 代码来自动填写内容
"""

def generate_fill_script(title, content, destination=""):
    """生成填写脚本"""
    
    # 转义内容
    title_js = title.replace('"', '\\"').replace("\n", "\\n")
    content_js = content.replace('"', '\\"').replace("\n", "\\n")
    dest_js = destination.replace('"', '\\"')
    
    script = f'''
// 携程笔记自动填写脚本
// 使用方法：在 Chrome 控制台粘贴此代码并回车

(function() {{
    console.log("开始填写携程笔记...");
    
    // 填写标题
    const titleInput = document.querySelector('input[placeholder*="标题"]') || 
                       document.querySelector('input[maxlength]') ||
                       document.querySelector('input[type="text"]');
    if (titleInput) {{
        titleInput.value = "{title_js}";
        titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        titleInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log("✅ 标题已填写");
    }} else {{
        console.log("❌ 未找到标题输入框");
    }}
    
    // 填写正文
    setTimeout(() => {{
        const editor = document.querySelector('[contenteditable="true"]') ||
                       document.querySelector('.editor') ||
                       document.querySelector('textarea');
        if (editor) {{
            editor.innerHTML = "{content_js}";
            editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
            console.log("✅ 正文已填写");
        }} else {{
            console.log("❌ 未找到编辑器");
        }}
    }}, 500);
    
    // 填写目的地
    setTimeout(() => {{
        const destInput = document.querySelector('input[placeholder*="目的地"]') ||
                          document.querySelector('.destination-input');
        if (destInput) {{
            destInput.value = "{dest_js}";
            destInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            console.log("✅ 目的地已填写");
        }}
    }}, 1000);
    
    console.log("🎉 填写完成！请检查内容并上传图片");
}})();
'''
    return script

def main():
    # 北京游内容
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
    
    # 生成脚本
    script = generate_fill_script(title, content, destination)
    
    # 保存到文件
    output_path = os.path.expanduser("~/.qclaw/workspace/ctrip_fill_script.js")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("=" * 60)
    print("🚀 携程笔记自动填写脚本已生成")
    print("=" * 60)
    print("\n📋 使用方法：")
    print("1. 确保已在 Chrome 中打开携程发布页面并登录")
    print("2. 按 F12 打开开发者工具")
    print("3. 切换到 Console（控制台）标签")
    print("4. 复制下面的代码并粘贴，然后回车")
    print("\n" + "=" * 60)
    print(script)
    print("=" * 60)
    print(f"\n💾 脚本已保存到: {output_path}")
    print("\n✅ 执行后会自动填写标题、正文和目的地")
    print("📸 然后你只需上传图片并点击发布即可")

if __name__ == "__main__":
    import os
    main()