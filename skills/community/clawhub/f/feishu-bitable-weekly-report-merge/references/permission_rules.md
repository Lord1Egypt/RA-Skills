# Permission Rules Reference

## URL 解析

```python
from urllib.parse import urlparse, parse_qs

def parse_bitable_url(url):
    """从多维表格 URL 中提取 app_token 和 table_id"""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    app_token = path_parts[0] if path_parts else None
    
    query = parse_qs(parsed.query)
    table_id = query.get('table', [None])[0]
    
    return app_token, table_id
```

示例：
```
输入：https://asiainfo.feishu.cn/base/FDo4bVmnVaYRJlslJttcPwgwnfh?table=tblRjin7OM9XvEDL&view=vew3qPDrS3
app_token = "FDo4bVmnVaYRJlslJttcPwgwnfh"
table_id  = "tblRjin7OM9XvEDL"
```

## 权限判断

```python
def check_permission(result):
    if result.get("success") == True:
        return "accessible"
    error_msg = result.get("message", "") + result.get("error", "")
    if "forBidden" in error_msg:
        return "forbidden"
    if "frequency limit" in error_msg:
        return "rate_limited"
    return "unknown_error"
```

## 重试策略

```python
def fetch_with_retry(doc_id, max_retries=2):
    for attempt in range(max_retries):
        result = feishu_fetch_doc(doc_id=doc_id)
        status = check_permission(result)
        
        if status == "accessible" or status == "forbidden":
            return status
        
        if status == "rate_limited" and attempt < max_retries - 1:
            wait_seconds = 3 * (attempt + 1)
            time.sleep(wait_seconds)
            continue
    
    return "failed_after_retries"
```

## 并发控制

每批最多 10 个并发请求，超出时分批执行，批次间隔 1 秒。
