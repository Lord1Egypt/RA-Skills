# 查询语法与输出字段

所有子命令都支持：`--project-dir`、`--format text|json|md`、`--out`。
除 `diff`、`devices`、`doctor` 外都支持 `--svd`、`--chip`、`--demo`（`diff` 用 `--svd-a/--chip-a`、`--svd-b/--chip-b`）。

`--demo` 使用内置合成芯片（ETK-DEMO，不是真实数据），用于零配置试用；与 `--svd` 同时给出会报 `E_INPUT_INVALID`。
`--format md` 输出 Markdown（表格与代码块），适合粘贴到文档、PR 或聊天；错误与警告以列表给出。

## 查询路径

```
外设.寄存器.位域
外设->寄存器            （与点号等价）
外设.簇.寄存器           （簇内寄存器，例如 DMA1.CH1.CCR）
裸寄存器名              （AVR/MSP430 风格：UCSR0B、P1OUT——整颗芯片唯一时自动定位外设）
裸寄存器名.位域         （UCSR0B.UDRIE0）
```

- 大小写不敏感：`usart1.cr1.ue` 与 `USART1.CR1.UE` 相同。
- 寄存器名和位域名相同时（如 `TIM1.CNT`），两层都存在时优先按寄存器解析；要查位域请写全 `TIM1.CNT.CNT`。
- 只写到外设（`USART1`）返回全部寄存器；只写到簇（`DMA1.CH1`）返回簇内寄存器。
- 裸寄存器名在多个外设中重名时（如 `SR`），会报错并列出候选（`USART1.SR、USART2.SR`），
  用 `外设.寄存器` 指定即可；名字与某个外设同名时（如 AVR 的 `PORTB`）优先按外设解析。

## 子命令

| 子命令 | 作用 | 示例 |
|---|---|---|
| `lookup <路径>...` | 查外设、寄存器、位域（可给多个） | `lookup USART1.CR1.UE USART1.BRR` |
| `addr <地址>` | 地址反查 | `addr 0x4001380C` |
| `search <关键词>` | 按名称或描述搜索；`--kind` 限定层级；`--peripheral` 限定外设；`--limit` 控制条数 | `search baud --peripheral USART1` |
| `irq [关键词或编号]` | 中断号查询（含 NVIC 使能/清挂起位，SVD 有 NVIC 数据时）；不给参数列出全部 | `irq USART1`、`irq 37` |
| `decode <寄存器> <值>...` | 按位域解码寄存器值，可给多个值；`--write` 给写入视角提示 | `decode RCC.CR 0x00040002 --write` |
| `fields <寄存器>...` | 位域速查表：位范围、宽度、掩码、访问、复位、未定义位 | `fields TIM1.CR1` |
| `diagram <寄存器>...` | 寄存器位图（符号图 + 图例 + 复位位） | `diagram TIM1.CR1` |
| `set <寄存器> <字段=值>...` | 按位域赋值计算写入值；值可为数字或枚举名；`--from reset\|数字` | `set TIM1.CR1 CEN=1 DIR=UP` |
| `macros <路径>` | 生成 CMSIS 风格参考宏（`_OFFSET`/`_ADDR`/`_Pos`/`_Msk`/枚举值） | `macros USART1.CR1` |
| `diff <寄存器或外设>...` | 对比两份 SVD：`外设.寄存器` 全字段对比；只给外设名做整体对比（`--all` 显示全部寄存器） | `diff USART1 --chip-a STM32F103C8 --chip-b STM32G431` |
| `range <起始> <结束>` | 列出地址区间内的寄存器；`--limit` | `range 0x40013800 0x40013FFF` |
| `lint` | SVD 质量检查：重叠、越界、重复名、复位值超宽、中断号冲突；`--peripheral`、`--limit` | `lint --peripheral TIM1` |
| `info` | SVD 元信息：厂商、CPU、统计、文件大小/SHA-256/修改时间 | `info` |
| `list` | 列出全部外设、基地址、派生关系 | `list` |
| `devices` | 本机可用 SVD 清单（项目扫描 + ETK_SVD_DIR + Pack 缓存）；`--filter`、`--limit` | `devices --filter STM32F4` |
| `doctor` | 环境体检：Python 版本、各 SVD 来源是否存在与数量、上手建议 | `doctor` |

- `lookup`、`fields`、`diagram`、`diff` 支持多个路径/寄存器：逐条独立判定，某个失败不影响其它（失败的进 `errors`，其余进 `results`，`ok` 为 `false`）。
- `decode` 的参数必须是寄存器，给位域会返回 `E_INPUT_INVALID`；多个值会输出多条结果。
- `set` 的位域不存在时返回 `E_FIELD_NOT_FOUND`（含拼写建议）；值超宽或无法解析返回 `E_INPUT_INVALID`。
- `range` 判定标准：寄存器**起始地址**落在 `[起始, 结束]` 内（闭区间）。
- `diff` 输出中没有顶层 `source`（外设整体对比是两个 `a`/`b` 对象）；寄存器对比的两侧出处分别在 `a.source`、`b.source`。
- `macros` 的宏名含外设实例名（`USART1_CR1_Pos` 风格）；含任意位的枚举（如 `1xx`）只出注释、不生成宏。
- `lint` 三级：`error`（**部分**重叠、越界、重复名、复位值超宽）、`warning`（同一中断名向量号冲突）、
  `info`（常见合法写法：同一偏移的寄存器别名、**包含关系**的多宽度视图 `register_view`、
  包含关系的位域别名 `field_alias`）。

## 解析缓存与环境变量

- 解析结果默认缓存在本机（Windows：`%LOCALAPPDATA%\etk\cache`，其他：`~/.cache/etk`），
  按 SVD 文件路径 + 字节数 + 修改时间自动失效；任何缓存故障都会静默降级为直接解析。
- `ETK_NO_CACHE=1` 关闭缓存；`ETK_CACHE_DIR` 自定义缓存目录；`ETK_SVD_DIR` 追加自备 SVD 目录；
  `ETK_PACKS_DIR` 覆盖 Pack 缓存目录（测试用）。`doctor` 会显示缓存目录与条目数。

## 地址反查的四种结果

| `kind` | 含义 |
|---|---|
| `exact` | 地址正好是一个或多个寄存器的起始地址（别名时可能有多个） |
| `inside_register` | 地址落在某寄存器内部，`offset_in_register` 为字节偏移 |
| `gap` | 在某外设范围内，但前面最近的寄存器之后没有定义寄存器（多为保留区） |
| `unmapped` | 不在任何外设地址范围内 |

## JSON 信封

```json
{
  "ok": true,
  "tool": "embedded-register-lookup",
  "version": "1.3.0",
  "results": [ { "kind": "...", "label": "已核验", "source": { ... } } ],
  "warnings": [],
  "errors": []
}
```

失败时 `ok` 为 `false`，`errors[0]` 含 `code`、`message`、`hint`，部分错误还有 `details`：

| 错误码 | `details` 字段 |
|---|---|
| `E_SVD_NOT_FOUND` | `tried`：已尝试的位置列表 |
| `E_SVD_PARSE` | `line`、`column` |
| `E_PERIPH_NOT_FOUND`、`E_REG_NOT_FOUND`、`E_FIELD_NOT_FOUND` | `suggestions`：最接近的候选名 |
| `E_INPUT_INVALID` | 无 |
| `E_INTERNAL` | 无（请附上输出提交 issue） |

## 各结果对象的字段

`register` 对象：`name`、`offset`、`address`、`size`、`access`、`reset`、`reset_mask`、`description`，
以及写读语义：`modified_write_values`（SVD 原值）、`write_semantics`（中文提示）、`read_action`、`read_semantics`。

`fields` 数组每项：`name`、`bits`（单比特写作 `5`，多比特写作 `15:0`）、`lsb`、`msb`、`width`、
`mask`（该位域在寄存器中的完整掩码，按寄存器位宽格式化）、`access`、`reset`（十进制）、`description`、
`modified_write_values`/`write_semantics`/`read_action`/`read_semantics`、`enums`。

`enums` 每项：`name`、`value`、`pattern`（二进制图样，`x` 表示任意值）、`description`。

### 新增子命令的结果要点

| `kind` | 关键字段 |
|---|---|
| `fields` | `fields`（含 `mask`）、`undefined_bits`（未被任何位域覆盖的位号数组） |
| `diagram` | `cells`（按位升序，含 `bit`/`char`/`field`）、`legend`（符号到字段）、`reset_bits`（复位为 1 的位号） |
| `set` | `from`（基准：`label`/`value`/`value_hex`）、`value`/`value_hex`、`assignments`（每项含 `field`/`given`/`before`/`value`/`changed`/`via_enum`）、`undefined_bits_set`、`notes` |
| `diff` | `a`/`b`（各含 `peripheral`/`base_address`/`register`/`source`）、`register_differences`、`fields`（每项 `status`：`same`/`diff`/`only_a`/`only_b`，`differences` 为文字说明数组）、`identical` |
| `diff_peripheral` | `path`、`a`/`b`（各含 `name`/`base_address`/`register_count`/`source`）、`base_address_changed`、`counts`（`total`/`same`/`diff`/`only_a`/`only_b`）、`registers`（每项 `status` 与 `register_differences`/`fields_changed`/`fields_same`/`fields_only_a`/`fields_only_b`）、`show_all`（命令行 `--all`）、`identical` |
| `range` | `start`/`end`、`count`、`truncated`、`registers`（`path`/`address`/`size`/`access`/`reset`/`description`） |
| `irq` | `query`、`total`、`truncated`、`matches`（`value`/`peripheral`/`name`/`description`/`nvic`；`nvic` 为 `{enable, clear_pending}` 或 `null`，各含 `register`/`bit`/`address`，按中断号排序） |
| `macros` | `path`、`registers`（每项含 `offset`/`address`/`macros`/`fields`）、`code`（完整的 C 文本，带出处头注释） |
| `lint` | `scope`、`counts`（`error`/`warning`/`info`/`total`）、`findings`（每项 `severity`/`code`/`peripheral`/`register`/`field`/`message`） |
| `info` | `device`/`vendor`/`cpu`/`description`、`file_size`/`mtime`/`sha256`、`counts`（各层级数量、中断数与警告数） |
| `devices` | `keyword`、`total`、`truncated`、`entries`（`file`/`path`/`device`/`source`）、`sources`（各来源数量） |
| `doctor` | `python`/`platform`、`checks`（`name`/`path`/`exists`/`count`/`note`）、`total_svds`、`advice` |

其他要点：

- 外设结果（`kind=peripheral`）含 `interrupts` 数组（`name`/`value`/`description`）。
- `decode` 结果含 `write_notes`：没加 `--write` 时为空数组；加了则给出只读位域、未定义位、写读语义与读-改-写陷阱提示。
- `set` 结果的 `notes` 也会包含读-改-写陷阱提示（寄存器含 `oneToClear` 等写语义时）。
- `search` 结果含 `peripheral`（限定外设时非 null）。
- `macros` 的 `code` 可直接复制；`fields[].macros` 给出宏名（`pos`/`msk`）。

## 证据标签

| 标签 | 本技能何时输出 |
|---|---|
| 已核验 | 结果直接来自 SVD |
| 需查手册、需实测、未判定 | 本技能不输出（解码的未定义位用 `undefined_bits` 字段表示，不打标签） |
