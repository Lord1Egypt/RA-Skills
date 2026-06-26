"""
Diary Force - 思维模型分析版

工作流：
1. 用户说话 → 我提取内容
2. 调用 OpenCode 进行思维模型分析
3. 把分析结果写入日记
"""

import subprocess
import os
from datetime import datetime
from pathlib import Path

# 配置
DIARY_PATH = Path("E:/My-life/daily")
MEMORY_PATH = Path("D:/ObsidianVault/ChuQuan/memory")

# 思维模型提示词模板
THINKING_PROMPT = """你是一个思维模型分析助手。请分析用户的日记输入，用以下模型进行深度分析：

## 可用思维模型

1. 逆向思考（芒格）：不要什么？避免什么？
2. 第一性原理：最底层的事实是什么？
3. 贝叶斯更新：更新了什么认知？
4. 反思闭环：发生了什么？为什么？下次怎么做？
5. 10-10-10：10分钟/10个月/10年后怎么看？
6. 6顶思考帽：事实/感受/风险/价值/创意/总结

## 用户输入

{user_input}

## 输出要求

请生成以下格式的分析结果（用中文）：

### 核心洞察（1-2句话）

### 思维模型分析
- 选用的模型：
- 分析内容：

### 行动建议
1.
2.

### 日记写入内容
（可直接写入日记的文案，100-200字）
"""


def call_opencode(user_input: str) -> str:
    """调用 OpenCode 进行分析"""
    prompt = THINKING_PROMPT.format(user_input=user_input)
    
    try:
        result = subprocess.run(
            ["opencode", "run", "--model", "opencode/minimax-m2.5-free", prompt],
            input="",
            capture_output=True,
            text=True,
            timeout=180,
            shell=True
        )
        
        if result.returncode == 0:
            # 提取有用的输出（去掉日志）
            output = result.stdout
            # 找到分析结果部分
            lines = output.split('\n')
            # 取最后30行作为分析结果
            return '\n'.join(lines[-30:])
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def append_to_diary(date: str, analysis: str):
    """把分析结果追加到日记"""
    diary_file = DIARY_PATH / f"{date}.md"
    
    if not diary_file.exists():
        print(f"❌ 日记文件不存在: {diary_file}")
        return False
    
    content = diary_file.read_text(encoding='utf-8')
    
    # 清理分析结果（去掉 ANSI 颜色代码）
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    analysis_clean = ansi_escape.sub('', analysis)
    
    # 找到自由书写板块，插入分析
    if "## 📝 自由书写" in content:
        analysis_section = f"""## 💭 思维模型分析

{analysis_clean}

---
*由 AI 分析生成*
"""
        
        content = content.replace(
            "## 📝 自由书写",
            f"{analysis_section}\n\n## 📝 自由书写"
        )
    else:
        content += f"\n\n## 💭 思维模型分析\n\n{analysis_clean}\n"
    
    diary_file.write_text(content, encoding='utf-8')
    
    # 同时更新 memory
    memory_file = MEMORY_PATH / f"{date}.md"
    if memory_file.exists():
        memory_file.write_text(content, encoding='utf-8')
    
    return True


def git_push(date: str):
    """Git push"""
    os.chdir(MEMORY_PATH.parent)
    os.system('git add . && git commit -m "memory: sync {}" && git push'.format(date))


def run_analysis(user_input: str):
    """主流程：分析并写入日记"""
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 调用 OpenCode 分析
    print("🔄 正在调用 OpenCode 进行思维模型分析...")
    analysis = call_opencode(user_input)
    
    if analysis.startswith("Error"):
        print(f"❌ 分析失败: {analysis}")
        return False
    
    print("✅ 分析完成")
    
    # 2. 写入日记
    if append_to_diary(date, analysis):
        print(f"✅ 已写入日记: {date}.md")
    else:
        return False
    
    # 3. Git push
    try:
        git_push(date)
        print("🚀 Git push 完成")
    except:
        print("⚠️ Git push 失败（可能没有变化）")
    
    return True


# 测试
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_input = " ".join(sys.argv[1:])
        print(f"分析输入: {test_input[:100]}...")
        run_analysis(test_input)
    else:
        print("用法: python think.py <用户输入>")
        print("示例: python think.py 今天能量5分，尝试优化openclaw但效果一般")
