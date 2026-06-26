# 数据恢复故障速查表

## 快速判断故障类型

### 听声音辨故障
| 声音 | 判断 | 怎么做 |
|------|------|--------|
| 滋滋/吱吱 | 磁头可能卡住 | 立即断电，别通电了 |
| 咔咔/哒哒 | 磁头损坏 | 断电，换磁头需要开盘 |
| 嗡嗡但不转 | 电机抱死 | 尝试换电路板 |
| 正常转但不识别 | 可能是固件/电路板问题 | 先查SMART信息 |
| 完全没动静 | 电路板烧了 | 换同型号电路板 |

### 看现象辨故障
| 现象 | 判断 | 可自修? |
|------|------|---------|
| 分区变成RAW | 文件系统损坏 | ✅ 可用TestDisk |
| 提示"需要格式化" | 引导扇区损坏 | ✅ 先别格式化 |
| 文件变乱码/0KB | 文件表损坏 | ✅ DMDE/R-Studio |
| 硬盘在BIOS不识别 | 硬件级问题 | ❌ 送修 |
| 读写极慢/卡死 | 坏道增多 | ✅ 先ddrescue镜像 |
| 摔过后不认盘 | 磁头移位 | ❌ 送修 |

## 常用命令速查

```bash
# ddrescue 创建镜像
sudo ddrescue -d /dev/sda /mnt/backup/image.img /mnt/backup/logfile.log

# 查看SMART信息
sudo smartctl -a /dev/sda

# TestDisk 修复分区表（交互式）
sudo testdisk /dev/sda

# 查看分区信息
sudo fdisk -l /dev/sda

# 查看文件系统
lsblk -f
```

## 工具获取

- TestDisk/PhotoRec: https://www.cgsecurity.org/
- DMDE: https://dmde.com/
- R-Studio: https://www.r-studio.com/
- ddrescue: apt install ddrescue / brew install ddrescue
- CrystalDiskInfo: https://crystalmark.info/
