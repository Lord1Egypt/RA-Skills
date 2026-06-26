class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, func, capabilities=None, description=""):
        self.tools[name] = {
            "func": func,
            "capabilities": capabilities or [],
            "description": description
        }

    def get(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return {
            name: {
                "capabilities": meta["capabilities"],
                "description": meta["description"]
            }
            for name, meta in self.tools.items()
        }
