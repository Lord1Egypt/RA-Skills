# 爬虫调试经验库（v3.4.0）

> 场景 1 交付物模板（v3.4.0 新增，源自 TRAE 社区爬虫教程）
> 配套方法论：M22-M26
> 用途：爬虫开发过程中的 8 大调试场景识别+解决方案

## 使用说明

**AI 行为**：
- 用户在场景 1 调试过程中遇到问题 → 主动匹配本库中的场景
- 识别信号词 → 提供对应解决方案
- 3 次未解决 → 强制换思路（规则 14）

**用户行为**：
- 描述错误现象（如"403""抓不到数据""字段为空"）
- AI 匹配调试场景 → 提供解决方案

---

## 调试场景 1：SPA 动态加载抓不到数据

### 识别信号
- "requests.get 抓不到数据"
- "网页内容是空的"
- "HTML 里没有我要的字段"
- 响应状态码 200 但内容为空

### 根因
网站是 SPA（单页应用），数据由 JavaScript 动态加载，HTML 源码只有骨架。

### 解决方案
1. **Network 面板分析**：F12 → Network → XHR/Fetch → 搜索目标数据
2. **找真实 API**：定位返回数据的 XHR 请求
3. **复制 cURL**：右键请求 → Copy → Copy as cURL
4. **转 Python**：用 `requests` 重写
5. **参考方法论**：M22 SPA 动态 API 识别

### 教程案例
> Airtable 社区爬虫：表面能看帖子列表，但 `requests.get()` 抓到的是空壳 HTML。实际数据来自 Algolia 搜索 API（XHR 请求）。

---

## 调试场景 2：API Key 失效（401/403）

### 识别信号
- "401 Unauthorized"
- "403 Forbidden"
- "复制的 Key 几分钟就失效"
- "API Key 是动态的"

### 根因
网站使用动态生成的 API Key（如 Algolia），静态复制很快过期。

### 解决方案
1. **溯源 Key**：在 Network 面板找到 Key 来源请求
2. **用 Session 模拟**：
   ```python
   session = requests.Session()
   session.get(page_url)  # 获取初始 Cookie
   key_resp = session.post(auth_endpoint, ...)  # 获取动态 Key
   api_resp = session.post(data_api, headers={'X-API-Key': key_resp.json()['key']})
   ```
3. **自动刷新**：捕获 401/403 → 重新获取 Key → 重试
4. **参考方法论**：M23 动态 API Key 模拟

### 教程案例
> Airtable 社区：Algolia API Key 是动态生成的，直接复制几分钟后失效。用 Session 模拟完整链路后，每次抓取前先刷新 Key。

---

## 调试场景 3：requests.Session Cookie 管理

### 识别信号
- "多步请求 Cookie 丢失"
- "第二步请求需要第一步的 Cookie"
- "CSRF Token 怎么传递"

### 根因
多步请求中，后续请求依赖前面设置的 Cookie，普通 `requests.get()` 不保留 Cookie。

### 解决方案
1. **用 Session 对象**：
   ```python
   session = requests.Session()
   # 所有请求都用 session.get() / session.post()
   # Cookie 自动保存和传递
   ```
2. **CSRF Token 流程**：
   ```python
   # Step 1: 访问页面，获取 CSRF Cookie
   session.get(page_url)
   csrf_token = session.cookies.get('csrf_token')
   
   # Step 2: 用 CSRF Token 请求 API
   session.post(api_url, headers={'X-CSRF-Token': csrf_token})
   ```
3. **参考方法论**：M23 § Step 3

### 教程原话
> "`requests.Session` 的妙用：在需要多步请求、且后续请求依赖于之前请求设置的 Cookies 的场景下，`requests.Session()` 对象能极大地简化Cookie管理。"

---

## 调试场景 4：User-Agent 与请求头

### 识别信号
- "403 Forbidden"
- "请求被拒绝"
- "网站识别到爬虫"

### 根因
默认 `requests` 的 User-Agent 是 `python-requests/2.x.x`，被网站识别为爬虫。

### 解决方案
1. **设置真实 User-Agent**：
   ```python
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
       'Accept': 'application/json, text/plain, */*',
       'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
       'Referer': page_url,  # 重要：很多 API 校验 Referer
   }
   requests.get(url, headers=headers)
   ```
2. **完整请求头**：从 Network 复制完整 cURL，转为 Python
3. **参考方法论**：M23 § Step 4

### 教程原话
> "设置一个接近真实浏览器的 `User-Agent` 和其他必要的请求头 (如 `Accept`, `X-Requested-With`, `X-CSRF-Token`) 对于成功模拟前端请求至关重要。"

---

## 调试场景 5：API 响应字段解析

### 识别信号
- "字段不存在"
- "字段名不对"
- "数据路径错误"

### 根因
API 响应的字段名可能与显示名不一致，或字段嵌套在深层路径。

### 解决方案
1. **打印原始 JSON**：
   ```python
   import json
   resp = requests.get(url, headers=headers)
   print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
   ```
2. **找真实字段名**：不要假设，必须实际查看
3. **识别嵌套路径**：如 `hits[].title` / `results.items[0].author.name`
4. **处理字段缺失**：
   ```python
   title = item.get('title', '')  # 字段不存在时返回空字符串
   ```

### 教训案例
> Airtable 社区：帖子内容在 `reply` 或 `first_post` 字段（非 `content`），必须打印原始 JSON 才能发现。

### 教程原话
> "仔细分析API响应结构：拿到API返回的JSON数据后，不能想当然地认为某个字段一定存在或名称是什么。务必打印原始JSON，仔细检查其结构。"

---

## 调试场景 6：增量唯一 ID 设计

### 识别信号
- "重复抓取"
- "怎么避免重复"
- "增量同步失败"

### 根因
没有设计唯一 ID，或 ID 不稳定（如用标题，标题被编辑后变新数据）。

### 解决方案
1. **优先用 URL 解析 ID**：最稳定
   ```python
   import re
   url = "https://community.airtable.com/t/topic/12345"
   tid = re.search(r'/t/topic/(\d+)', url).group(1)  # "12345"
   ```
2. **其次用 API 原生 ID**：`item['id']`
3. **缓存 ID 集合**：用 JSON 文件或 SQLite
4. **过滤已抓取**：
   ```python
   existing_ids = load_cache()
   new_data = [item for item in all_data if item['id'] not in existing_ids]
   ```
5. **参考方法论**：M24 增量唯一 ID 设计

### 教程案例
> Airtable 社区：从 `topic_url` 中解析 `tid` 作为唯一 ID，最稳定。

### 教程原话
> "实现增量抓取、避免重复处理的核心是为每个条目找到一个唯一且持久的ID。对于Airtable社区，最终选用了从 `topic_url` 中解析出的 `tid` 作为主要唯一标识。"

---

## 调试场景 7：飞书 SDK 兼容性

### 识别信号
- "飞书写入失败"
- "字段类型不匹配"
- "日期格式错误"
- "超链接写入异常"

### 根因
飞书多维表格对字段类型有严格要求，与 API 响应格式不一致。

### 解决方案
1. **日期转 Unix 毫秒**：
   ```python
   ts_ms = int(dt.timestamp() * 1000)  # 不是秒，是毫秒
   ```
2. **超链接转 dict**：
   ```python
   link = {"link": "https://...", "text": "查看原文"}  # 不是字符串
   ```
3. **文本长度限制**：单行 1000 字符，多行 10000 字符
4. **单选必须是已有选项**：否则飞书会创建新选项
5. **参考方法论**：M26 飞书多维表格双存储

### 教训案例
> 日期字段一开始传字符串 "2026-07-26" → 写入失败
> 改为 Unix 毫秒时间戳 → 成功
> 超链接字段一开始传字符串 URL → 写入失败
> 改为 dict 结构 → 成功

### 教程原话
> "将数据写入外部系统（如飞书多维表格）时，必须严格遵守其对字段类型和数据格式的要求。日期通常需要是Unix时间戳（毫秒或秒），超链接需要特定JSON结构。"

---

## 调试场景 8：HTML 元素定位（AI 识别失败）

### 识别信号
- "AI 没识别到我要的字段"
- "字段提取不到"
- "BeautifulSoup 解析不到"

### 根因
AI 没看到真实 HTML 结构，靠猜写字段路径。

### 解决方案
1. **用户用 DevTools 定位**：
   - F12 → 选择元素箭头 → 点击目标元素
   - 右键 HTML 代码 → Edit as HTML → Ctrl+A → Ctrl+C
2. **粘贴给 AI**：把 HTML 发给 AI
3. **AI 基于真实 HTML 写选择器**：
   ```python
   from bs4 import BeautifulSoup
   soup = BeautifulSoup(html, 'html.parser')
   title = soup.select_one('.topic-title').text
   ```
4. **参考方法论**：M25 HTML 元素定位法

### 教程原话
> "当需要抓取网页上特定数据，但 AI 没有识别到，可以这样定向获取 HTML 内容，发送给 AI。选择元素的时候，范围可以稍微大一点，要包含整个元素块。"

---

## 调试通用流程

### 标准调试 5 步法

```
1. 复现问题
   - 记录错误信息
   - 确认可稳定复现

2. 定位根因
   - 匹配 8 大调试场景
   - 如不匹配，分析新场景

3. 提供解决方案
   - 按本库的解决方案执行
   - 给 AI 充分上下文（日志、报错、截图）

4. 验证修复
   - 重新运行代码
   - 确认问题解决

5. 沉淀经验
   - 如是新场景，追加到本库
```

### 3 次未解决规则（规则 14）

> "修复同一个问题，超过 3 次还没解决，需要让 AI 想一些其他办法，而不是用同样的方案打转。"

**AI 行为**：同一问题 3 次未解决 → 强制提示用户换思路：
- 换工具（requests → selenium / playwright）
- 换方案（API → HTML 解析 / 反之）
- 换模型（用推理模型重新规划）
- 求助（社区 / 官方文档）

---

## 与其他模板的关系

- 前置：[website-analysis-script-template.md](website-analysis-script-template.md)（先分析网站，再调试）
- 配套：[feishu-base-storage-template.md](feishu-base-storage-template.md)（飞书写入问题参考本库）
- 配套：[scenario-1-prompt-template.md](scenario-1-prompt-template.md)（生成最终 Prompt）

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
