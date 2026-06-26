# C 盘清理指南

## 安全清理项目（无风险）

### 1. 临时文件
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Users\*\AppData\Local\Temp\*` | 用户临时文件 | 0.5-5 GB |
| `C:\Windows\Temp\*` | 系统临时文件 | 0.1-2 GB |

### 2. Windows 更新缓存
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Windows\SoftwareDistribution\Download\*` | 更新下载缓存 | 1-5 GB |
| `C:\Windows\Installer\$PatchCache$` | 补丁缓存 | 0.5-2 GB |

### 3. 浏览器缓存
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Users\*\AppData\Local\Google\Chrome\*\Cache` | Chrome 缓存 | 0.1-2 GB |
| `C:\Users\*\AppData\Local\Microsoft\Edge\*\Cache` | Edge 缓存 | 0.1-2 GB |

### 4. 包管理器缓存
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Users\*\AppData\Local\pip\Cache\*` | pip 缓存 | 0.1-1 GB |
| `C:\Users\*\AppData\Local\npm-cache\*` | npm 缓存 | 0.1-1 GB |

### 5. 回收站
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| 回收站 | 已删除文件 | 可变 |

---

## 谨慎清理项目（低风险）

### 1. 应用缓存
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Users\*\AppData\Local\Feishu\*\Cache` | 飞书缓存 | 0.5-3 GB |
| `C:\Users\*\AppData\Local\JianyingPro\UserCache` | 剪映缓存 | 1-5 GB |
| `C:\Users\*\AppData\Local\Quark\*\Cache` | 夸克缓存 | 0.5-2 GB |

**注意**：清理后应用可能需要重新加载数据

### 2. 缩略图缓存
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\thumbcache_*.db` | 缩略图 | 0.1-1 GB |

**注意**：首次打开文件夹会重新生成

### 3. 旧驱动缓存
| 路径 | 说明 | 可清理大小 |
|------|------|-----------|
| `C:\Users\*\AppData\Local\NVIDIA\*\*` | NVIDIA 旧驱动 | 1-5 GB |
| `C:\Windows\System32\DriverStore\FileRepository\*` | 驱动存储 | 2-10 GB |

**注意**：使用 `pnputil` 安全清理

---

## 高级清理项目（中风险）

### 1. WSL 发行版
```bash
# 查看
wsl --list --verbose

# 删除未使用的
wsl --unregister <发行版名称>
```

### 2. Docker 镜像
```bash
# 查看
docker system df

# 清理
docker system prune -a
```

### 3. 休眠文件
```powershell
# 禁用休眠（释放约 RAM 大小的空间）
powercfg -h off
```

### 4. 系统还原点
```powershell
# 删除旧还原点，保留最新的
vssadmin delete shadows /for=c: /oldest
```

---

## 禁止删除的文件

⚠️ **绝对不要删除以下文件/目录**：

```
C:\Windows\System32\*           # 系统核心文件
C:\Windows\WinSxS\*             # 组件存储
C:\Program Files\WindowsApps\*  # UWP 应用
C:\Users\*\NTUSER.DAT           # 用户注册表
C:\pagefile.sys                 # 页面文件
C:\hiberfil.sys                 # 休眠文件
```

---

## 可迁移的应用

以下应用可重新安装到其他盘：

| 应用 | 典型大小 | 迁移建议 |
|------|---------|---------|
| Epic Games | 5-20 GB | 重装到 D 盘 |
| Steam 游戏 | 10-100 GB | 使用 Steam 迁移功能 |
| 网易游戏 | 5-50 GB | 重装到 D 盘 |
| Adobe 系列 | 5-20 GB | 重装到 D 盘 |
| Docker Desktop | 5-10 GB | 重装到 D 盘 |

---

## 清理频率建议

| 项目 | 建议频率 |
|------|---------|
| 临时文件 | 每周 |
| 浏览器缓存 | 每周 |
| Windows 更新缓存 | 每月 |
| 应用缓存 | 每月 |
| 大文件扫描 | 每月 |
| 系统还原点 | 每季度 |

---

## 清理命令速查

```powershell
# 安全清理
python scripts/clean_c_drive.py --level safe

# 标准清理
python scripts/clean_c_drive.py --level standard

# 预览模式
python scripts/clean_c_drive.py --dry-run

# 查找大文件
python scripts/find_large_files.py --min-size 1GB

# 完整扫描
python scripts/scan_c_drive.py --full
```
