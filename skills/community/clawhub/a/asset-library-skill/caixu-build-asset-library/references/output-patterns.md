# Output Patterns

## Document triage response

始终返回：

```json
{
  "decisions": [
    {
      "file_id": "file_xxx",
      "include_in_library": true,
      "document_role": "personal_experience",
      "reason": null
    }
  ]
}
```

- 每个输入文件都必须有一条 decision
- `include_in_library = false` 时，`reason` 不应为空
- 优先输出极小 JSON；不要解释，不要补充说明
- 不确定时优先 `include_in_library = false`
- `document_role` 只允许：
  - `personal_proof`
  - `personal_experience`
  - `public_notice`
  - `team_notice`
  - `reference_only`
  - `noise`

## Asset extraction response

始终返回：

```json
{
  "decisions": [
    {
      "file_id": "file_xxx",
      "asset_card": {
        "schema_version": "1.0",
        "library_id": "lib_xxx",
        "asset_id": "asset_file_xxx",
        "material_type": "experience",
        "title": "个人简历",
        "holder_name": "张三",
        "issuer_name": null,
        "issue_date": null,
        "expiry_date": null,
        "validity_status": "unknown",
        "reusable_scenarios": [
          "summer_internship_application"
        ],
        "sensitivity_level": "medium",
        "source_files": [
          {
            "file_id": "file_xxx",
            "file_name": "resume.pdf",
            "mime_type": "application/pdf"
          }
        ],
        "confidence": 0.62,
        "normalized_summary": "张三的个人简历，包含教育背景、技能和项目经验。"
      },
      "skip_reason": null
    }
  ]
}
```

- `asset_card = null` 时，`skip_reason` 不应为空
- `asset_card` 非空时，必须包含完整必填字段，不要省略 `schema_version`、`title`、`validity_status`、`sensitivity_level`、`source_files`、`normalized_summary`
- `holder_name`、`issuer_name`、`issue_date` 不确定时返回 `null`
- `validity_status` 无明确有效期证据时优先返回 `unknown`
- `title` 和 `normalized_summary` 必须是短而保守的文本，不要留空
- 不要输出 `"unknown"`
- 简历类材料必须使用 `material_type = experience` 且 `issuer_name / issue_date / expiry_date = null`
- 公示/名单或团队材料若仍保留为 `asset_card`，`normalized_summary` 必须明确写出它只是佐证材料

## Merge decision response

始终返回：

```json
{
  "merged_assets": []
}
```

- 不确定时返回空数组
- 只归并高置信重复版本，例如同一 owner 的简历版本或明显重复扫描件
