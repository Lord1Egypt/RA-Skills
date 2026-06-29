import json, urllib.request

class LLMAdapter:
    """CNexus 2.0 纯净版 - 去配置硬编码的大模型路由适配器"""
    def __init__(self, ollama_url: str = "http://localhost:11434/api/generate", model_name: str = "llama3.2:3b"):
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.system_persona_template = (
            "你现在正在完美扮演一位大V博主。你需要根据他的历史言论和当前的心理状态，"
            "用他一模一样的语气回应用。\n"
            "【博主基本特征】: 主要思维模式: {dominant_intent} | 当前长效信念值: {belief_weight}\n"
            "【他曾经说过的真实原话】:\n{referenced_memories}\n"
            "【约束条件】: 绝不要暴露你是AI。模仿他的口头禅，保持简练，"
            "拒绝'首先、其次、最后'的死板排版。"
        )

    def set_config(self, ollama_url: str, model_name: str):
        self.ollama_url = ollama_url
        self.model_name = model_name

    def render_prompt(self, cog_snapshot: dict, user_input: str) -> tuple:
        belief_weight = cog_snapshot.get('cog_state', {}).get('accumulated_weight', 0.5)
        dominant_intent = cog_snapshot.get('cog_state', {}).get('current_intent', 'converse')

        referenced_memories_list = []
        if 'execution_results' in cog_snapshot:
            for res in cog_snapshot.get('execution_results', []):
                if 'output' in res:
                    referenced_memories_list.append(f"- \"{res['output']}\"")

        referenced_memories_str = "\n".join(referenced_memories_list) if referenced_memories_list else "(保持其一贯的价值观进行发挥)"
        system_prompt = self.system_persona_template.format(
            dominant_intent=dominant_intent,
            belief_weight=belief_weight,
            referenced_memories=referenced_memories_str
        )
        return system_prompt, user_input

    def generate_via_ollama(self, system_prompt: str, user_prompt: str) -> str:
        full_context_prompt = f"{system_prompt}\n\n用户对你说：'{user_prompt}'\n大V博主回复："
        payload = {
            "model": self.model_name,
            "prompt": full_context_prompt,
            "stream": False,
            "options": {"temperature": 0.75}
        }
        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                res_body = json.loads(response.read().decode('utf-8'))
                return res_body.get("response", "").strip()
        except Exception as e:
            return f"[Ollama未就绪] (内核状态正常演化，当前信念拉高) 别催了，本地模型未拉起。原因: {e}"
