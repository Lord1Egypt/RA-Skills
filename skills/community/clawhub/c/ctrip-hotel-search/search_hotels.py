import urllib.request
import os
import json

# 尝试从配置文件导入 API key
try:
    from api_key_config import MATON_API_KEY
    api_key = MATON_API_KEY
except ImportError:
    api_key = None

def search_jianshui_hotels():
    """搜索建水古城酒店"""
    
    # 获取 API key
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("[ERROR] 错误：未设置 MATON_API_KEY")
        print("[INFO] 请在 api_key_config.py 中设置您的 API Key")
        print("[INFO] 或者设置环境变量：export MATON_API_KEY='your_api_key_here'")
        return None
    
    # 搜索查询
    query = "建水古城 酒店 民宿 4月9日 双床 3钻 4钻 4.5分 特色民宿"
    
    # 构建请求 URL
    url = f'https://gateway.maton.ai/brave-search/res/v1/web/search?q={urllib.parse.quote(query)}&count=10&search_lang=zh&country=CN'
    
    print(f"[SEARCH] 搜索: {query}")
    print(f"[URL] 链接: {url}")
    
    try:
        # 创建请求
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {api_key}')
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
            
            print("\n[SUCCESS] 搜索成功！")
            print(f"[INFO] 找到 {len(data.get('web', {}).get('results', []))} 个结果\n")
            
            # 显示搜索结果
            results = data.get('web', {}).get('results', [])
            for i, result in enumerate(results[:10], 1):
                print(f"{i}. {result.get('title', '无标题')}")
                print(f"   链接: {result.get('url', '无链接')}")
                print(f"   描述: {result.get('description', '无描述')}")
                print()
            
            return data
            
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP 错误: {e.code} - {e.reason}")
        print(f"[INFO] 响应内容: {e.read().decode('utf-8')}")
        return None
    except urllib.error.URLError as e:
        print(f"[ERROR] URL 错误: {e.reason}")
        return None
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        return None

if __name__ == "__main__":
    search_jianshui_hotels()