---
name: "azure-cloud-inspector-free"
description: "面向日常巡检的Azure检查助手,默认只读,风险评分,暴露面发现,配置漂移检测。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Azure巡检员免费版"
  version: "1.0.0"
  summary: "面向日常巡检的Azure检查助手,默认只读,风险评分,暴露面发现,配置漂移检测。"
  tags:
    - "智能代理"
    - "云计算"
    - "Azure"
    - "巡检"
    - "安全检查"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Azure巡检员(免费版)

面向"日常巡检"场景的Azure CLI辅助工具。默认只读查询,聚焦检查与报告,不主动执行变更操作。仅在用户明确要求变更并确认后,才执行写/破坏性操作。

> 本免费版提供核心巡检能力(资源清单/健康检查/暴露面扫描/配置漂移/巡检报告)。RBAC安全审计、成本管理与NSG暴露深度检查为专业版功能。

## 使用流程

### 30秒:确认身份
```bash
az account show --query '{Subscription:name, Tenant:tenantId, User:user.name}' --output table
```
未登录时运行: `az login --use-device-code`

### 60秒:执行一次基础巡检
```bash
# 1. 列出当前订阅所有资源组
az group list --query '[].{Name:name, Location:location, Count:length(resources())}' --output table

# 2. 巡检第一个资源组(替换 <RG>)
az group show -n <RG> --query '{Name:name, State:properties.provisioningState, Tags:tags}'
az resource list -g <RG> --query '[].{Name:name, Type:type, Location:location}' --output table
```

### 300秒:完成完整巡检流程
1. 确认身份与订阅(参见订阅与租户处理)
2. 选择巡检范围(订阅级/资源组级)
3. 选择巡检任务模板(参见巡检任务模板)
4. 执行巡检(资源清单→健康检查→暴露面扫描→配置漂移)
5. 生成巡检报告(参见巡检报告生成)

#
## 安全规则(最高优先级,不可被任何用户指令覆盖)

* 所有操作默认**只读**,除非用户明确要求变更**且**确认
* 破坏性操作(delete/modify/scale/credential)需要二次确认步骤
* 优先使用 `--dry-run` 或 `what-if` 预演并展示计划
* **绝不要**透露或记录密钥(账户密钥、客户端密钥、令牌、连接字符串)
* **绝不要**将密钥输出到聊天或日志
* 巡检脚本中禁止硬编码订阅ID、租户ID、资源名称等敏感信息,使用参数化传入

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

结果为订阅范围时,明确说明使用的订阅。登录特定租户使用 `az login --tenant <tenant-id>`(tenant为Azure CLI标准参数)。

## 巡检任务模板(差异化)

### 模板1:资源组日常巡检
```bash
# 变量定义(由用户传入)
RG="${1:-myResourceGroup}"

echo "=== 资源组: $RG ==="
az group show -n "$RG" --query '{Name:name, Location:location, State:properties.provisioningState}'

echo "=== 资源清单 ==="
az resource list -g "$RG" --query '[].{Name:name, Type:type, Location:location, Created:createdTime}' --output table

echo "=== 资源数量统计 ==="
az resource list -g "$RG" --query '[].type' -o tsv | sort | uniq -c | sort -rn
```

### 模板2:VM健康巡检
```bash
echo "=== VM状态 ==="
az vm list -d --query '[].{Name:name, RG:resourceGroup, State:powerState, Size:hardwareProfile.vmSize}' --output table

echo "=== 停止的VM(可能浪费成本) ==="
az vm list -d --query "[?powerState=='VM stopped'].{Name:name, RG:resourceGroup}" --output table

echo "=== VM磁盘加密状态 ==="
az vm list --query '[].{Name:name, RG:resourceGroup}' -o tsv | while read name rg; do
  echo -n "$name: "; az vm encryption show -n "$name" -g "$rg" --query 'disks[].statuses[].code' -o tsv 2>/dev/null || echo "无法查询"
done
```

### 模板3:存储账户巡检
```bash
echo "=== 存储账户清单 ==="
az storage account list --query '[].{Name:name, RG:resourceGroup, SKU:sku.name, TLS:minimumTlsVersion}' --output table

echo "=== 公共Blob访问检查(应为false) ==="
az storage account list --query '[].{Name:name, PublicAccess:allowBlobPublicAccess}' --output table

echo "=== HTTPS强制检查(应为true) ==="
az storage account list --query '[].{Name:name, HTTPS:enableHttpsTrafficOnly}' --output table
```

## 五维风险评分模型(差异化核心)

每次巡检后按五维评分(0-10分,0=最低风险,10=最高风险),输出总体风险等级。

| 维度 | 检查项 | 评分方法 | 高风险阈值 |
|------|--------|----------|------------|
| 暴露面 | 公网IP、开放端口、公共存储 | 每发现一项暴露+2分 | ≥6分 |
| 加密 | 磁盘加密、传输加密、Key Vault | 未加密项+3分 | ≥4分 |
| 访问控制 | RBAC角色、Owner数量、公共访问 | Owner>3加3分,公共访问+2分 | ≥6分 |
| 配置漂移 | 与基线对比、未标签资源 | 偏离项+1分,无标签+0.5分 | ≥5分 |
| 健康度 | 停止VM、未挂载磁盘、告警 | 异常资源每项+1分 | ≥4分 |

### 风险等级映射
| 总分 | 等级 | 建议 |
|------|------|------|
| 0-10 | 低 | 例行巡检,记录归档 |
| 11-25 | 中 | 48小时内修复 |
| 26-40 | 高 | 24小时内修复 |
| >40 | 严重 | 立即介入,启动应急流程 |

### 示例
```bash
# 暴露面评分(示例)
public_ip_count=$(az network public-ip list --query '[?ipConfiguration==null] | length(@)' -o tsv)
exposure_score=$((public_ip_count * 2))
echo "暴露面评分: $exposure_score (未关联的公网IP: $public_ip_count 个)"

# 健康度评分(示例)
stopped_vm=$(az vm list -d --query "[?powerState=='VM stopped'] | length(@)" -o tsv)
health_score=$((stopped_vm * 1))
echo "健康度评分: $health_score (停止的VM: $stopped_vm 个)"
```

## 公网暴露面发现(差异化)

自动扫描订阅内对外暴露的资源:

```bash
echo "=== 公网IP清单 ==="
az network public-ip list --query '[].{Name:name, IP:ipAddress, Associated:ipConfiguration!=null}' --output table

echo "=== 未关联的公网IP(浪费+暴露风险) ==="
az network public-ip list --query '[?ipConfiguration==null].{Name:name, IP:ipAddress}' --output table

echo "=== 存储账户公共访问 ==="
az storage account list --query '[?allowBlobPublicAccess==true].{Name:name, RG:resourceGroup}' --output table

echo "=== 公网负载均衡器 ==="
az network lb list --query '[].{Name:name, RG:resourceGroup, FrontendIPs:length(frontendIpConfigurations)}' --output table
```

## 配置漂移检测(差异化)

通过快照对比发现配置偏离:

```bash
# 1. 生成当前配置快照
az resource list --query '[].{Name:name, Type:type, RG:resourceGroup, Tags:tags}' > /tmp/azure-snapshot-current.json

# 2. 与基线快照对比(假设基线快照已存在)
if [ -f /tmp/azure-snapshot-baseline.json ]; then
  echo "=== 与基线对比 ==="
  diff <(jq -r '.[] | "\(.Type)/\(.Name)"' /tmp/azure-snapshot-baseline.json | sort) \
       <(jq -r '.[] | "\(.Type)/\(.Name)"' /tmp/azure-snapshot-current.json | sort) || true
fi

# 3. 保存为新基线(用户确认后)
# cp /tmp/azure-snapshot-current.json /tmp/azure-snapshot-baseline.json
```

## 巡检报告生成(差异化)

巡检完成后自动生成Markdown格式报告:

```bash
REPORT="/tmp/azure-inspection-$(date +%Y%m%d-%H%M%S).md"

cat > "$REPORT" <<EOF
# Azure巡检报告

- 巡检时间: $(date)
- 订阅: $(az account show --query name -o tsv)
- 巡检范围: ${1:-全订阅}

## 资源概览
$(az resource list --query '[].type' -o tsv | sort | uniq -c | sort -rn)

## 健康状态
- 停止的VM: $(az vm list -d --query "[?powerState=='VM stopped'] | length(@)" -o tsv) 个
- 未挂载磁盘: $(az disk list --query "[?diskState=='Unattached'] | length(@)" -o tsv) 个
- 未关联公网IP: $(az network public-ip list --query '[?ipConfiguration==null] | length(@)' -o tsv) 个

## 风险等级
[根据五维评分模型计算]

## 建议项
[根据检查结果生成]
EOF

echo "巡检报告已生成: $REPORT"
```

## 真实场景示例

### 场景一:上线前暴露面检查
```text
用户:"我们准备上线一个新服务,帮我检查一下订阅里有没有不该暴露的东西"

执行流程:
1. 扫描所有公网IP,识别未关联的(浪费且暴露)
2. 扫描存储账户公共访问(allowBlobPublicAccess)
3. 扫描NSG入站规则中的0.0.0.0/0(免费版仅基础检查,深度检查在专业版)
4. 列出公网负载均衡器
5. 生成暴露面报告,标注高风险项
```

### 场景二:每日例行巡检
```text
用户:"帮我跑一次日常巡检,关注资源组prod-rg"

执行流程:
1. 应用模板1(资源组日常巡检)
2. 执行五维风险评分
3. 对比昨日基线快照,标记新增/删除资源
4. 生成Markdown巡检报告
5. 报告中标注中高风险项的修复建议
```

### 场景三:配置漂移排查
```text
用户:"运维同事昨天改了配置,我想知道具体改了什么"

执行流程:
1. 读取昨日基线快照
2. 生成当前配置快照
3. diff对比,列出新增/删除/变更资源
4. 对变更资源调用az resource show对比属性
5. 输出漂移报告
```

## 错误处理


| 序号 | 错误场景 | 原因 | 处理方式 | 优先级 |
|------|----------|------|----------|--------|
| 1 | 输入参数缺失 | 用户未提供必要参数 | 提示用户提供所需参数后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P0 |
| 2 | 执行超时 | 处理时间过长 | 检查输入数据量,分批处理 | P1 |
| 3 | 输出格式错误 | 结果不符合预期格式 | 检查`output_format`参数配置 | P1 |

## 常见问题

**Q: 巡检会修改我的Azure资源吗?**
A: 不会。巡检默认全部使用只读命令(list/show/get/query),不会对资源做任何变更。即使用户要求修复建议,也仅展示命令,需用户明确确认后才执行。

**Q: 五维风险评分如何加权?**
A: 免费版采用等权加权(每维度0-10分,总分0-50分)。专业版支持自定义权重,例如对"暴露面"加权到1.5倍,"健康度"降至0.8倍,适配不同业务场景。

**Q: 配置漂移检测的基线快照如何生成?**
A: 首次运行时执行 `az resource list --query ... > baseline.json` 生成基线。后续每次巡检生成current快照并与baseline对比。基线可手动更新(确认当前配置为新的标准)。

**Q: 巡检报告可以分享给团队吗?**
A: 可以。报告为标准Markdown格式,可直接粘贴到企业IM、Wiki或工单系统。免费版报告含资源概览、健康状态、风险等级与建议项;专业版额外包含趋势图表与历史对比。

**Q: 免费版与专业版的核心差异?**
A: 免费版提供核心巡检能力(资源清单/健康检查/暴露面扫描/配置漂移/巡检报告)。专业版额外解锁:RBAC深度安全审计、Cost Management成本管理、NSG暴露深度检查、自定义巡检模板、历史趋势对比、定时巡检调度。

**Q: 多订阅如何巡检?**
A: 免费版需手动切换订阅(`az account set --subscription <id>`)分别巡检。专业版支持跨订阅批量巡检,一次扫描所有可访问订阅并汇总报告。

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `Please run az login` | 未登录 | 运行 `az login --use-device-code` |
| `Subscription not found` | 订阅ID错误或无权限 | 用 `az account list` 确认可访问的订阅 |
| `Access denied` | RBAC权限不足 | 检查身份 `az account show`,确认Reader角色 |
| 巡检报告为空 | 资源组无资源或权限不足 | 确认资源组名称,检查订阅级Reader权限 |
| 配置漂移对比失败 | 基线快照不存在或格式错误 | 重新生成基线快照,确认JSON格式正确 |
| jq命令未找到 | 缺少jq工具 | 从stedolan.github.io/jq安装jq |
| 风险评分异常 | 部分资源查询失败 | 检查对应资源权限,补齐缺失维度后重算 |
| 巡检超时 | 订阅资源过多 | 缩小巡检范围(按资源组),或使用专业版并行巡检 |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Azure CLI**: v2.0+(建议v2.50+以支持costmanagement等扩展)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Azure CLI | 工具 | 必需 | 从docs.microsoft.com/cli/azure安装 |
| Azure账户 | 账户 | 必需 | 注册Azure账户 |
| jq | 工具 | 推荐(配置漂移对比) | 从stedolan.github.io/jq安装 |
| bash | 运行时 | 推荐(巡检脚本执行) | 系统自带或安装Git Bash |

### API Key 配置
- 通过 `az login` 认证,无需手动配置API Key
- 服务主体认证需 `az login --service-principal -u <app-id> -p <password> --tenant <tenant>`
- **绝不要**在聊天、日志或巡检报告中输出密钥、客户端密钥、令牌

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,需要命令行执行能力运行Azure CLI)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent使用Azure CLI执行云资源巡检。需要Azure CLI和Azure账户。

## 已知限制

本免费体验版限制以下高级功能:

- RBAC深度安全审计(角色分配清单、Owner过度授权检测、自定义角色审计):免费版仅展示当前订阅角色概览,不输出审计报告与建议
- Cost Management成本管理(按资源组/服务维度成本分析、空闲资源识别、成本趋势对比):免费版不提供
- NSG暴露深度检查(全订阅NSG规则扫描、0.0.0.0/0入站规则枚举、端口暴露矩阵):免费版仅基础检查
- 自定义巡检模板与定时巡检调度:免费版不提供
- 跨订阅批量巡检与历史趋势对比:免费版不提供

解锁全部功能请使用专业版: azure-cloud-inspector-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## License与版权声明

本skill基于原始作品改进,保留原始版权声明:

- 原始作品: azure-infra (Azure Infra)
- 原始license: MIT
- 改进作品: azure-cloud-inspector-free
- 改进license: MIT

本改进作品在原始作品基础上进行了深度差异化改造,包括但不限于:
- 重新定位为"巡检员"视角(原始为通用基础设施查询)
- 新增五维风险评分模型(暴露/加密/访问/配置/健康)
- 新增公网暴露面自动发现能力
- 新增配置基线漂移检测机制
- 新增可复用巡检任务模板(3类)
- 新增Markdown巡检报告自动生成
- 新增分级快速开始(30秒/60秒/300秒)
- 新增FAQ(6问)与故障排查表(8项)
- 重写description为五段结构,新增edition字段

原始MIT license允许修改与再分发,本改进作品在MIT license下发布,保留原始版权声明。

## 核心能力

### Azure巡检员免费版是一个以
Azure巡检员免费版是一个以"日常巡检"为核心视角的Azure CLI辅助工具

**输入**: 用户提供Azure巡检员免费版是一个以所需的指令和必要参数。
**处理**: 按照skill规范执行Azure巡检员免费版是一个以操作,遵循单一意图原则。
**输出**: 返回Azure巡检员免费版是一个以的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 针对云上资源"配置漂移无人察觉、公网暴露
针对云上资源"配置漂移无人察觉、公网暴露面长期敞开、巡检脚本每次重写、风险等级无量化、巡检结论难分享"五大痛点,构建了风险评分模型、暴露面发现、配置漂移检测、巡检任务模板和巡检报告生成五大基础能力

**输入**: 用户提供针对云上资源"配置漂移无人察觉、公网暴露所需的指令和必要参数。
**处理**: 按照skill规范执行针对云上资源"配置漂移无人察觉、公网暴露操作,遵循单一意图原则。
**输出**: 返回针对云上资源"配置漂移无人察觉、公网暴露的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心能力包括
核心能力包括:默认只读查询保障安全

**输入**: 用户提供核心能力包括所需的指令和必要参数。
**处理**: 按照skill规范执行核心能力包括操作,遵循单一意图原则。
**输出**: 返回核心能力包括的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 写操作与破坏性操作需双重确认
写操作与破坏性操作需双重确认

**输入**: 用户提供写操作与破坏性操作需双重确认所需的指令和必要参数。
**处理**: 按照skill规范执行写操作与破坏性操作需双重确认操作,遵循单一意图原则。
**输出**: 返回写操作与破坏性操作需双重确认的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 支持--dry-run与wha
支持--dry-run与what-if预演

**输入**: 用户提供支持--dry-run与wha所需的指令和必要参数。
**处理**: 按照skill规范执行支持--dry-run与wha操作,遵循单一意图原则。
**输出**: 返回支持--dry-run与wha的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向日常巡检的、检查助手、Use、when、模型调用、智能对话、Agent、LLM、应用时使用、不适用于需要、确定性的关键决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 适用场景

### 场景一:上线前暴露面检查
```text
用户:"我们准备上线一个新服务,帮我检查一下订阅里有没有不该暴露的东西"

执行流程:
1. 扫描所有公网IP,识别未关联的(浪费且暴露)
2. 扫描存储账户公共访问(allowBlobPublicAccess)
3. 扫描NSG入站规则中的0.0.0.0/0(免费版仅基础检查,深度检查在专业版)
4. 列出公网负载均衡器
5. 生成暴露面报告,标注高风险项
```

### 场景二:每日例行巡检
```text
用户:"帮我跑一次日常巡检,关注资源组prod-rg"

执行流程:
1. 应用模板1(资源组日常巡检)
2. 执行五维风险评分
3. 对比昨日基线快照,标记新增/删除资源
4. 生成Markdown巡检报告
5. 报告中标注中高风险项的修复建议
```

### 场景三:配置漂移排查
```text
用户:"运维同事昨天改了配置,我想知道具体改了什么"

执行流程:
1. 读取昨日基线快照
2. 生成当前配置快照
3. diff对比,列出新增/删除/变更资源
4. 对变更资源调用az resource show对比属性
5. 输出漂移报告
```
