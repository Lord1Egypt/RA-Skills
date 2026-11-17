# 概念与同步关系图，版本 1

## 使用

从本地 CONCEPT/SYNCS 生成含 Mermaid 的 `ARCHITECTURE.md`，输入采用[工具编码](tool-encoding.md)。原生记法不受支持；版本 1 不读取 PIPELINE、PRD 或源码。

```sh
python3 <skill-directory>/scripts/concept_map.py <root> --output <root>/ARCHITECTURE.md
```

报告输出位置、范围、退出状态与缺口。范围选项见下节，写入与检查规则见后文。

## 扫描与范围

扫描根目录下 `**/CONCEPT.md` 与 `**/SYNCS.md`。
排除 `.git`、`node_modules`、`.venv`，不跟随符号链接。
应用可重复的 `--exclude PATTERN`，按相对路径排序。
每次重扫并检查根索引，包括使用 `--scope` 时。
记录根索引来源与排除项，不按时间戳跳过输入。

`--scope RELPATH` 只显示范围内概念定义、规则及其直接实例边界。
根目录索引可解析范围外定义。
这些目标标为 `outside_scope`，不展开其其他规则。
保留范围内未被引用的概念。

## 身份与解析

身份键序列化为紧凑 JSON，使用 `ensure_ascii=False`，再编码为 UTF-8。
`hash12` 为 SHA-256 的前 12 位小写十六进制。

```text
c_<hash12(["concept", relativePath, name])>
i_<hash12(["instance", app, instanceName])>
s_<hash12(["sync", app, ruleName])>
```

`relativePath` 为以 `/` 分隔的根目录相对路径。
哈希冲突、同一 app 的冲突 include 或重名规则属于确定错误。
相同 app 的兼容 include 指向同一实例。
新增其他节点不改变既有 ID；定义路径或声明名变化时允许 ID 改变。

`include Name[T]` 按概念声明名在根索引中匹配。
唯一候选可解析，多候选为 `ambiguous`，无候选为 `missing`。
版本 1 不支持别名或外部根入口。
不支持或未解析的引用 MUST 保留原文并列缺口。
MUST NOT 猜目标或将其改标为外部参与者。

## 规则与边

每条 sync 一个节点。
每个 `when` 模式是一条共同成立的入边。
每个 `then` 调用是一条出边，不隐含顺序。
`where` 读取画虚线入边。

支持的 `where` 形状：

```text
Alias: { ?subject relation: value; ... }
Alias/query: [...] => [...]
bind(...)
```

状态关系和查询记录的顶层字段须具名、有值且不重名。
计算保留原文，不画关系，也不证明绑定正确。
未知状态模式或嵌套命名空间标为 partial，不补造读取边。
其他写法保留原文，结果标为 partial。
重复调用和不同模式角色分别保留原文顺序、原文及来源行号。

## Markdown 与写入

Mermaid 节点按身份键排序，边按规则、`when/where/then` 和原文序号排序。
ID MUST 使用稳定 ASCII；标签加双引号并转义。
输入不变时，生成源码 MUST 字节一致；不写生成时间。

生成区恰用一对标记：

```text
<!-- concept-map:start -->
...
<!-- concept-map:end -->
```

固定英文节名为 `Source status`、`Concept index`、`Synchronization diagram`、`Relations`、`Gaps`，
分别表示来源状态、概念索引、同步图、关系表与缺口。
概念索引保留目的原文、coverage 声明与规格链接。
实例表保留定义引用、类型绑定与 include 来源；规则表保留声明来源。
关系表保留模式角色、顺序、原文与来源行号。
缺口列明未解析或不支持的内容。

无 `--output` 时向 stdout 输出 Markdown。
有 `--output` 时创建新文件，或仅替换其标记区。
保留区外文字，字节相同时不写。
旧文件缺少标记、重复标记或标记不配对时报错。
MUST NOT 覆盖输入规格。
确定错误时不写入。
无规格时保留现有输出。
局部可解析结果仅在明确标为 partial 时写入。
`--check` 须配合 `--output`，只读比较指定输出。

| 退出码 | 含义 |
| --- | --- |
| `0` | 生成或现有输出一致，且无缺口 |
| `1` | 确定的结构/身份错误，或 `--check` 差异 |
| `2` | 用法或 I/O 错误 |
| `3` | 无规格，或结果为 partial |

多条件同时成立时，优先级为 `2 > 1 > 3 > 0`。
本图仅投影本地规格，不报告目的依赖、代码覆盖率或运行正确性。
