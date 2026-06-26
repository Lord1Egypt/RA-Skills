# mcp-chrome API 参考

## 关于 mcp-chrome

mcp-chrome 是一个 Chrome 浏览器插件，将 Chrome DevTools 协议（CDP）封装为 MCP server，允许 AI Agent 以用户已登录的会话操控浏览器。

安装：https://github.com/hangwin/mcp-chrome

默认监听：`http://127.0.0.1:12306/mcp`（可在插件设置中修改）

## 通用调用函数

```bash
SESSION_ID="your-session-id-here"

mcp_call() {
  local id=$1 tool=$2 args=$3
  curl -s -X POST "http://127.0.0.1:12306/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "mcp-session-id: $SESSION_ID" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":$id,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}"
}

# 解析响应（提取 result 文本）
parse_result() {
  python3 -c "
import sys, json
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try: print(json.loads(item.get('text', '')).get('result', ''))
            except: print(item.get('text', ''))
"
}
```

## 常用工具

### get_windows_and_tabs — 列出所有标签页

```bash
mcp_call 1 "get_windows_and_tabs" "{}" | parse_result | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
for w in d.get('windows', []):
    for t in w.get('tabs', []):
        print(f'tabId={t[\"tabId\"]} url={t[\"url\"][:80]}')
"
```

### chrome_navigate — 导航到 URL

```bash
mcp_call 2 "chrome_navigate" "{\"url\":\"https://sh.ke.com/xiaoqu/5011000015858/\",\"tabId\":309607900}"
sleep 6  # 必须等待 JS 渲染
```

参数：
- `url`：目标 URL
- `tabId`：可选，指定 Tab；不传则使用当前激活 Tab

### chrome_javascript — 在页面执行 JS

```bash
mcp_call 3 "chrome_javascript" "{\"tabId\":309607900,\"code\":\"return document.body.innerText\"}" | parse_result
```

参数：
- `tabId`：目标 Tab ID
- `code`：JS 代码字符串，使用 `return` 返回值

常用 JS 片段：
```javascript
// 读取页面全文
return document.body.innerText

// 读取当前 URL
return location.href

// 找小区详情链接
return document.querySelector('a.agentCardResblockLink')?.href

// 截取部分文本（节省 token）
return document.body.innerText.substring(0, 5000)
```

### chrome_screenshot — 截图

```bash
mcp_call 4 "chrome_screenshot" "{\"tabId\":309607900,\"storeBase64\":false,\"savePng\":true,\"width\":1280,\"height\":800}"
# 截图保存到用户 Downloads 目录
```

### chrome_switch_tab — 切换 Tab

```bash
mcp_call 5 "chrome_switch_tab" "{\"tabId\":309607900}"
```

### chrome_click_element — 点击元素

```bash
# CSS 选择器
mcp_call 6 "chrome_click_element" "{\"tabId\":309607900,\"selector\":\"a.agentCardResblockLink\",\"waitForNavigation\":true,\"timeout\":8000}"

# XPath
mcp_call 7 "chrome_click_element" "{\"tabId\":309607900,\"selector\":\"//a[contains(text(),'查看小区详情')]\",\"selectorType\":\"xpath\",\"waitForNavigation\":true}"
```

## 完整读页面流程

```bash
SESSION_ID="your-session-id"
TAB=309607900

# 1. 导航
mcp_call 10 "chrome_navigate" "{\"url\":\"https://sh.ke.com/xiaoqu/5011000015858/\",\"tabId\":$TAB}" > /dev/null
sleep 6

# 2. 读文本
mcp_call 11 "chrome_javascript" "{\"tabId\":$TAB,\"code\":\"return document.body.innerText\"}" \
  | parse_result > /tmp/page.txt

# 3. 检测验证码
if grep -q "请在下图\|请按语序" /tmp/page.txt; then
    echo "⚠️ 验证码！需要用户手动处理"
    exit 1
fi

# 4. 解析
python3 parse_beike.py xiaoqu < /tmp/page.txt
```

## 注意事项

- **等待时间**：每次 navigate 后必须等待 ≥6 秒，贝壳页面为 React SPA，JS 渲染需要时间
- **并发限制**：同一 Tab 不能并发操作；多小区并行请用不同 Tab
- **验证码频率**：连续快速访问成交记录页必然触发；每次访问之间建议间隔 10+ 秒
- **成交价格**：贝壳对所有用户隐藏成交价，即使已登录；需联系链家/贝壳经纪人获取
- **数据时效**：均价为"X月参考均价"，非实时成交价；在售房源挂牌价可能与实际成交价差 5-15%
