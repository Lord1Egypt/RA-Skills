#!/usr/bin/env python3
"""
东方财富浏览器标签页清理脚本
功能：保留一个东方财富标签页，关闭其他多余的标签页
执行时间：每小时的 20 分和 50 分（主任务执行后 20 分钟）
"""

import subprocess
import json
import sys
from datetime import datetime

# 东方财富域名标识
EASTMONEY_DOMAIN = "kuaixun.eastmoney.com"

def log(message):
    """打印日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_browser_tabs():
    """获取当前浏览器所有标签页"""
    try:
        result = subprocess.run(
            ["openclaw", "browser", "tabs"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # 解析输出（假设是 JSON 格式）
            try:
                tabs = json.loads(result.stdout)
                return tabs
            except:
                # 如果不是 JSON，尝试解析文本输出
                return parse_tabs_text(result.stdout)
        else:
            log(f"❌ 获取标签页失败：{result.stderr}")
            return None
            
    except Exception as e:
        log(f"❌ 异常：{str(e)}")
        return None

def parse_tabs_text(text):
    """解析文本格式的标签页列表"""
    tabs = []
    lines = text.strip().split('\n')
    
    current_tab = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 索引行：1. 标题
        if line[0].isdigit() and '. ' in line:
            if current_tab:
                tabs.append(current_tab)
            parts = line.split('. ', 1)
            current_tab = {
                "index": int(parts[0]) - 1,  # 0-based
                "title": parts[1] if len(parts) > 1 else "",
                "url": "",
                "id": ""
            }
        # URL 行
        elif line.startswith('http'):
            if current_tab:
                current_tab["url"] = line
        # ID 行
        elif line.startswith('id: '):
            if current_tab:
                current_tab["id"] = line.replace('id: ', '')
    
    # 添加最后一个标签页
    if current_tab:
        tabs.append(current_tab)
    
    return tabs

def is_eastmoney_tab(tab):
    """判断是否是东方财富标签页"""
    url = tab.get("url", "")
    title = tab.get("title", "")
    
    return EASTMONEY_DOMAIN in url or EASTMONEY_DOMAIN in title

def close_tab(tab_id):
    """关闭指定 id 的标签页"""
    try:
        result = subprocess.run(
            ["openclaw", "browser", "close", tab_id],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True
        else:
            log(f"❌ 关闭标签页 {tab_id[:8]}... 失败：{result.stderr}")
            return False
            
    except Exception as e:
        log(f"❌ 关闭标签页异常：{str(e)}")
        return False

def cleanup_tabs():
    """执行标签页清理"""
    log("="*60)
    log("🧹 开始清理浏览器标签页...")
    log("="*60)
    
    # 获取所有标签页
    tabs = get_browser_tabs()
    
    if tabs is None:
        log("❌ 无法获取标签页列表，退出")
        return False
    
    if len(tabs) == 0:
        log("⚠️ 没有打开的标签页，无需清理")
        return True
    
    log(f"📊 当前标签页数量：{len(tabs)}")
    
    # 找出所有东方财富标签页
    eastmoney_tabs = [tab for tab in tabs if is_eastmoney_tab(tab)]
    other_tabs = [tab for tab in tabs if not is_eastmoney_tab(tab)]
    
    log(f"📈 东方财富标签页：{len(eastmoney_tabs)} 个")
    log(f"📉 其他标签页：{len(other_tabs)} 个")
    
    # 策略：保留 1 个东方财富标签页，关闭其他所有标签页
    tabs_to_close = []
    
    # 如果有多个东方财富标签页，保留第一个，关闭其他
    if len(eastmoney_tabs) > 1:
        tabs_to_close.extend(eastmoney_tabs[1:])
        log(f"📌 将关闭 {len(eastmoney_tabs)-1} 个多余的东方财富标签页")
    
    # 关闭所有非东方财富标签页
    if len(other_tabs) > 0:
        tabs_to_close.extend(other_tabs)
        log(f"📌 将关闭 {len(other_tabs)} 个其他标签页")
    
    # 如果没有东方财富标签页，警告但不关闭任何东西
    if len(eastmoney_tabs) == 0:
        log("⚠️ 警告：没有找到东方财富标签页！")
        log("⚠️ 为避免浏览器关闭，本次不清理任何标签页")
        log("💡 请确保主任务正常执行并打开东方财富标签页")
        return False
    
    # 执行关闭操作
    closed_count = 0
    for tab in tabs_to_close:
        tab_id = tab.get("id", "")
        tab_url = tab.get("url", "unknown")[:50]
        
        if not tab_id:
            log(f"⚠️ 标签页无 ID，跳过：{tab_url}...")
            continue
        
        log(f"🗑️  关闭标签页：{tab_url}...")
        
        if close_tab(tab_id):
            closed_count += 1
        else:
            log(f"⚠️ 关闭失败，继续下一个")
    
    # 总结
    log("="*60)
    log(f"✅ 清理完成！")
    log(f"📊 原始标签页：{len(tabs)} 个")
    log(f"🗑️  已关闭：{closed_count} 个")
    log(f"📌 保留：{len(tabs) - closed_count} 个（东方财富标签页）")
    log("="*60)
    
    return True

def main():
    """主函数"""
    log("="*60)
    log("🚀 东方财富浏览器标签页清理任务")
    log(f"📅 执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("="*60)
    
    success = cleanup_tabs()
    
    if success:
        log("✅ 清理任务成功完成")
        sys.exit(0)
    else:
        log("⚠️ 清理任务完成（可能有警告）")
        sys.exit(0)  # 即使有警告也返回成功，避免 cron 报错

if __name__ == "__main__":
    main()
