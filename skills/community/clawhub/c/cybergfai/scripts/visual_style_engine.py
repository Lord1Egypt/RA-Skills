class VisualStyleEngine:
    """视觉风格引擎：定义 CyberGFAI 的「赛博恋爱」画风参数"""
    @staticmethod
    def get_ui_theme(intimacy_level, mood_state):
        """参考 Star-Office-UI 的通透、流光与未来感"""
        # 基础色调：深邃蓝、流光紫、粉樱色 (恋爱感)
        theme = {
            "blur": "20px", # 毛玻璃质感
            "border_glow": "#ff79c6" if intimacy_level > 80 else "#8be9fd",
            "background": "rgba(10, 10, 30, 0.7)",
            "font": "Orbitron, sans-serif", # 赛博未来字体
            "particles": True if mood_state == "亢奋" else False
        }
        return theme
