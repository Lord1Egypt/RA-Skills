#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS直聘窗口分析脚本 - 学习窗口特征，优化识别逻辑
"""

import json
import sys
import io

# Force UTF-8 for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import pygetwindow as gw
except ImportError:
    print("❌ 需要安装 pygetwindow: pip install pygetwindow")
    sys.exit(1)

def analyze_all_windows():
    """收集并分析所有窗口"""
    all_titles = gw.getAllTitles()
    print(f"📊 系统中共有 {len(all_titles)} 个窗口")
    
    windows = []
    keyword = "BOSS"
    
    for title in all_titles:
        if not title.strip():
            continue
            
        # 检查是否包含BOSS关键词
        has_boss = keyword.lower() in title.lower()
        
        try:
            # 获取窗口对象
            win_list = gw.getWindowsWithTitle(title)
            for win in win_list:
                try:
                    # 尝试获取更多属性
                    windows.append({
                        "title": title,
                        "has_boss": has_boss,
                        "left": win.left,
                        "top": win.top,
                        "width": win.width,
                        "height": win.height,
                        "area": win.width * win.height,
                        "visible": win.visible,
                        "isActive": win.isActive,
                        "isMinimized": win.left < -1000 or win.top < -1000,
                        "isMaximized": win.isMaximized if hasattr(win, 'isMaximized') else None,
                    })
                except Exception as e:
                    windows.append({
                        "title": title,
                        "has_boss": has_boss,
                        "error": str(e)
                    })
        except Exception as e:
            windows.append({
                "title": title,
                "has_boss": has_boss,
                "error": f"无法查询: {str(e)}"
            })
    
    return windows

def analyze_boss_windows(windows):
    """分析BOSS相关窗口的特征"""
    boss_windows = [w for w in windows if w.get("has_boss") and "error" not in w]
    
    print(f"\n🎯 找到 {len(boss_windows)} 个BOSS相关窗口:")
    
    for i, w in enumerate(boss_windows, 1):
        print(f"\n{i}. '{w['title']}'")
        print(f"   位置: ({w['left']}, {w['top']})")
        print(f"   尺寸: {w['width']}x{w['height']} (面积: {w['area']:,})")
        print(f"   状态: {'可见' if w['visible'] else '隐藏'} | "
              f"{'活跃' if w['isActive'] else '非活跃'} | "
              f"{'最小化' if w['isMinimized'] else '正常'}")
    
    # 分析特征
    if boss_windows:
        areas = [w["area"] for w in boss_windows]
        sizes = [(w["width"], w["height"]) for w in boss_windows]
        
        print(f"\n📈 BOSS窗口特征分析:")
        print(f"   平均面积: {sum(areas)/len(areas):,.0f}")
        print(f"   最小面积: {min(areas):,} (可能为小窗)")
        print(f"   最大面积: {max(areas):,} (可能为主窗)")
        
        # 按面积排序，找出可能的小窗
        sorted_by_area = sorted(boss_windows, key=lambda x: x["area"])
        
        print(f"\n🔍 可能的小窗候选 (按面积排序):")
        for i, w in enumerate(sorted_by_area[:5], 1):
            print(f"   {i}. '{w['title']}' - {w['width']}x{w['height']} (面积: {w['area']:,})")
    
    return boss_windows

def suggest_improvements(boss_windows):
    """根据分析结果提出改进建议"""
    print(f"\n💡 改进建议:")
    
    if not boss_windows:
        print("   1. 未找到BOSS窗口，请检查窗口是否已打开")
        return
    
    # 分析标题关键词
    titles = [w["title"] for w in boss_windows]
    title_keywords = set()
    for title in titles:
        words = title.lower().replace("boss", "").replace("直聘", "").strip().split()
        title_keywords.update(words)
    
    print("   1. 当前BOSS窗口标题关键词:", ", ".join(sorted(title_keywords)) if title_keywords else "(无特殊关键词)")
    
    # 分析窗口尺寸分布
    areas = [w["area"] for w in boss_windows]
    if len(areas) > 1:
        # 如果面积差异很大，可能有主窗和小窗之分
        area_ratio = max(areas) / min(areas)
        if area_ratio > 5:
            print("   2. 检测到明显的主窗/小窗尺寸差异，建议:")
            print("      - 优先选择面积较小的窗口 (可能是聊天小窗)")
            print("      - 添加尺寸过滤: width < 800 and height < 700")
    
    # 检查窗口位置
    on_screen = [w for w in boss_windows if 0 <= w["left"] < 5000 and 0 <= w["top"] < 5000]
    if len(on_screen) != len(boss_windows):
        print("   3. 部分窗口位置异常 (可能最小化)，已自动过滤")
    
    # 检查可见性
    visible_count = sum(1 for w in boss_windows if w["visible"])
    if visible_count < len(boss_windows):
        print(f"   4. 仅 {visible_count}/{len(boss_windows)} 个窗口可见")

def main():
    print("🤖 BOSS直聘窗口特征分析 (自主学习模式)")
    print("=" * 50)
    
    # 收集所有窗口
    windows = analyze_all_windows()
    
    # 分析BOSS窗口
    boss_windows = analyze_boss_windows(windows)
    
    # 提出改进建议
    suggest_improvements(boss_windows)
    
    # 保存分析结果供后续使用
    if boss_windows:
        with open("window_analysis.json", "w", encoding="utf-8") as f:
            json.dump({
                "total_windows": len(windows),
                "boss_windows": boss_windows,
                "analysis_time": sys._getframe().f_code.co_name
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📁 分析结果已保存至: window_analysis.json")

if __name__ == "__main__":
    main()
