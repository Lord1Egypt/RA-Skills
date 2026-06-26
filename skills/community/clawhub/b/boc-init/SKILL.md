---
name: boc-init
description: 博云BOC容器平台 部署机初始化工具。自动完成部署机环境检查、部署包校验、解压和 bocctl init 初始化。使用场景：用户需要初始化 BOC容器平台 部署机时使用。
version: 1.0.1
icon: 🚀
---

# BOC 部署机初始化

自动化完成 博云BOC容器平台 部署机的初始化工作。

## 输入参数

| 参数 | 说明 | 示例 |
|------|------|------|
| deploy_pkg_dir | 部署包和校验文件所在目录 | /opt |
| deploy_pkg_file | 部署包文件名 | BOC.tar.gz |
| ssh_host | 部署机IP | <部署机IP> |
| ssh_port | SSH端口 | 22 |
| ssh_user | SSH用户名 | root |
| ssh_password | SSH密码 | Password |

## 工作流程

### 1. 环境检查

连接部署机并检查：
- 主机名
- 操作系统版本
- 内核版本
- DNS配置
- 磁盘空间（/var 目录至少50GB）
- 部署包是否存在

### 2. 部署包校验

执行 SHA256 校验：
```bash
nohup cd <deploy_pkg_dir> && sha256sum <deploy_pkg_file>.sha256 > /tmp/sha256sum-<deploy_pkg_file>.txt
```
定期检查校验结果
```bash
cat /tmp/sha256sum-<deploy_pkg_file>.txt
```
判断标准: 结果中有 "<deploy_pkg_file>: 成功" 
 

### 3. 解压部署包

**重要**：解压前需先清理旧目录，避免残留文件导致问题：
```bash
# 解压前先清理旧目录
cd <deploy_pkg_dir>
test -d BOC_k8s_noarch && rm -rf BOC_k8s_noarch

# 后台执行解压（30GB文件预计15-20分钟）
nohup tar -xzf <deploy_pkg_file> > /tmp/unpack.log 2>&1 &

# 定期检查解压，通过进程判断
## 1 检查是否有以下进程，有就代表还在解压
ps aux |grep 'tar -xzf <deploy_pkg_file>'

## 2 没有就再检查/opt/BOC_k8s_noarch  占用空间正常应该在 31GB
du -sh /opt/BOC_k8s_noarch
```


### 4. 验证解压结果

解压后的正确目录结构：
```
/opt/BOC_k8s_noarch/
├── bocctl           # 主程序
├── bocctl_lib       # 库文件
├── images           # 镜像文件
├── packages         # 安装包
├── playbooks        # Ansible playbook
```


### 5. 执行 bocctl init

后台执行初始化（预计15-20分钟）：
```bash
cd <deploy_dir>
nohup ./bocctl init > /tmp/bocctl_init.log 2>&1 &
# 定期检查bocctl 进程是否存在，如存在代表init 还在进行
# 也一块检查执行日志
pa aux |grep bocctl 
tail -n 20 /opt/BOC_k8s_noarch/log/bocctl.log 
```



### 6. 验证初始化完成

**判断标准**：使用 `nerdctl ps` 检查以下两个容器是否正常运行：
```bash
nerdctl -n k8s.io ps | grep -E "(yum_registry|bocloud_deploy_registry)"
```

预期输出应包含：
- `yum_registry` 容器 - 运行中
- `bocloud_deploy_registry_k8s` 容器 - 运行中

## 使用示例

```
请使用 boc-init 初始化部署机：
- 部署包目录：/opt
- 部署包文件：BOC.tar.gz
- 部署机IP：10.50.6.181
- SSH端口：22
- SSH用户：root
- SSH密码：password
```

## 输出

- 部署机初始化完成状态
- 初始化后关键组件状态：
  - ansible 版本
  - nerdctl 容器运行状态（yum_registry 和 bocloud_deploy_registry_k8s）
  - containerd 服务状态

## 常见问题

### Q: 解压后目录结构异常
A: 重新执行解压，确保先删除旧目录

### Q: bocctl init 卡住不动
A: 检查是否有 yum 进程卡住，如有则杀掉后重试


### Q: 忽略./bocctl 参数参考
A：忽略./bocctl 参数参考，只使用./bocctl init 。不需要远程初始化部署，只用本地初始化。


### Q: 本地执行前置条件
A： 需要安装node 才能使用rssh2 skill 
    需要安装python 才能使用ssh-exec skill
    windows 系统需要安装git for windows 

### Q: ssh 使用密码连接问题解决
A: 如果安装了python ，优先使用ssh-exec skill
   如安装了node ，优先使用rssh2 skill
   先检查操作系统中是否有sshpass ，没有就参考以下处理：
   windows下sshpass 从 https://github.com/xhcoding/sshpass-win32/releases/download/v1.0.7/sshpass.exe  下载使用
   Linux 下使用pip install sshpass -g 进行安装 

