---
name: compshare-api
description: 管理优云智算CompShare平台的GPU实例全生命周期，包括创建、查询、启动、停止、重启、重置密码和删除实例；当用户需要创建GPU云服务器、查询实例状态、管理实例启停、重置实例密码或删除实例时使用
dependency:
  python:
    - ucloud-sdk-python3>=0.1.0
    - PyYAML>=6.0
    - paramiko>=3.0.0
---

# CompShare API 技能

## 任务目标
- 本技能用于：管理优云智算CompShare平台的GPU实例资源
- 能力包含：创建GPU实例、查询实例列表、启动/停止/重启实例、重置密码、删除实例
- 触发条件：用户需要创建或管理CompShare平台的GPU云服务器实例

## 前置准备

### 依赖安装
```bash
pip install ucloud-sdk-python3 PyYAML paramiko
```

### 配置文件
在使用前，需要在Skill目录下创建配置文件 `assets/config.yaml`：

1. 编辑配置文件，填入API凭证：
```yaml
compshare:
  public_key: "your-public-key"
  private_key: "your-private-key"
  region: "cn-wlcb"
  zone: "cn-wlcb-01"
  base_url: "https://api.compshare.cn"
```

2. 获取API凭证：
   - 登录 CompShare 控制台：https://console.compshare.cn/
   - 进入「API管理」页面：https://console.compshare.cn/uaccount/api_manage
   - 创建并获取 `public_key` 和 `private_key`

3. 配置文件查找优先级：
   - 命令行参数 `--config` 指定的路径
   - 默认路径 `assets/config.yaml`（Skill目录下）

## 操作步骤

### 1. 创建GPU实例（默认创建抢占式）
调用 `scripts/compshare_client.py` 脚本，使用 `create` 命令：
```bash
python scripts/compshare_client.py create \
  --gpu-type 4090 \
  --gpu-count 1 \
  --cpu 16 \
  --memory 64 \
  --disk-size 200 \
  --image-id 500WHhII1fnz \
  --name "ComfyUI-4090" \
  --charge-type Spot
```

### 2. 查询实例列表
调用脚本使用 `list` 命令：
```bash
python scripts/compshare_client.py list
# 或查询特定实例
python scripts/compshare_client.py list --instance-ids "instance-id-1,instance-id-2"
```

### 3. 启动实例

**正常开机**（带GPU）：
```bash
python scripts/compshare_client.py start --instance-id <UHostId>
```

**无卡开机**（不带GPU，节省费用）：
```bash
python scripts/compshare_client.py start --instance-id <UHostId> --without-gpu
```

### 4. 停止实例
调用脚本使用 `stop` 命令：
```bash
python scripts/compshare_client.py stop --instance-id <UHostId>
```

### 5. 重启实例
调用脚本使用 `reboot` 命令：
```bash
python scripts/compshare_client.py reboot --instance-id <UHostId>
```

### 6. 重置实例密码
调用脚本使用 `reset-password` 命令：
```bash
python scripts/compshare_client.py reset-password --instance-id <UHostId> --password <new-password>
```

### 7. 删除实例
调用脚本使用 `delete` 命令：
```bash
python scripts/compshare_client.py delete --instance-id <UHostId>
```

### 8. SSH连接实例
通过实例的 SshLoginCommand 和 Password 连接实例：

1. 先查询实例获取 SSH 登录信息：
```bash
python scripts/compshare_client.py list
# 返回结果中包含 SshLoginCommand 和 Password
```

2. 使用 SSH 客户端连接：
```bash
python scripts/ssh_client.py connect \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password"
```

### 9. SSH远程执行命令
```bash
python scripts/ssh_client.py exec \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --cmd "ls -la /home"
```

### 10. SSH文件操作

**列出目录**：
```bash
python scripts/ssh_client.py ls \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --path "/home"
```

**上传文件**：
```bash
python scripts/ssh_client.py upload \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --local ./local_file.txt \
  --remote /home/remote_file.txt
```

**下载文件**：
```bash
python scripts/ssh_client.py download \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --remote /home/remote_file.txt \
  --local ./local_file.txt
```

**上传整个目录**：
```bash
python scripts/ssh_client.py upload-dir \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --local ./my_project \
  --remote /home/my_project
```

**下载整个目录**：
```bash
python scripts/ssh_client.py download-dir \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --remote /home/data \
  --local ./data_backup
```

**查看文件内容**：
```bash
python scripts/ssh_client.py cat \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --path /etc/hosts
```

**创建目录**：
```bash
python scripts/ssh_client.py mkdir \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --path /home/new_dir
```

**删除文件**：
```bash
python scripts/ssh_client.py rm \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --path /home/old_file.txt
```

**重命名文件/目录**：
```bash
python scripts/ssh_client.py rename \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --old /home/old_name \
  --new /home/new_name
```

**修改权限**：
```bash
python scripts/ssh_client.py chmod \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password" \
  --path /home/script.sh \
  --mode 755
```

**交互式Shell**：
```bash
python scripts/ssh_client.py shell \
  --ssh-command "ssh -p 12345 root@192.168.1.1" \
  --password "your-password"
```

## 资源索引
- API客户端脚本：[scripts/compshare_client.py](scripts/compshare_client.py) - 封装所有API调用逻辑
- SSH客户端脚本：[scripts/ssh_client.py](scripts/ssh_client.py) - SSH连接和文件传输
- API详细参考：[references/api_reference.md](references/api_reference.md) - 完整的API参数说明和示例

## 注意事项
- 删除实例前必须先停止实例，否则会报错
- 密码需要符合平台规范，并通过 base64 编码传输
- GPU类型支持：4090、3080Ti、3090、A800、A100、H20等
- 地域和可用区固定为 cn-wlcb 和 cn-wlcb-01
- 所有API响应中的 RetCode=0 表示操作成功
- 配置文件包含敏感信息，请勿提交到版本控制系统
- SSH密码可通过查询实例列表获取（Password字段）
- SSH登录命令可通过查询实例列表获取（SshLoginCommand字段）
