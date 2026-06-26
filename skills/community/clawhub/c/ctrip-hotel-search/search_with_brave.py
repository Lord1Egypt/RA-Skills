import urllib.request
import os
import json

def search_with_brave(query, count=10):
    """使用 Brave Search 搜索"""
    
    # 从环境变量获取 API key
    api_key = os.environ.get('MATON_API_KEY')
    
    if not api_key:
        print("[ERROR] 未找到 MATON_API_KEY 环境变量")
        print("[INFO] 请设置环境变量：set MATON_API_KEY=your_api_key_here")
        return None
    
    # 构建搜索 URL
    base_url = "https://gateway.maton.ai/brave-search/res/v1/web/search"
    params = {
        'q': query,
        'count': count,
        'search_lang': 'zh',
        'country': 'CN'
    }
    
    # URL 编码
    import urllib.parse
    query_string = urllib.parse.urlencode(params)
    url = base_url + '?' + query_string
    
    print(f"[SEARCH] 搜索: {query}")
    print(f"[URL] {url}")
    
    try:
        # 创建请求
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {api_key}')
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
            
            print(f"\n[SUCCESS] 搜索成功！")
            print(f"[INFO] 找到 {len(data.get('web', {}).get('results', []))} 个结果\n")
            
            # 显示搜索结果
            results = data.get('web', {}).get('results', [])
            for i, result in enumerate(results[:count], 1):
                print(f"{i}. {result.get('title', '无标题')}")
                print(f"   链接: {result.get('url', '无链接')}")
                description = result.get('description', '无描述')
                if len(description) > 100:
                    description = description[:100] + "..."
                print(f"   描述: {description}")
                print()
            
            return data
            
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP 错误: {e.code} - {e.reason}")
        if e.code == 401:
            print("[INFO] API key 可能无效，请检查")
        return None
    except urllib.error.URLError as e:
        print(f"[ERROR] URL 错误: {e.reason}")
        return None
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        return None

if __name__ == "__main__":
    # 搜索建水古城酒店
    query = "建水古城 酒店 民宿 4月9日 双床 3钻 4钻 4.5分 特色民宿"
    search_with_brave(query, count=10)