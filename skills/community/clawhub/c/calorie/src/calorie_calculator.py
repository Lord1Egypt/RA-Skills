#!/usr/bin/env python3
"""
Food Calorie Calculator
通过照片识别食物并计算卡路里
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
    
    def __init__(self, provider: str = 'kimi', api_key: str = None, model: str = None):
        self.provider = provider
        self.api_key = api_key or os.environ.get('KIMI_API_KEY') or os.environ.get('OPENAI_API_KEY')
        self.model = model or os.environ.get('KIMI_MODEL', 'moonshot-v1-auto')
        
    def recognize(self, image_path: str) -> Dict:
        """
        识别食物图片
        
        Returns:
            {
                'foods': ['米饭', '红烧肉', '青菜'],
                'description': '一碗米饭配红烧肉和炒青菜',
                'confidence': 0.95
            }
        """
        if self.provider == 'kimi':
            return self._recognize_kimi(image_path)
        elif self.provider == 'openai':
            return self._recognize_openai(image_path)
        elif self.provider == 'claude':
            return self._recognize_claude(image_path)
        elif self.provider == 'qwen':
            return self._recognize_qwen(image_path)
        else:
            raise ValueError(f"Unsupported vision provider: {self.provider}")
    
    def _encode_image(self, image_path: str) -> str:
        """将图片编码为 base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _recognize_kimi(self, image_path: str) -> Dict:
        """使用月之暗面 Kimi 识别"""
        import base64
        
        with open(image_path, 'rb') as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,  # 支持 k2.5, moonshot-v1-auto 等
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """请识别这张图片中的食物，并以 JSON 格式返回：
{
    "foods": ["食物 1", "食物 2", ...],
    "description": "简短描述这顿饭",
    "estimated_servings": {
        "食物 1": "1 碗",
        "食物 2": "100 克"
    }
}
只返回 JSON，不要其他内容。用中文回答。"""
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
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # 解析 JSON
        try:
            content = re.sub(r'```json\s*|\s*```', '', content)
            data = json.loads(content)
            return {
                'foods': data.get('foods', []),
                'description': data.get('description', ''),
                'servings': data.get('estimated_servings', {}),
                'confidence': 0.9
            }
        except Exception as e:
            logger.error(f"解析识别结果失败：{e}")
            return {
                'foods': [],
                'description': content,
                'servings': {},
                'confidence': 0.5
            }
    
    def _recognize_openai(self, image_path: str) -> Dict:
        """使用 OpenAI GPT-4V 识别"""
        import base64
        
        with open(image_path, 'rb') as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """请识别这张图片中的食物，并以 JSON 格式返回：
{
    "foods": ["食物 1", "食物 2", ...],
    "description": "简短描述这顿饭",
    "estimated_servings": {
        "食物 1": "1 碗",
        "食物 2": "100 克"
    }
}
只返回 JSON，不要其他内容。用中文回答。"""
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
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # 解析 JSON
        try:
            # 清理可能的 markdown 标记
            content = re.sub(r'```json\s*|\s*```', '', content)
            data = json.loads(content)
            return {
                'foods': data.get('foods', []),
                'description': data.get('description', ''),
                'servings': data.get('estimated_servings', {}),
                'confidence': 0.9
            }
        except Exception as e:
            logger.error(f"解析识别结果失败：{e}")
            return {
                'foods': [],
                'description': content,
                'servings': {},
                'confidence': 0.5
            }
    
    def _recognize_claude(self, image_path: str) -> Dict:
        """使用 Claude Vision 识别"""
        # TODO: 实现 Claude Vision API
        raise NotImplementedError("Claude Vision 暂未实现")
    
    def _recognize_qwen(self, image_path: str) -> Dict:
        """使用 Qwen-VL 识别"""
        # TODO: 实现 Qwen-VL API
        raise NotImplementedError("Qwen-VL 暂未实现")


class NutritionCalculator:
    """营养计算器 - 查询卡路里"""
    
    # 常见食物卡路里参考数据（每 100 克）
    COMMON_FOODS = {
        '米饭': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3},
        '面条': {'calories': 110, 'protein': 2.5, 'carbs': 25, 'fat': 0.5},
        '馒头': {'calories': 220, 'protein': 7, 'carbs': 47, 'fat': 1},
        '面包': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3},
        '鸡蛋': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11},
        '牛奶': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1},
        '苹果': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2},
        '香蕉': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3},
        '鸡肉': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
        '猪肉': {'calories': 242, 'protein': 27, 'carbs': 0, 'fat': 14},
        '牛肉': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15},
        '鱼': {'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 12},
        '青菜': {'calories': 20, 'protein': 2, 'carbs': 3, 'fat': 0.3},
        '土豆': {'calories': 77, 'protein': 2, 'carbs': 17, 'fat': 0.1},
        '番茄': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2},
    }
    
    def __init__(self, provider: str = 'local', app_id: str = None, api_key: str = None):
        self.provider = provider
        self.app_id = app_id or os.environ.get('NUTRITIONIX_APP_ID')
        self.api_key = api_key or os.environ.get('NUTRITIONIX_API_KEY')
    
    def calculate(self, foods: List[str], servings: Dict = None) -> Dict:
        """
        计算食物的卡路里和营养
        
        Args:
            foods: 食物列表
            servings: 份量字典，如 {'米饭': '1 碗', '鸡肉': '100 克'}
            
        Returns:
            {
                'total_calories': 500,
                'total_protein': 30,
                'total_carbs': 50,
                'total_fat': 15,
                'items': [
                    {'name': '米饭', 'calories': 200, 'serving': '1 碗'},
                    ...
                ]
            }
        """
        if self.provider == 'nutritionix' and self.app_id:
            return self._calculate_nutritionix(foods, servings)
        else:
            return self._calculate_local(foods, servings)
    
    def _calculate_local(self, foods: List[str], servings: Dict = None) -> Dict:
        """使用本地数据库计算"""
        items = []
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for food in foods:
            # 查找食物（模糊匹配）
            nutrition = self._find_food(food)
            
            if nutrition:
                # 估算份量（简化处理）
                serving = servings.get(food, '100 克') if servings else '100 克'
                multiplier = self._parse_serving(serving)
                
                calories = int(nutrition['calories'] * multiplier)
                protein = round(nutrition['protein'] * multiplier, 1)
                carbs = round(nutrition['carbs'] * multiplier, 1)
                fat = round(nutrition['fat'] * multiplier, 1)
                
                items.append({
                    'name': food,
                    'calories': calories,
                    'protein': protein,
                    'carbs': carbs,
                    'fat': fat,
                    'serving': serving
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
        
        # 返回默认值（估算）
        return {'calories': 100, 'protein': 5, 'carbs': 15, 'fat': 3}
    
    def _parse_serving(self, serving: str) -> float:
        """解析份量，返回倍数"""
        serving = serving.lower()
        
        # 提取数字
        numbers = re.findall(r'\d+\.?\d*', serving)
        if numbers:
            return float(numbers[0])
        
        # 常见份量估算
        if '碗' in serving:
            return 1.5  # 1 碗约 150 克
        elif '盘' in serving:
            return 2.0
        elif '个' in serving:
            return 1.0
        elif '杯' in serving:
            return 2.4
        elif '片' in serving:
            return 0.3
        else:
            return 1.0  # 默认 100 克
    
    def _calculate_nutritionix(self, foods: List[str], servings: Dict = None) -> Dict:
        """使用 Nutritionix API 计算"""
        # TODO: 实现 Nutritionix API 调用
        logger.info("使用本地数据库计算（Nutritionix API 暂未实现）")
        return self._calculate_local(foods, servings)


class FoodCalorieCalculator:
    """食物卡路里计算器 - 主类"""
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 初始化模块
        vision_config = self.config.get('vision', {})
        api_keys = self.config.get('api_keys', {})
        
        self.recognizer = VisionRecognizer(
            provider=vision_config.get('provider', 'openai'),
            api_key=api_keys.get('openai')
        )
        
        nutrition_config = self.config.get('nutrition', {})
        self.calculator = NutritionCalculator(
            provider=nutrition_config.get('provider', 'local'),
            app_id=api_keys.get('nutritionix_app_id'),
            api_key=api_keys.get('nutritionix_api_key')
        )
    
    def analyze(self, image_path: str) -> Dict:
        """
        分析食物图片
        
        Returns:
            {
                'foods': [...],
                'description': '...',
                'nutrition': {
                    'total_calories': 500,
                    'total_protein': 30,
                    ...
                },
                'report': '完整的营养报告文本'
            }
        """
        logger.info(f"开始分析图片：{image_path}")
        
        # 1. 识别食物
        recognition = self.recognizer.recognize(image_path)
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
            'report': report
        }
    
    def _generate_report(self, recognition: Dict, nutrition: Dict) -> str:
        """生成营养报告"""
        lines = [
            "🍽️ **食物识别结果**",
            "",
            f"📝 {recognition['description']}",
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
    """主函数 - 测试用"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 src/calorie_calculator.py <图片路径>")
        print("示例：python3 src/calorie_calculator.py data/food.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"错误：图片文件不存在：{image_path}")
        sys.exit(1)
    
    # 初始化计算器
    calculator = FoodCalorieCalculator()
    
    # 分析图片
    result = calculator.analyze(image_path)
    
    # 输出报告
    print(result['report'])


if __name__ == "__main__":
    main()
