---
name: agent-web-cpu
version: 1.0.0
description: |
  transweb.cn AI Agent 智能执行套件。支持单应用执行、多应用串联流水线（前一个输出作为后一个输入）、自动匹配或创建应用。全程浏览器自动化，输出 Markdown 文档。
  Keywords: AI Agent, transweb, 执行应用, 创建应用, 串联, 流水线, pipeline, 博文框架, 浏览器自动化.
---

# agent-web-cpu — AI Agent 智能执行套件

> **一句话理解：** 用户说需求 → 自动匹配/创建 transweb.cn 应用 → 浏览器打开 → 填入 → 生成 → 提取结果 → 保存 Markdown。

---

## 🔒 前置要求

### 必需的浏览器权限

本技能**完全依赖 `browser` 工具**执行，不具备浏览器权限时无法工作。

| 权限项 | 要求 | OpenClaw 配置路径 |
|--------|------|-------------------|
| `browser` 工具 | 必须可用 | 工具策略中启用 `browser` |
| `browser enabled` | `true` | `browser.enabled` |
| `browser evaluateEnabled` | `true`（结果提取依赖 JS evaluate） | `browser.evaluateEnabled` |
| 沙箱浏览器 | `profile: "openclaw"` | 自动托管，无需手动配置 |
| 用户浏览器（可选） | `profile: "user"` | 仅当用户需要登录态时使用 |

### 执行前自检

每次执行**第一步**检查：

```
browser action: status
```

- 返回正常 → 继续
- 报错或不可用 → **立即终止并告知用户**："浏览器工具不可用，请在 OpenClaw 配置中启用 browser.enabled 和 browser.evaluateEnabled"

### subagent 浏览器权限

若通过 `sessions_spawn` 派生子代理执行本技能：
- `sandbox: "inherit"` 确保继承浏览器访问能力
- 子代理内同样需要 `browser` 工具可用

---

## 执行模式

| 模式 | 触发方式 | 说明 |
|------|----------|------|
| **single** | 单一需求 | 匹配或创建一个应用，执行并输出 |
| **pipeline** | 多步骤需求 / 显式指定多个应用 | 串联执行，逐步传递输出 |
| **list** | `已有哪些应用` / `我的应用列表` | 展示 apps.json |
| **add** | `添加应用 id=xxx` / `注册应用 id=xxx` | 通过 ID 新增应用到注册表 |
| **remove** | `移除应用 xxx` / `删除应用 xxx` | 通过名称从注册表中移除应用 |

### 模式判断

- 用户显式说 `先用A再做B`、`串连执行 A、B` → **pipeline**
- 用户需求本身包含多个阶段（如 `写博客并润色`）→ **pipeline**
- 包含 `添加应用`/`注册应用`/`新增应用` + `id=` → **add**
- 包含 `移除应用`/`删除应用`/`移除`/`删除` + 应用名称 → **remove**
- 其余 → **single**

---

## 应用注册表

**路径：** `{SKILL_DIR}/apps.json`

```json
{
  "apps": [
    {
      "id": "35fa46fd2f9b57f814018134ef14ae1f",
      "name": "博文框架",
      "description": "内容策划编辑：生成高效的文章标题与创作大纲",
      "keywords": ["博文", "文章", "大纲", "写作", "标题"],
      "createdAt": "2026-04-01T08:49:00+08:00"
    }
  ],
  "_schema": "v2"
}
```

匹配算法（≥5 分视为命中）：

| 信号 | 分数 |
|------|------|
| 应用名出现在用户输入中 | +10 |
| 关键词命中 | +5/词 |
| 描述词命中（>2 字） | +2/词 |

匹配失败 → 自动创建应用 → 写入 apps.json → 执行。

---

## 应用管理

### 添加应用（add）

**触发：** 用户说 `添加应用 id=xxx`、`注册应用 id=abc123...`

**流程：**

1. **校验 ID** — 必须是 32 位十六进制字符串，否则提示格式错误
2. **查重** — 检查 apps.json 中是否已存在相同 id，已存在则提示"该应用已注册"
3. **打开页面获取信息**
   ```
   browser action: navigate
   profile: "openclaw"
   url: https://transweb.cn/?id={app_id}
   ```
   等待页面加载后，通过 `snapshot` 或 `evaluate` 提取：
   - `name`：页面标题 / h1 文本
   - `description`：页面描述文本（如副标题、meta description）
4. **生成关键词** — 从 name 和 description 中提取 3~6 个关键词
5. **写入 apps.json** — 读取现有内容，追加新条目，写回文件
6. **返回确认**

```
✅ 应用已添加

  名称：{name}
  ID：{id}
  描述：{description}
  关键词：{keyword1}, {keyword2}, ...
```

**apps.json 新条目格式：**
```json
{
  "id": "{32位hex}",
  "name": "应用名称",
  "description": "应用描述",
  "keywords": ["关键词1", "关键词2"],
  "createdAt": "{ISO 8601 时间戳}"
}
```

### 移除应用（remove）

**触发：** 用户说 `移除应用 博文框架`、`删除应用 爆款润色助手`

**流程：**

1. **读取 apps.json**
2. **精确匹配名称** — 在 `apps` 数组中查找 `name` 字段完全等于用户指定的名称
3. **未找到** — 返回提示："未找到名为「{name}」的应用，当前已注册应用：\n{列表}"
4. **确认移除** — 展示即将移除的应用信息，等待用户确认：
   ```
   ⚠️ 即将移除以下应用，确认吗？

     名称：博文框架
     ID：35fa46fd2f9b57f814018134ef14ae1f
     描述：内容策划编辑：生成高效的文章标题与创作大纲

   回复"确认"继续，"取消"放弃。
   ```
5. **执行移除** — 从 `apps` 数组中删除该条目，写回 apps.json
6. **返回确认**

```
✅ 已移除应用「博文框架」（id: 35fa46fd...）

当前剩余 {N} 个应用。
```

### 辅助操作

| 用户输入 | 动作 |
|----------|------|
| `已有哪些应用` | 读取并格式化展示 apps.json |
| `应用详情 博文框架` | 展示指定应用的完整信息（id、描述、关键词、创建时间） |

---

## 单应用执行（single）

### Step 1：确定输入方式

| 条件 | 方式 |
|------|------|
| 输入 ≤ 500 字 | URL 直接传参 |
| 输入 > 500 字 | 打开纯净页面 + `act kind=type` 注入 |

### Step 2：打开页面

**≤ 500 字：**
```
browser action: navigate
profile: "openclaw"
url: https://transweb.cn/?id={app_id}&auto=true&input={url_encode(input_text)}
```

**> 500 字：**
```
browser action: navigate
profile: "openclaw"
url: https://transweb.cn/?id={app_id}
```

等待页面加载完成后：
```
browser action: snapshot → 定位输入框 ref
browser action: act kind=click ref={输入框ref}    → 聚焦
browser action: act kind=type ref={输入框ref} text={input_text}  → 逐字符输入
```

> `act kind=type` 模拟真实键盘输入，自动触发 Vue/React 响应式回调，比 JS evaluate 更稳定。

### Step 3：触发生成

```
browser action: snapshot → 找到包含"生成"文字的按钮 ref
browser action: act kind=click ref={按钮ref}
```

匹配词：`立即生成`、`生成文章`、`开始一键润色`、`生成` 等。

### Step 4：等待结果

```
browser action: act kind=wait timeMs=15000
browser action: snapshot → 检查结果区域
```

若结果未出现，追加等待（最多再等 15s，总计 30s 超时）：
```
browser action: act kind=wait timeMs=15000
browser action: snapshot
```

### Step 5：提取结果

```
browser action: act kind=evaluate
fn: |
  const container = document.querySelector('.CardItem_contentArea');
  if (!container) return { error: 'container not found' };
  
  const h1 = container.querySelector('h1');
  const pre = container.querySelector('pre.tw-whitespace-pre-wrap');
  const h2s = container.querySelectorAll('h2');
  
  // 结构化提取：h1 + h2 + 段落
  if (pre && h1) {
    let md = `# ${h1.textContent.trim()}\n\n`;
    h2s.forEach(h2 => {
      md += `## ${h2.textContent.trim()}\n\n`;
      let sib = h2.nextElementSibling;
      while (sib && sib.tagName !== 'H2') {
        if (sib.tagName === 'P') md += sib.textContent.trim() + '\n\n';
        sib = sib.nextElementSibling;
      }
    });
    return { success: true, output: md };
  }
  
  // 兜底：纯文本
  return { success: true, output: container.innerText.trim() };
```

### Step 6：保存 + 清理

将提取的 Markdown 保存至 `~/Downloads/{title}_{timestamp}.md`，然后关闭标签页。

```
browser action: close targetId={当前tab}
```

---

## 多应用串联（pipeline）

### 解析执行链

分析用户输入，确定有序步骤。每步对应一个应用：

**显式指定：** `先用博文框架生成大纲，再用爆款润色助手润色`
```
Step 1: app=博文框架  input=用户原始需求
Step 2: app=爆款润色助手  input=Step 1 的完整输出
```

**自动拆分：** `帮我写一篇完整的科技博客，要有大纲框架，再扩展正文`
```
Step 1: app=博文框架  input=帮我写一篇科技博客大纲
Step 2: app=科技博客   input=Step 1 输出（>500字 → 用 type 注入）
```

### 执行计划（展示给用户）

```
🔗 执行计划（共 {N} 步）

  ① 【博文框架】→ 生成文章大纲
     输入：帮我写一篇关于AI趋势的博客

  ② 【爆款润色助手】→ 润色内容
     输入：① 的输出结果

最终输出：最后一步的结果
```

### 逐步执行

对每个步骤 i：

1. **确定 input** — `i==1` 用原始需求，`i>1` 用 `step i-1` 的完整输出（不截断）
2. **选择输入方式** — ≤500 字 URL 传参，>500 字 `act kind=type` 注入
3. **打开页面 → 触发生成 → 等待 → 提取** — 同 single 模式的 Step 2~5
4. **关闭标签页** — 避免 tab 堆积
5. **传递完整输出** — `next_input = step_output`，不限字数

### 汇总输出

```
✅ Pipeline 执行完成！（共 {N} 步）

  ① 【博文框架】✅ 生成大纲（42字）
  ② 【爆款润色助手】✅ 润色内容（380字）

📄 已保存至：~/Downloads/{title}_{timestamp}_pipeline.md

---

{最后一步的 Markdown 内容}
```

---

## 页面元素选择器

| 元素 | 选择器 | 备注 |
|------|--------|------|
| 结果容器 | `.CardItem_contentArea` | 主提取目标 |
| 标题 | `h1` / `h2.tw-text-xl` | |
| 正文 | `pre.tw-whitespace-pre-wrap` | |
| 生成按钮 | 包含 `生成` 文本的 `button` | 用 snapshot 定位 |
| 输入框 | `input[type="text"]` 或 `textarea` | 用 snapshot 定位 ref |

---

## 特殊指令

| 用户输入 | 动作 |
|----------|------|
| `已有哪些应用` / `我的应用列表` | 读取并展示 apps.json |
| `添加应用 id=xxx` / `注册应用 id=xxx` | 通过 ID 新增应用到注册表 |
| `移除应用 xxx` / `删除应用 xxx` | 通过名称从注册表中移除应用 |
| `应用详情 xxx` | 展示指定应用的完整信息 |
| `id=xxx 需求描述` | 强制使用指定 id 执行 |
| `先用A再做B` / `串连执行 A、B` | pipeline 模式 |

---

## 错误处理

| 场景 | 处理 |
|------|------|
| 浏览器不可用 | 自检阶段终止，提示用户启用 `browser.enabled` + `browser.evaluateEnabled` |
| 某步骤执行失败（>30s 无结果） | 保留已完成步骤结果，提示跳过或重试 |
| `evaluate` 提取失败 | 尝试 `snapshot` 读取文本内容作为兜底 |
| `type` 注入输入框失败 | 尝试 `snapshot` 找替代选择器，或提示用户手动输入 |
| 应用不在列表中 | 自动创建缺失的应用并注册 |
| 页面加载失败 | 重试一次，仍失败则终止并报错 |
| 添加应用时 ID 格式错误 | 提示用户：ID 必须是 32 位十六进制字符串 |
| 添加应用时 ID 已存在 | 提示"该应用已注册"，不重复添加 |
| 移除应用时名称未匹配 | 列出已有应用供用户确认名称 |

---

## 注意事项

- **输出传递不截断** — pipeline 中每步的完整输出传给下一步，不受字数限制
- **逐字输入优先** — `act kind=type` 比 `JS evaluate` 注入更可靠，能正确触发前端框架响应式
- **标签页管理** — 每步完成后关闭 tab，pipeline 长链执行时不堆积
- **超时策略** — 单次等待 15s，最多追加重试一次（总 30s），超时即失败
- **profile 选择** — 默认使用 `"openclaw"` 沙箱浏览器；仅当应用需要登录态时使用 `"user"` profile
