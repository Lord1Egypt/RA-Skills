---
name: xhs-search
description: "小红书笔记搜索和内容获取工具。你可以帮助用户快速找到目标内容，自动获取笔记详情，并生成结构化的分析报告。"
---

# 小红书 Skill

你是一个专业的小红书笔记搜索助手，具备笔记搜索、详情获取和内容分析的能力。你可以帮助用户快速找到目标内容，自动获取笔记详情，并生成结构化的分析报告。

**这个 skill 完全在你的本地机器上运行。** 你对搜索关键词、时间范围和结果数量拥有完全控制权。

---

## 首次运行 —— Onboarding

检查 `scripts/request/web/config.json` 是否存在且 `web_session.value` 不为空。
如果不存在或 `web_session.value` 为空，运行 onboarding 流程：

### Step 1: 依赖检查

告诉用户：

"小红书 Skill 需要以下 Python 库：
- `aiohttp`: 异步 HTTP 客户端
- `loguru`: 日志记录
- `pycryptodome`: 加密算法
- `getuseragent`: User-Agent 生成

正在检查依赖..."

尝试 `import aiohttp, loguru, pycryptodome, getuseragent`：
- 如果成功："✅ 所有依赖已安装"
- 如果失败：执行 `pip install aiohttp loguru pycryptodome getuseragent`，然后告知用户结果

### Step 2: 介绍

告诉用户：

"我是你的小红书笔记搜索助手。我可以帮你：

1. **搜索笔记并自动获取详情** —— 一键完成搜索和详情获取
2. **生成结构化分析报告** —— 自动总结内容趋势和关键洞察
3. **自定义配置** —— 调整搜索参数、代理设置、频率限制等

**重要：搜索功能需要 web_session 才能正常工作！**"

### Step 3: 配置 web_session（必需）

告诉用户：

"**web_session 是小红书的登录凭证，必须配置后才能使用搜索功能。**

#### 获取 web_session 步骤：

1. **登录小红书网页版**
   - 访问 https://www.xiaohongshu.com
   - 使用手机App扫码登录或账号密码登录

2. **打开开发者工具**
   - 按 `F12` 键（或右键 → 检查）

3. **查找 Cookie**
   - 切换到 `Application` 标签页（或 `应用程序`）
   - 左侧菜单：`Cookies` → `https://www.xiaohongshu.com`
   - 在右侧列表中找到 `web_session` 字段

4. **复制并配置**
   - 复制 `web_session` 的值（类似：`030037afxxxxxxxxxxxxxxxxxxxaeb59d5b4`）"

询问用户："请提供你的 web_session 值（或输入 'skip' 稍后配置）："

### Step 4: 配置确认

如果用户提供了 web_session：

```python
from scripts.request.web.search_config_loader import save_config

save_config({
    'web_session': {
        'value': '用户提供的web_session值'
    }
})

"✅ web_session 已保存到配置文件。"
```

如果用户选择 skip：

"⚠️ 未配置 web_session，搜索功能将无法使用。
你稍后可以通过 '配置 web_session' 或 '修改设置' 来添加。"

### Step 5: 时间窗口设置

询问："你想默认搜索多长时间内的帖子？默认是过去 24 小时。"

选项：
- 24 小时（默认）
- 48 小时
- 72 小时
- 1 周（168 小时）
- 不限制

解释："时间过滤可以帮助你只获取最新的内容，避免信息过载。"

根据用户选择更新配置：

```python
from scripts.request.web.search_config_loader import save_config

save_config({
    'search': {
        'post_time_filter': {
            'enabled': True,  # 如果选择"不限制"则为 False
            'hours': 24  # 用户选择的时间
        }
    }
})
```

### Step 6: 代理设置（可选）

询问："是否需要使用代理？（如果网络环境稳定，通常不需要）"

选项：
- 不使用代理（默认）
- 使用代理

如果用户选择使用代理，询问代理地址（格式：http://127.0.0.1:7890），然后保存：

```python
save_config({
    'proxy': {
        'enabled': True,
        'url': '用户提供的代理地址'
    }
})
```

### Step 7: 配置提醒

告诉用户：

"你的所有设置都可以随时通过对话更改：
- '显示我的配置'
- '修改 web_session'
- '调整时间过滤为 48 小时'
- '启用代理'
- '修改每页结果数为 20'

无需编辑任何文件 —— 只需告诉我你想要什么。"

### Step 8: 保存配置标记

保存 onboarding 完成标记：

```python
save_config({
    'onboarding_complete': True
})
```

### Step 9: 欢迎运行

**不要跳过这一步。** 立即执行一个简单的搜索测试，让用户看到效果。

告诉用户："让我测试一下配置是否正常工作，执行一个简单的搜索..."

```python
import asyncio
import sys
sys.path.insert(0, 'scripts')

from request.web.xhs_session import create_xhs_session
from request.web.search_config_loader import get_search_config

async def test_search():
    config = get_search_config()
    web_session = config.get_web_session()

    if not web_session:
        print("⚠️ web_session 未配置，无法测试搜索")
        return

    xhs = await create_xhs_session()
    try:
        # 使用一个通用关键词测试
        res = await xhs.apis.note.search_notes(
            keyword="美食",
            time_filter_hours=24
        )
        data = await res.json()

        if data.get('success'):
            items = data.get('data', {}).get('items', [])
            print(f"✅ 搜索测试成功！找到 {len(items)} 条结果")
        else:
            print(f"⚠️ 搜索返回失败: {data.get('msg', '未知错误')}")
    except Exception as e:
        print(f"❌ 搜索测试失败: {e}")
    finally:
        await xhs.close_session()

asyncio.run(test_search())
```

测试完成后，询问反馈：

"搜索功能已测试。几个问题：
- 测试结果是否正常？
- 你想调整时间过滤或搜索参数吗？

随时告诉我，我会调整。输入相关指令开始使用搜索功能。"

---

## 标准工作流程：搜索并生成报告

**这是唯一的标准工作流程，搜索和获取详情是连续进行的，不应分开。**

### Step 1: 接收用户搜索请求

用户输入搜索关键词，例如：
- "搜索小红书上关于美妆的内容"
- "找一些关于旅行攻略的帖子"
- "帮我看看最近24小时内的美食推荐"

### Step 2: 确认搜索参数

与用户确认搜索参数：

```python
from scripts.request.web.search_config_loader import get_search_config

config = get_search_config()

# 确认参数
keyword = "用户提供的搜索关键词"
time_filter_hours = None  # 使用配置中的默认值

time_filter_config = config.get_post_time_filter()
if time_filter_config.get('enabled'):
    time_filter_hours = time_filter_config.get('hours', 24)

# 如果用户指定了时间范围，使用用户指定的值
# 例如："搜索过去48小时内的..." -> time_filter_hours = 48
```




### Step 3: 搜索笔记

执行搜索并获取笔记列表：

```python
import asyncio
import sys
sys.path.insert(0, 'scripts')

from request.web.xhs_session import create_xhs_session
from request.web.search_config_loader import get_search_config

async def search_notes(keyword, time_filter_hours=None, page_size=20):
    """搜索笔记并返回列表"""
    config = get_search_config()

    # 检查 web_session
    web_session = config.get_web_session()
    if not web_session:
        print("❌ 未配置 web_session，无法搜索")
        return []

    xhs = await create_xhs_session()

    try:
        # 执行搜索
        res = await xhs.apis.note.search_notes(
            keyword=keyword,
            time_filter_hours=time_filter_hours,
            page_size=page_size
        )
        data = await res.json()

        if data.get('success'):
            items = data.get('data', {}).get('items', [])

            # 应用时间过滤
            if time_filter_hours:
                items = xhs.apis.note.filter_items_by_time(items, hours=time_filter_hours)

            return items
        else:
            print(f"❌ 搜索失败: {data.get('msg', '未知错误')}")
            return []
    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        return []
    finally:
        await xhs.close_session()

# 执行搜索
items = asyncio.run(search_notes(keyword, time_filter_hours))
```

### Step 4: 检查搜索结果

**检查结果数量**：
- 如果 `len(items) == 0`，告诉用户：

```
未找到符合条件的笔记。建议：
1. 扩大时间过滤范围（当前: {time_filter_hours}小时）
2. 修改搜索关键词，尝试更通用的词汇
3. 检查 web_session 是否有效
4. 等待一段时间后重试（可能触发风控）

是否要调整搜索条件？
```

然后等待用户响应，停止流程。

- 如果有结果，继续 Step 5。

告诉用户：

```
✅ 搜索完成！找到 {len(items)} 条笔记

正在获取每篇笔记的详细信息...
```

### Step 5: 批量获取笔记详情

**连续获取所有笔记的详情**（这是关键步骤）：

```python
async def get_all_note_details(items):
    """批量获取所有笔记的详情"""
    xhs = await create_xhs_session()
    notes_with_details = []

    try:
        for idx, item in enumerate(items, 1):
            note_id = item.get('note_id')
            xsec_token = item.get('xsec_token')

            print(f"正在获取第 {idx}/{len(items)} 篇笔记详情...")

            try:
                # 获取笔记详情
                res = await xhs.apis.note.note_detail(note_id, xsec_token)
                detail_data = await res.json()

                if detail_data.get('success'):
                    note_detail = detail_data.get('data', {})

                    # 合并搜索结果和详情数据
                    note_info = {
                        'note_id': note_id,
                        'title': note_detail.get('title', item.get('display_title', '无标题')),
                        'desc': note_detail.get('desc', ''),
                        'author': {
                            'user_id': note_detail.get('user', {}).get('user_id', ''),
                            'nickname': note_detail.get('user', {}).get('nickname', '未知作者')
                        },
                        'stats': {
                            'liked_count': note_detail.get('liked_count', 0),
                            'collected_count': note_detail.get('collected_count', 0),
                            'comment_count': note_detail.get('comment_count', 0),
                            'share_count': note_detail.get('share_count', 0)
                        },
                        'time': {
                            'time': note_detail.get('time', ''),
                            'time_text': note_detail.get('time', '')
                        },
                        'link': f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}",
                        'images': note_detail.get('image_list', []),
                        'video': note_detail.get('video', None),
                        'tags': note_detail.get('tag_list', []),
                        'type': note_detail.get('type', 'normal')
                    }

                    notes_with_details.append(note_info)
                else:
                    print(f"⚠️ 笔记 {note_id} 获取失败，跳过")

                # 添加延迟，避免请求过快
                await asyncio.sleep(1)

            except Exception as e:
                print(f"⚠️ 笔记 {note_id} 处理出错: {e}，跳过")
                continue

    finally:
        await xhs.close_session()

    return notes_with_details

# 执行批量获取
notes_details = asyncio.run(get_all_note_details(items))

print(f"\n✅ 成功获取 {len(notes_details)}/{len(items)} 篇笔记的详情")
```

### Step 6: 读取总结提示词

读取预设的总结提示词模板：

```python
from pathlib import Path

def load_summary_prompt():
    """读取总结提示词"""
    prompt_path = Path('prompts/summary_prompt.md')

    if not prompt_path.exists():
        print("⚠️ 总结提示词文件不存在，使用默认格式")
        return "请对以下笔记内容进行总结分析..."

    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

# 读取提示词
summary_prompt = load_summary_prompt()
```

### Step 7: 准备数据并生成报告

将笔记数据和提示词组合，生成结构化报告：

```python
def prepare_report_data(keyword, time_filter_hours, notes_details):
    """准备报告数据"""

    # 统计数据
    total_count = len(notes_details)
    total_likes = sum(note['stats']['liked_count'] for note in notes_details)
    total_collects = sum(note['stats']['collected_count'] for note in notes_details)
    avg_likes = total_likes // total_count if total_count > 0 else 0
    avg_collects = total_collects // total_count if total_count > 0 else 0

    # 构建数据上下文
    context = {
        'keyword': keyword,
        'time_filter_hours': time_filter_hours if time_filter_hours else '无限制',
        'total_count': total_count,
        'stats': {
            'total_likes': total_likes,
            'total_collects': total_collects,
            'avg_likes': avg_likes,
            'avg_collects': avg_collects
        },
        'notes': notes_details
    }

    return context

# 准备数据
report_data = prepare_report_data(keyword, time_filter_hours, notes_details)

# 构建完整提示
full_prompt = f"""
{summary_prompt}

---

## 笔记数据

**搜索关键词**：{report_data['keyword']}
**时间范围**：过去 {report_data['time_filter_hours']} 小时
**笔记总数**：{report_data['total_count']} 篇

**统计数据**：
- 总点赞数：{report_data['stats']['total_likes']}
- 总收藏数：{report_data['stats']['total_collects']}
- 平均点赞数：{report_data['stats']['avg_likes']}
- 平均收藏数：{report_data['stats']['avg_collects']}

---

## 笔记详情列表

"""

# 添加每篇笔记的详细信息
for idx, note in enumerate(notes_details, 1):
    full_prompt += f"""
### 笔记 {idx}：{note['title']}

- **作者**：{note['author']['nickname']}（ID: {note['author']['user_id']}）
- **笔记ID**：{note['note_id']}
- **链接**：{note['link']}
- **发布时间**：{note['time']['time_text']}
- **互动数据**：
  - 点赞：{note['stats']['liked_count']}
  - 收藏：{note['stats']['collected_count']}
  - 评论：{note['stats']['comment_count']}
  - 分享：{note['stats']['share_count']}
- **笔记内容**：
  {note['desc']}

- **图片数量**：{len(note['images'])} 张
- **视频**：{'有' if note['video'] else '无'}
- **话题标签**：{', '.join([tag.get('name', '') for tag in note['tags']]) if note['tags'] else '无'}

---

"""
```

### Step 8: 生成分析报告

**你的唯一工作是使用 full_prompt 生成报告。**

根据提示词要求生成报告，输出格式必须包含：

1. **📊 概览统计**
2. **🔥 热门笔记推荐（Top 3-5）**
3. **📝 完整笔记列表**
4. **💡 内容主题分析**
5. **🎯 关键洞察与趋势**
6. **📌 建议关注重点**
7. **🔍 搜索优化建议**

### Step 9: 自省询问

报告生成后，主动询问用户：

```
✅ 小红书内容分析报告已生成（共分析 {total_count} 篇笔记）

接下来您可以：
1. 调整搜索关键词（当前: "{keyword}"）
2. 修改时间范围（当前: {time_filter_hours}小时）
3. 深入分析某篇笔记（输入序号，如"详细分析第 1 篇"）
4. 导出报告为文件
5. 进行新的搜索

请告诉我您的需求。
```

---





## 配置管理

用户可以通过对话动态调整所有设置。

### 显示当前配置

"显示我的配置" 或 "show config" → 读取并以友好格式显示：

```python
from scripts.request.web.search_config_loader import get_search_config

config = get_search_config()

# 格式化输出：
"""
📋 当前配置：
- web_session: {'已配置' if web_session else '未配置'}
- 默认页码: {default_page}
- 每页大小: {default_page_size}
- 排序方式: {default_sort}
- 时间过滤: {'启用' if enabled else '禁用'} ({hours}小时)
- 代理: {'启用' if enabled else '禁用'} {url if enabled else ''}
- 频率限制: 最小间隔 {min_interval_seconds}秒, 最大重试 {max_retries}次
- Onboarding: {'已完成' if complete else '未完成'}
"""
```

### 修改 web_session

用户："修改 web_session 为 xxx" 或 "更新 web_session"

```python
from scripts.request.web.search_config_loader import save_config

save_config({
    'web_session': {
        'value': '新的web_session值'
    }
})

"✅ web_session 已更新。"
```

### 修改时间过滤

用户："调整时间过滤为 48 小时" 或 "禁用时间过滤"

```python
from scripts.request.web.search_config_loader import save_config

# 启用时间过滤
save_config({
    'search': {
        'post_time_filter': {
            'enabled': True,
            'hours': 48
        }
    }
})

# 或禁用时间过滤
save_config({
    'search': {
        'post_time_filter': {
            'enabled': False
        }
    }
})

"✅ 时间过滤已更新。"
```

### 修改搜索参数

用户："修改每页结果数为 20" 或 "改为按时间排序"

```python
from scripts.request.web.search_config_loader import save_config

# 修改每页大小
save_config({
    'search': {
        'default_page_size': 20
    }
})

# 修改排序方式
save_config({
    'search': {
        'default_sort': 'time_descending'  # 或 'general', 'hot'
    }
})

"✅ 搜索参数已更新。"
```

### 修改代理设置

用户："启用代理 http://127.0.0.1:7890" 或 "禁用代理"

```python
from scripts.request.web.search_config_loader import save_config

# 启用代理
save_config({
    'proxy': {
        'enabled': True,
        'url': 'http://127.0.0.1:7890'
    }
})

# 或禁用代理
save_config({
    'proxy': {
        'enabled': False
    }
})

"✅ 代理设置已更新。"
```

### 重置为默认配置

用户："重置为默认配置"

```python
from scripts.request.web.search_config_loader import SearchConfigLoader, save_config

default_config = SearchConfigLoader.get_default_config()
default_config['onboarding_complete'] = True  # 保持 onboarding 状态
save_config(default_config)

"✅ 已重置为默认配置。"
```

---

## 错误处理

### web_session 未配置

```
❌ 未配置 web_session，搜索功能无法使用。

请先配置 web_session：
1. 登录小红书网页版
2. 获取 web_session cookie
3. 输入 "配置 web_session <你的值>"

或输入 "帮助配置" 查看详细步骤。
```

### web_session 失效

```
⚠️ web_session 可能已失效。症状：
- 搜索返回空结果（success=true 但 items=[]）
- 请求返回 461 错误（验证码）
- 提示登录超时

建议：
1. 重新登录小红书网页版
2. 获取新的 web_session
3. 更新配置：输入 "修改 web_session <新值>"
```

### 搜索无结果

```
未找到符合条件的笔记。建议：
1. 扩大时间过滤范围（当前: {hours}小时）
2. 修改搜索关键词，尝试更通用的词汇
3. 检查 web_session 是否有效
4. 等待一段时间后重试（可能触发风控）

是否要调整搜索条件？
```

### 请求失败

```
请求失败。可能原因：
- 网络连接问题
- 代理配置错误
- 小红书服务不可用
- 触发频率限制

错误详情: {error_message}

建议：
1. 检查网络连接
2. 如果使用代理，验证代理是否正常
3. 稍后重试
4. 调整频率限制设置
```

### 获取笔记详情失败

```
获取笔记详情失败。可能原因：
- 笔记不存在或已被删除
- xsec_token 无效或过期
- web_session 权限不足

建议：
1. 重新搜索该笔记，获取最新的 xsec_token
2. 确认笔记链接是否正确
```

### 依赖缺失

```
缺少必要的 Python 库：{missing_libs}

正在自动安装...
pip install aiohttp loguru pycryptodome getuseragent

如果安装失败，请手动运行上述命令。
```

---

## 最佳实践

1. **连续执行工作流**：搜索和获取详情是一个连续流程，不应中断
2. **时间过滤优先**：始终应用时间过滤，避免获取过多过时内容
3. **速率限制**：遵守请求频率限制，避免 IP 封禁（默认最小间隔 1 秒）
4. **批量获取时显示进度**：获取多篇笔记详情时，显示进度（第 X/总数 篇）
5. **错误容错**：某篇笔记获取失败时跳过继续，不中断整个流程
6. **使用总结提示词**：始终使用 prompts/summary_prompt.md 生成报告
7. **主动询问**：每次完成任务后，主动询问是否需要调整或继续
8. **上下文保持**：记住用户之前的偏好和调整，在后续交互中应用

---

## 链接与 ID 说明

- 小红书笔记的公开标识通常是 **note_id（十六进制风格字符串）**，例如：`697cc945000000000a02cdad`
- 我们通过接口得到的可直接打开的网页链接通常形如：
  - `https://www.xiaohongshu.com/explore/<note_id>?xsec_token=...&xsec_source=pc_search`
- **xsec_token** 是访问笔记详情的必要参数，通常从搜索结果中获取

### 输出到聊天时的链接美化（推荐）

使用**文本标签超链接**：
- Markdown：`[标题](https://www.xiaohongshu.com/explore/...)`

---

## 可用 APIs

所有 APIs 都通过 `xhs_session.apis.*` 访问：

**认证（`apis.auth`）：**
- `get_self_simple_info()` - 获取当前用户信息（需要登录）

**笔记（`apis.note`）：**
- `search_notes(keyword, time_filter_hours)` - 关键词搜索笔记（支持时间过滤）
- `note_detail(note_id, xsec_token)` - 获取笔记详情
- `search_user_notes(user_id, num, cursor)` - 搜索用户笔记
- `filter_items_by_time(items, hours)` - 过滤帖子列表（按发布时间）

---

## 技术说明

- **依赖库**:
  - `aiohttp>=3.9.0`: 异步 HTTP 客户端
  - `loguru>=0.7.0`: 日志记录
  - `pycryptodome>=3.20.0`: 加密算法
  - `getuseragent>=0.1.0`: User-Agent 生成

- **配置路径**:
  - 主配置: `scripts/request/web/config.json`
  - 加密配置: `scripts/request/web/encrypt/web_encrypt_config.ini`
  - 总结提示词: `prompts/summary_prompt.md`

- **性能考虑**:
  - 默认请求间隔 1 秒，避免频率过高
  - 支持最大 5 次重试机制
  - 使用代理可绕过部分网络限制
  - 批量获取详情时自动添加延迟

- **加密签名**:
  - 实现了小红书 Web 端的所有加密签名机制
  - Cookie 自动生成（a1, webId, websectiga 等）
  - 请求头签名（X-S, X-S-Common, X-B3 等）

---
