#!/usr/bin/env python3
"""
AI Density - 基础使用示例 / Basic Usage Examples
"""

from ai_density import detect_ai_content, AIDensityDetector

# 示例1: 快速检测
print("=" * 50)
print("示例1: 快速检测")
print("=" * 50)

text1 = """
人工智能是计算机科学的一个分支，它企图了解智能的实质，
并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
该领域的研究包括机器人、语言识别、图像识别、自然语言处理等。
"""

result = detect_ai_content(text1)
print(f"文本: {text1[:50]}...")
print(f"AI含量等级: {result.level}/10")
print(f"AI参与度得分: {result.score:.1f}")
print(f"置信度: {result.confidence:.1%}")
print(f"说明: {result.description}")
print()

# 示例2: 高级用法 - 查看各维度得分
print("=" * 50)
print("示例2: 高级用法 - 各维度分析")
print("=" * 50)

text2 = """
作为一个AI助手，我很乐意帮助你理解这个问题。
首先，我们需要从多个角度来看待这个现象。
其次，值得注意的是，这种情况在现实生活中很常见。
最后，综上所述，我们可以得出以下结论。
"""

detector = AIDensityDetector()
result2 = detector.detect(text2)

print(f"文本: {text2[:50]}...")
print(f"\n各维度得分:")
for dimension, score in result2.dimension_scores.items():
    print(f"  - {dimension}: {score:.1f}")
print()

# 示例3: 检测人工写作风格
print("=" * 50)
print("示例3: 检测人工写作风格")
print("=" * 50)

text3 = """
兄弟们，今天这事儿真给我整无语了！
我昨天那个项目，代码写到凌晨3点，结果早上发现有个bug...
你说气人不？不过还好最后解决了，就是头发又少了两根😂
下次再也不这么干了，真的，信我！
"""

result3 = detect_ai_content(text3)
print(f"文本: {text3[:50]}...")
print(f"AI含量等级: {result3.level}/10")
print(f"说明: {result3.description}")
print(f"提示: {result3.warning}")
