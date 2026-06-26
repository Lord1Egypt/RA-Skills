#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美食推荐器
核心推荐逻辑
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 尝试加载.env文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from baidu_map_client import BaiduMapClient


class FoodRecommender:
    """美食推荐器"""
    
    # 用餐场景映射
    MEAL_SCENES = {
        'breakfast': {'name': '早餐', 'keywords': ['早餐', '早点', '包子', '豆浆'], 'hours': (6, 10)},
        'lunch': {'name': '午餐', 'keywords': ['午餐', '快餐', '商务餐'], 'hours': (11, 14)},
        'dinner': {'name': '晚餐', 'keywords': ['晚餐', '美食', '餐厅'], 'hours': (17, 21)},
        'tea': {'name': '下午茶', 'keywords': ['咖啡', '甜品', '下午茶'], 'hours': (14, 17)},
        'supper': {'name': '夜宵', 'keywords': ['烧烤', '夜宵', '大排档'], 'hours': (21, 24)}
    }
    
    # 美食类型关键词映射
    FOOD_TYPE_KEYWORDS = {
        '火锅': '火锅',
        '日料': '日本料理',
        '日餐': '日本料理',
        '寿司': '日本料理',
        '川菜': '川菜',
        '辣': '川菜 湘菜',
        '烧烤': '烧烤',
        '烤串': '烧烤',
        '西餐': '西餐',
        '汉堡': '西餐 快餐',
        '粤菜': '粤菜',
        '茶餐厅': '茶餐厅',
        '小吃': '小吃',
        '快餐': '快餐',
        '杭帮菜': '杭帮菜',
        '江浙菜': '江浙菜',
        '面食': '面馆 面食',
        '咖啡': '咖啡',
        '甜品': '甜品'
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化推荐器
        
        Args:
            api_key: 百度地图API Key
        """
        self.api_key = api_key
        self.client = None
        self.api_available = False
        
        # 尝试初始化客户端（不传AK，让BaiduMapClient自己获取）
        try:
            self.client = BaiduMapClient(api_key)  # 传None让客户端自己读取
            self.api_key = self.client.api_key  # 获取实际使用的AK
            self.api_available = True
        except ValueError as e:
            print(f"API客户端初始化失败: {e}")
        
        # 加载本地兜底数据
        self.fallback_data = self._load_fallback_data()
    
    def _load_fallback_data(self) -> Dict:
        """加载本地兜底数据"""
        data_path = os.path.join(
            os.path.dirname(__file__), 
            'data', 
            'city_food_db.json'
        )
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"加载兜底数据失败: {e}")
            return {'cities': {}}
    
    def get_current_meal_scene(self) -> str:
        """
        根据当前时间判断用餐场景
        
        Returns:
            场景key：breakfast/lunch/dinner/tea/supper
        """
        hour = datetime.now().hour
        
        for scene_key, scene_info in self.MEAL_SCENES.items():
            start, end = scene_info['hours']
            if start <= hour < end:
                return scene_key
        
        # 默认返回晚餐
        return 'dinner'
    
    def get_meal_scene_name(self, scene_key: str) -> str:
        """获取用餐场景名称"""
        return self.MEAL_SCENES.get(scene_key, {}).get('name', '美食')
    
    def get_search_keyword(
        self, 
        food_type: Optional[str] = None, 
        meal_scene: Optional[str] = None
    ) -> str:
        """
        生成搜索关键词
        
        Args:
            food_type: 用户指定的美食类型
            meal_scene: 用餐场景
            
        Returns:
            搜索关键词
        """
        keywords = []
        
        # 优先使用用户指定的类型
        if food_type:
            # 查找关键词映射
            for key, value in self.FOOD_TYPE_KEYWORDS.items():
                if key in food_type:
                    keywords.append(value)
                    break
            else:
                keywords.append(food_type)
        
        # 根据用餐场景补充
        if meal_scene and meal_scene in self.MEAL_SCENES:
            scene_keywords = self.MEAL_SCENES[meal_scene]['keywords']
            if not keywords:
                keywords.extend(scene_keywords[:2])
        
        # 默认搜索美食
        if not keywords:
            keywords.append('美食')
        
        return ' '.join(keywords) if isinstance(keywords, list) else keywords
    
    def recommend(
        self,
        address: str,
        food_type: Optional[str] = None,
        budget: Optional[str] = None,
        meal_scene: Optional[str] = None,
        radius: int = 2000
    ) -> Dict:
        """
        推荐餐厅
        
        Args:
            address: 用户输入的地址
            food_type: 美食类型（如"火锅"、"日料"）
            budget: 预算范围（如"100-200"）
            meal_scene: 用餐场景（breakfast/lunch/dinner/tea/supper）
            radius: 搜索半径（米）
            
        Returns:
            推荐结果字典
        """
        # 如果没有指定用餐场景，自动判断
        if not meal_scene:
            meal_scene = self.get_current_meal_scene()
        
        result = {
            'success': False,
            'address': address,
            'meal_scene': self.get_meal_scene_name(meal_scene),
            'food_type': food_type or '不限',
            'budget': budget or '不限',
            'restaurants': [],
            'message': ''
        }
        
        # 检查API可用性
        if not self.api_available:
            print("API不可用，使用兜底方案")
            fallback_result = self._fallback_recommend(address)
            result.update(fallback_result)
            return result
        
        # 步骤1：地理编码
        print(f"正在定位: {address}")
        location = self.client.geocode(address)
        
        if not location:
            result['message'] = f'无法识别位置: {address}，请尝试更详细的地址描述'
            fallback_result = self._fallback_recommend(address)
            result.update(fallback_result)
            return result
        
        result['location'] = {
            'latitude': location[0],
            'longitude': location[1]
        }
        
        # 步骤2：生成搜索关键词
        keyword = self.get_search_keyword(food_type, meal_scene)
        print(f"搜索关键词: {keyword}")
        
        # 步骤3：搜索餐厅
        print(f"正在搜索半径{radius}米内的餐厅...")
        raw_restaurants = self.client.search_nearby(
            location, 
            keyword=keyword, 
            radius=radius, 
            page_size=15
        )
        
        if not raw_restaurants:
            # 扩大搜索范围重试
            print("未找到结果，扩大搜索范围...")
            raw_restaurants = self.client.search_nearby(
                location, 
                keyword='美食', 
                radius=5000, 
                page_size=15
            )
        
        if not raw_restaurants:
            result['message'] = '附近没有找到符合条件的餐厅'
            fallback_result = self._fallback_recommend(address)
            result.update(fallback_result)
            return result
        
        # 步骤4：解析和排序
        restaurants = []
        for raw in raw_restaurants:
            info = self.client.parse_restaurant_info(raw)
            # 计算综合得分（评分 + 距离权重）
            score = self._calculate_score(info)
            info['score'] = score
            restaurants.append(info)
        
        # 按得分排序
        restaurants.sort(key=lambda x: x['score'], reverse=True)
        
        # 步骤5：格式化输出
        result['success'] = True
        result['restaurants'] = restaurants[:5]  # 取前5
        result['total_found'] = len(raw_restaurants)
        result['message'] = f'找到 {len(raw_restaurants)} 家餐厅，为你推荐前 {len(result["restaurants"])} 家'
        
        return result
    
    def _calculate_score(self, restaurant: Dict) -> float:
        """
        计算餐厅推荐得分
        
        Args:
            restaurant: 餐厅信息
            
        Returns:
            得分（越高越好）
        """
        score = 0.0
        
        # 评分权重（最高5分）
        try:
            rating = float(restaurant.get('rating', 0))
            score += rating
        except (ValueError, TypeError):
            pass
        
        # 距离权重（越近越好，最高3分）
        try:
            distance = float(restaurant.get('distance', 99999))
            if distance < 500:
                score += 3
            elif distance < 1000:
                score += 2
            elif distance < 2000:
                score += 1
        except (ValueError, TypeError):
            pass
        
        # 有价格信息的加分
        if restaurant.get('price') and restaurant['price'] != '未知':
            score += 0.5
        
        return score
    
    def format_recommendation(self, result: Dict) -> str:
        """
        格式化推荐结果为可读文本
        
        Args:
            result: recommend()返回的结果字典
            
        Returns:
            格式化后的推荐文本
        """
        if not result['success']:
            return f"抱歉，{result['message']}"
        
        lines = []
        
        # 头部信息
        lines.append(f"📍 位置：{result['address']} 附近（半径2km）")
        lines.append(f"🕐 用餐场景：{result['meal_scene']} | 🔍 类型：{result['food_type']} | 💰 预算：{result['budget']}")
        lines.append("")
        lines.append(f"🏆 TOP {len(result['restaurants'])} 推荐")
        lines.append("")
        
        # 餐厅列表
        medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
        
        for i, restaurant in enumerate(result['restaurants']):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            lines.extend(self._format_single_restaurant(restaurant, medal))
            lines.append("")
        
        # 底部提示
        lines.append("---")
        lines.append("💡 小贴士：")
        lines.append("• 建议提前电话确认营业时间和排队情况")
        lines.append("• 节假日建议预约，避免长时间等待")
        lines.append("• 以上信息来自百度地图，可能存在滞后，出行前请二次确认")
        
        return "\n".join(lines)
    
    def _format_single_restaurant(self, restaurant: Dict, medal: str) -> List[str]:
        """
        格式化单个餐厅信息
        
        Args:
            restaurant: 餐厅数据字典
            medal: 排名奖牌
            
        Returns:
            格式化后的字符串列表
        """
        lines = []
        
        # 基本信息
        name = restaurant.get('name', '未知餐厅')
        tag = restaurant.get('tag', '美食')
        lines.append(f"{medal} {name}（{tag}）")
        
        # 评分和价格
        rating = restaurant.get('rating', '暂无')
        price = restaurant.get('price', '未知')
        distance = restaurant.get('distance', 0)
        
        # 转换距离为步行时间（假设步行速度5km/h）
        try:
            distance_num = float(distance) if distance and distance != '未知' else 0
            walk_time = int(distance_num / 83) if distance_num else 0  # 约83米/分钟
            distance_str = f"{int(distance_num)}m" if distance_num else "未知"
        except (ValueError, TypeError):
            distance_str = str(distance) if distance else "未知"
            walk_time = 0
        
        lines.append(f"   ⭐评分：{rating}/5  💰人均：¥{price}  📍距离：{distance_str}（步行约{walk_time}分钟）")
        
        # 地址和电话
        address = restaurant.get('address', '地址未知')
        telephone = restaurant.get('telephone', '')
        lines.append(f"   📍地址：{address}")
        if telephone:
            lines.append(f"   📞电话：{telephone}")
        
        # 推荐理由（简单版，后续可扩展）
        if rating != '暂无' and float(rating) >= 4.5:
            lines.append(f"   💡推荐理由：评分很高，深受食客喜爱")
        elif distance and distance < 500:
            lines.append(f"   💡推荐理由：距离超近，步行几分钟就到")
        
        return lines
    
    def _fallback_recommend(self, address: str) -> Dict:
        """
        兜底推荐：当API不可用时使用本地数据
        
        Args:
            address: 用户输入的地址（用于提取城市名）
            
        Returns:
            推荐结果字典
        """
        result = {
            'success': True,
            'message': '网络查询暂时不可用，为你推荐该城市的知名美食',
            'restaurants': [],
            'is_fallback': True
        }
        
        # 从地址中提取城市名（简化处理）
        city = self._extract_city_from_address(address)
        
        cities_data = self.fallback_data.get('cities', {})
        city_data = cities_data.get(city)
        
        if city_data:
            # 转换本地数据为统一格式
            for restaurant in city_data.get('famous_restaurants', [])[:5]:
                result['restaurants'].append({
                    'name': restaurant['name'],
                    'tag': restaurant['type'],
                    'rating': '4.5',  # 默认高分
                    'price': restaurant['budget'].replace('人均', '').replace('元', ''),
                    'distance': '未知',
                    'address': f"{city} {restaurant['area']}",
                    'telephone': '',
                    'description': restaurant.get('description', '')
                })
            
            # 添加特色菜信息
            specialties = city_data.get('specialties', [])
            if specialties:
                result['message'] += f"\n🍜 {city}特色美食：{', '.join(specialties[:5])}"
        else:
            # 未知城市，返回通用提示
            result['restaurants'] = [{
                'name': '建议查询当地美食攻略',
                'tag': '未知',
                'rating': '暂无',
                'price': '未知',
                'distance': '未知',
                'address': f'{city}（该城市数据暂不完善）',
                'telephone': ''
            }]
        
        return result
    
    def _extract_city_from_address(self, address: str) -> str:
        """
        从地址中提取城市名（简化版）
        
        Args:
            address: 地址字符串
            
        Returns:
            城市名
        """
        # 常见城市列表
        common_cities = [
            '北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉',
            '西安', '重庆', '天津', '苏州', '长沙', '郑州', '青岛', '厦门',
            '宁波', '无锡', '佛山', '东莞', '大连', '沈阳', '济南', '哈尔滨'
        ]
        
        for city in common_cities:
            if city in address:
                return city
        
        # 如果找不到，返回地址前两个字作为猜测
        return address[:2] if len(address) >= 2 else address


# 测试代码
if __name__ == "__main__":
    import os
    import sys
    
    # 设置UTF-8编码（Windows兼容）
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 解析命令行参数
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🍜 美食探店助手 - 帮你发现附近美食',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s                              # 交互式模式
  %(prog)s -l "杭州文三路"               # 搜索文三路附近美食
  %(prog)s -l "杭州西湖" -t "杭帮菜"     # 搜索西湖附近杭帮菜
  %(prog)s -l "成都春熙路" -t "火锅" -r 3000  # 搜索3公里内火锅
        '''
    )
    
    parser.add_argument(
        '-l', '--location',
        type=str,
        help='你的位置（如：杭州文三路、上海陆家嘴）'
    )
    
    parser.add_argument(
        '-t', '--type',
        type=str,
        default=None,
        help='美食类型（如：火锅、日料、川菜、小吃，默认不限）'
    )
    
    parser.add_argument(
        '-b', '--budget',
        type=str,
        default=None,
        help='预算范围（如：50-100，默认不限）'
    )
    
    parser.add_argument(
        '-r', '--radius',
        type=int,
        default=2000,
        help='搜索半径（米，默认2000）'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='运行默认测试案例'
    )
    
    args = parser.parse_args()
    
    # 初始化推荐器
    api_key = os.environ.get('BAIDU_MAP_API_KEY')
    recommender = FoodRecommender(api_key)
    
    if args.test:
        # 运行测试模式
        print("=== 美食探店助手测试 ===\n")
        
        test_cases = [
            {"address": "杭州西湖断桥", "food_type": "杭帮菜"},
            {"address": "上海陆家嘴", "food_type": None},
            {"address": "成都春熙路", "food_type": "火锅"},
        ]
        
        for case in test_cases:
            print(f"\n{'='*50}")
            print(f"测试: {case['address']} | {case['food_type'] or '不限类型'}")
            print('='*50)
            
            result = recommender.recommend(
                address=case['address'],
                food_type=case['food_type']
            )
            
            output = recommender.format_recommendation(result)
            print(output)
            print()
    
    elif args.location:
        # 命令行模式
        print(f"🍜 正在为你搜索：{args.location}")
        if args.type:
            print(f"   美食类型：{args.type}")
        print()
        
        result = recommender.recommend(
            address=args.location,
            food_type=args.type,
            budget=args.budget,
            radius=args.radius
        )
        
        output = recommender.format_recommendation(result)
        print(output)
    
    else:
        # 交互式模式
        print("🍜 欢迎来到美食探店助手！\n")
        
        # 询问位置
        location = input("📍 你在哪里？（如：杭州文三路、上海陆家嘴）：").strip()
        if not location:
            print("❌ 位置不能为空")
            sys.exit(1)
        
        # 询问类型
        food_type = input("🍽️ 想吃什么类型？（直接回车表示不限）：").strip()
        if not food_type:
            food_type = None
        
        # 询问预算
        budget = input("💰 预算范围？（如：50-100，直接回车表示不限）：").strip()
        if not budget:
            budget = None
        
        print(f"\n🔍 正在搜索：{location} 附近的美食...\n")
        
        result = recommender.recommend(
            address=location,
            food_type=food_type,
            budget=budget
        )
        
        output = recommender.format_recommendation(result)
        print(output)
