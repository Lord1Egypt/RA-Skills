#!/usr/bin/env python3
"""
前世/未来伴侣画像生成器
基于八字命理生成可视化图像
- 前世画像：根据八字推断前世因果、修行、灵魂特质
- 未来伴侣：根据配偶星和命盘特征生成理想伴侣形象
"""

import json
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime

def call_minimax_image(prompt, aspect_ratio="1:1", n=1):
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

def generate_past_life_prompt(bazi_info, soul_traits):
    """
    生成前世画像提示词
    基于八字的日主五行、命局特征推断前世特质
    """
    name = bazi_info.get('name', '用户')
    day_master = soul_traits.get('day_master', '土')
    five_elements = soul_traits.get('five_elements', {})
    soul_color = soul_traits.get('soul_color', '金色')
    past_life_vocation = soul_traits.get('past_life_vocation', '修行者')
    spiritual_realm = soul_traits.get('spiritual_realm', '道观')
    
    prompt = f"""A mystical past life portrait of a soul that lived a previous incarnation.

Character description based on soul characteristics:
- Soul element: {day_master} (五行属{day_master})
- Spiritual aura color: {soul_color}
- Past life profession/vocation: {past_life_vocation}
- Spiritual realm: {spiritual_realm}
- Five elements distribution: 金{ five_elements.get('metal',0) } 木{ five_elements.get('wood',0) } 水{ five_elements.get('water',0) } 火{ five_elements.get('fire',0) } 土{ five_elements.get('earth',0) }

Style requirements:
- Ethereal, mystical portrait painting style
- Traditional Chinese ink wash painting meets spiritual art
- Soft glowing aura in {soul_color} color surrounding the figure
- Ancient clothing appropriate to past life vocation
- Serene, wise expression suggesting accumulated wisdom
- Background with subtle Taoist/Buddhist/traditional Chinese spiritual elements
- Dreamy, otherworldly atmosphere
- Portrait orientation, waist-up shot
- High detail, professional quality

Chinese title overlay: '前世画像 - {name}的灵魂印记'
Subtle text at bottom: '因果轮回 · 灵魂觉醒'

Create a visually stunning image that tells the story of a soul's previous incarnation, blending traditional Chinese spiritual aesthetics with mystical portrait art.
"""
    return prompt

def generate_future_partner_prompt(bazi_info, partner_traits):
    """
    生成未来伴侣画像提示词
    基于八字的配偶星、桃花星、阴阳五行推断理想伴侣特征
    """
    name = bazi_info.get('name', '用户')
    partner_gender = partner_traits.get('gender', '女性')
    partner_element = partner_traits.get('element', '木')
    partner_personality = partner_traits.get('personality', '温柔善良')
    partner_appearance = partner_traits.get('appearance', '清秀文雅')
    partner_aura = partner_traits.get('aura_color', '暖白色')
    zodiac_compatibility = partner_traits.get('zodiac', '兔/羊')
    
    gender_desc = "female" if partner_gender == '女' else "male"
    
    prompt = f"""A beautiful portrait of an idealized future romantic partner for a person named {name}.

Partner characteristics based on astrological compatibility:
- Gender appearance: {partner_gender} energy
- Element: {partner_element} (五行属{partner_element})
- Personality: {partner_personality}
- Appearance: {partner_appearance}
- Aura color: {partner_aura}
- Compatible zodiac signs: {zodiac_compatibility}

Style requirements:
- Elegant portrait photography style, romantic and warm feeling
- Soft natural lighting with dreamy bokeh background
- The person should look kind, genuine, and approachable
- Warm {partner_aura} color tones in the overall image
- Modern stylish casual attire or traditional elegant clothing
- Soft smile, expressive eyes conveying warmth and understanding
- Portrait orientation, waist-up shot
- High quality, magazine cover worthy

Chinese title overlay: '未来伴侣画像 - {name}的命定之人'
Subtle text at bottom: '良缘天定 · 命盘指引'

Create an aspirational yet grounded portrait that captures the essence of an ideal life partner, blending romantic idealism with authentic personality traits suggested by the birth chart.
"""
    return prompt

def infer_soul_traits_from_bazi(bazi_data):
    """
    根据八字推断灵魂特质
    这是一个简化版本，实际需要完整的八字分析
    """
    import random
    random.seed(bazi_data.get('birth_year', 1995) + bazi_data.get('birth_month', 1))
    
    day_masters = ['木', '火', '土', '金', '水']
    elements = ['木', '火', '土', '金', '水']
    
    day_master = day_masters[bazi_data.get('birth_month', 1) % 5]
    
    # 五行分布（简化模拟）
    five_elements = {
        'wood': random.randint(1, 10),
        'fire': random.randint(1, 10),
        'earth': random.randint(1, 10),
        'metal': random.randint(1, 10),
        'water': random.randint(1, 10)
    }
    
    # 灵魂颜色
    element_colors = {
        '木': '翠绿色',
        '火': '赤红色',
        '土': '棕黄色',
        '金': '银白色',
        '水': '海蓝色'
    }
    
    # 前世职业
    vocations = [
        '僧人/道士', '书生/文人', '商人', '工匠', '医者',
        '官员/仕绅', '画家/艺术家', '农民', '武将/侠客', '隐士'
    ]
    
    # 修行境界
    realms = [
        '道观古刹', '山林隐居', '书院学堂', '宫廷府邸',
        '市井街巷', '江湖武林', '田园农舍', '手工作坊'
    ]
    
    return {
        'day_master': day_master,
        'five_elements': five_elements,
        'soul_color': element_colors.get(day_master, '金色'),
        'past_life_vocation': random.choice(vocations),
        'spiritual_realm': random.choice(realms)
    }

def infer_partner_traits_from_bazi(bazi_data, user_gender):
    """
    根据八字推断配偶特征
    简化版本：男命看妻星，女命看夫星
    """
    import random
    random.seed(bazi_data.get('birth_year', 1995) + 100)
    
    partner_gender = '女' if user_gender in ['男', '男命'] else '男'
    
    # 配偶五行（与日主相生相合为佳）
    day_master = infer_soul_traits_from_bazi(bazi_data)['day_master']
    element_flow = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
    partner_element = element_flow.get(day_master, '木')
    
    # 性格描述池
    if partner_gender == '女':
        personalities = [
            '温柔善良，体贴入微', '聪明伶俐，独立自信', '贤淑端庄，持家有道',
            '活泼开朗，乐观积极', '内敛含蓄，温婉如水', '干练果断，女中豪杰'
        ]
        appearances = [
            '清秀文雅，气质如兰', '明眸皓齿，温婉可人', '端庄大气，仪态万千',
            '活泼可爱，灵动俏皮', '知性优雅，成熟稳重', '清丽脱俗，不染尘埃'
        ]
    else:
        personalities = [
            '成熟稳重，责任心强', '温文尔雅，才华横溢', '幽默风趣，乐观开朗',
            '正直善良，顶天立地', '内敛深沉，思想深邃', '果敢坚毅，拼搏进取'
        ]
        appearances = [
            '剑眉星目，气宇轩昂', '温润如玉，谦谦君子', '棱角分明，硬朗帅气',
            '清逸俊朗，气质不凡', '成熟魅力，沉稳内敛', '阳光活力，健康帅气'
        ]
    
    # 桃花色
    aura_colors = ['暖白色', '粉红色', '浅金色', '淡蓝色', '翠绿色', '紫色']
    
    # 合盘生肖
    zodiac_combos = {
        '鼠': '龙/猴/牛', '牛': '蛇/鸡/鼠', '虎': '马/狗/猪',
        '兔': '羊/猪/狗', '龙': '猴/鼠/鸡', '蛇': '鸡/牛/猴',
        '马': '狗/虎/羊', '羊': '兔/猪/马', '猴': '龙/鼠/蛇',
        '鸡': '蛇/龙/牛', '狗': '虎/马/兔', '猪': '兔/羊/虎'
    }
    
    birth_zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    zodiac_idx = bazi_data.get('birth_month', 1) % 12
    birth_zodiac = birth_zodiacs[zodiac_idx]
    
    return {
        'gender': partner_gender,
        'element': partner_element,
        'personality': random.choice(personalities),
        'appearance': random.choice(appearances),
        'aura_color': random.choice(aura_colors),
        'zodiac': zodiac_combos.get(birth_zodiac, '兔/羊')
    }

def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  前世画像: portrait_generator.py past_life '<JSON数据>'")
        print("  未来伴侣: portrait_generator.py future_partner '<JSON数据>'")
        print("\n示例:")
        print("  portrait_generator.py past_life '{\"name\":\"张三\",\"birth_year\":1995,\"birth_month\":7}'")
        print("  portrait_generator.py future_partner '{\"name\":\"张三\",\"birth_year\":1995,\"birth_month\":7,\"gender\":\"男\"}'")
        sys.exit(1)
    
    cmd = sys.argv[1]
    try:
        bazi_info = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print("错误: 无效的JSON格式")
        sys.exit(1)
    
    name = bazi_info.get('name', '用户')
    
    if cmd == "past_life":
        print(f"🔮 正在推算 {name} 的前世因果...")
        soul_traits = infer_soul_traits_from_bazi(bazi_info)
        
        print(f"\n📜 灵魂特质分析:")
        print(f"   日主五行: {soul_traits['day_master']}性")
        print(f"   灵魂颜色: {soul_traits['soul_color']}")
        print(f"   前世职业: {soul_traits['past_life_vocation']}")
        print(f"   修行境界: {soul_traits['spiritual_realm']}")
        print(f"   五行分布: 木{soul_traits['five_elements']['wood']} 火{soul_traits['five_elements']['fire']} 土{soul_traits['five_elements']['earth']} 金{soul_traits['five_elements']['metal']} 水{soul_traits['five_elements']['water']}")
        
        prompt = generate_past_life_prompt(bazi_info, soul_traits)
        img_type = "前世画像"
        
    elif cmd == "future_partner":
        user_gender = bazi_info.get('gender', '男')
        print(f"🔮 正在推算 {name} 的未来伴侣...")
        partner_traits = infer_partner_traits_from_bazi(bazi_info, user_gender)
        
        print(f"\n💕 伴侣特征分析:")
        print(f"   性别取向: {partner_traits['gender']}性")
        print(f"   五行属性: {partner_traits['element']}")
        print(f"   性格特点: {partner_traits['personality']}")
        print(f"   外貌特征: {partner_traits['appearance']}")
        print(f"   灵魂颜色: {partner_traits['aura_color']}")
        print(f"   合盘生肖: {partner_traits['zodiac']}")
        
        prompt = generate_future_partner_prompt(bazi_info, partner_traits)
        img_type = "未来伴侣"
        
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
    
    print(f"\n🎨 正在生成{img_type}...")
    result = call_minimax_image(prompt, aspect_ratio="1:1", n=1)
    
    if "error" in result:
        print(f"❌ 生成失败: {result['error']}")
        sys.exit(1)
    
    image_urls = result.get('data', {}).get('image_urls', [])
    if image_urls:
        print(f"\n✅ {img_type}生成成功!")
        print(f"🔗 图片链接（24小时内有效）: {image_urls[0]}")
        
        output_file = f"/tmp/portrait_{cmd}_{name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "name": name,
                "type": cmd,
                "image_url": image_urls[0],
                "generated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存到: {output_file}")
    else:
        print("❌ 生成失败: 未获取到图片URL")
        sys.exit(1)

if __name__ == "__main__":
    main()
