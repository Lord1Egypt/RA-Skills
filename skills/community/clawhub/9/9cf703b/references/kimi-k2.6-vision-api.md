# Kimi K2.6 视觉 API 调用模式

> 当 deepseek-v4-pro 等纯文本模型无法使用 `vision_analyze` 时，通过 Python 直接调用 Kimi K2.6 多模态 API 进行图表视觉分析。

## 快速参考

| 属性 | 值 |
|------|-----|
| **模型** | `kimi-k2.6` |
| **API Base** | `https://api.moonshot.cn/v1` |
| **兼容性** | 完全兼容 OpenAI SDK |
| **视觉能力** | 图片 + 视频 |
| **上下文** | 256K tokens |
| **认证** | `MOONSHOT_API_KEY` 环境变量 |
| **图片格式** | base64 data URI: `data:image/{ext};base64,{data}` |
| **思考模式** | 默认开启，分析图表时建议禁用: `extra_body={"thinking": {"type": "disabled"}}` |

## 标准调用模板

```python
import base64, os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("MOONSHOT_API_KEY"),  # 或直接传入字符串
    base_url="https://api.moonshot.cn/v1",
)

# 1. 读取图片并 base64 编码
with open(image_path, "rb") as f:
    image_data = f.read()

ext = os.path.splitext(image_path)[1].lstrip('.')
image_url = f"data:image/{ext};base64,{base64.b64encode(image_data).decode('utf-8')}"

# 2. 发送多模态请求
completion = client.chat.completions.create(
    model="kimi-k2.6",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": "请描述这张科学图表的内容。"},
        ],
    }],
    extra_body={"thinking": {"type": "disabled"}},  # 禁用思考模式，直接输出
    max_tokens=4096,
)

# 3. 获取结果
print(completion.choices[0].message.content)
print(f"Tokens: {completion.usage.total_tokens}")
```

## 批量分析模板

```python
figs = [
    ("Figure 1", "/path/to/page03_img.jpeg", "详细prompt..."),
    ("Figure 2", "/path/to/page06_img.jpeg", "详细prompt..."),
    # ...
]

for fig_name, path, prompt in figs:
    with open(path, "rb") as f:
        image_data = f.read()
    ext = os.path.splitext(path)[1].lstrip('.')
    image_url = f"data:image/{ext};base64,{base64.b64encode(image_data).decode('utf-8')}"
    
    print(f"Analyzing {fig_name}... ({len(image_data)//1024}KB)")
    
    completion = client.chat.completions.create(
        model="kimi-k2.6",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": prompt},
            ],
        }],
        extra_body={"thinking": {"type": "disabled"}},
        max_tokens=4096,
    )
    
    print(completion.choices[0].message.content)
    print(f"[Tokens: {completion.usage.total_tokens}]")
```

## API Key 管理

**优先级**: 环境变量 > 配置文件 > 硬编码

```bash
export MOONSHOT_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

获取 Key: https://platform.kimi.com → 登录 → 用户中心 → API Key

**注意**: Kimi 有两种 Key 格式：
- `sk-kimi-...` — 新格式，可能对应新 API 端点（不兼容 `api.moonshot.cn`）
- `sk-...` — 标准格式，兼容 `api.moonshot.cn/v1`

如遇 `401 Invalid Authentication`，先 curl 验证：
```bash
curl -s https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer $MOONSHOT_API_KEY"
```

## Prompt 编写建议

好的 prompt 应包含：
1. **论文背景**（1句）: "这是论文 Figure X: ..."
2. **Panel 列表**: "共N个panels (A-Z)，A是..., B是..."
3. **具体请求**: "请提取所有可见的数值、标签、Kd值、fold change..."
4. **输出格式提示**: "请用Markdown表格整理"

## 性能参考

| 图片大小 | base64编码 | 典型响应时间 | tokens消耗 |
|----------|-----------|-------------|-----------|
| ~500 KB | ~660K chars | 50-80s | ~3000-5000 |
| ~900 KB | ~1.2M chars | 80-120s | ~5000-7000 |
| ~1.2 MB | ~1.6M chars | 50-60s | ~5000-6000 |

> 注：响应时间受网络和模型负载影响，1.2MB 图片可能比 900KB 更快，这取决于图片复杂度。

## 关键陷阱

| 陷阱 | 现象 | 解决 |
|------|------|------|
| **思考模式吃内容** | `content=""`, `reasoning_content="..."` | 加 `extra_body={"thinking": {"type": "disabled"}}` |
| **API Key 格式不匹配** | `401 Invalid Authentication` | 换标准 `sk-` 前缀 key，验证端点 |
| **输出截断** | 分析到一半停止 | 增大 `max_tokens`（4096+） |
| **base64 过大** | 请求超时/失败 | 对大图先 resize（PIL: `img.resize((w//2, h//2))`） |
| **pip 未装 openai** | `ModuleNotFoundError` | `python3 -m pip install 'openai>=1.0'` |

## 与 PyMuPDF 提取的整合

```
PDF → PyMuPDF 提取图片 + 全文
         ↓                    ↓
    .jpeg/.png 文件      full_text.txt
         ↓                    ↓
    Kimi K2.6 视觉分析   Caption + 正文提取
         ↓                    ↓
         └────── 数据融合 ──────┘
                    ↓
            结构化 Markdown/JSON 输出
```
