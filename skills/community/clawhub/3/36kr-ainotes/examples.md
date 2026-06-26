# 使用示例集合 — 36kr AI 测评笔记

## 示例 1：Python — 基础查询（今日测评笔记）

```python
import urllib.request
import json
import datetime

def get_today_ainotes():
    today = datetime.date.today().isoformat()  # "2026-03-18"
    url = f"https://openclaw.36krcdn.com/media/ainotes/{today}/ai_notes.json"

    with urllib.request.urlopen(url, timeout=10) as resp:
        notes = json.loads(resp.read().decode("utf-8"))

    print(f"=== 36kr AI 测评笔记 {today}  共 {len(notes)} 篇 ===")
    for i, item in enumerate(notes, 1):
        pub_ts = item.get("publishTime", 0)
        pub_str = datetime.datetime.fromtimestamp(pub_ts / 1000).strftime("%Y-%m-%d %H:%M") if pub_ts else "?"
        circles = "、".join(c.get("circleName", "") for c in (item.get("circleNames") or [])) or "—"
        products = "、".join(p.get("productName", "") for p in (item.get("productNames") or [])) or "—"
        print(f"  #{i:>2}  {item['title']}")
        print(f"       作者：{item['authorName']}  发布：{pub_str}")
        print(f"       圈子：{circles}  产品：{products}")
        print(f"       链接：{item['noteUrl']}")
        print()

# 运行
get_today_ainotes()
```

**输出示例：**
```
=== 36kr AI 测评笔记 2026-03-18  共 20 篇 ===
   #1  服装电商必备：美图设计室AI功能全测
       作者：氪友5sc4  发布：2026-03-18 10:30
       圈子：营销辅助  产品：—
       链接：https://36aidianping.com/note-detail/3477557660550660?channel=skills
```

---

## 示例 2：Python — 查询指定日期

```python
import urllib.request
import urllib.error
import json

def get_ainotes_by_date(date: str):
    """
    查询指定日期的测评笔记列表。
    Args:
        date: "YYYY-MM-DD" 格式，如 "2026-03-18"
    """
    url = f"https://openclaw.36krcdn.com/media/ainotes/{date}/ai_notes.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[!] {date} 的测评笔记数据不存在")
        else:
            print(f"[ERROR] HTTP {e.code}")
        return None

# Demo: 查询 2026-03-18
notes = get_ainotes_by_date("2026-03-18")
if notes:
    titles = [n["title"] for n in notes]
    print(f"共 {len(titles)} 篇笔记：", titles[:3])
```

---

## 示例 3：Java — HttpClient 查询

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDate;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

public class AiNotesDemo {

    private static final String URL_TEMPLATE =
        "https://openclaw.36krcdn.com/media/ainotes/%s/ai_notes.json";

    public static void main(String[] args) throws Exception {
        String date = LocalDate.now().toString();  // "2026-03-18"
        String url = String.format(URL_TEMPLATE, date);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() == 200) {
            JSONArray notes = JSONArray.parseArray(response.body());
            DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")
                    .withZone(ZoneId.systemDefault());

            System.out.println("=== 36kr AI 测评笔记 " + date + " ===");
            for (int i = 0; i < notes.size(); i++) {
                JSONObject note = notes.getJSONObject(i);
                long ts = note.getLongValue("publishTime");
                String pubTime = fmt.format(Instant.ofEpochMilli(ts));
                System.out.printf("  #%d  %s — %s  发布: %s%n",
                        i + 1,
                        note.getString("title"),
                        note.getString("authorName"),
                        pubTime);
                System.out.printf("       %s%n", note.getString("url"));
            }
        } else if (response.statusCode() == 404) {
            System.out.println("[!] " + date + " 的测评笔记数据不存在");
        }
    }
}
```

---

## 示例 4：JavaScript / Node.js — fetch 查询

```javascript
const today = new Date().toISOString().slice(0, 10); // "2026-03-18"
const url = `https://openclaw.36krcdn.com/media/ainotes/${today}/ai_notes.json`;

fetch(url)
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(notes => {
    console.log(`=== 36kr AI 测评笔记 ${today}  共 ${notes.length} 篇 ===`);
    notes.forEach((item, i) => {
      const pubTime = new Date(item.publishTime).toLocaleString("zh-CN");
      const circles = (item.circleNames || []).map(c => c.circleName).join("、") || "—";
      const products = (item.productNames || []).map(p => p.productName).join("、") || "—";
      console.log(`  #${i + 1}  ${item.title}`);
      console.log(`       作者: ${item.authorName}  |  发布: ${pubTime}`);
      console.log(`       圈子: ${circles}  产品: ${products}`);
      console.log(`       ${item.noteUrl}\n`);
    });
  })
  .catch(err => console.error('[ERROR]', err.message));
```

---

## 示例 5：Shell — curl 快速查看

```bash
# 查看今日测评笔记（格式化 JSON）
DATE=$(date +%Y-%m-%d)
curl -s "https://openclaw.36krcdn.com/media/ainotes/$DATE/ai_notes.json" | python3 -m json.tool

# 只显示标题和作者列表
curl -s "https://openclaw.36krcdn.com/media/ainotes/$DATE/ai_notes.json" \
  | python3 -c "
import sys, json
notes = json.load(sys.stdin)
for i, n in enumerate(notes, 1):
    print(f'#{i:>2} {n[\"title\"]} — {n[\"authorName\"]}  {n[\"noteUrl\"]}')
"
```

---

## 示例 6：Python — 按圈子筛选笔记

```python
import urllib.request
import json
import datetime

def get_ainotes_by_circle(circle_name: str, date: str = None):
    """筛选特定圈子的测评笔记。"""
    if date is None:
        date = datetime.date.today().isoformat()
    url = f"https://openclaw.36krcdn.com/media/ainotes/{date}/ai_notes.json"
    with urllib.request.urlopen(url, timeout=10) as resp:
        notes = json.loads(resp.read().decode("utf-8"))

    matched = [n for n in notes if circle_name in [c.get("circleName") for c in (n.get("circleNames") or [])]]
    print(f"圈子「{circle_name}」共 {len(matched)} 篇笔记：")
    for n in matched:
        print(f"  {n['title']} — {n['authorName']}")
        print(f"  {n['noteUrl']}")
    return matched

# Demo: 查看「营销辅助」圈子的笔记
get_ainotes_by_circle("营销辅助")
```

---

## 示例 7：Python — 按关联产品筛选笔记

```python
import urllib.request
import json
import datetime

def get_ainotes_by_product(product_name: str, date: str = None):
    """筛选包含特定产品的测评笔记。"""
    if date is None:
        date = datetime.date.today().isoformat()
    url = f"https://openclaw.36krcdn.com/media/ainotes/{date}/ai_notes.json"
    with urllib.request.urlopen(url, timeout=10) as resp:
        notes = json.loads(resp.read().decode("utf-8"))

    matched = [n for n in notes if product_name in [p.get("productName") for p in (n.get("productNames") or [])]]
    print(f"产品「{product_name}」相关笔记 {len(matched)} 篇：")
    for n in matched:
        print(f"  {n['title']} — {n['authorName']}")
        print(f"  {n['noteUrl']}")
    return matched

# Demo: 查看包含「豌豆云」的测评笔记
get_ainotes_by_product("豌豆云")
```

---

## 示例 8：Python — 查询最近 N 天数据并去重汇总

```python
import urllib.request
import urllib.error
import json
import datetime

def fetch_recent_ainotes(days: int = 7):
    """
    查询最近 days 天的测评笔记，去重后按发布时间倒序返回。
    """
    BASE_URL = "https://openclaw.36krcdn.com/media/ainotes/{date}/ai_notes.json"
    today = datetime.date.today()
    seen_ids = set()
    all_notes = []

    for i in range(days):
        date = (today - datetime.timedelta(days=i)).isoformat()
        url = BASE_URL.format(date=date)
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                notes = json.loads(resp.read().decode("utf-8"))
                for note in notes:
                    nid = note.get("noteId")
                    if nid not in seen_ids:
                        seen_ids.add(nid)
                        all_notes.append(note)
        except urllib.error.HTTPError:
            pass
        except Exception:
            pass

    all_notes.sort(key=lambda x: x.get("publishTime", 0), reverse=True)
    return all_notes

# Demo
notes = fetch_recent_ainotes(days=3)
print(f"最近 3 天共 {len(notes)} 篇测评笔记（已去重）：")
for n in notes[:5]:
    pub_ts = n.get("publishTime", 0)
    pub_str = datetime.datetime.fromtimestamp(pub_ts / 1000).strftime("%Y-%m-%d %H:%M") if pub_ts else "?"
    print(f"  [{pub_str}] {n['title']} — {n['authorName']}")
```
