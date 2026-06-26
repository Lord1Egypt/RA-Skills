"""
坐标记录工具 - 点击按钮自动记录相对坐标
使用方法：
1. 运行脚本
2. 点击BOSS直聘窗口内的目标按钮
3. 脚本会自动记录相对坐标
"""

import pyautogui
import pygetwindow as gw
import time

def find_boss_window():
    """查找BOSS直聘窗口"""
    windows = gw.getWindowsWithTitle("BOSS直聘")
    return windows[0] if windows else None

def record_coordinate(window, button_name):
    """记录按钮相对坐标"""
    print(f"\n请点击BOSS直聘窗口内的 '{button_name}' 按钮...")
    print("（3秒后开始捕获点击）")
    time.sleep(3)
    
    # 等待鼠标点击
    while True:
        if pyautogui.mouseDown():
            # 获取鼠标绝对坐标
            abs_x, abs_y = pyautogui.position()
            
            # 计算相对坐标
            rel_x = abs_x - window.left
            rel_y = abs_y - window.top
            
            print(f"✅ 记录成功！")
            print(f"绝对坐标：({abs_x}, {abs_y})")
            print(f"相对坐标：({rel_x}, {rel_y})")
            return (rel_x, rel_y)
        time.sleep(0.1)

if __name__ == "__main__":
    window = find_boss_window()
    if not window:
        print("❌ 未找到BOSS直聘窗口")
        exit()
    
    print("=== BOSS直聘坐标记录工具 ===")
    print(f"当前窗口：{window.title}")
    print(f"窗口位置：({window.left}, {window.top})")
    print(f"窗口大小：{window.width}x{window.height}")
    
    # 需要记录的按钮列表
    buttons = [
        "数据看板",
        "互动",
        "收藏牛人",
        "对我感兴趣",
        "推荐"
    ]
    
    # 记录坐标
    coordinates = {}
    for button in buttons:
        coord = record_coordinate(window, button)
        coordinates[button] = coord
    
    # 保存到配置文件
    with open("button_coordinates.json", "w", encoding="utf-8") as f:
        import json
        json.dump(coordinates, f, ensure_ascii=False, indent=2)
    
    print("\n🎉 所有坐标已保存到 button_coordinates.json")
    print("\n坐标列表：")
    for button, coord in coordinates.items():
        print(f"{button}: {coord}")
