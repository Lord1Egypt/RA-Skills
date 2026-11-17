# 工作流文档规范：操作指南 + 进度笔记

> 目的：这类任务周期长（几百张卡片、跨天跨周），期间**会话记忆会被压缩、可能换设备、
> 可能换执行者**。只要这两份文档落在持久化目录，任何人读一遍就能接着干。

## 〇、放哪里：任务数据与文档一律落在**持久化目录**，不留在易失层

| 模式 | 数据 + 文档位置 | 由谁生成 |
|---|---|---|
| A 书籍 / B 网站 | `books/<slug>/`（其下 `docs/guide.md` + `docs/progress.md`） | `book_setup.py` / `docs_layer.py` |
| **C 资料拆卡** | `<工作目录>/<任务名>/`（其下 `GUIDE.md` + `PROGRESS.md`） | `tile_setup.py init` |

**为什么不能留在易失层**：会话记忆会被压缩、容器/沙箱会被重置、也可能换设备换执行者。
只要数据与文档落在**持久化目录**，读 `GUIDE.md`（或 `docs/guide.md`）就能恢复全部上下文。

- **模式 C**：任务文件夹本来就建在**工作目录**下，天然持久。
- **模式 A/B**：默认数据根是 `<skill目录>/books/`。如果本平台的 skill 目录**不是持久层**
  （例如容器/沙箱里 `/root`、`~/.<agent>/skills` 会被重置），**务必设置环境变量 `B2L_DATA_DIR`
  指向工作目录**，例如：
  ```bash
  export B2L_DATA_DIR="$PWD/b2l-data"     # 之后 book_setup.py / push_card.py / docs_layer.py 都会用它
  ```
  （`book_setup.py`、`push_card.py`、`docs_layer.py`、`fetch_site.py`、`validate.py` 统一读取该变量。）
- 平台侧文档（如 IMA 笔记）只能是**可选镜像**。

> 拆卡模式的 `GUIDE.md` 由 `tile_setup.py init` 生成，**已内嵌**该工作流的全部规则、
> 强制门禁、渲染规则、复核方法与 12 条踩坑，读它即可接手，无需回查聊天记录。

## 一、本地文件为底，平台是可选镜像

| 层 | 位置 | 说明 |
|---|---|---|
| **操作指南** | `books/<slug>/docs/guide.md`（模式 C：`<任务目录>/GUIDE.md`） | 任务全景、规则、SOP、渠道、注意事项 |
| **进度笔记** | `books/<slug>/docs/progress.md`（模式 C：`<任务目录>/PROGRESS.md`） | 全量清单 + 更新记录（只增不删） |
| 可选镜像 | IMA / 其他知识库的笔记 | `config.notes.channel = ima|both` 且环境有凭据时才同步 |

**为什么本地为底**：不依赖任何平台、任何环境都能读；平台侧一旦没有删除/编辑接口，
反而会把唯一的进度记录锁死在一个地方。

```bash
python docs_layer.py init    --slug mydocs --title "OpenClaw 官方文档"
python docs_layer.py refresh --slug mydocs          # 按 config/catalog 刷新
python docs_layer.py log     --slug mydocs --entry "2026-10-05更新：9，已推送，序号OC009。"
python docs_layer.py status  --slug mydocs
python docs_layer.py mirror  --slug mydocs          # 可选：同步到 IMA 笔记
```

模式 C（资料拆卡，文档就在任务目录里）：
```bash
python tile_setup.py init     --dir "<工作目录>/<任务名>" --title "…" --source "…" --count 47
python tile_setup.py export-md --dir "<工作目录>/<任务名>"
python tile_setup.py log      --dir "<工作目录>/<任务名>" --entry "已出图 47 张。"
python tile_setup.py status   --dir "<工作目录>/<任务名>"
```

## 二、操作指南写什么（`guide.md`）

必备九块：一句话任务 / 范围与总数 / 工作目录 / **进度查看位置** / 命名与编号规则 /
推送 SOP / 渠道与目标 / 渲染规则 / 注意事项 + 变更记录。
其中三条最容易被忽略但最重要：

1. **进度看哪里**：明确「以进度笔记底部『更新记录』最新一段为准」；
2. **命名与编号**：写明双轨（文件名=推送序号；卡片标记与笔记=清单绝对序号）；
3. **变更记录**：每次环境/规则变化都追加一段（例如「渲染器支持 MDX 清理了」），
   否则下一个人会按旧规则踩坑。

## 三、进度笔记写什么（`progress.md`）

```
# 【<名称>·学习卡片·进度】
> 进度以最底部「更新记录」最新一段为准
> 全量清单共 **N** 张（开始=17 ｜ 智能体=54 ｜ 能力=216）
## 一、全量清单
| 一级类目 | 项目 | 链接 | 录入序号 |
## 二、更新记录（只增不删，最新在最底部）
2026-10-05更新：9，已推送，序号OC009。
```

约定：
- **更新记录只增不删**，最新在最底部；整体进度以最后一段为准。
- 每次推送**成功后**追加一行（失败不写）。
- 「录入序号」列可选维护；若选择不维护，就在指南里写清楚「仅以更新记录为准」，
  避免下一个人以为漏填。

## 四、每一轮开工的固定动作

1. 读 `GUIDE.md`（模式 C）或 `docs/guide.md`（模式 A/B）（恢复规则）；
2. `push_card.py status` / `tile_setup.py status`（定位进度）；
3. 模式 A/B：列「接下来 N 张」（`push_card.py list-next --n 10`）给用户，确认是否跳过；
   模式 C：确认当前落在五道门禁的哪一步（未过门禁不得批量出图）；
4. 再开始干活。

> 第 3 步不是可选项：用户需要靠这份预览决定「哪几张跳过」，跳过会占用清单编号；
> 拆卡模式则需要靠它确认「样式/文本是否已确认」，避免返工。

## 五、会话记忆被压缩后如何恢复

- 模式 A/B：`docs/guide.md` → `docs/progress.md` 底部 → `progress.json` → `README`/`references/`。
- 模式 C：`<任务目录>/GUIDE.md` → `PROGRESS.md` 底部 → `cards.json`（+ `out/_check.json` 看 k 与校验）→ `references/`。

读书面完成即可继续，**不需要回溯聊天记录**。
