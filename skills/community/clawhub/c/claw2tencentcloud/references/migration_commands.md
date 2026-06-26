# OpenClaw 迁移命令参考

## 单实例迁移命令模板

### 完整命令（参数替换后执行）

```bash
# 安装 sshpass
apt install -y sshpass;

# 停止源端 OpenClaw 服务
sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{src_ip} "openclaw gateway stop";

# 打包源端数据
# 注意: /root/.openclaw 目录可能数据量比较大，也可能不存在
sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{src_ip} "tar -czf /home/openclaw-state.tgz -C /root .openclaw";

# 从源端实例拷贝 openclaw-state.tgz 到当前实例
# 耗时可能会比较久，提示用户耐心等待。如果失败可以重试拷贝
sshpass -p '{password}' scp -o StrictHostKeyChecking=no {username}@{src_ip}:/home/openclaw-state.tgz /home;

# 备份当前 OpenClaw 实例数据
# 如果源端 OpenClaw 数据跟当前 OpenClaw 不兼容，可以使用 /home/openclaw-backup 这个备份恢复
cp -r /root/.openclaw /home/openclaw-backup

# 覆盖当前 OpenClaw 实例数据
tar -xvzf /home/openclaw-state.tgz -C /root;

# 修复配置文件路径
# 有可能源端 openclaw.json 配置跟当前 OpenClaw 版本不一致
sed -i 's|/app/extensions/|/root/.openclaw/extensions/|g' /root/.openclaw/openclaw.json

# 修复权限
chmod 0600 /root/.openclaw/openclaw.json;

# 重启 OpenClaw
openclaw gateway restart;
```

## 批量迁移脚本

### 脚本下载

```bash
wget https://go2tencentcloud-1251783334.cos.ap-guangzhou.myqcloud.com/others/claw2tencentcloud.py
```

### 实例配对文件格式

创建 `instances.txt` 文件，每行一组迁移配对，格式为：

```
<源端实例ID> <源端登录账号> <源端登录密码> <目标端实例ID>
```

示例：

```
lhins-abc12345 ubuntu MyP@ssw0rd ins-xyz67890
lhins-def11111 root P@ss1234 ins-ghi22222
```

### 执行命令

```bash
python3 claw2tencentcloud.py \
    --src-secret-id <源端SecretId> \
    --src-secret-key <源端SecretKey> \
    --dst-secret-id <目标端SecretId> \
    --dst-secret-key <目标端SecretKey> \
    --pairs-file instances.txt
```

### 所需权限

腾讯云 API 密钥需要以下权限：

| 权限策略 | 说明 |
|----------|------|
| `QcloudCVMFullAccess` | CVM 云服务器可读写权限 |
| `QcloudLighthouseFullAccess` | Lighthouse 轻量应用服务器可读写权限 |
| `QcloudTATFullAccess` | TAT 腾讯自动化助手可读写权限 |
