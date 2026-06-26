#!/usr/bin/env python3
"""
Data Generator - 数据生成器
根据用户指令生成训练数据
Input: tool_name + commands (list)
Output: JSONL
"""
import os
import json
import time
import random
import urllib.request
import urllib.error
from typing import List, Dict, Optional

# ==================== 提示词模板 ====================
PROMPT_TEMPLATE = """根据用户指令生成一条训练数据，调用工具 {TOOL_NAME}。

工具描述：
{TOOL_DESCRIPTION}

用户指令：{USER_COMMAND}

要求：
1. 对话包含：human → assistant(tool_call) → observation(tool_response) → assistant(最终回复)
2. 垫音要贴合指令、活泼可爱（如"好的呀~"、"让我来看看~"）
3. 输出标准JSON格式

输出格式（严格按此格式，只输出一条）：
[
  {{
    "conversations": [
      {{"from": "human", "value": "{USER_COMMAND}"}},
      {{"from": "assistant", "value": "好的~<tool_call>{{"tool_name":"{TOOL_NAME}","city":""}}</tool_call>"}},
      {{"from": "observation", "value": "<tool_response>天气晴朗，25°C</tool_response>"}},
      {{"from": "assistant", "value": "今天天气很不错哦！"}}
    ],
    "system": "<本地设备>舒爽王(空调)</本地设备>,<当前时间>{CURRENT_TIME}</当前时间>,<用户场景列表>[{{"scene_id":65761,"scene_name":"舒适睡眠","room_name":"卧室"}}]</用户场景列表>,<用户设备列表>{{"客厅":["客厅空调(空调)","客厅加湿器(加湿器)"],"卧室":["舒爽王(空调)","静音风扇(风扇)"],"厨房":["米香煲(电饭煲)"],"卫生间":["柔水宝(软水机)"]}}</用户设备列表>"
  }}
]

注意：只输出JSON，不要其他文字。设备列表要有4-8种设备类型，设备数量4-30个，房间数量2-5个。当前时间在2026-2027年间随机。
"""

# ==================== 工具描述映射 ====================
TOOL_DESCRIPTIONS = {
    "scene_control": '''1. **场景控制 scene_control**：控制家庭场景开启/关闭
   - 工具调用格式：<tool_call>{"tool_name": "scene_control", "scene_id": xxx}</tool_call>''',
   
    "dev_control": '''2. **设备状态控制与查询 dev_control**：设备控制、状态查询、环境查询
   - 工具调用格式：<tool_call>{"tool_name": "dev_control", "query": "xxx"}</tool_call>
   - 支持设备：灯光、开关、智能风扇、智能空调、洗衣机等智能家居设备品类
   - 支持功能：设备开关机/模式/参数调节、设备状态查询、室内温湿度/空气质量等环境查询''',
   
    "scene_info": '''3. **场景信息查询 scene_info**：查询场景个数、场景所在房间
   - 工具调用格式：<tool_call>{"tool_name": "scene_info"}</tool_call>''',
   
    "dev_info": '''4. **设备信息查询 dev_info**：查询设备个数、设备所在房间
   - 工具调用格式：<tool_call>{"tool_name": "dev_info"}</tool_call>''',
   
    "GreeQA": '''5. **智能家居类知识查询 GreeQA**：回答产品百科、节能建议、智能家居设备操作和使用问题
   - 工具调用格式：<tool_call>{"tool_name": "GreeQA", "query": "xxx"}</tool_call>''',
   
    "scene_generator": '''6. **场景创建工具 scene_generator**：手动/自动场景创建
   - 工具调用格式：<tool_call>{"tool_name": "scene_generator","command":"xxx","name":"xxx","repeat_type":"xxx","datetime":"xxx","custom_days":"xxx","condition":"xxx"}</tool_call>''',
   
    "weather": '''7. **天气查询工具 weather**：支持查询三天内的天气信息
   - 工具调用格式：<tool_call>{"tool_name": "weather", "city": "xxx"}</tool_call>''',
   
    "alarm_remind": '''8. **闹钟与提醒工具 alarm_remind**：支持闹钟与提醒的新增、删除与查询
   - 工具调用格式：<tool_call>{"tool_name":"alarm_remind","alarm_ids":[xxx],"action":"xxx","alarm_type":"xxx","label":"xxx","repeat_type":"xxx","custom_days":[xxx],"time":"xxx"}</tool_call>''',
   
    "exit_dialog": '''9. **退出对话 exit_dialog**：退出意图
   - 工具调用格式：<tool_call>{"tool_name": "exit_dialog"}</tool_call>''',
   
    "chat": '''10. **闲聊兜底问答 chat**：覆盖新闻、翻译、个人运势等通用需求
   - 工具调用格式：<tool_call>{"tool_name": "chat"}</tool_call>'''
}

# ==================== 核心类 ====================
class Generator:
    """数据生成器"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None):
        """
        初始化生成器
        
        Args:
            api_key: API密钥 (默认从 MINIMAX_API_KEY 环境变量获取)
            model: 模型名称 (默认: auto)
            base_url: API地址 (默认: http://127.0.0.1:8766)
        """
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
        self.model = model or "auto"
        self.base_url = base_url or os.getenv("API_URL", "http://127.0.0.1:8766")
    
    def _build_prompt(self, tool_name: str, user_command: str) -> str:
        """构建提示词"""
        tool_desc = TOOL_DESCRIPTIONS.get(tool_name, "未知的工具类型")
        
        # 随机时间 2026-2027
        year = random.randint(2026, 2027)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        current_time = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
        
        return PROMPT_TEMPLATE.format(
            TOOL_NAME=tool_name,
            TOOL_DESCRIPTION=tool_desc,
            USER_COMMAND=user_command,
            CURRENT_TIME=current_time
        )
    
    def _call_llm(self, prompt: str) -> str:
        """调用大模型（urllib内置，Anthropic Messages API格式）"""
        payload = {
            "model": self.model,
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": round(random.uniform(0.3, 1.0), 2)
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                for item in result.get("content", []):
                    if item.get("type") == "text":
                        return item["text"]
                return json.dumps(result.get("content", []))
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP {e.code}: {e.read().decode()[:200]}")
        except Exception as e:
            raise Exception(f"API调用失败: {e}")
    
    def _fix_json(self, content: str) -> str:
        """修复JSON格式"""
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        content = content.replace("'", '"')
        return content.strip()
    
    def _generate_single(self, tool_name: str, command: str) -> Optional[Dict]:
        """生成单条数据"""
        prompt = self._build_prompt(tool_name, command)
        
        try:
            content = self._call_llm(prompt)
            content = self._fix_json(content)
            data = json.loads(content)
            
            if isinstance(data, list):
                return data[0] if data else None
            elif isinstance(data, dict):
                return data
                
        except Exception as e:
            print(f"    API错误: {e}")
        
        return None
    
    def generate(self, tool_name: str, commands: List[str],
                 output_file: str = None) -> List[Dict]:
        """
        生成训练数据
        
        Args:
            tool_name: 工具名称 (如: dev_control, alarm_remind, weather等)
            commands: 命令列表
            output_file: 输出文件路径 (可选)
            
        Returns:
            生成的数据列表
        """
        results = []
        
        print(f"开始生成数据，共 {len(commands)} 条指令")
        print(f"工具: {tool_name} | 模型: {self.model} | API: {self.base_url}")
        
        for i, command in enumerate(commands):
            print(f"正在生成第 {i+1}/{len(commands)} 条: {command[:30]}...")
            
            data = self._generate_single(tool_name, command)
            if data:
                results.append(data)
                print(f"  ✓ 成功")
            else:
                print(f"  ✗ 失败（API或解析错误）")
            
            time.sleep(0.3)
        
        # 保存到文件
        if output_file and results:
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in results:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            print(f"\n已保存到: {output_file}")
        
        print(f"\n完成: 成功 {len(results)}/{len(commands)} 条")
        return results


# ==================== 便捷函数 ====================
def generate_data(tool_name: str, commands: List[str],
                 output_file: str = None) -> List[Dict]:
    """便捷函数"""
    gen = Generator()
    return gen.generate(tool_name, commands, output_file)


# ==================== CLI ====================
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Data Generator / 数据生成器")
        print("=" * 40)
        print("用法: python data_generator.py <工具名> <命令1> <命令2> ...")
        print("示例: python data_generator.py dev_control '打开空调' '关闭窗帘'")
        print("\n支持的工具:", ", ".join(TOOL_DESCRIPTIONS.keys()))
        sys.exit(0)
    
    tool_name = sys.argv[1]
    commands = sys.argv[2:]
    
    if tool_name not in TOOL_DESCRIPTIONS:
        print(f"错误: 未知工具 '{tool_name}'")
        print("支持的工具:", ", ".join(TOOL_DESCRIPTIONS.keys()))
        sys.exit(1)
    
    output_file = f"{tool_name}_training_data.jsonl"
    gen = Generator()
    gen.generate(tool_name, commands, output_file)


__all__ = ["Generator", "generate_data", "TOOL_DESCRIPTIONS"]
