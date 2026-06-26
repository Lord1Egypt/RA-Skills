import requests
import json
import time
import re
from typing import List, Dict, Optional, Any
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class BlockCitySkill:
    """BlockCity数据获取Skill - 用于从blockcity.vip获取城市排名和详细信息"""
    
    BASE_URL = "https://www.blockcity.vip"
    RANK_API = "/api/area/rankList"
    RANK_PAGE = "/pages/block/area"
    
    def __init__(self, use_cache: bool = True, cache_ttl: int = 300):
        """
        初始化Skill实例
        
        Args:
            use_cache: 是否启用缓存
            cache_ttl: 缓存有效期（秒）
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.blockcity.vip/pages/block/area"
        })
        
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        self._cached_data: Optional[List[Dict]] = None
        self._cache_time: float = 0
        
        self._mock_data = self._get_mock_data()
    
    def _get_mock_data(self) -> List[Dict]:
        """获取模拟数据（仅作为最后的fallback，前10个城市）"""
        cities_data = [
            {"areaName": "北京", "areaId": 1, "popularityBalance": 0, "population": 3903, "soldBlocks": 4875, "mayor": "", "viceMayor": ""},
            {"areaName": "杭州", "areaId": 2, "popularityBalance": 0, "population": 2786, "soldBlocks": 3749, "mayor": "", "viceMayor": ""},
            {"areaName": "中国数藏", "areaId": 3, "popularityBalance": 0, "population": 2498, "soldBlocks": 3121, "mayor": "", "viceMayor": ""},
            {"areaName": "上海", "areaId": 4, "popularityBalance": 0, "population": 2243, "soldBlocks": 3057, "mayor": "", "viceMayor": ""},
            {"areaName": "深圳", "areaId": 5, "popularityBalance": 0, "population": 2174, "soldBlocks": 3044, "mayor": "", "viceMayor": ""},
            {"areaName": "广州", "areaId": 6, "popularityBalance": 0, "population": 1394, "soldBlocks": 1907, "mayor": "", "viceMayor": ""},
            {"areaName": "成都", "areaId": 7, "popularityBalance": 0, "population": 1300, "soldBlocks": 1721, "mayor": "", "viceMayor": ""},
            {"areaName": "惠州", "areaId": 8, "popularityBalance": 0, "population": 1300, "soldBlocks": 1514, "mayor": "", "viceMayor": ""},
            {"areaName": "海口", "areaId": 9, "popularityBalance": 0, "population": 1167, "soldBlocks": 1451, "mayor": "", "viceMayor": ""},
            {"areaName": "重庆", "areaId": 10, "popularityBalance": 0, "population": 1089, "soldBlocks": 1434, "mayor": "", "viceMayor": ""},
        ]
        return cities_data
    
    def _parse_rank_page(self, html: str) -> List[Dict]:
        """
        解析排名页面获取200个城市数据
        
        Args:
            html: 网页HTML内容（备用）
            
        Returns:
            城市数据列表
        """
        cities = []
        
        # 优先尝试使用 Playwright 渲染页面获取数据
        if PLAYWRIGHT_AVAILABLE:
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    
                    # 导航到页面
                    page.goto(f"{self.BASE_URL}{self.RANK_PAGE}", wait_until="networkidle")
                    
                    # 等待数据加载（等待包含北京的元素出现）
                    try:
                        page.wait_for_selector("text=北京", timeout=5000)
                    except:
                        pass
                    
                    # 提取页面中的城市列表
                    # 查找包含排名、城市名、居民人数、开启区块的元素
                    items = page.query_selector_all(".item")
                    
                    if items:
                        for idx, item in enumerate(items, 1):
                            try:
                                # 尝试获取排名
                                rank_elem = item.query_selector(".rank, .rank4")
                                rank = idx
                                if rank_elem:
                                    rank_text = rank_elem.text_content().strip()
                                    if rank_text.isdigit():
                                        rank = int(rank_text)
                                
                                # 获取城市名、居民人数、开启区块
                                name = ""
                                population = 0
                                sold_blocks = 0
                                text_content = item.text_content().strip()
                                
                                # 文本格式是: 排名(1-3位)+城市名(中文)+居民人数(3-4位)+开启区块(3-4位)
                                # 例如: 
                                #   1北京39034875 (长度11)
                                #   16武汉9261239 (长度10)
                                #   20青岛578785 (长度9)
                                #   25哈尔滨484657 (长度11)
                                
                                # 第一步: 提取开头的排名数字
                                rank_match = re.match(r'^(\d+)', text_content)
                                if rank_match:
                                    rank_str = rank_match.group(1)
                                    remaining_after_rank = text_content[len(rank_str):]
                                    
                                    # 第二步: 从 remaining_after_rank 中提取城市名和后面的数字
                                    # 城市名是中文，后面跟着两个数字（居民人数+开启区块）
                                    # 找到所有中文和数字的分界点
                                    split_point = None
                                    for i in range(len(remaining_after_rank)):
                                        char = remaining_after_rank[i]
                                        # 如果当前字符是中文，下一个是数字，这就是城市名结束的地方
                                        if i < len(remaining_after_rank) - 1:
                                            if '\u4e00' <= char <= '\u9fff' and remaining_after_rank[i+1].isdigit():
                                                split_point = i + 1
                                                break
                                    
                                    if split_point:
                                        name = remaining_after_rank[:split_point]
                                        nums_part = remaining_after_rank[split_point:]
                                        
                                        # 第三步: 从 nums_part 中分割居民人数和开启区块
                                        # 尝试从中间分割，优先按 4+4, 3+4, 4+3, 3+3 的顺序尝试
                                        possible_splits = []
                                        n = len(nums_part)
                                        if n >= 6:  # 至少需要3+3
                                            # 尝试各种可能的分割方式
                                            for mid in [max(3, n-4), min(4, n-3), n//2]:
                                                if 3 <= mid <= n-3:
                                                    possible_splits.append((mid, n-mid))
                                        
                                        # 去重并尝试
                                        tried = set()
                                        for pop_len, sold_len in possible_splits:
                                            key = (pop_len, sold_len)
                                            if key in tried:
                                                continue
                                            tried.add(key)
                                            
                                            if pop_len + sold_len == len(nums_part):
                                                pop_str = nums_part[:pop_len]
                                                sold_str = nums_part[pop_len:]
                                                if pop_str.isdigit() and sold_str.isdigit():
                                                    population = int(pop_str)
                                                    sold_blocks = int(sold_str)
                                                    break
                                
                                if name:
                                    cities.append({
                                        "areaName": name,
                                        "areaId": idx,
                                        "popularityBalance": 0,
                                        "population": population,
                                        "soldBlocks": sold_blocks,
                                        "mayor": "",
                                        "viceMayor": ""
                                    })
                            except Exception as e:
                                print(f"解析第{idx}个城市失败: {e}")
                                continue
                    
                    browser.close()
                    
                    if cities:
                        print(f"Playwright成功解析到 {len(cities)} 个城市")
                        return cities[:200]  # 确保最多200个
                    
            except Exception as e:
                print(f"Playwright解析失败: {e}")
        
        # 如果 Playwright 不可用或失败，尝试传统方法
        print("尝试传统HTML解析方法...")
        
        # 从原始HTML尝试
        text = html
        
        # 使用正则表达式匹配: 数字 + 城市名 + 4位数字 + 4位数字
        pattern = r'(\d+)([\u4e00-\u9fa5]+)(\d{4})(\d{4})'
        matches = re.findall(pattern, text)
        
        if matches:
            for idx, match in enumerate(matches, 1):
                name = match[1]
                population = int(match[2])
                sold_blocks = int(match[3])
                
                cities.append({
                    "areaName": name,
                    "areaId": idx,
                    "popularityBalance": 0,
                    "population": population,
                    "soldBlocks": sold_blocks,
                    "mayor": "",
                    "viceMayor": ""
                })
        
        # 如果正则提取失败，尝试查找脚本中的JSON数据
        if not cities:
            try:
                script_pattern = r'<script[^>]*>([\s\S]*?)</script>'
                scripts = re.findall(script_pattern, html)
                
                for script in scripts:
                    if 'areaName' in script and 'population' in script:
                        json_pattern = r'\{[^{}]*"areaName"[^{}]*\}'
                        json_matches = re.findall(json_pattern, script)
                        for json_str in json_matches[:200]:
                            try:
                                city = json.loads(json_str)
                                cities.append(city)
                            except:
                                pass
                        if cities:
                            break
            except Exception as e:
                print(f"解析脚本JSON失败: {e}")
        
        return cities
    
    def _is_cache_valid(self) -> bool:
        """检查缓存是否有效"""
        if not self.use_cache or self._cached_data is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl
    
    def get_city_rank_list(self, area_id: int = 0, use_mock_on_error: bool = True) -> List[Dict[str, Any]]:
        """
        获取城市排名列表
        
        Args:
            area_id: 区域ID，默认为0获取全部城市
            use_mock_on_error: 出错时是否使用模拟数据
            
        Returns:
            城市列表，包含排名、名称、人气余额、人口、售卖区块数等信息
        """
        if self._is_cache_valid():
            return self._cached_data
        
        # 第一步：尝试调用API
        try:
            url = f"{self.BASE_URL}{self.RANK_API}"
            params = {"areaId": area_id}
            
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") == 0 and "data" in data:
                cities = data["data"]
                formatted = self._format_city_list(cities)
                
                if self.use_cache:
                    self._cached_data = formatted
                    self._cache_time = time.time()
                
                return formatted
            else:
                raise Exception(f"API返回错误: {data.get('msg', '未知错误')}")
                
        except Exception as e:
            print(f"API访问失败: {str(e)}，尝试访问网页获取")
        
        # 第二步：API失败，尝试访问网页解析（_parse_rank_page内部会用Playwright访问）
        try:
            cities = self._parse_rank_page("")  # 传递空字符串，_parse_rank_page会自己处理
            
            if cities:
                print(f"成功: 从网页解析到 {len(cities)} 个城市")
                formatted = self._format_city_list(cities)
                
                if self.use_cache:
                    self._cached_data = formatted
                    self._cache_time = time.time()
                
                return formatted
            else:
                print("警告: 网页解析失败，无数据")
                
        except Exception as page_error:
            print(f"网页访问失败: {str(page_error)}")
        
        # 第三步：网页也失败，使用模拟数据
        if use_mock_on_error:
            print("警告: 使用模拟数据")
            formatted = self._format_city_list(self._mock_data)
            if self.use_cache:
                self._cached_data = formatted
                self._cache_time = time.time()
            return formatted
        
        raise Exception("获取城市排名失败: API和网页均不可用")
    
    def _format_city_list(self, cities: List[Dict]) -> List[Dict[str, Any]]:
        """
        格式化城市列表数据
        
        Args:
            cities: 原始城市数据列表
            
        Returns:
            格式化后的城市数据列表
        """
        formatted = []
        for idx, city in enumerate(cities, 1):
            formatted.append({
                "rank": idx,
                "name": city.get("areaName", ""),
                "area_id": city.get("areaId", 0),
                "popularity_balance": city.get("popularityBalance", 0),
                "population": city.get("population", 0),
                "sold_blocks": city.get("soldBlocks", 0),
                "mayor": city.get("mayor", ""),
                "vice_mayor": city.get("viceMayor", ""),
                "avatar": city.get("avatar", ""),
                "mayor_avatar": city.get("mayorAvatar", "")
            })
        return formatted
    
    def get_city_by_name(self, city_name: str, use_mock_on_error: bool = True) -> Optional[Dict[str, Any]]:
        """
        根据城市名称获取城市详细信息
        
        Args:
            city_name: 城市名称
            use_mock_on_error: 出错时是否使用模拟数据
            
        Returns:
            城市详细信息，如果未找到则返回None
        """
        cities = self.get_city_rank_list(use_mock_on_error=use_mock_on_error)
        for city in cities:
            if city["name"] == city_name:
                return city
        return None
    
    def get_city_by_rank(self, rank: int, use_mock_on_error: bool = True) -> Optional[Dict[str, Any]]:
        """
        根据排名获取城市信息
        
        Args:
            rank: 城市排名（1-based）
            use_mock_on_error: 出错时是否使用模拟数据
            
        Returns:
            城市详细信息，如果排名无效则返回None
        """
        cities = self.get_city_rank_list(use_mock_on_error=use_mock_on_error)
        if 1 <= rank <= len(cities):
            return cities[rank - 1]
        return None
    
    def filter_cities(self, min_population: Optional[int] = None, 
                      max_population: Optional[int] = None,
                      min_sold_blocks: Optional[int] = None,
                      max_sold_blocks: Optional[int] = None,
                      use_mock_on_error: bool = True) -> List[Dict[str, Any]]:
        """
        根据条件筛选城市
        
        Args:
            min_population: 最小人口数
            max_population: 最大人口数
            min_sold_blocks: 最小售卖区块数
            max_sold_blocks: 最大售卖区块数
            use_mock_on_error: 出错时是否使用模拟数据
            
        Returns:
            符合条件的城市列表
        """
        cities = self.get_city_rank_list(use_mock_on_error=use_mock_on_error)
        filtered = []
        
        for city in cities:
            if min_population is not None and city["population"] < min_population:
                continue
            if max_population is not None and city["population"] > max_population:
                continue
            if min_sold_blocks is not None and city["sold_blocks"] < min_sold_blocks:
                continue
            if max_sold_blocks is not None and city["sold_blocks"] > max_sold_blocks:
                continue
            filtered.append(city)
        
        return filtered
    
    def to_json(self, data: Any, indent: int = 2) -> str:
        """
        将数据转换为JSON字符串
        
        Args:
            data: 要转换的数据
            indent: 缩进空格数
            
        Returns:
            JSON格式的字符串
        """
        return json.dumps(data, ensure_ascii=False, indent=indent)
    
    def _validate_city_identifier(self, city_id: str) -> bool:
        """
        验证城市标识格式
        
        Args:
            city_id: 城市标识（4位数字区号或4个小写字母）
            
        Returns:
            是否为有效格式
        """
        if len(city_id) == 4:
            if city_id.isdigit():
                return True
            if city_id.islower() and city_id.isalpha():
                return True
        return False
    
    def _get_mock_detail_data(self, city_id: str) -> Dict[str, Any]:
        """获取城市详情的模拟数据"""
        return {
            "city_id": city_id,
            "fund_balance": 0,
            "remaining_popularity": 0,
            "mayor": "",
            "vice_mayor": "",
            "total_blocks": 0,
            "available_blocks": 0
        }
    
    def _parse_city_detail_html(self, html: str, city_id: str) -> Dict[str, Any]:
        """
        解析城市详情页HTML（占位方法，待完善
        
        Args:
            html: HTML内容
            city_id: 城市标识
            
        Returns:
            解析后的城市详情数据
        """
        detail_data = {
            "city_id": city_id,
            "fund_balance": 0,
            "remaining_popularity": 0,
            "mayor": "",
            "vice_mayor": "",
            "total_blocks": 0,
            "available_blocks": 0
        }
        
        try:
            pass
            
        except Exception as e:
            print(f"HTML解析警告: {str(e)}，使用默认值")
        
        return detail_data
    
    def get_city_detail(self, city_id: str, use_mock_on_error: bool = True) -> Optional[Dict[str, Any]]:
        """
        从城市详情页获取城市详细信息
        
        Args:
            city_id: 城市标识（4位数字区号或4个小写字母）
            use_mock_on_error: 出错时是否使用模拟数据
            
        Returns:
            城市详细信息
        """
        if not self._validate_city_identifier(city_id):
            raise ValueError(f"无效的城市标识: {city_id}，应为4位数字区号或4个小写字母")
        
        try:
            url = f"{self.BASE_URL}/{city_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            if BS4_AVAILABLE:
                detail_data = self._parse_city_detail_html(response.text, city_id)
            else:
                print("警告: beautifulsoup4未安装，使用模拟数据")
                detail_data = self._get_mock_detail_data(city_id)
            
            return detail_data
            
        except Exception as e:
            if use_mock_on_error:
                print(f"警告: 使用模拟数据 - {str(e)}")
                return self._get_mock_detail_data(city_id)
            raise Exception(f"获取城市详情失败: {str(e)}")
    
    def get_complete_city_info(self, city_identifier: str, 
                              use_mock_on_error: bool = True) -> Optional[Dict[str, Any]]:
        """
        获取城市的完整信息（合并排名页和详情页数据
        
        Args:
            city_identifier: 城市名称
            use_mock_on_error: 出错时是否使用模拟数据
            
        Returns:
            完整的城市信息
        """
        rank_data = self.get_city_by_name(city_identifier, use_mock_on_error=use_mock_on_error)
        
        if rank_data is None:
            return None
        
        return rank_data


def main():
    """示例使用"""
    skill = BlockCitySkill()
    
    print("=== 获取前200个城市排名 ===")
    cities = skill.get_city_rank_list()
    print(f"共获取 {len(cities)} 个城市")
    for city in cities[:20]:
        print(f"{city['rank']}. {city['name']} - 人口: {city['population']}, 开启区块: {city['sold_blocks']}")
    
    print("\n=== 获取北京详细信息（来自排名页） ===")
    beijing = skill.get_city_by_name("北京")
    if beijing:
        print(skill.to_json(beijing))
    
    print("\n=== 获取排名第3的城市 ===")
    third_city = skill.get_city_by_rank(3)
    if third_city:
        print(skill.to_json(third_city))
    
    print("\n=== 从城市详情页获取北京信息（城市标识：0010） ===")
    try:
        beijing_detail = skill.get_city_detail("0010")
        print(skill.to_json(beijing_detail))
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n=== 测试4个小写字母的特殊自建城市标识（abcd） ===")
    try:
        special_city = skill.get_city_detail("abcd")
        print(skill.to_json(special_city))
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n=== 筛选人口超过2000的城市 ===")
    filtered = skill.filter_cities(min_population=2000)
    print(f"找到 {len(filtered)} 个城市:")
    for city in filtered:
        print(f"  {city['name']}: 人口 {city['population']}")


if __name__ == "__main__":
    main()
