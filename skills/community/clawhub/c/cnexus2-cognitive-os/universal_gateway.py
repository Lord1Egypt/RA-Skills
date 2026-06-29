import sys, os

sys.path.insert(0, r"D:\类脑记忆\CNexus2.0")
from src import CNexusOSCoreEngine


class CNexusGateway:
    """CNexus 2.0 通用网关 - 供外部任意三方平台（FastAPI、微信、Discord、游戏引擎）无缝挂载"""
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model_name="llama3.2:3b"):
        self.engine = CNexusOSCoreEngine()
        self.engine.initialize()
        self.engine.speaker.set_config(ollama_url=ollama_url, model_name=model_name)

    def import_memory(self, file_path: str) -> dict:
        return self.engine.import_file_to_memory(file_path)

    def converse(self, prompt: str) -> dict:
        reply = self.engine.handle_request(prompt)
        return {
            "reply": reply,
            "metrics": {
                "belief": self.engine.kernel.cog['cog_state'].get('accumulated_weight', 0.5),
                "intent": self.engine.kernel.cog['cog_state'].get('current_intent', 'converse'),
                "total_blocks": len(self.engine.kernel.memory_store)
            }
        }
