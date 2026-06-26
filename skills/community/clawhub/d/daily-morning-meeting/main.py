import datetime
import json
import subprocess
import os

# 配置项
CONFIG = {
    "search_count": 5,
    "max_news_items": 15,
    "save_path": "C:\\Users\\Admin\\.qclaw\\workspace\\",
    "receiver": "CEO"
}

def main():
    # 1. 获取当前日期
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"开始生成{today}早会简报...")

    # 2. 定义搜索关键词
    search_queries = [
        f"{today} 国内重要新闻",
        f"{today} 国际热点事件",
        f"{today} 财经要闻 股市动态",
        f"{today} 科技行业 互联网动态",
        f"{today} 政策新规 产业政策"
    ]

    all_news = []

    # 3. 调用搜索工具获取资讯
    for query in search_queries:
        try:
            cmd = f'openclaw tool call web_search --query "{query}" --count {CONFIG["search_count"]}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
            if result.returncode == 0:
                search_data = json.loads(result.stdout)
                all_news.extend(search_data.get("results", []))
        except Exception as e:
            print(f"搜索[{query}]失败: {str(e)}")
            continue

    # 4. 去重新闻（按URL）
    seen_urls = set()
    unique_news = []
    for news in all_news:
        url = news.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_news.append(news)

    # 5. 生成简报内容
    brief_content = f"# 🌅 每日早会简报 {today}\n\n"
    brief_content += "---\n\n"
    brief_content += "## 📢 今日重点资讯\n\n"

    for idx, news in enumerate(unique_news[:CONFIG["max_news_items"]], 1):
        title = news.get("title", "无标题").strip()
        snippet = news.get("snippet", "无摘要").strip()
        url = news.get("url", "无链接")
        brief_content += f"### {idx}. {title}\n"
        brief_content += f"> {snippet}\n"
        brief_content += f"> 🔗 详情：{url}\n\n"

    brief_content += "---\n\n"
    brief_content += "## 🎯 今日行动建议\n"
    brief_content += "1. 各部门负责人梳理相关资讯对业务的影响\n"
    brief_content += "2. 重点关注政策类动态，及时调整业务策略\n"
    brief_content += "3. 行业相关新闻组织团队内部同步讨论\n"

    # 6. 保存简报文件
    file_name = f"早会简报_{today}.md"
    full_path = os.path.join(CONFIG["save_path"], file_name)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(brief_content)
    print(f"简报已保存到: {full_path}")

    # 7. 发送简报给CEO
    try:
        send_cmd = f'openclaw tool call message --action send --target "{CONFIG["receiver"]}" --message "【每日早会简报 {today}】请查收今日最新资讯汇总。" --media "{full_path}"'
        subprocess.run(send_cmd, shell=True, capture_output=True, text=True)
        print("简报已成功发送给CEO")
    except Exception as e:
        print(f"发送简报失败: {str(e)}")

if __name__ == "__main__":
    main()
