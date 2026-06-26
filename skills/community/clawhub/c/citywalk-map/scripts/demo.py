#!/usr/bin/env python3
"""
Citywalk Map Demo Script
Run example routes to see the generator in action.
"""
import subprocess
import os
import sys

DEMOS = {
    'haikou': {
        'title': '海口万绿园 → 观海台 海岸漫步',
        'route': (
            '20.0352,110.3104,万绿园（起点）,海南最大热带海滨公园，椰林大道超适合拍照|'
            '20.0340,110.2931,海口湾公园,沿海健身步道，有休闲长椅可以歇脚看海|'
            '20.0315,110.2468,观海台（折返点）,百年钟楼，登顶俯瞰整个海口湾'
        ),
        'color': '#e94560',
    },
    'london': {
        'title': '伦敦经典5小时徒步路线',
        'route': (
            '51.5055,-0.0754,Tower Bridge（起点）,伦敦标志性地标，桥塔可登顶俯瞰|'
            '51.5138,-0.0984,St Pauls Cathedral,圣保罗大教堂，穹顶震撼，登顶看全城|'
            '51.5117,-0.1223,Covent Garden,最文艺广场，街头表演超赞，美食多|'
            '51.5080,-0.1277,Trafalgar Square,特拉法加广场，国家美术馆旁|'
            '51.5014,-0.1419,Buckingham Palace,白金汉宫，11:30换岗仪式|'
            '51.5007,-0.1246,Big Ben & Parliament,大本钟+国会大厦，伦敦最经典'
        ),
        'color': '#1a3a5c',
    },
    'paris': {
        'title': '巴黎经典1日路线',
        'route': (
            '48.8584,2.2945,埃菲尔铁塔（起点）,巴黎地标，登顶俯瞰全城|'
            '48.8606,2.3376,卢浮宫,世界最大博物馆|'
            '48.8530,2.3499,巴黎圣母院,哥特式建筑典范|'
            '48.8867,2.3206,蒙马特高地,艺术街区，俯瞰巴黎全景'
        ),
        'color': '#8b5cf6',
    },
}


def run_demo(name):
    demo = DEMOS[name]
    print(f"\n{'='*50}")
    print(f"Running demo: {name}")
    print(f"Title: {demo['title']}")
    print(f"Color: {demo['color']}")
    print('='*50)
    
    env = os.environ.copy()
    env['COLOR'] = demo['color']
    
    result = subprocess.run(
        ['python3', __file__.replace('/demo.py', '/generate.py'), demo['title'], demo['route']],
        env=env,
        capture_output=False,
    )
    print(f"\n✅ Demo '{name}' complete!")
    print(f"📍 Output: /tmp/citywalk_map.html")
    print(f"🌐 Open with: open /tmp/citywalk_map.html")


def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in DEMOS:
            run_demo(name)
        else:
            print(f"Unknown demo: {name}")
            print(f"Available: {', '.join(DEMOS.keys())}")
    else:
        print("Citywalk Map Demo Script")
        print("=" * 40)
        print("Usage: python3 demo.py <demo-name>")
        print()
        print("Available demos:")
        for name, demo in DEMOS.items():
            print(f"  • {name}: {demo['title']}")
        print()
        print("Example:")
        print("  python3 demo.py haikou")


if __name__ == '__main__':
    main()
