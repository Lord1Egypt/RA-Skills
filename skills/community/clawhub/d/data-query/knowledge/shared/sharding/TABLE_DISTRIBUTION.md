# 表分片分布

## 一、分片说明

ACM 系统使用 ShardingSphere 管理分片。分片规则由 `application-tenant-tables.yml` 配置。

**分片变量：**
- `${spring.shardingsphere.master.base}` — base 库分片标识
- `${spring.shardingsphere.master.biz}` — biz 库分片标识

**分片命名格式：** `ds-${sharding-column-value}-master`

## 二、按业务域分类

### 计划管理域（wsd_plan_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| WSD_PLAN_BASELINE | ds-biz | - | 基线表 |
| WSD_PLAN_CHECK | ds-biz | - | 检查表 |
| WSD_PLAN_CONTACTS | ds-biz | - | 联系人表 |
| WSD_PLAN_CPRTM | ds-biz | - | 项目关系表 |
| WSD_PLAN_DEFIN | ds-biz | - | 项目定义表 |
| WSD_PLAN_DELVASSIGN | ds-biz | - | 交付分配表 |
| WSD_PLAN_DELVASSIGN_CHANGE | ds-biz | - | |
| WSD_PLAN_EARNEDLOG | ds-biz | - | 挣值日志 |
| WSD_PLAN_EPS | ds-biz | - | EPS表 |
| WSD_PLAN_FBS | ds-biz | - | FBS表 |
| WSD_PLAN_FEEDBACK | ds-biz | - | 反馈表 |
| WSD_PLAN_FEEDBACK_COOPERATE | ds-biz | - | |
| WSD_PLAN_PREPA | ds-biz | - | 准备表 |
| **WSD_PLAN_PROJECT** | ds-biz | TENANT_ID | 项目主表 ✅ |
| WSD_PLAN_PROJECTDELV | ds-biz | - | 项目交付表 |
| WSD_PLAN_PROJECTQUESTION | ds-biz | - | 项目问题表 |
| **WSD_PLAN_PROJECT_SUMMARY** | ds-biz | - | |
| **WSD_PLAN_PROJECT_SYNC** | ds-biz | - | |
| **WSD_PLAN_TASK** | ds-biz | PROJECT_ID, TENANT_ID | 任务表 ✅ |
| WSD_PLAN_TASKBAK | ds-biz | - | 任务备份 |
| WSD_PLAN_TASKCHANGE | ds-biz | - | 任务变更 |
| WSD_PLAN_TASKCHANGEAPPLY | ds-biz | - | 任务变更申请 |
| WSD_PLAN_TASKPRED | ds-biz | - | 任务前置 |
| WSD_PLAN_TASKPRED_CHANGE | ds-biz | - | |
| **WSD_PLAN_TASKRSRC** | ds-biz | PROJECT_ID, TENANT_ID | 任务资源 ✅ |
| WSD_PLAN_TASKRSRC_FEEDBACK | ds-biz | - | |
| WSD_PLAN_TASKRSRC_TIMESHEET | ds-biz | - | |
| WSD_PLAN_TASKRSRC_WORKHOUR | ds-biz | - | |
| WSD_PLAN_TASK_FORMDATA | ds-biz | - | |
| WSD_PLAN_TASK_STEPS | ds-biz | - | |
| WSD_PLAN_QUESTION | ds-biz | - | 问题表 |
| WSD_PLAN_QUESTION_REPLY | ds-biz | - | 问题回复 |
| WSD_PLAN_RELATION | ds-biz | - | 关系表 |
| WSD_PLAN_RISK_RELATION | ds-biz | - | |
| WSD_PLAN_SYNCPRO_RELATION | ds-biz | - | |
| WSD_PLAN_TWOSYSTEM | ds-biz | - | |

### 风险管理域（wsd_risk_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| **WSD_RISK_REGISTER** | ds-biz | PROJECT_ID, TENANT_ID | 风险登记 ✅ |
| WSD_RISK_CASE | ds-biz | - | 风险案例 |
| WSD_RISK_MATRIX | ds-biz | - | 风险矩阵 |
| WSD_RISK_MATRIX_IMPACT | ds-biz | - | |
| WSD_RISK_MATRIX_PROBABILITY | ds-biz | - | |
| WSD_RISK_MATRIX_TOLE | ds-biz | - | |
| WSD_RISK_RBS | ds-biz | - | RBS表 |
| WSD_RISK_RELATION | ds-biz | - | |
| WSD_RISK_RESPONSE_PLAN | ds-biz | - | 应对计划 |
| WSD_RISK_RESULT_CHANGE | ds-biz | - | |
| WSD_RISK_STATUS | ds-biz | - | |
| WSD_RISK_WBS_RELATION | ds-biz | - | |

### 资源管理域（wsd_rsrc_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| **WSD_RSRC_USER** | ds-biz | USER_ID | 资源用户 ✅ |
| WSD_RSRC_ANALYSIS | ds-biz | - | 资源分析 |
| WSD_RSRC_ASSIGN | ds-biz | - | 资源分配 |
| WSD_RSRC_EQUIP | ds-biz | - | 设备资源 |
| WSD_RSRC_EQUIPTYPE | ds-biz | - | |
| WSD_RSRC_MATERIAL | ds-biz | - | 物资资源 |
| WSD_RSRC_MATERIALTYPE | ds-biz | - | |
| WSD_RSRC_ROLE | ds-biz | - | 资源角色 |

### 系统域（wsd_sys_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| **WSD_SYS_USER** | ds-base | - | 系统用户 ⚠️ |
| **WSD_SYS_ORG** | ds-base | - | 系统组织 ⚠️ |
| WSD_SYS_COMMENTS | ds-biz | - | 评论 |
| WSD_SYS_FAVORITES | ds-biz | - | 收藏 |
| WSD_SYS_IPT | ds-biz | - | |
| WSD_SYS_LOG | ds-biz | - | 日志 |
| WSD_SYS_PWDRULE | ds-base | - | |
| WSD_SYS_TENANT | ds-base | - | 租户 |
| WSD_SYS_USERIPT | ds-biz | - | |
| WSD_SYS_USERIPT_ROLE | ds-biz | - | |
| WSD_SYS_USERORG | ds-base | - | |

### 文档域（wsd_doc_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| WSD_DOC | ds-biz | - | 文档表 |
| WSD_DOC_AUTH | ds-biz | - | |
| WSD_DOC_FAVORITE | ds-biz | - | |
| WSD_DOC_FAVORITE_RELATION | ds-biz | - | |
| WSD_DOC_FILE | ds-biz | - | |
| WSD_DOC_FILE_RELATION | ds-biz | - | |
| WSD_DOC_FOLDER | ds-biz | - | |
| WSD_DOC_RELATION | ds-biz | - | |

### 工作流域（wsd_wf_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| WSD_WF_ACTIVITY | ds-base | - | 活动 |
| WSD_WF_ASSIGN | ds-base | - | |
| WSD_WF_BIZTYPE | ds-base | - | |
| WSD_WF_DELEGATE | ds-base | - | |
| WSD_WF_DELEGATE_PROC | ds-base | - | |
| WSD_WF_FORM | ds-base | - | |
| WSD_WF_FORMDATA | ds-biz | - | |
| WSD_WF_HI_FORMDATA | ds-biz | - | |
| WSD_WF_LOG | ds-base | - | |

### 沟通域（wsd_comu_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| WSD_COMU_BRIEFING | ds-biz | - | 简报 |
| WSD_COMU_BRIEFING_TYPE | ds-biz | - | |
| WSD_COMU_MEETING | ds-biz | - | 会议 |
| WSD_COMU_MEETINGACTION | ds-biz | - | |
| WSD_COMU_QUEHANDLE | ds-biz | - | |
| WSD_COMU_QUESTION | ds-biz | - | 问答 |

### 基础域（wsd_base_*）

| 表名 | 分片归属 | 分片键 | 备注 |
|------|---------|--------|------|
| WSD_BASE_BO | ds-base | - | |
| WSD_BASE_CALENDAR | ds-base | - | |
| WSD_BASE_CLASSIFY | ds-base | - | |
| WSD_BASE_CLASSIFYASSIGN | ds-base | - | |
| WSD_BASE_CODERULE | ds-base | - | |
| WSD_BASE_CODERULE_BO | ds-base | - | |
| WSD_BASE_CODERULE_CELL | ds-base | - | |
| WSD_BASE_CODERULE_TYPE | ds-base | - | |
| WSD_BASE_CPRTM | ds-base | - | |
| WSD_BASE_CURRENCY | ds-base | - | |
| WSD_BASE_CUSTOM_FIELD | ds-base | - | |
| WSD_BASE_DICT | ds-base | - | |
| WSD_BASE_DICT_TYPE | ds-base | - | |
| WSD_BASE_SET | ds-base | - | |
| WSD_BASE_TIME | ds-base | - | |
| WSD_BASE_TMPLDELV | ds-base | - | |
| WSD_BASE_TMPLDELV_TYPE | ds-base | - | |
| WSD_BASE_TMPLDOC | ds-base | - | |
| WSD_BASE_TMPLFILE | ds-base | - | |
| WSD_BASE_TMPLPLAN | ds-base | - | |
| WSD_BASE_TMPLSTEPS | ds-base | - | |
| WSD_BASE_TMPLSTEPS_BO | ds-base | - | |
| WSD_BASE_TMPLTASK | ds-base | - | |
| WSD_BASE_TMPLTASKDELV | ds-base | - | |
| WSD_BASE_TMPLTASKPRED | ds-base | - | |

---

## 三、关键注意事项

### Cockpit 页面 SQL 涉及的表

| 表 | 分片 | 能否 JOIN wsd_plan_* 表 |
|---|------|------------------------|
| WSD_PLAN_PROJECT | ds-biz | ✅ 同一分片 |
| WSD_PLAN_TASK | ds-biz | ✅ 同一分片 |
| WSD_PLAN_TASKRSRC | ds-biz | ✅ 同一分片 |
| WSD_RSRC_USER | ds-biz | ✅ 同一分片 |
| WSD_RISK_REGISTER | ds-biz | ✅ 同一分片 |
| **WSD_SYS_USER** | **ds-base** | ❌ **跨分片，不能直接 JOIN** |
| **WSD_SYS_ORG** | **ds-base** | ❌ **跨分片，不能直接 JOIN** |

### 跨分片 JOIN 报错示例

```sql
-- ❌ 错误：wsd_sys_user 在 ds-base，wsd_plan_task 在 ds-biz，跨分片 JOIN 会失败
SELECT t.TASK_NAME, u.USER_NAME
FROM wsd_plan_task t
LEFT JOIN wsd_sys_user u ON t.USER_ID = u.ID
WHERE t.PROJECT_ID = ?

-- ✅ 正确：用 wsd_rsrc_user 代替
SELECT t.TASK_NAME, r.RSRCUSER_NAME AS USER_NAME
FROM wsd_plan_task t
LEFT JOIN wsd_rsrc_user r ON t.USER_ID = r.USER_ID
WHERE t.PROJECT_ID = ?
```

### 更新此文档

当新增表或修改分片策略时，必须同步更新本文件。
