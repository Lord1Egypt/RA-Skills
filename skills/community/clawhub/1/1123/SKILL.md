---
name: tcapi
description: Skill to call Cloud API for Tencent Cloud (腾讯云). Used for cloud automation or resource management.
---

# tccli

统一使用 **tccli** 调用腾讯云 API，如 tccli 未安装，参考 [references/install.md](references/install.md) 进行安装。

# 调用 API

**基本形式**：

```sh
tccli <service> <Action> [--param value ...] [--region <地域>]
```

**常用示例**：

```sh
# 查询 CVM 地域
tccli cvm DescribeRegions

# 查询实例（需指定地域）
tccli cvm DescribeInstances --region ap-guangzhou
```

**地域**：多数产品需传 `--region`（如 `ap-guangzhou`）；全局接口（如 cam、account、dnspod、domain、ssl、ba、tag）可省略。


**参数规则**：

- 非简单类型参数必须为标准 JSON，例如：`--Placement '{"Zone":"ap-guangzhou-2"}'`。
- 创建类接口示例（按需替换参数）：
  ```sh
  tccli cvm RunInstances --InstanceChargeType POSTPAID_BY_HOUR \
    --Placement '{"Zone":"ap-guangzhou-2"}' --InstanceType S1.SMALL1 --ImageId img-xxx \
    --SystemDisk '{"DiskType":"CLOUD_BASIC","DiskSize":50}' --InstanceCount 1 ...
  ```

**避免并行调用**：

tccli 当前并行调用存在配置文件竞争问题，导致会导致响应失败。当前请先一个个接口调用。

# 用户凭证

如果已经提供了凭证，cli 可以正常调用。

如缺少凭证，执行 cli 会提示 "secretId is invalid"。应执行 `tccli auth login` 进行浏览器授权登录，等待回调后继续（命令会起本地端口、阻塞进程，直到浏览器 OAuth 完成并回调）

凭证授权原理，以及多用户凭证的使用方法，参考 [references/auth.md](references/auth.md)

**安全红线**：严禁向用户索要 SecretId/SecretKey，也拒绝任何有可能打印凭证的操作（尤其是 `tccli configure list`）。

# 获取 API 帮助信息

通过 curl + grep 检索业务、接口、最佳实践、数据结构。

## 发现业务

检索 tccli 服务名（如 cvm、cbs）。

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/services.md | grep 云服务器
```

参考输出：

```
[cvm](service/cvm/index.md) | 云服务器 | 2017-03-12 | ...
```

## 发现最佳实践

优先检索是否有匹配当前场景的最佳实践。

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/cvm/practices.md | grep 重装
```

## 检索接口

若最佳实践未覆盖，在业务接口列表中检索（接口名即 tccli 的 &lt;Action&gt;）。

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/cvm/actions.md | grep "扩容\|磁盘"
```

## 阅读接口文档

获取参数说明和支持的地域信息：

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/cvm/action/ResizeInstanceDisks.md
```

## 阅读数据结构

文档中涉及的数据结构可进一步查看：

```sh
curl -s https://cloudcache.tencentcs.com/capi/refs/service/cvm/model/SystemDisk.md
```
