# 工具编码

本文件规定检查器与关系图工具接受的 Markdown 编码。概念与同步的编写标准见[规格记法](spec-notation.md)。`coverage`、章节名与记录语法是工具字段。

## CONCEPT

工具输入的四个核心节 MUST 按以下顺序出现：`purpose`、`state`、`actions`、`operational principle`。
每节 MUST 有声明内容。
可选 `queries` 放在运作原理后，再接按需填写的执行约束节。
`coverage: complete|partial` 是本地元数据，用于声明规格覆盖范围。

```markdown
# concept Name [T]
coverage: partial

## purpose
<一个可评价的需要>

## state
items: set Item
owner: Item -> T
<局部类型、基数、初态、不变量>

## actions
act [item: Item; owner: T] => [item: Item]
  requires <成功条件>
  ensures <效果、输出、不变状态>
act [item: Item; owner: T] => [error: E]
  requires <拒绝条件>
  ensures <错误含义与状态后果>

## operational principle
after <已声明动作及结果>
then <兑现目的的后续动作或观察>
```

动作输入输出须具名；无输入用 `[]`，无返回用 `=> []`。
有相关要求时再补充[执行约束](execution.md#执行约束)。

可选 `## queries` 将公开关系映射为查询 API：

```markdown
## queries
_owners [item: Item] => [owner: T]
  returns 匹配的 owner 绑定；无匹配为零行
```

声明查询签名、基数与对应关系。
SYNCS 中的 `Name/_query: [输入] => [输出]` 只能用于 `where`。

## SYNCS

include MUST 指向概念或外部入口契约。
声明别名、具体类型及请求、定时、消息的根动作签名。
生成图前，按[图契约](diagram-contract.md#身份与解析)核对支持的 include。

`sync` 前 MAY 紧邻添加 `### <业务说明>`。

```markdown
# app AppName
include Source [Id]
include Target [Id]

### 传递完成结果
sync Transfer
when { Source/finish: [] => [item: ?item] }
where { Source: { ?item owner: ?owner } }
then { Target/accept: [item: ?item; owner: ?owner] }
```

| 部分 | 约束 |
| --- | --- |
| `sync` | 一个决定对应一个稳定、应用内唯一的名称。 |
| `when` | 必需且非空。全部完成模式 MUST 在同一运行时 flow 中匹配。 |
| 模式 | 省略字段为通配，`[]` 不代表成功。分支影响后续效果时 MUST 区分。 |
| `where` | 可选。读取、过滤、计算、绑定行；省略时保留输入绑定。 |
| `then` | 必需且非空。MUST 逐行调用，填全所需具名输入，不写输出。 |
| `?name` | 同一绑定行内，同名变量同值；调用只用常量或已绑定值。 |

[多场景同步示例](spec-examples.md#同步场景)。

## concept-lint

```sh
python3 <技能目录>/scripts/concept_lint.py CONCEPT.md SYNCS.md --json
```

CLI 只读，只用标准库。

- 检查声明、coverage、核心节唯一性与非空、规则块及括号。
- 对已闭合的 `when`/`then` 块，检查顶层输入输出字段具名、有值且不重名；`when` 须含输出，`then` 不含输出。
- 跨文件检查同一应用的规则重名；不同应用可复用名称。
- 忽略注释、字符串内容和围栏说明，保留诊断行号。
- 不检查嵌套值、`where`、include、签名、类型、绑定或执行策略。未知调用（含花括号内的旧点式调用）返回 `not_checked`。

| 退出码 | 状态 | 含义 |
| --- | --- | --- |
| 0 | `format_checked` | 全部输入通过所列结构检查。 |
| 1 | `format_error` | 至少一个已确定的结构错误。 |
| 2 | `read_error` | 用法、文件访问或编码错误。 |
| 3 | `not_checked` | 旧方言、未知或未闭合记法，或缺 coverage。 |

读取错误优先于格式错误；格式错误优先于未检查部分。
未闭合注释、字符串或围栏遮住的内容，不推断为缺失章节。
已完整闭合的节或块存在错误时仍报错。
有意不含状态或动作时，明确写出该声明，不留空节。
`format_checked` 不表示语义验证。
