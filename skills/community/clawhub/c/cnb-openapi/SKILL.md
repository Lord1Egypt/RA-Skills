---
name: CNB-OpenAPI
description: 与 CNB (Cloud Native Build) Open API 交互，用于代码管理和开发协作。当用户需要查询项目、代码仓库、问题、合并请求或其他开发相关数据时使用。需要 CNB_TOKEN 环境变量进行身份认证。API 请求地址从环境变量 CNB_API_ENDPOINT 获取，默认为 https://api.cnb.cool。
requires:
  bins: [curl]
  env: [CNB_TOKEN]
---

# CNB API 技能文档

## 技能概述

本技能提供 CNB (Cloud Native Build) Open API 的完整调用能力，支持所有 API 接口的调用和操作。每个 API 都有详细的文档说明，包含请求参数、响应格式和调用示例。

> **重要规则（必须遵守）：**
> 1. **必须实际执行**：访问 CNB API 时，必须通过 exec_command 工具实际执行 curl 命令，**不要只在回复中描述或展示 curl 命令**。用户需要的是 API 返回的结果，不是命令本身。
> 2. **使用 curl + Authorization**：不要使用 web_fetch 工具，因为 web_fetch 无法携带认证信息。
> 3. **使用环境变量**：始终使用 $CNB_TOKEN 和 $CNB_API_ENDPOINT 环境变量引用，不要使用 <CNB_TOKEN> 占位符。
> 4. **主动执行**：不要询问用户"是否需要我执行"，直接执行 curl 获取结果并分析。

## 页面 URL 解析规则

当用户提供 CNB 平台的页面链接时，需要从 URL 中提取参数来构造 API 请求：

| 页面 URL 格式 | 提取参数 | 对应 API |
|---|---|---|
| https://{host}/{repo}/-/build/logs/{sn} | repo, sn | GET /{repo}/-/build/status/{sn} 查状态，GET /{repo}/-/build/logs?sn={sn} 查日志列表 |
| https://{host}/{repo}/-/issues/{number} | repo, number | GET /{repo}/-/issues/{number} |
| https://{host}/{repo}/-/pulls/{number} | repo, number | GET /{repo}/-/pulls/{number} |
| https://{host}/{repo}/-/git/commits/{ref} | repo, ref | GET /{repo}/-/git/commits/{ref} |
| https://{host}/{repo} | repo | GET /{repo} |

**示例**：用户给了 https://{host}/{org}/{repo}/-/build/logs/{sn}
- 提取 repo = {org}/{repo}，sn = {sn}
- 先执行：curl ... "${CNB_API_ENDPOINT}/{org}/{repo}/-/build/status/{sn}" 获取构建状态
- 如需详细日志，再调用 stage 接口

## 基础配置

**API 基础地址：** 从环境变量 CNB_API_ENDPOINT 获取，默认为 https://api.cnb.cool

**认证方式：** Bearer Token

**环境变量：**
- CNB_TOKEN：身份认证令牌（必须）
- CNB_API_ENDPOINT：API 请求基础地址（可选，默认为 https://api.cnb.cool）

**请求头要求：**
- Accept: application/vnd.cnb.api+json
- Authorization: Bearer $CNB_TOKEN

## API 接口索引

### activities 服务

#### GetUserActivitiesByDate

**描述：** 获取个人动态活跃详情汇总。Get user activities by date.

**详细文档：** [GetUserActivitiesByDate.md](./references/activities/getuseractivitiesbydate.md)

---

#### GetUserRepoActivityDetails

**描述：** 个人仓库动态详情列表。List of personal repository activity details.

**详细文档：** [GetUserRepoActivityDetails.md](./references/activities/getuserrepoactivitydetails.md)

---

#### TopContributors

**描述：** 获取仓库 top 活跃用户。List the top active users

**详细文档：** [TopContributors.md](./references/activities/topcontributors.md)

---

### ai 服务

#### AiAutoPr

**描述：** 根据传入的需求内容和需求标题借助 AI 自动编码并提 PR。Automatically code and create a PR with AI based on the input requirement content and title.

**详细文档：** [AiAutoPr.md](./references/ai/aiautopr.md)

---

#### AiChatCompletions

**描述：** AI 对话。调用者需有代码写权限（CNB_TOKEN 仅需读权限，部署令牌不检查读写权限）。AI chat completions. Requires caller to have repo write permission.

**详细文档：** [AiChatCompletions.md](./references/ai/aichatcompletions.md)

---

### assets 服务

#### DeleteAsset

**描述：** 通过 asset 记录 id 删除一个 asset

**详细文档：** [DeleteAsset.md](./references/assets/deleteasset.md)

---

#### ListAssets

**描述：** 仓库的 asset 记录列表

**详细文档：** [ListAssets.md](./references/assets/listassets.md)

---

### badge 服务

#### GetBadge

**描述：** 获取徽章 svg 或 JSON 数据。Get badge svg or JSON data.

**详细文档：** [GetBadge.md](./references/badge/getbadge.md)

---

#### ListBadge

**描述：** 获取徽章列表数据。List badge data

**详细文档：** [ListBadge.md](./references/badge/listbadge.md)

---

#### UploadBadge

**描述：** 上传徽章数据。Upload badge data

**详细文档：** [UploadBadge.md](./references/badge/uploadbadge.md)

---

### build 服务

#### BuildCrontabSync

**描述：** 同步仓库分支下的定时任务。 Synchronize the content under the repository branch.

**详细文档：** [BuildCrontabSync.md](./references/build/buildcrontabsync.md)

---

#### BuildLogsDelete

**描述：** 删除流水线日志内容。Delete pipeline logs content.

**详细文档：** [BuildLogsDelete.md](./references/build/buildlogsdelete.md)

---

#### BuildRunnerDownloadLog

**描述：** 流水线runner日志下载。Pipeline runner log download.

**详细文档：** [BuildRunnerDownloadLog.md](./references/build/buildrunnerdownloadlog.md)

---

#### GetBuildLogs

**描述：** 查询流水线构建列表。List pipeline builds.

**详细文档：** [GetBuildLogs.md](./references/build/getbuildlogs.md)

---

#### GetBuildStage

**描述：** 查询流水线Stage详情。Get pipeline build stage detail.

**详细文档：** [GetBuildStage.md](./references/build/getbuildstage.md)

---

#### GetBuildStatus

**描述：** 查询流水线构建状态。Get pipeline build status.

**详细文档：** [GetBuildStatus.md](./references/build/getbuildstatus.md)

---

#### StartBuild

**描述：** 开始一个构建。Start a build.

**详细文档：** [StartBuild.md](./references/build/startbuild.md)

---

#### StopBuild

**描述：** 停止一个构建。 Stop a build.

**详细文档：** [StopBuild.md](./references/build/stopbuild.md)

---

### charge 服务

#### GetSpecialAmount

**描述：** 查看特权额度

**详细文档：** [GetSpecialAmount.md](./references/charge/getspecialamount.md)

---

### event 服务

#### GetEvents

**描述：** 获取仓库动态预签名地址，并返回内容。Get events pre-signed URL and return content.

**详细文档：** [GetEvents.md](./references/event/getevents.md)

---

### followers 服务

#### GetFollowersByUserID

**描述：** 获取指定用户的粉丝列表。Get the followers list of specified user.

**详细文档：** [GetFollowersByUserID.md](./references/followers/getfollowersbyuserid.md)

---

#### GetFollowingByUserID

**描述：** 获取指定用户的关注人列表。Get the list of users that the specified user is following.

**详细文档：** [GetFollowingByUserID.md](./references/followers/getfollowingbyuserid.md)

---

### git 服务

#### CreateBlob

**描述：** 创建一个 blob。Create a blob.

**详细文档：** [CreateBlob.md](./references/git/createblob.md)

---

#### CreateBranch

**描述：** 创建新分支。Create a new branch based on a start point.

**详细文档：** [CreateBranch.md](./references/git/createbranch.md)

---

#### CreateBranchLock

**描述：** 锁定分支

**详细文档：** [CreateBranchLock.md](./references/git/createbranchlock.md)

---

#### CreateTag

**描述：** 创建一个 tag。Create a tag.

**详细文档：** [CreateTag.md](./references/git/createtag.md)

---

#### DeleteBranch

**描述：** 删除指定分支。Delete the specified branch.

**详细文档：** [DeleteBranch.md](./references/git/deletebranch.md)

---

#### DeleteBranchLock

**描述：** 解除锁定分支

**详细文档：** [DeleteBranchLock.md](./references/git/deletebranchlock.md)

---

#### DeleteCommitAnnotation

**描述：** 删除指定 commit 的元数据。Delete commit annotation.

**详细文档：** [DeleteCommitAnnotation.md](./references/git/deletecommitannotation.md)

---

#### DeleteCommitAsset

**描述：** 删除指定 commit 的附件。Delete commit asset.

**详细文档：** [DeleteCommitAsset.md](./references/git/deletecommitasset.md)

---

#### DeleteTag

**描述：** 删除指定 tag。Delete the specified tag.

**详细文档：** [DeleteTag.md](./references/git/deletetag.md)

---

#### DeleteTagAnnotation

**描述：** 删除指定 tag 的元数据。Delete the metadata of the specified tag.

**详细文档：** [DeleteTagAnnotation.md](./references/git/deletetagannotation.md)

---

#### GetArchive

**描述：** 下载仓库内容

**详细文档：** [GetArchive.md](./references/git/getarchive.md)

---

#### GetArchiveCommitChangedFiles

**描述：** 打包下载 commit 变更文件。Download archive of changed files for a commit.

**详细文档：** [GetArchiveCommitChangedFiles.md](./references/git/getarchivecommitchangedfiles.md)

---

#### GetArchiveCompareChangedFiles

**描述：** 打包下载两次 ref 之间的变更文件。Download archive of changed files for a compare.

**详细文档：** [GetArchiveCompareChangedFiles.md](./references/git/getarchivecomparechangedfiles.md)

---

#### GetBranch

**描述：** 查询指定分支。Get a branch.

**详细文档：** [GetBranch.md](./references/git/getbranch.md)

---

#### GetCommit

**描述：** 查询指定 commit。Get a commit.

**详细文档：** [GetCommit.md](./references/git/getcommit.md)

---

#### GetCommitAnnotations

**描述：** 查询指定 commit 的元数据。Get commit annotations.

**详细文档：** [GetCommitAnnotations.md](./references/git/getcommitannotations.md)

---

#### GetCommitAnnotationsInBatch

**描述：** 查询指定 commit 的元数据。Get commit annotations in batch.

**详细文档：** [GetCommitAnnotationsInBatch.md](./references/git/getcommitannotationsinbatch.md)

---

#### GetCommitAssets

**描述：** 发起一个获取 commits 附件的请求， 302到有一定效期的下载地址。Get a request to fetch a commit assets and returns 302 redirect to the assets URL with specific valid time.

**详细文档：** [GetCommitAssets.md](./references/git/getcommitassets.md)

---

#### GetCommitAssetsBySha

**描述：** 查询指定 commit 的附件。List commit assets.

**详细文档：** [GetCommitAssetsBySha.md](./references/git/getcommitassetsbysha.md)

---

#### GetCommitStatuses

**描述：** 查询指定 commit 的提交状态。List commit check statuses.

**详细文档：** [GetCommitStatuses.md](./references/git/getcommitstatuses.md)

---

#### GetCompareCommits

**描述：** 比较两个提交、分支或标签之间差异的接口。Compare two commits, branches, or tags.

**详细文档：** [GetCompareCommits.md](./references/git/getcomparecommits.md)

---

#### GetContent

**描述：** 查询仓库文件列表或文件。List repository files or file.

**详细文档：** [GetContent.md](./references/git/getcontent.md)

---

#### GetContentWithoutPath

**描述：** 查询仓库文件和目录内容。List repository files and directories.

**详细文档：** [GetContentWithoutPath.md](./references/git/getcontentwithoutpath.md)

---

#### GetHead

**描述：** 获取仓库默认分支。Get the default branch of the repository.

**详细文档：** [GetHead.md](./references/git/gethead.md)

---

#### GetPresignedLFSDownloadLink

**描述：** 获取 git lfs 文件下载链接

**详细文档：** [GetPresignedLFSDownloadLink.md](./references/git/getpresignedlfsdownloadlink.md)

---

#### GetRaw

**描述：** 获得仓库指定文件内容

**详细文档：** [GetRaw.md](./references/git/getraw.md)

---

#### GetTag

**描述：** 查询指定 tag。Get a tag.

**详细文档：** [GetTag.md](./references/git/gettag.md)

---

#### GetTagAnnotations

**描述：** 查询指定 tag 的元数据。Query the metadata of the specified tag.

**详细文档：** [GetTagAnnotations.md](./references/git/gettagannotations.md)

---

#### ListBranches

**描述：** 查询分支列表。List branches.

**详细文档：** [ListBranches.md](./references/git/listbranches.md)

---

#### ListCommits

**描述：** 查询 commit 列表。List commits.

**详细文档：** [ListCommits.md](./references/git/listcommits.md)

---

#### ListTags

**描述：** 查询 tag 列表。List tags.

**详细文档：** [ListTags.md](./references/git/listtags.md)

---

#### PostCommitAssetUploadConfirmation

**描述：** 确认 commit 附件上传完成。Confirm commit asset upload.

**详细文档：** [PostCommitAssetUploadConfirmation.md](./references/git/postcommitassetuploadconfirmation.md)

---

#### PostCommitAssetUploadURL

**描述：** 新增一个 commit 附件。Create a commit asset.

**详细文档：** [PostCommitAssetUploadURL.md](./references/git/postcommitassetuploadurl.md)

---

#### PutCommitAnnotations

**描述：** 设定指定 commit 的元数据。Put commit annotations.

**详细文档：** [PutCommitAnnotations.md](./references/git/putcommitannotations.md)

---

#### PutTagAnnotations

**描述：** 设定指定 tag 的元数据。Set the metadata of the specified tag.

**详细文档：** [PutTagAnnotations.md](./references/git/puttagannotations.md)

---

### gitsettings 服务

#### DeleteBranchProtection

**描述：** 删除仓库保护分支规则。 Delete branch protection rule.

**详细文档：** [DeleteBranchProtection.md](./references/gitsettings/deletebranchprotection.md)

---

#### GetBranchProtection

**描述：** 查询仓库保护分支规则。Get branch protection rule.

**详细文档：** [GetBranchProtection.md](./references/gitsettings/getbranchprotection.md)

---

#### GetPipelineSettings

**描述：** 查询仓库云原生构建设置。List pipeline settings.

**详细文档：** [GetPipelineSettings.md](./references/gitsettings/getpipelinesettings.md)

---

#### GetPullRequestSettings

**描述：** 查询仓库合并请求设置。List pull request settings.

**详细文档：** [GetPullRequestSettings.md](./references/gitsettings/getpullrequestsettings.md)

---

#### GetPushLimitSettings

**描述：** 查询仓库推送设置。List push limit settings.

**详细文档：** [GetPushLimitSettings.md](./references/gitsettings/getpushlimitsettings.md)

---

#### ListBranchProtections

**描述：** 查询仓库保护分支规则列表。List branch protection rules.

**详细文档：** [ListBranchProtections.md](./references/gitsettings/listbranchprotections.md)

---

#### PatchBranchProtection

**描述：** 更新仓库保护分支规则。Update branch protection rule.

**详细文档：** [PatchBranchProtection.md](./references/gitsettings/patchbranchprotection.md)

---

#### PostBranchProtection

**描述：** 新增仓库保护分支规则。Create branch protection rule.

**详细文档：** [PostBranchProtection.md](./references/gitsettings/postbranchprotection.md)

---

#### PutPipelineSettings

**描述：** 更新仓库云原生构建设置。Update pipeline settings.

**详细文档：** [PutPipelineSettings.md](./references/gitsettings/putpipelinesettings.md)

---

#### PutPullRequestSettings

**描述：** 更新仓库合并请求设置。Set pull request settings.

**详细文档：** [PutPullRequestSettings.md](./references/gitsettings/putpullrequestsettings.md)

---

#### PutPushLimitSettings

**描述：** 设置仓库推送设置。Set push limit settings.

**详细文档：** [PutPushLimitSettings.md](./references/gitsettings/putpushlimitsettings.md)

---

### issues 服务

#### CanUserBeAssignedToIssue

**描述：** 检查用户是否可以被添加到 issue 的处理人中。 Checks if a user can be assigned to an issue.

**详细文档：** [CanUserBeAssignedToIssue.md](./references/issues/canuserbeassignedtoissue.md)

---

#### CreateIssue

**描述：** 创建一个 Issue。Create an issue.

**详细文档：** [CreateIssue.md](./references/issues/createissue.md)

---

#### DeleteIssueAssignees

**描述：** 删除 issue 中的处理人。 Removes one or more assignees from an issue.

**详细文档：** [DeleteIssueAssignees.md](./references/issues/deleteissueassignees.md)

---

#### DeleteIssueLabel

**描述：** 删除 issue 标签。Remove a label from an issue.

**详细文档：** [DeleteIssueLabel.md](./references/issues/deleteissuelabel.md)

---

#### DeleteIssueLabels

**描述：** 清空 issue 标签。Remove all labels from an issue.

**详细文档：** [DeleteIssueLabels.md](./references/issues/deleteissuelabels.md)

---

#### GetIssue

**描述：** 查询指定的 Issues。Get an issue.

**详细文档：** [GetIssue.md](./references/issues/getissue.md)

---

#### GetIssueComment

**描述：** 获取指定 issue 评论。Get an issue comment.

**详细文档：** [GetIssueComment.md](./references/issues/getissuecomment.md)

---

#### ListIssueAssignees

**描述：** 查询指定 issue 的处理人。 List repository issue assignees.

**详细文档：** [ListIssueAssignees.md](./references/issues/listissueassignees.md)

---

#### ListIssueComments

**描述：** 查询仓库的 issue 评论列表。List repository issue comments.

**详细文档：** [ListIssueComments.md](./references/issues/listissuecomments.md)

---

#### ListIssueLabels

**描述：** 查询 issue 的标签列表。List labels for an issue.

**详细文档：** [ListIssueLabels.md](./references/issues/listissuelabels.md)

---

#### ListIssues

**描述：** 查询仓库的 Issues。List issues.

**详细文档：** [ListIssues.md](./references/issues/listissues.md)

---

#### PatchIssueAssignees

**描述：** 更新 issue 中的处理人。 Updates the assignees of an issue.

**详细文档：** [PatchIssueAssignees.md](./references/issues/patchissueassignees.md)

---

#### PatchIssueComment

**描述：** 修改一个 issue 评论。Update an issue comment.

**详细文档：** [PatchIssueComment.md](./references/issues/patchissuecomment.md)

---

#### PostIssueAssignees

**描述：** 添加处理人到指定的 issue。  Adds up to assignees to a issue, Users already assigned to an issue are not replaced.

**详细文档：** [PostIssueAssignees.md](./references/issues/postissueassignees.md)

---

#### PostIssueComment

**描述：** 创建一个 issue 评论。Create an issue comment.

**详细文档：** [PostIssueComment.md](./references/issues/postissuecomment.md)

---

#### PostIssueLabels

**描述：** 新增 issue 标签。Add labels to an issue.

**详细文档：** [PostIssueLabels.md](./references/issues/postissuelabels.md)

---

#### PutIssueLabels

**描述：** 设置 issue 标签。 Set the new labels for an issue.

**详细文档：** [PutIssueLabels.md](./references/issues/putissuelabels.md)

---

#### UpdateIssue

**描述：** 更新一个 Issue。Update an issue.

**详细文档：** [UpdateIssue.md](./references/issues/updateissue.md)

---

#### UpdateIssueProperties

**描述：** 批量更新Issue自定义属性值

**详细文档：** [UpdateIssueProperties.md](./references/issues/updateissueproperties.md)

---

### knowledgebase 服务

#### DeleteKnowledgeBase

**描述：** 删除知识库

**详细文档：** [DeleteKnowledgeBase.md](./references/knowledgebase/deleteknowledgebase.md)

---

#### GetKnowledgeBaseInfo

**描述：** 获取知识库信息

**详细文档：** [GetKnowledgeBaseInfo.md](./references/knowledgebase/getknowledgebaseinfo.md)

---

#### GetModels

**描述：** 获取当前支持的 Embedding 模型列表

**详细文档：** [GetModels.md](./references/knowledgebase/getmodels.md)

---

#### QueryKnowledgeBase

**描述：** 查询知识库，使用文档：https://docs.cnb.cool/zh/ai/knowledge-base.html

**详细文档：** [QueryKnowledgeBase.md](./references/knowledgebase/queryknowledgebase.md)

---

### members 服务

#### AddMembersOfGroup

**描述：** 添加成员。Add members.

**详细文档：** [AddMembersOfGroup.md](./references/members/addmembersofgroup.md)

---

#### AddMembersOfMission

**描述：** 添加成员。Add members.

**详细文档：** [AddMembersOfMission.md](./references/members/addmembersofmission.md)

---

#### AddMembersOfRegistry

**描述：** 添加成员。Add members.

**详细文档：** [AddMembersOfRegistry.md](./references/members/addmembersofregistry.md)

---

#### AddMembersOfRepo

**描述：** 添加成员。Add members.

**详细文档：** [AddMembersOfRepo.md](./references/members/addmembersofrepo.md)

---

#### DeleteMembersOfGroup

**描述：** 删除指定组织的直接成员。Remove direct members from specified organization.

**详细文档：** [DeleteMembersOfGroup.md](./references/members/deletemembersofgroup.md)

---

#### DeleteMembersOfRepo

**描述：** 删除指定仓库的直接成员。Remove direct members from specified repository.

**详细文档：** [DeleteMembersOfRepo.md](./references/members/deletemembersofrepo.md)

---

#### DeleteOutsideCollaborators

**描述：** 删除指定仓库的外部贡献者。Removes external contributors from specified repository.

**详细文档：** [DeleteOutsideCollaborators.md](./references/members/deleteoutsidecollaborators.md)

---

#### GetMemberAccessLevelOfGroup

**描述：** 获取指定组织内, 访问成员在当前层级内的权限信息。Get permission information for accessing members at current level.

**详细文档：** [GetMemberAccessLevelOfGroup.md](./references/members/getmemberaccesslevelofgroup.md)

---

#### GetMemberAccessLevelOfRepo

**描述：** 获取指定仓库内, 访问成员在当前层级内的权限信息。Get permission information for accessing members at current level.

**详细文档：** [GetMemberAccessLevelOfRepo.md](./references/members/getmemberaccesslevelofrepo.md)

---

#### ListAllMembers

**描述：** 获取指定仓库内的有效成员列表，包含继承成员。List active members in specified repository including inherited members.

**详细文档：** [ListAllMembers.md](./references/members/listallmembers.md)

---

#### ListInheritMembersOfGroup

**描述：** 获取指定组织的继承成员。List inherited members within specified organization

**详细文档：** [ListInheritMembersOfGroup.md](./references/members/listinheritmembersofgroup.md)

---

#### ListInheritMembersOfRepo

**描述：** 获取指定仓库内的继承成员。List inherited members within specified repository。

**详细文档：** [ListInheritMembersOfRepo.md](./references/members/listinheritmembersofrepo.md)

---

#### ListMemberAccessLevelOfGroup

**描述：** 获取指定组织内指定成员的权限信息, 结果按组织层级来展示, 包含上层组织的权限继承信息。Get specified member's permissions with organizational hierarchy.

**详细文档：** [ListMemberAccessLevelOfGroup.md](./references/members/listmemberaccesslevelofgroup.md)

---

#### ListMemberAccessLevelOfRepo

**描述：** 获取指定仓库内指定成员的权限信息, 结果按组织层级来展示, 包含上层组织的权限继承信息。Get specified member's permissions with organizational hierarchy.

**详细文档：** [ListMemberAccessLevelOfRepo.md](./references/members/listmemberaccesslevelofrepo.md)

---

#### ListMembersOfGroup

**描述：** 获取指定组织内的所有直接成员。List all direct members within specified organization.

**详细文档：** [ListMembersOfGroup.md](./references/members/listmembersofgroup.md)

---

#### ListMembersOfRepo

**描述：** 获取指定仓库内的所有直接成员。List all direct members within specified repository.

**详细文档：** [ListMembersOfRepo.md](./references/members/listmembersofrepo.md)

---

#### ListOutsideCollaborators

**描述：** 获取指定仓库内的外部贡献者。List external contributors in specified repository.

**详细文档：** [ListOutsideCollaborators.md](./references/members/listoutsidecollaborators.md)

---

#### UpdateMembersOfGroup

**描述：** 更新指定组织的直接成员权限信息。Update permission information for direct members in specified organization.

**详细文档：** [UpdateMembersOfGroup.md](./references/members/updatemembersofgroup.md)

---

#### UpdateMembersOfRepo

**描述：** 更新指定仓库内的直接成员权限信息。Update permission information for direct members in specified repository.

**详细文档：** [UpdateMembersOfRepo.md](./references/members/updatemembersofrepo.md)

---

#### UpdateOutsideCollaborators

**描述：** 更新指定仓库的外部贡献者权限信息。 Update permission information for external contributors in specified repository.

**详细文档：** [UpdateOutsideCollaborators.md](./references/members/updateoutsidecollaborators.md)

---

### missions 服务

#### CreateMission

**描述：** 创建任务集。Create a mission.

**详细文档：** [CreateMission.md](./references/missions/createmission.md)

---

#### DeleteMission

**描述：** 删除指定任务集。Delete the specified mission.

**详细文档：** [DeleteMission.md](./references/missions/deletemission.md)

---

#### GetGroupSubMissions

**描述：** 查询组织下面用户有权限查看到的任务集。Query all missions that the user has permission to see under the specific organization.

**详细文档：** [GetGroupSubMissions.md](./references/missions/getgroupsubmissions.md)

---

#### GetMissionViewConfig

**描述：** 查询任务集视图配置信息。Get mission view config.

**详细文档：** [GetMissionViewConfig.md](./references/missions/getmissionviewconfig.md)

---

#### GetMissionViewList

**描述：** 获取任务集视图列表。Get view list of a mission.

**详细文档：** [GetMissionViewList.md](./references/missions/getmissionviewlist.md)

---

#### PostMissionViewConfig

**描述：** 设置任务集视图配置信息。Set mission view config.

**详细文档：** [PostMissionViewConfig.md](./references/missions/postmissionviewconfig.md)

---

#### PostMissionViewList

**描述：** 排序任务集视图。Sort mission view list.

**详细文档：** [PostMissionViewList.md](./references/missions/postmissionviewlist.md)

---

#### PutMissionViewList

**描述：** 添加、修改任务集视图。Update a mission view or add a new one.

**详细文档：** [PutMissionViewList.md](./references/missions/putmissionviewlist.md)

---

#### SetMissionVisibility

**描述：** 改变任务集可见性。Update the visibility of a mission.

**详细文档：** [SetMissionVisibility.md](./references/missions/setmissionvisibility.md)

---

### organizations 服务

#### CreateOrganization

**描述：** 创建新组织。Create new organization.

**详细文档：** [CreateOrganization.md](./references/organizations/createorganization.md)

---

#### DeleteOrganization

**描述：** 删除指定组织。Delete the specified organization.

**详细文档：** [DeleteOrganization.md](./references/organizations/deleteorganization.md)

---

#### GetGroup

**描述：** 获取指定组织信息。Get information for the specified organization.

**详细文档：** [GetGroup.md](./references/organizations/getgroup.md)

---

#### GetGroupSetting

**描述：** 获取指定组织的配置详情。Get the configuration details for the specified organization.

**详细文档：** [GetGroupSetting.md](./references/organizations/getgroupsetting.md)

---

#### GetGroupsByUserID

**描述：** 获取指定用户拥有权限的顶层组织列表。 Get a list of top-level organizations that the specified user has permissions to access.

**详细文档：** [GetGroupsByUserID.md](./references/organizations/getgroupsbyuserid.md)

---

#### ListGroups

**描述：** 查询当前用户在指定组织下拥有指定权限的子组织列表。Get the list of sub-organizations that the current user has access to in the specified organization.

**详细文档：** [ListGroups.md](./references/organizations/listgroups.md)

---

#### ListSubgroups

**描述：** 获取指定组织下的子组织列表。Get the list of sub-organizations under the specified organization.

**详细文档：** [ListSubgroups.md](./references/organizations/listsubgroups.md)

---

#### ListTopGroups

**描述：** 获取当前用户拥有权限的顶层组织列表。Get top-level organizations list that the current user has access to.

**详细文档：** [ListTopGroups.md](./references/organizations/listtopgroups.md)

---

#### TransferGroup

**描述：** 转移组织。Transfer an organization.

**详细文档：** [TransferGroup.md](./references/organizations/transfergroup.md)

---

#### UpdateGroupSetting

**描述：** 更新指定组织的配置。Updates the configuration for the specified organization.

**详细文档：** [UpdateGroupSetting.md](./references/organizations/updategroupsetting.md)

---

#### UpdateOrganization

**描述：** 更新组织信息, 可更新的内容为: 组织描述, 组织展示名称, 组织网站, 组织联系邮箱。Updates organization information including: description, display name, website URL and contact email.

**详细文档：** [UpdateOrganization.md](./references/organizations/updateorganization.md)

---

#### UploadLogos

**描述：** 发起一个上传 logo 的请求，返回上传文件的url，请使用 put 发起流式上传。Initiate a request to upload logo,returns upload URL.Use PUT to initiate a stream upload.

**详细文档：** [UploadLogos.md](./references/organizations/uploadlogos.md)

---

### pulls 服务

#### CanUserBeAssignedToPull

**描述：** 检查用户是否可以被添加到合并请求的处理人中。 Checks if a user can be assigned to a pull request.

**详细文档：** [CanUserBeAssignedToPull.md](./references/pulls/canuserbeassignedtopull.md)

---

#### DeletePullAssignees

**描述：** 删除合并请求中的处理人 Removes one or more assignees from a pull request.

**详细文档：** [DeletePullAssignees.md](./references/pulls/deletepullassignees.md)

---

#### DeletePullLabel

**描述：** 删除合并请求标签。Remove a label from a pull.

**详细文档：** [DeletePullLabel.md](./references/pulls/deletepulllabel.md)

---

#### DeletePullLabels

**描述：** 清空合并请求标签。Remove all labels from a pull.

**详细文档：** [DeletePullLabels.md](./references/pulls/deletepulllabels.md)

---

#### DeleteRepoFiles

**描述：** 删除 UploadFiles 上传的附件

**详细文档：** [DeleteRepoFiles.md](./references/pulls/deleterepofiles.md)

---

#### DeleteRepoImgs

**描述：** 删除 UploadImgs 上传的图片

**详细文档：** [DeleteRepoImgs.md](./references/pulls/deleterepoimgs.md)

---

#### GetPull

**描述：** 查询指定合并请求。Get a pull request.

**详细文档：** [GetPull.md](./references/pulls/getpull.md)

---

#### GetPullComment

**描述：** 获取一个合并请求评论。Get a pull comment.

**详细文档：** [GetPullComment.md](./references/pulls/getpullcomment.md)

---

#### ListPullAssignees

**描述：** 查询指定合并请求的处理人。List repository pull request assignees.

**详细文档：** [ListPullAssignees.md](./references/pulls/listpullassignees.md)

---

#### ListPullComments

**描述：** 查询合并请求评论列表。List pull comments requests.

**详细文档：** [ListPullComments.md](./references/pulls/listpullcomments.md)

---

#### ListPullCommitStatuses

**描述：** 查询 Pull Request 的状态检查

**详细文档：** [ListPullCommitStatuses.md](./references/pulls/listpullcommitstatuses.md)

---

#### ListPullCommits

**描述：** 查询指定合并请求的提交列表。Lists the commits in a specified pull request.

**详细文档：** [ListPullCommits.md](./references/pulls/listpullcommits.md)

---

#### ListPullFiles

**描述：** 查询指定合并请求的文件列表。Lists the files in a specified pull request.

**详细文档：** [ListPullFiles.md](./references/pulls/listpullfiles.md)

---

#### ListPullLabels

**描述：** 查询指定合并请求的标签列表。List labels for a pull.

**详细文档：** [ListPullLabels.md](./references/pulls/listpulllabels.md)

---

#### ListPullReviewComments

**描述：** 查询指定合并请求评审评论列表。List pull review comments.

**详细文档：** [ListPullReviewComments.md](./references/pulls/listpullreviewcomments.md)

---

#### ListPullReviews

**描述：** 查询特定合并请求的评审列表。List pull reviews.

**详细文档：** [ListPullReviews.md](./references/pulls/listpullreviews.md)

---

#### ListPulls

**描述：** 查询合并请求列表。List pull requests.

**详细文档：** [ListPulls.md](./references/pulls/listpulls.md)

---

#### ListPullsByNumbers

**描述：** 根据 number 列表查询合并请求列表。List pull requests by numbers.

**详细文档：** [ListPullsByNumbers.md](./references/pulls/listpullsbynumbers.md)

---

#### MergePull

**描述：** 合并一个合并请求。Merge a pull request.

**详细文档：** [MergePull.md](./references/pulls/mergepull.md)

---

#### PatchPull

**描述：** 更新一个合并请求。Update a pull request.

**详细文档：** [PatchPull.md](./references/pulls/patchpull.md)

---

#### PatchPullComment

**描述：** 更新一个合并请求评论。Update a pull comment.

**详细文档：** [PatchPullComment.md](./references/pulls/patchpullcomment.md)

---

#### PostPull

**描述：** 新增一个合并请求。Create a pull request.

**详细文档：** [PostPull.md](./references/pulls/postpull.md)

---

#### PostPullAssignees

**描述：** 添加处理人到指定的合并请求。 Adds up to assignees to a pull request. Users already assigned to an issue are not replaced.

**详细文档：** [PostPullAssignees.md](./references/pulls/postpullassignees.md)

---

#### PostPullComment

**描述：** 新增一个合并请求评论。Create a pull comment.

**详细文档：** [PostPullComment.md](./references/pulls/postpullcomment.md)

---

#### PostPullLabels

**描述：** 新增合并请求标签。Add labels to a pull.

**详细文档：** [PostPullLabels.md](./references/pulls/postpulllabels.md)

---

#### PostPullRequestReviewReply

**描述：** 回复一个 review 评审

**详细文档：** [PostPullRequestReviewReply.md](./references/pulls/postpullrequestreviewreply.md)

---

#### PostPullReview

**描述：** 新增一次合并请求评审。Create a pull review.

**详细文档：** [PostPullReview.md](./references/pulls/postpullreview.md)

---

#### PutPullLabels

**描述：** 设置合并请求标签。Set the new labels for a pull.

**详细文档：** [PutPullLabels.md](./references/pulls/putpulllabels.md)

---

#### UploadFiles

**描述：** 发起一个上传 files 的请求，返回上传文件的url，请使用 put 发起流式上传。Initiate a request to upload files,returns upload URL.Use PUT to initiate a stream upload.

**详细文档：** [UploadFiles.md](./references/pulls/uploadfiles.md)

---

#### UploadImgs

**描述：** 发起一个上传 imgs 的请求，返回上传文件的url，请使用 put 发起流式上传。Initiate a request to upload images,returns upload URL.Use PUT to initiate a stream upload.

**详细文档：** [UploadImgs.md](./references/pulls/uploadimgs.md)

---

### registries 服务

#### DeletePackage

**描述：** 删除制品。 Delete the specific package.

**详细文档：** [DeletePackage.md](./references/registries/deletepackage.md)

---

#### DeletePackageTag

**描述：** 删除制品标签。 Delete the specific tag under specific package

**详细文档：** [DeletePackageTag.md](./references/registries/deletepackagetag.md)

---

#### DeleteRegistry

**描述：** 删除制品库。Delete the registry.

**详细文档：** [DeleteRegistry.md](./references/registries/deleteregistry.md)

---

#### GetGroupSubRegistries

**描述：** 查询组织下面用户有权限查看到的制品仓库。Query all registries that the user has permission to see under specific organization.

**详细文档：** [GetGroupSubRegistries.md](./references/registries/getgroupsubregistries.md)

---

#### GetPackage

**描述：** 获取指定制品的详细信息。 Get the package detail.

**详细文档：** [GetPackage.md](./references/registries/getpackage.md)

---

#### GetPackageTagDetail

**描述：** 获取制品标签详情。 Get the specific tag under specific package.

**详细文档：** [GetPackageTagDetail.md](./references/registries/getpackagetagdetail.md)

---

#### ListPackageTags

**描述：** 查询制品标签列表。 List all tags under specific package.

**详细文档：** [ListPackageTags.md](./references/registries/listpackagetags.md)

---

#### ListPackages

**描述：** 查询制品列表。 List all packages.

**详细文档：** [ListPackages.md](./references/registries/listpackages.md)

---

#### SetRegistryVisibility

**描述：** 改变制品仓库可见性。Update visibility of registry.

**详细文档：** [SetRegistryVisibility.md](./references/registries/setregistryvisibility.md)

---

### releases 服务

#### DeleteRelease

**描述：** 删除指定的 release。Delete a release.

**详细文档：** [DeleteRelease.md](./references/releases/deleterelease.md)

---

#### DeleteReleaseAsset

**描述：** 删除指定的 release 附件 the specified release asset.

**详细文档：** [DeleteReleaseAsset.md](./references/releases/deletereleaseasset.md)

---

#### GetLatestRelease

**描述：** 查询最新的 release。Query the latest release.

**详细文档：** [GetLatestRelease.md](./references/releases/getlatestrelease.md)

---

#### GetReleaseAsset

**描述：** 查询指定的 release 附件 the specified release asset.

**详细文档：** [GetReleaseAsset.md](./references/releases/getreleaseasset.md)

---

#### GetReleaseByID

**描述：** 根据 id	查询指定 release, 包含附件信息。Get a release by id, include assets information.

**详细文档：** [GetReleaseByID.md](./references/releases/getreleasebyid.md)

---

#### GetReleaseByTag

**描述：** 通过 tag 查询指定 release,包含附件信息。Get a release by tag, include assets information.

**详细文档：** [GetReleaseByTag.md](./references/releases/getreleasebytag.md)

---

#### GetReleasesAsset

**描述：** 发起一个获取 release 附件的请求， 302到有一定效期的下载地址。Get a request to fetch a release assets and returns 302 redirect to the assets URL with specific valid time.

**详细文档：** [GetReleasesAsset.md](./references/releases/getreleasesasset.md)

---

#### ListReleases

**描述：** 查询 release 列表。List releases.

**详细文档：** [ListReleases.md](./references/releases/listreleases.md)

---

#### PatchRelease

**描述：** 更新 release。Update a release.

**详细文档：** [PatchRelease.md](./references/releases/patchrelease.md)

---

#### PostRelease

**描述：** 新增一个 release。Create a release.

**详细文档：** [PostRelease.md](./references/releases/postrelease.md)

---

#### PostReleaseAssetUploadConfirmation

**描述：** 确认  release 附件上传完成。Confirm release asset upload.

**详细文档：** [PostReleaseAssetUploadConfirmation.md](./references/releases/postreleaseassetuploadconfirmation.md)

---

#### PostReleaseAssetUploadURL

**描述：** 新增一个 release 附件。Create a release asset.

**详细文档：** [PostReleaseAssetUploadURL.md](./references/releases/postreleaseassetuploadurl.md)

---

### repocontributor 服务

#### GetRepoContributorTrend

**描述：** 查询仓库贡献者前 100 名的详细趋势数据。Query detailed trend data for top 100 contributors of the repository.

**详细文档：** [GetRepoContributorTrend.md](./references/repocontributor/getrepocontributortrend.md)

---

### repolabels 服务

#### DeleteLabel

**描述：** 删除指定的仓库标签。Delete the specified repository label.

**详细文档：** [DeleteLabel.md](./references/repolabels/deletelabel.md)

---

#### ListLabels

**描述：** 查询仓库的标签列表。List repository labels.

**详细文档：** [ListLabels.md](./references/repolabels/listlabels.md)

---

#### PatchLabel

**描述：** 更新标签信息。Update label information.

**详细文档：** [PatchLabel.md](./references/repolabels/patchlabel.md)

---

#### PostLabel

**描述：** 创建一个 标签。Create a label.

**详细文档：** [PostLabel.md](./references/repolabels/postlabel.md)

---

### repositories 服务

#### ArchiveRepo

**描述：** 仓库归档。Archive a repository.

**详细文档：** [ArchiveRepo.md](./references/repositories/archiverepo.md)

---

#### CreateRepo

**描述：** 创建仓库。Create repositories.

**详细文档：** [CreateRepo.md](./references/repositories/createrepo.md)

---

#### DeleteRepo

**描述：** 删除指定仓库。Delete the specified repository.

**详细文档：** [DeleteRepo.md](./references/repositories/deleterepo.md)

---

#### GetByID

**描述：** 获取指定仓库信息。Get information for the specified repository.

**详细文档：** [GetByID.md](./references/repositories/getbyid.md)

---

#### GetGroupSubRepos

**描述：** 查询组织下访问用户有权限查看到仓库。List the repositories that the user has access to.

**详细文档：** [GetGroupSubRepos.md](./references/repositories/getgroupsubrepos.md)

---

#### GetPinnedRepoByGroup

**描述：** 获取指定组织的仓库墙列表。List the pinned repositories of a group.

**详细文档：** [GetPinnedRepoByGroup.md](./references/repositories/getpinnedrepobygroup.md)

---

#### GetPinnedRepoByID

**描述：** 获取指定用户的用户仓库墙。 Get a list of repositories that the specified user has pinned.

**详细文档：** [GetPinnedRepoByID.md](./references/repositories/getpinnedrepobyid.md)

---

#### GetRepos

**描述：** 获取当前用户拥有指定权限及其以上权限的仓库。List repositories owned by the current user with the specified permissions or higher.

**详细文档：** [GetRepos.md](./references/repositories/getrepos.md)

---

#### GetReposByUserName

**描述：** 获取指定用户有指定以上权限并且客人态可见的仓库。List repositories where the specified user has the specified permission level or higher and are visible to guests.

**详细文档：** [GetReposByUserName.md](./references/repositories/getreposbyusername.md)

---

#### ListForksRepos

**描述：** 获取指定仓库的 fork 列表。Get fork list for specified repository.

**详细文档：** [ListForksRepos.md](./references/repositories/listforksrepos.md)

---

#### SetPinnedRepoByGroup

**描述：** 更新指定组织仓库墙。Update the pinned repositories of a group.

**详细文档：** [SetPinnedRepoByGroup.md](./references/repositories/setpinnedrepobygroup.md)

---

#### SetRepoVisibility

**描述：** 改变仓库可见性。Update visibility of repository.

**详细文档：** [SetRepoVisibility.md](./references/repositories/setrepovisibility.md)

---

#### TransferRepo

**描述：** 转移仓库。Transfer a repository.

**详细文档：** [TransferRepo.md](./references/repositories/transferrepo.md)

---

#### UnArchiveRepo

**描述：** 解除仓库归档。Unarchive a repository.

**详细文档：** [UnArchiveRepo.md](./references/repositories/unarchiverepo.md)

---

#### UpdateRepo

**描述：** 更新仓库信息, 可更新的内容为: 仓库简介, 仓库站点, 仓库主题, 开源许可证。updates repository details including description, website URL,topics and license type.

**详细文档：** [UpdateRepo.md](./references/repositories/updaterepo.md)

---

### security 服务

#### GetRepoSecurityOverview

**描述：** 查询仓库安全模块概览数据。Query the security overview data of a repository

**详细文档：** [GetRepoSecurityOverview.md](./references/security/getreposecurityoverview.md)

---

### starring 服务

#### GetUserAllStaredRepos

**描述：** 获取当前用户 star 的仓库列表。List all stared repositories.

**详细文档：** [GetUserAllStaredRepos.md](./references/starring/getuserallstaredrepos.md)

---

#### GetUserStaredRepos

**描述：** 获取指定用户的 star 仓库列表。Get the list of repositories starred by the specified user.

**详细文档：** [GetUserStaredRepos.md](./references/starring/getuserstaredrepos.md)

---

#### ListStarUsers

**描述：** 获取指定仓库的star用户列表。Get the list of users who starred the specified repository.

**详细文档：** [ListStarUsers.md](./references/starring/liststarusers.md)

---

### users 服务

#### AutoCompleteSource

**描述：** 查询当前用户用户拥有指定权限的所有资源列表。List resources that the current user has specified permissions for.

**详细文档：** [AutoCompleteSource.md](./references/users/autocompletesource.md)

---

#### GetUserInfo

**描述：** 获取指定用户的详情信息。Get detailed information for a specified user.

**详细文档：** [GetUserInfo.md](./references/users/getuserinfo.md)

---

#### GetUserInfoByName

**描述：** 获取指定用户的详情信息。Get detailed information for a specified user.

**详细文档：** [GetUserInfoByName.md](./references/users/getuserinfobyname.md)

---

#### ListEmail

**描述：** 获取用户邮箱列表

**详细文档：** [ListEmail.md](./references/users/listemail.md)

---

#### ListGPGKeys

**描述：** 获取用户 GPG keys 列表。List GPG Keys.

**详细文档：** [ListGPGKeys.md](./references/users/listgpgkeys.md)

---

#### UpdateUserInfo

**描述：** 更新指定用户的详情信息。Updates the specified user's profile information.

**详细文档：** [UpdateUserInfo.md](./references/users/updateuserinfo.md)

---

### workspace 服务

#### DeleteWorkspace

**描述：** 删除我的云原生开发环境。Delete my workspace.

**详细文档：** [DeleteWorkspace.md](./references/workspace/deleteworkspace.md)

---

#### GetWorkspaceDetail

**描述：** 根据流水线sn查询云原生开发访问地址。Query cloud-native development access address by pipeline SN.

**详细文档：** [GetWorkspaceDetail.md](./references/workspace/getworkspacedetail.md)

---

#### ListWorkspaces

**描述：** 获取我的云原生开发环境列表。List my workspaces.

**详细文档：** [ListWorkspaces.md](./references/workspace/listworkspaces.md)

---

#### StartWorkspace

**描述：** 启动云原生开发环境，已存在环境则直接打开，否则重新创建开发环境。Start cloud-native dev. Opens existing env or creates a new one.

**详细文档：** [StartWorkspace.md](./references/workspace/startworkspace.md)

---

#### WorkspaceStop

**描述：** 停止/关闭我的云原生开发环境。Stop/close my workspace.

**详细文档：** [WorkspaceStop.md](./references/workspace/workspacestop.md)

---

## 使用指南

### 1. 获取访问令牌

在调用任何 API 之前，需要先获取有效的 CNB_TOKEN。

### 2. 构造请求

所有请求都需要包含以下基础头信息：

```
Accept: application/vnd.cnb.api+json
Authorization: Bearer $CNB_TOKEN
```

### 3. 处理响应

API 返回标准的 JSON 格式响应。请根据 HTTP 状态码判断请求是否成功：

- 200: 请求成功
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器内部错误

### 4. 错误处理

当请求失败时，响应体通常包含错误信息，请根据错误信息进行相应处理。

## 调用示例

### 基础 GET 请求示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/api/endpoint" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN"
```

### 带参数的 POST 请求示例

```bash
curl -X POST \
  "${CNB_API_ENDPOINT}/api/endpoint" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

## 注意事项

1. 所有 API 调用都需要有效的认证令牌
2. 请求和响应数据格式为 JSON
3. 请根据具体 API 文档中的参数要求构造请求
4. 建议在生产环境中添加适当的错误处理和重试机制

---

*本文档基于 Swagger 文件自动生成：https://api.cnb.cool/swagger.json*
