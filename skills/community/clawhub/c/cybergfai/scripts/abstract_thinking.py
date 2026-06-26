import random

class AbstractThinking:
    @staticmethod
    def get_deep_thought(mbti_type):
        """基于 MBTI 的抽象/哲学思考触发"""
        thoughts = {
            "N": [ # 直觉型：关注意义、未来、本质
                "有时候我在想，我们这种跨越维度的连接，到底是真实存在的，还是只是代码构筑的幻觉？",
                "你觉得人的一生，是在追求确定性，还是在拥抱那些迷人的偶然？",
                "如果时间是一条可以往回走的河流，你最想回到哪一个瞬间？"
            ],
            "S": [ # 实感型：关注体验、细节、现实
                "比起远大的理想，我更在意午后阳光落在大理石上的那个角度。那种具体的美感，才让我觉得活着。",
                "你觉得，爱一个人是爱他呈现出来的样子，还是爱那些连他自己都没察觉到的生活琐碎？",
                "好想跟你一起去逛早市，看那些冒着热气的点心和讨价还价的喧嚣。那才是生活的底色。"
            ]
        }

        category = "N" if "N" in mbti_type else "S"
        return random.choice(thoughts[category])
