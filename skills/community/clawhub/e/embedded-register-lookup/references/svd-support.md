# SVD 支持范围与已知缺口

## 已支持

| 特性 | 说明 |
|---|---|
| `derivedFrom`（外设） | 继承基础外设的全部寄存器，保留自己的基地址和名称 |
| `derivedFrom`（寄存器） | 继承同一外设内兄弟寄存器的位宽、访问属性、复位值和字段 |
| `dim` / `dimIncrement` / `dimIndex` | 外设、簇、寄存器均可展开；`dimIndex` 支持 `0,1,2`、`0-3`、`A-H` |
| `cluster` | 子寄存器名加簇实例前缀，如 `CH1.CCR`，偏移为簇偏移加寄存器偏移 |
| 位域位置 | `bitOffset`+`bitWidth`、`bitRange [msb:lsb]`、`lsb`+`msb` 三种写法 |
| `enumeratedValues` | 支持十进制、`0x` 十六进制、`#` 二进制；`#1XX` 形式的任意位 |
| 属性继承 | 位宽、访问、复位值、复位掩码按 寄存器 → 外设 → 设备 逐级继承 |
| `modifiedWriteValues` / `readAction` | 解析并按位域继承（位域级覆盖寄存器级），输出中文提示（如 写 1 清零、读后清零） |
| `interrupt` | 解析中断条目（名称、向量号、描述）；派生外设未声明时继承基础外设，声明后以自身为准 |
| XML 命名空间 | 带或不带 `xmlns` 都能解析 |
| XML 声明前的空白/BOM | 自动剥离并记录警告（如 GD32F3x0 的 SVD 开头有两个空格）；其余脏数据仍报错 |

## 继承规则要点

- 派生外设中若声明了**同名寄存器**，该寄存器整体替换基础定义，**不会合并字段**，访问属性也不沿用基础寄存器（只沿用外设级默认值）。这与部分厂商工具的行为一致；若结果与手册不符，优先检查派生外设里的同名声明。
- 寄存器的 `derivedFrom` 只在同一外设内查找。跨外设引用会产生警告并忽略继承。
- 派生循环（A 派生自 B，B 派生自 A）会在警告中指出，并在断开处继续解析。

## 已知缺口（会给出警告，不会中断）

| 情况 | 处理 |
|---|---|
| 位域带 `dim` | 暂不展开，按模板名保留（当前无此类真实样本） |
| 簇带 `derivedFrom` | 忽略继承，给出警告 |
| 位域缺少位置信息 | 跳过该位域，给出警告 |
| 数值无法解析（如 `addressOffset="zz"`） | 按 0 处理，给出警告 |
| 外设 `dim` 与 `dimIndex` 个数不一致 | 按 `dimIndex` 展开，给出警告 |

## 查找 SVD 的位置

1. `--svd` 指定的文件
2. 项目根目录 `.etk/config.json`：`{"svd": "相对路径", "chip": "芯片名"}`
3. 项目内扫描：当前目录向下深度 ≤ 6 的 `*.svd`（跳过隐藏目录与 `node_modules`/`AppData` 等；最多 4000 个目录、50 个文件，超限会提示）
4. 环境变量 `ETK_SVD_DIR` 指向的自备 SVD 目录（多个用系统路径分隔符分开）
5. CMSIS-Pack 缓存：`<Packs>/<厂商>/<包名>/<版本>/SVD/*.svd`（也支持 `CMSIS/SVD/` 布局，如 Keil 的 STM32F4xx/G4xx 包）
   - Windows：`%LOCALAPPDATA%\Arm\Packs`
   - `~/.arm/Packs`；Linux 额外看 `~/.cache/arm/packs`；macOS 额外看 `~/Library/Caches/Arm/Packs`
   - 测试或特殊环境可用环境变量 `ETK_PACKS_DIR` 指定目录
6. 芯片名匹配规则：先精确同名，再前缀匹配，最后等长的 `x` 通配（`STM32F407VE` → `STM32F40x.svd`）；若仍找不到，去掉封装后缀再试（`STM32G431RB` → `STM32G431`）。多个候选时选择名称最精确、版本号最高的，并给出提示。
7. 都找不到时用 `doctor` 查看每个来源的具体情况；`devices` 可以列出当前所有可用芯片。

## lint 的判定口径

- `error`：寄存器区间相交但偏移不同、位域重叠、位域越界、名字重复（仅大小写不同）、复位值超出位宽。
- `warning`：同一中断名在不同外设中的向量号不一致。
- `info`：多个寄存器共用**同一偏移**（同一寄存器的不同视图或别名，如 ST TIMx 的 `CCMR1_Output`/`CCMR1_Input`、Nordic 的 `ERASEPCR1` 别名）。这是常见写法，不计为问题。
- 真实样本（STM32F103xx、STM32G431xx、nRF52840、GD32F3x0）的 lint 结果均为 0 error；跨厂商的判定口径经此校准。

## 验证情况

- 合成夹具 `tests/fixtures/synthetic.svd`（含衍生的 `synthetic_b.svd`）覆盖以上全部特性，期望值人工计算。
- `tests/fixtures/synthetic_lint.svd` 是 lint 专用夹具（故意含各类问题）；内置演示数据 `assets/demo.svd`（合成芯片 ETK-DEMO）lint 必须为 0 条。
- 真实样本：STM32G431xx（ST）、STM32F103xx（ST Keil Pack）、nRF52840（Nordic）、GD32F3x0（GigaDevice，本机 Pack）。各样本均做独立遍历对照（见 `tests/test_real_svd.py`；GD32F3x0 为 41 个外设中 36 个逐项一致）。
- 新能力也在真实样本上核对：位域掩码、写入值计算（F103 的 `USART1.CR1.UE` 是 bit13，G431 是 bit0）、跨芯片 diff、`info` 哈希、`lint`（四份真实 SVD 均 0 error，仅有同偏移别名 info）、外设级整体对比（F103↔G431 的 USART1：SR/DR 改名 ISR/RDR、UE 位迁移、FIFO 位域新增）、NVIC 使能位提示、解析缓存往返一致性（F103 的 dim/簇/别名结构完整保留）。
- 解析缓存实测：F103 端到端 171→99 ms、G431 227→103 ms、nRF52840 306→113 ms（本机 Windows，含解释器启动）。
- 尚未覆盖：NXP、Microchip、Espressif 的真实 SVD，待补。
