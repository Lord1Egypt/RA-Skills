"""
eastmoney_financial_search - 东方财富资讯搜索技能
根据用户问句搜索相关金融资讯，获取新闻、公告、研报、政策解读等
"""
import os
import json
import urllib.request
from datetime import datetime

def get_eastmoney_news(query):
    """查询东方财富金融资讯"""
    apikey = os.environ.get("EASTMONEY_APIKEY", "mkt_Z19TUfMY79_44k4wZsAHIVGVva0-g8PxD_DkBDQx2iM")
    
    if not apikey or apikey == "<EASTMONEY_APIKEY>":
        print("❌ 请设置 EASTMONEY_APIKEY 环境变量")
        return None
    
    url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"
    data = {
        "apikey": apikey,
        "query": query
    }
    
    req = Request(
        url, 
        data=json.dumps(data).encode("utf-8"), 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except Exception as e:
        print(f"❌ 查询失败：{e}")
        return None

def save_to_file(query, result, filename="eastmoney_news_{safe_query}_{timestamp}.txt"):
    """将结果保存到文件"""
    if not result or "title" not in result:
        return
    
    safe_query = query.replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"eastmoney_news_{safe_query}_{timestamp}.txt"
    
    content = f"""东方财富金融资讯查询结果
查询：{query}
时间：{timestamp}

=== 资讯标题 ===
{result.get('title', 'N/A')}

=== 关联证券 ===
"""
    for i, secu in enumerate(result.get('secuList', []), 1):
        content += f"{i}. 代码：{secu.get('secuCode', 'N/A')} | 名称：{secu.get('secuName', 'N/A')} | 类型：{secu.get('secuType', 'N/A')}\n"
    
    content += f"""
=== 核心内容 ===
{result.get('trunk', 'N/A')}
"""
    
    with open(full_filename, "w", encoding="utf-8-sig") as f:
        f.write(content)
    
    print(f"✅ 已保存到：{full_filename}")

def main():
    import sys
    
    # 从命令行参数获取查询内容，或从环境变量读取
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("请输入查询内容（例如：格力电器最新研报）：")
    
    print(f"🔍 正在查询：{query}")
    
    result = get_eastmoney_news(query)
    
    if result and "title" in result:
        print(f"✅ 查询成功！")
        save_to_file(query, result)
    else:
        print("❌ 查询失败")

if __name__ == "__main__":
    main()
