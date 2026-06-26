
import requests
from bs4 import BeautifulSoup
import argparse
import sys
import json

def query_beijing_house(community_name):
    # Beijing Beike community search URL
    search_url = f"https://bj.ke.com/xiaoqu/rs{community_name}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Beike xiaoqu list items
        items = soup.find_all('li', class_='xiaoquListItem')
        
        if not items:
            return {
                "error": "CAPTCHA_OR_NOT_FOUND",
                "message": f"未能直接获取到 '{community_name}' 的小区信息（可能触发了人机验证或未找到）。",
                "advice": f"建议 Agent 尝试执行 web_search(query='北京 {community_name} 房价 学区 建成年份') 以获取最新数据。"
            }

        results = []
        for item in items[:3]:  # Top 3 results
            info = {}
            # Title
            title_node = item.find('div', class_='title')
            info['name'] = title_node.text.strip() if title_node else "未知"
            
            # Price
            price_node = item.find('div', class_='totalPrice')
            info['avg_price'] = price_node.text.strip() + " 元/m²" if price_node else "暂无数据"
            
            # Info (Region, Year)
            house_info_node = item.find('div', class_='houseInfo')
            if house_info_node:
                text = house_info_node.text.strip()
                # Beike format is often like: 板楼 | 2003年建 | 海淀
                parts = [p.strip() for p in text.split('|')]
                info['raw_info'] = text
                for p in parts:
                    if '年建' in p:
                        info['construction_year'] = p
                    if any(region in p for region in ['东城', '西城', '海淀', '朝阳', '丰台', '石景山', '通州', '昌平', '大兴', '顺义', '房山', '门头沟', '怀柔', '平谷', '密云', '延庆']):
                        info['region'] = p
            
            # Tags (Filter out school info to avoid unofficial data)
            tag_nodes = item.find('div', class_='tagList')
            if tag_nodes:
                all_tags = [t.text.strip() for t in tag_nodes.find_all('span')]
                # Preserve only non-school tags (like metro, key delivery, etc.)
                filtered_tags = [t for t in all_tags if '学' not in t and '校' not in t]
                info['tags'] = filtered_tags
                # Try to extract metro info specifically
                for tag in filtered_tags:
                    if '距离' in tag and '站' in tag:
                        info['metro_distance'] = tag

            results.append(info)
            
        return {"results": results}

    except Exception as e:
        return {"error": f"查询出错: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询北京小区基础信息")
    parser.add_argument("--name", required=True, help="小区名称")
    args = parser.parse_args()

    result = query_beijing_house(args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
