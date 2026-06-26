# 01 资源检索与搜索

用于公开资源的检索、列表、详情查询，以及候选搜索与推荐。

## 适用范围

- 模型社区、官方模型、工作流、AI 应用
- 作品、MCP
- modelzoo 列表、详情、价格（详见 04-modelzoo-tasks.md）

## 常用查询入口

### 全局多类型搜索

```bash
python3 scripts/cli.py search "<关键词>" --remote
```

### 社区列表

```bash
python3 scripts/cli.py browse --remote-source community --modality Application --sort "Most Used"
```

### 官方列表

```bash
python3 scripts/cli.py browse --remote-source official --sort Auto
```

### 资源详情（按类型分流）

```bash
python3 scripts/cli.py info <链接或ID>
```

内部自动按类型路由：
- **Application** → 查 webapp 接口（返回 `web_app_id` + `input_nodes`）
- **Workflow / Official** → 查 detail 接口（返回 `versions[]`，无 input_nodes）
- **comfy-ui 链接** → 提示用户不支持运行，引导找 AI 应用链接

判断依据：列表每条都带 `model_type` 字段。

## 固定模型菜单

图片 7 项（5 精选模型 + 1 ModelZoo 搜索 + 1 AI 应用检索）/ 视频 7 项同结构的固定菜单路由定义在 `config/routes.json`。

触发：
```bash
python3 scripts/cli.py image-menu
python3 scripts/cli.py video-menu
```

菜单文案在 `config/menus.json`，agent 必须实际调脚本输出菜单，不能凭记忆合成。

路由规则：
- 1-5（图片）/ v1-v5（视频）：固定模型，给参数卡后执行
- 6（图片）/ v6（视频）：ModelZoo 搜索入口（详见 04）
- 7（图片）/ v7（视频）：AI 应用检索入口（本份文档下方「候选搜索」章节）

## 候选搜索

```bash
python3 scripts/cli.py pick-image "<短词1, 短词2, 短词3, 短词4, 短词5>" --remote --reply-format json
python3 scripts/cli.py pick-video "<短词1, 短词2, 短词3, 短词4, 短词5>" --remote --reply-format json
```

### 搜索词规则

- 中文优先，英文技术词作补充
- 单次最多 5 个短词，脚本按顺序逐个检索
- 复合词（如 ChatGPT Image2）必须同时给短子词（image2, gpt image, openai）
- 搜索词越简单越好，由窄到宽降维

### 结果清洗

- 不再做客户端模态过滤（旧版 `is_remote_image_candidate` / `is_remote_video_candidate` 已删）。AI 应用没有权威模态字段，启发式准确率低。
- picker 一次性返回服务端 Most Used 排序的候选，**不截断**。
- LLM 看 `name` / `base_model` 自己判断模态匹配度，不匹配的放到列表末尾或省略。
- 默认 limit=10，最多 30。
- 服务端 0 命中时自动用 `derive_subword_variants` 拆词重试一轮。

### 输出格式

脚本返回 `reply_markdown` 字段，agent **必须 100% 原样转发**，不要重写或合并。

每个候选 6 项信息：标题 / 最适合做什么 / 封面图 / 能否直接执行 / 链接 / ID。
