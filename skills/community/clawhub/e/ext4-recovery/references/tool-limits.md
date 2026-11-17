# 现成恢复工具的能力边界与失败判读

先跑现成工具（便宜），失败后再上自研解析器（贵但可控）。
关键是**看懂失败信息**，别把"工具失效"误判成"数据不存在"。

---

## 1. extundelete

```bash
extundelete <dev> --restore-directory <path>
extundelete <dev> --restore-all
extundelete <dev> --inode <ino>
extundelete -j <journal_copy> <dev> --restore-...
```

原理：读取日志描述符 → 找到被删 inode 的副本 → 用其中的块指针恢复数据。

**典型失败输出与含义**

| 输出 | 含义 |
|---|---|
| `Loading journal descriptors ... 0 descriptors loaded.` | **它只从日志超级块的 `s_start` 往后扫描**。正常卸载后 `s_start = 0`（日志被 checkpoint 复位），于是它一个事务都看不到。**这不代表日志里没有数据** |
| `Extent block checksum does not match extent block while finding inode for X` | 它在读一段已经过期的元数据（跨代残留），校验和不匹配 |
| `Operation not permitted while restoring directory` | 恢复动作失败，通常源于上一条的元数据不可信 |
| `Could not find correct inode number past inode N` | 只找到了目录项，找不到对应 inode |

**结论**：只要出现 `0 descriptors loaded`，就直接放弃 extundelete，
转向 ext4magic 或自研解析器。

---

## 2. ext4magic

```bash
ext4magic <dev> -m -d <outdir>            # 只恢复"已删除文件"
ext4magic <dev> -M -d <outdir>            # 恢复全部文件（整个文件系统被删时用）
ext4magic <dev> -f <path> -L -d <outdir>  # 按路径恢复目录树
ext4magic <dev> -I <ino> -T               # 打印某 inode 在日志中的所有副本
ext4magic <dev> -H                        # inode 时间戳直方图（判断删除时刻）
ext4magic <dev> -T                        # 日志中数据块副本的事务列表
```

时间选项：`-a <epoch>` = after，"数据可用"的时间；`-b <epoch>` = before，删除发生的时间。
不指定时默认 `before = now`、`after = now - 24h`。**大范围删除必须显式给时间窗口**，
否则要么漏（窗口太窄）要么白跑（窗口太宽）。

**典型失败模式**

| 现象 | 含义 |
|---|---|
| 只打印 `Filesystem in use: <dev>` 与 `ext4magic : EXIT_SUCCESS`，没有任何内容 | 该**发行版构建的信息/列表输出功能失效**（在新 mkfs 出来的测试镜像上同样复现）。此时 `-S / -J / -H / -T / -I / -L` 全部无输出，但 `-m/-M/-r/-R` 的**恢复动作**仍可能真正写文件 |
| 无任何输出且退出码非 0 | 日志加载失败（常见于 csum_v3 / 超大日志 / 64bit 组合） |

**判读建议**：先用一个小测试镜像（`mkfs.ext4` 一个 200MiB 文件 → 挂载 → 造文件 → 删除 → 卸载）
验证该 ext4magic 构建是否可用。验证不通过就直接上自研解析器，不要在主盘上反复试探。

---

## 3. 其它可用工具

| 工具 | 适用点 | 局限 |
|---|---|---|
| `testdisk` | 交互式 undelete，ext4 支持较好，能按目录树挑选恢复 | 依赖日志；大文件/大量文件时慢 |
| `photorec` | 按内容特征 carving | **丢失文件名与目录结构**；对压缩/加密/容器格式基本无效 |
| `debugfs` | `-R 'ls -l /'`、`imap`、`stat`、`logdump` | 不挂载即可浏览，是取证与校验的首选；不能用来恢复已删 inode 的块指针 |
| `dumpe2fs` / `tune2fs -l` | 超级块与日志参数 | 只读 |

`debugfs` 的只读浏览（无需挂载）应当成为第一步：
它能确认"目录还在不在、哪些条目消失了"，为后续定位提供权威坐标。

---

## 4. 决策树

```
1. 分区是否已挂载？          → 是：立即 umount。绝不要在挂载状态下恢复。
2. 设备是否可读？            → 否：sudo chown $USER:disk <dev>
3. dumpe2fs -h 看三件事：
     a. Filesystem state 是否 clean（决定 s_start 是否为 0）
     b. Total journal size（决定覆盖窗口长度）
     c. features 是否含 csum_v3 / 64bit / metadata_csum（决定 tag 尺寸等解析细节）
4. debugfs -R 'ls -l /' 确认目标目录与消失的条目
5. extundelete 试一次 → 若报 0 descriptors loaded 直接放弃
6. ext4magic 试一次（必要时先用测试镜像验证该构建可用）→ 若无效放弃
7. 自研 jbd2 解析器（scripts/ext4journal.py + ext4recover.py）
8. 恢复结果落到另一块盘 → 用文件自身格式做完整性验证 → 再考虑写回原盘
```

---

## 5. 一条重要判据

现成工具的"失败"大多只说明**它们依赖的入口指针失效**（如 `s_start = 0`），
并不说明物理日志里没有历史数据。

**只要满足下面两条，就值得自研解析器继续做：**

1. `Total journal size` 明显大于默认值（越长覆盖窗口越大），或删除发生得足够近；
2. 日志区原始字节扫描显示仍有大量 jbd2 事务魔数 `C0 3B 39 98`、且全零占比很低。

这正是 `diag.sh` 第 [8] 步在做的判断。
