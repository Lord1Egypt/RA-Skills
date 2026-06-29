# CSCSE / 留服认证 Analysis

## Purpose

Every CoopLens report must treat 留服认证 as a separate risk-and-value dimension, not only as a certificate footnote. The analysis should distinguish:

- Whether the project grants a foreign or overseas degree.
- Whether the degree has a plausible CSCSE/教育部留学服务中心 authentication path.
- Whether the result is likely to be a 中外合作办学学历学位认证、国境外学历学位认证、or another wording that affects family expectations.
- Whether the student has overseas study records and whether the family expects traditional overseas-student benefits.
- Whether domestic学籍、国内毕业证、国内学位证 already cover the family's domestic route even if the foreign degree is not treated as traditional overseas study.

Never write `一定能认证`, `保证认证`, or `等同海归` unless an official CSCSE source or school written answer for the exact project supports that claim. Prefer `需以教育部留学服务中心正式认证结果为准`.

## Runtime official-source targets

At every analysis run that involves foreign degree, overseas stage, 4+0, 2+2, 3+1, independent legal-person university, plan-outside program, or parent questions about recognition, search and open the latest available official sources:

1. 教育部留学服务中心 / 中国留学网: authentication introduction, guide, service agreement, material requirements, process, processing time, and online verification scope.
2. 国家政务服务平台 or official online service hall page for authentication application and result query.
3. 教育部中外合作办学监管工作信息平台 / CRS: project status, approval, certificate wording, mode, and validity.
4. School admissions charter, project brochure, official FAQ, and written school reply: certificate names, overseas requirement,学籍, enrollment mode, and prior graduate authentication evidence.
5. Provincial exam authority and school招生计划: whether the program is plan-in统招 and target-province enrollment is current.

## Required report fields

Use a dedicated module named `留服认证路径与风险`. It must contain:

- `认证对象`: which foreign/overseas degree or diploma would be submitted for authentication.
- `认证路径`: CSCSE path based on current official guidance and the project mode.
- `项目模式`: 4+0 / 2+2 / 3+1 / 1+3 / mixed / unknown.
- `境外学习记录`: whether overseas study is required, optional, absent, or unknown.
- `计划内/计划外`: whether domestic学籍 and domestic credentials exist.
- `认证结果预期`: authentication wording expectation and uncertainty; do not overpromise traditional overseas-student status.
- `官方证据`: links to CSCSE, CRS, school charter/FAQ, and written school answer if available.
- `风险等级`: 低 / 中 / 高 / 待核验.
- `家长书面提问`: exact questions for admissions office, college, international office, and registrar.

## Mode-specific interpretation

### Plan-in 4+0

- Usually the domestic route depends mainly on domestic学籍、国内毕业证、国内学位证 and project legality.
- If an overseas degree is granted without overseas residence, distinguish `foreign degree authentication` from `traditional overseas-student benefits`.
- Ask whether the authentication result would be marked or categorized as 中外合作办学 and whether past graduates have completed authentication.

### 2+2 / 3+1 / 1+3

- Verify overseas-study stage, foreign degree award conditions, GPA/language thresholds, visa and progression rules.
- Ask whether overseas learning duration, entry/exit records, and degree-awarding institution match CSCSE material requirements.
- Do not assume eligibility from the mode name alone.

### Plan-outside / international undergraduate / preparatory path

- Treat authentication as a high-risk dimension until the exact foreign degree, overseas study record, institution recognition, and CSCSE path are confirmed.
- Lack of domestic学籍 should be made explicit because it affects考公、考研、事业单位、国企 and some employer screening.
- Prior successful authentication examples help only if they are project-level and recent; anonymize any individual cases.

## Family-fit guidance

Tie 留服认证 to the family's goal:

- `考公/考编/国企`: prioritize domestic学籍、国内毕业证、国内学位证 and official major code; foreign-degree authentication is supplementary.
- `海外读研`: focus on foreign degree recognition, transcript language, GPA rules, recommendation letters, and overseas progression.
- `落户/留学生待遇`: do not infer eligibility from an overseas degree alone; check the target city's current policy and the CSCSE result wording.
- `预算紧张`: avoid projects that require an expensive overseas stage solely to make authentication expectations workable.

## Written questions to school

Use concrete questions:

1. 请书面确认该项目毕业后外方学位的准确英文/中文名称、颁发学校和证书样式。
2. 请书面确认该外方学位是否已有近三届毕业生完成教育部留学服务中心认证；如果有，请只提供去标识化的认证类别/结果口径，不提供姓名。
3. 请书面确认 4+0/2+2/3+1 路径下，是否必须出境学习才能取得外方学位或满足认证材料要求。
4. 请书面确认认证申请通常需要哪些材料由学校提供，例如成绩单、学习证明、授权声明、学籍证明、合作办学证明。
5. 请书面确认认证失败或无法申请时，学生仍可取得哪些国内证书，以及对考研、考公、就业的官方口径是什么。

## Decision impact

- If CSCSE/CRS/school evidence is clear and consistent: keep or upgrade recommendation confidence.
- If foreign degree exists but CSCSE path is unclear: downgrade to `观察` until written confirmation.
- If plan-outside and authentication path is unverified: place in `慎选` or `仅关注/待核验`.
- If the family relies on overseas-student benefits but the project is 4+0 without overseas record: explicitly warn that this expectation may not hold.
