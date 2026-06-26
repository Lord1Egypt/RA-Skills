---
name: 1688-distribution-material-newton
description: |
  1688 素材优化 skill，支持商品图片优化（AI 生图）、抠图（生成白底图）、标题优化和卖点生成。
  当用户提到"优化图片"、"优化主图"、"生成图片"、"换背景"、"AI 生图"、"抠图"、"白底图"、"去背景"、"扣图"、"优化标题"、"生成标题"、"改标题"、"生成卖点"、"提取卖点"、"素材优化"等意图时使用此 skill。
  支持通过 1688 商品 ID 或图片 URL 进行操作。
metadata: {"openclaw": {"emoji": "🎨", "requires": {"bins": ["python3"]}, "primaryEnv": "ALI_1688_AK"}}
---

# 1688 素材优化 Skill

## 核心原则

1. **渐进式加载**：不要一次性加载所有 references，根据用户意图按需加载对应的子 skill
2. **prompt 原封不动**：用户的 query 必须原封不动传入 `--prompt` 参数，不得改写、精简或翻译
3. **展示时直接输出 `markdown` 字段**，Agent 分析追加在后面，不得混入其中
4. **所有输出必须使用中文**

## 背景说明

AK（Access Key）通过 clawhub 获取，通过环境变量 ALI_1688_AK 配置。AK 已绑定用户身份，无需任何额外的身份参数。

统一入口：`python3 {baseDir}/cli.py <command> [options]`

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

## 前置检查：确认 AK 已配置

**skill 触发后，第一步必须立即检查 AK，不得先执行任何接口调用。**

→ 阅读并执行 `references/10_ak_configure.md`

## 渐进式加载规则

### 第一层：基础层（始终加载）

- `references/10_ak_configure.md` — AK 配置检查

### 第二层：路由层（根据意图加载）

解析用户 query，匹配操作类型，加载对应的子 skill：

| 用户关键词 | 操作类型 | 加载的子 skill | 优先级 |
|-----------|---------|---------------|--------|
| 抠图、白底图、去背景、扣图、抠背景、透明背景 | **抠图** | `references/50_cutout_image.md` | **最高**（优先匹配） |
| 优化图片、优化主图、生成图片、换背景、去水印、AI 生图、场景图 | **图片优化** | `references/80_image_optimize.md` | 高 |
| 优化标题、生成标题、改标题 | **标题优化** | `references/60_title_optimize.md` | 中 |
| 生成卖点、提取卖点、商品卖点 | **卖点生成** | `references/70_selling_point.md` | 中 |

### 第三层：依赖层（被上层 skill 按需加载）

以下子 skill 不直接由路由层触发，而是被上层 skill 引用时加载：

- `references/20_product_info.md` — 商品信息查询（被标题优化、卖点生成引用，用于提取商品 ID）
- `references/30_product_image.md` — 商品图片查询（被图片优化、抠图引用）
- `references/40_image_edit.md` — 图片编辑/异步提交+查询（被图片优化引用）

**加载示意：**

```
用户说"优化主图"
  → 加载 references/80_image_optimize.md（图片优化）
    → 用户提供了商品ID？加载 references/30_product_image.md（商品图片查询）
    → 加载 references/40_image_edit.md（图片编辑）

用户说"抠图"
  → 加载 references/50_cutout_image.md（抠图）
    → 用户提供了商品ID？加载 references/30_product_image.md（商品图片查询）

用户说"优化标题"
  → 加载 references/60_title_optimize.md（标题优化）
    → 加载 references/20_product_info.md（提取商品 ID）

用户说"生成卖点"
  → 加载 references/70_selling_point.md（卖点生成）
    → 加载 references/20_product_info.md（提取商品 ID）
```

## 抠图优先原则

当用户意图明确为"抠图"、"生成白底图"、"去背景"时，**必须优先使用抠图子 skill**（`references/50_cutout_image.md`），不要走图片优化流程（`references/80_image_optimize.md`）。

## 命令速查

### Capabilities 命令| 命令 | 说明 | 对应子 skill |
|------|------|-------------|
| `configure` | 配置/查看 AK | `references/10_ak_configure.md` |
| `image_info` | 获取商品主图 | `references/30_product_image.md` |
| `image_optimize` | 图片优化（AI 生图） | `references/40_image_edit.md` |
| `cutout_image` | 扣图（生成白底图） | `references/50_cutout_image.md` |
| `title_optimize` | 标题优化 | `references/60_title_optimize.md` |
| `selling_point` | 卖点生成 | `references/70_selling_point.md` |

### Biz 域命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `isv_token fetch` | 获取 ISV Token | `cli.py isv_token fetch --app_key=YOUR_KEY` |
| `isv_token status` | 查询 ISV Token 状态 | `cli.py isv_token status --app_key=YOUR_KEY` |

## 子 skill 一览

### 子 skill 一览

| 编号 | 名称 | 文件 | 类型 | 说明 |
|------|------|------|------|------|
| 10 | AK 配置 | `references/10_ak_configure.md` | 基础 | AK 检查与配置 |
| 20 | 商品信息查询 | `references/20_product_info.md` | 原子 | 商品 ID 提取 |
| 30 | 商品图片查询 | `references/30_product_image.md` | 原子 | 通过商品 ID 获取主图 URL |
| 40 | 图片编辑 | `references/40_image_edit.md` | 原子 | AI 图片编辑（异步提交+查询） |
| 50 | 抠图 | `references/50_cutout_image.md` | 原子 | 抠图生成白底图（同步） |
| 60 | 标题优化 | `references/60_title_optimize.md` | 原子 | 生成优化后的商品标题 |
| 70 | 卖点生成 | `references/70_selling_point.md` | 原子 | 生成商品卖点文案 |
| 80 | 图片优化 | `references/80_image_optimize.md` | 组合 | 商品图片查询（30）+ 图片编辑（40） |

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效" 或 "401" | 触发 AK 配置流程（`references/10_ak_configure.md`） |
| "参数缺失" 或 "offer_id" 或 "image_urls" | 提示用户补充必要参数 |
| "轮询超时" | 提示图片生成超时，建议稍后重试 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **只读** | image_info | 直接执行 |
| **只读** | image_optimize / title_optimize / selling_point / cutout_image | 直接执行，不修改原商品数据 |

## 环境变量（.env）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-distribution-material-newton` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录。上报失败静默忽略，不影响主流程。

## 依赖包

```bash
pip install requests
```

## 项目结构

```
1688-distribution-material-newton/
├── SKILL.md                                        # 主控 skill（本文档）
├── cli.py                                          # CLI 统一入口
├── .env                                            # Skill 基础信息
├── examples/                                       # 示例脚本
│   ├── check_env.py                                # 环境检查
│   ├── check_ak_exist.py                           # AK 配置检查
│   └── set_ak.py                                   # AK 配置设置
├── references/                                     # 子 skill
│   ├── 10_ak_configure.md                          # AK 配置
│   ├── 20_product_info.md                          # 商品信息查询
│   ├── 30_product_image.md                         # 商品图片查询
│   ├── 40_image_edit.md                            # 图片编辑（异步提交+查询）
│   ├── 50_cutout_image.md                          # 抠图
│   ├── 60_title_optimize.md                        # 标题优化
│   ├── 70_selling_point.md                         # 卖点生成
│   └── 80_image_optimize.md                        # 图片优化（组合：30 + 40）
├── scripts/
│   ├── _sys/                                       # 系统模块（不修改）
│   │   ├── _auth.py                                # 签名认证
│   │   ├── _const.py                               # 全局常量
│   │   ├── _errors.py                              # 错误类型
│   │   ├── _http.py                                # HTTP 客户端
│   │   ├── _output.py                              # 输出格式化
│   │   └── _skill_discovery.py                     # 技能发现
│   ├── _auth.py / _const.py / _errors.py ...       # 代理层（兼容旧 import）
│   ├── _tracker.py                                 # 埋点上报
│   └── biz/                                        # 业务模块
│       ├── const.py                                # API 路径、BASE_URL 等
│       ├── configure/                              # AK 配置
│       ├── image_info/                             # 获取商品主图
│       ├── image_optimize/                         # 图片优化（含异步轮询）
│       ├── cutout_image/                           # 抠图（同步）
│       ├── title_optimize/                         # 标题优化
│       ├── selling_point/                          # 卖点生成
│       └── isv_token/                              # ISV Token 管理
```

## 语言要求

**本技能的所有输出、提示、消息必须使用中文！**
