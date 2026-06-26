# ai-image-cli 完整参考文档

## 包信息

| 字段 | 值 |
|------|-----|
| 包名 | `ai-image-cli` |
| 入口命令 | `ai-image` |
| 模块路径 | `ai_image.cli` |
| 版本 | `1.0.0` |
| Python | `>=3.10` |
| 运行时依赖 | `typer>=0.9.0`, `requests>=2.28.0` |
| 许可证 | MIT |
| 私仓地址 | `http://music-pypi.hz.netease.com` |

## 安装方式

### 从内部私仓安装（推荐）

```bash
pip install ai-image-cli \
  -i http://music-pypi.hz.netease.com/simple \
  --trusted-host music-pypi.hz.netease.com
```

### 用户级安装

```bash
pip install --user ai-image-cli \
  -i http://music-pypi.hz.netease.com/simple \
  --trusted-host music-pypi.hz.netease.com
```

### 从源码安装（开发调试）

```bash
cd ai-image-cli
pip install -e .
```

## 项目架构

```
ai_image/
├── __init__.py               # 版本号定义
├── __main__.py               # python -m 入口
├── cli.py                    # Typer CLI 主入口，注册 3 个子命令
├── config.py                 # KeyProvider 自动选择（单例模式）
├── constants.py              # 全局常量（URL、默认值）
│
├── auth/                     # 鉴权层
│   ├── key_provider.py       # Protocol 接口 + ServiceKeys 数据类
│   ├── langbase_provider.py  # 企业认证：LANGBASE_TOKEN → Langbase API → 密钥
│   └── local_provider.py     # 本地认证：直读 ARK_API_KEY
│
├── providers/                # 服务提供商封装
│   └── ark_provider.py       # AIGW API 封装（text2img + img2img）
│
├── commands/                 # CLI 子命令实现
│   ├── text2img.py           # text2img — 文生图
│   ├── img2img.py            # img2img — 图生图
│   └── capabilities.py       # capabilities — 输出 JSON 能力描述
│
└── utils/
    ├── output.py             # 统一 JSON 输出（print_success / print_error）
    └── version_check.py      # 版本检查
```

## 环境变量

| 变量 | 说明 | 必须 |
|------|------|------|
| `LANGBASE_TOKEN` | Langbase 认证 Token（格式 `appId.appKey`） | 与下面二选一 |
| `ARK_API_KEY` | AIGW API Key（格式 `appId.appKey`） | 与上面二选一 |

## 认证流程

### 企业认证（LANGBASE_TOKEN）

```
LANGBASE_TOKEN (环境变量)
    │
    ▼
POST https://langbase.netease.com/api/langbase/openclaw/service/auth
  Body: {"token": "<LANGBASE_TOKEN>", "serviceName": "ai-image"}
    │
    ▼
Response: {"code": 200, "data": {"arkApiKey": "..."}}
    │
    ▼
缓存在进程内存（进程生命周期内只认证一次）
    │
    └─→ ArkProvider(ark_api_key) → AIGW API
```

### 本地认证（直读环境变量）

```
ARK_API_KEY (环境变量)
    │
    ▼
直接构造 ServiceKeys 对象
    │
    └─→ ArkProvider(ark_api_key) → AIGW API
```

## API 端点

### Langbase 认证

| 端点 | 方法 | URL |
|------|------|-----|
| 服务认证 | POST | `https://langbase.netease.com/api/langbase/openclaw/service/auth` |

### AIGW API

| 功能 | 方法 | URL |
|------|------|-----|
| 图像生成 | POST | `https://aigw-int.netease.com/ark/alpha/v1/image/generations` |

## 命令详细说明

### text2img

```
ai-image text2img PROMPT [OPTIONS]
```

| 参数 | 类型 | 必须 | 默认 | 说明 |
|------|------|------|------|------|
| PROMPT | str | 是 | - | 图片描述文本 |
| --size / -s | str | 否 | `1920x1920` | 图片尺寸（最低 `1920x1920`） |
| --seed | int | 否 | - | 随机种子（用于复现） |
| --guidance-scale / -g | float | 否 | `2.5` | 引导系数（控制生成质量） |
| --watermark / --no-watermark | bool | 否 | `false` | 是否添加水印 |

**返回数据结构：**
```json
{
  "success": true,
  "command": "text2img",
  "provider": "ark",
  "data": {
    "model": "doubao-seedream-4-5",
    "created": 1754384045,
    "data": [
      {
        "url": "https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/..."
      }
    ],
    "usage": {
      "generated_images": 1,
      "output_tokens": 4096,
      "total_tokens": 4096
    }
  }
}
```

### img2img

```
ai-image img2img PROMPT IMAGE_URL [OPTIONS]
```

| 参数 | 类型 | 必须 | 默认 | 说明 |
|------|------|------|------|------|
| PROMPT | str | 是 | - | 编辑描述文本 |
| IMAGE_URL | str | 是 | - | 源图片 URL |
| --seed | int | 否 | - | 随机种子（用于复现） |
| --guidance-scale / -g | float | 否 | `5.5` | 引导系数（控制编辑强度） |
| --watermark / --no-watermark | bool | 否 | `false` | 是否添加水印 |

**注意**: 图生图不支持 `--size` 参数，输出图片尺寸由源图片决定。

**返回数据结构：**
```json
{
  "success": true,
  "command": "img2img",
  "provider": "ark",
  "data": {
    "model": "doubao-seededit-3-0-i2i",
    "created": 1754384045,
    "data": [
      {
        "url": "https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/..."
      }
    ],
    "usage": {
      "generated_images": 1,
      "output_tokens": 4096,
      "total_tokens": 4096
    }
  }
}
```

### capabilities

```
ai-image capabilities
```

无参数，无需认证。输出完整的 JSON 能力描述，包含所有工具的参数定义和使用建议。

**返回数据结构：**
```json
{
  "success": true,
  "command": "capabilities",
  "tools": [
    {
      "name": "text2img",
      "description": "文生图 - 根据文本描述生成图片",
      "provider": "AIGW",
      "model": "doubao-seedream-4-5",
      "parameters": {
        "prompt": {"type": "string", "required": true, "description": "图片描述文本"},
        "size": {"type": "string", "required": false, "default": "1920x1920"},
        "seed": {"type": "integer", "required": false},
        "guidance_scale": {"type": "float", "required": false, "default": 2.5},
        "watermark": {"type": "boolean", "required": false, "default": false}
      }
    },
    {
      "name": "img2img",
      "description": "图生图 - 基于源图片和文本生成新图片",
      "provider": "AIGW",
      "model": "doubao-seededit-3-0-i2i",
      "parameters": {
        "prompt": {"type": "string", "required": true, "description": "编辑描述文本"},
        "image_url": {"type": "string", "required": true, "description": "源图片 URL"},
        "seed": {"type": "integer", "required": false},
        "guidance_scale": {"type": "float", "required": false, "default": 5.5},
        "watermark": {"type": "boolean", "required": false, "default": false}
      }
    }
  ]
}
```

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "command": "text2img",
  "error": "未找到 AIGW API Key",
  "hint": "请设置 LANGBASE_TOKEN 或 ARK_API_KEY 环境变量"
}
```

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `RuntimeError: 未配置认证` | 没有设置任何认证环境变量 | 设置 `LANGBASE_TOKEN` 或 `ARK_API_KEY` |
| `AUTH_FAILED (401)` | Token 无效或过期 | 联系管理员获取新的 Token |
| `SERVICE_NOT_FOUND (404)` | 应用未开通 ai-image 服务 | 联系管理员开通服务 |
| `Invalid size` | 尺寸参数格式错误或低于最低要求 | 使用 `1920x1920` 或更大尺寸 |
| `Invalid image URL` | 图片 URL 无效或无法访问 | 检查 URL 是否正确且可访问 |

## 模型说明

### doubao-seedream-4-5 (文生图)

- **能力**: 根据文本描述生成高质量图片
- **默认尺寸**: 1920x1920
- **最低尺寸**: 1920x1920
- **默认引导系数**: 2.5
- **特点**: 支持中文和英文提示词，生成速度快，质量稳定

### doubao-seededit-3-0-i2i (图生图)

- **能力**: 基于源图片进行编辑和转换
- **尺寸**: 由源图片决定，不可指定
- **默认引导系数**: 5.5
- **特点**: 保持源图片结构，精确执行编辑指令

## 最佳实践

### 提示词优化

1. **文生图提示词建议**:
   - 明确描述主体、风格、环境、光照等要素
   - 使用具体的形容词和名词
   - 中英文均可，建议使用中文
   - 示例: "一个穿着红色连衣裙的中国女孩，在夕阳下的海滩上微笑，高清，柔和光线"

2. **图生图提示词建议**:
   - 明确说明要修改的部分
   - 避免过于复杂的指令
   - 示例: "将背景改成蓝天白云" / "转为水彩画风格"

### 参数调优

1. **guidance_scale (引导系数)**:
   - 文生图: 2.0-4.0，推荐 2.5
   - 图生图: 4.0-7.0，推荐 5.5
   - 值越大，生成结果越贴近提示词，但可能过度拟合

2. **seed (随机种子)**:
   - 相同种子 + 相同参数 = 可复现的结果
   - 用于微调和对比实验
   - 不设置时每次生成不同的结果

3. **watermark (水印)**:
   - 默认不添加水印
   - 正式发布或版权保护时建议启用
