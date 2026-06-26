---
name: blueprint-generator
description: UE蓝图+材质双模式生成器。当主人说"蓝图生成器"、"材质生成器"、"合并生成器"时触发。已合并为统一App，支持Tab切换。
version: 3.0.0
---

# UE Generator 技能包（蓝图+材质合并版）

## 部署地址
https://ncvbhgghna86.space.minimaxi.com

## 项目位置
`/workspace/blueprint-generator/`

## 快速启动
```bash
cd /workspace/blueprint-generator
npm run dev      # 开发调试
npm run build    # 生产构建
```

## 核心功能
- 自然语言描述 → UE蓝图可视化节点图
- 自然语言描述 → UE材质节点图
- 上传截图 → AI分析还原蓝图/材质结构
- 悬停节点显示"为什么要这样设计"解释
- 节点拖拽、选中高亮、追加修改模式
- 导入JSON查看完整结构

## AI模型配置（重要）
- **当前使用**：MiniMax-M2.7
- **网关**：`https://api.minimaxi.com/v1`
- **API Key**：MiniMax Coding Plan Key
- **消耗**：消耗 MiniMax Token Plan 额度
- 如需切换模型：修改 `src/api.ts` 和 `src/api/material.ts` 中的 `model` 字段

## 切换模型方法
```python
# 文件：src/api.ts 和 src/api/material.ts
API_KEY  = '你的API Key'
API_BASE = 'https://api.minimaxi.com/v1'
model    = 'MiniMax-M2.7'  # 可选：MiniMax-M2.7、MiniMax-V01等
```

## ⚠️ 常见错误说明
- **错误码 2064**："服务集群负载较高" → MiniMax服务器限流，等30秒~2分钟再试
- **错误码 2011**："请求过于频繁" → 降低请求频率
- **解析失败** → 生成的JSON格式UE不认，减少描述复杂度重试

## 节点类型（UE标准）
| type | 颜色 | 说明 |
|------|------|------|
| event | #8B5CF6 紫色 | Event事件节点 |
| inputaxis | #059669 绿色 | InputAxis输入 |
| function | #2563EB 深蓝 | 函数/SET变量（SET xxx是function类型） |
| variable_get | #7C3AED 紫色药丸 | 变量获取，无exec引脚 |
| flow | #6B7280 灰色 | FlowControl流程控制 |
| math | #06B6D4 青色 | 数学运算 |

## 引脚类型颜色
| type | 颜色 |
|------|------|
| exec | 白色方形 |
| float | #4CAF50 绿色圆 |
| bool | #F44336 红色圆 |
| vector | #FFC107 黄色圆 |
| object | #9C27B0 紫色圆 |

## 重要规则（生成JSON时必须遵循）
1. SET节点类型是 `function`，不是 `variable_set`
2. SET节点标题格式："SET 变量名"，如 "SET EnemyController"
3. connections不能为空，每个非Event节点必须有输入/输出连接
4. 所有输入引脚必须被连接，禁止孤立节点
5. GET节点是紫色药丸形（variable_get），无彩色标题栏

## 关键文件
- `src/api.ts` — 蓝图生成逻辑 + 系统提示词
- `src/api/material.ts` — 材质生成逻辑 + 系统提示词
- `src/nodes/BlueprintNode.tsx` — 蓝图节点渲染
- `src/nodes/MaterialNode.tsx` — 材质节点渲染
- `src/GeneratorCanvas.tsx` — 统一画布（双模式切换）
- `src/Sidebar.tsx` — 节点详情+修改面板
- `src/types.ts` — 蓝图类型定义
- `src/types/material.ts` — 材质类型定义
- `public/BP_SetAIState.json` — SetAIState蓝图示例
- `public/BP_EnemyHitFlash.json` — 敌人受击蓝图示例
