# CDP Bridge 工具详细参数

## browser_get_tabs

获取所有已连接的浏览器标签页列表。

**参数：** 无

**返回示例：**
```json
{
    "tabs": [
        {"id": "702640649", "url": "https://example.com", "title": "Example"},
        {"id": "702640591", "url": "https://google.com", "title": "Google"}
    ],
    "active_tab": "702640649"
}
```

---

## browser_scan

扫描当前页面内容，返回简化 HTML 或纯文本。

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `tabs_only` | boolean | false | 仅返回标签页列表，不返回页面内容 |
| `switch_tab_id` | string | "" | 切换到此标签页后再扫描 |
| `text_only` | boolean | false | 返回纯文本而非 HTML |

**返回示例：**
```json
{
    "status": "success",
    "metadata": {
        "tabs_count": 15,
        "active_tab": "702640640"
    },
    "content": "页面文本内容..."
}
```

**建议：** 大页面使用 `text_only: true` 节省 token。

---

## browser_execute_js

在页面中执行 JavaScript。

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `script` | string | 必填 | JS 代码 |
| `switch_tab_id` | string | "" | 切换到此标签页后执行 |
| `no_monitor` | boolean | false | 跳过 DOM 变化监控（更快） |

**示例：**
```json
{
    "script": "document.querySelector('button.submit').click()"
}
```

```json
{
    "script": "document.title"
}
```

---

## browser_switch_tab

切换活动标签页（不影响用户可见的浏览器标签）。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `tab_id` | string | 必填，从 browser_get_tabs 获取 |

**示例：**
```json
{"tab_id": "702640640"}
```

---

## browser_navigate

跳转到新 URL。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `url` | string | 必填，目标 URL |

**示例：**
```json
{"url": "https://example.com"}
```

---

## browser_screenshot

截取页面截图。

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `tab_id` | string | "" | 指定标签页，空则用当前活动页 |

**返回：** Base64 PNG 图片数据

---

## browser_cookies

读取 Cookie。

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | string | "" | 指定 URL，空则用当前页面 URL |

---

## browser_wait

等待 JavaScript 条件返回真值。

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `condition_js` | string | 必填 | JS 表达式/脚本 |
| `timeout` | number | 10 | 最大等待秒数 |
| `interval` | number | 0.5 | 检查间隔秒数 |
| `switch_tab_id` | string | "" | 切换后等待 |

**示例：**
```json
{
    "condition_js": "document.querySelector('.result') !== null",
    "timeout": 15
}
```

---

## browser_batch

批量执行多个 CDP 命令。

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `commands` | array | 必填 | CDP 命令数组 |
| `tab_id` | string | "" | 继承给未指定 tabId 的命令 |
| `timeout` | number | 20 | 等待结果秒数 |

**命令格式：**
```json
{"cmd": "cdp", "method": "DOM.getDocument", "params": {"depth": 1}}
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `Another debugger is already attached` | 目标页已有 DevTools | 切换其他标签页 |
| `Tab not found` | tab_id 不存在 | 重新 get_tabs |
| `Script execution failed` | JS 错误 | 检查语法 |
| `Navigation failed` | URL 无效或网络问题 | 检查 URL |