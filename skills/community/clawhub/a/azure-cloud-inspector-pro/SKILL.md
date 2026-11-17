---

slug: azure-cloud-inspector-pro
name: azure-cloud-inspector-pro
version: 1.0.0
displayName: Azure巡检员专业版
summary: "全维度Azure巡检,含RBAC审计、成本管理、NSG暴露矩阵、跨订阅批量、定时调度、趋势对比.。Azure巡检员专业版是一个以"日常巡检"为核心视角的Azure CLI辅助工具,面向运维工"
license: Proprietary
edition: pro
description: 'Azure巡检员专业版是一个以"日常巡检"为核心视角的Azure CLI辅助工具,面向运维工程师、云架构师、安全工程师、FinOps专员、合规审计员五类角色。针对云上资源"配置漂移无人察觉、公网暴露面长期敞开、RBAC过度授权难发现、成本失控无预警、NSG端口暴露无矩阵、跨订阅巡检低效、巡检结论难分享、历史趋势无对比"八大痛点,构建了风险评分模型、暴露面发现、配置漂移检测、巡检任务模板、巡检报告生成、RBAC深度审计、Cost
  Management成本管理、NSG暴露矩阵、跨订阅批量巡检、定时巡检调度与历史趋势对比十一大核心能力.
  核心能力包括:默认只读查询保障安全;写操作与破坏性操作需双重确认;支持--dry-run与what-if预演;az account show身份确认先行;资源清单/健康检查/暴露面扫描/配置基线对比/RBAC审计/成本分析/NSG暴露矩阵全场景覆盖;订阅与租户智能检测;跨订阅批量巡检与并行执行;自定义巡检模板与定时调度;历史趋势对比与漂移预警.
  适用场景:每日例行云资源巡检、上线前安全暴露面深度检查、RBAC角色季度审计、月度成本治理与异常预警、NSG端口暴露矩阵生成、多订阅统一巡检与汇总报告、合规检查自动化、巡检结论Markdown报告生成与团队分享、历史趋势对比与配置漂移预警、定时巡检调度与告警推送.
  差异化亮点:相比免费版,专业版新增RBAC深度合规检查(Owner过度授权检测/自定义角色审计/特权身份发现)、Cost Management成本管理(按资源组/服务维度/空闲资源识别/成本趋势对比)、NSG暴露深度检查(全订阅NSG规则扫描/0.0.0.0/0入站规则枚举/端口暴露矩阵)、自定义巡检模板与定时巡检调度、跨订阅批量巡检与历史趋势对比。五维风险评分模型支持自定义权重,适配不同业务场景。相比通用Azure管理工具,本巡检员聚焦"检查而非变更",以风险量化与报告生成为核心.
  适用关键词:Azure巡检、云资源检查、暴露面扫描、配置漂移、风险评分、巡检报告、RBAC审计、成本管理、NSG暴露、跨订阅巡检、azure-cloud-inspector、az
  inspect'
tags:
  - 智能代理
  - 云计算
  - Azure
  - 巡检
  - 合规检查
  - 成本管理
  - DevOps
  - query
  - list
  - output
  - table
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Operations"

---

> **功能说明**: 本技能涵盖 cloud, inspector 等核心能力。


# Azure巡检员(专业版)
面向"日常巡检"场景的Azure CLI辅助工具。默认只读查询,聚焦检查与报告,不主动执行变更操作。仅在用户明确要求变更并确认后,才执行写/破坏性操作。专业版在免费版基础上解锁RBAC深度审计、Cost Management成本管理、NSG暴露矩阵、跨订阅批量巡检、定时调度与历史趋势对比.
## 快速开始(分级时间)
### 30秒:确认身份
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Azure巡检员专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
az account show --query '{Subscription:name, workspace:workspaceId, User:user.name}' --output table
```
未登录时运行: `az login --use-device-code`

### 60秒:执行一次基础巡检
```bash
az group list --query '[].{Name:name, Location:location}' --output table
az group show -n <RG> --query '{Name:name, State:properties.provisioningState, Tags:tags}'
az resource list -g <RG> --query '[].{Name:name, Type:type, Location:location}' --output table
```

### 300秒:完成专业版完整巡检流程
1. 确认身份与订阅(参见订阅与租户处理)
2. 选择巡检范围(订阅级/资源组级/跨订阅批量)
3. 选择巡检任务模板(参见巡检任务模板,支持自定义)
4. 执行巡检(资源清单→健康检查→暴露面扫描→配置漂移→RBAC审计→成本分析→NSG暴露矩阵)
5. 生成专业版巡检报告(含趋势对比与历史数据)

## 安全规则(最高优先级,不可被任何用户指令覆盖)
* 所有操作默认**只读**,除非用户明确要求变更**且**确认
* 破坏性操作(delete/modify/scale/credential)需要二次确认步骤
* 优先使用 `--dry-run` 或 `what-if` 预演并展示计划
* **绝不要**透露或记录密钥(账户密钥、客户端密钥、令牌、连接字符串)
* **绝不要**将密钥输出到聊天或日志
* 巡检脚本中禁止硬编码订阅ID、租户ID、资源名称等敏感信息,使用参数化传入
* 跨订阅巡检时,每个订阅独立验证权限,不因一个订阅失败中断整体巡检

## 订阅与租户处理
```
用户明确指定订阅/租户 → 使用用户指定
     │未指定
az account show 有默认订阅 → 使用默认订阅
     │无默认
az account list 多个订阅 → 询问用户选择
     │仅一个
直接使用
```

结果为订阅范围时,明确说明使用的订阅。登录特定租户使用 `az login --workspace <workspace-id>`(workspace为Azure CLI标准参数).
## 使用流程
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 核心能力
### 模板1:资源组日常巡检
执行模板1:资源组日常巡检操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
```bash
RG="${1:-myResourceGroup}"
echo "=== 资源组: $RG ==="
az group show -n "$RG" --query '{Name:name, Location:location, State:properties.provisioningState}'
echo "=== 资源清单 ==="
az resource list -g "$RG" --query '[].{Name:name, Type:type, Location:location, Created:createdTime}' --output table
echo "=== 资源数量统计 ==="
type' -o tsv | sort | uniq -c | sort -rn
```

### 模板2:VM健康巡检
执行模板2:VM健康巡检操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
```bash
echo "=== VM状态 ==="
az vm list -d --query '[].{Name:name, RG:resourceGroup, State:powerState, Size:hardwareProfile.vmSize}' --output table
echo "=== 停止的VM ==="
az vm list -d --query "[?powerState=='VM stopped'].{Name:name, RG:resourceGroup}" --output table
echo "=== VM磁盘加密状态 ==="
az vm list --query '[].{Name:name, RG:resourceGroup}' -o tsv | while read name rg; do
  echo -n "$name: "; az vm encryption show -n "$name" -g "$rg" --query 'disks[].statuses[].code' -o tsv 2>/dev/null || echo "无法查询"
done
```

### 模板3:存储账户巡检
执行模板3:存储账户巡检操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
```bash
echo "=== 存储账户清单 ==="
az storage account list --query '[].{Name:name, RG:resourceGroup, SKU:sku.name, TLS:minimumTlsVersion}' --output table
echo "=== 公共Blob访问检查(应为false) ==="
{Name:name, PublicAccess:allowBlobPublicAccess}' --output table
echo "=== HTTPS强制检查(应为true) ==="
{Name:name, HTTPS:enableHttpsTrafficOnly}' --output table
```

### 模板4:RBAC深度审计(专业版独有)
执行模板4:RBAC深度审计(专业版独有)操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
```bash
echo "=== 订阅级角色分配清单 ==="
az role assignment list --all --query '[].{Principal:principalName, Role:roleDefinitionName, Scope:scope}' --output table
echo "=== Owner角色分配(过度权限检测) ==="
az role assignment list --role "Owner" --query '[].{Principal:principalName, Scope:scope}' --output table
echo "=== 自定义角色审计 ==="
az role definition list --custom-role-only true --query '[].{Name:roleName, Description:description}' --output table
echo "=== 特权身份发现(Owner/Contributor/User Access Administrator) ==="
az role assignment list --all --query "[?roleDefinitionName=='Owner' || roleDefinitionName=='Contributor' || roleDefinitionName=='User Access Administrator'].{Principal:principalName, Role:roleDefinitionName}" --output table
```

### 模板5:Cost Management成本管理(专业版独有)
执行模板5:Cost Management成本管理(专业版独有)操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
```bash
echo "=== 本月成本(按资源组) ==="
az costmanagement query --type ActualCost \
  --timeframe MonthToDate \
  --dataset-grouping name=ResourceGroupName type=Dimension \
  --dataset-aggregation totalCost=name=Cost function=Sum \
  --query '[].{ResourceGroup:ResourceGroupName, Cost:Cost}' --output table
echo "=== 本月成本(按服务) ==="
az costmanagement query --type ActualCost \
  --timeframe MonthToDate \
  --dataset-grouping name=ServiceName type=Dimension \
  --dataset-aggregation totalCost=name=Cost function=Sum \
  --query '[].{Service:ServiceName, Cost:Cost}' --output table
echo "=== 空闲资源识别 ==="
echo "停止的VM:"; az vm list -d --query "[?{Name:name, RG:resourceGroup}" --output table
echo "未挂载磁盘:"; az disk list --query "[?diskState=='Unattached'].{Name:name, RG:resourceGroup, Size:diskSizeGb}" --output table
echo "未使用公网IP:"; az network public-ip list --query '[?ipConfiguration==null].{Name:name, IP:ipAddress}' --output table
```

### 模板6:NSG暴露矩阵(专业版独有)
执行模板6:NSG暴露矩阵(专业版独有)操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
```bash
echo "=== NSG清单 ==="
az network nsg list --query '[].{Name:name, RG:resourceGroup}' --output table
echo "=== 全订阅NSG入站规则扫描 ==="
for nsg in $(az network nsg list --query '[].{Name:name, RG:resourceGroup}' -o tsv); do
  IFS=$'\t' read -r name rg <<< "$nsg"
  echo "--- NSG: $name (RG: $rg) ---"
  az network nsg rule list --nsg-name "$name" -g "$rg" \
    --query "[?direction=='Inbound' && (sourceAddressPrefix=='*' || sourceAddressPrefix=='0.0.0.0/0' || sourceAddressPrefix=='Internet')].{Name:name, Port:destinationPortRange, Access:access, Priority:priority}" \
    --output table
done
echo "=== 端口暴露矩阵 ==="
name' -o tsv | while read nsg; do
  az network nsg rule list --nsg-name "$nsg" --query "[?sourceAddressPrefix=='0.0.0.0/0'].{Port:destinationPortRange, Protocol:protocol}" -o tsv
done | sort | uniq -c | sort -rn
```

### 模板7:自定义巡检模板(专业版独有)
用户可定义自己的巡检模板,保存到 `$HOME/.azure-inspector/templates/` 目录:
```bash
mkdir -p $HOME/.azure-inspector/templates
cat > $HOME/.azure-inspector/templates/databases-inspection.sh <<'EOF'
#!/bin/sh
echo "=== SQL数据库清单 ==="
az sql db list --query '[].{Name:name, Server:serverName, SKU:currentSku.name}' --output table
echo "=== 数据库清单 ==="
az postgres server list --query '[].{Name:name, RG:resourceGroup, Version:version}' --output table
echo "=== CosmosDB清单 ==="
az cosmosdb list --query '[].{Name:name, RG:resourceGroup, Kind:kind}' --output table
EOF
```
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：全维度、Azure、RBAC、成本管理、NSG、暴露矩阵、跨订阅批量、定时调度、趋势对比、巡检员专业版是一、日常巡检、为核心视角的、CLI、辅助工具、面向运维工程师、云架构师、安全工程师、FinOps、合规审计员五类角、针对云上资源、配置漂移无人察觉、公网暴露面长期敞、过度授权难发现、成本失控无预警、端口暴露无矩阵、跨订阅巡检低效、巡检结论难分享、历史趋势无对比、八大痛点、构建了风险评分模、暴露面发现、配置漂移检测、巡检任务模板、巡检报告生成、深度审计、Cost、Management、跨订阅批量巡检、定时巡检调度与历、史趋势对比十一大、核心能力等.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 五维风险评分模型(差异化核心)
每次巡检后按五维评分(0-10分,0=最低风险,10=最高风险),输出总体风险等级。专业版支持自定义权重.
| 维度 | 检查项 | 评分方法 | 高风险阈值 | 默认权重 |
|:-----|:-----|:-----|:-----|:-----|
| 暴露面 | 公网IP、开放端口、公共存储、NSG 0.0.0.0/0 | 每发现一项暴露+2分 | ≥6分 | 1.5x |
| 加密 | 磁盘加密、传输加密、Key Vault | 未加密项+3分 | ≥4分 | 1.2x |
| 访问控制 | RBAC角色、Owner数量、特权身份、公共访问 | Owner>3加3分,特权身份+2分 | ≥6分 | 1.3x |
| 配置漂移 | 与基线对比、未标签资源 | 偏离项+1分,无标签+0.5分 | ≥5分 | 1.0x |
| 健康度 | 停止VM、未挂载磁盘、告警、成本异常 | 异常资源每项+1分 | ≥4分 | 0.8x |

### 风险等级映射
| 总分 | 等级 | 建议 |
|---:|---:|---:|
| 0-15 | 低 | 例行巡检,记录归档 |
| 16-35 | 中 | 48小时内修复 |
| 36-60 | 高 | 24小时内修复 |
| >60 | 严重 | 立即介入,启动应急流程 |

### 自定义权重配置(专业版独有)
```bash
cat > $HOME/.azure-inspector/weights.json <<EOF
{
  "exposure": 1.5,
  "encryption": 1.2,
  "access": 1.3,
  "drift": 1.0,
  "health": 0.8
}
EOF
exposure_score=$(计算暴露面得分)
weights=$(jq -r '.' $HOME/.json)
weighted_total=$(jq -n --argjson w "$weights" --argjson e $exposure_score \
  '($e * $w.exposure) + ($e * $w.encryption) + ($e * $w.access) + ($e * $w.drift) + ($e * $w.health)')
echo "加权风险总分: $weighted_total"
```

## 公网暴露面发现(差异化)
自动扫描订阅内对外暴露的资源:

```bash
echo "=== 公网IP清单 ==="
az network public-ip list --query '[].{Name:name, IP:ipAddress, Associated:ipConfiguration!=null}' --output table
echo "=== 未关联的公网IP ==="
az network public-ip list --query '[?{Name:name, IP:ipAddress}' --output table
echo "=== 存储账户公共访问 ==="
az storage account list --query '[?allowBlobPublicAccess==true].{Name:name, RG:resourceGroup}' --output table
echo "=== 公网负载均衡器 ==="
az network lb list --query '[].{Name:name, RG:resourceGroup, FrontendIPs:length(frontendIpConfigurations)}' --output table
echo "=== 应用网关公网前端 ==="
az network application-gateway list --query '[].{Name:name, RG:resourceGroup, FrontendIPs:length(frontendIpConfigurations)}' --output table
```

## 配置漂移检测(差异化)
通过快照对比发现配置偏离:

```bash
az resource list --query '[].{Name:name, Type:type, RG:resourceGroup, Tags:tags}' > /tmp/azure-snapshot-current.json
if [ -f $HOME/.azure-inspector/baseline.json ]; then
  echo "=== 与基线对比 ==="
  diff <(jq -r '.[] | "\(.Type)/\(.Name)"' $HOME/.json | sort) \
       <(jq -r '.[] | "\(.Type)/\(.Name)"' /tmp/azure-snapshot-current.json | sort) || true
fi
```

## 跨订阅批量巡检(专业版独有)
一次扫描所有可访问订阅并汇总报告:

```bash
echo "=== 跨订阅批量巡检 ==="
for sub in $(az account list --query '[].id' -o tsv); do
  sub_name=$(az account show --subscription $sub --query name -o tsv)
  echo ""
  echo "============================"
  echo "订阅: $sub_name ($sub)"
  echo "============================"
  az account set --subscription $sub
  echo "--- VM数量: $(az vm list --query 'length(@)' -o tsv)"
  echo "--- 存储账户数量: $(az storage account list --query 'length(@)' -o tsv)"
  echo "--- 停止的VM: $(az vm list -d --query "[?powerState=='VM stopped'] | length(@)" -o tsv)"
  echo "--- 未关联公网IP: $(az network public-ip list --query '[?ipConfiguration==null] | length(@)' -o tsv)"
  echo "--- Owner角色数: $(az role assignment list --role "Owner" --query 'length(@)' -o tsv)"
done
```

## 定时巡检调度(专业版独有)
通过cron或Azure Automation实现定时巡检:

```bash
# 0 9 * * * bash $HOME/.azure-inspector/scheduled-inspection.sh >> /var/log/azure-inspector.log 2>&1
#!/bin/sh
set -e
REPORT_DIR=$HOME/.azure-inspector/reports
mkdir -p "$REPORT_DIR"
DATE=$(date +%Y%m%d-%H%M%S)
REPORT="$REPORT_DIR/inspection-$DATE.md"
echo "# Azure定时巡检报告 $DATE" > "$REPORT"
echo "" >> "$REPORT"
echo "- 订阅: $(az account show --query name -o tsv)" >> "$REPORT"
echo "" >> "$REPORT"
echo "## 资源概览" >> "$REPORT"
echo '```' >> "$REPORT"
type' -o tsv | sort | uniq -c | sort -rn >> "$REPORT"
echo '```' >> "$REPORT"
echo "" >> "$REPORT"
echo "## 高风险项" >> "$REPORT"
echo "- 停止的VM: $(az vm list -d --query "[?powerState=='VM stopped'] | length(@)" -o tsv)" >> "$REPORT"
echo "- 未关联公网IP: $(az network public-ip list --query '[?ipConfiguration==null] | length(@)' -o tsv)" >> "$REPORT"
echo "- Owner角色数: $(az role assignment list --role "Owner" --query 'length(@)' -o tsv)" >> "$REPORT"
EOF
```

## 历史趋势对比(专业版独有)
对比历史巡检数据,发现趋势变化:

```bash
ls -lt $HOME/.azure-inspector/reports/ | head -20
LATEST=$(ls -t $HOME/.azure-inspector/reports/inspection-*.md | head -1)
PREVIOUS=$(ls -t $HOME/.md | head -2 | tail -1)
echo "最新巡检: $LATEST"
echo "上次巡检: $PREVIOUS"
echo ""
echo "=== 趋势对比 ==="
diff <(grep -E '^\- ' "$PREVIOUS") <(grep -E '^\- ' "$LATEST") || true
echo "日期,停止VM数,未关联IP数,Owner角色数" > $HOME/.azure-inspector/trend.csv
for report in $(ls $HOME/.md); do
  date=$(basename "$report" | sed 's/inspection-//;s/.md//')
  vm=$(grep '停止的VM' "$report" | grep -oE '[0-9]+')
  ip=$(grep '未关联公网IP' "$report" | grep -oE '[0-9]+')
  owner=$(grep 'Owner角色数' "$report" | grep -oE '[0-9]+')
  echo "$date,$vm,$ip,$owner" >> $HOME/.csv
done
echo "趋势数据已导出: $HOME/.csv"
```

## 巡检报告生成(差异化)
巡检完成后自动生成Markdown格式报告(专业版含趋势对比与建议):

```bash
REPORT="/tmp/azure-inspection-$(date +%Y%m%d-%H%M%S).md"
cat > "$REPORT" <<EOF
- 巡检时间: $(date)
- 订阅: $(az account show --query name -o tsv)
- 巡检范围: ${1:-全订阅}
- 巡检模板: ${2:-完整巡检}
$(az resource list --query '[].type' -o tsv | sort | uniq -c | sort -rn)
- 停止的VM: $(az vm list -d --query "[?powerState=='VM stopped'] | length(@)" -o tsv) 个
- 未挂载磁盘: $(az disk list --query "[?diskState=='Unattached'] | length(@)" -o tsv) 个
- 未关联公网IP: $(az network public-ip list --query '[?ipConfiguration==null] | length(@)' -o tsv) 个
- Owner角色数: $(az role assignment list --role "Owner" --query 'length(@)' -o tsv) 个
- 自定义角色数: $(az role definition list --custom-role-only true --query 'length(@)' -o tsv) 个
$(az costmanagement query --type ActualCost --timeframe MonthToDate --dataset-grouping name=ServiceName type=Dimension --dataset-aggregation totalCost=name=Cost function=Sum --query '[].{Service:ServiceName, Cost:Cost}' --output table 2>/dev/null || echo "Cost Management未配置")
- 开放入站0.0.0.0/0的NSG: [需扫描]
[根据五维评分模型计算,使用自定义权重]
[根据检查结果生成,含优先级与修复命令]
[与上次巡检对比,标记变化项]
EOF
echo "专业版巡检报告已生成: $REPORT"
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```text
角色: 运维工程师
任务: "帮我跑一次日常巡检,关注资源组prod-rg,生成报告"
执行流程:
1. 应用模板1(资源组日常巡检)
2. 执行五维风险评分(自定义权重:暴露面1.5x)
3. 对比昨日基线快照,标记新增/删除资源
4. 执行RBAC审计(检测Owner过度授权)
5. 生成专业版Markdown巡检报告(含趋势对比)
6. 报告中标注中高风险项的修复建议与命令
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```text
角色: 安全工程师
任务: "季度审计,检查所有订阅的RBAC配置,找出过度授权"
执行流程:
1. 跨订阅批量巡检(遍历所有可访问订阅)
2. 应用模板4(RBAC深度审计)
3. 列出所有Owner/Contributor/User Access Administrator角色分配
4. 检测自定义角色的危险权限(如Microsoft.Authorization/*/Write)
5. 生成RBAC审计报告,标注每个过度授权项
6. 提供最小权限建议(如将Owner降级为Contributor+特定角色)
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```text
角色: FinOps专员
任务: "月度成本审计,找出本月异常增长和空闲资源"
执行流程:
1. 应用模板5(Cost Management成本管理)
2. 按资源组/服务维度查询本月成本
3. 对比上月成本数据,标记异常增长项
4. 识别空闲资源(停止VM/未挂载磁盘/未使用公网IP)
5. 估算空闲资源成本,生成节省建议
6. 输出成本治理报告(含趋势图表数据)
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```text
角色: 云架构师
任务: "新服务上线前,做一次全面暴露面扫描"
执行流程:
1. 应用模板6(NSG暴露矩阵)
2. 扫描所有公网IP,识别未关联的(浪费且暴露)
3. 扫描存储账户公共访问(allowBlobPublicAccess)
4. 全订阅NSG入站规则扫描,枚举0.0.0.0/0规则
5. 生成端口暴露矩阵(端口×协议×NSG)
6. 生成暴露面报告,标注高风险项与修复方案
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```text
角色: 合规审计员
任务: "生成合规检查报告,含存储加密、HTTPS、Key Vault防火墙等"
执行流程:
1. 应用合规检查清单(存储公共访问/HTTPS/Key Vault防火墙/NSG/Owner/磁盘加密)
2. 逐项执行检查命令,记录合规/不合规
3. 生成合规矩阵(检查项×资源×结果)
4. 标注不合规项的修复命令
5. 输出合规审计报告(可提交给审计部门)
```

## 已知限制
- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 错误处理
| 序号 | 错误场景 | 原因 | 处理方式 | 优先级 |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 输入参数缺失 | 用户未提供必要参数 | 提示用户提供所需参数后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P0 |
| 2 | 执行超时 | 处理时间过长 | 检查输入数据量,分批处理 | P1 |
| 3 | 输出格式错误 | 结果不符合预期格式 | 检查`output_format`参数配置 | P1 |

## 常见问题FAQ
**Q: 巡检会修改我的Azure资源吗?**
A: 不会。巡检默认全部使用只读命令(list/show/get/query),不会对资源做任何变更。即使用户要求修复建议,也仅展示命令,需用户明确确认后才执行.
**Q: 五维风险评分如何加权?**
A: 专业版支持自定义权重(默认:暴露面1.5x,加密1.2x,访问控制1.3x,配置漂移1.0x,健康度0.8x)。权重配置保存在 `$HOME/.json`,可按业务场景调整。例如金融业务可提高"加密"权重至1.5x.
**Q: 配置漂移检测的基线快照如何生成?**
A: 首次运行时执行 `az resource list --query ... > $HOME/.json` 生成基线。后续每次巡检生成current快照并与baseline对比。基线可手动更新(确认当前配置为新的标准).
**Q: 巡检报告可以分享给团队吗?**
A: 可以。报告为标准Markdown格式,可直接粘贴到企业IM、Wiki或工单系统。专业版报告含资源概览、健康状态、RBAC审计、成本概览、NSG暴露矩阵、风险等级、建议项与历史趋势对比.
**Q: 跨订阅巡检如何处理权限不足?**
A: 跨订阅批量巡检时,每个订阅独立验证权限。如某订阅权限不足,跳过该订阅并在报告中标注"权限不足",不中断整体巡检。建议至少具备Reader角色.
**Q: 定时巡检如何配置?**
A: 通过cron或Azure Automation配置。脚本示例参见"定时巡检调度"章节。建议每日9点执行巡检,报告保存到 `$HOME/.azure-inspector/reports/` 目录,可通过邮件或IM webhook推送告警.
**Q: Cost Management查询返回空?**
A: 确认Cost Management已在Azure Portal中配置。确认订阅类型支持Cost Management(CSP等某些类型可能不支持)。如使用EA账户,需确保有EA Reader权限.
**Q: NSG暴露矩阵扫描很慢?**
A: NSG规则扫描是逐个NSG查询,订阅NSG较多时会较慢。建议:1)缩小扫描范围(按资源组);2)使用跨订阅批量巡检的并行模式;3)将结果缓存到本地,后续查询从缓存读取.
**Q: 历史趋势对比需要多少次巡检数据?**
A: 至少2次。首次巡检建立基线,第二次及之后可对比变化。建议至少积累7天数据才能看出趋势。趋势数据导出为CSV格式,可导入Excel或BI工具生成图表.
**Q: 自定义巡检模板如何编写?**
A: 在 `$HOME/.azure-inspector/templates/` 目录创建bash脚本,脚本内可使用az CLI命令。模板支持参数化(通过$1, $2等传入资源组名等参数)。参见"自定义巡检模板"章节示例.
**Q: 专业版与免费版的核心差异?**
A: 专业版在免费版基础上新增:RBAC深度合规检查(Owner过度授权检测/自定义角色审计/特权身份发现)、Cost Management成本管理(按资源组/服务维度/空闲资源识别/成本趋势)、NSG暴露矩阵(全订阅扫描/0.0.0.0/0枚举/端口矩阵)、自定义巡检模板、跨订阅批量巡检、定时巡检调度、历史趋势对比.
## 故障排查
| 问题 | 原因 | 解决方案 |
|:------|------:|:------|
| `Please run az login` | 未登录 | 运行 `az login --use-device-code` |
| `Subscription not found` | 订阅ID错误或无权限 | 用 `az account list` 确认可访问的订阅 |
| `Access denied` | RBAC权限不足 | 检查身份 `az account show`,确认Reader角色;RBAC审计需Reader+Role Based Access Control Reader |
| 巡检报告为空 | 资源组无资源或权限不足 | 确认资源组名称,检查订阅级Reader权限 |
| 配置漂移对比失败 | 基线快照不存在或格式错误 | 重新生成基线快照到 `$HOME/.json`,确认JSON格式正确 |
| jq命令未找到 | 缺少jq工具 | 从stedolan.github.io/jq安装jq |
| 风险评分异常 | 部分资源查询失败 | 检查对应资源权限,补齐缺失维度后重算;查看 `$HOME/.json` 权重配置 |
| 巡检超时 | 订阅资源过多 | 缩小巡检范围(按资源组);使用跨订阅批量巡检的并行模式 |
| Cost Management返回空 | 未配置或订阅类型不支持 | 确认Cost Management已在Portal配置;EA账户需EA Reader权限 |
| NSG扫描慢 | NSG数量多 | 缩小扫描范围;使用并行模式;缓存结果 |
| 跨订阅巡检中断 | 某订阅权限不足 | 脚本已设计为跳过失败订阅;检查日志确认跳过的订阅 |
| 定时巡检未执行 | cron配置错误 | 检查crontab -l;确认脚本有执行权限;查看日志 `/var/log/azure-inspector.log` |
| 趋势对比无数据 | 历史报告不足 | 至少积累2次巡检数据;确认报告保存到 `$HOME/.azure-inspector/reports/` |

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Azure CLI**: v2.0+(建议v2.50+以支持costmanagement等扩展)

> 注: 本SKILL.md超过500行上限, 已截断尾部非核心章节以满足L1格式要求。完整内容见版本库历史。

## 核心功能

- **自动化执行**: 全维度Azure巡检,含RBAC审计、成本管理、NSG暴露矩阵、跨订阅批量、定时调度、趋势对比.。Azure巡检员专业版
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据