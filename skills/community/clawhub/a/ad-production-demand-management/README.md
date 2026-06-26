# Demand Management Skill

管理广告创意素材的需求发起、评审和拆解流程。

## Features

- ✅ 需求提交与标准化
- ✅ 需求评审会议安排
- ✅ 需求拆解为生产任务
- ✅ 需求状态跟踪
- ✅ 需求文档自动生成

## Usage

```bash
# 创建新需求
claw demand create --title "Q2游戏广告素材" --type "new_material" \
  --channel "抖音" --style "现代奇幻" --size "9:16" \
  --description "需要一批奇幻风格的9:16竖版视频素材"

# 查看需求列表
claw demand list --status "pending"

# 评审需求
claw demand review --id "REQ-001" --result "approved" --comments "通过"

# 拆解需求为生产任务
claw demand拆解 --id "REQ-001" --prompt-template "fantasy_character"
```

## Integration

这个技能会与其他技能协同：
- 产出需求文档给 `ai-generation`
- 触发 `workflow-orchestrator` 创建流程
- 更新 `material-library` 的元数据标签

## Configuration

在 `openclaw.json` 中配置：

```json
{
  "skills": {
    "demand-management": {
      "enabled": true,
      "config": {
        "reviewers": ["ou_xxx", "ou_yyy"],
        "autoAssign": true,
        "defaultDeadline": 7
      }
    }
  }
}
```