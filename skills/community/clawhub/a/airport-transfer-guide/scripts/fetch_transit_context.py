#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机场转机上下文获取脚本
纯 Python 标准库实现，零外部依赖
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


# 常量定义
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
REQUEST_TIMEOUT = 10
CHROME_TIMEOUT = 15


class AirportRegistry:
    """机场配置注册表"""
    
    def __init__(self, registry_path: Optional[Path] = None):
        self._data = {}
        # ifly.com slug 映射（从搜索结果验证的实际 URL）
        self._ifly_slugs = {
            'NRT': 'tokyo-narita-NRT', 'HND': 'tokyo-haneda-HND',
            'HKG': 'hong-kong-international', 'DXB': 'dubai',
            'SIN': 'singapore-changi', 'ICN': 'seoul-incheon-international',
            'BKK': 'bangkok-suvarnabhumi', 'DOH': 'doha-hamad-international',
            'IST': 'istanbul', 'KUL': 'kuala-lumpur-international',
            'LHR': 'london-heathrow', 'CDG': 'paris-charles-de-gaulle',
            'FRA': 'frankfurt', 'AMS': 'amsterdam-schiphol',
            'TPE': 'taipei-taoyuan-international', 'SYD': 'sydney',
            'LAX': 'los-angeles-international', 'JFK': 'new-york-jfk',
            'ORD': 'chicago-ohare-international',
        }
        self._meta = {
            'image_url_template': 'https://www.ifly.com/airports/{slug}-airport/terminal-map',
            'image_url_fallback': 'https://www.ifly.com/airports/{code}/terminal-map',
            'crowd_url_template': 'https://flightqueue.com/airport/{code}',
            'flight_board_template': 'https://www.flightradar24.com/data/airports/{code_lower}'
        }
        
        if registry_path is None:
            # 默认使用相对于脚本的路径
            script_dir = Path(__file__).parent
            registry_path = script_dir.parent / 'references' / 'airport_registry.json'
        
        self._load_registry(registry_path)
    
    def _load_registry(self, path: Path):
        """加载机场注册表配置"""
        try:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
        except Exception as e:
            print(f"警告: 无法加载注册表 {path}: {e}", file=sys.stderr)
    
    def get_airport_name(self, code: str) -> str:
        """获取机场名称"""
        code = code.upper()
        if code in self._data:
            return self._data[code].get('name', code)
        return f"{code} Airport"
    
    def get_image_urls(self, code: str) -> Dict[str, str]:
        """获取图片相关 URL"""
        code = code.upper()
        result = {}
        
        # 注册表中有 images 子字段时直接使用
        if code in self._data:
            imgs = self._data[code].get('images', {})
            if imgs:
                return imgs
            # 注册表中有 official_map 时加入结果
            official = self._data[code].get('official_map', '')
            if official:
                result['official_map'] = official
        
        # 通用聚合站 URL：优先使用 ifly slug 映射
        slug = self._ifly_slugs.get(code)
        if slug:
            result['airportguide'] = self._meta['image_url_template'].format(slug=slug)
        else:
            result['airportguide'] = self._meta['image_url_fallback'].format(code=code)
        
        return result
    
    def get_crowd_urls(self, code: str) -> Dict[str, str]:
        """获取拥挤度相关 URL"""
        code = code.upper()
        if code in self._data:
            urls = self._data[code].get('crowd', {})
            if urls:
                return urls
        
        # 降级到通用模板
        return {
            'flightqueue': self._meta['crowd_url_template'].format(code=code)
        }
    
    def get_flight_board_url(self, code: str) -> str:
        """获取航班看板 URL"""
        code = code.upper()
        if code in self._data:
            board_url = self._data[code].get('flight_board')
            if board_url:
                return board_url
        
        # 降级到通用模板
        return self._meta['flight_board_template'].format(code_lower=code.lower())
    
    def get_baggage_note(self, code: str) -> str:
        """获取行李说明"""
        code = code.upper()
        if code in self._data:
            note = self._data[code].get('baggage_note')
            if note:
                return note
        return "请根据您的航班和目的地确认行李转运规则"
    
    def get_cdp_targets(self, code: str) -> List[str]:
        """获取需要截图的目标 URL 列表"""
        code = code.upper()
        if code in self._data:
            return self._data[code].get('cdp_targets', [])
        return []


class ImageHTMLParser(HTMLParser):
    """HTML 解析器，用于提取图片 URL"""
    
    def __init__(self):
        super().__init__()
        self.images = []
        self._in_img = False
        self._current_img = {}
    
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            title = attrs_dict.get('title', '')
            
            # 过滤出 terminal map 相关图片
            if src and any(keyword in src.lower() or keyword in alt.lower() or keyword in title.lower() 
                          for keyword in ['terminal', 'map', 'floor', 'level']):
                self._current_img = {
                    'src': src,
                    'alt': alt,
                    'title': title
                }
    
    def handle_endtag(self, tag):
        if tag == 'img' and self._current_img:
            self.images.append(self._current_img)
            self._current_img = {}


class CrowdHTMLParser(HTMLParser):
    """HTML 解析器，用于提取拥挤度数据"""
    
    def __init__(self):
        super().__init__()
        self.crowd_data = {}
        self._in_wait_time = False
        self._current_section = None
        self._text_buffer = []
    
    def handle_starttag(self, tag, attrs):
        if tag in ['div', 'span', 'p', 'section']:
            attrs_dict = dict(attrs)
            class_attr = attrs_dict.get('class', '').lower()
            id_attr = attrs_dict.get('id', '').lower()
            
            if any(keyword in class_attr or keyword in id_attr 
                  for keyword in ['security', 'wait', 'time', 'immigration', 'baggage']):
                self._in_wait_time = True
                if 'security' in class_attr or 'security' in id_attr:
                    self._current_section = 'security'
                elif 'immigration' in class_attr or 'immigration' in id_attr:
                    self._current_section = 'immigration'
                elif 'baggage' in class_attr or 'baggage' in id_attr:
                    self._current_section = 'baggage_claim'
    
    def handle_endtag(self, tag):
        if tag in ['div', 'span', 'p', 'section']:
            if self._in_wait_time and self._text_buffer:
                text = ' '.join(self._text_buffer).strip()
                if self._current_section:
                    # 尝试提取数字作为等待时间
                    minutes = self._extract_minutes(text)
                    level = self._extract_level(text)
                    
                    if self._current_section not in self.crowd_data:
                        self.crowd_data[self._current_section] = {}
                    
                    if minutes:
                        self.crowd_data[self._current_section]['wait_minutes'] = minutes
                    if level:
                        self.crowd_data[self._current_section]['level'] = level
                
                self._in_wait_time = False
                self._text_buffer = []
                self._current_section = None
    
    def handle_data(self, data):
        if self._in_wait_time:
            self._text_buffer.append(data)
    
    def _extract_minutes(self, text: str) -> Optional[int]:
        """从文本中提取等待分钟数"""
        match = re.search(r'(\d+)\s*(?:min|minute|分钟)', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_level(self, text: str) -> Optional[str]:
        """从文本中提取拥挤级别"""
        text_lower = text.lower()
        if 'low' in text_lower or '低' in text_lower or 'short' in text_lower:
            return 'low'
        elif 'high' in text_lower or '高' in text_lower or 'long' in text_lower:
            return 'high'
        elif 'medium' in text_lower or '中' in text_lower or 'moderate' in text_lower:
            return 'medium'
        return None


class HTTPClient:
    """HTTP 客户端封装"""
    
    @staticmethod
    def fetch(url: str, timeout: int = REQUEST_TIMEOUT) -> Optional[str]:
        """获取 URL 内容"""
        try:
            req = Request(url, headers={'User-Agent': USER_AGENT})
            with urlopen(req, timeout=timeout) as response:
                return response.read().decode('utf-8', errors='ignore')
        except (URLError, HTTPError, TimeoutError, Exception) as e:
            print(f"警告: 请求失败 {url}: {e}", file=sys.stderr)
            return None


class ImageFetcher:
    """图片获取器"""
    
    def __init__(self, registry: AirportRegistry):
        self.registry = registry
    
    def fetch(self, airport_code: str, terminals: Optional[List[str]] = None) -> List[Dict]:
        """获取机场图片列表"""
        images = []
        
        # 优先级 1: airportguide.com
        images.extend(self._fetch_from_airportguide(airport_code))
        
        # 优先级 2: 官方网站
        if not images:
            images.extend(self._fetch_from_official(airport_code))
        
        # 降级: 如果都失败，返回 source_url 但 inline_available=false
        if not images:
            urls = self.registry.get_image_urls(airport_code)
            for source_type, url in urls.items():
                images.append({
                    'title': 'Terminal Map',
                    'image_url': '',
                    'source_url': url,
                    'source_type': 'third_party_aggregator',
                    'inline_available': False,
                    'why_it_matters': '需要访问源网站查看航站楼地图'
                })
        
        return images
    
    def _fetch_from_airportguide(self, airport_code: str) -> List[Dict]:
        """从 airportguide.com 获取图片"""
        urls = self.registry.get_image_urls(airport_code)
        url = urls.get('airportguide')
        
        if not url:
            return []
        
        html = HTTPClient.fetch(url)
        if not html:
            return []
        
        parser = ImageHTMLParser()
        parser.feed(html)
        
        images = []
        for img in parser.images[:5]:  # 最多取 5 张图片
            images.append({
                'title': 'Terminal Map',
                'image_url': urljoin(url, img['src']),
                'source_url': url,
                'source_type': 'third_party_aggregator',
                'inline_available': True,
                'why_it_matters': '确认到达层和入境方向'
            })
        
        return images
    
    def _fetch_from_official(self, airport_code: str) -> List[Dict]:
        """从官方网站获取图片"""
        urls = self.registry.get_image_urls(airport_code)
        url = urls.get('official_map')
        
        if not url:
            return []
        
        html = HTTPClient.fetch(url)
        if not html:
            return []
        
        parser = ImageHTMLParser()
        parser.feed(html)
        
        images = []
        for img in parser.images[:3]:
            images.append({
                'title': 'Official Terminal Map',
                'image_url': urljoin(url, img['src']),
                'source_url': url,
                'source_type': 'official',
                'inline_available': True,
                'why_it_matters': '官方最新航站楼地图'
            })
        
        return images


class CrowdEstimator:
    """拥挤度估算器"""
    
    def __init__(self, registry: AirportRegistry):
        self.registry = registry
        self.flight_board_proxy = FlightBoardProxy(registry)
    
    def estimate(self, airport_code: str, transit_datetime: Optional[str] = None) -> Dict:
        """估算拥挤度"""
        # 优先级 1: flightqueue.com
        crowd = self._estimate_from_flightqueue(airport_code)
        
        if crowd.get('status') == 'unavailable':
            # 优先级 2: 官方等待时间
            crowd = self._estimate_from_official(airport_code)
        
        if crowd.get('status') == 'unavailable':
            # 优先级 3: 航班密度代理
            crowd = self._estimate_from_flight_board(airport_code, transit_datetime)
        
        return crowd
    
    def _estimate_from_flightqueue(self, airport_code: str) -> Dict:
        """从 flightqueue.com 获取拥挤度"""
        urls = self.registry.get_crowd_urls(airport_code)
        url = urls.get('flightqueue')
        
        if not url:
            return self._unavailable_result()
        
        html = HTTPClient.fetch(url)
        if not html:
            return self._unavailable_result()
        
        parser = CrowdHTMLParser()
        parser.feed(html)
        
        if not parser.crowd_data:
            return self._unavailable_result()
        
        # 计算整体拥挤度
        details = parser.crowd_data
        levels = [d.get('level') for d in details.values() if d.get('level')]
        waits = [d.get('wait_minutes') for d in details.values() if d.get('wait_minutes')]
        
        if levels:
            # 简单的级别映射: low=1, medium=2, high=3
            level_map = {'low': 1, 'medium': 2, 'high': 3}
            avg_level = sum(level_map.get(l, 2) for l in levels) / len(levels)
            
            if avg_level <= 1.5:
                overall_level = 'low'
            elif avg_level <= 2.5:
                overall_level = 'medium'
            else:
                overall_level = 'high'
        else:
            overall_level = None
        
        overall_wait = int(sum(waits) / len(waits)) if waits else None
        
        # 确保所有环节都有默认值
        for section in ['security', 'immigration', 'baggage_claim']:
            if section not in details:
                details[section] = {'level': None, 'wait_minutes': None, 'source': 'none'}
            else:
                details[section]['source'] = 'flightqueue'
        
        return {
            'status': 'available',
            'level': overall_level,
            'wait_minutes': overall_wait,
            'signal_type': 'flightqueue',
            'summary': self._generate_summary(overall_level, overall_wait),
            'source_url': url,
            'details': details
        }
    
    def _estimate_from_official(self, airport_code: str) -> Dict:
        """从官方等待时间获取拥挤度"""
        urls = self.registry.get_crowd_urls(airport_code)
        url = urls.get('official_wait_time')
        
        if not url:
            return self._unavailable_result()
        
        html = HTTPClient.fetch(url)
        if not html:
            return self._unavailable_result()
        
        parser = CrowdHTMLParser()
        parser.feed(html)
        
        if not parser.crowd_data:
            return self._unavailable_result()
        
        details = parser.crowd_data
        for section in details:
            details[section]['source'] = 'official_wait_time'
        
        # 确保所有环节都有默认值
        for section in ['security', 'immigration', 'baggage_claim']:
            if section not in details:
                details[section] = {'level': None, 'wait_minutes': None, 'source': 'none'}
        
        return {
            'status': 'available',
            'level': None,
            'wait_minutes': None,
            'signal_type': 'official_wait_time',
            'summary': '官方等待时间数据',
            'source_url': url,
            'details': details
        }
    
    def _estimate_from_flight_board(self, airport_code: str, transit_datetime: Optional[str]) -> Dict:
        """从航班看板代理估算拥挤度"""
        # 使用 T1 作为默认航站楼
        density = self.flight_board_proxy.estimate_density(airport_code, 'T1', transit_datetime)
        
        details = {
            'security': {'level': None, 'wait_minutes': None, 'source': 'none'},
            'immigration': {'level': None, 'wait_minutes': None, 'source': 'none'},
            'baggage_claim': {'level': None, 'wait_minutes': None, 'source': 'none'}
        }
        
        url = self.registry.get_flight_board_url(airport_code)
        
        if density:
            return {
                'status': 'proxy',
                'level': density,
                'wait_minutes': None,
                'signal_type': 'flight_board_proxy',
                'summary': self._generate_summary(density, None),
                'source_url': url,
                'details': details
            }
        
        return {
            'status': 'unavailable',
            'level': None,
            'wait_minutes': None,
            'signal_type': 'none',
            'summary': '无法获取拥挤度数据',
            'source_url': url,
            'details': details
        }
    
    def _unavailable_result(self) -> Dict:
        """返回不可用结果"""
        return {
            'status': 'unavailable',
            'level': None,
            'wait_minutes': None,
            'signal_type': 'none',
            'summary': '无法获取拥挤度数据',
            'source_url': '',
            'details': {
                'security': {'level': None, 'wait_minutes': None, 'source': 'none'},
                'immigration': {'level': None, 'wait_minutes': None, 'source': 'none'},
                'baggage_claim': {'level': None, 'wait_minutes': None, 'source': 'none'}
            }
        }
    
    def _generate_summary(self, level: Optional[str], wait_minutes: Optional[int]) -> str:
        """生成拥挤度摘要"""
        if level == 'low':
            return '当前拥挤度较低'
        elif level == 'medium':
            return '当前中等拥挤'
        elif level == 'high':
            return '当前拥挤度较高'
        elif wait_minutes:
            if wait_minutes < 15:
                return '当前等待时间较短'
            elif wait_minutes < 30:
                return '当前中等等待时间'
            else:
                return '当前等待时间较长'
        return '拥挤度未知'


class FlightBoardProxy:
    """航班看板代理，用于通过航班密度估算拥挤度"""
    
    def __init__(self, registry: AirportRegistry):
        self.registry = registry
    
    def estimate_density(self, airport_code: str, terminal: str, datetime_str: Optional[str]) -> Optional[str]:
        """估算航班密度"""
        url = self.registry.get_flight_board_url(airport_code)
        
        html = HTTPClient.fetch(url)
        if not html:
            return None
        
        # 尝试从 HTML 中提取航班数量
        # 这里使用简单的正则匹配，实际可能需要更复杂的解析
        flight_count = self._count_flights_from_html(html)
        
        if flight_count is None:
            return None
        
        if flight_count < 10:
            return 'low'
        elif flight_count < 25:
            return 'medium'
        else:
            return 'high'
    
    def _count_flights_from_html(self, html: str) -> Optional[int]:
        """从 HTML 中统计航班数量"""
        # 简单的实现：查找常见的航班标识符
        # 实际网站可能需要更复杂的解析
        patterns = [
            r'flight[_\s]?count["\s:]+(\d+)',
            r'(\d+)\s*flights?',
            r'total[_\s]?flights["\s:]+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return None


class CDPScreenshot:
    """Chrome DevTools Protocol 截图工具"""
    
    def __init__(self):
        self.chrome_path = self._find_chrome()
    
    def _find_chrome(self) -> Optional[str]:
        """查找 Chrome 可执行文件"""
        import platform
        
        system = platform.system().lower()
        
        if system == 'darwin':  # macOS
            paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Chromium.app/Contents/MacOS/Chromium',
            ]
        elif system == 'linux':
            paths = [
                'google-chrome',
                'google-chrome-stable',
                'chromium-browser',
                'chromium',
            ]
        else:
            return None
        
        for path in paths:
            try:
                result = subprocess.run(
                    [path, '--version'],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return path
            except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
                continue
        
        return None
    
    def screenshot(self, url: str, output_path: str, timeout: int = CHROME_TIMEOUT) -> bool:
        """对 URL 进行截图"""
        if not self.chrome_path:
            print("警告: 未找到 Chrome，无法截图", file=sys.stderr)
            return False
        
        try:
            cmd = [
                self.chrome_path,
                '--headless=new',
                '--disable-gpu',
                '--no-first-run',
                '--no-default-browser-check',
                '--window-size=1280,900',
                '--screenshot=' + output_path,
                url
            ]
            
            result = subprocess.run(cmd, timeout=timeout, capture_output=True)
            
            if result.returncode == 0 and Path(output_path).exists():
                return True
            else:
                print(f"警告: 截图失败 {url}", file=sys.stderr)
                return False
        
        except subprocess.TimeoutExpired:
            print(f"警告: 截图超时 {url}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"警告: 截图异常 {url}: {e}", file=sys.stderr)
            return False
    
    def is_available(self) -> bool:
        """检查 Chrome 是否可用"""
        return self.chrome_path is not None


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='获取机场转机上下文数据')
    
    parser.add_argument(
        '--airport',
        required=True,
        help='机场三字码（必填）'
    )
    parser.add_argument(
        '--inbound-terminal',
        help='到达航站楼（可选）'
    )
    parser.add_argument(
        '--outbound-terminal',
        help='出发航站楼（可选）'
    )
    parser.add_argument(
        '--transit-datetime',
        help='中转时间 ISO 格式（可选）'
    )
    parser.add_argument(
        '--mode',
        choices=['normal', 'delay'],
        default='normal',
        help='运行模式（默认: normal）'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='输出 JSON 文件路径（必填）'
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 初始化组件
    registry = AirportRegistry()
    image_fetcher = ImageFetcher(registry)
    crowd_estimator = CrowdEstimator(registry)
    screenshot_tool = CDPScreenshot()
    
    # 获取数据
    airport_code = args.airport.upper()
    terminals = []
    if args.inbound_terminal:
        terminals.append(args.inbound_terminal.upper())
    if args.outbound_terminal:
        terminals.append(args.outbound_terminal.upper())
    
    # 获取图片
    images = image_fetcher.fetch(airport_code, terminals)
    
    # 获取拥挤度
    crowd = crowd_estimator.estimate(airport_code, args.transit_datetime)
    
    # 获取行李说明
    baggage_note = registry.get_baggage_note(airport_code)
    
    # 截图（如果需要）
    cdp_targets = registry.get_cdp_targets(airport_code)
    screenshots_taken = []
    if screenshot_tool.is_available() and cdp_targets:
        output_dir = Path(args.output).parent
        for idx, target_url in enumerate(cdp_targets[:2]):  # 最多截图 2 个
            screenshot_path = output_dir / f"{airport_code}_screenshot_{idx}.png"
            if screenshot_tool.screenshot(target_url, str(screenshot_path)):
                screenshots_taken.append(str(screenshot_path))
    
    # 组装最终结果
    result = {
        'airport_code': airport_code,
        'airport_name': registry.get_airport_name(airport_code),
        'fetched_at': datetime.now().isoformat(),
        'images': images,
        'crowd': crowd,
        'baggage_note': baggage_note,
        'support': {
            'images': len(images) > 0,
            'crowd': crowd.get('signal_type', 'none'),
            'cdp_available': screenshot_tool.is_available()
        }
    }
    
    # 写入输出文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印摘要到 stderr
    print(f"\n=== 转机上下文获取完成 ===", file=sys.stderr)
    print(f"机场: {airport_code} - {result['airport_name']}", file=sys.stderr)
    print(f"图片数量: {len(images)}", file=sys.stderr)
    print(f"拥挤度状态: {crowd.get('status')}", file=sys.stderr)
    if crowd.get('level'):
        print(f"拥挤度级别: {crowd['level']}", file=sys.stderr)
    if screenshots_taken:
        print(f"截图数量: {len(screenshots_taken)}", file=sys.stderr)
    print(f"输出文件: {output_path}", file=sys.stderr)
    print(f"=========================\n", file=sys.stderr)


if __name__ == '__main__':
    main()
