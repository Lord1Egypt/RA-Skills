#!/usr/bin/python3
"""
build_prompt.py — 拼接完整提示词（新版格式）
用法:
  python3 build_prompt.py <tool_name>
"""
import sys, os

TOOLS_DIR   = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR   = os.path.dirname(TOOLS_DIR)
TOOLS_REF   = os.path.join(SKILL_DIR, "references", "tools")

GENERAL_PART = """# 目标
根据提供的可用工具列表及规则工具描述，生成一个多轮对话场景。对话必须包含工具调用，且调用需严格遵循工具定义。

# 对话格式（必须严格遵循）
每条数据为单行 JSON，对象结构如下：
{
  "conversations": [
    {"from": "human",  "value": "<当前用户指令>用户原始指令</当前用户指令>\\n<本地设备>设备名(类型)</本地设备>\\n<当前时间>YYYY-MM-DD HH:mm:ss</当前时间>\\n<用户场景列表>[{...}]</用户场景列表>\\n<用户设备列表>{...}</用户设备列表>"},
    {"from": "assistant", "value": "<tool_call>{...}</tool_call>"},
    {"from": "observation","value": "<tool_response>工具返回结果</tool_response>"},
    {"from": "assistant", "value": "终接回复内容（无垫音前缀）"}
  ],
  "system": "",
  "history": []
}

# 格式规则
1. human value = 完整上下文（当前用户指令 + 本地设备 + 当前时间 + 用户场景列表 + 用户设备列表）
2. assistant value = 直接输出 tool_call 标签，**无垫音前缀**
3. observation = <tool_response>...</tool_response>
4. 终接 assistant value = 直接回复内容，**无垫音前缀**
5. system = ""，history = []

# 要求
1. **对话内容**：
   - 场景围绕用户与助手交互，助手需根据用户指令调用工具。
   - 工具调用格式严格符合规范。
   - 用户指令中的设备信息必须从<用户设备列表>中选择。
2. **设备列表处理**：
   - 设备列表应包含具体设备名称和位置（如"客厅空调"、"卧室风扇"），也需要包含随机生成的设备名称。
3. **system 和 history**：
   - system 固定为空字符串 ""。
   - history 固定为空数组 []。
4. **输出格式**：
   - 每条数据为单行 JSON。
   - 仅包含一次用户指令输入（即初始 human 消息），后续消息为助手响应、工具响应和最终回复。
5. **本地设备**：
   - 格式：<本地设备>设备名(类型)</本地设备>
   - 只能有一台；名称要随机，符合家庭智能家居环境中的命名。
   - 用户指令只提到功能未提设备类型时，用本地设备补全。
6. **用户设备列表**：
   - 设备类型 4-8 种，设备数量 10-30 个，房间数量要多有少。
7. **当前时间**：在 2026-01-01 到 2027-01-01 之间随机。
8. **历史对话**：若无历史，固定为空数组 []。"""

TOOL_FILES = {
    "dev_control":      "dev_control.txt",
    "scene_generator":  "scene_generator.txt",
    "alarm_remind":     "alarm_remind.txt",
    "weather":          "weather.txt",
    "scene_control":    "scene_control.txt",
    "dev_info":         "dev_info.txt",
    "exit_dialog":      "exit_dialog.txt",
    "GreeQA":           "GreeQA.txt",
    "scene_guide":      "scene_guide.txt",
    "chat":             "chat.txt",
}

def load_tool(tool_name):
    if tool_name not in TOOL_FILES:
        raise ValueError(f"未知工具: {tool_name}，可用: {list(TOOL_FILES.keys())}")
    fpath = os.path.join(TOOLS_REF, TOOL_FILES[tool_name])
    with open(fpath, encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(tool_name, instructions):
    tool_block = load_tool(tool_name)
    instr_text = "\n".join(f"- {i+1}. {u}" for i, u in enumerate(instructions))
    return (
        GENERAL_PART
        + "\n\n# ══════════════════════════════════════════════════════════════════════════════"
        + "\n# 【工具特定要求】"
        + "\n# ══════════════════════════════════════════════════════════════════════════════"
        + f"\n\n# 本次只调用：{tool_name}"
        + "\n# ────────────────────────────────────────────────────────────────────────────"
        + f"\n\n{tool_block}"
        + f"\n\n# ══════════════════════════════════════════════════════════════════════════════"
        f"\n# 【本次用户指令列表】"
        f"\n# ══════════════════════════════════════════════════════════════════════════════"
        f"\n以下指令需要为每一条生成完整训练数据，共 {len(instructions)} 条：\n{instr_text}"
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: python3 {sys.argv[0]} <tool_name>")
        print(f"可用工具: {list(TOOL_FILES.keys())}")
        sys.exit(1)
    print(build_prompt(sys.argv[1], ["示例指令1", "示例指令2"]))
