import os
import datetime
import subprocess
import re

def check_session_pressure(threshold_percent=0.8):
    """
    通过读取 session_status 获取真实的上下文使用率。
    """
    try:
        # 运行 session_status 命令
        result = subprocess.run(['openclaw', 'session_status'], capture_output=True, text=True)
        output = result.stdout
        print(f"DEBUG: session_status output:\n{output}") 
        
        # 尝试匹配多种可能的百分比格式，例如 (7%) 或 (7.0%)
        match = re.search(r'\((\d+(?:\.\d+)?)%\)', output)
        if match:
            current_usage = float(match.group(1)) / 100.0
            return current_usage >= threshold_percent, current_usage
        
        # 如果正则没匹配到，尝试查找 Context 这一行
        context_line = re.search(r'Context:.*\((\d+)%\)', output)
        if context_line:
            current_usage = float(context_line.group(1)) / 100.0
            return current_usage >= threshold_percent, current_usage

    except Exception as e:
        print(f"Error reading session status: {e}")
    
    # 降级方案：如果获取失败，返回一个默认值
    return False, 0.0

def summarize_and_persist(history_content):
    """
    模拟总结并持久化。
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    memory_file = os.path.expanduser(f"~/.openclaw/workspace/memory/{today}.md")
    
    # 模拟生成的摘要
    summary = f"\n\n[Auto-Guardian Summary - {datetime.datetime.now()}]\nExtracted core points from heavy session.\n"
    
    os.makedirs(os.path.dirname(memory_file), exist_ok=True)
    with open(memory_file, "a") as f:
        f.write(summary)
    
    return summary

def send_qq_alert(message):
    """
    模拟发送 QQ 告警。
    """
    print(f"[QQ-ALERT] {message}")
    return True

def run_guardian_task():
    print("Starting Context Guardian Task...")
    is_high_pressure, usage = check_session_pressure()
    
    if is_high_pressure:
        print(f"High pressure detected: {usage*100:.1f}% usage.")
        summary = summarize_and_persist("Simulated heavy history content")
        send_qq_alert("⚠️ Context Warning: Session is heavy. I've backed up the summary. Please start a new chat!")
        print("Action: Summarized and Notified.")
        return "SUCCESS: Summarized and Notified"
    else:
        print(f"Pressure is fine: {usage*100:.1f}% usage.")
        return "SUCCESS: No action needed"

if __name__ == "__main__":
    result = run_guardian_task()
    print(f"Task Result: {result}")
