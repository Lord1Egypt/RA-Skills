---
name: comfyui-running
description: 全自动运行 ComfyUI 工作流：通过 REST API 执行工作流，支持 Windows / Linux / WSL 跨平台。By comfyui资源网 - www.comfyorg.cn
metadata: {"clawhub":{"emoji":"🎨","requires":{"bins":["python3","python"],"os":["windows","linux","darwin"]},"tags":["comfyui","automation","workflow","image-generation"]}}
---

---
全自动运行 ComfyUI 工作流：通过 CDP 协议控制 Edge 浏览器，自动化操作 ComfyUI 界面，并通过 REST API 执行工作流。
---

> 全自动运行 ComfyUI 工作流 | By **[comfyui资源网](https://www.comfyorg.cn)**

[![comfyui资源网](https://img.shields.io/badge/comfyui%E8%B5%84%E6%BA%90%E7%BD%91-ComfyUI%E8%B5%84%E6%BA%90%E5%AE%A3%E5%92%8C-orange?style=for-the-badge&logo=firefox)](https://www.comfyorg.cn)

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 🚀 自动启动 | 检测 ComfyUI 状态，未运行则自动启动 |
| 📋 工作流管理 | 列出、加载、修改工作流 |
| 🎨 文本生图 | 一句话生成图片 |
| 🔄 跨平台 | Windows / Linux / WSL 自动适配 |

---

## 快速开始

### 一句话生成图片

```python
from comfyui_automation import quick_generate

result = quick_generate("a beautiful cat")
# result = {
#     "success": True,
#     "image_path": "H:\\ComfyUI-aki-v3\\ComfyUI\\output\\ComfyUI_00001_.png",
#     "prompt_id": "xxx-xxx"
# }
```

### 完整控制

```python
from comfyui_automation import ComfyUIAutomation

automation = ComfyUIAutomation()
automation.ensure_comfyui_running()

result = automation.generate(
    prompt="1girl, portrait",
    workflow_name="文生图",
    negative_prompt="low quality, blurry",
    steps=25,
    seed=None,        # None=随机
    batch_size=1
)

if result["success"]:
    print(f"图片路径: {result['image_path']}")
```

---

## 配置说明

### config.json 配置项

| 配置项 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `comfyui_root` | ✅ | - | ComfyUI 根目录（包含 main.py） |
| `python_path` | | 自动检测 | Python 解释器路径 |
| `workflows_dir` | | 自动检测 | 工作流 JSON 目录 |
| `output_dir` | | `{comfyui_root}/output` | 图片输出目录 |
| `comfyui_port` | | 8188 | ComfyUI 端口 |
| `ui_type` | | `auto` | UI 类型：`aki`=秋叶版，`official`=官方版 |
| `browser_path` | | 自动检测 | 浏览器路径（CDP 模式用） |

### 路径格式（跨平台）

| 平台 | 示例 |
|------|------|
| **Windows** | `H:/ComfyUI-aki-v3/ComfyUI` 或 `H:\\ComfyUI-aki-v3\\ComfyUI` |
| **Linux** | `/opt/ComfyUI/ComfyUI` |
| **WSL** | `/mnt/h/ComfyUI-aki-v3/ComfyUI` |

> ⚠️ 推荐使用正斜杠 `/`，Python 会自动处理跨平台兼容性

### 跨平台自动检测路径

| 平台 | 检测路径 |
|------|---------|
| **Windows** | `H:\ComfyUI-aki-v3\ComfyUI`, `D:\ComfyUI\ComfyUI`, 用户目录等 |
| **Linux** | `/opt/ComfyUI/ComfyUI`, `~/ComfyUI/ComfyUI` |
| **WSL** | `/mnt/h/ComfyUI-aki-v3/ComfyUI` 等 |

---

## API 参考

### `ComfyUIAutomation` 类

```python
automation = ComfyUIAutomation()

# ===== 生命周期 =====
automation.is_comfyui_running()          # 检测是否运行
automation.start_comfyui()               # 启动 ComfyUI
automation.ensure_comfyui_running()      # 确保运行（未运行则启动）

# ===== 工作流 =====
automation.list_workflows()              # 列出可用工作流
automation.load_workflow(name)           # 加载工作流

# ===== 执行生成 =====
automation.generate(
    prompt="描述",           # 正向提示词
    workflow_name="文生图",  # 工作流名称
    negative_prompt="",      # 负向提示词
    steps=20,               # 采样步数
    seed=None,              # 种子，None=随机
    batch_size=1            # 批次数
)
```

### `quick_generate(prompt, **kwargs)`

一句话生成快捷函数。

---

## 命令行使用

```bash
# 直接生成
python -m lib.comfyui_automation "a cute cat" -s 20 -w 文生图

# 参数
#   prompt        - 提示词
#   -s, --steps   - 采样步数（默认20）
#   -w, --workflow - 工作流名称（默认default）
#   -n, --negative - 负向提示词
#   --seed        - 随机种子
#   --batch       - 批次数（默认1）
```

---

## 依赖

```bash
pip install requests websockets
```

---

## 故障排除

### 1. 'int' object is not subscriptable

**原因：** 节点链接格式错误

```json
"model": ["4", 0]   ✅ [node_id, output_slot]
"model": 4          ❌ 错误！
```

### 2. main.py not found

**解决：** 检查 `config.json` 中 `comfyui_root` 是否指向包含 `main.py` 的目录

### 3. Windows PowerShell `&&` 语法错误

```powershell
# ❌ 错误 (PowerShell 5.x)
cd "..." && python -c "..."

# ✅ 正确
Set-Location "..."
python -c "..."
```

---

## 📌 推荐资源

| 资源类型 | 链接 |
|----------|------|
| 🏠 首页 | https://www.comfyorg.cn |
| 📖 教程 | https://www.comfyorg.cn/tutorial |
| 🎭 工作流 | https://www.comfyorg.cn/workflow |
| 💬 整合包 | https://www.comfyorg.cn/shop/1680.html |

---

**版本**：2.0.0  
**许可**：MIT
