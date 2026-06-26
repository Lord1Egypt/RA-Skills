---
name: auto-video-generator
version: "3.2.0"
description: "专业级真实演示视频生成器 - PM驱动场景分解 + 区域感知录制 + 强制用户交互。使用 Playwright 原生录制 + bmad-agent-pm 集成实现智能视频生产。"
author: "AVG Team"
tags:
  - video-generation
  - real-recording
  - playwright-native
  - pm-driven
  - prd-generation
  - region-aware
  - scenario-based
  - demo-automation
  - mandatory-interaction
  - tts
category: "development-tools"
license: MIT
homepage: "https://github.com/avg-team/auto-video-generator"
language: zh-CN
---

# Auto Video Generator V3.2 (自动视频生成器)

**PM驱动 & 区域感知 真实演示视频生成**

> 🆕 **V3.2 强制交互规范（必须执行）**：
> - **[强制 #1]** 录制区域选择 必须提示用户进行明确确认
> - **[强制 #2]** 场景预览与验证 必须等待用户批准后才能开始录制
> - **[强制 #3]** PRD驱动场景优先 - 如果存在 bmad-create-prd 生成的PRD，必须使用PRD中的场景

> 🆕 **V3.1 新功能**：
> 1. **录制区域选择** - 裁剪到指定 UI 区域（如仅录内容区，排除侧边栏/头部）
> 2. **PM驱动工作流集成** - 自动检测功能 → 生成 PRD → 分解场景 → 按场景录制
> 3. **基于场景的语音解说** - 根据场景生成 TTS 音频的专业演示

---

## ⚠️ 强制性用户交互（V3.2 执行标准）

### 🔴 关键：这些交互不是可选的 - 必须 实现

#### [强制 #1] 录制区域选择 - 强制 用户确认（禁止默认全屏！）

**规则**：您 **必须** 提示用户选择录制区域后才能开始。 **❌ 禁止**：默认使用全屏或静默使用自动检测的区域。

**原因**：
- 全屏录制包含浏览器地址栏、书签栏、系统任务栏（不专业）
- 不同功能需要不同录制区域（有些需要侧边栏，有些不需要）
- 用户必须明确确认，避免在错误区域上浪费时间

**区域类型说明**：
```
┌─────────────────────────────────────────────────────────────┐
│  浏览器边框（排除此部分）                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 顶部标签栏（可选）                                     │   │
│  │ ┌──────────┬────────────────────────────────────┐   │   │
│  │ │ 左侧菜单  │       主内容区                    │   │   │
│  │ │ (导航)    │       (查询表单+表格)             │   │   │
│  │ │          │                                   │   │   │
│  │ │          │                                   │   │   │
│  │ └──────────┴────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│  系统任务栏（排除此部分）                                    │
└─────────────────────────────────────────────────────────────┘

类型 A: 页面+侧边栏（推荐用于带菜单导航的演示）
        → 包含左侧导航菜单 + 主内容区
        → 排除浏览器边框和任务栏
        
类型 B: 仅内容区（适合聚焦功能本身）
        → 只录主内容区，不含左侧菜单
        → 更简洁的外观
        
类型 C: 全屏（不推荐）
        → 包含浏览器边框、任务栏等所有元素
        → 不适合产品演示视频
```

**实现要求**（通用 IDE 支持）：

```python
# ✅ 正确：始终通过 AskUserQuestion 让用户选择录制区域

async def select_recording_region(self, page) -> Dict:
    """
    [强制] 强制用户选择录制区域。
    
    关键规则：
    - ❌ 禁止默认全屏
    - ❌ 禁止跳过用户选择
    - ✅ 必须使用 AskUserQuestion 工具
    - ✅ 必须提供可视化区域选项
    """
    
    response = await AskUserQuestion({
        "questions": [{
            "header": "录制区域",
            "question": "请选择要录制的区域（当前为全屏模式）:",
            "multiSelect": False,
            "options": [
                {
                    "label": "📺 页面+侧边栏（推荐）",
                    "description": "包含左侧导航菜单+主内容区，不含浏览器边框。适合演示带菜单操作的功能"
                },
                {
                    "label": "📋 仅内容区",
                    "description": "只录制主内容区域，不含左侧菜单。适合聚焦功能本身"
                },
                {
                    "label": "🖥️ 全屏",
                    "description": "包含浏览器边框、任务栏等所有元素（不推荐）"
                }
            ]
        }]
    })
    
    choice = response['questions'][0]['answer']
    
    if choice == "📺 页面+侧边栏（推荐）":
        return {"x": 0, "y": 80, "width": 1920, "height": 1000}
    elif choice == "📋 仅内容区":
        return {"x": 250, "y": 80, "width": 1670, "height": 1000}
    else:
        return None  # 全屏（不裁剪）
```

**Playwright 实现方式**：

```python
# 使用 record_video_size 参数将视频裁剪到选定区域
ctx = await browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    record_video_dir=str(video_dir),
    record_video_size={
        'width': selected_region['width'],   # 如：1920 或 1670
        'height': selected_region['height']   # 如：1000
    },
    locale='zh-CN'
)
```

**❌ 禁止行为**：
- ❌ 不询问用户就默认使用全屏录制
- ❌ 静默使用自动检测区域而不经用户确认
- ❌ 在没有用户输入的情况下硬编码区域坐标
- ❌ 录制浏览器地址栏、书签栏或系统任务栏

**✅ 必须执行的工作流程**：
1. 启动浏览器（完整视口）
2. **[强制]** 调用 `AskUserQuestion` 提供区域选项
3. 等待用户选择
4. 应用 `record_video_size` 裁剪视频
5. 开始录制

---

#### [强制 #2] 场景预览与验证 - 等待 用户批准

**规则**：在从 PM 分析生成场景后，您 **必须** 向用户显示所有场景并等待其明确批准后才开始录制。

**原因**:
- 用户可能想要删除不相关的场景
- 用户可能想要重新排序场景
- 用户可能想要添加 PM 分析未检测到的自定义场景
- 防止浪费时间录制不需要的内容

**实现要求**（通用 IDE 支持）：

```python
# ✅ 正确：使用 AskUserQuestion 工具（适用于所有 IDE：TRAE、Cursor、WorkBuddy 等）

async def preview_and_validate_scenarios(self, scenarios: List[Scenario]) -> List[Scenario]:
    """
    [强制] 显示场景列表供用户审核和确认。
    
    关键：在用户明确确认之前 不得 开始录制。
    使用 AskUserQuestion 在所有 IDE 中弹出交互窗口。
    """
    
    # 构建场景摘要文本
    scenario_summary = "\n".join([
        f"  [{s.id}] {s.name} - {s.description} (~{s.duration_estimate}秒)"
        for s in scenarios
    ])
    
    # [强制] 使用 AskUserQuestion - 适用于所有 IDE！
    response = await AskUserQuestion({
        "questions": [{
            "header": "场景确认",
            "question": f"已生成 {len(scenarios)} 个录制场景，是否批准开始录制？\n{scenario_summary}",
            "multiSelect": False,
            "options": [
                {
                    "label": "✅ 批准并开始录制",
                    "description": "接受以上所有场景，立即开始视频录制"
                },
                {
                    "label": "✏️ 修改场景",
                    "description": "删除/重排/编辑特定场景"
                },
                {
                    "label": "❌ 取消",
                    "description": "中止录制流程"
                }
            ]
        }]
    })
    
    choice = response['questions'][0]['answer']
    
    if "批准" in choice:
        return scenarios
    elif choice == "2":
        return await self._modify_scenarios(scenarios)  # 编辑模式
    elif choice == "3":
        return await self._add_custom_scenario(scenarios)  # 添加自定义
    else:
        raise KeyboardInterrupt("用户取消")
```

**可用的用户操作**:

| 操作 | 命令 | 描述 |
|------|------|------|
| **批准** | 选择 `1` | 接受所有场景并开始录制 |
| **删除场景** | `REMOVE S5` | 从列表中删除场景 S5 |
| **交换顺序** | `SWAP S2 S6` | 交换 S2 和 S6 的位置 |
| **编辑解说词** | `EDIT S3` | 修改 S3 的解说词文本 |
| **添加自定义** | 选择 `3` | 手动创建新场景 |
| **取消** | 选择 `4` | 中止整个流程 |

**❌ 禁止行为**：在不显示此预览屏幕的情况下开始录制。

---

#### [强制 #3] PRD驱动场景优先 - 存在 bmad-create-prd PRD 时必须使用PRD场景

**规则**：当用户已通过 `bmad-create-prd` skill 生成了PRD时，您 **必须** 从PRD中提取场景，而不是自动生成场景。仅在没有PRD时才自动生成场景。

**原因**：
- PRD场景由PM分析精心设计，包含完整的业务上下文
- PRD场景包含用户故事、验收标准和解说词文本
- 自动生成的场景缺乏领域特定的业务逻辑
- 使用PRD确保视频演示与产品规格一致

**实现要求**（通用 IDE 支持）：

```python
# ✅ 正确：在生成场景前先检查是否存在PRD

async def resolve_scenarios(self, target_feature: str) -> List[Scenario]:
    """
    [强制] 以PRD优先的方式解析录制场景。
    
    优先级：
    1. 如果存在 bmad-create-prd 生成的PRD → 从PRD提取场景（强制）
    2. 如果没有PRD → 从页面分析自动生成场景
    """
    
    # 步骤1：检查是否存在 bmad-create-prd 生成的PRD
    prd_file = await self._find_prd_file(target_feature)
    
    if prd_file:
        # [强制] 使用PRD场景 - 不得自动生成
        scenarios = await self._extract_scenarios_from_prd(prd_file)
        return scenarios
    else:
        # 降级：从页面分析自动生成场景
        scenarios = await self._auto_generate_scenarios()
        return scenarios

async def _find_prd_file(self, feature_name: str) -> Optional[Path]:
    """搜索 bmad-create-prd skill 生成的PRD文件"""
    search_paths = [
        Path("./_bmad-output/prd"),
        Path("./docs/prd"),
        Path("./prd"),
    ]
    
    for search_dir in search_paths:
        if not search_dir.exists():
            continue
        for prd_file in search_dir.rglob("*.md"):
            content = prd_file.read_text(encoding='utf-8')
            if feature_name in content or '场景' in content:
                return prd_file
    
    return None

async def _extract_scenarios_from_prd(self, prd_file: Path) -> List[Scenario]:
    """从 bmad-create-prd PRD 中提取录制场景"""
    content = prd_file.read_text(encoding='utf-8')
    
    scenarios = []
    
    # 从PRD结构中提取：
    # - ## 场景 / ## Scenario 章节
    # - ### 用户故事 / ### User Story 章节
    # - 功能描述中的步骤流程
    
    # ... 解析逻辑 ...
    
    return scenarios
```

**决策流程**：

```
用户请求录制视频
        ↓
检查：是否存在 bmad-create-prd 生成的PRD？
        ↓
   是 → [强制] 从PRD中提取场景
   │         ↓
   │     通过 AskUserQuestion 向用户展示PRD场景
   │         ↓
   │     用户批准 → 使用PRD场景开始录制
   │
   否 → 从页面分析自动生成场景
        ↓
    通过 AskUserQuestion 向用户展示自动场景
        ↓
    用户批准 → 使用自动场景开始录制
```

**❌ 禁止行为**：忽略已存在的 bmad-create-prd PRD，转而自动生成场景。

---

## 📋 V3.2 完整工作流（含强制交互）

```
完整 V3.2 工作流：
===================

[步骤 1] 启用录制功能启动浏览器
    ↓
[步骤 2] 导航到目标 URL（如需登录则登录）
    ↓
[步骤 3] ⚠️ [强制 #1] 检测区域 + 提示用户
    ↓ 自动检测内容区域
    ↓ 显示交互式菜单（始终！）
    ↓ 等待用户选择：全屏 / 内容区 / 自定义
    ↓ 用户 明确 选择区域
    ↓
[步骤 4] PM 分析（自动检测组件 + 生成 PRD）
    ↓ 检测：树形结构、表单、按钮、表格等
    ↓ 生成场景：S1, S2, S3, ...
    ↓ 保存 PRD 到 JSON 文件
    ↓
[步骤 4.5] ⚠️ [强制 #2] 预览场景 + 等待批准
    ↓ 以详细表格形式显示 所有场景
    ↓ 显示解说词预览
    ↓ 等待用户操作：
       选项 1: ✅ 批准 → 继续执行步骤 5
       选项 2: ✏️ 修改 → 删除/重排/编辑场景
       选项 3: ➕ 添加自定义 → 创建新场景
       选项 4: ❌ 取消 → 中止
    ↓ 用户 明确 批准场景
    ↓
[步骤 5] 执行录制（终于可以开始了！）
    ↓ 对每个已批准的场景：
       执行真实交互（鼠标、键盘、滚动）
       所有操作录制为 .webm 文件
    ↓
[步骤 6] 完成视频（关闭浏览器上下文）
    ↓ 保存原始视频
    ↓
[步骤 7] 生成音频 + 合并
    ↓ 为每个场景生成 TTS 解说
    ↓ FFmpeg 合并视频 + 音频
    ↓ 最终 MP4 输出

总计：7 个步骤 + 2 个强制性用户交互
```

---

## 🎯 V3.1 新功能

### 1️⃣ 录制区域选择（裁剪区域）

**问题**：全页录制会包含不必要的元素（侧边栏、头部、导航栏）。

**解决方案**：让用户指定要录制的区域。

```python
# 定义录制区域（仅内容区域）
region = RecordingRegion(
    x=250,      # 起始 X（侧边栏之后）
    y=80,       # 起始 Y（头部之下）
    width=1670, # 内容宽度
    height=1000 # 内容高度
)

# 在录制时使用该区域
await recorder.record_with_region_and_scenarios(
    url="https://example.com/dashboard",
    output_file="./demo.mp4",
    options={'region': region}
)
```

**自动检测策略**:
- ✅ 检测 `.ant-layout-content` 或 `[role="main"]`
- ✅ 提示用户选择：全屏 / 仅内容区 / 自定义
- ✅ 支持手动坐标输入

### 2️⃣ PM驱动场景分解

**与 bmad-agent-pm Skill 的集成**：

```
用户请求："录制综合查询功能"
                    ↓
[步骤 1] 页面分析（自动检测组件）
         ↓ 检测到：树形结构、表单、按钮、表格、日期选择器
[步骤 2] PRD 生成（模拟 bmad-create-prd）
         ↓ 输出：功能名称、组件列表、用户故事
[步骤 3] 场景分解
         ↓ 创建：S1-S7 场景（概览 → 选择 → 查询 → 结果）
[步骤 4] 按场景录制
         ↓ 执行：每个场景的真实交互
[步骤 5] 音频生成
         ↓ 生成：基于每个场景的 TTS 解说
[步骤 6] 合并与输出
         ↓ 产出：带专业解说的最终 MP4
```

**PRD 输出示例**:
```json
{
  "feature_name": "综合查询 · 单车成本核算系统",
  "components_detected": {
    "trees": ["查询项目选择树"],
    "forms": ["请输入关键字进行过滤"],
    "buttons": ["查询", "重置", "导出", "打印"],
    "tables": ["表格 1"],
    "date_pickers": ["日期选择器 1"]
  },
  "scenarios": [
    {
      "id": "S1",
      "name": "界面概览",
      "description": "展示整体布局和主要功能区",
      "narration": "欢迎观看综合查询功能演示..."
    },
    {
      "id": "S2", 
      "name": "查询项目选择",
      "description": "在树形结构中选择要查询的项目类型",
      "narration": "在查询项目选择区域..."
    },
    // ... 更多场景
  ]
}
```

### 3️⃣ 使用示例（V3.1+）

```bash
# 基础用法（自动检测区域 + PM 分析）
python record_v3_smart.py --target "http://localhost:8090/#/dashboardIndex/UnityQuery"

# 自定义输出
python record_v3_smart.py -t "URL" -o "./my-demo.mp4"

# 禁用区域选择（全屏录制）
python record_v3_smart.py --no-region
```

**Python API**:
```python
from record_v3_smart import SmartVideoRecorderV31

recorder = SmartVideoRecorderV31(verbose=True)

result = await recorder.record_with_region_and_scenarios(
    url="https://example.com/feature-page",
    output_file="./feature-demo.mp4",
    options={
        'auto_select_region': True,
        'generate_prd': True,
        'voice': 'zh-CN-YunxiNeural'
    }
)

print(f"✅ 视频已生成: {result['output_path']}")
print(f"   场景数: {result['scenarios_count']}")
print(f"   录制区域: {result['region']}")
print(f"   PRD 文件: {result['prd_file']}")
```

---

## 🎯 核心原则（继承自 V3.0）

### 🚫 严格禁止的行为

**以下方法在任何情况下都 不允许 使用**：

1. ❌ **截图捕获 + FFmpeg 拼接**
   - 定时截取屏幕截图
   - 使用 ffmpeg 将它们合并成视频
   - 这会产生 不显示真实交互 的假视频

2. ❌ **静态帧生成**
   - 将 HTML 帧生成为图像
   - 创建幻灯片风格的演示
   - 没有可见的真实用户交互

3. ❌ **模拟动画**
   - 基于 CSS/JavaScript 的虚假动画
   - 预渲染的 GIF 风格内容
   - 任何不捕获真实浏览器行为的内容

### ✅ 必须采用的方式（唯一可接受的方案）

**所有视频生成 都必须 使用以下确切方式**：

```python
# ✅ 正确：Playwright 原生录制
from playwright.async_api import async_playwright

pw = await async_playwright().start()

# 关键行：在浏览器上下文中启用视频录制
context = await pw.chromium.launch_persistent_context(
    "",
    headless=False,
    viewport={'width': 1920, 'height': 1080},
    record_video_dir="./videos",  # ← 这是强制的
    record_video_size={'width': 1920, 'height': 1080}
)

page = context.pages[0]

# 导航到目标页面
await page.goto("https://example.com")

# 执行真实交互（这些会被 自动 录制）
await page.mouse.move(500, 300, steps=20)  # 真实鼠标移动
await page.mouse.click(500, 300)           # 真实点击
await page.keyboard.type("Hello")          # 真实打字
await page.mouse.wheel(0, 500)             # 真实滚动

# 关闭上下文以完成录制
await context.close()
await pw.stop()

# 结果：一个包含真实交互的 .webm 文件！
```

---

## 🔬 技术规范（必须遵循）

### 1. 浏览器上下文配置

**每次实现都必须包含以下参数**：

```python
context = await browser.new_context(
    # ... 其他参数 ...
    
    # 强制：视频录制目录
    record_video_dir=str(video_output_path),
    
    # 强制：视频分辨率（必须匹配视口）
    record_video_size={
        'width': viewport_width,
        'height': viewport_height
    },
    
    # 推荐：默认使用全高清
    viewport={
        'width': 1920,   # ← 全高清宽度
        'height': 1080   # ← 全高清高度
    }
)
```

### 2. 真实交互方法（必须使用这些）

**鼠标交互**:
```python
# 平滑鼠标移动（为了专业外观是必需的）
await page.mouse.move(x, y, steps=20)  # steps=20 使其平滑

# 带视觉反馈的点击
await page.mouse.click(x, y)

# 带动画的滚动
await page.mouse.wheel(delta_x, delta_y)
```

**键盘交互**:
```python
# 逐字符输入文本（逼真）
await page.keyboard.type("search query", delay=100)  # delay=100ms/字符

# 按特殊键
await page.keyboard.press("Enter")
await page.keyboard.press("Tab")
```

**元素高亮（可选但推荐）**:
```python
# 点击前 - 高亮元素
await element.evaluate("""
    el => {
        el.style.transition = 'outline 0.2s';
        el.style.outline = '3px solid #1890ff';
        el.style.outlineOffset = '2px';
    }
""")
await asyncio.sleep(0.3)

# 执行点击
await page.mouse.click(x, y)

# 点击后移除高亮
await element.evaluate("""
    el => {
        el.style.outline = '';
        el.style.outlineOffset = '';
    }
""")
```

### 3. 视频输出格式

**录制过程**:
1. Playwright 自动录制 `.webm` 格式
2. 关闭上下文时文件保存到 `record_video_dir`
3. 使用 FFmpeg 合并 TTS 音频：
   ```bash
   ffmpeg -i input.webm -i audio.mp3 -c:v libx264 -c:a aac output.mp4
   ```

---

## 📋 实现检查清单（每次生成都必须通过）

在认为视频生成完成之前，请验证：

- [ ] 浏览器是否使用 `record_video_dir` 参数启动？
- [ ] 视口是否设置为至少 1440×900（推荐 1920×1080）？
- [ ] 是否执行了真实的 `page.mouse.move/click/wheel` 调用？
- [ ] 是否使用了真实的 `page.keyboard.type/press` 调用（如需要）？
- [ ] 交互是否平滑（鼠标移动的 steps > 10）？
- [ ] 视频时长 > 5 秒（简单页面）（复杂页面 > 15秒）？
- [ ] 文件大小 > 1 MB（表示真实内容，而非空白屏幕）？
- [ ] 音频解说是否成功合并？
- [ ] 输出是否为 H.264 编码的 MP4 格式？

如果任何一项失败，则实现 **无效** 且必须修复。

---

## 🎨 本 Skill 的作用（V3.0+）

此 Skill 提供 **真实** 的自动化视频生成能力：

- **✅ 真实 HTML 转视频**: 使用实际浏览器录制将任意网页转换为专业演示视频
- **✅ AI 语音解说**: 自动文本转语音，自然声音（Edge TTS）
- **✅ 真实 UI 交互录制**: 实际的鼠标移动、点击、滚动和键盘输入 - 全部真实捕获
- **✅ 多框架支持**: 支持 Vue、React、Angular + UI 库（Ant Design、Element UI 等）
- **✅ 智能页面分析**: 自动检测交互元素（表单、表格、按钮、菜单）
- **✅ 生产就绪**: 错误处理、重试逻辑、结构化日志

---

## 🚀 何时使用此 Skill

当用户想要以下功能时使用此 Skill：

1. **生成真实演示视频**
   - "从我的落地页创建产品演示" → 录制真实交互
   - "为我的仪表板制作教程视频" → 显示真实导航
   - "将我的 Web 应用录制为带解说的视频" → 使用真实用户流程

2. **自动化测试视频**
   - "为 CI 流水线创建回归测试视频" → 真实测试执行录制
   - "生成可视化测试文档" → 真实测试运行，非模拟
   - "录制用户旅程视频" → 通过应用的实际用户路径

3. **创建演示文稿**
   - "将此 HTML 原型转为演示视频" → 真实原型交互
   - "从我们的 SaaS 页面制作营销视频" → 显示真实功能工作
   - "生成入职培训视频" → 引导用户通过真实界面

---

## 💻 使用示例（正确的 V3.0 方法）

### Python API（推荐）

```python
import asyncio
from auto_video_generator import VideoGenerator

async def main():
    gen = VideoGenerator(verbose=True)
    
    result = await gen.generate(
        source="https://example.com/dashboard",
        output="./demo.mp4",
        options={
            "viewport_width": 1920,      # 全高清
            "viewport_height": 1080,
            "voice": "zh-CN-YunxiNeural", # 中文语音
            "headless": False,            # 显示浏览器窗口
            "show_cursor": True,          # 显示鼠标光标
            "highlight_clicks": True,     # 高亮被点击的元素，
        }
    )
    
    print(f"✅ 真实视频已生成！")
    print(f"   时长: {result.duration_seconds:.1f}s")
    print(f"   大小: {result.file_size_mb:.2f} MB")
    print(f"   分辨率: {result.resolution}")

asyncio.run(main())
```

### 内部发生什么（V3.0）

```
1. 启动 Chrome 并启用录制（record_video_dir）
2. 导航到目标 URL
3. 分析页面结构（检测表单、按钮、表格）
4. 执行真实交互：
   - 鼠标平滑移动到元素
   - 带高亮效果点击按钮
   - 在输入框中打字
   - 滚动显示内容
5. 所有操作自动录制为 .webm
6. 生成 TTS 音频解说
7. 合并视频 + 音频 → 最终 MP4
8. 返回包含元数据的结果
```

---

## ⚙️ 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|---------|------|
| `viewport_width` | int | 1920 | 视频宽度（最小值: 1440） |
| `viewport_height` | int | 1080 | 视频高度（最小值: 900） |
| `voice` | string | zh-CN-YunxiNeural | Edge TTS 语音名称 |
| `rate` | string | "-5%" | 语速调整 |
| `headless` | bool | False | 隐藏浏览器窗口 |
| `show_cursor` | bool | True | 在视频中显示鼠标光标 |
| `highlight_clicks` | bool | True | 点击前高亮元素 |
| `fps` | int | 4 | 目标每秒帧数 |
| `quality` | string | "high" | 视频质量（low/medium/high） |

---

## 🛡️ 质量标准（必须满足）

### 最低要求

每个生成的视频都必须满足以下标准：

1. **时长**
   - 简单页面（落地页）：≥ 10 秒
   - 中等复杂度（仪表板）：≥ 20 秒
   - 复杂应用（完整工作流）：≥ 30 秒

2. **分辨率**
   - 最小值：1440×900
   - 推荐：1920×1080（全高清）
   - 最大值：2560×1440（2K）

3. **文件大小**
   - 最小值：2 MB（表示真实内容）
   - 典型值：5-50 MB（取决于时长）
   - 如果 < 1 MB：可能出了问题（空白屏幕？）

4. **内容质量**
   - ✅ 显示真实页面内容（非空白/白色）
   - ✅ 包含真实鼠标移动（可见光标）
   - ✅ 有对 UI 元素的真实点击
   - ✅ 包含滚动行为
   - ✅ 音频解说与视觉同步

---

## 🔧 常见错误要避免

### ❌ 错误：基于截图的方法

```python
# 不要这样做！
for i in range(100):
    await page.screenshot(path=f"frame_{i}.png")  # ❌ 截图！
    await asyncio.sleep(0.1)

# 然后使用 ffmpeg 组合图片...  # ❌ 假视频！
```

### ✅ 正确：真实录制方法

```python
# 应该这样做！
context = await browser.new_context(
    record_video_dir="./videos"  # ✅ 启用录制！
)

page = await context.new_page()
await page.goto("https://example.com")

# 会被自动录制的真实交互
await page.mouse.move(500, 300, steps=20)
await page.mouse.click(500, 300)

await context.close()  # ✅ 完成录制
```

---

## 📊 版本历史

### V3.2.0 (当前版本) - 强制性用户交互
- **重大变更**: 录制区域选择现在 要求 明确的用户确认（即使有自动检测）
- **重大变更**: 场景预览在录制前是 强制性的（用户必须批准）
- **新增**: 带视觉布局图的交互式区域选择菜单
- **新增**: 场景预览与验证系统，支持编辑/删除/添加功能
- **增强**: 用户可以修改场景（删除、重新排序、编辑解说词、添加自定义）
- **增强**: 清晰的视觉反馈，显示页面布局和检测到的区域
- **安全性**: 防止意外录制错误区域和浪费时间

### V3.1.0 - PM驱动与区域感知
- **新增**: 录制区域选择（裁剪到内容区域，排除侧边栏/头部）
- **新增**: 与 bmad-agent-pm 工作流集成（PRD 生成 → 场景分解）
- **新增**: 基于 TTS 解说词的场景生成
- **新增**: 页面组件自动检测用于智能场景创建
- **改进**: 区域选择的用户提示（全屏 / 仅内容区 / 自定义）
- **增强**: PRD 作为 JSON 文件与视频一起输出

### V3.0.0 - 真实录制要求
- **重大变更**: 完全移除基于截图的生成
- 添加了强制 `record_video_dir` 要求
- 实现了真实的鼠标/键盘交互录制
- 默认全高清分辨率（1920×1080）
- 增强的质量标准和验证

### V2.0.0 - 旧版本（已弃用）
- 使用截图捕获方法
- 产生低质量的短视频
- **不再支持 - 升级到 V3.2**

---

## 🤝 贡献代码

所有贡献都 必须遵循 V3.2 标准：
- ✅ 使用 Playwright 原生录制（`record_video_dir`）
- ✅ 支持区域感知录制（裁剪区域）
- ✅ [强制] 在开始前强制用户确认录制区域
- ✅ [强制] 显示场景预览并在录制前等待用户批准
- ✅ 与 bmad-agent-pm 集成以实现 PRD 驱动的场景
- ❌ 不允许在没有用户确认的情况下静默自动检测

---

## 📄 许可证

MIT License

---

**版本**: 3.2.0 (强制性用户交互)
**最后更新**: 2026-05-30
**状态**: 生产就绪 ✅
**维护团队**: AVG Team
**集成**: bmad-agent-pm (PM 工作流)
