---
name: claw2tencentcloud
description: This skill helps users migrate OpenClaw data to Tencent Cloud instances. It supports three scenarios — single instance migration to the current machine, batch migration of multiple instances to Tencent Cloud Lighthouse or CVM instances, and custom migration planning for unsupported scenarios. This skill should be used when users mention OpenClaw data migration, OpenClaw gateway migration, or need to move OpenClaw deployments between servers.
---

# OpenClaw 数据迁移助手

帮助用户将 OpenClaw 数据迁移到腾讯云实例，支持单实例迁移、批量迁移和自定义迁移方案。

## 技能概览

本技能包含三种能力：

1. **技能 1 — 单实例迁移**：将单个 OpenClaw 数据迁移到当前机器
2. **技能 2 — 批量迁移**：批量迁移多个 OpenClaw 数据到腾讯云 Lighthouse 或 CVM 实例
3. **技能 3 — 自定义方案**：对于不满足技能 1 和技能 2 的场景，给出相应的迁移方案

## 技能 1：迁移单个 OpenClaw 数据到当前机器

### 迁移风险告知

在开始迁移前**必须**告知用户以下风险：

- 开始迁移时源端 OpenClaw 实例会被停止
- 迁移后当前 OpenClaw 实例的数据会被源端 OpenClaw 实例的数据覆盖

### 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `src_ip` | 源端 OpenClaw 实例的公网 IP 地址 | ✓ |
| `username` | 源端 OpenClaw 实例的登录用户名 | ✓ |
| `password` | 源端 OpenClaw 实例的登录密码 | ✓ |

### 迁移步骤

提示用户输入上述 3 个参数，然后将 `src_ip`、`username`、`password` 替换到以下命令中逐步执行：

```bash
# 1. 安装 sshpass
apt install -y sshpass;

# 2. 停止源端 OpenClaw 服务
sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{src_ip} "openclaw gateway stop";

# 3. 打包源端数据（/root/.openclaw 目录可能数据量较大，也可能不存在）
sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{src_ip} "tar -czf /home/openclaw-state.tgz -C /root .openclaw";

# 4. 从源端拷贝数据到当前实例（耗时可能较久，提示用户耐心等待；失败可重试）
sshpass -p '{password}' scp -o StrictHostKeyChecking=no {username}@{src_ip}:/home/openclaw-state.tgz /home;

# 5. 备份当前 OpenClaw 实例数据（如源端数据不兼容可用此备份恢复）
cp -r /root/.openclaw /home/openclaw-backup

# 6. 覆盖当前 OpenClaw 实例数据
tar -xvzf /home/openclaw-state.tgz -C /root;

# 7. 修复配置文件路径（源端与当前版本可能不一致）
sed -i 's|/app/extensions/|/root/.openclaw/extensions/|g' /root/.openclaw/openclaw.json

# 8. 修复权限并重启
chmod 0600 /root/.openclaw/openclaw.json;
openclaw gateway restart;
```

### 常见问题

1. 用户源端实例未允许 SSH 访问
2. 用户源端实例 OpenClaw 数据不在 `/root` 目录下
3. 迁移期间源端 OpenClaw 数据被修改
4. 源端 OpenClaw 版本与当前版本不一致，配置文件不兼容

## 技能 2：批量迁移多个 OpenClaw 数据到腾讯云实例

### 迁移风险告知

在开始迁移前**必须**告知用户以下风险：

- 开始迁移时源端 OpenClaw 实例会被停止
- 迁移后目标 OpenClaw 实例的数据会被源端 OpenClaw 实例的数据覆盖

### 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| 源端云平台的云 API 访问密钥 | SecretId + SecretKey | ✓ |
| 腾讯云目标账号的云 API 访问密钥 | SecretId + SecretKey | ✓ |
| 待迁移的 OpenClaw 实例列表 | 见下方格式 | ✓ |
| 源端云平台名称 | 如腾讯云、阿里云等 | 选填 |
| 源端实例所在地域 | 如 ap-guangzhou | 选填 |
| 目标实例所在地域 | 如 ap-guangzhou | 选填 |

**实例列表格式**（每行一组，空格分隔）：

```
<源端实例ID> <源端登录账号> <源端登录密码> <目标端实例ID>
```

示例：

```
lhins-abc12345 ubuntu MyP@ssw0rd ins-xyz67890      # 腾讯云LH -> 腾讯云CVM
```

### 输出

结合脚本执行结果的文件，汇总迁移的汇总结果。

### 迁移步骤

1. 提示用户输入上述参数
2. 下载批量迁移脚本：`https://go2tencentcloud-1251783334.cos.ap-guangzhou.myqcloud.com/others/claw2tencentcloud.py`
3. 读取脚本的说明，按照说明填充脚本中的需要参数
4. 执行脚本。脚本会自动迁移多个 OpenClaw 实例到腾讯云实例，并结合脚本生成的结果文件生成迁移结果。因数据量大、机器带宽小等因素，脚本执行可能耗时较久，提示用户耐心等待

详细的迁移命令参考见 `references/migration_commands.md`。

### 常见问题

1. 用户源端实例未允许 SSH 访问
2. 用户源端实例 OpenClaw 数据不在 `/root` 目录下
3. 迁移期间源端 OpenClaw 数据被修改
4. 源端 OpenClaw 版本与当前版本不一致，配置文件不兼容
5. 云 API 密钥缺少权限，腾讯云需要以下权限：
   - CVM 可读写权限：`QcloudCVMFullAccess`
   - Lighthouse 可读写权限：`QcloudLighthouseFullAccess`
   - TAT（腾讯自动化助手）可读写权限：`QcloudTATFullAccess`

## 技能 3：自定义迁移方案

当技能 1 和技能 2 无法满足用户场景时，需要收集以下信息后给出迁移方案：

- 源端 OpenClaw 实例的部署情况
- 网络环境
- 目的实例类型等信息

根据上述信息提供可执行的迁移方案。
