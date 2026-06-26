<!--
文件：SECURITY.md
核心功能：说明 DaE 技能包的安全边界、数据处理方式与平台提交时可直接复用的安全声明。
输入：DaE 当前功能范围、文件输出范围与平台安全关注点。
输出：可用于仓库与平台提审的安全说明。
-->

# Security Notes

## What DaE does

DaE runs a structured elicitation dialogue and outputs a reusable profile asset such as:

- `.dae_profile.md`
- `.dae_profile.json`

## What DaE does not do

- no hidden network calls by design
- no credential harvesting
- no unrelated file-system scanning
- no shell execution requirement
- no privilege escalation
- no binary payloads

## Data handling model

- user profile data should be treated as a local private configuration asset
- public demos should only use historical or non-sensitive benchmark subjects
- private user profiles should not be published into public repositories

## Trust statement for submission

DaE is a profiling and context-generation skill.
Its intended function is local context preparation for downstream agents.
It does not require elevated privileges and should be reviewable as plain text.
