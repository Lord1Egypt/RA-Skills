# 操作字段

以下均为 POST `/api/v1/document-redaction/{operation}` 的最小 JSON 结构示例。尖括号是需要替换的占位值，版本数字只说明顺序，不能直接复制当作实际版本。完整请求头和续查见 HTTP-REQUESTS。不要为了补齐示例而虚构候选、坐标、逐页确认、费用授权或指纹。

## 字段来源与版本链

| 字段 | 真实来源 |
| --- | --- |
| `project_id` | 创建的 `data.public_id`，或项目 GET 的 `data.project_id` |
| `expected_version` | 每次 POST 前项目 GET 的 `data.version`，必须与用户正在复核的版本相同 |
| `page_ids` / `confirmed_pages` | 当前项目 `data.state.pages[].id`，不是页码整数 |
| 页面位置与尺寸 | `data.state.pages[]` 的 `file_id/physical_page/width/height/lines/coverage` 和授权 PNG 预览 |
| 候选 ID/位置 | 分析成功后重新 GET 的 `data.state.candidates[]` 的 `id/page_id/polygon/granularity` |
| `decisions/regions/confirmed_pages` | 展示上述页面及候选后用户的实际逐项决定、圈选和逐页确认 |
| `fingerprint` | review 成功任务的 `result.confirmation_fingerprint`，并与 GET 的 `data.state.confirmation.fingerprint` 核对 |
| `source_task_id` | 本人本产品成功 `redact.generate` 的外层 `task_id` |

inspect、locate、analyze、review 成功都会产生新修订；查询任务成功后重新 GET 项目，不自行将版本加一。不允许改写已提交请求去重试。generate、export 不创建确认修订；generate 前仍 GET 核对当前版本及冻结指纹。若文件、规则、定位、区域或候选决定变化，旧确认失效，重跑必要的检查/分析及用户复核，不把旧指纹套到新版本。export 只有 source_task_id，不支持随意添加版本、费用或格式字段。

## 本地检查资料：redact.inspect

上传全部文件后再检查，不调用 OCR；“本地”是平台服务端。最小请求：

```json
{"project_id":"<创建返回的 UUID>","expected_version":1}
```

任务成功结果含 `result.revision_id/project_version/page_count/candidate_count/coverage`。重新 GET 项目，读取每页尺寸、物理页码、文字位置和覆盖限制，并通过 GET `/api/v1/document-redaction/projects/{project}/pages/{page}` 获取真实 PNG，向用户展示。扫描/混合页没有可靠文字位置时不能宣称已完整扫描；可选择人工圈选，或明确授权 OCR。签名、加密、损坏文件及超资源预算明确拒绝处理。

## 可选付费识别：redact.locate

只对用户已选择且明确同意传给百炼、同意最高费用的页面执行：

```json
{"project_id":"<项目 UUID>","expected_version":2,"page_ids":["<当前页 UUID>"],"acknowledged_model_transfer":true}
```

page_ids 从当前 state.pages 取，1–50 项，不表示默认选择全部页。得到实际 words_info 行坐标后保存新版本；响应截断、无框、越界或未知用量不作为成功定位。多页会逐页保存并等待后续处理，持续查询同一任务，不新建请求重复 OCR。locate 后须重新 analyze、展示候选并复核。

## 免费规则匹配：redact.analyze

```json
{"project_id":"<项目 UUID>","expected_version":3,"configuration":"external_case","rules":{"phone":true,"email":true,"keywords":[]}}
```

跳过 locate 时使用 inspect 后的实际版本，不使用示例中的 3。`configuration` 是用户选定公开配置的标识，必须匹配 `[a-z][a-z0-9_-]{0,63}`，如 external_case、partner_materials；最多 5 个公开配置。规则只接受 phone/email 布尔值与 keywords 数组（最多 200 词，每词最多 120 字），不支持任意正则。

成功结果仅含候选数量等概况，完整候选从项目 GET 的 `data.state.candidates` 读取。结合相应 pages 与真实预览展示候选 ID、命中规则、物理页、位置、整行粒度和未覆盖限制；敏感原值仅在授权复核界面展示，避免复制到日志或对外包。结构化结果若有 `_truncated` 或 `_meta.truncated`，禁止当作完整候选清单或逐项确认依据；用管理 state 或工作台补齐。

## 免费人工确认：redact.review

仅在用户实际复核后构造。以下是“恰有一个候选、一个页面，用户明确选择保留”的结构；多候选、多页必须全部列出：

```json
{"project_id":"<项目 UUID>","expected_version":4,"decisions":[{"candidate_id":"<当前候选 id>","decision":"keep"}],"regions":[],"confirmed_pages":["<用户已确认的页 UUID>"]}
```

无候选且用户已逐页确认、也无需手工遮盖时 decisions/regions 都可为空，但不能从无命中自动推出此结论。用户决定处理候选时，相应项改为：

```json
{"candidate_id":"<当前候选 id>","decision":"process","region_id":"r1","region_confirmed":true}
```

regions 中加入对应区域，下面所有数值必须由该页真实图像与用户圈选取得，再写入 JSON number，不能直接发送占位字符串：

```json
{"id":"r1","page_id":"<对应页 UUID>","x":"<实测数字>","y":"<实测数字>","width":"<实测数字>","height":"<实测数字>","label":""}
```

原点为原页图左上，单位为原图像素；如果展示缩放，按原图 width/height 与实际显示区域比例转换，不用 PDF point、百分比或猜测数值。须在真实预览上叠加圈选让用户确认。区域必须完整覆盖候选 polygon 的整个包围范围，只有行级位置就覆盖整行，不能按字数等分伪造字符框；也允许用户独立圈选漏检区域。区域须正宽高、在页内、不重叠，id 唯一；label 可选、最多 40 字且不能含控制字符，不填敏感原值。decisions 必须覆盖每个候选且不重复，confirmed_pages 必须覆盖全部页（包括无候选页和覆盖不足页），禁止默认代签。

review 成功后取得 `result.confirmation_fingerprint` 和新 `result.project_version`，重新 GET 核对。若工具无法展示图像、交互画框或取得真实逐页确认，在 review 前停止，让用户登录脱敏工作台复核；不能把“继续”自动当成整份材料的逐项、逐页和收费授权。

## 付费生成及独立复检：redact.generate

展示当前全量 page_count、单价、总额并获得明确费用授权后：

```json
{"project_id":"<项目 UUID>","expected_version":5,"fingerprint":"<review 返回的 64 字符 confirmation_fingerprint>"}
```

只使用冻结内容，按实际解码像素遮盖，默认外扩 3 像素；标签容不下时失败。每个原 PDF 独立重建图片型 PDF，图片重新编码 PNG；检查结构、文字层、嵌入图像及区域内外像素。不能以搜索不到原文代替复检，失败/残留不交付。成功结果 `result.status` 为 confirmed_copy，附 page_count/fingerprint；保存外层 task_id 供导出。无下载 URL 时仅报告成功生成及对应任务，不声称已下载文件。

## 免费导出：redact.export

```json
{"source_task_id":"<成功 generate 的 task_id>"}
```

来源必须本人本产品成功且未过期的 generate 任务；导出已有成功副本，不重跑定位/生成，不重新按页收费。对外产物仅含安全编号副本及无原值覆盖说明。公开 artifacts 是元数据，用户应登录 `/dashboard/products/document-redaction/tasks/{task_id}` 下载对应任务产物，不从 artifact id 猜公开下载路径。原件、敏感词、原值、主体映射、原文件名、页预览和私有存储地址均不得混入对外包。
