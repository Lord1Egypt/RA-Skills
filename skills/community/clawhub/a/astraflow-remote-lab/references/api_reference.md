# UCloud CLI 与 API 常用运维命令速查

本文档梳理了在 UCloud 各地域管理云主机（UHost）与网络资源所需的高频命令，便于快速查询与排错。

---

## 1. VPC 专有网络与子网查询

在创建 UHost 实例前，必须获取目标地域有效的 `--vpc-id` 和 `--subnet-id`：

```bash
# 查询洛杉矶地域（us-ca）的全部 VPC
ucloud vpc list --region us-ca

# 查询洛杉矶地域（us-ca）的全部子网
ucloud subnet list --region us-ca

# 典型输出示例：
# SubnetName      ResourceID           Group    AffiliatedVPC                  NetworkSegment
# DefaultNetwork  subnet-xxxxxxxxxxxx  Default  uvnet-xxxxxxxxxxxx/DefaultVPC  10.11.0.0/16
```

---

## 2. 操作系统镜像查询

查询目标地域支持的官方镜像 ID（如 Windows Server 或 Linux）：

```bash
# 查询洛杉矶地域的 Windows Server 2022 镜像
ucloud image list --region us-ca | grep -iE 'Windows 2022'

# 查询所有可用的 Windows 系列镜像（2019/2022/2016）
ucloud image list --region us-ca | grep -B 2 -A 8 'Windows'

# us-ca 地域常用镜像 ID 参考：
# - Windows 2022 64位 英文版: uimage-1lbecold88le
# - Windows 2022 64位 中文版: uimage-1l8xtbvi7myz
# - CentOS Stream 9 64位:     uimage-1vfkh4bwbzea
```

---

## 3. UHost 云主机生命周期管理

```bash
# 列出洛杉矶地域的所有云主机
ucloud uhost list --region us-ca

# 启动实例
ucloud uhost start --uhost-id <UHOST_ID> --region us-ca

# 优雅关机
ucloud uhost stop --uhost-id <UHOST_ID> --region us-ca

# 强制断电关机
ucloud uhost poweroff --uhost-id <UHOST_ID> --region us-ca

# 销毁/删除云主机（停止计费，数据不可恢复）
ucloud uhost delete --uhost-id <UHOST_ID> --region us-ca
```

---

## 4. 弹性公网 IP (EIP) 管理

```bash
# 查看洛杉矶地域的所有 EIP
ucloud eip list --region us-ca

# 在 us-ca 申请一个国际线路（International）按时计费（Dynamic）EIP，带宽 5Mbps
ucloud eip allocate --region us-ca --line International --bandwidth-mb 5 --charge-type Dynamic

# 绑定 EIP 到指定的云主机
ucloud eip bind --eip-id <EIP_ID> --resource-id <UHOST_ID> --region us-ca

# 从云主机解绑 EIP
ucloud eip unbind --eip-id <EIP_ID> --region us-ca

# 释放 EIP（停止计费）
ucloud eip release --eip-id <EIP_ID> --region us-ca
```

---

## 5. 外网防火墙安全组规则

Windows 云主机若需支持 RDP 连接，必须放行入站 TCP 3389 端口：

```bash
# 查看 us-ca 地域的防火墙列表
ucloud firewall list --region us-ca

# 推荐的安全组规则通常放行：
# - TCP 22 (Linux SSH)
# - TCP 3389 (Windows RDP 远程桌面)
# - TCP 80 / 443 (HTTP / HTTPS 网页服务)
# - ICMP (Ping 网络探测)
```
