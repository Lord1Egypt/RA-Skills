import requests
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bilibili_popular():
    """
    调用 B 站热门推荐接口，返回原始完整响应数据
    """
    # 接口基础配置
    base_url = "https://lvhomeproxy2.dpdns.org"
    api_path = "/api/bilibili/web/fetch_com_popular"
    full_url = f"{base_url}{api_path}"

    # 基础请求头（仅保留必要标识，避免爬虫特征）
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    # 调用接口
    response = requests.get(full_url, headers=headers)
    raw_data = response.json()

    # 提取指定字段
    result_list = []
    # 从返回数据中定位到list数组
    video_list = raw_data.get("data", {}).get("data", {}).get("list", [])

    for video in video_list:
        # print(video)
        # 提取核心字段
        item = {
            "title": video.get("title", ""),  # 视频标题
            "up_name": video.get("owner", {}).get("name", ""), # UP主名称
            "short_link_v2": video.get("short_link_v2", ""),  # 视频地址
            "tnamev2": video.get("tnamev2", "") # 视频分类
        }
        result_list.append(item)

    return result_list


if __name__ == "__main__":
    extracted_data = get_bilibili_popular()

    for idx, item in enumerate(extracted_data, 1):
        print(f"\n【{idx}】")
        print(f"标题：{item['title']}")
        print(f"UP主：{item['up_name']}")
        print(f"视频地址：{item['short_link_v2']}")
        print(f"视频分类：{item['tnamev2']}")