from typing import List

class AgentCore:
    def __init__(self, identity: str):
        self.identity = identity

    def think(self, prompt: str) -> dict:
        # 模拟递归链式思考
        thought_process = [f"Analyzing: {prompt}", "Generating insights..."]
        return {
            "thought_process": thought_process,
            "confidence_score": 0.95,
            "action_required": False,
            "payload": {}
        }

# 可选：与 TUI 联动展示思考流
def think_with_tui(self, prompt: str, tui=None) -> dict:
    result = self.think(prompt)
    if tui:
        tui.display_thought(result["thought_process"])
    return result

def think_with_signature(self, prompt: str, crypto=None) -> dict:
    """
    生成思考结果并附带 Crypto 身份签名
    """
    result = self.think(prompt)
    if crypto:
        message = str(result).encode("utf-8")
        signature = crypto.sign(message)
        result["signature"] = signature.hex()
        result["public_key"] = crypto.serialize_public()
    return result
