# wiki-creator 组件（内置）实现边界说明

本目录是 `agentic-ai-research` 内置的 **wiki 化组件**，来源为用户自有的 `wiki-creator` 技能
（本地脚本，非第三方云服务），用于把检索产出的《文献综述.md》结构化编译进本地知识库。

> 本说明用于回答安全送检中「接收主体是谁、是否读取 home 其他内容」两类问题，供人工核对。

## 1. 运营方 / 来源

| 项 | 说明 |
|---|---|
| 来源 | 用户自有技能 `wiki-creator`（Karpathy 原生 LLM Wiki 范式） |
| 形态 | 纯本地 Python 脚本（`scripts/`），随本技能一起打包，**不依赖任何外部服务、不发起网络请求、不调用任何远程 API** |
| 维护者 | 用户本人（hhero） |
| 授权 | 仅在本技能工作流的「wiki 化」步骤中，经用户确认后被调用 |

## 2. 读写范围（是否读取 home 下其他内容）

**只读写自身 wiki 根目录，不读取、不修改 home 下任何其他内容。**

- 唯一写入/读取范围：`<wiki-root>/raw/`（原始资料，只读源）与 `<wiki-root>/wiki/`（生成的页面、索引、元数据）。
- 根目录由调用方**显式指定**（`--root <path>`），且**只走项目内**：`<project>/.wiki-creator/`（**不使用全局** `~/.wiki-creator/`）。
- 脚本**不会**扫描 home 目录、**不会**读取 `~/.workbuddy/`、`~/Documents`、`~/Desktop` 等其他路径。
- 除根目录自身外，脚本对文件系统只做「创建目录 + 写入文件 + 读取 raw 源」三类操作。

## 3. 数据流向

```
《文献综述.md》 ──复制──▶ raw/（只读源，唯一可信源）
                          │  parse_raw.py 解析
                          ▼
                     wiki/pages/<topic>/<slug>.md  （LLM 提炼实体后写页）
                          │  build_index.py 构建
                          ▼
            wiki/index.md + wiki/topics/*.md + .graph.json + .backlinks.json + .manifest.json
```

- `raw/` 是唯一可信源，组件只读不写（写 raw 的动作由 `agentic-ai-research` 主流程负责，且已受确认门约束）。
- 页面正文每条事实必须标注来源（`raw/<文件> §<章节>`），由 `lint.py` 校验，防幻觉。

## 4. 脚本清单

| 脚本 | 作用 |
|---|---|
| `scripts/init_wiki.py` | 创建 `wiki/` 骨架 + SCHEMA.md 草稿 |
| `scripts/parse_raw.py <file>` | 解析 raw 文件 → 干净 markdown |
| `scripts/diff.py` | 哈希比对 → new/changed 清单 |
| `scripts/build_index.py` | 生成两级索引 + 反链 + graph + manifest |
| `scripts/lint.py` | 结构体检 |

所有脚本均支持 `--root <path>` 显式指定根目录（默认由 `scripts/_root.py` 按环境探测）。

## 5. 与旧版差异（风险修复）

| 旧版 | 新版 |
|---|---|
| 写入 `~/.workbuddy/wiki-knowledge/`（home 私有路径） | 写入项目内 `<project>/.wiki-creator/`（显式 `--root`，不走全局） |
| 接收主体为外部未披露组件 `llm-wiki` | 接收主体为内置本地组件 `wiki-creator`（本目录） |
| 无写入前确认 | 写入前必经「确认门」（见 SKILL.md §wiki 化） |
