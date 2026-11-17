# ext4 / jbd2 磁盘格式要点与解析陷阱

本文件记录自研日志解析器必须踩对的细节。任何一处写错都会导致"解析成功但内容全是垃圾"，
而且往往表现为静默失败（不报错、输出看似合理），所以务必逐条核对。

---

## 1. 超级块（superblock）

位于设备偏移 **1024**，长度 1024 字节。关键字段（均为小端）：

| 偏移 | 字段 | 说明 |
|---|---|---|
| 0x00 | s_inodes_count | inode 总数 |
| 0x04 | s_blocks_count_lo | 块总数低 32 位 |
| 0x14 | s_first_data_block | 4K 块时为 0，1K 块时为 1 |
| 0x18 | s_log_block_size | 块大小 = `1024 << 该值` |
| 0x20 | s_blocks_per_group | 每组块数 |
| 0x28 | s_inodes_per_group | 每组 inode 数 |
| 0x2C / 0x30 | s_mtime / s_wtime | 最后挂载 / 写入时间 |
| 0x38 | s_magic | 必须是 0xEF53 |
| 0x3A | s_state | 1 = clean（正常卸载，说明 `s_start` 会被复位） |
| 0x54 | s_first_ino | 第一个非保留 inode（通常 11）|
| 0x58 | s_inode_size | inode 大小（128 / 256 / 512）|
| 0x5C / 0x60 / 0x64 | compat / incompat / ro_compat | 特性位 |
| 0x68 | s_uuid[16] | 文件系统 UUID |
| 0x150 | s_blocks_count_hi | 块总数高 32 位（启用 64bit 时）|

特性位速查（incompat）：`0x01` revoke、`0x02` 64bit、`0x08` csum_v2、`0x10` csum_v3、
`0x20` fast_commit、`0x40` extents、`0x80` 64bit（部分版本）。
ro_compat：`0x400` metadata_csum。

---

## 2. 组描述符表（GDT）—— **最容易踩的偏移错误**

- **块大小 > 1024 时**：超级块位于 block 0 的 `1024..2048`，
  **GDT 从 block 1 开始**；block 0 的 `2048..4096` 是**保留零区**。
- 块大小 = 1024 时：超级块独占 block 1，GDT 从 block 2 开始。

若误把 block 0 的 `2048..` 当作 GDT 起点，会读到一片零，进而算出
`inode_table = 0` 这类荒谬值 —— 而后续代码可能"歪打正着"地跑下去，非常隐蔽。

组描述符字段（64 字节版）：`bg_inode_table_lo` 在偏移 **8**，`bg_inode_table_hi` 在偏移 **40**。

`debugfs -R 'imap <ino>'` 可直接给出权威答案，用于校验自己的换算。

---

## 3. inode 与 inode 表定位

inode 表在组内是连续的 `inodes_per_group * inode_size / block_size` 个块（4K 块 + 256B inode 时 = 512 块）。

```
g    = (ino - 1) / inodes_per_group
idx  = (ino - 1) % inodes_per_group
blk  = inode_table[g] + idx / (block_size / inode_size)
off  = (idx % (block_size / inode_size)) * inode_size
```
**陷阱**：把 `idx * inode_size` 直接当作块内偏移（漏掉再除一次）会越界读到别的块，
在 inode 号较小时看起来"也能用"，inode 号大时才崩。

inode 字段偏移（raw，256 字节版）：

| 偏移 | 字段 |
|---|---|
| 0x00 | i_mode (u16) |
| 0x04 | i_size_lo (u32) |
| 0x08 / 0x0C / 0x10 | i_atime / i_ctime / i_mtime |
| 0x14 | **i_dtime**（非 0 表示已删除，是判断"何时被删"的权威依据）|
| 0x1A | i_links_count |
| 0x1C | i_blocks（512 字节为单位）|
| 0x20 | i_flags（`0x80000` = 使用 extent）|
| 0x28 | i_block[15]（60 字节：extent 树头或传统块指针）|
| 0x6C | i_size_high |
| 0x7C / 0x82 | i_checksum_lo / i_checksum_hi |
| 0x80 | i_extra_isize |
| 0x90 | i_crtime |

删除时的表现：`i_links_count = 0`、`i_dtime` 被写入、`i_size` 归零、
**extent 树被清空（eh_entries = 0）**。所以磁盘上的 inode 本身对恢复无用，
必须找到删除之前的日志历史版本。

---

## 4. extent 结构 —— **全部小端，字段顺序易错**

```c
struct ext4_extent_header {   /* 小端 */
    __le16 eh_magic;    /* 0xF30A */
    __le16 eh_entries;
    __le16 eh_max;
    __le16 eh_depth;
    __le32 eh_generation;
};
struct ext4_extent {          /* 小端！常见错误是用大端 */
    __le32 ee_block;      /* 逻辑块号 */
    __le16 ee_len;        /* 覆盖块数 */
    __le16 ee_start_hi;
    __le32 ee_start_lo;
};
struct ext4_extent_idx {      /* 小端 */
    __le32 ei_block;
    __le32 ei_leaf_lo;
    __le16 ei_leaf_hi;
    __le16 ei_unused;
};
```

要点：

- 头部与条目**都是小端**。用大端读会把 magic 读成 `0x0AF3`，于是"魔数不匹配"→返回空 extent。
- `ext4_extent` 的字段序是 **u32, u16, u16, u32**；写成 `"<HHII"` 会把 `ee_len` 读成 0、
  把 `ee_start_hi` 读成逻辑块号，最终得到"长度为 0、物理块号几十亿"的荒谬 extent。
  正确格式串是 `"<IHHI"`。
- 索引项格式串 `"<IIHH"`，注意第 1 个字段是 `ei_block` 而非叶块号，
  叶块号是第 2 个字段。把两者顺序搞反会得到越界块号。
- `eh_depth > 0` 时要在叶块里递归解析；叶块可容纳约 `(4096-12)/12 ≈ 340` 个 extent，
  **递归时必须传整块（不能截断成 60 字节）**，否则会 struct 解包越界。
- 稀疏文件的 extent 之间存在逻辑空洞，拼接数据时要按 `ee_block` 补零。

---

## 5. jbd2 日志：物理布局

日志 inode 恒为 **inode 8**。其 extent 映射给出日志的物理位置：

```
journal 逻辑块 0  <->  extent 的第一个物理块（这里放日志超级块）
journal 逻辑块 i  <->  extent 覆盖范围内的第 i 个物理块
```

日志超级块（journal 逻辑块 0）关键字段，**大端**：

| 偏移 | 字段 |
|---|---|
| 0x00 | h_magic = 0xC03B3998 |
| 0x04 | h_blocktype（4 = v2 超级块）|
| 0x0C | s_blocksize |
| 0x10 | s_maxlen（日志块总数）|
| 0x14 | s_first（日志首块，通常 1）|
| 0x18 | s_sequence |
| 0x1C | **s_start**（0 = 日志已被 checkpoint 复位）|
| 0x24 / 0x28 / 0x2C | compat / incompat / ro_compat |
| 0x30 | s_uuid[16] |

`debugfs -R 'logdump -a'` 输出 `Journal starts at block 0` + `No magic number at block 1: end of journal`
就是 `s_start = 0` 的表现。**这只说明"没有待回放事务"，并不代表物理日志里没有历史数据。**

---

## 6. jbd2 事务结构与 tag 格式 —— **本项目最关键的三处发现**

块类型：`1` 描述符、`2` 提交、`3` 撤销、`4` 超级块 v2。

### 6.1 tag 尺寸由 incompat 特性决定

| 条件 | tag 字节数 |
|---|---|
| csum_v3 (0x10) | **16** |
| csum_v2 (0x08) | 12 |
| 仅 64bit (0x02) | 8 |
| 都没有 | 4 |

csum_v3 的 16 字节布局（大端）：
`t_blocknr(4) | t_flags(4) | t_blocknr_high(4) | t_checksum(4)`

### 6.2 首 tag 之后存在 16 字节 UUID 字段 —— 必须跳过

实测（`journal_checksum_v3` 已启用）描述符块中，**首个 tag 的 `SAME_UUID` 位为 0，
其后紧跟 16 字节 UUID 字段**，之后各 tag 的 `SAME_UUID` 才置位。

若不跳过这 16 字节，会把它解析成一个 `blocknr=0, flags=0` 的"空 tag"，
多数实现（包括本项目第一版）会在此时 `break`，于是**每个描述符只解析出 1 个 tag**，
看起来"解析成功"，实际丢掉了 99.6% 的数据。

自查方法：正确模式下单个描述符应解析出约 **253** 个 tag，且块间隔与 tag 数吻合。
两种假设都跑一遍、比较"平均 tag 数"，自动选对的那个（`JournalScanner.detect_tag_mode()`）。

tag 标志位：`0x01` ESCAPE、`0x02` SAME_UUID、`0x04` DELETED、`0x08` LAST_TAG。
ESCAPE 表示数据块首 4 字节被替换为魔数（真实值为 0），读取时要把前 4 字节归零。

### 6.3 一个事务可横跨多个描述符块

写满 253 个 tag 就接下一个描述符块，**只有最后一个描述符块的末位 tag 带 LAST_TAG**，
其后才是提交块。因此正确的切分逻辑是：

```
while 当前块是描述符块:
    解析其 tag
    数据块紧跟其后（位置 = 描述符块号 + 1 + tag 序号）
    若末位 tag 带 LAST_TAG:
        跳出，下一块应是提交块
```

**实测注意**：并非所有 ext4 镜像都存在提交块。本案例中 1148 个描述符块均匀间隔 254 块
（1 描述符 + 253 数据）且**完全没有提交块**，因此不能把"找到提交块"作为解析正确的必要条件，
应以"描述符间隔与 tag 数是否自洽"作为主要判据。

### 6.4 日志环会绕回 —— 顺序必须按 seq 而非物理位置

环形缓冲写满后覆盖最旧数据，**物理位置相邻的两个事务，seq 可能相差很远**。
判断"某块的最新版本"时必须比较事务 `seq` 号（配合 `s_sequence` 取模），
不能简单地认为"物理位置靠后 = 更新"。

本案例中 `s_start = 0` 且日志空闲，物理位置靠后恰是较新的写入；
但仍应以 seq 排序为准。

---

## 7. 目录块格式

```
struct ext4_dir_entry_2 {
    __le32 inode;      /* 0 表示本槽位未使用 */
    __le16 rec_len;    /* 本条目总长度，4 字节对齐 */
    __u8   name_len;
    __u8   file_type;  /* 1 普通 2 目录 7 符号链接 */
    char   name[name_len];
};
```
启用 `metadata_csum` 时，块末尾 12 字节是目录块尾部：
`det_reserved_zero1(4)=0 | det_rec_len(2)=12 | det_reserved_zero2(1)=0 | det_reserved_ft(1)=0xDE | det_checksum(4)`。

可靠的结构校验：`rec_len` 链必须**恰好平铺满整块**、每个 `rec_len` 是 4 的倍数、
名字全为可打印字符。用它来判断"这一块到底是不是目录块"非常有效。

**为什么日志里的目录块极有价值**：删除文件/子目录时，父目录的数据块会被写回（去掉条目），
该块的旧内容因此进入日志。所以日志中往往能同时拿到
"删除前的目录清单"和"删除后的目录清单"，两者的差异直接给出被删名字与其 inode 号。

---

## 8. metadata_csum 校验和（可作为映射正确性的交叉验证）

- 文件系统级种子：`csum_seed = crc32c(~0, s_uuid, 16)`
- inode 级种子：`crc32c(csum_seed, le32(ino))`
- inode 校验和覆盖（跳过校验字段自身）：
  `raw[0x00:0x7C] + 0000 + raw[0x7E:0x82] + 0000 + raw[0x84:inode_size]`

用的是 **CRC-32C（Castagnoli，反射多项式 0x82F63B78）**，
且内核实现**不做最终取反**（`crc32c_le` 直接链式调用）。

**重要落坑经验**：即便按上述公式实现，也可能与镜像中的存储值不一致
（inode 大小 / `i_extra_isize` / 分段边界等有多种约定差异）。
因此**不要把 inode 校验和作为唯一的正确性判据**，更可靠的验证手段是下面第 9 节。

---

## 9. 推荐的映射正确性验证（比校验和可靠）

1. **结构自洽**：解析出的目录块条目名是否可读、`rec_len` 链是否平铺满块。
2. **交叉比对**：取一个"确定近期未被改动"的现存文件 inode，
   其日志最新版本应与磁盘上的 inode 字节完全一致。一致即证明
   `tag -> 数据块` 映射与所有解析全部正确（`ext4recover.py verify <ino>`）。
3. **内容特征**：恢复大文件后检查其首部特征码是否符合该格式
   （例如压缩包/索引文件自身的魔数）。
4. **工具交叉验证**：用该文件自身的解析器/校验器读一遍恢复结果。

---

## 10. 其它经验

- 日志大小直接决定可行性。`dumpe2fs -h | grep 'Total journal size'`：
  128MiB 是常见默认值且窗口很短；GB 级日志能覆盖很长的写入历史。
- 删除后**越少写入越好**；一旦以读写方式挂载，空闲块会被逐步复用，
  已恢复元数据指向的数据可能立刻被覆盖。**先把恢复结果落到另一块盘，再考虑写回。**
- ext4 **只记录元数据日志**，不记录文件数据（`data=ordered`）。
  所以恢复依赖的是"日志里有 inode/extent 元数据" + "数据块物理上还没被复用"这两件事同时成立。
- `i_dtime` 是所有被删 inode 的删除时间；把它与日志覆盖时间范围比对，
  就能判断目标文件是否还在可恢复窗口内。
