# API 文档输出模板

生成 API 文档时，按以下格式输出。将 `{{占位符}}` 替换为实际内容。

---

# {{网站名}} - {{功能名}} API

> 通过 form-to-api skill 逆向分析生成  
> 生成时间：{{YYYY-MM-DD}}  
> 目标网页：{{target_url}}

---

## 接口信息

| 项目 | 值 |
|------|-----|
| Endpoint | `{{METHOD}} {{full_url}}` |
| Content-Type | `{{content_type}}` |
| 认证方式 | {{auth_method}} |

---

## 请求参数

> 字段类型说明：
> - `<用户输入>` — 需要替换为实际值
> - `<固定值>` — 保持原样，不需要修改
> - `<自动生成>` — 由脚本自动生成（时间戳等）
> - `<从浏览器提取>` — 需要通过 Cookie 提取脚本获取

| 字段名 | 类型 | 必填 | 说明 | 示例/默认值 |
|-------|------|-----|------|------------|
| {{field_name}} | {{type}} | {{required}} | {{description}} | `{{example}}` |

---

## Cookie 提取

```bash
# 提取并缓存 Cookie（首次或过期后使用）
COOKIE=$(python3 <skill_dir>/scripts/extract_cookies.py {{target_url}})

# 强制刷新 Cookie
COOKIE=$(python3 <skill_dir>/scripts/extract_cookies.py {{target_url}} --force)
```

---

## 调用示例

### curl

```bash
COOKIE=$(python3 <skill_dir>/scripts/extract_cookies.py {{target_url}})

curl -s -X {{METHOD}} "{{full_url}}" \
  -H "Content-Type: {{content_type}}" \
  -H "Cookie: $COOKIE" \
  -d '{{request_body_example}}'
```

### Python

```python
import subprocess, json, requests

def get_cookie():
    result = subprocess.run(
        ["python3", "<skill_dir>/scripts/extract_cookies.py", "{{target_url}}"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

cookie = get_cookie()
headers = {
    "Content-Type": "{{content_type}}",
    "Cookie": cookie
}
payload = {{request_body_dict}}

resp = requests.{{method_lower}}("{{full_url}}", headers=headers, json=payload)
print(resp.json())
```

---

## 响应格式

```json
{{response_example}}
```

---

## 注意事项

- Cookie 缓存在 `/tmp/form_api_cookies/` 下，有效期 1 小时
- 若接口返回 401/403，请重新提取 Cookie：加 `--force` 参数
- {{additional_notes}}
