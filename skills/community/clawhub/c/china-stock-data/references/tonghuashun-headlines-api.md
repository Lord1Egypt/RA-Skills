# 同花顺快讯 (Tonghuashun Headlines) API 参考

## 端点

```
GET https://news.10jqka.com.cn/tapp/news/push/stock
User-Agent: Mozilla/5.0
```

## 响应结构 (2026-05 已验证)

```json
{
  "code": "200",
  "msg": "成功",
  "time": "1778742053",
  "data": {
    "list": [
      {
        "id": "4363571",
        "seq": "676688293",
        "title": "标题",
        "digest": "摘要正文...",
        "url": "https://news.10jqka.com.cn/20260514/c676688293.shtml",
        "shareUrl": "https://news.10jqka.com.cn/tapp/news/share/676688293/",
        "ctime": 1778742017,
        "tag": "A股",
        "stock": [{"name":"沪深300期指","stockCode":"IF9999"}]
      }
    ],
    "filter": {"...": "..."},
    "total": 20
  }
}
```

## 字段说明

| JSON字段 | Python字段 | 说明 |
|----------|-----------|------|
| `data.list` | (数组) | **注意**：不是 `data` 直接是数组！需要 `data.get('list', [])` |
| `.shareUrl` | 分享链接 | 字段名带大写 U (JavaScript camelCase) |
| `.url` | 原始链接 | 完整URL |
| `.ctime` | 时间戳(秒) | 需 `datetime.fromtimestamp()` 转换为可读时间 |
| `.digest` | 摘要 | 非必需字段，有则提供 |
| `.title` | 标题 | 必需字段 |

## 历史变更记录

- **2026-05之前**: `data` 直接是数组，可用 `resp.json().get('data', [])`
- **2026-05 (当前)**: `data` 变为对象 `{"list":[...], "filter":..., "total": N}`，字段 `share_url` → `shareUrl`

## Python 代码模板

```python
def fetch_thailand_headlines():
    try:
        url = 'https://news.10jqka.com.cn/tapp/news/push/stock'
        resp = requests.get(url, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        if resp.status_code != 200:
            return {'source':'同花顺快讯','error':f'HTTP {resp.status_code}'}
        data = resp.json()
        items = data.get('data', {}).get('list', [])
        if not items:
            return {'source':'同花顺快讯','error':'data.list为空'}
        headlines = []
        for item in items[:10]:
            ts = item.get('ctime', '')
            time_str = ''
            if ts and str(ts).isdigit():
                from datetime import datetime
                time_str = datetime.fromtimestamp(int(ts)).strftime('%H:%M')
            headlines.append({
                'title': item.get('title',''),
                'digest': item.get('digest',''),
                'time': time_str,
                'url': item.get('shareUrl', item.get('url','')),
            })
        return {'source':'同花顺快讯','headlines':headlines}
    except Exception as e:
        return {'source':'同花顺快讯','error':f'获取失败: {type(e).__name__}: {str(e)[:100]}'}
```

## 常见错误

1. **`data`误判为数组**: 旧代码 `resp.json().get('data', [])` 取到的是 dict，对其做 `[:10]` 切片会抛 TypeError，被 `except:` 静默吞掉
2. **字段名大小写**: `share_url` 不存在，正确字段是 `shareUrl`
3. **时间戳未格式化**: `ctime` 是秒级 Unix 时间戳，直接输出不好看，需转为 `HH:MM` 格式
4. **静默吞异常**: 不要用裸 `except:`，否则无法定位错误
