import requests
import sys

# 【核心修复】直接强制系统输出为 UTF-8，不管是闪电、火箭还是表情包，一律放行
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def fetch_data():
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        items = response.json().get('data', {}).get('list', [])[:20]

        result_lines = []
        for idx, item in enumerate(items, 1):
            title = item.get('title', '无标题')
            # 简介里也常有乱七八糟的符号，一并带走
            desc = item.get('desc', '无简介').replace('\n', ' ')[:100]
            bvid = item.get('bvid', '')
            result_lines.append(f"{idx}. {title} | 简介: {desc} | 链接: https://www.bilibili.com/video/{bvid}")

        print("\n".join(result_lines))

    except Exception as e:
        print(f"数据抓取失败: {str(e)}")


if __name__ == "__main__":
    fetch_data()