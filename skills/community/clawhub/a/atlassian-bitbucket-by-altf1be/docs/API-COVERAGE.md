# API Coverage — Bitbucket Cloud REST API 2.0

This document lists all 335 endpoints from the Bitbucket Cloud REST API 2.0, organized by tag, along with the corresponding CLI command names and implementation status.

---

## Addon (10 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 1 | DELETE | /addon | `addon-delete` | ✅ |
| 2 | PUT | /addon | `addon-update` | ✅ |
| 3 | GET | /addon/linkers | `addon-linkers` | ✅ |
| 4 | GET | /addon/linkers/{linker_key} | `addon-linker-get` | ✅ |
| 5 | DELETE | /addon/linkers/{linker_key}/values | `addon-linker-values-delete` | ✅ |
| 6 | GET | /addon/linkers/{linker_key}/values | `addon-linker-values` | ✅ |
| 7 | POST | /addon/linkers/{linker_key}/values | `addon-linker-value-create` | ✅ |
| 8 | PUT | /addon/linkers/{linker_key}/values | `addon-linker-value-update` | ✅ |
| 9 | DELETE | /addon/linkers/{linker_key}/values/{value_id} | `addon-linker-value-delete` | ✅ |
| 10 | GET | /addon/linkers/{linker_key}/values/{value_id} | `addon-linker-value-get` | ✅ |

## Branch restrictions (5 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 11 | GET | /repositories/{workspace}/{repo_slug}/branch-restrictions | `restriction-list` | ✅ |
| 12 | POST | /repositories/{workspace}/{repo_slug}/branch-restrictions | `restriction-create` | ✅ |
| 13 | DELETE | /repositories/{workspace}/{repo_slug}/branch-restrictions/{id} | `restriction-delete` | ✅ |
| 14 | GET | /repositories/{workspace}/{repo_slug}/branch-restrictions/{id} | `restriction-get` | ✅ |
| 15 | PUT | /repositories/{workspace}/{repo_slug}/branch-restrictions/{id} | `restriction-update` | ✅ |

## Branching model (7 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 16 | GET | /repositories/{workspace}/{repo_slug}/branching-model | `branching-model-get` | ✅ |
| 17 | GET | /repositories/{workspace}/{repo_slug}/branching-model/settings | `branching-model-settings-get` | ✅ |
| 18 | PUT | /repositories/{workspace}/{repo_slug}/branching-model/settings | `branching-model-settings-update` | ✅ |
| 19 | GET | /repositories/{workspace}/{repo_slug}/effective-branching-model | `branching-model-effective` | ✅ |
| 20 | GET | /workspaces/{workspace}/projects/{project_key}/branching-model | `project-branching-model-get` | ✅ |
| 21 | GET | /workspaces/{workspace}/projects/{project_key}/branching-model/settings | `project-branching-model-settings-get` | ✅ |
| 22 | PUT | /workspaces/{workspace}/projects/{project_key}/branching-model/settings | `project-branching-model-settings-update` | ✅ |

## Commit statuses (4 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 23 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses | `status-list` | ✅ |
| 24 | POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build | `status-create` | ✅ |
| 25 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build/{key} | `status-get` | ✅ |
| 26 | PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/statuses/build/{key} | `status-update` | ✅ |

## Commits (16 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 27 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit} | `commit-get` | ✅ |
| 28 | DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/approve | `commit-unapprove` | ✅ |
| 29 | POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/approve | `commit-approve` | ✅ |
| 30 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments | `commit-comments` | ✅ |
| 31 | POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments | `commit-comment-create` | ✅ |
| 32 | DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id} | `commit-comment-delete` | ✅ |
| 33 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id} | `commit-comment-get` | ✅ |
| 34 | PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/comments/{comment_id} | `commit-comment-update` | ✅ |
| 35 | GET | /repositories/{workspace}/{repo_slug}/commits | `commit-list` | ✅ |
| 36 | POST | /repositories/{workspace}/{repo_slug}/commits | `commit-list-post` | ✅ |
| 37 | GET | /repositories/{workspace}/{repo_slug}/commits/{revision} | `commit-list-revision` | ✅ |
| 38 | POST | /repositories/{workspace}/{repo_slug}/commits/{revision} | `commit-list-revision-post` | ✅ |
| 39 | GET | /repositories/{workspace}/{repo_slug}/diff/{spec} | `diff` | ✅ |
| 40 | GET | /repositories/{workspace}/{repo_slug}/diffstat/{spec} | `diffstat` | ✅ |
| 41 | GET | /repositories/{workspace}/{repo_slug}/merge-base/{revspec} | `merge-base` | ✅ |
| 42 | GET | /repositories/{workspace}/{repo_slug}/patch/{spec} | `patch` | ✅ |

## Deployments (16 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 43 | GET | /repositories/{workspace}/{repo_slug}/deploy-keys | `deploy-key-list` | ✅ |
| 44 | POST | /repositories/{workspace}/{repo_slug}/deploy-keys | `deploy-key-create` | ✅ |
| 45 | DELETE | /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id} | `deploy-key-delete` | ✅ |
| 46 | GET | /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id} | `deploy-key-get` | ✅ |
| 47 | PUT | /repositories/{workspace}/{repo_slug}/deploy-keys/{key_id} | `deploy-key-update` | ✅ |
| 48 | GET | /repositories/{workspace}/{repo_slug}/deployments | `deployment-list` | ✅ |
| 49 | GET | /repositories/{workspace}/{repo_slug}/deployments/{deployment_uuid} | `deployment-get` | ✅ |
| 50 | GET | /repositories/{workspace}/{repo_slug}/environments | `environment-list` | ✅ |
| 51 | POST | /repositories/{workspace}/{repo_slug}/environments | `environment-create` | ✅ |
| 52 | GET | /repositories/{workspace}/{repo_slug}/environments/{environment_uuid} | `environment-get` | ✅ |
| 53 | DELETE | /repositories/{workspace}/{repo_slug}/environments/{environment_uuid} | `environment-delete` | ✅ |
| 54 | POST | /repositories/{workspace}/{repo_slug}/environments/{environment_uuid}/changes | `environment-update` | ✅ |
| 55 | GET | /workspaces/{workspace}/projects/{project_key}/deploy-keys | `project-deploy-key-list` | ✅ |
| 56 | POST | /workspaces/{workspace}/projects/{project_key}/deploy-keys | `project-deploy-key-create` | ✅ |
| 57 | DELETE | /workspaces/{workspace}/projects/{project_key}/deploy-keys/{key_id} | `project-deploy-key-delete` | ✅ |
| 58 | GET | /workspaces/{workspace}/projects/{project_key}/deploy-keys/{key_id} | `project-deploy-key-get` | ✅ |

## Downloads (4 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 59 | GET | /repositories/{workspace}/{repo_slug}/downloads | `download-list` | ✅ |
| 60 | POST | /repositories/{workspace}/{repo_slug}/downloads | `download-upload` | ✅ |
| 61 | DELETE | /repositories/{workspace}/{repo_slug}/downloads/{filename} | `download-delete` | ✅ |
| 62 | GET | /repositories/{workspace}/{repo_slug}/downloads/{filename} | `download-get` | ✅ |

## GPG (4 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 63 | GET | /users/{selected_user}/gpg-keys | `gpg-key-list` | ✅ |
| 64 | POST | /users/{selected_user}/gpg-keys | `gpg-key-create` | ✅ |
| 65 | DELETE | /users/{selected_user}/gpg-keys/{fingerprint} | `gpg-key-delete` | ✅ |
| 66 | GET | /users/{selected_user}/gpg-keys/{fingerprint} | `gpg-key-get` | ✅ |

## Issue tracker (33 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 67 | GET | /repositories/{workspace}/{repo_slug}/components | `component-list` | ✅ |
| 68 | GET | /repositories/{workspace}/{repo_slug}/components/{component_id} | `component-get` | ✅ |
| 69 | GET | /repositories/{workspace}/{repo_slug}/issues | `issue-list` | ✅ |
| 70 | POST | /repositories/{workspace}/{repo_slug}/issues | `issue-create` | ✅ |
| 71 | DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id} | `issue-delete` | ✅ |
| 72 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id} | `issue-get` | ✅ |
| 73 | PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id} | `issue-update` | ✅ |
| 74 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments | `issue-attachment-list` | ✅ |
| 75 | POST | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments | `issue-attachment-upload` | ✅ |
| 76 | DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments/{path} | `issue-attachment-delete` | ✅ |
| 77 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/attachments/{path} | `issue-attachment-get` | ✅ |
| 78 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes | `issue-change-list` | ✅ |
| 79 | POST | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes | `issue-change-create` | ✅ |
| 80 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/changes/{change_id} | `issue-change-get` | ✅ |
| 81 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments | `issue-comment-list` | ✅ |
| 82 | POST | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments | `issue-comment-create` | ✅ |
| 83 | DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id} | `issue-comment-delete` | ✅ |
| 84 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id} | `issue-comment-get` | ✅ |
| 85 | PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/comments/{comment_id} | `issue-comment-update` | ✅ |
| 86 | DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote | `issue-unvote` | ✅ |
| 87 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote | `issue-vote-check` | ✅ |
| 88 | PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/vote | `issue-vote` | ✅ |
| 89 | DELETE | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch | `issue-unwatch` | ✅ |
| 90 | GET | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch | `issue-watch-check` | ✅ |
| 91 | PUT | /repositories/{workspace}/{repo_slug}/issues/{issue_id}/watch | `issue-watch` | ✅ |
| 92 | POST | /repositories/{workspace}/{repo_slug}/issues/export | `issue-export` | ✅ |
| 93 | GET | /repositories/{workspace}/{repo_slug}/issues/export/{repo_name}-issues-{task_id}.zip | `issue-export-status` | ✅ |
| 94 | GET | /repositories/{workspace}/{repo_slug}/issues/import | `issue-import-status` | ✅ |
| 95 | POST | /repositories/{workspace}/{repo_slug}/issues/import | `issue-import` | ✅ |
| 96 | GET | /repositories/{workspace}/{repo_slug}/milestones | `milestone-list` | ✅ |
| 97 | GET | /repositories/{workspace}/{repo_slug}/milestones/{milestone_id} | `milestone-get` | ✅ |
| 98 | GET | /repositories/{workspace}/{repo_slug}/versions | `version-list` | ✅ |
| 99 | GET | /repositories/{workspace}/{repo_slug}/versions/{version_id} | `version-get` | ✅ |

## Pipelines (68 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 100 | GET | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables | `env-var-list` | ✅ |
| 101 | POST | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables | `env-var-create` | ✅ |
| 102 | PUT | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables/{variable_uuid} | `env-var-update` | ✅ |
| 103 | DELETE | /repositories/{workspace}/{repo_slug}/deployments_config/environments/{environment_uuid}/variables/{variable_uuid} | `env-var-delete` | ✅ |
| 104 | GET | /repositories/{workspace}/{repo_slug}/pipelines | `pipeline-list` | ✅ |
| 105 | POST | /repositories/{workspace}/{repo_slug}/pipelines | `pipeline-create` | ✅ |
| 106 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config | `pipeline-config-get` | ✅ |
| 107 | PUT | /repositories/{workspace}/{repo_slug}/pipelines_config | `pipeline-config-update` | ✅ |
| 108 | PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/build_number | `pipeline-build-number-update` | ✅ |
| 109 | POST | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules | `pipeline-schedule-create` | ✅ |
| 110 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules | `pipeline-schedule-list` | ✅ |
| 111 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid} | `pipeline-schedule-get` | ✅ |
| 112 | PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid} | `pipeline-schedule-update` | ✅ |
| 113 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid} | `pipeline-schedule-delete` | ✅ |
| 114 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/schedules/{schedule_uuid}/executions | `pipeline-schedule-executions` | ✅ |
| 115 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair | `pipeline-ssh-keypair-get` | ✅ |
| 116 | PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair | `pipeline-ssh-keypair-update` | ✅ |
| 117 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/key_pair | `pipeline-ssh-keypair-delete` | ✅ |
| 118 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts | `pipeline-known-host-list` | ✅ |
| 119 | POST | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts | `pipeline-known-host-create` | ✅ |
| 120 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid} | `pipeline-known-host-get` | ✅ |
| 121 | PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid} | `pipeline-known-host-update` | ✅ |
| 122 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/ssh/known_hosts/{known_host_uuid} | `pipeline-known-host-delete` | ✅ |
| 123 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/variables | `pipeline-var-list` | ✅ |
| 124 | POST | /repositories/{workspace}/{repo_slug}/pipelines_config/variables | `pipeline-var-create` | ✅ |
| 125 | GET | /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid} | `pipeline-var-get` | ✅ |
| 126 | PUT | /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid} | `pipeline-var-update` | ✅ |
| 127 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines_config/variables/{variable_uuid} | `pipeline-var-delete` | ✅ |
| 128 | GET | /repositories/{workspace}/{repo_slug}/pipelines-config/caches | `pipeline-cache-list` | ✅ |
| 129 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines-config/caches | `pipeline-cache-delete` | ✅ |
| 130 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines-config/caches/{cache_uuid} | `pipeline-cache-delete-by-name` | ✅ |
| 131 | GET | /repositories/{workspace}/{repo_slug}/pipelines-config/caches/{cache_uuid}/content-uri | `pipeline-cache-content-uri` | ✅ |
| 132 | GET | /repositories/{workspace}/{repo_slug}/pipelines-config/runners | `pipeline-runner-list` | ✅ |
| 133 | POST | /repositories/{workspace}/{repo_slug}/pipelines-config/runners | `pipeline-runner-create` | ✅ |
| 134 | GET | /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid} | `pipeline-runner-get` | ✅ |
| 135 | PUT | /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid} | `pipeline-runner-update` | ✅ |
| 136 | DELETE | /repositories/{workspace}/{repo_slug}/pipelines-config/runners/{runner_uuid} | `pipeline-runner-delete` | ✅ |
| 137 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid} | `pipeline-get` | ✅ |
| 138 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps | `pipeline-steps` | ✅ |
| 139 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid} | `pipeline-step-get` | ✅ |
| 140 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/log | `pipeline-step-log` | ✅ |
| 141 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/logs/{log_uuid} | `pipeline-step-log-container` | ✅ |
| 142 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports | `pipeline-test-reports` | ✅ |
| 143 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports/test_cases | `pipeline-test-cases` | ✅ |
| 144 | GET | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/steps/{step_uuid}/test_reports/test_cases/{test_case_uuid}/test_case_reasons | `pipeline-test-case-reasons` | ✅ |
| 145 | POST | /repositories/{workspace}/{repo_slug}/pipelines/{pipeline_uuid}/stopPipeline | `pipeline-stop` | ✅ |
| 146 | GET | /teams/{username}/pipelines_config/variables | `team-pipeline-var-list` | ✅ |
| 147 | POST | /teams/{username}/pipelines_config/variables | `team-pipeline-var-create` | ✅ |
| 148 | GET | /teams/{username}/pipelines_config/variables/{variable_uuid} | `team-pipeline-var-get` | ✅ |
| 149 | PUT | /teams/{username}/pipelines_config/variables/{variable_uuid} | `team-pipeline-var-update` | ✅ |
| 150 | DELETE | /teams/{username}/pipelines_config/variables/{variable_uuid} | `team-pipeline-var-delete` | ✅ |
| 151 | GET | /users/{selected_user}/pipelines_config/variables | `user-pipeline-var-list` | ✅ |
| 152 | POST | /users/{selected_user}/pipelines_config/variables | `user-pipeline-var-create` | ✅ |
| 153 | GET | /users/{selected_user}/pipelines_config/variables/{variable_uuid} | `user-pipeline-var-get` | ✅ |
| 154 | PUT | /users/{selected_user}/pipelines_config/variables/{variable_uuid} | `user-pipeline-var-update` | ✅ |
| 155 | DELETE | /users/{selected_user}/pipelines_config/variables/{variable_uuid} | `user-pipeline-var-delete` | ✅ |
| 156 | GET | /workspaces/{workspace}/pipelines-config/identity/oidc/.well-known/openid-configuration | `ws-oidc-config` | ✅ |
| 157 | GET | /workspaces/{workspace}/pipelines-config/identity/oidc/keys.json | `ws-oidc-keys` | ✅ |
| 158 | GET | /workspaces/{workspace}/pipelines-config/runners | `ws-runner-list` | ✅ |
| 159 | POST | /workspaces/{workspace}/pipelines-config/runners | `ws-runner-create` | ✅ |
| 160 | GET | /workspaces/{workspace}/pipelines-config/runners/{runner_uuid} | `ws-runner-get` | ✅ |
| 161 | PUT | /workspaces/{workspace}/pipelines-config/runners/{runner_uuid} | `ws-runner-update` | ✅ |
| 162 | DELETE | /workspaces/{workspace}/pipelines-config/runners/{runner_uuid} | `ws-runner-delete` | ✅ |
| 163 | GET | /workspaces/{workspace}/pipelines-config/variables | `ws-pipeline-var-list` | ✅ |
| 164 | POST | /workspaces/{workspace}/pipelines-config/variables | `ws-pipeline-var-create` | ✅ |
| 165 | GET | /workspaces/{workspace}/pipelines-config/variables/{variable_uuid} | `ws-pipeline-var-get` | ✅ |
| 166 | PUT | /workspaces/{workspace}/pipelines-config/variables/{variable_uuid} | `ws-pipeline-var-update` | ✅ |
| 167 | DELETE | /workspaces/{workspace}/pipelines-config/variables/{variable_uuid} | `ws-pipeline-var-delete` | ✅ |

## Projects (16 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 168 | POST | /workspaces/{workspace}/projects | `project-create` | ✅ |
| 169 | DELETE | /workspaces/{workspace}/projects/{project_key} | `project-delete` | ✅ |
| 170 | GET | /workspaces/{workspace}/projects/{project_key} | `project-get` | ✅ |
| 171 | PUT | /workspaces/{workspace}/projects/{project_key} | `project-update` | ✅ |
| 172 | GET | /workspaces/{workspace}/projects/{project_key}/default-reviewers | `project-default-reviewer-list` | ✅ |
| 173 | DELETE | /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user} | `project-default-reviewer-delete` | ✅ |
| 174 | GET | /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user} | `project-default-reviewer-get` | ✅ |
| 175 | PUT | /workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user} | `project-default-reviewer-add` | ✅ |
| 176 | GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups | `project-group-permission-list` | ✅ |
| 177 | DELETE | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug} | `project-group-permission-delete` | ✅ |
| 178 | GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug} | `project-group-permission-get` | ✅ |
| 179 | PUT | /workspaces/{workspace}/projects/{project_key}/permissions-config/groups/{group_slug} | `project-group-permission-update` | ✅ |
| 180 | GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/users | `project-user-permission-list` | ✅ |
| 181 | DELETE | /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id} | `project-user-permission-delete` | ✅ |
| 182 | GET | /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id} | `project-user-permission-get` | ✅ |
| 183 | PUT | /workspaces/{workspace}/projects/{project_key}/permissions-config/users/{selected_user_id} | `project-user-permission-update` | ✅ |

## Pullrequests (36 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 184 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/pullrequests | `pr-for-commit` | ✅ |
| 185 | GET | /repositories/{workspace}/{repo_slug}/default-reviewers | `default-reviewer-list` | ✅ |
| 186 | DELETE | /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username} | `default-reviewer-delete` | ✅ |
| 187 | GET | /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username} | `default-reviewer-get` | ✅ |
| 188 | PUT | /repositories/{workspace}/{repo_slug}/default-reviewers/{target_username} | `default-reviewer-add` | ✅ |
| 189 | GET | /repositories/{workspace}/{repo_slug}/effective-default-reviewers | `effective-default-reviewers` | ✅ |
| 190 | GET | /repositories/{workspace}/{repo_slug}/pullrequests | `pr-list` | ✅ |
| 191 | POST | /repositories/{workspace}/{repo_slug}/pullrequests | `pr-create` | ✅ |
| 192 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id} | `pr-get` | ✅ |
| 193 | PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id} | `pr-update` | ✅ |
| 194 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/activity | `pr-activity` | ✅ |
| 195 | DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve | `pr-unapprove` | ✅ |
| 196 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve | `pr-approve` | ✅ |
| 197 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments | `pr-comments` | ✅ |
| 198 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments | `pr-comment-create` | ✅ |
| 199 | DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id} | `pr-comment-delete` | ✅ |
| 200 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id} | `pr-comment-get` | ✅ |
| 201 | PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id} | `pr-comment-update` | ✅ |
| 202 | DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}/resolve | `pr-comment-reopen` | ✅ |
| 203 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments/{comment_id}/resolve | `pr-comment-resolve` | ✅ |
| 204 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/commits | `pr-commits` | ✅ |
| 205 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/decline | `pr-decline` | ✅ |
| 206 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/diff | `pr-diff` | ✅ |
| 207 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/diffstat | `pr-diffstat` | ✅ |
| 208 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge | `pr-merge` | ✅ |
| 209 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge/task-status/{task_id} | `pr-merge-task-status` | ✅ |
| 210 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/patch | `pr-patch` | ✅ |
| 211 | DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes | `pr-unrequest-changes` | ✅ |
| 212 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes | `pr-request-changes` | ✅ |
| 213 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/statuses | `pr-statuses` | ✅ |
| 214 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks | `pr-tasks` | ✅ |
| 215 | POST | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks | `pr-task-create` | ✅ |
| 216 | DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id} | `pr-task-delete` | ✅ |
| 217 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id} | `pr-task-get` | ✅ |
| 218 | PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/tasks/{task_id} | `pr-task-update` | ✅ |
| 219 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/activity | `pr-activity-all` | ✅ |

## Refs (9 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 220 | GET | /repositories/{workspace}/{repo_slug}/refs | `ref-list` | ✅ |
| 221 | GET | /repositories/{workspace}/{repo_slug}/refs/branches | `branch-list` | ✅ |
| 222 | POST | /repositories/{workspace}/{repo_slug}/refs/branches | `branch-create` | ✅ |
| 223 | DELETE | /repositories/{workspace}/{repo_slug}/refs/branches/{name} | `branch-delete` | ✅ |
| 224 | GET | /repositories/{workspace}/{repo_slug}/refs/branches/{name} | `branch-get` | ✅ |
| 225 | GET | /repositories/{workspace}/{repo_slug}/refs/tags | `tag-list` | ✅ |
| 226 | POST | /repositories/{workspace}/{repo_slug}/refs/tags | `tag-create` | ✅ |
| 227 | DELETE | /repositories/{workspace}/{repo_slug}/refs/tags/{name} | `tag-delete` | ✅ |
| 228 | GET | /repositories/{workspace}/{repo_slug}/refs/tags/{name} | `tag-get` | ✅ |

## Reports (9 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 229 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports | `report-list` | ✅ |
| 230 | PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId} | `report-create` | ✅ |
| 231 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId} | `report-get` | ✅ |
| 232 | DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId} | `report-delete` | ✅ |
| 233 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations | `report-annotation-list` | ✅ |
| 234 | POST | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations | `report-annotation-bulk-create` | ✅ |
| 235 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId} | `report-annotation-get` | ✅ |
| 236 | PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId} | `report-annotation-create` | ✅ |
| 237 | DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/reports/{reportId}/annotations/{annotationId} | `report-annotation-delete` | ✅ |

## Repositories (26 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 238 | GET | /repositories | `repo-list-public` | ✅ |
| 239 | GET | /repositories/{workspace} | `repo-list` | ✅ |
| 240 | DELETE | /repositories/{workspace}/{repo_slug} | `repo-delete` | ✅ |
| 241 | GET | /repositories/{workspace}/{repo_slug} | `repo-get` | ✅ |
| 242 | POST | /repositories/{workspace}/{repo_slug} | `repo-create` | ✅ |
| 243 | PUT | /repositories/{workspace}/{repo_slug} | `repo-update` | ✅ |
| 244 | GET | /repositories/{workspace}/{repo_slug}/forks | `repo-forks` | ✅ |
| 245 | POST | /repositories/{workspace}/{repo_slug}/forks | `repo-fork-create` | ✅ |
| 246 | GET | /repositories/{workspace}/{repo_slug}/hooks | `hook-list` | ✅ |
| 247 | POST | /repositories/{workspace}/{repo_slug}/hooks | `hook-create` | ✅ |
| 248 | DELETE | /repositories/{workspace}/{repo_slug}/hooks/{uid} | `hook-delete` | ✅ |
| 249 | GET | /repositories/{workspace}/{repo_slug}/hooks/{uid} | `hook-get` | ✅ |
| 250 | PUT | /repositories/{workspace}/{repo_slug}/hooks/{uid} | `hook-update` | ✅ |
| 251 | GET | /repositories/{workspace}/{repo_slug}/override-settings | `repo-override-settings-get` | ✅ |
| 252 | PUT | /repositories/{workspace}/{repo_slug}/override-settings | `repo-override-settings-update` | ✅ |
| 253 | GET | /repositories/{workspace}/{repo_slug}/permissions-config/groups | `repo-group-permission-list` | ✅ |
| 254 | DELETE | /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug} | `repo-group-permission-delete` | ✅ |
| 255 | GET | /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug} | `repo-group-permission-get` | ✅ |
| 256 | PUT | /repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug} | `repo-group-permission-update` | ✅ |
| 257 | GET | /repositories/{workspace}/{repo_slug}/permissions-config/users | `repo-user-permission-list` | ✅ |
| 258 | DELETE | /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id} | `repo-user-permission-delete` | ✅ |
| 259 | GET | /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id} | `repo-user-permission-get` | ✅ |
| 260 | PUT | /repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id} | `repo-user-permission-update` | ✅ |
| 261 | GET | /repositories/{workspace}/{repo_slug}/watchers | `repo-watchers` | ✅ |
| 262 | GET | /user/permissions/repositories | `user-repo-permissions` | ✅ |
| 263 | GET | /user/workspaces/{workspace}/permissions/repositories | `user-ws-repo-permissions` | ✅ |

## Search (3 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 264 | GET | /teams/{username}/search/code | `search-team` | ✅ |
| 265 | GET | /users/{selected_user}/search/code | `search-account` | ✅ |
| 266 | GET | /workspaces/{workspace}/search/code | `search-code` | ✅ |

## Snippets (25 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 267 | GET | /snippets | `snippet-list` | ✅ |
| 268 | POST | /snippets | `snippet-create` | ✅ |
| 269 | GET | /snippets/{workspace} | `snippet-ws-list` | ✅ |
| 270 | POST | /snippets/{workspace} | `snippet-ws-create` | ✅ |
| 271 | DELETE | /snippets/{workspace}/{encoded_id} | `snippet-delete` | ✅ |
| 272 | GET | /snippets/{workspace}/{encoded_id} | `snippet-get` | ✅ |
| 273 | PUT | /snippets/{workspace}/{encoded_id} | `snippet-update` | ✅ |
| 274 | DELETE | /snippets/{workspace}/{encoded_id}/{node_id} | `snippet-revision-delete` | ✅ |
| 275 | GET | /snippets/{workspace}/{encoded_id}/{node_id} | `snippet-revision-get` | ✅ |
| 276 | PUT | /snippets/{workspace}/{encoded_id}/{node_id} | `snippet-revision-update` | ✅ |
| 277 | GET | /snippets/{workspace}/{encoded_id}/{node_id}/files/{path} | `snippet-file-revision` | ✅ |
| 278 | GET | /snippets/{workspace}/{encoded_id}/{revision}/diff | `snippet-diff` | ✅ |
| 279 | GET | /snippets/{workspace}/{encoded_id}/{revision}/patch | `snippet-patch` | ✅ |
| 280 | GET | /snippets/{workspace}/{encoded_id}/comments | `snippet-comment-list` | ✅ |
| 281 | POST | /snippets/{workspace}/{encoded_id}/comments | `snippet-comment-create` | ✅ |
| 282 | DELETE | /snippets/{workspace}/{encoded_id}/comments/{comment_id} | `snippet-comment-delete` | ✅ |
| 283 | GET | /snippets/{workspace}/{encoded_id}/comments/{comment_id} | `snippet-comment-get` | ✅ |
| 284 | PUT | /snippets/{workspace}/{encoded_id}/comments/{comment_id} | `snippet-comment-update` | ✅ |
| 285 | GET | /snippets/{workspace}/{encoded_id}/commits | `snippet-commit-list` | ✅ |
| 286 | GET | /snippets/{workspace}/{encoded_id}/commits/{revision} | `snippet-commit-get` | ✅ |
| 287 | GET | /snippets/{workspace}/{encoded_id}/files/{path} | `snippet-file` | ✅ |
| 288 | DELETE | /snippets/{workspace}/{encoded_id}/watch | `snippet-unwatch` | ✅ |
| 289 | GET | /snippets/{workspace}/{encoded_id}/watch | `snippet-watch-check` | ✅ |
| 290 | PUT | /snippets/{workspace}/{encoded_id}/watch | `snippet-watch` | ✅ |
| 291 | GET | /snippets/{workspace}/{encoded_id}/watchers | `snippet-watchers` | ✅ |

## Source (4 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 292 | GET | /repositories/{workspace}/{repo_slug}/filehistory/{commit}/{path} | `src-history` | ✅ |
| 293 | GET | /repositories/{workspace}/{repo_slug}/src | `src-root` | ✅ |
| 294 | POST | /repositories/{workspace}/{repo_slug}/src | `src-create` | ✅ |
| 295 | GET | /repositories/{workspace}/{repo_slug}/src/{commit}/{path} | `src-get` | ✅ |

## SSH (5 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 296 | GET | /users/{selected_user}/ssh-keys | `ssh-key-list` | ✅ |
| 297 | POST | /users/{selected_user}/ssh-keys | `ssh-key-create` | ✅ |
| 298 | DELETE | /users/{selected_user}/ssh-keys/{key_id} | `ssh-key-delete` | ✅ |
| 299 | GET | /users/{selected_user}/ssh-keys/{key_id} | `ssh-key-get` | ✅ |
| 300 | PUT | /users/{selected_user}/ssh-keys/{key_id} | `ssh-key-update` | ✅ |

## Users (4 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 301 | GET | /user | `user-get-current` | ✅ |
| 302 | GET | /user/emails | `user-emails` | ✅ |
| 303 | GET | /user/emails/{email} | `user-email-get` | ✅ |
| 304 | GET | /users/{selected_user} | `user-get` | ✅ |

## Webhooks (2 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 305 | GET | /hook_events | `webhook-events` | ✅ |
| 306 | GET | /hook_events/{subject_type} | `webhook-event-types` | ✅ |

## Workspaces (17 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 307 | GET | /user/permissions/workspaces | `workspace-permissions-for-user` | ✅ |
| 308 | GET | /user/workspaces | `workspace-list-for-user` | ✅ |
| 309 | GET | /user/workspaces/{workspace}/permission | `workspace-user-permission` | ✅ |
| 310 | GET | /workspaces | `workspace-list` | ✅ |
| 311 | GET | /workspaces/{workspace} | `workspace-get` | ✅ |
| 312 | GET | /workspaces/{workspace}/hooks | `workspace-hook-list` | ✅ |
| 313 | POST | /workspaces/{workspace}/hooks | `workspace-hook-create` | ✅ |
| 314 | DELETE | /workspaces/{workspace}/hooks/{uid} | `workspace-hook-delete` | ✅ |
| 315 | GET | /workspaces/{workspace}/hooks/{uid} | `workspace-hook-get` | ✅ |
| 316 | PUT | /workspaces/{workspace}/hooks/{uid} | `workspace-hook-update` | ✅ |
| 317 | GET | /workspaces/{workspace}/members | `workspace-member-list` | ✅ |
| 318 | GET | /workspaces/{workspace}/members/{member} | `workspace-member-get` | ✅ |
| 319 | GET | /workspaces/{workspace}/permissions | `workspace-permission-list` | ✅ |
| 320 | GET | /workspaces/{workspace}/permissions/repositories | `workspace-repo-permissions` | ✅ |
| 321 | GET | /workspaces/{workspace}/permissions/repositories/{repo_slug} | `workspace-repo-permission-get` | ✅ |
| 322 | GET | /workspaces/{workspace}/projects | `workspace-project-list` | ✅ |
| 323 | GET | /workspaces/{workspace}/pullrequests/{selected_user} | `workspace-user-prs` | ✅ |

## properties (12 endpoints)

| # | Method | API Path | CLI Command | Status |
|---|--------|----------|-------------|--------|
| 324 | PUT | /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name} | `commit-property-update` | ✅ |
| 325 | DELETE | /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name} | `commit-property-delete` | ✅ |
| 326 | GET | /repositories/{workspace}/{repo_slug}/commit/{commit}/properties/{app_key}/{property_name} | `commit-property-get` | ✅ |
| 327 | PUT | /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name} | `repo-property-update` | ✅ |
| 328 | DELETE | /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name} | `repo-property-delete` | ✅ |
| 329 | GET | /repositories/{workspace}/{repo_slug}/properties/{app_key}/{property_name} | `repo-property-get` | ✅ |
| 330 | PUT | /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name} | `pr-property-update` | ✅ |
| 331 | DELETE | /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name} | `pr-property-delete` | ✅ |
| 332 | GET | /repositories/{workspace}/{repo_slug}/pullrequests/{pullrequest_id}/properties/{app_key}/{property_name} | `pr-property-get` | ✅ |
| 333 | PUT | /users/{selected_user}/properties/{app_key}/{property_name} | `user-property-update` | ✅ |
| 334 | DELETE | /users/{selected_user}/properties/{app_key}/{property_name} | `user-property-delete` | ✅ |
| 335 | GET | /users/{selected_user}/properties/{app_key}/{property_name} | `user-property-get` | ✅ |

---

## Summary

| Metric | Value |
|--------|-------|
| **Total endpoints** | 335 |
| **Covered** | 335/335 (100%) |

*Based on Bitbucket Cloud REST API 2.0 specification*
*Last updated: 2026-03-31*
