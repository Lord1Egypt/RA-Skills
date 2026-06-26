# etcd Skill

一个纯净的etcd管理技能，用于OpenClaw系统。

## 功能

- 安全的etcd key/value操作
- 生产环境保护机制
- 备份和恢复功能
- 多环境支持（dev/test/prod）

## 安装

1. 将技能目录复制到OpenClaw技能目录：
   ```bash
   cp -r etcd ~/workspace/test/openclaw/skills/
   ```

2. 确保etcdctl已安装：
   ```bash
   # 检查etcdctl
   etcdctl version
   ```

## 依赖

- etcdctl (版本3.6.1+)
- bash
- jq (可选，用于JSON处理)

## 许可证

MIT