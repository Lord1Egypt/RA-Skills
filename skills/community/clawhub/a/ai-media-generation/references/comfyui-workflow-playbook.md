# ComfyUI 工作流 Playbook

> 本 Playbook 解决「怎么搭、怎么改、怎么验」ComfyUI 工作流的问题，是子技能 `image-generation` / `video-generation` 落地时的执行底座。
> 增量信息：部署决策树 + workflow JSON 结构解剖 + 命令 + 踩坑表 + 验收清单（不重复子技能的 prompt 方法论）。

## 1. 部署形态决策树

```
要生成媒体（图/视频）？
├─ 需求频率低、不想装环境
│   └─ 用云端 ComfyUI（RunComfy / ComfyDeploy / 各类 MaaS 网关）
│       → 只需拿到 API/工作流模板，走 skills/* 子技能的云端路径
├─ 需求频率高、有本地 GPU（或 Mac 统一内存）
│   ├─ 装 ComfyUI 桌面版（官方一体包）→ 本 Playbook 第 2 节
│   └─ 要批量/自动化/CI
│       ├─ 用 ComfyUI API 模式（--listen 启动 + /prompt 接口）→ 第 4 节
│       └─ 只是本地手动拖图 → 用可视化界面即可，不需要 API
└─ 完全不想碰 ComfyUI
    └─ 直接走厂商 API 技能（Veo / MiniMax / LTX 等）→ 见 video-generation-playbook
```

**选型原则**：本地 ComfyUI 的价值在**免费 + 离线 + 可控**，代价是环境维护。Mac 无 NVIDIA GPU 时优先选 Apple Silicon 原生版（MPS），性能可接受但慢于同价位 PC；纯 API 路线最省事但按量付费。

## 2. 本地安装（macOS / Linux 通用）

```bash
# 方式一：官方桌面版一体包（推荐新手）
#   下载 ComfyUI 桌面版 → 安装后首次启动自动拉依赖
# 方式二：源码 + venv（推荐开发者，可控性最高）
git clone https://github.com/Comfy-Org/ComfyUI.git comfyui
cd comfyui
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Apple Silicon 加装 MPS 支持（已含在 requirements；确认 torch 可用）
python -c "import torch; print(torch.backends.mps.is_available())"
# 启动（可视化 + API 双开）
python main.py --listen 0.0.0.0 --port 8188
```

模型目录约定（ComfyUI 按路径自动识别）：

```bash
# SD 系大模型 checkpoint（Stable Diffusion / SDXL / FLUX 等）
models/checkpoints/
# 文本编码器（FLUX 的 clip_l / t5xxl 等）
models/text_encoders/
# VAE（SDXL 的 sdxl_vae 等）
models/vae/
# ControlNet / LoRA / Embedding
models/controlnet/  models/loras/  models/embeddings/
# 视频模型（AnimateDiff / LTX 等）
models/checkpoints/ 或 models/diffusion_models/
```

**踩坑 1**：`pip install -r requirements.txt` 后 `import torch` 报 CUDA 错误是正常现象——无 NVIDIA GPU 的机器应确认 `mps.is_available()` 为 True（Apple Silicon）或 `cpu` 兜底，不要因为 CUDA 报错就以为装坏了。
**踩坑 2**：模型文件动辄 5–13GB，放错目录 ComfyUI 不报错但列表里看不到。模型放好后需刷新节点列表（Web 界面点刷新按钮或重启服务）。

## 3. workflow JSON 结构解剖

ComfyUI 的工作流可导出为 `.json`，核心是两个数组，**所有节点操作都围绕它俩**：

```json
{
  "nodes": [
    {
      "id": 4,
      "type": "CheckpointLoaderSimple",
      "inputs": [ { "name": "ckpt_name", "value": "sdxl_base.safetensors" } ],
      "widgets_values": ["sdxl_base.safetensors"]
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "inputs": [ { "name": "clip", "link": 4, "slot": 1 } ]
    }
  ],
  "links": [
    [0, 4, 0, 6, 0, "MODEL"],   // [link_id, 源节点id, 源slot, 目标节点id, 目标slot, 类型]
    [1, 4, 1, 6, 0, "CLIP"]
  ]
}
```

**解剖要点**（也是 [scripts/workflow_validator.py](../scripts/workflow_validator.py) 的校验逻辑）：

| 字段 | 含义 | 常见错误 |
|------|------|----------|
| `nodes[].id` | 节点唯一编号 | 重复 id、缺 id |
| `nodes[].type` | 节点类型（类名） | 拼错 → 加载时节点变红 |
| `nodes[].inputs[].link` | 该输入连接的 link id（-1 表示手动填值） | 指向不存在的 link |
| `links[][1]` / `links[][3]` | 源/目标节点 id | 引用不存在的节点 id |
| `links[][4]` | 目标 slot（节点的第几个输入） | 越界 |
| `links[][5]` | 连接类型（MODEL/CLIP/LATENT/VAE/IMAGE 等） | 类型不匹配 → 运行时红节点 |

## 4. API 模式：批量/自动化调用

ComfyUI 启动时加 `--listen` 即开 API。提交工作流的正确姿势（**必须先 /queue，不能直接 POST 整个 JSON**）：

```bash
# 1. 把 workflow JSON 转成 API 格式（对象以 class_type 为键、去掉位置信息）
python3 - <<'PY'
import json
wf = json.load(open('workflow.json'))
api = {}
for n in wf['nodes']:
    node = {"class_type": n["type"], "inputs": {}}
    for i in n["inputs"]:
        node["inputs"][i["name"]] = i.get("value", i.get("link", -1))
    api[n["id"]] = node
json.dump(api, open('api_format.json', 'w'), ensure_ascii=False, indent=2)
PY

# 2. 提交队列
curl -s http://127.0.0.1:8188/prompt -d @api_format.json \
  -H 'Content-Type: application/json'

# 3. 轮询历史（返回的 prompt_id 取 output 的 images）
curl -s http://127.0.0.1:8188/history/<prompt_id>
```

**踩坑 3**：`/prompt` 接口只接受 API 格式（class_type 键），直接丢 Web 导出的 workflow JSON 会 400。上面第 1 步的转换是必须的，别省。
**踩坑 4**：默认 `--port 8188`；Mac 上 8188 被占时用 `--port 8288`，端口改了所有 API 脚本里的 URL 要跟着改。

## 5. 常见踩坑表

| 现象 | 根因 | 处置 |
|------|------|------|
| 节点变红 "ValueError: ..." | 上游输出类型与下游输入不匹配（如 IMAGE 接了 LATENT） | 查 links[][5] 类型链；中间补 VAE Encode/Decode 节点 |
| 生成全黑/全噪点 | checkpoint 与 VAE 不配套（SDXL 模型 + SD1.5 VAE） | 换配套 VAE 或删 VAE 节点让模型默认解码 |
| 出图尺寸/比例不对 | 没接 Empty Latent 或宽高设错 | KSampler 上游必须有 EmptyLatentImage（或 LatentFromBatch） |
| 加载工作流缺自定义节点 | 用了 ControlNet/AnimateDiff 等扩展，未安装 | ComfyUI-Manager 一键装缺节点；装完重启 |
| 批量任务一半失败 | 单张 prompt 超时 / OOM | 拆小批；`--max-memory` 调显存上限；GPU 加 `--lowvram` |

## 6. 验收清单（提交工作流前逐条过）

- [ ] `workflow_validator.py --strict` 退出 0（节点图完整、link 无悬空）
- [ ] 每个节点 type 拼写正确，界面加载无红节点
- [ ] MODEL → CLIP → LATENT → KSampler → VAE → Save 链路类型匹配
- [ ] 宽高、步数、CFG、seed 是显式值（不是 -1 随机依赖）
- [ ] 出图人工抽查 2 张，确认非黑/噪/灰
- [ ] 若走 API：`/queue` 提交成功、`/history` 能取到 output 图片
- [ ] 模型文件名与实际放置目录一致（checkpoints/loras/embeddings）

## 7. 相关子技能与层次边界（L2→L3）

本篇是 **基建层（L2）**：只负责「ComfyUI 怎么装、workflow JSON 怎么读写、API 怎么批量调」。
具体某个媒体能力怎么落地，交给下列 L3 子技能，不在本篇重复：

| 落地能力 | 子技能 | 本篇为它提供什么 |
|----------|--------|------------------|
| 文生图 / 图生图 | [skills/image-generation/SKILL.md](../skills/image-generation/SKILL.md) | 本地节点图跑通、seed/尺寸显式化、`/queue` 批量提交 |
| 局部重绘 / 扩图 / ControlNet | [skills/image-editing/SKILL.md](../skills/image-editing/SKILL.md) | inpaint/ControlNet 节点接线与模型放置目录 |
| 文生视频 / 图生视频（本地路线） | [skills/video-generation/SKILL.md](../skills/video-generation/SKILL.md) | AnimateDiff / LTX-Video 节点的部署与显存前提 |
| 片段拼接 / 转码 | [skills/video-editing/SKILL.md](../skills/video-editing/SKILL.md) | 生成端产物规格（命名、格式）约定 |

**边界声明**：本篇不写 prompt 写法与参数取值（见 [references/image-generation-playbook.md](image-generation-playbook.md)、
[references/video-generation-playbook.md](video-generation-playbook.md)），也不替代子技能的操作步骤；节点图坏没坏由
[scripts/workflow_validator.py](../scripts/workflow_validator.py) 判定，不靠目检。
