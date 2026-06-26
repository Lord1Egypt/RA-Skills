#!/usr/bin/env python3
"""
从 seatmaps.com 抓取航司机型数据
用法:
    python scrape_seatmaps.py --airline "航司名" --output FlightData/
    python scrape_seatmaps.py "https://seatmaps.com/zh-CN/airlines/..." --output FlightData/
"""

import os
import re
import sys
import json
import argparse
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# 航司名称映射
AIRLINE_MAP = {
    "新加坡航空": "sq-singapore-airlines",
    "singapore airlines": "sq-singapore-airlines",
    "sq": "sq-singapore-airlines",
    "阿联酋航空": "emirates",
    "emirates": "emirates",
    "ek": "emirates",
    "国泰航空": "cathay-pacific",
    "cathay pacific": "cathay-pacific",
    "cx": "cathay-pacific",
    "日本航空": "jal",
    "japan airlines": "jal",
    "jl": "jal",
}

class SeatmapsScraper:
    def __init__(self, output_dir="FlightData"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        self.base_url = "https://seatmaps.com/zh-CN/airlines/"
    
    def parse_airline_name(self, name):
        """解析航司名称获取 slug"""
        name_lower = name.lower()
        for key, slug in AIRLINE_MAP.items():
            if key in name_lower:
                return slug
        # 默认处理：取英文部分转小写加连字符
        return re.sub(r'[^\w\s-]', '', name_lower).replace(' ', '-')
    
    def get_aircraft_list(self, airline_slug):
        """获取航司机型列表"""
        url = f"{self.base_url}{airline_slug}/"
        print(f"🔍 发现机型：{url}")
        
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            aircraft_links = []
            # 查找机型链接
            for link in soup.find_all('a', href=re.compile(r'/airlines/.+/airbus|/airlines/.+/boeing')):
                href = link.get('href')
                if href and 'airlines' in href:
                    full_url = urljoin(self.base_url, href)
                    name = link.get_text(strip=True)
                    if name and full_url not in [a['url'] for a in aircraft_links]:
                        aircraft_links.append({'name': name, 'url': full_url})
            
            return aircraft_links
        except Exception as e:
            print(f"❌ 获取机型列表失败: {e}")
            return []
    
    def download_image(self, img_url, save_path):
        """下载图片"""
        try:
            resp = self.session.get(img_url, timeout=30)
            resp.raise_for_status()
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            return True
        except Exception as e:
            print(f"  ⚠️ 下载失败 {img_url}: {e}")
            return False
    
    def scrape_aircraft(self, url, airline_name=""):
        """抓取单个机型数据"""
        print(f"\n✈️  抓取：{url}")
        
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 提取机型名称
            title_elem = soup.find('h1') or soup.find('title')
            aircraft_name = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            # 清理名称
            aircraft_name = re.sub(r'[\\/:*?"<>|]', '-', aircraft_name)
            
            # 创建目录
            if airline_name:
                base_dir = os.path.join(self.output_dir, airline_name, aircraft_name)
            else:
                base_dir = os.path.join(self.output_dir, aircraft_name)
            
            raw_dir = os.path.join(base_dir, "images", "0-原始数据")
            os.makedirs(raw_dir, exist_ok=True)
            
            # 保存原始页面
            html_path = os.path.join(raw_dir, "原始页面.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(resp.text)
            
            # 提取并下载图片
            images = soup.find_all('img')
            downloaded = 0
            
            for i, img in enumerate(images):
                src = img.get('src') or img.get('data-src')
                if not src:
                    continue
                
                # 过滤小图标
                if img.get('width') and int(img.get('width', 0)) < 100:
                    continue
                
                img_url = urljoin(url, src)
                ext = os.path.splitext(urlparse(img_url).path)[1] or '.webp'
                img_name = f"image_{i:03d}{ext}"
                save_path = os.path.join(raw_dir, img_name)
                
                if self.download_image(img_url, save_path):
                    downloaded += 1
            
            print(f"   📸 正在下载 {downloaded} 张图片...")
            
            # 生成机型详情文档
            self.create_detail_doc(base_dir, aircraft_name, url, soup)
            
            print(f"   ✅ 下载完成：{downloaded} 张图片")
            return True
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return False
    
    def create_detail_doc(self, base_dir, aircraft_name, source_url, soup):
        """创建机型详情文档"""
        doc_path = os.path.join(base_dir, "机型详情.md")
        
        # 提取基本信息
        title = aircraft_name
        
        content = f"""# {title} 机型详情

> 数据来源：seatmaps.com | 最后更新：{import datetime; datetime.datetime.now().strftime('%Y-%m-%d')}

---

## 📊 基本信息

| 项目 | 详情 |
|------|------|
| **航空公司** | {title.split()[0] if ' ' in title else '待确认'} |
| **机型** | {aircraft_name} |
| **版本** | 单类型（1 类型） |
| **总座位数** | 待确认 |
| **舱位配置** | 待确认 |

---

## 🛋️ 舱位详情

### 头等舱 / 套房 (First Class / Suites)

| 参数 | 数值 |
|------|------|
| 座位数 | 待补充 |
| 腿部空间 | 待补充 |
| 座椅宽度 | 待补充 |

### 商务舱 (Business Class)

| 参数 | 数值 |
|------|------|
| 座位数 | 待补充 |
| 腿部空间 | 待补充 |
| 座椅宽度 | 待补充 |
| 座椅类型 | 待补充 |

### 经济舱 (Economy Class)

| 参数 | 数值 |
|------|------|
| 座位数 | 待补充 |
| 腿部空间 | 待补充 |
| 座椅宽度 | 待补充 |

---

## 📸 图片资源

图片已分类存储至 `images/` 目录：

- `1-座椅布局/` - 座位图、舱位平面图
- `2-座椅图片/` - 座椅实物照片
- `3-机上餐食/` - 餐食、菜单相关
- `4-娱乐设备/` - IFE、端口、Wi-Fi 等
- `5-其他信息/` - 外观、logo、杂项等

---

## 🔗 来源链接

- 原始页面：{source_url}

---

## 📝 待补充信息

- [ ] 总座位数
- [ ] 各舱位座位数
- [ ] 座椅具体参数
- [ ] 机上餐食信息
- [ ] 娱乐系统详情
- [ ] Wi-Fi 信息
"""
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ 机型详情已保存：{doc_path}")
        
        # 创建完整内容整理文档
        full_doc_path = os.path.join(base_dir, "完整内容整理.md")
        with open(full_doc_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title} - 完整内容整理\n\n> 数据来源：seatmaps.com\n\n---\n\n")
            # 提取页面主要内容
            for elem in soup.find_all(['p', 'h2', 'h3', 'li']):
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    f.write(f"{text}\n\n")
        
        print(f"   ✅ 文档已保存：{full_doc_path}")


def main():
    parser = argparse.ArgumentParser(description="从 seatmaps.com 抓取航司机型数据")
    parser.add_argument("url_or_airline", nargs="?", help="航司名称或单个机型 URL")
    parser.add_argument("--airline", help="航空公司名称（中英文）")
    parser.add_argument("--output", "-o", default="FlightData", help="输出目录")
    parser.add_argument("--limit", "-l", type=int, help="限制抓取数量")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不下载")
    
    args = parser.parse_args()
    
    scraper = SeatmapsScraper(output_dir=args.output)
    
    # 确定航司名称或 URL
    if args.airline:
        airline_name = args.airline
        airline_slug = scraper.parse_airline_name(airline_name)
        print(f"🔍 解析航空公司名称：{airline_name}")
        print(f"✈️  航空公司 Slug: {airline_slug}")
        
        # 获取机型列表
        aircraft_list = scraper.get_aircraft_list(airline_slug)
        
        if not aircraft_list:
            print("❌ 未发现机型")
            return
        
        print(f"✅ 发现 {len(aircraft_list)} 个机型")
        
        if args.dry_run:
            print(f"📁 输出目录：{args.output}")
            print("🔍 预览模式，不下载")
            for ac in aircraft_list:
                print(f"   - {ac['name']}: {ac['url']}")
            return
        
        # 限制数量
        if args.limit:
            aircraft_list = aircraft_list[:args.limit]
            print(f"⏹️  限制抓取前 {args.limit} 个机型")
        
        # 逐个抓取
        for i, ac in enumerate(aircraft_list, 1):
            print(f"\n[{i}/{len(aircraft_list)}] {ac['name']}")
            scraper.scrape_aircraft(ac['url'], airline_name)
        
        print(f"\n✅ 抓取完成")
        print(f"📁 输出目录：{args.output}")
    
    elif args.url_or_airline:
        # 单个 URL
        if args.url_or_airline.startswith("http"):
            if args.dry_run:
                print(f"🔍 预览模式：{args.url_or_airline}")
                return
            scraper.scrape_aircraft(args.url_or_airline)
        else:
            # 航司名称
            airline_name = args.url_or_airline
            airline_slug = scraper.parse_airline_name(airline_name)
            print(f"🔍 解析航空公司名称：{airline_name}")
            print(f"✈️  航空公司 Slug: {airline_slug}")
            
            aircraft_list = scraper.get_aircraft_list(airline_slug)
            print(f"✅ 发现 {len(aircraft_list)} 个机型")
            
            for ac in aircraft_list[:args.limit or len(aircraft_list)]:
                scraper.scrape_aircraft(ac['url'], airline_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
