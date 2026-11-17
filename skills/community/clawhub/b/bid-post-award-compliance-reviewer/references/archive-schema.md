# 标后履约合规审查 · 可选项目档案（需用户知情同意后落盘）

> **本档案是「可选」的连续性辅助，默认不启用。** 仅在用户明确说「保存档案 / 存档」后，才按下方知情同意流程将项目状态写入本机 JSON 文件；否则全部状态仅在会话内维护，不创建任何目录或文件。
> 写入前必须向用户明示：① 保存的数据范围（含合同金额、人员/分包台账、风险结论等商业与个人隐私信息）；② 仅存于用户本机、不上传、不对外发送；③ 可随时回复「删除档案」清除。严格数据最小化：仅存结构化审查字段，不存文档原文，不存身份证号/社保号等原始个人敏感标识。

---

## 存储位置（仅在用户同意并主动要求时创建）

- **目录**：当前工作目录下的 `履约合规档案/`（仅当用户首次要求保存时创建）。
- **文件**：每个项目一个 `<项目名 sanitized>.json`。项目名含非法文件名字符时，替换为 `_`。
- **索引**：`履约合规档案/_index.json` 记录全部项目名 → 文件名映射，便于「查看项目档案 / 切换项目」（仅用户要求查看历史档案时读取，启动时不自动读取）。

---

## JSON Schema

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-07-27T16:41:55+08:00",
  "project": {
    "name": "示例市政道路工程",
    "type": "工程施工",
    "legal_system": "招投标法",
    "contract_amount_wan": 4980,
    "budget_amount_wan": 5200,
    "estimate_amount_wan": null,
    "contract_type": "固定单价",
    "current_stage": "合同已签正在履约",
    "user_role": "供应商/承包商/中标人",
    "region": "示例市",
    "review_focus": ["变更合规"]
  },
  "documents": [
    {
      "file_name": "中标通知书.pdf",
      "doc_type": "中标通知书",
      "key_terms": "工期365天；中标价4980万",
      "date": "2026-03-01",
      "registered_at": "2026-07-27T16:42:00+08:00"
    }
  ],
  "thresholds": {
    "supplement_contracts_count": 0,
    "cumulative_change_amount_wan": 0,
    "cumulative_change_ratio": 0.0,
    "govproc_supplement_ratio": null,
    "estimate_used_ratio": null,
    "over_estimate_5pct": false,
    "over_estimate_10pct": false,
    "contract_signed_within_30d": null,
    "pm_attendance_rate": null
  },
  "risks": [
    {
      "id": "R001",
      "source": "功能B-变更#1",
      "level": "🔴极高",
      "description": "未批先建",
      "legal_basis": "先审批后变更再实施",
      "status": "open"
    }
  ],
  "personnel_roster": [
    {
      "role": "项目经理",
      "bid_promise": "张某（一级建造师，高工）",
      "contract_promise": "张某",
      "actual": "李某（无注册证书）",
      "qualification": "低于原承诺",
      "consistency": "❌",
      "attendance_rate": null,
      "change_approved": false
    }
  ],
  "subcontract_roster": [
    {
      "subcontractor": "分包人A",
      "content": "______",
      "amount_wan": null,
      "qualification": "______",
      "approved_by_owner": null
    }
  ],
  "history": [
    {
      "ts": "2026-07-27T16:43:00+08:00",
      "action": "建档",
      "summary": "创建项目示例市政道路工程"
    }
  ]
}
```

---

## 读写规则（落盘仅在用户同意后）

0. **前置：知情同意**。用户首次说「保存档案 / 存档」时，先输出知情同意提示（见文件头），待用户明确确认后再创建目录与文件；未经确认绝不写入。
1. **查看历史档案**：仅当用户说「查看 / 继续档案」时，才读取 `履约合规档案/_index.json`（若存在），列出已有项目供其选择；**启动时不自动扫描或读取**，避免意外枚举本机文件。
2. **建档/登记后（已同意落盘）**：更新对应 JSON 字段 + 追加 `history` 一条；用 Edit 局部更新，避免整文件覆写丢失数据。
3. **评估后**：将新识别的风险写入 `risks[]`，更新 `thresholds` 与对应台账，记入 `history`。
4. **改参数**：仅更新对应字段（如仅改变更金额），不重算无关项，避免覆盖用户已确认结论。
5. **一致性**：写入前比对既有 `risks` 与历史结论，禁止出现自相矛盾的状态。
6. **安全与最小化**：档案仅含本项目结构化审查字段，不写入文档原文、不写身份证号/社保号等原始个人敏感标识；不对外发送档案内容。
7. **删除**：用户说「删除档案」时，删除对应 `<项目名>.json` 并在 `_index.json` 中移除该条目。
