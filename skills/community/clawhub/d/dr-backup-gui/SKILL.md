---
name: dr-backup-gui
version: 1.0.5
description: "统一灾备备份与迁移 GUI 工具。整合 Velero（K8s备份）、Rclone（云存储同步）、Rsync（文件同步）、Coriolis（跨云迁移），提供图形化配置、档案管理、执行日志和任务记录。"
---

# DR Backup GUI

## 安全警示

以下操作可能删除或覆盖数据，请务必在非生产环境测试后再用于生产系统：
- Rsync 同步模式会删除目标端多余文件
- Rclone sync/mirror 会覆盖目标端已有文件
- Velero 恢复会修改目标集群状态
- Coriolis 迁移/副本会移动或复制虚拟机
- 配置文件（~/.dr_backup_gui/profiles.json）可能包含敏感连接信息，请限制文件访问权限

## 功能概览

- Velero: K8s Deployment/Service/PVC 备份恢复、定时计划
- Rclone: 70+ 云存储同步复制（AWS S3/GCS/Azure）
- Rsync: 文件级增量同步，支持 SSH/SFTP/SCP
- Coriolis: 跨云平台 VM 迁移、副本创建

## 快速启动

### 1. 检查依赖

`cd ~/.qclaw/skills/dr-backup-gui/scripts && python3 check_and_launch.py`

### 2. 安装依赖（如需）

`python3 check_and_launch.py --install`

### 3. 运行 GUI

`cd ~/.qclaw/skills/dr-backup-gui/scripts && python3 dr_backup_gui.py`

最低要求：Python 3.9+，PyQt6

## 工具详情

### Velero（需 kubeconfig）

备份：指定命名空间、K8s 资源类型，TTL 保留策略  
恢复：支持命名空间映射（旧集群 → 新集群）  
定时：Cron 表达式或简写（@every 6h）  
依赖：kubectl 已配置 + velero CLI + 备份存储后端（S3/MinIO等）

### Rclone

自动发现已配置的远端存储  
四种模式：Sync / Copy / Mirror / Check  
过滤规则：include/exclude 模式  
带宽限制、并发数控制

### Rsync

本地/远程均可（通过 SSH）  
选项：归档模式、压缩、checksum比较、删除目标多余文件  
预演模式（dry-run）避免误操作

### Coriolis

列出源/目标端点  
选择 VM、Minion池  
创建迁移或副本任务  
依赖：Coriolis 服务运行中（默认 localhost:8077）

## 配置档案

每个工具支持保存/加载/删除多个命名配置档案  
配置存储在：~/.dr_backup_gui/profiles.json  
注意：配置文件中可能包含敏感连接信息，请限制访问权限

## 触发方式

- 「打开容灾备份工具」
- 「启动 DR Backup GUI」
- 「用 velero 做 K8s 备份」
- 「用 rclone 同步云存储」
- 「用 rsync 同步文件」
- 「用 coriolis 迁移虚拟机」
