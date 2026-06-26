# Output Patterns

## Package decision response

最终结果应收敛为 `package_plan` 主体，至少包含：

```json
{
  "package_plan": {
    "package_id": "pkg_xxx",
    "library_id": "lib_xxx",
    "goal": "summer_internship_application",
    "selected_asset_ids": ["asset_xxx"],
    "submission_profile": "judge_demo_v1"
  }
}
```

- `selected_asset_ids` 只能引用真实资产
- `readiness` 只能继承 lifecycle，不得翻转
- 被阻塞时允许 truthful package，但不得伪装成 ready
