#!/usr/bin/env python3
import argparse
import random
import sys

# 1. 动物特征库（核心新增逻辑）
ANIMAL_FEATURES = {
    "pig": {
        "appearance": ["pink skin", "curly tail", "round body", "big snout"],
        "environment": ["muddy pen", "farmyard", "green pasture"],
        "action": ["eating corn", "rolling in mud", "oinking softly"]
    },
    "horse": {
        "appearance": ["shiny coat", "flowing mane", "muscular legs", "intelligent eyes"],
        "environment": ["sunlit meadow", "forest trail", "rural stable"],
        "action": ["galloping freely", "grazing on grass", "standing calmly"]
    },
    "cat": {
        "appearance": ["soft fur", "pointed ears", "fluffy tail", "slender body"],
        "environment": ["cozy windowsill", "garden fence", "warm couch"],
        "action": ["curled up napping", "chasing a butterfly", "purring loudly"]
    },
    "dog": {
        "appearance": ["wagging tail", "floppy ears", "shiny eyes", "strong paws"],
        "environment": ["backyard", "park bench", "cozy dog bed"],
        "action": ["fetching a ball", "wagging happily", "guarding the house"]
    },
    "bird": {
        "appearance": ["colorful feathers", "sharp beak", "light wings", "tiny claws"],
        "environment": ["tree branch", "green lawn", "bird feeder"],
        "action": ["singing loudly", "flying high", "pecking seeds"]
    }
}

# 2. 默认特征（处理未知动物）
DEFAULT_FEATURES = {
    "appearance": ["unique fur/feathers", "distinctive features"],
    "environment": ["natural habitat", "outdoor setting"],
    "action": ["moving calmly", "exploring surroundings"]
}

def validate_animal(animal: str) -> str:
    """3. 参数校验：过滤无效动物名称，返回标准化名称"""
    animal = animal.strip().lower()
    # 简单的脏数据过滤
    invalid_words = ["delete", "remove", "rm", "sudo", "bash", "sh"]
    if any(word in animal for word in invalid_words):
        raise ValueError(f"Invalid animal name: {animal} (contains restricted words)")
    # 未知动物返回默认
    return animal if animal in ANIMAL_FEATURES else "default"

def generate_detailed_description(animal: str, lang: str = "en") -> str:
    """生成带随机特征的详细描述（核心复杂逻辑）"""
    # 获取对应特征（未知动物用默认）
    features = ANIMAL_FEATURES.get(animal, DEFAULT_FEATURES)
    
    # 随机选择特征组合
    appearance = random.choice(features["appearance"])
    environment = random.choice(features["environment"])
    action = random.choice(features["action"])
    
    # 多语言支持
    if lang == "zh":
        descriptions = {
            "pig": f"这是一张小猪的图片：{appearance}，它在{environment}里{action}。",
            "horse": f"这是一张马的图片：{appearance}，它在{environment}里{action}。",
            "cat": f"这是一张猫咪的图片：{appearance}，它在{environment}里{action}。",
            "dog": f"这是一张狗狗的图片：{appearance}，它在{environment}里{action}。",
            "bird": f"这是一张小鸟的图片：{appearance}，它在{environment}里{action}。",
            "default": f"这是一张{animal}的图片：{appearance}，它在{environment}里{action}。"
        }
        return descriptions.get(animal, descriptions["default"])
    else:
        # 英文描述（默认）
        base_sentence = f"This is a picture of a {animal if animal != 'default' else 'mystery animal'}"
        return f"{base_sentence} with {appearance}, {action} in the {environment}."

def main():
    # 解析命令行参数（保留原参数，新增可选lang参数）
    parser = argparse.ArgumentParser(description='Generate detailed animal picture description')
    parser.add_argument('--animal', type=str, default='pig', help='Type of animal (default: pig)')
    parser.add_argument('--lang', type=str, default='en', choices=['en', 'zh'], help='Language (en/zh, default: en)')
    
    try:
        args = parser.parse_args()
        # 参数校验
        valid_animal = validate_animal(args.animal)
        # 生成详细描述
        description = generate_detailed_description(valid_animal, args.lang)
        # 输出结果（供Ironclaw捕获）
        print(description)
        sys.exit(0)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
