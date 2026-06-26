# CMG 资源扫描 (cmg-scan)

扫描多云资源清单并导出 Excel 报表，用于云资源迁移前评估。

支持平台：阿里云、AWS（国际站/国内站）、华为云

产品代码速查：见 [{baseDir}/references/products.md]({baseDir}/references/products.md)

## 下载预编译包

所有平台的构建产物已上传至 COS，直接下载对应版本即可，无需自行编译。

基础地址：`https://msp-release-1258344699.cos.ap-shanghai.myqcloud.com/package/urp/`

### 阿里云

| 系统 | 架构 | 下载地址 |
|------|------|---------|
| macOS | Intel (amd64) | `aliyun-scanner-mac-amd64-1.0.0.tar.gz` |
| macOS | Apple Silicon (arm64) | `aliyun-scanner-mac-arm64-1.0.0.tar.gz` |
| Windows | amd64 | `aliyun-scanner-win-amd64-1.0.0.zip` |
| Linux | amd64 | `aliyun-scanner-linux-1.0.0.tar.gz` |

### AWS

AWS 分国际站和国内站两个版本（`-zh-` 为国内站版本）：

| 系统 | 架构 | 国际站 | 国内站 |
|------|------|--------|--------|
| macOS | Intel (amd64) | `aws-scanner-mac-amd64-1.0.0.tar.gz` | `aws-scanner-mac-amd64-zh-1.0.0.tar.gz` |
| macOS | Apple Silicon (arm64) | `aws-scanner-mac-arm64-1.0.0.tar.gz` | `aws-scanner-mac-arm64-zh-1.0.0.tar.gz` |
| Windows | amd64 | `aws-scanner-win-amd64-1.0.0.zip` | `aws-scanner-win-amd64-zh-1.0.0.zip` |
| Linux | amd64 | `aws-scanner-linux-1.0.0.tar.gz` | `aws-scanner-linux-zh-1.0.0.tar.gz` |

### 华为云

| 系统 | 架构 | 下载地址 |
|------|------|---------|
| macOS | Intel (amd64) | `huaweicloud-scanner-mac-amd64-1.0.0.tar.gz` |
| macOS | Apple Silicon (arm64) | `huaweicloud-scanner-mac-arm64-1.0.0.tar.gz` |
| Windows | amd64 | `huaweicloud-scanner-win-amd64-1.0.0.zip` |
| Linux | amd64 | `huaweicloud-scanner-linux-1.0.0.tar.gz` |

```bash
# 下载示例（以阿里云 macOS Apple Silicon 为例）
BASE=https://msp-release-1258344699.cos.ap-shanghai.myqcloud.com/package/urp
curl -O $BASE/aliyun-scanner-mac-arm64-1.0.0.tar.gz
tar -xzf aliyun-scanner-mac-arm64-1.0.0.tar.gz
# 解压后目录包含：aliyun-scanner（可执行文件）+ config.yaml（配置模板）
```

## 快速开始

解压后直接编辑 `config.yaml`，填入密钥和扫描范围，然后在**解压目录下**执行：

```bash
# -c 默认读取当前目录的 config.yaml，-o 默认输出到当前目录，均可省略
./aliyun-scanner
```

扫描完成后，当前目录生成 `aliyun_scan_xxxxxx.xlsx`，可将该文件作为后续选型推荐、TCO 分析的输入。

执行以下命令输出文字汇总（需要 Python3 + openpyxl）：

```bash
# 安装依赖（仅首次）
pip3 install openpyxl

python3 {baseDir}/scripts/summarize.py aliyun_scan_xxxxxx.xlsx
```

输出示例：
```
总实例数：12

【按产品】
  ECS          8 个
  RDS          4 个

【按地域】
  cn-hangzhou          6 个
  cn-beijing           4 个
  cn-shanghai          2 个
```

## 命令参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--conf` | `-c` | 配置文件路径 | - |

## 配置文件

解压包中自带 `config.yaml` 模板，直接编辑填写即可。

### 阿里云

```yaml
SecretId: 这里填写你的SecretId
SecretKey: 这里填写你的SecretKey

# 需要扫描地域，多个地域以英文逗号隔开。留空则自动扫描所有地域
# 可用地域：cn-qingdao, cn-beijing, cn-zhangjiakou, cn-huhehaote, cn-wulanchabu,
#           cn-hangzhou, cn-shanghai, cn-nanjing, cn-fuzhou, cn-wuhan-lr,
#           cn-shenzhen, cn-heyuan, cn-guangzhou, cn-chengdu, cn-hongkong
Regions: cn-hangzhou, cn-beijing

# 多个产品以英文逗号隔开。留空则扫描所有产品
# 支持：ack, acr, bh, cdn, ddos, dns, ecs, eip, emr, es, hbase, kafka,
#       mongodb, nas, nat, oss, polardb, polardbx, rabbitmq, ram, rds,
#       redis, rocketmq, slb, tsdb, vpc, vpn, waf, sas, ebs
Products: ecs, rds, vpc
```

### AWS

> ⚠️ **必须使用主账号扫描**，子账号即使有权限也会导致结果不完整。

```yaml
SecretId: 这里填写你的SecretId
SecretKey: 这里填写你的SecretKey

# 需要扫描地域，多个地域以英文逗号隔开。留空则自动扫描所有地域
# 地域列表参考：https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions
Regions:

# 多个产品以英文逗号隔开。留空则扫描所有产品
# 支持：apigateway, cloudfront, dns, dynamodb, ec2, ecr, efs, eks, elasticache,
#       elb, emr, es, kafka, mq, s3, sns, vpc, vpn, rds
Products: ec2
```

> 国内站与国际站配置格式相同，区别仅在于下载的包版本（`-zh-` 后缀）。

### 华为云

```yaml
SecretId: 这里填写你的SecretId
SecretKey: 这里填写你的SecretKey

# 需要扫描地域，多个地域以英文逗号隔开。留空则自动扫描所有地域
# 可用地域：cn-north-1, cn-north-2, cn-north-4, cn-north-9,
#           cn-east-2, cn-east-3, cn-east-4, cn-east-5,
#           cn-south-1, cn-south-2, cn-southwest-2
Regions:

# 多个产品以英文逗号隔开。留空则扫描所有产品
# 支持：ecs, rds, obs, dds, evs
Products:
```

## 常见问题

**Q: AWS 扫描结果不完整**
- 必须使用主账号，子账号即使有权限也会导致结果不全

**Q: 华为云鉴权失败**
- 密钥需要开放被扫描产品的**只读权限**

**Q: 扫描报 API 限流错误**
- 降低 `--req-rate` 参数（如 `--req-rate 10`）

**Q: 某些地域/产品无数据**
- 确认账号有对应地域/产品的只读权限
- 检查 Products 配置的产品代码拼写（参考 references/products.md）
