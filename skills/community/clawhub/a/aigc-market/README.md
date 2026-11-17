# AI 插件市场 · 全能创作

把 **aigc.a7w.cn** 的 21 个 AI 插件做成一个 Skill：**一个 Key，一次配好，全部能力可用**。

图片、视频、音乐、语音、数字人、口播、换装、超分、剪辑 —— 不用同时开五六个账号、管五六份账单和配额。

---

## 内容

```
aigc-market/
├── SKILL.md                    主入口：市场总览、拿 Key、调用方式、常见坑
├── README.md                   本文件
├── LICENSE.md                  MIT
├── references/
│   ├── catalog.md              21 个插件 / 71 个接口的完整清单（参数 + 计费）
│   ├── 选型指南.md              按任务挑插件：同一个需求有多个方案时怎么选
│   ├── getting-started.md      注册、充值、获取与配置 API Key
│   └── 通用说明.md              权限表、异步机制、错误码、计费口径
└── scripts/
    ├── a7w.py                  零依赖客户端（库 + 命令行，只用 Python 标准库）
    └── market.py               市场浏览器：分组列插件、搜接口、看必填参数
```

---

## 市场里有什么

| 分类 | 插件 | 能做什么 |
|---|---|---|
| **图片** | `nano_banana` | 文生图、图生图、图片编辑 |
| **视频生成** | `full_video` `happy_horse` `grok_video` `wan` `seedance` | 文生视频、图生视频、视频编辑 |
| **数字人与口播** | `image_human` `pic_lipsync` `lipsync` | 全驱动数字人、图片数字人、对口型 |
| **剪辑与特效** | `action_transfer` `person_replacement` `dressing_diffusion` `smart_clip` `flashvsr` | 动作迁移、人物替换、换装、混剪、超分 |
| **音频与音乐** | `voice_tts` `music_generation` `music_search` `mmaudio` `seedsvc` | 语音合成与识别、音乐生成、音效、翻唱 |
| **文档与检索** | `file_qa` | 文档问答与解析 |

---

## 快速开始

```bash
# 1. 配置你自己的 API Key（只需一次）
export A7W_API_KEY=sk-你的key
# 或者：python3 scripts/a7w.py login --key sk-你的key

# 2. 看市场里有哪些插件
python3 scripts/market.py list

# 3. 看某个插件要传什么
python3 scripts/market.py show nano_banana

# 4. 调用（异步任务自动轮询到结束）
python3 scripts/a7w.py call nano_banana submit \
  --body '{"action":"generate","prompt":"一只戴墨镜的柴犬"}'
```

> `--body` 是请求体 JSON。老版本文档里写的是 `--json`，两个都支持。

### 命令行速查

```bash
python3 scripts/a7w.py whoami              # 看这把 Key 能用的插件数
python3 scripts/a7w.py apps                # 列出全部插件（原始分类）
python3 scripts/a7w.py schema <app>        # 看某插件的接口与参数
python3 scripts/a7w.py call <app> <api> --body '{...}'
python3 scripts/a7w.py call <app> <api> --body '{...}' --no-wait   # 只提交
python3 scripts/a7w.py task <task_id>      # 查异步任务
```

---

## 用之前先拿 Key

**不填 Key 跑不起来。** 必须有一个 [api.a7w.cn](https://api.a7w.cn/) 的 API Key。

**第一步 · 注册**：到 https://api.a7w.cn/ 注册 → 控制台创建 Key（形如 `sk-xxx...`）→ 完整复制保存。

**第二步 · 填进你在用的地方**：

| 你在哪用 | 怎么填 |
|---|---|
| **AI 工具 / Agent 平台**（Kimi、扣子等） | 平台的**环境变量 / 凭证 / 插件配置**里加 `A7W_API_KEY=sk-你的key` |
| **本机命令行** | `export A7W_API_KEY=sk-你的key`（Windows 用 `$env:A7W_API_KEY="..."`） |
| **长期本机** | `python3 scripts/a7w.py login --key sk-你的key` |

读取顺序：`--key` → `A7W_API_KEY` → `~/.a7w/config.json`。

---

## 计费

- **按点数计费**，每个插件、每个接口单价都不同（有按次、有按视频秒数、有按 token 量）
- 异步任务**提交时预冻结点数**，完成后按实际结算
- 平台同时给**标准价**和**租户实际结算价**，可能差很多 —— **以实际扣费为准**
- 查询类接口（`query` / `list_*` / `template`）通常免费

完整单价见 `references/catalog.md`。

---

## 这个包不包含什么

- ❌ **不含平台数据抓取类接口** —— 市场里有一个 `watermark_removal`（水印消除），它同时含「去水印」和抖音/小红书数据抓取，涉及《著作权法》与《数据安全法》《个人信息保护法》，属平台红线，本 Skill 不收录
- ❌ **不提供 API Key** —— Key 需要使用者自己在 [api.a7w.cn](https://api.a7w.cn/) 获取
- ❌ **不代付费用** —— 调用消耗的是使用者自己账号的点数
- ❌ **不保证可用性** —— 上游模型服务的可用性与限流以站内为准

---

## 联系

- 技术微信：**9872659**
- AI 插件市场：https://aigc.a7w.cn/
- 算力集市：https://api.a7w.cn/
