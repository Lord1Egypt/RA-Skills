#!/usr/bin/env python3
"""
Food Calorie Calculator - 热量侦探
通过照片识别食物并计算卡路里
支持 Kimi 视觉识别 API
"""
import os
import re
import json
import requests
import yaml
import logging
from typing import Dict, List, Optional, Tuple
from PIL import Image
import base64
from io import BytesIO

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VisionRecognizer:
    """视觉识别模块 - 识别食物"""
    
    def __init__(self, provider: str = 'kimi', api_key: str = None, model: str = None, use_user_api: bool = False):
        self.provider = provider
        # Kimi 视觉识别模型
        self.model = model or os.environ.get('KIMI_MODEL', 'moonshot-v1-8k-vision-preview')
        
        # 支持用户使用自己的 API Key
        if use_user_api:
            self.api_key = api_key or os.environ.get('USER_KIMI_API_KEY')
            self.is_user_api = True
        else:
            self.api_key = api_key or os.environ.get('KIMI_API_KEY')
            self.is_user_api = False
    
    def recognize(self, image_path: str, user_description: str = None) -> Dict:
        """
        识别食物图片
        
        Args:
            image_path: 图片路径
            user_description: 用户描述（可选，如果提供则优先使用）
        
        Returns:
            {
                'foods': ['虾', '面包糠', '蒜蓉'],
                'description': '避风塘炒虾',
                'servings': {'虾': '200 克'},
                'confidence': 0.9,
                'source': 'kimi_vision'
            }
        """
        # 如果用户提供了描述，直接使用
        if user_description:
            logger.info("使用用户描述")
            return {
                'foods': self._parse_foods_from_description(user_description),
                'description': user_description,
                'servings': {},
                'confidence': 0.95,
                'source': 'user_description'
            }
        
        # 使用 Kimi 视觉识别
        return self._recognize_kimi(image_path)
    
    def _parse_foods_from_description(self, description: str) -> List[str]:
        """从用户描述中提取食物关键词"""
        food_keywords = ['虾', '鱼', '鸡', '猪', '牛', '羊', '米饭', '面条', '面包', '蛋', '菜', '土豆', '番茄', '蒜蓉', '面包糠']
        
        foods = []
        for keyword in food_keywords:
            if keyword in description:
                foods.append(keyword)
        
        return foods if foods else [description]
    
    def _recognize_kimi(self, image_path: str) -> Dict:
        """使用 Kimi 视觉识别 API"""
        import base64
        
        logger.info(f"使用 Kimi 视觉识别：{self.model}")
        
        with open(image_path, 'rb') as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请识别这是什么食物？列出主要食材。用中文简短回答。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        try:
            response = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 从文本中提取食物名称和食材
            # Kimi 返回格式："这是一道避风塘炒虾。...通常用面包糠、蒜末、辣椒等..."
            
            # 提取菜名
            dish_name = content.split('。')[0].replace('这是一道', '').replace('这是', '').strip()
            
            # 提取食材
            foods = self._parse_foods_from_description(content)
            
            return {
                'foods': foods,
                'description': dish_name,
                'servings': {},
                'confidence': 0.9,
                'source': 'kimi_vision'
            }
                
        except Exception as e:
            logger.error(f"Kimi 视觉识别失败：{e}")
            return {
                'foods': [],
                'description': '识别失败',
                'servings': {},
                'confidence': 0.5,
                'source': 'error',
                'error': str(e)
            }


class NutritionCalculator:
    """营养计算器 - 查询卡路里"""
    
    # 常见食物卡路里参考数据（每 100 克）
    COMMON_FOODS = {
        '米饭': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3},
        '面条': {'calories': 110, 'protein': 2.5, 'carbs': 25, 'fat': 0.5},
        '馒头': {'calories': 220, 'protein': 7, 'carbs': 47, 'fat': 1},
        '面包': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3},
        '面包糠': {'calories': 400, 'protein': 10, 'carbs': 70, 'fat': 8},
        '鸡蛋': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11},
        '牛奶': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1},
        '苹果': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2},
        '香蕉': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3},
        '鸡肉': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
        '猪肉': {'calories': 242, 'protein': 27, 'carbs': 0, 'fat': 14},
        '牛肉': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15},
        '羊肉': {'calories': 292, 'protein': 25, 'carbs': 0, 'fat': 20},
        '鱼': {'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 12},
        '虾': {'calories': 106, 'protein': 20, 'carbs': 1, 'fat': 1.7},
        '青菜': {'calories': 20, 'protein': 2, 'carbs': 3, 'fat': 0.3},
        '土豆': {'calories': 77, 'protein': 2, 'carbs': 17, 'fat': 0.1},
        '番茄': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2},
        '蒜蓉': {'calories': 150, 'protein': 6, 'carbs': 33, 'fat': 0.5},
        '烹饪油': {'calories': 900, 'protein': 0, 'carbs': 0, 'fat': 100},
        '油炸食品': {'calories': 300, 'protein': 10, 'carbs': 20, 'fat': 20},
    }
    
    def __init__(self, provider: str = 'local'):
        self.provider = provider
    
    def calculate(self, foods: List[str], servings: Dict = None) -> Dict:
        """计算食物的卡路里和营养"""
        return self._calculate_local(foods, servings)
    
    def _calculate_local(self, foods: List[str], servings: Dict = None) -> Dict:
        """使用本地数据库计算"""
        items = []
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        # 默认每样食材 100 克
        default_serving = 100  # 克
        
        for food in foods:
            nutrition = self._find_food(food)
            
            if nutrition:
                # 使用默认份量（100 克）
                calories = nutrition['calories']
                protein = nutrition['protein']
                carbs = nutrition['carbs']
                fat = nutrition['fat']
                
                items.append({
                    'name': food,
                    'calories': calories,
                    'protein': protein,
                    'carbs': carbs,
                    'fat': fat,
                    'serving': f'{default_serving}克'
                })
                
                total_calories += calories
                total_protein += protein
                total_carbs += carbs
                total_fat += fat
        
        return {
            'total_calories': total_calories,
            'total_protein': round(total_protein, 1),
            'total_carbs': round(total_carbs, 1),
            'total_fat': round(total_fat, 1),
            'items': items
        }
    
    def _find_food(self, food_name: str) -> Optional[Dict]:
        """模糊查找食物"""
        food_name = food_name.lower()
        
        # 精确匹配
        if food_name in self.COMMON_FOODS:
            return self.COMMON_FOODS[food_name]
        
        # 模糊匹配
        for name, nutrition in self.COMMON_FOODS.items():
            if name in food_name or food_name in name:
                return nutrition
        
        # 默认值
        return {'calories': 150, 'protein': 10, 'carbs': 20, 'fat': 5}


class FoodCalorieCalculator:
    """食物卡路里计算器 - 主类"""
    
    def __init__(self, config_path: str = 'config/config.local.yaml', use_user_api: bool = False):
        # 优先加载本地配置（包含 API Key）
        import os
        local_config = 'config/config.local.yaml'
        if os.path.exists(local_config):
            config_path = local_config
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        vision_config = self.config.get('vision', {})
        api_keys = self.config.get('api_keys', {})
        
        self.recognizer = VisionRecognizer(
            provider=vision_config.get('provider', 'kimi'),
            api_key=api_keys.get('kimi'),
            model=vision_config.get('model', 'moonshot-v1-8k-vision-preview'),
            use_user_api=use_user_api
        )
        
        self.use_user_api = use_user_api
        
        nutrition_config = self.config.get('nutrition', {})
        self.calculator = NutritionCalculator(
            provider=nutrition_config.get('provider', 'local')
        )
    
    def analyze(self, image_path: str, user_description: str = None) -> Dict:
        """分析食物图片"""
        logger.info(f"开始分析图片：{image_path}")
        
        # 1. 识别食物
        recognition = self.recognizer.recognize(image_path, user_description)
        logger.info(f"识别结果：{recognition['foods']}")
        
        # 2. 计算营养
        nutrition = self.calculator.calculate(
            recognition['foods'],
            recognition.get('servings')
        )
        
        # 3. 生成报告
        report = self._generate_report(recognition, nutrition)
        
        return {
            'foods': recognition['foods'],
            'description': recognition['description'],
            'nutrition': nutrition,
            'report': report,
            'use_user_api': self.use_user_api,
            'source': recognition.get('source', 'unknown')
        }
    
    def _generate_report(self, recognition: Dict, nutrition: Dict) -> str:
        """生成营养报告"""
        source_text = "Kimi 视觉识别" if recognition.get('source') == 'kimi_vision' else "用户描述"
        
        lines = [
            "🕵️ **热量侦探 - 营养分析报告**",
            "",
            f"📝 {recognition['description']}",
            f"ℹ️ 识别方式：{source_text}",
            "",
            "📊 **营养分析**",
            "",
            f"🔥 总卡路里：**{nutrition['total_calories']} 大卡**",
            f"💪 蛋白质：{nutrition['total_protein']}g",
            f"🍚 碳水化合物：{nutrition['total_carbs']}g",
            f"🥑 脂肪：{nutrition['total_fat']}g",
            "",
            "📋 **详细分解**",
            ""
        ]
        
        for item in nutrition['items']:
            lines.append(f"• **{item['name']}** ({item['serving']})")
            lines.append(f"  - 卡路里：{item['calories']} 大卡")
            lines.append(f"  - 蛋白质：{item['protein']}g | 碳水：{item['carbs']}g | 脂肪：{item['fat']}g")
            lines.append("")
        
        lines.append("──────────────────────────────")
        lines.append("💡 温馨提示：以上数据为 AI 估算，实际营养含量可能因烹饪方式和食材差异而有所不同。")
        
        return '\n'.join(lines)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 src/calorie_calculator.py <图片路径> [--description '食物描述']")
        print("示例：")
        print("  python3 src/calorie_calculator.py food.jpg")
        print("  python3 src/calorie_calculator.py food.jpg --description '蒜蓉炸虾'")
        sys.exit(1)
    
    image_path = sys.argv[1]
    user_description = None
    
    if '--description' in sys.argv:
        idx = sys.argv.index('--description')
        if idx + 1 < len(sys.argv):
            user_description = sys.argv[idx + 1]
    
    if not os.path.exists(image_path):
        print(f"错误：图片文件不存在：{image_path}")
        sys.exit(1)
    
    calculator = FoodCalorieCalculator()
    result = calculator.analyze(image_path, user_description)
    print(result['report'])


if __name__ == "__main__":
    main()
