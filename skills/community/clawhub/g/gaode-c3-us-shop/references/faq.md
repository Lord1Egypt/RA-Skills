# POI Debug Orchestrator — FAQ

## 安装与使用

### Q1: 如何安装这个技能？

```bash
# 技能已安装到 ~/.claude/skills/poi-debug-orchestrator/
# 直接使用即可，无需额外安装
```

### Q2: 使用前需要准备什么？

**必需**:
1. Loghouse MCP 授权 (`loghouse-mcp`)
2. Code MCP 授权 (`code`)
3. 内网环境（VPN 或办公网）

**可选**:
- `sf` CLI (用于查询监控报警)

### Q3: 如何运行？

**方式 A: 直接调用脚本**
```bash
cd ~/.claude/skills/poi-debug-orchestrator/scripts
./poi-debug.sh <gsid> <poiid> [env] [timeRange]
```

**方式 B: 让 Agent 执行**
```
"帮我排查这个 POI 问题：gsid=xxx, poiid=xxx"
```

---

## 常见问题

### Q4: 日志查询为空怎么办？

**可能原因**:
1. GSID 错误或不完整
2. 时间范围太短，日志已过期
3. 接口路径不匹配

**解决方法**:
```bash
# 扩大时间范围
./poi-debug.sh <gsid> <poiid> gray "4h ago"

# 检查 GSID 格式（应该是 38 位数字）
echo "31033080013090177494736367500059940538728" | wc -c
# 应该是 39 (38 位 + 换行符)
```

### Q5: 请求复现失败（响应为空）

**可能原因**:
1. 内网 IP 无法访问
2. 域名不正确
3. 环境不匹配

**解决方法**:
```bash
# 手动测试域名连通性
curl -I http://gray-us-business.amap.com/health

# 检查 URL 是否完整
echo "$FULL_URL" | head -c 500
```

### Q6: shopSettlement 为空，如何进一步排查？

**步骤**:

1. **确认 POI 类型**
```bash
# 查询 POI 基础信息
python3 ~/.claude/skills/poi-query/scripts/poi_query.py <poiid> online
```

2. **检查绑定关系**
```sql
-- 需要 DB 权限
SELECT * FROM poi_shop_bind WHERE poi_id = '<poiid>';
```

3. **查看上游日志**
```bash
# 查询 shopSettlement 单独接口
sf log query --app lse2-us-business-service \
  --query "/search_business/process/middleLayer/shopSettlement AND <poiid>"
```

### Q7: 如何查看完整的响应 JSON？

```bash
# 响应保存在临时文件
cat /tmp/poi_response_<gsid 后 8 位>.json | jq '.'

# 或格式化查看特定字段
cat /tmp/poi_response_*.json | jq '.data.middleLayerStrategy.shopSettlement'
```

### Q8: 代码定位失败怎么办？

**可能原因**:
- Code MCP 未授权
- 仓库路径变化
- 类名不匹配

**解决方法**:
```bash
# 手动搜索
aone-kit call-tool code::search_classes '{
  "search": "ShopSettlement",
  "repo": "gaode.search/us-business-service",
  "pageSize": 10
}'

# 或搜索文件
aone-kit call-tool code::search_file_path '{
  "search": "ShopSettlementDTO",
  "repo": "gaode.search/us-business-service"
}'
```

---

## 性能与优化

### Q9: 排查一个 POI 需要多长时间？

**正常情况**: 30-60 秒
- 日志查询：5-10 秒
- 请求复现：5-15 秒
- 解析响应：<1 秒
- 代码定位：5-10 秒
- 生成报告：<1 秒

**慢的情况**:
- Loghouse 查询慢 → 扩大时间范围导致
- 网络延迟 → 灰度环境响应慢

### Q10: 如何批量排查多个 POI？

```bash
# 创建批量脚本
cat > batch-debug.sh << 'EOF'
#!/bin/bash
while IFS=, read -r gsid poiid; do
    echo "=== 排查 $poiid ==="
    ./poi-debug.sh "$gsid" "$poiid"
done < poi_list.csv
EOF

chmod +x batch-debug.sh

# poi_list.csv 格式:
# gsid,poiid
# 31033080013090177494736367500059940538728,B0LR4UPN4M
# 31033080013090177494736367500059940538729,B0LR4UPN4N
```

---

## 扩展与定制

### Q11: 如何支持其他接口？

修改 `scripts/poi-debug.sh` 中的 `INTERFACE` 变量：

```bash
# 支持 shopBaseInfo
INTERFACE="/search_business/process/middleLayer/shopBaseInfo"

# 支持 shopSettlement 单独接口
INTERFACE="/search_business/process/middleLayer/shopSettlement"
```

### Q12: 如何添加自定义分析逻辑？

在 Step 5 的 Python 脚本中添加：

```python
# 在解析结果后添加自定义检查
if shop_settlement.get('operationalInfo', {}).get('traffic', 0) == 0:
    result['issues'].append('累积流量为 0，可能数据异常')
```

### Q13: 如何输出为 Markdown 报告？

```bash
# 添加导出选项
./poi-debug.sh <gsid> <poiid> --format markdown > report.md
```

---

## 故障排查

### Q14: 脚本执行报错 "command not found"

**原因**: `aone-kit` 或 `sf` 不在 PATH 中

**解决**:
```bash
export PATH="/app/501280/.local/bin:$PATH"
# 或添加到 ~/.bashrc
echo 'export PATH="/app/501280/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Q15: Loghouse 返回 "no match routingMapping"

**原因**: log_name 不正确

**解决**:
```bash
# 确认正确的 log_name
# 从 Loghouse UI 查看：https://loghouse.alibaba-inc.com/
# 对于 lse2-us-business-service，通常是 nginx_uni
```

### Q16: curl 请求超时

**原因**: 灰度环境响应慢或网络问题

**解决**:
```bash
# 增加超时时间
curl -s --max-time 60 "$FULL_URL"

# 或尝试线上环境
./poi-debug.sh <gsid> <poiid> online
```

---

## 最佳实践

### Q17: 排查问题的标准流程是什么？

```
1. 收集信息
   - GSID、POIID
   - 问题现象（哪个字段缺失/异常）
   - 发生时间

2. 执行编排器
   ./poi-debug.sh <gsid> <poiid>

3. 分析报告
   - 查看异常字段
   - 对比预期值

4. 深入排查
   - 根据报告建议，查代码/查 DB/查配置

5. 修复验证
   - 提 CR 或改配置
   - 灰度验证
   - 全量发布
```

### Q18: 如何记录排查过程？

```bash
# 每次排查结果自动保存
ls -lt /tmp/poi-debug-results/

# 归档重要 case
cp /tmp/poi-debug-results/poi_debug_xxx.json ~/documents/poi-issues/
```

---

## 联系方式

- **作者**: 土曜 (501280)
- **反馈**: 遇到问题请提 Issue 或直接联系

---

_最后更新：2026-03-31_
