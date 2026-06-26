#!/bin/bash
# 查询 RC 实例（Custom 实例）脚本
# 用法：./query_rc_instances.sh [地域]

REGION="${1:-cn-beijing}"

echo "=== RC 实例列表 ($REGION) ==="
echo ""

# 获取实例数据
RESULT=$(aliyun rds DescribeRCInstances --region "$REGION" 2>&1)

# 检查是否有错误
if echo "$RESULT" | grep -q "ERROR"; then
    echo "❌ 查询失败："
    echo "$RESULT"
    exit 1
fi

# 解析并显示实例信息
TOTAL=$(echo "$RESULT" | jq -r '.TotalCount')

if [ "$TOTAL" == "0" ] || [ -z "$TOTAL" ]; then
    echo "当前地域 ($REGION) 没有 RC 实例"
    exit 0
fi

# 遍历每个实例
echo "$RESULT" | jq -r '.RCInstances[] | 
"实例 ID: \(.InstanceId)
实例名称：\(.InstanceName)
集群名称：\(.ClusterName // "N/A")
状态：\(.Status)
CPU: \(.Cpu) 核
内存：\((.Memory / 1024) | floor) GB
地域：\(.RegionId)
可用区：\(.ZoneId)
私网 IP: \(.VpcAttributes.PrivateIpAddress[0] // .HostIp // "N/A")
VPC: \(.VpcId // .VpcAttributes.VpcId // "N/A")
计费方式：\(.InstanceChargeType)
创建时间：\(.GmtCreated)
到期时间：\(.ExpiredTime)
"'

echo "总计：$TOTAL 台实例"
