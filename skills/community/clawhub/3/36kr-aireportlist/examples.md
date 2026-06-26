# 使用示例集合 — 36kr 自助报道栏目文章

## 示例 1：Python — 基础查询（今日自助报道）

```python
import httpx
import datetime

def get_today_aireport():
    today = datetime.date.today().isoformat()  # "2026-03-17"
    url = f"https://openclaw.36krcdn.com/media/aireport/{today}/ai_report_articles.json"

    resp = httpx.get(url, timeout=10)
    resp.raise_for_status()
    result = resp.json()

    print(f"=== 36kr 自助报道 {result['date']} ===")
    for item in result["data"]:
        print(f"  #{item['rank']:>2}  {item['title']}")
        print(f"       作者：{item['author']}  发布：{item['publishTime']}")
        print(f"       链接：{item['url']}")
        print()

# 运行
get_today_aireport()
```

**输出示例：**
```
=== 36kr 自助报道 2026-03-17 ===
   #1  我们正在研发下一代工业机器人，寻求媒体报道
       作者：智能制造科技  发布：2026-03-17 09:00:00
       链接：https://36kr.com/p/9876543210000010?channel=openclaw

   #2  AI辅助医疗影像诊断系统完成B轮融资，寻求报道
       作者：医健科技  发布：2026-03-17 08:30:00
       链接：https://36kr.com/p/9876543210000011?channel=openclaw
```

---

## 示例 2：Python — 查询指定日期

```python
import httpx

def get_aireport_by_date(date: str):
    """
    查询指定日期的自助报道文章列表。
    Args:
        date: "YYYY-MM-DD" 格式，如 "2026-03-10"
    """
    url = f"https://openclaw.36krcdn.com/media/aireport/{date}/ai_report_articles.json"
    resp = httpx.get(url, timeout=10)

    if resp.status_code == 404:
        print(f"[!] {date} 的自助报道数据不存在")
        return None

    resp.raise_for_status()
    return resp.json()

# Demo: 查询 2026-03-10
data = get_aireport_by_date("2026-03-10")
if data:
    titles = [item["title"] for item in data["data"]]
    print(f"共 {len(titles)} 篇文章：", titles[:3])
```

---

## 示例 3：Java — HttpClient 查询

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDate;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

public class AiReportDemo {

    private static final String URL_TEMPLATE =
        "https://openclaw.36krcdn.com/media/aireport/%s/ai_report_articles.json";

    public static void main(String[] args) throws Exception {
        String date = LocalDate.now().toString();  // "2026-03-17"
        String url = String.format(URL_TEMPLATE, date);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() == 200) {
            JSONObject json = JSONObject.parseObject(response.body());
            JSONArray data = json.getJSONArray("data");

            System.out.println("=== 36kr 自助报道 " + json.getString("date") + " ===");
            for (int i = 0; i < data.size(); i++) {
                JSONObject item = data.getJSONObject(i);
                System.out.printf("  #%d  %s — %s%n",
                        item.getIntValue("rank"),
                        item.getString("title"),
                        item.getString("author"));
                System.out.printf("       %s%n", item.getString("url"));
            }
        } else if (response.statusCode() == 404) {
            System.out.println("[!] " + date + " 的自助报道数据不存在");
        }
    }
}
```

---

## 示例 4：JavaScript / Node.js — fetch 查询

```javascript
const today = new Date().toISOString().slice(0, 10); // "2026-03-17"
const url = `https://openclaw.36krcdn.com/media/aireport/${today}/ai_report_articles.json`;

fetch(url)
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(data => {
    console.log(`=== 36kr 自助报道 ${data.date} ===`);
    data.data.forEach(item => {
      console.log(`  #${item.rank}  ${item.title}`);
      console.log(`       ${item.author}  |  ${item.publishTime}`);
      console.log(`       ${item.url}\n`);
    });
  })
  .catch(err => console.error('[ERROR]', err.message));
```

---

## 示例 5：Shell — curl 快速查看

```bash
# 查看今日自助报道（格式化 JSON）
DATE=$(date +%Y-%m-%d)
curl -s "https://openclaw.36krcdn.com/media/aireport/$DATE/ai_report_articles.json" | python3 -m json.tool

# 只显示标题列表
curl -s "https://openclaw.36krcdn.com/media/aireport/$DATE/ai_report_articles.json" \
  | python3 -c "import sys,json; [print(f\"#{i['rank']:>2} {i['title']}\") for i in json.load(sys.stdin)['data']]"
```

---

## 示例 6：Python — 定时轮询（每 2 小时刷新）

```python
import httpx
import datetime
import time

def poll_aireport(interval_seconds: int = 7200):
    """每 interval_seconds 秒查询一次自助报道，打印有变化的文章。"""
    last_titles = set()

    while True:
        today = datetime.date.today().isoformat()
        url = f"https://openclaw.36krcdn.com/media/aireport/{today}/ai_report_articles.json"

        try:
            resp = httpx.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                current_titles = {item["title"] for item in data["data"]}

                new_titles = current_titles - last_titles
                if new_titles:
                    print(f"[{datetime.datetime.now()}] 新增自助报道文章：")
                    for t in new_titles:
                        print(f"  - {t}")
                else:
                    print(f"[{datetime.datetime.now()}] 自助报道无变化，共 {len(current_titles)} 篇")

                last_titles = current_titles
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(interval_seconds)

# Demo: 每 2 小时检查一次
poll_aireport(7200)
```

---

## 示例 7：Python — 将自助报道写入 CSV

```python
import httpx
import csv
import datetime

def export_aireport_to_csv(date: str = None, output_file: str = "aireport.csv"):
    """将指定日期的自助报道文章导出为 CSV 文件。"""
    if date is None:
        date = datetime.date.today().isoformat()

    url = f"https://openclaw.36krcdn.com/media/aireport/{date}/ai_report_articles.json"
    resp = httpx.get(url, timeout=10)
    resp.raise_for_status()

    articles = resp.json()["data"]

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "title", "author", "publishTime", "url"])
        writer.writeheader()
        for item in articles:
            writer.writerow({
                "rank": item["rank"],
                "title": item["title"],
                "author": item["author"],
                "publishTime": item["publishTime"],
                "url": item["url"],
            })

    print(f"已导出 {len(articles)} 条记录到 {output_file}")

# Demo
export_aireport_to_csv("2026-03-17", "aireport_20260317.csv")
```

---

## 示例 8：Python — 查询最近 N 天数据并去重汇总

```python
import httpx
import datetime

def fetch_recent_aireport(days: int = 7):
    """
    查询最近 days 天的自助报道文章，去重后按发布时间排序返回。
    """
    BASE_URL = "https://openclaw.36krcdn.com/media/aireport/{date}/ai_report_articles.json"
    today = datetime.date.today()
    seen_urls = set()
    all_articles = []

    for i in range(days):
        date = (today - datetime.timedelta(days=i)).isoformat()
        url = BASE_URL.format(date=date)
        try:
            resp = httpx.get(url, timeout=10)
            if resp.status_code == 200:
                for article in resp.json().get("data", []):
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        all_articles.append(article)
        except Exception:
            pass

    # 按发布时间倒序排列
    all_articles.sort(key=lambda x: x.get("publishTime", ""), reverse=True)
    return all_articles

# Demo
articles = fetch_recent_aireport(days=3)
print(f"最近 3 天共 {len(articles)} 篇自助报道：")
for a in articles[:5]:
    print(f"  [{a['publishTime']}] {a['title']} — {a['author']}")
```
