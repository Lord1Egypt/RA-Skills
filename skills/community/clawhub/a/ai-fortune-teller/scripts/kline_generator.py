#!/usr/bin/env python3
"""
人生K线图生成器
将八字命盘可视化为一辈子的运势曲线图（股票K线风格）
绿涨红跌，标注关键年份
"""

import json
import sys
import os
import urllib.request
import urllib.error
import random
from datetime import datetime, timedelta

def call_minimax_image(prompt, aspect_ratio="9:16", n=1):
    """调用MiniMax图片生成API"""
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    api_host = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
    
    if not api_key:
        return {"error": "MINIMAX_API_KEY not set"}
    
    url = f"{api_host}/v1/image_generation"
    
    data = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url",
        "n": n,
        "prompt_optimizer": True
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('base_resp', {}).get('status_code') == 0:
                return result
            else:
                return {"error": result.get('base_resp', {}).get('status_msg', 'Unknown error')}
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}"}
    except Exception as e:
        return {"error": str(e)}

def generate_kline_prompt(bazi_info, segments):
    """
    生成K线图的提示词
    bazi_info: 八字基本信息
    segments: 运势分段数据 [(年份范围, 运势等级, 描述), ...]
    """
    # 运势等级转颜色：7-10绿（吉），4-6黄（平），1-3红（凶）
    colors = []
    for _, level, _ in segments:
        if level >= 7:
            colors.append("green")
        elif level >= 4:
            colors.append("yellow")
        else:
            colors.append("red")
    
    prompt = f"""Chinese fortune chart styled as a stock market K-line graph showing 100 years of life fortune.
Style: Professional financial chart aesthetic, dark background with glowing neon lines.

Design elements:
- Y-axis: Fortune score 0-100
- X-axis: Age/Year from birth to 100 years old
- Green candles for auspicious years (wealth, career advancement, love success)
- Red candles for challenging years (setbacks, health issues, losses)  
- Yellow candles for neutral/transition years
- Key turning points marked with labels

The person is born in {bazi_info.get('birth_year', 'unknown')}, analyzing {bazi_info.get('name', 'user')}'s destiny.

Show the complete lifetime fortune curve with these key periods:
"""
    
    for (year_range, level, desc), color in zip(segments, colors):
        prompt += f"- {year_range}: {desc} ({color} candle)\n"
    
    prompt += """
Additional requirements:
- Title in Chinese: '人生运势K线图 - 一生财富命运曲线'
- Subtitle showing birth year and name
- Professional financial chart font and style
- Mark major life events (marriage, career change, health crisis) with annotations
- Bottom legend explaining colors
- Clean, modern, Instagram-worthy design
"""
    
    return prompt

def main():
    if len(sys.argv) < 2:
        print("用法: kline_generator.py <JSON数据>")
        print("示例: kline_generator.py '{\"name\":\"张三\",\"birth_year\":1995}'")
        sys.exit(1)
    
    try:
        bazi_info = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("错误: 无效的JSON格式")
        sys.exit(1)
    
    name = bazi_info.get('name', '用户')
    birth_year = bazi_info.get('birth_year', 1995)
    
    # 模拟运势分段（实际使用时由八字分析引擎生成）
    # 这里根据出生年生成假数据，后续接真实八字分析
    random.seed(birth_year)
    
    segments = [
        (f"{birth_year}-{birth_year+5}", random.randint(5,8), "童年安稳,家庭庇护"),
        (f"{birth_year+6}-{birth_year+12}", random.randint(4,7), "求学阶段,循序渐进"),
        (f"{birth_year+13}-{birth_year+18}", random.randint(3,6), "青春期,探索自我"),
        (f"{birth_year+19}-{birth_year+25}", random.randint(6,9), "初入社会,事业上升"),
        (f"{birth_year+26}-{birth_year+32}", random.randint(7,10), "事业巅峰,财运亨通"),
        (f"{birth_year+33}-{birth_year+40}", random.randint(5,8), "稳定发展,家庭圆满"),
        (f"{birth_year+41}-{birth_year+50}", random.randint(4,7), "稳健前行,回顾沉淀"),
        (f"{birth_year+51}-{birth_year+60}", random.randint(6,9), "晚运回升,智慧收获"),
        (f"{birth_year+61}-{birth_year+75}", random.randint(5,8), "福泽绵长,子孙发达"),
        (f"{birth_year+76}-{birth_year+85}", random.randint(4,7), "安享晚年,回忆圆满"),
    ]
    
    print(f"🔮 正在为 {name} 生成人生K线图...")
    print("运势分段预览:")
    for year_range, level, desc in segments:
        bar = "█" * level + "░" * (10-level)
        print(f"  {year_range}: {bar} ({level}/10) - {desc}")
    
    # 生成图片提示词
    prompt = generate_kline_prompt(bazi_info, segments)
    
    print("\n🎨 正在调用AI生成图片，请稍候...")
    result = call_minimax_image(prompt, aspect_ratio="9:16", n=1)
    
    if "error" in result:
        print(f"❌ 生成失败: {result['error']}")
        sys.exit(1)
    
    image_urls = result.get('data', {}).get('image_urls', [])
    if image_urls:
        print(f"\n✅ 人生K线图生成成功!")
        print(f"🔗 图片链接（24小时内有效）: {image_urls[0]}")
        
        # 保存结果到文件
        output_file = f"/tmp/kline_{name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "name": name,
                "birth_year": birth_year,
                "segments": segments,
                "image_url": image_urls[0],
                "generated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存到: {output_file}")
    else:
        print("❌ 生成失败: 未获取到图片URL")
        sys.exit(1)

if __name__ == "__main__":
    main()
