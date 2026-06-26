# 云端打印 API 故障实录

日期：2026-05-15
服务：`https://any.webprinter.cn`
目标：Xerox WorkCentre 7835 @ 192.168.65.130:9100

## 故障1：form-encoded → HTTP 404（已修复）

**现象**：`_cvturl` 和 `_pfs` 用 `application/x-www-form-urlencoded` 返回 404（不是 415，不是未授权）。

**根因**：服务端路由只匹配 `application/json`，form-encoded 的请求被路由层直接 404，给人"接口未部署"的错觉。

**修复**（`skillPrint.py`）：`convert_url_to_pdf()` 和 `print_for_skill()` 从 `_post_form` → `_post_json`，printer/config 传原生 JSON 对象而非 `json.dumps` 后嵌入 form 字段。

**验证 curl**：
```bash
# form-encoded → 404
curl -X POST .../_pfs -H "Content-Type: application/x-www-form-urlencoded" -d "printer={...}&url=..."

# JSON body → 200
curl -X POST .../_pfs -H "Content-Type: application/json" -d '{"printer":{...},"url":"..."}'
```

## 故障2：_cvturl 偶发超时（已内置降级）

**现象**：`_cvturl` 在多次调用中约 60% 概率超时（`The read operation timed out`），上传 `uploadFileMCP` 正常。

**降级方案**（`print_file_for_skill.py` 内置）：
1. 先走 `_cvturl`（60s 超时）
2. 失败 → LibreOffice `--headless --convert-to pdf` 本地转换
3. 重新 `uploadFileMCP` 上传 PDF
4. 继续执行 `_pfs` 打印

**验证日志**：
```
[降级] _cvturl 失败 (The read operation timed out)，回退到 LibreOffice 本地转换...
```

## 故障3：_pfs 间歇性不可用（TCP 9100 兜底）

**现象**：`_pfs` 在部分时段完全超时（curl `--max-time 30` 返回 exit code 28，无 HTTP 响应）。

**兜底方案**：TCP 9100 裸发 PDF 到打印机。
```python
import socket
s = socket.create_connection(('192.168.65.130', 9100), timeout=10)
s.sendall(open('/tmp/file.pdf', 'rb').read())
s.close()
```
⚠️ 此方式无法传份数/双面/纸张等配置。

## 时间线

| 时间 | 接口 | 结果 |
|------|------|------|
| 02:10 | uploadFileMCP | ✅ 200 |
| 02:10 | _cvturl (form) | ❌ 404 |
| 02:10 | _pfs (form) | ❌ 404 |
| 02:14 | _cvturl (JSON) | ✅ 200 |
| 02:15 | _pfs (JSON) | ✅ 200 `success:true` |
| 02:20 | _cvturl (JSON) | ❌ timeout→LibreOffice降级 |
| 02:20 | _pfs (JSON) | ✅ 200 |
| 02:24 | _pfs (JSON) | ✅ 200 |
| 02:34 | _cvturl (JSON) | ❌ timeout→降级 |
| 02:34 | _pfs (JSON) | ✅ 200 |
| 02:35 | _cvturl (JSON) | ❌ timeout→降级 |
| 02:35 | _pfs (JSON) | ❌ timeout（TCP 9100兜底） |
