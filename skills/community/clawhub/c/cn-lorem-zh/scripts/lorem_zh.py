#!/usr/bin/env python3
import argparse, random, json

PARAGRAPHS = [
    "人工智能正在深刻改变各行各业的运作方式，从医疗诊断到金融风控，AI技术的应用场景日益广泛。",
    "数字化转型已成为企业发展的必然趋势，无论规模大小，都需要拥抱新技术才能在竞争中保持优势地位。",
    "用户体验是产品成功的核心要素之一，优秀的设计不仅要美观，更要注重可用性和可访问性。",
    "数据驱动的决策模式正在取代传统的经验判断，通过数据分析可以更精准地把握市场趋势和用户需求。",
    "云计算和边缘计算的结合为应用部署提供了更灵活的架构选择，企业可以根据实际需求选择最适合的方案。",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=3, help="Number of paragraphs")
    args = parser.parse_args()
    texts = [random.choice(PARAGRAPHS) for _ in range(args.count)]
    print(json.dumps({"paragraphs": texts, "count": args.count}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
