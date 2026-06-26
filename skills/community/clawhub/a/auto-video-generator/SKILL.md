---
name: auto-video-generator
version: "3.2.0"
description: "Professional REAL demo video generation with PM-driven scenario decomposition and region-aware recording. Uses Playwright native recording + bmad-agent-pm integration for intelligent video production."
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
  - testing
  - tts
category: "development-tools"
license: MIT
homepage: "https://github.com/avg-team/auto-video-generator"
---

# Auto Video Generator V3.2

**PM-Driven & Region-Aware REAL Demo Video Generation**

> 🆕 **V3.2 MANDATORY INTERACTIONS (ENFORCED)**:
> - **[MANDATORY #1]** Recording Region Selection MUST prompt user for explicit confirmation
> - **[MANDATORY #2]** Scenario Preview & Validation MUST wait for user approval before recording
> - **[MANDATORY #3]** PRD-Driven Scenario Priority - If bmad-create-prd PRD exists, MUST use PRD scenarios

> 🆕 **V3.1 NEW FEATURES**:
> 1. **Recording Region Selection** - Clip to specific UI area (e.g., content area only, exclude sidebar/header)
> 2. **PM-Driven Workflow Integration** - Auto-detect features → Generate PRD → Decompose scenarios → Record per-scenario
> 3. **Scenario-Based Narration** - TTS audio generated from PRD scenarios for professional demos

---

## ⚠️ MANDATORY USER INTERACTIONS (V3.2 ENFORCEMENT)

### 🔴 CRITICAL: These interactions are NOT optional - they MUST be implemented

#### [MANDATORY #1] Recording Region Selection - FORCE User Confirmation (NO DEFAULT!)

**Rule**: You **MUST** prompt user to select recording region before starting. **❌ FORBIDDEN**: Using full-screen as default or silently using auto-detected region.

**Why**:
- Full-screen recording includes browser address bar, bookmarks, system taskbar (unprofessional)
- Different features need different regions (some need sidebar, some don't)
- User must explicitly confirm to avoid wasting time on incorrect recordings

**Region Types**:
```
┌─────────────────────────────────────────────────────────────┐
│  BROWSER CHROME (exclude this)                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ HEADER/TABS (optional)                               │   │
│  │ ┌──────────┬────────────────────────────────────┐   │   │
│  │ │ SIDEBAR  │     CONTENT AREA                   │   │   │
│  │ │ (menu)   │     (query form + table)           │   │   │
│  │ │          │                                    │   │   │
│  │ │          │                                    │   │   │
│  │ └──────────┴────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│  SYSTEM TASKBAR (exclude this)                             │
└─────────────────────────────────────────────────────────────┘

Type A: FULL PAGE WITH SIDEBAR (recommended for navigation demos)
        → Includes sidebar menu + content area
        → Excludes browser chrome & taskbar
        
Type B: CONTENT ONLY (for feature-focused demos)
        → Content area only, no sidebar
        → Cleaner look for specific functionality
        
Type C: FULL SCREEN (NOT recommended)
        → Everything including browser chrome
        → Unprofessional for product demos
```

**Implementation Requirements** (Universal IDE Support):

```python
# ✅ CORRECT: ALWAYS ask user to select region via AskUserQuestion

async def select_recording_region(self, page) -> Dict:
    """
    [MANDATORY] Force user to select recording region.
    
    CRITICAL RULES:
    - ❌ NEVER default to full-screen
    - ❌ NEVER skip user selection
    - ✅ MUST use AskUserQuestion tool
    - ✅ MUST provide visual region options
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
        return None  # Full screen (no cropping)
```

**Playwright Implementation**:

```python
# Use record_video_size parameter to crop video to selected region
ctx = await browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    record_video_dir=str(video_dir),
    record_video_size={
        'width': selected_region['width'],   # e.g., 1920 or 1670
        'height': selected_region['height']   # e.g., 1000
    },
    locale='zh-CN'
)
```

**❌ FORBIDDEN BEHAVIORS**:
- ❌ Defaulting to full-screen recording without asking
- ❌ Silently using auto-detected region without confirmation
- ❌ Hardcoding region coordinates without user input
- ❌ Recording browser address bar, bookmarks, or system taskbar

**✅ REQUIRED WORKFLOW**:
1. Launch browser (full viewport)
2. **[MANDATORY]** Call `AskUserQuestion` with region options
3. Wait for user selection
4. Apply `record_video_size` to crop video
5. Start recording

---

#### [MANDATORY #2] Scenario Preview & Validation - WAIT for User Approval

**Rule**: After generating scenarios from PM analysis, you **MUST** display all scenarios to the user and wait for their explicit approval before starting recording.

**Why**: 
- Users may want to remove irrelevant scenarios
- Users may want to reorder scenarios
- Users may want to add custom scenarios not detected by PM analysis
- Prevents wasted time recording unwanted content

**Implementation Requirements** (Universal IDE Support):

```python
# ✅ CORRECT: Use AskUserQuestion tool (works in ALL IDEs: TRAE, Cursor, WorkBuddy, etc.)

async def preview_and_validate_scenarios(self, scenarios: List[Scenario]) -> List[Scenario]:
    """
    [MANDATORY] Show scenario list to user for review and confirmation.
    
    CRITICAL: Must NOT start recording until user explicitly confirms.
    Use AskUserQuestion tool for universal IDE compatibility.
    """
    
    # Build scenario summary text
    scenario_summary = "\n".join([
        f"  [{s.id}] {s.name} - {s.description} (~{s.duration_estimate}s)"
        for s in scenarios
    ])
    
    # [MANDATORY] Use AskUserQuestion - works in ALL IDEs!
    response = await AskUserQuestion({
        "questions": [{
            "header": "Scenarios",
            "question": f"Generated {len(scenarios)} recording scenarios. Approve to start recording?\n{scenario_summary}",
            "multiSelect": False,
            "options": [
                {
                    "label": "✅ Approve & Start Recording",
                    "description": "Accept all scenarios and start video recording immediately"
                },
                {
                    "label": "✏️ Modify Scenarios",
                    "description": "Remove/reorder/edit specific scenarios"
                },
                {
                    "label": "❌ Cancel",
                    "description": "Abort recording process"
                }
            ]
        }]
    })
    
    choice = response['questions'][0]['answer']
    
    if "Approve" in choice:
        return scenarios
    elif choice == "2":
        return await self._modify_scenarios(scenarios)  # Edit mode
    elif choice == "3":
        return await self._add_custom_scenario(scenarios)  # Add custom
    else:
        raise KeyboardInterrupt("User cancelled")
```

**User Actions Available**:

| Action | Command | Description |
|--------|---------|-------------|
| **Approve** | Choice `1` | Accept all scenarios and start recording |
| **Remove Scenario** | `REMOVE S5` | Delete scenario S5 from list |
| **Swap Order** | `SWAP S2 S6` | Exchange positions of S2 and S6 |
| **Edit Narration** | `EDIT S3` | Change narration text for S3 |
| **Add Custom** | Choice `3` | Create new scenario manually |
| **Cancel** | Choice `4` | Abort entire process |

**❌ FORBIDDEN**: Starting recording without showing this preview screen.

---

#### [MANDATORY #3] PRD-Driven Scenario Priority - USE bmad-create-prd Scenarios When Available

**Rule**: When a PRD has been generated by the `bmad-create-prd` skill, you **MUST** extract scenarios from that PRD instead of auto-generating them. Only auto-generate scenarios when no PRD exists.

**Why**:
- PRD scenarios are carefully designed by PM analysis with proper business context
- PRD scenarios include user stories, acceptance criteria, and narration text
- Auto-generated scenarios lack domain-specific business logic
- Using PRD ensures video demos match the product specification

**Implementation Requirements** (Universal IDE Support):

```python
# ✅ CORRECT: Check for existing PRD before generating scenarios

async def resolve_scenarios(self, target_feature: str) -> List[Scenario]:
    """
    [MANDATORY] Resolve recording scenarios with PRD priority.
    
    Priority:
    1. If bmad-create-prd PRD exists → Extract scenarios from PRD (MANDATORY)
    2. If no PRD exists → Auto-generate scenarios from page analysis
    """
    
    # Step 1: Check if bmad-create-prd PRD exists
    prd_file = await self._find_prd_file(target_feature)
    
    if prd_file:
        # [MANDATORY] Use PRD scenarios - DO NOT auto-generate
        scenarios = await self._extract_scenarios_from_prd(prd_file)
        return scenarios
    else:
        # Fallback: Auto-generate scenarios from page analysis
        scenarios = await self._auto_generate_scenarios()
        return scenarios

async def _find_prd_file(self, feature_name: str) -> Optional[Path]:
    """Search for PRD files generated by bmad-create-prd skill."""
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
    """Extract recording scenarios from bmad-create-prd PRD."""
    content = prd_file.read_text(encoding='utf-8')
    
    # Parse PRD sections: user stories, scenarios, feature descriptions
    scenarios = []
    
    # Extract from PRD structure:
    # - ## 场景 / ## Scenario sections
    # - ### 用户故事 / ### User Story sections  
    # - Feature descriptions with step-by-step flows
    
    # ... parsing logic ...
    
    return scenarios
```

**Decision Flow**:

```
User requests video recording
        ↓
Check: Does bmad-create-prd PRD exist?
        ↓
   YES → [MANDATORY] Extract scenarios from PRD
   │         ↓
   │     Show PRD scenarios to user via AskUserQuestion
   │         ↓
   │     User approves → Start recording with PRD scenarios
   │
   NO → Auto-generate scenarios from page analysis
        ↓
    Show auto scenarios to user via AskUserQuestion
        ↓
    User approves → Start recording with auto scenarios
```

**❌ FORBIDDEN**: Ignoring an existing bmad-create-prd PRD and auto-generating scenarios instead.

---

## 📋 V3.2 Workflow (WITH MANDATORY INTERACTIONS)

```
COMPLETE V3.2 WORKFLOW:
=======================

[Step 1] Launch Browser + Enable Recording
    ↓
[Step 2] Navigate to Target URL (+ Login if needed)
    ↓
[Step 3] ⚠️ [MANDATORY #1] DETECT REGION + PROMPT USER
    ↓ Auto-detect content area
    ↓ SHOW interactive menu (ALWAYS!)
    ↓ Wait for user choice: FULL / CONTENT / CUSTOM
    ↓ User EXPLICITLY selects region
    ↓
[Step 4] PM Analysis (Auto-detect components + Generate PRD)
    ↓ Detect: trees, forms, buttons, tables, etc.
    ↓ Generate scenarios: S1, S2, S3, ...
    ↓ Save PRD to JSON file
    ↓
[Step 4.5] ⚠️ [MANDATORY #2] PREVIEW SCENARIOS + WAIT FOR APPROVAL
    ↓ Display ALL scenarios in detail table
    ↓ Show narration previews
    ↓ Wait for user action:
       Option 1: ✅ Approve → Continue to Step 5
       Option 2: ✏️ Modify → Remove/Swap/Edit scenarios
       Option 3: ➕ Add Custom → Create new scenario
       Option 4: ❌ Cancel → Abort
    ↓ User EXPLICITLY approves scenarios
    ↓
[Step 5] EXECUTE RECORDING (Finally!)
    ↓ For each approved scenario:
       Execute real interactions (mouse, keyboard, scroll)
       All actions recorded to .webm file
    ↓
[Step 6] Finalize Video (Close browser context)
    ↓ Raw video saved
    ↓
[Step 7] Generate Audio + Merge
    ↓ TTS narration for each scenario
    ↓ FFmpeg merge video + audio
    ↓ Final MP4 output

TOTAL: 7 Steps + 2 MANDATORY User Interactions
```

---

## 🎯 V3.1 NEW CAPABILITIES

### 1️⃣ Recording Region Selection (Clip Region)

**Problem**: Full-page recording includes unnecessary elements (sidebar, header, navigation).

**Solution**: Let users specify which area to record.

```python
# Define recording region (content area only)
region = RecordingRegion(
    x=250,      # Start X (after sidebar)
    y=80,       # Start Y (below header)
    width=1670, # Content width
    height=1000 # Content height
)

# Use region during recording
await recorder.record_with_region_and_scenarios(
    url="https://example.com/dashboard",
    output_file="./demo.mp4",
    options={'region': region}
)
```

**Auto-Detection Strategies**:
- ✅ Detect `.ant-layout-content` or `[role="main"]`
- ✅ Prompt user to choose: FULL / CONTENT ONLY / CUSTOM
- ✅ Support manual coordinate input

### 2️⃣ PM-Driven Scenario Decomposition

**Integration with bmad-agent-pm Skill**:

```
User Request: "Record the comprehensive query feature"
                    ↓
[Step 1] Page Analysis (Auto-detect components)
         ↓ Detects: trees, forms, buttons, tables, date pickers
[Step 2] PRD Generation (Simulated bmad-create-prd)
         ↓ Outputs: Feature name, component list, user stories
[Step 3] Scenario Decomposition
         ↓ Creates: S1-S7 scenarios (Overview → Selection → Query → Results)
[Step 4] Per-Scenario Recording
         ↓ Executes: Real interactions per scenario
[Step 5] Audio Generation
         ↓ Generates: TTS narration based on each scenario
[Step 6] Merge & Output
         ↓ Produces: Final MP4 with professional narration
```

**Example PRD Output**:
```json
{
  "feature_name": "综合查询 · 单车成本核算系统",
  "components_detected": {
    "trees": ["查询项目选择树"],
    "forms": ["请输入关键字进行过滤"],
    "buttons": ["查询", "重置", "导出", "打印"],
    "tables": ["Table 1"],
    "date_pickers": ["DatePicker 1"]
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
    // ... more scenarios
  ]
}
```

### 3️⃣ Usage Example (V3.1)

```bash
# Basic usage (auto-detect region + PM analysis)
python record_v3_smart.py --target "http://localhost:8090/#/dashboardIndex/UnityQuery"

# With custom output
python record_v3_smart.py -t "URL" -o "./my-demo.mp4"

# Disable region selection (full page)
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

print(f"✅ Video generated: {result['output_path']}")
print(f"   Scenarios: {result['scenarios_count']}")
print(f"   Region: {result['region']}")
print(f"   PRD saved to: {result['prd_file']}")
```

---

## 🎯 CORE PRINCIPLES (INHERITED FROM V3.0)

### 🚫 WHAT IS STRICTLY FORBIDDEN

**The following approaches are NOT ALLOWED under any circumstances:**

1. ❌ **Screenshot Capture + FFmpeg Concatenation**
   - Taking screenshots at intervals
   - Combining them into a video using ffmpeg
   - This produces FAKE videos that don't show real interactions

2. ❌ **Static Frame Generation**
   - Generating HTML frames as images
   - Creating slideshow-style presentations
   - No real user interactions visible

3. ❌ **Simulated Animations**
   - CSS/JavaScript-based fake animations
   - Pre-rendered GIF-style content
   - Anything that doesn't capture actual browser behavior

### ✅ WHAT IS MANDATORY (THE ONLY ACCEPTABLE APPROACH)

**ALL video generation MUST use this exact approach:**

```python
# ✅ CORRECT: Playwright Native Recording
from playwright.async_api import async_playwright

pw = await async_playwright().start()

# CRITICAL LINE: Enable video recording in browser context
context = await pw.chromium.launch_persistent_context(
    "",
    headless=False,
    viewport={'width': 1920, 'height': 1080},
    record_video_dir="./videos",  # ← THIS IS MANDATORY
    record_video_size={'width': 1920, 'height': 1080}
)

page = context.pages[0]

# Navigate to target page
await page.goto("https://example.com")

# Execute REAL interactions (these get RECORDED automatically)
await page.mouse.move(500, 300, steps=20)  # Real mouse movement
await page.mouse.click(500, 300)           # Real click
await page.keyboard.type("Hello")          # Real typing
await page.mouse.wheel(0, 500)             # Real scroll

# Close context to finalize recording
await context.close()
await pw.stop()

# Result: A .webm file with REAL interactions recorded!
```

---

## 🔬 TECHNICAL SPECIFICATION (MUST FOLLOW)

### 1. Browser Context Configuration

**Every implementation MUST include these parameters:**

```python
context = await browser.new_context(
    # ... other params ...
    
    # MANDATORY: Video recording directory
    record_video_dir=str(video_output_path),
    
    # MANDATORY: Video resolution (must match viewport)
    record_video_size={
        'width': viewport_width,
        'height': viewport_height
    },
    
    # Recommended: Full HD by default
    viewport={
        'width': 1920,   # ← Full HD width
        'height': 1080   # ← Full HD height
    }
)
```

### 2. Real Interaction Methods (MUST USE THESE)

**Mouse Interactions:**
```python
# Smooth mouse movement (REQUIRED for professional look)
await page.mouse.move(x, y, steps=20)  # steps=20 makes it smooth

# Click with visual feedback
await page.mouse.click(x, y)

# Scroll with animation
await page.mouse.wheel(delta_x, delta_y)
```

**Keyboard Interactions:**
```python
# Type text character by character (realistic)
await page.keyboard.type("search query", delay=100)  # delay=100ms per char

# Press special keys
await page.keyboard.press("Enter")
await page.keyboard.press("Tab")
```

**Element Highlighting (Optional but Recommended):**
```python
# Before click - highlight element
await element.evaluate("""
    el => {
        el.style.transition = 'outline 0.2s';
        el.style.outline = '3px solid #1890ff';
        el.style.outlineOffset = '2px';
    }
""")
await asyncio.sleep(0.3)

# Perform click
await page.mouse.click(x, y)

# Remove highlight after click
await element.evaluate("""
    el => {
        el.style.outline = '';
        el.style.outlineOffset = '';
    }
""")
```

### 3. Video Output Format

**Recording Process:**
1. Playwright records `.webm` format automatically
2. File saved to `record_video_dir` when context closes
3. Merge TTS audio using FFmpeg:
   ```bash
   ffmpeg -i input.webm -i audio.mp3 -c:v libx264 -c:a aac output.mp4
   ```

---

## 📋 IMPLEMENTATION CHECKLIST (EVERY GENERATION MUST PASS)

Before considering a video generation complete, verify:

- [ ] **Browser launched with `record_video_dir` parameter?**
- [ ] **Viewport set to minimum 1440x900 (recommended 1920x1080)?**
- [ ] **Real `page.mouse.move/click/wheel` calls executed?**
- [ ] **Real `page.keyboard.type/press` calls used if needed?**
- [ ] **Interactions are smooth (steps > 10 for mouse movements)?**
- [ ] **Video duration > 5 seconds for simple pages (> 15s for complex)?**
- [ ] **File size > 1 MB (indicates real content, not blank screen)?**
- [ ] **Audio narration merged successfully?**
- [ ] **Output is MP4 format with H.264 codec?**

If ANY of these fail, the implementation is **INVALID** and must be fixed.

---

## 🎨 What This Skill Does (V3.0)

This skill provides **REAL** automated video generation capabilities:

- **✅ REAL HTML to Video**: Convert any web page into a professional demo video using actual browser recording
- **✅ AI Voice Narration**: Automatic text-to-speech with natural voices (Edge TTS)
- **✅ REAL UI Interaction Recording**: Actual mouse movements, clicks, scrolls, and keyboard input - all captured authentically
- **✅ Multi-Framework Support**: Works with Vue, React, Angular + UI libraries (Ant Design, Element UI, etc.)
- **✅ Smart Page Analysis**: Automatic detection of interactive elements (forms, tables, buttons, menus)
- **✅ Production Ready**: Error handling, retry logic, structured logging

---

## 🚀 When to Use This Skill

Use this skill when the user wants to:

1. **Generate REAL Demo Videos**
   - "Create a product demo from my landing page" → Record REAL interactions
   - "Make a tutorial video for my dashboard" → Show REAL navigation
   - "Record my web app as a video with voiceover" → Use REAL user flows

2. **Automate Testing Videos**
   - "Create regression test videos for my CI pipeline" → REAL test execution recorded
   - "Generate visual test documentation" → Authentic test runs, not simulations
   - "Record user journey videos" → Actual user paths through the app

3. **Create Presentations**
   - "Turn this HTML prototype into a presentation video" → REAL prototype interaction
   - "Make a marketing video from our SaaS page" → Show REAL features working
   - "Generate onboarding videos" → Guide users through REAL interface

---

## 💻 Usage Example (CORRECT V3.0 APPROACH)

### Python API (RECOMMENDED)

```python
import asyncio
from auto_video_generator import VideoGenerator

async def main():
    gen = VideoGenerator(verbose=True)
    
    result = await gen.generate(
        source="https://example.com/dashboard",
        output="./demo.mp4",
        options={
            "viewport_width": 1920,      # Full HD
            "viewport_height": 1080,
            "voice": "zh-CN-YunxiNeural", # Chinese voice
            "headless": False,            # Show browser window
            "show_cursor": True,          # Show mouse cursor
            "highlight_clicks": True,     # Highlight clicked elements
        }
    )
    
    print(f"✅ REAL Video generated!")
    print(f"   Duration: {result.duration_seconds:.1f}s")
    print(f"   Size: {result.file_size_mb:.2f} MB")
    print(f"   Resolution: {result.resolution}")

asyncio.run(main())
```

### What Happens Internally (V3.0)

```
1. Launch Chrome with recording enabled (record_video_dir)
2. Navigate to target URL
3. Analyze page structure (detect forms, buttons, tables)
4. Execute REAL interactions:
   - Mouse moves smoothly to elements
   - Clicks buttons with highlight effects
   - Types in input fields
   - Scrolls to show content
5. All actions automatically recorded as .webm
6. Generate TTS audio narration
7. Merge video + audio → final MP4
8. Return result with metadata
```

---

## ⚙️ Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `viewport_width` | int | 1920 | Video width (min: 1440) |
| `viewport_height` | int | 1080 | Video height (min: 900) |
| `voice` | string | zh-CN-YunxiNeural | Edge TTS voice name |
| `rate` | string | "-5%" | Speech rate adjustment |
| `headless` | bool | False | Hide browser window |
| `show_cursor` | bool | True | Show mouse cursor in video |
| `highlight_clicks` | bool | True | Highlight elements before clicking |
| `fps` | int | 4 | Target frames per second |
| `quality` | string | "high" | Video quality (low/medium/high) |

---

## 🛡️ Quality Standards (MUST MEET)

### Minimum Requirements

Every generated video MUST meet these standards:

1. **Duration**
   - Simple pages (landing): ≥ 10 seconds
   - Medium complexity (dashboard): ≥ 20 seconds
   - Complex apps (full workflow): ≥ 30 seconds

2. **Resolution**
   - Minimum: 1440×900
   - Recommended: 1920×1080 (Full HD)
   - Maximum: 2560×1440 (2K)

3. **File Size**
   - Minimum: 2 MB (indicates real content)
   - Typical: 5-50 MB depending on duration
   - If < 1 MB: Something went wrong (blank screen?)

4. **Content Quality**
   - ✅ Shows REAL page content (not blank/white)
   - ✅ Contains REAL mouse movements (visible cursor)
   - ✅ Has REAL clicks on UI elements
   - ✅ Includes scrolling behavior
   - ✅ Audio narration synced with visuals

---

## 🔧 Common Mistakes TO AVOID

### ❌ WRONG: Screenshot-based Approach

```python
# DON'T DO THIS!
for i in range(100):
    await page.screenshot(path=f"frame_{i}.png")  # ❌ Screenshots!
    await asyncio.sleep(0.1)

# Then use ffmpeg to combine images...  # ❌ Fake video!
```

### ✅ CORRECT: Real Recording Approach

```python
# DO THIS INSTEAD!
context = await browser.new_context(
    record_video_dir="./videos"  # ✅ Enable recording!
)

page = await context.new_page()
await page.goto("https://example.com")

# Real interactions that get recorded automatically
await page.mouse.move(500, 300, steps=20)
await page.mouse.click(500, 300)

await context.close()  # ✅ Finalizes recording
```

---

## 📊 Version History

### V3.2.0 (CURRENT) - Mandatory User Interactions
- **BREAKING CHANGE**: Region selection now REQUIRES explicit user confirmation (even with auto-detect)
- **BREAKING CHANGE**: Scenario preview is MANDATORY before recording (user must approve)
- **NEW**: Interactive region selection menu with visual layout diagram
- **NEW**: Scenario preview & validation system with edit/remove/add capabilities
- **ENHANCED**: User can modify scenarios (remove, reorder, edit narration, add custom)
- **ENHANCED**: Clear visual feedback showing page layout and detected regions
- **SECURITY**: Prevents accidental wrong-area recordings and wasted time

### V3.1.0 - PM-Driven & Region-Aware
- **NEW**: Recording region selection (clip to content area, exclude sidebar/header)
- **NEW**: Integration with bmad-agent-pm workflow (PRD generation → scenario decomposition)
- **NEW**: Scenario-based TTS narration generation
- **NEW**: Auto-detection of page components for intelligent scenario creation
- **IMPROVED**: User prompts for region selection (FULL / CONTENT ONLY / CUSTOM)
- **ENHANCED**: PRD output as JSON file alongside video

### V3.0.0 - Real Recording Mandate
- **BREAKING CHANGE**: Screenshot-based generation completely removed
- Added mandatory `record_video_dir` requirement
- Implemented real mouse/keyboard interaction recording
- Full HD default resolution (1920×1080)
- Enhanced quality standards and validation

### V2.0.0 - Previous Version (DEPRECATED)
- Used screenshot capture approach
- Produced low-quality short videos
- **No longer supported - upgrade to V3.1**

---

## 🤝 Contributing

All contributions MUST follow the V3.2 standard:
- ✅ Use Playwright native recording (`record_video_dir`)
- ✅ Support region-aware recording (clip areas)
- ✅ [MANDATORY] Force user to confirm recording region before starting
- ✅ [MANDATORY] Show scenario preview and wait for user approval before recording
- ✅ Integrate with bmad-agent-pm for PRD-driven scenarios
- ❌ No silent auto-detection without user confirmation allowed

---

## 📄 License

MIT License

---

**Version**: 3.2.0 (Mandatory User Interactions)
**Last Updated**: 2026-05-30
**Status**: PRODUCTION READY ✅
**Maintained by**: AVG Team
**Integration**: bmad-agent-pm (PM workflow)
