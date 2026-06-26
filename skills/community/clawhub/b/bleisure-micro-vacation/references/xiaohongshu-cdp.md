# 小红书真实链接抓取（CDP 模式）

通过 CDP（Chrome DevTools Protocol）控制用户本地 Chrome，在小红书搜索推荐地点，提取 **点赞最高** 的笔记链接。

## 前置条件

本 Skill 复用 `holiday-enough` Skill 的 CDP 基础设施（同一台机器共享 `localhost:3456` 代理）。

### 检查 CDP 环境

```bash
node ~/.cursor/skills/holiday-enough/scripts/check-deps.mjs
```

- 需要 **Node.js 22+**
- 需要 **Chrome 远程调试已开启**

**若 check-deps 报 Chrome 未连接**，告诉用户：

> 需要开启 Chrome 远程调试才能抓取小红书真实链接。已为你打开设置页面，请勾选 **"Allow remote debugging for this browser instance"**，完成后告诉我。

**若 holiday-enough 未安装** 或脚本路径不存在：直接跳过 CDP 抓取，回退到「关键词为主」模式（见下文），不要报错阻断整个推荐流程。

---

## 抓取流程

### 时机与优先级

在主工作流 **推荐地点确定后、输出方案之前**，**自动执行** CDP 抓取。

**这不是可选步骤**——与高德链接同等重要。CDP 可用时必须抓取，抓取结果必须嵌入最终输出。只有 CDP 确认不可用（前置检查未通过且用户拒绝开启）时才回退为关键词。

### 第一步：搜索

用推荐地点的名称作为关键词搜索。关键词策略（选 1～2 组即可）：

- `"{地点名}"` —— 精准匹配（如 `"透微醺研究所"`）
- `"{地点名} {城市}"` —— 补城市限定（如 `"大兜路 杭州 夜晚"`）

```bash
curl -s "http://localhost:3456/new?url=https://www.xiaohongshu.com/search_result?keyword=KEYWORD&source=web_search_result_note"
```

记录返回的 `targetId`。

### 第二步：提取笔记列表（含点赞数）

等待页面加载（约 2～3 秒），提取前 10 条搜索结果的标题、链接和点赞数：

```bash
curl -s -X POST "http://localhost:3456/eval?target=TARGET_ID" \
  -d 'JSON.stringify([...document.querySelectorAll("section.note-item")].slice(0, 10).map(item => ({title: item.querySelector(".title span")?.textContent?.trim() || item.querySelector(".title")?.textContent?.trim() || "", url: item.querySelector("a")?.href || "", likes: item.querySelector(".like-wrapper .count")?.textContent?.trim() || item.querySelector("[class*=\"like\"] span")?.textContent?.trim() || "0"})))'
```

**DOM 选择器说明**：小红书前端频繁改版，上述选择器可能失效。如果返回空数组或全部字段为空：

1. 先用 `/eval` 查看实际 DOM 结构：
   ```bash
   curl -s -X POST "http://localhost:3456/eval?target=TARGET_ID" \
     -d 'document.querySelector(".feeds-container")?.innerHTML?.substring(0, 2000) || document.body.innerHTML.substring(0, 2000)'
   ```
2. 根据实际结构调整选择器，重新提取。

### 第三步：排序并选取 Top 笔记

在提取到的结果中：

1. 将 `likes` 字段转为数字（处理 `万` 后缀：`1.2万` → `12000`）
2. 按点赞数 **降序** 排列
3. 取 **Top 1～3** 条

### 第四步：清理

```bash
curl -s "http://localhost:3456/close?target=TARGET_ID"
```

---

## 输出格式

将抓取到的笔记嵌入 `output-template.md` 的小红书区块。格式：

```markdown
**小红书推荐笔记：**

- [笔记标题](https://www.xiaohongshu.com/...) · ❤️ 1.2万
- [笔记标题](https://www.xiaohongshu.com/...) · ❤️ 3860
```

附一句：**链接可能失效，以 App 内搜索为准。**

---

## 回退策略（CDP 不可用时）

若以下任一情况出现，**跳过 CDP 抓取，不要阻断推荐流程**：

- `check-deps.mjs` 脚本不存在（holiday-enough 未安装）
- Chrome 未开启远程调试且用户不想开
- CDP proxy（localhost:3456）无响应
- 小红书页面需要登录或返回空结果

回退为原有模式：

```markdown
**小红书怎么搜：**

- `关键词 A`
- `关键词 B`
```

在输出中 **不提 CDP 失败**，只自然地给关键词即可。

---

## 注意事项

- 小红书反爬严格，**必须** 通过 CDP 浏览器模式访问，不要用 WebSearch 或 WebFetch 直接抓取小红书页面。
- 需要用户 Chrome 中 **已登录** 小红书才能看到完整搜索结果。如果提取内容为空，提示用户先在 Chrome 中登录。
- 每次搜索只开 1 个标签页，提取完立即关闭，不要密集操作。
- 点赞数仅作为排序参考，展示时保留原始格式（如 `1.2万`），不要自己换算后展示。
