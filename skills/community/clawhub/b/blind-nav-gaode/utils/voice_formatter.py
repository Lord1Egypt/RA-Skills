def format_route_for_voice(steps: list) -> list:
    """将路线步骤转换为语音友好的描述"""
    voice_steps = []
    cum_distance = 0
    
    for i, step in enumerate(steps):
        cum_distance += int(step.get("distance", 0))
        
        # 简化导航指令
        instruction = step.get("instruction", "")
        road_name = step.get("road_name", "")
        
        # 生成语音友好描述
        if i == 0:
            voice = f"从当前位置出发，沿{road_name}步行{step.get('distance')}米"
        elif "左转" in instruction:
            voice = f"左转，沿{road_name}步行{step.get('distance')}米"
        elif "右转" in instruction:
            voice = f"右转，沿{road_name}步行{step.get('distance')}米"
        elif "直行" in instruction:
            voice = f"直行{step.get('distance')}米"
        elif "到达" in instruction:
            voice = f"已到达目的地"
        else:
            voice = f"沿{road_name}步行{step.get('distance')}米"
        
        voice_steps.append({
            "step": i + 1,
            "instruction": instruction,
            "road": road_name,
            "distance": step.get("distance"),
            "cumulative_distance": cum_distance,
            "voice_friendly": voice
        })
    
    return voice_steps