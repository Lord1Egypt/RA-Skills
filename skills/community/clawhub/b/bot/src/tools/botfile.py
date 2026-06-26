import yaml

class Botfile:
    def __init__(self, path):
        with open(path, "r") as f:
            self.data = yaml.safe_load(f)

    def get_identity(self):
        return self.data.get("IDENTITY", "unknown_agent")

    def get_tools(self):
        return self.data.get("EQUIP", [])

    def get_permissions(self):
        return self.data.get("GRANT", []), self.data.get("DENY", [])
