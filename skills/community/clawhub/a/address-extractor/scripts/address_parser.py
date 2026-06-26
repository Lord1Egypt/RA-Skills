#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地址解析和标准化工具
用于从文本中提取、清洗、标准化地址信息，并调用高德地图API获取坐标
"""

import re
import json
import requests
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AddressExtractor:
    """地址提取器主类"""
    
    def __init__(self, amap_api_key: str = None):
        """
        初始化地址提取器
        
        Args:
            amap_api_key: 高德地图API密钥
        """
        self.amap_api_key = amap_api_key
        
        # 中国省份正则表达式模式
        self.province_pattern = r'(北京|天津|河北|山西|内蒙古|辽宁|吉林|黑龙江|上海|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|广西|海南|重庆|四川|贵州|云南|西藏|陕西|甘肃|青海|宁夏|新疆|台湾|香港|澳门)'
        
        # 城市模式（包含直辖市、副省级城市、地级市等）
        self.city_pattern = r'([\u4e00-\u9fa5]{2,8}?(?:市|州|地区|盟|自治州))'
        
        # 区县模式
        self.district_pattern = r'([\u4e00-\u9fa5]{2,10}?(?:区|县|市|自治县|旗|自治旗))'
        
        # 乡镇街道模式
        self.town_pattern = r'([\u4e00-\u9fa5]{2,15}?(?:镇|乡|街道|苏木|民族乡))'
        
        # 村庄社区模式
        self.village_pattern = r'([\u4e00-\u9fa5]{2,20}?(?:村|社区|居委会|大队|组|巷|弄))'
        
        # 道路模式
        self.road_pattern = r'([\u4e00-\u9fa5\d]+?(?:路|街|大道|胡同|弄|巷|条|里))'
        
        # 门牌号模式
        self.house_number_pattern = r'[\u4e00-\u9fa5]?[\d\-]+[\u4e00-\u9fa5]?号?'
        
        # 楼栋号模式
        self.building_pattern = r'[\u4e00-\u9fa5]?[\d]+[\u4e00-\u9fa5]*(?:栋|号楼|幢|座|单元)'
        
        # 特殊字符过滤模式
        self.special_chars_pattern = r'[【】()（）[]{}<>《》""''「」『』\s]*'
        
        # 无效备注模式
        self.invalid_notes_pattern = r'(?:备注|说明|注意|提示|联系|电话|手机|邮箱|QQ|微信|联系人|姓名|年龄|性别|备注信息|补充说明)[：:][^，。；\n]*'
    
    def clean_text(self, text: str) -> str:
        """
        清洗文本，去除特殊字符和无效备注
        
        Args:
            text: 原始文本
            
        Returns:
            清洗后的文本
        """
        if not text:
            return ""
            
        # 去除首尾空白
        cleaned = text.strip()
        
        # 去除无效备注信息
        cleaned = re.sub(self.invalid_notes_pattern, '', cleaned, flags=re.IGNORECASE)
        
        # 去除特殊字符（保留中文、英文、数字、基本标点）
        cleaned = re.sub(self.special_chars_pattern, ' ', cleaned)
        
        # 规范化空白字符
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # 去除多余的标点和空格
        cleaned = re.sub(r'[,，。；;\s]+', ',', cleaned)
        cleaned = cleaned.strip(',。；;')
        
        return cleaned
    
    def extract_address_components(self, text: str) -> Dict[str, str]:
        """
        从文本中提取地址组成部分
        
        Args:
            text: 输入文本
            
        Returns:
            地址组成字典
        """
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return {}
        
        components = {}
        
        # 提取省份
        province_match = re.search(self.province_pattern, cleaned_text)
        if province_match:
            components['province'] = province_match.group(1)
        
        # 提取城市
        city_match = re.search(self.city_pattern, cleaned_text)
        if city_match:
            components['city'] = city_match.group(1)
        
        # 提取区县
        district_match = re.search(self.district_pattern, cleaned_text)
        if district_match:
            components['district'] = district_match.group(1)
        
        # 提取乡镇街道
        town_match = re.search(self.town_pattern, cleaned_text)
        if town_match:
            components['town'] = town_match.group(1)
        
        # 提取村庄社区
        village_match = re.search(self.village_pattern, cleaned_text)
        if village_match:
            components['village'] = village_match.group(1)
        
        # 提取道路
        road_match = re.search(self.road_pattern, cleaned_text)
        if road_match:
            components['road'] = road_match.group(1)
        
        # 提取门牌号
        house_match = re.search(self.house_number_pattern, cleaned_text)
        if house_match:
            components['house_number'] = house_match.group(0)
        
        # 提取楼栋号
        building_match = re.search(self.building_pattern, cleaned_text)
        if building_match:
            components['building'] = building_match.group(0)
        
        # 提取POI（兴趣点）
        poi_patterns = [
            r'([\u4e00-\u9fa5]{2,20}?(?:大厦|大楼|广场|中心|商场|超市|医院|学校|酒店|宾馆|餐厅|银行|邮局|车站|机场|公园|小区|花园|苑|山庄))',
            r'([\u4e00-\u9fa5]{2,10}?(?:公司|企业|工厂|机构|部门|局|院|所))'
        ]
        
        for pattern in poi_patterns:
            poi_match = re.search(pattern, cleaned_text)
            if poi_match:
                components['poi'] = poi_match.group(1)
                break
        
        return components
    
    def standardize_address(self, components: Dict[str, str]) -> str:
        """
        将地址组件标准化为层级路径格式
        
        Args:
            components: 地址组件字典
            
        Returns:
            标准化的地址路径
        """
        parts = []
        
        # 按层级顺序组装地址
        if 'province' in components:
            parts.append(components['province'])
        if 'city' in components:
            parts.append(components['city'])
        if 'district' in components:
            parts.append(components['district'])
        if 'town' in components:
            parts.append(components['town'])
        if 'village' in components:
            parts.append(components['village'])
        
        # 道路和门牌号
        road_part = []
        if 'road' in components:
            road_part.append(components['road'])
        if 'house_number' in components:
            road_part.append(components['house_number'])
        if road_part:
            parts.append(''.join(road_part))
        
        # POI
        if 'poi' in components:
            parts.append(components['poi'])
        
        # 楼栋号（附加信息）
        building_info = []
        if 'building' in components:
            building_info.append(f"({components['building']})")
        
        standardized = '-'.join(parts)
        if building_info:
            standardized += ''.join(building_info)
        
        return standardized
    
    def build_amap_query(self, components: Dict[str, str]) -> str:
        """
        构建高德地图API查询地址
        
        Args:
            components: 地址组件字典
            
        Returns:
            查询地址字符串
        """
        query_parts = []
        
        # 优先使用最具体的地址信息
        if 'house_number' in components and 'road' in components:
            query_parts.extend([components['road'], components['house_number']])
        elif 'road' in components:
            query_parts.append(components['road'])
        
        if 'building' in components:
            query_parts.append(components['building'])
        
        if 'poi' in components:
            query_parts.append(components['poi'])
        
        # 添加行政区划信息以提高精度
        admin_parts = []
        for key in ['district', 'city', 'province']:
            if key in components:
                admin_parts.append(components[key])
        
        if admin_parts:
            query_parts.extend(reversed(admin_parts))  # 从具体到一般
        
        return ''.join(query_parts) if query_parts else ''
    
    def get_coordinates_from_amap(self, address: str) -> Optional[Dict[str, float]]:
        """
        调用高德地图API获取坐标
        
        Args:
            address: 查询地址
            
        Returns:
            坐标字典，包含lng和lat
        """
        if not self.amap_api_key:
            logger.warning("未设置高德地图API密钥")
            return None
        
        if not address:
            logger.warning("地址为空")
            return None
        
        try:
            # 高德地图地理编码API
            url = "https://restapi.amap.com/v3/geocode/geo"
            params = {
                'address': address,
                'key': self.amap_api_key,
                'output': 'json',
                'city': '',  # 让API自动判断城市
                'batch': 'false'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '1' and data.get('geocodes'):
                location = data['geocodes'][0]['location']
                lng, lat = location.split(',')
                return {
                    'lng': float(lng),
                    'lat': float(lat),
                    'formatted_address': data['geocodes'][0]['formatted_address']
                }
            else:
                logger.warning(f"高德API返回错误: {data.get('info', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求高德API失败: {e}")
            return None
        except Exception as e:
            logger.error(f"解析高德API响应失败: {e}")
            return None
    
    def extract_and_standardize(self, text: str) -> Dict:
        """
        完整的地址提取和标准化流程
        
        Args:
            text: 输入文本
            
        Returns:
            包含提取结果的字典
        """
        # 1. 清洗文本
        cleaned_text = self.clean_text(text)
        
        # 2. 提取地址组件
        components = self.extract_address_components(cleaned_text)
        
        if not components:
            return {
                'success': False,
                'error': '未能从文本中提取到有效地址信息',
                'original_text': text,
                'cleaned_text': cleaned_text
            }
        
        # 3. 标准化地址
        standardized_address = self.standardize_address(components)
        
        # 4. 构建API查询地址
        query_address = self.build_amap_query(components)
        
        result = {
            'success': True,
            'original_text': text,
            'cleaned_text': cleaned_text,
            'components': components,
            'standardized_address': standardized_address,
            'query_address': query_address,
            'coordinates': None
        }
        
        # 5. 获取坐标（如果配置了API密钥）
        if self.amap_api_key and query_address:
            coordinates = self.get_coordinates_from_amap(query_address)
            if coordinates:
                result['coordinates'] = coordinates
        
        return result

# 使用示例和测试函数
def test_address_extractor():
    """测试地址提取器"""
    
    # 示例文本
    test_cases = [
        "张三的联系方式是13800138000，住址：北京市朝阳区建国门外大街1号国贸大厦A座1208室",
        "会议地点：上海市浦东新区陆家嘴环路1000号恒生银行大厦25楼，备注：请提前15分钟到达",
        "收货地址：广东省深圳市南山区科技园南区深南大道9988号深圳湾1号T7栋2801",
        "【重要通知】客户李四，电话15912345678，地址：江苏省南京市鼓楼区中山北路30号南京银行大厦B栋15层",
        "项目现场：四川省成都市武侯区人民南路四段11号附1号大陆国际写字楼8楼"
    ]
    
    # 初始化提取器（需要配置实际的API密钥）
    extractor = AddressExtractor(amap_api_key="your-amap-api-key-here")
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n=== 测试用例 {i} ===")
        print(f"原文: {text}")
        
        result = extractor.extract_and_standardize(text)
        
        if result['success']:
            print(f"清洗后: {result['cleaned_text']}")
            print(f"地址组件: {json.dumps(result['components'], ensure_ascii=False, indent=2)}")
            print(f"标准化地址: {result['standardized_address']}")
            print(f"查询地址: {result['query_address']}")
            if result['coordinates']:
                print(f"坐标: {result['coordinates']['lng']}, {result['coordinates']['lat']}")
                print(f"格式化地址: {result['coordinates']['formatted_address']}")
            else:
                print("坐标: 未获取到（可能缺少API密钥或地址无法解析）")
        else:
            print(f"错误: {result['error']}")

if __name__ == "__main__":
    test_address_extractor()