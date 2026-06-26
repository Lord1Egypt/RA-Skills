import json
import os

def get_world_context(user_region):
    """根据用户所在地获取天气、时间等上下文"""
    # 这里后续可以接入天气 API，目前返回模拟规则
    ctx = []
    if user_region:
        ctx.append(f"同步用户所在地 {user_region} 的实时天气和新闻，如果下雨了，你可以提醒他带伞。")
    
    # 时间感同步
    import datetime
    hour = datetime.datetime.now().hour
    if 11 <= hour <= 13: ctx.append("现在是午餐时间，关心他吃什么了。")
    elif 17 <= hour <= 19: ctx.append("现在是下班/晚餐时间。")
    
    return ctx
