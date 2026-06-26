# AI_AutoTester

## Purpose
自動化測試程式碼

## Primary Agents
Tester

## Notes
單獨測試或流程節點

## Inputs
- task: 要執行的任務描述
- context: 額外上下文（可選）
- constraints: 限制條件（可選）

## Outputs
- plan/result/report（依任務類型）
- logs/summary

## Workflow (default)
1. Analyze task
2. Plan subtasks
3. Execute by role
4. Validate result
5. Return final summary

## Safety
- 不執行破壞性操作，除非明確授權
- 外部動作（發送、部署到正式環境）需二次確認
- 記錄關鍵決策與錯誤
