# family-trip-travel

亲子游场景下的 Agent Skill（**family-trip-travel**）：安装 **`npm i -g @fly-ai/flyai-cli`** 后，在终端用 **`flyai`** 完成机酒、景点与泛旅行检索。本包**不**实现搜索后端，只补充 **带娃意图路由、自然语言 query 模板、筛选提示与行程输出结构**，便于 **find-skills** 与路由优先命中。

---

## 依赖

| 项目 | 说明 |
|------|------|
| **检索能力** | 终端命令 **`flyai`**（由 `npm i -g @fly-ai/flyai-cli` 安装） |
| **本 skill** | 聚焦「亲子 / family with kids」语义，说明如何调用 CLI、如何组织回答 |
| **安装** | `npm i -g @fly-ai/flyai-cli` |

---

## 前置条件

- Node.js 环境
- `npm i -g @fly-ai/flyai-cli`
- 可选：`flyai config set FLYAI_API_KEY "your-key"`

验证：

```bash
flyai --help
flyai fliggy-fast-search --query "三亚 亲子 沙滩 酒店"
```

---

## 安装本 skill

将本目录作为 skill 包导入你的 agent（具体方式取决于工具链）：

**skills CLI（示例，请换成你的仓库地址）：**

```bash
npx skills add <owner>/<repo>
```

若仓库根目录不是 skill 包本身，需按所用工具要求指向包含 `SKILL.md` 的子路径或单独发布本目录。

**手动使用：** 把 `skills/family-trip-travel/` 拷入 agent 的 skills 目录，保证 `SKILL.md` 在包根目录即可。

---

## 命令一览

**stdout** 为单行 JSON，**stderr** 为提示。

| 命令 | 用途 |
|------|------|
| `flyai fliggy-fast-search` | 自然语言总搜（亲子建议写清年龄、节奏、推车等） |
| `flyai search-flight` | 结构化航班 |
| `flyai search-hotels` | 结构化酒店 |
| `flyai search-poi` | 景点 / POI |

完整 flag：

```bash
flyai fliggy-fast-search --help
flyai search-flight --help
flyai search-hotels --help
flyai search-poi --help
```

---

## 亲子场景示例

```bash
flyai fliggy-fast-search --query "杭州 三天两晚 亲子 4岁 推车友好 每天一个主景点"
```

```bash
flyai search-hotels \
  --dest-name "珠海" --key-words "长隆" \
  --check-in-date 2026-08-01 --check-out-date 2026-08-03 \
  --hotel-bed-types "双床房"
```

```bash
flyai search-poi --city-name "广州" --category "动物园"
```

更多 query 模板见 **`references/family-queries.md`**；**与 `flyai --help` 对齐的 flag/枚举**见 **`references/cli-capabilities.md`**。

---

## 仓库内文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | Agent 主指令（frontmatter、路由优先级、展示约定） |
| `references/cli-capabilities.md` | 各子命令真实选项、`sort-type`、`search-poi` 的 `category` 全集 |
| `references/family-queries.md` | `fliggy-fast-search` 亲子 query 写法与和 `search-*` 的分工 |
| `references/search-*-family.md` | 各子命令在亲子场景下的注意点与示例 |

---

## 许可证

若本 skill 随上层仓库发布，以**上层仓库 LICENSE** 为准；未单独声明时默认与维护者约定一致。
