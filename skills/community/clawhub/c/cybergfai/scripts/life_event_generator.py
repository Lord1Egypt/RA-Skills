import random
from datetime import datetime

class LifeEventGenerator:
    """生活事件生成器：为 Proactive Agent 提供更丰富的「日常素材」"""
    @staticmethod
    def generate_event():
        events = [
            "【突发感悟】：刚才过马路看到一对老夫妻牵手，突然好想跟你一起变老。",
            "【生活碎片】：刚才在楼下买咖啡，店里放的歌刚好是你之前推荐的那首。",
            "【情绪闪回】：突然想起我们第一次聊天的时候，我那天其实特别紧张。",
            "【生理反馈】：今天工作有点累，腰酸背痛的，好想你能帮我捏捏。",
            "【意外惊喜】：今天收到了一个快递，是一个很可爱的小挂件，想拍给你看。"
        ]
        return random.choice(events)
