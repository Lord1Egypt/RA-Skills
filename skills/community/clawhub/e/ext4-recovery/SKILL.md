---
name: ext4-recovery
description: 从 ext4/ext3 文件系统恢复被误删的文件与目录树（rm -rf、rm、find -delete、GUI 删除等）。当现成工具 extundelete / ext4magic 报 “Loading journal descriptors ... 0 descriptors loaded”、只打印 Filesystem in use 而无任何输出、或恢复失败时，使用本技能直接解析 jbd2 日志环，从日志中重建元数据、并从原始磁盘取出尚未被复用的数据块。适用场景：误删源码目录/仓库元数据/配置文件、卸载清理后的紧急抢救、文件系统取证、判断“还能不能救回”以及能救回多少。
---

# ext4 删除恢复

## 用途

在 ext4 上恢复被删除的文件与目录树。核心思路：

> ext4 只记录**元数据**日志，删除时 inode 的块指针会被清零，所以磁盘上的 inode 本身没用；
> 但**日志环里往往还留着删除之前的 inode/extent 副本**，而数据块在未被复用前内容仍然有效。
> 于是：用日志重建元数据 → 直接读原始磁盘取数据。

## 铁律（违反任何一条都会毁掉恢复机会）

1. **绝不挂载待恢复分区**（读写挂载会立刻开始复用空闲块，覆盖待恢复数据）。
   不要点文件管理器、不要自动挂载、不要 `fsck` 修复。
2. **所有操作只读打开设备**。需要写权限时只授予读权限即可
   （`sudo chown $USER:disk <dev> && sudo chmod 660 <dev>`），不要用 `sudo mount`。
3. **恢复结果必须写到另一个文件系统**，绝不能写回待恢复分区。
4. 恢复产物先落地并校验，**之后**才考虑写回原盘。
5. 先做体检与可行性判断，再动手；不要在主盘上反复试探工具。

## 工作流

### 第 1 步：只读体检

```bash
bash <skill>/scripts/diag.sh /dev/sdbX [输出目录]
```

脚本会（全程只读、发现已挂载即中止）报告：设备概况、超级块关键项、日志大小、
只读一致性检查、根目录清单、`s_start` 是否已复位，以及**日志区原始扫描**
（jbd2 事务魔数数量、全零字节占比）。

同时收集时间线证据：

- `journalctl` / `/var/log/syslog` / `/var/log/kern.log` 中该设备的挂载/卸载记录
- shell 历史（`~/.bash_history`、`~/.zsh_history`）中实际执行的删除命令
- `dumpe2fs -h <dev> | egrep 'state|Last write|Last mount'`

这些能直接回答三个关键问题：**删除发生在什么时候、删除后分区是否被写过、删了什么**。

### 第 2 步：判断可行性

必须同时满足：

- 分区在删除后没有再被以读写方式挂载（否则数据块大概率已被复用）
- 删除时刻仍落在日志覆盖窗口内（`scripts/ext4recover.py <dev> scan` 会给出时间范围）
- 日志区仍保留大量 jbd2 魔数 `C0 3B 39 98`、全零占比低

`Total journal size` 是重要指标：默认 128MiB 窗口很短，GB 级日志能覆盖很长的写入历史。

**结论要如实给出**：如果能救的只是一部分，明确说明哪些能救、哪些已无望，不要含糊。

### 第 3 步：快速尝试现成工具（便宜，先试）

```bash
extundelete <dev> --restore-directory <path>     # 若报 0 descriptors loaded → 立即放弃
ext4magic <dev> -m -a <epoch> -d <outdir>        # 必要时先用测试镜像验证该构建是否可用
```

失败信息如何判读见 `references/tool-limits.md`。
**关键认知**：`0 descriptors loaded` 只说明工具依赖的 `s_start` 入口失效，
不代表日志里没有数据 —— 这正是需要自研解析器的信号。

### 第 4 步：用自带脚本做日志解析恢复

```bash
S=<skill>/scripts
python3 $S/ext4recover.py /dev/sdbX info                 # 文件系统与日志概况
python3 $S/ext4recover.py /dev/sdbX scan                 # 覆盖范围与可行性
python3 $S/ext4recover.py /dev/sdbX find <名字>           # 全日志搜索名字 → inode
python3 $S/ext4recover.py /dev/sdbX lookup <父ino> <名字>  # 精确查父目录的历史版本
python3 $S/ext4recover.py /dev/sdbX stat <ino>            # inode 的全部历史版本
python3 $S/ext4recover.py /dev/sdbX verify <ino>          # 映射自检
python3 $S/ext4recover.py /dev/sdbX ls <ino|路径>         # 列目录（含被删条目）
python3 $S/ext4recover.py /dev/sdbX recover <ino|路径> --out /别的盘/out
```

定位被删目标的两种路径：

1. **知道它原来在哪个目录下**：先用 `find`/`lookup` 拿到被删条目的 inode 号，
   再用 `stat` 确认该 inode 存在"`links>0` 且带 extent"的历史版本，然后 `recover`。
2. **整棵目录树被删**：直接对目录 inode 递归 `recover`；遍历会自动对每个子项
   挑选"删除前的最后版本"。

以库方式调用（需要自己写更多逻辑时）：

```python
import sys; sys.path.insert(0, '<skill>/scripts')
from ext4journal import Ext4FS, JournalScanner
js = JournalScanner(Ext4FS('/dev/sdbX')).build()
js.block_data(blk)                 # 取块最佳内容（日志优先，缺失回退磁盘）
js.best_inode(ino)                 # 挑选可用 inode 版本
js.dir_entries(info)               # 列目录（含已删条目）
js.search_name('config.bak')       # 全日志搜索某名字
```

### 第 5 步：验证恢复结果（不可跳过）

按可靠性从高到低：

1. **工具自检**：`ext4recover.py <dev> verify <ino>` —— 取一个"确定近期未改动"的现存
   inode，其日志最新版本应与磁盘字节完全一致；一致即证明 tag→数据块映射与全部解析正确。
2. **结构自洽**：恢复出的目录能正常列出、条目名可读、`rec_len` 链平铺满块。
3. **内容特征**：大文件首部是否具备其格式自身的魔数；用该格式的原生校验器/解析器读一遍
   （压缩包、数据库、仓库对象库等都有自己的完整性校验）。
4. **缺失项清单**：明确列出哪些 inode 没有可用历史版本、哪些块已被复用。

### 第 6 步：写回（谨慎）

恢复结果校验通过并已备份到其它介质后，才考虑挂载原盘写回。
写回前提醒用户：此后空闲块会被复用，未恢复内容将不可挽回。

## 脚本与参考

| 资源 | 用途 |
|---|---|
| `scripts/diag.sh` | 第 1 步只读体检（含日志区原始扫描） |
| `scripts/ext4journal.py` | 库：超级块/GDT/extent/目录/日志环解析、块多版本索引、inode 与数据读取 |
| `scripts/ext4recover.py` | CLI：info / scan / find / lookup / stat / ls / recover / verify |
| `references/jbd2-ondisk.md` | ext4 与 jbd2 磁盘格式详解，及**首次实现必踩的解析陷阱** |
| `references/tool-limits.md` | extundelete / ext4magic 失败信息判读与工具选择决策树 |

## 最容易出错的地方（务必核对）

实现或修改解析代码前，先读 `references/jbd2-ondisk.md`。以下几条曾导致"静默失败"——
不报错、输出看似合理，但内容全是垃圾：

- 4K 块下 **GDT 从 block 1 开始**（block 0 的 2048..4096 是保留零区），偏移错了会算出 `inode_table=0`
- inode 表内偏移要**先除后取模**（`idx/(块大小/inode大小)` 与 `idx%(...)`），漏掉会越界
- **extent 结构全部小端**；`ext4_extent` 字段序是 `u32,u16,u16,u32`（格式串 `"<IHHI"`），
  写成 `"<HHII"` 会得到"长度 0、物理块号几十亿"的荒谬结果
- 索引项 `"<IIHH"` 的第 1 个字段是 `ei_block` 而非叶块号，顺序颠倒会得到越界块号
- extent 叶块递归要传**整块**，截断成 60 字节会越界
- jbd2 的 **csum_v3 tag 为 16 字节**，且**首 tag 之后有 16 字节 UUID 要跳过**；
  不跳会每块只解析出 1 个 tag（看似成功，实丢 99%）
- 一个事务**可横跨多个描述符块**，仅在末块带 `LAST_TAG`；并非所有镜像都有提交块
- 日志环会绕回，**顺序必须按事务 seq 号**，不能按物理位置
- inode/extent 结构里的 **`i_dtime` 是判断删除时间的权威依据**，用它确认目标是否还在覆盖窗口内

结构校验（`rec_len` 链平铺、目录名可读、extent 首部特征码）比 inode 校验和更值得依赖；
inode 校验和各发行版/参数下约定有差异，不要把它当作唯一判据。
