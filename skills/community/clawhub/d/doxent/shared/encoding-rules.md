# 编码规则

## UTF-8 要求

凡是请求体里包含文本字段，都必须显式按 UTF-8 处理。

这条规则适用于：
- 用户直接提供的文本
- 从文件中读取的文本
- 从网页或外部内容抓取的文本
- 请求发送前通过变量拼接出来的文本

不要假设文本天然就是合法 UTF-8。

## PowerShell 5.1 规则

PowerShell 5.1 可能会把请求体静默重编码为系统 ANSI 代码页。只要是在 PowerShell 5.1 下发送带 JSON body 的 API 请求，都必须先把 JSON 字符串转成 UTF-8 字节数组再发送。

```powershell
$body = @{ title = "标题"; content = $content } | ConvertTo-Json -Depth 10
$utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
Invoke-RestMethod -Uri $url -Method Post -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -Headers $headers
```


