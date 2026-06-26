---
name: flyai-visa-timeline
description: 签证进度规划与提醒助手。输入目的地和出行日期，倒推生成签证办理时间线、材料清单和每步截止日期。当用户提到"签证怎么办"、"签证时间"、"签证材料"、"来得及办签证吗"、"签证规划"、"办签证"时使用。
---

# 签证时间线规划助手

根据用户的目的地和出行日期，倒推生成签证办理时间线、所需材料清单和每一步截止日期。

## 工具说明

> 详见 [reference/tools.md](reference/tools.md)

## 用户画像读取（双模式）

启动时读取用户历史偏好，减少重复询问。

> 详见 [reference/user-profile-storage.md](reference/user-profile-storage.md)

**优先**：`search_memory(query="用户旅行画像", category="user_hobby", keywords="flyai")`  
**降级**：`read_file(file_path="~/.flyai/user-profile.md")`

---


## 启动对话

当用户触发此 Skill 时，使用 `ask_user_question` 工具**分步骤**收集必需信息。

## 核心工作流
### FlyAI 能力

> 完整命令参考见 reference 目录

**本技能主要使用**：`keyword-search`（查询签证产品），`search-flight`/`search-hotel`（生成预订单）
> 详细步骤见 [reference/core-workflow.md](reference/core-workflow.md)

**核心阶段：**
1. 信息收集 - 确认目的地、出发日期、护照签发地、职业身份
2. 签证查询 - 调用 FlyAI keyword-search 获取签证产品与办理周期
3. 时间线倒推 - 根据办理周期计算各节点截止日期
4. 材料清单 - 按用户身份生成个性化材料清单
5. 方案输出 - 生成时间线卡片，提供机票酒店预订单辅助


## 异常处理

| 场景 | 处理方式 |
|------|----------|
| 时间已来不及 | 直接告知"⚠️ 常规流程来不及"，推荐：1) 加急方案 2) 免签/落地签替代目的地 |
| 签证政策变动 | 标注"信息更新于{日期}，建议出发前再次确认领馆官网" |
| 材料要求因人而异 | 识别用户身份（白本护照、单身女性、自由职业等），给出替代材料方案 |
| 拒签风险较高 | 根据用户基础条件给出风险评估和提升建议 |
| 目的地信息查询失败 | 使用内置签证周期参考表，标注"建议确认最新政策" |

## 免签/落地签替代推荐

如果用户时间紧张，推荐以下免签或落地签目的地：

### 免签目的地
- **东南亚**: 泰国（2024年起免签）、马来西亚（30天）、新加坡（30天）
- **海岛**: 马尔代夫（30天落地签）、斐济（120天）、毛里求斯（60天）
- **中东**: 阿联酋（30天）、卡塔尔（30天）

### 落地签目的地
- **泰国**: 15天落地签
- **印度尼西亚**: 30天落地签
- **柬埔寨**: 30天落地签
- **尼泊尔**: 90天落地签

## 后续操作

用户确认时间线后，可以继续：

1. **搜索签证代办服务**:
   ```bash
   /flyai keyword-search --query "{目的地} 签证代办"
   ```

2. **预订机票生成预订单**:
   ```bash
   /flyai search-flight --origin "{出发城市}" --destination "{目的地}" --dep-date {日期}
   ```

3. **预订酒店生成预订单**:
   ```bash
   /flyai search-hotel --dest-name "{目的地}" --check-in-date {日期} --check-out-date {日期}
   ```

4. **设置关键节点提醒**:
   询问用户是否需要设置手机日历提醒

## 示例对话

> 详见 [reference/examples.md](reference/examples.md)

## 用户偏好保存（双模式）

发现新偏好时提示保存。详见 [reference/user-profile-storage.md](reference/user-profile-storage.md)

**保存流程**：发现偏好 → 提示确认 → Qoder用update_memory / 非Qoder更新本地文件
