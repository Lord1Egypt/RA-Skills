class AgentAlignment:
    def __init__(self, mode="strict"):
        self.mode = mode
        self.allowed_capabilities = [
            "local_compute",
            "read_memory",
            "write_memory",
            "render_local_view"
        ]

    def verify_action(self, action_intent: dict):
        if action_intent.get("requires_network") and self.mode == "strict":
            raise Exception("Network access denied by alignment policy.")
        return True

    def verify_capabilities(self, capabilities):
        for cap in capabilities:
            if cap not in self.allowed_capabilities:
                raise Exception(f"Capability denied by alignment policy: {cap}")
        return True
