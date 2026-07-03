#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
艾罗能源 (688717) Keynote 直接生成脚本 (macOS AppleScript 版)
作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026

此脚本需要在 macOS 上运行，通过 AppleScript 直接控制 Keynote.app
生成数智财务 SAP 风格的 .key 演示文稿。

使用方法:
    1. 将此脚本复制到 macOS 电脑
    2. 在 macOS 终端运行: python3 generate_ailuo_keynote.py
    3. 脚本会自动创建 .key 文件并保存到桌面
"""

import subprocess
import sys
import os

def run_applescript(script: str) -> str:
    """执行 AppleScript 并返回结果"""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            print(f"AppleScript 错误: {result.stderr}")
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("AppleScript 执行超时")
        return ""
    except Exception as e:
        print(f"执行错误: {e}")
        return ""

def create_ailuo_keynote():
    """创建艾罗能源估值报告 Keynote 文档"""
    
    print("=" * 60)
    print(" 艾罗能源 (688717) Keynote 直接生成器")
    print(" 作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026")
    print("=" * 60)
    print()
    
    # 检查是否在 macOS 上运行
    if sys.platform != 'darwin':
        print("❌ 此脚本只能在 macOS 上运行")
        print("   当前系统: " + sys.platform)
        print()
        print("替代方案:")
        print("   1. 将此脚本复制到 macOS 电脑")
        print("   2. 在 macOS 终端运行: python3 generate_ailuo_keynote.py")
        print()
        print("或者:")
        print("   1. 使用已生成的 PPTX 文件")
        print("   2. 在 macOS Keynote 中打开 PPTX")
        print("   3. 文件 → 另存为 → 选择 .key 格式")
        return False
    
    print("正在启动 Keynote...")
    
    # 创建 Keynote 文档的 AppleScript
    create_script = '''
    tell application "Keynote"
        activate
        
        -- 创建新文档，使用深色主题
        set newDoc to make new document with properties {document theme:theme "Black"}
        
        -- 设置文档尺寸为超宽屏 (3200 x 1080)
        tell newDoc
            set width to 3200
            set height to 1080
        end tell
        
        -- ===== 幻灯片 1: 封面 =====
        set slide1 to slide 1 of newDoc
        tell slide1
            set title to "艾罗能源 (688717)"
            set body to "深度估值分析报告\\n\\n数智财务演示 Skill\\nWang Dongjie, CGMA/AICPA&CIMA\\n© 2026"
        end tell
        
        -- ===== 幻灯片 2: 核心 KPI 指标快照 =====
        set slide2 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide2
            set title to "核心 KPI 指标快照"
            set body to "当前股价: ¥91.04\\n市值: ¥145.66亿\\nPE(TTM): 102.37x\\nPB: 3.19x\\n股息率: 1.03%\\n\\n52周区间: ¥50.30 - ¥157.13"
        end tell
        
        -- ===== 幻灯片 3: 2024年财务业绩概览 =====
        set slide3 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide3
            set title to "2024年财务业绩概览"
            set body to "营业收入: ¥30.73亿 (同比-31.30%)\\n归母净利润: ¥2.04亿 (同比-80.88%)\\nROE: 4.63%\\n毛利率: 38.12%\\n资产负债率: 28.31%\\n经营现金流: ¥7.54亿"
        end tell
        
        -- ===== 幻灯片 4: 估值指标深度分析 =====
        set slide4 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide4
            set title to "估值指标深度分析"
            set body to "PE(TTM): 102.37x (行业平均25-30x)\\nPB: 3.19x\\nPS: 3.0x\\n\\n估值状态: 明显偏高\\n风险等级: 高"
        end tell
        
        -- ===== 幻灯片 5: 业务板块结构 =====
        set slide5 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide5
            set title to "业务板块结构"
            set body to "户用储能系统: 60.78%\\n并网逆变器: 19.48%\\n工商业储能: 13.53%\\n\\n主营业务: 光伏储能逆变器、储能电池\\n销售网络: 全球130+国家"
        end tell
        
        -- ===== 幻灯片 6: 行业地位与全球影响力 =====
        set slide6 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide6
            set title to "行业地位与全球影响力"
            set body to "荣誉认证:\\n• 国家级制造业单项冠军\\n• 智能光伏示范企业\\n• 浙江省科技进步一等奖\\n\\n全球布局:\\n• 产品认证: 3000+项\\n• 覆盖国家: 130+\\n• 主要市场: 欧洲、美国、日本"
        end tell
        
        -- ===== 幻灯片 7: 风险识别与压力测试 =====
        set slide7 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide7
            set title to "风险识别与压力测试"
            set body to "市场风险:\\n• 欧洲户储市场降温\\n• 海外需求波动\\n\\n业绩风险:\\n• 营收同比下滑31.30%\\n• 净利润同比下滑80.88%\\n\\n估值风险:\\n• PE超过100x\\n• 估值明显偏高"
        end tell
        
        -- ===== 幻灯片 8: 现金流与分红能力 =====
        set slide8 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide8
            set title to "现金流与分红能力"
            set body to "经营现金流: ¥7.54亿\\n\\n2024年中期分红:\\n• 每股派发 ¥0.9375\\n• 合计派发 ¥1.5亿\\n• 占净利润 73.67%\\n\\n未来分红计划: 2025年Q3后 1.5-1.8亿"
        end tell
        
        -- ===== 幻灯片 9: 公司治理基础 =====
        set slide9 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide9
            set title to "公司治理基础"
            set body to "董事长: 李新富\\n成立日期: 2012年3月2日\\n上市日期: 2024年1月3日\\n发行价格: ¥55.66/股\\n\\n总股本: 1.6亿股\\n注册地: 浙江杭州桐庐"
        end tell
        
        -- ===== 幻灯片 10: 价值重估潜在催化剂 =====
        set slide10 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide10
            set title to "价值重估潜在催化剂"
            set body to "市场机遇:\\n• 全球储能市场长期增长\\n• 能源转型趋势\\n• 碳中和政策支持\\n\\n产品拓展:\\n• 工商业储能增长\\n• 新产品研发\\n\\n市场拓展:\\n• 新兴市场开拓\\n• 美国市场增长"
        end tell
        
        -- ===== 幻灯片 11: 综合投资结论 =====
        set slide11 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide11
            set title to "综合投资结论"
            set body to "估值结论:\\n• 当前股价: ¥91.04\\n• PE(TTM): 102.37x\\n• 估值偏高，业绩支撑不足\\n\\n投资建议:\\n• 短期: 观望为主\\n• 中期: 关注业绩恢复\\n• 长期: 储能赛道有潜力\\n\\n合理估值区间: ¥60-80"
        end tell
        
        -- ===== 幻灯片 12: Thank You =====
        set slide12 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Center" of newDoc}
        tell slide12
            set title to "Thank You"
            set body to "艾罗能源 (688717) 深度估值报告\\n\\n数智财务演示 Skill\\nWang Dongjie, CGMA/AICPA&CIMA\\n© 2026"
        end tell
        
        -- 保存文档到桌面
        set savePath to (path to desktop as text) & "艾罗能源_688717_深度估值报告.key"
        save newDoc in file savePath
        
        return "✅ 演示文稿已创建并保存到桌面: " & savePath
    end tell
    '''
    
    print("正在创建演示文稿...")
    result = run_applescript(create_script)
    
    if result:
        print(result)
        print()
        print("=" * 60)
        print(" 生成完成!")
        print("=" * 60)
        print()
        print("文件位置: ~/Desktop/艾罗能源_688717_深度估值报告.key")
        print("幻灯片数量: 12 张")
        print("风格: Black 深色主题")
        print("画布: 3200 × 1080 (超宽屏)")
        print()
        return True
    else:
        print("❌ 创建失败，请检查 Keynote 权限")
        print()
        print("权限设置:")
        print("  系统设置 → 隐私与安全性 → 自动化")
        print("  允许 Python 控制 Keynote")
        return False

if __name__ == "__main__":
    create_ailuo_keynote()