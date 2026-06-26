from .config import config


class AnchorManager:
    def __init__(self):
        self.anchors = {}

    def set_anchors_manually(self, anchors: dict):
        self.anchors = anchors

    def get_anchor_prompt(self) -> str:
        if not self.anchors:
            return ""
        anchor_prompt = "\n\n【核心设定】\n"
        for key, value in self.anchors.items():
            anchor_prompt += f"{key}：{value}\n"
        return anchor_prompt