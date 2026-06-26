# doubao-video-creator - 豆包视频创作助手 v3.0

## 🆕 v3.0 更新 (2026-04-28)

- ✅ **默认时长**：从 5 秒改为 10 秒
- ✅ **用户可选时长**：10 秒或 15 秒
- ✅ **用户可选模型版本**：1.0 / 1.5 / 2.0
- ✅ 每个场景独立选择时长和模型版本
- ✅ 文生图模型升级：`wan2.6-t2i` → `wan2.7-image-pro`

---

## 📋 技能描述

使用火山引擎豆包（Doubao Seedance）视频生成模型，帮助用户创作专业视频。支持**项目化配置管理**、**分场景生成方式选择**、**完整状态追踪**。

## 🎯 触发条件

用户提到以下关键词时触发：
- "豆包生成视频"
- "帮我做视频"
- "制作短视频"
- "视频创作"
- "生成宣传视频"
- "doubao 视频"
- "火山引擎视频"

## 🔄 工作流程（v3.0 增强版）

### 阶段 0：首次配置

```
您好！我是豆包视频创作助手 🎬

检测到您是首次使用，需要先配置豆包 API 信息：

1️⃣ 请提供您的火山引擎豆包 API Key
   - 获取地址：https://console.volcengine.com/ark

配置将保存，后续使用无需重复输入。
```

### 阶段 1：需求收集

```
为了生成更符合您需求的视频，请告诉我：

**1. 视频主题**：是什么产品/服务？

**2. 目标受众**：视频给谁看的？

**3. 视频风格**：科技感？温馨？专业？电影感？

**4. 参考资料**（可选）：
📄 文档资料 | 🔗 网页链接 | 🖼️ 参考图片 | 📝 文字描述
```

### 阶段 2：脚本规划
1. 分析参考资料
2. 生成视频场景规划脚本
3. 发送脚本给用户确认

### 阶段 3：分场景生成确认

**对每个场景，单独确认生成方式、时长和模型版本：**

```
🎬 场景 1/3：开场展示

请选择生成方式：
A) 文生视频 - 直接用文字提示词
B) 图生视频 - 使用参考图片生成

请选择时长：
1️⃣ 10 秒（默认）
2️⃣ 15 秒

请选择模型版本：
① 2.0 - 最新版本，效果最佳（推荐）
② 1.5 - 稳定版本，广泛使用
③ 1.0 - 基础版本，兼容性好
```

### 阶段 4：提示词确认（关键！）

**⚠️ 重要：必须先确认提示词，才能生成视频！**

### 阶段 5：分场景生成（逐个进行！）

**⚠️ 重要：逐个场景生成，不要批量！**

### 阶段 6：视频合成
1. 将所有确认的场景视频按顺序合成
2. 添加转场效果
3. 发送最终视频

## 🛠️ 工具调用

### 1. 火山引擎豆包 API（视频生成）

**API Key**: `65ae8f92-134c-4194-a3af-6e6cb74284e0`  
**API 端点**: `https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`

#### 文生视频 (T2V) ✅

```python
import requests

payload = {
    "model": "doubao-seedance-2-0-260128",
    "content": [{"type": "text", "text": "一只可爱的小猫在草地上玩耍"}],
    "parameters": {
        "ratio": "16:9",
        "duration": 10,  # 10 秒（默认）或 15 秒
        "watermark": False
    }
}

response = requests.post(url, headers=headers, json=payload, timeout=30)
task_id = response.json()["id"]
```

#### 图生视频 (I2V) ✅

```python
payload = {
    "model": "doubao-seedance-2-0-260128",
    "content": [
        {"type": "image_url", "image_url": {"url": "http://example.com/coffee.jpg"}},
        {"type": "text", "text": "镜头缓缓推进，展示咖啡店温馨环境"}
    ],
    "parameters": {
        "ratio": "16:9",
        "duration": 10,
        "watermark": False
    }
}
```

#### 查询任务状态

```python
status_url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"
response = requests.get(status_url, headers=headers, timeout=10)
result = response.json()
# status: "pending" | "running" | "succeeded" | "failed"
video_url = result["content"][0]["url"]
```

### 可用模型列表

| 模型 ID | 版本 | 推荐 | 说明 |
|--------|------|------|------|
| `doubao-seedance-2-0-260128` | 2.0 | ✅ 推荐 | 最新版本，效果最佳 |
| `doubao-seedance-2-0-fast-260128` | 2.0-fast | ✅ | 2.0 快速版 |
| `doubao-seedance-1-5-pro-251215` | 1.5 | ✅ | 稳定版本，广泛使用 |
| `doubao-seedance-1-0-pro-250528` | 1.0 | | 基础版本，兼容性好 |
| `doubao-seedance-1-0-pro-fast-251015` | 1.0-fast | | 1.0 快速版 |

### 2. 通义万相 API（图片生成）

```python
python3 /root/.openclaw/workspace/wanxiang_generate.py "提示词" output.png
```

## ⚙️ 配置参数

### 全局配置文件: `~/.openclaw/workspace/doubao-config.json`

```json
{
  "default_api_key": "65ae8f92-134c-4194-a3af-6e6cb74284e0",
  "default_text_to_video_model": "doubao-seedance-2-0-260128",
  "default_duration": 10,
  "last_updated": "2026-04-28T18:00:00"
}
```

### 视频生成参数
- **时长**: 10 秒或 15 秒（默认 10 秒，用户可选）
- **分辨率**: 480p / 720p / 1080p
- **比例**: 16:9 / 9:16 / 1:1
- **帧率**: 24 fps

## ⚠️ 注意事项

### 1. API 格式
- ✅ Seedance 使用 `content: [{type: "text"}, {type: "image_url"}]`
- ✅ 已验证通过（2026-04-28）

### 2. 模型 ID 必须带版本号
- ❌ 错误：`doubao-seedance-1-5-pro`
- ✅ 正确：`doubao-seedance-1-5-pro-251215`

### 3. 图片 URL 要求
- ✅ 必须使用 HTTP/HTTPS 公网可访问的 URL

### 4. 成本控制
- 先确认参考图再生成视频（避免浪费）
- 逐个场景生成

### 5. 时长说明
- 10 秒：约 1-2 分钟生成
- 15 秒：约 2-3 分钟生成

---

## 📁 文件管理

### 项目目录结构
```
/root/.openclaw/workspace/doubao-video-projects/
└── video_20260331_120000/
    ├── project.json
    ├── config.json
    ├── references/
    ├── characters/
    ├── scenes/
    ├── videos/
    └── final_video.mp4
```

## 🔄 更新日志

### v3.0 (2026-04-28)
**新增功能**:
- ✅ 默认时长从 5 秒改为 10 秒
- ✅ 支持用户选择时长：10 秒或 15 秒
- ✅ 支持用户选择模型版本：1.0 / 1.5 / 2.0
- ✅ 每个场景独立选择时长和模型

### v2.2 (2026-04-28)
- ✅ 更新模型列表：添加 2.0 版本
- ✅ 文生图模型升级：wan2.6-t2i → wan2.7-image-pro

### v2.1 (2026-04-03)
- ✅ 文生图模型升级：wan2.6-t2i → wan2.7-image-pro

### v2.0 (2026-03-31)
- ✅ 首次使用配置流程
- ✅ 分场景生成方式选择
- ✅ 完整项目记录文件

---

**Skill 版本**: v3.0  
**创建时间**: 2026-03-31  
**更新时间**: 2026-04-28  
**作者**: 卡妹 🌸
