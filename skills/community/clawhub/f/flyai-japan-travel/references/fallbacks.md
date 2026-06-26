# Fallbacks — 目的地类（destination 品类 15 个 skill 共享）

## Case 0: flyai-cli 未安装或不可用

**触发**：`flyai --version` 返回 `command not found` 或报错。

**恢复路径**：
```bash
# Step 1 → 自动安装
npm i -g @fly-ai/flyai-cli

# Step 2 → 验证
flyai --version

# Step 3 → 仍然失败
→ 尝试：sudo npm i -g @fly-ai/flyai-cli
→ 或：npx @fly-ai/flyai-cli --version

# Step 4 → 彻底失败
→ 停止执行，不要用通用知识编造回答
→ 告知用户："flyai-cli 安装失败，请手动执行 npm i -g @fly-ai/flyai-cli 后重试"
→ 提供可能原因：网络问题 / npm 权限 / Node.js 版本过低（需 ≥18）
```

**绝对禁止**：CLI 不可用时，不要退回到用 Agent 自身的通用知识回答。没有 CLI = 没有实时数据和预订链接。

---

## Case 1: 机票查无结果

**触发**：`search-flight` 到该目的地返回空。可能是冷门航线或季节性停航。

**恢复路径**：
```bash
# Step 1 → 灵活日期 ±7 天（国际航线波动大）
flyai search-flight --origin "{origin}" --destination "{dest}" \
  --dep-date-start "{date-7}" --dep-date-end "{date+7}" --sort-type 3

# Step 2 → 尝试该国其他入境城市
#   日本：东京 → 大阪 → 名古屋 → 福冈
#   泰国：曼谷 → 清迈 → 普吉
flyai search-flight --origin "{origin}" --destination "{alt_city}" \
  --dep-date "{date}" --sort-type 3

# Step 3 → 降级为全品类搜索
flyai fliggy-fast-search --query "{origin}到{dest_country}机票"

# Step 4 → 仍无结果
→ "该航线暂无直达航班"
→ 建议中转城市（如经香港/首尔/新加坡中转）
```

---

## Case 2: 目的地酒店信息不足

**触发**：`search-hotels` 返回少于 3 条。可能是小众目的地或数据覆盖不足。

**恢复路径**：
```bash
# Step 1 → 去掉筛选条件（星级/价格）
flyai search-hotels --dest-name "{city}" --sort rate_desc

# Step 2 → 扩大到周边城市
flyai search-hotels --dest-name "{nearby_city}" --sort rate_desc

# Step 3 → 全品类搜索
flyai fliggy-fast-search --query "{city} 酒店住宿"

# Step 4 → 仍不足
→ 展示已有结果
→ 标注 "该目的地在飞猪的酒店覆盖有限，建议同时查看 Booking/Agoda"
```

---

## Case 3: 景点搜索无结果

**触发**：`search-poi --city-name "{city}"` 返回空。可能是海外城市名不在数据库中。

**恢复路径**：
```bash
# Step 1 → 换中/英文名重试
flyai search-poi --city-name "{city_cn}" --keyword "{keyword}"
flyai search-poi --city-name "{city_en}" --keyword "{keyword}"

# Step 2 → 全品类搜索
flyai fliggy-fast-search --query "{city} 景点 旅游"

# Step 3 → 仍无结果
→ 基于内置知识推荐热门景点（不含预订链接）
→ 标注 "以上为推荐信息，非实时数据"
```

---

## Case 4: 签证信息查询失败

**触发**：`fliggy-fast-search --query "XX签证"` 返回无关内容或空。

**恢复路径**：
```
→ 基于内置知识提供基本签证信息
→ 标注 "以上为一般性信息，具体以使领馆最新政策为准"
→ 提供使领馆官网链接（如有）
```

---

## Case 5: 全行程编排中部分命令失败

**触发**：多命令编排中，某个环节（如酒店或景点）失败，其他成功。

**恢复路径**：
```
→ 不要因为一个环节失败就放弃全部
→ 成功的部分正常展示
→ 失败的部分标注 "⚠️ {环节} 暂未获取到数据"
→ 提供该环节的手动搜索建议
→ 在 runbook 中记录 partial 状态

示例输出：
  ✅ 签证信息：已获取
  ✅ 机票：最低 ¥2,500
  ⚠️ 京都酒店：暂未获取，建议手动搜索
  ✅ 东京景点：已获取 Top 5
```
