# 儿童绘本生成器


## 一、概述

儿童绘本生成器是一个基于百度文心大模型图像生成模型能力的 OpenClaw Skill，封装了 Baidu AI Studio 的 `ERNIE-Image-Turbo` API，通过提炼儿童故事核心画面，通过文本生成图像（Text-to-Image）核心能力生成儿童绘本。Skill 通过 Python 脚本调用 OpenAI 兼容接口，实现与百度文心图像生成服务的无缝对接。

### 1.1 设计目标

| 目标 | 说明 |
|------|------|
| **易用性** | 单条命令即可完成图像生成，无需手动处理 API 调用细节 |
| **灵活性** | 支持多种分辨率、支持命令行传参和环境变量配置 API Key |
| **分辨率** | 1024x1024/1376x768/1264x848/ 1200x896/896x1200/848x1264/768x1376 |
| **跨平台** | 基于 Python 3.7+ 和 `openai` 库，兼容 Windows/macOS/Linux |

### 1.2 核心能力矩阵

| 能力 | 支持状态 | 备注 |
|------|---------|------|
| 文本生成图像 | ✅ | 核心功能，支持详细 prompt |
| 多分辨率输出 | ✅ | 7 种预设分辨率 |
| 中文文字渲染 | ✅ | 可在 prompt 中指定中文文字内容 |
| 批量生成 | ❌ | 当前版本单图生成 |
| 风格迁移 | ⚠️ | 依赖 prompt 描述，无独立风格参数 |
---

## 二、架构设计

### 2.1 组件关系图

```
输入儿童故事，或者儿童故事主题
    ↓
通过大模型生成故事关键画面prompt
    ↓
调用ERNIE-Image 生成绘本图  

```

### 2.2 数据流

```
用户输入故事内容，或者故事主题
    │
    ▼

生成故事多个关键画面Prompt
    │
    ▼
[generate_image.py]
    │
    ├── 1. 解析命令行参数 (argparse)
    │      ├── --prompt: 图像描述文本
    │      ├── --filename: 输出文件路径
    │      ├── --resolution: 输出分辨率
    │      └── --api-key: API 密钥（可选）
    │
    ├── 2. 解析 API Key（优先级递减）
    │      ├── ① --api-key 参数
    │      ├── ② ERNIE-Image_API_KEY 环境变量
    │      ├── ③ ERNIE_Image_API_KEY 环境变量
    │
    ├── 3. 初始化 OpenAI 客户端
    │      ├── api_key = 解析结果
    │      ├── base_url = "https://aistudio.baidu.com/llm/lmapi/v3"
    │      └── 模型 = "ERNIE-Image-Turbo"
    │
    ├── 4. 调用 API
    │      ├── POST /images/generations
    │      ├── payload: {model, prompt, size, response_format: "b64_json"}
    │      └── 接收 base64 编码图像数据
    │
    └── 5. 保存文件
           ├── 创建输出目录（如果不存在）
           ├── base64 解码 → PNG 字节流
           └── 写入磁盘
```

---

## 三、核心模块详解

### 3.1 参数解析模块

**文件:** `scripts/generate_image.py`

使用 Python 标准库 `argparse` 实现命令行参数解析，设计为**全显式传参**，无交互式输入：

| 参数 | 简写 | 必填 | 类型 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--prompt` | `-p` | ✅ | string | - | 图像描述文本 |
| `--filename` | `-f` | ✅ | string | - | 输出文件路径（支持绝对/相对路径） |
| `--resolution` | `-r` | ❌ | choice | `1024x1024` | 输出分辨率 |
| `--api-key` | `-k` | ❌ | string | `None` | API 密钥（覆盖环境变量） |

**设计决策：**
- `--filename` 为必填项而非自动生成：赋予用户完全的文件命名控制权
- `--resolution` 使用 `choices` 限制：避免传入 API 不支持的分辨率导致报错
- 无 `--output-dir` 参数：通过 `--filename` 中的路径信息直接推导

### 3.2 API Key 解析模块

```python
def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    for key in ["ERNIE-Image_API_KEY", "ERNIE_Image_API_KEY", "BAIDU_API_KEY"]:
        value = os.environ.get(key)
        if value:
            return value
    return None
```

**多环境变量兼容设计：**

| 环境变量名 | 优先级 | 设计原因 |
|-----------|--------|---------|
| `ERNIE-Image_API_KEY` | 1（最高） | 官方推荐命名，与 Skill 名称一致 |
| `ERNIE_Image_API_KEY` | 2 | 兼容下划线命名（部分系统不支持连字符） |

**安全考量：**
- 命令行传参 `--api-key` 会暴露在进程列表中（`ps` 可见），建议仅在临时场景使用
- 生产环境推荐设置环境变量，避免密钥泄露

### 3.3 OpenAI 客户端封装

```python
client = OpenAI(
    api_key=api_key,
    base_url="https://aistudio.baidu.com/llm/lmapi/v3"
)
```

**关键设计：**
- 使用 `openai` Python SDK（非百度原生 SDK），利用其 **OpenAI 兼容接口** 能力
- `base_url` 指向百度 AI Studio 的 OpenAI 兼容端点
- 模型名称硬编码为 `"ERNIE-Image-Turbo"`，这是当前百度文心图像生成的默认模型

### 3.4 API 调用与响应处理

```python
img = client.images.generate(
    model="ERNIE-Image-Turbo",
    prompt=contents,
    size=output_resolution,
    response_format="b64_json",
)

# 解码并保存
image_bytes = base64.b64decode(img.data[0].b64_json)
with open(output_path, "wb") as f:
    f.write(image_bytes)
```

**响应格式：**
- `response_format="b64_json"`：返回 base64 编码的 PNG 图像数据
- 不返回 URL（避免临时链接失效问题）
- 直接内存解码写入磁盘，无中间临时文件

---

## 四、分辨率系统设计

### 4.1 支持的分辨率列表

| 分辨率 | 宽高比 | 适用场景 | 备注 |
|--------|--------|---------|------|
| `1024x1024` | 1:1 | 头像、方形插画 | 默认分辨率 |
| `1376x768` | 16:9 | 横屏壁纸、视频封面 | 宽屏 |
| `1264x848` | ~3:2 | 照片比例 | 接近单反相机比例 |
| `1200x896` | ~4:3 | 传统屏幕比例 | 兼容旧设备 |
| `896x1200` | ~3:4 | 竖屏照片 | 类似手机竖拍 |
| `848x1264` | ~2:3 | 竖屏壁纸 | 接近手机屏幕 |
| `768x1376` | ~9:16 | 手机竖屏壁纸 | 全面屏手机适配 |



## 五、Prompt 工程指南

### 5.1 Prompt 传递策略

Skill 采用**透传优先**策略：
- 默认将用户描述原样传递给 API
- 仅在用户描述明显不足时进行补充优化

### 5.2 高命中率 Prompt 模板

```
Create an image of: <主体描述>
Style: <艺术风格>
Composition: <构图/镜头>
Lighting: <光影效果>
Background: <背景描述>
Color palette: <色彩方案>
Avoid: <需要避免的内容>
```

### 5.3 中文文字渲染技巧

ERNIE-Image 支持在图像中渲染中文文字，关键要点：

1. **明确指定文字内容**：在 prompt 中直接写出要显示的中文
2. **指定字体风格**：如「行书」「楷书」「宋体」等
3. **指定位置和样式**：如「顶部居中」「白色字体带金色光晕」
4. **控制大小**：避免文字过大遮挡主体或过小无法辨认

**示例：**
```
In the upper portion of the image, elegant vertical Chinese calligraphy 
text arranged in two lines: first line '山再高，往上攀，总能登顶；' 
and second line '路再长，走下去，定能到达。' — the text is rendered 
in a refined semi-cursive Chinese calligraphy style (行书), white color 
with subtle golden glow effect, positioned in the upper third area.
```

---

## 六、错误处理与故障排查

### 6.1 预检清单（Preflight）

在调用脚本前，Agent 应检查：

```bash
#  API Key 是否可用
test -n "$ERNIE-Image_API_KEY" || echo "API Key 未设置"


```

### 6.2 常见错误与解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Error: No API key provided.` | API Key 未提供 | 设置环境变量或传 `--api-key` |
| 401/403 权限错误 | Key 无效或过期 | 更换有效 Key |
| 配额超限错误 | 调用次数达到上限 | 等待配额重置或升级账户 |
| 图像生成失败 | Prompt 包含敏感内容 | 修改 prompt 避免违规描述 |

### 6.3 调试模式

当前脚本无独立 `--verbose` 参数，调试时可：
1. 检查命令行参数是否正确传递
2. 验证环境变量是否加载到当前进程
3. 手动测试 API 连通性：`curl https://aistudio.baidu.com/llm/lmapi/v3`

---

## 七、安全设计

### 7.1 密钥管理

| 场景 | 风险等级 | 建议做法 |
|------|---------|---------|
| 命令行传参 `--api-key` | ⚠️ 中 | 临时使用，避免在共享环境使用 |
| 用户级环境变量 | ✅ 低 | 推荐方案，仅当前用户可见 |
| 系统级环境变量 | ⚠️ 中 | 多用户共享，注意权限控制 |
| 硬编码在脚本中 | ❌ 高 | 严禁，会泄露到版本控制 |

### 7.2 输入安全

- Prompt 内容直接传递给百度 API，**无本地过滤**
- 依赖百度服务端的内容安全策略
- 敏感/违规内容会被 API 拒绝并返回错误

### 7.3 输出安全

- 生成的图像保存到用户指定路径
- 脚本自动创建父目录（`mkdir(parents=True)`）
- 无文件覆盖确认，同名文件直接覆盖

---

## 八、扩展性设计

### 8.1 当前限制

| 限制项 | 说明 | 未来改进方向 |
|--------|------|------------|
| 单图生成 | 每次调用仅生成一张 | 支持 `--batch` 批量生成 |
| 无回调机制 | 生成完成后仅打印路径 | 支持 webhook/消息通知 |
| 无进度反馈 | 长时间生成无中间状态 | 添加进度条或流式输出 |
| 固定模型 | 仅支持 ERNIE-Image-Turbo | 支持模型选择参数 |
| 无元数据 | 输出 PNG 无 EXIF 信息 | 嵌入生成参数到图像元数据 |

### 8.2 与其他 Skill 的协作

| 协作场景 | 方式 | 示例 |
|---------|------|------|
| 图像 → 文档 | 插入 docx/pptx | 使用 `docx`/`pptx` Skill 将生成图像插入文档 |
| 图像 → 云存储 | 上传备份 | 使用 `cloud-upload-backup` Skill 上传生成图像 |
| 图像 → 展示 | 浏览器查看 | 使用 `xbrowser` Skill 打开生成图像预览 |
| 批量 → 自动化 | 定时任务 | 使用 `qclaw-cron-skill` 定时生成图像 |

---

## 九、使用示例

### 9.1 基础生成

```bash
python scripts/generate_image.py \
  --prompt "A serene Japanese garden with cherry blossoms" \
  --filename "japanese-garden.png" \
  --resolution 1024x1024
```

### 9.2 手机壁纸（竖屏）

```bash
python scripts/generate_image.py \
  --prompt "A mystical dark fantasy meadow with a glowing-eyed kitten..." \
  --filename "wallpaper.png" \
  --resolution 768x1376 \
  --api-key "your-api-key-here"
```



---

## 十、版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 1.0.1 | 2026-04-25 | 初始版本，支持文生图、图生图、7种分辨率 |

---

## 十一、参考资源

- **百度 AI Studio:** https://aistudio.baidu.com
- **OpenAI Python SDK:** https://github.com/openai/openai-python
- [https://aistudio.baidu.com/blog/detail/794723628346373](https://aistudio.baidu.com/blog/detail/794723628346373)
- [https://aistudio.baidu.com/ernieimage](https://aistudio.baidu.com/ernieimage)
- [https://aistudio.baidu.com/modelsdetail/46030/intro](https://aistudio.baidu.com/modelsdetail/46030/intro)

---

